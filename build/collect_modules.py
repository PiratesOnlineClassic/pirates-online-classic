#!/usr/bin/env python3
"""Work out which game modules the compiled client must contain.

Nuitka follows ordinary ``import`` statements by itself, but this client
loads a lot of code by name at run time, which Nuitka cannot see:

* The dc files (astron/dclass/*.dc) list distributed classes as
  ``from pirates.ship import DistributedShip/AI/UD/OV``.  The client's
  repository (direct.distributed.ConnectionRepository.readDCFile) calls
  ``__import__`` on the base name of every import line, and on the ``OV``
  variant of every line that lists ``OV``.  A missing module is fatal.
* pirates.world.WorldCreatorBase.openFile loads island/interior data with
  ``__import__('pirates.leveleditor.worldData.' + name)``.
* PLocalizer and OTPLocalizer ``exec`` ``from <language module> import *``.
* Panda3D's ShowBase hides a few imports from freezers on purpose
  (importlib.import_module), e.g. the particle and physics managers.

This script parses the dc files and the source tree and prints the list of
modules to pass to Nuitka.  nuitka_build.py imports it, so the build always
uses the current dc files; run it by hand to inspect or check the list:

    python build/collect_modules.py                 # summary
    python build/collect_modules.py --flags         # Nuitka flags
    python build/collect_modules.py --json          # everything, as JSON
    python build/collect_modules.py --check-imports --python /path/to/python

It only reads files.  --check-imports imports every listed module, each in
its own subprocess with a timeout, using the given Python (one that has
panda3d installed), and reports the ones that fail.
"""

import argparse
import ast
import importlib.util
import json
import os
import re
import subprocess
import sys
import sysconfig
from concurrent.futures import ThreadPoolExecutor

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BUILD_DIR)

# Game packages that live in the repository.  libotp is gitignored and is
# normally a symlink to a checkout of the nametag code; it is real client code.
LOCAL_PACKAGES = ('pirates', 'otp', 'libotp', 'libpirates')

DC_FILES = ('astron/dclass/otp.dc', 'astron/dclass/pirates.dc')

ENTRY_MODULE = 'pirates.piratesbase.PiratesStart'

# Loaded as a whole package by name (WorldCreatorBase.openFile).  It is about
# 20 MB of dict literals, so nuitka_build.py includes it as bytecode instead
# of compiling it to C.
WORLD_DATA_PACKAGE = 'pirates.leveleditor.worldData'

# The two worldData helpers exec a module named on the command line; they are
# level editor tools, not client code.
WORLD_DATA_SKIP = (
    'pirates.leveleditor.worldData.dataToText',
    'pirates.leveleditor.worldData.dataToText_1',
)

# Language modules PLocalizer/OTPLocalizer pick with exec() from the
# "language" prc variable.  Every language file present is included.
LOCALIZER_PATTERNS = (
    ('pirates/piratesbase', re.compile(r'^(PLocalizer|PQuestStrings|PGreetingStrings)[A-Z_]\w*\.py$')),
    ('otp/otpbase', re.compile(r'^OTPLocalizer[A-Z_]\w*\.py$')),
)

# Panda3D modules that are imported by name at run time, with the reason.
DIRECT_DYNAMIC = {
    'direct.particles.ParticleManagerGlobal': 'ShowBase.enableParticles importlib (PiratesBase enables particles)',
    'direct.showbase.PhysicsManagerGlobal': 'ShowBase.enableParticles importlib',
    'panda3d.physics': 'ShowBase.enableParticles importlib; ParticleEffect .ptf files',
    'direct.distributed.ClockDelta': 'PythonUtil importlib',
    'direct.showbase.ProfileSession': 'Task manager profiling, importlib',
    'direct.task.FrameProfiler': 'Task manager profiling, importlib',
    'direct.task.TaskProfiler': 'Task manager profiling, importlib',
}

# Anything else that is loaded by name and that the scan cannot find.
EXTRA_DYNAMIC = {
}

# Dev-only tools Panda or the game import lazily.  They need tkinter/Pmw/wx,
# which a release does not ship.  nuitka_build.py passes these to
# --nofollow-import-to, so the import fails (ImportError) only if a player
# turns on a dev setting that uses them.
DEV_ONLY_NOFOLLOW = (
    'tkinter',
    '_tkinter',
    'Pmw',
    'wx',
    'direct.tkpanels',
    'direct.tkwidgets',
    'direct.directtools',
    'direct.directdevices',
    'direct.leveleditor',
    'direct.wxwidgets',
    'direct.cluster',
    'direct.dist',
    'direct.p3d',
    'pytest',
    # The game's own Tk dev panels, behind want-water-panel and dev hotkeys.
    'pirates.seapatch.WaterPanel',
    'pirates.seapatch.SeaPatchPanel',
    'pirates.leveleditor.TimeOfDayPanel',
)

# Module name endings that mark server (AI / UberDOG) code.
SERVER_SUFFIXES = ('AI', 'UD')

# Server entry points, used to tell server-only modules apart.
SERVER_ROOTS = (
    'pirates.ai.ServiceStart',
    'pirates.uberdog.ServiceStart',
)

STDLIB = set(getattr(sys, 'stdlib_module_names', ())) or None


# ---------------------------------------------------------------- source tree

def find_local_modules(root=REPO_ROOT):
    """Return {module name: file path} for every .py file in the game packages."""
    modules = {}
    for package in LOCAL_PACKAGES:
        top = os.path.join(root, package)
        if not os.path.isdir(top):
            continue
        # libotp is usually a symlink; walk its real path but do not follow
        # symlinks below it (a stray libotp/libotp -> libotp link would loop).
        real_top = os.path.realpath(top)
        for dirpath, dirnames, filenames in os.walk(real_top, followlinks=False):
            dirnames[:] = sorted(
                d for d in dirnames
                if d != '__pycache__'
                and not os.path.islink(os.path.join(dirpath, d))
                and os.path.exists(os.path.join(dirpath, d, '__init__.py'))
            )
            rel = os.path.relpath(dirpath, real_top)
            parts = [package] + ([] if rel == '.' else rel.split(os.sep))
            for filename in sorted(filenames):
                if not filename.endswith('.py'):
                    continue
                path = os.path.join(dirpath, filename)
                if os.path.islink(path):
                    continue
                if filename == '__init__.py':
                    name = '.'.join(parts)
                else:
                    name = '.'.join(parts + [filename[:-3]])
                modules[name] = path
    return modules


def is_package(name, modules):
    path = modules.get(name)
    return path is not None and os.path.basename(path) == '__init__.py'


def parse_imports(name, path, modules):
    """Return (local modules imported, top-level external names) for one file.

    Every import statement counts, including ones inside functions and
    try/except blocks: Nuitka follows those too.
    """
    with open(path, 'rb') as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as e:
        return set(), set(), 'syntax error: %s' % e

    package = name if is_package(name, modules) else name.rpartition('.')[0]
    local, external = set(), set()

    def add(target):
        if not target:
            return
        top = target.split('.')[0]
        if top in LOCAL_PACKAGES:
            # Add the module and every parent package.
            parts = target.split('.')
            for i in range(1, len(parts) + 1):
                candidate = '.'.join(parts[:i])
                if candidate in modules:
                    local.add(candidate)
        else:
            external.add(target)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = package.split('.')
                if node.level > 1:
                    base = base[:-(node.level - 1)]
                base = '.'.join(base)
                target = base + ('.' + node.module if node.module else '')
            else:
                target = node.module or ''
            add(target)
            # "from pkg import name" imports pkg.name when it is a submodule.
            for alias in node.names:
                if alias.name != '*' and (target + '.' + alias.name) in modules:
                    add(target + '.' + alias.name)
    return local, external, None


def build_graph(modules):
    graph, externals, errors = {}, {}, {}
    for name, path in modules.items():
        local, external, error = parse_imports(name, path, modules)
        graph[name] = local
        externals[name] = external
        if error:
            errors[name] = error
    return graph, externals, errors


def closure(roots, graph):
    seen, stack = set(), [r for r in roots if r in graph]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        # Importing a.b.c runs a/__init__ and a/b/__init__ first.
        parts = name.split('.')
        for i in range(1, len(parts)):
            parent = '.'.join(parts[:i])
            if parent in graph and parent not in seen:
                stack.append(parent)
        stack.extend(graph.get(name, ()) - seen)
    return seen


# ------------------------------------------------------------------- dc files

DC_IMPORT_RE = re.compile(r'^\s*from\s+([\w./]+)\s+import\s+(.+?)\s*;?\s*$')
DC_PLAIN_IMPORT_RE = re.compile(r'^\s*import\s+([\w./]+)\s*;?\s*$')


def parse_dc_imports(root=REPO_ROOT):
    """Return [(dc file, line number, module, [(symbol, [suffixes])])]."""
    entries = []
    for dc in DC_FILES:
        path = os.path.join(root, dc)
        with open(path, encoding='utf-8', errors='replace') as f:
            for lineno, line in enumerate(f, 1):
                line = line.split('//')[0].rstrip()
                m = DC_IMPORT_RE.match(line)
                if m:
                    module = m.group(1)
                    symbols = []
                    for sym in m.group(2).split(','):
                        sym = sym.strip()
                        if sym:
                            parts = sym.split('/')
                            symbols.append((parts[0], parts[1:]))
                    entries.append((dc, lineno, module, symbols))
                    continue
                m = DC_PLAIN_IMPORT_RE.match(line)
                if m:
                    entries.append((dc, lineno, m.group(1), []))
    return entries


def dc_client_modules(entries, modules):
    """Modules the client repository imports for the dc files.

    The client's dcSuffix is '' and it has owner views, so it imports
    <module>.<Symbol> for every symbol and <module>.<Symbol>OV for symbols
    tagged /OV (ConnectionRepository.readDCFile).
    """
    wanted = {}
    for dc, lineno, module, symbols in entries:
        mod_parts = module.split('/')
        base_module = mod_parts[0]
        where = '%s:%d' % (dc, lineno)
        if not symbols:
            wanted.setdefault(base_module, where)
            continue
        wanted.setdefault(base_module, where)
        for symbol, suffixes in symbols:
            names = [symbol]
            if 'OV' in suffixes:
                names.append(symbol + 'OV')
            for sym in names:
                candidate = base_module + '.' + sym
                # "from pkg import Name": Name is usually a submodule; if not,
                # it is an attribute of pkg itself, which is already wanted.
                if candidate in modules or candidate.split('.')[0] not in LOCAL_PACKAGES:
                    wanted.setdefault(candidate, where)
                else:
                    wanted.setdefault(candidate, where + ' (MISSING)')
    return wanted


# --------------------------------------------------------------------- report

def is_server_name(name):
    last = name.rsplit('.', 1)[-1]
    # CrewHUD is a client HUD, not UberDOG code.
    return last.endswith(SERVER_SUFFIXES) and not last.endswith('HUD')


def is_stdlib(top):
    """True if a top-level module name belongs to the running Python's stdlib."""
    if STDLIB is not None:
        return top in STDLIB
    if top in sys.builtin_module_names:
        return True
    try:
        spec = importlib.util.find_spec(top)
    except (ImportError, ValueError):
        return False
    if spec is None:
        # Not importable here: Windows-only modules such as winreg.
        return top in ('winreg', 'winsound', 'msvcrt', '_winapi', 'nt')
    origin = spec.origin or ''
    if origin in ('built-in', 'frozen'):
        return True
    stdlib = os.path.normcase(sysconfig.get_paths()['stdlib'])
    platstdlib = os.path.normcase(sysconfig.get_paths()['platstdlib'])
    origin = os.path.normcase(os.path.realpath(origin))
    in_std = origin.startswith((os.path.realpath(stdlib), os.path.realpath(platstdlib)))
    return in_std and 'site-packages' not in origin


def external_top(name):
    return name.split('.')[0]


def collect(root=REPO_ROOT):
    modules = find_local_modules(root)
    graph, externals, errors = build_graph(modules)

    dc_entries = parse_dc_imports(root)
    dc_wanted = dc_client_modules(dc_entries, modules)
    dc_missing = sorted(m for m, why in dc_wanted.items() if why.endswith('(MISSING)'))
    dc_local = sorted(m for m in dc_wanted if m in modules)
    dc_direct = sorted(m for m in dc_wanted if m.split('.')[0] not in LOCAL_PACKAGES)

    world_data = sorted(
        m for m in modules
        if m.startswith(WORLD_DATA_PACKAGE + '.') and m not in WORLD_DATA_SKIP
    )

    localizers = []
    for subdir, pattern in LOCALIZER_PATTERNS:
        directory = os.path.join(root, subdir)
        for filename in sorted(os.listdir(directory)):
            if pattern.match(filename):
                localizers.append(subdir.replace('/', '.') + '.' + filename[:-3])

    roots = [ENTRY_MODULE] + dc_local + localizers + list(EXTRA_DYNAMIC)
    # worldData modules import only panda3d.core; keep them out of the
    # closure walk so the report stays readable.
    client = closure(roots, graph)
    client_with_world = client | set(world_data) | closure([WORLD_DATA_PACKAGE], graph)

    server = closure(SERVER_ROOTS, graph)
    all_server_named = sorted(m for m in modules if is_server_name(m))
    server_in_client = sorted(m for m in client if is_server_name(m))
    excluded = sorted(
        m for m in modules
        if m not in client_with_world and (is_server_name(m) or m in server)
    )
    unused = sorted(
        m for m in modules
        if m not in client_with_world and m not in excluded and m not in WORLD_DATA_SKIP
    )

    # Who pulls a server-named module into the client?
    pulled_by = {}
    for m in server_in_client:
        pulled_by[m] = sorted(src for src in client if m in graph.get(src, ()))

    ext = {}
    for m in client:
        for e in externals.get(m, ()):
            ext.setdefault(external_top(e), set()).add(m)
    third_party = {
        k: sorted(v) for k, v in ext.items()
        if k not in ('panda3d', 'direct', 'pandac', '__future__')
        and not is_stdlib(k)
    }
    stdlib_used = sorted(k for k in ext if is_stdlib(k))
    direct_static = sorted({e for m in client for e in externals.get(m, ()) if external_top(e) in ('direct', 'panda3d')})

    include_modules = sorted(set(dc_local) | set(dc_direct) | set(localizers)
                             | set(DIRECT_DYNAMIC) | set(EXTRA_DYNAMIC))

    return {
        'repo_root': root,
        'entry_module': ENTRY_MODULE,
        'include_modules': include_modules,
        'include_packages': [WORLD_DATA_PACKAGE],
        'bytecode_packages': [WORLD_DATA_PACKAGE],
        'nofollow': list(DEV_ONLY_NOFOLLOW) + list(WORLD_DATA_SKIP),
        'dc_client_modules': dc_local,
        'dc_direct_modules': dc_direct,
        'dc_missing_modules': dc_missing,
        'localizer_modules': localizers,
        'direct_dynamic': DIRECT_DYNAMIC,
        'extra_dynamic': EXTRA_DYNAMIC,
        'world_data_modules': world_data,
        'client_closure': sorted(client),
        'server_named_in_client': pulled_by,
        'excluded_server_modules': excluded,
        'unreferenced_modules': unused,
        'third_party_imports': third_party,
        'stdlib_imports': stdlib_used,
        'panda_static_imports': direct_static,
        'syntax_errors': errors,
        'counts': {
            'local_modules': len(modules),
            'client_closure': len(client),
            'world_data': len(world_data),
            'server_named_total': len(all_server_named),
            'excluded_server': len(excluded),
            'unreferenced': len(unused),
        },
    }


def nuitka_flags(info):
    flags = []
    for m in info['include_modules']:
        flags.append('--include-module=' + m)
    for p in info['include_packages']:
        flags.append('--include-package=' + p)
    for p in info['bytecode_packages']:
        flags.append('--noinclude-custom-mode=%s:bytecode' % p)
    for m in info['nofollow']:
        flags.append('--nofollow-import-to=' + m)
    return flags


# -------------------------------------------------------------- import check

CHECK_PRELUDE = r'''
import builtins, os, sys
sys.path.insert(0, os.getcwd())
from panda3d.core import loadPrcFile, loadPrcFileData
for prc in ('config/general.prc', 'config/dev.prc', 'config/performance.prc'):
    loadPrcFile(prc)
loadPrcFileData('', 'window-type none\naudio-library-name null\nwant-discord-rich-presence #f')
class game:
    name = 'pirates'
    process = 'client'
builtins.game = game()
# The client imports dc classes after ShowBase has set its builtins
# (base, config, directNotify, ...), so do the same without a window.
from direct.showbase.ShowBase import ShowBase
ShowBase()
import importlib
# PiratesStart imports these before the repository reads the dc files;
# importing a dc module on its own can hit an import cycle the real start
# order never does.
if len(sys.argv) > 2 and sys.argv[2] == 'warm':
    from pirates.launcher.PiratesDummyLauncher import PiratesDummyLauncher
    builtins.launcher = PiratesDummyLauncher()
    for warm in ('pirates.piratesbase.PiratesGlobals', 'pirates.piratesbase.PiratesBase',
                 'pirates.distributed.PiratesClientRepository'):
        importlib.import_module(warm)
importlib.import_module(sys.argv[1])
'''

ERROR_LINE_RE = re.compile(r'^(\w+(\.\w+)*(Error|Exception|Exit)|AssertionError|KeyboardInterrupt)\b')


def check_one(python, module, cwd, timeout, warm=True):
    try:
        proc = subprocess.run(
            [python, '-c', CHECK_PRELUDE, module] + (['warm'] if warm else []), cwd=cwd, timeout=timeout,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    except subprocess.TimeoutExpired:
        return module, 'timeout', ''
    if proc.returncode == 0:
        return module, 'ok', ''
    out = [l for l in proc.stdout.decode('utf-8', 'replace').splitlines() if l.strip()]
    errors = [l for l in out if ERROR_LINE_RE.match(l.strip())]
    detail = (errors or out or ['exit code %d' % proc.returncode])[-1].strip()
    return module, 'fail', detail


def make_check_stage(root, resources_dir):
    """Lay the tree out like a release: <stage>/game (cwd) next to <stage>/resources.

    The client reads some files from the hardcoded relative path
    ../resources/phase_N/etc, so the check runs from a directory whose
    parent holds the resources.  Uses symlinks; nothing is copied.
    """
    import tempfile
    stage = tempfile.mkdtemp(prefix='poc-import-check-')
    game = os.path.join(stage, 'game')
    os.mkdir(game)
    for name in LOCAL_PACKAGES + ('config', 'astron'):
        src = os.path.realpath(os.path.join(root, name))
        if os.path.exists(src):
            os.symlink(src, os.path.join(game, name))
    os.symlink(os.path.realpath(resources_dir), os.path.join(stage, 'resources'))
    return game


def check_imports(info, python, timeout, jobs, modules, resources_dir=None):
    modules = sorted(set(modules))
    cwd = info['repo_root']
    if resources_dir:
        cwd = make_check_stage(info['repo_root'], resources_dir)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda m: check_one(python, m, cwd, timeout), modules))
    return results


# ----------------------------------------------------------------------- main

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--flags', action='store_true', help='print the Nuitka flags, one per line')
    parser.add_argument('--json', action='store_true', help='print everything as JSON')
    parser.add_argument('--check-imports', action='store_true',
                        help='import each listed module in a subprocess and report failures')
    parser.add_argument('--python', default=sys.executable, help='Python with panda3d for --check-imports')
    parser.add_argument('--timeout', type=float, default=60.0, help='seconds per module for --check-imports')
    parser.add_argument('--jobs', type=int, default=os.cpu_count() or 4)
    parser.add_argument('--world-data', action='store_true', help='also import-check every worldData module')
    parser.add_argument('--resources-dir', default=None,
                        help='resources checkout for --check-imports (default: ../resources next to the repo, if present)')
    args = parser.parse_args(argv)

    info = collect()

    if args.json:
        print(json.dumps(info, indent=2, sort_keys=True))
        return 0
    if args.flags:
        print('\n'.join(nuitka_flags(info)))
        return 0

    c = info['counts']
    print('Game modules in tree:        %d' % c['local_modules'])
    print('Client closure (static+dyn): %d' % c['client_closure'])
    print('  dc client modules:         %d' % len(info['dc_client_modules']))
    print('  dc panda modules:          %s' % ', '.join(info['dc_direct_modules']))
    print('  localizer modules:         %s' % ', '.join(info['localizer_modules']))
    print('  panda dynamic imports:     %s' % ', '.join(info['direct_dynamic']))
    print('worldData modules (bytecode): %d' % c['world_data'])
    print('Server modules excluded:     %d' % c['excluded_server'])
    print('Unreferenced modules:        %d (not reached from the client; Nuitka leaves them out)' % c['unreferenced'])
    print('Third-party imports reached by the client:')
    for k, v in sorted(info['third_party_imports'].items()):
        print('  %-12s %s' % (k, ', '.join(v)))
    if info['dc_missing_modules']:
        print('dc imports with no module in the tree (the client will fail to load them):')
        for m in info['dc_missing_modules']:
            print('  ' + m)
    if info['server_named_in_client']:
        print('AI/UD-named modules the client code imports (they get compiled in):')
        for m, srcs in info['server_named_in_client'].items():
            print('  %s  <- %s' % (m, ', '.join(srcs[:4]) + (' ...' if len(srcs) > 4 else '')))
    if info['syntax_errors']:
        print('Files that do not parse:')
        for m, e in sorted(info['syntax_errors'].items()):
            print('  %s: %s' % (m, e))

    if args.check_imports:
        mods = info['include_modules'] + info['dc_client_modules']
        if args.world_data:
            mods += info['world_data_modules']
        print('\nImport check with %s (%d modules, %ds timeout each)...' % (args.python, len(set(mods)), args.timeout))
        resources = args.resources_dir or os.path.join(os.path.dirname(REPO_ROOT), 'resources')
        if not os.path.isdir(resources):
            print('warning: no resources dir at %s; modules that read phase files will fail' % resources)
            resources = None
        results = check_imports(info, args.python, args.timeout, args.jobs, mods, resources)
        bad = [r for r in results if r[1] != 'ok']
        for module, status, detail in bad:
            print('  %-7s %s: %s' % (status.upper(), module, detail))
        print('%d ok, %d failed' % (len(results) - len(bad), len(bad)))
        return 1 if bad else 0
    return 0


if __name__ == '__main__':
    sys.exit(main())

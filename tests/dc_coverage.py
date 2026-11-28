#!/usr/bin/env python
"""Coverage audit of the network protocol in astron/dclass against the code.

Parses otp.dc and pirates.dc with panda3d.direct.DCFile and, using the dc
import lines (``from x import Name/AI/UD/OV``), checks every dclass and every
field:

  missing-handler   an airecv field whose receiving server class (the AI
                    class, or the UD class for UberDOG objects) has no method
                    of that name anywhere in its MRO. Updates to it are
                    dropped by the server (or crash when sent server-side).
  missing-getter    a required field whose AI class has no getter (``setX`` ->
                    ``getX``). generateWithRequired packs required fields by
                    calling their getters, so the generate raises.
  never-sent        a field the client class handles (has a method) that can
                    only reach the client from the server, but which no server
                    code ever names and that is not delivered at generate
                    (required, or ram db).
  client-send       a client ``sendUpdate('x')`` whose field is unknown to
                    the object's dclass, or that has neither clsend nor ownsend
                    (the client agent ejects the client), or an ownsend-only
                    field sent on an object the client does not own.
  global-object     a global object the client generates that the UberDOG does
                    not generate with the same dclass, or that astrond.yml does
                    not list with that dclass.

Class members are taken from the real classes where the module imports
(``dir()`` covers the full MRO, C++ bases included) and are merged with an AST
walk of the class and its resolved bases, so modules that cannot be imported
without the game resources are still covered.

Usage:  python tests/dc_coverage.py [--no-import] [--json | --json-out path]

The allowlist of intentional gaps lives in tests/test_dc_protocol_coverage.py.
"""

import ast
import builtins
import fnmatch
import importlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DC_FILES = ('astron/dclass/otp.dc', 'astron/dclass/pirates.dc')
ASTROND_CONFIGS = ('astron/config/astrond.yml', 'astron/config/blackbox.yml')
SOURCE_PACKAGES = ('otp', 'pirates')

# Server modules that do not follow the AI/UD file suffix convention.
SERVER_MODULE_NAMES = {
    'otp.distributed.AstronInternalRepository',
    'pirates.distributed.PiratesInternalRepository',
    'pirates.ai.PiratesAIRepository',
    'pirates.uberdog.PiratesUberRepository',
}

# Client classes the client owns (it is given ownership by the UberDOG, so
# ownsend fields may be sent on them). Owner views (OV) are added from the dc.
LOCAL_AVATAR_DCLASS = 'DistributedPlayerPirate'
CLIENT_OWNED_DCLASSES = {
    'DistributedPlayer',
    'DistributedPlayerPirate',
}


# ---------------------------------------------------------------------------
# Source index (AST)
# ---------------------------------------------------------------------------

class ClassInfo:

    def __init__(self, module, node):
        self.module = module
        self.name = node.name
        self.node = node
        self.bases = node.bases
        self.members = set()
        self._collect(node.body)

    def _collect(self, body):
        for stmt in body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.members.add(stmt.name)
            elif isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    for name in _targetNames(target):
                        self.members.add(name)
            elif isinstance(stmt, (ast.AnnAssign, ast.AugAssign)):
                self.members.update(_targetNames(stmt.target))
            elif isinstance(stmt, (ast.If, ast.Try, ast.With, ast.For, ast.While)):
                for field in ('body', 'orelse', 'finalbody'):
                    self._collect(getattr(stmt, field, []) or [])
                for handler in getattr(stmt, 'handlers', []) or []:
                    self._collect(handler.body)


def _targetNames(target):
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        names = []
        for elt in target.elts:
            names.extend(_targetNames(elt))
        return names
    return []


class ModuleInfo:

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.isPackage = os.path.basename(path) == '__init__.py'
        with open(path, 'rb') as f:
            source = f.read()
        try:
            self.tree = ast.parse(source, path)
        except SyntaxError:
            self.tree = ast.Module(body=[], type_ignores=[])
        self.classes = {}
        self.imports = {}        # local name -> ('module', dotted) | ('attr', dotted, attr)
        self.starImports = []
        self.aliases = {}        # local name -> expr (module level Name = expr)
        for stmt in self._walkTop(self.tree.body):
            if isinstance(stmt, ast.ClassDef):
                self.classes[stmt.name] = ClassInfo(self, stmt)
            elif isinstance(stmt, ast.Import):
                for alias in stmt.names:
                    if alias.asname:
                        self.imports[alias.asname] = ('module', alias.name)
                    else:
                        top = alias.name.split('.')[0]
                        self.imports[top] = ('module', top)
            elif isinstance(stmt, ast.ImportFrom):
                base = self._absolute(stmt)
                for alias in stmt.names:
                    if alias.name == '*':
                        self.starImports.append(base)
                    else:
                        self.imports[alias.asname or alias.name] = ('attr', base, alias.name)
            elif isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
                if isinstance(stmt.value, (ast.Name, ast.Attribute)):
                    self.aliases[stmt.targets[0].id] = stmt.value

        # Methods attached after the class body: ``Cls.name = func``.
        for stmt in self._walkTop(self.tree.body):
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) \
                            and target.value.id in self.classes:
                        self.classes[target.value.id].members.add(target.attr)

    def _walkTop(self, body):
        for stmt in body:
            yield stmt
            if isinstance(stmt, (ast.If, ast.Try)):
                for field in ('body', 'orelse', 'finalbody'):
                    yield from self._walkTop(getattr(stmt, field, []) or [])
                for handler in getattr(stmt, 'handlers', []) or []:
                    yield from self._walkTop(handler.body)

    def _absolute(self, stmt):
        if not stmt.level:
            return stmt.module or ''
        parts = self.name.split('.')
        if not self.isPackage:
            parts = parts[:-1]
        if stmt.level > 1:
            parts = parts[:-(stmt.level - 1)]
        if stmt.module:
            parts.append(stmt.module)
        return '.'.join(parts)


class SourceIndex:
    """Lazily parsed modules, both of this repository and of installed packages."""

    def __init__(self, useImport=True):
        self.useImport = useImport
        self.modules = {}
        self.importErrors = {}
        self._memberCache = {}
        self._pathCache = {}

    # -- module lookup -------------------------------------------------------

    def findModulePath(self, dotted):
        if dotted not in self._pathCache:
            self._pathCache[dotted] = self._findModulePath(dotted)
        return self._pathCache[dotted]

    def _findModulePath(self, dotted):
        parts = dotted.split('.')
        for base in [ROOT] + [p for p in sys.path if p and os.path.isdir(p)]:
            path = os.path.join(base, *parts)
            if os.path.isfile(path + '.py'):
                return path + '.py'
            if os.path.isfile(os.path.join(path, '__init__.py')):
                return os.path.join(path, '__init__.py')
        return None

    def module(self, dotted):
        if dotted not in self.modules:
            path = self.findModulePath(dotted)
            self.modules[dotted] = ModuleInfo(dotted, path) if path else None
        return self.modules[dotted]

    def isModule(self, dotted):
        return self.findModulePath(dotted) is not None

    # -- name resolution -----------------------------------------------------

    def resolve(self, module, expr, depth=0):
        """Resolve an expression in a module to ('class', ClassInfo),
        ('module', dotted), ('external', obj) or None."""
        if depth > 20:
            return None
        if isinstance(expr, ast.Name):
            return self.resolveName(module, expr.id, depth)
        if isinstance(expr, ast.Attribute):
            owner = self.resolve(module, expr.value, depth + 1)
            if owner is None:
                return None
            kind = owner[0]
            if kind == 'module':
                return self.resolveInModule(owner[1], expr.attr, depth + 1)
            if kind == 'external':
                obj = getattr(owner[1], expr.attr, None)
                return ('external', obj) if obj is not None else None
        return None

    def resolveName(self, module, name, depth=0):
        if name in module.classes:
            return ('class', module.classes[name])
        if name in module.imports:
            entry = module.imports[name]
            if entry[0] == 'module':
                return self.moduleRef(entry[1])
            return self.resolveInModule(entry[1], entry[2], depth + 1)
        if name in module.aliases:
            return self.resolve(module, module.aliases[name], depth + 1)
        for star in module.starImports:
            result = self.resolveInModule(star, name, depth + 1, star=True)
            if result is not None:
                return result
        if hasattr(builtins, name):
            return ('external', getattr(builtins, name))
        return None

    def moduleRef(self, dotted):
        if self.isRepoModule(dotted) or self.module(dotted) is not None:
            return ('module', dotted)
        return self.externalModule(dotted)

    def resolveInModule(self, dotted, name, depth=0, star=False):
        if depth > 20:
            return None
        if not star and self.isModule(dotted + '.' + name):
            return self.moduleRef(dotted + '.' + name)
        if not self.isRepoModule(dotted):
            external = self.externalModule(dotted)
            if external is not None:
                obj = getattr(external[1], name, None)
                if obj is not None:
                    return ('external', obj)
        mod = self.module(dotted)
        if mod is None:
            return None
        if star and name not in mod.classes and name not in mod.imports and name not in mod.aliases:
            # only follow star imports through, do not pick up builtins
            for inner in mod.starImports:
                result = self.resolveInModule(inner, name, depth + 1, star=True)
                if result is not None:
                    return result
            return None
        return self.resolveName(mod, name, depth + 1)

    def isRepoModule(self, dotted):
        return dotted.split('.')[0] in SOURCE_PACKAGES + ('libotp',)

    def externalModule(self, dotted):
        try:
            return ('external', importlib.import_module(dotted))
        except BaseException:
            return None

    # -- class members -------------------------------------------------------

    def astMembers(self, cls, seen=None):
        key = (cls.module.name, cls.name)
        if key in self._memberCache:
            return self._memberCache[key]
        seen = seen or set()
        if key in seen:
            return set()
        seen.add(key)
        members = set(cls.members)
        for base in cls.bases:
            resolved = self.resolve(cls.module, base)
            if resolved is None:
                continue
            if resolved[0] == 'class':
                members |= self.astMembers(resolved[1], seen)
            elif resolved[0] == 'external' and isinstance(resolved[1], type):
                members |= set(dir(resolved[1]))
        self._memberCache[key] = members
        return members

    def findClass(self, dotted, name):
        mod = self.module(dotted)
        if mod is None:
            return None
        return mod.classes.get(name)

    def realClass(self, dotted, name):
        if not self.useImport:
            return None
        try:
            return getattr(importlib.import_module(dotted), name)
        except BaseException as e:
            self.importErrors['%s.%s' % (dotted, name)] = '%s: %s' % (type(e).__name__, str(e)[:120])
            return None

    def members(self, dotted, name):
        """Member names of class ``name`` in module ``dotted``, or None if the
        class does not exist."""
        found = False
        members = set()
        real = self.realClass(dotted, name)
        if isinstance(real, type):
            found = True
            members |= set(dir(real))
        cls = self.findClass(dotted, name)
        if cls is not None:
            found = True
            members |= self.astMembers(cls)
        return members if found else None

    def astMro(self, cls, seen=None):
        """All repository ClassInfos in the class hierarchy."""
        seen = seen if seen is not None else []
        if cls in seen:
            return seen
        seen.append(cls)
        for base in cls.bases:
            resolved = self.resolve(cls.module, base)
            if resolved is not None and resolved[0] == 'class':
                self.astMro(resolved[1], seen)
        return seen


# ---------------------------------------------------------------------------
# dc model
# ---------------------------------------------------------------------------

class DcClass:

    def __init__(self, dcClass):
        self.dc = dcClass
        self.name = dcClass.getName()
        self.module = None
        self.suffixes = set()     # '', 'AI', 'UD', 'OV' for the classes the dc imports
        self.fields = []          # (field, definingClassName)
        for i in range(dcClass.getNumInheritedFields()):
            field = dcClass.getInheritedField(i)
            self.fields.append(field)

    def hasSide(self, suffix):
        return suffix in self.suffixes


def fieldFlags(field):
    return {
        'required': field.isRequired(),
        'broadcast': field.isBroadcast(),
        'ownrecv': field.isOwnrecv(),
        'ram': field.isRam(),
        'db': field.isDb(),
        'clsend': field.isClsend(),
        'ownsend': field.isOwnsend(),
        'airecv': field.isAirecv(),
    }


def loadDcFile():
    from panda3d.direct import DCFile
    dcFile = DCFile()
    for path in DC_FILES:
        if not dcFile.read(os.path.join(ROOT, path)):
            raise RuntimeError('could not read %s' % path)
    return dcFile


def dcModel(dcFile):
    classes = {}
    for i in range(dcFile.getNumClasses()):
        dclass = dcFile.getClass(i)
        if dclass.isStruct():
            continue
        classes[dclass.getName()] = DcClass(dclass)

    for i in range(dcFile.getNumImportModules()):
        module = dcFile.getImportModule(i)
        for j in range(dcFile.getNumImportSymbols(i)):
            parts = dcFile.getImportSymbol(i, j).split('/')
            name = parts[0]
            if name not in classes:
                continue
            classes[name].module = module
            classes[name].suffixes.add('')
            classes[name].suffixes.update(parts[1:])
    return classes


def definingClass(dclass, field):
    """Name of the dclass (in dclass's hierarchy) that declares field."""
    best = dclass.dc
    stack = [dclass.dc]
    while stack:
        current = stack.pop()
        for i in range(current.getNumFields()):
            if current.getField(i).getNumber() == field.getNumber():
                best = current
        for i in range(current.getNumParents()):
            stack.append(current.getParent(i))
    return best.getName()


def atomicNames(field):
    molecular = field.asMolecularField()
    if molecular is None:
        return [field.getName()]
    return [molecular.getAtomic(i).getName() for i in range(molecular.getNumAtomics())]


# ---------------------------------------------------------------------------
# Code scans
# ---------------------------------------------------------------------------

def iterSourceFiles():
    for package in SOURCE_PACKAGES:
        for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, package)):
            dirnames[:] = [d for d in dirnames if d != '__pycache__' and d != 'leveleditor']
            for filename in sorted(filenames):
                if filename.endswith('.py'):
                    path = os.path.join(dirpath, filename)
                    dotted = os.path.relpath(path, ROOT)[:-3].replace(os.sep, '.')
                    if dotted.endswith('.__init__'):
                        dotted = dotted[:-len('.__init__')]
                    yield dotted, path


def isServerModule(dotted):
    stem = dotted.rsplit('.', 1)[-1]
    return stem.endswith('AI') or stem.endswith('UD') or dotted in SERVER_MODULE_NAMES


SENDER_SEVERITY = {'nobody': 0, 'server': 1, 'client': 2}

SEND_METHODS = {'sendUpdate', 'sendUpdateToAvatarId', 'sendUpdateToAccountId',
                'sendUpdateToChannel', 'sendUpdateToDoId'}


def scanServerStrings(index):
    """{module: every string constant in it} for server code; sending a field
    always names it (sendUpdate('x'), sendUpdateToAvatarId(av, 'x'), the
    fields of createObject, ...)."""
    strings = {}
    for dotted, path in iterSourceFiles():
        if not isServerModule(dotted):
            continue
        mod = index.module(dotted)
        if mod is None:
            continue
        strings[dotted] = {node.value for node in ast.walk(mod.tree)
                           if isinstance(node, ast.Constant) and isinstance(node.value, str)}
    return strings


LIFECYCLE_METHODS = {
    'generate', 'announceGenerate', 'disable', 'delete', 'generateInit', 'postGenerateMessage',
    'disableAnnounceAndDelete', 'load', 'unload', 'destroy', 'cleanup',
}


def _isRootFunction(name, fieldNames):
    if name in fieldNames or name in LIFECYCLE_METHODS:
        return True
    if name.startswith('__') and name.endswith('__'):
        return True
    return re.match(r'^(enter|exit|filter)[A-Z]', name) is not None


def scanClientSends(index, fieldNames):
    """[(module, className or None, receiverKind, field, lineno)] for every
    ``x.sendUpdate('field', ...)`` in live client code.

    A function is live when it is a network handler (a dc field), an object
    lifecycle or FSM state method, or when its name is referenced from module
    or class level code or from the body of a live function. The client dump
    carries many ``d_``/``b_`` helpers nothing calls; those do not count."""
    functions = []           # (name, references, sends)
    rootReferences = set()

    for dotted, path in iterSourceFiles():
        if isServerModule(dotted) or dotted.rsplit('.', 1)[-1].startswith('Original_'):
            continue

        # a module that sends nothing only matters for the names it references,
        # a plain token scan is enough (and much cheaper than walking its AST)
        with open(path, encoding='utf-8', errors='replace') as f:
            text = f.read()
        if 'sendUpdate' not in text:
            defined = set(re.findall(r'\bdef\s+(\w+)', text))
            rootReferences.update(set(re.findall(r'[A-Za-z_]\w*', text)) - defined)
            continue

        mod = index.module(dotted)
        if mod is None:
            continue

        def references(node, skipFunctions):
            names = set()
            stack = [node]
            while stack:
                current = stack.pop()
                for child in ast.iter_child_nodes(current):
                    if skipFunctions and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        continue
                    if isinstance(child, ast.Attribute):
                        names.add(child.attr)
                    elif isinstance(child, ast.Name):
                        names.add(child.id)
                    elif isinstance(child, ast.Constant) and isinstance(child.value, str):
                        names.add(child.value)
                    stack.append(child)
            return names

        def visit(node, className, function):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.ClassDef):
                    rootReferences.update(references(child, skipFunctions=True))
                    visit(child, child.name, None)
                    continue
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    entry = (child.name, references(child, skipFunctions=False), [])
                    functions.append(entry)
                    visit(child, className, entry)
                    continue
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute) \
                        and child.func.attr == 'sendUpdate' and child.args \
                        and isinstance(child.args[0], ast.Constant) and isinstance(child.args[0].value, str):
                    receiver = child.func.value
                    if isinstance(receiver, ast.Name) and receiver.id == 'self':
                        receiverKind = 'self'
                    elif (isinstance(receiver, ast.Name) and receiver.id == 'localAvatar') or \
                            (isinstance(receiver, ast.Attribute) and receiver.attr == 'localAvatar'):
                        receiverKind = 'localAvatar'
                    else:
                        receiverKind = None
                    send = (dotted, className, receiverKind, child.args[0].value, child.lineno)
                    if function is None:
                        rootReferences.add(send)
                    else:
                        function[2].append(send)
                visit(child, className, function)

        rootReferences.update(references(mod.tree, skipFunctions=True))
        visit(mod.tree, None, None)

    live = set()
    referenced = set(rootReferences)
    changed = True
    while changed:
        changed = False
        for i, (name, refs, sends) in enumerate(functions):
            if i in live:
                continue
            if _isRootFunction(name, fieldNames) or name in referenced:
                live.add(i)
                referenced |= refs - {name}
                changed = True

    sends = [item for item in rootReferences if isinstance(item, tuple)]
    for i in sorted(live):
        sends.extend(functions[i][2])
    return sorted(sends, key=lambda send: (send[0], send[4], send[3]))


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

def globalObjects(module, index):
    """{doIdName: dclassName} of generateGlobalObject calls in a module."""
    mod = index.module(module)
    result = {}
    if mod is None:
        return result
    for node in ast.walk(mod.tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr == 'generateGlobalObject' and len(node.args) >= 2 \
                and isinstance(node.args[1], ast.Constant):
            idExpr = node.args[0]
            idName = idExpr.attr if isinstance(idExpr, ast.Attribute) else getattr(idExpr, 'id', None)
            if idName:
                result[idName] = node.args[1].value
    return result


def astrondUberdogs(path):
    uberdogs = {}
    current = None
    with open(os.path.join(ROOT, path)) as f:
        inUberdogs = False
        for line in f:
            if re.match(r'^\S', line):
                inUberdogs = line.startswith('uberdogs:')
                continue
            if not inUberdogs:
                continue
            match = re.match(r'^\s*-?\s*class:\s*(\S+)', line)
            if match:
                current = match.group(1)
                continue
            match = re.match(r'^\s*id:\s*(\d+)', line)
            if match and current:
                uberdogs[int(match.group(1))] = current
    return uberdogs


def run(useImport=True):
    os.chdir(ROOT)
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    if useImport:
        _prepareImports()

    index = SourceIndex(useImport=useImport)
    dcFile = loadDcFile()
    classes = dcModel(dcFile)

    from otp.distributed import OtpDoGlobals
    clientGlobals = globalObjects('pirates.distributed.PiratesClientRepository', index)
    clientGlobals.update(globalObjects('otp.distributed.OTPClientRepository', index))
    udGlobals = globalObjects('pirates.uberdog.PiratesUberRepository', index)
    aiGlobals = globalObjects('pirates.ai.PiratesAIRepository', index)
    globalDclasses = set(udGlobals.values())

    findings = {
        'missing-handler': [],
        'missing-getter': [],
        'never-sent': [],
        'client-send': [],
        'global-object': [],
    }

    membersCache = {}
    fieldNames = {field.getName() for dclass in classes.values() for field in dclass.fields}
    clientSends = scanClientSends(index, fieldNames)
    clientMro = {}
    for name, dclass in classes.items():
        if not dclass.module or not dclass.hasSide(''):
            continue
        cls = index.findClass('%s.%s' % (dclass.module, name), name)
        if cls is None:
            continue
        for info in index.astMro(cls):
            clientMro.setdefault((info.module.name, info.name), set()).add(name)


    def sendTargets(module, className, receiverKind):
        if receiverKind == 'self':
            return clientMro.get((module, className), set())
        if receiverKind == 'localAvatar':
            return {LOCAL_AVATAR_DCLASS}
        return set()

    # (dclass, field) the client sends to, and the fields it sends to objects
    # we cannot tell the dclass of
    clientSentTargets = set()
    clientSentUnknown = set()
    for module, className, receiverKind, fieldName, lineno in clientSends:
        targets = sendTargets(module, className, receiverKind)
        if targets:
            clientSentTargets.update((target, fieldName) for target in targets)
        else:
            clientSentUnknown.add(fieldName)
    clientSentNames = clientSentUnknown | {fieldName for target, fieldName in clientSentTargets}
    missingHandlers = {}
    serverStringsByModule = scanServerStrings(index)
    serverStrings = set().union(*serverStringsByModule.values())

    # the server classes of every dclass declaring a field: sending a field
    # from one of them only reaches the clients, never another of them
    fieldFamilies = {}
    for name, dclass in classes.items():
        for field in dclass.fields:
            for suffix in ('AI', 'UD'):
                if dclass.module and dclass.hasSide(suffix):
                    fieldFamilies.setdefault(field.getNumber(), set()).add(
                        '%s.%s%s' % (dclass.module, name, suffix))

    def members(dclass, suffix):
        key = (dclass.name, suffix)
        if key not in membersCache:
            membersCache[key] = index.members('%s.%s%s' % (dclass.module, dclass.name, suffix),
                                              dclass.name + suffix) if dclass.module else None
        return membersCache[key]

    # -- airecv handlers and required getters --------------------------------
    for name in sorted(classes):
        dclass = classes[name]
        if not dclass.module:
            continue

        # Who receives the airecv fields: for a global object, the UberDOG
        # class generated at that doId (the client may know it by a parent
        # dclass) plus the AI's proxy for it; otherwise the AI object, or the
        # UD object for UD-only classes.
        receivers = []
        globalIds = [idName for idName, dclassName in clientGlobals.items() if dclassName == name] or \
                    [idName for idName, dclassName in udGlobals.items() if dclassName == name]
        if globalIds:
            for idName in globalIds:
                if idName in udGlobals and udGlobals[idName] in classes:
                    receivers.append((classes[udGlobals[idName]], 'UD'))
                if idName in aiGlobals and aiGlobals[idName] in classes:
                    receivers.append((classes[aiGlobals[idName]], 'AI'))
        elif dclass.hasSide('UD') and not dclass.hasSide('AI'):
            receivers.append((dclass, 'UD'))
        elif dclass.hasSide('AI'):
            receivers.append((dclass, 'AI'))
        receivers = [(owner, suffix) for owner, suffix in receivers if owner.hasSide(suffix)]

        if receivers:
            receiver = '/'.join(owner.name + suffix for owner, suffix in receivers)
            serverMembers = None
            for owner, suffix in receivers:
                ownerMembers = members(owner, suffix)
                if ownerMembers is not None:
                    serverMembers = (serverMembers or set()) | ownerMembers
            for field in dclass.fields:
                if not field.isAirecv():
                    continue
                names = atomicNames(field)
                if serverMembers is None:
                    missing = True
                else:
                    missing = field.getName() not in serverMembers and \
                        not all(atom in serverMembers for atom in names)
                if missing:
                    # who sends it decides whether the gap is live: 'client'
                    # (live client code sends it), 'server' (server code names
                    # it), otherwise 'nobody'
                    if (field.isClsend() or field.isOwnsend()) and \
                            ((name, field.getName()) in clientSentTargets or field.getName() in clientSentUnknown):
                        sender = 'client'
                    elif any(field.getName() in strings for module, strings in serverStringsByModule.items()
                             if module not in fieldFamilies.get(field.getNumber(), ())):
                        sender = 'server'
                    else:
                        sender = 'nobody'
                    key = '%s.%s' % (definingClass(dclass, field), field.getName())
                    item = missingHandlers.setdefault(key, {'key': key, 'sender': sender, 'missingOn': []})
                    if SENDER_SEVERITY[sender] > SENDER_SEVERITY[item['sender']]:
                        item['sender'] = sender
                        item['missingOn'] = []
                    if sender == item['sender']:
                        item['missingOn'].append(receiver)

        # Objects activated from the database get their required fields from
        # the database; the AI only packs them itself for objects it generates.
        dbBacked = any(field.isDb() for field in dclass.fields)
        if dclass.hasSide('AI') and name not in globalDclasses and not globalIds and not dbBacked:
            aiMembers = members(dclass, 'AI')
            for field in dclass.fields:
                if not field.isRequired() or field.asMolecularField() is not None:
                    continue
                for atom in atomicNames(field):
                    if not atom.startswith('set'):
                        continue
                    getter = 'g' + atom[1:]
                    if aiMembers is None or getter not in aiMembers:
                        findings['missing-getter'].append({
                            'key': '%sAI.%s' % (name, getter), 'dclass': name, 'field': atom,
                            'declaredIn': definingClass(dclass, field)})

    # -- fields only the server can send that it never sends -----------------
    findings['missing-handler'] = list(missingHandlers.values())
    for item in findings['missing-handler']:
        item['missingOn'] = ' '.join(sorted(item['missingOn']))
    seen = set()
    for name in sorted(classes):
        dclass = classes[name]
        if not dclass.module or not dclass.hasSide(''):
            continue
        clientMembers = members(dclass, '')
        if clientMembers is None:
            continue
        for field in dclass.fields:
            fieldName = field.getName()
            if fieldName not in clientMembers:
                continue
            if field.isAirecv() and not field.isBroadcast() and not field.isOwnrecv():
                continue
            if field.isRequired() or (field.isRam() and field.isDb()):
                continue
            if (field.isClsend() or field.isOwnsend()) and fieldName in clientSentNames:
                continue
            if fieldName in serverStrings:
                continue
            molecular = field.asMolecularField()
            if molecular is not None and all(atom in serverStrings for atom in atomicNames(field)):
                continue
            declaredIn = definingClass(dclass, field)
            key = '%s.%s' % (declaredIn, fieldName)
            if key in seen:
                continue
            seen.add(key)
            findings['never-sent'].append({'key': key, 'dclass': declaredIn, 'field': fieldName})

    # -- client send flags -----------------------------------------------------
    fieldsByName = {}
    for name, dclass in classes.items():
        for field in dclass.fields:
            fieldsByName.setdefault(field.getName(), {})[definingClass(dclass, field)] = field

    owned = set(CLIENT_OWNED_DCLASSES)
    for name, dclass in classes.items():
        if dclass.hasSide('OV'):
            owned.add(name)

    for module, className, receiverKind, fieldName, lineno in clientSends:
        where = '%s:%d' % (module.replace('.', '/') + '.py', lineno)
        targets = sendTargets(module, className, receiverKind)
        if targets:
            # the method may only ever run on some of the dclasses sharing it
            known = {}
            for target in targets:
                field = classes[target].dc.getFieldByName(fieldName)
                if field is not None:
                    known[target] = field
            key = '%s.%s' % (className, fieldName)
        else:
            known = fieldsByName.get(fieldName, {})
            key = '%s.%s' % (className or '?', fieldName)

        if not known:
            problem = 'unknown field'
        elif not any(field.isClsend() or field.isOwnsend() for field in known.values()):
            problem = 'not clsend/ownsend'
        elif targets and not any(field.isClsend() or name in owned for name, field in known.items()):
            problem = 'ownsend on unowned object'
        else:
            continue
        findings['client-send'].append({'key': key, 'problem': problem, 'where': where})

    unique = {}
    for item in findings['client-send']:
        unique.setdefault(item['key'], item)
    findings['client-send'] = list(unique.values())

    # -- global objects --------------------------------------------------------
    configs = {path: astrondUberdogs(path) for path in ASTROND_CONFIGS}
    for idName, dclassName in sorted(clientGlobals.items()):
        doId = getattr(OtpDoGlobals, idName, None)
        if dclassName not in classes:
            findings['global-object'].append({'key': '%s=%s' % (idName, dclassName), 'problem': 'unknown dclass'})
            continue
        if udGlobals.get(idName) != dclassName:
            findings['global-object'].append({
                'key': '%s=%s' % (idName, dclassName),
                'problem': 'UberDOG generates %s' % (udGlobals.get(idName) or 'nothing')})
        for path, uberdogs in configs.items():
            if uberdogs.get(doId) != dclassName:
                findings['global-object'].append({
                    'key': '%s=%s@%s' % (idName, dclassName, os.path.basename(path)),
                    'problem': 'listed as %s' % (uberdogs.get(doId) or 'nothing')})
    for idName, dclassName in sorted(aiGlobals.items()):
        if idName not in udGlobals:
            findings['global-object'].append({'key': '%s=%s@AI' % (idName, dclassName),
                                              'problem': 'AI proxy for a global the UberDOG does not generate'})

    for kind in findings:
        findings[kind].sort(key=lambda item: item['key'])
    return findings, index.importErrors


def _prepareImports():
    from panda3d.core import loadPrcFile, loadPrcFileData
    loadPrcFile(os.path.join(ROOT, 'config/dev.prc'))
    loadPrcFileData('', 'audio-library-name null\nwindow-type none\nnotify-level-dclass error')
    if not hasattr(builtins, 'base'):
        from direct.showbase.ShowBase import ShowBase
        ShowBase(windowType='none')


def isAllowed(kind, key, allowlist):
    return any(fnmatch.fnmatchcase(key, pattern) for pattern in allowlist.get(kind, {}))


def isFailure(kind, item):
    """Missing handlers of fields nobody ever sends are listed, not failed."""
    return not (kind == 'missing-handler' and item.get('sender') == 'nobody')


def formatReport(findings, importErrors=None, allowlist=None):
    allowlist = allowlist or {}
    lines = []
    for kind, items in findings.items():
        allowed = [item for item in items if isAllowed(kind, item['key'], allowlist)]
        lines.append('== %s: %d (%d allowlisted)' % (kind, len(items), len(allowed)))
        for item in items:
            extra = ', '.join('%s=%s' % (k, v) for k, v in sorted(item.items()) if k != 'key')
            if isAllowed(kind, item['key'], allowlist):
                mark = '  [allowed] '
            elif not isFailure(kind, item):
                mark = '  [unsent]  '
            else:
                mark = '  '
            lines.append('%s%s  (%s)' % (mark, item['key'], extra))
    if importErrors:
        lines.append('== modules audited from source only (import failed): %d' % len(importErrors))
        for name, error in sorted(importErrors.items()):
            lines.append('  %s  %s' % (name, error))
    return '\n'.join(lines)


def main(argv):
    findings, importErrors = run(useImport='--no-import' not in argv)
    result = {'findings': findings, 'importErrors': importErrors}
    if '--json-out' in argv:
        with open(argv[argv.index('--json-out') + 1], 'w') as f:
            json.dump(result, f, indent=1, sort_keys=True)
    elif '--json' in argv:
        print(json.dumps(result, indent=1, sort_keys=True))
    else:
        print(formatReport(findings, importErrors))


if __name__ == '__main__':
    # run as a script, tests/ is on sys.path and its test packages (tests/pirates,
    # tests/otp) would shadow the real ones...
    sys.path[:] = [path for path in sys.path if os.path.abspath(path or '.') != os.path.dirname(os.path.abspath(__file__))]
    main(sys.argv[1:])

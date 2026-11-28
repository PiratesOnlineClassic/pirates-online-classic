"""Entry point of the compiled Pirates Online Classic client.

Nuitka compiles this file as the program's __main__.  It does what the dev
launchers (darwin/start_game.command, win32/start_dev.bat) do by hand, then
starts the game exactly like ``python -m pirates.piratesbase.PiratesStart``:

1. Finds the game folder (the one holding config/general.prc) and makes it
   the working directory.  PiratesStart loads config/*.prc by relative path,
   general.prc names the dc files by relative path, and the game reads some
   phase files from ../resources, so the working directory has to be the
   game folder with the resources folder beside it.
2. Points Panda3D at the Config.prc and plugins Nuitka bundled.
3. Fills in the environment the game reads (GAME_* URLs, POC_GAMESERVER)
   from config/release.env, without overriding anything already set.
4. Takes the play token from --token, POC_TOKEN, or a prompt when run from a
   terminal.
5. Sends output to a log file when there is no console to show it.

It also runs unfrozen from a checkout for testing:
``python build/client_main.py --token dev``.

Release layout it expects (nuitka_build.py makes it):

    <release>/game/       working directory: executable, config/, astron/
    <release>/resources/  phase_2 .. phase_5

On macOS the same two folders live in the app bundle under
Contents/Resources/ and the executable is in Contents/MacOS/.
"""

import os
import sys
import time

APP_NAME = 'PiratesOnlineClassic'


def _compiled_containing_dir():
    compiled = globals().get('__compiled__')
    if compiled is not None:
        containing = getattr(compiled, 'containing_dir', None)
        if containing:
            return containing
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def find_game_dir(explicit=None):
    """The folder with config/general.prc: next to the executable, in its
    game/ subfolder, in a macOS bundle's Contents/Resources/game, or the
    current directory (a source checkout)."""
    exe_dir = _compiled_containing_dir()
    candidates = []
    if explicit:
        candidates.append(explicit)
    if os.environ.get('POC_GAME_DIR'):
        candidates.append(os.environ['POC_GAME_DIR'])
    candidates += [
        exe_dir,
        os.path.join(exe_dir, 'game'),
        os.path.join(exe_dir, '..', 'Resources', 'game'),
        os.getcwd(),
    ]
    for candidate in candidates:
        if os.path.isfile(os.path.join(candidate, 'config', 'general.prc')):
            return os.path.realpath(candidate)
    return None


def user_data_dir():
    """A per-user writable folder for logs."""
    if sys.platform == 'win32':
        base = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~\\AppData\\Local')
        return os.path.join(base, APP_NAME)
    if sys.platform == 'darwin':
        return os.path.expanduser('~/Library/Logs/' + APP_NAME)
    base = os.environ.get('XDG_STATE_HOME') or os.path.expanduser('~/.local/state')
    return os.path.join(base, APP_NAME)


def redirect_output_to_log():
    """Without a console, send stdout/stderr (Python and Panda3D's C++
    notify output alike) to a log file at the file-descriptor level."""
    log_dir = os.path.join(user_data_dir(), 'logs')
    try:
        os.makedirs(log_dir, exist_ok=True)
        path = os.path.join(log_dir, 'client-%s.log' % time.strftime('%Y%m%d-%H%M%S'))
        log = open(path, 'a', buffering=1, encoding='utf-8', errors='replace')
    except OSError:
        return None
    for fd in (1, 2):
        try:
            os.dup2(log.fileno(), fd)
        except OSError:
            pass
    sys.stdout = sys.stderr = log
    return path


def has_console():
    stream = sys.stdout
    try:
        return stream is not None and stream.isatty()
    except (AttributeError, ValueError):
        return False


def load_env_file(path):
    """KEY=VALUE lines; '#' starts a comment.  Never overrides the caller's
    environment, so a launcher or the player can still set any of these."""
    if not os.path.isfile(path):
        return
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())


def bundled_root():
    """Where Nuitka put the bundled files (panda3d/, DLLs).  In onefile mode
    that is the unpack folder, not the folder holding the executable."""
    return os.path.dirname(os.path.abspath(__file__))


def point_panda_at_bundle():
    """Before panda3d is imported: let Panda3D find the Config.prc and
    Confauto.prc copied from the panda3d wheel (they hold load-audio-type
    for p3ffmpeg, which the game's mp3 sounds need)."""
    if 'PANDA_PRC_DIR' in os.environ:
        return
    root = bundled_root()
    for etc in (os.path.join(root, 'panda3d', 'etc'), os.path.join(root, 'etc')):
        if os.path.isfile(os.path.join(etc, 'Config.prc')):
            os.environ['PANDA_PRC_DIR'] = etc
            return


def add_plugin_path():
    """After panda3d.core is imported, before the window opens: add the
    folders holding the display/audio plugins to plugin-path.  Panda looks
    next to libp3dtool by default; this also covers Nuitka putting the
    plugins somewhere else, and onefile's unpack folder."""
    from panda3d.core import ExecutionEnvironment, Filename, loadPrcFileData
    dirs = []
    dtool = ExecutionEnvironment.getDtoolName()
    if dtool:
        dirs.append(os.path.dirname(Filename(dtool).toOsSpecific()))
    root = bundled_root()
    dirs += [os.path.join(root, 'panda3d'), root]
    lines = []
    seen = set()
    for d in dirs:
        d = os.path.realpath(d)
        if d in seen or not os.path.isdir(d):
            continue
        seen.add(d)
        lines.append('plugin-path %s' % Filename.fromOsSpecific(d).getFullpath())
    # The same audio/video loaders Confauto.prc sets, in case it was missed.
    lines.append('load-audio-type * p3ffmpeg')
    lines.append('load-video-type * p3ffmpeg')
    loadPrcFileData('poc-bundle', '\n'.join(lines))


def show_error(message):
    print(message, file=sys.stderr)
    if sys.platform == 'win32':
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, message, 'Pirates Online Classic', 0x10)
        except Exception:
            pass


def parse_args(argv):
    """--token, --server and --game-dir; everything else is left alone."""
    opts, rest = {}, []
    it = iter(argv)
    for arg in it:
        for name in ('--token', '--server', '--game-dir'):
            if arg == name:
                opts[name] = next(it, '')
                break
            if arg.startswith(name + '='):
                opts[name] = arg.split('=', 1)[1]
                break
        else:
            if arg == '--log':
                opts['--log'] = True
            else:
                rest.append(arg)
    return opts, rest


def main():
    opts, rest = parse_args(sys.argv[1:])
    sys.argv = sys.argv[:1] + rest

    console = has_console()
    log_path = None
    if not console or opts.get('--log'):
        log_path = redirect_output_to_log()

    game_dir = find_game_dir(opts.get('--game-dir'))
    if game_dir is None:
        show_error('Pirates Online Classic could not find its game folder '
                   '(config/general.prc).  Reinstall the game, or set POC_GAME_DIR.')
        return 1
    os.chdir(game_dir)
    if '__compiled__' not in globals():
        # Unfrozen run from a checkout: import the game from the game folder.
        sys.path.insert(0, game_dir)

    load_env_file(os.path.join(game_dir, 'config', 'release.env'))
    if opts.get('--server'):
        os.environ['POC_GAMESERVER'] = opts['--server']
    if opts.get('--token'):
        os.environ['POC_TOKEN'] = opts['--token']

    if not os.environ.get('POC_TOKEN'):
        if console and sys.stdin is not None and sys.stdin.isatty():
            token = input('Username / play token: ').strip()
            if token:
                os.environ['POC_TOKEN'] = token
        if not os.environ.get('POC_TOKEN'):
            show_error('No play token.  Start the game from the launcher, or run it '
                       'with --token <token> (or set POC_TOKEN).')
            return 1

    if not os.path.isdir(os.path.join(game_dir, '..', 'resources', 'phase_3')):
        print('Warning: no resources at %s' % os.path.join(game_dir, '..', 'resources'))

    print('Pirates Online Classic: game folder %s, server %s%s' % (
        game_dir, os.environ.get('POC_GAMESERVER', '(unset)'),
        (', log %s' % log_path) if log_path else ''))

    point_panda_at_bundle()
    import panda3d.core  # noqa: F401  (initialises the Config.prc search)
    add_plugin_path()

    # Runs the whole game; returns when the window closes.
    import pirates.piratesbase.PiratesStart  # noqa: F401
    return 0


if __name__ == '__main__':
    sys.exit(main())

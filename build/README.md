# Building the release client with Nuitka

`build/nuitka_build.py` compiles the game client (what
`python -m pirates.piratesbase.PiratesStart` runs) into a native executable
with [Nuitka](https://nuitka.net) and lays out a release folder players can
download. Nothing in the game code changes; the build adds an entry point
(`build/client_main.py`) and release config.

| File | What it is |
| --- | --- |
| `nuitka_build.py` | Assembles and prints the Nuitka command, runs it, lays out the release. |
| `collect_modules.py` | Works out the modules Nuitka can't find by itself (dc classes, worldData, localizers, Panda's hidden imports). `nuitka_build.py` runs it on every build. |
| `client_main.py` | The compiled program's entry point: sets the working directory, environment and Panda3D paths, then imports `PiratesStart`. |
| `release.prc` | Release settings, shipped as `config/dev.prc` (see [Config](#config)). |
| `release.env` | Default environment (server address, `GAME_*` URLs), shipped as `config/release.env`. |

## Prerequisites

Build each OS on that OS: Nuitka can't cross-compile.

- **Python 3.12, 64-bit CPython**, matching a panda3d 1.10.16 wheel
  (`pip install -r requirements-build.txt` installs panda3d, requests and
  Nuitka 4.4). Use the same Python minor version on every OS.
  - macOS: the python.org installer (universal2). Apple's
    `/usr/bin/python3` (Command Line Tools) is refused by Nuitka for
    standalone builds. Homebrew Python works too but ties the build to the
    build machine's macOS version.
  - Windows: the python.org installer, 64-bit.
  - Linux: the distro's `python3.12` plus `python3.12-dev`, or pyenv.
- **Nuitka 4.4** (`requirements-build.txt`). `pip install imageio` too if
  the icon is a `.png` (Nuitka converts it).
- **A C compiler**
  - Windows: Visual Studio 2022 Build Tools with "Desktop development with
    C++". (Nuitka can download MinGW-w64 itself, but MSVC is what the
    python.org build uses.)
  - macOS: Xcode Command Line Tools (`xcode-select --install`), clang.
  - Linux: gcc, plus `patchelf` (required for standalone builds) and
    optionally `ccache`. Build on the oldest distro you support: the binary
    needs a glibc at least as new as the build machine's.
- **libotp/** in the checkout (it's tracked in git); the client imports it.
- **The resources checkout** (`../resources`) if you bundle resources.

Do it in a venv:

```sh
python3.12 -m venv .venv-build
. .venv-build/bin/activate          # Windows: .venv-build\Scripts\activate
pip install -r requirements-build.txt
```

## GitHub Actions

`.github/workflows/build-client.yml` builds all three OSes on GitHub's
runners (Windows Server 2022 with MSVC, macOS 14, Ubuntu 22.04 for an old
enough glibc), each with Python 3.12 and `requirements-build.txt`.

- **Pushing a tag like `v1.2.3`** builds version `1.2.3.0` and publishes a
  GitHub Release with the three archives attached.
- **Run workflow** in the Actions tab builds by hand (version
  `0.0.0.<run number>`), optionally as a single executable. The archives
  are attached to the run as artifacts.

Archives are zips on Windows and macOS (`ditto` keeps the `.app` intact)
and a `.tar.gz` on Linux (keeps the executable bits). Resources aren't
bundled, and the builds aren't code signed. Nuitka's cache is kept between
runs, so builds after the first are much faster.

## Commands

```sh
# See exactly what would run, and check the prerequisites. Builds nothing.
python build/nuitka_build.py --dry-run

# Folder build for this OS (recommended for releases)
python build/nuitka_build.py --jobs 8

# Folder build with the phase files copied in (all-in-one download)
python build/nuitka_build.py --resources-dir ../resources

# Single executable (Windows/Linux; macOS always makes an .app)
python build/nuitka_build.py --onefile

# Version, icon, macOS identity
python build/nuitka_build.py --version 1.0.1.0 --icon path/to/icon.ico
python build/nuitka_build.py --bundle-id com.example.piratesclassic --codesign-identity "Developer ID Application: ..."

# Re-run only the layout step after a build
python build/nuitka_build.py --layout-only
```

Other options: `--output-dir` (default `dist/nuitka`), `--python` (the
interpreter that runs Nuitka, default the one running the script),
`--nuitka-arg=...` (repeatable, passed straight to Nuitka, e.g.
`--nuitka-arg=--assume-yes-for-downloads` on a CI box).

The module lists, on their own:

```sh
python build/collect_modules.py                # summary
python build/collect_modules.py --flags        # the Nuitka flags it adds
python build/collect_modules.py --json         # everything, including what was left out
python build/collect_modules.py --check-imports --python .venv-build/bin/python \
    --resources-dir ../resources [--world-data]
```

`--check-imports` imports every listed module in its own subprocess (with
the dev prc files loaded, a windowless ShowBase and the dummy launcher,
in the order PiratesStart imports things) and reports the ones that fail.
Run it after adding a dc class or a dynamic import.

## Release layout

```
dist/nuitka/PiratesOnlineClassic-windows/
  game/                          working directory of the client
    PiratesOnlineClassic.exe     + DLLs, python3xx.dll, panda3d/ (plugins, etc/Config.prc)
    config/general.prc
    config/performance.prc
    config/dev.prc               = build/release.prc
    config/release.env           = build/release.env
    astron/dclass/otp.dc, pirates.dc
  resources/                     phase_2 .. phase_5 (with --resources-dir), else a README
  PiratesOnlineClassic.bat       starts game\PiratesOnlineClassic.exe (.sh on Linux)
  BUILD-INFO.txt                 git revision and the Nuitka command
```

With `--onefile`, `game/` holds the single executable instead of the
folder; config and dc files stay next to it so they can be edited. It
unpacks once per version into the user cache
(`{CACHE_DIR}/PiratesOnlineClassic/<version>`).

On macOS the release is `Pirates Online Classic.app`: Nuitka's files are in
`Contents/MacOS`, and `game/` and `resources/` are in `Contents/Resources/`.
The layout step re-signs the bundle (ad hoc by default) because adding
files breaks the signature Nuitka made.

Why two folders: the game reads several files from the hardcoded relative
path `../resources/phase_N/etc` (WeaponGlobals.pkl, the whitelist, quest
scripts, sea patch and particle files), and PiratesStart loads
`config/*.prc` by relative path. So the working directory must be a folder
that has `config/` in it and `resources/` beside it. `client_main.py`
finds that folder (next to the executable, in `game/`, or in the bundle)
and changes into it, so players can start the executable from anywhere.

## Config

PiratesStart loads `config/general.prc`, `config/dev.prc`,
`config/performance.prc` (each overriding the one before) and then
`config/personal.prc` if it exists. The release ships:

- `general.prc` and `performance.prc` unchanged.
- `build/release.prc` **as `config/dev.prc`**: dev settings off
  (`want-dev-access`, `disable-blockers`, `teleport-all`, `exec-chat` and
  friends), `model-path` pointing at `../resources`. Putting it in the
  `dev.prc` slot keeps PiratesStart unchanged.
- `build/release.env` as `config/release.env`.
- Not `personal.prc`: players can create one to override settings.

Not shipped:

- `config/dev.prc`: developer settings (`want-dev-access`,
  `disable-blockers`).
- `config/server.prc`: server only, and it holds a Discord bot token.
- `config/release/dist_prod.prc`: out of date. It sets `server-port 7198`
  (astron listens on 6667) and two different `server-version`s, and turns on
  `teleport-all`, `ignore-teleport-requirements` and `disable-blockers`.
  It also has analytics keys. `release.prc` replaces it; delete it or bring
  it up to date.

`server-version` comes from `general.prc` (`pirates-dev`) and must match
`version:` in `astron/config/astrond.yml`, or the server drops the client.

Environment: `client_main.py` reads `config/release.env` and sets each
variable only if it isn't already set, so a launcher can override any of
them. It sets `POC_GAMESERVER` (the production server from
`config/environ/default.env`, **check it before a release**),
`GAME_ENVIRONMENT=LIVE` and the `GAME_*` URLs (the `MOREINFO` URL is fixed
to `https://`; `default.env` has `https:/`). The play token comes from
`--token`, then `POC_TOKEN`, then a prompt when run from a terminal. With
none of those it shows an error and exits.

Command line: `PiratesOnlineClassic --token TOKEN --server HOST [--game-dir DIR] [--log]`.

Output: with no console (double-clicked), stdout/stderr, including
Panda3D's own messages, go to a log file:
`%LOCALAPPDATA%\PiratesOnlineClassic\logs\` on Windows,
`~/Library/Logs/PiratesOnlineClassic/logs/` on macOS,
`~/.local/state/PiratesOnlineClassic/logs/` on Linux. `--log` forces it.

## Resources: bundle or download separately?

The resources checkout is about 650 MB (3,100 `.bam` models, 1,200 `.jpg`,
450 `.mp3`, plus `.rgb`, `.glsl`, `.spf`, `.ptf`, `.pkl`, `.txt`) and
changes on its own schedule.

**Recommendation: ship resources as a separate download**, unpacked into
`resources/` beside `game/`. A code fix then doesn't mean re-downloading
650 MB, and an art update doesn't need a rebuild. Use `--resources-dir` to
make an all-in-one archive for first installs. It copies everything except
`.git`, `.DS_Store` and editor files. A launcher or patcher that downloads
both is the long-term answer.

The `.cg` shaders in resources aren't used (this Panda has no Cg; the game
loads the `.glsl` ports). Models are `.bam` only, so the Assimp loader is
left out. `pandaegg` stays because Nuitka's panda3d config always copies it
and `StormEye` still asks for two `.egg` files (they don't exist in
resources either way).

## What's included and why

Nuitka follows ordinary imports. These are loaded by name, so
`collect_modules.py` adds them with `--include-module`:

| What | Where it's loaded | Count |
| --- | --- | --- |
| dc client classes: for every `from pkg import Name/AI/UD/OV` line, `pkg.Name`, plus `pkg.NameOV` when the line lists `OV` | `direct.distributed.ConnectionRepository.readDCFile` (`__import__`); a missing one is fatal | 239 game + 5 `direct.distributed` |
| `pirates.leveleditor.worldData.*` | `WorldCreatorBase.openFile`: `__import__('pirates.leveleditor.worldData.' + name)` | 366, as bytecode |
| `PLocalizerEnglish`, `PQuestStringsEnglish`, `PGreetingStringsEnglish`, `OTPLocalizerEnglish` (every language file present) | `exec('from ' + languageModule + ' import *')` in PLocalizer / OTPLocalizer | 4 |
| `direct.particles.ParticleManagerGlobal`, `direct.showbase.PhysicsManagerGlobal`, `panda3d.physics` | `ShowBase.enableParticles` (`importlib`, hidden from freezers on purpose); PiratesBase turns particles on | 3 |
| `direct.distributed.ClockDelta`, `direct.showbase.ProfileSession`, `direct.task.FrameProfiler`, `direct.task.TaskProfiler` | `importlib` in PythonUtil / Task | 4 |

worldData is about 20 MB of dict literals. Compiling it to C would take a
very long time and a lot of memory for no speed gain, so
`--noinclude-custom-mode=pirates.leveleditor.worldData:bytecode` includes it
as bytecode. `dataToText*` (level editor tools) are left out.

Other dynamic code, checked and needing nothing extra:
`eval`/`exec` on data (WorldCreatorBase, QuestParser `PLocalizer.*`,
ShipModel, HumanDNA, AvatarTypes, Flag), `.spf` files exec'd by SeaPatch,
`.ptf` particle files exec'd by ParticleEffect, and the `>` exec chat
(turned off in release.prc). They run Python source, not module imports,
and work the same in a compiled build.

Panda3D native parts: Nuitka 4.4 has no panda3d plugin, but its built-in
package config (`standard.nuitka-package.config.yml`, `panda3d` entry)
copies `panda3d/etc` (Config.prc, Confauto.prc), `panda3d/models`, and the
plugins `libpandagl`, `libpandadx9`, `libp3tinydisplay`, `libp3openal_audio`,
`libp3ffmpeg`, `libp3ptloader`, `libp3assimp`, `libpandaegg`. The client asks
for: `load-display pandagl`, `aux-display pandadx9` / `p3tinydisplay`
(`pandadx8` no longer exists in 1.10 and is ignored), `audio-library-name
p3openal_audio`, and `p3ffmpeg` (through Confauto.prc's `load-audio-type`)
for the mp3 sounds. `libp3assimp` is dropped with `--noinclude-dlls`. Like
Panda's own `build_apps` (direct/dist), which copies the plugins next to the
executable and writes the prc into `etc/`, `client_main.py` points
`PANDA_PRC_DIR` at the bundled `panda3d/etc` and adds the plugin folders to
`plugin-path` at run time. It also sets `load-audio-type * p3ffmpeg` in case
Confauto.prc is missed. The layout step lists where each plugin ended up and
warns if one is missing.

Third-party packages the client imports: **requests** (top-level import in
`pirates.uberdog.ClientServicesManager`, a dc class; Nuitka brings in
urllib3, idna, charset_normalizer and certifi's `cacert.pem` through its
package config). Optional imports that are absent on purpose: `embedded`
(Disney's ActiveX ad frame, `try`/`except`) and `win32api` (old launcher
code, only reached on the Disney launcher path). There is no Discord RPC
library: the `discord-*` prc settings have no client code behind them, and
`pirates.discord` is server-only (webhooks). **semidbm** and
**pycryptodome** are server-only.

### Left out

- 293 server modules (`*AI`, `*UD`, `PiratesAIRepository`,
  `PiratesUberRepository`, the RPC server, Discord webhooks, the
  `ServiceStart`s). Nothing on the client reaches them, so Nuitka never
  follows them; `collect_modules.py --json` lists them under
  `excluded_server_modules`. `CrewHUD` ends in "UD" but is client GUI and is
  kept.
- Dev tools, with `--nofollow-import-to`: `tkinter`, `Pmw`, `wx`,
  `direct.tkpanels`, `direct.tkwidgets`, `direct.directtools` and the other
  editor/cluster/dist packages, and the game's own Tk panels
  (`pirates.seapatch.WaterPanel`, `SeaPatchPanel`,
  `pirates.leveleditor.TimeOfDayPanel`). They're only imported behind dev
  settings (`want-water-panel`, sea patch keys, the time of day editor) and
  would raise `ImportError` if a player turned those on.

## Known risks

- **The working directory must be writable.** In a release
  (`__dev__` off), `pirates.piratesgui.GameOptions` writes
  `game_options.txt`, `last_working_options.txt` and
  `p_working_options.txt` to the working directory, which is `game/`.
  Install to a per-user folder (e.g. `%LOCALAPPDATA%` on Windows, not
  Program Files). On macOS that folder is inside the .app: writing there
  breaks the code signature and fails for a non-admin user in
  /Applications. A small code change, moving those paths to a per-user
  folder, would fix this properly. Screenshots (`PiratesBase.takeScreenShot`)
  are saved to the working directory too.
- **Never build with `-O` / `--python-flag=no_asserts`.** WeaponGlobals,
  PWhiteList, QuestParser, SeaPatch and Twister pick
  `../resources/phase_N/etc` only under `if __debug__:` and otherwise look in
  `phase_N/etc` relative to the working directory, which doesn't exist.
- **Plugin and Config.prc placement isn't verified by a real build yet.**
  `client_main.py` covers both "next to libp3dtool" and "bundle root". Check
  the layout step's plugin list and the smoke test below.
- **Build time and memory**: about 1,100 game modules plus Panda's `direct`
  compile to C. Expect a long first build and several GB of RAM; lower
  `--jobs` if the compiler runs out of memory. `ccache` (Linux/macOS) or
  `clcache` speeds up rebuilds.
- `pirates.leveleditor.worldData.spawningTestIsle` fails to import
  (`NameError: Point3`): a broken test island, and harmless unless loaded.
- `importlib.reload(CutsceneData)` (cutscene dev path) can't reload a
  compiled module from source.
- **No icon in the repo.** `general.prc` asks for
  `phase_3/etc/Pirates_Adds.ico`, which isn't in resources, and the only
  image is the wide `.github/logo.png`. Put a square icon in
  `build/icons/PiratesOnlineClassic.ico` / `.icns` / `.png`, or pass `--icon`.
- **Windows SmartScreen and antivirus** flag unsigned Nuitka executables,
  onefile ones especially. Sign the `.exe` and prefer the folder build.
- **macOS Gatekeeper**: an ad-hoc-signed app has to be opened with
  right-click > Open. A public release needs a Developer ID signature, the
  hardened runtime and notarization (`--codesign-identity`, then
  `xcrun notarytool`).
- **Linux**: check `ldd game/libp3openal_audio.so` and
  `ldd game/panda3d/libpandagl.so` for missing system libraries (OpenAL,
  libGL, X11).
- `config/server.prc` (Discord bot token) and `dist_prod.prc` (analytics
  keys) have secrets in git. They aren't shipped, but rotate them if the
  repository is public.
- Some checkouts have a `libotp/libotp` symlink back to the folder itself
  (it's gitignored). The collector skips it, and the build never walks into
  it because libotp is only included through imports.

## Smoke test after a build

On a clean machine or user account without Python or Panda3D installed:

1. The release folder has `game/config/{general,performance,dev}.prc`,
   `game/config/release.env`, `game/astron/dclass/{otp,pirates}.dc`, and
   `resources/phase_2..5` (bundled or unpacked).
2. The layout step listed `libpandagl`, `libp3openal_audio`, `libp3ffmpeg`,
   `libp3tinydisplay` (and `libpandadx9` and `OpenAL32` on Windows).
3. From a terminal: `game/PiratesOnlineClassic --token test --server 127.0.0.1`
   against a local server. It prints the game folder and server, and
   `PLocalizer: Running in language: english`.
4. A window opens with the title "Pirates Online Classic" and the loading
   screen. No `Unable to open window`, no `could not load display`.
5. Sound: the GUI click on buttons (mp3 through p3ffmpeg) and music play.
6. Log in and pick or make a pirate. Make-a-pirate covers the localizer and
   many GUI modules.
7. Enter the world: Port Royal or the tutorial loads (worldData bytecode,
   `../resources/phase_2/etc/WeaponGlobals.pkl`, quest scripts).
8. Walk, fight an enemy, open the map and inventory, and board and sail a
   ship (dc OV classes such as `PlayerShipOV`, `DistributedHullOV`; sea
   patch `.spf` files; water shaders).
9. Change a setting in Options, quit, start again: `game_options.txt` was
   written and read back.
10. Double-click start (no terminal): the game runs and a log appears in the
    per-user logs folder.
11. Start it from another working directory, and from a path with spaces:
    it still finds its game folder.
12. Search the log for `ImportError`, `ModuleNotFoundError`,
    `No class definition for` and `Missing plugin`.
13. macOS: run from /Applications as a non-admin user (see the
    writable-folder risk). Windows: run without admin rights.

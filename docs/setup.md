# Setting up a local server

This guide takes a fresh machine to a running server with you logged in as a
pirate. You run five things: Astron, the UberDOG, the AI, and then the game
client. Plan on about 30 minutes, most of it building Astron.

## What you need

| | Notes |
|---|---|
| Python 3.9 or newer, 64-bit | Use the same interpreter for the servers and the client. On Windows the scripts use Panda3D's `ppython`. |
| Panda3D 1.10.x | Use the unmodified release from pip (`panda3d`). Development uses 1.10.16. |
| Git | |
| CMake, a C++17 compiler and Boost | Needed to build Astron. Read the Astron fork's README for its full dependency list. |
| About 4 GB of disk | Most of it is the game resources. |

## 1. Get the code and the resources

The client loads its models from `../resources`. Clone the resources **next to**
this repository, not inside it:

```bash
git clone https://github.com/PiratesOnlineClassic/pirates-online-classic.git
```

```bash
git clone https://github.com/PiratesOnlineClassic/poc-resources.git resources
```

```
parent-folder/
├── pirates-online-classic/   # this repository
└── resources/                # phase_2 … phase_5
```

If you keep them somewhere else, point `model-path` at them in
`config/personal.prc` (see [configuration](configuration.md)).

## 2. Install the Python packages

From the repository root:

```bash
python3 -m pip install -r requirements.txt
```

Check that Panda3D imports:

```bash
python3 -c "import panda3d.core; print(panda3d.core.PandaSystem.getVersionString())"
```

## 3. Build Astron

The project uses a fork of Astron
([PiratesOnlineClassic/Astron](https://github.com/PiratesOnlineClassic/Astron)).
Its client agent lets the client connect without a dc hash check
(`send_hash: false` in `astron/config/astrond.yml`).

```bash
git clone https://github.com/PiratesOnlineClassic/Astron.git
cd Astron && mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --config Release -j 8
```

Copy the binary into this repository's `astron/` folder, next to `config/` and
`dclass/`:

| OS | Copy |
|---|---|
| macOS / Linux | `build/astrond` → `pirates-online-classic/astron/astrond` |
| Windows | `build\Release\astrond.exe` → `pirates-online-classic\astron\astrond.exe` |

## 4. Start the servers

Start them **in this order**, each in its own terminal, and let each one finish
starting before you launch the next. The UberDOG must be up before the AI, or
the AI's district never shows up in the shard list.

| Step | macOS | Linux | Windows |
|---|---|---|---|
| 1. Astron | `astron/darwin/start_astron.command` | `astron/linux/start_astron.sh` | `astron\win32\start_astron.bat` |
| 2. UberDOG | `astron/darwin/start_uberdog.command` | `astron/linux/start_uberdog.sh` | `astron\win32\start_uberdog.bat` |
| 3. AI (one district) | `astron/darwin/start_ai.command` | `astron/linux/start_ai.sh` | `astron\win32\start_ai.bat` |
| 4. Client | `darwin/start_game.command` | run it by hand (below) | `win32\start_dev.bat` |

Run each script from inside its own folder (`cd astron/darwin` and so on): the
scripts `cd` back to the right place themselves. The prompts all have defaults,
so you can press Enter through them.

### Starting by hand

If you'd rather not use the scripts, these are the same commands. Run every
Python process from the **repository root**, because the config paths are
relative to it.

```bash
cd astron && ./astrond --loglevel debug config/astrond.yml
```

```bash
python3 -m pirates.uberdog.ServiceStart --base-channel 1000000 --max-channels 999999 --stateserver 10000 --astron-ip 127.0.0.1:7199 --eventlogger-ip 127.0.0.1:7197
```

```bash
python3 -m pirates.ai.ServiceStart --base-channel 401000000 --max-channels 999999 --stateserver 10000 --district-name Abassa --astron-ip 127.0.0.1:7199 --eventlogger-ip 127.0.0.1:7197
```

```bash
POC_TOKEN=yourname POC_GAMESERVER=127.0.0.1 GAME_ENVIRONMENT=DEV python3 -m pirates.piratesbase.PiratesStart
```

The AI is ready once it logs that its district is up and the world has finished
loading. Loading every island takes a little while the first time.

### More than one district

Start another AI with a different `--district-name` **and** a different
`--base-channel`, for example `402000000`. Two AIs on the same base channel
collide.

## 5. Log in

The client asks for a username (`POC_TOKEN`). On a local server there are no
passwords: the developer account database (`accountdb-type developer`) creates
the account the first time you log in with a new name. Every developer account
gets access level 600, so you can use all the [magic words](magic-words.md).

Pick a district, make a pirate, and the tutorial starts. [Playing](playing.md)
walks through it.

## Ports

| Port | What | Bound to |
|---|---|---|
| 6667 | Client agent, where the game client connects | `0.0.0.0` |
| 7199 | Message director, where the UberDOG and AIs connect | `127.0.0.1` |
| 7197 | Event logger | `127.0.0.1` |
| 6484 | UberDOG RPC server | whitelisted to `127.0.0.1` |

To let friends on your network join, they set `POC_GAMESERVER` to your machine's
address and you open port 6667. Everything else stays local.

## Where the data lives

| Path | What |
|---|---|
| `astron/databases/astrondb/` | Astron's YAML database: accounts, pirates, inventories, ships. |
| `astron/databases/account-bridge`, `guilds`, `player-friends`, … | UberDOG `semidbm` stores. |
| `astron/logs/events-*.log` | Event log: logins, magic words, suspicious activity. |
| `local/holiday-state` | Holidays that are running. |

To wipe the server and start fresh, stop everything and empty those
directories. Keep a copy first if there are pirates you care about.

## Next steps

- [Playing](playing.md): the tutorial, the opening quests, ships.
- [Configuration](configuration.md): `config/personal.prc`, skipping the tutorial, graphics.
- [Troubleshooting](troubleshooting.md): what to do when something won't start.

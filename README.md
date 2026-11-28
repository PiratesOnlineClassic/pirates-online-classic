<p align="center">
  <img src=".github/logo.png" alt="Pirates Online Classic Logo">
</p>

<h1 align="center">Pirates Online Classic</h1>

<p align="center">
  A fan-made revival of Disney's Pirates of the Caribbean Online, as it played in 2007.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/engine-Panda3D%201.10-green.svg" alt="Panda3D 1.10">
</p>

---

Disney shut Pirates of the Caribbean Online down in 2013. This project runs the
original game client against a server rebuilt from scratch: the AI and UberDOG
were reverse-engineered from the client's own code and its network definitions,
and they run on [Astron](https://github.com/Astron/Astron), an open-source
version of the server technology the game was built on.

You can run the whole thing on one computer and play: make a pirate, play the
tutorial, sail, fight, quest and level up.

<p align="center">
  <img src="screenshots/Screenshot%202026-02-01%20at%209.07.34%E2%80%AFPM.png" alt="Screenshot 1" width="800">
</p>

## Quick start

You need **Python 3.9+**, **Git**, and the tools to build Astron (**CMake**, a
**C++ compiler** and **Boost**). [docs/setup.md](docs/setup.md) has every step in
detail, including Windows and Linux.

**1. Get the code, with the game resources next to it.**

```bash
git clone https://github.com/PiratesOnlineClassic/pirates-online-classic.git
```

```bash
git clone https://github.com/PiratesOnlineClassic/poc-resources.git resources
```

**2. Install the Python packages** (from inside `pirates-online-classic/`):

```bash
python3 -m pip install -r requirements.txt
```

**3. Build [our Astron fork](https://github.com/PiratesOnlineClassic/Astron)**
and copy the `astrond` binary into `astron/`.

**4. Start the servers in this order**, each in its own terminal, waiting for
each to finish starting:

| | macOS | Linux | Windows |
|---|---|---|---|
| 1. Astron | `astron/darwin/start_astron.command` | `astron/linux/start_astron.sh` | `astron\win32\start_astron.bat` |
| 2. UberDOG | `astron/darwin/start_uberdog.command` | `astron/linux/start_uberdog.sh` | `astron\win32\start_uberdog.bat` |
| 3. AI | `astron/darwin/start_ai.command` | `astron/linux/start_ai.sh` | `astron\win32\start_ai.bat` |
| 4. Game | `darwin/start_game.command` | see [setup](docs/setup.md#starting-by-hand) | `win32\start_dev.bat` |

> [!IMPORTANT]
> Start the UberDOG **before** the AI. If you don't, the AI's district never
> shows up in the shard list.

**5. Log in** with any username; there's no password on a local server. Your
account is created on first login and given full developer access, so every
[magic word](docs/magic-words.md) works.

## Playing

Make a pirate and you start in the tutorial on Rambleshack. You break out of
jail, collect your sea chest from Doggerel Dan, sail with Captain Bo Beck, sink
an undead ship at cannon practice and meet the Jolly Roger, then land in Port
Royal for the main story. [docs/playing.md](docs/playing.md) covers the controls
and walks through the opening quests.

Quick tips:

- Follow the **ray of light** to your active quest.
- **`Tab`** opens your sea chest, **`R`** auto-runs, **`Ctrl`** attacks.
- Type **`~run`**, **`~god`**, **`~gold 10000`** or **`~tp Tortuga`** in chat
  while testing.
- To skip the tutorial while developing, put `skip-tutorial #t` and
  `force-tutorial-complete #t` in `config/personal.prc`.

## Documentation

| | |
|---|---|
| [Setup](docs/setup.md) | Installing, building Astron, starting the servers, ports, where data lives |
| [Playing](docs/playing.md) | Controls, the tutorial, the opening quests, ships |
| [Configuration](docs/configuration.md) | `config/personal.prc` and the settings worth knowing |
| [Magic words](docs/magic-words.md) | Every in-game admin command |
| [Troubleshooting](docs/troubleshooting.md) | Fixes for common problems, and known issues |
| [Architecture](docs/architecture.md) | How the client, Astron, the UberDOG and the AI fit together |
| [Development](docs/development.md) | Code rules, tests, commits, branches, project layout |

## Contributing

Bug reports and pull requests are welcome. Read [development](docs/development.md)
first. In short: the original client is the spec, new code should read like the
original developers wrote it, and every change comes with a test
(`python3 -m pytest -q`).

- Report bugs and ask for features in [Issues](https://github.com/PiratesOnlineClassic/pirates-online-classic/issues).
- Send changes as [pull requests](https://github.com/PiratesOnlineClassic/pirates-online-classic/pulls).

## Disclaimer

This is a non-commercial fan project made for education and preservation.
Pirates of the Caribbean is a trademark of Disney. This project is not
affiliated with, endorsed by or connected to The Walt Disney Company.

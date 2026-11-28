# Configuration

The game and the servers are configured with Panda3D `.prc` files in `config/`.
Each line is `setting value`, `#t`/`#f` are true/false, and a `#` starts a
comment.

## Which files load

| Process | Loads, in order |
|---|---|
| Client (`pirates.piratesbase.PiratesStart`) | `general.prc`, `dev.prc`, `performance.prc`, then `personal.prc` |
| UberDOG and AI (`ServiceStart`) | `general.prc`, `dev.prc`, `server.prc`, then `personal.prc`, then the command-line options |

A setting that appears in a later file wins. **Put your own changes in
`config/personal.prc`.** It's git-ignored, loads last, and is read by the client
and both servers, so it overrides everything without leaving you with a dirty
checkout. Create it if it doesn't exist.

Restart the process after changing a setting. The client and servers only read
these files at startup.

## The tutorial

| Setting | Default | Effect |
|---|---|---|
| `skip-tutorial` | `#f` | New pirates skip the tutorial and start in Port Royal. |
| `force-tutorial-complete` | `#f` | Treat every pirate as having finished the tutorial. |
| `force-tutorial` | `#t` in `general.prc`, `#f` in `dev.prc` | Always run the tutorial for new pirates. |

To skip the tutorial while developing, put this in `personal.prc`:

```
skip-tutorial #t
force-tutorial-complete #t
```

## Accounts and access

| Setting | Where | Effect |
|---|---|---|
| `accountdb-type` | `server.prc` | `developer` (default): log in with any username, no password, and the account is created on first login. `remote` checks tokens against an account server. |
| `want-dev-access` | `dev.prc` | `#t` gives developer accounts access level 600, which unlocks every [magic word](magic-words.md). |
| `min-access-level` | | Raises every account to at least this access level. |
| `want-membership` | `general.prc` | `#f` (default) gives everyone Unlimited Access. `#t` turns on the Freebooter (Basic Access) limits. |
| `default-account-access` | | With membership on, the access new accounts get (for example `FULL`). |

## World and NPCs

| Setting | Default | Effect |
|---|---|---|
| `want-townfolk` / `want-enemies` / `want-animals` | `#t` | Spawn that kind of NPC. Turn them off for a faster AI start while you work on something else. |
| `want-random-bosses` | `#f` in `dev.prc` | Let ordinary spawns occasionally roll a boss. |
| `want-island-barriers` | `#t` | The invisible walls around islands. |
| `disable-blockers` | `#t` in `dev.prc` | Turn off the quest blockers that fence off areas until you reach that point in the story. |
| `teleport-all` | `#f` | Client: teleport to any island from the map, even before Tia Dalma's compass. |
| `want-rpc-server` / `rpc-port` | `#t` / `6484` | The UberDOG's local RPC endpoint. |

## Graphics and performance (client)

| Setting | Default | Effect |
|---|---|---|
| `win-size` | `800 600` | Window size. |
| `fullscreen` | `#f` | Fullscreen. |
| `want-seapatch` | `#t` | Animated ocean. It costs the most frame time in Port Royal, so turn it off if you're short on FPS. |
| `want-low-end-water` | `#f` | A cheaper ocean. |
| `want-shaders` / `want-grass` / `want-particles` | `#t` | Shader effects, grass and particle effects. |
| `want-avatar-shadows` | `#t` | Shadows under pirates. |
| `clock-frame-rate` | `120` | Frame rate cap. |
| `load-display` | `pandagl` | Graphics backend. |

Many of these can also be changed in-game under **Options**, which saves them to
`game_options.txt`.

## A known Panda3D crash

On some machines the client, and occasionally the AI, crashes with assertion
spam from `simpleHashMap.I` / `renderAttrib.cxx`, ending in
`RenderState.garbageCollect`. Until the root cause is fixed, this
`personal.prc` workaround stops it:

```
uniquify-states #f
uniquify-transforms #f
state-cache #f
garbage-collect-states #f
```

It costs a little memory and some performance. Remove it once the fix lands.

## Environment variables (client)

| Variable | Meaning |
|---|---|
| `POC_TOKEN` | Your username (play token). |
| `POC_GAMESERVER` | Address of the client agent, `127.0.0.1` for a local server. Port 6667 is the default. |
| `GAME_ENVIRONMENT` | `DEV` on local and development servers; adds the in-game feedback (?) button. |
| `GAME_SHOW_ADDS` | `NO` hides the membership upsell popups. |

The launch scripts in `darwin/` and `win32/` set these for you.

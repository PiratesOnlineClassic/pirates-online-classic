# Troubleshooting

When something breaks, look at the terminal of the process that broke first:
Astron, the UberDOG, the AI or the client. Most problems show up there as a
Python traceback or a warning. Logins, magic words and anything flagged as
suspicious are also written to `astron/logs/events-*.log`.

## Starting up

**`Failed to locate prc config/general.prc`, or the game ignores your settings**
: Run the Python processes from the repository root. The config paths are
  relative to it, and the launch scripts `cd` there for you.

**Astron exits straight away with an address already in use error**
: An old `astrond` is still running. Stop it, or find what's on the port with
  `lsof -i :7199` (macOS/Linux) or `netstat -ano | findstr 7199` (Windows).

**The UberDOG or the AI can't connect**
: Astron must be running first, on `127.0.0.1:7199`. Check the `--astron-ip`
  you passed.

**The district list is empty, or the AI's district never appears**
: The UberDOG has to be running *before* the AI starts. Stop the AI, check the
  UberDOG is up, and start the AI again.

**Two AIs fight over objects or crash each other**
: Every AI needs its own `--base-channel`, for example `401000000` and
  `402000000`.

## Connecting and logging in

**The client can't connect**
: Check `POC_GAMESERVER` points at the machine running Astron, and that port 6667
  is reachable (`0.0.0.0:6667` in `astron/config/astrond.yml`).

**Strange disconnects or field errors right after updating the code**
: The client and the servers must use the same `astron/dclass/*.dc` files. The
  client agent doesn't compare dc hashes (`send_hash: false`), so a mismatch
  shows up as odd errors instead of a clean refusal. Restart Astron, the
  UberDOG, the AI and the client after you pull.

**A connection error while waiting to start the tutorial**
: Only one pirate can be in the tutorial at a time. Others wait for up to two
  minutes, then get an error. Try again once the other player is through, or
  turn the tutorial off for testing (see [configuration](configuration.md#the-tutorial)).

## In the game

**The world is grey or missing models, or the log says `Couldn't load file`**
: The resources aren't where the client looks for them. They belong in
  `../resources` next to the repository, or set `model-path` in
  `config/personal.prc`.

**Assertion spam from `simpleHashMap.I` / `renderAttrib.cxx` ending in a crash in `RenderState.garbageCollect`**
: A Panda3D render state cache problem. Use the `personal.prc` workaround in
  [configuration](configuration.md#a-known-panda3d-crash).

**Low frame rate, especially in Port Royal**
: The animated ocean is the main cost. Try `want-seapatch #f` or
  `want-low-end-water #t`, and turn down the in-game Options.

**"Trade timeout!" when buying a ship**
: The shipwrights only sell ships to pirates who have finished the Visit Darby
  Drydock quest, which grants the new ship token. A pirate that got past Darby
  without the token (older builds could skip it) can be fixed with
  `~givePlayerStack 13402 1`.

**Darby Drydock doesn't give you anything**
: He only builds your first ship while Visit Darby Drydock is your active quest.
  Check your quests with `~quests`. Skipping it with `~skipQuest` still grants
  the ship token but not the free ship, so buy one from a shipwright.

**Stuck behind an invisible wall or a quest blocker**
: `disable-blockers #t` turns the quest blockers off, and `~dropBlockers` stashes
  the ones already loaded on your client.

## Resetting

Stop everything, then empty `astron/databases/astrondb/` and delete the
UberDOG stores next to it (`account-bridge`, `guilds`, `player-friends`,
`accessories-bridge`, `code-redemption-bridge`). Back them up first if there
are pirates worth keeping.

## Known issues

These are open:

- The tutorial's undead ship doesn't fire back or carry a deck crew yet.
- The Black Pearl treasure map's sea stages haven't been fully played through
  on a live server.
- Ship parts that arrive on a client before their ship can log a
  `DistributedShippart` `KeyError`.
- Frame drops in Port Royal (see above).

If you hit something else, [open an issue](https://github.com/PiratesOnlineClassic/pirates-online-classic/issues)
with the traceback and the steps that led to it.

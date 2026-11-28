# How the server fits together

Pirates of the Caribbean Online was built on Disney's OTP (Online Theme Park)
framework, the same distributed-object system as Toontown. The client we have is
the original game's code. The servers are a reconstruction, written from what
that client sends and expects, and they run on [Astron](https://github.com/Astron/Astron),
an open-source take on Disney's OTP server.

```
               ┌────────────────────────── Astron (astrond) ─────────────────────────┐
 game client ──┤ client agent :6667 ── message director :7199 ── state server, db,   │
   (Panda3D)   │                                                 dbss, event logger  │
               └─────────────────────────────────┬───────────────┬───────────────────┘
                                                 │               │
                                            UberDOG          AI (one per district)
                                     accounts, friends,      the world: islands, NPCs,
                                     guilds, inventory,      combat, quests, ships,
                                     ships, travel           the tutorial
```

| Process | Code | Job |
|---|---|---|
| Astron | `astron/` (config, dc files, databases) | Routes every message, stores objects (state server), persists them (database + dbss), and talks to clients (client agent). |
| UberDOG | `pirates/uberdog/ServiceStart.py` | Global services that span districts. |
| AI | `pirates/ai/ServiceStart.py` | One district (shard): the whole game world and its rules. |
| Client | `pirates/piratesbase/PiratesStart.py` | The original game. |

## Distributed objects

Everything shared over the network is a distributed object, declared in
`astron/dclass/otp.dc` and `astron/dclass/pirates.dc`. A dc class lists fields,
and each field's keywords say who may send it and who receives it:

| Keyword | Meaning |
|---|---|
| `required` / `ram` / `db` | Part of the object's state, kept in RAM and, with `db`, saved to the database. |
| `broadcast` | Sent to every client that can see the object. |
| `airecv` | The AI (or UberDOG) receives it. |
| `clsend` | Any client may send it. Treat it as untrusted input. |
| `ownsend` / `ownrecv` | Only the object's owner sends or receives it. |

Each object has a Python class per side, picked by suffix from the dc import
line, for example `from pirates.ship import PlayerShip/AI/UD/OV`:

| Suffix | Lives on |
|---|---|
| *(none)* | the client |
| `AI` | the AI |
| `UD` | the UberDOG |
| `OV` | the client, as the owner's private view (your own pirate, your own ships) |

So `PlayerShip.py` is what clients draw, `PlayerShipAI.py` is the authority
that sails and fights, `PlayerShipUD.py` creates it in the database, and
`PlayerShipOV.py` is what the owner sees in their ship list. A field sent from the AI with `sendUpdate('setHp', ...)`
arrives on the client as a call to `setHp(...)`.

Objects sit in a tree: every object has a parent and a zone. A client is told
about an object when it has *interest* in that object's parent and zone. Islands
and the ocean are split into Cartesian grids (Panda3D's
`direct.distributed.DistributedCartesianGrid`, used by the island and ocean
classes in `pirates/world/`), so as you move, the AI's
`WorldGridManagerAI` moves your interest to the cells around you, and you only
receive what's nearby.

## The UberDOG

The UberDOG runs the services listed under `uberdogs:` in
`astron/config/astrond.yml`. Each one has a fixed doId:

| Object | doId | Does |
|---|---|---|
| `ClientServicesManager` | 4665 | Login, the pirate list, creating, naming and deleting pirates. |
| `DistributedAvatarManager` | 4674 | Pirate slots and names. |
| `DistributedInventoryManager` | 4677 | Inventories (gold, weapons, ships, quest items). |
| `DistributedTravelAgent` | 4679 | Moving pirates between districts. |
| `DistributedChatManager` | 4681 | Chat routing and moderation. |
| `PCAvatarFriendsManager` / `PCPlayerFriendsManager` | 4686 / 4687 | Pirate friends and account friends. |
| `CentralLogger` | 4688 | Event logging. |
| `DistributedMatchMaker` | 4700 | Matchmaking for parlor games and activities. |
| `GuildManager` | 4701 | Guilds. |
| `CodeRedemption` | 4703 | Redeeming codes. |
| `PiratesSettingsMgr` | 4704 | Server-wide settings. |

The ship loader (`DistributedShipLoaderUD`) creates player ships and their parts
in the database.

## The AI

`pirates/ai/PiratesAIRepository.py` starts the district and its managers. The
most important ones:

| Attribute | Class | Does |
|---|---|---|
| `worldCreator` | `WorldCreatorAI` | Loads the world files (islands, interiors, spawn points) the same way the client does. |
| `worldGridManager` | `WorldGridManagerAI` | Interest in the grids as pirates move. |
| `teleportMgr` | `DistributedTeleportMgrAI` | Teleports, instances, the jail. |
| `tutorialManager` | `PiratesTutorialManagerAI` | Runs the tutorial for one new pirate at a time. |
| `questMgr` | `QuestManagerAI` | Quest ladders, tasks, rewards and finalize scenes, driven by `pirates/quest/QuestDB.py`. |
| `enemySpawner` | `DistributedEnemySpawnerAI` | Townsfolk, enemies, animals and bosses. |
| `battleMgr` | `BattleManagerAI` | Combat: skills, damage, range checks. |
| `shipManager` | `ShipManagerAI` | Deploying player ships and spawning NPC ships. |
| `tradeMgr` | `TradeManagerAI` | Handing items and gold to pirates. |
| `timeOfDayMgr`, `newsManager` | | Day and night, holidays. |
| `magicWords` | `PiratesMagicWordManagerAI` | [Magic words](magic-words.md). |

Instances (`pirates/instance/`) are separate world copies for the tutorial,
treasure maps such as the Black Pearl, jail and parlor games.

## Where to start reading

| To understand | Read |
|---|---|
| What a client can ask for | `astron/dclass/pirates.dc` |
| The client side of a feature | the class without a suffix, for example `pirates/npc/DistributedNPCTownfolk.py` |
| The server side | the `AI`/`UD` class next to it |
| Quests | `pirates/quest/QuestDB.py`, `QuestLadderDB.py`, `QuestManagerAI.py` |
| NPC dialog scripts | `QuestScripts.txt` in the resources (`phase_3/etc/`) |
| World layout | the world `.py` data files in `pirates/leveleditor/worldData/` |

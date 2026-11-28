# Magic words

Magic words are chat commands for developers and game masters. Type them into
the chat box and press Enter.

| Prefix | Applies to |
|---|---|
| `~word` | yourself |
| `~~word` | the pirate whose nametag you last clicked (yourself if none) |

Arguments are separated by spaces, for example `~gold 5000`, `~tp Tortuga` or
`~level 13703 10`. The reply shows up as a `Spellbook:` speech bubble over your
pirate.

## Who can use them

Every command has an access level, and your account needs at least that level.
On a local server, `config/dev.prc` sets `want-dev-access #t`, which gives every
developer account access level 600 when it logs in. That level unlocks
everything below. Use `~showAccess` to see your level and `~access <level>` to
change it.

| Level | Category |
|---|---|
| 200 | Tester |
| 300 | Moderation |
| 400 | Game master |
| 500 | Lead game master |
| 600 | System admin |

"Runs on" says where the command is handled. Client commands only change what
your own game shows. Server commands change the shared world and are written to
the event log in `astron/logs/`.

## Handy commands while testing

| Goal | Command |
|---|---|
| Move faster on foot | `~run` (toggle), `~turbo` |
| Can't die | `~god` or `~immortal` |
| Money | `~gold 10000` |
| Jump to a place | `~tp Port Royal`, `~tp Tortuga`, `~areaTeleport <uid>` |
| Skip the step of the main story you're on | `~skipQuest` |
| See your active quests | `~quests` |
| Level a weapon or notoriety | `~level <repType> <level>`, `~rep <repType> <amount>` |
| Get every weapon | `~maxWeapons`, then `~maxSP` for skill points |
| Fight something | `~spawn <spawnable>`, `~spawnShip <shipClass>` |
| Ship trouble | `~repairShip`, `~sinkShip`, `~kraken` |
| Time of day | `~tod <state>` |
| Frame rate meter | `~fps` |

Arguments are numbers wherever the game uses ids:

| Reputation (`repType`, from `InventoryType` in `pirates/uberdog/UberDogGlobals.py`) | Id |
|---|---|
| Notoriety (`OverallRep`) | 13700 |
| Cutlass / Pistol / Musket / Dagger / Grenade | 13703 / 13704 / 13705 / 13706 / 13707 |
| Staff (`WandRep`) / Doll | 13708 / 13709 |
| Cannon / Sailing | 13711 / 13712 |

| Ship class (`pirates/ship/ShipGlobals.py`) | Id |
|---|---|
| Light sloop / galleon / frigate (`INTERCEPTORL1`, `MERCHANTL1`, `WARSHIPL1`) | 1 / 11 / 21 |
| Navy Ferret / Navy Panther | 80 / 88 |
| EITC Sea Viper | 100 |
| Skeleton Phantom (the tutorial's undead ship) | 120 |

`~docs` writes the full list of commands to a CSV file, on the client or the
server.

## Full reference

This list was generated from the `@magicWord` declarations in the code.

## Moderation (access 300)

| Command | Arguments | Runs on | What it does |
|---|---|---|---|
| `~kick` | `name` | server | Disconnects the player with the given name or avatarId from the game |
| `~setGMTag` | `gmNameTagState` `gmNameTagColor` `gmNameTagString` | server | Sets your GM nametag properties |
| `~toggleGM` |  | server | Toggles your GM name tag |

## Game master (access 400)

| Command | Arguments | Runs on | What it does |
|---|---|---|---|
| `~goto` | `name` | server | Teleports the invoker to the player with the given name or avatarId |
| `~holidays` |  | server | Lists the currently active holidays |
| `~players` |  | server | Lists the players currently on this district |
| `~siege` | `pvpEnabled` | server | Enables or disables privateer siege pvp on this district |
| `~summon` | `name` | server | Teleports the player with the given name or avatarId to the invoker |
| `~tod` | `state` `cycleDuration` | server | Sets the district's time of day state and optionally the cycle duration |

## System admin (access 600)

| Command | Arguments | Runs on | What it does |
|---|---|---|---|
| `~access` | `access` | server | Interface for manually verifying or changing your ingame access level |
| `~alight` | `red` `green` `blue` | client | Sets the alight value of the scene |
| `~analyze` |  | client | Returns a string of analytic scenegraph data |
| `~areaTeleport` | `locationUid` | server | Teleports the target based off a locations uniqueId |
| `~axis` |  | client | Loads in the XYZ axis model |
| `~badDelete` |  | client | Performs a bad delete operation |
| `~battleRandom` | `command` | client | Shows the client battle random counter, `resync` resets it |
| `~blackpearl` |  | client | Teleports the local avatar to the Black Pearl treasure map instance. |
| `~blackpearlai` |  | server | Creates and teleports the invoker to a Black Pearl treasure map instance. |
| `~bonfire` |  | client | Spawns a bonefire particle effect where the player is standing |
| `~bpdestroy` | `barricadeId` | server | Destroy a barricade in the Black Pearl instance (0-4). |
| `~bpstate` | `state` | server | Set the Black Pearl instance state. |
| `~camerafar` | `far` | client | Sets the cameras far value |
| `~clearAxis` |  | client | Clears the loaded axis models |
| `~clientcrash` |  | client | Simulates a client crash |
| `~clouds` | `level` | client | Locally sets the timeOfDayManager cloud state |
| `~crewtut` |  | client | Displays the unused original crew tutorial |
| `~cutscene` | `csId` | client | Plays the requested cutscene id |
| `~darkfog` |  | client | Toggles the dark fog particle effects |
| `~deployShip` | `shipIndex` | client | Deploys the users requested ship index |
| `~detectleaks` |  | client | Starts the client leak detector |
| `~disconnect` |  | client | Disconnects from the Client Agent |
| `~displayMessage` | `messageId` | server | Broadcasts a news manager message by id to the district |
| `~dlight` | `red` `green` `blue` | client | Sets the dlight value of the scene |
| `~dna` | `dnaType` `val` | server | Changes one of the target's DNA values (`hair`, `mustache`, ...) |
| `~docs` |  | client + server | Generates helpful documentation regarding available client commands in a CSV file |
| `~dropAllQuests` |  | server | Drops every active quest |
| `~dropBlockers` |  | client | Stashes all blocker nodes in the scene |
| `~dropQuest` | `questId` | server | Drops the given quest (defaults to the active quest) |
| `~dumpinstance` |  | client | Dumps the current instance object to a BAM file |
| `~dust` |  | client | Spawns dust particles at the players location |
| `~explorer` |  | client | Toggles the direct explorer. |
| `~fireworks` | `showType` | client | Locally enables or disables Fourth of July fireworks |
| `~flush` |  | client | Flushes all client data caches |
| `~fogColor` | `red` `green` `blue` | client | Sets the local fog's color |
| `~fogDensity` | `density` | client | Sets the local fog's density |
| `~forceLod` |  | client | Forces all LOD states to the highest |
| `~fps` |  | client | Toggle frame rate meter on or off. |
| `~givePlayerStack` | `stackId` `amount` | server | Sets an inventory stack (an `InventoryType` id) to the given amount |
| `~givePork` |  | server | Gives 10 pork chunks |
| `~giveQuest` | `questId` | server | Gives the quest with the given `QuestDB` id |
| `~god` |  | server | Toggles the targets god mode, a god is immortal and fully healed |
| `~gold` | `amount` | server | Gives you gold |
| `~guildname` | `name` | server | Sets your guild name |
| `~hideCams` |  | client | Hides all the area live cameras |
| `~hp` | `hp` | server | Sets the targets current HP |
| `~idTags` |  | client | Enables idTags |
| `~immortal` |  | server | Toggles immortality on yourself |
| `~islandShips` | `state` | client | Toggles the flat ships shown around islands |
| `~jobMgr` |  | client | Logs the client's job manager |
| `~jobtime` | `time` | client | Sets the client jobMgr timeslice |
| `~joincrew` |  | client | Requests a new crew with the crew manager |
| `~kraken` |  | server | Summons the kraken to attack the invoker's ship, or sends it back to the deep if it is already attacking |
| `~level` | `repType` `level` | server | Sets the invokers level |
| `~lfa` | `activityName` | client | Requests the avatars current activity |
| `~liveCam` | `camNum` | client | GameMaster Utility for viewing points of interest around a game area |
| `~location` |  | server | Returns the avatar's current parentId and zoneId |
| `~lookoutStatus` |  | server | Prints the status of the lookout's queue on the UberDOG |
| `~mario` |  | client | Toggles the local client's Mario mode |
| `~maxHp` | `maxHp` | server | Sets the targets max HP |
| `~maxMojo` | `maxMojo` | server | Sets the targets max Mojo |
| `~maxSP` |  | server | Gives 255 unspent skill points in every weapon |
| `~maxWeapons` |  | server | Gives you the best weapon of every type |
| `~messenger` |  | client | Logs the client messenger |
| `~model` | `path` | client | Loads a model into the world locally |
| `~mojo` | `mojo` | server | Sets the targets Mojo level |
| `~name` | `name` | server | Sets the targets name |
| `~nameTags` |  | client | Disables idTags |
| `~net` |  | client | Pulls or restores the client network plug (simulates a disconnect) |
| `~objectcount` |  | client | Logs the clients DO count |
| `~oobe` |  | client | Toggles OOBE mode |
| `~oobeCull` |  | client | Toggles OOBE Cull mode |
| `~pilot` |  | client | Takes the wheel of the closest ship |
| `~placer` |  | client | Toggles the direct placer. |
| `~pvp` | `gameStyle` `opponentId` | server | Starts a pvp game of the given style for the target, optionally against an opponent |
| `~pvpmoney` |  | client | Shows the users pvp infamy details |
| `~quests` |  | server | Lists the targets active quests |
| `~rain` |  | client | Toggles local rain state |
| `~removeGold` | `amount` | server | Takes gold away from you |
| `~removeGroggy` |  | server | Removes the invokers groggy effect |
| `~rep` | `repType` `amount` | server | Gives the target an amount of reputation in the given InventoryType category |
| `~repairShip` |  | server | Fully repairs the hull and sails of the ship the invoker is aboard |
| `~roll` | `mass` `roll` | client | Sets a ships fake mass and adds a roll value |
| `~ru` |  | client | Toggles the local radar utility |
| `~run` |  | client | Toggles the debug running on/off |
| `~setDoubleXP` | `val` | server | Gives the target a double XP reward for the given number of minutes |
| `~setFounder` | `state` | server | Sets your founder state |
| `~setwave` | `num` `amplitude` `wavelength` `speed` | client | Sets the requested SeaPatch wave settings |
| `~shipModel` | `shipClass` `team` `wantCollisions` | client | Spawns a ship model at the players location |
| `~showAccess` |  | client | Returns the access of the current localAvatar. |
| `~showAvIds` |  | client | Show avId in Nametags. |
| `~showCams` |  | client | Shows all the available live cameras |
| `~showNames` |  | client | Remove avIds in Nametags. |
| `~sinkShip` |  | server | Sinks the ship the invoker is aboard |
| `~skipQuest` | `questId` | server | Force-completes the given quest (defaults to the active quest) |
| `~spawn` | `spawnable` | server | Spawns a non respawning enemy at the invoker's location, see `AvatarTypes.NPC_SPAWNABLES` |
| `~spawnShip` | `shipClass` | server | Spawns an enemy ship of the given ShipGlobals ship class on the ocean |
| `~startHoliday` | `holidayId` `duration` | server | Starts a holiday by id, optionally for a duration |
| `~stayTuned` | `questId` | client | Displays the Stay Tuned popup dialog |
| `~stopHoliday` | `holidayId` | server | Stops a running holiday |
| `~storm` | `grid` | client | Toggles the local storm state |
| `~swamp` |  | client | Toggles swamp particle effects |
| `~sysadmin` | `message` | server | Send a system message to the whole district, prefixed with 'ADMIN:'. |
| `~system` | `message` | server | Send a system message to the whole district |
| `~taskMgr` |  | client | Logs the client's task manager |
| `~taskprofileflush` | `name` | client | Flushes the requested AI task profile |
| `~taskthreshold` | `threshold` | client | Sets the task manager duration threshold |
| `~te` |  | client | Sets the local avatar's teleport out state |
| `~terminator` |  | client | Equips a preset of weapons |
| `~tex` |  | client | Toggles base texture mode |
| `~todpanel` |  | client | Loads the client Time of Day editor panel |
| `~toggle2d` |  | client | Toggles visibility of all aspect2d nodes |
| `~topten` |  | client | Requests the top ten leaderboard for guilds |
| `~tp` | `locationName` | server | Teleport command for teleporting to an object by its location name, e.g. `~tp Tortuga` |
| `~treasuremap` | `mapId` | server | Start a treasure map instance |
| `~turbo` |  | client | Toggles the local avatar's turbo mode |
| `~tutorial` | `state` | server | Sets the targets tutorial progress, see PiratesGlobals.TUT_* |
| `~update` | `minutes` | server | Initiate the maintenance message sequence. It lasts the given number of minutes |
| `~walk` |  | client | Sets the local avatar's state to LandRoam |
| `~wave` |  | client | Retrieves current SeaPatch wave settings |
| `~weaponrank` | `rank` | server | Sets your weapon rank to the specified rank (1-6) |
| `~wire` |  | client | Toggles wireframe mode |
| `~world` | `instanceType` `worldName` `locationUid` | server | Teleport command for traveling to different worlds |
| `~zombie` |  | server | Toggles the targets zombie state |

## Adding a magic word

Declare a module-level function with the `@magicWord` decorator from
`otp.ai.MagicWordGlobal`. Put it in an `AI`/`UD` module to run it on the server,
or in a client module to run it locally. Give it a one-line docstring, which
`~docs` and this page use.

```python
from otp.ai.MagicWordGlobal import *

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def hp(hp):
    """
    Sets the targets current HP
    """

    target = spellbook.getTarget()
    target.b_setHp(hp)
    return 'Set HP to %d' % hp
```

`spellbook.getInvoker()` is the pirate who typed the command, and
`spellbook.getTarget()` is the pirate it applies to. The function's return value
is shown to the invoker.

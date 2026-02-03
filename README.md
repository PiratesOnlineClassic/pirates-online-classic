<p align="center">
  <img src=".github/logo.png" alt="Pirates Online Classic Logo">
</p>

<h1 align="center">Pirates Online Classic</h1>

<p align="center">
  A fan-made recreation of Disney's now-defunct MMORPG, Pirates of the Caribbean Online.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11-blue.svg" alt="Python 3.11">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/engine-Panda3D-green.svg" alt="Panda3D">
</p>

---

## 📖 About

Pirates Online Classic is an open-source project dedicated to recreating the beloved Pirates of the Caribbean Online MMORPG that was shut down by Disney in 2013. Our goal is to bring back the nostalgic experience of sailing the Caribbean seas, engaging in ship battles, and exploring the pirate world.

This project is community-driven and welcomes contributions from developers of all skill levels!

### The Reverse Engineering Journey

Recreating a game of this scale required careful reverse engineering of both the client and original server protocols. **The nature of this work meant that systems had to be implemented in a specific order based on dependencies** — you can't test combat without NPCs, you can't spawn NPCs without a world, and you can't load a world without instance management.

Our reverse engineering process followed this general order:

1. **Network Protocol** — Understanding the `.dc` files and Astron message format
2. **Account & Login Flow** — Implementing CSM before anything else could be tested
3. **World Loading** — Basic world instantiation and zone management
4. **Teleportation** — Moving between zones required understanding interest sets
5. **NPC Spawning** — Populating the world with townfolk and enemies
6. **Combat System** — Skill effects, damage calculation, range validation
7. **Quest System** — Discovered extensive server-side logic left in client files
8. **Ship System** — Ocean grids, ship spawning, and naval combat
9. **Cross-Shard Services** — Travel Agent, friends, guilds via UberDOG

Many discoveries were serendipitous — for example, the quest directory contained over 1,400 lines of server-side quest definitions that were never stripped from the client, providing invaluable insight into how the original quest system functioned.

## 📸 Screenshots

<p align="center">
  <img src="screenshots/Screenshot 2026-02-01 at 9.07.34 PM.png" alt="Screenshot 1" width="800">
</p>

<p align="center">
  <img src="screenshots/Screenshot 2026-02-01 at 9.36.30 PM.png" alt="Screenshot 2" width="800">
</p>

<p align="center">
  <img src="screenshots/Screenshot 2026-02-01 at 9.39.45 PM.png" alt="Screenshot 3" width="800">
</p>

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **CMake** - Required for building Astron
- **A C++ Compiler** - GCC (Linux), Clang (macOS), or MSVC (Windows)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/PiratesOnlineClassic/pirates-online-classic.git
cd pirates-online-classic
```

#### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Install Panda3D

This project works with the latest unmodified version of Panda3D. You can install it via pip:

```bash
pip install panda3d
```

Or build from source from the official repository: [https://github.com/panda3d/panda3d](https://github.com/panda3d/panda3d)

#### 4. Clone Game Resources

Clone the resources repository **next to** (not inside) the pirates-online-classic folder:

```bash
cd ..  # Go back to parent directory
git clone https://github.com/PiratesOnlineClassic/poc-resources.git resources
```

Your folder structure should look like this:

```
parent-folder/
├── pirates-online-classic/   # This repository
└── resources/                # Game resources (cloned above)
```

---

## 🔧 Building Astron

Astron is the distributed server architecture that powers Pirates Online Classic. We maintain a custom fork with modifications specific to our project.

### Clone the Astron Repository

```bash
git clone https://github.com/PiratesOnlineClassic/Astron.git
cd Astron
```

### Build on macOS

```bash
mkdir build && cd build
cmake ..
make -j$(sysctl -n hw.ncpu)
```

### Build on Linux

```bash
mkdir build && cd build
cmake ..
make -j$(nproc)
```

### Build on Windows

```powershell
mkdir build && cd build
cmake .. -G "Visual Studio 17 2022"
cmake --build . --config Release
```

### Post-Build

After building, copy the `astrond` executable to the `astron/` directory in this project:

```bash
# macOS/Linux
cp build/astrond ../pirates-online-classic/astron/

# Windows
copy build\Release\astrond.exe ..\pirates-online-classic\astron\
```

---

## 🎮 Running the Game

The servers must be started in a specific order. **UberDOG must be running before the AI server starts**, otherwise no shards will be detected.

### Startup Order

```
1. Astron (Message Director)
2. UberDOG (Global Services) ← Must be running before AI!
3. AI Server (Game World)
4. Client (Game)
```

### 1. Start Astron

First, start the Astron message director:

```bash
./start_astron
```

### 2. Start UberDOG

Next, start the UberDOG server. **This must be running before the AI server or shards won't be detected:**

```bash
./start_uberdog
```

### 3. Start the AI Server

Once UberDOG is running, start the AI server:

```bash
./start_ai
```

### 4. Launch the Client

Finally, open the game client:

```bash
./start_client
```

---

## 🤝 Contributing

We welcome contributions from everyone! Here's how you can help:

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add some amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Pull Request Process

All merges follow a three-step review process:

1. PR is submitted by the creator when changes are ready
2. PR is reviewed by a second contributor
3. PR is reviewed and merged by a third contributor

*For emergency/security fixes, only steps 1 and 2 are required.*

### Commit Guidelines

- **Be descriptive**: Use clear commit messages like `pirates/piratesbase: fix grammar issue with localizer`
- **Keep code clean**: Use spaces instead of tabs, remove extraneous whitespace
- **Add descriptions**: Include commit descriptions when applicable
- **Branch properly**: Create feature branches for substantial changes

### Code Guidelines

- **Do NOT** modify the client to benefit the server — we're creating a server for the client, not a client for the server
- **Retain originality**: Keep the codebase as close to the original as possible
- **No auto-formatters**: The codebase has been manually formatted; do not run autopep or similar tools
- **Don't remove "unnecessary" code**: If it isn't broken, don't fix it

---

## 🌿 Branch Structure

| Branch | Purpose |
|--------|---------|
| `master` | Stable release branch — no direct commits |
| `develop` | Active development, experimental changes, and new features |
| `qa` | Internal testing server for W.I.P features |
| `verify` | Client verification and bytecode matching work |

---

## 📁 Project Structure

```
pirates-online-classic/
├── astron/           # Astron server binaries and configuration
│   ├── config/       # Astron YAML configuration files
│   ├── databases/    # YAML database storage
│   └── dclass/       # Distributed class definitions
├── config/           # Game configuration files (.prc)
├── otp/              # Online Theme Park framework
├── pirates/          # Main game source code
├── libotp/           # OTP library bindings
├── libpirates/       # Pirates-specific library bindings
└── screenshots/      # Game screenshots
```

---

## 🧠 Server Architecture Deep Dive

This section provides an in-depth look at our reverse-engineered server architecture, covering the AI (Artificial Intelligence) server, UberDOG (global services), and the distributed object system.

### Overview: Three-Tier Architecture

Pirates Online Classic uses a distributed architecture consisting of three main server components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Client      │◄──►│     Astron      │◄──►│   AI Server     │
│   (Panda3D)     │    │  (Message Dir)  │    │ (Game Logic)    │
└─────────────────┘    └────────┬────────┘    └─────────────────┘
                                │
                       ┌────────▼────────┐
                       │    UberDOG      │
                       │ (Global Svcs)   │
                       └─────────────────┘
```

1. **Astron** - Message Director and distributed object manager
2. **AI Server** - Game logic, world simulation, NPC behavior
3. **UberDOG (UD)** - Global services like authentication, friends, guilds

---

### AI Server (`pirates/ai/`)

The AI server is the heart of the game — it runs all authoritative game logic, world simulation, NPC behavior, combat resolution, and quest management. Each AI server instance represents one "shard" or "district" that players can join.

#### PiratesAIRepository

The main entry point for the AI server is `PiratesAIRepository`, which inherits from `PiratesInternalRepository`. This class orchestrates the entire game world.

```python
class PiratesAIRepository(PiratesInternalRepository):
    def __init__(self, baseChannel, serverId, districtName):
        # Initializes the zone allocator for dynamic zone management
        self.zoneAllocator = UniqueIdAllocator(
            PiratesGlobals.DynamicZonesBegin,
            PiratesGlobals.DynamicZonesEnd
        )
        self.zoneId2owner = {}  # Track zone ownership
        self.uidMgr = UniqueIdManager(self)  # Unique ID to doId mapping
```

**Key Responsibilities:**
- **Zone Allocation**: Dynamically allocates zones for instances, ships, and game areas using `UniqueIdAllocator`
- **Global Manager Creation**: Spawns all singleton manager objects on startup
- **World Creation**: Initializes the game world through `WorldCreatorAI`
- **Population Tracking**: Monitors shard population via `DistributedPopulationTrackerAI`
- **District Management**: Creates and manages the `PiratesDistrictAI` that represents this shard

#### Startup Sequence

The AI server follows a precise startup sequence:

```python
def handleConnected(self):
    # 1. Allocate our district channel
    self.districtId = self.allocateChannel()
    
    # 2. Create the district object (represents this shard)
    self.distributedDistrict = PiratesDistrictAI(self)
    self.distributedDistrict.setName(self.districtName)
    self.distributedDistrict.generateWithRequiredAndId(...)
    
    # 3. Create all global manager objects
    self.createGlobals()
    
    # 4. Load and spawn the game world
    self.createWorlds()
    
    # 5. Mark district as available for players
    self.distributedDistrict.b_setAvailable(1)
```

#### Global Managers Created

| Manager | Purpose |
|---------|---------|
| `TimeManagerAI` | Server time synchronization with clients |
| `FriendManagerAI` | Friend list operations and online status |
| `QuestManagerAI` | Quest state machines and progression |
| `BattleManagerAI` | Combat resolution, damage calculation, skill effects |
| `EnemySpawnerAI` | NPC spawning, respawning, and holiday-aware behavior |
| `ShipManagerAI` | Player and NPC ship management |
| `TeleportMgrAI` | Cross-instance and cross-shard teleportation |
| `TimeOfDayManagerAI` | Day/night cycle synchronization |
| `NewsManagerAI` | Holiday events and server announcements |
| `TradeManagerAI` | Player-to-player trading |
| `TutorialManagerAI` | Tutorial instance management |
| `WorldGridManagerAI` | Dynamic zone interest for players |
| `TargetManagerAI` | Combat targeting system |
| `BandManagerAI` | Crew/party system |
| `CrewMatchAI` | Crew matchmaking |
| `DiscordNotificationsAI` | Discord webhook integration |

#### Battle Manager

The `BattleManagerAI` handles all combat logic server-side. Combat was one of the more complex systems to reverse-engineer due to the number of interacting components: skills, weapons, status effects, and the Pirate Code.

```python
class BattleManagerBase:
    PirateCodeWeapons = (
        InventoryType.PistolWeaponL1, InventoryType.PistolWeaponL2,
        InventoryType.PistolWeaponL3, InventoryType.PistolWeaponL4,
        InventoryType.PistolWeaponL5, InventoryType.PistolWeaponL6,
        InventoryType.MusketWeaponL1, InventoryType.MusketWeaponL2,
        InventoryType.MusketWeaponL3
    )
    
    def isPVP(self, attacker, target):
        """Check if this is player-vs-player combat"""
        if target and target.getTeam() == PiratesGlobals.PLAYER_TEAM:
            if attacker and attacker.getTeam() == PiratesGlobals.PLAYER_TEAM:
                return True
        return False
    
    def obeysPirateCode(self, attacker, target):
        """Check if attack follows the Pirate Code (no guns vs humans)"""
        if not hasattr(target, 'avatarType'):
            return True
        
        # Zombies are exempt from Pirate Code
        if not target.isNpc and target.zombie:
            return True
        
        # Human types: Navy, Townfolk, Pirates, EITC
        human = (target.avatarType.isA(AvatarTypes.Navy) or 
                 target.avatarType.isA(AvatarTypes.Townfolk) or 
                 target.avatarType.isA(AvatarTypes.Pirate) or 
                 target.avatarType.isA(AvatarTypes.TradingCo))
        
        # Can't use guns against humans
        if human and attacker.currentWeaponId in self.PirateCodeWeapons:
            return False
        
        return True
```

**Hit/Miss Resolution:**

```python
def willWeaponHit(self, attacker, target, skillId, ammoSkillId, charge):
    """Calculate if an attack hits, misses, is dodged, parried, or resisted"""
    chanceOfHit = WeaponGlobals.getAttackAccuracy(skillId, ammoSkillId)
    
    # Apply level-based accuracy modifier
    if target and not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId):
        accuracyModifier = WeaponGlobals.getComparativeLevelAccuracyModifier(
            attacker, target)
        chanceOfHit = max(0.0, chanceOfHit + accuracyModifier)
    
    # Check for debuffs affecting accuracy
    for effect in attacker.getSkillEffects():
        if effect == WeaponGlobals.C_BLIND or effect == WeaponGlobals.C_DIRT:
            chanceOfHit *= WeaponGlobals.BLIND_PERCENT
        elif effect == WeaponGlobals.C_TAUNT:
            chanceOfHit *= WeaponGlobals.TAUNT_PERCENT
    
    # Roll for hit/miss/dodge/parry/resist
    hitRoll = chanceOfHit - attacker.battleRandom.getRandom('accuracy') * 100
    
    if hitRoll < 0:
        return WeaponGlobals.RESULT_MISS
    if dodgeRoll >= 0:
        return WeaponGlobals.RESULT_DODGE
    if parryRoll >= 0:
        return WeaponGlobals.RESULT_PARRY
    if resistRoll >= 0:
        return WeaponGlobals.RESULT_RESIST
    
    return WeaponGlobals.RESULT_HIT
```

**Combat Features:**
- Range validation between attacker and target
- Skill effect queuing with duration tracking
- Weapon ammo type detection (pistol, grenade, cannon, dagger)
- Combo diary tracking for skill chains
- Synchronized random number generation for client prediction

---

### UberDOG Server (`pirates/uberdog/`)

UberDOG (Uber Distributed Object Globals) handles all global services that persist across shards. There is typically only ONE UberDOG server for the entire game cluster.

#### PiratesUberRepository

```python
class PiratesUberRepository(PiratesInternalRepository):
    def handleConnected(self):
        # Create the root directory object
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)
        
        # Start RPC server for external tools
        if config.GetBool('want-rpc-server', True):
            self.rpc = PiratesRPCServiceUD(self)
            self.rpc.start()
        
        self.createGlobals()
```

**Global Services:**

| Service | Description |
|---------|-------------|
| `ClientServicesManager` | Authentication, account creation, avatar management |
| `DistributedInventoryManager` | Persistent inventory storage across sessions |
| `DistributedShipLoader` | Ship data persistence and loading |
| `PCAvatarFriendsManager` | Cross-shard friend lists and online status |
| `PCGuildManager` | Guild creation, membership, and management |
| `DistributedTravelAgent` | Cross-shard teleportation routing |
| `CodeRedemption` | Promo code validation and rewards |
| `CentralLogger` | Centralized event logging |
| `PiratesSettingsMgr` | Server-wide configuration |
| `NewsManagerUD` | Server announcements and holiday sync |
| `DistrictTrackerUD` | Tracks all online shards |

#### Client Services Manager (CSM)

The CSM is the most complex UberDOG service — it handles the entire login and avatar selection flow using finite state machines:

```python
class LoginAccountFSM(OperationFSM):
    def enterStart(self, token):
        self.token = token
        self.demand('QueryAccountDB')
    
    def enterQueryAccountDB(self):
        self.csm.accountDB.lookup(self.token, self.__handleLookup)
    
    def __handleLookup(self, result):
        if self.accountId:
            self.demand('RetrieveAccount')
        else:
            self.demand('CreateAccount')
    
    def enterCreateAccount(self):
        self.account = {
            'ACCOUNT_AV_SET': [0] * 4,  # 4 avatar slots
            'CREATED': time.ctime(),
            'LAST_LOGIN': time.ctime(),
            'ACCESS_LEVEL': self.accessLevel
        }
        self.csm.air.dbInterface.createObject(...)
```

**Login Flow States:**
1. `Start` → Receives login token
2. `QueryAccountDB` → Validates credentials
3. `CreateAccount` OR `RetrieveAccount` → Gets/creates account
4. `StoreAccountID` → Links user ID to account
5. `SetAccount` → Finalizes login, sends avatar list

**Account Database Types:**

| Type | Use Case |
|------|----------|
| `DeveloperAccountDB` | Local dev (auto-creates accounts with access level 600) |
| `LocalAccountDB` | Persistent local accounts (first user gets 700, others 100) |
| `RemoteAccountDB` | Production with AES-128-CBC encrypted tokens |

#### Inventory Manager

The `DistributedInventoryManagerUD` handles all persistent inventory operations:

```python
class InventoryOperationFSM(FSM):
    TIMEOUT_SECONDS = 30.0  # All operations timeout after 30s
    
    def _finish(self, *args, **kwargs):
        # Guaranteed cleanup with timeout cancellation
        taskMgr.remove(self._timeoutTaskName)
        self.manager.avatar2fsm.pop(self.avatarId, None)
        if self.callback:
            self.callback(*args, **kwargs)
```

**Inventory FSM Types:**
- `QueryInventoryFSM` - Fetches inventory ID for an avatar
- `CreateInventoryFSM` - Creates new inventory in database
- `QueryShipInventoryFSM` - Ship-specific inventory queries
| `PCGuildManager` | Guild creation and management |
| `DistributedTravelAgent` | Cross-shard teleportation |
| `CodeRedemption` | Promo code redemption |

#### Client Services Manager (CSM)

The CSM handles the entire login flow:

1. **Account Lookup** - Validates credentials against the account database
2. **Account Creation** - Creates new accounts if needed
3. **Avatar Selection** - Loads pirate avatars for the account
4. **Avatar Creation** - Handles Make-A-Pirate flow
5. **Shard Selection** - Routes player to appropriate game server

**Account Database Types:**
- `DeveloperAccountDB` - For local development (auto-creates accounts)
- `LocalAccountDB` - Persistent local accounts
- `RemoteAccountDB` - Production with encrypted tokens

---

### World System (`pirates/world/`)

The world system manages all game areas, from the open ocean to island interiors. Understanding this system was foundational — it had to be implemented early because nearly every other system depends on having a functioning world to operate within.

#### World Hierarchy

```
DistributedMainWorldAI (piratesWorld)
├── DistributedOceanGridAI (Open Sea)
│   ├── DistributedIslandAI (Port Royal)
│   │   ├── DistributedGameAreaAI (Town Areas)
│   │   │   ├── DistributedGAInteriorAI (Buildings)
│   │   │   └── DistributedBuildingDoorAI (Doors)
│   │   └── DistributedShipDeployerAI
│   └── DistributedIslandAI (Tortuga)
│       └── ...
└── DistributedInstanceWorldAI (Instanced Content)
    └── DistributedPiratesTutorialWorldAI
```

#### WorldCreatorAI

The `WorldCreatorAI` is responsible for parsing world data files and instantiating game objects:

```python
class WorldCreatorAI(WorldCreatorBase, DirectObject):
    def __init__(self, air):
        # Managers for different object relationships
        self.linkManager = LinkManager(self.air)
        self.locatorManager = LocatorManager(self.air)
        self.connectorManager = ConnectorManager(self.air)
        self.movementLinkManager = MovementLinkManager(self.air)
        self.oceanAreaManager = OceanAreaManager(self.air)
```

**Key Managers:**
- **LinkManager** - Manages door/portal connections between areas
- **LocatorManager** - Tracks spawn points and object positions
- **ConnectorManager** - Handles area transitions (tunnels, doors)
- **MovementLinkManager** - AI pathing connections
- **OceanAreaManager** - Defines ocean spawn regions for ships

#### Client-Side Game Areas

The `DistributedGameArea.py` is the client representation of a game area:

```python
class DistributedGameArea(DistributedNode):
    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        self.uniqueId = ''
        self.geom = None
        self.links = []              # Door/portal connections
        self.connectors = {}         # Active connector objects
        self.connectorInterests = set()
        self.envEffects = None       # Environment effects
        self.spawnTriggers = []      # NPC spawn triggers
        self.islandWaterParameters = None
    
    def handleChildArrive(self, childObj, zoneId):
        """Called when an avatar enters this area"""
        DistributedNode.handleChildArrive(self, childObj, zoneId)
        if childObj.isLocal():
            # Refresh quest indicators when entering new area
            childObj.refreshActiveQuestStep()
    
    def handleEnterGameArea(self, collEntry=None):
        """Triggered when player enters the area's collision bounds"""
        # Show area name on HUD
        taskMgr.doMethodLater(1, self.showEnterMessage, 'showEnterMessage')
        
        # Log for analytics
        UserFunnel.logSubmit(0, 'ENTERING_' + str(self.funnelDisplayName))
        
        # Update location code for crash reports
        displayName = PLocalizer.LocationNames.get(self.uniqueId)
        base.setLocationCode(displayName)
```

#### Connector System (Doors & Tunnels)

Connectors enable seamless transitions between areas. When a player approaches a door:

```python
def loadConnectors(self):
    """Load all connectors (doors, tunnels) for this area"""
    for link in self.links:
        if link:
            connectorId = link[0]
            if connectorId not in self.connectorInterests:
                self.connectorInterests.add(connectorId)
                parentId = link[1]
                zoneId = link[2]
                
                # Set interest in the connector's zone
                connectorEvent = 'connector-%s' % connectorId
                self.acceptOnce(connectorEvent, self.reparentConnector, 
                    extraArgs=[connectorId])
                localAvatar.setInterest(parentId, zoneId, 
                    ['Connectors-%s' % self.doId], connectorEvent)

def reparentConnector(self, connectorId):
    """Attach connector to this area once loaded"""
    connector = self.cr.doId2do.get(connectorId)
    if connector:
        self.connectors[connectorId] = connector
        if connector.dclass.getName() == 'DistributedGATunnel':
            connector.reparentConnectorToArea(self)
```

#### Cartesian Grid System

Both oceans and islands use a Cartesian grid for zone management:

```python
# Ocean Grid Configuration
OCEAN_GRID_SIZE = 60
OCEAN_CELL_SIZE = 2000
OCEAN_GRID_RADIUS = 3

# Island Grid Configuration  
ISLAND_GRID_SIZE = 20
ISLAND_CELL_SIZE = 75
ISLAND_GRID_RADIUS = 2
```

The grid system enables:
- **Interest Management** - Players only receive updates for nearby zones
- **Seamless Movement** - Zone transitions happen transparently
- **Scalable Visibility** - Reduces network traffic significantly

#### WorldGridManagerAI

Manages dynamic interest sets for avatars as they move through the world:

```python
class GridInterestHandler:
    def addInterestHandle(self, newZoneId):
        # Adds interest via CLIENTAGENT_ADD_INTEREST
        clientChannel = self.avatar.GetPuppetConnectionChannel(self.avatar.doId)
        self.air.clientAddInterest(clientChannel, context, parentDoId, zoneId)
```

#### Unique ID System

Every game area has a unique string ID used for persistence and teleportation:

```python
def setUniqueId(self, uid):
    """Register this area's unique ID with the UID manager"""
    if self.uniqueId != '':
        self.cr.uidMgr.removeUid(self.uniqueId)
    
    self.uniqueId = uid
    self.cr.uidMgr.addUid(self.uniqueId, self.getDoId())

# Example unique IDs:
# 'port_royal_island' -> Port Royal Island
# 'tortuga_island' -> Tortuga Island  
# 'jail_interior_1' -> Port Royal Jail Interior
```

---

### Instance System (`pirates/instance/`)

Instances are isolated world copies for instanced content like tutorials, treasure maps, and boss encounters. This system had to be implemented before we could test the tutorial flow, which was critical for understanding the early game experience.

#### Instance Types

```python
INSTANCE_NONE = 0       # Invalid/unset
INSTANCE_MAIN = 1       # Main open world
INSTANCE_GENERIC = 2    # Generic private instance
INSTANCE_PG = 3         # Poker Game instance
INSTANCE_TUTORIAL = 4   # Tutorial island
INSTANCE_WELCOME = 5    # Welcome shard
```

#### DistributedInstanceBaseAI

Base class for all instance types, providing spawn point management and world building:

```python
class DistributedInstanceBaseAI(DistributedObjectAI, WorldNodeAI):
    def __init__(self, air):
        self.spawnPts = {}  # Spawn point registry by area
        self.builder = ClientAreaBuilderAI(self.air, self)
    
    def addSpawnPt(self, area, spawnPt, index=None):
        """Registers spawn points for player respawning"""
        if area not in self.spawnPts:
            self.spawnPts[area] = {}
        
        idx = index if index is not None else len(self.spawnPts[area])
        self.spawnPts[area][idx] = spawnPt
    
    def getSpawnPt(self, areaUid, index=0):
        """Get spawn point for a specific area"""
        if areaUid not in self.spawnPts:
            return None
        return self.spawnPts[areaUid].get(index)
    
    def getType(self):
        """Return instance type constant"""
        return INSTANCE_GENERIC
    
    def getFileName(self):
        """Return world file name for loading"""
        return self.fileName
```

#### Tutorial Instance

The tutorial system creates private instances for new players:

```python
class DistributedPiratesTutorialWorldAI(DistributedInstanceBaseAI):
    def __init__(self, air, avatar):
        DistributedInstanceBaseAI.__init__(self, air)
        self.avatar = avatar  # Owner of this tutorial instance
    
    def getType(self):
        return INSTANCE_TUTORIAL
    
    def getFileName(self):
        return 'tutorial_jungle'
    
    def avatarCompletedTutorial(self, avatar):
        """Called when player finishes tutorial"""
        # Set tutorial completion flag
        avatar.b_setTutorial(PiratesGlobals.TUT_COMPLETED)
        
        # Teleport to main world
        self.air.teleportMgr.d_initiateTeleport(
            avatar,
            instanceType=INSTANCE_MAIN,
            instanceName='piratesWorld',
            locationUid='port_royal_island')
        
        # Schedule instance cleanup
        taskMgr.doMethodLater(5.0, self.cleanup, 'tutorial-cleanup')
```

#### Instance Lifecycle

1. **Creation** - Instance created when player requests instanced content
2. **Population** - World builder creates game areas and NPCs
3. **Active** - Players interact within the instance
4. **Cleanup** - Instance deleted when all players leave

```python
def cleanup(self, task=None):
    """Destroy the instance and all contained objects"""
    # Remove all NPCs
    for npc in self.builder.getNPCs():
        npc.requestDelete()
    
    # Remove all game areas
    for area in self.builder.getAreas():
        area.requestDelete()
    
    # Delete self
    self.requestDelete()
    return task.done
```

#### Travel Agent

The teleport and travel system is one of the most complex subsystems in the game, spanning client, AI, and UberDOG components. Understanding how these pieces interact was critical to enabling seamless cross-shard travel.

##### The Complete Teleport Flow

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Client  │───►│ TeleportMgr  │───►│  TravelAgent │───►│ Destination  │
│          │    │    (AI)      │    │    (UD)      │    │   AI Shard   │
└──────────┘    └──────────────┘    └──────────────┘    └──────────────┘
     │                 │                   │                    │
     │ initiateTeleport│                   │                    │
     │────────────────►│                   │                    │
     │                 │ d_requestTeleport │                    │
     │                 │  ToShardAItoUD    │                    │
     │                 │──────────────────►│                    │
     │                 │                   │ requestTeleportTo  │
     │                 │                   │   ShardUDtoAI      │
     │                 │                   │───────────────────►│
     │                 │                   │                    │
     │                 │◄──────────────────┼────────────────────│
     │                 │     setAI (transfer avatar ownership)  │
     │◄────────────────│                   │                    │
     │  teleportHasBegun                   │                    │
```

##### Client-Side Teleport Manager

The `DistributedTeleportMgr.py` on the client handles all teleport initiation, visual effects, and completion:

```python
class DistributedTeleportMgr(DistributedObject):
    def initiateTeleport(self, instanceType, instanceName, shardId=0, locationUid='',
                         instanceDoId=0, doneCallback=None, startedCallback=None, 
                         gameType=-1, friendDoId=0, friendAreaDoId=0, doEffect=True):
        # Exit any current interaction
        currInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if currInteractive:
            currInteractive.requestExit()
        
        # Prevent concurrent teleports
        if self.amInTeleport():
            return
        
        self.setAmInTeleport()
        
        # Send teleport request to AI server
        self.sendUpdate('initiateTeleport', [
            instanceType,
            fromInstanceType,
            shardId,
            locationUid,
            instanceDoId,
            instanceName,
            gameType,
            friendDoId,
            friendAreaDoId])
```

**Client Teleport Types:**
- `localTeleport()` — Same-shard, same-instance teleport (e.g., island to island)
- `localTeleportToId()` — Teleport to a specific object by doId (e.g., to a ship)
- `requestTeleportToAvatar()` — Teleport to a friend's location
- `requestTeleportToIsland()` — Map-based island teleport

The client also handles **visual effects** during teleport:

```python
def localTeleportEffect(self, destPos, destNode):
    # Show fade-out effect
    base.cr.loadingScreen.show(waitForLocation=True)
    
    # Set position after fade
    self.localTeleportingObj.setPosHpr(destPos[0], destPos[1], destPos[2], 
                                        destPos[3], 0, 0)
    self.localTeleportingObj.reparentTo(destNode)
    destNode.addObjectToGrid(self.localTeleportingObj)
```

##### AI-Side Teleport Manager (FSM-Based)

The `DistributedTeleportMgrAI.py` uses finite state machines to manage teleport operations server-side:

```python
class TeleportFSM(FSM):
    """Manages the server-side teleport state machine"""
    
    def __init__(self, air, avatar, world, gameArea, spawnPt):
        FSM.__init__(self, 'TeleportFSM')
        self.air = air
        self.avatar = avatar
        self.world = world
        self.gameArea = gameArea
        self.spawnPt = spawnPt
    
    def enterTeleporting(self):
        # Create temporary teleport zone for the avatar
        zoneId = self.air.allocateZone()
        self.teleportZone = DistributedTeleportZoneAI(self.air)
        self.teleportZone.generateWithRequired(zoneId)
        
        # Create teleport handler to manage avatar transfer
        self.teleportHandler = DistributedTeleportHandlerAI(self.air, self)
        self.teleportHandler.generateWithRequiredAndId(
            self.avatar.doId, self.air.districtId, zoneId)

class DistributedTeleportMgrAI(DistributedObjectAI):
    def d_initiateTeleport(self, avatar, instanceType=None, instanceName=None, 
                           locationUid=None, spawnPt=None):
        # Check for existing teleport
        if avatar.doId in self.avatar2fsm:
            self.notify.warning('Cannot initiate teleport for avatar %d, '
                'already teleporting!' % avatar.doId)
            return
        
        # Handle return location for login teleports
        returnLocation = avatar.getReturnLocation()
        currentIsland = avatar.getCurrentIsland()
        if returnLocation and not currentIsland:
            locationUid = returnLocation
        
        # Lookup the world and game area
        world = self.getWorld(instanceType, instanceName)
        gameArea = world.builder.getObject(uniqueId=locationUid)
        
        # Start the teleport FSM
        self.avatar2fsm[avatar.doId] = TeleportFSM(
            self.air, avatar, world, gameArea, spawnPt)
        self.avatar2fsm[avatar.doId].request('Teleporting')
```

##### Cross-Shard Travel Agent (UberDOG)

The `DistributedTravelAgentUD.py` routes teleport requests between shards. Since UberDOG is a global service, it knows about all active shards:

```python
class DistributedTravelAgentUD(DistributedObjectGlobalUD):
    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        
        # Registry of all active shards: {channel: shardId}
        self.__shards = {}
        
        # Listen for shard registrations
        self.air.netMessenger.accept('registerShard', self, self.addShard)
    
    def getShard(self, shardId):
        """Get the channel for a shard by ID"""
        for channel in self.__shards:
            if self.__shards[channel] == shardId:
                return channel
        return None
    
    def requestTeleportToShardAItoUD(self, avatarId, shardId, instanceType, 
                                      instanceName, locationUid):
        """Route cross-shard teleport from source AI to destination AI"""
        channel = self.getShard(shardId)
        if not channel:
            self.notify.warning('Cannot teleport avatar %d to unknown shard %d!' 
                % (avatarId, shardId))
            return
        
        # Forward to destination shard's AI
        self.sendUpdateToChannel(channel, 'requestTeleportToShardUDtoAI', 
            [avatarId, shardId, instanceType, instanceName, locationUid])
```

##### AI-Side Travel Agent

The `DistributedTravelAgentAI.py` receives cross-shard requests and handles avatar ownership transfer:

```python
class DistributedTravelAgentAI(DistributedObjectGlobalAI):
    def announceGenerate(self):
        # Register this shard with UberDOG on startup
        self.air.netMessenger.send('registerShard', 
            [self.air.ourChannel, self.air.districtId])
    
    def requestTeleportToShardUDtoAI(self, avatarId, shardId, instanceType, 
                                      instanceName, locationUid):
        """Handle incoming cross-shard teleport"""
        
        def avatarArrived(avatar):
            if not avatar:
                self.notify.warning('Invalid avatar generate for %d!' % avatarId)
                return
            
            # Initiate the teleport on this shard
            self.air.teleportMgr.d_initiateTeleport(
                avatar, instanceType, instanceName, locationUid)
        
        # Wait for avatar to arrive on this shard
        self.acceptOnce('generate-%d' % avatarId, avatarArrived)
        
        # Transfer avatar ownership to this AI
        self.air.setAI(avatarId, self.air.ourChannel)
```

##### Teleport to Friend Flow

When teleporting to a friend, the system queries their availability first:

```python
# Client queries friend
def queryAvatarForTeleport(self, avId):
    self.setTeleportQueryId(avId)
    handle = self.cr.identifyAvatar(avId)
    handle.sendTeleportQuery(avId, bandMgr, bandId, guildId, shardId)

# Friend responds with their location
def handleAvatarTeleportQuery(self, requesterId, ...):
    handle.sendTeleportResponse(
        PiratesGlobals.TAAvailable, 
        self.cr.distributedDistrict.doId,      # shardId
        self.cr.getActiveWorld().doId,          # instanceDoId
        localAvatar.getParentObj().doId,        # areaDoId
        sendToId=requesterId)

# Original requester initiates teleport
def handleAvatarTeleportResponse(self, avId, available, shardId, instanceDoId, areaDoId):
    if available == PiratesGlobals.TAAvailable:
        self.requestTeleportToAvatar(shardId, instanceDoId, avId, areaDoId)
```

---

### NPC & Enemy System (`pirates/battle/`, `pirates/npc/`)

The NPC system was one of the later systems to be reverse-engineered, as it required a working world, combat, and quest system first. Understanding how the original game spawned and managed thousands of NPCs across the Caribbean was essential.

#### Spawn Node Architecture

NPCs are spawned from **spawn nodes** defined in world data files. The `SpawnNodeBase` class is the foundation:

```python
class SpawnNodeBase:
    def __init__(self, air, objType, objectData, parent, objKey):
        self.air = air
        self._objType = objType       # 'Spawn Node', 'Creature', etc.
        self._objectData = objectData  # World data dictionary
        self._parent = parent          # Parent game area
        self._objKey = objKey          # Unique spawn key
        self._npc = None               # The spawned NPC object
    
    def processDeath(self):
        """Called when the NPC dies - schedules respawn"""
        if not self._npc:
            return
        
        # Wait 5 seconds before starting respawn process
        taskMgr.doMethodLater(5, self.__respawn, 'perform-respawn-%s' % self.objKey)
    
    def canRespawn(self):
        """Check if NPC can respawn (holiday checks, etc.)"""
        holidayName = self.objectData.get('Holiday', None)
        if holidayName:
            for holidayId, name in list(HolidayGlobals.holidayNames.items()):
                if name == holidayName:
                    return self.air.newsManager.isHolidayActive(holidayId)
            return False
        return True
```

#### NPC Team Assignment

NPCs are assigned to teams for combat targeting:

```python
def getNPCTeam(self, avatarType):
    if avatarType.isA(AvatarTypes.Navy):
        return PiratesGlobals.NAVY_TEAM
    elif avatarType.isA(AvatarTypes.TradingCo):
        return PiratesGlobals.TRADING_CO_TEAM
    elif avatarType.isA(AvatarTypes.Undead):
        if avatarType.isA(AvatarTypes.French):
            return PiratesGlobals.FRENCH_UNDEAD_TEAM
        elif avatarType.isA(AvatarTypes.Spanish):
            return PiratesGlobals.SPANISH_UNDEAD_TEAM
        else:
            return PiratesGlobals.UNDEAD_TEAM
    elif avatarType.isA(AvatarTypes.Creature):
        return PiratesGlobals.UNDEAD_TEAM
    elif avatarType.isA(AvatarTypes.Townfolk):
        return PiratesGlobals.VILLAGER_TEAM
    else:
        return PiratesGlobals.PLAYER_TEAM
```

#### NPC Spawning Process

When a spawn node activates, it creates and configures the NPC:

```python
def __spawn(self, task=None):
    # Create the NPC instance
    avatarType = self.getAvatarType()
    npcCls = self.getNPCClass(avatarType)
    npc = npcCls(self.air)
    
    # Set position and scale from world data
    npc.setScale(self.objectData.get('Scale'))
    sx, sy, sz = self.objectData.get('GridPos', self.objectData.get('Pos', (0, 0, 0)))
    npc.setPos(sx, sy, sz)
    npc.setHpr(self.objectData.get('Hpr', (0, 0, 0)))
    
    # Configure aggro behavior
    aggroRadius = self.objectData.get('Aggro Radius')
    aggroInfo = EnemyGlobals.determineAggroInfo(aggroRadius)
    npc.setAggroMode(aggroInfo[0])
    npc.setAggroRadius(aggroInfo[1])
    
    # Set level and stats
    npc.setLevel(EnemyGlobals.getRandomEnemyLevel(avatarType))
    npcHp, npcMp = EnemyGlobals.getEnemyStats(avatarType, npc.getLevel())
    npc.setMaxHp(npcHp)
    npc.setHp(npcHp)
    
    # Generate in the world
    npc.generateWithRequired(self.parent.zoneId)
    self._npc = npc
```

#### DistributedEnemySpawnerAI

Manages all NPC spawning with support for:

- **Townfolk** - Friendly NPCs for quests and shops
- **Skeletons** - Undead enemies
- **Navy Sailors** - British Navy enemies
- **EITC** - East India Trading Company soldiers
- **Animals** - Wildlife (chickens, pigs, etc.)
- **Creatures** - Special enemies (crabs, bats, scorpions)
- **Boss NPCs** - Elite enemies with special mechanics

```python
# NPC Class mapping
from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.npc.DistributedNPCSkeletonAI import DistributedNPCSkeletonAI
from pirates.npc.DistributedNPCNavySailorAI import DistributedNPCNavySailorAI
from pirates.npc.DistributedBossSkeletonAI import DistributedBossSkeletonAI
from pirates.npc.DistributedBossNavySailorAI import DistributedBossNavySailorAI
from pirates.creature.DistributedAnimalAI import DistributedAnimalAI
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from pirates.creature.DistributedBossCreatureAI import DistributedBossCreatureAI
```

#### Holiday-Aware Spawning

NPCs can be configured to only spawn during specific holidays:

```python
def processHolidayStart(self, holidayId):
    """Spawn holiday-specific NPCs when event starts"""
    if self._npc:
        return  # Already spawned
    
    if self.canRespawn():
        self.notify.debug('Spawning holiday npc for holiday: %s' % holidayId)
        self.__attemptSpawn()

def processHolidayEnd(self, holidayId):
    """Despawn holiday NPCs when event ends"""
    if not self._npc:
        return
    
    if not self.canRespawn():
        self.notify.debug('Despawning holiday npc for holiday: %s' % holidayId)
        self._npc.requestDelete()
        self._npc = None
```

**Supported Holidays:**
- Halloween (special skeleton spawns)
- Christmas (decorations and themed NPCs)
- Mardi Gras (festival NPCs)
- Custom events

---

### Ship System (`pirates/ship/`)

The ship system manages both player-owned vessels and NPC ships across the ocean. This was one of the more challenging systems to reverse-engineer due to its integration with the Cartesian grid, combat, and instance systems.

#### ShipManagerAI

The central manager for all ships in the world:

```python
class ShipManagerAI:
    def __init__(self, air):
        self.air = air
        self.world = None
        
        self.playerShips = set()   # Player-owned ships
        self.npcShips = set()      # NPC enemy ships
        self.flagships = set()     # Boss ships (tracked separately)
        
        # Configuration
        NPCSHIP_POP_UPKEEP_DELAY = 10.0   # Upkeep check interval
        NPCSHIP_POP_MAX = 96              # Max regular NPC ships
        FLAGSHIP_POP_MAX = 24             # Max flagships
        FLAGSHIP_SPAWN_DELAY = 120.0      # Delay between flagship spawns
```

#### Ship Types and Factions

```python
# Navy Ships (British Royal Navy)
REGULAR_NPC_SHIPS = [
    ShipGlobals.NAVY_FERRET,
    ShipGlobals.NAVY_GREYHOUND,
    ShipGlobals.NAVY_PREDATOR,
    ShipGlobals.NAVY_BULWARK,
    ShipGlobals.NAVY_VANGUARD,
    ShipGlobals.NAVY_MONARCH,
    ShipGlobals.NAVY_PANTHER,
    ShipGlobals.NAVY_CENTURION,
    ShipGlobals.NAVY_DREADNOUGHT,
    
    # EITC Ships (East India Trading Company)
    ShipGlobals.EITC_SEA_VIPER,
    ShipGlobals.EITC_BLOODHOUND,
    ShipGlobals.EITC_CORSAIR,
    ShipGlobals.EITC_IRONWALL,
    ShipGlobals.EITC_OGRE,
    ShipGlobals.EITC_BEHEMOTH,
    ShipGlobals.EITC_MARAUDER,
    ShipGlobals.EITC_WARLORD,
    ShipGlobals.EITC_JUGGERNAUT,
    
    # Undead Ships (Skeleton Pirates)
    ShipGlobals.SKEL_PHANTOM,
    ShipGlobals.SKEL_REVENANT,
    ShipGlobals.SKEL_STORM_REAPER,
    ShipGlobals.SKEL_BLACK_HARBINGER,
    ShipGlobals.SKEL_DEATH_OMEN,
    
    # French Undead Ships
    ShipGlobals.SKEL_SHADOW_CROW_FR,
    ShipGlobals.SKEL_HELLHOUND_FR,
    
    # Spanish Undead Ships
    ShipGlobals.SKEL_SHADOW_CROW_SP,
    ShipGlobals.SKEL_HELLHOUND_SP,
]
```

#### Ocean Grid Spawning

Ships must spawn within valid Cartesian grid boundaries:

```python
def _getGridBounds(self):
    """Get valid ocean grid boundaries for ship spawning"""
    gridSize = WorldGlobals.OCEAN_GRID_SIZE
    cellWidth = WorldGlobals.OCEAN_CELL_SIZE
    halfSize = (gridSize * cellWidth) / 2.0
    
    # Safety margin to keep ships within bounds
    margin = cellWidth * 2  # 2 cells from edge
    
    return (-halfSize + margin, halfSize - margin, 
            -halfSize + margin, halfSize - margin)

def _getValidSpawnPosition(self, oceanGrid, world):
    """Get a valid spawn position within the Cartesian grid"""
    for _ in range(maxAttempts):
        # Get position from ocean area manager
        sx, sy = self.air.worldCreator.oceanAreaManager.getRandomOceanPos(
            world.getUniqueId())
        
        # Validate within grid bounds
        if self._isValidSpawnPosition(sx, sy):
            return sx, sy
        
        # Clamp if outside bounds
        sx, sy = self._clampToGridBounds(sx, sy)
    
    # Fallback: random position within grid
    minX, maxX, minY, maxY = self._getGridBounds()
    return random.uniform(minX, maxX), random.uniform(minY, maxY)
```

#### Island Patrol Ships

Ships can spawn near islands to create patrol encounters:

```python
def _getIslandPatrolPosition(self, island):
    """Spawn position near an island for patrol ships"""
    islandX = island.getX()
    islandY = island.getY()
    
    # Get patrol distance from island sphere
    sphereRadii = getattr(island, 'sphereRadii', None)
    if sphereRadii and len(sphereRadii) > 2:
        patrolRadius = sphereRadii[2] + 500  # Just outside outer sphere
    else:
        patrolRadius = 3000  # Default patrol distance
    
    # Random angle around island
    angle = random.uniform(0, 2 * math.pi)
    sx = islandX + patrolRadius * math.cos(angle)
    sy = islandY + patrolRadius * math.sin(angle)
    
    return sx, sy
```

#### Ship Deployer

Each island has a `DistributedShipDeployerAI` that handles:
- Player ship spawning when entering the ocean
- Spawn radius management around islands
- Ship-to-island proximity detection

```python
# Player deploys ship from dock
def deployShip(self, avatar, shipId, callback):
    # Load ship data from database
    shipData = self.air.shipLoader.getShipData(avatar.doId, shipId)
    
    # Create ship instance
    ship = PlayerShipAI(self.air)
    ship.setOwnerId(avatar.doId)
    ship.setShipClass(shipData['class'])
    
    # Position near island dock
    ship.setPos(self.getSpawnPos())
    ship.generateWithRequired(self.oceanGrid.zoneId)
    
    callback(True)
```

---

### Quest System (`pirates/quest/`)

The quest system is one of the most valuable reverse-engineering discoveries in this project. **A significant amount of server-side AI logic was left in the original client's quest directory**, providing deep insight into how the game's quest system was designed.

#### QuestManagerAI

The quest system uses a FSM-based approach for managing quest state transitions:

```python
class QuestOperationFSM(FSM):
    def __init__(self, air, avatar, callback=None):
        self.air = air
        self.avatar = avatar
        self.callback = callback
```

#### QuestDB — The Goldmine

The `QuestDB.py` file contains **over 1,400 lines of quest definitions** that were originally server-side only. This includes:

- **Complete main story quests** (Chapters 1-3 with Jack Sparrow, Will Turner, Elizabeth, etc.)
- **NPC dialogue triggers** and cutscene sequences
- **Quest task definitions** (defeat enemies, recover items, visit locations)
- **Reward structures** (reputation, items, ships)
- **Quest prerequisites** and progression logic

```python
# Example quest definition from QuestDB
'c2_visit_will_turner': QuestDNA(
    tasks=VisitTaskDNA(npcId=NPCIds.WILL_TURNER, autoTriggerInfo=(AUTO_TRIGGER_OBJ_EXISTS, [NPCIds.WILL_TURNER])),
    instanceInfo=(INSTANCE_REF_TYPE_OBJECT, NPCIds.WILL_TURNER),
    finalizeInfo=({
        'type': 'cutscene',
        'giverId': NPCIds.WILL_TURNER,
        'sceneId': '2.1: Will Turner Sword',
        'preloadInfo': ['2.1.b: Sword Tut end']
    }, ...),
    questInt=2000,
    rewards=(ReputationReward(ExpRewards.TRIVIAL),),
    checkPoint=PiratesGlobals.TUT_GOT_CUTLASS
)
```

#### QuestLadderDB — Quest Chains

The `QuestLadderDB.py` defines quest progression trees with branching paths:

- **MainStory** - The core game storyline (Chapters 1-3)
- **Weapon Unlock Quests** - Dagger, Pistol, Cutlass, Voodoo Doll, Staff
- **Fortune Quests** - Side quests for treasure and items
- **Ship PVP Quests** - Spanish and French faction ship battles
- **Outfit Quests** - Basic, Intermediate, and Advanced clothing quests
- **Holiday Quests** - Father's Day 2008, special events

```python
# Quest ladder structure showing branching
FameQuestLadderDict = {
    'MainStory': QuestLadderDNA(
        name='MainStory',
        firstQuestId='Chapter1.rung1',
        containers=(
            QuestLadderDNA(name='Chapter 1', ...),
            QuestLadderDNA(name='Chapter 2', ...),
            QuestLadderDNA(name='Chapter 3', ...)  # Largest chapter with rum running, ship building
        )
    ),
    'WeaponDoll': QuestLadderDNA(...),   # Voodoo doll weapon quest
    'WeaponDagger': QuestLadderDNA(...), # Dagger unlock quest
    'WeaponGrenade': QuestLadderDNA(...),# Grenade quest
    ...
}
```

#### Quest Task Types

The quest system supports various task types defined in `QuestTaskDNA.py`:

| Task Type | Description |
|-----------|-------------|
| `VisitTaskDNA` | Visit a specific NPC or location |
| `DefeatTaskDNA` | Defeat a number of enemies of a type |
| `RecoverAvatarItemTaskDNA` | Loot items from enemies |
| `DeliverItemTaskDNA` | Deliver items to NPCs |
| `DeployShipTaskDNA` | Launch a ship from a dock |
| `CaptureTaskDNA` | Capture an enemy NPC |
| `MaroonTaskDNA` | Strand a captured NPC |
| `SinkShipTaskDNA` | Sink enemy ships |
| `PlayMinigameTaskDNA` | Play poker/blackjack |
| `BribeTaskDNA` | Bribe an NPC with gold |
| `SmuggleTaskDNA` | Smuggle cargo past enemies |

#### Quest Rewards

```python
# Reward types from QuestReward.py
ReputationReward(ExpRewards.TRIVIAL)  # XP rewards
ShipReward(1)                          # Ship unlocks
ItemReward(itemId, quantity)           # Inventory items
GoldReward(amount)                     # Currency
WeaponReward(weaponType)               # Weapon unlocks
```

#### Quest Indicators

The quest system includes sophisticated indicator nodes for guiding players:

- `QuestIndicatorNodeNPC` - Points to quest NPCs
- `QuestIndicatorNodeItem` - Points to collectible items
- `QuestIndicatorNodeShip` - Points to ships
- `QuestIndicatorNodeArea` - Points to areas/zones
- `QuestIndicatorNodeTunnel` - Points to area transitions

---

### Distributed Class System (DClass)

The `.dc` files define the network protocol for all distributed objects. Understanding these files was one of the first steps in reverse engineering — they define every field and method that can be transmitted over the network.

Located in `astron/dclass/`:
- `otp.dc` - Base OTP (Online Theme Park) classes
- `pirates.dc` - Pirates-specific classes (2,182 lines)

#### DClass Syntax

```
// Type definitions
typedef uint32 DoId;
typedef DoId DoIdList[];
typedef uint16 SkillId;

// Custom structs for network transmission
struct PosHpr {
  int32/10 x;   // Divide by 10 for decimal precision
  int32/10 y;
  int32/10 z;
  int16/10 h;
  int16/10 p;
  int16/10 r;
};

struct Buff {
  uint8 effectId;
  int16 duration;
  int16 timestamp;
  DoId attackerId;
};
```

#### Field Modifiers

| Modifier | Description |
|----------|-------------|
| `required` | Field is sent on object generation |
| `broadcast` | Field is sent to all clients with interest |
| `ram` | Field is stored in RAM on the server |
| `db` | Field is persisted to database |
| `ownrecv` | Only the owner receives this field |
| `airecv` | Only the AI server receives this field |
| `clsend` | Client can send this message |

#### Example DClass Definition

```
dclass PiratesDistrict : DistributedDistrict {
  setParentingRules(string, string) broadcast ram;
  setAvatarCount(uint32) broadcast required;
  setNewAvatarCount(uint32) broadcast required;
  setMainWorld(string) broadcast required;
  setShardType(uint8) broadcast required ram;
  
  // Compound update macro
  setStats : setAvatarCount, setNewAvatarCount;
};

dclass Teamable {
  setTeam(int16) required broadcast ram ownrecv;
  setPVPTeam(int8) required broadcast ram ownrecv airecv;
  setSiegeTeam(int8) required broadcast ram ownrecv airecv;
};
```

#### Import Structure

The `.dc` files define which Python modules implement each class:

```
// Format: module/AI/UD/OV (AI server, UberDOG, Owner View)
from pirates.ship import DistributedShip/AI/UD
from pirates.ship import PlayerShip/AI/UD/OV
from pirates.pirate import DistributedPlayerPirate/AI/UD
from pirates.instance import DistributedTeleportMgr/AI
from pirates.uberdog import ClientServicesManager/UD
```

---

### RPC System (`pirates/web/`)

The server exposes an RPC interface for external tools, monitoring, and administrative actions. This allows web dashboards and Discord bots to interact with the game server.

```python
@rpcservice(serviceName='cluster')
class ClusterService(RPCServiceUD):
    def systemMessage(self, message):
        """Broadcasts a message to all players"""
        self.air.systemMessage(message)
    
    def kickChannel(self, channel, reason=1, message=''):
        """Kicks users on a specific channel"""
        self.air.kickChannel(channel, reason, message)
    
    def getPopulation(self):
        """Returns current shard population"""
        return self.air.populationTracker.getPopulation()
```

#### Available RPC Services

| Service | Purpose |
|---------|---------|
| `ClusterService` | Shard management, broadcasts, kicks |
| `GuildService` | Guild operations from web interface |
| `PlayerService` | Player lookups and moderation |
| `StatsService` | Real-time population and metrics |

#### Discord Integration

The `DiscordNotificationsAI` sends webhooks for server events:

```python
class DiscordNotificationsAI:
    def notifyShardOnline(self, shardName):
        self.sendWebhook({
            'embeds': [{
                'title': 'Shard Online',
                'description': f'{shardName} is now online!',
                'color': 0x00FF00
            }]
        })
```

---

## 💬 Community

Join our community to get help, share ideas, and connect with other contributors!

- Report bugs and request features through [GitHub Issues](https://github.com/PiratesOnlineClassic/pirates-online-classic/issues)
- Submit improvements through [Pull Requests](https://github.com/PiratesOnlineClassic/pirates-online-classic/pulls)

---

## ⚠️ Disclaimer

This is a non-commercial fan project created for educational and preservation purposes. Pirates of the Caribbean is a trademark of Disney. This project is not affiliated with, endorsed by, or connected to The Walt Disney Company in any way.

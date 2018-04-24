from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from otp.distributed.OtpDoGlobals import *
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory

class InventoryFSM(FSM):

    def __init__(self, manager, avatarId, callback):
        self.manager = manager
        self.avatarId = avatarId
        self.callback = callback

        FSM.__init__(self, 'InventoryFSM')

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterStart(self):

        def queryAvatar(dclass, fields):
            if not dclass or not fields:
                self.notify.warning('Failed to query avatar %d!' % (
                    self.avatarId))

                return

            inventoryId, = fields.get('setInventoryId', (0,))

            if not inventoryId:
                self.request('Create')
            else:
                self.request('Load', inventoryId)

        self.manager.air.dbInterface.queryObject(self.manager.air.dbId, self.avatarId, queryAvatar,
            dclass=self.manager.air.dclassesByName['DistributedPlayerPirateUD'])

    def exitStart(self):
        pass

    def enterCreate(self):

        def inventorySet(fields, inventoryId):
            if fields:
                self.notify.warning('Failed to set inventory %d for %d!' % (
                    inventoryId, self.avatarId))

            self.request('Load', inventoryId)

        def inventoryCreated(inventoryId):
            if not inventoryId:
                self.notify.warning('Failed to create inventory for %d!' % (
                    self.avatarId))

                return

            self.manager.air.dbInterface.updateObject(self.manager.air.dbId, self.avatarId, self.manager.air.dclassesByName['DistributedPlayerPirateUD'],
                {'setInventoryId': (inventoryId,)}, callback=lambda fields: inventorySet(fields, inventoryId))

        accumulators = [
            # Experience
            [InventoryType.OverallRep, 0],
            [InventoryType.GeneralRep, 0],
            [InventoryType.CutlassRep, 0],
            [InventoryType.PistolRep, 0],
            [InventoryType.DollRep, 0],
            [InventoryType.DaggerRep, 0],
            [InventoryType.GrenadeRep, 0],
            [InventoryType.WandRep, 0],
            [InventoryType.CannonRep, 0],
            [InventoryType.SailingRep, 0],
            [InventoryType.MonsterRep, 0],
            [InventoryType.LockpickRep, 0],
            [InventoryType.GamblingRep, 0]
        ]

        categoryLimits = [
            [InventoryCategory.QUESTS, 255], 
            [InventoryCategory.MONEY, 7], 
            [InventoryCategory.MAX_PLAYER_ATTRIBUTES, 2], 
            [InventoryCategory.WEAPONS, 100], 
            [InventoryCategory.WEAPON_SKILL_MELEE, 100], 
            [InventoryCategory.WEAPON_SKILL_CUTLASS, 100], 
            [InventoryCategory.WEAPON_SKILL_PISTOL, 100], 
            [InventoryCategory.WEAPON_SKILL_MUSKET, 100], 
            [InventoryCategory.WEAPON_SKILL_DAGGER, 100],
            [InventoryCategory.WEAPON_SKILL_GRENADE, 100], 
            [InventoryCategory.WEAPON_SKILL_DOLL, 100], 
            [InventoryCategory.WEAPON_SKILL_WAND, 100], 
            [InventoryCategory.WEAPON_SKILL_KETTLE, 100], 
            [InventoryCategory.WEAPON_SKILL_CANNON, 100], 
            [InventoryCategory.WEAPON_SKILL_ITEM, 10],
            [InventoryCategory.SKILL_SAILING, 100],
            [InventoryCategory.WAGERS, 100], 
            [InventoryCategory.KEY_ITEMS, 30], 
            [InventoryCategory.TELEPORT_TOKENS, 30], 
            [InventoryCategory.CONSUMABLES, 50], 
            [InventoryCategory.SHIPS, 3], 
            [InventoryCategory.SHIP_ACCESSORIES, 250], 
            [InventoryCategory.SHIP_CANNONS, 200], 
            [InventoryCategory.FLAGS, 5], 
            [InventoryCategory.COLLECTIONS, 250], 
            [InventoryCategory.TREASURE_MAPS, 3], 
            [InventoryCategory.QUEST_SLOTS, 255], 
            [InventoryCategory.ACCUMULATORS, 20], 
            [InventoryCategory.REPAIR_TOKENS, 2], 
            [InventoryCategory.WEAPON_PISTOL_AMMO, 200], 
            [InventoryCategory.WEAPON_MUSKET_AMMO, 200], 
            [InventoryCategory.WEAPON_GRENADE_AMMO, 200], 
            [InventoryCategory.WEAPON_CANNON_AMMO, 200], 
            [InventoryCategory.WEAPON_DAGGER_AMMO, 200], 
            [InventoryCategory.UNSPENT_SKILL_POINTS, 100], 
            [InventoryCategory.VITAE_PENALTY, 10000], 
            [InventoryCategory.PLAYER_RANKING, 10000], 
            [InventoryCategory.CARDS, 100], 
            [InventoryCategory.PISTOL_POUCHES, 10], 
            [InventoryCategory.DAGGER_POUCHES, 10], 
            [InventoryCategory.GRENADE_POUCHES, 10], 
            [InventoryCategory.CANNON_POUCHES, 10], 
            [InventoryCategory.SONGS, 100], 
        ]
        stackLimits = [
            # Skills
            [InventoryType.MeleePunch, 6],
            [InventoryType.MeleeKick, 6], 
            [InventoryType.SailBroadsideLeft, 6], 
            [InventoryType.SailBroadsideRight, 6], 
            [InventoryType.SailFullSail, 6], 
            [InventoryType.SailComeAbout, 6], 
            [InventoryType.SailOpenFire, 6], 
            [InventoryType.SailRammingSpeed, 6], 
            [InventoryType.SailTakeCover, 6], 
            [InventoryType.SailWindcatcher, 6], 
            [InventoryType.SailTacking, 6], 
            [InventoryType.SailPowerRecharge, 2], 
            [InventoryType.CutlassHack, 6], 
            [InventoryType.CutlassSlash, 6], 
            [InventoryType.DaggerCut, 6], 
            [InventoryType.DaggerSwipe, 6], 
            [InventoryType.AmmoAsp, 100], 
            [InventoryType.AmmoAdder, 50], 
            [InventoryType.AmmoSidewinder, 50], 
            [InventoryType.AmmoViperNest, 25], 
            [InventoryType.PistolShoot, 6], 
            [InventoryType.PistolLeadShot, 6], 
            [InventoryType.AmmoLeadShot, 6], 
            [InventoryType.AmmoBaneShot, 100], 
            [InventoryType.AmmoSilverShot, 100], 
            [InventoryType.AmmoHexEaterShot, 100], 
            [InventoryType.AmmoSteelShot, 100], 
            [InventoryType.AmmoVenomShot, 100], 
            [InventoryType.CannonShoot, 6], 
            [InventoryType.CannonRoundShot, 6], 
            [InventoryType.CannonGrappleHook, 6], 
            [InventoryType.DollAttune, 6], 
            [InventoryType.DollPoke, 6], 
            [InventoryType.StaffBlast, 6], 
            [InventoryType.StaffSoulFlay, 6], 
            [InventoryType.GrenadeThrow, 6], 
            [InventoryType.GrenadeExplosion, 6],

            # Ammo
            [InventoryType.AmmoRoundShot, 1], 
            [InventoryType.AmmoChainShot, 100], 
            [InventoryType.AmmoExplosive, 3], 
            [InventoryType.AmmoGrapeShot, 100], 
            [InventoryType.AmmoFirebrand, 50], 
            [InventoryType.AmmoThunderbolt, 50], 
            [InventoryType.AmmoFury, 50], 
            [InventoryType.AmmoGrappleHook, 100], 

            # Potions
            [InventoryType.Potion1, 3],
            [InventoryType.Potion2, 3],
            [InventoryType.Potion3, 3],
            [InventoryType.Potion4, 3],
            [InventoryType.Potion5, 3],

            # Pouches
            [InventoryType.PistolPouchL1, 1], 
            [InventoryType.PistolPouchL2, 1], 
            [InventoryType.PistolPouchL3, 1], 
            [InventoryType.DaggerPouchL1, 1], 
            [InventoryType.DaggerPouchL2, 1], 
            [InventoryType.DaggerPouchL3, 1], 
            [InventoryType.GrenadePouchL1, 1], 
            [InventoryType.GrenadePouchL2, 1], 
            [InventoryType.GrenadePouchL3, 1], 
            [InventoryType.CannonPouchL1, 1], 
            [InventoryType.CannonPouchL2, 1], 
            [InventoryType.CannonPouchL3, 1], 

            # Skill points
            [InventoryType.UnspentCutlass, 50], 
            [InventoryType.UnspentDagger, 50], 
            [InventoryType.UnspentGrenade, 50], 
            [InventoryType.UnspentWand, 50], 
            [InventoryType.UnspentDoll, 50], 
            [InventoryType.UnspentCannon, 50], 
            [InventoryType.UnspentPistol, 50], 
            [InventoryType.UnspentSailing, 50], 
        
            # Vitae
            [InventoryType.Vitae_Level, 100], 
            [InventoryType.Vitae_Cost, 10000], 
            [InventoryType.Vitae_Left, 10000], 
            [InventoryType.Vitae_Update, 10000], 

            # Use
            [InventoryType.UseItem, 6],

            # Parlor Games
            [InventoryType.PokerGame, 9999], 
            [InventoryType.BlackjackGame, 9999], 

            # PVP
            [InventoryType.CTFGame, 9999], 
            [InventoryType.CTLGame, 9999], 
            [InventoryType.PTRGame, 9999], 
            [InventoryType.BTLGame, 9999], 
            [InventoryType.TBTGame, 9999], 
            [InventoryType.SBTGame, 9999], 
            [InventoryType.ARMGame, 9999], 
            [InventoryType.TKPGame, 9999], 
            [InventoryType.BTBGame, 9999], 
            [InventoryType.ShipPVPRank, 9999], 
            [InventoryType.PVPTotalInfamyLand, 10000], 
            [InventoryType.PVPCurrentInfamy, 50000], 
            [InventoryType.PVPTotalInfamySea, 10000],
            [InventoryType.PvPRenownLand, 10000], 
            [InventoryType.PvPRenownSea, 10000], 
            [InventoryType.PvPPointsLand, 10000],
            [InventoryType.PvPPointsSea, 10000],

            # Misc.
            [InventoryType.Dinghy, 1], 
            [InventoryType.SmallBottle, 5], 
            [InventoryType.MediumBottle, 5], 
            [InventoryType.LargeBottle, 5], 

            # Tokens
            [InventoryType.CutlassToken, 1], 
            [InventoryType.PistolToken, 1], 
            [InventoryType.MusketToken, 1], 
            [InventoryType.DaggerToken, 1], 
            [InventoryType.GrenadeToken, 1], 
            [InventoryType.WandToken, 1], 
            [InventoryType.DollToken, 1], 
            [InventoryType.KettleToken, 1], 
            [InventoryType.FirstDeathToken, 1], 

            [InventoryType.TortugaTeleportToken, 1], 
            [InventoryType.PortRoyalTeleportToken, 1], 
            [InventoryType.KingsheadTeleportToken, 1], 
            [InventoryType.PadresDelFuegoTeleportToken, 1], 
            [InventoryType.CubaTeleportToken, 1], 

            [InventoryType.PlayerHealToken, 1000], 
            [InventoryType.PlayerMojoHealToken, 1000], 

            # Respec
            [InventoryType.NumRespecCutlass, 32767], 
            [InventoryType.NumRespecPistol, 32767], 
            [InventoryType.NumRespecDoll, 32767], 
            [InventoryType.NumRespecDagger, 32767], 
            [InventoryType.NumRespecGrenade, 32767], 
            [InventoryType.NumRespecStaff, 32767], 
            [InventoryType.NumRespecCannon, 32767], 
            [InventoryType.NumRespecSailing,  32767],

            # Music
            [InventoryType.Song_1, 1],
            [InventoryType.Song_2, 1],
            [InventoryType.Song_3, 1],
            [InventoryType.Song_4, 1],
            [InventoryType.Song_6, 1],
            [InventoryType.Song_7, 1],
            [InventoryType.Song_8, 1],
            [InventoryType.Song_9, 1],
            [InventoryType.Song_10, 1],
            [InventoryType.Song_11, 1],
            [InventoryType.Song_12, 1],
            [InventoryType.Song_13, 1],
            [InventoryType.Song_14, 1],
            [InventoryType.Song_15, 1],
            [InventoryType.Song_16, 1],
            [InventoryType.Song_17, 1],
            [InventoryType.Song_18, 1],
            [InventoryType.Song_19, 1],
            [InventoryType.Song_20, 1],
        ]

        stacks = [
            # Weapons
            [InventoryType.CutlassWeaponL1, 1],
            [InventoryType.PistolWeaponL1, 1],
            [InventoryType.MusketWeaponL1, 0],
            [InventoryType.BayonetWeaponL1, 0],
            [InventoryType.DaggerWeaponL1, 1],
            [InventoryType.GrenadeWeaponL1, 1],
            [InventoryType.DollWeaponL1, 1],
            [InventoryType.WandWeaponL1, 1],

            # Skills
            [InventoryType.CutlassHack, 1],
            [InventoryType.CutlassSlash, 1],
            [InventoryType.PistolShoot, 1],
            [InventoryType.PistolLeadShot, 1],
            [InventoryType.DollAttune, 1],
            [InventoryType.DollPoke, 1],
            [InventoryType.DaggerCut, 1],
            [InventoryType.DaggerSwipe, 1],
            [InventoryType.StaffBlast, 1],
            [InventoryType.StaffSoulFlay, 1],
            [InventoryType.GrenadeThrow, 1],

            # Music
            [InventoryType.Song_1, 1],
            [InventoryType.Song_2, 1],
            [InventoryType.Song_3, 1],
            [InventoryType.Song_4, 1],
            [InventoryType.Song_5, 1],
        ]

        if config.GetBool('want-all-weapons', False):

            weaponTokens = [
                [InventoryType.PistolToken, 1],
                [InventoryType.MusketToken, 1],
                [InventoryType.DaggerToken, 1],
                [InventoryType.GrenadeToken, 1],
                #[InventoryType.WandToken, 1], TODO: Causes weird issue presumably with tia dalma quest stuff
                [InventoryType.DollToken, 1],
                [InventoryType.KettleToken, 1]
            ]

            stacks = stacks + weaponTokens

        fields = {
            'setOwnerId': (self.avatarId,),
            'setInventoryVersion': (0,),
            'setCategoryLimits': (categoryLimits,),
            'setAccumulators': (accumulators,),
            'setStackLimits': (stackLimits,),
            'setStacks': (stacks,)
        }

        self.manager.air.dbInterface.createObject(self.manager.air.dbId, self.manager.air.dclassesByName[
            'PirateInventoryUD'], fields=fields, callback=inventoryCreated)

    def exitCreate(self):
        pass

    def enterLoad(self, inventoryId):
        if not inventoryId:
            self.warning('Failed to activate invalid inventory object!')
            return

        self.manager.air.sendActivate(inventoryId, self.avatarId, OTP_ZONE_ID_MANAGEMENT, dclass=\
            self.manager.air.dclassesByName['PirateInventoryUD'])

        if self.callback:
            self.callback(inventoryId)

        del self.manager.avatar2fsm[self.avatarId]
        self.demand('Off')

    def exitLoad(self):
        pass

class DistributedInventoryManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.avatar2fsm = {}

        self.air.netMessenger.accept('hasInventoryResponse', self, self.proccessCallbackResponse)
        self.air.netMessenger.accept('getInventoryResponse', self, self.proccessCallbackResponse)

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

    def hasInventory(self, inventoryId, callback):
        self.air.netMessenger.send('hasInventory', [inventoryId, callback])

    def addInventory(self, inventory):
        if inventory and inventory.doId:
            self.air.netMessenger.send('addInventory', [inventory])

    def removeInventory(self, inventory):
        if inventory and inventory.doId:
            self.air.netMessenger.send('removeInventory', [inventory])

    def getInventory(self, avatarId, callback):
        self.air.netMessenger.send('getInventory', [avatarId, callback])

    def initiateInventory(self, avatarId, callback=None):
        if not avatarId:
            return

        if avatarId in self.avatar2fsm:
            self.notify.warning('Failed to initiate inventory for already existing avatar %s!' % (
                avatarId))

            return

        self.avatar2fsm[avatarId] = InventoryFSM(self, avatarId, callback)
        self.avatar2fsm[avatarId].request('Start')

    def proccessCallbackResponse(self, callback, *args, **kwargs):
        if callback and callable(callback):
            callback(*args, **kwargs)
            return

        self.notify.warning("No valid callback for a callback response! What was the purpose of that?")

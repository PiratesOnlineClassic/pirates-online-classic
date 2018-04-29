# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.HighSeasScoreboard
import time

from direct.distributed.ClockDelta import *
from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.economy import EconomyGlobals
from pirates.piratesbase import Freebooter, PiratesGlobals, PLocalizer
from pirates.piratesgui import (DialogButton, GuiPanel, PiratesGuiGlobals,
                                Scoreboard)
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import *


class HighSeasScoreboard(GuiPanel.GuiPanel):
    
    width = PiratesGuiGlobals.PortPanelWidth
    height = PiratesGuiGlobals.PortPanelHeight
    titleHeight = PiratesGuiGlobals.PortTitleHeight
    buffer = 0.05

    def __init__(self, name, stats, playerStats, ship):
        GuiPanel.GuiPanel.__init__(self, '', self.width, self.height, showClose=False)
        self.ship = ship
        self.stats = stats
        self.playerStats = playerStats
        self.initialiseoptions(HighSeasScoreboard)
        self.leftPanel = None
        self.rightPanel = None
        titleTxt = PLocalizer.ScoreboardTitle
        if self.ship.shipClass == ShipGlobals.BLACK_PEARL:
            titleTxt = PLocalizer.BlackPearlScoreboard
        self.title = DirectLabel(parent=self, relief=None, text=titleTxt, text_align=TextNode.ALeft, text_scale=self.titleHeight, text_fg=PiratesGuiGlobals.TextFG10, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.03, 0, self.height - self.titleHeight - 0.03), text_font=PiratesGlobals.getPirateOutlineFont(), textMayChange=1)
        self.closeButton = DialogButton.DialogButton(parent=self, buttonStyle=DialogButton.DialogButton.NO, text=PLocalizer.lClose, pos=(1.05,
                                                                                                                                         0,
                                                                                                                                         0.075), command=self.closePanel)
        self.createScoreboard()
        return

    def destroy(self):
        if self.leftPanel:
            self.leftPanel.destroy()
            self.leftPanel = None
        if self.rightPanel:
            self.rightPanel.destroy()
            self.rightPanel = None
        GuiPanel.GuiPanel.destroy(self)
        return

    def getMissionResults(self):
        missionTime, shipDamage, skeletonKills, navyKills, creatureKills, seamonsterKills, pirateKills, townfolkKills, shipKills, repairCost, exp, gold, cargo, numCrew = self.stats
        pMissionTime, pShipDamage, pSkeletonKills, pNavyKills, pCreatureKills, pSeamonsterKills, pPirateKills, pTownfolkKills, pShipKills, pRepairCost, pExp, pGold, pCargo, dummyCrew = self.playerStats
        inventory = base.localAvatar.getInventory()
        if inventory:
            currentGold = inventory.getStackQuantity(InventoryType.GoldInPocket)
        t = time.gmtime(missionTime)
        totalTime = str(t[3]) + '"' + str(t[4]) + "'" + str(t[5])
        self.cargo = cargo
        cargoValue = EconomyGlobals.getCargoTotalValue(cargo)
        totalGold = max(cargoValue + gold - repairCost, 0)
        self.results = []
        self.results.append({'Type': 'Title', 'Text': PLocalizer.AdventureResults, 'Value1': PLocalizer.You, 'Value2': PLocalizer.Team})
        self.results.append({'Type': 'Entry', 'Text': PLocalizer.TotalTime, 'Value1': totalTime})
        self.results.append({'Type': 'Entry', 'Text': PLocalizer.CrewRemaining, 'Value1': numCrew})
        self.results.append({'Type': 'Entry', 'Text': PLocalizer.ShipsSunk, 'Value1': pShipKills, 'Value2': shipKills})
        if skeletonKills:
            self.results.append({'Type': 'Entry', 'Text': PLocalizer.UndeadDefeated, 'Value1': pSkeletonKills, 'Value2': skeletonKills})
        if navyKills:
            self.results.append({'Type': 'Entry', 'Text': PLocalizer.NavyDefeated, 'Value1': pNavyKills, 'Value2': navyKills})
        if pirateKills:
            self.results.append({'Type': 'Entry', 'Text': PLocalizer.PiratesDefeated, 'Value1': pPirateKills, 'Value2': pirateKills})
        if creatureKills:
            self.results.append({'Type': 'Entry', 'Text': PLocalizer.CreaturesDefeated, 'Value1': pCreatureKills, 'Value2': creatureKills})
        if seamonsterKills:
            self.results.append({'Type': 'Entry', 'Text': PLocalizer.SeamonstersDefeated, 'Value1': pSeamonsterKills, 'Value2': seamonsterKills})
        if townfolkKills:
            self.results.append({'Type': 'Entry', 'Text': PLocalizer.TownfolkDefeated, 'Value1': pTownfolkKills, 'Value2': townfolkKills})
        self.results.append({'Type': 'Space', 'Text': '', 'Value1': ''})
        self.results.append({'Type': 'Title', 'Text': PLocalizer.ShipStatus, 'Value1': ''})
        self.results.append({'Type': 'Entry', 'Text': PLocalizer.ShipDamage, 'Value1': str(shipDamage) + '%'})
        crewRating = shipKills * 5 + pirateKills * 2 + skeletonKills * 2 + creatureKills + seamonsterKills * 10 + navyKills * 2 + gold / 10 + len(cargo) - shipDamage / 10
        crewRating = PLocalizer.getCrewRating(crewRating)
        rating = pShipKills * 5 + pPirateKills * 2 + pSkeletonKills * 2 + pCreatureKills + pSeamonsterKills * 10 + pNavyKills * 2 + pGold / 10 + len(pCargo) - pShipDamage / 20
        rating = PLocalizer.getHighSeasRating(rating)
        self.results.append({'Type': 'Space', 'Text': '', 'Value1': ''})
        self.results.append({'Type': 'Title', 'Text': PLocalizer.RatingsTitle, 'Value1': ''})
        self.results.append({'Type': 'Entry', 'Text': PLocalizer.CrewRating, 'Value1': crewRating})
        self.results.append({'Type': 'Entry', 'Text': PLocalizer.Rating, 'Value1': rating})
        return self.results

    def getCargoResults(self):
        missionTime, shipDamage, skeletonKills, navyKills, creatureKills, seamonsterKills, pirateKills, townfolkKills, shipKills, repairCost, exp, gold, cargo, numCrew = self.stats
        pMissionTime, pShipDamage, pSkeletonKills, pNavyKills, pCreatureKills, pSeamonsterKills, pPirateKills, pTownfolkKills, pShipKills, pRepairCost, pExp, pGold, pCargo, dummyCrew = self.playerStats
        inventory = base.localAvatar.getInventory()
        if inventory:
            currentGold = inventory.getStackQuantity(InventoryType.GoldInPocket)
        avId = base.localAvatar.getDoId()
        cargoValue = EconomyGlobals.getCargoTotalValue(pCargo)
        totalGold = cargoValue + pGold
        bonusGold = 0
        if base.localAvatar.ship:
            if base.localAvatar.ship.getOwnerId() == avId and len(base.localAvatar.ship.getCrew()) > 1:
                bonusGold = int(totalGold * EconomyGlobals.CAPTAIN_LOOT_MULTIPLIER)
                totalGold += bonusGold
        if base.getHoliday(PiratesGlobals.DOUBLEGOLDHOLIDAYPAID) and Freebooter.getPaidStatus(avId) or base.getHoliday(PiratesGlobals.DOUBLEGOLDHOLIDAY):
            totalGold *= 2
        netGold = totalGold - pRepairCost
        self.results = []
        self.results.append({'Type': 'Title', 'Text': PLocalizer.DividingPlunder, 'Value1': ''})
        if pGold:
            self.results.append({'Type': 'Entry', 'Text': PLocalizer.GoldLooted, 'Value1': pGold, 'Value2': gold})
        if len(pCargo) == 0:
            self.results.append({'Type': 'Entry', 'Text': PLocalizer.NoCargoLooted, 'Value1': '', 'UnwrapMode': 1})
        for itemId in pCargo:
            self.results.append({'Type': 'Cargo', 'Text': '', 'Value1': itemId, 'UnwrapMode': 1})

        if bonusGold > 0:
            self.results.append({'Type': 'Space', 'Text': '', 'Value1': '', 'UnwrapMode': 1})
            self.results.append({'Type': 'Entry', 'Text': PLocalizer.CaptainsBonus, 'Value1': str(bonusGold) + ' ' + PLocalizer.MoneyName, 'UnwrapMode': 1})
        if base.getHoliday(PiratesGlobals.DOUBLEGOLDHOLIDAYPAID) and Freebooter.getPaidStatus(avId) or base.getHoliday(PiratesGlobals.DOUBLEGOLDHOLIDAY):
            self.results.append({'Type': 'Space', 'Text': '', 'Value1': '', 'UnwrapMode': 1})
            self.results.append({'Type': 'Entry', 'Text': PLocalizer.DoubleGoldBonus, 'Value1': str(totalGold / 2) + ' ' + PLocalizer.MoneyName, 'UnwrapMode': 1})
        self.results.append({'Type': 'Space', 'Text': '', 'Value1': '', 'UnwrapMode': 1})
        self.results.append({'Type': 'Title', 'Text': PLocalizer.PlunderShare, 'Value1': str(netGold) + ' ' + PLocalizer.MoneyName, 'UnwrapMode': 1})
        return self.results

    def createScoreboard(self):
        missionResults = self.getMissionResults()
        self.leftPanel = Scoreboard.Scoreboard('', (self.width - self.buffer * 2) / 2.0, self.height - 0.1, missionResults, self.titleHeight)
        self.leftPanel.reparentTo(self)
        self.leftPanel.setPos(self.buffer, 0, 0.2)
        cargoResults = self.getCargoResults()
        self.rightPanel = Scoreboard.Scoreboard('', (self.width - self.buffer * 2) / 2.0, self.height - 0.1, cargoResults, self.titleHeight)
        self.rightPanel.reparentTo(self)
        self.rightPanel.setPos((self.width + self.buffer) / 2.0, 0, 0.2)

    def getListFinishedMessage(self):
        return 'listFinished'

    def payForShipRepairs(self):
        self.ship.requestRepairAll()

    def getShowNextItemMessage(self):
        return 'showNextHighSeaStat'

    def destroy(self):
        GuiPanel.GuiPanel.destroy(self)

    def closePanel(self):
        GuiPanel.GuiPanel.closePanel(self)
        self.destroy()
        messenger.send('highSeasScoreBoardClose')
# okay decompiling .\pirates\piratesgui\HighSeasScoreboard.pyc

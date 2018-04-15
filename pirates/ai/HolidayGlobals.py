from pirates.ai.HolidayDates import *
from pirates.piratesbase import PiratesGlobals, PLocalizer

Month = Enum('JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER', 1)
Day = Enum('MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY')

holidayNames = {
    PiratesGlobals.DOUBLEGOLDHOLIDAY: 'DoubleGoldHolidayAll',
    PiratesGlobals.DOUBLEGOLDHOLIDAYPAID: 'DoubleGoldHolidayPaid',
    PiratesGlobals.DOUBLEXPHOLIDAY: 'DoubleXPHolidayAll',
    PiratesGlobals.DOUBLEXPHOLIDAYPAID: 'DoubleXPHolidayPaid',
    PiratesGlobals.FREEHATWEEK: 'FreeHatWeek',
    PiratesGlobals.SAINTPATRICKSDAY: 'SaintPatricksDay',
    PiratesGlobals.MOTHERSDAY: 'MothersDay',
    PiratesGlobals.FATHERSDAY: 'FathersDay',
    PiratesGlobals.FOURTHOFJULY: 'FourthOfJuly',
    PiratesGlobals.HALFOFFCUSTOMIZATION: 'HalfOffCustomization',
    PiratesGlobals.ALLACCESSWEEKEND: 'AllAccessWeekend',
    PiratesGlobals.HALLOWEEN: 'Halloween',
    PiratesGlobals.JOLLYROGERCURSE: 'JollyRogerCurse',
    PiratesGlobals.FOUNDERSFEAST: 'FoundersFeast',
    PiratesGlobals.FREEITEMTHANKSGIVING: 'FreeItemThanksgiving',
    PiratesGlobals.CURSEDNIGHT: 'CursedNight',
    PiratesGlobals.JOLLYCURSEAUTO: 'JollyCurseAuto',
    PiratesGlobals.WINTERFESTIVAL: 'WinterFestival'
}

def getHolidayName(holidayId):
    return holidayNames.get(holidayId)

def getHolidayIdFromName(holidayName):
    found = None
    for holidayId in holidayNames:
        if holidayNames[holidayId] == holidayName:
            found = holidayId
            break
    return found

def getAllHolidayIds():
    return holidayNames.keys()

holidays = {
    PiratesGlobals.DOUBLEGOLDHOLIDAY: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.SEPTEMBER, 13, 12, 0, 0), 
        (2008, Month.SEPTEMBER, 13, 15, 0, 0)]), 
    PiratesGlobals.DOUBLEGOLDHOLIDAYPAID: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.SEPTEMBER, 14, 12, 0, 0), 
        (2008, Month.SEPTEMBER, 14, 15, 0, 0)]), 
    PiratesGlobals.DOUBLEXPHOLIDAY: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.SEPTEMBER, 27, 12, 0, 0), 
        (2008, Month.SEPTEMBER, 27, 15, 0, 0)]), 
    PiratesGlobals.DOUBLEXPHOLIDAYPAID: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.SEPTEMBER, 28, 12, 0, 0), 
        (2008, Month.SEPTEMBER, 28, 15, 0, 0)]), 
    PiratesGlobals.FREEHATWEEK: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.FEBRUARY, 25, 0, 0, 0), 
        (2008, Month.MARCH, 2, 0, 0, 0)]), 
    PiratesGlobals.SAINTPATRICKSDAY: HolidayDates(HolidayDates.TYPE_YEARLY, [
        (Month.MARCH, 14, 0, 0, 0), 
        (Month.MARCH, 18, 0, 0, 0)]), 
    PiratesGlobals.MOTHERSDAY: HolidayDates(HolidayDates.TYPE_YEARLY, [
        (Month.MAY, 10, 0, 0, 0), 
        (Month.MAY, 12, 0, 0, 0)]), 
    PiratesGlobals.FATHERSDAY: HolidayDates(HolidayDates.TYPE_YEARLY, [
        (Month.JUNE, 13, 0, 0, 0), 
        (Month.JUNE, 16, 0, 0, 0)]), 
    PiratesGlobals.FOURTHOFJULY: HolidayDates(HolidayDates.TYPE_YEARLY, [
        (Month.JULY, 3, 18, 0, 0), 
        (Month.JULY, 7, 0, 0, 0)]), 
    PiratesGlobals.HALFOFFCUSTOMIZATION: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.AUGUST, 14, 0, 0, 0), 
        (2008, Month.AUGUST, 18, 12, 0, 0)]), 
    PiratesGlobals.ALLACCESSWEEKEND: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.AUGUST, 14, 0, 0, 0),
        (2008, Month.AUGUST, 18, 12, 0, 0)]), 
    PiratesGlobals.HALLOWEEN: HolidayDates(HolidayDates.TYPE_YEARLY, [
        (Month.OCTOBER, 31, 3, 0, 0), 
        (Month.NOVEMBER, 3, 0, 0, 0)]), 
    PiratesGlobals.JOLLYROGERCURSE: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.OCTOBER, 31, 12, 0, 0), 
        (2008, Month.OCTOBER, 31, 12, 30, 0), 
        (2008, Month.OCTOBER, 31, 17, 0, 0), 
        (2008, Month.OCTOBER, 31, 17, 30, 0), 
        (2008, Month.OCTOBER, 31, 20, 0, 0), 
        (2008, Month.OCTOBER, 31, 20, 30, 0), 
        (2008, Month.NOVEMBER, 1, 12, 0, 0), 
        (2008, Month.NOVEMBER, 1, 12, 30, 0), 
        (2008, Month.NOVEMBER, 1, 16, 0, 0), 
        (2008, Month.NOVEMBER, 1, 16, 30, 0), 
        (2008, Month.NOVEMBER, 1, 21, 0, 0), 
        (2008, Month.NOVEMBER, 1, 21, 30, 0), 
        (2008, Month.NOVEMBER, 2, 13, 0, 0), 
        (2008, Month.NOVEMBER, 2, 13, 30, 0), 
        (2008, Month.NOVEMBER, 2, 16, 0, 0), 
        (2008, Month.NOVEMBER, 2, 16, 30, 0), 
        (2008, Month.NOVEMBER, 2, 19, 0, 0), 
        (2008, Month.NOVEMBER, 2, 19, 30, 0)]),
    PiratesGlobals.FOUNDERSFEAST: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.NOVEMBER, 27, 3, 0, 0), (2008, Month.NOVEMBER, 30, 18, 0, 0)]),
    PiratesGlobals.FREEITEMTHANKSGIVING: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.NOVEMBER, 27, 3, 0, 0), (2008, Month.NOVEMBER, 30, 18, 0, 0)]),
    PiratesGlobals.CURSEDNIGHT: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.DECEMBER, 6, 3, 0, 0), (2008, Month.DECEMBER, 21, 3, 0, 0)]),
    PiratesGlobals.JOLLYCURSEAUTO: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.DECEMBER, 12, 12, 0, 0), (2008, Month.DECEMBER, 15, 4, 0, 0),
        (2008, Month.DECEMBER, 19, 12, 0, 0), (2008, Month.DECEMBER, 22, 4, 0, 0)])
}
holidaysEnglish = {}
holidaysJapanese = {}
holidaysGerman = {}
holidaysFrench = {}

def getHolidayDates(holidayId):
    return holidays.get(holidayId)


holidayMessages = {
    PiratesGlobals.DOUBLEGOLDHOLIDAY: (
        PLocalizer.DoubleGoldStart, 
        PLocalizer.DoubleGoldStartChat, 
        PLocalizer.DoubleGoldEnd, 
        PLocalizer.DoubleGoldEnd, 
        PLocalizer.CHAT_STATUS_DOUBLEGOLD, 'admin'), 
    PiratesGlobals.DOUBLEGOLDHOLIDAYPAID: (
        PLocalizer.DoubleGoldFullStart, 
        PLocalizer.DoubleGoldFullStartChat, 
        PLocalizer.DoubleGoldFullEnd, 
        PLocalizer.DoubleGoldFullEnd, 
        PLocalizer.CHAT_STATUS_DOUBLEGOLD_PAID, 'admin'), 
    PiratesGlobals.DOUBLEXPHOLIDAY: (
        PLocalizer.DoubleXPStart, 
        PLocalizer.DoubleXPStartChat, 
        PLocalizer.DoubleXPEnd, 
        PLocalizer.DoubleXPEnd,
        PLocalizer.CHAT_STATUS_DOUBLEXP, 'admin'),
    PiratesGlobals.DOUBLEXPHOLIDAYPAID: (
        PLocalizer.DoubleXPFullStart, 
        PLocalizer.DoubleXPFullStartChat, 
        PLocalizer.DoubleXPFullEnd, 
        PLocalizer.DoubleXPFullEnd, 
        PLocalizer.CHAT_STATUS_DOUBLEXP_PAID, 'admin'), 
    PiratesGlobals.BLACKJACKFRIDAY: (
        PLocalizer.BlackJackFridayStart, 
        PLocalizer.BlackJackFridayStartChat, 
        PLocalizer.BlackJackFridayEnd, 
        PLocalizer.BlackJackFridayEndChat, 
        PLocalizer.CHAT_STATUS_BLACKJACK_FRIDAY, 'friends'), 
    PiratesGlobals.FREEHATWEEK: (
        PLocalizer.FreeHatStartUnlimited, 
        PLocalizer.FreeHatStartUnlimitedChat, 
        None, 
        None, 
        None, 'admin'), 
    PiratesGlobals.SAINTPATRICKSDAY: (
        PLocalizer.StPatricksStartUnlimited, 
        PLocalizer.StPatricksStartUnlimitedChat, 
        None, 
        None, 
        None, 'admin'), 
    PiratesGlobals.MOTHERSDAY: (
        PLocalizer.MothersDayStartUnlimited, 
        PLocalizer.MothersDayStartUnlimitedChat, 
        None, 
        None, 
        PLocalizer.CHAT_STATUS_MOTHERS_DAY_PAID, 'tattoo'), 
    PiratesGlobals.FATHERSDAY: (
        PLocalizer.FathersDayStart, 
        PLocalizer.FathersDayStartChat, 
        None, 
        None, 
        PLocalizer.CHAT_STATUS_FATHERS_DAY, 'admin'), 
    PiratesGlobals.FOURTHOFJULY: (
        PLocalizer.FourthOfJulyStart, 
        PLocalizer.FourthOfJulyStartChat, 
        None, 
        None, 
        PLocalizer.CHAT_STATUS_FOURTHOFJULY, 'admin'), 
    PiratesGlobals.HALFOFFCUSTOMIZATION: (
        PLocalizer.HalfOffCustomizationUnlimited, 
        PLocalizer.HalfOffCustomizationUnlimited, 
        PLocalizer.HalfOffCustomizationEnd, 
        PLocalizer.HalfOffCustomizationEnd, 
        PLocalizer.HalfOffCustomizationStatus, 'admin'), 
    PiratesGlobals.ALLACCESSWEEKEND: (
        PLocalizer.UnlimitedAccessEventBasic, 
        PLocalizer.UnlimitedAccessEventBasic, 
        None,
        None,
        PLocalizer.AllAccessHolidayStart, 'admin'), 
    PiratesGlobals.HALLOWEEN: (
        PLocalizer.HalloweenStart, 
        PLocalizer.HalloweenStartChat, 
        PLocalizer.HalloweenEnd, 
        PLocalizer.HalloweenEnd, 
        PLocalizer.CHAT_STATUS_HALLOWEEN, 'admin'), 
    PiratesGlobals.JOLLYROGERCURSE: (
        None, 
        None, 
        None, 
        None, 
        PLocalizer.CHAT_STATUS_JOLLYROGERCURSE, 'admin'),
    PiratesGlobals.FOUNDERSFEAST: (
        PLocalizer.FoundersFeastStart, 
        PLocalizer.FoundersFeastStartChat,
        PLocalizer.FoundersFeastEnd, 
        PLocalizer.FoundersFeastEnd,
        PLocalizer.CHAT_STATUS_FOUNDERSFEAST, 'admin'),
    PiratesGlobals.FREEITEMTHANKSGIVING: (
        PLocalizer.FreeBandanaStartUnlimited, 
        PLocalizer.FreeBandanaStartUnlimitedChat,
        PLocalizer.FreeBandanaStartBasic, 
        PLocalizer.FreeBandanaStartBasicChat, 'hat'),
    PiratesGlobals.CURSEDNIGHT: (
        PLocalizer.CursedNightStart, 
        PLocalizer.CursedNightStart,
        PLocalizer.CursedNightEnd, 
        PLocalizer.CursedNightEnd, 'admin'), 
    PiratesGlobals.JOLLYCURSEAUTO: (       
        None, 
        None, 
        None, 
        None, 
        PLocalizer.CHAT_STATUS_JOLLYROGERCURSE, 'admin'),
    PiratesGlobals.WINTERFESTIVAL: (
        PLocalizer.WinterFestivalStart, 
        PLocalizer.WinterFestivalStartChat,
        PLocalizer.WinterFestivalEnd, 
        PLocalizer.WinterFestivalEnd,
        PLocalizer.CHAT_STATUS_WINTERFESTIVAL, 'admin'),
}

def getHolidayStartMsg(holidayId):
    return holidayMessages.get(holidayId)[0]


def getHolidayStartChatMsg(holidayId):
    return holidayMessages.get(holidayId)[1]


def getHolidayEndMsg(holidayId):
    return holidayMessages.get(holidayId)[2]


def getHolidayEndChatMsg(holidayId):
    return holidayMessages.get(holidayId)[3]


def getHolidayStatusMsg(holidayId):
    return holidayMessages.get(holidayId)[4]


def getHolidayIcon(holidayId):
    return holidayMessages.get(holidayId)[5]

discordHolidayNames = {
    PiratesGlobals.DOUBLEGOLDHOLIDAY: PLocalizer.DISCORD_DOUBLE_GOLD_HOLIDAY,
    PiratesGlobals.DOUBLEGOLDHOLIDAYPAID: PLocalizer.DISCORD_DOUBLE_GOLD_HOLIDAY_PAID,
    PiratesGlobals.DOUBLEXPHOLIDAY: PLocalizer.DISCORD_DOUBLE_EXP_HOLIDAY,
    PiratesGlobals.DOUBLEXPHOLIDAYPAID: PLocalizer.DISCORD_DOUBLE_EXP_HOLIDAY_PAID,
    PiratesGlobals.FREEHATWEEK: PLocalizer.DISCORD_FREE_HAT_WEEK,
    PiratesGlobals.SAINTPATRICKSDAY: PLocalizer.DISCORD_SAINT_PATRICKS_DAY,
    PiratesGlobals.MOTHERSDAY: PLocalizer.DISCORD_MOTHERS_DAY,
    PiratesGlobals.FATHERSDAY: PLocalizer.DISCORD_FATHERS_DAY,
    PiratesGlobals.FOURTHOFJULY: PLocalizer.DISCORD_FOURTH_OF_JULY,
    PiratesGlobals.HALFOFFCUSTOMIZATION: PLocalizer.DISCORD_HALF_OFF_CUSTOMIZATION,
    PiratesGlobals.ALLACCESSWEEKEND: PLocalizer.DISCORD_ALL_ACCESS_WEEKEND,
    PiratesGlobals.HALLOWEEN: PLocalizer.DISCORD_HALLOWEEN,
    PiratesGlobals.JOLLYROGERCURSE: PLocalizer.DISCORD_JOLLY_ROGER_CURSE,
    PiratesGlobals.FOUNDERSFEAST: PLocalizer.DISCORD_FOUNDERS_FEAST,
    PiratesGlobals.FREEITEMTHANKSGIVING: PLocalizer.DISCORD_FREE_ITEM_THANKSGIVING,
    PiratesGlobals.CURSEDNIGHT: PLocalizer.DISCORD_CURSED_NIGHT,
    PiratesGlobals.JOLLYCURSEAUTO: PLocalizer.DISCORD_JOLLY_CURSE_AUTO,
    PiratesGlobals.WINTERFESTIVAL: PLocalizer.DISCORD_WINTER_FESTIVAL
}

def getHolidayDiscordName(holidayId):
    return discordHolidayNames.get(holidayId)

discordHolidayImages = {

}

def getHolidayDiscordImage(holidayId):
    return discordHolidayImages.get(holidayId, None)

discordHolidayMessages = {
    PiratesGlobals.HALLOWEEN: """
Ahoy ye landlubbers! Jolly Roger has casted an evil spell across the Caribbean turning
everyone into undead!

Come join in on the fun! October 31st - November 3rd
        """
}

def getHolidayDiscordMessage(holidayId):
    return discordHolidayMessages.get(holidayId, '')
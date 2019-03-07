from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.ai.HolidayDates import *
Month = Enum('JANUARY, FEBRUARY, MARCH, APRIL,               MAY, JUNE, JULY, AUGUST, SEPTEMBER,               OCTOBER, NOVEMBER, DECEMBER', 1)
Day = Enum('MONDAY, TUESDAY, WEDNESDAY, THURSDAY,             FRIDAY, SATURDAY, SUNDAY')
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
    PiratesGlobals.JOLLYCURSEAUTO: 'JollyCurseAuto'}

def getHolidayName(holidayId):
    return holidayNames.get(holidayId)


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
    PiratesGlobals.SAINTPATRICKSDAY: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.MARCH, 14, 0, 0, 0),
        (2008, Month.MARCH, 18, 0, 0, 0)]),
    PiratesGlobals.MOTHERSDAY: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.MAY, 10, 0, 0, 0),
        (2008, Month.MAY, 12, 0, 0, 0)]),
    PiratesGlobals.FATHERSDAY: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.JUNE, 13, 0, 0, 0),
        (2008, Month.JUNE, 16, 0, 0, 0)]),
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
        (2008, Month.NOVEMBER, 27, 3, 0, 0),
        (2008, Month.NOVEMBER, 30, 18, 0, 0)]),
    PiratesGlobals.FREEITEMTHANKSGIVING: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.NOVEMBER, 27, 3, 0, 0),
        (2008, Month.NOVEMBER, 30, 18, 0, 0)]),
    PiratesGlobals.CURSEDNIGHT: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.DECEMBER, 6, 3, 0, 0),
        (2008, Month.DECEMBER, 21, 3, 0, 0)]),
    PiratesGlobals.JOLLYCURSEAUTO: HolidayDates(HolidayDates.TYPE_CUSTOM, [
        (2008, Month.DECEMBER, 12, 12, 0, 0),
        (2008, Month.DECEMBER, 15, 4, 0, 0),
        (2008, Month.DECEMBER, 19, 12, 0, 0),
        (2008, Month.DECEMBER, 22, 4, 0, 0)])}
holidaysEnglish = {}
holidaysJapanese = {}
holidaysGerman = {}
holidaysFrench = {}

def getHolidayDates(holidayId):
    return holidays.get(holidayId)

MSG_START_ALL = 0
MSG_START_UNLIMITED = 1
MSG_START_BASIC = 2
MSG_END_ALL = 3
MSG_END_UNLIMITED = 4
MSG_END_BASIC = 5
MSG_CHAT_STATUS = 6
MSG_ICON = 7
holidayMessages = {
    PiratesGlobals.DOUBLEGOLDHOLIDAY: {
        MSG_START_ALL: (PLocalizer.DoubleGoldStart, PLocalizer.DoubleGoldStartChat),
        MSG_END_ALL: (PLocalizer.DoubleGoldEnd, PLocalizer.DoubleGoldEnd),
        MSG_CHAT_STATUS: PLocalizer.CHAT_STATUS_DOUBLEGOLD,
        MSG_ICON: 'admin'},
    PiratesGlobals.DOUBLEGOLDHOLIDAYPAID: {
        MSG_START_ALL: (PLocalizer.DoubleGoldFullStart, PLocalizer.DoubleGoldFullStartChat),
        MSG_END_ALL: (PLocalizer.DoubleGoldFullEnd, PLocalizer.DoubleGoldFullEnd),
        MSG_CHAT_STATUS: PLocalizer.CHAT_STATUS_DOUBLEGOLD_PAID,
        MSG_ICON: 'admin'},
    PiratesGlobals.DOUBLEXPHOLIDAY: {
        MSG_START_ALL: (PLocalizer.DoubleXPStart, PLocalizer.DoubleXPStartChat),
        MSG_END_ALL: (PLocalizer.DoubleXPEnd, PLocalizer.DoubleXPEnd),
        MSG_CHAT_STATUS: PLocalizer.CHAT_STATUS_DOUBLEXP,
        MSG_ICON: 'admin'},
    PiratesGlobals.DOUBLEXPHOLIDAYPAID: {
        MSG_START_ALL: (PLocalizer.DoubleXPFullStart, PLocalizer.DoubleXPFullStartChat),
        MSG_END_ALL: (PLocalizer.DoubleXPFullEnd, PLocalizer.DoubleXPFullEnd),
        MSG_CHAT_STATUS: PLocalizer.CHAT_STATUS_DOUBLEXP_PAID,
        MSG_ICON: 'admin'},
    PiratesGlobals.BLACKJACKFRIDAY: {
        MSG_START_ALL: (PLocalizer.BlackJackFridayStart, PLocalizer.BlackJackFridayStartChat),
        MSG_END_ALL: (PLocalizer.BlackJackFridayEnd, PLocalizer.BlackJackFridayEndChat),
        MSG_CHAT_STATUS: PLocalizer.CHAT_STATUS_BLACKJACK_FRIDAY,
        MSG_ICON: 'friends'},
    PiratesGlobals.FREEHATWEEK: {
        MSG_START_UNLIMITED: (PLocalizer.FreeHatStartUnlimited, PLocalizer.FreeHatStartUnlimitedChat),
        MSG_START_BASIC: (PLocalizer.FreeHatStartUnlimited, PLocalizer.FreeHatStartUnlimitedChat),
        MSG_ICON: 'hat'},
    PiratesGlobals.SAINTPATRICKSDAY: {
        MSG_START_ALL: (PLocalizer.StPatricksStartUnlimited, PLocalizer.StPatricksStartUnlimitedChat),
        MSG_ICON: 'admin'},
    PiratesGlobals.MOTHERSDAY: {
        MSG_START_UNLIMITED: (PLocalizer.MothersDayStartUnlimited, PLocalizer.MothersDayStartUnlimitedChat),
        MSG_START_BASIC: (PLocalizer.MothersDayStartBasic, PLocalizer.MothersDayStartBasicChat),
        MSG_CHAT_STATUS: PLocalizer.CHAT_STATUS_MOTHERS_DAY_PAID,
        MSG_ICON: 'tattoo'},
    PiratesGlobals.FATHERSDAY: {
        MSG_START_ALL: (PLocalizer.FathersDayStart, PLocalizer.FathersDayStartChat),
        MSG_CHAT_STATUS: PLocalizer.CHAT_STATUS_FATHERS_DAY,
        MSG_ICON: 'admin'},
    PiratesGlobals.FOURTHOFJULY: {
        MSG_START_ALL: (PLocalizer.FourthOfJulyStart, PLocalizer.FourthOfJulyStartChat),
        MSG_CHAT_STATUS: PLocalizer.CHAT_STATUS_FOURTHOFJULY,
        MSG_ICON: 'admin'},
    PiratesGlobals.HALFOFFCUSTOMIZATION: {
        MSG_START_ALL: (PLocalizer.HalfOffCustomizationUnlimited, PLocalizer.HalfOffCustomizationUnlimited),
        MSG_END_ALL: (PLocalizer.HalfOffCustomizationEnd, PLocalizer.HalfOffCustomizationEnd),
        MSG_CHAT_STATUS: PLocalizer.HalfOffCustomizationStatus,
        MSG_ICON: 'admin'},
    PiratesGlobals.ALLACCESSWEEKEND: {
        MSG_START_BASIC: (PLocalizer.UnlimitedAccessEventBasic, PLocalizer.UnlimitedAccessEventBasic),
        MSG_CHAT_STATUS: PLocalizer.AllAccessHolidayStart,
        MSG_ICON: 'admin'},
    PiratesGlobals.HALLOWEEN: {
        MSG_START_ALL: (PLocalizer.HalloweenStart, PLocalizer.HalloweenStartChat),
        MSG_END_ALL: (PLocalizer.HalloweenEnd, PLocalizer.HalloweenEnd),
        MSG_CHAT_STATUS: PLocalizer.CHAT_STATUS_HALLOWEEN,
        MSG_ICON: 'admin'},
    PiratesGlobals.JOLLYROGERCURSE: {
        MSG_CHAT_STATUS: PLocalizer.CHAT_STATUS_JOLLYROGERCURSE,
        MSG_ICON: 'admin'},
    PiratesGlobals.FOUNDERSFEAST: {
        MSG_START_ALL: (PLocalizer.FoundersFeastStart, PLocalizer.FoundersFeastStartChat),
        MSG_END_ALL: (PLocalizer.FoundersFeastEnd, PLocalizer.FoundersFeastEnd),
        MSG_CHAT_STATUS: PLocalizer.CHAT_STATUS_FOUNDERSFEAST,
        MSG_ICON: 'admin'},
    PiratesGlobals.FREEITEMTHANKSGIVING: {
        MSG_START_UNLIMITED: (PLocalizer.FreeBandanaStartUnlimited, PLocalizer.FreeBandanaStartUnlimitedChat),
        MSG_START_BASIC: (PLocalizer.FreeBandanaStartBasic, PLocalizer.FreeBandanaStartBasicChat),
        MSG_ICON: 'hat'},
    PiratesGlobals.CURSEDNIGHT: {
        MSG_START_ALL: (PLocalizer.CursedNightStart, PLocalizer.CursedNightStart),
        MSG_END_ALL: (PLocalizer.CursedNightEnd, PLocalizer.CursedNightEnd),
        MSG_ICON: 'admin'},
    PiratesGlobals.JOLLYCURSEAUTO: {}}

def getHolidayStartMsg(holidayId, paidStatus):
    if holidayMessages.get(holidayId).has_key(MSG_START_ALL):
        return holidayMessages.get(holidayId).get(MSG_START_ALL)[0]
    elif holidayMessages.get(holidayId).has_key(MSG_START_UNLIMITED) and paidStatus:
        return holidayMessages.get(holidayId).get(MSG_START_UNLIMITED)[0]
    elif holidayMessages.get(holidayId).has_key(MSG_START_BASIC) and not paidStatus:
        return holidayMessages.get(holidayId).get(MSG_START_BASIC)[0]
    return None


def getHolidayStartChatMsg(holidayId, paidStatus):
    if holidayMessages.get(holidayId).has_key(MSG_START_ALL):
        return holidayMessages.get(holidayId).get(MSG_START_ALL)[1]
    elif holidayMessages.get(holidayId).has_key(MSG_START_UNLIMITED) and paidStatus:
        return holidayMessages.get(holidayId).get(MSG_START_UNLIMITED)[1]
    elif holidayMessages.get(holidayId).has_key(MSG_START_BASIC) and not paidStatus:
        return holidayMessages.get(holidayId).get(MSG_START_BASIC)[1]
    return None

def getHolidayEndMsg(holidayId, paidStatus):
    if holidayMessages.get(holidayId).has_key(MSG_END_ALL):
        return holidayMessages.get(holidayId).get(MSG_END_ALL)[0]
    elif holidayMessages.get(holidayId).has_key(MSG_END_UNLIMITED) and paidStatus:
        return holidayMessages.get(holidayId).get(MSG_END_UNLIMITED)[0]
    elif holidayMessages.get(holidayId).has_key(MSG_END_BASIC) and not paidStatus:
        return holidayMessages.get(holidayId).get(MSG_END_BASIC)[0]
    return None

def getHolidayEndChatMsg(holidayId, paidStatus):
    if holidayMessages.get(holidayId).has_key(MSG_END_ALL):
        return holidayMessages.get(holidayId).get(MSG_END_ALL)[1]
    elif holidayMessages.get(holidayId).has_key(MSG_END_UNLIMITED) and paidStatus:
        return holidayMessages.get(holidayId).get(MSG_END_UNLIMITED)[1]
    elif holidayMessages.get(holidayId).has_key(MSG_END_BASIC) and not paidStatus:
        return holidayMessages.get(holidayId).get(MSG_END_BASIC)[1]
    return None

def getHolidayStatusMsg(holidayId):
    if holidayMessages.get(holidayId).has_key(MSG_CHAT_STATUS):
        return holidayMessages.get(holidayId).get(MSG_CHAT_STATUS)
    return None

def getHolidayIcon(holidayId):
    if holidayMessages.get(holidayId).has_key(MSG_ICON):
        return holidayMessages.get(holidayId).get(MSG_ICON)
    return None


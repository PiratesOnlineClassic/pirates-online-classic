
class DiscordMentions:
    """
    Contains all possible Discord mentions the game has access too
    """

    Everyone = '@everyone'

class DiscordChannels:
    """
    Contains all Discord channels the game has access too
    """

    # Sandbox
    SandboxGeneral = 271779649313439753
    SandboxWebhooks = 309745967907733504

    # Staff
    StaffAnnouncements = 430870801005150209
    StaffEvaluationPolls = 430870772878409738
    StaffInternalReleaseNotes = 542131149066076193
    StaffUpdates = 430871490481750018
    StaffGeneral = 430822422984523779
    StaffLeads = 430870148707254282
    StaffLogChannel = 430877077357723648
    StaffDevelopment = 430823903846465537
    StaffVerificationIssues = 552472982862299148
    StaffBugList = 456228201161818133
    StaffBetaChecklist = 460618982836142090
    StaffServerIssues = 436731946828300301
    StaffCrashLogs = 433429385698213888
    StaffWebDevelopment = 430874021463195648
    StaffDiscordSandbox = 431167445735178241
    StaffBotTest = 489756496578740224
    StaffCMNotices = 430874379996626944
    StaffCommunications = 430874393347096576
    StaffSeniorCM = 430882697221636100
    StaffHackerLog = 430876132175380481
    StaffGMNotices = 430868740037410816
    StaffGameMasters = 430868775286603776
    StaffSeniorGM = 430868809096757248

    # Public
    PublicReadThisFirst = 432427998038196235
    PublicAnnouncements = 431658283284168704
    PublicEvaluationPolls = 431658307883630593
    PublicRulesAndGuidelines = 431658261100363776
    PublicSneakPeaks = 433411676444950538
    PublicProgressLog = 433411777523613696
    PublicDevelopmentEncylopedia = 455541031874723841
    PublicGeneral = 431519069380804608
    PublicGMNotices = 433411250903449611
    PublicSupport = 431938771911442442
    PublicGuildRecruitment = 433819651366060052
    PublicMusic = 432447685832736788
    PublicModChat = 432002631179829258
    PublicLogs = 431914144770424856
    PublicTheGallows = 432306465420607490

class DiscordColorCode:
    Green = 7601920
    Red = 16711680

BotAuthorization = 'Bot %s' % config.GetString('discord-bot-token', '')
MessageUrl = 'https://discordapp.com/api/channels/%s/messages'

def getChannelMessageUrl(channel):
    return MessageUrl % channel
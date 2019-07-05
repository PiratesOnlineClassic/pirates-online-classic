
class DiscordWebhooks:
    """
    Contains all Discord webhook urls
    """

    DiscordPlayground = 'https://discordapp.com/api/webhooks/309745988401102849/i2Xhy-qTeCgTKOL4DkPKoIZarAIVsYtcY8UyGPnlqo-lwnAd4qUJcgO9QsI7ckWvkCir'
    ServerIssues = 'https://discordapp.com/api/webhooks/436732182396928000/8sQtnSPEl7sck9Q3UR4FbyF2MemNkEGSvQETo_Bnvv4Z4vc2N619XWA-0k0F8ZfXSQnj'
    
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
    StaffDevelopment = 430823903846465537
    StaffBugList = 456228201161818133
    StaffBetaChecklist = 460618982836142090
    StaffServerIssues = 436731946828300301
    StaffCrashLogs = 433429385698213888
    StaffWebDevelopment = 430874021463195648
    StaffDiscordSandbox = 431167445735178241

BotAuthorization = 'Bot %s' % config.GetString('discord-bot-token', '')
"""
The Pirates specific SpeedChat checks, on top of otp.chat.ChatFilter.
"""

from pirates.piratesbase import PLocalizer
from pirates.quest import QuestDB


def isValidSpeedChatEmote(emoteId):
    # Every client looks the emote up when it logs the message.
    return emoteId in PLocalizer.EmoteMessagesThirdPerson


def isValidSpeedChatQuest(questInt, msgType, taskNum):
    """
    Returns True if the quest SpeedChat message is one the client's quest
    menu can offer (PSpeedChatQuestMenu), which every client receiving it
    decodes out of the QuestDB.
    """

    if msgType not in (0, 1, 2):
        return False

    questId = QuestDB.questIntDict.get(questInt)
    questDNA = QuestDB.QuestDict.get(questId)
    if questDNA is None:
        return False

    numTasks = len(questDNA.getTasks())
    return numTasks == 1 or 0 <= taskNum < numTasks

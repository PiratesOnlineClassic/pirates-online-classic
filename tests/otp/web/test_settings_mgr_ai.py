import unittest
from unittest.mock import Mock

from otp.distributed.CentralLoggerUD import CentralLoggerUD
from otp.web.Setting import Setting
from otp.web.SettingsMgrAI import SettingsMgrAI


class SettingsMgrAITests(unittest.TestCase):
    def makeManager(self):
        mgr = SettingsMgrAI.__new__(SettingsMgrAI)
        mgr.air = Mock()
        mgr.air.getAvatarIdFromSender.return_value = 5
        mgr.air.doId2do = {5: Mock(doId=5)}
        mgr._settings = {}
        mgr._originalValueReprs = {}
        mgr._currentValueReprs = {}
        mgr._addSettings(Setting('a', 1), Setting('b', 'text'))
        mgr.sendUpdate = Mock()
        mgr.sendUpdateToAvatarId = Mock()
        return mgr

    def test_only_changed_settings_sent_as_strings(self):
        mgr = self.makeManager()
        mgr.requestAllChangedSettings()
        mgr.sendUpdateToAvatarId.assert_not_called()

        mgr.settingChange('b', repr('other'))
        self.assertEqual(mgr._getSetting('b').getValue(), 'other')
        mgr.requestAllChangedSettings()
        mgr.sendUpdateToAvatarId.assert_called_once_with(5, 'settingChange', ['b', "'other'"])

    def test_unknown_setting_ignored(self):
        mgr = self.makeManager()
        mgr.settingChange('missing', '1')
        mgr.sendUpdate.assert_not_called()


class CentralLoggerUDTests(unittest.TestCase):
    def test_client_event_logged_with_sender(self):
        logger = CentralLoggerUD.__new__(CentralLoggerUD)
        logger.air = Mock()
        logger.air.getAvatarIdFromSender.return_value = 7
        logger.sendMessage('ClientEvent', 'GUEST_FEEDBACK', 0, 0)
        args, kwargs = logger.air.writeServerEvent.call_args
        self.assertEqual(args, ('ClientEvent',))
        self.assertEqual(kwargs['avId'], 7)
        self.assertNotIn('feedbackCategory', kwargs)


if __name__ == '__main__':
    unittest.main()

import dbm.dumb
import sys
import types
import unittest
from unittest.mock import Mock

try:
    import semidbm
except ImportError:
    # semidbm is only needed by the live UberDOG; dbm.dumb has the same API.
    sys.modules['semidbm'] = types.SimpleNamespace(open=dbm.dumb.open)

from pirates.coderedemption.CodeRedemptionUD import CodeRedemptionUD, CodeReward
from pirates.economy import AwardGlobals


AV_ID = 100000001


def makeRedemption(codes):
    redemption = CodeRedemptionUD.__new__(CodeRedemptionUD)
    redemption.air = Mock()
    redemption.air.getAvatarIdFromSender.return_value = AV_ID
    redemption.verifyEndpoint = ''
    redemption.codes = dict((reward.code, reward) for reward in codes)
    redemption.pendingAvatars = set()
    redemption.redeemedDB = {}
    redemption.sendUpdateToAvatarId = Mock()
    return redemption


class CodeRedemptionTests(unittest.TestCase):
    def test_config_parse(self):
        reward = CodeReward.fromConfig('Ahoy;7;0;500')
        self.assertEqual((reward.code, reward.awardType, reward.itemId, reward.quantity), ('ahoy', 7, 0, 500))
        reward = CodeReward.fromConfig('shirt;2;10;3;20')
        self.assertEqual(reward.getItemId('f'), 20)
        self.assertEqual(reward.getItemId('m'), 10)
        self.assertRaises(ValueError, CodeReward.fromConfig, 'bad;1')

    def test_unknown_code_fails(self):
        redemption = makeRedemption([])
        redemption.sendCodeForRedemption('nope', '')
        redemption.sendUpdateToAvatarId.assert_called_with(AV_ID, 'notifyClientCodeRedeemStatus', [0])

    def test_code_redeemed_once(self):
        redemption = makeRedemption([CodeReward('ahoy', AwardGlobals.GOLD, 0, 500)])
        redemption.air.awardMaker.giveAward.side_effect = \
            lambda avId, awardType, itemId, quantity, callback: callback(True)

        redemption.sendCodeForRedemption(' AHOY ', '')
        redemption.air.awardMaker.giveAward.assert_called_once()
        redemption.sendUpdateToAvatarId.assert_called_with(AV_ID, 'notifyClientCodeRedeemStatus', [1])

        redemption.sendCodeForRedemption('ahoy', '')
        redemption.air.awardMaker.giveAward.assert_called_once()
        redemption.sendUpdateToAvatarId.assert_called_with(AV_ID, 'notifyClientCodeRedeemStatus', [0])

    def test_failed_award_can_retry(self):
        redemption = makeRedemption([CodeReward('ahoy', AwardGlobals.GOLD, 0, 500)])
        redemption.air.awardMaker.giveAward.side_effect = \
            lambda avId, awardType, itemId, quantity, callback: callback(False)
        redemption.sendCodeForRedemption('ahoy', '')
        self.assertFalse(redemption.hasRedeemed('ahoy', AV_ID))
        self.assertEqual(redemption.pendingAvatars, set())

    def test_gendered_reward(self):
        redemption = makeRedemption([CodeReward('shirt', AwardGlobals.CLOTHING, 10, 3, 20)])
        redemption.air.avatarManager.getAvatarGender.side_effect = lambda avId, callback: callback('f')
        redemption.sendCodeForRedemption('shirt', '')
        args = redemption.air.awardMaker.giveAward.call_args[0]
        self.assertEqual(args[:4], (AV_ID, AwardGlobals.CLOTHING, 20, 3))


if __name__ == '__main__':
    unittest.main()

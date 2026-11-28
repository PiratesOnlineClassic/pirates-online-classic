import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

try:
    import semidbm
except ImportError:  # the live UberDOG needs it, the other tests fall back to dbm.dumb
    semidbm = None


@unittest.skipIf(semidbm is None, 'semidbm is not installed')
class SemidbmStoreTests(unittest.TestCase):
    # semidbm keeps it's keys as bytes, so a str key is never "in" it even
    # right after storing under it. Every UberDOG store has to look its keys
    # up as bytes, and has to read back what it stored after a restart.

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def path(self, name):
        return os.path.join(self.tmp.name, name)

    def test_wardrobes_read_back_and_survive_a_restart(self):
        from pirates.economy.AvatarAccessoriesManagerUD import AccessoriesDB
        db = AccessoriesDB(self.path('accessories'))
        self.assertEqual(db.getWardrobe(5), {'clothing': [], 'jewelry': [], 'tattoos': []})
        db.setWardrobe(5, {'clothing': [[10000, 3, 0]], 'jewelry': [7], 'tattoos': []})
        self.assertEqual(db.getWardrobe(5)['clothing'], [[10000, 3, 0]])
        db.close()

        db = AccessoriesDB(self.path('accessories'))
        self.assertEqual(db.getWardrobe(5), {'clothing': [[10000, 3, 0]], 'jewelry': [7], 'tattoos': []})
        db.close()

    def test_guilds_and_guild_ids_survive_a_restart(self):
        from otp.friends.GuildManagerUD import GuildDB
        db = GuildDB(semidbm.open(self.path('guilds'), 'c'))
        self.assertEqual(db.allocateGuildId(), 1)
        self.assertEqual(db.allocateGuildId(), 2)
        db.storeGuild(1, {'name': 'Black Gulls'})
        db.storeGuild(2, {'name': 'Sea Dogs'})
        db.deleteGuild(2)
        db.dbm.close()

        db = GuildDB(semidbm.open(self.path('guilds'), 'c'))
        self.assertEqual(db.getGuild(1), {'name': 'Black Gulls'})
        self.assertIsNone(db.getGuild(2))
        self.assertEqual(db.getGuildIds(), [1])

        # a new guild never takes over an existing guild's id...
        self.assertEqual(db.allocateGuildId(), 3)
        db.dbm.close()

    def test_a_code_is_only_redeemed_once(self):
        from pirates.coderedemption.CodeRedemptionUD import CodeRedemptionUD
        ud = CodeRedemptionUD.__new__(CodeRedemptionUD)
        ud.redeemedDB = semidbm.open(self.path('codes'), 'c')
        self.assertFalse(ud.hasRedeemed('PIRATES', 5))
        ud.setRedeemed('PIRATES', 5)
        self.assertTrue(ud.hasRedeemed('PIRATES', 5))
        self.assertFalse(ud.hasRedeemed('PIRATES', 6))
        ud.redeemedDB.close()

        ud.redeemedDB = semidbm.open(self.path('codes'), 'c')
        self.assertTrue(ud.hasRedeemed('PIRATES', 5))
        ud.redeemedDB.close()

    def test_holiday_states_read_back(self):
        from pirates.discord.DiscordNotificationsUD import DiscordNotificationsUD
        ud = DiscordNotificationsUD.__new__(DiscordNotificationsUD)
        ud.notify = Mock()
        ud.holidayDb = semidbm.open(self.path('holidays'), 'c')
        self.assertFalse(ud.getHolidayState(12))
        ud.storeHolidayState(12, True)
        ud.storeHolidayState(13, False)
        ud.holidayDb.close()

        ud.holidayDb = semidbm.open(self.path('holidays'), 'c')
        self.assertTrue(ud.getHolidayState(12))
        self.assertFalse(ud.getHolidayState(13))
        ud.holidayDb.close()


if __name__ == '__main__':
    unittest.main()

import unittest

from direct.distributed.PyDatagramIterator import PyDatagramIterator

from otp.ai import AIInterestHandles
from otp.distributed.MsgTypes import CLIENTAGENT_ADD_INTEREST, CLIENTAGENT_ADD_INTEREST_MULTIPLE, \
    CLIENTAGENT_REMOVE_INTEREST
from otp.distributed.OTPInternalRepository import OTPInternalRepository
from pirates.world.WorldGridManagerAI import GridInterestContextAllocator


class AIInterestIdTests(unittest.TestCase):
    # the client numbers it's own interests from 1, the interests the AI opens for it
    # live in the upper half of the ids, where the client closes them
    # (DoInterestManager._sendRemoveAIInterest sends (1 << 15) + handle)

    def makeAir(self):
        air = OTPInternalRepository.__new__(OTPInternalRepository)
        air.ourChannel = 401000000
        air.sent = []
        air.send = air.sent.append
        return air

    def readInterestId(self, dg):
        di = PyDatagramIterator(dg)
        di.getUint8()  # channel count
        di.getUint64()  # client channel
        di.getUint64()  # sender
        msgType = di.getUint16()
        return msgType, di.getUint16()

    def test_ai_interests_are_opened_where_the_client_closes_them(self):
        air = self.makeAir()
        air.clientAddInterest(1000000000, AIInterestHandles.PIRATES_BAND, 1, 2, False)
        air.clientAddInterestMultiple(1000000000, AIInterestHandles.PIRATES_TREASUREMAP, 1, [2, 3], False)
        air.clientRemoveInterest(1000000000, AIInterestHandles.PIRATES_TREASUREMAP, False)

        self.assertEqual([self.readInterestId(dg) for dg in air.sent], [
            (CLIENTAGENT_ADD_INTEREST, (1 << 15) + AIInterestHandles.PIRATES_BAND),
            (CLIENTAGENT_ADD_INTEREST_MULTIPLE, (1 << 15) + AIInterestHandles.PIRATES_TREASUREMAP),
            (CLIENTAGENT_REMOVE_INTEREST, (1 << 15) + AIInterestHandles.PIRATES_TREASUREMAP)])

    def test_grid_interests_never_take_a_fixed_ai_handle(self):
        handles = {(1 << 15) + value for name, value in vars(AIInterestHandles).items()
            if name.startswith('PIRATES_')}
        allocator = GridInterestContextAllocator()
        contexts = {allocator.allocate() for _ in range(GridInterestContextAllocator.MaxContext -
            GridInterestContextAllocator.MinContext + 1)}
        self.assertFalse(handles & contexts)
        self.assertTrue(all(context & (1 << 15) for context in contexts))


if __name__ == '__main__':
    unittest.main()

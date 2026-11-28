import unittest

from direct.distributed.PyDatagram import PyDatagram

from otp.distributed.AstronInternalRepository import msgpack_encode


def encode(value):
    dg = PyDatagram()
    msgpack_encode(dg, value)
    return dg.getMessage()


class MsgpackEncodeTests(unittest.TestCase):
    # server events (writeServerEvent) are sent to the event logger as MsgPack

    def test_tuples_are_sent_as_arrays(self):
        # the shopkeepers log what was bought as (itemId, quantity) pairs...
        self.assertEqual(encode([(1, 2), (3, 4)]), encode([[1, 2], [3, 4]]))
        self.assertEqual(encode({'buying': [(1, 2)]}), bytes([0x81, 0xa6]) + b'buying' + bytes([0x91, 0x92, 1, 2]))

    def test_an_unpackable_value_names_itself(self):
        with self.assertRaises(TypeError) as context:
            encode({'value': {1, 2}})

        self.assertIn('{1, 2}', str(context.exception))


if __name__ == '__main__':
    unittest.main()

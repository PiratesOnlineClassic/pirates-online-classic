import sys
import os
import __builtin__
import StringIO
import zlib
import pyaes

from panda3d.core import *


def main():
    IV = ''.join(['0'] * 16)
    KEY = 'ExampleKey123456'

    cipher = pyaes.AESModeOfOperationOFB(
        KEY, iv=IV)

    del IV
    del KEY

    if not os.path.exists('gamedata.bin'):
        raise SystemExit

    with open('gamedata.bin', 'rb') as f:
        data = f.read()
        f.close()

    try:
        data = cipher.decrypt(data)
    except:
        raise SystemExit

    del cipher

    datagram = Datagram(data)
    di = DatagramIterator(datagram)

    del data

    try:
        num_dc_files = di.get_uint8()
        num_config_files = di.get_uint8()
    except:
        raise SystemExit

    for _ in xrange(num_config_files):
        try:
            length = di.get_uint16()
        except:
            raise SystemExit

        if not di.get_remaining_size():
            raise SystemExit

        try:
            data = zlib.decompress(di.extract_bytes(length))
        except:
            raise SystemExit

        io = StringIO.StringIO(data)

        for line in io.readlines():
            if not line or line == '\n':
                continue

            load_prc_file_data('config data', line)

        io.close()

        del length
        del data
        del io

    __builtin__.dcStream = StringStream()

    for _ in xrange(num_dc_files):
        try:
            length = di.get_uint16()
        except:
            raise SystemExit

        if not di.get_remaining_size():
            raise SystemExit

        try:
            data = zlib.decompress(di.extract_bytes(length))
        except:
            raise SystemExit

        dcStream.set_data(dcStream.get_data() + data)

        del length
        del data

    from pirates.piratesbase import PiratesStart

    return 0

if __name__ == '__main__':
    sys.exit(main())

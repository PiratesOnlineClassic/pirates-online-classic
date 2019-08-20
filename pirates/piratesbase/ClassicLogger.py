import time
import sys
import os

ltime = time.localtime()
prefix = 'poc-'  # define the prefix
suffix = '%02d%02d%02d_%02d%02d%02d' % (ltime[0] - 2000, ltime[1], ltime[2],
                                        ltime[3], ltime[4], ltime[5])  # get the time

if not os.path.exists('logs/'):
    # if the folder doesnt exist, create it
    os.mkdir('logs')

# Apply the prefix/suffix to the log file
LOGFILE = 'logs/' + prefix + suffix + '.log'


class LogAndOutput:
    def __init__(self, out, file):
        self.out = out
        self.file = file
        self.__buffer = ''

    def write(self, string):
        # Write the log data
        self.out.write(string)

        asctime = time.asctime()
        self.__buffer += string
        while '\n' in self.__buffer:
            data, self.__buffer = self.__buffer.split('\n', 1)
            data = data.rstrip()
            if data:
                formatted = '%s: %s\n' % (asctime, data)
                self.file.write(formatted)
        # Were done
        self.flush()

    def flush(self):
        self.file.flush()
        self.out.flush()


file = open(LOGFILE, 'wb')
sys.stdout = LogAndOutput(sys.stdout, file)
sys.stderr = LogAndOutput(sys.stderr, file)


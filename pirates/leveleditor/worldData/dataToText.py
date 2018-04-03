# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.leveleditor.worldData.dataToText
import direct, sys
dataFileName = sys.argv[1]
textFileName = sys.argv[2]
dataModule = dataFileName.split('.py')[0]
print 'Parsing %s.py --> %s\n' % (dataModule, textFileName)
exec 'from pirates.leveleditor.worldData.%s import *' % dataModule
lines = []
for mainUid in objectStruct['Objects']:
    mainObj = objectStruct['Objects'][mainUid]
    lines.append('Name:\t%s\t%s\nType:\t%s\n\n' % (mainObj['Name'], mainUid, mainObj['Type']))
    for uid in mainObj['Objects']:
        object = mainObj['Objects'][uid]
        lines.append('%s\t%s\t%s\n' % (uid, object['Type'], `(object['Pos'])`))

    lines.append('\n')

textFile = file(textFileName, 'w')
textFile.writelines(lines)
textFile.close()
# okay decompiling .\pirates\leveleditor\worldData\dataToText.pyc

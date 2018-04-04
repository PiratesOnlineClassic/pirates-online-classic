from panda3d.core import *
from panda3d.direct import *
from direct.directnotify.DirectNotifyGlobal import directNotify
import argparse
import traceback
import sys
import os

os.chdir('..')

parser = argparse.ArgumentParser()
parser.add_argument('--type', default='AI', help='Server type to generate files for (AI, UD)')
parser.add_argument('dc', nargs='*', help ='DC files to generate stubs for')
args = parser.parse_args()

dcFiles = args.dc
ignoredFields = ['setParentingRules']
ignoredClasses = []
genType = args.type

stub_body = '''%(comment)s
%(imports)s
from direct.directnotify import DirectNotifyGlobal

class %(dclassName)s(%(bases)s):
    notify = DirectNotifyGlobal.directNotify.newCategory('%(dclassName)s')

    def __init__(self, air):
%(init)s
%(defvalues)s

%(methods)s
'''

notify = directNotify.newCategory('StubGenerator')
notify.setInfo(True)

dc = DCFile()
for dcFile in dcFiles:
    dc.read(dcFile)

importDict = {}
dclassesByName = {}

notify.info('Parsing DC files...')

for i in xrange(dc.getNumImportModules()):
    moduleName = '.'.join(dc.getImportModule(i).split('.')[:2])
    importSymbols = []
    for j in range(dc.getNumImportSymbols(i)):
        symbolName, suffixes = (dc.getImportSymbol(i, j) + '/').split('/', 1)
        suffixes = suffixes.split('/')
        if genType in suffixes:
            symbolName += genType

        importDict[symbolName] = moduleName

for i in xrange(dc.getNumClasses()):
    dclass = dc.getClass(i)
    name = dclass.getName()
    if name + genType in importDict:
        name += genType
        
    parents = []
    for j in xrange(dclass.getNumParents()):
        base = dclass.getParent(j).getName()
        if base + genType in importDict:
            base += genType
            
        parents.append(base)

    dclassesByName[name] = (parents, dclass)

def getDefault(args):
    r = []
    for arg in args:
        if 'int' in arg:
            r.append(0)

        elif 'string' in arg or 'blob' in arg:
            r.append('')

        elif '[' in arg:
            r.append([])

        elif 'DoId' in arg:
            r.append(0)

        elif 'bool' in arg:
            r.append(False)

        elif 'SkillId' in arg:
            r.append(0)

        elif 'CardHand' in arg:
            r.append([])

        else:
            notify.warning('Unknown argument: %s' % arg)
            r.append(None)
            #raise ValueError(arg)

    return r if len(r) > 1 else r[0]

def createErrorStub(path, name, type):
    notify.debug('Generating basic error stub')
    stubData = '''# AN UNEXPECTED ERROR OCCURED WHILE GENERATING THIS STUB FILE.
from direct.distributed.DistributedObject%(type)s import DistributedObject%(type)s
from direct.directnotify import DirectNotifyGlobal

class %(name)s(DistributedObject%(type)s):
    notify = DirectNotifyGlobal.directNotify.newCategory('%(name)s')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)''' % locals()

    stub = open(path, 'wb')
    stub.write(stubData)
    stub.close()


notify.info('Generating stubs...')
for name in dclassesByName:
    if name.endswith(genType):

        notify.debug('Processing %s...' % name)

        try:
            fileDirectory = str(importDict[name]).replace(".", "/") + "/"
            filePath = '%s%s.py' % (fileDirectory, name)

            if os.path.exists(filePath):
                notify.debug('File %s already exists at %s. Skipping class.' % (name, filePath))
                continue

            if 'direct/distributed' in filePath:
                continue

            basesList, dclass = dclassesByName.get(str(name), ([], None))
            comment = ''

            if not basesList:
                basesList.append('DistributedObject%s' % genType)
                comment = '# NO BASE CLASSES WERE FOUND! \n #THIS CLASS LIKELY HAD NO DEFINITION IN THE DCLASS FILES WHEN stub_generator.py WAS RUN!\n'
                notify.warning('%s has no base classes. Defaulting to DistributedObject%s' % (name, genType))

            bases = ', '.join(basesList)
            notify.debug('Bases: %s' % bases)

            init = '\n'.join(' ' * 8 + '%s.__init__(self, air)' % base for base in basesList)
            notify.debug('Init: %s' % init)

            imports = '\n'.join(['from %s.%s import %s' % (importDict[base], base, base) for base in basesList])
            notify.debug('Imports: %s' % imports)

            methods = ''
            defvalues = ''

            if dclass:
                for index in xrange(dclass.getNumFields()):
                    field = repr(dclass.getField(index))

                    if not '(' in field:
                        continue

                    fieldName, keywords = field.rsplit(')', 1)
                    fieldName, args = fieldName.split('(', 1)
                    args = args.split(',')
                    keywords = keywords.split()

                    if fieldName in ignoredFields:
                        continue

                    fieldName1 = fieldName[1:]

                    genComment = True
                    if 'airecv' in keywords and not genType == 'AI':
                        genComment = False

                    if genComment:
                        methods += ' ' * 4 + '# %s\n' % field

                    if 'required' in keywords:
                        paramName = fieldName[3].lower() + fieldName[4:] if fieldName.startswith('set') else fieldName
                        parameters = ['todo_%s_%d' % (type.strip(' []').replace('/','_').replace('(', '_').replace(')', '_').replace('-', '_'), j) for j, type in enumerate(args)]
                        parameters[0] = paramName
                        parameters = ', '.join(parameters)                    

                        # Setter / getter
                        defvalues += '        self.%s = %r\n' % (paramName, getDefault(args))
                        methods += '''    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def %(fieldName)s(self, %(parameters)s):
        self.%(paramName)s = %(paramName)s

    def d_%(fieldName)s(self, %(parameters)s):
        self.sendUpdate('%(fieldName)s', [%(parameters)s])

    def b_%(fieldName)s(self, %(parameters)s):
        self.%(fieldName)s(%(parameters)s)
        self.d_%(fieldName)s(%(parameters)s)

    def g%(fieldName1)s(self):
        return self.%(paramName)s

'''  % locals()
                    elif 'airecv' in keywords and genType == 'AI':
                        paramName = fieldName[3].lower() + fieldName[4:] if fieldName.startswith('set') else fieldName
                        parameters = ['todo_%s_%d' % (type.strip(' []').replace('/','_').replace('(', '_').replace(')', '_').replace('-', '_'), j) for j, type in enumerate(args)]
                        parameters[0] = paramName
                        parameters = ', '.join(parameters)

                        # Placeholder
                        methods += '''
    def %(fieldName)s(self, %(parameters)s):
        pass

''' % locals()

                    elif len(keywords) == 0 or 'broadcast' in keywords:
                        paramName = fieldName[3].lower() + fieldName[4:] if fieldName.startswith('set') else fieldName
                        parameters = ['todo_%s_%d' % (type.strip(' []').replace('/','_').replace('(', '_').replace(')', '_').replace('-', '_'), j) for j, type in enumerate(args)]
                        parameters[0] = paramName
                        parameters = ', '.join(parameters)

                        # Placeholder
                        if len(args) > 0:
                            methods += '''
    def %(fieldName)s(self, %(parameters)s):
        self.sendUpdate('%(fieldName)s', [%(parameters)s])

''' % locals()          
                        else:
                            methods += '''
    def %(fieldName)s(self):
        self.sendUpdate('%(fieldName)s', [])

''' % locals()                 

                    else:
                        methods += '\n'

            dclassName = name #ugly

            notify.info('Generating %s' % filePath)
            stub = open(filePath, 'wb')
            stub.write(stub_body % locals())
            stub.close()

            notify.debug('=' * 20)

        except Exception as e:
            notify.warning('Unexpected error occured while processing %s...' % name)
            #traceback.print_exc()
            notify.warning('Attempting to generate default stub...')
            try:
                createErrorStub(str(importDict[name]).replace(".", "/") + "/" + name + ".py", name, genType)
            except:
                notify.warning('Failed to generate default stub for %s' % name)
                traceback.print_exc()
            continue 

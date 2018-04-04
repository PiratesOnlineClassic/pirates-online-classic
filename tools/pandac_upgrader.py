import os, glob, sys
import inspect
import logging

import panda3d.core
import panda3d.direct
import panda3d.bullet
import panda3d.ai
import panda3d.ode

coreImports = inspect.getmembers(panda3d.core, inspect.isclass)
directImports = inspect.getmembers(panda3d.direct, inspect.isclass)
bulletImports = inspect.getmembers(panda3d.bullet, inspect.isclass)
aiImports = inspect.getmembers(panda3d.ai, inspect.isclass)
odeImports = inspect.getmembers(panda3d.ode, inspect.isclass)

pandaImports = {
    'core': coreImports,
    'direct': directImports,
    'bullet': bulletImports,
    'ai': aiImports,
    'ode': odeImports
}

logging.basicConfig(filename='pandac_upgrader.txt', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

def scandirs(path):
    for currentFile in glob.glob( os.path.join(path, '*') ):
        if os.path.isdir(currentFile):
            scandirs(currentFile)
        if currentFile.endswith('py'):
            filedata = None
            with open(currentFile, 'r') as file:
                filedata = file.read()

            if 'from pandac.PandaModules import *' in filedata:
                found = {}
                potential = {}
                for key in pandaImports:
                    found[key] = []
                    potential[key] = []
                    classes = pandaImports[key]
                    for c in classes:
                        name = c[0]
                        if name + "(" in filedata:
                            found[key].append(name + "(")
                        elif name in filedata:
                            potential[key].append(name)
            
                logging.info('%s has pandac imports!' % currentFile)

                if len(found) > 0:
                    Imports = ''
                    for key in found:
                        if len(found[key]) > 0:
                            pImport = 'from panda3d.%s import %s' % (key, ', '.join([str(x) for x in found[key]]))
                            Imports += pImport + '\n'

                    filedata = filedata.replace('from pandac.PandaModules import *', Imports)
                else:
                    filedata = filedata.replace('from pandac.PandaModules import *', '')
                    logging.info('%s has unnessisary pandac imports. removing.' % currentFile)

                with open(currentFile, 'w') as file:
                    file.write(filedata)
                logging.info('Updated: %s!' % currentFile)
                if len(potential) > 0:
                    logging.info('%s has potential missing imports. %s were detected but not added.' % (currentFile, potential))

            if 'from pandac.PandaModules import' in filedata:
                logging.info('%s has pandac imports!' % currentFile)
                filedata = filedata.replace('from pandac.PandaModules', 'from panda3d.core')
                with open(currentFile, 'w') as file:
                    file.write(filedata)
                logging.info('Updated: %s!' % currentFile)


if __name__ == '__main__':
	path = '../pirates'
	scandirs(path)
	path = '../otp'
	scandirs(path)
	logging.info('Done!')
from pandac.PandaModules import loadPrcFile
import os

if __debug__:
    loadPrcFile('config/general.prc')
    loadPrcFile('config/dev.prc')

    if os.path.exists('config/personal.prc'):
        loadPrcFile('config/personal.prc')

from pirates.launcher.PiratesQuickLauncher import PiratesQuickLauncher
launcher = PiratesQuickLauncher()
launcher.notify.info('Reached end of StartPiratesLauncher.py.')

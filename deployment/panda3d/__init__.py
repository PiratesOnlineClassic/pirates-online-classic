"""
This file is an import hook package initializer to load all of
the panda3d core pyd modules without the use of a package initializer
outside of the executable runtime environment...
"""

import sys
import os
import imp
import platform


class Panda3dImporter(object):
    """
    Dynamic module import hook to import panda3d dynamic modules
    from disk without exposing the panda3d package...
    """

    def __init__(self, dynamic_modules):
        self._dynamic_modules = dynamic_modules

    @property
    def dynamic_modules(self):
        """
        Returns the importer's dynamic module dictionary.
        """

        return self._dynamic_modules

    def find_module(self, fullname, path):
        """
        Finds the dynamic module by filepath...
        """

        fullnames = fullname.split('.')

        if len(fullnames) > 1:
            for name in path:
                if name in fullnames:
                    fullnames.remove(name)

            if len(fullnames) > 1:
                raise ImportError('Cannot find module: %s!' % fullname)

            name = fullnames[0]
        else:
            name = fullnames

        if name not in self._dynamic_modules:
            raise ImportError('Cannot find module: %s!' % fullname)

        return self

    def load_module(self, fullname):
        """
        Loads the dynamic module from the filepath...
        """

        name = fullname.split('.')
        name = name[len(name) - 1]

        if not name:
            raise ImportError('Cannot load module: %s!' % fullname)

        filename = self._dynamic_modules.get(name)

        if not filename:
            raise ImportError('Cannot load module: %s!' % fullname)

        module = imp.load_dynamic(name, filename)

        if not module:
            raise ImportError('Cannot load module: %s!' % fullname)

        return module

def format_dynamic(filename):
    """
    Formats the dynamic module name with an extension
    corresponding to the operating system...
    """

    if platform.system() == 'Windows':
        extension = '.pyd'
    else:
        extension = '.so'

    return '%s%s' % (filename, extension)

sys.meta_path.insert(0, Panda3dImporter({
    'direct': format_dynamic('direct'),
    'core': format_dynamic('core'),
    'egg': format_dynamic('egg'),
    'fx': format_dynamic('fx'),
    'interrogatedb': format_dynamic('interrogatedb'),
    'physics': format_dynamic('physics'),
}))

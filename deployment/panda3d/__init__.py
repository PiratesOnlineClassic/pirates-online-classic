"""
This file is an import hook package initializer to load all of
the panda3d core pyd modules without the use of a package initializer
outside of the executable runtime environment...
"""

import sys
import os
import imp
import importlib
import multiprocessing
import platform


class Panda3dImporter(object):
    """
    Dynamic module import hook to import panda3d dynamic modules
    from disk without exposing the panda3d package...
    """

    def __init__(self, dynamic_modules):
        self._dynamic_modules = dynamic_modules
        self._module_cache = {}
        self._process = None

    @property
    def dynamic_modules(self):
        """
        Returns the importer's dynamic module dictionary.
        """

        return self._dynamic_modules

    @property
    def module_cache(self):
        """
        Returns the importer's dynamic module cache dictionary.
        """

        return self._module_cache

    @property
    def process(self):
        """
        Returns the importer's process in which loads the dynamic module.
        """

        return self._process

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
        if name not in self._dynamic_modules:
            raise ImportError('Cannot find module: %s!' % fullname)

        return self

    def load_module(self, fullname):
        """
        Loads the dynamic module from the filepath...
        """

        imp.acquire_lock()

        name = fullname.split('.')
        name = name[len(name) - 1]

        if not name:
            raise ImportError('Cannot load module: %s!' % fullname)

        filename = self._dynamic_modules.get(name)

        if not filename:
            raise ImportError('Cannot load module: %s!' % fullname)

        file, file_path, (suffix, mode, type_) = imp.find_module(
            name, ['./'])

        # check to ensure this module we are looking for is
        # actually an python extension module...
        if type_ != imp.C_EXTENSION:
            raise ImportError('Cannot load invalid module: %s!' % fullname)
        else:
            # close the file object since it is no longer
            # needed and could possibly cause issues...
            file.close()

        module = self._module_cache.get(name)

        if not module:
            # create a process and attempt to import our module
            # within it because if we try and import it here,
            # this class will cause recusion...
            queue = multiprocessing.Queue()
            self._process = multiprocessing.Process(target=self.__load_module,
                args=(queue, name, filename,))

            self._process.daemon = True
            self._process.start()

            # block and wait for the module object to be placed
            # in the module cache dictionary before we can do anything...
            module = queue.get()

            if not module:
                raise ImportError('Cannot load module: %s!' % fullname)
            else:
                self._module_cache[name] = module

            self._process.join()
            self._process = None

        imp.release_lock()
        return module

    def __load_module(self, queue, name, filename):
        """
        Called by a separate Python process which will load the
        dynamic module outside the main process...
        """

        module = importlib.import_module(name, filename)
        queue.put(module)

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

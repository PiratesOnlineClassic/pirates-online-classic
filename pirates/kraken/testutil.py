"""
Helpers for the kraken and boss AI unit tests.

The game resources (*.pkl tables) and the compiled libotp module are not
available when running the tests, so they are replaced with stub modules
whose attributes are MagicMocks.
"""

import sys
import types
import importlib.abc
import importlib.machinery
from unittest.mock import MagicMock


class _StubModule(types.ModuleType):

    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise AttributeError(attr)

        value = MagicMock(name='%s.%s' % (self.__name__, attr))
        setattr(self, attr, value)
        return value


class _StubFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):

    def __init__(self, prefixes):
        self.prefixes = prefixes

    def find_spec(self, fullname, path, target=None):
        for prefix in self.prefixes:
            if fullname == prefix or fullname.startswith(prefix + '.'):
                return importlib.machinery.ModuleSpec(fullname, self, is_package=True)

        return None

    def create_module(self, spec):
        module = _StubModule(spec.name)
        module.__path__ = []
        return module

    def exec_module(self, module):
        pass


def _stubModule(name):
    module = _StubModule(name)
    sys.modules[name] = module
    parentName, _, childName = name.rpartition('.')
    if parentName:
        setattr(importlib.import_module(parentName), childName, module)

    return module


def installStubs():
    try:
        import libotp
    except ImportError:
        sys.meta_path.insert(0, _StubFinder(['libotp']))

    try:
        from pirates.battle import WeaponGlobals
    except (IOError, OSError):
        sys.modules.pop('pirates.battle.WeaponGlobals', None)
        _stubModule('pirates.battle.WeaponGlobals')

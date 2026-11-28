import dbm.dumb
import importlib.machinery
import importlib.util
import sys
import types


def _installSemidbmFallback():
    # semidbm is only installed on real UberDOG servers. Several suites stub it
    # at import time in slightly different ways; install one well-formed stub
    # (with a module spec, backed by dbm.dumb which has the same API) before any
    # test module is collected so the suites agree on what they get.
    if 'semidbm' in sys.modules or importlib.util.find_spec('semidbm') is not None:
        return

    module = types.ModuleType('semidbm')
    module.__spec__ = importlib.machinery.ModuleSpec('semidbm', None)
    module.open = dbm.dumb.open
    sys.modules['semidbm'] = module


_installSemidbmFallback()

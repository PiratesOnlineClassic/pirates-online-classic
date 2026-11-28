"""Static Python 2 -> 3 / Panda3D 1.10 drift checks for the client GUI and
presentation packages.

These patterns all compile fine under Python 3 but crash (or silently misbehave)
at runtime, so they are only caught by looking at the source.
"""
import ast
import os
import unittest
import warnings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLIENT_GUI_PACKAGES = [
    'pirates/piratesgui', 'pirates/economy', 'pirates/makeapirate', 'pirates/login', 'pirates/cutscene',
    'pirates/effects', 'pirates/inventory', 'pirates/reputation', 'pirates/speedchat', 'pirates/chat',
    'pirates/map', 'pirates/minigame', 'pirates/treasuremap', 'otp/otpgui', 'otp/chat', 'otp/speedchat',
    'otp/namepanel', 'otp/avatar',
]

REMOVED_BUILTINS = {'unicode', 'basestring', 'long', 'xrange', 'raw_input', 'reduce', 'unichr', 'file',
                    'execfile', 'intern', 'apply', 'buffer', 'cmp', 'coerce'}
PY2_DICT_METHODS = {'has_key', 'iteritems', 'itervalues', 'iterkeys', 'viewkeys', 'viewvalues', 'viewitems'}
# NodePathCollection.asList() and the NodePath.lerp* task helpers are gone in Panda3D 1.10.
REMOVED_PANDA_METHODS = {'asList', 'lerpPos', 'lerpHpr', 'lerpScale', 'lerpColor', 'lerpColorScale',
                         'lerpPosHpr', 'lerpPosHprScale'}
REMOVED_STRING_ATTRS = {'letters', 'lowercase', 'uppercase', 'maketrans', 'join', 'joinfields', 'split',
                        'splitfields', 'atoi', 'atof', 'atol', 'replace', 'strip', 'lstrip', 'rstrip', 'upper',
                        'lower', 'find', 'rfind', 'zfill', 'capitalize', 'count', 'index', 'ljust', 'rjust',
                        'center', 'swapcase', 'expandtabs', 'translate'}


def clientGuiFiles():
    for package in CLIENT_GUI_PACKAGES:
        for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, package)):
            for filename in sorted(filenames):
                if filename.endswith('.py') and not filename.endswith(('AI.py', 'UD.py')):
                    yield os.path.join(dirpath, filename)


def findProblems(path):
    with open(path, encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source, path)
    defined = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            defined.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            defined.update((alias.asname or alias.name).split('.')[0] for alias in node.names)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            defined.add(node.id)
        elif isinstance(node, ast.arg):
            defined.add(node.arg)

    problems = []

    def report(node, message):
        problems.append('%s:%d: %s' % (os.path.relpath(path, ROOT), node.lineno, message))

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute):
                if func.attr == 'sort' and node.args:
                    report(node, 'cmp-style list.sort(); use key=cmp_to_key(...)')
                if func.attr in PY2_DICT_METHODS:
                    report(node, 'Python 2 dict method %s()' % func.attr)
                if func.attr in REMOVED_PANDA_METHODS:
                    report(node, '%s() was removed in Panda3D 1.10' % func.attr)
            elif isinstance(func, ast.Name) and func.id == 'sorted' and len(node.args) > 1:
                report(node, 'cmp-style sorted(); use key=cmp_to_key(...)')
            for keyword in node.keywords:
                if keyword.arg == 'cmp':
                    report(node, 'cmp= keyword argument')
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id in REMOVED_BUILTINS and node.id not in defined:
                report(node, 'Python 2 builtin %s' % node.id)
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == 'string' and node.attr in REMOVED_STRING_ATTRS:
                report(node, 'string.%s does not exist in Python 3' % node.attr)
            if node.value.id == 'sys' and node.attr == 'maxint':
                report(node, 'sys.maxint does not exist in Python 3')
        elif isinstance(node, ast.ClassDef):
            methods = {item.name for item in node.body if isinstance(item, ast.FunctionDef)}
            if '__cmp__' in methods and '__lt__' not in methods:
                report(node, 'class %s sorts with __cmp__ but has no __lt__' % node.name)
            for name in ('__nonzero__', '__div__', '__unicode__'):
                if name in methods:
                    report(node, 'class %s defines Python 2 only %s' % (node.name, name))
            if '__getslice__' in methods:
                setitem = [item for item in node.body if isinstance(item, ast.FunctionDef) and item.name == '__setitem__']
                if setitem and 'slice' not in ast.dump(setitem[0]):
                    report(node, 'class %s relies on __setslice__ which Python 3 never calls' % node.name)

    return problems


class TestClientGuiPython3Static(unittest.TestCase):

    def test_files_found(self):
        self.assertGreater(len(list(clientGuiFiles())), 400)

    def test_compiles_without_syntax_warnings(self):
        failures = []
        for path in clientGuiFiles():
            with open(path, encoding='utf-8') as f:
                source = f.read()

            with warnings.catch_warnings():
                warnings.simplefilter('error', SyntaxWarning)
                try:
                    compile(source, path, 'exec')
                except (SyntaxError, SyntaxWarning) as e:
                    failures.append('%s: %s' % (os.path.relpath(path, ROOT), e))

        self.assertEqual(failures, [])

    def test_no_python2_or_removed_panda_patterns(self):
        problems = []
        for path in clientGuiFiles():
            problems.extend(findProblems(path))

        self.assertEqual(problems, [])

    def test_checker_flags_known_bad_patterns(self):
        import tempfile
        source = '\n'.join([
            'import sys',
            'def f(items, d, nodes):',
            '    items.sort(lambda a, b: 0)',
            '    sorted(items, cmp=None)',
            '    d.has_key(1)',
            '    nodes.findAllMatches("**").asList()',
            '    sys.maxint',
            '    return unicode(xrange(3))',
            'class Item:',
            '    def __cmp__(self, other):',
            '        return 0',
        ])
        with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
            f.write(source)

        try:
            problems = findProblems(f.name)
        finally:
            os.unlink(f.name)

        self.assertEqual(len(problems), 8, problems)


if __name__ == '__main__':
    unittest.main()

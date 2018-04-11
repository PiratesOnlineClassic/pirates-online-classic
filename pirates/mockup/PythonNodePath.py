from pandac.PandaModules import NodePath

class PythonNodePath(NodePath):
    __module__ = __name__

    def __init__(self, node):
        NodePath.NodePath.__init__(self, node)
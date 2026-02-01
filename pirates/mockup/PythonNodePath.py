from panda3d.core import NodePath

class PythonNodePath(NodePath):
    
    def __init__(self, node):
        NodePath.NodePath.__init__(self, node)



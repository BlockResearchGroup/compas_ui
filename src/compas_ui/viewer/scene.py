from compas.plugins import plugin


@plugin(category='ui', requires=['PySide2'])
def update_scene(self):
    for guid in self.nodes:
        node = self.nodes[guid]
        
        node.draw()


@plugin(category='ui', requires=['PySide2'])
def clear_scene(self):
    raise NotImplementedError
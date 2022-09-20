from compas.plugins import plugin


@plugin(category="ui", requires=["bpy"])
def redraw_scene(self):
    pass


@plugin(category="ui", requires=["bpy"])
def update_scene(self):
    for obj in self.objects:
        obj.draw()


@plugin(category="ui", requires=["bpy"])
def clear_scene(self):
    for obj in self.objects:
        obj.clear()
    self.objects = []


@plugin(category="ui", requires=["bpy"])
def highlight_objects(self, guids):
    pass

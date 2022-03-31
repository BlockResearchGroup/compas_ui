import compas_rhino
from compas.plugins import plugin


@plugin(category="ui", requires=["Rhino"])
def redraw_scene(self):
    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()


@plugin(category="ui", requires=["Rhino"])
def update_scene(self):
    compas_rhino.rs.EnableRedraw(False)
    for obj in self.objects:
        obj.draw()
    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()


@plugin(category="ui", requires=["Rhino"])
def clear_scene(self):
    compas_rhino.rs.EnableRedraw(False)
    for obj in self.objects:
        obj.clear()
    self.objects = []
    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()


@plugin(category="ui", requires=["Rhino"])
def highlight_objects(self, guids):
    compas_rhino.rs.EnableRedraw(False)
    compas_rhino.rs.SelectObjects(guids)
    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()

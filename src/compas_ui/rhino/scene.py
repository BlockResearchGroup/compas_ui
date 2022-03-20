import compas_rhino
from compas.plugins import plugin


@plugin(category='ui', requires=['Rhino'])
def update_scene(self):
    compas_rhino.rs.EnableRedraw(False)
    for obj in self.objects:
        obj.draw()
    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()


@plugin(category='ui', requires=['Rhino'])
def clear_scene(self):
    compas_rhino.rs.EnableRedraw(False)
    for obj in self.objects:
        obj.clear()
    self.objects = []
    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()


@plugin(category='ui', requires=['Rhino'])
def highlight_objects(self, guids):
    compas_rhino.rs.EnableRedraw(False)
    compas_rhino.rs.SelectObjects(guids)
    compas_rhino.rs.EnableRedraw(True)


# def match_vertices(diagram, keys):
#     temp = compas_rhino.get_objects(name="{}.vertex.*".format(diagram.name))
#     names = compas_rhino.get_object_names(temp)
#     guids = []
#     for guid, name in zip(temp, names):
#         parts = name.split('.')
#         key = literal_eval(parts[2])
#         if key in keys:
#             guids.append(guid)
#     return guids


# def match_edges(diagram, keys):
#     temp = compas_rhino.get_objects(name="{}.edge.*".format(diagram.name))
#     names = compas_rhino.get_object_names(temp)
#     guids = []
#     for guid, name in zip(temp, names):
#         parts = name.split('.')[2].split('-')
#         u = literal_eval(parts[0])
#         v = literal_eval(parts[1])
#         if (u, v) in keys or (v, u) in keys:
#             guids.append(guid)
#     return guids


# def match_faces(diagram, keys):
#     temp = compas_rhino.get_objects(name="{}.face.*".format(diagram.name))
#     names = compas_rhino.get_object_names(temp)
#     guids = []
#     for guid, name in zip(temp, names):
#         parts = name.split('.')
#         key = literal_eval(parts[2])
#         if key in keys:
#             guids.append(guid)
#     return guids


# def select_vertices(diagram, keys):
#     guids = match_vertices(diagram, keys)
#     compas_rhino.rs.EnableRedraw(False)
#     compas_rhino.rs.SelectObjects(guids)
#     compas_rhino.rs.EnableRedraw(True)


# def select_edges(diagram, keys):
#     guids = match_edges(diagram, keys)
#     compas_rhino.rs.EnableRedraw(False)
#     compas_rhino.rs.SelectObjects(guids)
#     compas_rhino.rs.EnableRedraw(True)


# def select_faces(diagram, keys):
#     guids = match_faces(diagram, keys)
#     compas_rhino.rs.EnableRedraw(False)
#     compas_rhino.rs.SelectObjects(guids)
#     compas_rhino.rs.EnableRedraw(True)

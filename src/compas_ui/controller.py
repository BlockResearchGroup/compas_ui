import os
import compas_rhino
from compas.utilities import flatten


class Controller(object):
    def __init__(self, ui):
        self.ui = ui

    # ========================================================================
    # Geometry
    # ========================================================================

    # ========================================================================
    # Datastructures
    # ========================================================================

    def mesh_create(self):
        """Create a COMPAS mesh."""
        from compas.datastructures import Mesh
        from compas_rhino.conversions import RhinoMesh
        from compas_rhino.conversions import RhinoSurface

        options = ["FromFile", "FromSurface", "FromMesh", "FromShape", "FromMeshgrid"]
        option = compas_rhino.rs.GetString("Create a COMPAS mesh:", strings=options)

        if not option:
            return

        if option == "FromFile":
            path = self.ui.pick_file_open()
            if not path:
                return

            _, ext = os.path.splitext(path)

            if ext == ".obj":
                mesh = Mesh.from_obj(path)
                mesh.name = "MeshFromOBJ"
            elif ext == ".off":
                mesh = Mesh.from_off(path)
                mesh.name = "MeshFromOFF"
            elif ext == ".ply":
                mesh = Mesh.from_ply(path)
                mesh.name = "MeshFromPLY"
            elif ext == ".json":
                mesh = Mesh.from_json(path)
                mesh.name = "MeshFromJSON"
            else:
                raise NotImplementedError

        elif option == "FromSurface":
            guid = compas_rhino.select_surface()
            if not guid:
                return

            U = self.ui.get_integer(
                "Number of faces in the U direction?", minval=1, maxval=1000, default=10
            )
            if not U:
                return

            V = self.ui.get_integer(
                "Number of faces in the V direction?", minval=1, maxval=1000, default=U
            )
            if not V:
                return

            mesh = RhinoSurface.from_guid(guid).to_compas_quadmesh(
                nu=U, nv=V, weld=True
            )
            mesh.name = "MeshFromSurface"

        elif option == "FromMesh":
            guid = compas_rhino.select_mesh()
            if not guid:
                return

            mesh = RhinoMesh.from_guid(guid).to_compas()
            mesh.name = "MeshFromMesh"

        elif option == "FromShape":
            raise NotImplementedError

        elif option == "FromMeshgrid":
            dx = self.ui.get_real(
                "Span in the X direction?", minval=1, maxval=100, default=10
            )
            if not dx:
                return
            nx = self.ui.get_integer(
                "Number of faces in the X direction?", minval=1, maxval=1000, default=10
            )
            if not nx:
                return
            dy = self.ui.get_real(
                "Span in the Y direction?", minval=1, maxval=100, default=dx
            )
            if not dy:
                return
            ny = self.ui.get_integer(
                "Number of faces in the Y direction?", minval=1, maxval=1000, default=nx
            )
            if not ny:
                return

            mesh = Mesh.from_meshgrid(dx=dx, nx=nx, dy=dy, ny=ny)
            mesh.name = "MeshFromMeshgrid"

        else:
            raise NotImplementedError

        name = self.ui.get_string("Mesh name?", default=mesh.name)
        if not name:
            name = mesh.name

        objects = self.ui.scene.get(name)
        if objects:
            for obj in objects:
                self.ui.scene.remove(obj)

        self.ui.scene.add(mesh, name=name)
        self.ui.scene.update()
        self.ui.record()

    def mesh_modify(self):
        """Create a COMPAS mesh."""

    def mesh_delete(self):
        """Delete a COMPAS mesh."""

    def mesh_export(self):
        """Export a COMPAS mesh."""

    def mesh_select_vertices(self, meshobj):
        """Select vertices of a mesh object through the UI.

        Parameters
        ----------
        meshobj : :class:`compas_ui.objects.MeshObject`

        Returns
        -------
        list[int]

        """
        mesh = meshobj.mesh

        options = ["All", "Boundary", "Corners", "ByContinuousEdges", "Manual"]
        mode = self.get_string(message="Selection mode.", options=options)
        if not mode:
            return

        vertex_guid = {
            vertex: guid for guid, vertex in iter(meshobj.guid_vertex.items())
        }

        if mode == "All":
            vertices = list(mesh.vertices())

        elif mode == "Boundary":
            vertices = list(set(flatten(mesh.vertices_on_boundaries())))
            guids = [vertex_guid[vertex] for vertex in vertices]
            self.scene.highlight_objects(guids)

        elif mode == "Corners":
            vertices = mesh.corner_vertices()
            guids = [vertex_guid[vertex] for vertex in vertices]
            self.scene.highlight_objects(guids)

        elif mode == "ByContinuousEdges":
            temp = meshobj.select_edges()
            vertices = list(
                set(flatten([mesh.vertices_on_edge_loop(key) for key in temp]))
            )
            guids = [vertex_guid[vertex] for vertex in vertices]
            self.scene.highlight_objects(guids)

        elif mode == "Manual":
            vertices = meshobj.select_vertices()

        return vertices

    def mesh_select_edges(self, meshobj):
        """Select edges of a mesh object through the UI.

        Parameters
        ----------
        meshobj : :class:`compas_ui.objects.MeshObject`

        Returns
        -------
        list[tuple[int, int]]

        """
        mesh = meshobj.mesh

        options = ["All", "AllBoundaryEdges", "Continuous", "Parallel", "Manual"]
        mode = self.get_string(message="Selection mode.", options=options)
        if not mode:
            return

        edge_guid = {edge: guid for guid, edge in iter(meshobj.guid_edge.items())}
        edge_guid.update(
            {(v, u): guid for guid, (u, v) in iter(meshobj.guid_edge.items())}
        )

        if mode == "All":
            edges = list(mesh.edges())

        elif mode == "AllBoundaryEdges":
            edges = list(set(flatten(mesh.edges_on_boundaries())))
            guids = [edge_guid[edge] for edge in edges]
            self.scene.highlight_objects(guids)

        elif mode == "Continuous":
            temp = meshobj.select_edges()
            edges = list(set(flatten([mesh.edge_loop(edge) for edge in temp])))
            guids = [edge_guid[edge] for edge in edges]
            self.scene.highlight_objects(guids)

        elif mode == "Parallel":
            temp = meshobj.select_edges()
            edges = list(set(flatten([mesh.edge_strip(edge) for edge in temp])))
            guids = [edge_guid[edge] for edge in edges]
            self.scene.highlight_objects(guids)

        elif mode == "Manual":
            edges = meshobj.select_edges()

        return edges

    # ========================================================================
    # Robots
    # ========================================================================

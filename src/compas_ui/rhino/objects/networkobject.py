from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino

from compas_ui.objects import NetworkObject

from ._modify import network_update_attributes
from ._modify import network_update_node_attributes
from ._modify import network_update_edge_attributes
from ._modify import network_move_node

from .object import RhinoObject


class RhinoNetworkObject(RhinoObject, NetworkObject):
    """Class for representing COMPAS networkes in Rhino.

    Attributes
    ----------
    guid_node : dict[System.Guid, int]
        Map between Rhino object GUIDs and mesh node identifiers.
    guid_edge : dict[System.Guid, tuple[int, int]]
        Map between Rhino object GUIDs and mesh edge identifiers.

    """

    def __init__(self, *args, **kwargs):
        super(RhinoNetworkObject, self).__init__(*args, **kwargs)
        self._guid_node = {}
        self._guid_edge = {}

    @property
    def network(self):
        return self.item

    @network.setter
    def network(self, network):
        self.item = network
        self._guid_node = {}
        self._guid_edge = {}

    @property
    def guid_node(self):
        if not self._guid_node:
            self._guid_node = {}
        return self._guid_node

    @guid_node.setter
    def guid_node(self, values):
        self._guid_node = dict(values)

    @property
    def guid_edge(self):
        if not self._guid_edge:
            self._guid_edge = {}
        return self._guid_edge

    @guid_edge.setter
    def guid_edge(self, values):
        self._guid_edge = dict(values)

    def clear(self):
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guids = []
        self._guid_node = {}
        self._guid_edge = {}

    def draw(self):
        self.clear()
        if not self.visible:
            return
        self.artist.node_xyz = self.node_xyz

        if self.settings["show.nodes"]:
            nodes = list(self.network.nodes())
            guids = self.artist.draw_nodes(nodes=nodes, color=self.settings["color.nodes"])
            self.guids += guids
            self.guid_node = zip(guids, nodes)

            if self.settings["show.nodelabels"]:
                text = {node: str(node) for node in nodes}
                self.guids += self.artist.draw_nodelabels(text=text, color=self.settings["color.nodes"])

        if self.settings["show.edges"]:
            edges = list(self.network.edges())
            guids = self.artist.draw_edges(edges=edges, color=self.settings["color.edges"])
            self.guids += guids
            self.guid_edge = zip(guids, edges)

            if self.settings["show.edgelabels"]:
                text = {edge: "{}-{}".format(*edge) for edge in edges}
                self.guids += self.artist.draw_edgelabels(text=text, color=self.settings["color.edges"])

    def select_nodes(self):
        """Select nodes of the network.

        Returns
        -------
        list
            A list of node identifiers.
        """
        guids = compas_rhino.select_points()
        nodes = [self.guid_node[guid] for guid in guids if guid in self.guid_node]
        return nodes

    def select_edges(self):
        """Select edges of the network.

        Returns
        -------
        list
            A list of edge identifiers.
        """
        guids = compas_rhino.select_lines()
        edges = [self.guid_edge[guid] for guid in guids if guid in self.guid_edge]
        return edges

    def modify(self):
        """Update the attributes of the network.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.

        """
        return network_update_attributes(self.network)

    def modify_nodes(self, nodes, names=None):
        """Update the attributes of the nodes.

        Parameters
        ----------
        nodes : list
            The identifiers of the nodes to update.
        names : list, optional
            The names of the atrtibutes to update.
            Default is to update all attributes.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.

        """
        return network_update_node_attributes(self.network, nodes, names=names)

    def modify_edges(self, edges, names=None):
        """Update the attributes of the edges.

        Parameters
        ----------
        edges : list
            The identifiers of the edges to update.
        names : list, optional
            The names of the atrtibutes to update.
            Default is to update all attributes.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.

        """
        return network_update_edge_attributes(self.network, edges, names=names)

    def move_node(self, node):
        """Move a single node of the network object and update the data structure accordingly.

        Parameters
        ----------
        node : int
            The identifier of the node.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.

        """
        return network_move_node(self.network, node)

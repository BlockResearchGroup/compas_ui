"""
********************************************************************************
scene
********************************************************************************

.. currentmodule:: compas_ui.scene


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Scene

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import pluggable

from compas_ui.objects import Object
from compas_ui.singleton import Singleton


@pluggable(category='ui')
def update_scene(self):
    raise NotImplementedError


@pluggable(category='ui')
def clear_scene(self):
    raise NotImplementedError


@pluggable(category='ui')
def highlight_objects(self):
    raise NotImplementedError


class Scene(Singleton):
    """The scene singleton keeps track of the view objects of an app.

    Parameters
    ----------
    settings : dict[str, Any], optional
        Visualization settings of the scene.

    Attributes
    ----------
    state : dict[str, Any]
        The current state of the scene, containing the objects and the scene settings.
    objects : list[:class:`compas_ui.objects.Object`]
        The objects in the scene.
    settings : dict[str, Any]
        The visualization settings.

    """

    SETTINGS = {}

    def __init__(self, settings=None):
        super(Scene, self).__init__()
        self.objects = []
        self.settings = Scene.SETTINGS.copy()
        self.settings.update(settings or {})

    @property
    def state(self):
        data = {}
        objects = []
        for obj in self.objects:
            guid = str(obj.item.guid)
            if guid not in data:
                data[guid] = obj.item
            objects.append({
                'item': guid,
                'name': obj.name,
                'visible': obj.visible,
                'settings': obj.settings,
            })
        return {'data': data, 'objects': objects, 'settings': self.settings}

    @state.setter
    def state(self, state):
        self.objects = []
        for obj in state['objects']:
            item = state['data'][obj['item']]
            self.add(item, name=obj['name'], visible=obj['visible'], settings=obj['settings'])
        self.settings = Scene.SETTINGS.copy()
        self.settings.update(state['settings'])

    def add(self, item, **kwargs):
        """Add a COMPAS data item to the scene.

        Parameters
        ----------
        item : :class:`compas.data.Data`
            A COMPAS data item/object.
        **kwargs : dict[str, Any], optional
            Additional parameters to be passed on to the scene object corresponding to the data item.

        Returns
        -------
        :class:`compas_ui.objects.Object`

        """
        obj = Object(item, **kwargs)
        # implement __hash__ on Data
        # to allow for
        # self.objects[item] = obj
        self.objects.append(obj)
        return obj

    def get(self, name):
        """Get all scene objects with a given name.

        Parameters
        ----------
        name : str
            The name of the object(s).

        Returns
        -------
        list[:class:`compas_ui.objects.Object`]

        """
        objects = []
        for obj in self.objects:
            if name == obj.name:
                objects.append(obj)
        return objects

    def update(self):
        """Update the scene.

        Returns
        -------
        None

        """
        update_scene(self)

    def clear(self):
        """Clear the scene.

        Returns
        -------
        None

        """
        clear_scene(self)

    def highlight_objects(self, guids):
        """Highlight objects in the scene.

        Returns
        -------
        None

        """
        highlight_objects(self, guids)

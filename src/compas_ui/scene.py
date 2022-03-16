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

from copy import deepcopy

from compas.plugins import pluggable

from compas_ui.objects import Object
from compas_ui.singleton import Singleton


@pluggable(category='ui')
def update_scene(self):
    raise NotImplementedError


@pluggable(category='ui')
def clear_scene(self):
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

    def __init__(self, settings=None):
        super(Scene, self).__init__()
        self._history = []
        self._current = -1
        self.objects = []
        self.settings = settings or {}
        self.record()

    @property
    def state(self):
        return {'objects': self.objects, 'settings': self.settings}

    @state.setter
    def state(self, state):
        self.objects = state['objects']
        self.settings = state['settings']

    def record(self):
        """Record the current state of the scene.

        Returns
        -------
        None

        """
        if self._current > -1:
            if self._current < len(self._history) - 1:
                # remove everything that comes after current
                # but keep current
                self._history[:] = self._history[:self._current + 1]

        self._history.append(deepcopy(self.state))
        self._current = len(self._history) - 1

    def undo(self):
        """Undo changes to the scene by rewinding to a recorded state.

        Returns
        -------
        None

        """
        self.clear()

        if self._current < 0:
            print("Nothing to undo!")
            return

        if self._current == 0:
            print("Nothing more to undo!")
            return

        self._current -= 1
        self.state = self._history[self._current]
        self.update()

    def redo(self):
        """Redo changes to the scene by forwarding to a recorded state.

        Returns
        -------
        None

        """
        self.clear()

        if self._current < 0:
            print("Nothing to redo!")
            return

        if self._current == len(self._history) - 1:
            print("Nothing more to redo!")
            return

        self._current += 1
        self.state = self._history[self._current]
        self.update()

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
        obj = Object(item, scene=self, **kwargs)
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

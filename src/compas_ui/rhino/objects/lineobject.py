from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
import compas_rhino

from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import point_to_compas
from compas_ui.objects import LineObject
from .object import RhinoObject


class RhinoLineObject(RhinoObject, LineObject):
    """
    Class for representing COMPAS lines in Rhino.
    """

    def __init__(self, *args, **kwargs):
        super(RhinoLineObject, self).__init__(*args, **kwargs)

    def clear(self):
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guids = []

    def draw(self):
        self.clear()
        if not self.visible:
            return
        self._guids = self.artist.draw()

    def move_start(self):
        """
        Move the starting point of the line.

        Returns
        -------
        bool
            True if the operation was a success.
            False otherwise.

        Examples
        --------
        .. code-block:: python

            import compas_rhino
            from compas.geometry import Line
            from compas_ui.objects import Object

            line = Line([0, 0, 0], [1, 0, 0])

            lineobj = Object(line)
            lineobj.draw()

            compas_rhino.redraw()

            if lineobj.move_start():
                lineobj.clear()
                lineobj.draw()

        """
        start = point_to_rhino(self.line.start)
        end = point_to_rhino(self.line.end)
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        gp = Rhino.Input.Custom.GetPoint()

        def OnDynamicDraw(sender, e):
            e.Display.DrawDottedLine(start, e.CurrentPoint, color)

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(end, False)
        gp.DrawLineFromPoint(end, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = point_to_compas(gp.Point())
        self.line.start = start
        return True

    def move_end(self):
        """
        Move the end point of the line.

        Returns
        -------
        bool
            True if the operation was a success.
            False otherwise.

        Examples
        --------
        .. code-block:: python

            import compas_rhino
            from compas.geometry import Line
            from compas_ui.objects import Object

            line = Line([0, 0, 0], [1, 0, 0])

            lineobj = Object(line)
            lineobj.draw()

            compas_rhino.redraw()

            if lineobj.move_end():
                lineobj.clear()
                lineobj.draw()

        """
        start = point_to_rhino(self.line.start)
        end = point_to_rhino(self.line.end)
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        gp = Rhino.Input.Custom.GetPoint()

        def OnDynamicDraw(sender, e):
            e.Display.DrawDottedLine(end, e.CurrentPoint, color)

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = point_to_compas(gp.Point())
        self.line.end = end
        return True

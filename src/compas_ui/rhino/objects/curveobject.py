from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
import compas_rhino

from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import point_to_compas
from compas_ui.objects import CurveObject
from .object import RhinoObject


class RhinoCurveObject(RhinoObject, CurveObject):
    """
    Class for representing COMPAS curves in Rhino.
    """

    def __init__(self, *args, **kwargs):
        super(RhinoCurveObject, self).__init__(*args, **kwargs)

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
        Move the starting point of the curve.

        Returns
        -------
        bool
            True if the operation was a success.
            False otherwise.

        Examples
        --------
        .. code-block:: python

            import compas_rhino
            from compas.geometry import Curve
            from compas_ui.objects import Object

            curve = Curve([0, 0, 0], [1, 0, 0])

            curveobj = Object(curve)
            curveobj.draw()

            compas_rhino.redraw()

            if curveobj.move_start():
                curveobj.clear()
                curveobj.draw()

        """
        start = point_to_rhino(self.curve.start)
        end = point_to_rhino(self.curve.end)
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        gp = Rhino.Input.Custom.GetPoint()

        def OnDynamicDraw(sender, e):
            e.Display.DrawDottedCurve(start, e.CurrentPoint, color)

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(end, False)
        gp.DrawCurveFromPoint(end, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = point_to_compas(gp.Point())
        self.curve.start = start
        return True

    def move_end(self):
        """
        Move the end point of the curve.

        Returns
        -------
        bool
            True if the operation was a success.
            False otherwise.

        Examples
        --------
        .. code-block:: python

            import compas_rhino
            from compas.geometry import Curve
            from compas_ui.rhino.objects.curveobject import CurveObject

            curve = Curve([0, 0, 0], [1, 0, 0])
            curveobj = CurveObject(curve)

            curveobj.draw()

            compas_rhino.redraw()

            if curveobj.move_end():
                curveobj.clear()
                curveobj.draw()

        """
        start = point_to_rhino(self.curve.start)
        end = point_to_rhino(self.curve.end)
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        gp = Rhino.Input.Custom.GetPoint()

        def OnDynamicDraw(sender, e):
            e.Display.DrawDottedCurve(end, e.CurrentPoint, color)

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(start, False)
        gp.DrawCurveFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = point_to_compas(gp.Point())
        self.curve.end = end
        return True

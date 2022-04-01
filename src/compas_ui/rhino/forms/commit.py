from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ast import literal_eval
from email import message

import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms


class CommitForm(Eto.Forms.Dialog[bool]):
    """Form for working with mesh data.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    title : str, optional
        Title of the dialog.
    width : int, optional
        Window width.
    height : int, optional
        Window height.
    exclude_vertex_attr : list[str], optional
        The names of vertex attributes to exclude.
    exclude_edge_attr : list[str], optional
        The names of edge attributes to exclude.
    exclude_face_attr : list[str], optional
        The names of face attributes to exclude.

    """

    def __init__(
        self,
        item,
        title="Commit",
        width=400,
        height=200,
    ):

        self.item = item
        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(
            Eto.Drawing.Padding(12, 12, 12, 12), Eto.Drawing.Size(0, 0), True, True
        )
        layout.AddRow(Eto.Forms.Label(Text="Message"))
        layout.AddRow(self.message)
        layout.EndVertical()
        layout.BeginVertical(
            Eto.Drawing.Padding(12, 18, 12, 24), Eto.Drawing.Size(6, 0), False, False
        )
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndVertical()
        self.Content = layout

    @property
    def message(self):
        self.MessageTextBox = Eto.Forms.TextBox()
        return self.MessageTextBox

    @property
    def ok(self):
        self.DefaultButton = Eto.Forms.Button(Text="OK")
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    @property
    def cancel(self):
        self.AbortButton = Eto.Forms.Button(Text="Cancel")
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    def on_ok(self, sender, event):
        """Callback for the OK event."""
        try:
            self.item.speckle_push(message=self.MessageTextBox.Text)
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, event):
        """Callback for the CANCEL event."""
        self.Close(False)

    def show(self):
        """Show the form dialog."""
        return self.ShowModal(Rhino.UI.RhinoEtoUI.MainWindow)

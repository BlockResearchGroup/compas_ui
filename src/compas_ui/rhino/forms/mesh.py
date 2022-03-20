from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from ast import literal_eval

import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms


class MeshForm(Eto.Forms.Dialog[bool]):

    def __init__(self, mesh, title="Mesh Attributes", width=800, height=800):
        self.mesh = mesh

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(
            Eto.Drawing.Padding(0, 12, 0, 12), Eto.Drawing.Size(0, 0), True, True
        )

        # start panels
        control = Eto.Forms.TabControl()
        control.TabPosition = Eto.Forms.DockPosition.Top

        tab = Eto.Forms.TabPage()
        tab.Text = 'Attributes'
        tab.Content = None
        control.Pages.Add(tab)

        tab = Eto.Forms.TabPage()
        tab.Text = 'Vertices'
        tab.Content = self.make_table()
        control.Pages.Add(tab)

        tab = Eto.Forms.TabPage()
        tab.Text = 'Edges'
        tab.Content = None
        control.Pages.Add(tab)

        tab = Eto.Forms.TabPage()
        tab.Text = 'Faces'
        tab.Content = None
        control.Pages.Add(tab)

        self.TabControl = control
        # end panels

        layout.AddRow(self.TabControl)

        layout.EndVertical()
        layout.BeginVertical(
            Eto.Drawing.Padding(12, 18, 12, 24), Eto.Drawing.Size(6, 0), False, False
        )
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndVertical()

        self.Content = layout

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
            pass
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, event):
        """Callback for the CANCEL event."""
        self.Close(False)

    def show(self):
        """Show the form dialog."""
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

    def make_table(self):
        def on_cell_formatting(sender, e):
            try:
                text = e.Column.HeaderText
                if not e.Column.Editable:
                    e.ForegroundColor = Eto.Drawing.Colors.DarkGray
                if text == 'Vertex':
                    vertex = e.Item.Values[0]
                    # if key in color:
                    #     rgb = color[key]
                    #     rgb = [c/255. for c in rgb]
                    #     e.BackgroundColor = drawing.Color(*rgb)
            except Exception as e:
                print(e)

        public = sorted([name for name in self.mesh.default_vertex_attributes.keys() if not name.startswith('_')])
        private = sorted([name for name in self.mesh.default_vertex_attributes.keys() if name.startswith('_')])
        names = public + private

        table = Eto.Forms.GridView()
        table.ShowHeader = True
        table.DataStore = [
            [vertex] + self.mesh.vertex_attributes(vertex, names) for vertex in self.mesh.vertices()
        ]

        col = Eto.Forms.GridColumn()
        col.HeaderText = "Vertex"
        col.Editable = False
        col.DataCell = Eto.Forms.TextBoxCell(0)
        table.Columns.Add(col)

        index = 1

        for name in public:
            c = Eto.Forms.GridColumn()
            c.HeaderText = name
            c.Editable = True
            c.DataCell = Eto.Forms.TextBoxCell(index)
            table.Columns.Add(c)
            index += 1

        for name in private:
            c = Eto.Forms.GridColumn()
            c.HeaderText = name
            c.Editable = False
            c.DataCell = Eto.Forms.TextBoxCell(index)
            table.Columns.Add(c)
            index += 1

        table.CellFormatting += on_cell_formatting

        return table

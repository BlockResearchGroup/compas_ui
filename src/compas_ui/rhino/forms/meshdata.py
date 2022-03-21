from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from ast import literal_eval

import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms


class MeshDataForm(Eto.Forms.Dialog[bool]):

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

        control = Eto.Forms.TabControl()
        control.TabPosition = Eto.Forms.DockPosition.Top
        control.Pages.Add(self.make_tab('Vertices', self.mesh.default_vertex_attributes, self.mesh.vertex_attribute, list(self.mesh.vertices())))
        control.Pages.Add(self.make_tab('Edges', self.mesh.default_edge_attributes, self.mesh.edge_attribute, list(self.mesh.edges())))
        control.Pages.Add(self.make_tab('Faces', self.mesh.default_face_attributes, self.mesh.face_attribute, list(self.mesh.faces())))

        self.TabControl = control

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

    def make_tab(self, title, defaults, attrfunc, keys):
        """Make a tab page for the tab control.

        Parameters
        ----------
        title : str
            The text in the tab control.
        defaults : dict[str, Any]
            The dict with default attribute values.
        attrfunc : callable
            The function for retrieving individual attribute values.
        keys : list[int, tuple[int, int]]
            The identifiers of the objects in the table.

        Returns
        -------
        Eto.Forms.TabPage

        """
        public = sorted([name for name in defaults.keys() if not name.startswith('_')])
        private = sorted([name for name in defaults.keys() if name.startswith('_')])

        cols = [('ID', False, False, None)]

        for name in public:
            default = defaults[name]
            if isinstance(default, bool):
                cols.append((name, True, True, None))
            elif isinstance(default, float):
                cols.append((name, True, False, '3f'))
            else:
                cols.append((name, True, False, None))

        for name in private:
            default = defaults[name]
            if isinstance(default, bool):
                cols.append((name, False, True, None))
            elif isinstance(default, float):
                cols.append((name, False, False, '3f'))
            else:
                cols.append((name, False, False, None))

        rows = []
        for key in keys:
            row = [str(key)]
            for col in cols[1:]:
                name = col[0]
                precision = col[-1]
                value = attrfunc(key, name)
                if precision:
                    value = '{0:.{1}}'.format(value, precision)
                row.append(value)
            rows.append(row)

        tab = Eto.Forms.TabPage()
        tab.Text = title
        tab.Content = self.make_table(cols, rows)
        return tab

    def make_table(self, cols, rows):
        """Make a grid view of the data in the tab.

        Parameters
        ----------
        cols : list[tuple[str, bool, bool, str | None]]
            Information about the table columns.
        rows : list
            The data contained in the rows.

        Returns
        -------
        Eto.Forms.GridView

        """
        def on_cell_formatting(sender, e):
            try:
                if not e.Column.Editable:
                    e.ForegroundColor = Eto.Drawing.Colors.DarkGray
            except Exception as e:
                print(e)

        table = Eto.Forms.GridView()
        table.ShowHeader = True
        table.DataStore = rows

        for i, (name, editable, checkbox, _) in enumerate(cols):
            col = Eto.Forms.GridColumn()
            col.HeaderText = name
            col.Editable = editable
            if checkbox:
                col.DataCell = Eto.Forms.CheckBoxCell(i)
            else:
                col.DataCell = Eto.Forms.TextBoxCell(i)
                col.DataCell.VerticalAlignment = Eto.Forms.VerticalAlignment.Center
            table.Columns.Add(col)

        table.CellFormatting += on_cell_formatting

        return table

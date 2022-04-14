from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import ast

import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms


class AttributesForm(Eto.Forms.Dialog[bool]):
    def __init__(self, names, values, title="Attributes", width=500, height=800):
        def on_cell_formatting(sender, e):
            try:
                if not e.Column.Editable:
                    e.ForegroundColor = Eto.Drawing.Colors.DarkGray
            except Exception as e:
                print(e)

        self.attributes = dict(zip(names, values))
        self.names = names
        self.values = [str(value) for value in values]

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        table = Eto.Forms.GridView()
        table.ShowHeader = True
        table.DataStore = list(zip(self.names, self.values))

        self.data = table.DataStore

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Name"
        column.Editable = False
        cell = Eto.Forms.TextBoxCell(0)
        column.DataCell = cell
        table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Value"
        column.Editable = True
        cell = Eto.Forms.TextBoxCell(1)
        cell.AutoSelectMode = Eto.Forms.AutoSelectMode.OnFocus
        column.DataCell = cell
        table.Columns.Add(column)

        table.CellFormatting += on_cell_formatting

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(
            Eto.Drawing.Padding(0, 0, 0, 0), Eto.Drawing.Size(0, 0), True, True
        )
        layout.AddRow(table)
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
        try:
            for row in self.data:
                name = row[0]
                value = row[1]
                if value != "-":
                    try:
                        value = ast.literal_eval(value)
                    except Exception as e:
                        print(e)
                    else:
                        value = None
                self.attributes[name] = value
        except Exception as e:
            print(e)
            self.Close(False)
        else:
            self.Close(True)

    def on_cancel(self, sender, event):
        self.Close(False)

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


class Table(object):
    """Wrapper for Eto grid view.

    Parameters
    ----------
    cols
    rows

    """

    def __init__(self, cols, rows):
        def on_cell_formatting(sender, e):
            try:
                if not e.Column.Editable:
                    e.ForegroundColor = Eto.Drawing.Colors.DarkGray
            except Exception as e:
                print(e)

        self.widget = Eto.Forms.GridView()
        self.widget.ShowHeader = True
        self.widget.DataStore = rows

        for i, col in enumerate(cols):
            column = Eto.Forms.GridColumn()
            column.HeaderText = col["name"]
            column.Editable = col["is_editable"]
            if col["is_checkbox"]:
                cell = Eto.Forms.CheckBoxCell(i)
                column.DataCell = cell
            else:
                cell = Eto.Forms.TextBoxCell(i)
                cell.AutoSelectMode = Eto.Forms.AutoSelectMode.OnFocus
                cell.VerticalAlignment = Eto.Forms.VerticalAlignment.Center
                cell.TextAlignment = Eto.Forms.TextAlignment.Right
                column.DataCell = cell

            self.widget.Columns.Add(column)

        self.widget.CellFormatting += on_cell_formatting

        self.cols = cols
        self.rows = rows
        self.data = self.widget.DataStore

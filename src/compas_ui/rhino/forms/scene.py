from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms

from compas.colors import Color


class ColorCell(Eto.Forms.CustomCell):
    def __init__(self, position):
        self.position = position

    def OnCreateCell(self, args):
        def on_value_changed(sender, e):
            color = Eto.Drawing.Color(control.Value)
            item.SetValue(self.position, Color(color.R, color.G, color.B))

        item = args.Item
        value = item.GetValue(self.position)
        control = Eto.Forms.ColorPicker()
        control.AllowAlpha = False
        control.Value = Eto.Drawing.Color.FromArgb(*value.rgb255)
        control.ValueChanged += on_value_changed
        return control


class SceneObjectsForm(Eto.Forms.Dialog[bool]):
    def __init__(self, scene, title="Scene Objects", width=800, height=500):
        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        self.scene = scene
        self.table = Eto.Forms.TreeGridView()
        self.table.ShowHeader = True

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Scene Objects"
        column.Editable = False
        column.DataCell = Eto.Forms.TextBoxCell(self.table.Columns.Count)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Name"
        column.Editable = True
        column.DataCell = Eto.Forms.TextBoxCell(self.table.Columns.Count)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Visible"
        column.Editable = True
        column.DataCell = Eto.Forms.CheckBoxCell(self.table.Columns.Count)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "VColor"
        column.Editable = True
        column.DataCell = ColorCell(self.table.Columns.Count)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "EColor"
        column.Editable = True
        column.DataCell = ColorCell(self.table.Columns.Count)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "FColor"
        column.Editable = True
        column.DataCell = ColorCell(self.table.Columns.Count)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Data"
        column.Editable = False
        column.DataCell = Eto.Forms.TextBoxCell(self.table.Columns.Count)
        self.table.Columns.Add(column)

        collection = Eto.Forms.TreeGridItemCollection()
        for obj in self.scene.objects:
            item = Eto.Forms.TreeGridItem(
                Values=(
                    obj.__class__.__name__,
                    obj.name,
                    obj.visible,
                    obj.settings["color.vertices"],
                    obj.settings["color.edges"],
                    obj.settings["color.faces"],
                    str(obj.item),
                )
            )
            collection.Add(item)

        self.table.DataStore = collection

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(
            Eto.Drawing.Padding(0, 0, 0, 0), Eto.Drawing.Size(0, 0), True, True
        )
        layout.AddRow(self.table)
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
        self.Close(True)

    def on_cancel(self, sender, event):
        self.Close(False)

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import uuid

import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms

from .meshdata import MeshDataForm
from .settings import SettingsForm

from compas.datastructures import Mesh


class ObjCell(Eto.Forms.CustomCell):

    def __init__(self, parent):
        self.parent = parent


class ObjNameCell(ObjCell):

    def OnCreateCell(self, args):
        obj = args.Item.GetValue(0)
        control = Eto.Forms.TextBox()
        control.Text = obj.name
        control.ShowBorder = False

        def on_text_changed(sender, e):
            obj.name = sender.Text

        control.TextChanged += on_text_changed

        return control


class ObjTypeCell(ObjCell):

    def OnCreateCell(self, args):
        obj = args.Item.GetValue(0)
        control = Eto.Forms.Label(Text=obj.item.__class__.__name__)
        return control


class VisibleCell(ObjCell):

    def OnCreateCell(self, args):
        def on_click(sender, e):
            obj.visible = sender.Checked
            self.parent.scene.update()

        obj = args.Item.GetValue(0)
        control = Eto.Forms.CheckBox()
        control.Checked = obj.visible
        control.CheckedChanged += on_click

        return control


class SettingsCell(ObjCell):

    def OnCreateCell(self, args):
        obj = args.Item.GetValue(0)
        if isinstance(obj.item, Mesh):
            def on_click(sender, e):
                form = SettingsForm(obj.settings)
                if form.ShowModal(self.parent):
                    obj.settings.update(form.settings)
                    self.parent.scene.update()

            control = Eto.Forms.Button(Text="Settings")
            control.Click += on_click

            return control


class ItemCell(ObjCell):

    def OnCreateCell(self, args):
        obj = args.Item.GetValue(0)
        if isinstance(obj.item, Mesh):
            def on_click(sender, e):
                # switch between data types
                form = MeshDataForm(obj.item)
                if form.ShowModal(self.parent):
                    self.parent.scene.update()

            text = "{} Data".format(obj.item.__class__.__name__)
            control = Eto.Forms.Button(Text=text)
            control.Click += on_click

            return control


class ActiveCell(ObjCell):

    def OnCreateCell(self, args):
        def on_click(sender, e):
            self.parent.scene.active_object = obj
            for _obj, _control in self.parent.active_controls:
                if _obj != obj:
                    _control.Checked = self.parent.scene.active_object == _obj

            print("active object:", self.parent.scene.active_object)

        obj = args.Item.GetValue(0)
        control = Eto.Forms.RadioButton()
        control.Checked = obj.active
        control.MouseDown += on_click
        self.parent.active_controls.append((obj, control))

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
        column.HeaderText = "Object"
        column.Editable = False
        column.DataCell = ObjTypeCell(self)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Name"
        column.Editable = False
        column.DataCell = ObjNameCell(self)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Active"
        column.Editable = False
        column.DataCell = ActiveCell(self)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Visible"
        column.Editable = False
        column.DataCell = VisibleCell(self)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = ""
        column.Editable = False
        column.DataCell = SettingsCell(self)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = ""
        column.Editable = False
        column.DataCell = ItemCell(self)
        self.table.Columns.Add(column)

        collection = Eto.Forms.TreeGridItemCollection()

        def add_items(parent, objects):
            for obj in objects:
                item = Eto.Forms.TreeGridItem(Values=(obj,))
                if obj.children:
                    add_items(item.Children, obj.children)
                parent.Add(item)

        root_objects = [obj for obj in self.scene.objects if obj.parent is None]
        add_items(collection, root_objects)

        self.table.DataStore = collection

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(
            Eto.Drawing.Padding(0, 0, 0, 0), Eto.Drawing.Size(0, 0), True, True
        )
        layout.AddRow(self.table)
        layout.EndVertical()

        self.Content = layout
        self.active_controls = []

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

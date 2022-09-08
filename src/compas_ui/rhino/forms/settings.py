from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms
import decimal
from compas.colors import Color
from ast import literal_eval
from compas_rhino.forms import TextForm


class CustomCell(Eto.Forms.CustomCell):

    def __init__(self, parent):
        self.parent = parent

    def OnGetIdentifier(self, args):
        return str(args.Row)


class KeyCell(CustomCell):

    def OnCreateCell(self, args):
        item = args.Item
        key = item.GetValue(0)
        control = Eto.Forms.TextBox()
        control.Text = str(key)

        def on_text_changed(sender, e):
            old_key = item.GetValue(0)
            new_key = str(control.Text)
            if new_key and not old_key:
                print("adding newkey:", new_key)
                item.SetValue(0, new_key)
                self.parent.add_empty_row()
            elif not new_key and old_key:
                form = TextForm("Are you sure you want to delete this key?")
                if form.show():
                    self.parent.remove_row(item)
            else:
                item.SetValue(0, new_key)

        control.LostFocus += on_text_changed
        control.Size = Eto.Drawing.Size(100, 25)
        return control


class ValueCell(CustomCell):

    def OnCreateCell(self, args):
        item = args.Item
        value = item.GetValue(1)

        if isinstance(value, bool):
            control = Eto.Forms.CheckBox()
            control.Checked = value

            def on_checked(sender, e):
                item.SetValue(1, control.Checked)

            control.CheckedChanged += on_checked

        elif isinstance(value, int):
            control = Eto.Forms.NumericUpDown()
            control.Value = value

            def on_value_changed(sender, e):
                item.SetValue(1, int(control.Value))

            control.ValueChanged += on_value_changed

        elif isinstance(value, float):
            control = Eto.Forms.NumericUpDown()
            control.Value = value
            precision = str(value)
            d = decimal.Decimal(precision).as_tuple()
            control.DecimalPlaces = -d.exponent
            control.Increment = 10**d.exponent

            def on_value_changed(sender, e):
                item.SetValue(1, float(control.Value))

            control.ValueChanged += on_value_changed

        elif isinstance(value, str):
            control = Eto.Forms.TextBox()
            control.Text = str(value)

            def on_text_changed(sender, e):
                item.SetValue(1, str(control.Text))

            control.TextChanged += on_text_changed

        elif isinstance(value, (Color, tuple, list)):
            if isinstance(value, (tuple, list)):
                value = Color(*value)
            control = Eto.Forms.ColorPicker()
            control.Value = Eto.Drawing.Color.FromArgb(*value.rgb255)

            def on_value_changed(sender, e):
                color = Eto.Drawing.Color(control.Value)
                item.SetValue(1, Color(color.R, color.G, color.B))

            control.ValueChanged += on_value_changed

        else:
            control = Eto.Forms.Label()

        control.Size = Eto.Drawing.Size(100, 25)

        return control


class SettingsForm(Eto.Forms.Dialog[bool]):
    def __init__(self, settings, title="Settings", width=500, height=500, use_tab=False, allow_edit_key=False):
        self._settings = None
        self._names = None
        self._values = None
        self.settings = settings
        self.use_tab = use_tab
        self.allow_edit_key = allow_edit_key

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(
            Eto.Drawing.Padding(0, 0, 0, 0), Eto.Drawing.Size(0, 0), True, True
        )

        if self.use_tab:

            control = Eto.Forms.TabControl()
            control.TabPosition = Eto.Forms.DockPosition.Top

            self.tables = {}
            for key, settings in self.settings.items():
                if not isinstance(settings, dict):
                    raise TypeError("When use_tab is True the firt level of the settings value must be all dicts.")
                tab = Eto.Forms.TabPage(Text=key)
                control.Pages.Add(tab)
                table = self.map_tree(settings)
                tab.Content = self.tables[key] = table
            layout.AddRow(control)

        else:
            self.table = self.map_tree(settings)
            layout.AddRow(self.table)

        layout.EndVertical()
        layout.BeginVertical(
            Eto.Drawing.Padding(12, 18, 12, 24), Eto.Drawing.Size(6, 0), False, False
        )
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndVertical()

        self.Content = layout

    def map_tree(self, settings):
        """Create the items for the form."""
        table = Eto.Forms.TreeGridView()
        treecollection = Eto.Forms.TreeGridItemCollection()
        table.ShowHeader = True

        if self.allow_edit_key:
            column = Eto.Forms.GridColumn()
            column.HeaderText = "Key"
            column.Editable = False
            column.Sortable = True
            column.Expand = True
            column.DataCell = KeyCell(self)
            table.Columns.Add(column)
        else:
            column = Eto.Forms.GridColumn()
            column.HeaderText = "Key"
            column.Editable = False
            column.Sortable = True
            column.Expand = True
            column.DataCell = Eto.Forms.TextBoxCell(table.Columns.Count)
            table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Value"
        column.Editable = True
        column.Sortable = False
        column.DataCell = ValueCell(self)

        table.Columns.Add(column)

        def add_items(parent, items):
            keys = list(items.keys())
            keys.sort()
            for key in keys:
                value = items[key]
                item = Eto.Forms.TreeGridItem(Values=(key, value))
                if isinstance(value, dict):
                    add_items(item.Children, value)
                parent.Add(item)

        add_items(treecollection, settings)
        if self.allow_edit_key:
            treecollection.Add(Eto.Forms.TreeGridItem(Values=("", "")))

        table.DataStore = treecollection
        return table

    def add_empty_row(self, table=None):
        table = table or self.table
        table.DataStore.Add(Eto.Forms.TreeGridItem(Values=("", "")))
        table.ReloadData()

    def remove_row(self, item, table=None):
        table = table or self.table
        table.DataStore.Remove(item)
        table.ReloadData()

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

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        self._settings = settings.copy()

    @property
    def names(self):
        return self._names

    @property
    def values(self):
        return self._values

    def on_ok(self, sender, event):
        try:
            self.settings = {}

            def set_value(items, setting):
                for item in items:
                    key = item.GetValue(0)
                    if not key:
                        continue
                    value = item.GetValue(1)
                    if isinstance(value, dict):
                        set_value(item.Children, setting[key])
                    else:
                        try:
                            setting[key] = literal_eval(value)
                        except Exception:
                            setting[key] = value
            if not self.use_tab:
                set_value(self.table.DataStore, self.settings)
            else:
                for key in self.settings:
                    set_value(self.tables[key].DataStore, self.settings[key])

        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, event):
        self.Close(False)

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

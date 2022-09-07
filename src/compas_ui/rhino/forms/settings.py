from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms
import decimal
from compas.colors import Color


class CustomCell(Eto.Forms.CustomCell):

    def OnGetIdentifier(self, args):
        return str(args.Row)

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
    def __init__(self, settings, title="Settings", width=500, height=500, use_tab=False):
        self._settings = None
        self._names = None
        self._values = None
        self.settings = settings
        self.use_tab = use_tab

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
        column.DataCell = CustomCell()

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
        table.DataStore = treecollection
        return table

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
            def set_value(items, setting):
                for item in items:
                    key = item.GetValue(0)
                    value = item.GetValue(1)
                    if isinstance(value, dict):
                        set_value(item.Children, setting[key])
                    else:
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

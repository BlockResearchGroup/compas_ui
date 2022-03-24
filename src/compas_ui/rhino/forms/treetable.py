import Eto.Drawing
import Eto.Forms
import decimal
from compas.colors import Color


class CustomCell(Eto.Forms.CustomCell):

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
            control.Increment = 10 ** d.exponent

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


class TreeTable(Eto.Forms.TreeGridView):

    def __init__(self, data):
        super(TreeTable, self).__init__()
        self.data = data
        self.GridLines = Eto.Forms.GridLines.Horizontal

    @property
    def data(self):
        def set_value(items, setting):
            for item in items:
                key = item.GetValue(0)
                value = item.GetValue(1)
                if isinstance(value, dict):
                    set_value(item.Children, setting[key])
                else:
                    setting[key] = value

        set_value(self.DataStore, self._data)

    @data.setter
    def data(self, data):
        self._data = data
        self.map_dict(data)

    def map_dict(self, data):
        treecollection = Eto.Forms.TreeGridItemCollection()
        self.ShowHeader = True
        column = Eto.Forms.GridColumn()
        column.HeaderText = "Key"
        column.Editable = False
        column.Sortable = True
        column.Expand = True
        column.DataCell = Eto.Forms.TextBoxCell(self.Columns.Count)
        self.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Value"
        column.Editable = True
        column.Sortable = False
        column.DataCell = CustomCell()

        self.Columns.Add(column)

        def add_items(parent, items):
            keys = list(items.keys())
            keys.sort()
            for key in keys:
                value = items[key]
                item = Eto.Forms.TreeGridItem(Values=(key, value))
                if isinstance(value, dict):
                    add_items(item.Children, value)
                parent.Add(item)

        add_items(treecollection, data)
        self.DataStore = treecollection

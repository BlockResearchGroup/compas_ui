from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import ast

import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms

class BaseCell(Eto.Forms.CustomCell):

    def __init__(self, parent):
        self.parent = parent

    def OnGetIdentifier(self, args):
        return str(args.Row)


class DeleteCell(BaseCell):

    def OnCreateCell(self, args):
        key = args.Item.GetValue(0)
        control = Eto.Forms.Button(Text="X")
        control.Width = 5

        def on_click(sender, e):
            print("delete", key)

        control.Click += on_click

        return control


class DefaultAttributesForm(Eto.Forms.Dialog[bool]):
    def __init__(self, attributes, title="Attributes", width=500, height=500):

        self.attributes = attributes.copy()

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        self.table = table = Eto.Forms.TreeGridView()
        collection = Eto.Forms.TreeGridItemCollection()
        for k, v in self.attributes.items():
            collection.Add(Eto.Forms.TreeGridItem(Values=(k, str(v))))
        table.DataStore = collection
        table.ShowHeader = True


        column = Eto.Forms.GridColumn()
        column.HeaderText = "Name"
        column.Editable = True
        column.DataCell = Eto.Forms.TextBoxCell(0)
        table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Value"
        column.Editable = True
        column.DataCell = Eto.Forms.TextBoxCell(1)
        table.Columns.Add(column)

        try:
            column = Eto.Forms.GridColumn()
            column.HeaderText = "Delete"
            column.Editable = True
            column.DataCell = DeleteCell(self)
            table.Columns.Add(column)
        except Exception as e:
            print(e)


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
        self.attributes.clear()
        try:
            for row in self.table.DataStore:
                name = row[0]
                value = row[1]
                try:
                    value = ast.literal_eval(value)
                except Exception as e:
                    print(e)
                self.attributes[name] = value
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, event):
        self.Close(False)

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

if __name__ == "__main__":

    attributes = {
        "a": 10,
        "b": True,
        "c": "hello",
        "d": (0, 0, 0),
    }


    form = DefaultAttributesForm(attributes)
    form.show()

    print(form.attributes)
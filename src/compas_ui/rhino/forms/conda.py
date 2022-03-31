import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms


class CondaEnvsForm(Eto.Forms.Dialog[bool]):
    def __init__(self, envs):
        self.Title = "Conda Environments"
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = False
        self.ClientSize = Eto.Drawing.Size(800, 500)

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(
            Eto.Drawing.Padding(12, 12, 12, 0),
            Eto.Drawing.Size(0, 0),
            True,
            True,
        )

        self.table = Eto.Forms.GridView()
        self.table.ShowHeader = True
        self.table.DataStore = envs

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Name"
        column.Editable = False
        column.DataCell = Eto.Forms.TextBoxCell(self.table.Columns.Count)
        self.table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Path"
        column.Editable = False
        column.DataCell = Eto.Forms.TextBoxCell(self.table.Columns.Count)
        self.table.Columns.Add(column)

        layout.AddRow(self.table)
        layout.EndVertical()

        layout.BeginVertical(
            Eto.Drawing.Padding(12, 12, 12, 18),
            Eto.Drawing.Size(6, 0),
            False,
            False,
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

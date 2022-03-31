import System
import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms


class SearchPathsForm(Eto.Forms.Dialog[bool]):
    def __init__(self):
        self.Title = "Python Search Paths"
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = False
        self.ClientSize = Eto.Drawing.Size(800, 500)

        paths = [[str(path)] for path in Rhino.Runtime.PythonScript.SearchPaths]
        while len(paths) < 8:
            paths.append([""])

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(
            Eto.Drawing.Padding(12, 12, 12, 0),
            Eto.Drawing.Size(0, 0),
            True,
            True,
        )
        self.table = Eto.Forms.GridView()
        self.table.ShowHeader = False
        self.table.GridLines = Eto.Forms.GridLines.Horizontal
        self.table.DataStore = paths[3:]

        column = Eto.Forms.GridColumn()
        column.Editable = True
        column.Expand = True
        column.AutoSize = True
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
        paths = []
        for path in Rhino.Runtime.PythonScript.SearchPaths:
            paths.append(path)
        paths[:] = paths[:3]
        for row in self.table.DataStore:
            path = row[0]
            path = path.strip()
            if path:
                paths.append(path)
        paths = System.Array[System.String](paths)
        Rhino.Runtime.PythonScript.SearchPaths = paths

        self.Close(True)

    def on_cancel(self, sender, event):
        self.Close(False)

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

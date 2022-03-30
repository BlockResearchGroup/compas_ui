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
        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(
            Eto.Drawing.Padding(12, 12, 12, 0),
            Eto.Drawing.Size(0, 0),
            True,
            True,
        )
        paths = [[str(path)] for path in Rhino.Runtime.PythonScript.SearchPaths]
        while len(paths) < 8:
            paths.append([""])
        gridview = Eto.Forms.GridView()
        gridview.ShowHeader = True
        gridview.GridLines = Eto.Forms.GridLines.Horizontal
        self.data = gridview.DataStore = paths[3:]
        column = Eto.Forms.GridColumn()
        column.HeaderText = "Path"
        column.Editable = True
        column.Expand = True
        column.AutoSize = True
        cell = Eto.Forms.TextBoxCell(0)
        cell.AutoSelectMode = Eto.Forms.AutoSelectMode.OnFocus
        cell.VerticalAlignment = Eto.Forms.VerticalAlignment.Center
        cell.TextAlignment = Eto.Forms.TextAlignment.Left
        column.DataCell = cell
        gridview.Columns.Add(column)
        layout.AddRow(gridview)
        layout.EndVertical()
        layout.BeginVertical(
            Eto.Drawing.Padding(12, 12, 12, 18),
            Eto.Drawing.Size(6, 0),
            False,
            False,
        )
        self.DefaultButton = Eto.Forms.Button(Text="OK")
        self.DefaultButton.Click += self.ok
        self.AbortButton = Eto.Forms.Button(Text="Cancel")
        self.AbortButton.Click += self.cancel
        layout.AddRow(None, self.DefaultButton, self.AbortButton)
        layout.EndVertical()
        self.Content = layout

    def ok(self, sender, event):
        self.Close(True)

    def cancel(self, sender, event):
        self.Close(False)

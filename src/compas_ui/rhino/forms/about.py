import System
import Eto.Forms
import Rhino.UI


class AboutForm:
    def __init__(self, plugin):
        self.dialog = Eto.Forms.AboutDialog()
        self.dialog.Copyright = plugin["copyright"]
        self.dialog.Designers = System.Array[System.String](plugin["designers"])
        self.dialog.Developers = System.Array[System.String](plugin["developers"])
        self.dialog.Documenters = System.Array[System.String](plugin["documenters"])
        self.dialog.License = plugin["license"]
        self.dialog.ProgramDescription = plugin["description"]
        self.dialog.ProgramName = plugin["title"]
        self.dialog.Title = plugin["title"]
        self.dialog.Version = plugin["version"]
        self.dialog.Website = System.Uri(plugin["website"])

    def show(self):
        self.dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)

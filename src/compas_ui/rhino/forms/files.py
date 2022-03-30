import os

import System
import Rhino.UI
import Eto.Forms


class FileForm(Eto.Forms.Dialog[bool]):
    @staticmethod
    def open(dirname=None):
        dialog = Eto.Forms.OpenFileDialog()
        if dirname:
            dialog.Directory = System.Uri(dirname)
        dialog.MultiSelect = False
        result = dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
        if result != Eto.Forms.DialogResult.Ok:
            return
        return dialog.FileName

    @staticmethod
    def save(dirname=None, basename=None):
        dirname = dirname or os.path.expanduser("~")
        dialog = Eto.Forms.SaveFileDialog()
        if dirname:
            dialog.Directory = System.Uri(dirname)
        dialog.FileName = basename
        result = dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
        if result != Eto.Forms.DialogResult.Ok:
            return
        return dialog.FileName

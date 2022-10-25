from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import System
import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms


class SplashForm(Eto.Forms.Dialog[bool]):
    def __init__(self, title, url, width=800, height=450):

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = False
        self.ClientSize = Eto.Drawing.Size(width, height)
        self.WindowStyle = getattr(Eto.Forms.WindowStyle, "None")

        webview = Eto.Forms.WebView()
        webview.Size = Eto.Drawing.Size(width, height)
        webview.Url = System.Uri(url)
        webview.BrowserContextMenuEnabled = False
        webview.DocumentLoading += self.action

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical()
        layout.AddRow(webview)
        layout.EndVertical()
        self.Content = layout

    def action(self, sender, e):
        if e.Uri.Scheme == "action" and e.Uri.Host == "close":
            self.Close()

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

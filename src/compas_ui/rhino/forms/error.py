from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
import traceback
from functools import wraps

import Eto.Drawing
import Eto.Forms
import Rhino.UI
import Rhino


def error(title="Error", showLocalTraceback=True):
    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                if showLocalTraceback:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    text = traceback.format_exception(exc_type, exc_value, exc_tb)
                    text = "".join(text)
                else:
                    text = str(error)
                ErrorForm(text, title=title)

        return wrapper

    return outer


ISSUE_TEMPLATE = """---
name: Bug report
about: Create a report to help us improve

---
<!-- The link below shows a list of known-issues and how to fix them -->
<!-- https://blockresearchgroup.gitbook.io/FF/documentation/known-issues -->
<!-- If the error you encounter is not in the list, please describe it as following -->
<!-- We thank you on the feedback -->

**Describe the bug**
```bash
%s
```

**To Reproduce**
Steps to reproduce the behavior:
1. Please provide an input 3dm file
2. Describe the command that causes the error
3. A screenshot of error behavior

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots or video record to help explain your problem.

**Desktop (please complete the following information):**
 - OS: %s
 - Rhino version %s
 - FoFin version %s

**Additional context**
Add any other context about the problem here.
"""


class ErrorForm(Eto.Forms.Dialog[bool]):

    def __init__(self, error="Unknown", title="Error", width=800, height=500):
        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        textarea = Eto.Forms.TextArea()
        textarea.Text = error
        textarea.ReadOnly = True

        dynamic = Eto.Forms.DynamicLayout()
        dynamic.BeginVertical(
            Eto.Drawing.Padding(12, 12, 12, 0), Eto.Drawing.Size(0, 0), True, True
        )
        dynamic.AddRow(textarea)
        dynamic.EndVertical()
        dynamic.BeginVertical(
            Eto.Drawing.Padding(12, 12, 12, 18), Eto.Drawing.Size(6, 0), False, False
        )
        dynamic.AddRow(None, self.cancel)
        dynamic.EndVertical()

        self.Content = dynamic

        self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

    @property
    def cancel(self):
        self.AbortButton = Eto.Forms.Button(Text="Close")
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    def on_cancel(self, sender, event):
        self.Close()

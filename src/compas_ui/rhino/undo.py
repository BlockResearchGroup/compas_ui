from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.ui import UI
from functools import wraps
import scriptcontext as sc


def rhino_undo(command_name):

    def undo_redo_handler(sender, e):
        ui = UI()
        if e.Tag == "undo":
            ui.undo()
            e.Document.AddCustomUndoEvent(command_name, undo_redo_handler, "redo")
        if e.Tag == "redo":
            ui.redo()
            e.Document.AddCustomUndoEvent(command_name, undo_redo_handler, "undo")

    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sc.doc.EndUndoRecord(sc.doc.CurrentUndoRecordSerialNumber)
            undoRecord = sc.doc.BeginUndoRecord(command_name)
            if undoRecord == 0:
                print("undo record did not start")

            func(*args, **kwargs)

            sc.doc.AddCustomUndoEvent(command_name, undo_redo_handler, "undo")

            if undoRecord > 0:
                sc.doc.EndUndoRecord(undoRecord)

        return wrapper

    return outer


def skip_rhino_undo():

    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sc.doc.EndUndoRecord(sc.doc.CurrentUndoRecordSerialNumber)
            func(*args, **kwargs)
        return wrapper

    return outer

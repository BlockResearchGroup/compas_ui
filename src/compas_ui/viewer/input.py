from compas.plugins import plugin
from PySide2 import QtWidgets


@plugin(category='ui', requires=['PySide2'])
def get_real(parent=None, message=None, default=None, minimum=None, maximum=None):
    return QtWidgets.QInputDialog.getDouble(parent=parent.app.window, title="Input Real Number", label=message, value=default, minValue=minimum, maxValue=maximum)

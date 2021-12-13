# from .session import Session
# from .controller import Controller
# from .view import View
# from .menu import Menu
# from .toolbar import Toolbar

from .session import Session
from .controller import Controller
from .scene import Scene

# from .view import View
# from .forms import FilepathForm


class App(object):

    _instance = None

    def __new__(cls, name, *args, **kwargs):
        if not cls._instance:
            self = super(App, cls).__new__(cls)
            self.name = name
            self.session = Session(name)
            self.controller = Controller(self)
            self.scene = Scene(self)
            self.cloud = None
            cls._instance = self
        return cls._instance

    def __init__(self, name):
        pass

    def start(self):
        pass

    def restart(self):
        pass

    def shutdown(self):
        pass

    def load_session(self):
        # filepath = QtWidgets.QFileDialog.getOpenFileName(
        #     parent=self.app.window,
        #     caption="Select File",
        #     dir="",
        #     filter="OBJ Files (*.obj)"
        # )
        filepath = 'session.json'
        self.session.load(filepath)

    def save_session(self):
        # filepath = QtWidgets.QFileDialog.getOpenFileName(
        #     parent=self.app.window,
        #     caption="Select File",
        #     dir="",
        #     filter="OBJ Files (*.obj)"
        # )
        filepath = 'session.json'
        self.session.save(filepath)

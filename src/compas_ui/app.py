# from .session import Session
# from .controller import Controller
# from .view import View
# from .menu import Menu
# from .toolbar import Toolbar

from .session import Session
from .controller import Controller
from .scene import Scene
from .ui import UserInterface

# from .view import View
# from .forms import FilepathForm


class App(object):

    _count = 0
    _instance = None
    _default_context = 'Viewer'

    def __new__(cls, name, *args, **kwargs):
        if not cls._instance:
            cls._count += 1
            self = super(App, cls).__new__(cls)
            cls._instance = self
            self.name = name
            self.session = Session(name)
            self.controller = Controller(self)
            self.scene = Scene(self)
            self.ui = UserInterface(self)
            self.cloud = None
            self.context = kwargs.get('context') or cls._default_context
            self.start()
        return cls._instance

    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        if self.context == 'Viewer':
            from compas_view2.app import App
            self.app = App(enable_sidebar=True, width=1200, height=750)

    def show(self):
        if self.context == 'Viewer':
            self.app.show()

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

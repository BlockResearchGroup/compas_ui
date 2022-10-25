from compas.data import Data


class Group(Data):
    def __init__(self, items=None):
        super(Group, self).__init__()
        self.items = items or set()

    def add(self, item):
        self.items.add(item)

    def remove(self, item):
        self.items.remove(item)

    @property
    def data(self):
        return {"items": list(self.items)}

    @data.setter
    def data(self, data):
        self.items = set(data["items"])

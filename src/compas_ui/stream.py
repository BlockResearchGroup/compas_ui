from compas.data import Data
from compas.data import json_dumps
import json

class Stream(object):

    _proxy = None

    def __init__(self, item, id=None):
        self.item = item
        self.id = id
        self.branch = "main"
        self.commit = None
        self.stream_info = None

    def __getstate__(self):
        return self.state

    def __setstate__(self, state):
        self.state = state

    @classmethod
    def from_state(cls, item, state):
        stream = cls(item)
        stream.state = state
        return stream

    @classmethod
    def proxy(cls):
        if not cls._proxy:
            from compas_ui.ui import UI
            cls._proxy = UI().proxy
        return cls._proxy

    @property
    def state(self):
        return {'id': self.id, 'branch': self.branch, 'commit': self.commit}

    @state.setter
    def state(self, state):
        self.__dict__.update(state)

    @classmethod
    def list_streams(self):
        return self.proxy().speckle_operation("list_streams")

    @property
    def branches(self):
        return [branch_info["name"] for branch_info in self.stream_info["branches"]["items"]]

    @property
    def branch_info(self):
        return next(branch for branch in self.stream_info["branches"]["items"] if branch["name"] == self.branch)

    @property
    def commits(self):
        return [commit_info["id"] for commit_info in self.branch_info["commits"]["items"]]

    @property
    def commit_info(self):
        return next(commit for commit in self.commits if commit["id"] == self.commit)

    def fecth(self):
        self.stream_info = self.proxy().speckle_operation("fetch", {"stream_id": self.id})

    def checkout(self, branch=None, commit=None):
        if branch:
            self.branch = branch
        if commit:
            self.commit = commit

        content = self.proxy().speckle_operation("checkout", {"stream_id": self.id, "branch_name": self.branch, "commit_id": self.commit})

        if isinstance(self.item, Data):
            self.item.data = content
        elif hasattr(self.item, "state"):
            self.item.state = content
        else:
            raise Exception("Not sure what to do with item type: ".format(type(self.item)))

    def pull(self):
        self.fecth()
        self.checkout(commit=self.commits[0]["id"])

    def push(self, message=None):

        if not self.id:
            self.id = self.proxy().speckle_operation("create_stream", {"name": self.item.name})
            print("Created stream: {} with name {}".format(self.id, self.item.name))

        if isinstance(self.item, Data):
            item_state = json.loads(json_dumps(self.item))
        elif hasattr(self.item, "state"):
            item_state = self.item.state
        else:
            raise Exception("Not sure what to do with item type: ".format(type(self.item)))

        if "stream" in item_state:
            del item_state["stream"]

        commit_id = self.proxy().speckle_operation("commit", {"stream_id": self.id, "item": item_state, "message": message})

        # Update commit info
        self.fecth()
        commit = next(commit for commit in self.branch_info["commits"]["items"] if commit["id"] == commit_id)    
        self.commit = commit["id"]

        print("Commit {} pushed.".format(self.commit))
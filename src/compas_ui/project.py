import compas
import json


class Project(object):

    def __init__(self, ui):
        self._ui = ui
        self.stream_id = None
        self.name = "Untitled"
        self.data = {}
        self.scenes = {}
        self.session = {}

    def __getstate__(self):
        return self.state

    def __setstate__(self, state):
        self.state = state

    @property
    def ui(self):
        if not hasattr(self, '_ui') or self._ui is None:
            from compas_ui.ui import UI
            self._ui = UI()
        return self._ui

    def update(self):
        """Update the project state base on what's available in the scene."""

        self.data.clear()
        for obj in self.ui.scene.objects:
            # Update data states
            if str(obj.item.guid) not in self.data:
                stream_id = None
                if hasattr(obj.item, 'stream_id'):
                    stream_id = obj.item.stream_id
                item_state = json.loads(compas.json_dumps(obj.item))
                self.data[str(obj.item.guid)] = {"name": str(obj.item.name), "stream_id": stream_id, "state": item_state, "_pointer": obj.item}

        # Update scene states
        # TODO: this needs to be adjusted when multi scenes are supported.
        self.scenes.clear()
        for scene in [self.ui.scene]:
            scene_state = scene.state
            del scene_state['data']
            self.scenes[str(scene.guid)] = {"name": str(self.name), "stream_id": scene.stream_id, "state": scene_state, "_pointer": scene}

        # Update session data
        self.session = self.ui.session.data

    @property
    def state(self):
        state = self.__dict__.copy()
        # Exclude _ui and _pointer from the state
        for key, collection in list(state.items()):
            if key.startswith('_'):
                del state[key]
            elif isinstance(collection, dict):
                for wrapper in collection.values():
                    if "_pointer" in wrapper:
                        del wrapper['_pointer']
        return state

    @state.setter
    def state(self, state):
        self.__dict__.update(state)

    def push(self, message=None):

        self.update()

        # Push data
        for guid, wrapper in self.data.items():
            wrapper['_pointer'].stream_id = self.ui.proxy.speckle_push(stream_id=wrapper["stream_id"], item=wrapper["state"], name=wrapper["name"]+".data", message=message)
            print("data pushed:", wrapper['_pointer'].stream_id)

        # Push scene
        for guid, wrapper in self.scenes.items():
            wrapper['_pointer'].stream_id = self.ui.proxy.speckle_push(stream_id=wrapper["stream_id"], item=wrapper["state"], name=wrapper["name"]+".scene", message=message)
            print("scene pushed:", wrapper['_pointer'].stream_id)

        # Push project
        self.stream_id = self.ui.proxy.speckle_push(stream_id=self.stream_id, item=self.state, name=self.name+".project", message=message)
        print("project pushed:", self.stream_id)

    def pull(self):
        # Load project
        self.state = self.ui.proxy.speckle_pull(self.stream_id)

        # Load data
        data = {}
        for guid, wrapper in self.state['data'].items():
            item = self.ui.proxy.speckle_pull(wrapper['stream_id'])
            item._guid = guid
            data[guid] = item

        # Load scene
        # TODO: this needs to be adjusted when multi scenes are supported.
        self.ui.scene.clear()
        for guid, wrapper in self.state['scenes'].items():
            scene_state = self.ui.proxy.speckle_pull(wrapper["stream_id"])
            scene_state['data'] = data
            self.ui.scene.state = scene_state
            wrapper["_pointer"] = self.ui.scene
            self.ui.scene._guid = guid
        self.ui.scene.update()

        # Load session
        self.ui.session.data = self.state['session']

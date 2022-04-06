class Project(object):

    def __init__(self, ui):
        self.stream_id = None
        self.name = "Untitled"
        self._ui = ui

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

    @property
    def state(self):

        objects = []
        data_dict = {}
        for obj in self.ui.scene.objects:
            objects.append(obj.stream_id)
            data = obj.item
            guid = str(data.guid)
            if guid not in data_dict:
                if hasattr(data, 'stream_id'):
                    data_dict[guid] = data.stream_id
                else:
                    data_dict[guid] = None

        return {
            "name": self.name,
            "stream_id": self.stream_id,
            "session": self.ui.session.data,
            "data": list(data_dict.values()),
            "objects": objects,
            "scenes": [self.ui.scene.stream_id]
        }

    @state.setter
    def state(self, state):
        self.name = state['name']
        self.stream_id = state['stream_id']

    def push(self, message=None):

        data_dict = {}
        for obj in self.ui.scene.objects:
            data = obj.item
            guid = str(data.guid)
            if guid not in data_dict:
                data_dict[guid] = data

        for data in data_dict.values():
            # Push object data
            if not hasattr(data, 'stream_id'):
                data.stream_id = None
            data.stream_id = self.ui.proxy.speckle_push(stream_id=data.stream_id, item=data, name=data.name+".data", message=message)
            print("data", data.stream_id)

        for obj in self.ui.scene.objects:
            # Push object state
            obj_state = obj.state
            for key in list(obj_state.keys()):
                if key.startswith('_guid'):
                    del obj_state[key]
            del obj_state['_item']
            obj_state['data'] = obj.item.stream_id
            obj.stream_id = self.ui.proxy.speckle_push(stream_id=obj.stream_id, item=obj_state, name=obj.name+".object", message=message)
            print("obj", obj.stream_id)

        # Push scene
        scene = {'objects': [obj.stream_id for obj in self.ui.scene.objects], 'settings': self.ui.scene.settings}
        self.ui.scene.stream_id = self.ui.proxy.speckle_push(stream_id=self.ui.scene.stream_id, item=scene, name=self.name+".scene", message=message)
        print("scene", self.ui.scene.stream_id)

        # Push project
        self.stream_id = self.ui.proxy.speckle_push(stream_id=self.stream_id, item=self.state, name=self.name+".project", message=message)
        print("project pushed:", self.state)

    def pull(self):
        # Load project
        state = self.ui.proxy.speckle_pull(self.stream_id)
        print("project pulled:", state)
        self.state = state
        self.ui.scene.clear()
        # Load session
        self.ui.session.data = state['session']
        # Load scene
        scene = self.ui.proxy.speckle_pull(state['scenes'][0])
        self.ui.scene.settings = scene["settings"]
        for obj_stream_id in scene['objects']:
            # Load object state
            obj_state = self.ui.proxy.speckle_pull(obj_stream_id)
            # Load object data
            data = self.ui.proxy.speckle_pull(obj_state['data'])
            obj = self.ui.scene.add(data)
            del obj_state['data']
            obj.state = obj_state
        self.ui.scene.update()

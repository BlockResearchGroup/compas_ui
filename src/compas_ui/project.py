from compas_ui.stream import Stream

class Project(object):

    def __init__(self, ui):
        self._ui = ui
        self.stream = Stream(self)
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

    @property
    def state(self):
        # gather data stream_states
        self.data.clear()
        for obj in self.ui.scene.objects:
            if str(obj.item.guid) not in self.data:
                if not hasattr(obj.item, 'stream'):
                    obj.item.stream = Stream(obj.item) # Create stream if not present
                self.data[str(obj.item.guid)] = obj.item.stream.state

        # gather scene stream_states
        self.scenes.clear()
        for scene in [self.ui.scene]:
            self.scenes[str(scene.guid)] = scene.stream.state

        # Update session data
        self.session = self.ui.session.data

        state = self.__dict__.copy()
        del state['_ui']
        return state

    @state.setter
    def state(self, state):
        self.__dict__.update(state)
        self.ui.session.data = self.ui.session

    def load_from_stream(self):
        # Load data
        data = {}
        for guid, stream_state in self.state['data'].items():
            # Recreate data item from stream state
            item = self.ui.proxy.speckle_operation("checkout", stream_state)
            item.stream = Stream.from_state(item, stream_state)
            data[guid] = item

        # Load scene
        # TODO: this needs to be adjusted when multi scenes are supported.
        scene = self.ui.scene
        for guid, stream_state in self.state['scenes'].items():
            scene.clear()
            scene_state = self.ui.proxy.speckle_operation("checkout", stream_state)
            scene_state['data'] = data
            scene.state = scene_state
            scene._guid = guid
            scene.stream = Stream.from_state(scene, stream_state)
            scene.update()

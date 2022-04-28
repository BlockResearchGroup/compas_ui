from compas_stream.project import Project
from compas_stream.stream import checkout
from compas.data import json_dumps, json_loads
import json


class Project(Project):

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.name = "Untitled"

    def update_tracking(self):
        for obj in self.ui.scene.objects:
            data = obj.item

            def getter():
                return json.loads(json_dumps(data))

            def setter(self, content):
                self.data = json_loads(json.dumps(content)).data

            self.track(data.guid, data, getter=getter, setter=setter)

        self.track(self.ui.scene.guid, self.ui.scene)
        self.track(self.guid, self)

    @property
    def stream_content(self):

        self.update_tracking()
        content = {"data": {}, "scenes": {}}

        # gather data stream states
        for obj in self.ui.scene.objects:
            guid = str(obj.item.guid)
            content["data"][guid] = self.streams[guid].state

        # gather scene stream states
        guid = str(self.ui.scene.guid)
        content["scenes"][guid] = self.streams[guid].state

        return content

    @stream_content.setter
    def stream_content(self, content):

        # Load data
        data = {}
        for guid, stream_state in content["data"].items():
            # Recreate data item from stream state
            data[guid] = checkout(**stream_state)

        # Load scene
        # TODO: this needs to be adjusted when multi scenes are supported.
        for guid, stream_state in content["scenes"].items():
            scene_state = checkout(**stream_state)
            scene_state["data"] = data
            self.ui.scene.state = scene_state

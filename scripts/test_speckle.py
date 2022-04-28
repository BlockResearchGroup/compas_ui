from compas.datastructures import Mesh
from compas_ui.ui import UI
from compas_ui.stream import Stream
import compas

ui = UI(config={
    "plugin": {
        "title": "COMPAS",
    },
    "settings": {
        "cloud": {
            "speckle": {
                "host": "speckle.xyz",
                "token": "4b6a06f4c7b114e3b4115e1bba5536261cb4d3bf20"
            },
            "background": False
        }
    },

})

ui.cloud_start()

mesh = Mesh.from_obj(compas.get('tubemesh.obj'))
# mesh.stream = Stream(mesh)
mesh.name = "TEST MESH"
# mesh.stream.push("init")

ui.scene.add(mesh)

ui.project.stream.push()

print(ui.project.state)
from compas.datastructures import Mesh
from compas_ui.ui import UI
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
            }
        }
    },

})

ui.cloud_start()

# # PUSH SCENE TO SPECKLE
# mesh = Mesh.from_obj(compas.get('tubemesh.obj'))
# ui.scene.add(mesh)
# scene_id = ui.scene.speckle_push()
# print(scene_id) 
# # 72db928f2e

ui.scene.speckle_id = "72db928f2e"
ui.scene.speckle_pull()
print(ui.scene.state)
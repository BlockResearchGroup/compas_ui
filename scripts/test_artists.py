from compas_ui.ui import UI
from compas.geometry import Frame
from compas.geometry import Line
from compas_rhino.geometry import RhinoCurve
import compas_rhino


ui = UI({"plugin": {"title": ["Frame"]}, "settings": {}})
ui.scene.clear()

line = Line([0, 0, 0], [10, 0, 0])
lineObj = ui.scene.add(line, name='line', frame=Frame([20, 0, 0], [1, 0, 0], [0, 1, 0]))

guid = compas_rhino.select_curve('Select a curve')
rhinoCurve = RhinoCurve.from_guid(guid)
curve = rhinoCurve.to_compas()
curveObj = ui.scene.add(curve, name='curve', frame=Frame([0, 20, 0], [1, 0, 0], [0, 1, 0]))

ui.scene.update()

lineObj.move_start()
ui.scene.update()

# curveObj.move_start()
# ui.scene.update()
from compas_ui.ui import UI
import Eto.Forms


__commandname__ = "COMPAS_scene_clear"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    if (
        Eto.Forms.MessageBox.Show(
            "Are you sure you want to clear the scene?",
            "Confirm",
            Eto.Forms.MessageBoxButtons.YesNo,
        )
        == Eto.Forms.DialogResult.Yes
    ):
        ui.scene_clear()


if __name__ == "__main__":
    RunCommand(True)

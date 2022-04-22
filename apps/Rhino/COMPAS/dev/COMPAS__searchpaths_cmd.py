from compas_ui.ui import UI


__commandname__ = "COMPAS__searchpaths"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.rhinopython_searchpaths()


if __name__ == "__main__":
    RunCommand(True)

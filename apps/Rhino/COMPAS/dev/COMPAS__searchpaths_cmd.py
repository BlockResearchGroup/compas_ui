__commandname__ = "COMPAS__searchpaths"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.rhinopython_searchpaths()


if __name__ == "__main__":
    RunCommand(True)

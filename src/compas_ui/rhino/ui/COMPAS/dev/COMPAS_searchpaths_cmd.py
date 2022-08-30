from compas_ui.ui import UI

# TODO: inspect current search paths
# TODO: provide option to set/edit search paths as alternative for installed conda envs


__commandname__ = "COMPAS_searchpaths"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.rhinopython_searchpaths()


if __name__ == "__main__":
    RunCommand(True)

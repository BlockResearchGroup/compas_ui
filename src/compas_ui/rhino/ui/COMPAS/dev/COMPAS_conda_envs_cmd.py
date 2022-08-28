from compas_ui.ui import UI

# TODO: make window pop up automatically
# TODO: allow path to conda installation to be set
# TODO: show all available envs
# TODO: mark active environment
# TODO: allow environment to be activated (make user aware of need for restart)
# TODO: provide overview of installed packages per environment


__commandname__ = "COMPAS_conda_envs"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.conda_envs()


if __name__ == "__main__":
    RunCommand(True)

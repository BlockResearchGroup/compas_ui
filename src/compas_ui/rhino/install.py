import os
import sys

from shutil import copyfile
from subprocess import call

import compas
from compas.plugins import plugin
import compas_rhino

from compas_rhino.install_plugin import install_plugin
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


HERE = os.path.dirname(__file__)


def get_version_from_args():
    args = compas_rhino.INSTALLATION_ARGUMENTS
    return compas_rhino._check_rhino_version(args.version)


@plugin(category="install", tryfirst=True)
def after_rhino_install(installed_packages):
    if "compas_cloud" not in installed_packages:
        return []

    version = get_version_from_args()
    install(version)

    return [("compas_ui", "COMPAS UI installed", True)]


@plugin(category="install", tryfirst=True)
def installable_rhino_packages():
    return ["compas_ui"]


def check_folders(plugin_name, version="7.0"):
    try:
        print("Checking that the plugin folder exists")
        plugin_name = "COMPAS"
        plugin_path = os.path.join(HERE, "ui", plugin_name)
        if not os.path.isdir(plugin_path):
            raise Exception("Cannot find the plugin: {}".format(plugin_path))
        print(plugin_path, "Exists")
        print("PASSED.\n")

        print("Checking that the plugin folder contains a dev folder")
        plugin_path = os.path.abspath(plugin_path)
        plugin_dev = os.path.join(plugin_path, "dev")
        if not os.path.isdir(plugin_dev):
            raise Exception("Cannot find the dev folder at: {}".format(plugin_dev))
        print(plugin_dev, "Exists")
        print("PASSED.\n")

        print("Checking that the dev folder contains config.json")
        plugin_config = os.path.join(plugin_dev, "config.json")
        if not os.path.isfile(plugin_config):
            raise Exception("Cannot find the config file at: {}".format(plugin_config))
        print(plugin_config, "Exists")
        print("PASSED.\n")

        print("Checking that the Rhino scripts folder exists")
        rhino_scripts_path = compas_rhino._get_rhino_scripts_path(version)
        if not os.path.isdir(rhino_scripts_path):
            raise Exception("Cannot find the Rhino scripts folder at: {}".format(rhino_scripts_path))
        print(rhino_scripts_path, "Exists")
        print("PASSED.\n")

        print("Checking that user has write access to the Rhino scripts folder")
        if not os.access(rhino_scripts_path, os.W_OK):
            raise Exception(
                "User does not have write access to the Rhino scripts folder at: {}".format(rhino_scripts_path)
            )
        print("User has write access to the Rhino scripts folder")
        print("PASSED.\n")

        print("\n All checks passed.")
        return True

    except Exception as e:
        print("FAILED:")
        print(e)
        return False


def check_dependencies(requirements_path=None):
    try:
        dependencies = []
        with open(
            requirements_path or os.path.join(HERE, "..", "..", "..", "requirements.txt"),
            "r",
        ) as f:
            for line in f.readlines():
                if line.startswith("#"):
                    continue
                dependencies.append(line.rstrip())

        print("Required packages:")
        print(dependencies)

        pkg_resources.require(dependencies)

        print("\n All checks passed.")
        return True
    except (DistributionNotFound, VersionConflict) as e:
        print("FAILED:")
        print(e)
        return False


def install(version="7.0"):
    plugin_name = "COMPAS"
    plugin_path = os.path.join(HERE, "ui", plugin_name)
    if not os.path.isdir(plugin_path):
        raise Exception("Cannot find the plugin: {}".format(plugin_path))

    plugin_path = os.path.abspath(plugin_path)
    plugin_dev = os.path.join(plugin_path, "dev")

    install_plugin(plugin_path)

    if compas.WINDOWS:
        plugin_ruipy = os.path.join(plugin_dev, "rui.py")
        plugin_rui = "{}.rui".format(plugin_name)
        python_plugins_path = compas_rhino._get_rhino_pythonplugins_path(version)

        call(sys.executable + " " + plugin_ruipy, shell=True)
        copyfile(
            os.path.join(plugin_dev, plugin_rui),
            os.path.join(python_plugins_path, "..", "..", "UI", plugin_rui),
        )


if __name__ == "__main__":

    print("This installation procedure is deprecated.")
    print("Use `python -m compas_rhino.install` instead.")

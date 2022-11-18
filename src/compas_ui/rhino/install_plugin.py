import os
import imp

import compas
import compas_rhino

from compas._os import create_symlinks
from compas._os import remove_symlinks

import sys

from shutil import copyfile
from subprocess import call
from importlib import import_module


def get_version_from_args():
    args = compas_rhino.INSTALLATION_ARGUMENTS
    return compas_rhino._check_rhino_version(args.version)


def get_package_plugins(package_name):

    plugin_paths = []

    package = import_module(package_name)
    package_dir = os.path.dirname(package.__file__)
    package_plugins_path = os.path.join(package_dir, "rhino", "ui")
    if os.path.exists(package_plugins_path):
        for plugin_name in os.listdir(package_plugins_path):
            plugin_path = os.path.join(package_plugins_path, plugin_name)
            plugin_path = os.path.abspath(plugin_path)
            plugin_dev = os.path.join(plugin_path, "dev")
            if os.path.exists(plugin_dev):
                plugin_paths.append(plugin_path)

    return plugin_paths


def install_plugin(plugin, generate_rui=False):
    """Install a Rhino Python Command Plugin."""
    if not os.path.isdir(plugin):
        raise Exception("Cannot find the plugin: {}".format(plugin))

    version = get_version_from_args()

    plugin_dir = os.path.abspath(plugin)

    # -----------------------------
    # proceed with the installation
    # -----------------------------

    plugin_path, plugin_name = os.path.split(plugin_dir)
    plugin_path = plugin_path or os.getcwd()

    plugin_dev = os.path.join(plugin_dir, "dev")

    if not os.path.isdir(plugin_dev):
        raise Exception("The plugin does not contain a dev folder.")

    plugin_info = os.path.join(plugin_dev, "__plugin__.py")

    if not os.path.isfile(plugin_info):
        raise Exception("The plugin does not contain plugin info.")

    __plugin__ = imp.load_source("__plugin__", plugin_info)

    if not __plugin__.id:
        raise Exception("Plugin id is not set.")

    if not __plugin__.title:
        raise Exception("Plugin title is not set.")

    plugin_fullname = "{}{}".format(__plugin__.title, __plugin__.id)

    python_plugins_path = compas_rhino._get_rhino_pythonplugins_path(version)

    if not os.path.exists(python_plugins_path):
        os.mkdir(python_plugins_path)

    source = plugin_dir
    destination = os.path.join(python_plugins_path, plugin_fullname)

    # print("\nInstalling PlugIn {} to Rhino PythonPlugIns.".format(plugin_name))

    remove_symlinks([destination])
    create_symlinks([(source, destination)])

    # print("\nPlugIn {} Installed.".format(plugin_name))

    if compas.WINDOWS and generate_rui:
        # Allow rui generation to fail. It is not critical.
        try:
            plugin_ruipy = os.path.join(plugin_dev, "rui.py")
            plugin_rui = "{}.rui".format(plugin_name)
            cmd = '"{}" "{}"'.format(sys.executable, plugin_ruipy)
            call(cmd, shell=True)
            copyfile(
                os.path.join(plugin_dev, plugin_rui),
                os.path.join(python_plugins_path, "..", "..", "UI", plugin_rui),
            )
            print("PlugIn {} RUI file generated.".format(plugin_name))
        except Exception as e:
            print("PlugIn {} RUI file generation failed.".format(plugin_name))
            print(e)

    return "python plugin {} installed".format(plugin_fullname)


def clean_up(plugins):

    version = get_version_from_args()

    # Clean up the plugin directory
    symlinks_to_remove = []
    python_plugins_path = compas_rhino._get_rhino_pythonplugins_path(version)
    if not os.path.exists(python_plugins_path):
        os.mkdir(python_plugins_path)

    for name in os.listdir(python_plugins_path):
        path = os.path.join(python_plugins_path, name)
        if os.path.islink(path):
            # Check if the symlink is pointing to a valid location
            if not os.path.exists(path):
                symlinks_to_remove.append(dict(name=name, link=path))

            # Check if the symlink is one of the plugins we are installing
            if name in plugins:
                symlinks_to_remove.append(dict(name=name, link=path))

    symlinks_removed = []
    symlinks_unremoved = []

    if symlinks_to_remove:
        symlinks = [link["link"] for link in symlinks_to_remove]
        removal_results = remove_symlinks(symlinks)
        for uninstall_data, success in zip(symlinks_to_remove, removal_results):
            if success:
                symlinks_removed.append(uninstall_data["name"])
            else:
                symlinks_unremoved.append(uninstall_data["name"])

    if symlinks_removed:
        print("\nThe following package symlinks were removed:\n")
        for name in symlinks_removed:
            print("   {}".format(name.ljust(20)))

    if symlinks_unremoved:
        print("\nThe following package symlinks could not be removed:\n")
        for name in symlinks_unremoved:
            print("   {}".format(name.ljust(20)))

    print("\nClean up complete.\n")

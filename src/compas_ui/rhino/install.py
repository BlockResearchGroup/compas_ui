import os
from compas.plugins import plugin
from .install_plugin import install_plugin
from .install_plugin import clean_up
from .install_plugin import get_package_plugins


HERE = os.path.dirname(__file__)
PLUGINS = [
    "COMPAS{6c18fcab-3ae5-4b03-b515-d33d8078b977}",
    "FoFin{18a65b9c-1a08-43ef-a1fd-ef458f0a1fa0}",
    "IGS2{aa509b0a-64d6-4a3f-a0c3-028565cf3174}",
    "IGS{3e33b31b-86ac-402c-babf-d3c16962ed33}",
    "RV2{949ca7a4-7ddf-4939-8a5b-d945d5ac0bc8}",
    "TNO{7dfe0ab6-2352-405b-a19b-a6017f92b6b4}",
    "3GS{7ce56e93-79c1-44ac-9716-1a53ca42ac9c}",
]


@plugin(category="install", tryfirst=True)
def after_rhino_install(installed_packages):
    if "compas_cloud" not in installed_packages:
        return []

    # Clean up old plugins and broken links
    clean_up(PLUGINS)

    # Install plugins from each package
    results = []
    for package in installed_packages:
        plugin_paths = get_package_plugins(package)
        for plugin_path in plugin_paths:
            message = install_plugin(plugin_path, generate_rui=True)
            results.append((package, message, True))

    return results


@plugin(category="install", tryfirst=True)
def installable_rhino_packages():
    return ["compas_ui"]


if __name__ == "__main__":

    print("This installation procedure is deprecated.")
    print("Use `python -m compas_rhino.install` instead.")

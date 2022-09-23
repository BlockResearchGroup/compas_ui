# -*- coding: utf-8 -*-

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = "1.0"

import inspect
import importlib

import sphinx_compas_theme
from sphinx.ext.napoleon.docstring import NumpyDocstring

# -- General configuration ------------------------------------------------

project = "COMPAS UI"
copyright = "ETH Zurich - Block Research Group"
author = "tom van mele"
release = "0.6.1"
version = ".".join(release.split(".")[0:2])

master_doc = "index"
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
templates_path = sphinx_compas_theme.get_autosummary_templates_path()
exclude_patterns = []

pygments_style = "sphinx"
show_authors = True
add_module_names = True
language = None


# -- Extension configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.linkcode",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.coverage",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    "matplotlib.sphinxext.plot_directive",
    "tabs",
]

# autodoc options

autodoc_type_aliases = {}

# this does not work properly yet
autodoc_typehints = "none"
autodoc_typehints_format = "short"
autodoc_typehints_description_target = "documented"

autodoc_mock_imports = [
    "System",
    "clr",
    "Eto",
    "Rhino",
    "Grasshopper",
    "scriptcontext",
    "rhinoscriptsyntax",
    "bpy",
    "bmesh",
    "mathutils",
]

autodoc_default_options = {
    "undoc-members": True,
    "show-inheritance": True,
}

autodoc_member_order = "groupwise"

autoclass_content = "class"


def skip(app, what, name, obj, would_skip, options):
    if name.startswith("_"):
        return True
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)


# autosummary options

autosummary_generate = True
autosummary_mock_imports = [
    "System",
    "clr",
    "Eto",
    "Rhino",
    "Grasshopper",
    "scriptcontext",
    "rhinoscriptsyntax",
    "bpy",
    "bmesh",
    "mathutils",
]

# graph options

inheritance_graph_attrs = dict(rankdir="LR", resolution=150)
inheritance_node_attrs = dict(fontsize=8)

# napoleon options

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False


# first, we define new methods for any new sections and add them to the class
def parse_keys_section(self, section):
    return self._format_fields("Keys", self._consume_fields())


NumpyDocstring._parse_keys_section = parse_keys_section


def parse_attributes_section(self, section):
    return self._format_fields("Attributes", self._consume_fields())


NumpyDocstring._parse_attributes_section = parse_attributes_section


def parse_class_attributes_section(self, section):
    return self._format_fields("Class Attributes", self._consume_fields())


NumpyDocstring._parse_class_attributes_section = parse_class_attributes_section


def parse_other_attributes_section(self, section):
    return self._format_fields("Other Attributes", self._consume_fields())


NumpyDocstring._parse_other_attributes_section = parse_other_attributes_section


# we now patch the parse method to guarantee that the the above methods are
# assigned to the _section dict
def patched_parse(self):
    self._sections["keys"] = self._parse_keys_section
    self._sections["attributes"] = self._parse_attributes_section
    self._sections["class attributes"] = self._parse_class_attributes_section
    self._sections["others attributes"] = self._parse_other_attributes_section
    self._unpatched_parse()


NumpyDocstring._unpatched_parse = NumpyDocstring._parse
NumpyDocstring._parse = patched_parse


# plot options

plot_include_source = False
plot_html_show_source_link = False
plot_html_show_formats = False
plot_formats = ["png"]
# plot_pre_code
# plot_basedir
# plot_rcparams
# plot_apply_rcparams
# plot_working_directory

plot_template = """
{{ only_html }}

   {% for img in images %}
   {% set has_class = false %}

   .. figure:: {{ build_dir }}/{{ img.basename }}.{{ default_fmt }}
      :class: figure-img img-fluid

      {{ caption }}

   {% endfor %}
"""

# intersphinx options

intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "compas": ("https://compas.dev/compas/latest/", None),
}

# linkcode


def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    if not info["module"]:
        return None
    if not info["fullname"]:
        return None

    package = info["module"].split(".")[0]
    if not package.startswith("compas_ui"):
        return None

    module = importlib.import_module(info["module"])
    parts = info["fullname"].split(".")

    if len(parts) == 1:
        obj = getattr(module, info["fullname"])
        filename = inspect.getmodule(obj).__name__.replace(".", "/")
        lineno = inspect.getsourcelines(obj)[1]
    elif len(parts) == 2:
        obj_name, attr_name = parts
        obj = getattr(module, obj_name)
        attr = getattr(obj, attr_name)
        if inspect.isfunction(attr):
            filename = inspect.getmodule(obj).__name__.replace(".", "/")
            lineno = inspect.getsourcelines(attr)[1]
        else:
            return None
    else:
        return None

    return f"https://github.com/blockresearchgroup/compas_ui/blob/master/src/{filename}.py#L{lineno}"


# extlinks

extlinks = {
    "rhino": ("https://developer.rhino3d.com/api/RhinoCommon/html/T_%s.htm", "%s"),
    "blender": ("https://docs.blender.org/api/2.93/%s.html", "%s"),
}

# -- Options for HTML output ----------------------------------------------

html_theme = "compaspkg"
html_theme_path = sphinx_compas_theme.get_html_theme_path()

html_theme_options = {
    "package_name": "compas_ui",
    "package_title": project,
    "package_version": release,
    "package_author": "tom van mele",
    "package_docs": "https://blockresearchgroup.github.io/compas_ui/",
    "package_repo": "https://github.com/blockresearchgroup/compas_ui",
    "package_old_versions_txt": "https://blockresearchgroup.github.io/compas_ui/doc_versions.txt",
}

html_context = {}
html_static_path = sphinx_compas_theme.get_html_static_path()
html_extra_path = []
html_last_updated_fmt = ""
html_copy_source = False
html_show_sourcelink = False
html_permalinks = False
html_permalinks_icon = ""
html_experimental_html5_writer = False
html_compact_lists = True

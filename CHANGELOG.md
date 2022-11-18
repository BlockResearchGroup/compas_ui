# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.4] 2022-11-18

### Added

### Changed

### Removed


## [0.8.3] 2022-11-17

### Added

### Changed

### Removed


## [0.8.2] 2022-11-17

### Added

### Changed

### Removed


## [0.8.1] 2022-11-17

### Added

### Changed

### Removed


## [0.8.0] 2022-11-17

### Added

### Changed

### Removed


## [0.7.1] 2022-11-09

### Added

* Added `compas_ui.rhino.install.after_rhino_install`.

### Changed

### Removed

* Removed `compas_ui.rhino.install.main`.


## [0.7.0] 2022-10-25

### Added

### Changed

* Use `black` as formatter.
* Updated all github workflows to v2

### Removed


## [0.6.2] 2022-09-24

### Added

### Changed

### Removed


## [0.6.1] 2022-09-23

### Added

### Changed

### Removed


## [0.6.0] 2022-09-23

### Added

### Changed

### Removed


## [0.5.3] 2022-09-23

### Added

### Changed

### Removed


## [0.5.2] 2022-09-23

### Added

### Changed

### Removed


## [0.5.1] 2022-09-22

### Added

### Changed

### Removed


## [0.5.0] 2022-09-21

### Added

* Added `compas_ui.rhino.forms.AboutForm`.
* Added `compas_ui.rhino.forms.CondaEnvsForm`.
* Added `compas_ui.rhino.forms.FileForm`.
* Added `compas_ui.rhino.forms.FolderForm`.
* Added `compas_ui.rhino.forms.InfoForm`.
* Added `compas_ui.rhino.forms.SceneObjectsForm`.
* Added `compas_ui.rhino.forms.SearchPathsForm`.
* Added default controller for all non-system commands.
* Added `active_object` to `scene`.
* Added `use_tab` option to `compas_ui.rhino.forms.SettingsForm`.
* Added `export` and `remove` buttons to `compas_ui.rhino.forms.SceneForm`.
* Added `compas_ui.rhino.forms.ToolbarForm`.
* Added rigorous checks before installation.

### Changed

* Change on `SceneObjectsForm` is reflected realtime.
* Locked `sphinx` to `4.5`

### Removed


## [0.4.1] 2022-03-23

### Added

* Added `App.pick_file_save` and `App.pick_file_open`.

### Changed

* Use `TreeView` and `CustomCell` for `SettingsForm`.
* Changed clien size of browser form.

### Removed


## [0.4.0] 2022-03-22

### Added

* `SingletonMetaClass` for Python 3+.
* `SingletonMetaClass` for IronPython 2.7.
* `App` singleton as main entry point.
* `Scene` singleton for managing UI objects.
* `Session` singleton for managing additional session data.
* `Scene.record`, `Scene.undo`, `Scene.redo` based on copy/deepcopy.
* `Scene.save`, `Scene.saveas`, `Scene.load` based on pickle.
* `Session.record`, `Session.undo`, `Session.redo` based on JSON dumps/loads.
* `Session.save`, `Session.saveas`, `Session.load` based on JSON dump/load.
* `App.record`, `App.undo`, `App.redo` combining scene and session.
* `App.save`, `App.saveas`, `App.load` combining scene and session.
* `Object` pluggable as context-aware UI wrapper for data and artist, with support for copy/deepcopy and pickle dump/load.
* `MeshObject` as base for context-aware UI wrapper for mesh data and artist.
* `NetworkObject` as base for context-aware UI wrapper for network data and artist.
* `VolMeshObject` as base for context-aware UI wrapper for volmesh data and artist.
* `RhinoObject` as plugin for `Object` in the Rhino context.
* `RhinoMeshObject` as plugin for `MeshObject` in the Rhino context.
* `RhinoNetworkObject` as plugin for `NetworkObject` in the Rhino context.
* `RhinoVolMeshObject` as plugin for `VolMeshObject` in the Rhino context.

### Changed

### Removed


## [0.3.0] 2022-02-25

### Added

### Changed

### Removed


## [0.2.0] 2022-02-25

### Added

### Changed

### Removed


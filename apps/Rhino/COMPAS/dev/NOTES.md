# Rhino Apps

## Config

App config and settings should be in `__plugin__.py`.
This file should contain

* the plugin data required by Rhino
* environment info
* default app settings
* cloud/proxy info

## Install

```bash
cd compas_ui
python -m compas_rhino.install_plugin apps/Rhino/COMPAS
```


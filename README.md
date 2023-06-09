﻿# [COA Tools](https://github.com/ndee85/coa_tools) Importer Plugin

This plugins adds support for Synfig to import COA Tools exported content in Synfig. This is a importer plugin and works with development version only (as of July 2023).

## Features:

- Import COA Tools exported content directly in Synfig
- Imports position and offset values properly
- Arranges layers as per order
- Supports tiling features by converting into Switch Layer with all necessary tiles

## Installation:

Download the zip file, and paste it in the plugins directory ([more](https://synfig.readthedocs.io/en/latest/plugins.html#how-to-install-plugins)).

This plugin depends on Pillow library for Python. You need to manually [install](https://pillow.readthedocs.io/en/latest/installation.html) it for Synfig's python, which you need to locate based on your OS, [more details on Python installation used by Synfig](https://synfig.readthedocs.io/en/latest/plugins.html#details).

## How to use the plugin

This is a importer plugin, just import a file as normal. You need to select the JSON file, and make sure all the resources are relative to the selected JSON.

## FAQ

### I have found a problem, issue what should I do ?

Please open a new issue with necessary details.

### Plugin seems outdated, what to do ?

Please open a new issue and I will update it to the necessary changes.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'Radar simulator.',
	'author': 'Oscar Franzén',
	'url': 'URL to get Radar at.',
	'download_url': 'Where to download it.',
	'author_email': 'oscarfranzen@yahoo.se',
	'version': '0.0',
	'install_requires': ['nose', 'numpy', 'scipy', 'PyQt4', 'pyqt', 'pyqtgraph'],
	'packages': ['RADAR'],
	'scripts': [],
	'name': 'Radar'
}

setup(**config)


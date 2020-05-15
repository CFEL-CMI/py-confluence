#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 80 -*-
#
# Copyright (C) 2016,2017 Jochen Küpper <jochen.kuepper@cfel.de>
# Copyright (C) 2016,2017 Alexander Franke <alexander.franke@cfel.de>


import os
from setuptools import setup

extra_compile_args = []
library_dirs = []

long_description = """CMI Confluence Python extensions

CFEL Controlled Molecule Imaging (CMI) tools for Atlassian Confluence.

This packages provides a few scripts to help using Confluence in a systematic
fashion; see description of the individual files below.

This package is provided as is and without any warranty included! If you have
improvements or further tools, please send a patch to the maintainer -- see
setup.py for details.

Original author:    Alexander Franke
Current maintainer: no-one (Jochen Küpper)

See the distribution files AUTHORS and README for further contributions.
"""


setup(name="py-confluence",
      author              = "Alexander Franke, Jochen Küpper",
      author_email        = "jochen.kuepper@cfel.de",
      maintainer          = "Alexander Franke",
      maintainer_email    = "alexander.franke@cfel.de",
      url                 = "https://stash.desy.de/projects/CMI/repos/py-confluence",
      description         = "CMI Confluence Python Tools",
      version             = "0.2.dev0",
      long_description    = long_description,
      license             = "GPL",
      packages            = ['confluence'],
      scripts             = ['bin/confluence_clone-space',
                             'bin/confluence_create-CMI-space',
                             'bin/confluence_example_create_blog',
                             'bin/confluence_upload_evernote'],
      install_requires    = ['requests>=2.21.0',
                             'six>=1.12.0',
                             'python-dateutil>=2.7.5',
                             'eml_parser>=1.11'],
      )

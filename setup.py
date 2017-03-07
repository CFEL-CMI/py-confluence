#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 120 -*-
#
# Copyright (C) 2016 Jochen Küpper <jochen.kuepper@cfel.de>


import os
from setuptools import setup

extra_compile_args = []
library_dirs = []

long_description = """CMI Confluence Python extensions

Original author:    Alexander Franke
Current maintainer: Alexander Franke
See the distribution files AUTHORS and THANKS for further contributions.
"""


setup(name="py-confluence",
      author              = "Jochen Küpper, Alexander Franke, CFEL-CMI group, et al (see AUTHORS)",
      author_email        = "jochen.kuepper@cfel.de",
      maintainer          = "Jochen Küpper and the CFEL-CMI group",
      maintainer_email    = "jochen.kuepper@cfel.de",
      url                 = "http://confluence.desy.de",
      description         = "CMI Confluence Python Tools",
      version             = "0.1.dev0",
      long_description    = long_description,
      license             = "GPL",
      packages            = ['confluence'],
      scripts             = ['bin/confluence_create_CMI_space',
                             'bin/confluence_static_archive'],
      )

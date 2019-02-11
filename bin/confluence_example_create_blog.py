#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 120 -*-
#
# Copyright (C) 2018 Alexander Franke

from confluence import *

blog = Blogpost("username", "password", "spacekey")
blog.title = "Blogtitle"
blog.labels = "label1,label2"
blog.attachments = "/tmp/untitled.html"
blog.publish()

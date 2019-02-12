#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 120 -*-
#
# Copyright (C) 2018 Alexander Franke

from confluence import *

# create a new blog post
confluence = Confluence(username="USERNAME", password="PASSWORD")
blog = Blogpost(confluence)
blog.title = "Blogtitle"
blog.labels = "label1,label2"
blog.attachments = "/tmp/untitled.html"
blog.spacekey = "SPACEKEY"
blog.publish()


# get a page from the server and modify it
page = Page(confluence, content_id="CONTENTID")
print(page)
page.labels = "newlabelforpage"
page.update()

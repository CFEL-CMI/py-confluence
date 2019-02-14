#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 120 -*-
#
# Copyright (C) 2018 Alexander Franke

from confluence import *

# create a new blog post
confluence = Confluence("USERNAME", "PASSWORD")
blog = Blogpost(confluence)
blog.title = "Blogtitle"
blog.labels = "label1,label2"
blog.attachments = "/tmp/untitled.html"
blog.spacekey = "SPACEKEY"
blog.date = "2019-01-01"
blog.publish()


# get a page from the server (known content_id) and modify it. In this example labels are added.
# Please note the usage of update() and not publish()
page = Page(confluence, content_id="CONTENTID")
print(page)
page.labels = "newlabelforpage"
page.update()

# to change the default server address you may use the kwarg "url". This might be useful for testing
confluence2 = Confluence("USERNAME", "PASSWORD", url="https://myserverurl.de")

# read from eml file
blogfromeml = Blogpost(confluence)
blogfromeml.read_eml("pathToEmlFile")
blogfromeml.spacekey = "SPACEKEY"
blogfromeml.publish()

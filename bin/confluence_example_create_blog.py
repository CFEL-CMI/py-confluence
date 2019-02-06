#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 120 -*-
#
# Copyright (C) 2018 Alexander Franke

from confluence import connector

confluence = connector.Confluence(
    username='USERNAME e.g. afrank or jkuepper',
    password='password'
)

newblog = confluence.create_blog_post(
    space='~afrank',
    title='testblog with label33',
    body='This is the body. You can use <strong>HTML tags</strong>!'
)

labels = confluence.set_blog_post_label(newblog["id"], "testlabel")



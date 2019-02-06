#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 120 -*-
#
# Copyright (C) 2018 Alexander Franke

from confluence import connector

confluence = connector.Confluence(
    url='http://134.100.104.244:8090',
    username='admin',
    password='admin')

status = confluence.create_blog_post(
    space='DS',
    title='Testtitle',
    body='This is the body. You can use <strong>HTML tags</strong>!')

print(status)


#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 100 -*-


import requests, json
import os
import sys
import datetime
import string
import getpass
import xmlrpc
import xmlrpc.client

class Confluence(url,username):
	
	def login():
		print ("Please enter your password  (user:" + user+")")
	    pwd = getpass.getpass()
	    srv = getServerProxy(serverurl)
	    token   = auth(user,srv,pwd)

	def getToken(user,srv,pwd):
    """Try to logout from server in case any previous connection is still open. Finally login and return authentification token."""
    try:
        srv.confluence2.logout(token)
    finally:
        return srv.confluence2.login(user, pwd)

	def getServerProxy(serverurl):
    	return xmlrpc.client.ServerProxy(serverurl+'rpc/xmlrpc')

    def getWritableSpaces(srv):
    	srv.


	def printResponse(r):
   		print ('{} {}\n'.format(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': ')), r))

class ConfluenceContent(Confluence):
	def setTitle():

	def setLabels():

	def setContent():

	def setPermissions():

class ConfluenceBlogpost(ConfluenceContent):
	#Date cannot be in the future
	def setDate():
	def publish():


class ConfluencePage(ConfluenceContent):
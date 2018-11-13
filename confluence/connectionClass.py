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
	def __init__(self,username):
		self.serverurl = self.getServerurl()
		self.username = username
		self.token = self.login(username)

	'''void setUser(string username), set a new user by the username NOT fullname'''
	def setUser(username):
		self.username = username

	'''string getUser(), return the current user as a string'''
	def getUser():
		return self.username

	'''string getServerUrl(), return serverurl, currently fixed to our confluence.desy.de instance. There is not setServerUrl currently'''
	def getServerurl():
		return "https://confluence.desy.de"

	'''token login(string username), asks to input a password. This method should only be called if not valid token is present'''
	def login(username):
		print ("Please enter your password  (user:" + username+")")
		pwd = getpass.getpass()
		srv = self.getServerProxy(serverurl)
		token   = self.getToken(user,srv,pwd)
		return token

	#def checkIfValidtoken(token):

	'''token getToken(string user,string srv,password pwd),executed from login(username)'''
	def getToken(user,srv,pwd):
		"""Try to logout from server in case any previous connection is still open. Finally login and return authentification token."""
		"""check if token is valid"""
		try:
			srv.confluence2.logout(token)
		finally:
			return srv.confluence2.login(user, pwd)

	def getServerProxy(serverurl):
		return xmlrpc.client.ServerProxy(serverurl+'rpc/xmlrpc')

	def getWritableSpaces():
		srv = self.getServerProxy(serverurl)
		readablespaces =  readConfluenceResponse(srv.confluence2.getSpaces())
	
	#helper function 
	def readConfluenceResponse(r):
		print ('{} {}\n'.format(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': ')), r))

class ConfluenceContent(Confluence):
	def __init__(self,title,labels,content,permissions):
		self.title = title 
		self.labels = labels #this is a list
		if (checkIfContentValid(content)):
			self.content = content
		else ThrowError("Content not in valid format")
		self.content = content #make sure this is 

	def checkIfContentValid(content):


	def getTitle():
		return self.title
	def setTitle(title):
		self.title = title
	def setLabels():

	def setContent():

	def ThrowError():#there is surely a better way.
	def setPermissions():
	def setSpace():
		#store space key and have a change class for space key
	
	def saveConfluenceContent(srv,token,id):
		"""saveConfluenceContent

		returns the content of the given id in plain html wrapped by a <div>
		"""
		parameter = {}
		parameter['style'] = 'clean'
		return srv.confluence2.renderContent(token,'',id,'',parameter)

	def html_escape(text):
	# escape() and unescape() takes care of &, < and >.
	html_escape_table = {
		'"': "&quot;",
		"'": "&apos;"
	}
	return escape(text, html_escape_table)

class ConfluenceBlogpost(ConfluenceContent):
	#Date cannot be in the future, we need to check for that
	def setDate():
	def publish():
		#pubish, get blog id, set labels, set permissions and return link / blog post id


	def getCurrentDate():



class ConfluencePage(ConfluenceContent):
	def publish():
		#pubish, get blog id, set labels, set permissions and return link / blog post id
		

	def getCurrentDate():


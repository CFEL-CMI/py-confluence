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
import html

class Confluence:
    def __init__(self,username):
        self.serverUrl = self.get_serverurl()
        self.username = username
        self.token = self.login()
        self.srv = self.get_serverproxy()


    '''void setUser(string username), set a new user by the username NOT fullname'''
    def set_user(self,username):
        self.username = username
        #refresh token
        self.token = self.login()

    '''string getUser(), return the current user as a string'''
    def get_user(self):
        return self.username

    '''string getServerUrl(), return serverurl, currently fixed to our confluence.desy.de instance. There is not setServerUrl currently'''
    def get_serverurl():
        return "https://confluence.desy.de"

    '''token login(string username), asks to input a password. This method should only be called if not valid token is present'''
    def login(self):
        print ("Please enter your password  (user:" + self.username+")")
        pwd = getpass.getpass()
        return self.get_token(self.username,pwd)

    #def checkIfValidtoken(token):

    '''token getToken(string user,string srv,password pwd),executed from login(username)'''
    def get_token(self,user,pwd):
        """Try to logout from server in case any previous connection is still open. Finally login and return authentification token."""
        """check if token is valid"""
        try:
            self.srv.confluence2.logout(self.token)
        finally:
            return self.srv.confluence2.login(user, pwd)

    def get_serverproxy(self):
        return xmlrpc.client.ServerProxy(self.serverUrl+'rpc/xmlrpc')

    def get_writablespaces(self):
        readablespaces =  self.read_confluence_response(self.srv.confluence2.getSpaces())

    #helper function
    def read_confluence_response(self,r):
        return ('{} {}\n'.format(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': ')), r))

class ConfluenceContent(Confluence):
    def __init__(self,title,labels,content,permissions,spacekey):
        self.title = title
        self.labels = labels #this is a list
        self.spacekey = spacekey
        self.permissions = permissions
        if self.checkIfContentValid(content):
            self.content = content
        else:
            self.throw_error('Content not in valid format')

    def checkIfContentValid(self,content):
        return True

    # string getTitle(), returns current title
    def get_title(self):
        return self.title

    def set_title(self,title):
        self.title = title

    def set_labels():

    def setContent():

    def throw_error(message):
    def set_permissions():
        return 0
    def set_space(self,spacekey):
        self.spacekey = spacekey

    def get_confluence_content(self,id):
        """get_confluence_content

        returns the content of the given id in plain html wrapped by a <div>
        """
        parameter = {}
        parameter['style'] = 'clean'
        return self.srv.confluence2.renderContent(self.token,'',id,'',parameter)

    def html_escape(text):
        # escape() and unescape() takes care of &, < and >.
        html_escape_table = {
            '"': "&quot;",
            "'": "&apos;"
        }
        return html.escape(text, html_escape_table)

class ConfluenceBlogpost(ConfluenceContent):
    #Date cannot be in the future, we need to check for that
    def set_date(self):
    def publish(self):

        #pubish, get blog id, set labels, set permissions and return link / blog post id


    def get_date(self):



class ConfluencePage(ConfluenceContent,):
    def publish(self):
        #pubish, get blog id, set labels, set permissions and return link / blog post id


    def get_date(self):


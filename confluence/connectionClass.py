#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 100 -*-


import requests, json
import html


class Confluence:
    def __init__(self,username,pwd):
        self.serverUrl = self.get_serverurl()
        self.username = username
        self.pwd = pwd


    '''void setUser(string username), set a new user by the username NOT fullname'''
    def set_user(self, username):
        self.username = username

    def set_pwd(self, pwd):
        self.pwd = pwd

    '''string getUser(), return the current user as a string'''
    def get_user(self):
        return self.username

    '''string getServerUrl(), return serverurl, currently fixed to our confluence.desy.de instance. There is not setServerUrl currently'''
    def get_serverurl():
        return "https://confluence.desy.de"

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

    # set_title(string)
    def set_title(self,title):
        self.title = title

    # set_labels(string)
    # requires comma separated list of labels and sets them as a python list
    def set_labels(self, labels):
        self.labels = labels.split(",")

    def get_labels(self):
        return self.labels

    def set_content(self, content):
        self.content = content

    def throw_error(self,message):
        return

    def set_permissions():
        return

    def set_space(self,spacekey):
        self.spacekey = spacekey

    def get_confluence_content(self,id):
        """get_confluence_content

        returns the content of the given id in plain html wrapped by a <div>
        """
        parameter = {}
        parameter['style'] = 'clean'
        #TODO this has to be rewritter in rest api
        return self.srv.confluence2.renderContent(self.token,'',id,'',parameter)

    def html_escape(text):
        # escape() and unescape() takes care of &, < and >.
        html_escape_table = {
            '"': "&quot;",
            "'": "&apos;"
        }
        return html.escape(text, html_escape_table)

    def publish_labels(self, page_id):
        return

    def publish_permissions(self, page_id):
        return


class ConfluenceBlogPost(ConfluenceContent):
    # Date cannot be in the future, we need to check for that
    def set_date(self):
        return
    #TODO add the ability to set a date.
    # publish, get blog id, set labels, set permissions and return link / blog post id

    def publish(self):
        page_data = {'type': 'blogpost', 'body': {'storage': {'value': self.content, 'representation': 'storage'}}}
        r = requests.post(self.serverUrl + '/rest/api/content',
                          data=json.dumps(page_data),
                          auth=(self.username, self.pwd),
                          headers=({'Content-Type': 'application/json'})).json()

        page_id = r.id
        self.publish_labels(page_id)
        self.publish_permissions(page_id)
        return self.read_confluence_response(r)


class ConfluencePage(ConfluenceContent):
    # publish, get blog id, set labels, set permissions and return link / blog post id
    def publish(self):
        page_data = {'type': 'page', 'body': {'storage': {'value': self.content, 'representation': 'storage'}}}
        r = requests.post(self.serverUrl + '/rest/api/content',
                          data=json.dumps(page_data),
                          auth=(self.username, self.pwd),
                          headers=({'Content-Type': 'application/json'})).json()

        page_id = r.id
        self.publish_labels(page_id)
        self.publish_permissions(page_id)
        return self.read_confluence_response(r)

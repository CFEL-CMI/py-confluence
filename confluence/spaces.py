#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 100 -*-


import requests, json
import os
import sys
import string
import getpass
import xmlrpc
import xmlrpc.client


def auth(user,srv,pwd):
    """Try to logout from server in case any previous connection is still open. Finally login and return authentification token."""
    try:
        srv.confluence2.logout(token)
    finally:
        return srv.confluence2.login(user, pwd)



def xmlrpcServer(serverurl):
    return xmlrpc.client.ServerProxy(serverurl+'rpc/xmlrpc')

def printResponse(r):
    print ('{} {}\n'.format(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': ')), r))

def addReadPermissions(token,srv,entity,spacekey):
    """Adds the permission VIEWSPACE to a given entity (String of a confluence group or user)"""
    srv.confluence2.addPermissionToSpace(token,"VIEWSPACE",entity,spacekey)

def addWritePermissions(token,srv,entity,spacekey):
    """Adds the permissions VIEWSPACE,EDITSPACE,COMMENT,CREATEATTACHMENT,EDITBLOG to a given entity (String of a confluence group or user)"""
    permissions = ['VIEWSPACE','EDITSPACE','COMMENT','CREATEATTACHMENT','EDITBLOG']
    for perm in permissions:
        srv.confluence2.addPermissionToSpace(token,perm,entity,spacekey)

def addAdminPermissions(token,srv,entity,spacekey):
    """Adds the administration permission to a given entity (String of a confluence group or user)"""
    permissions = ['VIEWSPACE','SETSPACEPERMISSIONS','EDITSPACE','COMMENT','REMOVECOMMENT','CREATEATTACHMENT','REMOVEATTACHMENT','EDITBLOG','REMOVEPAGE','REMOVEBLOG','EXPORTSPACE','SETPAGEPERMISSIONS']
    for perm in permissions:
        srv.confluence2.addPermissionToSpace(token,perm,entity,spacekey)

def createCMISpace(serverurl, user, spacekey, spacename, reads,writes,admins):
    """Creates a new space (required spacekey, name), sets the homepage according to the CMI template and sets space categories **cfel-cmi** and **cmi-elog-calendar**"""

    # Get Authentification Token
    print ("Please enter your password  (user:" + user+")")
    pwd = getpass.getpass()

    srv = xmlrpcServer(serverurl)
    token   = auth(user,srv,pwd)

    # Content for homepage
    content = '<ac:layout><ac:layout-section ac:type="two_equal"><ac:layout-cell><ac:structured-macro ac:name="info"><ac:parameter ac:name="title">Overview</ac:parameter><ac:rich-text-body><p>This is the Confluence Space (Wiki, logbook, etc.) of the project '+spacename+'.</p></ac:rich-text-body></ac:structured-macro></ac:layout-cell>'
    content +='<ac:layout-cell><p><br /><ac:structured-macro ac:name="livesearch"><ac:parameter ac:name="additional">page excerpt</ac:parameter><ac:parameter ac:name="placeholder">Search space</ac:parameter><ac:parameter ac:name="'+spacekey+'">com.atlassian.confluence.content.render.xhtml.model.resource.identifiers.SpaceResourceIdentifier@35</ac:parameter><ac:parameter ac:name="spaceKey"><ri:space ri:space-key="'+spacekey+'" /></ac:parameter></ac:structured-macro></p></ac:layout-cell></ac:layout-section>'
    content +='<ac:layout-section ac:type="single"><ac:layout-cell><ac:structured-macro ac:name="info"><ac:parameter ac:name="title">Members of the project (Confluence Space permissions)</ac:parameter><ac:rich-text-body><ac:macro ac:name="spaceaccessusersminimal" /></ac:rich-text-body></ac:structured-macro></ac:layout-cell></ac:layout-section>'
    content +='<ac:layout-section ac:type="two_equal"><ac:layout-cell><h2>Recent space activity</h2><p><ac:structured-macro ac:name="recently-updated"><ac:parameter ac:name="spaces"><ri:space ri:space-key="'+spacekey+'" /></ac:parameter><ac:parameter ac:name="max">5</ac:parameter><ac:parameter ac:name="hideHeading">true</ac:parameter><ac:parameter ac:name="theme">social</ac:parameter><ac:parameter ac:name="types">page, comment, blogpost</ac:parameter></ac:structured-macro></p>'
    content +='<hr /><h2>Hot topics</h2><p><ac:structured-macro ac:name="popular-labels"><ac:parameter ac:name="style">heatmap</ac:parameter><ac:parameter ac:name="count">35</ac:parameter><ac:parameter ac:name="'+spacekey+'">com.atlassian.confluence.content.render.xhtml.model.resource.identifiers.SpaceResourceIdentifier@35</ac:parameter><ac:parameter ac:name="spaceKey"><ri:space ri:space-key="'+spacekey+'" /></ac:parameter></ac:structured-macro></p>'
    content +='<h2>All labels in this space</h2><p><ac:structured-macro ac:name="listlabels"><ac:parameter ac:name="'+spacekey+'">com.atlassian.confluence.content.render.xhtml.model.resource.identifiers.SpaceResourceIdentifier@35</ac:parameter><ac:parameter ac:name="spaceKey"><ri:space ri:space-key="'+spacekey+'" /></ac:parameter></ac:structured-macro></p></ac:layout-cell>'
    content +='<ac:layout-cell><h2>Space contributors</h2><p><ac:structured-macro ac:name="contributors-summary"><ac:parameter ac:name="spaces"><ri:space ri:space-key="'+spacekey+'" /></ac:parameter></ac:structured-macro></p></ac:layout-cell></ac:layout-section>'
    content +='<ac:layout-section ac:type="single"><ac:layout-cell><h2>Incomplete tasks</h2><p><ac:structured-macro ac:name="tasks-report-macro"><ac:parameter ac:name="spaces">'+spacekey+'</ac:parameter><ac:parameter ac:name="spaceAndPage">space:'+spacekey+'</ac:parameter><ac:parameter ac:name="pageSize">40</ac:parameter></ac:structured-macro></p></ac:layout-cell></ac:layout-section></ac:layout>'

    # Create new space
    print ('----------------------------------------------------------------')
    print ('                  ')
    print ('Creating new space')


    r = requests.post(serverurl+'rest/api/space',
        data=json.dumps({'key' : spacekey, 'name':spacename,"description": {"plain": {"value": "CMI space","representation": "plain" }},"metadata": {}}),
        auth=(user, pwd),
        headers=({'Content-Type':'application/json'}))
    printResponse(r)
    print ('                  ')
    print ('                  ')
    print ('----------------------------------------------------------------')

    # Add labels (categories)
    srv.confluence2.addLabelByNameToSpace(token,"team:cfel-cmi",spacekey)
    srv.confluence2.addLabelByNameToSpace(token,"team:cmi-elog-calendar",spacekey)

    # Get information about newly created space
    newspace   = srv.confluence2.getSpace(token,spacekey)

    # Get content ID of homepage of the space
    homepageid = newspace["homePage"]
    print(homepageid)
    r = requests.put(serverurl+'rest/api/content/'+homepageid,
        data=json.dumps({ "version": {"number": 2 },"title":spacename+ " Home", "type": "page","body": {"storage": {"value": content,"representation": "storage" }}}),
        auth=(user, pwd),
        headers=({'Content-Type':'application/json'}))
    #print(str(r))
    #printResponse(r)


    #add link to space overview page
    print ('------------------------------')
    print ('                  ')
    print ('    Updating Spaceoverview    ')

    r = requests.get(serverurl+'rest/api/content/14421128',
        params={'expand' : 'body.storage,version'},
        auth=(user, pwd))
    content = r.json()['body']['storage']['value']
    versionnumber = int(r.json()['version']['number']) + 1
    print("version number:")
    print (versionnumber)
    r = requests.put(serverurl+'rest/api/content/14421128',
        data=json.dumps({'type':'page', "version": {"number": str(versionnumber)}, "title":"Spaces/Projects/Stashs with relevance to CMI", 'body':{'storage':{'value':content[:-49]+'<ul><li><a href="/display/'+spacekey+'">'+spacename+'</a></li></ul></ac:layout-cell></ac:layout-section></ac:layout>','representation':'storage'}}}),
        auth=(user, pwd),
        headers=({'Content-Type':'application/json'}))
    print ('                  ')
    print ('       Response:          ')
    print (r.json())
    print ('                  ')
    print ('------------------------------')


    # Add permissions
    for entity in reads:
            addReadPermissions(token,srv,entity,spacekey)
    for entity in writes:
            addWritePermissions(token,srv,entity,spacekey)
    for entity in admins:
            addAdminPermissions(token,srv,entity,spacekey)

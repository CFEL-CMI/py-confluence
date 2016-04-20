#!/usr/bin/python3

import os
import sys
import string
import getpass
import xmlrpc
import xmlrpc.client

# https://developer.atlassian.com/confdev/confluence-rest-api/confluence-xml-rpc-and-soap-apis/remote-confluence-methods

def auth(user,pwd,srv):
	try:
		srv.confluence2.logout(token)
	finally:
		return srv.confluence2.login(user, pwd)

"""docstring for confluence_create_CMI_space"""
def createCMISpace(servername,user,spacekey,spacename):
	
	content = '<ac:layout><ac:layout-section ac:type="two_equal"><ac:layout-cell><ac:structured-macro ac:name="info"><ac:parameter ac:name="title">Overview</ac:parameter><ac:rich-text-body><p>This is the Confluence Space (Wiki, logbook, etc.) of the project '+spacename+'.</p></ac:rich-text-body></ac:structured-macro></ac:layout-cell>'
	content +='<ac:layout-cell><p><br /><ac:structured-macro ac:name="livesearch"><ac:parameter ac:name="additional">page excerpt</ac:parameter><ac:parameter ac:name="placeholder">Search space</ac:parameter><ac:parameter ac:name="'+spacekey+'">com.atlassian.confluence.content.render.xhtml.model.resource.identifiers.SpaceResourceIdentifier@35</ac:parameter><ac:parameter ac:name="spaceKey"><ri:space ri:space-key="'+spacekey+'" /></ac:parameter></ac:structured-macro></p></ac:layout-cell></ac:layout-section>'
	content +='<ac:layout-section ac:type="single"><ac:layout-cell><ac:structured-macro ac:name="info"><ac:parameter ac:name="title">Members of the project (Confluence Space permissions)</ac:parameter><ac:rich-text-body><ac:macro ac:name="spaceaccessusersminimal" /></ac:rich-text-body></ac:structured-macro></ac:layout-cell></ac:layout-section>'
	content +='<ac:layout-section ac:type="two_equal"><ac:layout-cell><h2>Recent space activity</h2><p><ac:structured-macro ac:name="recently-updated"><ac:parameter ac:name="spaces"><ri:space ri:space-key="'+spacekey+'" /></ac:parameter><ac:parameter ac:name="max">5</ac:parameter><ac:parameter ac:name="hideHeading">true</ac:parameter><ac:parameter ac:name="theme">social</ac:parameter><ac:parameter ac:name="types">page, comment, blogpost</ac:parameter></ac:structured-macro></p>'
	content +='<hr /><h2>Hot topics</h2><p><ac:structured-macro ac:name="popular-labels"><ac:parameter ac:name="style">heatmap</ac:parameter><ac:parameter ac:name="count">35</ac:parameter><ac:parameter ac:name="'+spacekey+'">com.atlassian.confluence.content.render.xhtml.model.resource.identifiers.SpaceResourceIdentifier@35</ac:parameter><ac:parameter ac:name="spaceKey"><ri:space ri:space-key="'+spacekey+'" /></ac:parameter></ac:structured-macro></p>'
	content +='<h2>All labels in this space</h2><p><ac:structured-macro ac:name="listlabels"><ac:parameter ac:name="'+spacekey+'">com.atlassian.confluence.content.render.xhtml.model.resource.identifiers.SpaceResourceIdentifier@35</ac:parameter><ac:parameter ac:name="spaceKey"><ri:space ri:space-key="'+spacekey+'" /></ac:parameter></ac:structured-macro></p></ac:layout-cell>'
	content +='<ac:layout-cell><h2>Space contributors</h2><p><ac:structured-macro ac:name="contributors-summary"><ac:parameter ac:name="spaces"><ri:space ri:space-key="'+spacekey+'" /></ac:parameter></ac:structured-macro></p></ac:layout-cell></ac:layout-section>'
	content +='<ac:layout-section ac:type="single"><ac:layout-cell><h2>Incomplete tasks</h2><p><ac:structured-macro ac:name="tasks-report-macro"><ac:parameter ac:name="spaces">'+spacekey+'</ac:parameter><ac:parameter ac:name="spaceAndPage">space:'+spacekey+'</ac:parameter><ac:parameter ac:name="pageSize">40</ac:parameter></ac:structured-macro></p></ac:layout-cell></ac:layout-section></ac:layout>'
	# Get Authentification Token
	print ("Please enter the password for User " + user)
	pwd     = getpass.getpass()
	srv     = xmlrpc.client.ServerProxy(servername+'rpc/xmlrpc')
	token   = auth(user,pwd,srv)

	#create new space
	newspace = {'name':spacename,'type': 'global', 'key': spacekey}
	srv.confluence2.addSpace(token,newspace)
	srv.confluence2.addLabelByNameToSpace(token,"team:cfel-cmi",spacekey)
	srv.confluence2.addLabelByNameToSpace(token,"team:cmi-elog-calendar",spacekey)

	#get information about newly created space
	newspace   = srv.confluence2.getSpace(token,spacekey) 
	#get content ID of homepage of the space
	homepageid = newspace["homePage"]

	#get Page object for homePage
	homepage = srv.confluence2.getPage(token, homepageid)

	#set new content according to tempate defined above
	homepage["content"] = content

	#upload content to server
	srv.confluence2.updatePage(token, homepage,{"versionComment": "updated Page according to template"})











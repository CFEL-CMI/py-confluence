#!/usr/bin/python3

# static-archive.py

# This script will generate a local and readable
# HTML backup of a Confluence space within a new folder 

import os
import datetime
import time
import json
import xmlrpc
import xmlrpc.client
from collections import defaultdict
from collections import OrderedDict

import sys
import string
import getpass
from pprint import pprint


# settings
# Url to the Server. Please include a / after the url
servername     = input("Server address with trailing /         [default: https://confluence.desy.de/]:  ") or "https://confluence.desy.de/"
user           = input("Please enter your Username. You need access to all pages! [default: jkuepper]:  ") or "jkuepper"
sk             = input("Please enter the spacekey of the space you want to copy to your computer     :  ")
downloadPages  = True
downloadBlog   = True
downloadAttach = True


# Get Authentification Token
def auth(user,pwd,srv):
	try:
		srv.confluence2.logout(token)
	finally:
		return srv.confluence2.login(user, pwd)

def getSpaceInfo(token,sk):
	return srv.confluence2.getSpace(token,sk)

#returns the content of the given id in plain html wrapped by a <div>
def saveConfluenceContent(token,id):
	parameter = {}
	parameter['style'] = 'clean'
	return srv.confluence2.renderContent(token,'',id,'',parameter)

def recursivePagetreeHTML(parents,i):
	html = ""
	for ele in parents[i]:
		#get element information
		elehtml = srv.confluence2.getPage(token,ele)

		#root element is visible
		if i == "0":
			html +=  '<ul id="'+elehtml["id"]+'"><li>'
		#every subpage is not
		else:
			html += '<ul id="'+elehtml["id"]+'" style="display:none"><li>'

		
		#if current element has children 
		if ele in parents:
			html += '<a class="arrow" onclick="showChildren(this)" href="#">&rarr;</a>'
			html += '<a class="pagelink" href="'+elehtml["id"]+'.html">'+elehtml["title"]+'</a>'
			#recursively insert children
			html += recursivePagetreeHTML(parents,ele)
		#current element has no children 
		else:
			html += '<a class="dot">&middot;</a>'
			html += '<a class="pagelink" href="'+elehtml["id"]+'.html">'+elehtml["title"]+'</a>'

		html += "</li></ul>"

	return html

def getConfAttachments(token,contentid,dirname):
	attachments = srv.confluence2.getAttachments(token,contentid)
	attachHTML = ""
	if attachments:
		attachHTML+= '<div style="background-color: #DDD; border: 1px silver ridge; padding: 5px;"><b>Attachments</b><ul>'
		for attachment in attachments:
			os.mkdir(dirname + '/attachments/' + contentid)
			attachPath = '/attachments/'+ contentid+'/'+attachment["fileName"]
			with open(os.path.join(script_dir, dirname+ attachPath),"wb") as out_file:
				print('Downloading '+attachment["fileName"]+' for contentid '+contentid)
				attbytes = srv.confluence2.getAttachmentData(token,contentid,attachment["fileName"],"0").data
				out_file.write(attbytes)
			attachHTML+='<li><a href="..'+attachPath+'">'+attachment["fileName"]+'</a></li>'
		attachHTML +='</ul></div>'
	return attachHTML


print ("Please enter the password for User " + user)
pwd     = getpass.getpass()
srv     = xmlrpc.client.ServerProxy(servername+'rpc/xmlrpc')
token   = auth(user,pwd,srv)

script_dir = os.path.dirname(__file__)

dirname = 'Conf_'+sk+'_'+str(datetime.datetime.now())
os.mkdir(dirname)
os.mkdir(dirname+'/assets')

#Get space info
spaceinfo = getSpaceInfo(token,sk)
if "description" in spaceinfo:
	description = spaceinfo["description"]
else:
	description = ""

print('Saving Space ' + spaceinfo["name"])

#home page id and newest blog id
homepage = spaceinfo["homePage"]
lastblog = srv.confluence2.search(token,"type = blogpost AND spacekey="+sk,1)
lastblog = lastblog[0]["id"]

#save css
with open(os.path.join(script_dir, dirname+'/assets/main.css'), "wt",encoding="utf-8") as css:
	css.write('.blogtree a, .blogtree a:link { color: seashell;}#sidebar object{position:absolute;height:100%;width:100%}#gotospan{padding:2px 10px; border:1px #83B7D9 solid; color:seashell!important} #sidebar{position:fixed;top:0;bottom:0;left:0;overflow:scroll; width:20em;background-color:#404040}#sidebarheader{background-color:#2980B9; padding:10px 20px; text-align:center;}.blogtree{color:#2980B9} li.active > a { color: Crimson}#sidebar::-webkit-scrollbar { display: none;} html,body{font-family:sans-serif; margin:0; padding:0;height:100%}.pagetree{color:seashell} a,a:link{text-decoration:none; color:Crimson}a:hover{text-decoration:underline}#pagetree ul{list-style-type: none}a.pagelink:hover,.arrow:hover{text-decoration: underline}a.arrow, a.dot{font-family: monospace; font-size: 20px;text-decoration: none; color:seashell} a.pagelink{color: seashell; padding-left: 5px;text-decoration:none}.confluenceTable{border-collapse:collapse;}.confluenceTh, .confluenceTd {    border: 1px solid #ddd; padding: 7px 10px; vertical-align: top; text-align: left;}.confluenceTh{background-color:#f0f0f0;}')
#save scripts
with open(os.path.join(script_dir, dirname+'/assets/main.js'), "wt",encoding="utf-8") as js:
	js.write('function findUpTag(n,e){for(;n.parentNode;)if(n=n.parentNode,n.tagName===e)return n;return null} function showChildren(ele){var children=ele.parentElement.childNodes; for (var i=0; i < children.length; i++){if (children[i].nodeName.toLowerCase()=="ul"){children[i].style.display="block";}}ele.setAttribute("onclick","hideChildren(this)"); ele.innerHTML="&darr;";}function hideChildren(ele){var children=ele.parentElement.childNodes; for (var i=0; i < children.length; i++){if (children[i].nodeName.toLowerCase()=="ul"){children[i].style.display="none";}}ele.setAttribute("onclick","showChildren(this)"); ele.innerHTML="&rarr;";}function openTree(){var e=document.body.getAttribute("pageid"),t=document.getElementById(e);for(t.firstElementChild.children.length>2&&showChildren(t.firstElementChild.firstElementChild),t.firstElementChild.className+=" active";findUpTag(t,"UL");)showChildren(findUpTag(t,"UL").firstElementChild.firstElementChild),t=findUpTag(t,"UL")}')

if downloadAttach:
	os.mkdir(dirname+'/attachments')

if downloadPages:
	print('Saving pages')
	os.mkdir(dirname+'/pages')

	#get all pageIDs
	pages = srv.confluence2.getPages(token,sk)
	pagescount = str(len(pages))
	print(pagescount+ " pages found.")
	print('Generating page tree. Might take some time...')
	parents = defaultdict(list)

	for page in pages:
		pagemeta = srv.confluence2.getPage(token,page["id"])
		parents[pagemeta["parentId"]].append(page["id"])

	pagetreeHTML = recursivePagetreeHTML(parents,"0")

	for count, page in enumerate(pages, start=1):

		pagepath = dirname+'/pages/'+page["id"]+'.html'
		comments = srv.confluence2.getComments(token,page["id"])
		commentHTML =""
		#print(comments)
		for comment in comments:
			commentHTML += "<div><hr><h4>"+comment["creator"]+'</h4><p><i>'+str(comment["created"])+'</i></p>'+comment["content"]
		pagemeta = srv.confluence2.getPage(token,page["id"])
		anchestors = srv.confluence2.getAncestors(token,page["id"])
		anchestorsJS = ""
		for anchestor in anchestors:
			anchestorsJS += anchestor["id"] + ','
		anchestorsJS = anchestorsJS[:-1]

		#downloading Attachments of page
		attachHTML = ""
		if downloadAttach:
			attachHTML = getConfAttachments(token,page["id"],dirname)
			

		with open(os.path.join(script_dir, pagepath), "wt",encoding="utf-8") as out_file:
			print("("+str(count)+"/"+pagescount+") writing page "+ page["id"])
			pageheader = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>'+page["title"]+'</title><script language="javascript" type="text/javascript" src="../assets/main.js"></script><link rel="stylesheet" href="../assets/main.css"></head>'
			pageheader += '<body onload="openTree()" pageid="'+page["id"]+'"><div id="sidebar"><div id="sidebarheader"><div><h3>Local copy of Confluence Space<br><i>'+spaceinfo["name"]+'</i></h3><p><i>saved '+str(datetime.datetime.today())+'</i></p></div><div><a href="../blogs/'+lastblog+'.html"><span id="gotospan">go&nbsp;to&nbsp;blog</span></a></div></div><div id="pagetree" style="padding:0 10px;"><h3 style="color:Crimson">PAGES</h3>'+pagetreeHTML+'</div></div><div style="float:left; padding: 0px 30px; height:100%; padding-left:22em;"> <h1>'+page["title"]+' (<a href="'+page["url"]+'">Origin</a>)</h1>'+'<h5>Published '+str(pagemeta["created"])[0:4]+'-'+str(pagemeta["created"])[4:6]+'-'+str(pagemeta["created"])[6:8]+' '+str(pagemeta["created"])[9:]+' by '+pagemeta["creator"]+'</h5>'
			pagefooter = '</div></body></html>'
			#modify links within pagehtml
			contenthtml = saveConfluenceContent(token,page["id"]).replace('="/download/attachments','="../attachments')
			contenthtml = contenthtml.replace('/pages/viewpage.action\?pageId=([1-9]*)','../pages/\1.html')
			out_file.write(pageheader+attachHTML+contenthtml+commentHTML+pagefooter)





if downloadBlog:
	print('Saving blog')
	os.mkdir(dirname+'/blogs')
	blogs = srv.confluence2.getBlogEntries(token,sk)
	
	blogscount = str(len(blogs))
	print(blogscount+ " blog posts found.")
	print("creating sorted blog tree.")

	monthnames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	blogtreeHTML = '<!DOCTYPE html><html><head><meta charset="UTF-8"><base target="_parent" /><link rel="stylesheet" href="../assets/main.css"><script language="javascript" type="text/javascript" src="../assets/main.js"></script><title>blogtree</title></head><body><div id="sidebar"><div id="sidebarheader"><div><h3>Local copy of Confluence Space<br><i>'+spaceinfo["name"]+'</i></h3><p><i>saved '+str(datetime.datetime.today())+'</i></p></div><div><a target href="../pages/'+spaceinfo["homePage"]+'.html"><span id="gotospan">go&nbsp;to&nbsp;pages</span></a></div></div><div style="padding:0 10px;"><h3 style="color:Crimson">BLOG</h3><table class="blogtree" style="width:100%">'
	#create a defaultdict with keys 201510,201509,2014111 etc for every month. Insert every blog resp. as value
	yearmonthDict = defaultdict(list)	
	for blog in blogs:
		yearmonthDict[str(blog["publishDate"])[0:6]].append(blog) #fill default dict
	#sort months
	yearmonthDictSrt = OrderedDict(sorted(yearmonthDict.items()))
	yearmonthDictSrtIt = list(yearmonthDictSrt.items())
	yearmonthDictSrtIt.reverse()
	#iterate over every year/month combination and sort the blogs with OrderedDict
	for yearmonth,yearmonthEntry in yearmonthDictSrtIt:
		#create dict for sorting
		usrtBlogs = dict()
		for blog in yearmonthEntry:
			usrtBlogs[str(blog["publishDate"])] = blog
		#sorted dict of all blogs. Key is publish date, value is blog 	
		srtBlogs = OrderedDict(sorted(usrtBlogs.items()))
		srtBlogsIt = list(srtBlogs.items())
		srtBlogsIt.reverse()
		#finally output sorted html for every month
		blogtreeHTML += '<tr><th colspan="2">'+monthnames[int(yearmonth[4:6])-1] +' '+ yearmonth[0:4]+'</th></tr>'
		for blogdate, blog in srtBlogsIt:
			blogtreeHTML += '<tr><td>'+blogdate[6:8]+'.</td><td><a href="../blogs/'+blog["id"]+'.html">'+blog["title"]+'</a></td></tr>'

	blogtreeHTML += "</table></body>"
	with open(os.path.join(script_dir, dirname+'/assets/blogtree.html'), "wt",encoding="utf-8") as out_file:
		out_file.write(blogtreeHTML)


	print("downloading blogs...")
	for count, blog in enumerate(blogs, start=1):
		blogpath = dirname+'/blogs/'+blog["id"]+'.html'
		comments = srv.confluence2.getComments(token,blog["id"])
		commentHTML =""
		#print(comments)
		for comment in comments:
			commentHTML += "<div><hr><h4>"+comment["creator"]+'</h4><p><i>'+str(comment["created"])+'</i></p>'+comment["content"]
		#downloading Attachments of page
		attachHTML = ""
		if downloadAttach:
			attachHTML = getConfAttachments(token,blog["id"],dirname)

		with open(os.path.join(script_dir, blogpath), "wt",encoding="utf-8") as out_file:
			print("("+str(count)+"/"+blogscount+") writing blog entry "+ blog["id"])
			blogheader = '<!DOCTYPE html><html><head><meta charset="UTF-8"><link rel="stylesheet" href="../assets/main.css"><script language="javascript" type="text/javascript" src="../assets/main.js"></script><title>'+blog["title"]+'</title></head><body><div id="sidebar"><object type="text/html" data="../assets/blogtree.html"></object></div><div style="float:left; padding: 0px 30px; height:100%; padding-left:22em;"> <h1>'+blog["title"]+' (<a href="'+blog["url"]+'">Origin</a>)</h1>'+'<h5>Published '+str(blog["publishDate"])[0:4]+'-'+str(blog["publishDate"])[4:6]+'-'+str(blog["publishDate"])[6:8]+' '+str(blog["publishDate"])[9:]+' by '+blog["author"]+'</h5>'
			blogfooter = '</div></body></html>'

			#modify links within html
			replacethis = '="/download/attachments'
			withthis = '="../attachments'
			contenthtml = saveConfluenceContent(token,blog["id"]).replace(replacethis,withthis)
			out_file.write(blogheader+attachHTML+contenthtml+commentHTML+blogfooter)
	



print('creating start-here page')

startpage = '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=pages/'+homepage+'.html"></head><body><p>Please visit <a href="pages/'+homepage+'.html">this page</a></p></body></html>'
with open(os.path.join(script_dir, dirname+'/start-here.html'), "a",encoding="utf-8") as out:
	out.write(startpage)

print('Backup finished successfully.')





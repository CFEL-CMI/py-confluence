#!/usr/bin/python3
from lib import static_archive

# Url to the Server. Please include a / after the url
servername     = input("Server address with trailing /         [default: https://confluence.desy.de/]:  ") or "https://confluence.desy.de/"
user           = input("Please enter your Username. You need access to all pages! [default: jkuepper]:  ") or "jkuepper"
sk             = input("Please enter the spacekey of the space you want to copy to your computer     :  ")
downloadPages  = True
downloadBlog   = True
downloadAttach = True
static_archive.startArchive(servername,user,sk,downloadPages,downloadBlog,downloadAttach)


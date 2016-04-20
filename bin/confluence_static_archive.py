#!/usr/bin/python3
"""
This script downloads....
"""
from lib import static_archive

def main():
	"""
	Main function of static_backup script. User is asked some needed information like server address and username.
	"""
	servername     = input("Server address with trailing /         [default: https://confluence.desy.de/]:  ") or "https://confluence.desy.de/"
	user           = input("Please enter your Username. You need access to all pages! [default: jkuepper]:  ") or "jkuepper"
	sk             = input("Please enter the spacekey of the space you want to copy to your computer     :  ")
	downloadPages  = True
	downloadBlog   = True
	downloadAttach = True
	static_archive.startArchive(servername,user,sk,downloadPages,downloadBlog,downloadAttach)

if __name__ == "__main__":
	main()
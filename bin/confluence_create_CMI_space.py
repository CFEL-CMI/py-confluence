#!/usr/bin/python3

"""
This python3 module creates a new space according to the CMI template.
The CMI template includes a custom homepage, the space categories **cfel-cmi** and **cmi-elog-calendar**.
You have to provide a servername and a user with rights to create a new space.
Additional settings like the spacekey and name of the new space are required. 
"""

from lib import spaces
def main():
	"""
	Url to the Server. Please include a / after the url
	"""
	print('Please make sure you have the permission to create a space!')
	servername     = input("Server address with trailing /   [default: https://confluence.desy.de/]  :  ") or "http://at-stage-05:8090/"
	user           = input("Please enter your Username!      [default: jkuepper]                     :  ") or "admin"
	spacekey       = input("Please enter the spacekey of the new space                               :  ")
	spacename      = input("Please enter the name of the new space                                   :  ")
	readGroup      = input("Comma separated list of GROUPS with READONLY access  [default: cmi-users]:  ") or "cmi-users"
	writeGroup     = input("Comma separated list of GROUPS with WRITE    access  [default: none]     :  ") or ""
	readUser       = input("Comma separated list of USERS  with READONLY access  [default: none]     :  ") or ""
	writeUser      = input("Comma separated list of USERS  with WRITE    access  [default: you]      :  ") or ""

	spaces.createCMISpace(servername,user,spacekey,spacename)
if __name__ == "__main__":
	main()

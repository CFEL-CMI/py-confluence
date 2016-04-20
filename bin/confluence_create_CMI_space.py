#!/usr/bin/python3

from lib import spaces

print('Please make sure you have the permission to create a space!')
# Url to the Server. Please include a / after the url
servername     = input("Server address with trailing /   [default: https://confluence.desy.de/]  :  ") or "https://confluence.desy.de/"
user           = input("Please enter your Username!      [default: jkuepper]                     :  ") or "jkuepper"
spacekey       = input("Please enter the spacekey of the new space                               :  ")
spacename      = input("Please enter the name of the new space                                   :  ")
readGroup      = input("Comma separated list of GROUPS with READONLY access  [default: cmi-users]:  ") or "cmi-users"
writeGroup     = input("Comma separated list of GROUPS with WRITE    access  [default: none]     :  ") or ""
readUser       = input("Comma separated list of USERS  with READONLY access  [default: none]     :  ") or ""
writeUser      = input("Comma separated list of USERS  with WRITE    access  [default: you]      :  ") or ""

spaces.createCMISpace(servername,user,spacekey,spacename)


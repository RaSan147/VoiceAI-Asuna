# print current path and file list

import os, sys

if not os.getcwd().endswith("src"):
	os.chdir("./src")
	sys.path[0] = os.path.dirname(os.path.abspath(__file__))

try:
	from App_server import SH
except:
	raise Exception(os.getcwd(), os.listdir())


handler = SH
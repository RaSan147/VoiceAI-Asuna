# print current path and file list

import os, sys, traceback

if not os.getcwd().endswith("src"):
	sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
	os.chdir("./src")

try:
	from App_server import SH
except:
	raise Exception(os.getcwd(), os.listdir(), traceback.format_exc())


handler = SH
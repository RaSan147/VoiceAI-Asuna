# print current path and file list

import os

if not os.getcwd().endswith("src"):
	os.chdir("./src")


from App_server import SH


handler = SH
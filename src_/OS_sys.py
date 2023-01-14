"""Operating System functions"""

__all__ = ('os_name', 'subprocess_call', 'os_system', 
			'check_internet', 'null', 'install', 'install_req', 
			'check_installed', 'install_missing_libs')


from platform import system as os_name
import sys
from subprocess import call as subprocess_call
import os
from os import system as os_system
os_name = os_name()
import socket
import importlib.util

from PRINT_TEXT3 import xprint
from IO_sys import delete_last_line


def check_internet(hostname='1.1.1.1'):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except Exception:
     pass # we ignore any errors, returning False
  return False

def null(*args):
	pass

def install(pack, alias=None):  # fc=0701 v
	"""Just install package

	args:
	-----
		pack: the name the library (bs4, requests)
		alias: if the pip package name is different from lib name, then used alias (not required here) [beautifulsoup4 (pip)=> bs4 (lib name) """

	import sysconfig
	if alias is None:
		alias = pack

	more_arg = " --disable-pip-version-check --no-python-version-warning --quiet"

	py_h_loc = os.path.dirname(sysconfig.get_config_h_filename())
	on_linux = f'export CPPFLAGS="-I{py_h_loc}";'
	command = "" if os_name == "Windows" else on_linux
	comm = f'{command} {sys.executable} -m pip install  {more_arg} {alias}'

	subprocess_call(comm, shell=True)


	
def install_req(pkg_name, alias=None):  # fc=0702 v
	"""install requirement package if not installed

	args:
	-----
		pkg_name: Package name to search if installed
		alias: if the pip package name is different from lib name,
			then used alias (not required here) [beautifulsoup4 (pip)=> bs4 (lib name)] """
	if isinstance(pkg_name, (list, tuple)):
		alias = pkg_name[1] # alias is used in pypl
		pkg_name = pkg_name[0]
	if alias is None:
		alias = pkg_name
		
	if not check_installed(pkg_name):
		if not check_internet():
			xprint("/rh/No internet! Failed to install requirements/=/\n/ruh/Closing in 5 seconds/=/")
			return False
			
		xprint("/y/Installing missing libraries (%s)/=/"%pkg_name)
		install(pkg_name, alias)
		delete_last_line()

	if not check_installed(pkg_name):
		xprint('/r/Failed to install and load required Library: "%s"/y/\nThe app will close in 5 seconds/=/'%pkg_name)
		try:
			pass #leach_logger('00006||%s||%s'%(pkg_name, str(Netsys.check_internet("https://pypi.org", '00006'))))
		except NameError:
			pass
		return False
	return True

def check_installed(pkg):
	"""pkg: str or list
	if list [module name, name in pip or link]"""
	if not isinstance(pkg, str):
		pkg = pkg[0]
	return bool(importlib.util.find_spec(pkg))



def install_missing_libs(req):  # fc=0706 v
	""" installs missing libraries from the requirements variable"""

	failed = False
	
	for i in req:
		install_req(i)

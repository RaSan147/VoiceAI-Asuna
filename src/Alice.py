#pylint:disable= '\.'. String constant might be missing an r prefix.
# pylint:disable=C0103
# pylint:disable=W0312
# pylint:disable=W191
#	#tab
##~~~ need to take test


print('		Initializing...')
Vcode = ""
func_ver = '37'
'''update:
	i) regex smplified

'''

QUEUE = {}

#: *****************************************************************************
#:					This code was created by Ratul Hasan					 *
#:					 So comlpete credit goes to him(me)					  *
#: *****************************************************************************
#: Sharing this code without my permission is not allowed					  *
#: *****************************************************************************
#: This code was created based on IDLE, Pydroid(Android), qPython(Android) etc.*
#: So most online/web site based idle(i.e: Sololearn) can't run this code	  *
#: properly.																   *
#: *****************************************************************************
#: If there is any error or you want to help please let me know.			   *
#: e-mail: wwwqweasd147@gmail.com											  *
#: *****************************************************************************


try:  # to check if the file is reloaded or not
	if reloader: # is True
		reloaded = True
except NameError:
	reloader = False
	reloaded = False
ai_import = True

BREAK_POINT = False

# Basic imports

print('			 00%',end='\r')
from platform import system as os_name
os_name=os_name()

from os import system
from sys import exit as sys_exit, executable as sys_executable, getsizeof
import ctypes

exit = sys_exit


def is_tool(name):  #fc=0000 xx
		"""Check whether `name` is on PATH and marked as executable."""
		from shutil import which
		return which(name) is not None


def Ctitle(title):  # fc=0001
		"""sets CLI window title
		title: Window title"""

		try:
			ctypes.windll.kernel32.SetConsoleTitleW(title)
		except:
			if is_tool("title"):
				from os import system as os_system
				os_system('title ' + title)
				
				
Ctitle('Project Alice (Initializing)')
import datetime
print('			 03%',end='\r')
from random import choice
print('			 05%',end='\r')
import re
print('			 07%',end='\r')
import sys, os
print('			 10%',end='\r')
# from web_link import *
import webbrowser
print('			 13%',end='\r')
from os import makedirs, getcwd
from os.path import exists, isdir, basename, splitext
print('			 18%',end='\r')
import subprocess

print('			 25%',end='\r')
from threading import Thread, local
print('			 28%',end='\r')
from time import sleep, time as time_on
print('			 30%',end='\r')
from urllib import parse, request  # used to parse values  # used to make requests into the url
print('			 35%',end='\r')
from importlib import reload, import_module
import pkg_resources, traceback
print('			 38%',end='\r')

#personal lib
from bbc_news import bbc_news
from basic_conv_pattern import *
from errors import LeachKnownError, LeachNetworkError, LeachPermissionError, LeachCorruptionError, LeachICancelError,Error404
from PRINT_TEXT3 import xprint, remove_style

from fsys import Fsys_, Datasys_, Netsys_, IOsys_
Fsys = Fsys_()
Datasys = Datasys_()
IOsys = IOsys_()
from config import  config

print('			 40%',end='\r')

import warnings
warnings.filterwarnings("ignore")

'''try:
	import httplib
except ModuleNotFoundError:
	import http.client as httplib'''

# Basic Variables
on_screen = ''
was_on_screen = ''
audionum = '0'
m_paused=None


########################################
##--------##pdata##start------------####
########################################

# sign= True
uiName = "x"
aiName = "Alice"
upwmd5 = "8d5e957f297893487bd98fa830fa6413"
talk_aloud = True
talk_aloud_temp = True

bbc_topic = 'Asia_url'  # exec( reader("Yui_data/RAM/pdatas2.py"))
played_music = False


########################################
##--------##pdata##end------------####
########################################

print('			 42%',end='\r')

########################################
##--------##conv-file##start--------####
########################################
# all conversations

def generate_list(prefix):
	#l = [globals()[name] for name in globals().keys() if name.startswith(prefix)]
	#return (item for sublist in l for item in sublist)

	return ( item for sublist in [globals()[name] for name in globals().keys() if name.startswith(prefix)] for item in sublist)

def gen_list(x):
	#returns generator, can be used as list, but won't print as a lidt unless its converted

	#l = globals()[name] for name in globals().keys() if name.startswith(x)
	#return [sublist for sublist in l]
	return (sublist for sublist in [globals()[name] for name in globals().keys() if name.startswith(x) ])



########################################
####-------##conv_file##end##------#####
########################################
print('			 50%',end='\r')
##~~~<need to take speed test


class OSsys_:  # fc=0700
	"""Operating System functions"""

	def null(*args):
		pass

	def install(self, pack, alias=None):  # fc=0701 v
		"""Just install package

		args:
		-----
			pack: the name the library (beautifulsoup4, requests)
			alias: if the pip package name is different from lib name, then used alias (not required here) [beautifulsoup4 (pip)=> bs4 (lib name) """

		if alias is None:
			alias = pack

		subprocess.call([sys_executable, "-m", "pip", "install", '--disable-pip-version-check', '--quiet', alias])

	def install_req(self, pkg_name, alias=None):  # fc=0702 v
		"""install requirement package if not installed

		args:
		-----
			pkg_name: Package name to search if installed
			alias: if the pip package name is different from lib name,
				then used alias (not required here) [beautifulsoup4 (pip)=> bs4 (lib name)] """

		if alias is None:
			alias = pkg_name

		

		if not check_installed(alias):
			if not check_internet():
				xprint("/rh/No internet! Failed to install requirements/=/\n/ruh/Closing in 5 seconds/=/")
				return False
				
			xprint("/y/Installing missing libraries (%s)/=/"%pkg_name)
			self.install(pkg_name, alias)
			IOsys.delete_last_line()

		if not check_installed(alias):
			xprint('/r/Failed to install and load required Library: "%s"/y/\nThe app will close in 5 seconds/=/'%pkg_name)
			try:
				pass #leach_logger('00006||%s||%s'%(pkg_name, str(Netsys.check_internet("https://pypi.org", '00006'))))
			except NameError:
				pass
			return False
		return True

	def get_installed(self):  # fc=0703 v
		"""returns a list of installed libraries"""

		import pkg_resources as pkg_r
		reload(pkg_r)

		return [pkg.key for pkg in pkg_r.working_set]


	def catch_KeyboardInterrupt(self, func, f_code, *args):  # fc=0705 v
		"""Runs a function in a isolated area so that Keyboard cancel
		can be caught and processed accordingly

		args:
		-----
			func: The function to call inside the space
			f_code: The caller function id
			*args: The args to send inside the program"""
		try:
			try:
				try:
					box = func(*args)
					return box
				except EOFError:
					raise LeachICancelError
				except KeyboardInterrupt:
					raise LeachICancelError
				except LeachICancelError:
					tnt("Cancelled")
			except EOFError:
				raise LeachICancelError
			except KeyboardInterrupt:
				raise LeachICancelError
		except EOFError:
			raise LeachICancelError
		except KeyboardInterrupt:
			raise LeachICancelError

	def install_missing_libs(self):  # fc=0706 v
		""" installs missing libraries from the requirements variable"""

		failed = False
		
		for i in requirements_all:
			if not OSsys.install_req(i):
				failed = True
				break

		if os_name == "Windows":
			for i in requirements_win:
				if not OSsys.install_req(i):
					failed = True
					break
		if failed:
			xprint("/r/Failed to install a requirement./=//hui/Exiting in 3/s1/ 2/s1/ 1")
			exit()
		xprint('/hu/Rebooting Program. Please wait/=/')
		try:
			subprocess.call(sys_executable + ' "' + os.path.realpath(__file__) + '"')
		except KeyboardInterrupt: pass
		except EOFError: pass
		finally:
			exit(0)

	def import_missing_libs(self, failed=False):  # fc=0707 v
		""" imports missing libs to global level and on missing installs and re-imports
		
		failed: failed once, won't retry"""
		# print(config.disable_lib_check)

		if config.disable_lib_check:
			return 0

		all_libs = OSsys.get_installed()
		
		has_all_libs = all(i in all_libs for i in requirements_all)
		if os_name=="Windows":
			has_all_libs = has_all_libs and all(i in all_libs for i in requirements_win)
		
		
		# print(has_all_libs, all_libs)
		if has_all_libs:
			return 0
		global mplay4
		self.install_missing_libs()

		######### RE-IMPORTING THE PYTHON 3RD PARTY LIBRARIES #########
		try:
			
			from googlesearch import search as g_search
			import requests, natsort
			
			
			if os_name == "Windows": import mplay4

		except:
			if failed:
				traceback.print_exc()
				xprint("/r/Failed to load required libraries.\n/=//yh/Possible cause 1st initialization without internet")
				exit()

			else:
				self.import_missing_libs(failed=True)



OSsys = OSsys_()


try:
	if os_name == "Windows": import mplay4
except:
	pass


import json

class System_Data:
	def __init__(self):
		self.local_file = "Alice_data/RAM/pdatas2.json"
		self.local_dir = "Alice_data/RAM"
		
		
		self.local_data = json.loads(Fsys.reader(self.local_file, on_missing='{}', ignore_missing_log=True))
		
		self.default_data = {
		"ai_name": aiName
		}
		
		self.local_data = Datasys.default_dict(self.default_data, self.local_data)
		


		self.aiName = self.local_data["ai_name"]
		
		print(self.local_data)
		
	def edit_pdata(self, old_dat, new_dat):
		filedata = json.dumps(self.local_data)
		Fsys.writer("pdatas2.json", "w", filedata, self.local_dir)
	
	def save_data(self, data = None):
		if data == None:
			filedata = json.dumps(self.local_data)
			Fsys.writer("pdatas2.json", "w", filedata , self.local_dir)
		else:
			Fsys.writer("pdatas2.json", "w", data, self.local_dir)

		
sysData = System_Data()
sysData.save_data()




class Flags:
	def __init__(self):
		self.hello_bit = 1
		self.hi_bit = 1
		self.what_u_name_bit = 1
		self.TyuiName = "0"
		
		
flags = Flags()

########################################
##--------##checkers##start---------####
########################################
def check_signin():
	if exists("Alice_data/RAM/pdatas2.json") == False:
		return False
	else:
		#Fsys.reader()
		with open("Alice_data/RAM/pdatas2.json") as f:
			for i in f.readlines():
				if i.startswith('sign= '):
					line = i
					break
				else:
					line = None
		if line == 'sign= False':
			return False
		elif line == 'sign= True':
			return True
		else:
			print('The data is corrupted')
			raise SystemError


def check_internet(host='google', timeout=3):
	"""returns True or False based on internet availability"""
	if host == 'fast':
		return check_internet('http://www.muskfoundation.org/', timeout=timeout)

	elif host == 'pypi':  #pypi.org
		return check_internet('https://pypi.org', timeout=timeout)

	elif host == 'google':   #www.google.com
		return check_internet('https://8.8.8.8', timeout=timeout)

	else:
		try:
			request.urlopen(host, timeout=timeout)
			return True
		except request.URLError:
			return False
		#except socket.timeout:
			#return False

def check_installed(pkg):
	reload(pkg_resources)
	if type(pkg)==list:
		out=True
		for i in pkg:
			out= out and (i.lower() in  [x.key.lower() for x in pkg_resources.working_set])
		return out
	#installed_packages = pkg_resources.working_set
	#installed_packages_list = [i.key for i in installed_packages]
	else: return (pkg.lower() in  [i.key.lower() for i in pkg_resources.working_set])


def check_version(package):
	reload(pkg_resources)
	package = package.lower()
	return (next((p.version for p in pkg_resources.working_set if p.project_name.lower() == package), "No match"))
def check_talk():
	global played_music
	# print("played_music", played_music)
	# print("talk_aloud", talk_aloud)
	# print("talk_aloud_temp", talk_aloud_temp)
	if played_music : # ==True
		played_music= not (os_name=='Windows' and (not yt_plugin.music.isplaying()))
		return talk_aloud and talk_aloud_temp and (not played_music)
	else:
		return talk_aloud and talk_aloud_temp

print('			 55%',end='\r')
########################################
##--------##web-file##start---------####
########################################
# all web functions


url_google = ('https://www.google.com', 'google', 'gogle', 'gooogle')
url_fb = ('https://www.facebook.com', 'facebook', 'facebok', 'fb')
url_yahoo = ['https://www.yahoo.com', 'yahoo', 'yaho']
url_youtube = ['https://www.youtube.com', 'youtube', 'tubemate', 'utube']
url_wiki = ['https://www.wikipedia.com', 'wikipedia', 'wikipidia', 'wikipidea', 'wikipedea']
url_reddit = ['https://www.reddit.com', 'reddit', 'redit']
url_bing = ['https://www.bing.com', 'bing', 'microsoft search']
url_insta = ['https://www.instagram.com', 'instagram', 'insta']
url_apple = ['http://apple.com/', 'apple website', 'apple.com']
url_microsoft = ['http://microsoft.com/', 'microsoft website', 'microsoft.com', 'microsoft site', 'microsoft page']
url_pornhub = ['https://www.pornhub.com/', 'pornhub website', 'pornhub']

goog_supp = ['http://support.google.com/', 'support', 'supports']
goog_docs = ['http://docs.google.com/', 'doc', 'docs']
links = generate_list('url_')
#if 'insta' in links:print(links)
#sleep(10)
links_li = gen_list('url_')
googles = generate_list('goog_')
googles_li = gen_list('goog_')


print('			 60%',end='\r')


def web_go(link):
	webbrowser.open_new_tab(link)


# web_go('C:/Users/Dell/Documents/Python/Project_Alice/datapy.html')
def linker(link):
	global links_li
	for i in links_li:
		if link in i:
			web_go(i[0])
			return True
			break

	return False


def googler(link):
	global googles_li
	for i in googles_li:
		if link in i:
			web_go(i[0])
			return True
			break
	return False


def searcher(search_txt):
	loc = search_txt.replace(' ', '+')
	webbrowser.open_new_tab('https://www.google.com/search?q=' + loc)


########################################
##----------##web-file##end---------####
########################################

print('			 63%',end='\r')
# exec(reader('func_file'+func_ver+'.py'))

########################################
##--------##func-file##start--------####
########################################
# all functions

def loc(x):
	"""to fix dir problem"""
	if os_name == 'Windows':
		return x.replace('/', '\\')
	else:
		return x.replace('\\', '/')


def reader(direc):
	with open(loc(direc)) as f:
		return f.read()


def writer(locs, fname, mode, data, bit=0):
	if dir == 0:
		with open(fname, mode) as file:
			file.write(data)
	else:
		if isdir(locs):
			if locs.endswith('/'):
				with open(loc(locs + fname), mode) as f:
					f.write(data)
			else:
				with open(loc(locs + '/' + fname), mode) as f:
					f.write(data)
		else:
			makedirs(loc(locs))
			writer(locs, fname, mode, data, bit)


def backup(data_entry):
	c_time = str(datetime.datetime.now())
	"""Will backup every command by user"""
	Fsys.writer("uidb.txt" , "a", str((c_time, data_entry)) + "\n", "Alice_data/RAM",)


def on_win(func,*var):
	if os_name=='Windows':
		func(*var)

def cmdrun(cmd_in, y=None):
	#import subprocess
	if isinstance(cmd_in, list):
		if len(cmd_in)>2: raise ValueError
		cmd_in,y= tuple(cmd_in)
	cmd_line = cmd_in.split()
	if y != None: print(y)
	cmd_out = subprocess.run(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return cmd_out.stdout.decode('utf-8')


def inputer(msg='', only_type=False):
	global BREAK_POINT
	try:
		if only_type:
			raise LeachKnownError
		tnt(msg)
	except:
		slowtype(msg)
	a = True
	while a == True:
		try:
			y = input()
			a = False
		except UnicodeDecodeError:
			tnt('/r/*invalid input!/=/\nPlease re-type correctly:  ')
		except KeyboardInterrupt:
			BREAK_POINT = True
		except EOFError:
			BREAK_POINT = True
	del a, msg
	backup(y)
	return y


def asker(out='', self =None, true_func = OSsys.null, false_func=OSsys.null):
	tnt(out, toaster = True)
	Ques2 = inputer()
	Ques2 = Ques2.lower()
	while Ques2 not in cond:
		tnt(condERR)
		Ques2 = inputer()
		Ques2 = Ques2.lower()
	if Ques2 in cond:
		if Ques2 in yes:
			true_func()
			return True
		else:
			false_func()
			return False

print('			 70%',end='\r')
# exec( reader('Alice_data/brain/brain.py'))

########################################
####-------##brain##start##--------#####
########################################

# help()


# asdf='aaddffghhjjkl'
# writer('temp_Alice_data/crack/c','aa.txt','w',asdf)
def delprevline():
	"""Use this function to delete the last line in the STDOUT"""

	# cursor up one line
	sys.stdout.write('\x1b[1A')

	# delete last line
	sys.stdout.write('\x1b[2K')


def delthisline():
	"""Use this to delete current line"""
	sys.stdout.write('\x1b[2K')


# def clean():
# 	# return 0
# 	# for windows
# 	if os_name == 'Windows':
# 		_ = system('cls')
# 	# for mac and linu
# 	# x(here, os.name is 'posix')
# 	else:
# 		_ = system('clear')

def text_styling_markup(text):
	''' for custom text stypling like html
	print(tnt_helper('/<style= col: red>/ 69'))'''
	if '/<' not in text:
		return text
	while re.search('/<(.*)>/', text):
		a = re.search('/<(.*?)>/', text)
		if a:
			style = a.group(1)

			text = text.replace(a.group(0), '')
	return text

custom_type_codes = ['/u/', '/a/', '/y/', '/g/', '/k/', '/b/', '/r/', '/h/', '/bu/', '/hu/', '/=/']


def tnt_helper(text, bit=0):
	''' i) custom_type_codes are used for custom commands to
	 simplify the code
	ii) other text modifications are made here and passes optimized
	 text for the typing and speaking engine respectively'''
	if bit==0: bit='type'

	# pattern [[xx//yy]]
	if '//' in text:
		while re.search('\[\[(.*?)//(.*?)\]\]', text):
			a = re.search('\[\[(.*?)//(.*?)\]\]', text)
			if bit == 'talk':
				text = text.replace(a.group(0), a.group(2))
			elif bit == 'type':
				text = text.replace(a.group(0), a.group(1))
	while re.search('==(.*)==', text):
		a = re.search('===([^(==)]*)===', text)
		if a:
			text = text.replace('==='+a.group(0)+'===', '/hu/' + a.group(1) + '/=/')
		a = re.search('==(.*?)==', text)
		if a:
			text = text.replace('=='+a.group(0)+'==', '/u/' + a.group(1) + '/=/')

	# text =text.replace(a.group(0),a.group(1))
	if bit == 'type':

		text= text_styling_markup(text)
		'''text_styling_markup(text) for custom text stypling like html
		print(tnt_helper('/<style= col: red>/ 69'))'''

		'''text = text.replace('/u/', '/h/\033[4;37;40m')  # UNDERLINE
		text = text.replace('/a/', '\033[4;34;40m')  # LINK
		text = text.replace('/y/', '\033[1;33;40m')  # DID YOU MEAN...?
		text = text.replace('/g/', '\033[1;32;40m')  # YES SURE
		text = text.replace('/k/', '\033[0;30;40m')  # HIDDEN
		text = text.replace('/b/', '\033[1;37;40m')  # BRIGHT
		text = text.replace('/r/', '\033[1;31;40m')  # WARNING
		text = text.replace('/h/', '\033[1;30;43m')  # HIGHLIGHT
		text = text.replace('/bu/', '\033[1;37;40m\033[4;37;40m')  # Brightlight+Underline
		text = text.replace('/hu/', '\033[0;37;40m\033[4;30;43m')  # Highlight+Underline
		text = text.replace('/=/', '\033[0m')'''
	else:
		text=re.sub("/[argybpcw \=uih_]+/","", text)
	return text

# print("\033[4;37;40m hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
nap_time = 0.03



def slowtype(*args):
	wait_ = nap_time
	xprint (*args, highlighter=True, wait_time=wait_, run_at_start=tnt_helper)
def slowtyper(*args, wait_time = nap_time):
	"""thread to start slowtype engine"""
	global typer
	typer = Thread(target=slowtype, args=(*args,))
	typer.start()
	return


def tnt(txt, y=nap_time):
	slowtype(txt)


not_installed = []


def install(pack, alias=0):
	"""Just install package"""
	global not_installed
	#import subprocess
	if alias == 0:
		alias = pack
	if check_installed(alias) == True:
		# slowtype(pack+ ' is already installed\n')
		return True
	elif check_internet(host='pypi'):
		subprocess.call([sys.executable, "-m", "pip", "install", "--user",'--disable-pip-version-chec','--quiet', pack])

		if check_installed(alias) == False:
			print('method 1 failed\nretrying with method 2(' + pack + ')')
			subprocess.call([sys.executable, "-m", "pip", "install", pack])
		return check_installed(alias)
	else:
		tnt('/r/Failed! \nPossible cause: No internet connection./=/\n')
		not_installed.append(alias)
		return False


def off_install(direc, pack, bit=1):
	"""install package offline"""
	global not_installed
	#import subprocess
	if check_installed(pack) == True:
		if bit == 0:
			tnt('Already installed')
	else:
		subprocess.call([sys.executable, "-m", "pip", "install", "--user", direc])
		if check_installed(pack) == False:
			print('method 1 failed\nretrying with method 2(' + pack + ')')
			subprocess.call([sys.executable, "-m", "pip", "install", direc])
		if check_installed(pack) == False:
			tnt('/r/Failed! \nPossible cause: File not found or Corrupted./=/\n')
			not_installed.append(pack)


# off_install()
OSsys.install_req('https://github.com/RaSan147/Wikipedia/archive/refs/tags/v1.1.1.zip', "wikipedia")
import wikipedia


asd=time_on()
#cmd = ['pip', 'freeze']
#output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0].decode()
#zxcz=subprocess.run([sys.executable, 'pip', 'freeze'])
#print(time_on()-asd)
#print(list(i.split('==')[0] for i in output.split('\n')))


def upgrade(pack):
	"""Upgrades a package"""
	#import subprocess
	prev = check_version(pack)
	if check_internet() == True:
		subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", '--user','--disable-pip-version-chec', '--quiet ', pack])

		print(check_version(pack))
		if check_version(pack) == prev:
			subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", pack])
	else:
		tnt('/r/Failed! \nPossible cause: No internet connection./=/\n')


def install_req(pkg, alias=0, msg=''):
	if alias == 0:
		alias = pkg
	out=True
	if not check_installed(alias):
		slowtype(
			msg if msg != '' else alias + " is missing. Do you want to download it from here?\n*Data charge may apply*")
		permit = inputer("/r/Yes to continue or no to cancel??\n*If no some error will occur*/=/\n")
		while permit not in cond:
			permit = inputer(condERR)
			permit = permit.lower()
		if permit in cond:
			if permit in yes:
				if type(pkg)==list:
					for i in pkg:
						out= out and install(i, alias[pkg.index(i)])
					return out
				else:
					return install(pkg, alias)
			else:
				tnt("/y/*Some error may occur & the program will break!*/=/")
				return False

print('			 80%',end='\r')
# for i in range(1,1500):
#	print(chr(i))

#install_req('mega.py')
requirements_all = ['pafy','mutagen', 'comtypes', 'six', "yt-dlp", "requests"]
requirements_win = ["pywin32"]

OSsys.import_missing_libs()
import requests
#install_req(, msg='Some Requrements are missing. The program will download the download them (Data charge may apply)')
# install_req()
#install_req('openpyxl')
# install_req()

import yt_plugin

print('			 85%',end='\r')


def ins_frm_imp(frm, imp, alias=0, aas=''):
	if alias == 0:
		alias = imp
	if aas == '':
		aas = imp
	import_bit = 0
	"Install and import package"
	# import importlib
	try:
		globals()[aas] = getattr(__import__(frm, globals(), locals(), [imp], 0), imp)
	except ImportError:
		install_req(alias)
	# if
	#	import_bit=1
	finally:
		if import_bit == 0:
			globals()[aas] = getattr(__import__(frm, globals(), locals(), [imp], 0), imp)


# del importlib

def ins_n_imp(pack, aas=''):
	"Install and import package"
	import_bit = 0
	if aas == '':
		aas = pack
	# import importlib
	try:
		globals()[aas] = import_module(pack)
	except (ImportError, ModuleNotFoundError):
		tnt('\n' + pack + " is missing. Do you want to download it from here?\n*Data charge may apply*")
		permit = inputer("Yes or no?? *If no some error will occur*\n")
		while permit not in cond:
			permit = inputer(condERR)
			permit = permit.lower()
		if permit in yes:
			install(pack)
		else:
			tnt("/r/*Some error will occur & the program will break!*/=/")
			import_bit = 1

	finally:
		if import_bit == 0:
			globals()[aas] = import_module(pack)


# del importlib

def compress(file_names):
	import zipfile

	path = getcwd() + '/'

	# Select the compression mode ZIP_DEFLATED for compression
	# or zipfile.ZIP_STORED to just store the file
	compression = zipfile.ZIP_DEFLATED

	# create the zip file first parameter path/name, second mode
	zf = zipfile.ZipFile("RAWs.zip", mode="w")
	try:
		for file_name in file_names:
			# Add file to the zip file
			# first parameter file to zip, second filename in zip
			zf.write(path + file_name, file_name, compress_type=compression)

	except FileNotFoundError:
		print("/r/An error occurred/=/")
	finally:
		# Don't forget to close the file!
		zf.close()


# file_names= ["brain.py", "voice.py"]
# compress(file_names)


########################################
####---------##brain##end##--------#####
########################################
# sleep(5)
print('			 90%',end='\r')
########################################
####--------##voice##start##-------#####
########################################

def ins_n_imp_voice():
	"""Installs And Sets Up Voice Module Based On Os And Returns Its Name.
	If No Voice Module Was Installed Or Imported ReturnS 'unav'
	"""
	global not_installed
	no_voice_error = "\n \n|*Warning! Voice won't work\n\033*|"
	if os_name == 'Windows':
		try:

			global pyttsx3
			import pyttsx4 as pyttsx3
			voice_module = 'pyttsx3'

		except ValueError:
			ins_frm_imp('gtts', 'gTTS')
			if check_installed('gtts') == True:
				voice_module = 'gtts'
			else:
				print(no_voice_error)
				voice_module = 'unav'
	elif os_name == 'linux':
		try:
			import androidhelper
			global droid
			droid = androidhelper.Android()
			voice_module = 'androidhelper'
		except:
			voice_module = 'unav'
	else:
		voice_module = 'unav'
		droid = None
	return voice_module


vmodule = ins_n_imp_voice()
SPEAKER_BUSY = False



def speak_(text):
	global vmodule, speakers, droid, talk_aloud_temp, SPEAKER_BUSY
	text = tnt_helper(text, 'talk')
	# talk_aloud_temp = False
	if vmodule == 'pyttsx3':
		global engine
		engine = pyttsx3.init()
		# Set properties _before_ you add things to say
		engine.setProperty('rate', 180)
		# Speed percent (can go over 100)
		engine.setProperty('volume', 0.9)  # Volume 0-1
		en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
		# Use female English voice
		engine.setProperty('voice', en_voice_id)
		
		SPEAKER_BUSY = True
		
		engine.say(text)
		engine.startLoop(False, error = False)
		# engine.iterate() must be called inside externalLoop()
		engine.iterate()
		engine.endLoop()
		
		SPEAKER_BUSY = False
		


	elif vmodule == 'gtts':
		global audionum
		a = gTTS(text=text, lang='en', slow=False)
		name = 'Alice_data/RAM/outvoice' + audionum + '.mp3'
		a.save(name)
		audionum = str(int(audionum) + 1)
	elif vmodule == 'androidhelper':
		droid.ttsSpeak(text)
	else:
		pass

	# talk_aloud_temp = True

del tnt

def speakup(text):
	x = Thread(target=speak_, args= (text,))
	x.start()
	# if join: x.join()
	# speak_(text)


def tnt(text, speed=nap_time, force = False, toaster =None):
	global typer, speakers
	slowtyper(text, wait_time=speed)
	rr = re.compile('/s([\d\.]*)/')
	ss = re.compile('/s[\d\.]*/')

	def custom_replace(match):
		result = '<silence msec="%s"/>'%str(int(float(str(match.group(1)))*1000))
		return result

	def any_request(text):
		text = text.replace("<", "&lt;")
		text = text.replace(">", "&gt;")
		text = '<voice required="Gender=Female;Age!=Child">' +text
		return rr.sub(lambda match: custom_replace(match), text)

		# a0h hella1 wa2w

	


	if check_talk(): # ==True ==True
		if ss.search(text):
			text= any_request(text)

		speakup(text)
	typer.join()


# tnt("/hui/3 \n/s1/2 /s1/\n1 \n\n/s1/TIMES UP/=/" )


def tntr(*args, speed=nap_time, force = False):
	'''tnt from multuple arguments and gives a random output'''

	tnt(choice(args), speed, force)
def tntr_li(li ,speed=None):
	'''tntr from a list'''
	if speed==None:
		tnt(choice(list(li)))
	else:
		tnt(choice(list(li)), speed)
#tntr_li(li_how_r_u, speed=.3)
#sleep(100)
def tnt_ff(x, z, y):
	slowtyper(x, wait_time=nap_time)
	try:
		yt_plugin.mplay.load('Alice_data/ROM/offvoice/outvoice' + z + '.mp3')
	except:
		pass


########################################
####---------##voice##end##--------#####
########################################
print('			 95%',end='\r')
########################################
####--------##extra##start##-------#####
########################################


Vcode = splitext(basename(__file__))[0]


def curr_dir():
	# current directory
	return loc(getcwd())


def i_slim(in_dat):
	in_dat = in_dat.strip()
	in_dat = re.sub('\s{2,}', ' ', in_dat)
	in_dat = in_dat.lower()
	in_dat = in_dat.replace("'", "")
	in_dat = in_dat.replace("?", "")
	in_dat = in_dat.replace("!", "")
	in_dat = in_dat.replace(".", "")
	in_dat = in_dat.replace(",", "")
	in_dat = in_dat.replace(" us", " me")
	in_dat = in_dat.replace(" him", " me")
	in_dat = in_dat.replace(" her", " me")
	in_dat = in_dat.replace(" them", " me")

	return in_dat


print('			 100%',end='\r')
IOsys.clear_screen()

Ctitle('Project Alice')

def locker():
	IOsys.clear_screen()
	slowtype("Please enter your User name: ")
	Name = inputer()

	while Name == "" or Name != uiName:
		slowtype("/r/Invalid username!/=/\nPlease RETYPE YOUR USER NAME: ")
		Name = inputer()

	'''uipw=inputer("Please enter the Password: ")
	while uipw=="":
		uipw=inputer("\033[1;31;40mDon't leave this empty. Enter the correct Password. Otherwise you can't run this.\033[1;37;40m N\nEnter the Password: ")
	uipwmd5 = md5(uipw.encode('utf-8')).hexdigest()
	while uipwmd5!=upwmd5:
		uipw = inputer("\033[1;31;40m*WARNING!*\nYou have entered incorrect Password.\033[1;37;40m\nPlease enter the correct one: ")
		uipwmd5 = md5(uipw.encode('utf-8')).hexdigest()

	for i in range(10):
		sleep(.08)
		if i%3==0:
			x=":=="*12
		elif i%3==1:
			x="=:="*12
		elif i%3==2:
			x="==:"*12
		print("\rLogging in",x, end='',flush=True)
	delthisline()
	print("\n\nLogged in")#'''
	return Name


def check_performance():
	start_time = time_on()





#######To be continued #########

def wolfram(text):
	r = requests.get("http://api.wolframalpha.com/v1/result",
	params = {
		"i": text,
		"appid": "L32A8W-J8X5U6KG26"
	})
	if r.text == "Wolfram|Alpha did not understand your input": return False
	return r.text
def wikisearch(uix):
	if check_internet() == True:
		wolf = wolfram(uix)
		if not wolf:
			asker("/y/I don't know the answer ...\nShall I Google?/=/", true_func=lambda:searcher(uix))
			return
		tnt (wolf)
		sleep(2)

		def _wiki(uix):
			if uix in [i.lower() for i in wikipedia.search(uix)]:
				tnt('\n' + wikipedia.summary(uix, sentences=2))
				def _go_to_page():
					ny = wikipedia.page(uix)
					web_go(ny.url)
				
				if not asker('Do you want to know some more? ', true_func=_go_to_page): return
				_go_to_page()
				
			elif wikipedia.search(uix) != []:
				uix = wikipedia.search(uix)[0]
				
				if asker('Did you mean ' + uix + '? ', true_func= lambda: _wiki(uix)):
					_wiki(uix)
			else:
				
				if asker("Couldn't find " + uix + "!\nWould you like to search instead?  ", true_func= lambda: searcher(uix)):
					searcher(uix)
				#else:
				#	tnt('\nOk then.')
		
		if asker('Do you want to know some more? ' , true_func= lambda: _wiki(uix)):
			_wiki(uix)
		
	else:
		tnt('No internet connection!')


'''def test1():
	global engine
	sleep(10)
	engine.setProperty('rate', 180)
	# Speed percent (can go over 100)
	engine.setProperty('volume', 0.2)

def test():
	global engine
	sleep(10)
	engine.setProperty('rate', 90)
	# Speed percent (can go over 100)
	engine.setProperty('volume', 0.9)
	#tester1= Thread(target=test1)
	#tester1.start()
tester= Thread(target=test)
tester.start()'''


def find_person(txt):
	wikisearch(txt)


# tnt("Can't find him")

def tell_time():
	"""tells the current time"""
	nowits = datetime.datetime.now()
	tnt(choice(li_tell_time2) + nowits.strftime("%I:%M %p."))

def timer(text):
	r = wolfram("convert " + text + " to second")
	if r:
		sec = int(re.match(".*?(\d+).*", r).group(1))
		if sec>60:
			sleep(sec-60)
			tnt("1 minute left" ,force=True)
			
			sleep(51)
		elif sec>5:
			sleep(sec-5)
		else:

			sleep(sec)
			tnt("Times UP" ,force=True)
			return
		tnt("/hui/3 \n/s1/2 /s1/\n1 \n\n/s1/TIMES UP/=/" )
	else:
		tnt("Invalid time duration ", force=True)
	
def set_timer(text):
	print("TIMER BEGAN")
	t = Thread(target= timer, args=(text,))
	t.start()



def go_youtube(search):
	topic = search.split("youtube ", 1)[1]
	query_string = parse.urlencode({"search_query":topic})
	# print(query_string)
	html_content = request.urlopen("https://www.youtube.com/results?" + query_string)
	search_results = re.search(r'watch\?v=(.{11})',
								  html_content.read().decode())  # finds all links in search result
	webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results.group(1)))


########################################
####-------##func-file##end--------#####
########################################


if reloaded == False:
	uName = '[[Ratul//Rah tool]]'
	#locker()	   ###when planting

	# install_req()
	uitimes = str(datetime.datetime.now())
	uinput = "==========Code start on (" + uitimes + ") Version:" + Vcode + "=========="
	uinput = str(uinput) + "\n"
	Fsys.writer("uidb.txt", "a", uinput, "Alice_data/RAM/")

	sleep(1)
	wb = "\nWelcome back! "
	timex = datetime.datetime.now()
	timex = timex.strftime("%H")
	timex = int(timex)
	if timex >= 6 and timex < 12:
		outtxt = "Good morning, " + uName + wb
	elif timex >= 12 and timex < 18:
		outtxt = "Good afternoon, " + uName + wb
	elif timex >= 18 or timex < 6:
		outtxt = "Good evening, " + uName + wb
	else:
		outtxt = wb + uName
	# tnt(outtxt)
	sleep(1)
	IOsys.clear_screen()

	ui = ""
	uibit1 = 0
	outtxt = "Hello, my name is " + sysData.aiName + ".\n"
	outtxt += "My current version is: 0.1.0\n"
	outtxt += "Currently I can do some simple talk & things.\nAnd one more thing, please type 'exit' before exiting or closing for good.;) \n"
# ******uncomment following line******#
# tnt(outtxt)

escape = ["exit", "close", "shut down", "quit", "bye", "esc", "tata", "see ya", "see you"]



'''

while check_internet()==False:
	pass
tnt("internet asce yaaaaaaaay")

'''





def FCyuiName():
	a = "\nWant to change my name?   "
	tnt(a)
	q = asker()
	if q == True:
		a = "I'm sorry for my name )-;\nJust type my new name: "
		tnt(a)
		VR.send_output()
		flags.TyuiName = inputer()
		a = "Are you sure? It will change my name. However you can change it later by asking the same question ;-) "
		tnt(a)
		q = asker()
		if q == True:
			sysData.edit_pdata(sysData.aiName, flags.TyuiName)
			a = "Ok, my new name is " + flags.TyuiName + ".\nPLease Type exit to make it work well."
			tnt(a)
		else:
			tnt(nameGlad)
	else:
		tnt(nameGlad)
########################################
####-------##IO-file##start--------#####
########################################
case=None
cases=[]

ui_bit2=False
# print(links)

def failed(*args):
	xprint("/_r/FAILED/=/")
	
def L(arg):
	def l(arg):
		return arg.lower()
	if isinstance(arg, (list, tuple)):
		return type(arg)(map(l, arg))
	
	else: return arg.lower()

def Ltuple(arg):
	return L(tuple(arg))

def read_rest_news():
	news = bbc_news.last_news
	if news is None:
		return tnt("No news available")
	tnt(*news[5:])



ui = ""
ui1 = ""
ui2 = ""
def basic_talk2(INPUT_CODE):
	global talk_aloud_temp, reloader, ui, ui1, ui2, case, cases, uibit1, uibit2, reloader, reloaded, BREAK_POINT
	ui = i_slim(QUEUE[INPUT_CODE])
	while len(QUEUE) > 1:
		sleep(1)
	# ui = QUEUE[code]
	if ui in li_redo:
		try:

			if ui1 in li_redo:
				ui = ui2
			else:
				ui = ui1
		except NameError:
			tnt('There is no previous command to redo')
	# print(Ltuple([i%{"aiName": sysData.aiName} for i in li_hi]))
	if ui.startswith(Ltuple([i%{"aiName": sysData.aiName} for i in li_hi])):
		what_ = Ltuple([i%{"aiName": sysData.aiName} for i in li_hi if ui.startswith(L(i%{"aiName": sysData.aiName}))])
		# print(what_[0])
		reg_ex = re.search(what_[0] + '[,.]* ?(.*)', ui)
		if reg_ex:
			uiopen = reg_ex.group(1)
			if uiopen == "":
				ui = "hi"
			else:
				ui = uiopen

		
	if ui.startswith(Ltuple([i%{"aiName": sysData.aiName} for i in li_hello])):
		what_ = Ltuple([i%{"aiName": sysData.aiName} for i in li_hello if ui.startswith(L(i%{"aiName": sysData.aiName}))])
		
			
		#[i%{"aiName": sysData.aiName} for i in li_hello if ui.startswith(i%a{"aiName": sysData.aiName}]
		reg_ex = re.search(what_[0] + '[,.]* ?(.*)', ui)
		
		if reg_ex:
			uiopen = reg_ex.group(1)
			if uiopen == "":
				ui = "hello"
			else:
				ui = uiopen


	# print(ui)
	return basic_output(ui)
			
			
def basic_output(INPUT):
	global talk_aloud_temp, reloader, ui, ui1, ui2, case, cases, uibit1, uibit2, reloader, reloaded, BREAK_POINT, m_paused
	ui = i_slim(INPUT)
	if ui == "":
		return
	
	if ui in li_hi:
		if flags.hi_bit<2:
			tntr('Hello','Hello '+uName)
		else:
			tntr('Hello','Yeah!','Yes?','Yeah, need something?')
		flags.hi_bit+=1
		case='basic1'

	elif ui in li_hello:
		if flags.hello_bit<2:
			tntr('Hi', 'Hey','Hi there','Hey there')
		else:
			tntr('Yes?','Yeah?','Yeah, I can hear you','Yes, need something?')
		flags.hello_bit+=1
		case='basic2'

	elif ui in li_r_u_fine:
		tntr("Yeah, I'm fine!", "Yeah! I'm doing great.")
		case='yui3'
	elif ui in li_how_r_u:
		tntr("I'm fine!", "I'm doing great.")
	elif ui in li_loveu:
		tntr_li(li_relove)
		case='yui4'
	elif ui in ('i hate u', 'i hate you'):
		tntr("I'm sorry.", 'Sorry to dissapoint you.',"Please forgive me")
		case= 'yui5'

	elif ui in li_what_ur_name:

		outtxt = choice(["My name is ", "I am ", "Its "]) + sysData.aiName
		if flags.what_u_name_bit == 1:
			outtxt += "\nIf you want, you can change my name."
			tnt(outtxt)
			# FCyuiName()
		else:
			tnt(outtxt)	
		flags.what_u_name_bit += 1

	elif re.search('((replay)|(pause)|(stop)|(resume)|(mute)|(continue))(\s((the )?(music)|(song))|(it))?', ui):
		if os_name == 'Windows':
			no_music = False
			if yt_plugin.music.isrunning() == True:
				if ui in mc_stop:
					yt_plugin.music.stop()
					tnt("Stopped")
					m_paused= None
				elif ui in mc_pause:
					if m_paused == True or yt_plugin.music.ispaused():
						tnt('The music is already paused.')
						m_paused = True
					else:
						yt_plugin.music.pause()
						talk_aloud_temp = True
						m_paused=True
				elif ui in mc_resume:
					if m_paused == True or yt_plugin.music.ispaused():
						yt_plugin.music.resume()
						talk_aloud_temp = False
						m_paused=False
					else:
						tnt('The music is already playing.')
						m_paused = False
				elif ui in mc_replay:
					yt_plugin.music.replay()
				else:
					tnt('/r/Invalid command/=/')
			else:
				no_music = True
			if no_music:
				tnt('No music is playing right now.')
		else:
			tnt("You can't control music play in your Operating system")
	elif ui in li_QyuiName:
		outtxt = "Yes, you can."
		tnt(outtxt)
		FCyuiName()
	elif ui.startswith(li_play):
		what = [i for i in li_play if ui.startswith(i) == True]
		reg_ex = re.search(what[0] + ' *(.+)', ui)
		if len(ui) != what[0] and reg_ex:
			uiopen = reg_ex.group(1)
			try:
				yt_plugin.music.stop()
			except: pass
			yt_plugin.play_youtube(uiopen)
			played_music=True
			m_paused= False
			#music_patch.start()


	elif ui.startswith('install '):
		reg_ex = re.search('install (.+)', ui)
		uiopen = reg_ex.group(1)

		tnt('Installing ' + uiopen + '\n')
		install(uiopen)
		if check_installed(uiopen) == False:
			tnt('/r/Could not install!/=/')
		else:
			tnt('/g/Successfully installed %s/=/'%uiopen)
	elif ui.startswith('upgrade ') or ui.startswith('update '):
		reg_ex = re.search('up...?.. (.+)', ui)
		uiopen = reg_ex.group(1)
		if check_installed(uiopen) == False:
			install(uiopen)
		else:
			old_v = check_version(uiopen)
			tnt('Upgrading ' + uiopen + '\n')
			upgrade(uiopen)
			if old_v != check_version(uiopen):
				tnt('/g/Upgrade complete./=/')
			else:
				tnt('/r/Could not upgrade!/=/')
	elif ui.startswith(li_can_do):
		if ui.startswith(li_goto):
			what = [i for i in li_goto if ui.startswith(i) == True]
			reg_ex = re.search(what[0] + ' (.+)', ui)
			if reg_ex:
				uiopen = reg_ex.group(1)
				if uiopen in links:
					linker(uiopen)
				elif uiopen.startswith(url_google[1:]):
					uiopen = [i for i in url_google[1:] if uiopen.startswith(i)][0]
					reg_ex2 = re.search(what[0] + ' ' + uiopen + ' (.*)', ui)
					if reg_ex2:
						uiopen = reg_ex2.group(1)
						if uiopen in googles:
							googler(uiopen)
				else:
					searcher(uiopen)

	elif ui in li_AmyName:
		tnt(choice(li_AmyName) + uName + '.')


	elif ui=='parrot':
		parrot_input=inputer("say something: ")
		while parrot_input!= "exit":
			parrot_time=time_on()
			tnt(parrot_input)
			parrot_time=time_on()-parrot_time
			print('[time took =', parrot_time,'s,total words= ', len(parrot_input.split()),', wpm= ',(60/parrot_time)*len(parrot_input.split()))
			parrot_input=inputer("say something: ")


	elif ui == 'whats up':
		tnt('Just doing my things.')
	elif ui in li_tell_time1:
		tell_time()

	elif re.search('read (the )?(latest )?news', ui):
		if check_internet():
			news = bbc_news.task(bbc_topic)
			if news is None:
				tnt('No news available')
			else:
				tnt(*news[:5])
				asker("Do you want to read more?", true_func=lambda: tnt(*news[5:15]))
		else:
			tnt('No internet!')

	elif ui.startswith(li_whats):
		what = [i for i in li_whats if ui.startswith(i) == True]
		reg_ex = re.search(what[0] + ' (.+)', ui)
		if len(ui) != what[0] and reg_ex:
			uiopen = reg_ex.group(1)
			if uiopen in li_WmyName:
				tnt(choice(yeses) + choice(li_AmyName) + uName + '.')

			elif uiopen in ["latest news", "news update", 'news']:
				if check_internet():
					news = bbc_news.task(bbc_topic)
					if news is None:
						tnt("No news available")
					else:
						tnt(*news[:5])
						asker("Do you want to hear the rest?", true_func=read_rest_news)


				else:
					tnt('No internet!')

			elif uiopen in li_tell_time:
				tell_time()

			else:
				wikisearch(uiopen)

	elif ui.startswith(li_who):
		if ui in li_who_r_u:
			tnt(choice(li_AamI) % sysData.aiName)
		elif ui == "who am i":
			tnt("You are " + uName + ", a human being. Far more intelligent than me.")
		else:
			who = [i for i in li_who if ui.startswith(i) == True]
			reg_ex = re.search(who[0] + ' (.+)', ui)
			if len(ui) != len(who[0]) and reg_ex:
				uiopen = reg_ex.group(1)
				if uiopen in li_r_u:
					tnt(choice(li_AamI) % sysData.aiName)
				elif uiopen in li_Qcreator:
					tnt(choice(li_Acreator) % choice(li_syn_created))
				else:
					find_person(uiopen)

	elif ui in li_check_int:
		if check_internet() == False:
			tnt("No internet available.")
		else:
			tnt("Internet connection available.")

	elif ui in li_fucku:
		tntr_li(li_refuck)
		
	elif re.search(set_timer_pattern, ui):
		x = re.match(set_timer_pattern, ui).group(1)
		
		set_timer(x)

	elif ui in li_reload:
		exec(open(Vcode + '.py').read())
		reloader = True
		return "reload"


	elif ui in escape:
		reloaded = False
		reloader = False
		BREAK_POINT =True
		return "exit"

	else:
		outtxt = "Sorry, I don't understand.\n"
		tnt(outtxt)
		ui = inputer()
		ui = i_slim(ui)
		uibit1 = 1
	ui1 = ui
	if ui not in li_redo:
		ui2 = ui

	return "nn"
# tnt('/<style=a>/===hell===o')


out = ''

def send_message(message):
	"""send message to command control panel ("basic_talk2")"""
	code = time_on()
	QUEUE[code] = message
	basic_talk2(code)
	QUEUE.pop(code)



class VR_:
	"""Voice Recognizer"""
	
	
	# with sr.Microphone() as source:
	#     # read the audio data from the default microphone
	#     audio_data = r.record(source, duration=5)
	#     print("Recognizing...")
	#     # convert speech to text
	#     text = r.recognize_google(audio_data)
	#     print(text)
	def __init__(self):
		self.r = sr.Recognizer()
		self.output = None
		self.not_basic_talk = False
		
	
	def send_output(args, function = OSsys.null):
		function(args)
		return args


	def vc(self):
		global talk_aloud_temp, reloader, ui, ui1, ui2, case, cases, uibit1, uibit2, reloader, reloaded, BREAK_POINT
		import time
		
		while (out not in escape) and (len(QUEUE) == 0) and (out != "reload"):
			if BREAK_POINT: return
			with sr.Microphone() as source:
				# print("Listening...")
				self.r.pause_threshold = 1
				self.r.adjust_for_ambient_noise(source, duration=0.5)
				audio = self.r.listen(source)

			try:
				# print("Recognizing...")
				query = self.r.recognize_google(audio, language='en-in')
				# if query.startswith(aiName)
				print(f"User said: {query}\n")
				# return query
				ui = query
				try:
					if self.not_basic_talk:
						self.send_output_(query)
						continue
					send_message(query)
							
				except KeyboardInterrupt:
					BREAK_POINT = True
					send_message("exit")

				except EOFError:
					BREAK_POINT = True
					send_message("exit")
			except Exception as e:
				# print(e)
				# tnt("Say that again please...")
				# return "None"
				pass

if os_name == "Windows":
	import speech_recognition as sr
	VR = VR_()

	VC_THREAD = Thread(target=VR.vc)
	VC_THREAD.start()

while (out not in escape) and (len(QUEUE) == 0) and (out != "reload"):
	if uibit1 == 0:
		if ui_bit2==False:
			ui = inputer("\nWrite something that I know: ")
			
			ui_bit2=True
		else:
			# talk_aloud_temp=False
			ui = inputer("\n\nEnter Message: ", only_type=True)
			# talk_aloud_temp=True
	ui = i_slim(ui)

	while ui == "":
		ui = inputer("Try to type something: ")
		ui = i_slim(ui)

	uibit1 = 0
	print('"'+ui+'"')
	code_ = datetime.datetime.now()
	QUEUE[code_] = ui
	try:
		out = basic_talk2(code_)
		
	except KeyboardInterrupt:
		BREAK_POINT = True
	except EOFError:
		BREAK_POINT = True
	QUEUE.pop(code_)


if reloaded == False and reloader == False:
	timex = datetime.datetime.now()
	timex = timex.strftime("%H")
	timex = int(timex)
	if timex >= 18 or timex < 6:
		outtxt = "Good night."
	else:
		outtxt = ''
	outtxt += "\nBye! "
	if timex >= 6 and timex < 17:
		outtxt += '\nHave a nice day!'
	tnt(outtxt)
"""


"""

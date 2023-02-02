#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=C0413

__version__ = "0.2"

import os
import sys
import shutil
import urllib.parse
import urllib.request

from http import HTTPStatus

import json
import traceback


from CONFIG import appConfig
from user_handler import User, user_handler
from OS_sys import check_internet
from PRINT_TEXT3 import xprint


from pyroboxCore import SimpleHTTPRequestHandler as SH
from pyroboxCore import run as run_server
from pyroboxCore import config as pyrobox_config
from pyroboxCore import DealPostData as DPD
from pyroboxCore import PostError



from Chat_raw2 import basic_output



pyrobox_config.log_location = appConfig.log_location
true = T = True
false = F = False
null = N = None





class Tools:
	def __init__(self):
		self.styles = {
			"equal" : "=",
			"star"    : "*",
			"hash"  : "#",
			"dash"  : "-",
			"udash": "_"
		}

	def text_box(self, *text, style = "equal"):
		"""
		Returns a string of text with a border around it.
		"""
		text = " ".join(map(str, text))
		term_col = shutil.get_terminal_size()[0]

		s = self.styles[style] if style in self.styles else style
		tt = ""
		for i in text.split('\n'):
			tt += i.center(term_col) + '\n'
		return f"\n\n{s*term_col}\n{tt}{s*term_col}\n\n"



tools = Tools()


def join_path(*paths):
	"""join multiple path parts, same as `os.path.join()`
	"""
	return os.path.join(*paths)

#############################################
#             MESSAGE HANDLER               #
#############################################




#############################################
#             SERVER HANDLER                #
#############################################

######### HANDLE GET REQUEST #########

@SH.on_req('GET', '/favicon.ico')
def send_favico(self: SH, *args, **kwargs):
	"""
	re-direct favicon.ico request to cloud to make server less file bloated
	"""
	self.send_response(301)
	self.send_header('Location','https://cdn.jsdelivr.net/gh/RaSan147/py_httpserver_Ult@main/assets/favicon.ico')
	self.end_headers()
	return None



@SH.on_req('GET', '/')
def send_homepage(self: SH, *args, **kwargs):
	"""
	returns the main page as home
	"""
	return self.return_file(join_path(pyrobox_config.ftp_dir, "html_page.html"))

@SH.on_req('GET', '/login')
def send_login(self: SH, *args, **kwargs):
	"""
	returns login.html on login request
	js will redirect here or to home based on wheather user is logged in or not
	"""
	return self.return_file(join_path(pyrobox_config.ftp_dir, "html_login.html"))

@SH.on_req('GET', '/signup')
def send_signup(self: SH, *args, **kwargs):
	"""
	returns signup.html on signup request
	js will redirect here or to home based on wheather user is logged in or not
	"""
	return self.return_file(join_path(pyrobox_config.ftp_dir, "html_signup.html"))


@SH.on_req('GET')
def send_default(self: SH, *args, **kwargs):
	"""
	Serves as default GET request handler and returns files on file system under the hosted directory
	"""
	path = kwargs.get('path', '')
	url_path = kwargs.get('url_path', '')
	spathsplit = kwargs.get('spathsplit', '')
	first = kwargs.get('first', '')
	last = kwargs.get('last', '')


	if os.path.isdir(path):
		parts = urllib.parse.urlsplit(self.path)
		if not parts.path.endswith('/'):
			# redirect browser - doing basically what apache does
			self.send_response(HTTPStatus.MOVED_PERMANENTLY)
			new_parts = (parts[0], parts[1], parts[2] + '/',
							parts[3], parts[4])
			new_url = urllib.parse.urlunsplit(new_parts)
			self.send_header("Location", new_url)
			self.send_header("Content-Length", "0")
			self.end_headers()
			return None
		for index in "index.html", "index.htm":
			index = os.path.join(path, index)
			if os.path.exists(index):
				path = index
				break
		else:
			# return self.list_directory(path)
			self.send_error(HTTPStatus.NOT_FOUND, "File not found")
			return None

	# check for trailing "/" which should return 404. See Issue17324
	# The test for this was added in test_httpserver.py
	# However, some OS platforms accept a trailingSlash as a filename
	# See discussion on python-dev and Issue34711 regarding
	# parseing and rejection of filenames with a trailing slash
	if path.endswith("/"):
		self.send_error(HTTPStatus.NOT_FOUND, "File not found")
		return None



	# else:

	return self.return_file(path)



























def AUTHORIZE_POST(req: SH, post:DPD, post_type=''):
	"""Check if the user is authorized to post

	reads upto line 5
	# args:
		req: the request handler (self of server handler class
		post: instance of DealPostData class
		post_type: post type to check
	"""

	# START
	try:
		post_verify = post.start(post_type)
	except PostError as e:
		req.send_txt(HTTPStatus.BAD_REQUEST, str(e))
		return None
	if not post_verify:
		req.send_txt(HTTPStatus.BAD_REQUEST, post_verify)
		return None


	##################################

	# HANDLE USER PERMISSION BY CHECKING UID

	##################################

	return post_verify


def Get_User_from_post(self: SH, post:DPD, pass_or_uid='password'):
	"""
	Get username and password from post data
	READS UPTO LINE 13
	# args:
		self: the request handler (self of server handler class
		post: instance of DealPostData class
		pass_or_uid: verify using password or uid
		"""

	if not post.match_type('username'): # line 6
		return self.send_error(HTTPStatus.BAD_REQUEST, "Invalid request")
	post.skip() # line 7
	username = post.get(strip=T).decode('utf-8') # line 8
	post.pass_bound() # line 9

	if not post.match_type(pass_or_uid): # line 10
		return self.send_error(HTTPStatus.BAD_REQUEST, "Invalid request")
	post.skip() # line 11
	password = post.get(strip=T).decode('utf-8') # line 12
	post.pass_bound() # line 13

	return username, password

def resp_json(success, message='', **kwargs):
	"""
	returns json.dumps string based on success of an post action
	# args:
		success: bool or string refering wheather the task was successful or not
		message: any message or info the server wants to send to the front end
	"""
	out = {"status": success, "message": message}
	out.update(kwargs)
	return json.dumps(out)


@SH.on_req('POST', hasQ='do_login')
def do_login(self: SH, *args, **kwargs):	
	"""
	handle log in post request.
	1st validate post
	2nd get user from request username and *password*
	2.1 if username or password invalid, then Get_User_from_post(...) will send invalid request error and this will return None
	3rd sends username pass to user_handler and the handler will return if the action was successful or not and a message
	"""
	post = DPD(self)

	valid = AUTHORIZE_POST(self, post, 'login')
	if not valid:
		return self.send_error(HTTPStatus.BAD_REQUEST, "Invalid request")

	data = Get_User_from_post(self, post)
	if not data: return None

	username, password = data

	return self.send_json(user_handler.server_login(username, password))



@SH.on_req('POST', hasQ='do_signup')
def do_signup(self: SH, *args, **kwargs):
	"""
	signup user
	same as `do_login(...)`
	"""
	post = DPD(self)

	valid = AUTHORIZE_POST(self, post, 'signup')
	if not valid:
		return self.send_error(HTTPStatus.BAD_REQUEST, "Invalid request")

	data = Get_User_from_post(self, post)
	if not data: return None

	username, password = data

	return self.send_json(user_handler.server_signup(username, password))


@SH.on_req('POST', hasQ='do_verify')
def do_verify(self: SH, *args, **kwargs):
	"""
	verify user
	same as `do_login`
	"""
	post = DPD(self)

	valid = AUTHORIZE_POST(self, post, 'verify')
	if not valid:
		return self.send_error(HTTPStatus.BAD_REQUEST, "Invalid request")

	data = Get_User_from_post(self, post, 'uid')
	if not data:
		return self.send_error(HTTPStatus.BAD_REQUEST, "Invalid request")

	username, uid = data

	x = resp_json(user_handler.server_verify(username, uid))
	return self.send_json(x)



@SH.on_req('POST', hasQ='bot_manager')
def bot_manager(self: SH, *args, **kwargs):
	"""
	handles user based varius bot queries like bot background, skin texture url etc.
	
	
	"""
	post = DPD(self)

	post_type = AUTHORIZE_POST(self, post)
	if not post_type:
		return self.send_error(HTTPStatus.BAD_REQUEST, "Invalid request")

	data = Get_User_from_post(self, post, 'uid')
	if not data: return None

	username, uid = data

	if post_type == 'get_skin_link':
		skin = user_handler.get_skin_link(username, uid)
		success = bool(skin)
		return self.send_json(resp_json(success, skin))

	elif post_type == 'room_bg':
		skin = user_handler.room_bg(username, uid)
		success = bool(skin)
		return self.send_json(resp_json(success, skin))

	else:
		return self.send_error(HTTPStatus.BAD_REQUEST, "Invalid request")


@SH.on_req('POST', url='/chat', hasQ='send_msg')
def chat(self: SH, *args, **kwargs):
	"""
	handles messaging to bot.
	
	gets message and sent time from post
	and send it to message handlerq
	"""
	post = DPD(self)

	post_type = AUTHORIZE_POST(self, post)
	if not post_type:
		return self.send_error(HTTPStatus.BAD_REQUEST, "Invalid request")

	data = Get_User_from_post(self, post, 'uid')
	if not data: return None

	username, uid = data

	_m = post.match_type('message')
	post.skip()
	message = post.get(strip=T).decode('utf-8')
	post.pass_bound()

	_t = post.match_type('time')
	post.skip()
	_time = post.get(strip=T).decode('utf-8')
	post.pass_bound()

	if not _m or not _t:
		return self.send_error(HTTPStatus.BAD_REQUEST, "Invalid request")


	out = {
		"status": "success",
		"message": '',
		"mid": 1, # message id
		"rid": 1, # reply id
	}
	# print("Message from %s: %s"%(username, msg))

	user = user_handler.collection(username, uid)
	if not user:
		out["status"] = "error"
		out["message"] = "User not found!\nPlease register first."
		out["script"] = ["""(async () => {
			tools.sleep(3000)
			user.redirect_2_login()
		})()"""]
		return self.send_json(out)


	reply = basic_output(message, user, _time=int(_time))

	if isinstance(reply, dict):
		out.update(reply)
	else:
		out["message"] = reply
	return self.send_json(out)



if __name__ == '__main__':
	if 0 and not check_internet():
		pass # now works
		xprint("/rh/No internet connection!\nPlease connect to the internet and try again.\n\n/=//hu/THIS APP IS HIGHLY DEPENDENT ON INTERNET CONNECTION!/=/")
		sys.exit(1)
	run_server(45454, './page', handler=SH)

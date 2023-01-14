#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "0.1"
enc = "utf-8"
__all__ = [
	"HTTPServer", "ThreadingHTTPServer", "BaseHTTPRequestHandler",
	"SimpleHTTPRequestHandler",

]

import os
from DS import Callable_dict
from CONFIG import appConfig
from user_handler import user_handler
from OS_sys import install_missing_libs
from PRINT_TEXT3 import xprint, remove_style


endl = "\n"

class Config:
	def __init__(self):
		# DEFAULT DIRECTORY TO LAUNCH SERVER
		self.ftp_dir = "." # DEFAULT DIRECTORY TO LAUNCH SERVER

		self.IP = None # will be assigned by checking

		# DEFAULT PORT TO LAUNCH SERVER
		self.port= 45454  # DEFAULT PORT TO LAUNCH SERVER

		# UPLOAD PASSWORD SO THAT ANYONE RANDOM CAN'T UPLOAD
		self.PASSWORD= "SECret".encode('utf-8')

		# LOGGING
		self.allow_web_log = True # if you want to see some important LOG in browser, may contain your important information

		# CHECK FOR MISSING REQUEIREMENTS
		self.run_req_check = True

		# FILE INFO
		self.log_location = "./Alice_data/server/"  # fallback log_location = "./"

		self.MAIN_FILE = os.path.realpath(__file__)
		self.MAIN_FILE_dir = os.path.dirname(self.MAIN_FILE)

		print(tools.text_box("Running File: ",self.MAIN_FILE))

		# OS DETECTION
		self.OS = self.get_os()


		# RUNNING SERVER STATS
		self.ftp_dir = self.get_default_dir()
		#print(self.ftp_dir)
		self.dev_mode = True
		self.reload = False



		# ASSET MAPPING
		self.file_list = {}

		self.disabled_func = {}

	def clear_temp(self):
		for i in self.temp_file:
			try:
				os.remove(i)
			except:
				pass






	def get_os(self):
		from platform import system as platform_system

		out = platform_system()
		if out=="Linux":
			if hasattr(sys, 'getandroidapilevel'):
				#self.IP = "192.168.43.1"
				return 'Android'

		return out

	def get_default_dir(self):
		return './page/'


	def address(self):
		return "http://%s:%i"%(self.IP, self.port)





import datetime
import email.utils
import html
import http.client
import io
import mimetypes
import posixpath
import shutil
import socket # For gethostbyaddr()
import socketserver
import itertools
import sys
import time
import urllib.parse
import urllib.request
import contextlib
from functools import partial
from http import HTTPStatus
import importlib.util
import re
from string import Template as _Template # using this because js also use {$var} and {var} syntax and py .format is often unsafe
import threading
import subprocess
import tempfile, random, string, json
import traceback

import hashlib

import F_sys


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
		return (f"\n\n{s*term_col}\n{tt}{s*term_col}\n\n")



tools = Tools()
serverConfig = Config()

# FEATURES
# ----------------------------------------------------------------


#TODO:
# RIGHT CLICK CONTEXT MENU


# INSTALL REQUIRED PACKAGES 
["module", "name_in_pip"]
REQUEIREMENTS= ['requests', 'pafy','mutagen', 'comtypes', 'six', "yt_dlp", ("wikipedia", 'https://github.com/RaSan147/Wikipedia/archive/refs/tags/v1.1.1.zip')]
REQUEIREMENTS_WIN = [("win32api","pywin32"), 'lxml']




# def check_installed(pkg):
# 	return bool(importlib.util.find_spec(pkg))


# def run_pip_install():
# 	dep_modified = False

# 	import sysconfig, pip
# 	for i in REQUEIREMENTS:
# 		if isinstance(i, tuple):
# 			i = i[0]
# 		if check_installed(i):
# 			continue

# 		more_arg = ""
# 		if pip.__version__ >= "6.0":
# 			more_arg += " --disable-pip-version-check"
# 		if pip.__version__ >= "20.0":
# 			more_arg += " --no-python-version-warning"


# 		py_h_loc = os.path.dirname(sysconfig.get_config_h_filename())
# 		on_linux = f'export CPPFLAGS="-I{py_h_loc}";'
# 		command = "" if serverConfig.OS == "Windows" else on_linux
# 		comm = f'{command} {sys.executable} -m pip install  --quiet {more_arg} {i}'

# 		subprocess.call(comm, shell=True)


# 		#if i not in get_installed():
# 		if check_installed(i):
# 			dep_modified = True


# 		else:
# 			print("Failed to load ", i)
# 			serverConfig.disabled_func[i] = True

# 	if dep_modified:
# 		print("Reloading...")
# 		serverConfig.reload = True

if serverConfig.run_req_check:
	# run_pip_install()
	if serverConfig.OS == "Windows":
		REQUEIREMENTS += REQUEIREMENTS_WIN
	#print(REQUEIREMENTS)
	install_missing_libs(REQUEIREMENTS)


if serverConfig.reload == True:
	subprocess.call([sys.executable, serverConfig.MAIN_FILE] + sys.argv[1:])
	sys.exit(0)





#############################################
#             MESSAGE HANDLER               #
#############################################


from user_handler import User, user_handler
from Alice_raw import basic_output
def message_handler(username, uid, msg):
	import json
	out = {
		"status": "success",
		"message": '',
		"mid": 1,
		"rid": 1,
	}
	print("Message from %s: %s"%(username, msg))

	user = user_handler.collection(username, uid)
	if not user:
		out["status"] = "error"
		out["message"] = "User not found!\nPlease register first."
		out["script"] = ["""(async () => {
			tools.sleep(3000)
			user.redirect_2_login()
		})()"""]
		return json.dumps(out)
	
	reply = basic_output(msg, user)
	if isinstance(reply, dict):
		out.update(reply)
	else:
		out["message"] = reply
	return json.dumps(out)




"""HTTP server classes.

Note: BaseHTTPRequestHandler doesn't implement any HTTP request; see
SimpleHTTPRequestHandler for simple implementations of GET, HEAD and POST,
and CGIHTTPRequestHandler for CGI scripts.

It does, however, optionally implement HTTP/1.1 persistent connections,
as of version 0.3.

XXX To do:

- log requests even later (to capture byte count)
- log user-agent header and other interesting goodies
- send error log to separate file
"""




##############################################
#         PAUSE AND RESUME FEATURE           #
##############################################

def copy_byte_range(infile, outfile, start=None, stop=None, bufsize=16*1024):
	'''
	TO SUPPORT PAUSE AND RESUME FEATURE
	Like shutil.copyfileobj, but only copy a range of the streams.
	Both start and stop are inclusive.
	'''
	if start is not None: infile.seek(start)
	while 1:
		to_read = min(bufsize, stop + 1 - infile.tell() if stop else bufsize)
		buf = infile.read(to_read)
		if not buf:
			break
		outfile.write(buf)


BYTE_RANGE_RE = re.compile(r'bytes=(\d+)-(\d+)?$')
def parse_byte_range(byte_range):
	'''Returns the two numbers in 'bytes=123-456' or throws ValueError.
	The last number or both numbers may be None.
	'''
	if byte_range.strip() == '':
		return None, None

	m = BYTE_RANGE_RE.match(byte_range)
	if not m:
		raise ValueError('Invalid byte range %s' % byte_range)

	#first, last = [x and int(x) for x in m.groups()] #

	first, last = map((lambda x: int(x) if x else None), m.groups())

	if last and last < first:
		raise ValueError('Invalid byte range %s' % byte_range)
	return first, last

#---------------------------x--------------------------------



# download file from url using urllib
def fetch_url(url, file = None):
	try:
		with urllib.request.urlopen(url) as response:
			data = response.read() # a `bytes` object
			if not file:
				return data

		with open(file, 'wb') as f:
			f.write(data)
		return True
	except Exception:
		traceback.print_exc()
		return None


def URL_MANAGER(url:str):
	"""
	returns a tuple of (`path`, `query_dict`, `fragment`)\n

	`url` = `'/store?page=10&limit=15&price=ASC#dskjfhs'`\n
	`path` = `'/store'`\n
	`query_dict` = `{'page': ['10'], 'limit': ['15'], 'price': ['ASC']}`\n
	`fragment` = `dskjfhs`\n
	"""

	# url = '/store?page=10&limit=15&price#dskjfhs'
	parse_result = urllib.parse.urlparse(url)


	dict_result = Callable_dict(urllib.parse.parse_qs(parse_result.query, keep_blank_values=True))

	return (parse_result.path, dict_result, parse_result.fragment)



# Default error message template
DEFAULT_ERROR_MESSAGE = """
<!DOCTYPE HTML>
<html lang="en">
<html>
	<head>
		<meta charset="utf-8">
		<title>Error response</title>
	</head>
	<body>
		<h1>Error response</h1>
		<p>Error code: %(code)d</p>
		<p>Message: %(message)s.</p>
		<p>Error code explanation: %(code)s - %(explain)s.</p>
	</body>
</html>
"""

DEFAULT_ERROR_CONTENT_TYPE = "text/html;charset=utf-8"

class HTTPServer(socketserver.TCPServer):

	allow_reuse_address = True	# Seems to make sense in testing environment

	def server_bind(self):
		"""Override server_bind to store the server name."""
		socketserver.TCPServer.server_bind(self)
		host, port = self.server_address[:2]
		self.server_name = socket.getfqdn(host)
		self.server_port = port


class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
	daemon_threads = True


class BaseHTTPRequestHandler(socketserver.StreamRequestHandler):

	"""HTTP request handler base class.

	The various request details are stored in instance variables:

	- client_address is the client IP address in the form (host,
	port);

	- command, path and version are the broken-down request line;

	- headers is an instance of email.message.Message (or a derived
	class) containing the header information;

	- rfile is a file object open for reading positioned at the
	start of the optional input data part;

	- wfile is a file object open for writing.

	IT IS IMPORTANT TO ADHERE TO THE PROTOCOL FOR WRITING!

	The first thing to be written must be the response line.  Then
	follow 0 or more header lines, then a blank line, and then the
	actual data (if any).  The meaning of the header lines depends on
	the command executed by the server; in most cases, when data is
	returned, there should be at least one header line of the form

	Content-type: <type>/<subtype>

	where <type> and <subtype> should be registered MIME types,
	e.g. "text/html" or "text/plain".

	"""

	# The Python system version, truncated to its first component.
	sys_version = "Python/" + sys.version.split()[0]

	# The server software version.  You may want to override this.
	# The format is multiple whitespace-separated strings,
	# where each string is of the form name[/version].
	server_version = "BaseHTTP/" + __version__

	error_message_format = DEFAULT_ERROR_MESSAGE
	error_content_type = DEFAULT_ERROR_CONTENT_TYPE

	# The default request version.  This only affects responses up until
	# the point where the request line is parsed, so it mainly decides what
	# the client gets back when sending a malformed request line.
	# Most web servers default to HTTP 0.9, i.e. don't send a status line.
	default_request_version = "HTTP/0.9"

	def parse_request(self):
		"""Parse a request (internal).

		The request should be stored in self.raw_requestline; the results
		are in self.command, self.path, self.request_version and
		self.headers.

		Return True for success, False for failure; on failure, any relevant
		error response has already been sent back.

		"""
		self.command = None  # set in case of error on the first line
		self.request_version = version = self.default_request_version
		self.close_connection = True
		requestline = str(self.raw_requestline, 'iso-8859-1')
		requestline = requestline.rstrip('\r\n')
		self.requestline = requestline
		words = requestline.split()
		if len(words) == 0:
			return False

		if len(words) >= 3:  # Enough to determine protocol version
			version = words[-1]
			try:
				if not version.startswith('HTTP/'):
					raise ValueError
				base_version_number = version.split('/', 1)[1]
				version_number = base_version_number.split(".")
				# RFC 2145 section 3.1 says there can be only one "." and
				#   - major and minor numbers MUST be treated as
				#	  separate integers;
				#   - HTTP/2.4 is a lower version than HTTP/2.13, which in
				#	  turn is lower than HTTP/12.3;
				#   - Leading zeros MUST be ignored by recipients.
				if len(version_number) != 2:
					raise ValueError
				version_number = int(version_number[0]), int(version_number[1])
			except (ValueError, IndexError):
				self.send_error(
					HTTPStatus.BAD_REQUEST,
					"Bad request version (%r)" % version)
				return False
			if version_number >= (1, 1) and self.protocol_version >= "HTTP/1.1":
				self.close_connection = False
			if version_number >= (2, 0):
				self.send_error(
					HTTPStatus.HTTP_VERSION_NOT_SUPPORTED,
					"Invalid HTTP version (%s)" % base_version_number)
				return False
			self.request_version = version

		if not 2 <= len(words) <= 3:
			self.send_error(
				HTTPStatus.BAD_REQUEST,
				"Bad request syntax (%r)" % requestline)
			return False
		command, path = words[:2]
		if len(words) == 2:
			self.close_connection = True
			if command != 'GET':
				self.send_error(
					HTTPStatus.BAD_REQUEST,
					"Bad HTTP/0.9 request type (%r)" % command)
				return False
		self.command, self.path = command, path


		# gh-87389: The purpose of replacing '//' with '/' is to protect
		# against open redirect attacks possibly triggered if the path starts
		# with '//' because http clients treat //path as an absolute URI
		# without scheme (similar to http://path) rather than a path.
		if self.path.startswith('//'):
			self.path = '/' + self.path.lstrip('/')  # Reduce to a single /

		# Examine the headers and look for a Connection directive.
		try:
			self.headers = http.client.parse_headers(self.rfile,
													 _class=self.MessageClass)
		except http.client.LineTooLong as err:
			self.send_error(
				HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE,
				"Line too long",
				str(err))
			return False
		except http.client.HTTPException as err:
			self.send_error(
				HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE,
				"Too many headers",
				str(err)
			)
			return False

		conntype = self.headers.get('Connection', "")
		if conntype.lower() == 'close':
			self.close_connection = True
		elif (conntype.lower() == 'keep-alive' and
			  self.protocol_version >= "HTTP/1.1"):
			self.close_connection = False
		# Examine the headers and look for an Expect directive
		expect = self.headers.get('Expect', "")
		if (expect.lower() == "100-continue" and
				self.protocol_version >= "HTTP/1.1" and
				self.request_version >= "HTTP/1.1"):
			if not self.handle_expect_100():
				return False
		return True

	def handle_expect_100(self):
		"""Decide what to do with an "Expect: 100-continue" header.

		If the client is expecting a 100 Continue response, we must
		respond with either a 100 Continue or a final response before
		waiting for the request body. The default is to always respond
		with a 100 Continue. You can behave differently (for example,
		reject unauthorized requests) by overriding this method.

		This method should either return True (possibly after sending
		a 100 Continue response) or send an error response and return
		False.

		"""
		self.send_response_only(HTTPStatus.CONTINUE)
		self.end_headers()
		return True

	def handle_one_request(self):
		"""Handle a single HTTP request.

		You normally don't need to override this method; see the class
		__doc__ string for information on how to handle specific HTTP
		commands such as GET and POST.

		"""
		try:
			self.raw_requestline = self.rfile.readline(65537)
			if len(self.raw_requestline) > 65536:
				self.requestline = ''
				self.request_version = ''
				self.command = ''
				self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
				return
			if not self.raw_requestline:
				self.close_connection = True
				return
			if not self.parse_request():
				# An error code has been sent, just exit
				return
			mname = 'do_' + self.command
			if not hasattr(self, mname):
				self.send_error(
					HTTPStatus.NOT_IMPLEMENTED,
					"Unsupported method (%r)" % self.command)
				return
			method = getattr(self, mname)
			method()
			self.wfile.flush() #actually send the response if not already done.
		except (TimeoutError, socket.timeout) as e:
			#a read or a write timed out.  Discard this connection
			self.log_error("Request timed out: %r", e)
			self.close_connection = True
			return

	def handle(self):
		"""Handle multiple requests if necessary."""
		self.close_connection = True

		try:
			self.handle_one_request()
			while not self.close_connection:
				self.handle_one_request()
		except:
			traceback.print_exc()

	def send_error(self, code, message=None, explain=None):
		"""Send and log an error reply.

		Arguments are
		* code:	an HTTP error code
				   3 digits
		* message: a simple optional 1 line reason phrase.
				   *( HTAB / SP / VCHAR / %x80-FF )
				   defaults to short entry matching the response code
		* explain: a detailed message defaults to the long entry
				   matching the response code.

		This sends an error response (so it must be called before any
		output has been generated), logs the error, and finally sends
		a piece of HTML explaining the error to the user.

		"""

		try:
			shortmsg, longmsg = self.responses[code]
		except KeyError:
			shortmsg, longmsg = '???', '???'
		if message is None:
			message = shortmsg
		if explain is None:
			explain = longmsg
		self.log_error("code %d, message %s", code, message)
		self.send_response(code, message)
		self.send_header('Connection', 'close')

		# Message body is omitted for cases described in:
		#  - RFC7230: 3.3. 1xx, 204(No Content), 304(Not Modified)
		#  - RFC7231: 6.3.6. 205(Reset Content)
		body = None
		if (code >= 200 and
			code not in (HTTPStatus.NO_CONTENT,
						 HTTPStatus.RESET_CONTENT,
						 HTTPStatus.NOT_MODIFIED)):
			# HTML encode to prevent Cross Site Scripting attacks
			# (see bug #1100201)
			content = (self.error_message_format % {
				'code': code,
				'message': html.escape(message, quote=False),
				'explain': html.escape(explain, quote=False)
			})
			body = content.encode('UTF-8', 'replace')
			self.send_header("Content-Type", self.error_content_type)
			self.send_header('Content-Length', str(len(body)))
		self.end_headers()

		if self.command != 'HEAD' and body:
			self.wfile.write(body)

	def send_response(self, code, message=None):
		"""Add the response header to the headers buffer and log the
		response code.

		Also send two standard headers with the server software
		version and the current date.

		"""
		self.log_request(code)
		self.send_response_only(code, message)
		self.send_header('Server', self.version_string())
		self.send_header('Date', self.date_time_string())

	def send_response_only(self, code, message=None):
		"""Send the response header only."""
		if self.request_version != 'HTTP/0.9':
			if message is None:
				if code in self.responses:
					message = self.responses[code][0]
				else:
					message = ''
			if not hasattr(self, '_headers_buffer'):
				self._headers_buffer = []
			self._headers_buffer.append(("%s %d %s\r\n" %
					(self.protocol_version, code, message)).encode(
						'utf-8', 'strict'))

	def send_header(self, keyword, value):
		"""Send a MIME header to the headers buffer."""
		if self.request_version != 'HTTP/0.9':
			if not hasattr(self, '_headers_buffer'):
				self._headers_buffer = []
			self._headers_buffer.append(
				("%s: %s\r\n" % (keyword, value)).encode('utf-8', 'strict'))

		if keyword.lower() == 'connection':
			if value.lower() == 'close':
				self.close_connection = True
			elif value.lower() == 'keep-alive':
				self.close_connection = False

	def end_headers(self):
		"""Send the blank line ending the MIME headers."""
		if self.request_version != 'HTTP/0.9':
			self._headers_buffer.append(b"\r\n")
			self.flush_headers()

	def flush_headers(self):
		if hasattr(self, '_headers_buffer'):
			self.wfile.write(b"".join(self._headers_buffer))
			self._headers_buffer = []

	def log_request(self, code='-', size='-'):
		"""Log an accepted request.

		This is called by send_response().

		"""
		if isinstance(code, HTTPStatus):
			code = code.value
		self.log_message('"%s" %s %s',
						 self.requestline, str(code), str(size))

	def log_error(self, format, *args):
		"""Log an error.

		This is called when a request cannot be fulfilled.  By
		default it passes the message on to log_message().

		Arguments are the same as for log_message().

		XXX This should go to the separate error log.

		"""

		self.log_message(format, *args)




	def log_message(self, format, *args):
		"""Log an arbitrary message.

		This is used by all other logging functions.  Override
		it if you have specific logging wishes.

		The first argument, FORMAT, is a format string for the
		message to be logged.  If the format string contains
		any % escapes requiring parameters, they should be
		specified as subsequent arguments (it's just like
		printf!).

		The client ip and current date/time are prefixed to
		every message.

		"""

		message = format % args

		sys.stderr.write("%s - - [%s] %s\n" %
						 (self.address_string(),
						  self.log_date_time_string(),
						  message))

		try:
			# create config.log_location if it doesn't exist
			os.makedirs(serverConfig.log_location, exist_ok=True)
			with open(serverConfig.log_location + 'log.txt','a+') as f:
				f.write("\n\n" + "%s - - [%s] %s\n" %
							(self.address_string(),
							self.log_date_time_string(),
							format%args))
		except Exception:
			traceback.print_exc()

	def version_string(self):
		"""Return the server software version string."""
		return self.server_version + ' ' + self.sys_version

	def date_time_string(self, timestamp=None):
		"""Return the current date and time formatted for a message header."""
		if timestamp is None:
			timestamp = time.time()
		return email.utils.formatdate(timestamp, usegmt=True)

	def log_date_time_string(self):
		"""Return the current time formatted for logging."""
		now = time.time()
		year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
		s = "%02d/%3s/%04d %02d:%02d:%02d" % (
				day, self.monthname[month], year, hh, mm, ss)
		return s

	weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

	monthname = [None,
				 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
				 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

	def address_string(self):
		"""Return the client address."""

		return self.client_address[0]

	# Essentially static class variables

	# The version of the HTTP protocol we support.
	# Set this to HTTP/1.1 to enable automatic keepalive
	protocol_version = "HTTP/1.0"

	# MessageClass used to parse headers
	MessageClass = http.client.HTTPMessage

	# hack to maintain backwards compatibility
	responses = {
		v: (v.phrase, v.description)
		for v in HTTPStatus.__members__.values()
	}


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

	"""Simple HTTP request handler with GET and HEAD commands.

	This serves files from the current directory and any of its
	subdirectories.  The MIME type for files is determined by
	calling the .guess_type() method.

	The GET and HEAD requests are identical except that the HEAD
	request omits the actual contents of the file.

	"""

	server_version = "SimpleHTTP/" + __version__

	if not mimetypes.inited:
		mimetypes.init() # try to read system mime.types
	extensions_map = mimetypes.types_map.copy()
	extensions_map.update({
		'': 'application/octet-stream', # Default
		'.py': 'text/plain',
		'.c': 'text/plain',
		'.h': 'text/plain',
		'.css': 'text/css',
		'html': "text/html",

		'.gz': 'application/gzip',
		'.Z': 'application/octet-stream',
		'.bz2': 'application/x-bzip2',
		'.xz': 'application/x-xz',
	})

	def __init__(self, *args, directory=None, **kwargs):
		if directory is None:
			directory = os.getcwd()
		self.directory = os.fspath(directory)
		super().__init__(*args, **kwargs)

	def do_GET(self):
		"""Serve a GET request."""
		try:
			f = self.send_head()
		except Exception as e:
			traceback.print_exc()
			self.send_error(500, str(e))
			return
				
		if f:
			try:
				self.copyfile(f, self.wfile)
			except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError) as e:
				print(tools.text_box(e.__class__.__name__, e,"\nby ", self.client_address))
			finally:
				f.close()

	def do_HEAD(self):
		"""Serve a HEAD request."""
		try:
			f = self.send_head()
		except Exception as e:
			traceback.print_exc()
			self.send_error(500, str(e))
			return
		if f:
			f.close()

	def do_POST(self):
		"""Serve a POST request."""
		self.range = None # bug patch
		url_path, query, fragment = URL_MANAGER(self.path)





		try:
			dealed = self.deal_post_data()
			# print(tools.text_box("dealed", dealed))
		except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError) as e:
			print(tools.text_box(e.__class__.__name__, e,"\nby ", self.client_address))
			return
		post_type, return_box = dealed
		print(tools.text_box("post_type", post_type, "by", self.client_address))
		data = return_box
		content_type = 'application/json'


		f = io.BytesIO()
		f.write(data.encode('utf-8'))

		length = f.tell()
		f.seek(0)
		self.send_response(200)
		self.send_header("Content-type", content_type)
		self.send_header("Content-Length", str(length))
		self.end_headers()

		self.copyfile(f, self.wfile)

		f.close()


	def deal_post_data(self):

		
		url_path, query, fragment = URL_MANAGER(self.path)


		boundary = None
		num = 0
		blank = 0 # blank is used to check if the post is empty or Connection Aborted


		def make_json(status, info= ''):
			return json.dumps({"status": status, "message": info})

		def get(show=True, strip=False, self=self):
			"""
			show: print line
			strip: strip \r\n at end
			"""
			nonlocal num, remainbytes, blank

			line = self.rfile.readline()

			if line == b'':
				blank += 1
			else:
				blank = 0
			if blank>=20: # allow 20 loss packets
				self.send_error(408, "Request Timeout")
				time.sleep(1) # wait for the client to close the connection

				raise ConnectionAbortedError
			
			if show:
				num+=1
			remainbytes -= len(line)

			if strip and line.endswith(b"\r\n"):
				line = line.rpartition(b"\r\n")[0]

			# print(line)
			return line

		def pass_bound(self=self):
			nonlocal remainbytes
			line = get(0)
			if not boundary in line:
				return make_json(False, "Content NOT begin with boundary")

		def get_type(line=None, self=self):
			nonlocal remainbytes
			if not line:
				line = get()
			try:
				return re.findall(r'Content-Disposition.*name="(.*?)"', line.decode())[0]
			except: return None

		def skip(self=self):
			get(0)

		def run_log_in():
			skip()
			pass_bound()
			i_type = get_type()
			if i_type!="username":
				return make_json(False, "username not found")
			skip()
			username = get(strip=True).decode()
			pass_bound()
			i_type = get_type()
			if i_type!="password":
				return make_json(False, "password not found")
			skip()
			password = get(strip=True).decode()
			pass_bound()
			return user_handler.server_login(username, password)
		
		def run_sign_up():
			skip()
			pass_bound()
			i_type = get_type()
			if i_type!="username":
				return make_json(False, "username not found")
			skip()
			username = get(strip=True).decode()
			pass_bound()
			i_type = get_type()
			print(i_type)
			if i_type!="password":
				return make_json(False, "password not found")
			skip()
			password = get(strip=True).decode()
			pass_bound()
			return user_handler.server_signup(username, password)
		
		def verify_user():
			skip()
			pass_bound()
			i_type = get_type()
			if i_type!="username":
				return make_json(False, "username not found")
			skip()
			username = get(strip=True).decode()
			pass_bound()
			i_type = get_type()
			if i_type!="uid":
				return make_json(False, "id not found")
			skip()
			id = get(strip=True).decode()
			pass_bound()
			return make_json(user_handler.server_verify(username, id))
		

		def handle_message():
			skip()
			pass_bound()
			i_type = get_type()
			if i_type!="username":
				return make_json(False, "username not found")
			skip()
			username = get(strip=True).decode()
			pass_bound()
			i_type = get_type()
			if i_type!="uid":
				return make_json(False, "id not found")
			skip()
			id = get(strip=True).decode()
			pass_bound()
			i_type = get_type()
			if i_type!="message":
				return make_json(False, "message not found")
			skip()
			message = get(strip=True).decode()
			pass_bound()
			return message_handler(username, id, message)
		
		





		while 0:
			line = get()


		content_type = self.headers['content-type']
		print(tools.text_box(content_type))

		if not content_type:
			return "POST", make_json(False, "Content-Type header doesn't exist")
		
		try:
			boundary = content_type.split("=")[1].encode()
		except:
			boundary = None
			# return (False, "Content-Type header doesn't contain boundary")

		remainbytes = int(self.headers['content-length'])

		print(self.path)
		
		pass_bound()# LINE 1
		print(tools.text_box("pass bound"))


		# get post type
		post_type = get_type() # LINE 2
		print(tools.text_box(post_type))
		if post_type=="login":
			skip() # newline
			if url_path == "/do_login":
				print(tools.text_box("run log in"))
				return "login", run_log_in()
			else:
				return (False, "Invalid post request")
		elif post_type=="signup":
			skip()
			if url_path == "/do_signup":
				return "signup", run_sign_up()
			
		elif post_type=="verify":
			skip()
			if url_path == "/do_verify":
				return "verify", verify_user()
		elif post_type=="chat":
			print(tools.text_box("is chat"))
			skip()
			if url_path == "/chat" and query("send_msg"):
				return "chat", handle_message()
		else:
			return (False, "Invalid post request")

		line = get()
		handle_type = line.decode().strip() # post type LINE 3

		pass_bound() #boundary for password or guid of user

		if get_type()=="post-uid":
			skip() # newline
		else:
			return (False, "Unknown User request")

		uid = get() # uid LINE 5

		##################################

		# HANDLE USER PERMISSION BY CHECKING UID

		##################################

		# if handle_type == "check":


		return handle_type


	def return_txt(self, code, msg):

		if not isinstance(msg, bytes):
			encoded = msg.encode('utf-8', 'surrogateescape')
		else:
			encoded = msg

		f = io.BytesIO()
		f.write(encoded)
		f.seek(0)

		self.send_response(code)
		self.send_header("Content-type", "text/html; charset=utf-8")
		self.send_header("Content-Length", str(len(encoded)))
		self.end_headers()
		return f

	def return_file(self, path, first, last, filename=None):
		f = None

		try:
			ctype = self.guess_type(path)

			f = open(path, 'rb')
			fs = os.fstat(f.fileno())

			file_len = fs[6]

			if self.range and first >= file_len: # PAUSE AND RESUME SUPPORT
				self.send_error(416, 'Requested Range Not Satisfiable')
				return None
			# Use browser cache if possible
			if ("If-Modified-Since" in self.headers
					and "If-None-Match" not in self.headers):
				# compare If-Modified-Since and time of last file modification
				try:
					ims = email.utils.parsedate_to_datetime(
						self.headers["If-Modified-Since"])
				except (TypeError, IndexError, OverflowError, ValueError):
					# ignore ill-formed values
					pass
				else:
					if ims.tzinfo is None:
						# obsolete format with no timezone, cf.
						# https://tools.ietf.org/html/rfc7231#section-7.1.1.1
						ims = ims.replace(tzinfo=datetime.timezone.utc)
					if ims.tzinfo is datetime.timezone.utc:
						# compare to UTC datetime of last modification
						last_modif = datetime.datetime.fromtimestamp(
							fs.st_mtime, datetime.timezone.utc)
						# remove microseconds, like in If-Modified-Since
						last_modif = last_modif.replace(microsecond=0)

						if last_modif <= ims:
							self.send_response(HTTPStatus.NOT_MODIFIED)
							self.end_headers()
							f.close()
							return None
			if self.range:
				self.send_response(206)
				self.send_header('Content-Type', ctype)
				self.send_header('Accept-Ranges', 'bytes')


				if last is None or last >= file_len:
					last = file_len - 1
				response_length = last - first + 1

				self.send_header('Content-Range',
								'bytes %s-%s/%s' % (first, last, file_len))
				self.send_header('Content-Length', str(response_length))



			else:
				self.send_response(HTTPStatus.OK)
				self.send_header("Content-Type", ctype)
				self.send_header("Content-Length", str(file_len))

			self.send_header("Last-Modified",
							self.date_time_string(fs.st_mtime))
			self.send_header("Content-Disposition", 'filename="%s"' % (os.path.basename(path) if filename is None else filename))
			self.end_headers()

			return f

		except PermissionError:
			self.send_error(HTTPStatus.FORBIDDEN, "Permission denied")
			return None

		except OSError:
			self.send_error(HTTPStatus.NOT_FOUND, "File not found")
			return None


		except:
			f.close()
			raise



	def send_head(self):
		"""Common code for GET and HEAD commands.

		This sends the response code and MIME headers.

		Return value is either a file object (which has to be copied
		to the outputfile by the caller unless the command was HEAD,
		and must be closed by the caller under all circumstances), or
		None, in which case the caller has nothing further to do.

		"""


		if 'Range' not in self.headers:
			self.range = None
			first, last = 0, 0

		else:
			try:
				self.range = parse_byte_range(self.headers['Range'])
				first, last = self.range
			except ValueError as e:
				self.send_error(400, 'Invalid byte range')
				return None

		path = self.translate_path(self.path)
		# DIRECTORY DONT CONTAIN SLASH / AT END



		url_path, query, fragment = URL_MANAGER(self.path)

		spathsplit = url_path.split("/")

		filename = None

		if self.path == '/favicon.ico':
			self.send_response(301)
			self.send_header('Location','https://cdn.jsdelivr.net/gh/RaSan147/py_httpserver_Ult@main/assets/favicon.ico')
			self.end_headers()
			return None




		print(f'url: {url_path}\nquery: {query}\nfragment: {fragment}')

		########################################################
		#    TO	TEST ASSETS
		#if spathsplit[1]=="@assets":
		#	path = serverConfig.MAIN_FILE_dir+ "/../assets/"+ "/".join(spathsplit[2:])
		#	print("USING ASSETS", path)

		########################################################

		if url_path=='/' and not query:
			return self.return_file(f"{serverConfig.ftp_dir}html_page.html", first=first, last=last)

		elif url_path=="/login":
			return self.return_file(f"{serverConfig.ftp_dir}html_login.html", first=first, last=last)



		elif url_path=="/signup":
			return self.return_file(f"{serverConfig.ftp_dir}html_signup.html", first=first, last=last)
		if query("reload"):
			# RELOADS THE SERVER BY RE-READING THE FILE, BEST FOR TESTING REMOTELY. VULNERABLE
			serverConfig.reload = True

			httpd.server_close()
			httpd.shutdown()

		f = None
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
			else:
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

		return self.return_file(path, first, last, filename)





	def translate_path(self, path):
		"""Translate a /-separated PATH to the local filename syntax.

		Components that mean special things to the local file system
		(e.g. drive or directory names) are ignored.  (XXX They should
		probably be diagnosed.)

		"""
		# abandon query parameters
		path = path.split('?',1)[0]
		path = path.split('#',1)[0]
		# Don't forget explicit trailing slash when normalizing. Issue17324
		trailing_slash = path.rstrip().endswith('/')

		try:
			path = urllib.parse.unquote(path, errors='surrogatepass')
		except UnicodeDecodeError:
			path = urllib.parse.unquote(path)
		path = posixpath.normpath(path)
		words = path.split('/')
		words = filter(None, words)
		path = self.directory


		for word in words:
			if os.path.dirname(word) or word in (os.curdir, os.pardir):
				# Ignore components that are not a simple file/directory name
				continue
			path = os.path.join(path, word)
		if trailing_slash:
			path += '/'

		return os.path.normpath(path) # fix OS based path issue

	def copyfile(self, source, outputfile):
		"""Copy all data between two file objects.

		The SOURCE argument is a file object open for reading
		(or anything with a read() method) and the DESTINATION
		argument is a file object open for writing (or
		anything with a write() method).

		The only reason for overriding this would be to change
		the block size or perhaps to replace newlines by CRLF
		-- note however that this the default server uses this
		to copy binary data as well.

		"""


		if not self.range:
			source.read(1)
			source.seek(0)
			shutil.copyfileobj(source, outputfile)

		else:
			# SimpleHTTPRequestHandler uses shutil.copyfileobj, which doesn't let
			# you stop the copying before the end of the file.
			start, stop = self.range  # set in send_head()
			copy_byte_range(source, outputfile, start, stop)


	def guess_type(self, path):
		"""Guess the type of a file.

		Argument is a PATH (a filename).

		Return value is a string of the form type/subtype,
		usable for a MIME Content-type header.

		The default implementation looks the file's extension
		up in the table self.extensions_map, using application/octet-stream
		as a default; however it would be permissible (if
		slow) to look inside the data to make a better guess.

		"""

		base, ext = posixpath.splitext(path)
		if ext in self.extensions_map:
			return self.extensions_map[ext]
		ext = ext.lower()
		if ext in self.extensions_map:
			return self.extensions_map[ext]
		guess, _ = mimetypes.guess_type(path)
		if guess:
			return guess

		return self.extensions_map[''] #return 'application/octet-stream'




def _get_best_family(*address):
	infos = socket.getaddrinfo(
		*address,
		type=socket.SOCK_STREAM,
		flags=socket.AI_PASSIVE
	)
	family, type, proto, canonname, sockaddr = next(iter(infos))
	return family, sockaddr

def get_ip():
	IP = '127.0.0.1'
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(0)
	try:
		# doesn't even have to be reachable
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except:
		try:
			if serverConfig.OS=="Android":
				IP = s.connect(("192.168.43.1",  1))
				IP = s.getsockname()[0]
				# Assigning this variable because Android does't return actual IP when hosting a hotspot
		except (socket.herror, OSError):
			pass
	finally:
		s.close()
	return IP


def test(HandlerClass=BaseHTTPRequestHandler,
		 ServerClass=ThreadingHTTPServer,
		 protocol="HTTP/1.0", port=8000, bind=None):
	"""Test the HTTP request handler class.

	This runs an HTTP server on port 8000 (or the port argument).

	"""

	global httpd
	if sys.version_info>(3,7,2): # BACKWARD COMPATIBILITY
		ServerClass.address_family, addr = _get_best_family(bind, port)
	else:
		addr =(bind if bind!=None else '', port)

	HandlerClass.protocol_version = protocol
	httpd = ServerClass(addr, HandlerClass)
	host, port = httpd.socket.getsockname()[:2]
	url_host = f'[{host}]' if ':' in host else host
	hostname = socket.gethostname()
	local_ip = serverConfig.IP if serverConfig.IP else get_ip()
	serverConfig.IP= local_ip

	print(tools.text_box(
		f"Serving HTTP on {host} port {port} \n" #TODO: need to check since the output is "Serving HTTP on :: port 6969"
		f"(http://{url_host}:{port}/) ...\n" #TODO: need to check since the output is "(http://[::]:6969/) ..."
		f"Server is probably running on {serverConfig.address()}"
		, style="star"
		)
	)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		print("\nKeyboard interrupt received, exiting.")

	except OSError:
		print("\nOSError received, exiting.")
	finally:
		if not serverConfig.reload:
			sys.exit(0)


class DualStackServer(ThreadingHTTPServer): # UNSUPPORTED IN PYTHON 3.7

	def handle_error(self, request, client_address):
		pass

	def server_bind(self):
		# suppress exception when protocol is IPv4
		with contextlib.suppress(Exception):
			self.socket.setsockopt(
				socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
		return super().server_bind()

	def finish_request(self, request, client_address):
			self.RequestHandlerClass(request, client_address, self,
									directory=args.directory)




if __name__ == '__main__':
	import argparse



	parser = argparse.ArgumentParser()

	parser.add_argument('--bind', '-b', metavar='ADDRESS',
						help='Specify alternate bind address '
							 '[default: all interfaces]')
	parser.add_argument('--directory', '-d', default=serverConfig.get_default_dir(),
						help='Specify alternative directory '
						'[default:current directory]')
	parser.add_argument('port', action='store',
						default=serverConfig.port, type=int,
						nargs='?',
						help='Specify alternate port [default: 8000]')
	args = parser.parse_args()
	if args.directory == serverConfig.ftp_dir and not os.path.isdir(serverConfig.ftp_dir):
		print(serverConfig.ftp_dir, "not found!\nReseting directory to current directory")
		args.directory = "."

	handler_class = partial(SimpleHTTPRequestHandler,
								directory=args.directory)

	serverConfig.port = args.port

	if not serverConfig.reload:
		if sys.version_info>(3,7,2):
			test(
			HandlerClass=handler_class,
			ServerClass=DualStackServer,
			port=args.port,
			bind=args.bind,
			)
		else: # BACKWARD COMPATIBILITY
			test(
			HandlerClass=handler_class,
			ServerClass=ThreadingHTTPServer,
			port=args.port,
			bind=args.bind,
			)

if serverConfig.reload == True:
	subprocess.call([sys.executable, serverConfig.MAIN_FILE] + sys.argv[1:])
	sys.exit(0)

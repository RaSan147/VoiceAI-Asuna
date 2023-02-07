from os import sep as os_sep, makedirs as os_makedirs, walk as os_walk
import os.path
from html import unescape as html_unescape
import urllib.parse
#from os_sys import os_name
import time
from queue import Queue
from random import random

import DATA_sys as Datasys
from PRINT_TEXT3 import xprint
from REGEX_TOOLS import web_re

def get_sep(path):  # fc=0601
	"""returns the separator of the path"""
	if '/' in path:
		return '/'
	
	if '\\' in path:
		return '\\'
	#else:
	return os_sep

def loc(path, _os_name='Linux'):  # fc=0602 v
	"""to fix dir problem based on os

	args:
	-----
		x: directory
		os_name: Os name *Linux"""

	if _os_name == 'Windows':
		return path.replace('/', '\\')
		
	#else:
	return path.replace('\\', '/')


def check_access(path):
	"""
	Check if the user has access to the file.

	path: path to the file
	"""
	if os.path.exists(path):
		try:
			with open(path):
				return True
		except Exception:
			pass
	return False


def get_file_name(directory, mode='dir'):  # fc=0603 v
	"""takes a file directory and returns the last last part of the dir (can be file or folder)

	args:
	-----
		directory: the file directory, only absolute path to support multiple os
		mode: url or file directory
	"""

	if isinstance(directory, bytes): directory = directory.decode()
	if mode == 'url':
		extra_removed = web_re.gen_link_facts(directory)["path"]
		# print(extra_removed)
		if extra_removed[-1] == "/":
			extra_removed = extra_removed[:-1]
		if extra_removed == '':
			name = web_re.gen_link_facts(directory)["host"]
		name = extra_removed.rpartition("/")[2]

		name = Datasys.trans_str(html_unescape(name), {'/\\|:*><?': '-',
														'"': "'",
														"\n\t\r": " "})
		return os.path.basename(name)
	if mode == 'dir':
		return os.path.basename(directory)
	#else:
	raise ValueError

def get_file_ext(directory, mode='dir', no_format='noformat'):  # fc=0604 v
	"""to get the extension of a file directory

	args:
	-----
		directory: file directory relative or direct
		mode: url or file directory ** need to work with url
		no_format: returning format if no file extension was detected *noformat"""

	temp = get_file_name(directory, mode).rsplit('.',1)
	if len(temp) == 1:
		return no_format
	#else:
	return temp[1]


def get_dir(directory, mode='dir'):  # fc=0605 v
	"""takes a file directory and returns the last last part of the dir (can be file or folder)

	args:
	-----
		directory: the file directory, only absolute path to support multiple os
		mode: url or file directory (os based)
	"""

	if mode == 'url':
		extra_removed = web_re.gen_link_facts(directory)['path']

		dirs = extra_removed.split('/')
		if dirs == []:
			return web_re.gen_link_facts(directory)['host']
		while len(dirs) != 0 and dirs[-1] == '':
			dirs.pop()

		if dirs == []:
			return web_re.gen_link_facts(directory)['host']

		directory = Datasys.trans_str(urllib.parse.unquote(html_unescape(dirs[-1])), {'/\\|:*><?': '-', '"': "'"})

		return directory
		
	if mode == 'dir':
		if os.path.basename(directory) == '':
			return os.path.basename(os.path.dirname(directory))
		#else:
		return os.path.basename(directory)
		
	#else:
	raise ValueError

def go_prev_dir(directory, preserve_sep=False):  # fc=0606 v
	"""returns the previous path str of web link or directory
	warning: returns only in linux directory format
	if preserve_sep is True, it will preserve the separator of the directory

	directory: the file directory, only absolute path to support multiple os
	preserve_sep: if True, it will preserve the separator of the directory
	"""

	if not preserve_sep:
		directory = loc(directory, 'Linux')

	sep = get_sep(directory)

	if directory.endswith(sep):
		return sep.join(directory[:-1].split(sep)[:-2]) + sep
		
	#else:
	return sep.join(directory.split(sep)[:-2]) + sep
	
from collections import deque
from DS import Callable_dict
BUSY_FS = Callable_dict()

def reader(direc, read_mode='r', ignore_error=False, output=None,
			encoding='utf-8', f_code='?????', on_missing=None,
			ignore_missing_log=False, timeout=3):  # fc=0607 v
	"""reads file from given directory. If NOT found, returns `None`

	args:
	-----
		direc: file directory
		read_mode: `r` or `rb` *`r`
		ignore_error: ignores character encoding errors *`False`
		output: output type `bin`/`str`/`None` to auto detect *`None`
		encoding: read encoding charset *`utf-8`
		func_code: calling function *`????`
	"""

	if type(read_mode) != str:
		xprint("/rh/Invalid read type./yh/ Mode must be a string data/=/")
		raise TypeError
	if read_mode in ('w', 'wb', 'a', 'ab', 'x', 'xb'):
		xprint("/r/Invaid read mode:/wh/ %s/=//y/ is not a valid read mode.\nTry using 'r' or 'rb' based on your need/=/")
		raise ValueError
	if 'b' in read_mode:
		read_mode = 'rb'

	else:
		read_mode = 'r'
		
	location = loc(direc)

	if not os.path.isfile(location):
		if not ignore_missing_log:
			print(location, 'NOT found to read. Error code: 0607x1')
		return on_missing
		
	
	waited = 0
	token = (time.time(), random())
	if not BUSY_FS(location):
		BUSY_FS[location] = deque()
	
	BUSY_FS[location].append(token)
	
		
	while 1:
		if token==BUSY_FS[location][0]:
			break
		if waited==-1:
			OSError(f"{location} File is busy")
		if timeout and waited>timeout:
			raise TimeoutError(f"Failed to writed {location}")
		time.sleep(.01)
		waited +=.01

		
	#BUSY_FS.add(location)

	try:
		with open(location, read_mode, encoding=None if 'b' in read_mode else encoding) as f:
			out = f.read()
	except PermissionError:
		if not ignore_missing_log:
			xprint(loc(direc), 'failed to read due to /hui/ PermissionError /=/. Error code: 0607x2')
		return on_missing
	finally:
		BUSY_FS[location].popleft()


	if output is None:
		if read_mode == 'r':
			output = 'str'
		else:
			output = 'bin'
	if ignore_error:
		out = Datasys.remove_non_uni(out, '00013', output)

	else:
		if output == 'str' and read_mode == 'rb':
			try:
				out = out.decode()
			except Exception as e:
				xprint(f"/r/failed to decode /hui/{loc(direc)}/=//y/ to the specified character encoding. \nError code: 0607x5")
				raise e
		elif output == 'bin' and read_mode == 'r':
			try:
				out = out.encode(encoding)
			except Exception as e:
				xprint(loc(direc), 'failed to encode to the specified character encoding. \nError code: 0607x5')
				raise e

	return out

def writer(fname, mode, data, direc="", f_code='????',
			encoding='utf-8', timeout=3):  # fc=0608 v
	"""Writing on a file
	
	why this monster?
	> to avoid race condition, folder not found etc

	args:
	-----
		fname: filename
		mode: write mode (w, wb, a, ab)
		data: data to write
		direc: directory of the file, empty for current dir *None
		func_code: (str) code of the running func *empty string
		encoding: if encoding needs to be specified (only str, not binary data) *utf-8
		timeout: how long to wait until free, 0 for unlimited, -1 for immidiate or crash"""

	def write(location):
		if 'b' not in mode:
			with open(location, mode, encoding=encoding) as file:
				file.write(data)
		else:
			with open(location, mode) as file:
				file.write(data)

	if type(mode) != str:
		xprint("\n/rh/Invalid write type./yh/ Mode must be a string data/=/Error code 0608x%s\n" % f_code)
		raise TypeError
	if mode not in ('w', 'wb', 'a', 'ab', 'r+', 'rb+', 'w+', 'wb+', 'a+', 'ab+'):
		xprint('\n/r/Invalid mode\nMust be a Writable Mode/=/Error code 0608x%s\n' % f_code)

	if not isinstance(data, (str, bytes)):
		xprint("/rh/Invalid data type./yh/ Data must be a string or binary data/=/")
		raise TypeError
	mode = mode.replace('+', '').replace('r', 'w')
	
	_direc, fname = os.path.split(fname)
	direc = os.path.join(direc, _direc)

	if any(i in fname for i in ('/\\|:*"><?')):
		# these characters are forbidden to use in file or folder Names
		fname = Datasys.trans_str(fname, {'/\\|:*><?': '-', '"': "'"})

	direc = loc(direc, 'Linux')
	
	# directory and file names are auto stripped by OS
	# or else shitty problems occurs

	direc = direc.strip()
	if not direc.endswith("/"):
		direc+="/"

	fname = fname.strip()
	

	location = loc(direc + fname)
	
	"""
	if any(i in location for i in ('\\|:*"><?')):
		location = Datasys.trans_str(location, {'\\|:*><?': '-', '"': "'"})
	"""
	
	waited = 0
	token = (time.time(), random())
	if not BUSY_FS(location):
		BUSY_FS[location] = deque()
	
	BUSY_FS[location].append(token)
	
		
	while 1:
		if token==BUSY_FS[location][0]:
			break
		if waited==-1:
			OSError(f"{location} File is busy")
		if timeout and waited>timeout:
			raise TimeoutError(f"Failed to writed {location}")
		time.sleep(.01)
		waited +=.01

	
	
	
	# creates the directory, then write the file
	try:
		os_makedirs(direc, exist_ok=True)
	except Exception as e:
		if e.__class__.__name__ == "PermissionError":
			_temp = ''
			_temp2 = direc.split('/')
			_temp3 = 0
			for _temp3 in range(len(_temp2)):
				_temp += _temp2[_temp3] + '/'
				if not os.path.isdir(_temp): 
					break
			raise PermissionError(_temp) from e


	try:
		write(location)

	except Exception as e:
		xprint('/r/', e.__class__.__name__, "occurred while writing", fname, 'in', 'current directory' if direc is None else direc, '/y/\nPlease inform the author. Error code: 00008x' + f_code, '/=/')
		raise e
	finally:
		BUSY_FS[location].popleft()
	
def get_dir_size(start_path = '.', limit=None, return_list= False, full_dir=True):
	"""
	Get the size of a directory and all its subdirectories.

	start_path: path to start calculating from
	limit (int): maximum folder size, if bigger returns "2big"
	return_list (bool): if True returns a tuple of (total folder size, list of contents)
	full_dir (bool): if True returns a full path, else relative path
	"""
	r=[] # if return_list: 
	total_size = 0
	start_path = os.path.normpath(start_path)

	for dirpath, dirnames, filenames in os_walk(start_path, onerror= print):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			if return_list: 
				r.append(fp if full_dir else fp.replace(start_path, "", 1))

			if not os.path.islink(fp):
				total_size += os.path.getsize(fp)
			if limit!=None and total_size>limit:
				print('counted upto', total_size)
				if return_list: return (-1, [])
				return -1
	if return_list: return total_size, r
	return total_size


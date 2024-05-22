"""Network system functions"""

import webbrowser
import time
from random import choice as random_choice


from re import compile as re_compile, sub as re_sub
from os.path import isfile as os_isfile
import os
from hashlib import md5


import urllib3
import urllib3.exceptions
import requests
from bs4 import BeautifulSoup as bs, FeatureNotFound as bs_FeatureNotFound


from headers_file import header_list

#from gen_uuid import random as gen_random_uuid

import F_sys as Fsys
from REGEX_TOOLS import web_re
from print_text3 import xprint
from RESPONSE_CACHE import Cached_Response
from CONFIG import appConfig
NetErrors = (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError,
			 requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,
			 requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema,
			 requests.exceptions.SSLError, urllib3.exceptions.SSLError)

# print(8)  # x

_parser = 'lxml'
try:
	bs('<br>', _parser)
except bs_FeatureNotFound:
	_parser = 'html.parser'


def html2str(data:str):
	data = data.replace("<br>", "\n").replace("<br/>", "\n")
	data = data.replace("&emsp;", "\t")

	data = bs(data, _parser).text

	return data

def str2html(data:str):
	data = data.replace("\n", "<br>")
	data = data.replace("\t", "&emsp;")

	return data




def header_(referer=None):  # fc=0802 v
	"""returns a random header from header_list for requests lib

	referer: if not none, adds referer to the header"""
	header = {'User-Agent': random_choice(header_list)}
	if referer:
		header['Referer'] = referer
	return header

def hdr(header):  # fc=0803 v
	"""returns the index of a header

	args:
	-----
		header: header dict"""

	return str(header_list.index(header['User-Agent']))


def get_link(i, current_link, homepage=None):  # UPDATED
	"""Gets permanent link from relative link.

	Args:
	-----
		i : relative link
		current_link : the link used for getting links inside the page
		homepage : the homepage of the current_link

	Returns:
	--------
		str: permanent link
	"""

	if homepage is None:
		homepage = get_homepage(current_link)

	if i.startswith('#'): 
		frag = gen_link_facts(current_link)['fragment']
		if frag:
			i = current_link.partition('#')[0] + i
	elif i.startswith('?'): 
		no_Q = gen_link_facts(current_link)['noQuery']
		query = gen_link_facts(current_link)['query']
		if query:
			i = no_Q + '?' + query + '&' + i[1:]

		else:
			i = no_Q + '?' + i[1:]

		if frag:
			i += '#' + frag


	elif i.startswith('//'):
		if current_link.startswith('https'):
			i = 'https:' + i
		elif current_link.startswith('http'):
			i = 'http:' + i
		else:
			scheme = gen_link_facts(homepage)['scheme']
			if scheme:
				i = scheme + i
			else:
				i = 'http:' + i

	if i.startswith('../'):
		_temp = current_link
		while i.startswith('../'):
			_temp = Fsys.go_prev_dir(_temp)
			i = i.replace('../', '', 1)
		i = _temp + i # new path

	if i.startswith('/'):
		i = homepage + i

	if i.startswith('./'):
		_current_link = gen_link_facts(current_link)["noQuery"]
		path = gen_link_facts(_current_link)["path"]
		if _current_link.endswith('/'):
			i = _current_link + i[2:]
		else:
			prev_dir = path.rpartition('/')[0]
			i = get_link(i[2:], prev_dir, homepage)



	if '//' not in i:
		temp = homepage
		if temp.endswith('/'):
			if i.startswith('/'):
				i = temp + i[1:]
			else:
				i = temp + i
		else:
			if i.startswith('/'):
				i = temp + i
			else:
				i = temp + '/' + i

	return i


def get_homepage(link):  # fc=0805
	"""Gets the homepage of a link

	Args:
	-----
		link : link to get homepage from
	"""

	x = gen_link_facts(link)

	return x['homepage']

def check_site_active(link, f_code='????', timeout=None):  # fc=0806
	"""Check if the connection is available or not

	args:
	-----
		link: link to check for connection status
		f_code: function caller id
		timeout: set timeout if not none
		"""

	current_header = header_()
	try:
		r = requests.head(link, headers=current_header, timeout=timeout)

		return bool(r)

	except NetErrors as e:
		return False
	except (KeyboardInterrupt, EOFError):
		return False


def check_network_available(self):
	"""check if the computer has internet access"""

	current_header = header_()

	try:
		r = requests.head('https://www.google.com', headers = current_header)
		if not r:
			time.sleep(2)
			_ = requests.head('https://www.bing.com', headers = header_())

		return True

	except NetErrors:
		return False





def open_local_page(port, path=''):  # fc=0809
	"""opens a directory or a file in localhost server using browser

	args:
	-----
		port : port number
		host_dir : desired file or folder directory"""
	webbrowser.open_new_tab(f'http://localhost:{port}/{path}')


def remove_noscript(content):  # fc=080B
	"""Removes <noscript> contents from html to fool my app

	content: HTML content returned by requests.get().content or requests.get().text"""
	if isinstance(content, bytes):
		if b'<noscript>' in content:
			return re_sub(b"(?i)(?:<noscript>)(?:.|\n)*?(?:</noscript>)", b'', content)
	elif isinstance(content, str):
		if '<noscript>' in content:
			return re_sub("(?i)(?:<noscript>)(?:.|\n)*?(?:</noscript>)", '', content)

	return content

def gen_link_facts(link):  # fc=080C
	"""Generates facts for a link #proxy of REGEX_TOOLS.gen_link_facts

	link: link to be checked
	returns: dict of facts"""

	return web_re.gen_link_facts(link)


def get_page(link, referer=False, header=None, cache=False, failed=False, do_not_cache=True,
			session=None, return_none=True, raise_error=False, cache_priority=False):  # fc=080D
	"""Gets a page from the internet and returns the page object

	link: page link
	referer: page referer, default = main_link, None means don't use referer
	header: header string
	cache: get or store the page object from Cached_data.cached_webpages by calling Cached_data.get_webpage or Cached_data.add_webpage
	failed: if failed in previous try
	do_not_cache: if True, don't cache the page object to file
	session: if requests.session is avaialbe
	return_none: if True, return None if page is not found, else return the page object
	raise_error: if True, raise an error if an Error occured while getting the page
	cache_priority: if True, tries to get the page from cache first if available

	"""

	def retry():
		return get_page(link=link,
						referer=False if referer == False else referer,
						cache=cache,
						failed=True,
						do_not_cache=do_not_cache,
						session=session,
						return_none=return_none,
						raise_error=raise_error)

	def get_cache():
		# if CachedData.has_cache(link): # this will be done anyways
		__x = CachedData.get_webpage(link)
		return __x

	if cache and cache_priority:
		page = get_cache()
		if page:
			return page



	if session is None:
		session = requests

	if not referer:
		referer_ = get_homepage(link)
	else:
		referer_ = referer

	if header is None:
		current_header = header_(referer_)
	else:
		current_header = header

	page = None
	try:
		page = session.get(link, headers=current_header, timeout=3)
		if not page:
			if not failed:
				page = retry()
			else:
				if cache:
					page = get_cache()
					if page:
						return page

	except NetErrors as e:
		if not failed:
			page = retry()
		else:
			if cache:
				page = get_cache()
				if page:
					return page


			if raise_error:
				raise e
			else:
				return None

	if cache and page:
		if not do_not_cache:
			CachedData.add_webpage(link, page)
	return page
def link_downloader(link:str, file_loc:str, filename:str, server_error_code:str, internet_error_code:str, overwrite:bool, err_print=True, allow_old=True, proxy=[]):  # fc=080E
	"""
	Just to keep the code clean
		link: link to download
		file_loc: location to save file
		filename: name of file
		server_error_code: error code when server returns error (>200 code)
		internet_error_code: error code when internet is not working
		overwrite: if file is already there, overwrite it
		err_print: if error should be printed
		allow_old: if old file is allowed to be used when failed to download
		proxy: list of proxy links
	"""
	proxy = proxy[:] if proxy else []

	try:
		# check if the proxy link is a list or string, usable or not.
		if isinstance(proxy, str):
			proxy = [proxy]
		elif not isinstance(proxy, list):
			proxy = list(proxy)

	except:
		# invalid proxy type is ignored
		proxy = []


	if isinstance(link , list):
		proxy = link + proxy

	else:
		proxy.insert(0, link) # add link to top of proxy list


	current_header = header_()
	returner = True
	try:
		if not overwrite and  os_isfile(file_loc + filename):
			return True

		file = None

		for link in proxy:
			file = get_page(link, header=current_header, cache=False, raise_error=True, return_none=False)
			if file:
				break
		if file:
			Fsys.writer(filename, 'wb', file.content, file_loc, '0306')
			return True
		else:
			if err_print: xprint("/rh/Error code: %s\nNo internet connection!/=/\nRunning offline mode"%server_error_code)
			returner = False
	except NetErrors as e:
		if err_print: xprint("/rh/Error code: %s\nNo internet connection!/=/\nRunning offline mode"%internet_error_code)
		returner = False

	if not returner and allow_old:
		return os_isfile(file_loc + filename)


class CachedData_ :  # fc=0C00
	def __init__(self):  # fc=0C01
		self.data_vars = ("cached_webpages", "cached_link_facts")
		self.cached_webpages = dict()
		self.cached_link_facts = dict()

	def add_webpage(self, url, response):
		""" Add a webpage to the cache
		url: url of the webpage
		response: response object"""

		# TODO: use JSON

		__x = Cached_Response(status_code=response.status_code, headers=response.headers, content=response.content,
							  encoding=response.encoding, url=response.url)
		file_id = md5(url)
		with open(appConfig.cached_webpages_dir + file_id + '.cache', 'w') as f:
			f.write(repr(__x))
		self.cached_webpages[url] = file_id

	def get_webpage(self, url):
		""" Get a webpage from the cache
		url: url of the webpage """

		if url in self.cached_webpages:
			if os_isfile(appConfig.cached_webpages_dir + self.cached_webpages[url]):
				with open(appConfig.cached_webpages_dir + self.cached_webpages[url] + '.cache', 'r') as f:
					__x = eval(f.read()) # TODO: remove it. use JSON
				return __x

		return None

	def clean_cached_webpages(self):
		""" Cleans the cached_webpages from storage"""
		for i in os.listdir(appConfig.cached_webpages_dir):
			try:
				os.remove(appConfig.cached_webpages_dir + i)
			except:
					pass

	def clear(self):
		"""Cleans both from memory and storage"""
		self.clean_cached_webpages()
		for i in self.data_vars:
			self.__dict__[i].clear()


CachedData = CachedData_()

import pickle
class CachedData_2 :  # fc=0C00
	def __init__(self):  # fc=0C01
		self.data_vars = ("cached_webpages", "cached_link_facts")
		self.cached_webpages = []
		self.cached_link_facts = dict()

		os.makedirs(appConfig.cached_webpages_dir, exist_ok=True)

	def load_old_cache(self):
		f_list = os.scandir(appConfig.cached_webpages_dir)

		for f in f_list:
			name = f.name
			if name.endswith(".cache") and f.is_file():
				self.cached_webpages.append(os.path.splitext(name)[0])

	def add_webpage(self, url, response):
		""" Add a webpage to the cache
		url: url of the webpage
		response: response object"""

		# TODO: use JSON

		__x = Cached_Response(status_code=response.status_code, headers=response.headers, content=response.content,
							  encoding=response.encoding, url=response.url)
		file_id = md5(url.encode("utf-8")).hexdigest()
		with open(appConfig.cached_webpages_dir + file_id + '.cache', 'wb') as f:
			pickle.dump(__x, f)
		self.cached_webpages.append(file_id)

	def has_cache(self, url):
		url_hash = md5(url.encode("utf-8")).hexdigest()
		if url_hash in self.cached_webpages:
			return url_hash

		return False


	def get_webpage(self, url):
		""" Get a webpage from the cache
		url: url of the webpage """


		url_hash = self.has_cache(url)

		if url_hash and  os_isfile(appConfig.cached_webpages_dir + url_hash + '.cache'):
			with open(appConfig.cached_webpages_dir + url_hash + '.cache', 'rb') as f:
				__x = pickle.load(f)
					# __x = eval(f.read()) # TODO: remove it. use JSON
			return __x

		return None

	def clean_cached_webpages(self):
		""" Cleans the cached_webpages from storage"""
		for i in os.listdir(appConfig.cached_webpages_dir):
			try:
				os.remove(appConfig.cached_webpages_dir + i)
			except:
					pass

	def clear(self):
		"""Cleans both from memory and storage"""
		self.clean_cached_webpages()
		for i in self.data_vars:
			self.__dict__[i].clear()


CachedData = CachedData_2()

CachedData.load_old_cache()




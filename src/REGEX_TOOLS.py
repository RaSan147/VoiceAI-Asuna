__all__ = ['web_re']

import re
from re import compile as re_compile
import traceback
from DS import LimitedDict
from typing import Union
from PRINT_TEXT3 import xprint

class WEB_RE:
	# compiled regex tool for getting homepage
	link_extractor = re_compile(
		r'^(?P<noQuery>(?P<homepage>(?P<schema>((?P<scheme>[^:/?#]+):(?=//))?(//)?)(((?P<login>[^:/]+)(?::(?P<password>[^@]+)?)?@)?(?P<host>[^@/?#:]*)(?::(?P<port>\d+)?)?)?)?(?P<path>[^?#]*))(\?(?P<query>[^#]*))?(#(?P<fragment>.*))?')
	# https://regex101.com/r/UKWPmt/1
	# noQuery: https://regex101.com/r/UKWPmt/1
	# homepage: https://regex101.com
	# schema: https://
	# scheme: https
	# login:
	# password:
	# host: regex101.com
	# port:
	# path: /r/UKWPmt/1
	# query: ? part
	# fragment: # part
	link_facts = LimitedDict(max=1000)

	def gen_link_facts(self, link):  # fc=080C
		"""Generates facts for a link

		link: link to be checked"""

		if isinstance(link, bytes):
			link = link.decode()
		if self.link_facts(link):
			return self.link_facts[link]
		facts = dict()

		facts['is link'] = None
		facts['scheme'] = None
		facts['scheme'] = None
		facts['login'] = None
		facts['host'] = None
		facts['port'] = None
		facts['path'] = None
		facts['query'] = None
		facts['fragment'] = None
		facts['noQuery'] = None
		facts['homepage'] = None
		facts['has homepage'] = None
		facts['after homepage'] = None
		facts['needs scheme'] = None
		facts['is absolute'] = None

		x = self.link_extractor.search(link)
		if x:
			facts['is link'] = True
			facts['scheme'] = x.group('schema')
			facts['scheme'] = x.group('scheme')
			facts['login'] = x.group('login')
			facts['host'] = x.group('host')
			facts['port'] = x.group('port')
			facts['path'] = x.group('path')
			facts['query'] = x.group('query')
			facts['fragment'] = x.group('fragment')
			facts['noQuery'] = x.group('noQuery')
			facts['homepage'] = x.group('homepage')

			facts['has homepage'] = (facts['homepage'] is not None)
			facts['after homepage'] = link.startswith('/')
			facts['needs scheme'] = link.startswith('//')
			facts['is absolute'] = (
				facts['scheme'] is not None and facts['host'] is not None)

			self.link_facts[link] = facts

		return facts


web_re = WEB_RE()

def _pp(pattern):
	xprint(f"	/p/Pattern: /=/ {pattern}")


class Tool_belt:
	def __init__(self):
		pass

	def starts(self, patterns: Union[list, str, re.Pattern], string: str, PRINT_PATTERN=False):
		"""checks and returns string if it **starts with** any of the patterns in the given patterns list
		"""
		
		m = None
		if isinstance(patterns, (re.Pattern, str)):
			patterns = [patterns,]

		for ptrn in patterns:
			if isinstance(ptrn, str):
				ptrn = re_compile(f"^{re.escape(ptrn)}", re.IGNORECASE)

			m = ptrn.search(string)
			if m and m.start() == 0:
				if PRINT_PATTERN: _pp(ptrn)
				return m.group(0)
			

	def check(self, patterns: Union[list, str, re.Pattern], string: str, PRINT_PATTERN=False):
		"""checks and returns string if it **has** any of the patterns in the given patterns list
		"""
		m = None
		if isinstance(patterns, (re.Pattern, str)):
			patterns = [patterns,]

		for ptrn in patterns:
			if isinstance(ptrn, str):
				ptrn = re_compile(re.escape(ptrn), re.IGNORECASE)

			m = ptrn.search(string)
			if m:
				if PRINT_PATTERN: _pp(ptrn)
				return m.group(0)
			

	def fullmatch(self, patterns: Union[list, str, re.Pattern], string: str, PRINT_PATTERN=False):
		"""checks and returns string if it **full match** with any of the patterns in the given patterns list
		"""
		if isinstance(patterns, (re.Pattern, str)):
			patterns = [patterns,]

		for i in patterns:
			if isinstance(i, re.Pattern):

				m = i.fullmatch(string)
				if m:
					if PRINT_PATTERN: _pp(i)
					return m.group(0)

			else:
				if string == i:
					if PRINT_PATTERN: _pp(i)
					return i

	def search(self, patterns: Union[list, str, re.Pattern], string: str, PRINT_PATTERN=False):
		"""checks and returns `re.match object` if it has any of the patterns in the given patterns list
		"""
		m = None
		if isinstance(patterns, (re.Pattern, str)):
			patterns = [patterns,]

		for ptrn in patterns:
			if isinstance(ptrn, str):
				ptrn = re_compile(ptrn, re.IGNORECASE)

			m = ptrn.search(string)
			if m:
				if PRINT_PATTERN: _pp(ptrn)
				return m
			


re_tools = Tool_belt()

re_starts = re_tools.starts
re_check = re_tools.check
re_fullmatch = re_tools.fullmatch
re_search = re_tools.search

eol = eos = r"(?:\n|$)"


def C(pattern):
	""" return re.compile of the pattern with ignore case flag
	also add to to_bot_suffix so that it can capture calling by bot name or other nouns
	"""
	pattern = pattern.replace(" ?) ", " ?)") # to avoid double space catcher
	pattern = pattern.replace(" ? ", " ?") # to avoid double space catcher
	pattern = pattern.replace(" *) ", " *)") # to avoid double space catcher
	pattern = pattern.replace(" * ", " *") # to avoid double space catcher
	try:
		return re_compile(pattern, flags=re.IGNORECASE)
	except re.error:
		print("FAILED TO COMPILE:")
		print(pattern)
		print("\n")
		traceback.print_exc()
		exit()

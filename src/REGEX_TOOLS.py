__all__ = ['web_re']

import os
import re
from re import compile as re_compile
import traceback
from DS import LimitedDict
from typing import Union
from print_text3 import xprint
import exrex

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

def _pp(pattern:re.Pattern):
	xprint(f"	/p/Pattern: /=/ {pattern.pattern}")
	flags = []
	if pattern.flags & re.IGNORECASE:
		flags.append('IGNORECASE')
	if pattern.flags & re.MULTILINE:
		flags.append('MULTILINE')
	if pattern.flags & re.DOTALL:
		flags.append('DOTALL')
	if pattern.flags & re.VERBOSE:
		flags.append('VERBOSE')
	if pattern.flags & re.ASCII:
		flags.append('ASCII')
	if pattern.flags & re.DEBUG:
		flags.append('DEBUG')
	if pattern.flags & re.LOCALE:
		flags.append('LOCALE')
	if pattern.flags & re.UNICODE:
		flags.append('UNICODE')
	xprint(f"	/g/Pattern flags: /=/ {flags}")


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
				ptrn = C(f"^{re.escape(ptrn)}")

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
				ptrn = C(re.escape(ptrn))

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
				ptrn = C(re.escape(ptrn))

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

_TEST = True


def C(pattern):
	""" return re.compile of the pattern with ignore case flag
	also add to to_bot_suffix so that it can capture calling by bot name or other nouns
	"""
	if _TEST:
		p = re.sub(r"[^a-z0-9\s\|]", '', pattern, flags=re.I)
		if '  ' in p:
			def highlight(match):
				return f" {'^' * len(match.group(1))} "
			p = re.sub(r"[^a-z0-9\s\|]", '~', pattern, flags=re.I)
			p = re.sub(r" (~+) ", highlight, p, flags=re.I)
			raise Warning("Double SPACE in " +'\n' + pattern + '\n\nHIGHLIGHTED:\n' + p)

	pattern = pattern.replace(" ?) ", " ?)") # to avoid double space catcher
	pattern = pattern.replace(" ? ", " ?") # to avoid double space catcher
	pattern = pattern.replace(" *) ", " *)") # to avoid double space catcher
	pattern = pattern.replace(" * ", " *") # to avoid double space catcher
	try:
		return re_compile(pattern, flags=re.IGNORECASE)
	except re.error:
		xprint("/r/FAILED TO COMPILE:/=/")
		xprint('/c/ Pattern:', repr(pattern), '/=/')
		print("\n")
		traceback.print_exc()
		exit()


def re_vert(pattern_list, print_=True, print_output=False, store_path=None):
	"""
	pattern_list: 	
		[
			[
				[
					complied_pattern_1,
					...
				],
				output,
				intent
			],...
		]

	returns:
		intent
		pattern text,
		>> possible inputs using exrex,
	"""

	markdown = ''

	if store_path:
		# also make the directory if not exists
		store_path = os.path.abspath(store_path)
		store_dir = os.path.dirname(store_path)
		os.makedirs(store_dir, exist_ok=True)

		f = open(store_path, "w", newline='')

	for pattern in pattern_list:
		patterns = pattern[0]
		intent = pattern[2]

		if print_: xprint(f"/hi/Intent: /=/ {intent}")
		markdown += f"## {intent}\n"

		for p in patterns:
			if isinstance(p, str):
				p = C(re.escape(p))
			pattern_text = p.pattern

			if print_: xprint(f"\t/p/Pattern: /=/ {pattern_text}")
			markdown += f"### {pattern_text}\n"

			if print_: xprint(f"\t/g/>> Possible Inputs:/g/")
			markdown += f"#### Possible Inputs\n"

			n = 0

			for i in exrex.generate(pattern_text, limit=2):
				if print_ and print_output: xprint(f"\t\t/c/{i}/=/")
				markdown += f"- {i}\n"

				n += 1

				if n > 2_000_000:
					break

			if print_: xprint(f"\t/g/>> Total Inputs: {n}/=/")

			if print_: print("\n")
			markdown += "\n"

			
			if store_path:
				f.write(markdown)
				markdown = ''
		
		if print_: print("\n\n")
		markdown += "\n\n"

		if store_path:
			f.write(markdown)
			markdown = ''

	if store_path:
		f.close()
		return None


	return markdown


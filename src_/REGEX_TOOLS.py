__all__ = ['web_re']

from re import compile as re_compile
from DS import Callable_dict


class WEB_RE:
	link_extractor = re_compile( r'^(?P<noQuery>(?P<homepage>(?P<schema>((?P<scheme>[^:/?#]+):(?=//))?(//)?)(((?P<login>[^:/]+)(?::(?P<password>[^@]+)?)?@)?(?P<host>[^@/?#:]*)(?::(?P<port>\d+)?)?)?)?(?P<path>[^?#]*))(\?(?P<query>[^#]*))?(#(?P<fragment>.*))?')  # compiled regex tool for getting homepage
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
	link_facts = Callable_dict()


	
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
			facts['is absolute'] = (facts['scheme'] is not None and facts['host'] is not None)

			self.link_facts[link] = facts
		
		return facts

web_re = WEB_RE()
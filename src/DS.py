
class Callable_dict(dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__dict__ = self

	def __call__(self, *key):
		return all([i in self for i in key])


class GETdict(Callable_dict):
	"""
	to set item, use dict["key"] = value for the 1st time,
	then use dict.key or dict["key"] to both get and set value

	but using dick.key = value 1st, will assign it as attribute and its temporary
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__dict__ = self


	def __setitem__(self, key, value):
		super().__setitem__(key, value)

	def __setattr__(self, key, value):
		if self(key):
			self.__setitem__(key, value)
		else:
			super().__setattr__(key, value)

	def  __getattr__(self, __name: str):
		return super().__getitem__(__name)

	def __getitem__(self, __key):
		return super().__getitem__(__key)

class Flag(GETdict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__dict__ = self

	def  __getattr__(self, __name: str):
		try:
			return super().__getitem__(__name)
		except Exception:
			return None

from string import Template as _Template

class Template(_Template):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def __add__(self, other):
		if isinstance(other, _Template):
			return Template(self.template + other.template)
		return Template(self.template + str(other))


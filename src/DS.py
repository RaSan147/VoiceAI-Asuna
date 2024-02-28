from collections import OrderedDict


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

	__setitem__ = Callable_dict.__setitem__
	
	def __setattr__(self, key, value):
		if self(key):
			self.__setitem__(key, value)
		else:
			super().__setattr__(key, value)

	def  __getattr__(self, __name: str):
		if self(__name):
			return self.__getitem__(__name)
		return super().__getattribute__(__name)



class NODict(GETdict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__dict__ = self

	__setitem__ = Callable_dict.__setitem__
	
	def __setattr__(self, key, value):
		try:
			if self(key):
				self.__setitem__(key, value)
			else:
				super().__setattr__(key, value)
		except:
			pass

	def  __getattr__(self, __name: str):
		try:
			if self(__name):
				return self.__getitem__(__name)
			return super().__getattribute__(__name)
		except:
			return Concatable_None()



class Concatable_None():
	# when using + operator with string, will add ""
	# when using + with number or float, will add 0
	# when using + with iterable, will add an empty iterable of same type
	def __bool__(self):
		return False

	def __repr__(self):
		return 'None'

	def __str__(self):
		return 'None'
	
	
	def __eq__(self, other):
		if other is None:
			return True
		else:
			return super().__eq__(other)

	def __add__(self, other):
		if isinstance(other, str):
			return other
		elif isinstance(other, (int, float)):
			return other
		elif isinstance(other, list):
			return other
		elif isinstance(other, dict):
			return other
		else:
			return Concatable_None()

	def __radd__(self, other):
		return self + other
	
	def __contains__(self, item):
		return False
	
	def __getitem__(self, key):
		return Concatable_None()
	
	def __setitem__(self, key, value):
		pass

	def __delitem__(self, key):
		pass

	def __iter__(self):
		return iter([])
	
	def __len__(self):
		return 0
	
	def __call__(self, *key):
		return Concatable_None()
	
	def __getattr__(self, __name: str):
		return Concatable_None()
	

# N = Concatable_None()
# print(N+1)
# print(N+"1")
# print(N+[])
# print(N+{})
# print(N+None)
# print(N+0.0)
# print(N is None) # False
# print(N==None) # True
# print(N==0)
# print(N==0.0)
# print(N==[])
# print(N=={})
# print(N=="")
# print(N==1)


class Flag(GETdict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__dict__ = self

	__getitem__ = GETdict.get
	__getattr__ = GETdict.get



class LimitedDict(OrderedDict, Callable_dict):
	def __init__(self, *args, max=0, **kwargs):
		self._max = max
		super().__init__(*args, **kwargs)

	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		if self._max > 0:
			if len(self) > self._max:
				self.popitem(False)

class str2(str):
	def __joiner__(self, joiner="\n\n"):
		self.joiner = joiner
	def __add__(self, other):
		if not hasattr(self, "joiner"):
			self.__joiner__()
		self = str2(self.joiner.join([self, other]))
		return self

	def example(self):
		x = str2("abc")
		print(x + "123")
		print(repr(x+"123"))
		print(x=="")

#x = str2("abc")
#x.example()

from string import Template as _Template

class Template(_Template):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def __add__(self, other):
		if isinstance(other, _Template):
			return Template(self.template + other.template)
		return Template(self.template + str(other))



from queue import Queue

class Zfunc(object):
	"""Thread safe sequncial printing/queue task handler class"""

	__all__ = ["new", "update"]
	def __init__(self, caller, store_return=False):
		super().__init__()

		self.queue = Queue()
		# stores [args, kwargs], ...
		self.store_return = store_return
		self.returner = Queue()
		# queue to store return value if store_return enabled

		self.BUSY = False

		self.caller = caller

	def next(self):
		""" check if any item in queje and call, if already running or queue empty, returns """
		if self.queue.empty() or self.BUSY:
			return None

		self.BUSY = True
		args, kwargs = self.queue.get()

		x = self.caller(*args, **kwargs)
		if self.store_return:
			self.returner.put(x)

		self.BUSY = False

		if not self.queue.empty():
			# will make the loop continue running
			return True


	def update(self, *args, **kwargs):
		""" Uses xprint and parse string"""

		self.queue.put((args, kwargs))
		while self.next() is True:
			# use while instead of recursion to avoid recursion to avoid recursion to avoid recursion to avoid recursion to avoid recursion to avoid recursion to avoid recursion.... error
			pass



	def new(self, caller, store_return=False):
		self.__init__(caller, store_return)


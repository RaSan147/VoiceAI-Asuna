
class Callable_dict(dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__dict__ = self

	def __call__(self, *key):
		return all([i in self for i in key])


class GETdict(Callable_dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__dict__ = self

	
	def __setitem__(self, key, value):
		super().__setitem__(key, value)

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

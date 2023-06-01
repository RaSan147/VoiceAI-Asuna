import sys

import basic_conv_pattern as Constants
from OS_sys import os_name, os_system
from PRINT_TEXT3 import xprint
from NUM_sys import flatten_array

""" Contains Input and Output functions """

def sys_write(msg:str=""):  # fc=0501 v
	"""Use this function to write to STDOUT

	args:
	-----
		msg: message to write (MUST BE STR)"""

	sys.stdout.write(msg)

def clear_screen():  # fc=0501 v
	"""clears terminal output screen"""

	if os_name == "Windows":
		os_system('cls')
	else:
		os_system('clear')

def delete_last_line(lines=1):  # fc=0502 v
	"""Use this function to delete the last line in the STDOUT

	args:
	-----
		lines: total number of lines *1
			0 to delete current line"""

	# return 0
	if lines == 0:
		sys_write('\n')
		delete_last_line()
		return 0

	for _ in range(lines):
		# cursor up one line
		sys_write('\x1b[1A')

		# delete last line
		sys_write('\x1b[2K')


def safe_input(msg='', i_func=input, o_func=xprint,
				on_error=KeyboardInterrupt):  # fc=0504 v
	"""gets user input and returns str

	args:
	-----
		msg: the message to show for asking input *`empty string`
		i_func: the function used for input *`input()`
		o_func: the function used for msg print *`xprint()`
		on_error: What to do when `^C` pressed *`raise KeyboardInterrupt` or `return None`"""

	o_func(msg, end='')
	try:
		box = i_func()
		return box
	except EOFError:
		if on_error == KeyboardInterrupt:
			raise KeyboardInterrupt
		else:
			return on_error
	except KeyboardInterrupt:
		if on_error == KeyboardInterrupt:
			raise KeyboardInterrupt
		else:
			return on_error

def asker(out='', default=None, True_False=(True, False),
			extra_opt=tuple(), extra_return=tuple(),
			i_func=input, o_func=xprint, on_error=KeyboardInterrupt,
			condERR=Constants.condERR, no_bool=False):  # fc=0505 v
	"""asks for yes no or equivalent inputs

	args:
	-----
		out: `xprint` text to ask tha question *`empty string`
		default: default output for empty response *`None`
		True_False: returning data instead of True and False *`(True, False)`
		extra_opt: Add additional options with Yeses and Nos *must be array of single options*
		extra_return: Returns output according to `extra_ops`
		i_func: the function used for input *`input()`
		o_func: the function used for msg print *`xprint()`
		on_error: What to do when `^C` pressed *`raise KeyboardInterrupt` or `return None`
		no_bool: won't take yes no as input [extras required] *`False`"""

	if len(extra_opt) != len(extra_return):
		xprint('/r/Additional options and Additional return data don\'t have equal length/=/')
		raise TypeError

	if no_bool:
		if len(extra_opt) < 1:
			xprint('/r/With no_bool arg, you must give at least 1 extra option [extra_arg & extra_return]/=/')
			raise TypeError

	Ques2 = safe_input(out, i_func, o_func, on_error).lower()
	if default is not None and Ques2 == '':
		return default
	# Ques2 = Ques2
	while Ques2 not in (tuple() if no_bool else Constants.cond) + flatten_array(extra_opt, tuple):
		Ques2 = safe_input(condERR, i_func, o_func, on_error).lower()
	# Ques2 = Ques2

	if not no_bool and Ques2 in Constants.cond:
		if Ques2 in Constants.yes:
			return True_False[0]
		else:
			return True_False[1]
	else:
		return extra_return[extra_opt.index(Ques2)]



from queue import Queue
class Zfunc(object):
	"""
	UNDER TESTING

	Thread safe sequncial printing/queue task handler class
	"""

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
		self.__init__(caller=caller, store_return=store_return)

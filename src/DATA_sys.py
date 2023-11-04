import json
import io
from types import FunctionType

from functools import reduce as functools_reduce
from operator import iconcat as operator_iconcat


from PRINT_TEXT3 import xprint


"""Data types and conversion functions"""

def remove_duplicate(seq, return_type=list):  # fc=0901 v
	"""removes duplicates from a list or a tuple
	also keeps the array in the same order

	args:
	-----
		seq: `tuple`|`list` to remove dups
		return_type: type of array to return"""

	return return_type(dict.fromkeys(seq))

def remove_non_ascii(text, f_code='????'):  # fc=0902 v
	"""[DEPRECATED] [STILL WORKS] removes ascii characters from a string

	args:
	-----
		test: text to remove non ASCII
		f_code: The function Code called this function"""

	return ''.join([i if ord(i) < 128 else '' for i in text])


def remove_non_uni(text, f_code='????', types='str', encoding='utf-8'):  # fc=0903 v
	"""Converts a string or binary to unicode string or binary by removing all non unicode char

	args:
	-----
		text: str to work on
		f_code: caller func code
		types: output type ('str' or 'bytes')
		encoding: output encoding *utf-8"""

	try:
		if type(text) == str:
			text = text.encode(encoding, 'ignore')
			if types == 'bin':
				return text
			return text.decode(encoding)
		if types == 'bin':
			return text.decode(encoding, 'ignore').encode(encoding)
		return text.decode(encoding, 'ignore')
	except Exception as e:
		xprint("/r/Failed to remove non-Unicode characters from string.\nError code: 00018x", f_code, '/y/\nPlease inform the author./=/')
		return remove_non_ascii(text, f_code)

def trans_str(txt, dicts):  # fc=0904 v
	"""replaces all the matching characters of a string for multiple times

	args:
	-----
		txt: string data
		dicts: dict of { find : replace }"""

	for i in dicts.keys():
		a = dicts[i]
		for j in i:
			txt = txt.replace(j, a)
	return txt

def flatten2D(arr):  # fc=0905
	functools_reduce(operator_iconcat, arr, [])

def is_json(data, raise_=False): # fc=xxxx
	"""checks if a string is a valid json
	data: string or file object or ioBase to check
	raise_: if True, raises the error instead of returning None
	returns: True if valid, False if invalid"""

	if isinstance(data, (io.TextIOBase,
	io.BufferedIOBase,
	io.RawIOBase,
	io.IOBase)):
		func = json.load
	elif isinstance(data, (str, bytes)):
		func = json.loads
	else:
		return False
	try:
		func(data)
		return True
	except Exception as e:
		# if logger: traceback.print_exc()
		if raise_: raise e
		return False


def call_or_return(arg, *i_args, **i_kwargs):
	"""
	if `arg` is callable it will call it with `i_args` and return
	
	else it will return it as what it is
	"""
	if isinstance(arg, FunctionType):
		return arg(*i_args, **i_kwargs)

	return arg





class SetEncoder (json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, set):
			return list(obj)
		return json.JSONEncoder.default(self, obj)




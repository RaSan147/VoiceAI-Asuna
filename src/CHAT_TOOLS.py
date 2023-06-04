from random import choice, shuffle
import re

def if_list(obj):
	if len(obj)==1 and not isinstance(obj[0], str):
		obj = obj[0]
		
	return list(obj)

def Rchoice(*args, blank=0):
	"""
		return `random choice` from (args and blank `""`)
	"""
	args = if_list(args)
	b = ['']*blank
	return choice(args + b)

def Rshuffle(*args):
	args = if_list(args)
	shuffle(args)
	return args
	


def list_merge(li:list):
	txt = ' '.join(li)
	txt = re.sub(r'\s{2,}', ' ', txt)

	return txt.strip()
	
def merge(*args):
	args = if_list(args)
	
	return list_merge(args)

def shuf_merge(*args):
	args = if_list(args)
	
	return list_merge(Rshuffle(args))







if __name__ == "__main__":
	print(shuf_merge(['string1', 'string2', 'string3']))
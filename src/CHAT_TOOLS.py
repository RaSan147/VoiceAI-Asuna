from random import choice, shuffle
import re

def Rchoice(*args, blank=0):
	b = ['']*blank
	return choice([*args, *b])
	
def Rshuffle(*args):
	args = list(args)
	shuffle(args)
	return args
	
def list_merge(li):
	txt = ' '.join(li)
	txt = re.sub(r'\s+', ' ', txt)
	
	return txt
	
def shuf_merge(*args):
	return list_merge(Rshuffle(*args))

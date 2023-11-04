from typing import List
from random import choice, shuffle
import re

from bs4 import BeautifulSoup as bs

def if_list(obj):
	if isinstance(obj, str):
		# fix list("ab") = ["a", "b"]
		obj = [obj]
	if len(obj)==1 and not isinstance(obj[0], str):
		obj = obj[0]
	
		
	return list(obj)

def Rchoice(*args, blank=0):
	"""
		return `random.choice` from (args and blank `""`)
	"""
	args = if_list(args)
	b = ['']*blank
	return choice(args + b)

def Rshuffle(*args):
	args = if_list(args)
	shuffle(args)
	return args
	


def list_merge(li:List):
	txt = ' '.join(li)
	txt = re.sub(r'\s{2,}', ' ', txt)

	return txt.strip()
	
def merge(*args):
	args = if_list(args)
	
	return list_merge(args)

def shuf_merge(*args):
	args = if_list(args)
	
	return list_merge(Rshuffle(args))



def for_voice(message:dict):
	text = message["message"]
	render = message["render"]

	if render == "innerHTML":
		text = bs(text, 'html.parser').text

	text = re.sub(r'\*[a-zA-Z\s]+\*', '', text)
	text = text.encode('ascii', 'ignore').decode('ascii')

	return text



if __name__ == "__main__":
	print(shuf_merge(['string1', 'string2', 'string3']))
from random import choice, shuffle
import re
from REGEX_TOOLS import re_check, re_fullmatch, re_starts
from basic_re_pattern import C

from CHAT_TOOLS import Rshuffle, Rchoice, shuf_merge, list_merge


from OS_sys import null


from user_handler import User
from msg_class import MessageObj

from DS import NODict
def patterns(user:User=NODict(), msg:MessageObj=MessageObj(test=True)):
	"""
	context: Counter object to keep track of previous message intents
	check_context: function to check if something is in the prev msg intent (context)


	"""
	return [
[
	[
		C(r"((yo)?u|y(a|o)) (doing?|up ?to)"),
	],
	(Rchoice("Just thinking about you"+ Rchoice(" and waiting for your text", blank=2)+".",
		"Nothing particular... Just chatting with you ☺️",
		"Just staring at you🥰",
		"Wondering about you 😄"
		)
	),
	"(what)_ai_doing"
],


][::-1]




__ptn = patterns()

if __name__ != '__main__':
	from REGEX_TOOLS import re_vert
	import os
	filename = os.path.basename(__file__)
	store_path = f"patterns.tmp/{filename}.md"
	markdown = re_vert(__ptn, store_path=store_path)



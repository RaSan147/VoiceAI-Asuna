from REGEX_TOOLS import re_check, re_is_in, re_starts
from basic_conv_re_pattern import C

from CHAT_TOOLS import Rshuffle, Rchoice, shuf_merge, list_merge

from OS_sys import null
from collections import Counter
def patterns(context=Counter(), check_context=null):
	"""
	context: Counter object to keep track of previous message intents
	check_context: function to check if someting is in the prev msg intent (context)
	"""
	
	return [
[
	[
		C(r"(speak|talk|tell)( it)?( aloud| out loud)?( to me)?$"),
	],
	( Rchoice("Sorry, I lost my headphones",
			"Sorry, I don't have a voice device yet",
			"I'll buy a headset soon",
			"Sorry, Can't talk right now",
			"Sorry, I'm not allowed to talk now") +
		Rchoice(" 😅", " ~", "...", blank=1)
	),
	"can_you_speak"
],
[
	[
		C(r"(voice )?(listen|hear)(( to)? ?(me|my voice|what(ever)? i (say|speak)))?$"),
	],
	( Rchoice("Sorry, I lost my headphones",
			"Sorry, I don't have a headset yet",
			"I'll buy a headset soon",
			"Sorry, Can't hear you right now") +
		Rchoice(" so that i can hear you", blank=1) +
		Rchoice(" 😅", " ~", "...", blank=1)
	),
	"can_you_speak"
],
[
	[
		C(r"voice( listen)?( to me)?$"),
	],
	( Rchoice("Sorry, I lost my headphones",
			"Sorry, I don't have a headset yet",
			"I'll buy a headset soon",
			"Sorry, Can't hear you right now") +
		Rchoice(" so that i can hear you", blank=1) +
		Rchoice(" 😅", " ~", "...", blank=1)
	),
	"can_you_speak"
],



]

patterns()

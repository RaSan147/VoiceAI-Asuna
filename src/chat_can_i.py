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
		C(r"(ask|say|tell) ((yo)?u|y(a|o)) (something?|smtg)"),
	],
	( Rchoice(
		"Sure! Ask away",
		"Of course. I'll try my best to answer",
		"Yes indeed... Thats why I am here.",
		"Go ahead. But I might disappoint you "
	) +
		Rchoice(" 😅", " 😁", " ~", "...", blank=1)
	),
	"can_i_ask_u"
],
[
	[
		C(r"help ((yo)?u|y(a|o))( with anything)?"),
		C(r"(suggest|report) ((yo)?u|y(a|o))? ?(an? )?(something?|smtg|issue|problem )?"),
	],
	( Rchoice(
		"Sure!",
		"Of course",
		"Yes indeed...",
		"Go ahead."
	) +
	"Just go here and create a new issue.<br><a href='https://github.com/RaSan147/VoiceAI-Asuna/issues' target='_blank'>Github issue</a>"
	),
	"can_i_report_u"
],
[
	[
		C(r"(listen|hear) ((yo)?u|y(a|o))( voice)?"),
	],
		( Rchoice("Sorry, I lost my headphones",
			"Sorry, I don't have a voice device yet",
			"I'll buy a headset soon",
			"Sorry, Can't talk right now",
			"Sorry, I'm not allowed to talk now") +
		Rchoice(" 😅", " ~", "...", blank=1)
	),
	"can_i_hear_you"
],



]

patterns()

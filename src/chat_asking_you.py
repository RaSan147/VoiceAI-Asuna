from REGEX_TOOLS import re_check, re_fullmatch, re_starts, eos
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
		"die",
		"be dead",
		C("(be )?expired?"),
		"shut down",
		C("(be )?turn(ed)? off"),
		C('disconnect(ed)?'),
	],
	(
		Rchoice(
			"As long as the server runs",
			'As long as you support the <a href="https://github.com/RaSan147/VoiceAI-Asuna" target="_blank">Creator</a>',
			"As long as you support me"
		) + ' I' + Rchoice("'ll", " will") + ' ' +
		Rchoice("try", "do") + "my best to " + Rchoice("stay", "be") + " " +
		Rchoice("active", "available", "online") + '.'
	),
	"will_you_die"
],

[
	[
		C("mate|reproduce|fuck|(have )?sex|make (child(ren)?|baby)|suck")
	],
	(
		Rchoice("Honestly", "Well", "Well you see", blank=2) + ' I ' +
		Rchoice("am not interested", 
				"don't have interest in doing such things",
				"don't want to do so",
				"don't feel like it",
				"don't think its the right time and place to do so") + 
		Rchoice(" right now.", " currently.", 
				" at this moment.", ".", "...", 
				blank=1)
	),
	"can_you_fuck"
]
]


patterns()
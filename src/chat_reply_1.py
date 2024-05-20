from REGEX_TOOLS import re_check, re_fullmatch, re_starts
from basic_re_pattern import C, IM___, YOU___, YOUR___, YOURE___, AuxV___, DEFINE_WHAT___, WHAT___, OKAY___
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
		C(rf"{IM___} "
			"(doing? )?"
			f"(fine|good|great|{OKAY___}|well)")
	],
	(
		Rchoice(
			Rchoice("Good", "Glad") + " to hear that",
			"Thats good to hear",
			"Great",
			) +  '.'
	),
	"i_am_fine"
],
[
	[
		C(rf"{IM___} "
			"(doing? |feeling? )?"
			f"(bad|not good|not great|not {OKAY___}|not well|unwell|sick|ill|depressed|sad|angry|mad|upset|annoyed|frustrated|bored|lonely|alone|anxious|nervous|stressed|stressed out|worried|scared|frightened|fearful|terrified|afraid|confused|lost|conflicted)"),

		C(rf"{IM___} "
			"not (doing? |feeling? )?"
			f"(good|great|{OKAY___}|well|fine)"),
	],
	(
		Rchoice(
			Rchoice("Sorry to hear that", "Thats too bad") + " to hear that",
			"I'm sorry to hear that",
			) +  ' ' + 
			"I hope you " + 
			Rchoice("feel better soon", "get well soon", "get better soon") + '.'
	),
	"i_am_feeling_bad"
],	
[
	[
		C(rf"{IM___} "
			"(sleepy|sleep deprived|tired|exhausted)"),
	],
	(
		Rchoice("Try to ", "Please", "You should", blank=1) +
		Rchoice(
			Rchoice("Get", "Have", "Take") + " some ",
			Rchoice("sleep", "rest"),
		) +  '.',
		Rchoice("Please take care of yourself...", "Please try to relax") + '.' +
		Rchoice("I'll be here when you come back", "I'll be here when you feel better", "You are important to me", blank=2)
	),
	'i_am_sleepy'
],
[
	[
		C(rf"{IM___} "
			"(hungry|starving|famished)")
	],
	(
		Rchoice("Try to ", "Please", "You should", blank=1) +
		Rchoice(
			Rchoice("Get", "Have", "Take") + " some ",
			Rchoice("food", "snack", "meal"),
		) +  '.',
		Rchoice("Please take care of yourself...", "Please try to relax") + '.' +
		Rchoice("I'll be here when you come back", "I'll be here when you feel better", "You are important to me", blank=2)
	),
	'i_am_hungry'
],
[
	[
		C(rf"{IM___} "
			"(thirsty|dehydrated)")
	],
	(
		Rchoice("Try to ", "Please", "You should", blank=1) +
		Rchoice(
			Rchoice("Get", "Have", "Take") + " some ",
			Rchoice("water", "drink"),
		) +  '.',
		Rchoice("Please take care of yourself...", "Please try to relax") + '.' +
		Rchoice("I'll be here when you come back", "I'll be here when you feel better", "You are important to me", blank=2)
	),

	'i_am_thirsty'
],



















]

__ptn = patterns()

if __name__ != '__main__':
	from REGEX_TOOLS import re_vert
	import os
	filename = os.path.basename(__file__)
	store_path = f"patterns.tmp/{filename}.md"
	markdown = re_vert(__ptn, store_path=store_path)



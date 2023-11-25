from REGEX_TOOLS import re_check, re_fullmatch, re_starts, eos
from basic_conv_re_pattern import C, An___

from CHAT_TOOLS import Rshuffle, Rchoice, shuf_merge, list_merge

from OS_sys import null


from user_handler import User
from msg_class import MessageObj

def patterns(user:User, msg=MessageObj):
	"""
	context: Counter object to keep track of previous message intents
	check_context: function to check if something is in the prev msg intent (context)


	"""

	return [

[
	[
		C(rf"{An___}? ai|(ro)?bot|chat( |-)?(bot|gpt)"),
	], # hiiii/heey there Asuna
	(
		Rchoice(
			"Well, I am not an smart AI yet, but I'm learning to be one",
			"I'm your chat partner, but I'm not that much knowledgeable yet",
			"I am trained on small dataset, so I can't call myself an smart AI yet",
			"I don't have the ability of an Chat GPT like AI yet, but I'm trying",
		) +  '.'
	),

	"are_you_ai"
],
[
	[
		C(r"awake"),
	], # hiiii/heey there Asuna
	(
		Rchoice(
			"Yup, I'm awake",
			"Yup, I'm here",
			"Yes I'm always awake",
			"Yup, I'm always here",
			"Yeah",
		) + " " +
		Rchoice(
			"and ready to help you",
			"and ready to talk to you",
			"and ready to chat with you",
			"and ready to do anything for you",
			blank=2
		) + Rchoice('.', '...', '!',  '~', blank=1)
	),

	"are_you_awake"
],
[
	[
		C(rf"{An___}? boy( or g[iu]rl)?"),
		C(rf"{An___}? g[iu]rl( or boy)?"),
		C(rf"{An___}? m[ae]n( or wom[ae]n)?"),
		C(rf"{An___}? wom|ae]n( or m[ae]n)?"),
		C(rf"{An___}? male( or female)?"),
		C(rf"{An___}? female( or male)?"),

	], # hiiii/heey there Asuna
	(
		Rchoice(
			"Well, of course I am girl. 🤨",
			"As you can see, I am a woman.",
			"I am a girl and you clearly know that. 😬",
		)
	),

	"are_you_boy"
],
[
	[
		C(rf"{An___}? (gay|geh|gah)" + eos),
		C(rf"{An___}? lesb(o|ian)?"),
		C(rf"{An___}? straight"),
		C(rf"{An___}? trans"),
		C(rf"{An___}? bisex")
	], # hiiii/heey there Asuna
	(
		Rchoice(
			"Well, of course I am straight . 🤨",
			"As you can see, I am a straight.",
			"I am straight and you clearly know that. 😬",
		)
	),

	"are_you_lesb"
],





]
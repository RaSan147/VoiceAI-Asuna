from collections import Counter

from REGEX_TOOLS import re_check, re_is_in, re_starts
from basic_conv_re_pattern import C

from CHAT_TOOLS import Rshuffle, Rchoice, shuf_merge, list_merge

from OS_sys import null

def patterns(context=Counter(), check_context=null):
	"""
	context: Counter object to keep track of previous message intents
	check_context: function to check if someting is in the prev msg intent (context)


	"""
	return [

[
	[
		C(r"(an? )?ai|(ro)?bot|chat( |-)?(bot|gpt)"),
	], # hiiii/heey there Asuna
	(
		Rchoice(
			"Well, I am not an AI yet, but I'm learning to be one",
			"I'm your chat partner, but I'm not an AI yet",
			"I am trained on small dataset, so I can't call myself an AI yet",
			"I don't have the ability of an AI yet, but I'm trying"
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
			"Yup, I'm always here"
			"Yeah"
		) +  
		Rchoice(
			" and ready to help you",
			" and ready to talk to you",
			" and ready to chat with you",
			" and ready to do anything for you",
			blank=2
		) + Rchoice('.', '...', '!',  '~', blank=1)
	),

	"are_you_awake"
],






]
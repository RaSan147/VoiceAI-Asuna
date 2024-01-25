from REGEX_TOOLS import re_check, re_fullmatch, re_starts
from basic_conv_re_pattern import C, happy_emj, sad_emj, AuxV___, YOURE___, YOUR___, YOU___, PLEASE___, WHAT___, WHAT___, WHEN_WHAT___, WHO_WHAT___, WHEN___, eos, DEFINE_WHAT___, eol


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
		C(rf"{WHAT___}?{YOUR___} (nick|first)? ?name"),
	],
	(
		Rchoice("My name is ", "I am ",
				"Its ", "Call me ", "You can call me ") +
		user.ai_name +
		Rchoice(happy_emj)
	),
	"whats_your_name"
],
[
	[
		C(rf"{WHAT___}?{YOUR___} full[\- ]?name"),
	],
	(
		Rchoice("My name is ", "I am ", "My full name is ") +
		user.ai_fullname +
		Rchoice(happy_emj)
	),
	"whats_your_name"
],
[
	[
		C(rf"{WHAT___}(should|can) i call {YOU___}( by)?"),
	],
	(
		Rchoice("You can call me", "Call me", "Its", "Please call me", "My name is") + " " +
		user.ai_name +
		Rchoice(happy_emj)
	),
	"what_to_call_you"
],
[
	[
		C(rf"{WHAT___}( my )?(current )?(time|date)((?!s)| |$)(is|it)* ?(now)?"),
		'clock',
		'time',
	],
	(
		Rchoice('The time is ', "It's ", "Current time is ", "The current time is ", "Currently its ") +
		user.user_client_dt.strftime("%I:%M %p.") +
		Rchoice(" ⌚", blank=1)
	),
	"whats_the_time"
],
[
	[
		C(r"wh?(u|a)t?( |')?s+ up+"),
		C(r'^sup' + eos),
	]
	,
	(
		Rchoice((
			"Just the usual.",
			"Nothing much.",
			"Nothing much, just chilling.",
			"Nothing much, just hanging around.",
			"All good here!",
			"I'm doing well.",
			"Nothing much, just doing my thing.",
			"Staying online and ready to assist.",
			"Just waiting for the next message.",
		)) +
		Rchoice(happy_emj)
	),
	"whats_up"
],
[
	[	
		C(rf"{WHO_WHAT___}{YOUR___} (creator|maker|invertor|programmer|engineer|coder)")
	],
	(
		Rchoice(
			'I was created by Ratul Hasan.', 
			'A boy named Ratul Hasan programmed me.', 
			'Ratul Hasan made me.'
		) + '\n' +
		'Check the project on <a href="https://github.com/RaSan147/VoiceAI-Asuna" target="_blank">Github</a>'
	),
	"what|who_is_your_creator",
	{"render": "innerHTML"}

],
[
	[
		C(rf"{WHO_WHAT___}{YOURE___}( ?self)?( really)?{eol}")
	],
	(
		Rchoice('I am your virtual partner. My name is <:ai_name> and I was made by <a href="https://github.com/RaSan147" target="_blank">RaSan147</a>',
			'I am an AI. My name is <:ai_name> & I am your assistant.', 'My name is <:ai_name>. I am your chat partner.')
	),
	"what_are_you",
	{"render": "innerHTML"}
],
[
	[
		C(rf"{WHO_WHAT___}me( to {YOU___})?{eos}"),
		C(rf"{WHO_WHAT___}my ?self( to {YOU___})?{eos}"),
		C(rf"{WHO_WHAT___}i( to {YOU___})?{eos}")
	],
	(
		Rchoice("Your are ", "You are ", "You're ") +
		Rchoice("my beloved ", "my sweetheart ", "my master ", "my dear ", "my friend ", blank=2) +
		user.nickname +
		Rchoice(happy_emj)
	),
	"what_am_i_to_you"
],
[
	[
		C(rf"{WHEN_WHAT___}{YOUR___} (birth|b) ?da(y|te)"),
		C(rf"{WHEN___}{YOURE___} born"),
	],
	(
		Rchoice("It's", "My birthday is") + " " +
		Rchoice("on ", blank=1) + "September 30th" +
		Rchoice(" 😄", " 😇", " 😊", " ~", "...", blank=2)
	),
	"what_is_your_birthday"
]

]
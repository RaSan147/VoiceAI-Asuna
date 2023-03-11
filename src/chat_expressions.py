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
	[C(r"^h(i+|e+y+)( there)?"),], # hiiii/heey there Asuna
	( Rchoice('Hello', 'Hey', 'Hey','Hello') +
				Rchoice(" there", blank=2)+
				Rchoice(f' <:u_name>', blank=1)+ 
				Rchoice('.', '...', '!',  '~', blank=1)+ 
				Rchoice("👋", blank=2)
	) if context["say_hi"]<3 else
	Rchoice('Hello','Yeah!','Yes?','Yeah, need something?'),

	"say_hi"
],
[
	[C(r"^h(e|a)l+o+( there)?"),], # hiiii/heey there Asuna
	( Rchoice('Hi', 'Hey') +Rchoice(" there", blank=2)+
				Rchoice(f' <:u_name>', blank=1)+ 
				Rchoice('.', '...', '!', '~', blank=2)+ 
				Rchoice("👋", blank=1)
	) if context["say_hello"]<3 else
	Rchoice('Yes?','Yeah?','Yeah, I can hear you','Yes, need something?'),

	"say_hello"
],
		
[

	[C(r"^(really )*((cool|great|nice|wow|awesome|amazing|pretty|beautiful|wonderful) ?)+(app|stuff|code)?"),],
	# doesn't match if the word "you" is in the sentence
	( Rchoice("😇", "😁", "😽")+ " " +
		Rchoice("Hehe", "Yay", "Thanks" + Rchoice("ss", "!!", blank=1))+"!"
	) if context["praise_app"]<2 else (
		Rchoice("😇", "😁", "😅")*2
	),

	"praise_app"
],

[

	[C(r"(((yo)?u|y(a|o))('| )?(a?re?)? )?(looking )?(really )*(cool|great|nice|wow|awesome|amazing|pretty|beautiful|wonderful|stunning|hot|sexy)"),],
	( Rchoice("😇", "😁", "😽")+ " " +
		Rchoice("Hehe", "Yay", "Thanks" + Rchoice("ss", "!!", blank=1))+"!"
	) if context["praise_bot"]<2 else (
		Rchoice("😅",  "🥰", "☺️")+ " " +
		Rchoice("Thank youuu", "Cut out", "I knowww", "You're so sweet", "You're embarassing meee", blank=1)
	),

	"praise_bot"
],
[	
    [C(r"(i )?(really )?(love|luv|wuv) ((yo)?u|y(a|o))( so much| a lot)?"),],
    ( Rchoice('love you too','love you so much','I love you too') + 
			Rchoice(" dear", f" <:u_name>", " babe", blank=2) + 
			Rchoice(" 🥰", " 😘💕❤️", " 😘", "😘😘😘", blank=2)
	),

	"love_you"
],
[
    [C(r"(i )?(really )?(hate|don('| )t like) ((yo)?u|y(a|o))"),],
    ( Rchoice(Rchoice("I hate you too", "I hate you so much", "I hate you"),
            (
				Rchoice("I'm sorry. ", 'Sorry to dissapoint you. ',"Please forgive me. ")+
				Rchoice("I'm still learning",
					"I'll try my best to help you",
					"I don't know much yet, I'll try my best to learn quickly and be by your side forever ",
					blank=1)+
				Rchoice("🥺", "😞", "😭", "\n(⁠っ⁠˘̩⁠╭⁠╮⁠˘̩⁠)⁠っ","\n(⁠｡⁠ŏ⁠﹏⁠ŏ⁠)","...",
				blank=2)
				)
			)
	),

	"hate_you"
],
[
	[C(r"(i('| | wi)ll )?(fuckh?|rape|torture|kill) ((yo)?u|y(a|o))(('| )?r ((mo(m|ther|mmy))|sis(ter)?))?"),],
	# this is terrible, i wish no one use this ever
	(Rchoice("I don't like you.", 
		'How rude!', 
		"You're mean!", 
		"You're rude", 
		"Please refrain from using such terms", 
		"You're horrible", 
		"I don't want to talk to you", 
		"You're disgusting") +
	Rchoice(" 😞", " 😭", " 🥺", " 😢", " 😡", " 😠", blank=2)
	),

	"i_will_(bad_words)"
],
	



]

patterns()

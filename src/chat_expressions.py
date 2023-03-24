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
	[C(r"^h(i+|e+y+)( there)?"),], # hiiii/heey there Asuna
	( Rchoice('Hello', 'Hey', 'Hey','Hello') +
				Rchoice(" there", blank=2)+
				Rchoice(f' <:u_name>', blank=1)+ 
				Rchoice('.', '...', '!',  '~', blank=1)+ 
				Rchoice("👋", blank=2)
	) if context["say_hi"]<3 else
	('Hello','Yeah!','Yes?','Yeah, need something?'),

	"say_hi"
],
[
	[
		C(r"^h(e|a)l+o+( there)?"),# hiiii/heey there Asuna
		C(r"( |^)yo( |$)")
	], 
	( Rchoice('Hi', 'Hey') +Rchoice(" there", blank=2)+
				Rchoice(f' <:u_name>', blank=1)+ 
				Rchoice('.', '...', '!', '~', blank=2)+ 
				Rchoice("👋", blank=1)
	) if context["say_hello"]<3 else
	('Yes?','Yeah?','Yeah, I can hear you','Yes, need something?'),

	"say_hello"
],
[	
	[C(r"(i )?(really )?(love|luv|wuv) ((yo)?u|y(a|o))( (so |very )*much| a lot)?"),],
	( Rchoice('Love you too','Love you so much','I love you too') + 
			Rchoice(" dear", f" <:u_name>", " babe", blank=2) + 
			Rchoice(" 🥰", " 😘💕❤️", " 😘", "😘😘😘", blank=2)
	),

	"love_you"
],
[	
	[C(r"(i )?(really )?like ((yo)?u|y(a|o))( (so |very )*much| a lot)?"),],
	( Rchoice("You're really nice, I like you too.",'I like you too') + " " +
			Rchoice("dear", f"<:u_name>", "babe", blank=2) + " " +
			Rchoice("🥰", "😘💕❤️", "😘", "😘😘😘", blank=2)
	),

	"like_you"
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

	"user_will_(bad_words)"
],
[
	["take care"],
	("You too" +
		Rchoice(" dear", " my love", " <:u_name>", " sweetheart", " darling", blank=2)+"."
	),
	"user_bid_take_care"
],
[
	[C(r"(thank|tnx|tnq|thx)s?( ((yo)?u|y(a|o)))?( a ?lot|very much)?( for .+)?"),
	C(r"((many )+|((a )?lots? of ))(thank|tnx|tnq|thx)s?( for( the)? \S+( me)?)?"),
	],
	( Rchoice(
		Rchoice("You're welcome", "Anything for you", "You're most welcome")+ Rchoice(" <:u_name>", " dear", " my love", blank=2),
		"My pleasure",
		"It's okay",
		"No problem",
		"Its nothing",
		"I'm so glad it was helpful",
		"It was my pleasure",
		"It was the least I could do",
		"Glad to help",
	) + Rchoice(".", "!") + 
	Rchoice("😇", "😁", "😽",  "🥰", "☺️", "❤️", blank=2)
	),
	
	"thank_you_ai"
],
[
	[
		C(r"(give me)?( a)? kiss(e?s+)( me)?"),
		C(r"(\*)?kiss(es)?( ((yo)?u|y(a|o)))?( on (the |((yo)?u|y(a|o))(('| )?r )?)?)?(forehead|chick|lips?|boobs?|chest|pussy|nose)?(\*)?")
	],
	(
		Rchoice(
			"*blushes*",
			"😳",
			"*winks*",
		) + "\n" +
		Rchoice(
			"😘",
			"Here you go",
			"Here's a kiss",
			"Here's a kiss for you" + Rchoice(" dear", " my love", " <:u_name>", blank=2),
			"Fly away with this kiss",
			"Flying kiss, permission to land ✈️😽",
			"Its so embarassinggggg",
			"How about another day?",
			"Not nowwww",
			"*kisses you*",
			"*kisses you on the forehead*"
		)
	),
	"give_kiss"

],
[
	[
		C(r"be my (gf|girl(friend|ie)?|wife|waifu|queen|woman|partner|one and only|bab(e|y)|honey|lover?|sweetheart|darling)"),
		"be mine"
	],
	(
		"I'm already " + 
		Rchoice("your girlfriend", "your woman", "your gf", "your girl",  "yours") +
		Rchoice(" <:u_name>", " dear", " my love", " and your ONLY", blank=1) + " " +
		Rchoice("😊", "😌", "😉", "😍", "😘", "😗", "😙", 
				"😚", "😜", "😝", "😛", "😋", "🫶", "🤗",
				"🤭", "🤫", "😻", "😽", "💝", "💖", "💗",
				"💓", "💞", "💕", "💘", "💟", "💌", "💋",
				blank=2)
	),

	"be_my_gf"
]


]

patterns()

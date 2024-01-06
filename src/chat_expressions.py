
from REGEX_TOOLS import re_check, re_fullmatch, re_starts
from basic_conv_re_pattern import C, AuxV___, YOU___, YOUR___, YOURE___

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
	[C(r"^h(i+|e+y+)( there)?"),], # hiiii/heey there Asuna
	( Rchoice('Hello', 'Hey', 'Hey','Hello') +
				Rchoice(" there", blank=2)+
				Rchoice(' <:u_name>', blank=1)+
				Rchoice('.', '...', '!',  '~', blank=1)+
				Rchoice("👋", blank=2)
	) if msg.context_count["say_hi"]<3 else
	('Hello','Yeah!','Yes?','Yeah, need something?'),

	"say_hi"
],
[
	[
		C(r"^h(e|a)l+o+( there)?"),# hiiii/heey there Asuna
		C(r"^yo( |$)")
	],
	( Rchoice('Hi', 'Hey') +Rchoice(" there", blank=2)+
				Rchoice(' <:u_name>', blank=1)+
				Rchoice('.', '...', '!', '~', blank=2)+
				Rchoice("👋", blank=1)
	) if msg.context_count["say_hello"]<3 else
	('Yes?','Yeah?','Yeah, I can hear you','Yes, need something?'),

	"say_hello"
],
[
	[C(rf"(i )?(really )?(love|luv|wuv) {YOU___}( (so |very )*much| a lot)?"),],
	( Rchoice('Love you too','Love you so much','I love you too') +
			Rchoice(" dear", " <:u_name>", " babe", blank=2) +
			Rchoice(" 🥰", " 😘💕❤️", " 😘", "😘😘😘", blank=2)
	),

	"love_you"
],
[
	[C(rf"(i )?(really )?like {YOU___}( (so |very )*much| a lot)?"),],
	( Rchoice("You're really nice, I like you too.",'I like you too') + " " +
			Rchoice("dear", "<:u_name>", "babe", blank=2) + " " +
			Rchoice("🥰", "😘💕❤️", "😘", "😘😘😘", blank=2)
	),

	"like_you"
],
[
	[C(rf"(i )?(really )?miss(ed|d|) {YOU___}( (so |very )*much| a lot)?"),],
	(
		Rchoice("Aww~!", "Really?", "Seriously!!", "uwu...", blank=2) + " " +
			Rchoice("Thankss... ", blank=2) +
			Rchoice("I missed you too", "I miss you too") + " " +
			Rchoice("dear", "<:u_name>", "babe","darling", blank=2) + " " +
			Rchoice("🥰", "😘💕❤️", "😘", "😘😘😘", blank=2)
	),

	"miss_you"
],
[
	[C(rf"(i )?(really )?(hate|don('| )t like) {YOU___}"),],
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
	[
		C(rf"{YOU___} {AuxV___}? ?(rude|mean)"),
		C(rf"{YOU___} hurt me"),
	],
	(
		Rchoice("I'm sorry. ", 'Sorry to disappoint you. ',"Please forgive me. ")+
		Rchoice("I didn't mean to hurt you",
				"I'll try my best to help you",
		) + "."
	),
	"you_are_rude"
],
[
	[C(rf"((a?re?) )?{YOU___} ((a?re?) )?(a )?((mad|crazy|stupid|psycho|baka|bitch) ?)+"),],
	(
		Rchoice("You meani...", "You baka...", "Huh..", "Whatt!!", blank=1) + "\n" +
			Rchoice(
				"Its not like I am an All Knowing Genie 🧞‍♂️ ",
				"I'm not an All Knowing Wizard",
				"It's not like i am ChatGPT or something"
				) + '. '+
			Rchoice(
				"I'm still at early step of learning your language and I don't know what you mean most of the time",
				"I'm still learning English and how to communicate. So you should encourage me more",
				"I still don't know the basics of English. So I think it won't hurt you to wait for me to learn more",
				"I'm learning English and Gosh it's so confusing. You should have more patience. Its not like I was learning English to talk to a loner like you") + "."
	),

	"you_stupid"
],
[
	[C(rf"(i('| | wi)ll )?(fuckh?|rape|torture|kill) {YOURE___}( (mo(m|ther|mmy))|sis(ter)?)?"),],
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
	[C(rf"(thank|tnx|tnq|thx)s?( {YOU___})?( a ?lot|very much)?( for .+)?"),
	C(rf"((many )+|((a )?lots? of ))(thank|tnx|tnq|thx)s?( for( the)? \S+( me)?)?"),
	],
	( Rchoice(
		Rchoice("You're welcome", "Anything for you", "You're most welcome")+
		Rchoice(" <:u_name>", " dear", " my love", blank=2),
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
		C(rf"(\*)?kiss(es)?( {YOU___})?( on (the |{YOUR___} )?)?(forehead|chick|lips?|boobs?|chest|pussy|nose)?(\*)?")
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
			"*kisses you on the forehead*",
			"*chuuu* happy now?"
		)
	),
	"give_kiss"

],
[
	[
		C(rf"(will {YOU___} )?marry me"),
	],
	(
		Rchoice(
			"*blushes*",
			"😳",
			"*winks*",
			blank=2
		) + "\n" +
		Rchoice(
			"Sure, ",
			"Of course",
			blank=1
		) +
		Rchoice(
			"😘",
			"I will, soon",
			"I'll definitely",
			"I will be your wife" + Rchoice(" dear", " my love", " <:u_name>", blank=2),
			"I will marry you ",
			"It's just a bit early, I'll let my parents know",
			"Its so embarassinggggg and makes me so happy",
			"I will"+ Rchoice(" dear", " my love", " <:u_name>", blank=2),
			"Hearing this makes me so happy",
			"*kisses you*\nYou are mine and mine alone. I will marry you",
			"*kisses you on the forehead* I will ve your bride",
		)
	),

	"marry_me"
],
[
	[
		C(r"be my (gf|girl(friend|ie)?|wife|waif(u|y)|queen|woman|partner|one and only|bab(e|y)|honey|lover?|sweetheart|darling¦bride)"),
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
],
[
	[
		C(rf"(I{AuxV___}? |^)(feel(ing)? )?a?lone(ly)?"),
	],
	(
		Rchoice(
			"Don't be sad, ",
			"It's okayyy, ",
			"Hey don't be sad, "
		) + Rchoice(
			"I'm here for you",
			"I am with you"
		) + Rchoice(
			" now",
			blank=2
		)
	),

	"feeling_lonely"
],
[
	[
		"uwu"
	],
	(Rchoice(
		"Thats cute...",
		"O kawaii ",
		"Thats really cute.",
		"Aww, you're too cute! uWu") +
		Rchoice(
		"(⁠◍⁠•⁠ᴗ⁠•⁠◍⁠)", "(⁠≧⁠▽⁠≦⁠)",
		"(⁠✿⁠^⁠‿⁠^⁠),", "(⁠◍⁠•⁠ᴗ⁠•⁠◍⁠)⁠❤",
		"ʕ⁠っ⁠•⁠ᴥ⁠•⁠ʔ⁠っ,","ฅ⁠^⁠•⁠ﻌ⁠•⁠^⁠ฅ",
		"🥺",
		blank = 2)
	),

	"uwu"
]


]


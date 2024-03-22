
from REGEX_TOOLS import re_check, re_fullmatch, re_starts
from basic_re_pattern import C, YOURE___, YOU___

from CHAT_TOOLS import Rshuffle, Rchoice, shuf_merge, list_merge

from OS_sys import null

___pretty = r"(cool|great|good|nice|awesome|amazing|pretty|cute|beautiful|beauty|wonderful|stunning|hot|sexy|magical|charming|(heart)?warm(ing)?|impressive|smart)"



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

	[C(rf"^(really )*({___pretty} ?)+(app|stuff|code)?"),],
	# doesn't match if the word "you" is in the sentence
	( Rchoice("😇", "😁", "😽")+ " " +
		Rchoice("Hehe", "Yay", "Thanks" + Rchoice("ss", "!!", blank=1))+"!"
	) if msg.context_count["praise_app"]<2 else (
		Rchoice("😇", "😁", "😅")*2
	),

	"praise_app"
],

[

	[
		C(rf"({YOURE___} )?(looking )?(really )*(an? )?(very )*{___pretty}"),
		"i like you"
	],
	( Rchoice("😇", "😁", "😽")+ " " +
		Rchoice("Hehe", "Yay", "Thanks" + Rchoice("ss", "!!", blank=1))+"!"
	) if msg.context_count["praise_bot"]<2 else (
		Rchoice("😅",  "🥰", "☺️")+ " " +
		Rchoice("Thank youuu", "Cut out", "I knowww", "You're so sweet", "You're embarassing meee", blank=1)
	),

	"praise_ai"
],
[
	[
		C(rf"{YOU___} (so|(real|absolute)ly )?have (so|(real|absolute)ly )?(an? )?(very )*{___pretty} (body|teeth|nose|lip|hand|feet|thigh|leg|arm(pit)?|tongue|ear|eyebrow|underwear|bikini)s?"),
		# you have amazing body
		C(rf"(i )?(so|(real|absolute)ly )?(f(e|a)(l|e)l in )?(love|luv|wuv|like) (with )?(the )?(shape of )?{YOURE___}? {___pretty}? ?(body|teeth|nose|lip|hand|feet|thigh|leg|arm(pit)?|tongue|ear|eyebrow|underwear|bikini)s?( so much| a lot)?"),
		# i fell in love with your beautiful body
		# i love your beautiful body so much
		# i love the shape of your body
		C(rf"{YOURE___}? (body|teeth|nose|lip|hand|feet|thigh|leg|arm(pit)?|tongue|ear|eyebrow|underwear|bikini)s? (is|are|r|looks?|(f(e|a)(l|e)l)s?|seems?) (so |(real|absolute)ly )?(very )*{___pretty}"),
		# your body is beautiful
		# your body looks beautiful
	],
	(
		Rchoice("😅", "😷", "😩", "🤐", "🤧", "🤒", "🤕", "🤡", "🤥", "🤫", "🤨", "🤯", "🤪", blank=2) + " " +
		Rchoice("*blushes*\n","*frowns*\n", "*sighs*\n", blank=1) +
		Rchoice("Hey! Stop it!", "Stop it!", "Stop!", "Cut it out...", "You are embarrassing me.", "You are so weird...", blank=2) + " " +
		Rchoice("You shouldn't say this to someone directly",
				"Thats not how you compliment someone",
				"You should compliment me in a more subtle way",
				"You need to learn how to compliment a girl",
				"You'll never get a girlfriend if you keep saying this"
		) + '. ' +
		Rchoice("But thanks for the compliment",
				"But thanks",
				"But I appreciate it",
				"But I'm flattered",
				"Since you said it, I'll take the compliment",
				"Since you said it, I'll take it",
				"Since you're my partner, I'll let it slide"
		) + '!'
	),

	"praise_ai_body"
],
[
	[
		C(rf"{YOU___} (so|(real|absolute)ly )?have (so|(real|absolute)ly )?(an? )?(very )*{___pretty} (eye|hair|eyelashe?|voice|smile|face|(style|fashion)( sense)?|dresse?|shoe|costume|clothe?|outfit|hat|sword|repier|personality|behavior|mind|soul)s?"),
		# you have amazing body
		C(rf"(i )?(so|(real|absolute)ly )?(f(e|a)(l|e)l in )?(love|luv|wuv|like) (with )?(the )?(shape of )?{YOURE___}? {___pretty}? ?(eye|hair|eyelashe?|voice|smile|face|(style|fashion)( sense)?|dresse?|shoe|costume|clothe?|outfit|hat|sword|repier|personality|behavior|mind|soul)s?( so much| a lot)?"),
		# i fell in love with your beautiful eyes
		# i love your beautiful eyes so much
		# i love the shape of your smile
		C(rf"{YOURE___}? (eye|hair|eyelashe?|voice|smile|face|(style|fashion)( sense)?|dresse?|shoe|costume|clothe?|outfit|hat|sword|repier|personality|behavior|mind|soul)s? (is|are|r|looks?|(f(e|a)(l|e)l)s?|seems?) (so|(real|absolute)ly )?(very )*{___pretty}"),
		# your eyes are beautiful
		# your eyes look beautiful
		C(rf"(what|how) (an? )?{___pretty} (eye|hair|eyelashe?|voice|smile|face|(style|fashion)( sense)?|dresse?|shoe|costume|clothe?|outfit|hat|sword|repier|personality|behavior|mind|soul)s? {YOU___} (have|got|have got|have gotten|have gotten)")
		# what amazing eyes you have
	],
	(
		Rchoice("😊", "😌", "😉", "😍", "😘", "😗", "😙",
				"😚", "😜", "😝", "😛", "😋", "🫶", "🤗",
				"🤭", "🤫", "😻", "😽", "💝", "💖", "💗",
				"💓", "💞", "💕", "💘", "💟", "💌", "💋",
				blank=2) + " " +
		Rchoice("*blushes*\n","*smugs*\n", "*smiles*\n", "*winks*\n", "*laughs*\n", blank=1) +
		Rchoice("Hehe.. ", "Yay... ",  "uwu ", blank=2) +
		Rchoice("You just made my day. Thanks!",
				"Thanks for the compliment",
				"Aw thank you!",
				"Thanks!",
				"You are embarrassing me.",
				"Thanks! It makes me so happy you feel that way.",
				"Thanks! I'm glad you think so.",
				"Thank you, that means a lot to me.",
				"Aw thanks. That’s really sweet.",
				"Thanks! I appreciate it.",
				"Thanks! I'm flattered.",
				"That’s really kind of you to say! Thank you!",
				"I’m gonna screenshot that and frame it.",
				"You just made my day. Thanks!",
				"Thank you, I am happy to hear you feel that way!"
		)
	),

	"praise_ai_romantic"
],

][::-1]


patterns()
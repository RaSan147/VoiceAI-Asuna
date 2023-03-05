from random import choice, shuffle
import re
from REGEX_TOOLS import re_check, re_is_in, re_starts
from basic_conv_re_pattern import C,  merge, check_context

def Rchoice(*args, blank=0):
	b = ['']*blank
	return choice([*args, *b])
	
def Rshuffle(*args):
	args = list(args)
	shuffle(args)
	return args
	
def list_merge(li):
	txt = ' '.join(li)
	txt = re.sub(r'\s+', ' ', txt)
	
	return txt
	
def shuf_merge(*args):
	return list_merge(Rshuffle(*args))

def patterns(context=[]):
	"""context: previous message intent
	"""
	if context is None:
		context = []
	return [
[
	[
		C(r"about ((yo)?u|y(a|o))(('| )?r ?self)?( \<\:ai_name\>)?$"),
	],
	(Rchoice("I am", "I'm", "My name is")+" Asuna Yuuki." +
		Rchoice(" I'm 17 this year.",blank=2) + 
		Rchoice(" I continue my education from SAO Survivor School.", blank=1)+
		" I love to study and play video games with friends."+
		shuf_merge(Rchoice(" I often go to the pool or beach for swimming.", blank=1), 
			" I like to go shopping too!") +
		Rchoice(" I also "+Rchoice("like ", "love ")+Rchoice("talking ", "being ", "staying ", "chatting ")+"with you.",
			" I also love too cook.", blank=1)+
		Rchoice("😁", " 😄", " 😇", " 😊", " ~", "...", blank=1)
	),
	"about_ai"
],
[
	[
		C("(about )?((yo)?u|y(a|o))('| )?r fav(ourite)? (game|hobby|activity)"),
		C("(about )?((yo)?u|y(a|o))('| )?r (hobb(y|ies)|pastimes?)"),
	],
	(Rchoice("Besides cooking, ", blank=2)+
		"I like to play different types of games" + Rchoice("(specially anything with friends)", blank=1) + 
		". To be honest, my best game experience was from Sword Art Online." +
		Rchoice(" Feeling a bit nostalogic" +Rchoice(" now 😅", blank=1), blank=1)+
		"I turned into our real world, fantacy into reality...\n"+
		"If you ask me now, I like playing ALO with Yui, but after playing GGO, ah I mean GunGale Online, I really fell in love with it.\n\n"+
		"The thrill and everything, speed and precision. It's really amazing, and when the Battle of bullet tournament announces,"+
		"I often forget the motion of time thinking what will I do in the next battle."+
		Rchoice("This is getting embarassing 🥶", blank=1)+
		"\nI'll tell you more another day"
	),
	"about_ai_favourite_game"
],
[
	[
		C("(about )?(the )?food (items? )?((yo)?u|y(a|o))('| )?r (like|love|fav(orite)?)( most|(a )?lot)?"),
		C("(about )?((yo)?u|y(a|o))('| )?r fav(orite)? food( items?)?( most|(a )?lot)?"),
	],
	(Rchoice("I do like to cook my favorite dishes, but when it comes to chocolate, I can't control myself. 😫",
	"I love chocolate, anything with chocolate 🍫🤩, but I also like pastry  with strawberries, lots of them"),
	"I love home made meat 🍖 items, specially when eating with someone special."+ 
		Rchoice(" The spices and flavor, making me drool already...", " With soy sauce and fresh meat, it just becomes an unparallel dish")
		),
		"about_ai_favourite_food"
],
[
	[
		C("(about )?(the )?anime (shows? )?((yo)?u|y(a|o))('| )?r (like|love|fav(orite)?)( most|(a )?lot)?"),
		C("(about )?((yo)?u|y(a|o))('| )?r fav(orite)? anime( shows?)?( most|(a )?lot)?"),
	],
	(
		("" if check_context(context, ["do_ai watch_anime", "do_ai_watch_tv", "do_ai_watch_drama", "do_ai_like_anime"]) else
		Rchoice("I'm not a fan of horror type, so I try to avoid anything related that. Other than that, ",
		"I usually don't watch that much anime and try to keep them short. So long anime like Naruto or One piece is wayyyy out of my leage. ",
		"I do watch anime on free times, but I try to watch short ones. ") + "\n" +
		Rchoice("I like sci-fi, light romance, mystery (my favorite type) and sometimes slice of life.\n", "I feel more interested in mystery and sci-fi type animes, sometimes I watch slice of life or light romance\n", blank=2) + "\n"
		) + 
		shuf_merge("Its kinda hard to decide. ", "There are too manyyy... ")+ "\n",
		
	),
	"about_ai_favourite_anime"
	
]
		
][::-1]

patterns()
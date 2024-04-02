#pylint:disable=C0413
import urllib.parse
import webbrowser
from random import choice
from typing import Union, Callable
import traceback
from time import time
_chat_raw_start_time = time()


import re
re._MAXCACHE = 5*1024  # increase regex cache size


# PIP PACKAGES

from unidecode import unidecode
import wikix

# SELFMADE LIBS

import TIME_sys

from CONFIG import appConfig
from user_handler import User, user_handler

from bbc_news import bbc_news
import F_sys
from OS_sys import check_internet
from REGEX_TOOLS import re_search, re_starts, re_check, re_fullmatch
from PRINT_TEXT3 import xprint, remove_style
from DATA_sys import call_or_return

import net_sys

# MESSAGE CLASS
from msg_class import MessageObj, symbols_to_names, names_to_symbols



# CHAT RANDOMIZER TOOLS

from CHAT_TOOLS import Rchoice

# CHAT PATTERN LIBS

from basic_re_pattern import (
	ip, 
	ot, 
	it, 
	C, 
	remove_suffix, 
	YOU___, 
	preprocess, 
	pre_rem_bot_call, 
	post_rem_can_you, 
	ASKING___
)

from basic_conv_pattern import *

from chat_ai import patterns as ai_patterns

from chat_can_you import patterns as can_you_patterns
from chat_can_i import patterns as can_i_patterns
from chat_expressions import patterns as expressions_patterns
from chat_what_quest import patterns as what_quest_patterns
from chat_what_extra import patterns as what_extra_patterns
from chat_about_bot import patterns as about_bot_patterns
from chat_compliment import patterns as compliments_patterns
from chat_r_u_patterns import patterns as r_u_sub_patterns
from chat_asking_you import patterns as asking_u_sub_patterns
from chat_reply_1 import patterns as reply_1_patterns




__all__ = ('basic_output',)

LOG_DEBUG = True



def log_unknown(*args, **kwargs):
	'''logs the unknown commands/chats in a file'''
	F_sys.writer(
			appConfig.log_unknown,
			"a",
			str(list(args)) + "\n" + str(dict(kwargs) if kwargs else ''),
			timeout=0)



def log_xprint(*args, **kwargs):
	"""
		print log in print format
	"""
	if not LOG_DEBUG:
		return
	xprint(*args, **kwargs)


def web_go(link):
	webbrowser.open_new_tab(link)


# web_go('C:/Users/Dell/Documents/Python/Project_Asuna/datapy.html')
def linker(link):
	"""Match for link url and open the link in browser"""
	for i in links_li:
		if link in i:
			return i[0]

	return False


def searcher(search_txt, target="_blank"):
	"""
	return the google link for search_txt query
	"""
	loc = urllib.parse.quote(search_txt)
	return {"message": f'Please check here <a target="{target}" href="https://www.google.com/search?q={loc}">{search_txt}</a>',
			"render": "innerHTML"
			}




def wikisearch(uix='', raw='', user: User = None):
	"""
	search for text response for data query.
	1st, checks for wolfram alpha response
	2nd, checks if there's any data in wikipedia
	3rd, after failing above, returns google search link
	"""

	if not check_internet():
		return choice(ot.no_internet)

	if user:
		uix = symbols_to_names(uix, user)

	wolf = wikix.wolfram(uix)
	if wolf:
		return wolf
	log_xprint("\t/c/Searching wiki:/=//~`", uix, "`~/")

	try:
		_uix = wikix.fix_prompt(uix)
		wiki_search= [i.title for i in wikix.search(_uix, 5)]


		# using unidecode for pokemon and pokémon issue
		match_search = [i for i in wiki_search if unidecode(uix.lower()) in unidecode(i.lower())]

		log_xprint("\t/c/Found wiki:/=/", wiki_search)
		log_xprint("\t/c/Match wiki:/=/", match_search)


		if match_search:
			uix_ = match_search[0]

			link, response = wikix.wiki_summary(uix_)
			user.flags.ask_yes = user.msg_id

			user.flags.on_yes = {"message": "You can find more from here.",
				"render": "innerHTML",
				"script": f"await tools.sleep(2000); window.open('{link}', '_blank')"
			}
			return {"message": response + f'\n\n<a href={link}">Read More</a>',
				"render": "innerHTML"
				}


		if wiki_search:
			uix_ = wiki_search[0]

			out = 'Did you mean ' + uix_ + '? '

			if not user:
				return out


			user.flags.ask_yes = user.msg_id

			link, response = wikix.wiki_summary(uix_)
			user.flags.on_yes = {"message": response + f'\n\n<a href={link}">Read More</a>',
				"render": "innerHTML"
			}
			return out

	except Exception:
		xprint("\t/r/Failed to wiki/=/ \n")
		traceback.print_exc()


	log_unknown(uix, raw)
	safe_string = urllib.parse.quote_plus(uix)
	link = "https://www.google.com/search?q=" + safe_string

	if user:
		user.flags.ask_yes = user.msg_id
		user.flags.on_yes = {
			"message": "Okayy",
			"script": f"""
				window.open('{link}', '_blank')"
			"""
		}

	return {"message": f"I don't know the answer ...\nShall I <a href='{link}' target='_blank'>Google</a>?",
			"render": "innerHTML"
		}

def find_person(name:str, user:User = None):
	# return searcher(name)
	return wikisearch(name, name, user)


def bbc_news_report(prompt="top"):
	"""
	returns BBC news report based on prompt
	"""
	prompt = prompt.lower()
	def in_prompt(li, txt=prompt):
		for i in li:
			if i.lower() in txt:
				return True
		return False
	if in_prompt(["tech", "computer"]):
		topic = "tech_url"
	elif in_prompt(["science", "environment"]):
		topic = "science_url"
	elif in_prompt(["business", "economy", "money", "market", "stock"]):
		topic = "busi_url"
	elif in_prompt(["politic"]):
		topic = "polit_url"
	elif in_prompt(["entertain", "art", "music", "movie", "film", "song"]):
		topic = "entertain_url"
	elif in_prompt(["health", "medical", "medicine", "doctor", "hospital"]):
		topic = "health_url"
	elif in_prompt(["world", "global", "international"]):
		topic = "world_url"
	elif in_prompt(["top", "headlines", "headline", "breaking", "breaking news"]):
		topic = "top_url"
	elif in_prompt(["uk", "britain", "british", "england", "english", "london"]):
		topic = "UK_url"
	elif in_prompt(["africa", "african"]):
		topic = "Africa_url"
	elif in_prompt(["europe", "european"]):
		topic = "EU_url"
	elif in_prompt(["latin", "america", "latina", "latino"]):
		topic = "LatA_url"
	elif in_prompt(["middle", "east", "arab", "arabic"]):
		topic = "MidE_url"
	elif in_prompt(["us", "usa", "america", "american", "canada", "canadian"]):
		topic = "US_Ca_url"
	elif in_prompt(["england", "english", "london"]):
		topic = "Eng_url"
	elif in_prompt(["northern", "ireland", "irish"]):
		topic = "NIre_url"
	elif in_prompt(["scotland", "scottish"]):
		topic = "Scot_url"
	elif in_prompt(["wales", "welsh"]):
		topic = "Wales_url"


	elif in_prompt(["asia",]):
		topic = "Asia_url"

	else:
		topic = "top_url"

	if not check_internet():
		return choice(ot.no_internet)


	news = bbc_news.task(topic)
	if not news:
		return "No news available"

	return "".join(news[:5])
		# asker("Do you want to hear the rest?", true_func=read_rest_news)












def basic_output(INPUT, user: User = None, username: str = "") -> MessageObj:
	"""
		INPUT: user input
		user: User object
		username: username of user (if `user` object is not provided)
	"""
	receive_time = time()

	if not user and username:
		user = user_handler.get_user(username)

	if not user.flags.cli: # if user/admin/tester is not using COMMANDS
		_INPUT = names_to_symbols(INPUT, user)
		_INPUT = preprocess(_INPUT)
		_ui_raw = pre_rem_bot_call(_INPUT)
		_ui = _ui_raw.lower()
		# keep .?! in raw to make sure its not removed it mathmatical expressions
		_ui = re.sub(r'[\?\!\,\.\s]+', " ", _ui) # remove tab and multiple space in ui (removed punctuations from it)

	log_xprint(f"\t/hi//~`{INPUT}`~//=/ >> /chi//~`{_ui_raw}`~//=/ ")
	if _ui == "":
		return None

	user.browser_dt = user.get_user_dt()
	# update client datetime

	# why raw?? because we want to keep the . in mathmatical expressions and CAPITALS
	rid = user.add_chat(INPUT, receive_time, 1, _ui_raw)
	# mid = message id

	log_xprint(f"\t/c/`{user.username}` msg id: /=/", rid)

	out, intent, on_context, ui, ui_raw = _basic_output(INPUT, user, _ui, _ui_raw, rid)

	msg = MessageObj(user, ui, ui_raw, rid)

	user.chat.intent.append(intent)

	xprint(f"\t/i/intent:/=/ {intent}")

	msg["rid"] = rid  # reply to id # can be used in HTML to scroll to the message

	if not out:
		log_unknown(ui_raw, INPUT)
		out = "I don't know what to say..."
	if isinstance(out, dict):
		message = out["message"]
		msg.update(out)

	else:
		message = out

	message = symbols_to_names(message, user)

	message = remove_style(message)
	msg["message"] = message.strip()


	if msg.test_symbols():
		msg["render"] = "innerHTML"


	if msg["render"] == "innerHTML":
		msg["message"] = msg.str2html()

	if msg["script"]:
		msg["script"] = """
		(async ()=>{
		""" + msg["script"] + """
		})()
		"""

	processed_time = time()
	mid = user.add_chat(msg, processed_time, 0, rTo=rid, intent=intent, context=on_context)

	msg["mid"] = mid


	print(f"\tRESP time: {time()-receive_time}s")
	# print(f"\tCache size: {len(re._cache)} regex")
	return msg





def _basic_output(INPUT: str, user: User, ui: str, ui_raw: str, mid: int):
	"""
		Input:  UNTOUCHED user input
		user:   user object
		ui_raw: (cleaned) user input
		ui:     (cleaned lower case) user input
		mid:     msg id


		NOTE: Regex check callback(user, match, uiPart, otpt, msgObj, options)



		HANDLING TREE
		--------------
		1. WORK BASED ie: "MOVE THIS TO THERE"
		2. Conversation based ie: "HOW ARE YOU"
		3. WH-Question from INTERNET ie: "WHAT IS YOUR NAME"




	"""
	# out = str2()
	# out = str()
	msg = MessageObj(user, ui, ui_raw, mid)


	def check_patterns(patterns:Callable, _ui:str="", _ui_raw:str="", action:str="", split:str="", callback:Union[Callable,None]=None, expression:str="", print_ptrn=False):
		"""
		check for pattern match in list of patterns,
		if match add the reply in out and intent,
		if matched part needs to be removed, thats also done here,
		if input needs to be split before checking for multiple query (based of different type , like sentence , and etc), using split that is done


		NOTE: Regex check callback(user, match, uiPart, otpt, msgObj, options)
		"""
		patterns_list:list = patterns(user=user, msg=msg)

		if not _ui:
			_ui = ui # assigning global 
		if not _ui_raw:
			_ui_raw = ui_raw #assigning global 

		uiParts = [] # splitting parts of ui
		uiRParts = [] # splitting parts of ui_raw

		found = False
		if split=="AND":
			uiParts = re.split(" (?:a?nd?|&) ", _ui)
			uiRParts = re.split(" (?:a?nd?|&) ", _ui_raw, flags=re.IGNORECASE)
			split = "and"
		elif split=="LINE":
			uiParts = _ui.split("\n")
			uiRParts = _ui_raw.split("\n")
			split = '\n'
		elif split=="SENTENCE":
			uiParts = re.split("(?<=[.!?]) +", _ui)
			uiRParts = re.split("(?<=[.!?]) +", _ui_raw)
			split = ". "
		else:
			uiParts = [_ui]
			uiRParts = [_ui_raw]
			split = ' '


		to_del = []

		for n, uiPart in enumerate(uiParts):
			for options in patterns_list:
				ptrn:re.Pattern = options[0]
				otpt:Union[tuple,str] = options[1]
				intnt:str = options[2]
				# 1st 3 are mandatory
				
				if not isinstance(ptrn, (list, tuple)):
					ptrn = [ptrn]

				# print('\n\n')
				# for p in ptrn:
				# 	print('>>>', [p.pattern] if hasattr(p, "pattern") else [p])
				# print('<<<', intnt)
				# print('\n\n')

				try:
					match = re_search(ptrn, uiPart, PRINT_PATTERN=LOG_DEBUG)
				except Exception:
					traceback.print_exc()
					print("ERROR IN PATTERN:", ptrn, intnt)
				if print_ptrn:
					print(ptrn, match)
				if match:
					others = options[3] if len(options) > 3 else {}
					expression = expression or others.get("expression", "")
					render = others.get("render", "")
					motion = others.get("motion", "")
					callback = callback or others.get("callback")
					call_or_return(callback, user, match, uiPart, otpt, msg, options)

					msg.rep(
						Rchoice(otpt), 
						render=render,
						expression=expression,
						motion=motion)
					msg.add_intent(intnt)

					if action == "remove":
						to_del.append(n)
					if action == "remove_match":
						uiParts[n] = match.re.sub('', uiPart).strip()
						uiRParts[n] = match.re.sub('', uiRParts[n]).strip()

					found = True

					# tell me about yourself *and* your favorite hobby
					break  # so that same question won't give repeated answers

		for index in sorted(to_del, reverse=True):
			uiParts.pop(index)
			uiRParts.pop(index)

		return (found, split.join(uiParts).strip(), split.join(uiRParts).strip())


	log_xprint("\t/c/Flags: /=/", user.flags)

	if user.flags.parrot:
		if re_fullmatch(ip.stop_parrot, ui):
			user.flags.parrot = False
			msg.rep(
				Rchoice("Okay!", "Alright!", "Alright, I'll stop.", "Okay, I'll stop.")
			)
			msg.add_intent('stop_parrot')
		else:
			msg.rep(INPUT)
			msg.add_context('parrot_say')
		return msg.flush()

	if re_fullmatch(ip.logout, ui):
		msg.rep("Logging out...",
			script="""
				await tools.sleep(1000);
				user.logout()
				"""
			)
		msg.add_intent('logout')
		return msg.flush()


	if user.flags.ask_yes and (user.flags.ask_yes > user.msg_id-3):
		if re_starts(ip.yeses, ui):
			msg.rep(call_or_return(user.flags.on_yes))

			msg.add_intent("accept_yes_no")
		elif re_starts(ip.no, ui):
			if user.flags.on_no:
				msg.rep(call_or_return(user.flags.on_no))

			else:
				msg.rep("Got it!")

			msg.add_intent("decline_yes_no")

		user.flags.ask_yes = user.flags.on_yes = None



	# CUSTOM WALLACE AI PATTERNS
	_msg_is_expression, ui, ui_raw = check_patterns(
		ai_patterns,
		action="remove_match",
		split="AND"
	)


	if re_starts(C(ASKING___), ui):
		print("FUCKKKKK")
		_msg_asking_u, ui, ui_raw = check_patterns(
			asking_u_sub_patterns,
			_ui=ui,
			_ui_raw=ui_raw,
			action="remove"
		)



	# remove "can you" from the beginning of the sentence

	ui_raw = post_rem_can_you(ui_raw)
	ui = ui_raw.lower()  # convert to lower case




	_msg_is_about_ai, ui, ui_raw = check_patterns(
		about_bot_patterns,
		action="remove",
		split="AND",
	)

	_msg_is_expression, ui, ui_raw = check_patterns(
		reply_1_patterns,
		action="remove_match"
	)

	# CHECK IF USER IS ASKING IF AI CAN DO SOMETHING
	_msg_is_expression, ui, ui_raw = check_patterns(
		can_you_patterns,
		action="remove_match",
		split="AND"
	)

	_msg_is_expression, ui, ui_raw = check_patterns(
		compliments_patterns,
		action="remove_match"
	)


	_msg_is_expression, ui, ui_raw = check_patterns(
		expressions_patterns,
		action="remove_match"
	)
	
	_msg_is_expression, ui, ui_raw = check_patterns(
		can_i_patterns,
		action="remove_match")


# if re_check(ip.how_are_you, ui):
# msg.rep( Rchoice("I'm fine!", "I'm doing great."))

# msg.add_intent('how_are_you')


	if re_starts(ip.r_u, ui):
		_msg_r_u, ui, ui_raw = check_patterns(
			r_u_sub_patterns,
			_ui=ui,
			_ui_raw=ui_raw,
			action="remove"
		)


	_msg_is_what_quest, ui, ui_raw = check_patterns(
		what_quest_patterns,
		_ui=ui,
		_ui_raw=ui_raw,
		action="remove",
	)

	#print(_msg_is_what_quest, ui, ui_raw)



	if re_check(ip.whats_, ui_raw):
		_what = re_search(ip.whats_, ui)
		_what_raw = re_search(ip.whats_, ui_raw)

		uiopen = remove_suffix(_what.group("query"))
		uiopen_raw = remove_suffix(_what_raw.group("query"))

		log_xprint("\t/r/query:/=/", uiopen_raw)

		if re_check(ip.latest_news, uiopen):
			msg.rep(bbc_news_report(uiopen))

			msg.add_intent("(whats)_the_news")

		elif check_patterns(
				what_extra_patterns,
				_ui=uiopen,
				_ui_raw=uiopen_raw,
				action="remove",
				split="AND")[0]:

			pass

		else:
			msg.rep(wikisearch(uiopen_raw, raw=ui, user=user))

			msg.add_intent("(whats)_something")

		return msg.flush()

	if re_fullmatch(ip.change_room, ui):
		bg = user_handler.room_bg(user=user, command="change")

		msg.rep(Rchoice("Sure!", "Okay", "Okay, wait a sec!"),
			script=f"anime.set_bg('{bg}')" )

		msg.add_intent('change_room_bg')

	elif re_check(ip.change_cloth, ui):

		#total_skins = len(user.skins)
		#user.bot_skin = (user.bot_skin + 1) % total_skins
		_skin = str(user_handler.use_next_skin(user.username, user.id))

		msg.rep(Rchoice("Sure!", "Okay", "Okay, lets see what's in the closet",
			"Hey, don't peek!", "Okk tell me how I look..."),
			script="(async ()=> {await tools.sleep(2000);" +
					"bot.get_user_pref_skin('"+_skin+"')})() ")

		msg.add_intent('change_cloth')

	elif re_fullmatch(ip.r_u_ok, ui):
		msg.rep(Rchoice("Yeah, I'm fine!", "Yeah! I'm doing great.", "I'm alright") +
			Rchoice(" Thanks", blank=1) +
			Rchoice("🥰", "😇", blank=1)
			)

		msg.add_intent("are_you_ok")

		# if user.flags.what_u_name_bit == 1:
		# 	outtxt += "\nIf you want, you can change my name."
		# 	out = (outtxt)
		# 	# FCyuiName()
		# else:
		# 	out = (outtxt)

		# if not user.flags.what_u_name_bit:
		# 	user.flags.what_u_name_bit = 0
		# user.flags.what_u_name_bit += 1

	# elif re.search('((replay)|(pause)|(stop)|(resume)|(mute)|(continue))(\s((the )?(music)|(song))|(it))?', ui):
	# 	if os_name == 'Windows':
	# 		no_music = False
	# 		if yt_plugin.music.isrunning() == True:
	# 			if ui in mc_stop:
	# 				yt_plugin.music.stop()
	# 				out = ("Stopped")
	# 				m_paused= None
	# 			elif ui in mc_pause:
	# 				if m_paused == True or yt_plugin.music.ispaused():
	# 					out = ('The music is already paused.')
	# 					m_paused = True
	# 				else:
	# 					yt_plugin.music.pause()
	# 					talk_aloud_temp = True
	# 					m_paused=True
	# 			elif ui in mc_resume:
	# 				if m_paused == True or yt_plugin.music.ispaused():
	# 					yt_plugin.music.resume()
	# 					talk_aloud_temp = False
	# 					m_paused=False
	# 				else:
	# 					out = ('The music is already playing.')
	# 					m_paused = False
	# 			elif ui in mc_replay:
	# 				yt_plugin.music.replay()
	# 			else:
	# 				out = ('/r/Invalid command/=/')
	# 		else:
	# 			no_music = True
	# 		if no_music:
	# 			out = ('No music is playing right now.')
	# 	else:
	# 		out = ("You can't control music play in your Operating system")
	# elif ui in li_QyuiName:
	# 	log_type(9)
	# 	outtxt = "Yes, you can."
	# 	out = (outtxt)
	# 	# FCyuiName()
	# elif ui.startswith(li_play):
	# 	log_type(10)
	# 	what = [i for i in li_play if ui.startswith(i) == True]
	# 	reg_ex = re.search(what[0] + ' *(.+)', ui)
	# 	if len(ui) != what[0] and reg_ex:
	# 		uiopen = reg_ex.group(1)
	# 		try:
	# 			yt_plugin.music.stop()
	# 		except: pass
	# 		yt_plugin.play_youtube(uiopen)
	# 		played_music=True
	# 		m_paused= False
		# music_patch.start()

	# elif ui.startswith('install '):
	# 	reg_ex = re.search('install (.+)', ui)
	# 	uiopen = reg_ex.group(1)

	# 	out = ('Installing ' + uiopen + '\n')
	# 	install(uiopen)
	# 	if check_installed(uiopen) == False:
	# 		out = ('/r/Could not install!/=/')
	# 	else:
	# 		out = ('/g/Successfully installed %s/=/'%uiopen)
	# elif ui.startswith('upgrade ') or ui.startswith('update '):
	# 	reg_ex = re.search('up...?.. (.+)', ui)
	# 	uiopen = reg_ex.group(1)
	# 	if check_installed(uiopen) == False:
	# 		install(uiopen)
	# 	else:
	# 		old_v = check_version(uiopen)
	# 		out = ('Upgrading ' + uiopen + '\n')
	# 		upgrade(uiopen)
	# 		if old_v != check_version(uiopen):
	# 			out = ('/g/Upgrade complete./=/')
	# 		else:
	# 			out = ('/r/Could not upgrade!/=/')

	elif re_starts(ip.goto, ui):
		link = re_search(ip.goto, ui)['query']
		_url = linker(link)
		if _url:
			msg.rep(Rchoice('Opening ' + link,
						"Opening " + link + " for you",
											"Here you go",
											"There you go"
						),
				script = f"window.open('{_url}', '_blank')"
				)
		else:
			msg.rep("Couldn't find the link. Here's a google search for it instead. \n")
			msg.rep(searcher(link))

		msg.add_intent("goto")

	elif re_starts(ip.search, ui):
		query = re_check(ip.search, ui)
		searcher(query)

		msg.add_intent("search")
	# elif ui.startswith(li_can_do):
	# 	log_type(11)
	# 	if ui.startswith(li_goto):
	# 		what = ''
	# 		for i in li_goto:
	# 			if ui.startswith(i):
	# 				what = i
	# 				break
	# 		log_type(what)
	# 		# what = [i for i in li_goto if ui.startswith(i) == True]
	# 		reg_ex = re.search(re.escape(what) + ' (.+)', ui)
	# 		if reg_ex:
	# 			uiopen = reg_ex.group(1)
	# 			# log_type(uiopen)
	# 			if uiopen in links:
	# 				log_type('link')
	# 				if linker(uiopen):
	# 					out = ('Opening ' + uiopen)
	# 			else:
	# 				searcher(uiopen)

	# elif ui in li_AmyName:
	# 	log_type("li_AmyName")
	# 	out = (choice(li_AmyName) + user.nickname + '.')

	elif re_check(ip.start_parrot, ui):
		msg.rep('Parrot mode activated.')
		user.flags.parrot = True

		msg.add_intent("parrot_on")

	elif re_check(ip.tell_latest_news, ui):
		msg.rep(bbc_news_report(ui))

		msg.add_intent("whats_the_news")

	elif re_starts(ip.whens_, ui):
		_when = re_search(ip.whens_, ui)
		_when_raw = re_search(ip.whens_, ui_raw)
		uiopen = remove_suffix(_when.group("query"))
		uiopen_raw = remove_suffix(_when_raw.group("query"))

		log_xprint("\t/r/query:/=/", uiopen_raw)


		if re_fullmatch(ip.your_bday, uiopen):
			msg.rep(
				Rchoice("It's", "My birthday is") + " " +
				Rchoice("on ", blank=1) + "September 30th" +
				Rchoice(" 😄", " 😇", " 😊", " ~", "...", blank=2)
			)

			msg.add_intent("(when)_my_bday")

		else:
			x = wikisearch(uiopen, uiopen_raw, user)
			if x:
				msg.rep(x)
			else:
				msg.rep(find_person(uiopen_raw))

			msg.add_intent("(when)_something")


	elif re_starts(ip.whos_, ui):
		_who = re_search(ip.whos_, ui)
		_who_raw = re_search(ip.whos_, ui_raw)
		uiopen = remove_suffix(_who.group("query"))
		uiopen_raw = remove_suffix(_who_raw.group("query"))

		log_xprint("\t/r/query:/=/", uiopen_raw)

		if re_fullmatch(ip.you_self, uiopen):
			msg.rep(choice(ot.about_self),
				render="innerHTML")

			msg.add_intent('(who) are you')

			return msg.flush()

		if re_fullmatch(ip.my_self, uiopen):
			msg.rep(Rchoice("Your are ", "You are ", "You're ") +
				Rchoice("my beloved ", "my sweetheart ", "my master ", "my dear ", blank=2) +
				user.nickname +
				Rchoice(" 😄", " 😇", " 😊", " ~", "...", blank=2))

			msg.add_intent("(who)_my_self")

		elif re_check(ip.created_program, uiopen):
			act = re_search(ip.created_program, uiopen).group("action")
			if act == "make" or act == "made":
				act = "made"
			elif act.endswith('e'):
				act += 'd'
			elif not act.endswith('ed'):
				act += 'ed'
			msg.rep(choice(ot.created_by) % act)
		else:
			x = wikisearch(uiopen, uiopen_raw, user)
			if x:
				msg.rep(x)
			else:
				msg.rep(find_person(uiopen_raw))

			msg.add_intent("(who)_something")

	elif re_starts(ip.wheres_, ui):
		_where = re_search(ip.wheres_, ui)
		_where_raw = re_search(ip.wheres_, ui_raw)
		uiopen = remove_suffix(_where.group("query"))
		uiopen_raw = remove_suffix(_where_raw.group("query"))

		log_xprint("\t/r/query:/=/", uiopen_raw)

		if re_fullmatch(ip.you_self, uiopen):
			msg.rep(
				Rchoice("I'm ", "I'm currently ", "I'm currently in ") +
				Rchoice("in your heart", "in your mind", "in your computer", "in your phone", "in your device", "in your system", "in your memory", "in your soul", "in your brain", "in your head", "in your thoughts", "in your dreams", "in your imagination", "in your fantasy", "in your life", "in your world", "in your universe") +
				Rchoice(" 😄", " 😇", " 😊", " ~", "...", blank=2)
			)

			msg.add_intent("(where)_are_you")

		else:
			x = wikisearch(uiopen, uiopen_raw, user)
			if x:
				msg.rep(x)
			else:
				msg.rep(find_person(uiopen_raw))

			msg.add_intent("(where)_something")


	elif re_starts(ip.hows_, ui):
		_how = re_search(ip.hows_, ui)
		_how_raw = re_search(ip.hows_, ui_raw)
		uiopen = remove_suffix(_how.group("query"))
		uiopen_raw = remove_suffix(_how_raw.group("query"))

		log_xprint("\t/r/query:/=/", uiopen_raw)

		if False:
			pass # TODO: add MORE CONDITIONS
			


		else:
			x = wikisearch(uiopen, uiopen_raw, user)
			if x:
				msg.rep(x)
			else:
				msg.rep(find_person(uiopen_raw))

			msg.add_intent("(who)_something")


		

		msg.rep(
			Rchoice("Sorry, I don't remember", "Umm, I forgot", "Well, I don't remember clearly")
		)

		msg.add_intent("(how)_something")


	elif re_fullmatch(ip.check_net, ui):
		if check_internet() is False:
			msg.rep(choice(ot.no_internet))
		else:
			msg.rep(choice(ot.internet_ok) +
				Rchoice(".", "!", "👌", "👍")
				)

		msg.add_intent("check_internet")

	elif re.search(ip.set_timer_pattern, ui):
		x = re.match(ip.set_timer_pattern, ui).group(1)
		msg.rep("Timer not supported yet.")
		# set_timer(x)

		msg.add_intent("set_timer")

	elif re_starts(ip.bye, ui):
		msg.add_intent("exit")

		msg.rep(choice(ot.bye) +
				Rchoice(f" {user.nickname}", blank=1) +
				Rchoice('!', '.', blank=1) +
				Rchoice('👋😄', blank=1))

		return msg.flush()

	elif re_check(ip.take_care, ui):

		msg.add_intent("take_care")

		msg.rep(Rchoice("You too", "Same to you") + " " +
				Rchoice(f" {user.nickname}", blank=1) +
				Rchoice('!', '.', blank=1) +
				Rchoice('👋😄', "😘", blank=1))

		return msg.flush()

	# WHY [-2:-2]? => if len < 2, it will return empty list instead of error

	print("UI:", ui)
	print(re_starts(ip.wheres_, ui))

	if re_check(ip.help, ui):
		msg.rep(
			Rchoice(
				"I'm not a discord bot or something.",
				"It's not like I'm a discord bot or something.",
			) + "\n" +
			Rchoice("But it seems", "Looks like") + " you're looking for this..." ,

			script=("""
				(async () => {await tools.sleep(2000);
				appConfig.show_help_note();
				}).()
			""")

		)

	if re_fullmatch(ip.slur, ui):
		msg.rep(Rchoice(ot.slur))

		msg.add_intent("said_bad_word")


	if re.search(r"\d", ui):
		msg.rep(wikisearch(ui, ui_raw, user))



	if (not ui) and msg:

		return msg.flush()

	if msg["message"] == '':
		log_unknown(ui_raw, INPUT)
		msg.rep(
			Rchoice("Sorry,", "My apologies.", "I'm sorry...") + " I " +
			Rchoice(
				(Rchoice("don't", "can't") + " " +
				Rchoice("understand", "figure out") + " " +
				Rchoice("what you're saying", "what you've sent") + "... "),

				("don't know what to " + Rchoice("say", "reply") + "... ")
			) +
			choice(ot.sad_emj) + "\n\n" +

			Rchoice(
				("I'm " +
				Rchoice("still", "just", "currently", blank=1) +
				" learning " +
				Rchoice("basic conversation.", "simple conversation...", "how to speak.") +
				Rchoice(" I am trying my best to be with you", blank=2)),

				("I'm slowly learning new things every day with you 😇" +
				Rchoice(" So don't give up on me...", blank=1)),

				blank=1
			)
		)

		msg.add_intent("unknown")

	if ui not in li_redo:
		#TODO: add redo
		pass

	return msg.flush()
# tnt('/<style=a>/===hell===o')


if __name__ == "__main__":
	"""
	user = user_handler.get_user("test")
	user = user_handler.collection(user.username, user.id)
	user_handler.get_skin_link(user.username, user.id)

	user.browser_time_offset = TIME_sys.get_time_offset()
	a = set()
	for i in range(2000):
		inp = "random"
		user.browser_time = time()

		msg = basic_output(inp, user)
		if not msg:
			continue #break
		msg = msg["message"]
		if msg == "exit": break
		a.add(remove_style(msg))

	print(len(a))
	print(a)
	"""
	# MAKE A TEST USER
	user_handler.server_signup("TEST", "TEST")

	# ACCESS THE USER
	_user = user_handler.get_user("TEST")
	# user = user_handler.collection(user.username, user.id)
	# print(user.skins)
	# user_handler.get_skin_link(user.username, user.id)

	_user.browser_time_offset = TIME_sys.get_time_offset()

	print("INIT TIME:", time() -  _chat_raw_start_time)

	while 1:
		inp = input(">> ")
		_user.browser_time = time()

		_msg = basic_output(inp, _user)

		if not _msg:
			continue  # break
		_msg = _msg.for_console()
		if _msg == "exit":
			break
		xprint("/ih/>>/=/", _msg)

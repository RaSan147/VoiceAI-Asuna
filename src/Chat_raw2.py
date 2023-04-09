from collections import Counter
import urllib.parse
import webbrowser
from random import choice
from typing import Union
import traceback
from time import time

import TIME_sys

from basic_conv_re_pattern import ip, ot, it, remove_suffix
from basic_conv_pattern import *
from CONFIG import appConfig
from user_handler import User, user_handler
# from DS import str2


# PIP PACKAGES

import requests
import wikipediaapi
from unidecode import unidecode
import wikix

# SELFMADE LIBS

from bbc_news import bbc_news
import F_sys
from OS_sys import check_internet
from REGEX_TOOLS import re_search, re_starts, re_check, re_is_in
from PRINT_TEXT3 import xprint, remove_style
from DATA_sys import call_or_return

import net_sys

# CHAT PATTERN LIBS

from chat_can_you import patterns as can_you_patterns
from chat_can_i import patterns as can_you_patterns
from chat_expressions import patterns as expressions_patterns
from chat_what_extra import patterns as what_extra_patterns
from chat_about_bot import patterns as about_bot_patterns
from chat_compliment import patterns as compliments_patterns
from chat_r_u_patterns import patterns as r_u_sub_patterns

import re
re._MAXCACHE = 1024  # increase regex cache size



__all__ = ('basic_output',)

LOG_DEBUG = True




wikipedia = wikipediaapi.Wikipedia('en')
bbc_topic = 'Asia_url'


def log_unknown(*args, **kwargs):
	F_sys.writer(appConfig.log_unknown, "a", str(list(args)) + "\n", timeout=0)



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


def searcher(search_txt):
	"""
	return the google link for search_txt query
	"""
	loc = urllib.parse.quote(search_txt)
	return {"message": f'Please check here <a href="https://www.google.com/search?q={loc}">{search_txt}</a>',
			"render": "innerHTML"
			}


def wolfram(text, raw=''):
	"""
	returns wolfram alpha response based on query text
	text: query
	raw: the untouched user input for logging
	"""
	r = requests.get("http://api.wolframalpha.com/v1/spoken",
					 params={
						 "i": text,
						 "appid": "L32A8W-J8X5U6KG26"
					 }
					)
	if not r:
		return False
	return r.text


def _wiki(uix):
	"""
	search in wikipedia,
	split only 4 sentences 
	parse results to HTML
	"""
	ny = wikipedia.page(uix)
	link = ny.fullurl
			
	# returns 4 line of summary
	s = ny.summary
	s = s.replace("\n", "<br>")
	s = re.sub("</?br>", " <br>", s)
	s = re.sub("( ){2,}", " ", s)
	s = (". ").join(ny.summary.split(". ")[:4])
	
	return link, s
			


def wikisearch(uix='', raw='', user: User = None):
	"""
	search for text response for data query.
	1st, checks for wolfram alpha response 
	2nd, checks if there's any data in wikipedia
	3rd, after failing above, returns google search link
	"""
	
	if not check_internet():
		return 'No internet connection!'
		
	if user:
		uix = parsed_names_back(uix, user)
		
	wolf = wolfram(uix)
	if wolf:
		return wolf
		
	xprint("\t/c/Searching wiki:/=/", uix)
	
	try:
		_uix = wikix.fix_promt(uix)
		wiki_search= [i.title for i in wikix.search(_uix, 5)]
		
		
		# using unidecode for pokemon and pokémon issue
		match_search = [i for i in wiki_search if unidecode(uix.lower()) in unidecode(i.lower())]
				
		log_xprint("\t/c/Found wiki:/=/", wiki_search)
		log_xprint("\t/c/Match wiki:/=/", match_search)
		
			
		if match_search:
			uix_ = match_search[0]
			log_xprint("\t/c/Getting wiki:/=/", uix_)
		
			link, response = _wiki(uix_)
			return {"message": response + 'f\n\n<a href={link}">Read More</a>',
				"render": "innerHTML"
				}

		if wiki_search:
			uix_ = wiki_search[0]
	
			out = 'Did you mean ' + uix_ + '? '
			
			if not user:
				return out
				
			
			user.flags.ask_yes = user.msg_id
				
			link, response = _wiki(uix_)
			user.flags.on_yes = {"message": response + 'f\n\n<a href={link}">Read More</a>',
				"render": "innerHTML"
			}
			return out
	
	except Exception:
		xprint("/r/Failed to wiki/=/: ", uix, "\n\n")
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

def find_person(name, user:User = None):
	# return searcher(name)
	return wikisearch(name, name, user)
 



def parsed_names(ui, user: User):
	"""Replace variable nicknames with constant strings"""
	ui = re.sub(re.escape(user.ai_name), "<:ai_name>", ui, flags=re.IGNORECASE)
	ui = re.sub(re.escape(user.nickname), "<:u_name>", ui, re.IGNORECASE)
	return ui


def parsed_names_back(ui, user: User):
	"""Replace constant strings with variable nicknames"""
	ui = ui.replace("<:ai_name>", user.ai_name)
	ui = ui.replace("<:u_name>", user.nickname)

	return ui


def preprocess(in_dat):
	""" replace . , " ' ? ! with space """
	# in_dat = in_dat.replace("'", " ")
	in_dat = in_dat.replace("?", " ")
	in_dat = in_dat.replace("!", " ")
	in_dat = in_dat.replace(",", " ")
	in_dat = in_dat.strip()
	in_dat = re.sub(r'\s{2,}', ' ', in_dat)
	# in_dat = in_dat.replace(" us ", " me")
	# in_dat = in_dat.replace(" him", " me")
	# in_dat = in_dat.replace(" her", " me")
	# in_dat = in_dat.replace(" them", " me")

	return in_dat


def pre_rem_bot_call(ui):
	""" 
		* remove *hey* whats ....
		* remove *hey Asuna* whats ....

	"""
	nick = "<:ai_name>"
	ui = re.sub(
		rf'^(hey|miss|dear|yo)? ?(girl|babe|{nick})? ', '', ui, flags=re.IGNORECASE)

	ui = re.sub(r'^(please|plz) ', '', ui, flags=re.IGNORECASE)

	return ui


def post_rem_can_you(ui):
	"""
		0. remove `*can you* ....`
		1. remove `*will you* ....`
		2. remove `*do you know* ....`

		3. replace `*tell me* ....` with `....`
		4. remove `*tell me regarding* ....` with `*about* ....`
	"""
	ui = re.sub(r'^((can|will|do|did) ((yo)?u|y(a|o)))?( please| plz)?( even)? ?(know|tell|remember|speak|say)?( to)?( me)? (?P<msg>.+)',
				r'\g<msg>', ui, flags=re.IGNORECASE)
	ui = re.sub(r'^(of|regarding) ', 'about ', ui, flags=re.IGNORECASE)

	return ui


def Rchoice(*args, blank=0):
	"""
		return `random choice` from (args and blank `""`)
	"""
	b = ['']*blank
	return choice([*args, *b])


# default message dict
message_dict = {
	"message": "",
	"render": "innerText",
	"script": ""
}


def basic_output(INPUT, user: User = None, username: str = ""):
	"""
		INPUT: user input
		user: User object
		username: username of user (if `user` object is not provided)
	"""
	receive_time = time()

	if user is None and username:
		user = user_handler.get_user(username)

	_INPUT = parsed_names(INPUT, user)
	_INPUT = preprocess(_INPUT)
	_ui_raw = pre_rem_bot_call(_INPUT)
	_ui = _ui_raw.lower().replace(".", " ").replace("'", " ")  # remove . from input
	# keep . in raw to make sure its not removed it mathmatical expressions
	log_xprint(f"\t/hi/{INPUT}/=/ >> /chi/{_ui_raw}/=/ ")
	if _ui == "":
		return

	user.user_client_dt = user.get_user_dt()
	# update client datetime

	# why raw?? because we want to keep the . in mathmatical expressions and CAPITALS
	mid = user.add_chat(INPUT, receive_time, 1, _ui_raw)
	# mid = message id
	
	log_xprint(f"\t/c/`{user.username}` msg id: /=/", mid)
	msg = message_dict.copy()
	out, intent, on_context, ui, ui_raw = _basic_output(INPUT, user, _ui, _ui_raw, mid)
	user.chat.intent.append(intent)

	xprint(f"\t/i/intent:/=/ {intent}")

	msg["rTo"] = mid  # reply to id # can be used in HTML to scroll to the message

	if not out:
		log_unknown(ui_raw, INPUT)
		out = "I don't know what to say..."
	if isinstance(out, dict):
		message = out["message"]
		msg.update(out)

	else:
		message = out
	
	message = parsed_names_back(message, user)
	
	message = remove_style(message)
	msg["message"] = message.strip()

	if msg["render"] == "innerHTML":
		msg["message"] = net_sys.str2html(msg["message"])

	processed_time = time()
	user.add_chat(msg, processed_time, 0, rTo=mid, intent=intent, context=on_context)
	
	
	print(f"\tRESP time: {time()-receive_time}s")
	return msg


def _basic_output(INPUT: str, user: User, ui: str, ui_raw: str, mid: int):
	"""
		Input:  UNTOUCHED user input
		user:   user object
		ui_raw: (cleaned) user input
		ui:     (cleaned lower case) user input
		mid:     msg id
	"""
	# out = str2()
	# out = str()
	out = message_dict.copy()

	_intent = []  # intent of the current message
	# intent of the previous message
	prev_intent = user.chat.intent[-1] if user.chat.intent else []
	# context [[...],...] is the intent of the previous message
	_context = Counter([j for i in user.chat.intent for j in i])
	# intent of the current message that is based on the previous message intent (context)
	on_context = []

	# print("context: ", _context)

	def intent(i):
		nonlocal _intent

		_intent.append(i)

	def add_context(i: str):
		"""
		if bot replies based on previous message intent (context),
		then the bot will add the intent to the context list
		"""
		nonlocal on_context

		on_context.append(i)

	def check_context(context=()):
		"""
		check if any of the context list is in previous msg intent
		"""
		for i in context:
			if i in prev_intent:
				return True

	def clean():
		"""
		forgot what it is
		"""
		nonlocal out
		out = message_dict.copy()

	def rep(msg_txt, script="", render=""):
		"""add message to the output"""
		nonlocal out

		if isinstance(msg_txt, dict):
			_msg_txt = msg_txt["message"]
			script = msg_txt.get("script", "")
			render = msg_txt.get("render", "")
			msg_txt = _msg_txt

		out["message"] += "\n\n" + str(msg_txt)

		if render:
			out["render"] = str(render)

		if script:
			out["script"] += "\n\n" + str(script)

		return out

	def flush():
		"""flush the output, intent and context"""
		return out, _intent, on_context, ui, ui_raw

	def rand_out(outputs: Union[list, tuple, str]):
		"""
		randomly send a string from a list
		"""
		if isinstance(outputs, str):
			return outputs
		return choice(outputs)

	def check_patterns(patterns, _ui=None, _ui_raw=None, action=None, split=None):
		"""
		check for pattern match in list of patterns,
		if match add the reply in out and intent,
		if matched part needs to be removed, thats also done here,
		if input needs to be split before checking for multiple query (based of different type , like sentence , and etc), using split that is done
		"""
		if _ui is None:
			_ui = ui
		if _ui_raw is None:
			_ui_raw = ui_raw

		found = False
		if split=="AND":
			uiParts = re.split(" (?:a?nd?|&) ", _ui)
			uiRParts = re.split(" (?:a?nd?|&) ", _ui_raw, flags=re.IGNORECASE)
		elif split=="LINE":
			uiParts = _ui.split("\n")
			uiRParts = _ui_raw.split("\n")
		elif split=="SENTENCE":
			uiParts = re.split("(?<=[.!?]) +", _ui)
			uiRParts = re.split("(?<=[.!?]) +", _ui_raw)
		else:
			uiParts = [_ui]
			uiRParts = [_ui_raw]


		to_del = []

		for ptrn, otpt, intnt in patterns:
			for n, i in enumerate(uiParts):
				m = re_search(ptrn, i, PRINT_PATTERN=LOG_DEBUG)
				if m:
					rep(rand_out(otpt))
					intent(intnt)

					if action == "remove":
						# uiParts[n] = re.sub(m.Pattern, '', i)
						# uiParts[n] = uiParts[n].replace(m.group(0), "")
						to_del.append(n)
					if action == "remove_match":
						uiParts[n] = re.sub(m.re.pattern, '', i).strip()
						uiRParts[n] = re.sub(
							m.re.pattern, '', uiRParts[n]).strip()

					found = True
					# tell me about yourself *and* your favourite hobby
					continue  # so that same question won't give repeated answers

		for index in sorted(to_del, reverse=True):
			uiParts.pop(index)
			uiRParts.pop(index)

		return (found, " and ".join(uiParts).strip(), " and ".join(uiRParts).strip())

	# global talk_aloud_temp, reloader, ui, ui1, ui2, case, cases, uibit1, uibit2, reloader, reloaded, BREAK_POINT, m_paused

	log_xprint("\t/c/Flags: /=/", user.flags)

	if user.flags.parrot:
		if re_is_in(ip.stop_parrot, ui):
			user.flags.parrot = False
			rep(
				Rchoice("Okay!", "Alright!", "Alright, I'll stop.", "Okay, I'll stop.")
			)
			intent('stop_parrot')
		else:
			rep(INPUT)
			add_context('parrot_say')
		return flush()
	
	if re_is_in(ip.logout, ui):
		rep("Logging out...",
			script="""
				await tools.sleep(1000)
				user.logout()
				"""
			)
		intent('logout')
		return flush()
		

	if user.flags.ask_yes and (user.flags.ask_yes > user.msg_id-3):
		if re_is_in(ip.yeses, ui):
			
			if user.flags.on_yes:
				rep(call_or_return(user.flags.on_yes))
			
			intent("accept_yes_no")
		elif re_is_in(ip.no, ui):
			if user.flags.on_no:
				rep(call_or_return(user.flags.on_no))
			
			else:
				rep("Got it!")
			
			intent("decline_yes_no")

		user.flags.ask_yes = user.flags.on_yes = None
		

	# CHECK IF USER IS ASKING IF AI CAN DO SOMETHING
	_msg_is_expression, ui, ui_raw = check_patterns(
		can_you_patterns(context=_context, check_context=check_context),
		action="remove_match",
		split="AND")

	# remove "can you" from the beginning of the sentence
	ui_raw = post_rem_can_you(ui_raw)
	ui = ui_raw.lower()  # convert to lower case
	

	_msg_is_expression, ui, ui_raw = check_patterns(
		compliments_patterns(context=_context, check_context=check_context),
		action="remove_match")
	

	_msg_is_expression, ui, ui_raw = check_patterns(
		expressions_patterns(
			context=_context, check_context=check_context),
			action="remove_match")
	
	
# if re_check(ip.how_are_you, ui):
# rep( Rchoice("I'm fine!", "I'm doing great."))

# intent('how_are_you')


	if re_starts(ip.r_u, ui):
		_msg_is_expression, ui, ui_raw = check_patterns(
			r_u_sub_patterns(context=_context, check_context=check_context), 
			_ui=ui, 
			_ui_raw=ui_raw, 
			action="remove")


	if re_check(ip.whats_your_name, ui):
		rep(choice(ot.my_name_is) + user.ai_name)

		intent('whats_your_name')

	elif re_check(ip.what_to_call_you, ui):
		rep(choice(ot.call_me) + user.ai_name + choice(ot.happy_emj))

		intent('what_to_call_you')

	elif re_check(ip.what_time, ui):
		rep(choice(ot.tell_time) + user.user_client_dt.strftime("%I:%M %p."))

		intent('whats_the_time')

	elif re_check(ip.whats_up, ui):
		rep(choice(ot.on_whats_up))

		intent("whats_up")

	elif re_check(ip.whats_, ui_raw):
		_what = re_search(ip.whats_, ui)
		_what_raw = re_search(ip.whats_, ui_raw)

		uiopen = remove_suffix(_what.group("query"))
		uiopen_raw = remove_suffix(_what_raw.group("query"))
		
		log_xprint("\t/r/query:/=/", uiopen_raw)

		if re_is_in(ip.you_self, uiopen):
			rep(choice(ot.about_self),
				render="innerHTML")

			intent('what are you')
			return flush()

		if uiopen in it.my_name:
			rep(Rchoice("Your name is ", "You are ", "You're ") +
				user.nickname +
				Rchoice(" 😄", " 😇", " 😊", " ~", "...", blank=2))

			intent("(whats)_my_name")

		elif re_is_in(ip.my_self, uiopen):
			rep(Rchoice("Your are ", "You are ", "You're ") +
				Rchoice("my beloved ", "my sweetheart ", "my master ", "my dear ", blank=2) +
				user.nickname +
				Rchoice(" 😄", " 😇", " 😊", " ~", "...", blank=2))

			intent("(what)_my_self")
			
		elif re_is_in(ip.your_bday, uiopen):
			rep(
				Rchoice("It's", "My birthday is") + " " + 
				Rchoice("on ", blank=1) + "September 30th" +
				Rchoice(" 😄", " 😇", " 😊", " ~", "...", blank=2)
			)
			
			intent("(what)_my_bday")

		elif re.match("(current )?time( is| it)*( now)?", uiopen):
			rep(choice(ot.tell_time) + user.user_client_dt.strftime("%I:%M %p."))

			intent("(whats)_the_time")

		elif re_check(ip.latest_news, uiopen):
			if check_internet():
				news = bbc_news.task(bbc_topic)
				if news is None:
					rep("No news available")
				else:
					rep("".join(news[:5]))
					# asker("Do you want to hear the rest?", true_func=read_rest_news)

			else:
				rep('Sorry, No internet!')

			intent("(whats)_the_news")

		elif check_patterns(
				what_extra_patterns(context=_context, check_context=check_context),
				_ui=uiopen,
				_ui_raw=uiopen_raw,
				action="remove",
				split="AND")[0]:

			pass

		else:
			rep(wikisearch(uiopen_raw, raw=ui, user=user))

			intent("(whats)_something")

		return flush()

	if re_check(ip.change_cloth, ui):

		total_skins = len(user.skins)
		#user.bot_skin = (user.bot_skin + 1) % total_skins
		_skin = user_handler.use_next_skin(user.username, user.id)

		rep(Rchoice("Sure!", "Okay", "Okay, let me change my clothes",
			"Hey, don't peek!", "Okk tell me how I look..."),
			script="(async ()=> {await tools.sleep(2000); bot.get_user_pref_skin('"+_skin+"')})() ")

		intent('change_cloth')

	elif re_check(ip.change_room, ui):
		bg = user_handler.room_bg(user=user, command="change")

		rep(Rchoice("Sure!", "Okay", "Okay, wait a sec!"),
			script=f"anime.set_bg('{bg}')" )

		intent('change_room_bg')

	elif re_check(ip.r_u_ok, ui):
		rep(Rchoice("Yeah, I'm fine!", "Yeah! I'm doing great.", "I'm alright") +
			Rchoice(" Thanks", blank=1) +
			Rchoice("🥰", "😇", blank=1)
			)

		intent("are_you_ok")

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
			rep(Rchoice('Opening ' + link,
						"Opening " + link + " for you",
											"Here you go",
											"There you go"
						),
				script = f"window.open('{_url}', '_blank')"
				)
		else:
			rep("Couldn't find the link. Here's a google search for it instead. \n")
			rep(searcher(link))

		intent("goto")

	elif re_starts(ip.search, ui):
		query = re_check(ip.search, ui)
		searcher(query)

		intent("search")
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

	elif ui in start_parrot:
		rep('Parrot mode activated.')
		user.flags.parrot = True

		intent("parrot_on")

	elif re_check(ip.tell_latest_news, ui):
		if check_internet():
			news = bbc_news.task(bbc_topic)
			if news is None:
				rep('No news available')
			else:
				rep("".join(news[:5]))
				# asker("Do you want to read more?", true_func=lambda: out = (*news[5:15]))
		else:
			rep('No internet!')

		intent("whats_the_news")

	elif re_starts(ip.whens_, ui):
		_when = re_search(ip.whens_, ui)
		_when_raw = re_search(ip.whens_, ui_raw)
		uiopen = remove_suffix(_when.group("query"))
		uiopen_raw = remove_suffix(_when_raw.group("query"))
		
		log_xprint("\t/r/query:/=/", uiopen_raw)

		
		if re_is_in(ip.your_bday, uiopen):
			rep(
				Rchoice("It's", "My birthday is") + " " + 
				Rchoice("on ", blank=1) + "September 30th" +
				Rchoice(" 😄", " 😇", " 😊", " ~", "...", blank=2)
			)
			
			intent("(what)_my_bday")
		
		else:
			x = wikisearch(uiopen, uiopen_raw, user)
			if x:
				rep(x)
			else:
				rep(find_person(uiopen_raw))
				
			intent("(when)_something")
 

	elif re_starts(ip.whos_, ui):
		_who = re_search(ip.whos_, ui)
		_who_raw = re_search(ip.whos_, ui_raw)
		uiopen = remove_suffix(_who.group("query"))
		uiopen_raw = remove_suffix(_who_raw.group("query"))
		
		log_xprint("\t/r/query:/=/", uiopen_raw)

		if re_is_in(ip.you_self, uiopen):
			rep(choice(ot.about_self),
				render="innerHTML")

			intent('(who) are you')

			return flush()

		if re_is_in(ip.my_self, uiopen):
			rep(Rchoice("Your are ", "You are ", "You're ") +
				Rchoice("my beloved ", "my sweetheart ", "my master ", "my dear ", blank=2) +
				user.nickname +
				Rchoice(" 😄", " 😇", " 😊", " ~", "...", blank=2))

			intent("(who)_my_self")

		elif re_check(ip.created_program, uiopen):
			act = re_search(ip.created_program, uiopen).group("action")
			if act == "make":
				act = "made"
			elif not act.endswith('ed'):
				act += 'ed'
			rep(choice(li_Acreator) % act)
		else:
			x = wikisearch(uiopen, uiopen_raw, user)
			if x:
				rep(x)
			else:
				rep(find_person(uiopen_raw))

			intent("(who)_something")

	elif ui in li_check_int:
		if check_internet() == False:
			rep("No internet available.")
		else:
			rep("Internet connection available.")

		intent("check_internet")

	elif re.search(set_timer_pattern, ui):
		x = re.match(set_timer_pattern, ui).group(1)
		rep("Timer not supported yet.")
		# set_timer(x)

		intent("set_timer")

	elif re_check(ip.bye, ui):
		intent("exit")

		out = (choice(li_bye) +
				Rchoice(f" {user.nickname}", blank=1) +
				Rchoice('!', '.', blank=1) +
				Rchoice('👋😄', blank=1))

		return flush()
		
	elif re_check(ip.take_care, ui):
		
		intent("take_care")

		out = (Rchoice("You too", "Same to you") + " " +
				Rchoice(f" {user.nickname}", blank=1) +
				Rchoice('!', '.', blank=1) +
				Rchoice('👋😄', "😘", blank=1))

		return flush()

	# WHY [-2:-2]? => if len < 2, it will return empty list instead of error
	# print(user.chat.intent)
	_msg_is_about_ai, ui, ui_raw = check_patterns(
		about_bot_patterns(context=_context, check_context=check_context),
		action="remove",
		split="AND")


	if re_check(ip.help, ui):
		rep(
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
		
	if re.search(r"\d", ui):
		rep(wikisearch(ui, ui_raw, user))



	if (not ui) and out:

		return flush()

	if out["message"] == '':
		log_unknown(ui_raw, INPUT)
		out = (
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

		intent("unknown")

	if ui not in li_redo:
		#TODO: add redo
		pass

	return flush()
# tnt('/<style=a>/===hell===o')


if __name__ == "__main__":
	"""
	user = user_handler.get_user("test")
	user = user_handler.collection(user.username, user.id)
	user_handler.get_skin_link(user.username, user.id)

	user.user_client_time_offset = TIME_sys.get_time_offset()
	a = set()
	for i in range(2000):
		inp = "random"
		user.user_client_time = time()

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
	user = user_handler.get_user("TEST")
	# user = user_handler.collection(user.username, user.id)
	# print(user.skins)
	# user_handler.get_skin_link(user.username, user.id)

	user.user_client_time_offset = TIME_sys.get_time_offset()

	while 1:
		inp = input(">> ")
		user.user_client_time = time()

		_msg = basic_output(inp, user)

		if not _msg:
			continue  # break
		_msg = net_sys.html2str(_msg["message"])
		if _msg == "exit":
			break
		xprint("/ih/>>/=/", _msg)

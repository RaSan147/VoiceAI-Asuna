
from collections import Counter
import urllib.parse
import webbrowser
from random import choice
from typing import Union


from basic_conv_re_pattern import ip, ot, it, remove_suffix
from basic_conv_pattern import *
from CONFIG import appConfig
from user_handler import User, user_handler
from DS import str2

# import datetime

from time import sleep, time
import TIME_sys



# PIP PACKAGES

import requests
import wikipedia

# SELFMADE LIBS

from bbc_news import bbc_news
import F_sys
from OS_sys import check_internet
from REGEX_TOOLS import re_search, re_starts, re_check, re_is_in
from PRINT_TEXT3 import xprint, remove_style

# CHAT PATTERN LIBS

from chat_can_you import patterns as can_you_patterns
from chat_expressions import patterns as expressions_patterns
from chat_what_extra import patterns as what_extra_patterns
from chat_about_bot import patterns as about_bot_patterns

import re
re._MAXCACHE = 1024  # increase regex cache size



__all__ = ('basic_output',)





bbc_topic = 'Asia_url'


def log_unknown(*args, **kwargs):
	F_sys.writer(appConfig.log_unknown, "a", str(list(args)) + "\n", timeout=0)


def log_type(*args, **kwargs):
	xprint("USER INPUT", *args, **kwargs, end="\n\n")


def web_go(link):
	webbrowser.open_new_tab(link)


# web_go('C:/Users/Dell/Documents/Python/Project_Asuna/datapy.html')
def linker(link):
	"""Match for link url and open the link in browser"""
	for i in links_li:
		if link in i:
			web_go(i[0])
			return True

	return False


def searcher(search_txt):
	loc = urllib.parse.quote(search_txt)
	return {"message": f'<a href="https://www.google.com/search?q={loc}">{search_txt}</a>',
			"render": "innerHTML"
			}


def find_person(name):
	return searcher(name)


def wolfram(text, raw=''):
	r = requests.get("http://api.wolframalpha.com/v1/spoken",
					 params={
						 "i": text,
						 "appid": "L32A8W-J8X5U6KG26"
					 }
					)
	if not r:
		return False
	return r.text


def _wiki(uix, raw=''):
	if uix in [i.lower() for i in wikipedia.search(uix)]:
		ny = wikipedia.page(uix)
		return {"message": wikipedia.summary(uix, sentences=2) + 'f\n<a href={ny.url}">More</a>',
				"render": "innerHTML"
				}

	elif wikipedia.search(uix) != []:
		uix = wikipedia.search(uix)[0]

		out = 'Did you mean ' + uix + '? '
	else:
		log_unknown(uix, raw)
		out = "Couldn't find " + uix + "!\nWould you like to search instead?  "

	return out


def wikisearch(uix, raw='', user: User = None):
	if check_internet() == True:
		wolf = wolfram(uix)
		if not wolf:
			log_unknown(uix, raw)
			safe_string = urllib.parse.quote_plus(uix)
			link = "https://www.google.com/search?q=" + safe_string

			if user:
				# TODO: add to user flags for later use "yes/no" message
				user.flags

			return {"message": f"I don't know the answer ...\nShall I <a href='{link}' target='_blank'>Google</a>?",
					"render": "innerHTML"
					}

		return wolf

	else:
		return 'No internet connection!'


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

	ui = re.sub(r'^please ', '', ui, flags=re.IGNORECASE)

	return ui


def post_rem_can_you(ui):
	"""
		0. remove `*can you* ....`
		1. remove `*will you* ....`
		2. remove `*do you know* ....`

		3. replace `*tell me* ....` with `....`
		4. remove `*tell me regarding* ....` with `*about* ....`
	"""
	ui = re.sub(r'^(((can|will|do|did) ((yo)?u|y(a|o)) )?(please )?(even )?(know|tell|remember|speak|say)( to)? me)? (?P<msg>.+)',
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
	if user is None and username:
		user = user_handler.get_user(username)

	_INPUT = parsed_names(INPUT, user)
	_INPUT = preprocess(_INPUT)
	_ui_raw = pre_rem_bot_call(_INPUT)
	_ui = _ui_raw.lower().replace(".", " ").replace("'", " ")  # remove . from input
	# keep . in raw to make sure its not removed it mathmatical expressions
	xprint(f"\t/hi/{INPUT}/=/ >> /chi/{_ui_raw}/=/")
	if _ui == "":
		return

	user.user_client_dt = user.get_user_dt()
	# update client datetime

	_time = time()
	# why raw?? because we want to keep the . in mathmatical expressions and CAPITALS
	id = user.add_chat(INPUT, _time, 1, _ui_raw)
	xprint("\t/c/user msg id: /=/", id)
	msg = message_dict.copy()
	out, intent, on_context, ui, ui_raw = _basic_output(INPUT, user, _ui, _ui_raw, id)
	user.chat.intent.append(intent)

	xprint(f"\t/i/intent:/=/ {intent}")

	msg["rTo"] = id  # reply to id # can be used in HTML to scroll to the message

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
		msg["message"] = msg["message"].replace("\n", "<br>")

	_time = time()
	user.add_chat(msg, _time, 0, rTo=id, intent=intent, context=on_context)
	return msg


def _basic_output(INPUT: str, user: User, ui: str, ui_raw: str, id: int):
	"""
		Input:  UNTOUCHED user input
		user:   user object
		ui_raw: (cleaned) user input
		ui:     (cleaned lower case) user input
		id:     chat id
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

	def check_context(context=[]):
		for i in context:
			if i in prev_intent:
				return True

	def clean():
		nonlocal out
		out = message_dict.copy()

	def rep(msg_txt, script="", render=""):
		"""add message to the output"""
		nonlocal out

		out["message"] += "\n\n" + msg_txt

		if render:
			out["render"] = render

		if script:
			out["script"] += script

		return out

	def flush():
		"""flush the output, intent and context"""
		return out, _intent, on_context, ui, ui_raw

	def rand_out(outputs: Union[list, tuple, str]):
		if isinstance(outputs, str):
			return outputs
		return choice(outputs)

	def check_patterns(patterns, ui=ui, ui_raw=ui_raw, action=None):
		found = False
		uiParts = re.split(" (?:a?nd?|&) ", ui)
		uiRParts = re.split(" (?:a?nd?|&) ", ui_raw, flags=re.IGNORECASE)

		to_del = []

		for ptrn, otpt, intnt in patterns:
			for n, i in enumerate(uiParts):
				m = re_search(ptrn, i)
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

	xprint("\t/c/Flags: /=/", user.flags)

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

	# CHECK IF USER IS ASKING IF AI CAN DO SOMETHING
	_msg_is_expression, ui, ui_raw = check_patterns(
		can_you_patterns(context=_context, check_context=check_context), action="remove_match")

	# remove "can you" from the beginning of the sentence
	ui_raw = post_rem_can_you(ui_raw)
	ui = ui_raw.lower()  # convert to lower case

	_msg_is_expression, ui, ui_raw = check_patterns(
		expressions_patterns(context=_context, check_context=check_context), action="remove_match")

# if re_check(ip.how_are_you, ui):
# rep( Rchoice("I'm fine!", "I'm doing great."))

# intent('how_are_you')

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
		xprint("\t/r/query:/=/", uiopen_raw)

		if re_is_in(ip.you_self, uiopen):
			rep(choice(ot.about_self),
				render="innerHTML")

			intent('what are you')
			return flush()

		elif uiopen in it.my_name:
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
				what_extra_patterns(context=_context, check_context=check_context), ui=uiopen, ui_raw=uiopen_raw, action="remove")[0]:

			return flush()

		else:
			rep(wikisearch(uiopen_raw, raw=ui, user=user))

			intent("(whats)_something")

			return flush()

	if ui in it.change_cloth:
		# TODO: NEED TO ADD IN PATTERNS
		rep(Rchoice("Sure!", "Okay", "Okay, let me change my clothes",
			"Hey, don't peek!", "Okk tell me how I look..."))
		case = 'change_cloth'
		total_skins = len(user.skins)
		user.bot_skin = (user.bot_skin + 1) % total_skins
		_skin = user_handler.use_next_skin(user.username, user.id)

		# _skin = str(user.bot_skin)

		out = {
			"message": out,
			"script": "(async ()=> {await tools.sleep(2000); bot.get_user_pref_skin('"+_skin+"')})()"
		}

		intent('change_cloth')

	elif ui in it.change_room:
		# TODO: NEED TO ADD IN PATTERNS
		rep(Rchoice("Sure!", "Okay", "Okay, wait a sec!"))

		bg = user_handler.room_bg(user=user, command="change")

		out = {
			"message": out,
			"script": f"anime.set_bg('{bg}')"
		}

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
						))
		else:
			rep('No such link found')

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

	elif re_starts(ip.whos_, ui):
		_who = re_search(ip.whos_, ui)
		_who_raw = re_search(ip.whos_, ui_raw)
		uiopen = remove_suffix(_who.group("query"))
		uiopen_raw = remove_suffix(_who_raw.group("query"))
		xprint("\t/r/query:/=/", uiopen_raw)

		if re_is_in(ip.you_self, uiopen):
			rep(choice(ot.about_self),
				render="innerHTML")

			intent('(who) are you')

			return flush()

		elif re_is_in(ip.my_self, uiopen):
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
			x = wikisearch(uiopen_raw, user)
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

	elif ui in escape:
		reloaded = False
		reloader = False
		BREAK_POINT = True

		intent("exit")

		out = (choice(li_bye) +
				Rchoice(f" {user.nickname}", blank=1) +
				Rchoice('!', '.', blank=1) +
				Rchoice('👋😄', blank=1))

		return flush()

	# WHY [-2:-2]? => if len < 2, it will return empty list instead of error
	# print(user.chat.intent)
	_msg_is_about_ai, ui, ui_raw = check_patterns(
		about_bot_patterns(context=_context, check_context=check_context), action="remove")

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

		uibit1 = 1
	ui1 = ui
	if ui not in li_redo:
		ui2 = ui

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

	user = user_handler.get_user("Ray")
	user = user_handler.collection(user.username, user.id)
	user_handler.get_skin_link(user.username, user.id)

	user.user_client_time_offset = TIME_sys.get_time_offset()

	while 1:
		inp = input(">> ")
		user.user_client_time = time()
		tt = time()
		msg = basic_output(inp, user)
		print(f"\tRESP time: {time()-tt}s")
		if not msg:
			continue  # break
		msg = msg["message"]
		if msg == "exit":
			break
		xprint("/ih/>>/=/", msg)

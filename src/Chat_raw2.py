__all__ = ('basic_output',)


import re
from random import choice
import webbrowser
import datetime
from time import sleep, time
import urllib.parse

import wikipedia

import requests

from PRINT_TEXT3 import xprint, remove_style

from basic_conv_pattern import *
from basic_conv_re_pattern import ip, ot, it, remove_suffix

from REGEX_TOOLS import re_search, re_starts, re_check, re_is_in

from OS_sys import os_name, check_internet
import F_sys

import yt_plugin
from bbc_news import bbc_news

import TIME_sys
from DS import str2

from user_handler import User, user_handler
from CONFIG import appConfig




from chat_about_bot import patterns as about_bot_patterns




bbc_topic = 'Asia_url'

def log_unknown(*args, **kwargs):
	F_sys.writer(appConfig.log_unknown, "a", str(args) + "\n", timeout=0)


def log_type(*args, **kwargs):
	xprint("USER INPUT", *args, **kwargs, end="\n\n")
	
	
	



def web_go(link):
	webbrowser.open_new_tab(link)


# web_go('C:/Users/Dell/Documents/Python/Project_Asuna/datapy.html')
def linker(link):
	for i in links_li:
		# print(i[0])
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
	params = {
		"i": text,
		"appid": "L32A8W-J8X5U6KG26"
	})
	if not r: return False
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
			link= "https://www.google.com/search?q=" + safe_string
			
			if user:
				# TODO: add to user flags for later use "yes/no" message
				user.flags

			return {"message": f"I don't know the answer ...\nShall I <a href='{link}' target='_blank'>Google</a>?",
		"render": "innerHTML"
		}

			
		return wolf
		sleep(2)

	else:
		return 'No internet connection!'

def parsed_names(ui, user:User):
	"""Replace variable nicknames with constant strings"""
	ui = re.sub(re.escape(user.ai_name), "<:ai_name>", ui, flags=re.IGNORECASE)
	ui = re.sub(re.escape(user.nickname), "<:u_name>", ui, re.IGNORECASE)
	return ui

def parsed_names_back(ui, user:User):
	"""Replace constant strings with variable nicknames"""
	ui = ui.replace("<:ai_name>", user.ai_name)
	ui = ui.replace("<:u_name>", user.nickname)
	
	return ui

def preprocess(in_dat):
	""" replace . , " ' ? ! with space """
	in_dat = in_dat.replace("'", " ")
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
	""" remove *hey Asuna* whats ....
		remove *can you* ....
		remove *will you* ....
		remove *do you know* ....
		"""
	nick = "<:ai_name>"
	# ui_parts = ui.split()
	# if len(ui_parts)<2:
	# 	# no job here
	# 	return ui

	# ui_LParts = ui.lower().split()
	

	# bkp = ui_parts.copy()
	# Lbkp = ui_LParts.copy()
	
	# if ui_LParts[0] in ("hey", "miss", "dear", "yo"):
	# 	ui_parts.pop(0)
	# 	ui_LParts.pop(0)
	# if ui_LParts[0] in ("girl", "babe", nick):
	# 	ui_parts.pop(0)

	ui = re.sub(rf'^(hey|miss|dear|yo)? ?(girl|babe|{nick})\s', '', ui, flags=re.IGNORECASE)


	# if ui_LParts[0] in ("can", "will", "do"):
	# 	ui_parts.pop(0)
	# 	ui_LParts.pop(0)
	# 	if ui_LParts[0] in ("you", "u"):
	# 		ui_parts.pop(0)
	# 		ui_LParts.pop(0)
	# 		if ui_LParts[0] in ("know", "tell", "remember", "think"):
	# 			ui_parts.pop(0)
	# 			ui_LParts.pop(0)
	# 			if ui_LParts[0] in ("of", "regarding"):
	# 				ui_parts[0] = "about"
	# 				ui_LParts[0] = "about"


	ui = re.sub(r'^please ', '', ui, flags=re.IGNORECASE)
	ui = re.sub(r'^(((can|will|do|did) ((yo)?u|y(a|o)) )?(please )?(even )?(know|tell|remember|speak|say)( me)? )(?P<msg>.+)', r'\g<msg>', ui, flags=re.IGNORECASE)
	ui = re.sub(r'^(of|regarding) ', 'about ', ui, flags=re.IGNORECASE)

	return ui
			
	
	
	

def Rchoice(*args, blank=0):
	b = ['']*blank
	return choice([*args, *b])

message_dict = {
	"message": "",
	"render": "innerText",
	"script": ""
}


def basic_output(INPUT, user: User = None, username: str = None):
	if user is None and username is not None:
		user = user_handler.get_user(username)

	_INPUT = parsed_names(INPUT, user)
	_INPUT = preprocess(_INPUT)
	_ui_raw = pre_rem_bot_call(_INPUT)
	_ui = _ui_raw.lower().replace(".", " ") # remove . from input
	# keep . in raw to make sure its not removed it mathmatical expressions
	xprint(f"/hi/{INPUT}/=/ >> /chi/{_ui_raw}/=/")
	if _ui == "":
		return
	
	user.user_client_dt = user.get_user_dt()
	# update client datetime
	
	_time = time()
	id = user.add_chat(INPUT, _time, 1, _ui_raw) # why raw?? because we want to keep the . in mathmatical expressions and CAPITALS
	msg = message_dict.copy()
	x = _basic_output(INPUT, user, _ui, _ui_raw, id)
	intent = user.chat.intent[id]

	msg["rTo"] = id # reply to id # can be used in HTML to scroll to the message

	if not x:
		log_unknown(INPUT)
		x = "I don't know what to say..."

	if isinstance(x, dict):
		message = x["message"]
		msg.update(x)
		
	else:
		message = x
		
	message = parsed_names_back(message, user)
	message = remove_style(message)
	msg["message"] = message.strip()

	if msg["render"] =="innerHTML":
		msg["message"] = msg["message"].replace("\n", "<br>")

	_time = time()
	user.add_chat(msg, _time, 0, rTo=id, intent=intent)
	return msg
	



def _basic_output(INPUT, user: User, ui:str, ui_raw:str, id:int, user_time=0):
	"""Input: user input
		user: user object
	{
		"username": username,
		"password": hash.hexdigest(),
		"created_at": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
		"last_active": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
		"last_message": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
		"pointer": 0, # current chat index (100 msg => 1 pointer)
		"nickname": username, # current user name
		"bot": None, # user preferred bot name
		"id": id, #
		"ai_name": "Asuna", # user preferred ai name
	}
	"""
	out = str2()
	
	_intent = []

	def intent(i):
		nonlocal _intent
		_intent.append(i)
		user.chat.intent[id] = _intent
		
	def rep(msg):
		nonlocal out
		
		if isinstance(msg, dict):
			if isinstance(out, dict):
				_out = out

			else:
				_out = {"message": out}
				
			_out["message"]  += "\n\n" +  msg["message"]
				
			if msg.get("render"):
				_out["render"] = msg["render"]
				
			out = _out
		else:
			out += str(msg)
		return out
		
	def rand_out(outputs):
		if isinstance(outputs, str):
			return outputs
		return choice(outputs)
		
	def check_patterns(patterns, ui, action=None):
		found = False
		uiParts = ui.split(" and ")
		remove_match = False 
		if action=="remove":
			remove_match =True
		for n, i in enumerate(uiParts):
			for ptrn, otpt, intnt in patterns:
				m = re_search(ptrn, i)
				if m:
					rep(rand_out(otpt))
					intent(intnt)
					
					if remove_match:
						uiParts[n] = re.sub(ptrn, '', i)
						
					found = True
					# tell me about yourself *and* your favourite hobby
				
		if remove_match:
			return " and ".join(uiParts)
		return found
	


	# global talk_aloud_temp, reloader, ui, ui1, ui2, case, cases, uibit1, uibit2, reloader, reloaded, BREAK_POINT, m_paused
	
	

	print("Flags: ", user.flags)

	if user.flags.parrot:
		if re_is_in(ip.stop_parrot, ui):
			user.flags.parrot = False
			rep("Parrot mode disabled")
			intent('stop_parrot')
		else:
			rep(ui)
			intent('parrot_say')
		return out
		
	if check_patterns(about_bot_patterns(), ui):
		return out

	if re_starts(ip.hi, ui):
		if not user.flags.hi_bit:
			user.flags.hi_bit = 0
		if user.flags.hi_bit<2:
			rep(Rchoice('Hello', 'Hey', 'Hey','Hello') +
				Rchoice(" there", blank=2)+
				Rchoice(f' {user.nickname}', blank=1)+ 
				Rchoice('.', '...', '!', '', '~', blank=1)+ 
				Rchoice("👋", blank=2))
		else:
			rep(Rchoice('Hello','Yeah!','Yes?','Yeah, need something?'))
		user.flags.hi_bit+=1
		if user.flags.hi_bit == 5:
			user.flags.hi_bit = 0

		intent('say_hi')

	elif re_starts(ip.hello, ui):
		if not user.flags.hello_bit:
			user.flags.hello_bit = 0
		if user.flags.hello_bit<2:
			rep( Rchoice('Hi', 'Hey') +Rchoice(" there", blank=2)+
				Rchoice(f' {user.nickname}', blank=1)+ 
				Rchoice('.', '...', '!', '', '~', blank=2)+ 
				Rchoice("👋", blank=1))
		else:
			rep(Rchoice('Yes?','Yeah?','Yeah, I can hear you','Yes, need something?'))
		user.flags.hello_bit+=1
		if user.flags.hello_bit == 5:
			user.flags.hello_bit = 0

		intent('say_hello')
		
	if check_patterns(about_bot_patterns(), ui, action="remove"):
		pass

		
	
		
	if re_check(ip.how_are_you, ui):
		rep( Rchoice("I'm fine!", "I'm doing great."))

		intent('how_are_you')
		
	if re_check(ip.whats_your_name, ui):
		rep( choice(ot.my_name_is) + user.ai_name)

		intent('whats_your_name')
		
	

	elif re_check(ip.what_to_call_you, ui):
		rep( choice(ot.call_me) + user.ai_name + choice(ot.happy_emj))

		intent('what_to_call_you')

	elif re_check(ip.what_time, ui):
		rep(choice(ot.tell_time) + user.user_client_dt.strftime("%I:%M %p."))

		intent('whats_the_time')
		
	elif re_check(ip.whats_, ui_raw):
		_what = re_search(ip.whats_, ui)
		_what_raw = re_search(ip.whats_, ui_raw)
		uiopen = remove_suffix(_what.group("query"))
		uiopen_raw = remove_suffix(_what_raw.group("query"))
		print("query:", uiopen_raw)


		if uiopen == "up":
			rep( choice(ot.on_whats_up))

			intent("(whats)_up")
		

		elif re_is_in(ip.you_self, uiopen):
			rep( choice(ot.about_self))
			
			intent('what are you')

			return {"message": out,
					"render": "innerHTML"
					}
		

		elif uiopen in it.my_name:
			rep( Rchoice("Your name is ", "You are ", "You're ") + 
				user.nickname + 
				Rchoice(" 😄", " 😇", " 😊", " ~", "...", blank=2))

			intent("(whats)_my_name")
			
		elif re_is_in(ip.my_self, uiopen):
			rep( Rchoice("Your are ", "You are ", "You're ")+ 
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

		else:
			rep(wikisearch(uiopen_raw, raw=ui, user=user))

			intent("(whats)_something")

			return out
	

	if ui in it.change_cloth:
		# TODO: NEED TO ADD IN PATTERNS
		rep(Rchoice("Sure!", "Okay", "Okay, let me change my clothes", "Hey, don't peek!", "Okk tell me how I look..."))
		case='change_cloth'
		total_skins = len(user.skins)
		user.bot_skin = (user.bot_skin + 1)%total_skins
		_skin = user_handler.use_next_skin(user.username, user.id)

		#_skin = str(user.bot_skin)

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
			Rchoice(" Thanks", blank=1)  + 
			Rchoice("🥰", "😇", blank=1))
		
		intent("are_you_ok")

	elif re_check(ip.love_you, ui):
		rep(choice(li_relove) + 
			Rchoice(" dear", f" {user.nickname}", " babe", blank=2) + 
			Rchoice(" 🥰", " 😘💕❤️", " 😘", "😘😘😘", blank=2))
		
		intent("love_you")

	elif re_check(ip.hate_you, ui):
		rep(Rchoice("I'm sorry. ", 'Sorry to dissapoint you. ',"Please forgive me. ")+
		 	Rchoice("I'm still learning",
		 		"I'll try my best to help you",
		 		"I don't know much yet, I'll try my best to learn quickly and be by your side forever ",
		 		blank=1)+
		 	Rchoice("🥺", "😞", "😭", "\n(⁠っ⁠˘̩⁠╭⁠╮⁠˘̩⁠)⁠っ","\n(⁠｡⁠ŏ⁠﹏⁠ŏ⁠)","...",
		 	blank=2)
		 	)
		
		intent("hate_you")

	
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
			#music_patch.start()


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
		if linker(link):
			rep(Rchoice('Opening ' + link, 
							"Opening " + link + " for you", 
							"Here you go",
							"There you go"
							))
		else:
			rep('No such link found')

		print(link)
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


	elif re_check (ip.whats_up, ui):
		rep( choice(ot.on_whats_up))
		
		intent("whats_up")


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
		print("query:", uiopen_raw)



		if re_is_in(ip.you_self, uiopen):
			rep(choice(ot.about_self))
			
			intent('(who) are you')

			return {"message": out,
					"render": "innerHTML"
					}
					
		elif re_is_in(ip.my_self, uiopen):
			rep( Rchoice("Your are ", "You are ", "You're ")+ 
				Rchoice("my beloved ", "my sweetheart ", "my master ", "my dear ", blank=2) + 
				user.nickname + 
				Rchoice(" 😄", " 😇", " 😊", " ~", "...", blank=2))

			intent("(who)_my_self")
			
			
		elif re_check(ip.created_program, uiopen):
			act = re_search(ip.created_program, uiopen)
			rep(choice(li_Acreator) % Rchoice(li_syn_created))
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

	elif re_check(ip.fuck_you, ui):
		rep(choice(ot.fuck_you))

		intent('fuck_you')

	elif re.search(set_timer_pattern, ui):
		x = re.match(set_timer_pattern, ui).group(1)
		rep("Timer not supported yet.")
		# set_timer(x)

		intent("set_timer")


	elif ui in escape:
		reloaded = False
		reloader = False
		BREAK_POINT =True

		intent("exit")

		return choice(li_bye)+Rchoice(f" {user.nickname}", blank=1)+ Rchoice('', '!', '.')+ Rchoice('👋😄', '')

	
	if out == '':
		log_unknown(ui)
		out = "Sorry, I don't understand..." + choice(ot.sad_emj)
		
		intent("unknown")

		uibit1 = 1
	ui1 = ui
	if ui not in li_redo:
		ui2 = ui

	return out
# tnt('/<style=a>/===hell===o')

if __name__=="__main__":
	user = user_handler.get_user("Ray")
	user = user_handler.collection(user.username, user.id)
	user_handler.get_skin_link(user.username, user.id)

	user.user_client_time_offset = TIME_sys.get_time_offset()
	while 1:
		inp = input(" >> ")
		user.user_client_time = time()

		msg = basic_output(inp, user)
		if not msg:
			continue #break
		msg = msg["message"]
		if msg == "exit": break
		print(remove_style(msg))

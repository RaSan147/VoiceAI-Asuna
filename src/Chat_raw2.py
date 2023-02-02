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
from basic_conv_re_pattern import ip, op, search, starts, check, is_in
from OS_sys import os_name, check_internet

import yt_plugin
from bbc_news import bbc_news

from TIME_sys import from_jstime

from user_handler import User, user_handler
from CONFIG import appConfig

bbc_topic = 'Asia_url'

def log_unknown(*args, **kwargs):
	with open(appConfig.log_unknown, 'a') as f:
		f.write(str(args) + "\n")

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

def tell_time():
	"""tells the current time"""
	nowits = datetime.datetime.now()
	return (choice(op.tell_time) + nowits.strftime("%I:%M %p."))



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

			return f"/y/I don't know the answer ...\nShall I <a href='{link}' target='_blank'>Google</a>?/=/"
			
			
		return wolf
		sleep(2)

	else:
		return 'No internet connection!'

def parsed_names(ui, user:User):
	"""Replace variable nicknames with constant strings"""
	ui = re.sub(re.escape(user.ai_name), "<:ai_name>", ui, flags=re.IGNORECASE)
	ui = re.sub(re.escape(user.nickname), "<:u_name>", ui, re.IGNORECASE)
	return ui

def preprocess(in_dat):
	""" replace . , " ' ? ! with space """
	in_dat = in_dat.replace("'", " ")
	in_dat = in_dat.replace("?", " ")
	in_dat = in_dat.replace("!", " ")
	in_dat = in_dat.replace(".", " ")
	in_dat = in_dat.replace(",", " ")
	in_dat = in_dat.strip()
	in_dat = re.sub(r'\s{2,}', ' ', in_dat)
	# in_dat = in_dat.replace(" us ", " me")
	# in_dat = in_dat.replace(" him", " me")
	# in_dat = in_dat.replace(" her", " me")
	# in_dat = in_dat.replace(" them", " me")

	return in_dat
	
def pre_rem_bot_call(ui):
	""" remove *hey Asuna* whats ...."""
	nick = "<:ai_name>"
	ui_parts = ui.split()
	ui_LParts = ui.lower().split()
	if len(ui_LParts)>2 and nick in ui_LParts[:2]:
		if nick == ui_LParts[0]:
			ui_parts.pop(0)
		if ui_LParts[0] in ("hey", "miss", "dear", "yo"):
			ui_parts.pop(0)
			ui_parts.pop(1)
			
	return " ".join(ui_parts)
			
	
	
	

def Rchoice(*args):
	return choice(args)

message_dict = {
	"message": "",
	"render": "innerHTML",
	"script": ""
}


def basic_output(INPUT, user: User = None, username: str = None, _time=0):
	if user is None and username is not None:
		user = User(username)

	user.add_chat(INPUT, _time, 1)
	msg = message_dict.copy()
	x = _basic_output(INPUT, user)
	if not x:
		log_unknown(INPUT)
		x = "I don't know what to say..."
	if isinstance(x, dict):
		x["message"] = remove_style(x["message"])
		msg.update(x)
	else:
		x = remove_style(x)
		msg["message"] = x

	_time = int(time()*1000)
	user.add_chat(msg["message"], _time, 0)
	return msg



def _basic_output(INPUT, user: User):
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




	# global talk_aloud_temp, reloader, ui, ui1, ui2, case, cases, uibit1, uibit2, reloader, reloaded, BREAK_POINT, m_paused
	INPUT = parsed_names(INPUT, user)
	INPUT = preprocess(INPUT)
	ui_raw = pre_rem_bot_call(INPUT)
	ui = ui_raw.lower()

	if ui == "":
		return

	out = ""

	print(user.flags)
	print(ui)

	if user.flags.parrot:
		log_type(1)
		if is_in(ip.stop_parrot, ui):
			user.flags.parrot = False
			out = "Parrot mode disabled"
		else:
			out = ui

	elif is_in(ip.hi, ui):
		log_type(2)
		if not user.flags.hi_bit:
			user.flags.hi_bit = 0
		if user.flags.hi_bit<2:
			out = Rchoice('Hello', 'Hey', 'Hey','Hello') +Rchoice('', " there", '')+Rchoice("", f' {user.nickname}')+ Rchoice('.', '...', '!', '', '~')+ Rchoice('', "👋", "")
		else:
			out = Rchoice('Hello','Yeah!','Yes?','Yeah, need something?')
		user.flags.hi_bit+=1
		if user.flags.hi_bit == 5:
			user.flags.hi_bit = 0
		case='basic1'

	elif is_in(ip.hello, ui):
		log_type(3)
		if not user.flags.hello_bit:
			user.flags.hello_bit = 0
		if user.flags.hello_bit<2:
			out = Rchoice('Hi', 'Hey') +Rchoice('', '', " there")+Rchoice("", f' {user.nickname}')+ Rchoice('.', '...', '!', '', '~')+ Rchoice('', "👋", "")
		else:
			out = Rchoice('Yes?','Yeah?','Yeah, I can hear you','Yes, need something?')
		user.flags.hello_bit+=1
		if user.flags.hello_bit == 5:
			user.flags.hello_bit = 0
		case='basic2'

	elif ui in ('change', "change cloth", "change skin", "change dress"):
		# TODO: NEED TO ADD IN PATTERNS
		log_type(4)
		out = Rchoice("Sure!", "Okay", "Okay, let me change my clothes", "Hey, don't peek!", "Okk tell me how I look...")
		case='change_cloth'
		total_skins = len(user.skins)
		user.bot_skin = (user.bot_skin + 1)%total_skins

		_skin = str(user.bot_skin)

		out = {
			"message": out,
			"script": "(async ()=> {await tools.sleep(2000); bot.get_user_pref_skin('"+_skin+"')})()"
		}


	elif ui in ('switch room', "change room", "change background"):
		# TODO: NEED TO ADD IN PATTERNS
		log_type(4)
		out = Rchoice("Sure!", "Okay", "Okay, wait a sec!")
		case='change_room_bg'

		bg = user_handler.room_bg(user=user, command="change")

		out = {
			"message": out,
			"script": f"anime.set_bg('{bg}')"
		}



	elif ui in li_r_u_fine:
		log_type(4)
		out = Rchoice("Yeah, I'm fine!", "Yeah! I'm doing great.") + Rchoice("", "🥰", "😇")
		case='yui3'
	elif is_in(ip.how_are_you, ui):
		log_type(5)
		out = Rchoice("I'm fine!", "I'm doing great.")
	elif ui in li_loveu:
		log_type(6)
		out = choice(li_relove) + Rchoice(" dear", f" {user.nickname}", " babe", "", "") + Rchoice(" 🥰", " 😘💕❤️" " 😘", "😘😘😘", "", "")
		case='yui4'
	elif ui in ('i hate u', 'i hate you'):
		log_type(7)
		out = Rchoice("I'm sorry.", 'Sorry to dissapoint you.',"Please forgive me")
		case= 'yui5'

	elif ui in li_what_ur_name:
		log_type(8)

		out = choice(["My name is ", "I am ", "Its ", "Call me ", "You can call me "]) + user.ai_name
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
	elif ui in li_QyuiName:
		log_type(9)
		outtxt = "Yes, you can."
		out = (outtxt)
		# FCyuiName()
	elif ui.startswith(li_play):
		log_type(10)
		what = [i for i in li_play if ui.startswith(i) == True]
		reg_ex = re.search(what[0] + ' *(.+)', ui)
		if len(ui) != what[0] and reg_ex:
			uiopen = reg_ex.group(1)
			try:
				yt_plugin.music.stop()
			except: pass
			yt_plugin.play_youtube(uiopen)
			played_music=True
			m_paused= False
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
	elif ui.startswith(li_can_do):
		log_type(11)
		if ui.startswith(li_goto):
			what = ''
			for i in li_goto:
				if ui.startswith(i):
					what = i
					break
			log_type(what)
			# what = [i for i in li_goto if ui.startswith(i) == True]
			reg_ex = re.search(re.escape(what) + ' (.+)', ui)
			if reg_ex:
				uiopen = reg_ex.group(1)
				# log_type(uiopen)
				if uiopen in links:
					log_type('link')
					if linker(uiopen):
						out = ('Opening ' + uiopen)
				else:
					searcher(uiopen)

	elif ui in li_AmyName:
		log_type("li_AmyName")
		out = (choice(li_AmyName) + user.nickname + '.')

	elif ui in start_parrot:
		log_type("parrot mode")
		out = ('Parrot mode activated.')
		parrot_mode = True


	elif ui in ('whats up', 'sup', 'what is up'):
		log_type("What's up")
		out = ('Just doing my things.')


	elif ui in li_tell_time1:
		log_type("li_tell_time1")
		out = tell_time()

	elif re.search('read (the )?(latest )?news', ui):
		log_type("read news")
		if check_internet():
			news = bbc_news.task(bbc_topic)
			if news is None:
				out = ('No news available')
			else:
				out = "".join(news[:5])
				# asker("Do you want to read more?", true_func=lambda: out = (*news[5:15]))
		else:
			out = ('No internet!')


	elif ui.startswith(li_whats):
		log_type("li_whats")
		# what = [i for i in li_whats if ui.startswith(i) == True]
		what = ''
		for w in li_whats:
			if ui.startswith(w):
				what = w
				break
		if len(ui) == len(what):
			return

		reg_ex = re.search(what + ' (.+)', ui)
		reg_ex_raw = re.search(what + ' (.+)', ui_raw, flags=re.IGNORECASE)


		if not reg_ex:
			return ("I don't know.")

		uiopen = reg_ex.group(1)
		uiopen_raw = reg_ex_raw.group(1)


		if uiopen in ["you", "yourself"]:
			log_type("what are you")
			out = (f'I am your virtual partner. My name is {user.ai_name} and I was made by <a href="https://github.com/RaSan147">RaSan147</a>')
			return {"message": out,
					"render": "innerHTML"
					}

		if uiopen in li_WmyName:
			log_type("what is my name")
			out = (choice(yeses) + Rchoice(li_AmyName) + user.nickname + '.')

		elif uiopen in ["latest news", "news update", 'news']:
			log_type(18)
			if check_internet():
				news = bbc_news.task(bbc_topic)
				if news is None:
					out = ("No news available")
				else:
					out = "".join(news[:5])
					# asker("Do you want to hear the rest?", true_func=read_rest_news)


			else:
				out = ('No internet!')

		else:
			log_type(20)
			out = wikisearch(uiopen_raw, raw=ui, user=user)

	elif ui.startswith(li_who):
		log_type(21)

		if ui in li_who_r_u:
			log_type(22)
			out = (choice(li_AamI) % user.ai_name)
		elif ui == "who am i":
			log_type(23)
			out = ("You are " + user.nickname + ", a human being. Far more intelligent than me.")
		else:
			who = [i for i in li_who if ui.startswith(i)]
			if len(ui) == len(who[0]):
				return

			reg_ex = re.search(who[0] + ' (.+)', ui)
			reg_ex_raw = re.search(who[0] + ' (.+)', ui_raw, flags=re.IGNORECASE)

			if not reg_ex:
				return ("I don't know.")
			uiopen = reg_ex.group(1)
			uiopen_raw = reg_ex_raw.group(1)
			if uiopen in li_r_u:
				log_type(24)
				out = (choice(li_AamI) % user.ai_name)
			elif uiopen in li_Qcreator:
				log_type(25)
				out = (choice(li_Acreator) % Rchoice(li_syn_created))
			else:
				log_type(26)
				x = wikisearch(uiopen_raw, user)
				if x:
					out = x
				else:
					out = find_person(uiopen_raw)


	elif ui in li_check_int:
		log_type(27)
		if check_internet() == False:
			out = ("No internet available.")
		else:
			out = ("Internet connection available.")

	elif ui in li_fucku:
		log_type(28)
		out = choice(li_refuck)

	elif re.search(set_timer_pattern, ui):
		log_type(29)
		x = re.match(set_timer_pattern, ui).group(1)
		out = "Timer not supported yet."
		# set_timer(x)


	elif ui in escape:
		log_type(30)
		reloaded = False
		reloader = False
		BREAK_POINT =True

		return choice(li_bye)+Rchoice('', f" {user.nickname}")+ Rchoice('', '!', '.')+ Rchoice('👋😄', '')

	if out == '':
		log_type(0)
		log_unknown(ui)
		outtxt = "Sorry, I don't understand.\n"
		out = (outtxt)
		#ui = inputer()
		#ui = i_slim(ui)
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
	while 1:
		msg = basic_output(input(" >> "), user)["message"]
		if msg == "exit": break
		print(remove_style(msg))

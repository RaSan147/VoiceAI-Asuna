__all__ = ('basic_output',)


import re
from random import choice
import webbrowser
import datetime
from time import sleep
import urllib.parse

import wikipedia

import requests

from PRINT_TEXT3 import xprint, remove_style

from basic_conv_pattern import *
from user_handler import User
from OS_sys import os_name, check_internet

import yt_plugin
from bbc_news import bbc_news
bbc_topic = 'Asia_url'


def web_go(link):
	webbrowser.open_new_tab(link)


# web_go('C:/Users/Dell/Documents/Python/Project_Alice/datapy.html')
def linker(link):
	for i in links_li:
		print(i[0])
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
	return (choice(li_tell_time2) + nowits.strftime("%I:%M %p."))



def wolfram(text):
	r = requests.get("http://api.wolframalpha.com/v1/result",
	params = {
		"i": text,
		"appid": "L32A8W-J8X5U6KG26"
	})
	if r.text == "Wolfram|Alpha did not understand your input": return False
	return r.text


def _wiki(uix):
	if uix in [i.lower() for i in wikipedia.search(uix)]:
		ny = wikipedia.page(uix)
		return {"message": wikipedia.summary(uix, sentences=2) + 'f\n<a href={ny.url}">More</a>', 
		"render": "innerHTML"
		}
		
		
	elif wikipedia.search(uix) != []:
		uix = wikipedia.search(uix)[0]
		
		out = 'Did you mean ' + uix + '? '
	else:
		
		out = "Couldn't find " + uix + "!\nWould you like to search instead?  "

	return out

def wikisearch(uix):
	if check_internet() == True:
		wolf = wolfram(uix)
		if not wolf:
			return ("/y/I don't know the answer ...\nShall I Google?/=/")
		return wolf
		sleep(2)

	else:
		return ('No internet connection!')



def i_slim(in_dat):
	in_dat = in_dat.strip()
	in_dat = re.sub(r'\s{2,}', ' ', in_dat)
	in_dat = in_dat.lower()
	in_dat = in_dat.replace("'", "")
	in_dat = in_dat.replace("?", "")
	in_dat = in_dat.replace("!", "")
	in_dat = in_dat.replace(".", "")
	in_dat = in_dat.replace(",", "")
	# in_dat = in_dat.replace(" us ", " me")
	# in_dat = in_dat.replace(" him", " me")
	# in_dat = in_dat.replace(" her", " me")
	# in_dat = in_dat.replace(" them", " me")

	return in_dat

def Rchoice(*args):
	return choice(args)


def basic_output(INPUT, user: User = None, username: str = None):
	if user is None and username is not None:
		user = User(username)
	x = _basic_output(INPUT, user)
	if isinstance(x, dict):
		x["message"] = remove_style(x["message"])
	else:
		x = remove_style(x)
	return x



def _basic_output(INPUT, user: User):
	"""Input: user input
		user: user object
	{
		"username": username,
		"password": hash.hexdigest(),
		"created_at": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
		"last_login": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
		"pointer": 0, # current chat index (100 msg => 1 pointer)
		"nickname": username, # current user name
		"bot": None, # user preferred bot name
		"id": id, #
		"ai_name": "Alice", # user preferred ai name
	}
	"""




	# global talk_aloud_temp, reloader, ui, ui1, ui2, case, cases, uibit1, uibit2, reloader, reloaded, BREAK_POINT, m_paused
	ui = i_slim(INPUT)
	if ui == "":
		return
	
	out = ""
	
	#print(user.flags)

	if user.flags.parrot:
		print(1)
		if ui in stop_parrot:
			user.flags.parrot = False
			out = "Parrot mode disabled"
		else:
			out = ui
	
	elif ui in li_hi:
		print(2)
		if not user.flags.hi_bit:
			user.flags.hi_bit = 0
		if user.flags.hi_bit<2:
			out = Rchoice('Hello','Hello '+user.nickname)
		else:
			out = Rchoice('Hello','Yeah!','Yes?','Yeah, need something?')
		user.flags.hi_bit+=1
		case='basic1'

	elif ui in li_hello:
		print(3)
		if not user.flags.hello_bit:
			user.flags.hello_bit = 0
		if user.flags.hello_bit<2:
			out = Rchoice('Hi', 'Hey','Hi there','Hey there')
		else:
			out = Rchoice('Yes?','Yeah?','Yeah, I can hear you','Yes, need something?')
		user.flags.hello_bit+=1
		case='basic2'

	elif ui in li_r_u_fine:
		print(4)
		out = Rchoice("Yeah, I'm fine!", "Yeah! I'm doing great.")
		case='yui3'
	elif ui in li_how_r_u:
		print(5)
		out = Rchoice("I'm fine!", "I'm doing great.")
	elif ui in li_loveu:
		print(6)
		out = choice(li_relove)
		case='yui4'
	elif ui in ('i hate u', 'i hate you'):
		print(7)
		out = Rchoice("I'm sorry.", 'Sorry to dissapoint you.',"Please forgive me")
		case= 'yui5'

	elif ui in li_what_ur_name:
		print(8)

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
		print(9)
		outtxt = "Yes, you can."
		out = (outtxt)
		# FCyuiName()
	elif ui.startswith(li_play):
		print(10)
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
		print(11)
		if ui.startswith(li_goto):
			what = ''
			for i in li_goto:
				if ui.startswith(i):
					what = i
					break
			print(what)
			# what = [i for i in li_goto if ui.startswith(i) == True]
			reg_ex = re.search(re.escape(what) + ' (.+)', ui)
			if reg_ex:
				uiopen = reg_ex.group(1)
				print(uiopen)
				if uiopen in links:
					print('link')
					if linker(uiopen):
						out = ('Opening ' + uiopen)
				else:
					searcher(uiopen)

	elif ui in li_AmyName:
		print(12)
		out = (choice(li_AmyName) + user.nickname + '.')


	elif ui in ('whats up', 'sup'):
		print(13)
		out = ('Just doing my things.')


	elif ui in li_tell_time1:
		print(14)
		out = tell_time()

	elif re.search('read (the )?(latest )?news', ui):
		print(15)
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
		print(16)
		# what = [i for i in li_whats if ui.startswith(i) == True]
		what = ''
		for w in li_whats:
			if ui.startswith(w):
				what = w
				break
		reg_ex = re.search(what + ' (.+)', ui)

		if len(ui) != what and reg_ex:
			uiopen = reg_ex.group(1)

			if uiopen in ["you", "yourself"]:
				out = (f'I am your virtual partner. My name is {user.ai_name} and I was made by <a href="https://github.com/RaSan147">RaSan147</a>')
				return {"message": out, 
						"render": "innerHTML"
						}
							
			if uiopen in li_WmyName:
				print(17)
				out = (choice(yeses) + Rchoice(li_AmyName) + user.nickname + '.')

			elif uiopen in ["latest news", "news update", 'news']:
				print(18)
				if check_internet():
					news = bbc_news.task(bbc_topic)
					if news is None:
						out = ("No news available")
					else:
						out = "".join(news[:5])
						# asker("Do you want to hear the rest?", true_func=read_rest_news)


				else:
					out = ('No internet!')

			elif uiopen in li_tell_time:
				print(19)
				out = tell_time()

			else:
				print(20)
				out = wikisearch(uiopen)

	elif ui.startswith(li_who):
		print(21)
		
		if ui in li_who_r_u:
			print(22)
			out = (choice(li_AamI) % user.ai_name)
		elif ui == "who am i":
			print(23)
			out = ("You are " + user.nickname + ", a human being. Far more intelligent than me.")
		else:
			who = [i for i in li_who if ui.startswith(i) == True]
			reg_ex = re.search(who[0] + ' (.+)', ui)
			if len(ui) != len(who[0]) and reg_ex:
				uiopen = reg_ex.group(1)
				if uiopen in li_r_u:
					print(24)
					out = (choice(li_AamI) % user.ai_name)
				elif uiopen in li_Qcreator:
					print(25)
					out = (choice(li_Acreator) % Rchoice(li_syn_created))
				else:
					print(26)
					x = wolfram(uiopen)
					if x:
						out = x
					else:
						out = find_person(uiopen)
						

	elif ui in li_check_int:
		print(27)
		if check_internet() == False:
			out = ("No internet available.")
		else:
			out = ("Internet connection available.")

	elif ui in li_fucku:
		print(28)
		out = choice(li_refuck)
		
	elif re.search(set_timer_pattern, ui):
		print(29)
		x = re.match(set_timer_pattern, ui).group(1)
		out = "Timer not supported yet."
		# set_timer(x)


	elif ui in escape:
		print(30)
		reloaded = False
		reloader = False
		BREAK_POINT =True
		return "exit"

	if out == '':
		print(0)
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
	user = User("Ray")
	while 1:
		msg = basic_output(input(), user)
		if msg == "exit": break
		print(remove_style(msg))

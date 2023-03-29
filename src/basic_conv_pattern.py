import re

def generate_list(prefix):
	#l = [globals()[name] for name in globals().keys() if name.startswith(prefix)]
	#return (item for sublist in l for item in sublist)

	return tuple( item for sublist in [globals()[name] for name in globals().keys() if name.startswith(prefix)] for item in sublist)

def merge(*args):
	txt = ' '.join(args)
	txt = re.sub(r'\s+', ' ', txt)
	return txt.strip()


yeses = 'Yeah! ', 'Yeah. ', 'Yes! ', 'Yes. ', 'Sure! ', 'Sure. ', 'Yeah of course. '

li_QyuiName = "can i change your name", 'i want to change your name'
li_QyuiNamePre = "can i call you ", 'may i call you'

li_redo = 'redo my last command', 'retry my last command', 'redo last command', 'redo last command', 'redo'


li_Acreator = 'I was %s by Ratul Hasan.', 'Ratul Hasan %s me.', "I was %s by Rasan147 (Ratul Hasan)"







li_where_r_u = 'you',
li_where_r_u_frm = 'you from',







li_tell_time2 = ('The time is ', "It's ")
li_goto = ('open', 'go to', 'goto')
li_play = ('play', 'lets play', 'hit', 'tune', 'sing')
li_reload = ('re', 'reload', '11')
li_fucku = ('fuck you', 'fuck u','fuck ya')
li_loveu=('love u','i love you','love ya','love you','i love u','i love you so much','i really love you','i really love you a lot','i wuv u')
li_check_int = ["check " + i for i in ('net', 'internet',"connection", "wifi", "network")]

li_refuck = ('Fuck yourself!', 'Go to hell!', 'Whatever! You can\'t do that!')
li_relove='love you too','love you so much','I love you too' 
li_voice0 = ['silent', 'silence', 'shut up', 'turn off volume', 'stop speaking']
li_can_do = li_goto + li_play
works = ["talk", "calculate"]

mc_pause = ['pause', 'pause it', 'pause the song', 'pause the music']
mc_resume = ['resume', 'resume it', 'resume the song', 'resume the music', 'continue', 'continue the song', 'continue the music']
mc_stop = ['stop', 'stop it', 'stop the song', 'stop the music']
mc_replay = ['replay', 'replay the song', 'replay the music', 'restart', 'restart the song', 'restart the music']
mc_vol_down = ['volume down', 'lower the volume', 'lower volume', 'vol down']
mc_vol_up = ['volume '+i for i in ('up', 'higher')
			 ] + [i+' the volume' for i in ('raise', 'increase', 'higher')
				  ] + [i+' volume' for i in ('raise', 'increase', 'higher')]

li_window_manage = ("forcemin",
"hide",
"maximize",
"minimize",
"restore",
"show")




"""yes = "y", "yes", "yeah", "sure", "ok", "lets go", "let's go", "start", "yep", "yeap"
yes2 = yes1 = yes
yes+=tuple('well ' + j for j in yes2)
yes+=tuple('actually ' + i for i in yes1)"""
yes= ('y', 'yes', 'yeah', 'sure', 'ok', 'lets go', "let's go", 'start', 'yep', 'yeap', 'well y', 'well yes', 'well yeah', 'well sure', 'well ok', 'well lets go', "well let's go", 'well start', 'well yep', 'well yeap', 'actually y', 'actually yes', 'actually yeah', 'actually sure', 'actually ok', 'actually lets go', "actually let's go", 'actually start', 'actually yep', 'actually yeap')


"""no = ("n", "no", "na", "nah", "nope", "stop", "quit", "exit", 'not really', 'no', 'not at all', 'never')
no2 = no1 = no
no+=tuple('well ' + j for j in no2)
no+=tuple('actually ' + i for i in no1)"""
no = ('n', 'no', 'na', 'nah', 'nope', 'stop', 'quit', 'exit', 'not really', 'no', 'not at all', 'never', 'well n', 'well no', 'well na', 'well nah', 'well nope', 'well stop', 'well quit', 'well exit', 'well not really', 'well no', 'well not at all', 'well never', 'actually n', 'actually no', 'actually na', 'actually nah', 'actually nope', 'actually stop', 'actually quit', 'actually exit', 'actually not really', 'actually no', 'actually not at all', 'actually never')

cond = yes + no

condERR = "Sorry,  I can't understand what you are saying. Just type yes or no.   "
nameGlad = "Ok. Glad to hear that you like my name."

set_timer_pattern = "set ?a? timer of (.*)"

#db = generate_list('li_')

escape = ["exit", "close", "shut down", "quit", "bye", "esc", "tata", "see ya", "see you"]
li_bye = "Bye", "See ya", "Take care", "See you later", "Good bye", "Good bye!", "Good bye..."


m_comm = generate_list('mc_')


start_parrot = "parrot", "repeat after me", "repeat what i say", "mimic", "mimic me", "parrot mode", "parrot on", "turn parrot on", "start parrot", "start mimic", "start mimicing", "start mimicing me", "start mimicing me", "reply what i say", 'reply what i send', "copy me"
stop_parrot = "stop", "stop it", "stop mimicing", "stop mimic", "stop parrot", "off", "turn off", "turn parrot off", "cancel", "cancel mimic", "cancel parrot"










links_dict = {
"url_google" : ('https://www.google.com', 'google', 'gogle', 'gooogle', 'google.com'),
"url_fb" : ('https://www.facebook.com', 'facebook', 'facebok', 'fb', 'facebook.com'),
"url_yahoo" : ['https://www.yahoo.com', 'yahoo', 'yaho', 'yahho', 'yahoo.com'],
"url_youtube" : ['https://www.youtube.com', 'youtube', 'tubemate', 'utube', 'youtub', 'youtub.com', 'youtube.com'],
"url_wiki" : ['https://www.wikipedia.com', 'wikipedia', 'wikipidia', 'wikipidea', 'wikipedea', 'wiki', 'wikipidia.com', 'wikipidea.com', 'wikipedea.com', 'wikipedia.com'],
'url_reddit' : ['https://www.reddit.com', 'reddit', 'redit', 'reddit.com', 'redit.com'],
'url_bing' : ['https://www.bing.com', 'bing', 'microsoft search', 'bing.com'],
'url_insta' : ['https://www.instagram.com', 'instagram', 'insta', 'insta.com', 'instagram.com'],
'url_apple' : ['http://apple.com/', 'apple website', 'apple.com', 'apple site', 'apple page'],
'url_microsoft' : ['http://microsoft.com/', 'microsoft website', 'microsoft.com', 'microsoft site', 'microsoft page'],
'url_pornhub' : ['https://www.pornhub.com/', 'pornhub website', 'pornhub', 'pornhub.com', 'pornhub site'],

'goog_supp' : ['http://support.google.com/', 'support', 'supports'],
'goog_docs' : ['http://docs.google.com/', 'doc', 'docs'],
}
#if 'insta' in links:print(links)
#sleep(10)
links = tuple(i for k,v in links_dict.items() for i in v)
links_li = tuple(v for k,v in links_dict.items())
# googles = generate_list('goog_')
# googles_li = gen_list('goog_')

# print(*links, sep='\n')


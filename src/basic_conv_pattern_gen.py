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
li_hello = "hello %(aiName)s", "halo %(aiName)s", 'hello', 'helo'
li_hi = "hi %(aiName)s", "hey %(aiName)s", 'hi', 'hey'

li_redo = 'redo my last command', 'retry my last command', 'redo last command', 'redo last command', 'redo'
li_QmyName = 'my name', 'my name is'

li_syn_created = 'created', 'programmed', 'invented', 'designed', 'made'
li_Qcreator = tuple(i + " you" for i in li_syn_created)

li_Acreator = 'I was %s by Ratul Hasan.', 'A boy named Ratul Hasan %s me.', 'Ratul Hasan %s me.'






li_do_u_know = 'do you know ', 'you know ', 'did you know ', ''
_li_extra = 's', ' is', ' was', ' are', ' were', 're',''

li_whats = tuple()
li_who = tuple()
li_where = tuple()
li_whats += tuple(s + 'what' + x + t for x in _li_extra for s in li_do_u_know for t in (' the', ''))
li_who += tuple(s + 'who' + x + t for x in _li_extra for s in li_do_u_know for t in (' the', ''))
li_where += tuple(s + 'where' + x + t for x in _li_extra for s in li_do_u_know for t in (' the', ''))


li_what_is = tuple('what' + x + t for x in ('s', ' is') for t in (' the', ''))


li_whats2 = tuple('what'+x for x in _li_extra)
li_what_is2 = tuple('what'+x for x in ('s', ' is'))


li_you = 'you', 'ya', 'u'
li_your = tuple(i+'r' for i in li_you)
li_r = 'are','re','re', 'r', 'r'
li_r_u = tuple(merge(a, i) for i in li_you for a in li_r)


####################################################
li_how_r_u = tuple(merge('how', i) for i in li_r_u)
li_how_r_u += tuple(merge('howr', i) for i in li_you)
li_how_r_u += tuple(merge('howre', i) for i in li_you)

li_doing = 'doing', 'doin', ''
li_today = 'today', 'now', ''
li_doing_today = tuple(merge(i, a) for i in li_doing for a in li_today)

li_how_r_u += tuple(merge('how', i, a) for i in li_r_u for a in li_doing_today)

# print(tuple(set(li_how_r_u)))
####################################################









######################################################
li_who_r_u = tuple(merge('who', i) for i in li_r_u)
li_who_r_u += tuple(merge('whor', i) for i in li_you)
li_who_r_u += tuple(merge('whore', i) for i in li_you)
# print(tuple(set(li_who_r_u)))
#####################################################



















########################################################################
li_what_ur_name0 = tuple(merge(i, y, "name") for i in li_do_u_know for y in li_your)
li_what_ur_name= tuple(merge(w, i, "name") for i in li_your for w in li_whats2)
# print(li_what_ur_name)
li_what_ur_name1= tuple(merge("tell me", i) for i in li_what_ur_name)
li_what_ur_name1+= tuple(merge("tell me", i, "name") for i in li_your)
li_what_ur_name1+= tuple(merge("tell", i, "name") for i in li_your)
li_what_ur_name1+= tuple(merge("say", i, "name") for i in li_your)
li_what_ur_name1+= tuple(merge("speak", i, "name") for i in li_your)

li_what_ur_name2= tuple(merge("can",y, i) for i in li_what_ur_name1 for y in li_you)
li_what_ur_name2+= tuple(merge("can",y,"please", i) for i in li_what_ur_name1 for y in li_you)
li_what_ur_name2+= tuple(merge("please", i) for i in li_what_ur_name1)


li_what_ur_name3= tuple(merge(i, 'please') for i in li_what_ur_name)
li_what_ur_name3+= tuple(merge(i, 'name please') for i in li_your)
li_what_ur_name3+= tuple(merge(i, 'please') for i in li_what_ur_name1)

li_what_ur_name+= li_what_ur_name0
li_what_ur_name+= li_what_ur_name1
li_what_ur_name+= li_what_ur_name2
li_what_ur_name+= li_what_ur_name3

li_what_ur_name = tuple(set(li_what_ur_name))
# print(li_what_ur_name)
#######################################################################





li_r_u_fine = tuple(merge(r, y, f) for r in li_r for y in li_you for f in ('fine', 'ok'))
li_how_old_r_u= 'old are you', 'your age'
li_where_r_u = 'you',
li_where_r_u_frm = 'you from',

li_AamI = 'I am an AI. My name is %s & I am your voice assistant.', 'My name is %s. I am an AI voice assistant.'
li_WmyName = 'my name',
li_AmyName = 'Your name is ',

# print(li_whats)




###############################################################
_li_time =('time', 'the time', 'current time')

li_time = tuple(merge(what, time) for time in _li_time for what in li_what_is)
# print(li_time)
li_time1= tuple(merge("tell me",what, i) for i in _li_time for what in li_what_is2)
li_time1+= tuple(merge("tell me", i) for i in _li_time)
li_time1+= tuple(merge("tell", i) for i in _li_time)
li_time1+= tuple(merge("say", i) for i in _li_time)
li_time1+= tuple(merge("speak", i) for i in _li_time)

li_time2= tuple(merge("can",y, i) for i in li_time1 for y in li_you)
li_time2+= tuple(merge("can",y,"please", i) for i in li_time1 for y in li_you)
li_time2+= tuple(merge("please", i) for i in li_time1)


li_time3= tuple(merge(i, 'please') for i in li_time)
li_time3+= tuple(merge(i, 'please') for i in li_time1)

li_time+= li_time1
li_time+= li_time2
li_time+= li_time3

li_time = tuple(set(li_time))
print(tuple(set(li_time)))
#############################################################










li_tell_time2 = ('The time is ', "It's ")
li_goto = ('open', 'go to', 'goto')
li_play = ('play', 'lets play', 'hit', 'tune', 'sing')
li_reload = ('re', 'reload', '11')
li_fucku = ('fuck you', 'fuck u','fuck ya')
li_loveu=('love u','i love you','love ya','love you','i love u')
li_check_int = ["check " + i for i in ('net', 'internet',"connection", "wifi", "network")]

li_refuck = ('Fuck yourself!', 'Go to hell!', 'Whatever! You can\'t do that!')
li_relove='love ya too','love you too','I love you too'
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


m_comm = generate_list('mc_')



stop_parrot = "stop", "stop it", "stop mimicing", "stop mimic", "stop parrot", "off", "turn off", "turn parrot off", "cancel", "cancel mimic", "cancel parrot"










links_dict = {
"url_google" : ('https://www.google.com', 'google', 'gogle', 'gooogle'),
"url_fb" : ('https://www.facebook.com', 'facebook', 'facebok', 'fb'),
"url_yahoo" : ['https://www.yahoo.com', 'yahoo', 'yaho'],
"url_youtube" : ['https://www.youtube.com', 'youtube', 'tubemate', 'utube'],
"url_wiki" : ['https://www.wikipedia.com', 'wikipedia', 'wikipidia', 'wikipidea', 'wikipedea'],
'url_reddit' : ['https://www.reddit.com', 'reddit', 'redit'],
'url_bing' : ['https://www.bing.com', 'bing', 'microsoft search'],
'url_insta' : ['https://www.instagram.com', 'instagram', 'insta'],
'url_apple' : ['http://apple.com/', 'apple website', 'apple.com'],
'url_microsoft' : ['http://microsoft.com/', 'microsoft website', 'microsoft.com', 'microsoft site', 'microsoft page'],
'url_pornhub' : ['https://www.pornhub.com/', 'pornhub website', 'pornhub'],

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
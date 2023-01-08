def generate_list(prefix):
	#l = [globals()[name] for name in globals().keys() if name.startswith(prefix)]
	#return (item for sublist in l for item in sublist)

	return ( item for sublist in [globals()[name] for name in globals().keys() if name.startswith(prefix)] for item in sublist)

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

li_you = 'you', 'ya', 'u'
li_r = (' are ',' re ','re ')
"""li_r_u=tuple()
for i in li_you:
	for a in li_r:
		li_r_u+=(a+i,)"""
li_r_u=(' are you', ' re you', 're you', ' are ya', ' re ya', 're ya', ' are u', ' re u', 're u', 'r u')

li_what_r_u = 'you',
li_how_r_u = tuple('how'+i for i in li_r_u)
for i in li_how_r_u:
	for a in (' today', ' doing',' doing today',' doin today','doin'):
		li_how_r_u+=(i+a,)

li_who_r_u = tuple('who'+i for i in li_r_u)

li_what_ur_name= 'what your name please', 'what your name', 'what ur name please', 'what ur name', 'whats your name please', 'whats your name', 'whats ur name please', 'whats ur name', 'what is your name', "what is ur n"
'''for w in wh:
	for r in ur:
		for p in pl:
			asd+=[w+r+' name'+p]'''
'''for p in pl:
	for u in you:
		for r in ur:
			for m in me:
				asd+=[c+u+p+'tell '+m+r+' name']'''
'''for m in me:
	for p in pl:
		for m in me:
			for r in ur:
				asd+=[p+'tell '+m+r+'name']'''
li_what_ur_name+= ('can you please tell me your name', 'can you please tell your name', 'can you please tell me ur name', 'can you please tell ur name', 'can u please tell me your name', 'can u please tell your name', 'can u please tell me ur name', 'can u please tell ur name', 'can you tell me your name', 'can you tell your name', 'can you tell me ur name', 'can you tell ur name', 'can u tell me your name', 'can u tell your name', 'can u tell me ur name', 'can u tell ur name')

li_what_ur_name+=('please tell me your name', 'please tell me ur name', 'please tell your name', 'please tell ur name', 'tell me your name', 'tell me ur name', 'tell your name', 'tell ur name', 'please tell me your name', 'please tell me ur name', 'please tell your name', 'please tell ur name', 'tell me your name', 'tell me ur name', 'tell your name', 'tell ur name')

li_how_r_u=('how are you', 'how re you', 'howre you', 'how are ya', 'how re ya', 'howre ya', 'how are u', 'how re u', 'howre u', 'how are you today', 'how are you doing', 'how are you doing today', 'how are you doin today', 'how are youdoin', 'how re you today', 'how re you doing', 'how re you doing today', 'how re you doin today', 'how re youdoin', 'howre you today', 'howre you doing', 'howre you doing today', 'howre you doin today', 'howre youdoin', 'how are ya today', 'how are ya doing', 'how are ya doing today', 'how are ya doin today', 'how are yadoin', 'how re ya today', 'how re ya doing', 'how re ya doing today', 'how re ya doin today', 'how re yadoin', 'howre ya today', 'howre ya doing', 'howre ya doing today', 'howre ya doin today', 'howre yadoin', 'how are u today', 'how are u doing', 'how are u doing today', 'how are u doin today', 'how are udoin', 'how re u today', 'how re u doing', 'how re u doing today', 'how re u doin today', 'how re udoin', 'howre u today', 'howre u doing', 'howre u doing today', 'howre u doin')
li_r_u_fine = 'are you fine', 'are you fine', 'are you ok'
li_how_old_r_u= 'old are you', 'your age'
li_where_r_u = 'you',
li_where_r_u_frm = 'you from',

li_AamI = 'I am an AI. My name is %s & I am your voice assistant.', 'My name is %s. I am an AI voice assistant.'
li_WmyName = 'my name',
li_AmyName = 'Your name is ',
li_do_u_know = 'do you know ', 'you know ', 'did you know ', ''
li_do_u_know2 = 's', ' is', ' was', ' are', ' were', 're',''
li_whats = ()
li_who = ()
li_where = ()
for x in li_do_u_know2:
	for s in li_do_u_know:
		for t in (' the', ''):
			li_whats += (s + 'what' + x + t,)
			li_who += (s + 'who' + x + t,)
			li_where += (s + 'where' + x + t,)
			
			
li_tell_time =('time', 'the time', 'current time')
li_tell_time1 = li_tell_time + ('tell time', 'tell the time')

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



m_comm = generate_list('mc_')

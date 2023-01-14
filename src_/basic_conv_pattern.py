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
# li_how_r_u = tuple(merge('how', i) for i in li_r_u)
# li_how_r_u += tuple(merge('howr', i) for i in li_you)
# li_how_r_u += tuple(merge('howre', i) for i in li_you)
# 
# li_doing = 'doing', 'doin', ''
# li_today = 'today', 'now', ''
# li_doing_today = tuple(merge(i, a) for i in li_doing for a in li_today)
# 
# li_how_r_u += tuple(merge('how', i, a) for i in li_r_u for a in li_doing_today)
# 
# print(tuple(set(li_how_r_u)))
####################################################

li_how_r_u = ('how re you', 'how are ya today', 'how re u', 'how are ya doing today', 'how are ya doin', 'how are you doing today', 'how are u today', 'how are u doin', 'how r you doin now', 'how re you doin', 'how are u doing', 'how are u doin today', 'how are you doin now', 'how r u now', 'how re u doing now', 'how r u doin now', 'how re you doin today', 'how r you doing now', 'how re u doin', 'how re you doin now', 'how r ya', 'how r ya now', 'howre you', 'how re you doing', 'how re you now', 'how r u doin', 'how r ya doin now', 'how are you doing now', 'how r you', 'how r ya doin today', 'how are ya', 'how are ya doin today', 'how r u doing today', 'how are you doin', 'how are u now', 'how r you doin', 'how are you today', 'how re u doing today', 'how re ya now', 'how are u doing today', 'how r you now', 'how r you today', 'how re you today', 'how are u', 'how r u today', 'how re you doing today', 'howre ya', 'how r u doin today', 'how re ya doin now', 'how are you now', 'how re u doing', 'how re u doin today', 'how are you', 'how are you doing', 'howre u', 'how re ya today', 'how re ya doing today', 'howr ya', 'how r u doing', 'how re you doing now', 'how are ya doin now', 'how r you doin today', 'howr you', 'how r you doing', 'howr u', 'how re u now', 'how are u doin now', 'how re ya doin today', 'how r ya doing', 'how r u', 'how are ya now', 'how r ya today', 'how r ya doing now', 'how are u doing now', 'how re u doin now', 'how re ya doin', 'how re ya', 'how r u doing now', 'how re ya doing now', 'how are ya doing', 'how are you doin today', 'how re ya doing', 'how r ya doin', 'how are ya doing now', 'how r you doing today', 'how r ya doing today', 'how re u today')









######################################################
# li_who_r_u = tuple(merge('who', i) for i in li_r_u)
# li_who_r_u += tuple(merge('whor', i) for i in li_you)
# li_who_r_u += tuple(merge('whore', i) for i in li_you)
# print(tuple(set(li_who_r_u)))
#####################################################
li_who_r_u = ('who re ya', 'whore you', 'who r you', 'whore ya', 'who r u', 'who are u', 'whor ya', 'who re you', 'whor you', 'who r ya', 'who re u', 'whore u', 'who are you', 'whor u', 'who are ya')



















########################################################################
# li_what_ur_name0 = tuple(merge(i, y, "name") for i in li_do_u_know for y in li_your)
# li_what_ur_name= tuple(merge(w, i, "name") for i in li_your for w in li_whats2)
# # print(li_what_ur_name)
# li_what_ur_name1= tuple(merge("tell me", i) for i in li_what_ur_name)
# li_what_ur_name1+= tuple(merge("tell me", i, "name") for i in li_your)
# li_what_ur_name1+= tuple(merge("tell", i, "name") for i in li_your)
# li_what_ur_name1+= tuple(merge("say", i, "name") for i in li_your)
# li_what_ur_name1+= tuple(merge("speak", i, "name") for i in li_your)

# li_what_ur_name2= tuple(merge("can",y, i) for i in li_what_ur_name1 for y in li_you)
# li_what_ur_name2+= tuple(merge("can",y,"please", i) for i in li_what_ur_name1 for y in li_you)
# li_what_ur_name2+= tuple(merge("please", i) for i in li_what_ur_name1)


# li_what_ur_name3= tuple(merge(i, 'please') for i in li_what_ur_name)
# li_what_ur_name3+= tuple(merge(i, 'name please') for i in li_your)
# li_what_ur_name3+= tuple(merge(i, 'please') for i in li_what_ur_name1)

# li_what_ur_name+= li_what_ur_name0
# li_what_ur_name+= li_what_ur_name1
# li_what_ur_name+= li_what_ur_name2
# li_what_ur_name+= li_what_ur_name3

# li_what_ur_name = tuple(set(li_what_ur_name))
# print(li_what_ur_name)
#######################################################################


li_what_ur_name = ('tell me what were ur name', 'can you tell me what ur name', 'tell me what is your name', 'can u please say your name', 'can u tell me what yar name', 'can u tell me what your name', 'what are ur name', 'can u please tell me whats your name', 'please speak your name', 'please tell me yar name', 'yar name', 'can u speak your name', 'can ya please tell me what are ur name', 'tell me what was ur name', 'what ur name please', 'please tell me ur name', 'tell me what was yar name', 'can u tell me what are ur name', 'can u say ur name', 'what was ur name please', 'can you please tell me what is ur name', 'please tell me what your name', 'can ya tell me what were yar name', 'please speak yar name', 'what is ur name please', 'say ur name please', 'can ya tell me what are your name', 'can u please tell me what were your name', 'can ya please tell me whatre ur name', 'can you please tell me whatre yar name', 'tell me what are your name', 'can ya tell me what yar name', 'did you know your name', 'can you please tell me what are ur name', 'can u please tell me what yar name', 'can you tell me whats yar name', 'can ya please speak your name', 'tell me what yar name', 'tell ur name please', 'can ya please tell ur name', 'can you tell me whatre your name', 'please tell me whats your name', 'can u please tell me what was your name', 'tell me what was ur name please', 'tell me what ur name please', 'what are your name', 'tell ur name', 'can you tell me what was ur name', 'please tell me what are your name', 'tell me what is ur name', 'can ya tell me whats yar name', 'can ya tell ur name', 'can ya please tell me what were your name', 'can ya please say your name', 'what is your name please', 'can ya please tell me what ur name', 'tell me your name please', 'do you know ur name', 'can u please tell your name', 'can u please say ur name', 'can you tell me what is your name', 'can ya tell me what is your name', 'tell me yar name please', 'can ya please tell me yar name', 'tell me your name', 'please tell me whatre ur name', 'can ya please tell me what is ur name', 'please tell me what yar name', 'tell me what were yar name', 'can ya speak your name', 'please say ur name', 'what ur name', 'what were yar name please', 'can u tell me what was ur name', 'tell me what were yar name please', 'can you please tell me what are your name', 'can you speak yar name', 'can ya speak yar name', 'can you please tell me what was your name', 'can ya tell me what were ur name', 'please tell your name', 'can ya tell me whatre your name', 'can ya please tell me what is your name', 'tell me what is yar name please', 'what yar name please', 'what was your name', 'tell me whats your name please', 'can u please speak ur name', 'can ya please tell me what was ur name', 'please tell me what is your name', 'can u tell me what were ur name', 'can u tell me whatre ur name', 'what were ur name please', 'did you know ur name', 'whatre ur name please', 'can u please tell me yar name', 'can u please tell me what were ur name', 'speak yar name please', 'can u please tell yar name', 'can ya please tell me whatre yar name', 'can you please tell me yar name', 'what your name please', 'can u tell me what are yar name', 'tell me what are ur name please', 'can you please tell me what is yar name', 'can u please tell me ur name', 'please tell me what are yar name', 'whats yar name please', 'tell me what was yar name please', 'can you tell me yar name', 'can u tell me what was yar name', 'can you tell me whats your name', 'can u say your name', 'please tell me whatre your name', 'tell me what ur name', 'can ya please tell me what your name', 'can you tell me your name', 'can ya tell me what ur name', 'can you tell me whats ur name', 'can you please tell me whats your name', 'please tell me what is yar name', 'can u tell me whats your name', 'can you please tell ur name', 'please tell me what was yar name', 'tell me whats ur name', 'can u tell me whats ur name', 'please tell me what was ur name', 'please tell ur name', 'tell me ur name please', 'can ya tell me what your name', 'what is ur name', 'can ya please tell me whats yar name', 'can u tell me what were your name', 'what are ur name please', 'tell me whatre ur name please', 'can you tell your name', 'tell me whats yar name', 'tell me what is yar name', 'can ya please tell me what are yar name', 'can you please speak your name', 'please tell me what was your name', 'ur name', 'speak ur name please', 'please tell me whats ur name', 'can ya please tell yar name', 'can ya tell me whats your name', 'whats ur name', 'can you please tell me whats yar name', 'what is yar name please', 'can u please tell me what were yar name', 'can you please tell me what were yar name', 'can ya please tell me whats your name', 'can you tell me what yar name', 'can u tell me whatre yar name', 'can you speak ur name', 'tell me whats your name', 'what was ur name', 'tell me ur name', 'can you tell me what is ur name', 'can ya please tell me whats ur name', 'what is yar name', 'whats ur name please', 'tell me whatre your name', 'please tell me what are ur name', 'can u please tell me what ur name', 'can you please tell yar name', 'please tell me what were ur name', 'whatre your name please', 'can u tell me ur name', 'can ya please tell me what were ur name', 'what were yar name', 'can u please tell me whatre ur name', 'can you tell me what were your name', 'tell me whats ur name please', 'can you say ur name', 'can you please say yar name', 'say your name please', 'can you tell me what were yar name', 'can ya tell me what are ur name', 'can you please speak yar name', 'can you please tell me what ur name', 'tell me whatre yar name please', 'can you please tell me your name', 'can u please tell me whats yar name', 'can you say yar name', 'can ya please speak ur name', 'can you please tell me whatre ur name', 'say yar name please', 'tell me what were your name please', 'tell me what are ur name', 'can u please tell me whats ur name', 'tell me what were ur name please', 'please tell me what were your name', 'can you tell me what your name', 'can u please speak your name', 'can you say your name', 'tell your name please', 'can ya please say ur name', 'can ya please tell me ur name', 'can you please tell your name', 'can ya tell me ur name', 'can u tell me what ur name', 'you know your name', 'can you speak your name', 'can ya please tell me what yar name', 'do you know yar name', 'your name', 'can ya say yar name', 'tell me what is ur name please', 'please tell me what is ur name', 'please tell me what ur name', 'tell me what yar name please', 'can ya tell yar name', 'what were ur name', 'can ya tell your name', 'can ya tell me whatre ur name', 'can ya please tell me what are your name', 'can ya please tell me what were yar name', 'can ya say ur name', 'can you please tell me what was ur name', 'can ya tell me what are yar name', 'can you tell me what is yar name', 'can you please say your name', 'ur name please', 'say yar name', 'say ur name', 'can ya tell me whats ur name', 'can ya please say yar name', 'can you tell me what was yar name', 'can you tell me what was your name', 'tell me yar name', 'tell me what are yar name', 'can you please tell me what were your name', 'what was yar name please', 'yar name please', 'can you please tell me ur name', 'please say your name', 'please say yar name', 'can u please tell me whatre yar name', 'can ya tell me whatre yar name', 'can u speak ur name', 'speak your name please', 'can u please tell me what are yar name', 'can ya please tell me what was your name', 'tell me what your name', 'can ya speak ur name', 'can u tell me what is yar name', 'do you know your name', 'can ya please tell me whatre your name', 'did you know yar name', 'say your name', 'tell me whatre your name please', 'can ya tell me what were your name', 'can ya tell me what was ur name', 'can ya tell me what is ur name', 'can u tell me what are your name', 'can ya tell me what was yar name', 'tell me what your name please', 'tell me whats yar name please', 'whats your name please', 'can you please say ur name', 'can u tell me what was your name', 'can u please tell me whatre your name', 'speak ur name', 'can ya please tell me your name', 'whatre ur name', 'can u please speak yar name', 'can u please say yar name', 'can u tell me your name', 'tell me what are your name please', 'can you tell yar name', 'what was yar name', 'can u please tell me what are ur name', 'can you please tell me what yar name', 'can ya please speak yar name', 'tell me what is your name please', 'can ya please tell me what is yar name', 'tell yar name', 'can ya tell me your name', 'can you please tell me whats ur name', 'what are yar name', 'tell me what are yar name please', 'can u please tell me what was ur name', 'can u please tell me what is yar name', 'can you tell me what were ur name', 'can you please speak ur name', 'can u tell ur name', 'can ya tell me what was your name', 'what your name', 'tell me what were your name', 'can you tell me whatre yar name', 'what are yar name please', 'can ya please tell me what was yar name', 'can you please tell me whatre your name', 'tell your name', 'whatre yar name please', 'can u please tell me your name', 'can u tell your name', 'tell me whatre ur name', 'can u tell yar name', 'can u please tell ur name', 'can u tell me what were yar name', 'tell me what was your name please', 'tell me whatre yar name', 'can you please tell me what your name', 'whatre your name', 'please speak ur name', 'can u please tell me what your name', 'what are your name please', 'can ya please tell your name', 'please tell me whats yar name', 'whatre yar name', 'what were your name please', 'tell yar name please', 'can u tell me whatre your name', 'you know ur name', 'can you please tell me what are yar name', 'speak your name', 'your name please', 'please tell me what were yar name', 'can u tell me what is your name', 'you know yar name', 'what was your name please', 'can u please tell me what is ur name', 'please tell yar name', 'can you tell me ur name', 'can u please tell me what are your name', 'can u speak yar name', 'please tell me your name', 'can you tell me what are your name', 'can you tell ur name', 'can ya tell me what is yar name', 'can u tell me what is ur name', 'can you tell me what are yar name', 'can u please tell me what is your name', 'please tell me whatre yar name', 'can you please tell me what is your name', 'whats yar name', 'what is your name', 'can you please tell me what was yar name', 'can u say yar name', 'whats your name', 'can u tell me yar name', 'can you please tell me what were ur name', 'can ya tell me yar name', 'what yar name', 'speak yar name', 'can you tell me what are ur name', 'tell me what was your name', 'can you tell me whatre ur name', 'can ya say your name', 'what were your name', 'can u tell me whats yar name', 'can u please tell me what was yar name')




li_r_u_fine = tuple(merge(r, y, f) for r in li_r for y in li_you for f in ('fine', 'ok'))
li_how_old_r_u= 'old are you', 'your age'
li_where_r_u = 'you',
li_where_r_u_frm = 'you from',

li_AamI = 'I am an AI. My name is %s & I am your voice assistant.', 'My name is %s. I am an AI voice assistant.'
li_WmyName = 'my name',
li_AmyName = 'Your name is ',
			
# print(li_whats)




###############################################################
# _li_time =('time', 'the time', 'current time')

# li_time = tuple(merge(what, time) for time in _li_time for what in li_what_is)
# # print(li_time)
# li_time1= tuple(merge("tell me",what, i) for i in _li_time for what in li_what_is2)
# li_time1+= tuple(merge("tell me", i) for i in _li_time)
# li_time1+= tuple(merge("tell", i) for i in _li_time)
# li_time1+= tuple(merge("say", i) for i in _li_time)
# li_time1+= tuple(merge("speak", i) for i in _li_time)

# li_time2= tuple(merge("can",y, i) for i in li_time1 for y in li_you)
# li_time2+= tuple(merge("can",y,"please", i) for i in li_time1 for y in li_you)
# li_time2+= tuple(merge("please", i) for i in li_time1)


# li_time3= tuple(merge(i, 'please') for i in li_time)
# li_time3+= tuple(merge(i, 'please') for i in li_time1)

# li_time+= li_time1
# li_time+= li_time2
# li_time+= li_time3

# li_time = tuple(set(li_time))
# print(tuple(set(li_time)))
#############################################################

li_tell_time1 = ('tell me whats the time', 'speak the time', 'can u please tell me what is current time', 'can ya tell me what is current time', 'please tell me current time', 'please tell me what is time', 'can you please tell me what is current time', 'whats current time', 'can ya please tell me whats time', 'can u please say current time', 'can ya please say the time', 'please tell me whats current time', 'can u please tell current time', 'tell time', 'can you please tell me time', 'say current time', 'tell me what is time please', 'what is the time please', 'tell me what is the time please', 'can ya please tell me time', 'speak current time', 'can you please speak time', 'can ya speak the time', 'can you please speak the time', 'tell me what is current time', 'can you please say time', 'please speak current time', 'can u say current time', 'tell me time please', 'please say the time', 'can you please tell me the time', 'please tell me what is current time', 'can u please tell me what is the time', 'can u please speak current time', 'can u tell me what is time', 'can ya please speak current time', 'what is current time', 'can u tell me whats time', 'can ya please tell me the time', 'whats time please', 'can you please tell me current time', 'whats time', 'can ya please speak time', 'can ya please tell me current time', 'can you tell me whats the time', 'please tell me whats time', 'can you tell current time', 'can you tell me what is time', 'please speak the time', 'tell me the time', 'can ya please tell me what is time', 'can u please tell me what is time', 'can you speak current time', 'tell me what is the time', 'what is the current time', 'what is the time', 'whats the current time please', 'what is the the time please', 'can you speak time', 'tell me the time please', 'can you tell me the time', 'can you say time', 'can you tell me current time', 'can u tell me what is the time', 'can u tell the time', 'please speak time', 'whats the the time', 'please tell me the time', 'tell me whats time', 'whats current time please', 'tell me what is time', 'can u tell time', 'say the time please', 'can you please tell me what is time', 'can u please tell the time', 'can you tell me whats current time', 'please tell the time', 'can u tell current time', 'tell me whats time please', 'can you please say current time', 'can u please tell me the time', 'can you tell me time', 'can you please tell time', 'please tell time', 'can ya tell the time', 'can you please tell the time', 'please tell me whats the time', 'can ya tell me what is time', 'say time please', 'can u tell me what is current time', 'can you please tell current time', 'can you please tell me whats time', 'can you tell me what is current time', 'can you speak the time', 'can ya say current time', 'tell me what is current time please', 'can ya tell me whats the time', 'can ya tell time', 'can u please tell time', 'tell the time please', 'can ya please tell me whats the time', 'can u tell me whats current time', 'can ya tell me what is the time', 'can u tell me time', 'whats the current time', 'can ya please say current time', 'tell me whats the time please', 'can you tell time', 'can u tell me whats the time', 'please say time', 'speak time please', 'can ya tell me whats current time', 'say the time', 'tell current time', 'can u speak the time', 'whats the time', 'can u please speak the time', 'can you please speak current time', 'can ya please tell the time', 'what is time', 'what is current time please', 'can u speak time', 'can ya tell current time', 'can u tell me the time', 'can you please tell me whats current time', 'can you tell me what is the time', 'can u tell me current time', 'can u please tell me whats the time', 'can you please tell me what is the time', 'can u please say the time', 'can ya please tell current time', 'can ya please tell me what is current time', 'can ya please speak the time', 'tell me whats current time please', 'can ya say time', 'tell me current time please', 'can u please tell me time', 'can ya tell me current time', 'can u please speak time', 'can u please tell me whats current time', 'what is the current time please', 'can u say the time', 'say time', 'can ya please tell me whats current time', 'can u please say time', 'whats the time please', 'whats the the time please', 'what is time please', 'speak time', 'can you tell me whats time', 'can u please tell me whats time', 'please tell current time', 'please tell me what is the time', 'tell the time', 'tell time please', 'can u speak current time', 'tell me whats current time', 'can ya say the time', 'tell me time', 'please tell me time', 'tell current time please', 'what is the the time', 'can you say current time', 'can ya tell me whats time', 'can ya please tell time', 'can ya tell me the time', 'can you tell the time', 'can u say time', 'tell me current time', 'can ya tell me time', 'can you say the time', 'can you please say the time', 'say current time please', 'speak the time please', 'can ya speak time', 'can ya please tell me what is the time', 'please say current time', 'can you please tell me whats the time', 'can ya speak current time', 'can ya please say time', 'speak current time please', 'can u please tell me current time')








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
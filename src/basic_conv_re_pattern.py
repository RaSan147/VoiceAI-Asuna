import json
import re
from re import compile


from REGEX_TOOLS import re_starts, re_check, re_is_in, re_search, eos
from DS import GETdict


def generate_list(prefix):
    # l = [globals()[name] for name in globals().keys() if name.startswith(prefix)]
    # return (item for sublist in l for item in sublist)

    return tuple(item for sublist in [globals()[name] for name in globals().keys() if name.startswith(prefix)] for item in sublist)


def merge(*args):
    txt = ' '.join(args)
    txt = re.sub(r'\s+', ' ', txt)
    return txt.strip()


def check_context(context=[], contextsss=[]):
    for i in context:
        if i in contextsss:
            return True


def C(pattern):
    """ return re.compile of the pattern with ignore case flag
    also add to to_bot_suffix so that it can capture calling by bot name or other nouns
    """

    return compile(rf"{pattern}", flags=re.IGNORECASE)


to_bot_suffix = C(
    r"(( please| plz)? (<:ai_name>|girl|dear|babe|honey|sweet ?heart|darling|ma.?am))$"
)


def remove_suffix(string):
    return to_bot_suffix.sub("", string)


"""yes = "y", "yes", "yeah", "sure", "ok", "lets go", "let's go", "start", "yep", "yeap"
yes2 = yes1 = yes
yes+=tuple('well ' + j for j in yes2)
yes+=tuple('actually ' + i for i in yes1)"""
yes = (
    'y', 'yes', 'yeah', 'sure', 'ok', 'lets go', "let's go",
    'start', 'yep', 'yeap', 'well y', 'well yes', 'well yeah',
    'well sure', 'well ok', 'well lets go', "well let's go",
    'well start', 'well yep', 'well yeap', 'actually y',
    'actually yes', 'actually yeah', 'actually sure',
    'actually ok', 'actually lets go', "actually let's go",
    'actually start', 'actually yep', 'actually yeap'
)


"""no = ("n", "no", "na", "nah", "nope", "stop", "quit", "exit", 'not really', 'no', 'not at all', 'never')
no2 = no1 = no
no+=tuple('well ' + j for j in no2)
no+=tuple('actually ' + i for i in no1)"""


output_TEXTS = GETdict()
ot = output_TEXTS

ot.yes = ("Yeah!", "Sure...", "Sure!!" "Okkay~", "Okie~", "Okay!")
ot.no = ("No", "Sorry but nope")
ot.tell_time = ('The time is ', "It's ")

ot.happy_emj = ("(◕‿◕)💞", "😄",
                "😇", "😊", "~", "...", "", "")
ot.sad_emj = ("😿", "😢", "😭",
              "😞", "😔", "~", "...", "", "")

ot.my_name_is = ["My name is ", "I am ",
                 "Its ", "Call me ", "You can call me "]
ot.call_me = ["You can call me ", "Call me ", "Its "]
ot.about_self = ('I am your virtual partner. My name is <:ai_name> and I was made by <a href="https://github.com/RaSan147">RaSan147</a>',
                 'I am an AI. My name is <:ai_name> & I am your voice assistant.', 'My name is <:ai_name>. I am an AI voice assistant.')

ot.on_whats_up = (
    "Just the usual.",
    "Nothing much.",
    "Nothing much, just chilling.",
    "Nothing much, just hanging around.",
    "All good here!",
    "I’m doing well.",
    "Nothing much, just doing my thing.",
)


ot.no_internet = (
	"Sorry, server is offline right now.",
	"Its kinda embarrassing to say, the server is facing internet outage."
	"Something is wrong with out network. We're working on it."
)

input_PATTERNS = GETdict({})
ip = input_PATTERNS

input_text = GETdict()
it = input_text

ip.logout = [
    C(r"(log|sign)o? ?(out|off)"),
]


ip.yeses = [
    C(r'(well )?(actually )?y(e|a)(ah|s|p)( of ?course)?( sure)?'),
    # well actually yes/yep/yeah of~course
    'sure',
    'of( |-)?course',
    C(r"ok+(ay|h|eh)?"),  # okkay/okeh
    "go (on|ahead)",
    C("^y$")
]

# print(ip["yeses"][3].match("okkeh"))

no = ('n', 'no', 'na', 'nah', 'nope', 'stop', 'quit', 'exit', 'not really', 'no', 'not at all', 'never', 'well n', 'well no', 'well na', 'well nah', 'well nope', 'well stop', 'well quit', 'well exit', 'well not really', 'well no',
      'well not at all', 'well never', 'actually n', 'actually no', 'actually na', 'actually nah', 'actually nope', 'actually stop', 'actually quit', 'actually exit', 'actually not really', 'actually no', 'actually not at all', 'actually never')

cond = yes + no
ip.no = [
    # well actually no/nope/not/nah // not at all! never!!!
    C(r"(well )?(actually )?n(o(pe)?t?|ah?)( at all)?( never)?"),
    "(please |plz )?stop",
    "never",
]


# print(ip["no"][0].match("well nope"))
# print(is_in(ip["no"], "well nope"))

li_QyuiName = "can i change your name", 'i want to change your name'
li_QyuiNamePre = "can i call you ", 'may i call you'
# li_hello = "hello <:ai_name>", "helo <:ai_name>", 'hello', 'helo'
# li_hi = "hi <:ai_name>", "hey <:ai_name>", 'hi', 'hey', "hiii"

li_redo = 'redo my last command', 'retry my last command', 'redo last command', 'redo last command', 'redo'

ip.created_program = [
    C(r'(?P<action>created?|program(med)?|invent(ed)?|design(ed)?|ma(d|k)e) ((yo)?u|y(a|o))'),
    C(r"((yo)?u|y(a|o))(( |')?r)? (?P<action>creat|programm?|invent|design|mak)(o|e)?r")
]

ip.r_u_ok = [
    C(r"a?re? ((yo)?u|y(a|o)) (fine|ok((a|e)y)?|well|alright)"),
]

ip.thanks = [
    C(r"thank(s( a (lot|bunch))?| ((yo)?u|y(a|o))( (so+|very) much))?"),
]

ip.r_u = [
    C(r"a?re? ((yo)?u|y(a|o))"),
]
ip.who_are_you = [
    C(r"who ?a?re? ((yo)?u|y(a|o))"),  # who are u
]


ip.whats_ = [
    # C(r"((can ((yo)?u|y(a|o)) )?(please )?((tell|speak|say)( me)? )|((do|did) )?((yo)?u|y(a|o)) know )?(what ?(s|re|is|are|was|were)? )(the )?(?P<query>.*)"),
    C(r"w(h|g)at('| )?(s|re|is|are|r|was|were|am|will|will be)? (the )?(?P<query>.*)"),
]

ip.whos_ = [
    # C(r"((can ((yo)?u|y(a|o)) )?(please )?((tell|speak|say)( me)? )|((do|did) )?((yo)?u|y(a|o)) know )?(what ?(s|re|is|are|was|were)? )(the )?(?P<query>.*)"),
    C(r"who('| )?(s|re|is|are|r|was|were|am|will|will be)? (the )?(?P<query>.*)"),
]

ip.whens_ = [
    C(r"when('| )?(s|re|is|are|r|was|were|am|will|will be)? (the )?(?P<query>.*)"),
]

ip.whats_your_name = [
    # C(r"((can ((yo)?u|y(a|o)) )?(please )?((tell|speak|say)( me)? )|((do|did) )?((yo)?u|y(a|o)) know )?(what(s|re| (is|are|was|were))? )?((yo)?u|y(a|o))(r|re)? name"),
    C(r"(what('| )?(s|re|is|are|r|was|were|am|will|will be)? )?((yo)?u|y(a|o))(r|re)? name"),
    # C(r"((((can|will) ((yo)?u|y(a|o)) )?(please )?)?(tell|speak|say) (me )?)?what should i call ((yo)?u|y(a|o))( by)?")

]

ip.what_to_call_you = [
    C(r"what should i call ((yo)?u|y(a|o))( by)?"),
]

ip.what_time = [
    # C(r"((can ((yo)?u|y(a|o)) )?(please )?((tell|speak|say)( me)? )|((do|did) )?((yo)?u|y(a|o))( even)? know )?(what(s|re| (is|are|was|were))? )?(the )?(current )?time( is| it)*( now)?( please)?"),
    C(r"(what('| )?(s|re|is|are|r|was|were|am|will|will be)? )?(the )?(current )?time((?!s)| |$)(is|it)* ?(now)? ?(please|plz)?"),
    'clock',
]

li_how_old_r_u = 'old are you', 'your age'
li_where_r_u = 'you',
li_where_r_u_frm = 'you from',

li_WmyName = 'my name',


"whats my name"
it.my_name = ['my name', 'my nickname']


"what/who am i to you?"
ip.my_self = [
    "me( to ((yo)?u|y(a|o)))?",
    C(r"my ?self( to ((yo)?u|y(a|o)))?"),
    C(r"i( to ((yo)?u|y(a|o)))?")
]


"what are you?"
ip.you_self = [
    C(r"((yo)?u|y(a|o))('| )?(re?)?( ?self)?( really)?"),
]

ip.your_bday = [
	C(r"((yo)?u|y(a|o))('| )?(re?)? (birthday|bday)")
]


"whats the latest news" "tell me the latest news"
ip.latest_news = [
    C(r'(latest|any|global|world)? ?(news|special|) ?(news|headlines?|events?|updates?)'),
]

ip.tell_latest_news = ip.latest_news + [
    "anything interesting happening",
    C(r"(do ((yo)?u|y(a|o)))? ?(got|have) (some|any)(thing)? (news|headlines?|interesting)(today)?")
]


'((tell|speak|read )(out)?)?(the )?(latest )?news'

"change Anime dress"
ip.change_cloth = [
	'change', 
	C(r"change (((yo)?u|y(a|o))('| )?(re?)? )?(dress|cloth|skin|costume|wear)(e?s)?"),
	C(r"wear (a )?(((yo)?u|y(a|o))('| )?(re?)? )?(new )?(dress|cloth|skin|costume|wear)(e?s)?"), 
]

"change Anime room"
ip.change_room = [
	C(r"(change|switch|move) (to )?(a )?(((yo)?u|y(a|o))('| )?(re?)? )?(new )?(room|place|location|background|bg)"), 
]


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


ip.goto = [
    C(r"(open|go ?to)( the)? (?P<query>.*?)( website| site| page)?$")
]

ip.search = [
    C(r"(search|find|chack) (the )?(?P<query>.*?)")
]


li_tell_time2 = ('The time is ', "It's ")
li_goto = ('open', 'go to', 'goto')
li_play = ('play', 'lets play', 'hit', 'tune', 'sing')
li_reload = ('re', 'reload', '11')
li_fucku = ('fuck you', 'fuck u', 'fuck ya')

ip.fuck_you = [
    C(r"(i('| | wi)ll )?(fuckh?|rape|torture|kill) ((yo)?u|y(a|o))(('| )?(re?)? ((mo(m|ther|mmy))|sis(ter)?))?"),
]
# this is terrible, i wish no one use this ever
ot.fuck_you = (
    "I don't like you.", 'How rude!', "You're mean!", "You're rude",
    "Please refrain from using such terms", "You're horrible", "I don't want to talk to you", "You're disgusting")


ip.love_you = [
    C(r'(i )?(really )?(love|wuv) ((yo)?u|y(a|o))( so much| a lot)?'),
]

ip.hate_you = [
    C(r"(i )?(really )?(hate|don('| )t like) ((yo)?u|y(a|o))"),
]

ip.whats_up = [
    C(r"wh?(u|a)t?( |')?s+ up+"),
    C(r'^sup' + eos),
]


li_check_int = [
    "check " + i for i in ('net', 'internet', "connection", "wifi", "network")
]


li_relove = 'love you too', 'love you so much', 'I love you too'
li_voice0 = ['silent', 'silence', 'shut up',
             'turn off volume', 'stop speaking']
li_can_do = li_goto + li_play
works = ["talk", "calculate"]

mc_pause = ['pause', 'pause it', 'pause the song', 'pause the music']
mc_resume = ['resume', 'resume it', 'resume the song', 'resume the music',
             'continue', 'continue the song', 'continue the music']
mc_stop = ['stop', 'stop it', 'stop the song', 'stop the music']
mc_replay = ['replay', 'replay the song', 'replay the music',
             'restart', 'restart the song', 'restart the music']
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


condERR = "Sorry,  I can't understand what you are saying. Just type yes or no.   "
nameGlad = "Ok. Glad to hear that you like my name."

set_timer_pattern = "set ?a? timer of (.*)"

# db = generate_list('li_')

ip.bye = [
    "exit", "close", 
    C(r"(shut|turn) ?(down|off)"), 
    "quit",
    C(r"(good )?(bye+ ?)+"), 
    C(r"esc(ape)?"), 
    C(r"ta( |-)?ta"), 
    C(r"see ((yo)?u|y(a|o))"),
]
#li_bye = "Bye", "See ya", "Take care", "See you later", "Good bye", "Good bye!", "Good bye..."

ip.take_care = [
	C(r"take( |-)?care"),
	C(r"sweet( |-)?dreams?"),
	"have a nice day",
]

ip.help = [
	C(r"[/\\]?(show(-| )?)?(help|commands?|menu)"),
]


m_comm = generate_list('mc_')


# start_parrot = "parrot", "repeat after me", "repeat what i say", "mimic", "mimic me", "parrot mode", "parrot on", "turn parrot on", "start parrot", "start mimic", "start mimicing", "start mimicing me", "start mimicing me", "reply what i say", 'reply what i send', "copy me"

ip.start_parrot = [
    C(r"(start )?parrot(mode )?( on)?"),
    C(r"mimic( me)?"),
    C(r"start mimicing( me)?"),
    C(r"(re(ply|peat)|say) what i (say|type|send|write)"),
    C(r"repeat after me")
]
stop_parrot = "stop", "stop it", "stop mimicing", "stop mimic", "stop parrot", "off", "turn off", "turn parrot off", "cancel", "cancel mimic", "cancel parrot"

ip.stop_parrot = [
    C(r"(stop|cancel)( (it|mimicing|repeating|parrot))?"),
    C(r"(turn )?((parrot|it) )?of+"),
]


links_dict = {
    "url_google": ('https://www.google.com', 'google', 'gogle', 'gooogle'),
    "url_fb": ('https://www.facebook.com', 'facebook', 'facebok', 'fb'),
    "url_yahoo": ['https://www.yahoo.com', 'yahoo', 'yaho'],
    "url_youtube": ['https://www.youtube.com', 'youtube', 'tubemate', 'utube'],
    "url_wiki": ['https://www.wikipedia.com', 'wikipedia', 'wikipidia', 'wikipidea', 'wikipedea'],
    'url_reddit': ['https://www.reddit.com', 'reddit', 'redit'],
    'url_bing': ['https://www.bing.com', 'bing', 'microsoft search'],
    'url_insta': ['https://www.instagram.com', 'instagram', 'insta'],
    'url_apple': ['http://apple.com/', 'apple website', 'apple.com'],
    'url_microsoft': ['http://microsoft.com/', 'microsoft website', 'microsoft.com', 'microsoft site', 'microsoft page'],
    'url_pornhub': ['https://www.pornhub.com/', 'pornhub website', 'pornhub'],

    'goog_supp': ['http://support.google.com/', 'support', 'supports'],
    'goog_docs': ['http://docs.google.com/', 'doc', 'docs'],
}
# if 'insta' in links:print(links)
# sleep(10)
links = tuple(i for k, v in links_dict.items() for i in v)
links_li = tuple(v for k, v in links_dict.items())
# googles = generate_list('goog_')
# googles_li = gen_list('goog_')

# print(*links, sep='\n')

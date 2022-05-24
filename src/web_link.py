#pylint:disable=W0312
import webbrowser
import re
def generate_list(x):
    l = [globals()[name] for name in globals().keys() if name.startswith(x)]
    return [item for sublist in l for item in sublist]

def gen_list(x):
    l = [globals()[name] for name in globals().keys() if name.startswith(x)]
    return [sublist for sublist in l]


url_google=('https://www.google.com','google','gogle','gooogle')
url_fb=['https://www.facebook.com','facebook','facebok','fb']
url_yahoo=['https://www.yahoo.com','yahoo','yaho']
url_youtube=['https://www.youtube.com','youtube','tubemate','utube']
url_wiki=['https://www.wikipedia.com','wikipedia','wikipidia','wikipidea','wikipedea']
url_reddit=['https://www.reddit.com','reddit','redit']
url_bing=['https://www.bing.com','bing','microsoft search']
url_insta=['https://www.instagram.com','instagram','insta']
url_apple=['http://apple.com/', 'apple website','apple.com']
url_microsoft=['http://microsoft.com/','microsoft website', 'microsoft.com']
'''url_
url_
url_
url_
url_
url_
url_'''
goog_supp=['http://support.google.com/','support','supports']
goog_docs=['http://docs.google.com/','doc','docs']
links=generate_list('url_')
links_li=gen_list('url_')
googles=generate_list('goog_')
googles_li=gen_list('goog_')

def web_go(link):
	webbrowser.open_new_tab(link)

def linker(x):
	global links_li
	for i in links_li:
		if x in i:
			web_go(i[0])
def googler(link):
	global googles_li
	for i in googles_li:
		if x in i:
			web_go(i[0])
def searcher(x):
	loc= x.replace(' ','+')
	webbrowser.open_new_tab( 'https://www.google.com/search?q='+loc)

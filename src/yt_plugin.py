from urllib import request, parse
from urllib.error import URLError, HTTPError
from threading import Thread
import random

#import urllib.request
#import urllib
#from urllib.parse import *

from os import getcwd, remove, makedirs
#from bs4 import BeautifulSoup
from time import sleep
from os.path import exists
import re
from platform import system as os_name
os_name = os_name()
if os_name == "Windows":
    import console_mod
    console_mod.set_width(16)
    console_mod.enable_color()

from os import system as os_system
yt_code = re.compile("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?")
#from playsound import playsound
"""from mplay import playsound
if system()=='Windows':
    from mplay import Wvolume as vol, Wpause as pause, Wresume as resume, Wmode as mode, Wispaused as ispaused, Wisplaying as isplaying, Wison as ison, Wstop as stop, Wduration_ms as dur_ms"""

'''

py -3.7 -m pip freeze > r.txt
py -3.7 -m pip uninstall -r r.txt -y
py -3.7 -m pip install pyinstaller-4.3.zip pypiwin32 comtypes pywin32-ctypes pafy youtube_dl cffi
py -3.7 -O -m PyInstaller "yt_plugin.py" -F -n "Youtube Player CLI" --version-file vtesty.py -i "ic.ico" --upx-dir=.
py -3.7 -m pip install -r r.txt -y
'''

#import urllib.parse

import re
#print(0)
if os_name == "Windows":
	import mplay4 as mplay
	use_mplay = True

else:
	use_mplay = False

from print_text2 import xprint
from fsys import Datasys_, IOsys_, Fsys_
Datasys = Datasys_()
IOsys = IOsys_()
Fsys = Fsys_()
import json
import yt_dlp
ydl_opts = {
    'format': 'm4a/bestaudio',
    "ext": "m4a"
}

#exit()

def get_title(url):
	x = ydl_opts.copy()
	x["quiet"] = True
	with yt_dlp.YoutubeDL(x) as ydl:
		info = ydl.extract_info(url, download=False)


    # ℹ️ ydl.sanitize_info makes the info json-serializable
	return ydl.sanitize_info(info)["title"]


#mplay.load('Songs/v0J8WzahNC0.mp3').play()
##sleep(5)
#mplay.Wstop()
#print("hi")


def check_internet(host='https://www.google.com/', timeout=2):
    """returns True or False based on internet availability"""
    if host == 'fast':
        return check_internet('http://www.muskfoundation.org/', timeout=timeout)

    elif host == 'pypi':
        return check_internet('https://pypi.org/', timeout=timeout)

    else:
        #request.urlopen(host, timeout=timeout)
        try:
            request.urlopen(host, timeout=timeout)
            return True
        except URLError:
            return False


start='title%21%3A%21'

end='%21%2C%21lengthSeconds'

remove_non_ascii = Datasys.remove_non_ascii



clear_screen = IOsys.clear_screen

delprevline = IOsys.delete_last_line


db_format= {
"codes":
[],
"titles":
[],
"counts":
[],

"search_txt":
[],
"tags":
[]
}


import json

def make_db():
        
    Fsys.writer("data3.json", 'w', json.dumps(db_format), "songs/")
#make_db()

search='asdf'
def loc(x):
    """to fix dir problem"""
    if os_name.lower() == 'windows':
        return x.replace('/', '\\')
    else:
        return x.replace('\\', '/')


def reader(direc):
    with open(loc(direc),'rb') as f:
        return f.read()
#import __main__
def get_dat():
    global codes, titles, counts, search_txt, counts, doc
    if exists(loc('songs/data3.json')) ==False:
        make_db()
    if Fsys.reader('songs/data3.json').strip() == "":
        make_db()
    
    return json.loads(Fsys.reader("songs/data3.json"))
    # exec(reader('songs/data3.json'))
    #print(counts)
    # returns search_txt
    # returns tags
    # returns codes
    # returns titles
    # returns counts
#get_dat()

def set_dat():
    x= {
"codes":
codes,
"titles":
titles,
"counts":
counts,

"search_txt":
search_txt,
"tags":
tags
}
    y= json.dumps(x)
    Fsys.writer('data3.json', 'w', y, 'songs/') 
def delthisline():
    print('\x1b[2K',end='')

def mk_title(title):
    x = remove_non_ascii(title, '_')
    return ''.join(i if i not in '\\/|:*"><?' else '#' for i in x )

#print(request.urlopen("https://www.youtube.com/results?search_query=stay+gold").read().decode())

def url_research(search_string):

    query_string = parse.urlencode({"search_query" : search_string})

    html_content = request.urlopen("http://www.youtube.com/results?" + query_string)

    search_results = re.findall(r'\"url\"\:\"\/watch\?v\=(.{11})\"', html_content.read().decode())

    if search_results:

        return search_results[0]

    else: url_research(search_string)


def get_cache():
    global search_txt, tags, counts, titles, codes
    xxx = get_dat()

    # db_py=reader('songs/data3.json').split(b'\n')
    search_txt= xxx['search_txt'] # returns search_txt
    tags= xxx['tags'] # returns tags
    codes= xxx['codes'] # returns codes
    titles= xxx['titles']# returns titles
    counts= xxx['counts']# returns countspass



class Youtube_mp3(): 

    def __init__(self):
        get_cache()

        self.lst = [] 

        self.url = 0

        self.dict_names = 0

        self.playlist = []

        self.code = 0
        self.search_string = ''

    def url_search(self, search_string):
        self.search_string = search_string

        if check_internet('https://www.youtube.com') == True:
            self.code = url_research(search_string)
            i = 0
            while self.code==None:
                self.code = url_research(search_string)
                if i>6:
                    xprint('  /yb/retry(', i, ')/=/', end='\r')
                    xprint("Failed to Get the link. \n/y/Please check your Internet Connection/=/")
                    return False
                i+=1
            if i>0:
                delthisline()
        else:
            if search_string in search_txt:
                asd=tags[search_txt.index(search_string)]
                self.code = codes[asd]
            else: return False
        
        self.url= "http://www.youtube.com/watch?v="+ self.code
        return True

    def link_parse(self, link):
        
        if yt_code.search(link):
            self.code = link
            self.url= "http://www.youtube.com/watch?v="+ self.code
            self.search_string = link
            return True
            
        
        return False

    def download_media(self):

        global song_name
        
        #info = pafy.new(self.code)
        
        '''for a in info.audiostreams:
            print(a.bitrate, a.extension, a.get_filesize())'''
        #audio=None
        #while audio==None:
        #    audio = info.getbestaudio()
        #self.dict_names = mk_title(info.title, 'Youyube_mp3.download_media')
        self.dict_names = mk_title(get_title(self.url))
        self.update_dat()

        song_name="songs/"+self.dict_names+'.m4a'
        

        xprint("\n  /hui/ Buffering /=/ : /u/{0}/=/".format(self.dict_names))
        
        if  exists(song_name):
            if check_internet('https://www.youtube.com') == True:
                remove(song_name)
            else: return True
        ydl_opts_ = ydl_opts
        ydl_opts_['outtmpl'] = song_name
        while True:
            try:
                with yt_dlp.YoutubeDL(ydl_opts_) as ydl:
                    ydl.download(self.url)
                break
            except KeyboardInterrupt:
                print('\n')
                return False
            except EOFError:
                print('\n')
                return False
            except (HTTPError, URLError):
                continue

        delprevline()
        delprevline()
        xprint("   /hui/ Playing /=/ : /u/{0}/=/\n".format(self.dict_names))
        
        return True



    def add_playlist(self, search_query):

        url = self.url_search(search_query)

        self.playlist.append(url)

    def update_dat(self):
        
        global search_txt, tags, counts, titles, codes
        if self.code in codes:
            #code = codes[tags[search_txt.index(search)]]
            #title = titles[codes.index(x.code)]
            counts[codes.index(self.code)] += 1
            #tags+=[codes.index(x.code)]
            # doc[18]= str(counts)+'\n'
            if self.search_string not in search_txt:
                search_txt.append(self.search_string)

                tags.append(codes.index(self.code))


        else:
            #
            search_txt.append(self.search_string)
            codes.append(self.code)
            tags.append(len(codes))
            titles.append(self.dict_names)
            counts.append(1)

        set_dat()


retry=0

def play_youtube(search, sleep_play = False):
    
    global search_txt, tags, counts, titles, codes
    global music
    if search=='plr':
        if exists(loc('songs/watch_list.txt')):
            search= random.choice(open(loc('songs/watch_list.txt')).readlines())
        elif exists(loc('watch_list.txt')):
            search= random.choice(open(loc('watch_list.txt')).readlines())
        else:
            xprint('\n/y/Playlist /b/"watch_list.txt"/=/ file not found!!!/=/\n')
    search=search.replace('\n', "")
    #found=False

    get_cache()


    x = Youtube_mp3()


    if check_internet('https://www.youtube.com') == True:
        global song_name, retry

        if not x.link_parse(search):
            if not x.url_search(search):
                return 0

        if not x.download_media():
            return 0

        if exists(song_name):
            play_music=True
        else: play_music=False
    else:
        #print(titles,counts,search_txt,codes,tags)
        if search in search_txt:
            asd=tags[search_txt.index(search)]
            x.code = codes[asd]
            x.dict_names = titles[asd]
            song_name= loc("songs/"+x.dict_names+'.m4a')
            if exists(song_name):
                play_music=True
            else: play_music=False
        else: play_music=False
    if os_name !="Windows": 
        xprint("/y/Can only play on Windows/=/")
        return
    if play_music==True:
        music=mplay.load(song_name)
        try:
            music.play()
            if sleep_play:
                sleep(music.duration())
        except KeyboardInterrupt:
            print('\n')
            music.stop()
        except EOFError:
            print('\n')
            music.stop()


    else:
        xprint('/hui/ Unable to play due to /r/Internet Issue. /=/')
    return 0

    #delprevline()


    """if exists('songs/data2.py'):
        with open('songs/data2.py','r') as file:
            #file.write(x.dict_names.encode('utf-8'))
            #print(file.read())
            if file.read()!='':
                exec(file.readlines()[16])
                if search in search_txt:

                if i.startswith(x.code+b"="):
                    print(i)
                    found=file.index(i)
                    exec(file[found])
                    exec(b'count='+x.dict+b'[0]')
                    data1=data[0]+1
            else:
                make_db()
    else:
        make_db()
    if found==False:
        with open('songs/data.py','ab+') as file:
            file.write(x.code.encode('utf-8'))
            file.write(b'= [1, "')
            file.write(x.dict_names.encode('utf-8'))
            file.write(b'",["')
            file.write(search.encode('utf-8'))
            file.write(b'"]]\n')
    else:
        print(found)
        with open('songs/data.py','w+') as file:
            old=file.readlines()[found]
            exec(old)
            exec('dat = '+x.code)
            a=len(str(dat[0]))
            new=x.code+'= ['+str(dat[0])+ old[16+a:len(old)-2]+',"'+search+'"]]'
            file.write(file.read().replace(old,new))"""





#mplay.load('songs/0nOYRp1821.m4a')
if __name__ == '__main__':
    clear_screen()
while __name__=='__main__':
    xprint('/hui/ Enter the Song title or Link /=/ : ', end="")
    ui= input()

    if ui=="pl":
        for i in open('songs/watch_list.txt').readlines():
            play_youtube(i, True)
    elif ui=='plr':
        plr= random.choices(open(loc('songs/watch_list.txt')).readlines(),k=random.randrange(20,30))
        for i in plr:
            play_youtube(i, True)
    else:

        play_youtube(ui, True)


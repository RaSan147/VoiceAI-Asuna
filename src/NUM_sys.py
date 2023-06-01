#: *****************************************************************************
#:               The code in this file was created by Ratul Hasan              *
#:                     So comlpete credit goes to him(me)                      *
#: *****************************************************************************
#:         Sharing this code without my permission is not allowed              *
#: *****************************************************************************
#: This code was created based on IDLE, Pydroid(Android), qPython(Android) etc.*
#: So most online/web site based idle(i.e: Sololearn) can't run this code	   *
#: properly.                                                                   *
#: *****************************************************************************
#: If there is any bug or you want to help please let me know.                 *
#: e-mail: wwwqweasd147[at]gmail[dot]com                                       *
#: *****************************************************************************


from random import randint
from functools import partial
from base64 import b85encode, b85decode
# import os

from datetime import datetime, timedelta
import time

base_li0= {'0':0,
	'1':1,
	'2':2 ,
	'3':3 ,
	'4':4 ,
	'5':5 ,
	'6':6 ,
	'7':7 ,
	'8':8 ,
	'9':9 ,
	'a':10 ,
	'b':11 ,
	'c':12 ,
	'd':13 ,
	'e':14 ,
	'f':15 ,
	'g':16 ,
	'h':17 ,
	'i':18 ,
	'j':19 ,
	'k':20 ,
	'l':21 ,
	'm':22 ,
	'n':23 ,
	'o':24 ,
	'p':25 ,
	'q':26 ,
	'r':27 ,
	's':28 ,
	't':29 ,
	'u':30 ,
	'v':31 ,
	'w':32 ,
	'x':33 ,
	'y':34 ,
	'z':35 ,
	'A':36 ,
	'B':37 ,
	'C':38 ,
	'D':39 ,
	'E':40 ,
	'F':41 ,
	'G':42 ,
	'H':43 ,
	'I':44 ,
	'J':45 ,
	'K':46 ,
	'L':47 ,
	'M':48 ,
	'N':49 ,
	'O':50 ,
	'P':51 ,
	'Q':52 ,
	'R':53 ,
	'S':54 ,
	'T':55 ,
	'U':56 ,
	'V':57 ,
	'W':58 ,
	'X':59 ,
	'Y':60 ,
	'Z':61 ,
	'+':62 , '?': 62, # old version compatibilitys
	'/':63 , '!': 63 # old version compatibilitys

}

base_li= "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"

def dec2base(n,base):


	out=''

	if n == "": # IPv6 :: patch
		return out
	n = int(n)
	if n==0:
		return '0'

	while n!=0:
		out+=base_li[n%base]
		n//=base

	return out[::-1]



def base2dec(n, base, _type:type=int):
	if n =='':
		return ''
	out=0
	n=str(n)[::-1]

	for  i in range(len(n)):

		out+=base_li0[n[i]]*(base**(i))

	return _type(out)

def base2base(n, ibase, obase):
	if n == "":
		return ""

	dec = base2dec(n, ibase)
	return dec2base(dec, obase)

def dt_():
	"""returns time in GMT+6
	"""
	return str(datetime.now()+ timedelta(hours=6))

def compressed_dt(_dt= ''):

	# OLD VERSION# dt_now= int((dt_() if _dt is None else _dt).replace('-','').replace(' ','').replace('.','').replace(':',''))
	_dt = str(time.time()) if _dt is None else _dt
	xtime = _dt.split('.')
	return dec2base(xtime[0], 63) +'.'+ dec2base(xtime[1], 63)
	# return dec2base(dt_now,63)

cdt_ = compressed_dt

def compressed_ip(ip):
	if isinstance(ip, dict):
		ip = ip['ip']

	# if IPv4
	joint = "~"
	junk = [randint(0,255) for i in range(4)]
	if ":" in ip: # IPv6
		ip_now= ip.split(':')

		for n, i in enumerate(ip_now):
			if i:
				ip_now[n] = int(i, 16)
				joint = "#" # if IPv6
				junk = [randint(0,65535) for _ in range(4)]
	else:
		ip_now= ip.split('.')
	new_dec2base = partial(dec2base, base=63)


	return joint.join(map(new_dec2base,  junk[:2]+ip_now+junk[2:]))

def dec_ip(ip):
	if not isinstance(ip, str):
		return '127.0.0.1'

	sep = "~"
	joint = "."
	converter = partial(base2dec, base=63, _type=str)
	if "#" in ip:
		sep = "#"
		joint = ":"
		converter = partial(base2base, ibase=63, obase=16)

	ip_now= ip.split(sep)[2:-2]


	return joint.join(map(converter, ip_now))


#print(compressed_ip("2001:db8::1"))
#print(dec_ip(compressed_ip("2001:db8::1")))

def dec_dt(dt):
	ddt = str(base2dec(dt, 63))
	#print(ddt)
	YYYY = ddt[:4]
	MM= ddt[4:6]
	DD= ddt[6:8]
	hh= ddt[8:10]
	mm= ddt[10:12]
	ss= ddt[12:14]+'.'+ddt[14:]

	return (YYYY,MM,DD,hh, mm, ss)

# print(dec_dt(compressed_dt()))

def get_tz():

	tznow = datetime.now().astimezone()

	return (str(tznow)[-6:])

def flatten_array(out, output_type = list):
	'''Will flatten `list`, `tuple`, `set`'''
	if not isinstance(out, list):
		out= list(out)
	i=0
	l =len(out)
	while i<l:
		if isinstance(out[i], (list, tuple, set)):
			out.extend(flatten_array(out.pop(i)))
			l-=1
		else: i+=1
	if not isinstance(out, output_type):
		out= output_type(out)
	return out


def hash_bin64(data):
	try:
		import xxhash
	except ImportError:
		raise ImportError("Please install xxhash")

	if isinstance(data, int):
		data = data.to_bytes((data.bit_length() + 7) // 8, byteorder="big")  # Here's where the magic happens

	x = xxhash.xxh3_64_digest(data)
	return b85encode(x)



def fmbytes(B=0):
	'Return the given bytes as a file manager friendly KB, MB, GB, or TB string'

	B = B
	KB = 1024
	MB = (KB ** 2) # 1,048,576
	GB = (KB ** 3) # 1,073,741,824
	TB = (KB ** 4) # 1,099,511,627,776


	if B/TB>1:
		return '%.2f TB  '%(B/TB)
	if B/GB>1:
		return '%.2f GB  '%(B/GB)
	if B/MB>1:
		return '%.2f MB  '%(B/MB)
	if B/KB>1:
		return '%.2f KB  '%(B/KB)
	if B>1:
		return '%i bytes'%B

	return "%i byte"%B


def humanbytes(B=0):
	'Return the given bytes as a human friendly KB, MB, GB, or TB string'
	B = B
	KB = 1024
	MB = (KB ** 2) # 1,048,576
	GB = (KB ** 3) # 1,073,741,824
	TB = (KB ** 4) # 1,099,511,627,776
	ret=''

	if B>=TB:
		ret+= '%i TB  '%(B//TB)
		B%=TB
	if B>=GB:
		ret+= '%i GB  '%(B//GB)
		B%=GB
	if B>=MB:
		ret+= '%i MB  '%(B//MB)
		B%=MB
	if B>=KB:
		ret+= '%i KB  '%(B//KB)
		B%=KB
	if B>0:
		ret+= '%i bytes'%B

	return ret



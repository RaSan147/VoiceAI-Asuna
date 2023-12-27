#!/usr/bin/python3

"""
	search.py

	MediaWiki API Demos
	Demo of `Search` module: Search for a text or title

	MIT License
"""
import re


import requests
import wikipediaapi

from DS import Flag

session = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"




def wolfram(text):
	"""
	returns wolfram alpha response based on query text
	text: query
	raw: the untouched user input for logging
	"""
	r = session.get("http://api.wolframalpha.com/v1/spoken",
					params={
						"i": text,
						"appid": "L32A8W-J8X5U6KG26"
					},
					timeout=60
				)
	if not r:
		return False

	if r.text == "My name is Wolfram Alpha":
		return "My name is <:ai_name>"
	return r.text


wikipedia = wikipediaapi.Wikipedia(
		user_agent="VoiceAI-Asuna/1.0 (https://github.com/RaSan147/VoiceAI-Asuna; wwwqweasd147@gmail.com)"
	)



def wiki_summary(uix):
	"""
	search in wikipedia,
	split only 4 sentences
	parse results to HTML
	"""
	ny = wikipedia.page(uix)
	link = ny.fullurl

	# returns 4 line of summary
	s = ny.summary
	s = s.split("\n\n")[0]
	s = s.replace("\n", "<br>")
	s = re.sub(r"</?br>", " <br>", s)
	s = re.sub("( ){2,}", " ", s)
	s = re.split("<br> ?<br>", s)[0]
	s = (". ").join(s.split(". ")[:4]).strip() + "..." # should end with a fullstop as well

	return link, s



def search(SEARCHPAGE:str, limit=10):
	PARAMS = {
		"action": "query",
		"format": "json",
		"list": "search",
		"srsearch": SEARCHPAGE,
		#"srqiprofile": "wsum_inclinks_pv",
		"srprop": "timestamp",
		"srlimit": limit,
		"srenablerewrites": True,
	}

	R = session.get(url=URL, params=PARAMS)
	DATA = R.json()

	#print(*[i for i in DATA['query']['search']], sep="\n\n")

	return [Flag(i) for i in DATA.get('query', {}).get('search', {}) if i]


#if DATA['query']['search'][0]['title'] == SEARCHPAGE:
#    print("Your search page '" + SEARCHPAGE + "' exists on English Wikipedia")

def fix_prompt(ui):
	ui = ui.lower()
	if ui == "asuna":
		ui="Asuna Yuuki"
	if ui == "kirito":
		ui = "Kirito (Sword Art Online)"
	if ui == "sao":
		ui = "Sword Art Online"

	return ui


if __name__ == "__main__":
	for i in search("green vitriol"):
		print(i)
		print("\n"*2)
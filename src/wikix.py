#!/usr/bin/python3

"""
	search.py

	MediaWiki API Demos
	Demo of `Search` module: Search for a text or title

	MIT License
"""

import requests

from DS import Flag

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

SEARCHPAGE = "SAO"


def search(SEARCHPAGE:str, max=10):
	PARAMS = {
		"action": "query",
		"format": "json",
		"list": "search",
		"srsearch": SEARCHPAGE,
		#"srqiprofile": "wsum_inclinks_pv",
		"srprop": "timestamp",
		"srlimit": max,
		"srenablerewrites": True,
	}

	R = S.get(url=URL, params=PARAMS)
	DATA = R.json()

	#print(*[i for i in DATA['query']['search']], sep="\n\n")

	return [Flag(i) for i in DATA['query']['search']]


#if DATA['query']['search'][0]['title'] == SEARCHPAGE:
#    print("Your search page '" + SEARCHPAGE + "' exists on English Wikipedia")

def fix_promt(ui):
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
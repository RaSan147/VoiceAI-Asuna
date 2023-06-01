import requests
import json
import net_sys


class OnLine:
	def __init__(self):
		self.latest_link = "https://cdn.jsdelivr.net/gh/RaSan147/voiceAI-skins@" + self.get_latest_commit()
		self.characters = self.get_characters()
		self.cached_characters = {}

	def get_characters(self):
		r = net_sys.get_page(self.latest_link + "/characters.json",
							cache=True,
							do_not_cache=False,
							cache_priority=True)
		return json.loads(r.content)

	def get_latest_commit(self):
		r = net_sys.get_page("https://api.github.com/repos/RaSan147/voiceAI-skins/commits/main",
							cache=True,
							do_not_cache=False,
							cache_priority=True)
		commits = json.loads(r.content)
		return commits['sha']

	def get_character(self, name):
		c = self.characters[name]
		if name in self.cached_characters:
			return self.cached_characters[name]
		folder = c['folder']
		link = self.latest_link + "/" + folder + "/skins.json"
		r = net_sys.get_page(link,
							cache=True,
							do_not_cache=False,
							cache_priority=True)
		# print(r.text)
		c['skins'] = json.loads(r.text)
		self.cached_characters[name] = c
		return c

	def get_skins(self, character):
		return self.get_character(character)['skins']

	def get_skin(self, character, skin):
		skin = str(skin)
		skins = self.get_skins(character)
		return skins[skin]

	def get_skin_link(self, character, skin):
		skin = self.get_skin(character, skin)
		folder = self.get_character(character)['folder']
		return self.latest_link + "/" + folder + "/" + skin['file']

if __name__ == "__main__":
	online = OnLine()
	print(online.get_skin_link("Asuna", 1))
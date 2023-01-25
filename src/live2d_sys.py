import requests
import json


class OnLine:
	def __init__(self):
		self.latest_link = "https://cdn.jsdelivr.net/gh/RaSan147/voiceAI-skins@" + self.get_latest_commit()
		self.characters = self.get_characters()
		self.cached_characters = {}

	def get_characters(self):
		r = requests.get(self.latest_link + "/characters.json")
		return json.loads(r.text)
	
	def get_latest_commit(self):
		r = requests.get("https://api.github.com/repos/RaSan147/voiceAI-skins/commits/main")
		commits = json.loads(r.text)
		return commits['sha']
	
	def get_character(self, name):
		c = self.characters[name]
		if name in self.cached_characters:
			return self.cached_characters[name]
		folder = c['folder']
		link = self.latest_link + "/" + folder + "/skins.json"
		r = requests.get(link)
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
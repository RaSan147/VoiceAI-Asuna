from collections import Counter
import re

from bs4 import BeautifulSoup as bs, FeatureNotFound as bs_FeatureNotFound

from user_handler import User


_parser = 'lxml'
try:
	bs('<br>', _parser)
except bs_FeatureNotFound:
	_parser = 'html.parser'



# default message dict
message_dict = {
	"message": "",
	"render": "innerText",
	"script": ""
}

def strip_msg(msg:dict):
	for i in msg:
		if isinstance(msg[i], str):
			msg[i] = re.sub(r'[ \t]{2,}', ' ', msg[i].strip())
	return msg



class MessageObj(dict):
	def __init__(self, user: User, ui: str="", ui_raw: str="", mid: int=0, *args, **kwargs):
		super().__init__(message_dict.copy(), *args, **kwargs)

		self.__dict__ = self

		self.intents = []
		self.ui = ui
		self.ui_raw = ui_raw
		self.mid = mid


		self.context_count = Counter([j for i in user.chat.intent for j in i])
		self.prev_intent = user.chat.intent[-1] if user.chat.intent else []
	# context [[...],...] is the intent of the previous message

		self.on_context = []

	#def __setitem__(self, key, value):
#		super().__setitem__(key, value)

#	def __getitem__(self, __key):
#	 	return self.msg.__getitem__(__key)

	def trimmed(self):
		out = {}
		items = [
			"status",
			"message",
			"script",
			"render",
			"expression",
			"motion",
			"voice",

			"mid",
			"rid",
			"delay",

		]
		for i in items:
			out[i] = self.get(i)

		return out

	def add_intent(self, intent: str):
		"""Add message intent in list"""

		self.intents.append(intent)

	def add_context(self, context: str):
		"""
		if bot replies based on previous message intent (context),
		then the bot will add the intent to the context list
		"""

		self.on_context.append(context)

	def check_context(self, context=()):
		"""
		check if any of the context list is in previous msg intent
		"""
		for i in context:
			if i in self.prev_intent:
				return True

	def clean(self):
		"""
		forgot what it is
		"""
		self.clear()
		self.update(message_dict.copy())

	def rep(self, msg_txt, script="", render="", expression=""):
		"""add message to the output"""
		if isinstance(msg_txt, dict):
			script = msg_txt.get("script", "") + "\n\n" + str(script)
			render = msg_txt.get("render", "")
			message = msg_txt["message"]
			expression = expression or msg_txt.get("expression", "")
		else:
			message = msg_txt

		self["message"] += "\n\n" + str(message)

		if render:
			self["render"] = str(render)

		if script:
			self["script"] += "\n\n" + str(script)

		if expression:
			self["expression"] = str(expression)

		return strip_msg(self)

	def string_text(self):
		"""return the message text"""
		return self["message"]

	def flush(self):
		"""flush the output, intent and context"""
		return self, self.intents, self.on_context, self.ui, self.ui_raw

	def for_voice(self):
		"""
		|*t|For Text output ONLY|t*|
		|*v|For Voice output ONLY|v*|
		|/*|For Text|*|For Voice|*/|
		"""

		if self["render"] == "innerHTML":
			text = self.html2str()
		else:
			text = self["message"]

		text = text.encode("ascii", errors="ignore").decode("ascii")

		text = re.sub(r'\|\*t\|(.*?)\|t\*\|', r'', text)
		text = re.sub(r'\|\*v\|(.*?)\|v\*\|', r'\1', text)

		text = re.sub(r'\|\*\|(.*?)\|\*\|(.*?)\|\*\/\|', r'\2', text)

		return text

	def for_HTML(self):
		"""
		|*t|For Text output ONLY|t*|
		|*v|For Voice output ONLY|v*|
		|*/|For Text|*|For Voice|/*|
		"""

		if self["render"] == "innerHTML":
			text = self.str2html()
		else:
			text = self["message"]

		text = re.sub(r'\|\*t\|(.*?)\|t\*\|', r'\1', text)
		text = re.sub(r'\|\*v\|(.*?)\|v\*\|', r'', text)

		text = re.sub(r'\|\*\|(.*?)\|\*\|(.*?)\|\*\/\|', r'\1', text)

		return text

	def for_console(self):
		"""
		|*t|For Text output ONLY|t*|
		|*v|For Voice output ONLY|v*|
		|/*|For Text|*|For Voice|*/|
		"""

		if self["render"] == "innerHTML":
			text = self.html2str()
		else:
			text = self["message"]

		text = re.sub(r'\|\*t\|(.*?)\|t\*\|', r'\1', text)
		text = re.sub(r'\|\*v\|(.*?)\|v\*\|', r'', text)

		text = re.sub(r'\|\*\|(.*?)\|\*\|(.*?)\|\*\/\|', r'\1', text)

		return text

	def html2str(self):
		"""convert html to string"""
		data = self["message"]

		data = data.replace("<br>", "\n").replace("<br/>", "\n")
		data = data.replace("&emsp;", "\t")
		data = data.replace("&nbsp;", "  ")
		data = data.replace("&lt;", "<")
		data = data.replace("&gt;", ">")
		data = data.replace("&quot;", '"')
		data = data.replace("&apos;", "'")
		data = data.replace("&amp;", "&")

		data = bs(data, _parser).text

		return data

	def str2html(self):
		"""convert string to html"""
		data = self["message"]

		data = data.replace("\n", "<br>")
		data = data.replace("\t", "&emsp;")
		data = data.replace("  ", "&nbsp; ")


		return data



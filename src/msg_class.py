from collections import Counter

from user_handler import User


# default message dict
message_dict = {
	"message": "",
	"render": "innerText",
	"script": ""
}



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
			script = msg_txt.get("script", "")
			render = msg_txt.get("render", "")
			msg_txt = msg_txt["message"]
			expression = expression or msg_txt.get("expression", "")

		self["message"] += "\n\n" + str(msg_txt)

		if render:
			self["render"] = str(render)

		if script:
			self["script"] += "\n\n" + str(script)

		if expression:
			self["expression"] = str(expression)

		return self

	def flush(self):
		"""flush the output, intent and context"""
		return self, self.intents, self.on_context, self.ui, self.ui_raw


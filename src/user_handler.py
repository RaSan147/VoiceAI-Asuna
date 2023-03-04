import os
import json
import hashlib
import time, datetime
import traceback
import inspect


import F_sys
import net_sys

from CONFIG import appConfig
from DS import GETdict, Flag
import live2d_sys
import CONSTANTS

#############################################
#                USERS HANDLER              #
#############################################



class User(GETdict):
	"""can get and set user data like a js object

	to set item, use dict["key"] = value for the 1st time,
	then use dict.key or dict["key"] to both get and set value

	but using dick.key = value 1st, will assign it as attribute and its temporary
	"""
	def __init__(self, username):


		self.username = username
		self.user_path = os.path.join(appConfig.user_data_dir, username)
		self.file_path = os.path.join(self.user_path, '__init__.json')



		self.flags = Flag()
		self.chat = Flag()
		self.chat.intent = {}
		self.pointer = 0

		# if the data asked for is already there
		data = F_sys.reader(self.file_path, on_missing=None)
		if not data:
			raise Exception("User not found")

		try:
			json_data = json.loads(data)
			for key in json_data:
				self[key] = json_data[key]
		except Exception:
			traceback.print_exc()
			raise Exception("User data corrupted")
				

	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		self.save()

	# def __getattribute__(self, __name: str):
	# 	return super().__getattribute__(__name)

	def save(self):
		J = json.dumps(self, indent=2)
		F_sys.writer("__init__.json", 'w', J, self.user_path)

	def get_chat(self, pointer=-1):
		if pointer == -1: pointer = self.pointer
		pointer = str(pointer)
		file_path = os.path.join(self.user_path, pointer+'.json')

		# if the data asked for is already there
		data = F_sys.reader(file_path, on_missing=None)
		if data:
			return json.loads(data)

		return None
	
	demo_chat = {
		"id": 0,
		"msg": "hello Asuna",
		"time": 123456789,
		"user": "USER",
		"parsed_msg": "hello <:ai_name>",
		"rTo": -1,
		"intent": "", 
		# intent of user message can't be determined immediately
		# so it will be determined later, on bot's reply
	}

	def add_chat(self, msg, time, user=1, parsed_msg="", rTo=-1, intent=""):
		"""
		msg: message sent
		time: time of message
		user: 1 if user, 0 if bot
		parsed_msg: parsed message by basic_output
		rTo: reply to message id (-1 if not reply)
		"""
		pointer = self.pointer
		old = self.get_chat(pointer)
		if old is None:
			old = []
		
		if len(old) >= 100:
			self.pointer += 1
			old = []
		pointer = str(self.pointer)

		chat = self.demo_chat.copy()

		user = "USER" if user else "BOT"

		self.msg_id += 1
		id = self.msg_id
		chat['id'] = id
		chat['msg'] = msg # dict, contains msg, script and render mode
		chat['time'] = time
		chat["parsed_msg"] = parsed_msg
		chat['rTo'] = rTo
		chat['intent'] = intent
		chat['user'] = user

		old.append(chat)

		J = json.dumps(old, indent=2, separators=(',', ':'))
		F_sys.writer(pointer+'.json', 'w', J, self.user_path)

		return id


class UserHandler:
	def __init__(self) -> None:
		self.users = {} #username: User()

		self.online_avatar = live2d_sys.OnLine()

		self.default_user = {
			"username": "default",
			"password" : "default",
			"created_at": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
			"last_active": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
			"pointer": 0, # current chat index (100 msg => 1 pointer)
			"nickname": "default", # current user name
			"bot": None, # user preferred bot name
			"id": "default", #
			"ai_name": "Asuna", # user preferred ai name
			"bot_charecter": "Asuna", # user preferred ai avatar
			"bot_skin": 0,
			"skin_mode": 1, # 0 = offline, 1 = online
			"room": 0,
			"custom_room": None,
			"msg_id": 0,
		}


	def u_path(self, username):
		return os.path.join(appConfig.user_data_dir, username)

	# def login(self, username, password):
	# 	hash = hashlib.sha256(username)

	# def get_user(self, username, uid=None):
	# 	return self.collection(username, uid)

	# def get_user_data(self, username, pointer):
	# 	user_path = self.u_path(username)
	# 	file_path = os.path.join(user_path, pointer+'.json')

	# 	# if the data asked for is already there
	# 	if os.path.exists(file_path):
	# 		with open(file_path, 'r') as f:
	# 			return json.load(f)

	# 	return None

	def create_user(self, username, password):
		hash = hashlib.sha256((username+password).encode('utf-8'))
		id = hashlib.sha1((str(time.time()) + username).encode("utf-8")).hexdigest()
		u_data = {
			"username": username,
			"password": hash.hexdigest(),
			"created_at": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
			"last_active": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
			"pointer": 0, # current chat index (100 msg => 1 pointer)
			"nickname": username, # current user name
			"bot": None, # user preferred bot name
			"id": id, #
			"ai_name": "Asuna", # user preferred ai name
			"bot_charecter": "Asuna", # user preferred ai avatar
			"bot_skin": 0,
			"skin_mode": 1, # 0 = offline, 1 = online
			"room": 0,
			"custom_room": None,
			"msg_id": 0,
		}

		J = json.dumps(u_data, indent=2)
		F_sys.writer("__init__.json", 'w', J, self.u_path(username))

		return id

	def update_user(self, username=None, user=None):
		"""update user data"""
		if not user:
			user = self.get_user(username)
			if user is None:
				return False

		# merge data
		temp = self.default_user
		for key in temp:
			if key not in user:
				user[key] = temp[key]

	def server_signup(self, username, password):
		# check if username is already taken
		if self.get_user(username) is not None:
			return json.dumps({
				"status": "error",
				"message": "Username already taken"
			}, indent=0)

		# create user
		id = self.create_user(username, password)
		return json.dumps({
			"status": "success",
			"message": "User created",
			"user_name": username,
			"user_id": id
		}, indent=0)

	def server_login(self, username, password):
		user = self.get_user(username)
		if user is None:
			return json.dumps({
				"status": "error",
				"message": "User not found"
			}, indent=0)
		hash = hashlib.sha256((username+password).encode('utf-8'))
		if user["password"] != hash.hexdigest():
			return json.dumps({
				"status": "error",
				"message": "Wrong password"
			}, indent=0)

		user["last_active"] = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		print("logged in", user)
		# user.flags.clear() # clear flags

		return {
			"status": "success",
			"message": "User logged in",
			"user_name": username,
			"user_id": user["id"]
		}

	def get_user(self, username):
		if username in self.users:
			return self.users[username]
		try:
			user = User(username)
			self.users[username] = user
			return user
		except:
			return None

	def server_verify(self, username, id, return_user=False):
		user = self.get_user(username)
		if not user:
			return False
		if user.get("id") != id:
			return False

		user["last_active"] = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		# user.flags.clear() # clear flags on refresh
		self.update_user(username)

		if return_user:
			return user
		return True


	def collection(self, username, uid):
		# verify uid from users collection
		x = self.get_user(username)
		if not x: return None
		if x.get("id")!=uid: return None
		return x

	def get_skin_link(self, username, uid, retry=0):
		user = self.collection(username, uid)
		if not user:
			print("USER NOT FOUND")
			return None
		charecter = user["bot_charecter"]
		skin = user["bot_skin"]
		mode = user["skin_mode"]
		if user.get("skins") and user.get("c_skin_mode")==mode:
			return user.skins[skin]

		if mode == 0:
			return 0
		elif mode == 1:
			try:
				_skin = self.online_avatar.get_skin_link(charecter, skin)
				user.skins = self.online_avatar.get_skins(charecter)
				print("SKINS LOADED")
				user.c_skin_mode = mode
				return _skin
			except net_sys.NetErrors:
				traceback.print_exc()
				return None
			except Exception:
				traceback.print_exc()
				if retry: return None

				user["bot_charecter"] = self.default_user["bot_charecter"]
				user["bot_skin"] = self.default_user["bot_skin"]
				user["skin_mode"] = self.default_user["skin_mode"]

				self.get_skin_link(username, uid, 1)
		return 0
		
	def use_next_skin(self, username, uid):
		user = self.collection(username, uid)
		if not user:
			print("USER NOT FOUND")
			return None
		
		self.get_skin_link(username, uid) # init
		total_skins = len(user.skins)
		user.bot_skin = (user.bot_skin + 1)%total_skins
		
		_skin = str(user.bot_skin)
		
		return _skin

	def room_bg(self, username="", uid="", command=None, custom=None, user=None):
		if not user:
			user = self.collection(username, uid)
		if not user:
			print("USER NOT FOUND")
			return None

		if command=="change":
			user.room = (user.room+1)%len(CONSTANTS.room_bg)
			user.custom_room = None # clear custom room

		if command=="custom":
			if len(custom)>2000:
				return False
			user.custom_room = custom #set custom room bg

		if user.custom_room:
			return user.custom_room # if custom room enabled, then return it.

		room_id = user.room
		return CONSTANTS.room_bg[room_id]









	# def set_user_data(self, username, pointer):


user_handler = UserHandler()

# user = User("test")

if __name__ == "__main__":
	user_handler.create_user("test", "test")
	__user = User("test")
	print(__user.username)
	__user.x = 1 # set temporary data (not saved in file)
	__user['y'] = 2 # set permanent data (saved in file)
	print(__user.x)
	__user.y = 3 # change permanently (saved)
	__user.x = 4 # changed, but not saved in file
	print(__user)
	print(user_handler.get_skin_link("test", __user["id"]))

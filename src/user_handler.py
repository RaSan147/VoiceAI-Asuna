import os
import json
import hashlib
import time, datetime
import traceback
# import inspect
from collections import deque

from PRINT_TEXT3 import xprint

import F_sys
import net_sys
import TIME_sys

from CONFIG import appConfig
from DS import GETdict, Flag, NODict
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

	
	_default_user = {
		"username": "default",
		"password" : "default",
		"id": "default", # user token id (permanent)
		"created_at": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
		"last_active": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
		"pointer": 0, # current chat index (100 msg => 1 pointer)
		"nickname": "default", # current user name
		"bot": None, # user preferred bot name
		"ai_name": "Asuna", # user preferred ai name
		"ai_fullname": "Asuna Yuuki", # user preferred ai full name
		"bot_character": "Asuna", # user preferred ai avatar
		"bot_skin": 0,
		"skin_mode": 1, # 0 = offline, 1 = online
		"room": 0,
		"custom_room": None,
		"msg_id": 0,
		"pointer": 0,
	}


	__non_default_params = {
		"msg_id"         : int,            # current id of last message
		"chat"           : Flag            # cache chat data/intents
	}


	# FLAGS: if not found, returns None. DOESN'T STORE in DB
	__available_flags = { 
		"force_skin_link": str,           # to assign a forced skin link
		"cli"            : bool,          # enables COMMAND MODE, disables text parsing
		"parrot"         : bool,          # parrot mode, repeats user message
		"ask_yes"        : int,           # msg_id which asked for yes or no
		"on_yes"         : dict,          # MessageObj dict, to be sent on yes reply
		"on_no"          : dict,          # MessageObj dict, to be sent on no reply
	}




	def __init__(self, username=""):
		self.username = username
		self.user_path = os.path.join(appConfig.user_data_dir, username)
		self.file_path = os.path.join(self.user_path, '__init__.json')

		self.flags = Flag()
		self.chat = Flag() # dict to store session chat data (actual chats are stored separately in files)
		self.chat.intent = deque(maxlen=20) # last 20 intents
		self.os_time = 0.0 # in seconds
		self.os_time_offset = 0.0 # in seconds
		self.os_dt = datetime.datetime.now() #will be replaced on new msg
		# self.pointer = self.msg_id = 0

		# self.skins = {}
		self.loaded_skin = None
		self.skins = {} # cache skin links for a character


		# if the data asked for is already there
		data = F_sys.reader(self.file_path, on_missing=None)
		if not data:
			raise Exception("User not found")

		try:
			json_data = json.loads(data)
			#for key in json_data:
#				self[key] = json_data[key]
			self.update(json_data)
		except Exception as e:
			traceback.print_exc()
			raise Exception("User data corrupted") from e


	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		self.save()


	def __setattr__(self, key, value):
		if self(key):
			self.__setitem__(key, value)
		else:
			super().__setattr__(key, value)


	# def __getattribute__(self, __name: str):
	# 	return super().__getattribute__(__name)


	def save(self):
		"""Saves updated dict in users folder
		"""
		new = json.dumps(self, indent="\t", sort_keys=True)
		F_sys.writer("__init__.json", 'w', new, self.user_path)

	def get_chat(self, pointer=-1):
		if pointer == -1:
			pointer = self.pointer
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

	def add_chat(self, msg, mtime, user=1, parsed_msg="", rTo=-1, intent=(), context=()):
		"""
		msg: message sent
		mtime: time of message
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

		if user:
			user= "USER"
			# actual time on user side
			chat["uTime"] = str(self.get_user_dt())
		else:
			user= "BOT"

		mid = self.msg_id

		self.msg_id += 1 # starts from 0 => User, 1 => Bot, 2 => User, 3 => Bot, ...

		chat['id'] = mid
		chat['msg'] = msg # dict, contains msg, script and render mode
		chat['time'] = str(TIME_sys.utc_to_bd_time(mtime))
		chat["parsed_msg"] = parsed_msg
		chat['rTo'] = rTo
		chat['intent'] = "+".join(intent)
		chat['user'] = user

		old.append(chat)
		
		#print(old)

		J = json.dumps(old, indent="\t", separators=(',', ':'))
		F_sys.writer(pointer+'.json', 'w', J, self.user_path)

		return mid


	def get_user_dt(self):
		return TIME_sys.ts2dt(self.os_time, self.os_time_offset)
	
	def update_user_dt(self):
		self.os_dt = self.get_user_dt()


class UserHandler:
	def __init__(self) -> None:
		self.users = {} #username: User()

		self.online_avatar = live2d_sys.OnLine()

		self.default_user = User._default_user


	def u_path(self, username):
		"""returns user folder path"""
		return os.path.join(appConfig.user_data_dir, username)

	def create_user(self, username, password):
		_hash = hashlib.sha256((username+password).encode('utf-8'))
		_id = hashlib.sha1((str(time.time()) + username).encode("utf-8")).hexdigest()
		u_data = {
			"username": username,
			"password": _hash.hexdigest(),
			"created_at": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
			"last_active": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
			"pointer": 0, # current chat index (100 msg => 1 pointer)
			"nickname": username, # current user name
			"bot": None, # user preferred bot name
			"id": _id, #
			"ai_name": "Asuna", # user preferred ai name
			"ai_fullname": "Asuna Yuuki", # user preferred ai full name
			"bot_character": "Asuna", # user preferred ai avatar
			"bot_skin": 0,
			"skin_mode": 1, # 0 = offline, 1 = online
			"room": 0,
			"custom_room": None,
			"msg_id": 0,
		}

		new = json.dumps(u_data, indent=2)
		F_sys.writer("__init__.json", 'w', new, self.u_path(username))

		return _id

	def update_user(self, username=None, user:User=None):
		"""update user data"""
		if not user:
			user = self.get_user(username)
			if user is None:
				return False

		# merge data
		temp = self.default_user
		#for key in temp:
		#	if key not in user:
		#		user[key] = temp[key]
		temp = {**temp, **user}
		user.update(temp)
		
		return True

	def server_signup(self, username, password):
		# check if username is already taken
		if self.get_user(username, temp=True) is not None:
			return {
				"status": "error",
				"message": "Username already taken"
			}

		# create user
		uid = self.create_user(username, password)
		return {
			"status": "success",
			"message": "User created",
			"user_name": username,
			"user_id": uid
		}

	def server_login(self, username, password):
		user = self.get_user(username)
		if user is None:
			return {
				"status": "error",
				"message": "User not found"
			}
		_hash = hashlib.sha256((username+password).encode('utf-8'))
		if user["password"] != _hash.hexdigest():
			return {
				"status": "error",
				"message": "Wrong password"
			}

		user["last_active"] = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		print("logged in", user)
		# user.flags.clear() # clear flags

		return {
			"status": "success",
			"message": "User logged in",
			"user_name": username,
			"user_id": user["id"]
		}

	def get_user(self, username, temp=False) -> User:
		if username in self.users:
			return self.users[username]
		try:
			user = User(username)
			self.update_user(user=user)
			if not temp:
				self.users[username] = user
				self.get_skin_link(user=user)

			return user
		except:
			traceback.print_exc()
			return NODict()


	def server_verify(self, username, uid, return_user=False):
		user = self.collection(username, uid)
		if not user:
			return False

		user["last_active"] = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		# user.flags.clear() # clear flags on refresh
		self.update_user(username)

		if return_user:
			return user
		return True


	def collection(self, username:str, uid:str):
		# verify uid from users collection
		user = self.get_user(username)
		if not user:
			return False
		if user.id != uid:
			return False
		return user
	
	def set_force_skin(self, username, uid, skin_link):
		"""
		Set force skin link for user, so that it will be used instead of online skin
		"""
		user = self.collection(username, uid)
		if not user:
			print("USER NOT FOUND")
			return None
		user.force_skin_link = skin_link
		return True
	
	def reset_force_skin(self, username, uid):
		"""
		Reset force skin link for user, so that online skin will be used
		"""
		user = self.collection(username, uid)
		if not user:
			print("USER NOT FOUND")
			return None
		user.force_skin_link = None
		return True

	def get_skin_link(self, username="", uid="", user=None ,retry=0):

		user = user if user else self.collection(username, uid)
		if not user:
			print("USER NOT FOUND")
			return None
		
		if user.get("force_skin_link"): # for test purpose
			return user.force_skin_link
		
		character = user.get("bot_character") or user.get("bot_charecter") # typo
		skin = user["bot_skin"]
		mode = user["skin_mode"]
		
		print(user.get("skins") , user.get("c_skin_mode"),mode , user.loaded_skin , skin)

		if user.get("skins") and user.get("c_skin_mode")==mode and user.loaded_skin == skin:
			# if skins are already loaded
			return user.skins[skin]

		if mode == 0:
			xprint("/y/OFFLINE MODE NOT SUPPORTED YET/=/")
			return 0
		elif mode == 1: # online mode
			try:
				_skin = self.online_avatar.get_skin_link(character, skin) # get skin links from server, can be cached
				user.skins = self.online_avatar.get_skins(character) # get all skins, is cached for reuse mentioned above
				print("SKINS LOADED")
				user.c_skin_mode = mode # offline/online mode
				user.loaded_skin = skin # skin variant
				return _skin # return skin link
			except net_sys.NetErrors:
				traceback.print_exc()
				return None
			except Exception:
				traceback.print_exc()
				if retry: #already retried
					return None

				# if things go wrong, use default skin and retry
				user["bot_character"] = self.default_user["bot_character"]
				user["bot_skin"] = self.default_user["bot_skin"]
				user["skin_mode"] = self.default_user["skin_mode"]

				# retry
				self.get_skin_link(username, uid, retry=1)
		return 0

	def use_next_skin(self, username, uid):
		user = self.collection(username, uid)
		if not user:
			print("USER NOT FOUND")
			return None

		self.get_skin_link(username, uid) # init
		total_skins = len(user.skins)
		print("....current skin", user.bot_skin)
		print("....total skin ", total_skins)
		user.bot_skin = (user.bot_skin + 1)%(total_skins)
		print("sent skin", user.bot_skin)

		_skin = str(user.bot_skin)

		return _skin

	def room_bg(self, username="", uid="", command="", custom="", user:User=None):
		if not user:
			_user = self.collection(username, uid)
			if not _user:
				print("USER NOT FOUND")
				return None
			user =  _user

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
	_user = User("test")
	print(_user.username)
	_user.x = 1 # set temporary data (not saved in file)
	_user['y'] = 2 # set permanent data (saved in file)
	print(_user.x)
	_user.y = 3 # change permanently (saved)
	_user.x = 4 # changed, but not saved in file
	print(_user)
	print(user_handler.get_skin_link("test", _user["id"]))

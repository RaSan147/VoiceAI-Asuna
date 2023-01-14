import os
import json
import hashlib
import time, datetime
import traceback


import F_sys

from CONFIG import appConfig
from DS import GETdict, Flag

#############################################
#                USERS HANDLER              #
#############################################



class User(GETdict):
	"""can get and set user data like a js object"""
	def __init__(self, username):
		self.username = username
		self.user_path = os.path.join(appConfig.data_dir, username)
		self.file_path = os.path.join(self.user_path, '__init__.json')

		self.flags = Flag()

		# if the data asked for is already there
		if os.path.exists(self.file_path):
			with open(self.file_path, 'r') as f:
				data = json.load(f)
				for key in data:
					self[key] = data[key]

		
		else:
			raise Exception("User not found")
	
	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		self.save()

	# def __getattribute__(self, __name: str):
	# 	return super().__getattribute__(__name)
	
	def save(self):
		J = json.dumps(self)
		F_sys.writer("__init__.json", 'w', J, self.user_path)

	def get_chat(self, pointer):
		file_path = os.path.join(self.user_path, pointer+'.json')

		# if the data asked for is already there
		if os.path.exists(file_path):
			with open(file_path, 'r') as f:
				return json.load(f)

		return None

	def set_chat(self, pointer, data):
		file_path = os.path.join(self.user_path, pointer+'.json')
		J = json.dumps(data)
		F_sys.writer(pointer+'.json', 'w', J, self.user_path)

# user = User("test")


class UserHandler:
	def __init__(self) -> None:
		self.users = {}

	def u_path(self, username):
		return os.path.join(appConfig.data_dir, username)

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
			"last_login": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
			"pointer": 0, # current chat index (100 msg => 1 pointer)
			"nickname": username, # current user name
			"bot": None, # user preferred bot name
			"id": id, #
			"ai_name": "Alice", # user preferred ai name
		}

		J = json.dumps(u_data)
		F_sys.writer("__init__.json", 'w', J, self.u_path(username))

		return id
	
	def server_signup(self, username, password):
		# check if username is already taken
		if self.get_user(username) is not None:
			return json.dumps({
				"status": "error",
				"message": "Username already taken"
			})
		
		# create user
		id = self.create_user(username, password)
		return json.dumps({
			"status": "success",
			"message": "User created",
			"user_name": username,
			"user_id": id
		})
	
	def server_login(self, username, password):
		hash = hashlib.sha256((username+password).encode('utf-8'))
		user = self.get_user(username)
		if user is None:
			return json.dumps({
				"status": "error",
				"message": "User not found"
			})
		if user["password"] != hash.hexdigest():
			return json.dumps({
				"status": "error",
				"message": "Wrong password"
			})
		
		return json.dumps({
			"status": "success",
			"message": "User logged in",
			"user_name": username,
			"user_id": user["id"]
		})
	
	def get_user(self, username):
		try:
			user = User(username)
			return user
		except:
			return None
	
	def server_verify(self, username, id, return_user=False):
		user = self.get_user(username)
		if not user:
			return False
		if user.get("id") != id:
			return False
		if return_user:
			return user
		return True
	
	
	def collection(self, username, uid=None, temp=False):
		if uid not in self.users: # if user is not in memory
			verified_user = self.server_verify(username, uid, return_user=True)
			if not verified_user:
				return None
			if not temp or uid is not None:
				self.users[uid] = User(username)
		return self.users[uid]

	


		
	# def set_user_data(self, username, pointer):
		

user_handler = UserHandler()

# user = User("test")

# if __name__ == "__main__":
# 	user_handler.create_user("test", "test")
# 	user = User("test")
# 	print(user.username)
# 	user.x = 1 # set temporary data
# 	user['y'] = 2 # set permanent data
# 	print(user.x)
# 	print(user)

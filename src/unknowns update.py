from Chat_raw2 import user_handler, basic_output, TIME_sys, xprint, time

# MAKE A TEST USER
user_handler.server_signup("TEST", "TEST")

# ACCESS THE USER
user = user_handler.get_user("TEST")
# user = user_handler.collection(user.username, user.id)
# print(user.skins)
# user_handler.get_skin_link(user.username, user.id)

user.user_client_time_offset = TIME_sys.get_time_offset()

def run(inp):
	user.user_client_time = time()
	tt = time()
	msg = basic_output(inp, user)
	print(f"\tRESP time: {time()-tt}s")
	if not msg:
		return
	msg = msg["message"]
	if msg == "exit":
		return
	xprint("/ih/>>/=/", msg)


with open("./Asuna_data/server/unknown query (upto 26-apr-2023).txt", "r") as f:
	for line in f.readlines():
		try:
			line = line.strip()
			if not line:
				continue
			try:
				line = eval(line)[1]
			except:
				line = eval(line)[0]
		except:
			xprint("/r/FAILED TO EVALUATE >>", line, "/=/")
			continue
		print(">>", line)
		run(line)

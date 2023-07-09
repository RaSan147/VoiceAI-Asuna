import emoji
import asyncio
from hashlib import sha1

import os

import edge_tts


from F_sys import writer

TEXT = "Hello World! ʕ •ᴥ•ʔ	I am Aria Kazuto discovers that 300 SAO players, including Asuna, remain trapped in their NerveGear. As he goes to the hospital to see Asuna, he meets Asuna's father Shouzou Yuuki who is asked by an associate of his, Nobuyuki Sugou, to make a decision, which Sugou later reveals to be his marriage with Asuna, angering Kazuto."
VOICE = "en-US-AriaNeural"
# VOICE = "en-SG-LunaNeural"

def remove_emoji(text):
	return emoji.replace_emoji(text, "")

async def _main(TEXT, VOICE, OUTPUT_FILE) -> None:
	communicate = edge_tts.Communicate(TEXT, VOICE)#, output_type="riff-48khz-16bit-mono-pcm")

	

	# os.makedirs(OUTPUT_DIR, exist_ok=True)

	await communicate.save(OUTPUT_FILE)
	# with open(OUTPUT_FILE, "wb") as file:
	# 	async for chunk in communicate.stream():
	# 		if chunk["type"] == "audio":
	# 			file.write(chunk["data"])
	# 		elif chunk["type"] == "WordBoundary":
	# 			if print_sub:
	# 				# print(f"WordBoundary: {chunk}")

def get_audio(text, voice=VOICE, output_dir='./'):
	text = remove_emoji(text)
	hashed = sha1()
	hashed.update((text+voice).encode())
	hashed_text = hashed.hexdigest()
	
	
	f_name = os.path.join(output_dir, f"{hashed_text}.mp3")
	
	if os.path.isfile(f_name):
		return f_name
	
	writer(f"init.txt", "w", "", direc=output_dir)
	
	loop = asyncio.get_event_loop_policy().set_event_loop(asyncio.new_event_loop())
	loop = asyncio.get_event_loop_policy().get_event_loop()
	try:
		loop.run_until_complete(_main(text, voice, f_name))
	finally:
		loop.close()

	return f_name



if __name__ == "__main__":
	OUTPUT_DIR = "Asuna_data/temp/audio/"

	# VOICE = 'en-GB-SoniaNeural'
	print(get_audio(TEXT, VOICE))
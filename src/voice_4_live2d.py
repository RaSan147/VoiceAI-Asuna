import emoji
import asyncio
from hashlib import sha1

import os

import edge_tts


TEXT = "Hello World! ʕ •ᴥ•ʔ	I am Aria Kazuto discovers that 300 SAO players, including Asuna, remain trapped in their NerveGear. As he goes to the hospital to see Asuna, he meets Asuna's father Shouzou Yuuki who is asked by an associate of his, Nobuyuki Sugou, to make a decision, which Sugou later reveals to be his marriage with Asuna, angering Kazuto."
VOICE = "en-US-AriaNeural"
VOICE = "en-SG-LunaNeural"

def remove_emoji(text):
	return emoji.replace_emoji(text, "")

async def _main(TEXT, VOICE, OUTPUT_FILE, print_sub=False) -> None:
	communicate = edge_tts.Communicate(TEXT, VOICE)#, output_type="riff-48khz-16bit-mono-pcm")

	

	# os.makedirs(OUTPUT_DIR, exist_ok=True)


	with open(OUTPUT_FILE, "wb") as file:
		async for chunk in communicate.stream():
			if chunk["type"] == "audio":
				file.write(chunk["data"])
			elif chunk["type"] == "WordBoundary":
				if print_sub:
					print(f"WordBoundary: {chunk}")

def get_audio(text, voice=VOICE, output_dir='./'):
	text = remove_emoji(TEXT)
	hashed = sha1()
	hashed.update(text.encode())
	hashed_text = hashed.hexdigest()

	f_name = os.path.join(OUTPUT_DIR, f"{hashed_text}.mp3")

	asyncio.get_event_loop().run_until_complete(_main(text, voice, f_name, True))
	asyncio.get_event_loop().close()




	return f_name


if __name__ == "__main__":
	OUTPUT_DIR = "Asuna_data/temp/audio/"

	# VOICE = 'en-GB-SoniaNeural'
	print(get_audio(TEXT, VOICE))
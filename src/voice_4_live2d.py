import emoji
import asyncio
from hashlib import sha1

import edge_tts

TEXT = "Hello World! ʕ •ᴥ•ʔ	I am Aria"
VOICE = "en-US-AriaNeural"

def remove_emoji(text):
	return emoji.replace_emoji(text, "")

async def _main(TEXT, VOICE, OUTPUT_FILE, print_sub=False) -> None:
	communicate = edge_tts.Communicate(TEXT, VOICE)

	with open(OUTPUT_FILE, "wb") as file:
		async for chunk in communicate.stream():
			if chunk["type"] == "audio":
				file.write(chunk["data"])
			elif chunk["type"] == "WordBoundary":
				if print_sub:
					print(f"WordBoundary: {chunk}")

def get_audio(text, voice=VOICE):
	text = remove_emoji(TEXT)
	hashed = sha1()
	hashed.update(text.encode())
	hashed_text = hashed.hexdigest()

	f_name = f"audio/{hashed_text}.mp3"

	asyncio.get_event_loop().run_until_complete(_main(text, voice, f_name, True))
	asyncio.get_event_loop().close()

	return f_name


if __name__ == "__main__":
	# VOICE = 'en-GB-SoniaNeural'
	print(get_audio(TEXT, VOICE))
from queue import Queue
from time import sleep
import re
import sys
from shutil import get_terminal_size
from math import ceil


# if os is windows import console_mod
import platform
if platform.system() == "Windows":
	from console_mod import enable_color2
	enable_color2() # enable color on windows cmd terminal




wait_time = 0.0


def null_func(*a):
	return a[0]


class XprintClass:
	def __init__(self) -> None:

		# self.text = ""

		self.normal_tx = "0"
		self.ul_tx = "4"
		self.neg_tx = "7"
		self.bold_tx = "1"

		self.ash_c = "30"
		self.red_c = "31"
		self.green_c = "32"
		self.yello_c = "33"
		self.blue_c = "34"
		self.pink_c = "35"
		self.cayan_c = "36"
		self.white_c = "37"

		self.normal_b = "40"
		self.red_b = "41"
		self.green_b = "42"
		self.yello_b = "43"
		self.blue_b = "44"
		self.pink_b = "45"
		self.cayan_b = "46"
		self.white_b = "47"
		self.black_b = "48"

		self.custom_type_codes = ['/u/', '/a/', '/y/', '/g/',
								  '/k/', '/b/', '/r/', '/h/', '/bu/', '/hu/', '/=/']

		self.re = {  # regex for custom type codes
			'markup': re.compile(r'/<(.*)?>/'),
			'/u/': re.compile(r'==(.*?)=='),
			'/hu/': re.compile(r'===(.*?)==='),
		}

		self.no_code = False
		self.no_colors = False

	def __getattr__(self, name):
		if name == "default_style":
			return {
				"color": '',
				"bg": '',
				"style": []
			}
		else:
			return self.__dict__[name]

	def make_str(self, *text, sep: str = " ", end: str = "\n", highlighter=False) -> str:
		text = str(sep).join(map(str, text)) + str(end)
		text = self.tnt_helper(text, highlighter)
		return text

	def text_styling_markup(self, text: str) -> str:  # not in use
		''' for custom text stypling like html
		print(tnt_helper('/<style= col: red>/ 69'))'''
		if '/<' not in text:
			return text

		a = self.re['markup'].search(text)
		while a:
			style = a.group(1)
			# do stuff with style
			text = text.replace(a.group(0), '')
			a = self.re['markup'].search(text)

		return text

	def tnt_helper(self, text, highlighter):
		''' i) custom_type_codes are used for custom commands to
		simplify the code
		ii) other text modifications are made here and passes optimized
		text for the typing and speaking engine respectively'''

		if highlighter:

			text = self.re["/hu/"].sub(r"/hu/\1/=/", text)
			text = self.re["/u/"].sub(r"/u/\1/=/", text)

		text = self.text_styling_markup(text)

		return text

	def slowtype(self, *text, sep=' ', wait_time=wait_time, end='\n', highlighter=False, auto_resetting=True, run_at_start=None, parsed=False):
		"""main typing engine that prints inputted text
				slowly based on waiting time

				text: text to be printed
				sep: separator between each text args
				wait_time: time to wait between each character
				end: end of line character
				highlighter: if True, will highlight text using ===.*=== -> /hu/ and ==.*== -> /u/
				auto_resetting: if True, will reset the no_code and no_color after each output
				"""
		self.custom_style = self.default_style.copy()
		if parsed:
			# print([text])
			text = text[0]
		else:
			text = self.make_str(*text, sep=sep, end=end,
								 highlighter=highlighter)
		if run_at_start:
			text = run_at_start(text)
		self.wait_time = float(wait_time)
		# self.end=str(end)

		self.custom_style_temp = self.custom_style.copy()

		# custom_type_codes = ['/u/', '/a/', '/y/', '/g/', '/k/', '/b/', '/r/', '/h/', '/bu/', '/hu/', '/=/']
		i = 0
		text_len = len(text)

		has_code = False

		while i < text_len:

			### MUST CLOSE THESE NO COLOR AND NO CODE TAGS ###

			if text[i:i+3] == '/~`':
				self.no_code = True
				i += 3
				continue

			if text[i:i+3] == '`~/':
				self.no_code = False
				i += 3
				continue

			if text[i:i+3] == '/~~':
				self.no_colors = True
				i += 3
				continue

			if text[i:i+3] == '~~/':
				self.no_colors = False
				i += 3
				continue

			if self.no_code == False:
				if text[i] == '/' and '/' in text[i+2:i+5]:
					if self.no_colors == False and text[i+1] in ('a', 'r', 'g', 'y', 'b', 'p', 'c', 'w', '=', 'u', 'i', 'h', '_'):
						x = text[i+1]
						if x == 'a':
							self.custom_style_temp["color"] = self.ash_c
						elif x == 'r':
							self.custom_style_temp["color"] = self.red_c
						elif x == 'g':
							self.custom_style_temp["color"] = self.green_c
						elif x == 'y':
							self.custom_style_temp["color"] = self.yello_c
						elif x == 'b':
							self.custom_style_temp["color"] = self.blue_c
						elif x == 'p':
							self.custom_style_temp["color"] = self.pink_c
						elif x == 'c':
							self.custom_style_temp["color"] = self.cayan_c
						elif x == 'w':
							self.custom_style_temp["color"] = self.white_c
						elif x == '=':
							sys.stdout.write('\033[0m')
							sys.stdout.flush()
							self.custom_style_temp = self.default_style.copy()
						elif x == 'u':
							self.custom_style_temp["style"].append(self.ul_tx)
						elif x == 'i':
							self.custom_style_temp["style"].append(self.neg_tx)
						elif x == 'h':
							self.custom_style_temp["style"].append(self.bold_tx)

						if text[i+2] == '/':
							has_code = True
							i += 2
						elif text[i+2] in ('k', 'r', 'g', 'y', 'b', 'p', 'c', 'w', 'u', 'i', 'h', '_'):
							x = text[i+2]
							if x == 'k':
								self.custom_style_temp["bg"] = self.normal_b
							elif x == 'r':
								self.custom_style_temp["bg"] = self.red_b
							elif x == 'g':
								self.custom_style_temp["bg"] = self.green_b
							elif x == 'y':
								self.custom_style_temp["bg"] = self.yello_b
							elif x == 'b':
								self.custom_style_temp["bg"] = self.blue_b
							elif x == 'p':
								self.custom_style_temp["bg"] = self.pink_b
							elif x == 'c':
								self.custom_style_temp["bg"] = self.cayan_b
							elif x == 'w':
								self.custom_style_temp["bg"] = self.white_b
							elif x == 'u':
								self.custom_style_temp["style"].append(self.ul_tx)
							elif x == 'i':
								self.custom_style_temp["style"].append(
									self.neg_tx)
							elif x == 'h':
								self.custom_style_temp["style"].append(self.bold_tx)

							if text[i+3] == '/':
								has_code = True
								i += 3
							elif text[i+3] in ('u', 'i', 'h'):
								x = text[i+3]
								if x == 'u':
									self.custom_style_temp["style"].append(self.ul_tx)
								elif x == 'i':
									self.custom_style_temp["style"].append(self.neg_tx)
								elif x == 'h':
									self.custom_style_temp["style"].append(self.bold_tx)

								if text[i+4] == '/':
									has_code = True
									i += 4

					elif text[i+1] == 's':

						sys.stdout.flush()
						try:
							if text[i+3] == '/':
								sleep(float(text[i+2]))
								i += 4
							elif text[i+4] == '/':
								sleep(float(text[i+2:i+4]))
								i += 5
							elif text[i+5] == '/':
								sleep(float(text[i+2:i+5]))
								i += 6
							continue
						except:
							pass
			if has_code == True:
				has_code = False
				self.custom_style = self.custom_style_temp.copy()

				# print(self.custom_style)

				style = '\033['

				for s in ("color", "bg"):
					if self.custom_style[s]:
						style += self.custom_style[s] + ";"

				if self.custom_style["style"]:
					style += ";".join(self.custom_style["style"])
				else:
					style = style[:-1]

				style += "m"
				sys.stdout.write(style)
				# sys.stdout.flush()

			else:
				sys.stdout.write(text[i])
				if wait_time != 0:
					sys.stdout.flush()
					sleep(self.wait_time)
			i += 1
			# print(has_code, slept)

		# sys.stdout.write(self.end)
		sys.stdout.flush()

		if auto_resetting:
			self.reset()

	def reset(self):
		self.no_colors = self.no_code = False

	def remove_style(self, text, highlighter=False):
		"""text: must be parsed string (sep, end are parsed)"""

		self.tnt_helper(text, highlighter)
		text = re.sub(r"/s\d*[.]?\d*/", "", text)
		return re.sub(r"/[argybpcw \=uih_]+/", "", text)


class oneLine(XprintClass):
	__all__ = ["new", "update", "_update"]

	def __init__(self):
		super().__init__()
		self.old_len = None

		self.queue = Queue()
		self.BUSY = False

	def get_len(self, string: str):
		# loop to read each line
		lens = []
		for line in string.split('\n'):
			l = len(line)
			if l == 0:
				l = 1  # empty line
			lens.append(l)

		# print(lens, "\n\n")

		return lens

	def get_ceil(self, i):
		size = int(get_terminal_size()[0])
		return ceil(i/size)

	def next(self):
		# return self.queue.get()
		if self.queue.empty() or self.BUSY:
			return None

		self.BUSY = True
		text, wait_time, auto_resetting, out_func = self.queue.get()

		if self.old_len is not None:

			to_del = sum(map(self.get_ceil, self.old_len))-1

			# print(to_del)
			sys.stdout.write("\033[2K\033[1G" + ('\x1b[1A\x1b[2K'*to_del))
			# sys.stdout.write('\x1b[K' + ('\x1b[1A\x1b[2K'*to_del))

			# )#
			# sys.stdout.flush()
			# print("boom\n")

		if out_func == "slowtype":
			self.old_len = self.get_len(self.remove_style(text))
			self.slowtype(text, wait_time=wait_time,
						  auto_resetting=auto_resetting, parsed=True)
		if out_func == "print":
			self.old_len = self.get_len(text)
			sys.stdout.write(text)
			sys.stdout.flush()
		self.BUSY = False

		if not self.queue.empty():
			return True

	def update(self, *text, sep=' ', wait_time=wait_time, end='\n', highlighter=False, auto_resetting=True, run_at_start=null_func):
		""" Uses xprint and parse string"""
		text = self.make_str(*text, sep=sep, end=end, highlighter=highlighter)
		text = run_at_start(text)
		self.queue.put((text, wait_time, auto_resetting, "slowtype"))
		while self.next() is True:
			pass

	def _update(self, *text, sep=' ', wait_time=wait_time, end='\n', run_at_start=null_func):
		""" Uses print and does not parse string"""
		text = run_at_start(text)
		text = str(sep).join(map(str, text)) + str(end)

		self.queue.put((text, wait_time, False, "print"))
		self.next()

	def new(self):
		self.__init__()


# x= """Traceback (most recent call last):
#   File "g:/Ratul/C_coding/Python/Web Leach/Web-leach/Web-leach_CLI/v7/print_text3.py", line 352, in <module>
#     oneline.update([i for i in range(i)])
#   File "g:/Ratul/C_coding/Python/Web Leach/Web-leach/Web-leach_CLI/v7/print_text3.py", line 340, in update
#     self.next()
#   File "g:/Ratul/C_coding/Python/Web Leach/Web-leach/Web-leach_CLI/v7/print_text3.py", line 321, in next
#     sleep(.1)
# KeyboardInterrupt"""

# print(x.splitlines())

XprintEngine = XprintClass()
xprint = XprintEngine.slowtype
remove_style = XprintEngine.remove_style


if __name__ == '__main__':
	print("test")

	def xx(t):
		# print([t], "\n")
		return t

	oneline = oneLine()

	l = [i for i in range(50)] + [i for i in range(101)[::-1]]
	for i in l:
		# oneline.update([i for i in range(i)])
		oneline._update(i, end="", run_at_start=xx)
		sleep(.02)
		
	print("\n\nTesting multiline")
		
	loads = [
"""\t\\
\t \\
\t  \\
""",
'''\t |
\t |
\t |
''',
"""\t  /
\t /
\t/
""",
"""
\t————

"""
]
	oneline = oneLine()
	for i in range(50):
		oneline._update(loads[i%len(loads)])
		sleep(.2)

	xprint("/rhu/hello/=/ q to quit")

	x = ''

	while x != 'q':
		x = input()
		xprint(x, highlighter=True)

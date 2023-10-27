import sys
from ctypes import POINTER, WinDLL, Structure, sizeof, byref
from ctypes.wintypes import BOOL, SHORT, WCHAR, UINT, ULONG, DWORD, HANDLE
import ctypes

LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11


class COORD(Structure):
	_fields_ = [
		("X", SHORT),
		("Y", SHORT),
	]


class CONSOLE_FONT_INFOEX(Structure):
	_fields_ = [
		("cbSize", ULONG),
		("nFont", DWORD),
		("dwFontSize", COORD),
		("FontFamily", UINT),
		("FontWeight", UINT),
		("FaceName", WCHAR * LF_FACESIZE)
	]


kernel32_dll = WinDLL("kernel32.dll")

get_last_error_func = kernel32_dll.GetLastError
get_last_error_func.argtypes = []
get_last_error_func.restype = DWORD

get_std_handle_func = kernel32_dll.GetStdHandle
get_std_handle_func.argtypes = [DWORD]
get_std_handle_func.restype = HANDLE

get_current_console_font_ex_func = kernel32_dll.GetCurrentConsoleFontEx
get_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
get_current_console_font_ex_func.restype = BOOL

set_current_console_font_ex_func = kernel32_dll.SetCurrentConsoleFontEx
set_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
set_current_console_font_ex_func.restype = BOOL


def main():
	# Get stdout handle
	stdout = get_std_handle_func(STD_OUTPUT_HANDLE)
	if not stdout:
		print("{:s} error: {:d}".format(get_std_handle_func.__name__, get_last_error_func()))
		return
	# Get current font characteristics
	font = CONSOLE_FONT_INFOEX()
	font.cbSize = sizeof(CONSOLE_FONT_INFOEX)
	res = get_current_console_font_ex_func(stdout, False, byref(font))
	if not res:
		print("{:s} error: {:d}".format(get_current_console_font_ex_func.__name__, get_last_error_func()))
		return
	# Display font information
	print("Console information for {:}".format(font))
	for field_name, _ in font._fields_:
		field_data = getattr(font, field_name)
		if field_name == "dwFontSize":
			print("    {:s}: {{X: {:d}, Y: {:d}}}".format(field_name, field_data.X, field_data.Y))
		else:
			print("    {:s}: {:}".format(field_name, field_data))
	while 1:
		try:
			height = int(input("\nEnter font height (invalid to exit): "))
		except:
			break
		# Alter font height
		font.dwFontSize.X = 10  # Changing X has no effect (at least on my machine)
		font.dwFontSize.Y = height
		# Apply changes
		res = set_current_console_font_ex_func(stdout, False, byref(font))
		if not res:
			print("{:s} error: {:d}".format(set_current_console_font_ex_func.__name__, get_last_error_func()))
			return
		print("OMG! The window changed :)")
		# Get current font characteristics again and display font size
		res = get_current_console_font_ex_func(stdout, False, byref(font))
		if not res:
			print("{:s} error: {:d}".format(get_current_console_font_ex_func.__name__, get_last_error_func()))
			return
		print("\nNew sizes    X: {:d}, Y: {:d}".format(font.dwFontSize.X, font.dwFontSize.Y))


def set_width(y=14):
	stdout = get_std_handle_func(STD_OUTPUT_HANDLE)
	font = CONSOLE_FONT_INFOEX()
	font.cbSize = sizeof(CONSOLE_FONT_INFOEX)
	# font.dwFontSize.X = 10  # Changing X has no effect (at least on my machine)
	font.dwFontSize.Y = y #height
	res = set_current_console_font_ex_func(stdout, False, byref(font))


def enable_color():
	"""
	Enables colored output in the console on Windows systems.  (via https://stackoverflow.com/a/36760881/9209949)
	"""
	kernel32 = ctypes.windll.kernel32
	kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
	
def enable_color2():
	"""
	Enables ANSI color codes in the Windows console. [preferred method]

	This function uses the Windows API to enable ANSI color codes in the console.
	"""
	kernel32 = ctypes.WinDLL('kernel32')
	hStdOut = kernel32.GetStdHandle(-11)
	mode = ctypes.c_ulong()
	kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
	mode.value |= 4
	kernel32.SetConsoleMode(hStdOut, mode)

if __name__ == "__main__":
	print("Python {:s} on {:s}\n".format(sys.version, sys.platform))
	# main()
	stdout = get_std_handle_func(STD_OUTPUT_HANDLE)
	font = CONSOLE_FONT_INFOEX()
	font.cbSize = sizeof(CONSOLE_FONT_INFOEX)
	# font.dwFontSize.X = 10  # Changing X has no effect (at least on my machine)
	font.dwFontSize.Y = 16 #height
	res = set_current_console_font_ex_func(stdout, False, byref(font))
	res = get_current_console_font_ex_func(stdout, False, byref(font))
	if not res:
		print("{:s} error: {:d}".format(get_current_console_font_ex_func.__name__, get_last_error_func()))
		exit(1)
	print("\nNew sizes    X: {:d}, Y: {:d}".format(font.dwFontSize.X, font.dwFontSize.Y))
	input()
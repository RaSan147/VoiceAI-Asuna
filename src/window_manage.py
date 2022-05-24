import win32gui, win32con, ctypes,time



commands={
"forcemin":11,
"hide":0,
"maximize":3,
"minimize":6,
"restore":9,
"show":5,

}



class Window_Manager:
	def control(self, window, todo):
		toplist = []
		winlist = []
		def enum_callback(hwnd, results):
			winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

		win32gui.EnumWindows(enum_callback, toplist)

		window_code = [(hwnd, title) for hwnd, title in winlist if window in title.lower()][0]
		#notepad_handle = ctypes.windll.user32.FindWindowW(u"Notepad", None)
		#time.sleep()
		ctypes.windll.user32.ShowWindow(int(window_code[0]), commands[todo])

def enum_callback(hwnd, results):
	winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
while __name__=='__main__':
	toplist = []
	winlist = []
	
	window= input('Enter the window name: ')
	win32gui.EnumWindows(enum_callback, toplist)
	window_code = [(hwnd, title) for hwnd, title in winlist if window in title.lower()]
	print(window_code)
	if window_code!=[]:
		window_code=window_code[0]
		print(window_code[1],' found!')
		todo= input('Enter the window task: ')
		if todo!='pass':
			for i in window_code:
				ctypes.windll.user32.ShowWindow(int(i), commands[todo])


documentation= """
SW_FORCEMINIMIZE
11
Minimizes a window, even if the thread that owns the window is not responding. This flag should only be used when minimizing windows from a different thread.

SW_HIDE
0
Hides the window and activates another window.

SW_MAXIMIZE
3
Maximizes the specified window.

SW_MINIMIZE
6
Minimizes the specified window and activates the next top-level window in the Z order.

SW_RESTORE
9
Activates and displays the window. If the window is minimized or maximized, the system restores it to its original size and position. An application should specify this flag when restoring a minimized window.

SW_SHOW
5
Activates the window and displays it in its current size and position.

SW_SHOWDEFAULT
10
Sets the show state based on the SW_ value specified in the STARTUPINFO structure passed to the CreateProcess function by the program that started the application.

SW_SHOWMAXIMIZED
3
Activates the window and displays it as a maximized window.

SW_SHOWMINIMIZED
2
Activates the window and displays it as a minimized window.

SW_SHOWMINNOACTIVE
7
Displays the window as a minimized window. This value is similar to SW_SHOWMINIMIZED, except the window is not activated.

SW_SHOWNA
8
Displays the window in its current size and position. This value is similar to SW_SHOW, except that the window is not activated.

SW_SHOWNOACTIVATE
4
Displays a window in its most recent size and position. This value is similar to SW_SHOWNORMAL, except that the window is not activated.

SW_SHOWNORMAL
1
Activates and displays a window. If the window is minimized or maximized, the system restores it to its original size and position. An application should specify this flag when displaying the window for the first time.

Return value
Type: BOOL

If the window was previously visible, the return value is nonzero.

If the window was previously hidden, the return value is zero.

link: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow?redirectedfrom=MSDN
"""

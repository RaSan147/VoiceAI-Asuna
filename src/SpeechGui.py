# A simple speech recognition program for Windows
# When speech is recognized, Python macros are executed.

# This requires:
#   That the wxPython library is installed (obtain from http://www.wxpython.org/)
#   That the MS Speech API 5 is installed (obtain from http://microsoft.com/speech/)
#   That MakePy has been run on the MS Speech API (in PythonWin, select Tools |
#       COM MakePy Utility | Microsoft Speech Object Library 5.1)

# Copyright (C) 2001 Inigo Surguy, inigosurguy@hotmail.com

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#    or download it from http://www.gnu.org/licenses/gpl.txt

from wxPython.wx import *
import sys, time, math, string, win32com.client,win32event,pythoncom
from win32com.client import constants
import win32con
import cPickle, zlib

import string
import pickle
import win32api
import win32com.client
import traceback

# Handy methods that make the code included inside the macro area simpler
speaker = win32com.client.Dispatch("SAPI.SpVoice")
"""Say the text via the MS Speech API"""
def say(text):
    speaker.Speak(text)

shell = win32com.client.Dispatch("WScript.Shell")
"""Use the Windows Scripting Host sendKeys function to send keystrokes to the
    currently focused application. See help on the Microsoft site for values
    that represent special keys: common ones I use are %{TAB} for Alt-Tab, and
    {PGDN} and {PGUP} for page down and up, and %{F4} for Alt-F4."""
def sendKeys(keystrokes):
    shell.SendKeys(keystrokes)

"""Launch a command via the Windows Scripting Host"""    
def start(command):
    shell.Run(command)

"""Launch Internet Explorer, and navigate to a given URL"""
def browseTo(location):
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible = 1
    ie.Navigate(location)

"""Display a message box with the given message and title"""
def message(message, title="Message"):
    dlg = wxMessageDialog(app.frame, message, title, wxOK | wxICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()

# Taken from wxPython demo - generated with wxPython\demo\encode_bitmaps.py
"""Get the Mondrian picture (from the wxPython demo) that's used as an application
    icon"""
def getMondrianData():
    return cPickle.loads(zlib.decompress(
    'x\332\323\310)0\344\012V76R\000"3\005Cu\256\304`u\005\205d\005\247\234\304\
\344l0/\002\310Sv\003\0030?\037\3047\000\002(_\017"\017\022\001\363\265!\362\
NnP\276?L?\224\257@\000@\024\351\201\201B\004v0"\024\021\025NP\035X\014\311\
\007\202!\251\210(\337!\205\323\250"\222\024a\001\230\212\374\221\200\2026\
\010\014\013E\204\263\224\036\000\277\004Z\355' ))

def getMondrianBitmap():
    return wxBitmapFromXPMData(getMondrianData())

def getMondrianImage():
    return wxImageFromBitmap(getMondrianBitmap())

"""The event handler for speech events"""
class ContextEvents(win32com.client.getevents("SAPI.SpSharedRecoContext")):
    def OnRecognition(self, StreamNumber, StreamPosition, RecognitionType, Result):
        newResult = win32com.client.Dispatch(Result)
        try:
            # Exec the appropriate listbox entry
            exec app.items[newResult.PhraseInfo.GetText()]
        except:
            # If execution fails, display a messagebox with error and cause
            etype, value, tb = sys.exc_info()
            message = (str(etype)+":"+str(value)+
                      "\nat line "+`tb.tb_next.tb_lineno`+
                      "for text '"+newResult.PhraseInfo.GetText()+"'")
            dlg = wxMessageDialog(app.frame, 
                                  message,
                                  'Exception: '+str(etype),
                                  wxOK | wxICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

"""Windows speech recognition application""" 
class MyApp(wxApp):
    ADD_BUTTON_ID = 10
    DELETE_BUTTON_ID = 20
    LISTBOX_ID = 30
    EDITOR_ID = 40
    TEST_BUTTON_ID = 50
    TURNON_BUTTON_ID = 60 
    TURNOFF_BUTTON_ID = 70
    SAVE_FILENAME = "save.p"
    def setItems(self):
        try:
            self.items = pickle.load(open(self.SAVE_FILENAME))
        except IOError:
            self.items = {"Hello" : "print 'Hello'" , "Goodbye" : "print 'Goodbye'" }
    def InitSpeech(self):
        listener = win32com.client.Dispatch("SAPI.SpSharedRecognizer")
        self.context = listener.CreateRecoContext()
        self.grammar = self.context.CreateGrammar()
        self.grammar.DictationSetState(0)
        self.ListItemsRule = self.grammar.Rules.Add("ListItemsRule", constants.SRATopLevel + constants.SRADynamic, 0)
        events = ContextEvents(self.context)
        self.turnedOn = true        
        self.SetWords()
    def SetWords(self):
        self.ListItemsRule.Clear()
        if self.turnedOn:
            print "Setting words - turned on"
            [ self.ListItemsRule.InitialState.AddWordTransition(None, word) for word in self.items.keys() ]
        else:
            print "Setting words - OFF"
            self.ListItemsRule.InitialState.AddWordTransition(None, "Turn on")
        self.grammar.Rules.Commit()
        self.grammar.CmdSetRuleState("ListItemsRule", 1)
        self.grammar.Rules.Commit()
    def SetUpTaskbar(self):
        # setup a taskbar icon, and catch some events from it
        self.tbicon = wxTaskBarIcon()
        icon = wxIconFromXPMData(getMondrianData())        
        self.tbicon.SetIcon(icon, "Speech recognition")
        EVT_TASKBAR_LEFT_DCLICK(self.tbicon, self.OnTaskBarActivate)
        EVT_TASKBAR_RIGHT_UP(self.tbicon, self.OnTaskBarMenu)
        EVT_MENU(self.tbicon, self.TBMENU_RESTORE, self.OnTaskBarActivate)
        EVT_MENU(self.tbicon, self.TBMENU_CLOSE, self.OnTaskBarClose)
    def OnInit(self):
        self.setItems()
        self.InitSpeech()

        self.frame = wxFrame(NULL, -1, "Speech tester", wxPoint(10,10), wxSize(770,300))
        self.listBox = wxListBox(self.frame, self.LISTBOX_ID, wxPoint(10, 10), wxSize(120, 200),
                       self.items.keys(), wxLB_SINGLE)
        self.addButton = wxButton(self.frame, self.ADD_BUTTON_ID, "Add", wxPoint(10,230), wxSize(50, 30))
        self.deleteButton = wxButton(self.frame, self.DELETE_BUTTON_ID, "Delete", wxPoint(80, 230), wxSize(50, 30))
        self.editor = wxTextCtrl(self.frame, self.EDITOR_ID, "", wxPoint(140,10), wxSize(600,200),
                                style=wxSUNKEN_BORDER+wxTE_MULTILINE+wxTE_PROCESS_TAB)
        self.testButton = wxButton(self.frame, self.TEST_BUTTON_ID, "Test", wxPoint(140, 230), wxSize(50, 30))

        self.turnonButton = wxButton(self.frame, self.TURNON_BUTTON_ID, "On", wxPoint(210, 230), wxSize(50, 30))
        self.turnoffButton = wxButton(self.frame, self.TURNOFF_BUTTON_ID, "Off", wxPoint(280, 230), wxSize(50, 30))

        self.SetUpTaskbar()        

        EVT_LISTBOX(self, self.LISTBOX_ID, self.OnListBoxSelect)        
        EVT_BUTTON(self, self.ADD_BUTTON_ID, self.OnAddClick)
        EVT_BUTTON(self, self.DELETE_BUTTON_ID, self.OnDeleteClick)
        EVT_BUTTON(self, self.TEST_BUTTON_ID, self.OnTestClick)
        EVT_BUTTON(self, self.TURNON_BUTTON_ID, self.OnTurnOnClick)
        EVT_BUTTON(self, self.TURNOFF_BUTTON_ID, self.OnTurnOffClick)
        EVT_TEXT(self, self.EDITOR_ID, self.OnTextEntered)

        EVT_ICONIZE(self.frame, self.OnIconize)
        EVT_CLOSE(self.frame, self.OnExitFrame)

        self.listBox.SetSelection(0)
        self.displayTextBox()
        
        self.frame.Show(true)
        self.SetTopWindow(self.frame)
        return true
    def OnExitFrame(self, event):
        pickle.dump(self.items, open(self.SAVE_FILENAME, 'w'))
        if hasattr(self, "tbicon"):
            del self.tbicon
        self.frame.Destroy()
    def OnIconize(self, event):
        self.frame.Show(false)

    def OnAddClick(self,event):
        dlg = wxTextEntryDialog(self.frame, 'Text to recognize', "New item")
        if dlg.ShowModal() == wxID_OK:
            self.items[dlg.GetValue()] = ""
            self.resetItemsList()
            self.listBox.SetStringSelection(dlg.GetValue())
            self.displayTextBox()
            self.SetWords()
        dlg.Destroy()
    def OnDeleteClick(self,event):
        del self.items[ self.listBox.GetStringSelection() ]
        self.resetItemsList()
        self.listBox.SetSelection(0)
        self.displayTextBox()
        self.SetWords()
    def OnListBoxSelect(self,event):
        self.displayTextBox()
    def OnTestClick(self, event):
        self.executeItemInList(self.listBox.GetStringSelection())
    def OnTextEntered(self, event):
        self.items[self.listBox.GetStringSelection()] = event.GetString()

    #---------------------------------------------
    # This is code to use the system tray taken from the wxPython demo
        
    TBMENU_RESTORE = 1000
    TBMENU_CLOSE   = 1001
        
    def OnTaskBarActivate(self, evt):
        if self.frame.IsIconized():
            self.frame.Iconize(false)
        if not self.frame.IsShown():
            self.frame.Show(true)
        self.frame.Raise()

    def OnTaskBarMenu(self, evt):
        menu = wxMenu()
        menu.Append(self.TBMENU_RESTORE, "Restore wxPython Demo")
        menu.Append(self.TBMENU_CLOSE,   "Close")
        self.tbicon.PopupMenu(menu)
        menu.Destroy()

    def OnTaskBarClose(self, evt):
        self.frame.Close()
        # because of the way wxTaskBarIcon.PopupMenu is implemented we have to
        # prod the main idle handler a bit to get the window to actually close
        wxGetApp().ProcessIdle()

    #---------------------------------------------        

    def displayTextBox(self):
        self.editor.SetValue( self.items[self.listBox.GetStringSelection()] )        
    def executeItemInList(self,itemName):
        codeToExecute = self.items[itemName]
        try:
            exec codeToExecute
        except:
            etype, value, tb = sys.exc_info()
            message = (str(etype)+":"+str(value)+
                      "\nat line "+`tb.tb_next.tb_lineno`)
            dlg = wxMessageDialog(self.frame, message,
                                  'Exception: '+str(etype),
                                  wxOK | wxICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()        
    def resetItemsList(self):
        self.listBox.Set(self.items.keys())

    def OnTurnOnClick(self, event):
        self.turnOn()
    def OnTurnOffClick(self, event):
        self.turnOff()
        
    def turnOn(self):
        if not self.turnedOn:
            self.turnedOn = true            
            self.SetWords()
    def turnOff(self):
        if (self.turnedOn):
            self.turnedOn = false
            self.SetWords()

app = MyApp(0)


app.MainLoop()



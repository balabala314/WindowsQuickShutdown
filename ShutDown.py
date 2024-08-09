# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import wx, wx.adv, time, ctypes, winreg
def getDPI():
    HKCU = winreg.HKEY_CURRENT_USER
    src = r"Control Panel\Desktop\WindowMetrics"
    value = "AppliedDPI"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, src)  # 只读
        if key:
            a = winreg.QueryValueEx(key, value)
            winreg.CloseKey(key)
    except FileNotFoundError:
        return 1
    return a[0]/96
OPERATION = None
TIME = 0
try :
    DPI = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
except :
    DPI = getDPI()
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    ctypes.windll.user32.SetProcessDPIAware()
class ShutdownFrame(wx.Frame) :
    def __init__(self,parent = None, ID = wx.ID_ANY, title : str = "Quick Shutdown & Restart App") :
        global DPI
        wx.Frame.__init__(self, parent, ID, size = (round(300 * DPI),round(160 * DPI)), title = title)
        self.Bind(wx.EVT_CLOSE, self.Close)
        self.SetWindowStyleFlag(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX) | wx.STAY_ON_TOP)
        try :
            icon = wx.Icon('power.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon)
        except :
            pass
        panel = wx.Panel(self, )
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.TimeSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.LabelFont = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Microsoft YaHei")
        self.LabelText = wx.StaticText(panel, label = "Quick to Shutdown", style = wx.ALIGN_CENTRE_HORIZONTAL)
        self.LabelText.SetFont(self.LabelFont)

        self.ButtonShut = wx.Button(panel, wx.ID_ANY, label = "&Shutdown")
        self.Bind(wx.EVT_BUTTON, self.Shutdown, self.ButtonShut)
        self.ButtonRest = wx.Button(panel, wx.ID_ANY, label = "&Restart")
        self.Bind(wx.EVT_BUTTON, self.Restart, self.ButtonRest)
        self.ButtonQuit = wx.Button(panel, wx.ID_EXIT, label = "&Quit")
        self.Bind(wx.EVT_BUTTON, self.Close, self.ButtonQuit)

        self.TimeChoose = wx.CheckBox(panel, label="Set Time :")
        self.Bind(wx.EVT_CHECKBOX, self.CheckBoxHandle, self.TimeChoose)
        self.TimePicker = wx.adv.TimePickerCtrl(panel)
        self.TimePicker.Enable(False)
        self.TimePicker.SetTime(0,0,0)

        self.MainSizer.Add(self.LabelText, 3, wx.ALL|wx.EXPAND, round(5 * DPI))
        self.ButtonSizer.Add(self.ButtonShut, 1, wx.ALL|wx.EXPAND, round(5 * DPI))
        self.ButtonSizer.Add(self.ButtonRest, 1, wx.ALL|wx.EXPAND, round(5 * DPI))
        self.ButtonSizer.Add(self.ButtonQuit, 1, wx.ALL|wx.EXPAND, round(5 * DPI))

        self.TimeSizer.Add(self.TimeChoose, 1,wx.ALL|wx.EXPAND, round(5 * DPI))
        self.TimeSizer.Add(self.TimePicker, 1,wx.ALL|wx.EXPAND, round(5 * DPI))

        self.MainSizer.Add(self.ButtonSizer, 2, wx.ALL|wx.EXPAND, round(5 * DPI))
        self.MainSizer.Add(self.TimeSizer, 2, wx.ALL|wx.EXPAND)
        panel.SetSizer(self.MainSizer)
    def Shutdown(self, event) :
        global OPERATION, TIME
        OPERATION = "shutdown"
        if self.TimeChoose.IsChecked() :
            TIME = self.TimePicker.GetTime()[0] * 3600 + self.TimePicker.GetTime()[1] * 60 + self.TimePicker.GetTime()[2]
        self.Close(True)
    def Restart(self, event) :
        global OPERATION, TIME
        OPERATION = "restart"
        if self.TimeChoose.IsChecked() :
            TIME = self.TimePicker.GetTime()[0] * 3600 + self.TimePicker.GetTime()[1] * 60 + self.TimePicker.GetTime()[2]
        self.Close(True)
    def CheckBoxHandle(self, event) :
        self.TimePicker.Enable(self.TimeChoose.IsChecked())
    def Close(self, force = True) :
        self.Show(False)
        self.Destroy()
def main() :
    app = wx.App(False)
    SDFrame = ShutdownFrame()
    SDFrame.Show(True)
    app.MainLoop()
    time.sleep(TIME)
    if OPERATION :
        key = 5
        if OPERATION == "shutdown" : key = 6
        s = ctypes.create_string_buffer(4)
        ctypes.windll.ntdll.RtlAdjustPrivilege(19,1,0,s)
        ctypes.windll.ntdll.NtInitiatePowerAction(key,6,0,1)

if __name__ == "__main__" :
    main()

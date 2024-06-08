import wx, wx.adv, time, ctypes
OPERATION = None
TIME = 0
class ShutdownFrame(wx.Frame) :
    def __init__(self,parent = None, ID = wx.ID_ANY, title : str = "Quick Shutdown & Restart App") :
        wx.Frame.__init__(self, parent, ID, size = (300,160),title = title)
        self.SetWindowStyleFlag(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        
        panel = wx.Panel(self, )
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.TimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.LabelFont = wx.Font(18, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.BOLD)
        self.LabelText = wx.StaticText(panel, label = "Quick to Shutdown", style = wx.ALIGN_CENTRE_HORIZONTAL)
        self.LabelText.SetFont(self.LabelFont)
        
        self.ButtonShut = wx.Button(panel, wx.ID_ANY, label = "&Shutdown")
        self.Bind(wx.EVT_BUTTON, self.Shutdown, self.ButtonShut)
        self.ButtonRest = wx.Button(panel, wx.ID_ANY, label = "&Restart")
        self.Bind(wx.EVT_BUTTON, self.Restart, self.ButtonRest)
        self.ButtonQuit = wx.Button(panel, wx.ID_EXIT, label = "&Quit")
        self.Bind(wx.EVT_BUTTON, self.Quit, self.ButtonQuit)
        
        self.TimeChoose = wx.CheckBox(panel, label="Set Time :")
        self.Bind(wx.EVT_CHECKBOX, self.CheckBoxHandle, self.TimeChoose)
        self.TimePicker = wx.adv.TimePickerCtrl(panel)
        self.TimePicker.Enable(False)
        self.TimePicker.SetTime(0,0,0)
        
        self.MainSizer.Add(self.LabelText, 3, wx.ALL|wx.EXPAND, 5)
        self.ButtonSizer.Add(self.ButtonShut, 1, wx.ALL|wx.EXPAND, 5)
        self.ButtonSizer.Add(self.ButtonRest, 1, wx.ALL|wx.EXPAND, 5)
        self.ButtonSizer.Add(self.ButtonQuit, 1, wx.ALL|wx.EXPAND, 5)
        
        self.TimeSizer.Add(self.TimeChoose, 1,wx.ALL|wx.EXPAND, 5)
        self.TimeSizer.Add(self.TimePicker, 1,wx.ALL|wx.EXPAND, 5)
        
        self.MainSizer.Add(self.ButtonSizer, 2, wx.ALL|wx.EXPAND, 5)
        self.MainSizer.Add(self.TimeSizer, 2, wx.ALL|wx.EXPAND)
        panel.SetSizer(self.MainSizer)
    def Shutdown(self, event) :
        global OPERATION, TIME
        print("Shutdown!!", event)
        OPERATION = "shutdown"
        if self.TimeChoose.IsChecked() :
            TIME = self.TimePicker.GetTime()[0] * 3600 + self.TimePicker.GetTime()[1] * 60 + self.TimePicker.GetTime()[2]
        self.Close(True)
    def Restart(self, event) :
        global OPERATION, TIME
        print("Restart!!", event)
        OPERATION = "restart"
        if self.TimeChoose.IsChecked() :
            TIME = self.TimePicker.GetTime()[0] * 3600 + self.TimePicker.GetTime()[1] * 60 + self.TimePicker.GetTime()[2]
        self.Close(True)
    def Quit(self, event) :
        global OPERATION, TIME
        self.Close(True)
    def CheckBoxHandle(self, event) :
        print("CheckBox Event :", self.TimeChoose.IsChecked())
        self.TimePicker.Enable(self.TimeChoose.IsChecked())
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

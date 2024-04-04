from ctypes import create_string_buffer,windll,c_void_p, c_wchar_p, c_wchar_p, c_uint,c_int
try :
    windll.shcore.SetProcessDpiAwareness(1)
except :
    pass
def shut(num):
    s = create_string_buffer(4)
    windll.ntdll.RtlAdjustPrivilege(19,1,0,s)
    if num != 5:
        windll.ntdll.NtInitiatePowerAction(9-num,6,0,1)
def show_message_box(title, message, style=34):
    MessageBoxW = windll.user32.MessageBoxW
    MessageBoxW.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_uint]
    MessageBoxW.restype = c_int
    return MessageBoxW(None, message, title, style)
res = show_message_box('Quick Shutdown', '终止以关机，重试以重启，忽略以退出')
shut(res)
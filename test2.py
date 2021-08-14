import win32api
import win32con
import time


input('132321')
time.sleep(1)

win32api.keybd_event(0x0D, 0, 0, 0)
win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)
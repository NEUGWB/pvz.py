# -*- coding: utf-8 -*- 
'''
作者: lmintlcx
日期: 2017-9-29 20:30
---
按键控制示范代码, 需要安装pyHook3k
'''
 
import pythoncom, pyHook, sys, threading, pvz
from pvz import *

pvz.scene = 'PE'

def AJ():
    hm = pyHook.HookManager()
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()

def onKeyboardEvent(event):
    print ("KeyID:", event.KeyID)
    if (event.KeyID == 49):
        pass
    return True


def main():

    print('nowopen %s' % win32gui.GetWindowText(hwnd))
    print('mainthread going')
    sleep(1)

    aj = threading.Thread(target=AJ, name='AJThread')
    aj.setDaemon(True)
    aj.start()

    while True:
        sleep(1)
        print("test")

if __name__ == "__main__":
    main()

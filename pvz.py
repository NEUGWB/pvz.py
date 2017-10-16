# -*- coding: utf-8 -*-
'''
File Name: pvz.py
Description: a python module contains some method of game "Plants Vs Zombies"
Author: no_doudle
Date: 2017-2-24 20:00
Modified By: lmintlcx
Modified Date: 2017-9-24 22:00
'''

import win32api, win32con, win32gui, win32process, ctypes, threading
from time import sleep

x, y = win32api.GetCursorPos()
hwnd = win32gui.WindowFromPoint((x, y))
nowPao = 0
countMemAddress = -1
zombNumMemAddress = -1
Screenx = 800
Screeny = 600
scene = 'PE'

PROCESS_ALL_ACCESS  =  ( 0x000F0000 | 0x00100000 | 0xFFF )
tid,pid = win32process.GetWindowThreadProcessId(hwnd)
PROCESS = win32api.OpenProcess(PROCESS_ALL_ACCESS, 0, pid)
rPM = ctypes.WinDLL('kernel32', use_last_error=True).ReadProcessMemory
buffer = ctypes.create_string_buffer(4)
bytes_read = ctypes.c_size_t()

#植物大战僵尸版本，0原版，1年度版
PVZ_VER = 1
address_list = { "WaveCountDown" :  [[0x6a9ec0, 0x768, 0x559c], [0x729670, 0x868, 0x55B4]],
            "RedWordCountDown" :    [[0x6a9ec0, 0x768, 0x55a4], [0x729670, 0x868, 0x55bc]],
           "RedWordCountDown2" :    [[0x6a9ec0, 0x768, 0x140,0x88],[0x729670,0x868,0x158,0x88]],
           "FinishedWaveNum" :      [[0x6A9EC0, 0x768, 0x557c],[0x729670,0x868,0x5594]],
            "InterfaceState" :      [[0x6A9EC0, 0x7fc],[0x729670, 0x91c]],
                 "WordKind" :       [[0x6a9ec0, 0x768, 0x140,0x8c],[0x729670,0x868,0x158,0x8c]],
                 "WordShow" :       [[0x6a9ec0, 0x768, 0x140,0x4],[0x729670,0x868,0x158,0x4]],}

def ReadMemory(address):
    global PROCESS, buffer
    rPM(PROCESS.handle, address, buffer, 4, ctypes.byref(bytes_read))
    ret = 0x0
    cnt = len(buffer.value) -1
    while cnt >= 0:
        ret *= 256
        ret += buffer.value[cnt]
        cnt -= 1
    return ret

def MemReader(addr):
    mem = -1
    def Reader():
        nonlocal mem
        if  mem == -1:
            mem = addr[0]
            for i in range(1, len(addr)):
                mem = ReadMemory(mem)
                mem = mem + addr[i]
            for i in range(0, len(addr)-1):
                mem
        return ReadMemory(mem)
    return Reader

def MUP(x, y, right = False):
    global Screenx,Screeny
    x *= (Screenx/800)
    y *= (Screeny/600)
    x = int(x)
    y = int(y)
    if(right):
        win32api.SendMessage(hwnd, win32con.WM_RBUTTONUP, win32con.NULL, y*65536+x)
    else:
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.NULL, y*65536+x)
    
def MDOWN(x, y, right = False):
    global Screenx,Screeny
    x *= (Screenx/800)
    y *= (Screeny/600)
    x = int(x)
    y = int(y)
    if(right):
        win32api.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.NULL, y*65536+x)
    else:
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.NULL, y*65536+x)

def Click(x, y, right = False):
    if(right):
        MDOWN(x, y, True)
        MUP(x, y, True)
    else:
        MDOWN(x, y)
        MUP(x, y)

def MoveClick(x, y, right = False):
    x_0, y_0 = win32gui.GetCursorPos()
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    border_width = (right - left - 800) / 2
    title_bar_height = bottom - top - border_width - 600
    x_1, y_1 = left + border_width + x, top + title_bar_height + y
    x_1, y_1 = int(x_1), int(y_1)
    win32api.SetCursorPos((x_1, y_1))
    sleep(0.02)
    Click(x, y, right)
    sleep(0.01)
    win32api.SetCursorPos((x_0, y_0))

def SafeClick():
    Click(60, 50, True)

WaveCountdown       = MemReader(address_list["WaveCountDown"][PVZ_VER])
FinishedWaveNum     = MemReader(address_list["FinishedWaveNum"][PVZ_VER])
RedWordCountDown    = MemReader(address_list["RedWordCountDown"][PVZ_VER])
InterfaceState      = MemReader(address_list["InterfaceState"][PVZ_VER])
WordKind            = MemReader(address_list["WordKind"][PVZ_VER])
WordShow            = MemReader(address_list["WordShow"][PVZ_VER])

def Countdown():
    countdown = WaveCountdown()
    while countdown == 0 :
        countdown = WaveCountdown()
        sleep(0.005)
    return countdown
'''
def ZombNum():
    global zombNumMemAddress
    if zombNumMemAddress < 0 :
        zombNumMemAddress = ReadMemory(0x729670) + 0x868
        zombNumMemAddress = ReadMemory(zombNumMemAddress) + 0xB8
    return ReadMemory(zombNumMemAddress) 
'''

def ChooseCard(row, column, imitater = False):
    if(imitater):
        MoveClick(490, 550)
        sleep(0.2)
        x = 190 + 50/2 + (column - 1) * 51
        y = 125 + 70/2 + (row - 1) * 71
    else:
        x = 22 + 50/2 + (column - 1) * 53
        y = 123 + 70/2 + (row - 1) * 70
    Click(x, y)
    sleep(0.2)

def LetsRock():
    sleep(0.2)
    MDOWN(234, 567)
    sleep(0.1)
    MUP(234, 567)

def Card(num):
    Click(50 + 51 * num, 42)

def Pnt(pnt):
    global scene
    row = pnt[0]
    column = pnt[1]
    if (scene == 'DE') or (scene == 'NE'):
        Click(80 * column, 30 + 100 * row)
    elif (scene == 'PE') or (scene == 'FE'):
        Click(80 * column, 30 + 85 * row)
    elif (scene == 'RE') or (scene == 'ME'):
        if (column > 5):
            Click(80 * column, 85 * row)
        else:
            Click(80 * column, 85 * row + (120 - 20 * column))

def preJudge(t, hugewave = False):
    if(hugewave == False):
        while(Countdown() > t):
            sleep(0.01)
    else:
        while(Countdown() > 4):
            sleep(0.01)
            
        #sleep((724-t)/100)
        delay = 200
        #while(RedWordCountDown() != 0 and RedWordCountDown() + delay > t):
        while True:
            rwcd = RedWordCountDown()
            if(rwcd > 0 and rwcd < 700):
                break
        print("RedwordCount", rwcd, WordKind())
        sleep((rwcd + 4 - t)/100)

def Pao(row, column):
    global nowPao, paoList
    print("Pao", paoList[nowPao], row, column)
    for i in range(10):
        Pnt(paoList[nowPao])
    #sleep(0.1)
    Pnt((row, column))
    SafeClick()
    nowPao = (1+nowPao)%len(paoList)
    
def wave20():
    preJudge(150, True)
    Pao(4,7)
    sleep(0.9)
    Pao(2,9)
    Pao(2,9)
    Pao(5,9)
    Pao(5,9)
    sleep(1.08)
    Pao(1,9)
    Pao(2,9)
    Pao(5,9)
    Pao(5,9)

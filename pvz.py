# -*- coding: utf-8 -*-
'''
File Name: pvz.py
Description: a python module contains some method of game "Plants Vs Zombies"
Author: no_doudle
Date: 2017-2-24 20:00
Modified By: lmintlcx
Modified Date: 2017-9-24 22:00
'''

import win32api, win32con, win32gui, win32process, ctypes, threading, win32ui, traceback
import time, os, shutil
from time import sleep
from PIL import Image

hwnd = win32gui.WindowFromPoint(win32api.GetCursorPos())
nowPao = 0
Screenx = 800
Screeny = 600
scene = 'PE'

opRLock = threading.RLock() #操作锁，可递归，防止多线程操作冲突

PROCESS_ALL_ACCESS  =  ( 0x000F0000 | 0x00100000 | 0xFFF )
tid,pid = win32process.GetWindowThreadProcessId(hwnd)
PROCESS = win32api.OpenProcess(PROCESS_ALL_ACCESS, 0, pid)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
saveFile = r"C:\ProgramData\PopCap Games\PlantsVsZombies\userdata\game1_13.dat"

#植物大战僵尸版本，0原版，1年度版
PVZ_VER = 1
address_list = { "WaveCountDown" :  [[0x6a9ec0, 0x768, 0x559c], [0x729670, 0x868, 0x55B4]], #波刷新倒计时
            "RedWordCountDown" :    [[0x6a9ec0, 0x768, 0x55a4], [0x729670, 0x868, 0x55bc]], #红字结束倒计时
           "RedWordCountDown2" :    [[0x6a9ec0, 0x768, 0x140,0x88],[0x729670,0x868,0x158,0x88]], #也是红字结束倒计时，跟上面那个效果似乎一样
           "FinishedWaveNum" :      [[0x6A9EC0, 0x768, 0x557c],[0x729670,0x868,0x5594]], #已出现波数
            "InterfaceState" :      [[0x6A9EC0, 0x7fc],[0x729670, 0x91c]], #界面状态，2选卡，3游戏，4僵尸进屋
                "WordKind" :       [[0x6a9ec0, 0x768, 0x140,0x8c],[0x729670,0x868,0x158,0x8c]], #字的类型，12是白字，比较有效的判断白字出现的方法
                "WordShow" :       [[0x6a9ec0, 0x768, 0x140,0x4],[0x729670,0x868,0x158,0x4]], #字显示的值，字符串类型
                "PlantNum" :       [[0x6A9EC0, 0x768, 0xbc],[0x729670,0x868,0xd4]], #植物数量
                "MouseState" :     [[0x6A9EC0, 0x768, 0x138, 0x30],[0x729670,0x868,0x150, 0x30]],} #鼠标状态
                
protectAddress = {}
def MyVirtualProtect(addr):
    OldProtect = ctypes.c_uint()
    if addr not in protectAddress:
        kernel32.VirtualProtect(addr, 4, 0x40, ctypes.byref(OldProtect))
        protectAddress[addr] = OldProtect


def ReadMemory(address):
    buffer = ctypes.create_string_buffer(4)
    bytes_read = ctypes.c_size_t()
    
    opRLock.acquire()
    MyVirtualProtect(address)
    suc = kernel32.ReadProcessMemory(PROCESS.handle, address, buffer, 4, ctypes.byref(bytes_read))
    opRLock.release()
    if suc == 0:
        print("Read Mem Error", win32api.GetLastError(), address)
        #traceback.print_stack() 
        return 0

    ret = 0x0
    cnt = len(buffer.value) -1
    while cnt >= 0:
        ret *= 256
        ret += buffer.value[cnt]
        cnt -= 1
        
    return ret
#一个比较通用的读内存方法
def MemReader(addr):
    mem = -1
    def Reader(reset = False):
        nonlocal mem
        if reset or mem == -1:
            mem = addr[0]
            for i in range(1, len(addr)):
                mem = ReadMemory(mem)
                mem = mem + addr[i]
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
    opRLock.acquire()
    if(right):
        MDOWN(x, y, True)
        MUP(x, y, True)
    else:
        MDOWN(x, y)
        MUP(x, y)
    opRLock.release()

def EnsureClick(x, y, right = False):
    opRLock.acquire()
    sleep(0.05)
    if(right):
        MDOWN(x, y, True)
        sleep(0.02)
        MUP(x, y, True)
    else:
        MDOWN(x, y)
        sleep(0.02)
        MUP(x, y)
    sleep(0.01)
    opRLock.release()


def MoveClick(x, y, right = False):
    opRLock.acquire()
    x_0, y_0 = win32gui.GetCursorPos()
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    border_width = (right - left - 800) / 2
    title_bar_height = bottom - top - border_width - 600
    x_1, y_1 = left + border_width + x, top + title_bar_height + y
    x_1, y_1 = int(x_1), int(y_1)
    win32api.SetCursorPos((x_1, y_1))
    sleep(0.15)
    Click(x,y)
    sleep(0.01)
    win32api.SetCursorPos((x_0, y_0))
    opRLock.release()

def SafeClick():
    opRLock.acquire()
    Click(60, 50, True)
    opRLock.release()

WaveCountdown       = MemReader(address_list["WaveCountDown"][PVZ_VER])
FinishedWaveNum     = MemReader(address_list["FinishedWaveNum"][PVZ_VER])
RedWordCountDown    = MemReader(address_list["RedWordCountDown"][PVZ_VER])
InterfaceState      = MemReader(address_list["InterfaceState"][PVZ_VER])
WordKind            = MemReader(address_list["WordKind"][PVZ_VER])
WordShow            = MemReader(address_list["WordShow"][PVZ_VER])
PlantNum            = MemReader(address_list["PlantNum"][PVZ_VER])
MouseState          = MemReader(address_list["MouseState"][PVZ_VER])

def WriteMemory(address, b):
    MyVirtualProtect(address)

    print("write mem", ctypes.sizeof(b), b.raw)
    bytes_write = ctypes.c_size_t()
    kernel32.WriteProcessMemory(PROCESS.handle, address, b, ctypes.sizeof(b), ctypes.byref(bytes_write))
    print(bytes_write.value)
    print(win32api.GetLastError())
    if bytes_write.value > 0:
        print("write success")
    else:
        print("write fail", address)
        
#年度版后台
#WriteMemory(0x4536b0,ctypes.create_string_buffer(bytes.fromhex('c20400')))
def NoPause():
    if PVZ_VER == 1:
        WriteMemory(0x4536b0,ctypes.create_string_buffer(bytes.fromhex('c20400')))
def TimeStamp():
    tm = time.time()
    ms = int((tm - int(tm) + 0.0005)*1000)
    if ms < 0:
        ms = 0
    stamp = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(tm))
    stamp = stamp + "." + str(ms)
    return stamp
    
def SafeDelete(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        else:
            print("delete nonexistent file", path)
    except:
        print("delete file error", path)
    
def SafeCopy(src, dst):
    try:
        if os.path.isfile(src):
            shutil.copy (src, dst)
        else:
            print("copy nonexistent file", src)
    except:
        print("copy file error", src, "->", dst)

#用队列的方式备份存档，只备份最近若干个
backupList = []
def BackUp(path):
    datname = TimeStamp() + '.dat'
    datname = path + datname
    SafeCopy(saveFile, datname)
    print("copy success")
    backupList.append(datname)
    if len(backupList) > 3:
        SafeDelete(backupList[0])
        del(backupList[0])

#取色
def GetColor(x, y):
    hwndDC = win32gui.GetDC(hwnd)  
    ret = win32gui.GetPixel(hwndDC, x, y)
    win32gui.ReleaseDC(hwnd, hwndDC)
    return ret

#截图
screenList = []
def ScreenShot(dpath): 
    hwndDC = win32gui.GetDC(hwnd)
    memDc = win32gui.CreateCompatibleDC(hwndDC)
    hBmp   = win32gui.CreateCompatibleBitmap(hwndDC, 800, 600)
    oldBmp = win32gui.SelectObject(memDc, hBmp)

    #win32gui.BitBlt(memDc,0,0,800,600,hwndDC,0,0,win32con.SRCCOPY);
    ctypes.windll.user32.PrintWindow(hwnd, memDc, 1)
    
    filename = TimeStamp()
    bmpname = dpath + filename + '.bmp'

    saveBitMap = win32ui.CreateBitmapFromHandle(hBmp)
    saveDC = win32ui.CreateDCFromHandle(memDc)
    saveBitMap.SaveBitmapFile(saveDC, bmpname)

    win32gui.SelectObject(memDc, oldBmp)
    win32gui.DeleteObject(memDc)
    win32gui.DeleteObject(hBmp)
    win32gui.ReleaseDC(hwnd, hwndDC)
    
    jpgname = bmpname[:-4]+".jpg"
    Image.open(bmpname).save(jpgname)
    SafeDelete(bmpname)
    
    screenList.append(jpgname)
    if len(screenList) > 300:
        SafeDelete(screenList[0])
        del(screenList[0])

def ChooseCard(row, column, imitater = False):
    opRLock.acquire()
    if(imitater):
        MoveClick(490, 550)
        sleep(0.2)
        x = 190 + 50/2 + (column - 1) * 51
        y = 125 + 70/2 + (row - 1) * 71
    else:
        x = 22 + 50/2 + (column - 1) * 53
        y = 123 + 70/2 + (row - 1) * 70
    Click(x, y)
    sleep(0.05)
    opRLock.release()

def LetsRock():
    opRLock.acquire()
    EnsureClick(234, 567)
    opRLock.release()

def Card(num):
    opRLock.acquire()
    Click(50 + 51 * num, 42)
    opRLock.release()

def Pnt(pnt):
    opRLock.acquire()
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
    opRLock.release()
            
#使用物品，返回1表示没拿到物品，返回2表示没放下物品，0表示成功
def UseCard(card, r, c):
    opRLock.acquire()
    ret = 0
    Card(card)
    if MouseState() != 1:
        ret = 1
    Pnt((r, c))
    if MouseState() == 1:
        ret = 2
    SafeClick()
    opRLock.release()
    return ret
    
def WaitWaveCountDown(pre):
    tmbegin = time.time()
    while True:
        if 0 < WaveCountdown() <= pre:
            break
        else:
            sleep(0.005)
            if time.time() - tmbegin > 20:# 20秒没发炮肯定是哪出问题了
                print("preJudge timeout!!!")
                exit()
            
def preJudge(t, hugewave = False):
    if(hugewave == False):
        WaitWaveCountDown(t)
    else:
        WaitWaveCountDown(4)
        while True:
            rwcd = RedWordCountDown()
            if(rwcd > 0 and rwcd < 700):
                break
        print("RedwordCount", rwcd, WordKind())
        sleep((rwcd + 4 - t)/100)

def Pao(row, column):
    opRLock.acquire()
    global paoList, nowPao
    pntcount = 0
    while True:
        pntcount += 1
        if pntcount > 500:
            print("No Pao ???")
            exit()
        pntPao = paoList[nowPao]
        if abs(pntPao[0]-row) + abs(pntPao[1]-column) < 2:
            if abs(pntPao[0]-row) + abs(pntPao[1]+1-column) >= 2:
                pntPao = (pntPao[0],pntPao[1]+1)
            else:
                nowPao = (1+nowPao)%len(paoList)
                continue
        for i in range(5):
            Pnt(pntPao)
        sleep(0.01)
        nowPao = (1+nowPao)%len(paoList)
        mst = MouseState()
        if mst != 8:
            SafeClick()
        else:
            break

    #print("Pao", paoList[nowPao - 1], row, column, "pntcount", pntcount)
    Pnt((row, column))
    SafeClick()
    opRLock.release()
    
collectBlock = [ (1,2),(1,3),(1,4),(2,2),(2,3),(2,4)
            ,   (5,2),(5,3),(5,4),(6,2),(6,3),(6,4)
            ,   (1,9),(2,9),(3,9),(4,9),(5,9),(6,9)
            ,   (1,1),(2,1),(5,1),(6,1),(1,8),(2,8),(5,8),(6,8),(6,9)]

def Collector():
    nowCollect = 0
    def _Collect():
        nonlocal nowCollect
        block = collectBlock[nowCollect]
        nowCollect = (nowCollect + 1) % len(collectBlock)
        row = block[0]
        col = block[1]
        opRLock.acquire()
        
        Pnt((row-0.33, col-0.33))
        Pnt((row-0.33, col+0.33))
        Pnt((row+0.33, col+0.33))
        Pnt((row+0.33, col-0.33))
        
        #Pnt(block)
        SafeClick()
        opRLock.release()
    return _Collect
Collect = Collector()

#(十分之一秒倍数，任务函数，参数)组成的列表
#TaskList = [(1, Collect, ()), (10, ScreenShot, ("./screen/",))]
TaskList = []
TaskStop = False
TaskEvent = threading.Event() 
def BackTask():
    ds = 0 #十分之一秒
    while not TaskStop:
        '''
        TaskEvent.wait()
        for task in TaskList:
            if ds % task[0] == 0:
                task[1](*task[2])
        '''
        sleep(100)
        ds += 1
        
# -*- coding: utf-8 -*- 
'''
作者: lmintlcx
日期: 2017-9-28 20:20
---
FE无冰瓜十八炮
节奏 ch9-56s: PPDD|IPP-PP|PPDD|IPP-PP|PPDD|PPDD|PPN, (6|13|6|13|6|6|6)
视频 https://www.bilibili.com/video/av14889388/
'''

import pvz
from pvz import *

pvz.scene = 'FE'
pvz.paoList = [\
(2,1),(3,1),(4,1),(5,1),(3,3),(4,3),\
(1,5),(2,5),(3,5),(4,5),(5,5),(6,5),\
(1,7),(2,7),(3,7),(4,7),(5,7),(6,7)]

def ChoosingCard():
    ChooseCard(2, 7, True)
    ChooseCard(2, 7)
    ChooseCard(2, 8)
    ChooseCard(3, 1)
    ChooseCard(1, 3)
    ChooseCard(3, 2)
    ChooseCard(1, 4)
    ChooseCard(4, 4)
    ChooseCard(2, 2)
    ChooseCard(2, 1)

def Ice1(r, c):
    Card(1)
    Pnt((r, c))

def Ice0(r, c):
    Card(2)
    Pnt((r, c))

def N(r, c):
    Card(4)
    Pnt((r, c))
    Card(3)
    Pnt((r, c))

def A(r, c):
    Card(5)
    Pnt((r, c))

def B(r, c):
    Card(8)
    Pnt((r, c))

def NoFog():
    for i in range(10):
        B(6, 1)
        sleep(27)

def main():

    print('nowopen %s' % win32gui.GetWindowText(hwnd))
    sleep(4)
    ChoosingCard()
    sleep(0.5)
    LetsRock()
    # sleep(0.2)
    # Click(320, 400)
    sleep(6)
    
    noFog = threading.Thread(target=NoFog, name='NoFogThread')
    noFog.start()

    for wave in range(1, 21):
        print('wave: %s' % wave)
        if(wave == 20):
            preJudge(150, True)
        elif(wave == 10):
            preJudge(55, True)
        else:
            preJudge(95, wave%10 == 0)
        print('mainthread afterpj')
        if (wave == 1): # |PPDD|I
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            Pao(2,9)
            Pao(5,9)
            sleep(6+0.95-0.8-3.2-1+0.1)
            Ice1(1,1)
        elif (wave == 2): # PP-PP|
            Pao(2,8.5)
            Pao(5,8.5)
            sleep(13+0.95-2-3.73)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 3): # |PPDD|
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 4): # |IPP-PP|
            Pao(2,8.5)
            Pao(5,8.5)
            sleep(0.05)
            Ice0(1,1)
            sleep(13+0.95-0.05-2-3.73)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 5): # |PPDD|
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 6): # |PPDD|
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 7): # |PPN|
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            sleep(3.73-1)
            N(3,9)
        elif (wave == 8): # |PPDD|I
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            Pao(2,9)
            Pao(5,9)
            sleep(6+0.95-0.8-3.2-1+0.1)
            Ice1(1,1)
        elif (wave == 9): # PP-PP|
            Pao(2,8.5)
            Pao(5,8.5)
            sleep(13+0.95-2-3.73)
            Pao(2,9)
            Pao(5,9)
            if (wave == 9): # PPPPPP
                sleep(3.73+2-0.95)
                Pao(2,9)
                Pao(5,9)
                sleep(0.8)
                Pao(2,9)
                Pao(5,9)
                sleep(6-0.8)
                Pao(2,9)
                Pao(5,9)
        elif (wave == 10): # |PPDD|
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 11): # |IPP-PP|
            Pao(2,8.5)
            Pao(5,8.5)
            sleep(0.05)
            Ice0(1,1)
            sleep(13+0.95-0.05-2-3.73)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 12): # |PPDD|I
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            Pao(2,9)
            Pao(5,9)
            sleep(6+0.95-0.8-3.2-1+0.1)
            Ice1(1,1)
        elif (wave == 13): # PP-PP|
            Pao(2,8.5)
            Pao(5,8.5)
            sleep(13+0.95-2-3.73)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 14): # |PPDD|
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 15): # |PPDD|
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 16): # |PPN|
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            sleep(3.73-1)
            N(4,9)
        elif (wave == 17): # |PPDD|
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 18): # |IPP-PP|
            Pao(2,8.5)
            Pao(5,8.5)
            sleep(0.05)
            Ice0(1,1)
            sleep(13+0.95-0.05-2-3.73)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 19): # |PPDD|
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            Pao(2,9)
            Pao(5,9)
            if (wave == 19): # PP
                sleep(6+0.95-0.8-3.2-1+0.1)
                Ice1(1,1)
                sleep(3.2+1-0.95)
                Pao(2,9)
                Pao(5,9)
                pvz.nowPao += 4
        elif (wave == 20):
            Pao(4,6)
            Pao(4,8)
            sleep(0.95)
            Pao(2,9)
            Pao(5,9)
            sleep(0.3)
            Pao(2,9)
            Pao(5,9)
            sleep(0.3)
            Pao(2,9)
            Pao(5,9)
            sleep(0.3)
            Pao(2,9)
            Pao(5,9)
            sleep(4)
            Ice0(1,1)
        else:
            pass
        sleep(1)

if __name__ == '__main__':
    main()

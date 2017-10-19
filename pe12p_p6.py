# -*- coding: utf-8 -*- 
'''
作者: lmintlcx
日期: 2017-9-24 22:13
---
PE经典十炮
节奏 P6: PP|PP|PP|PP|PP|N
视频 https://www.bilibili.com/video/av14875298/
'''

# 导入模块
import pvz
from pvz import *

# 场地, 可选值"DE""NE""PE""FE""RE""ME"
# 场上所有炮的位置列表, 一般以后轮坐标为准
pvz.scene = 'PE'
pvz.paoList = [(3,1),(4,1),(3,3),(4,3),(3,8),(4,8),(1,5),(2,5),(3,5),(4,5),(5,5),(6,5)]

# 选卡界面选十张卡
def ChoosingCard():
    while True:
        print("choose card", InterfaceState())
        ChooseCard(2, 7) # 寒冰菇
        ChooseCard(2, 8) # 核蘑菇
        ChooseCard(3, 1) # 睡莲
        ChooseCard(5, 4) # 咖啡豆
        ChooseCard(1, 3) # 樱桃
        ChooseCard(2, 7, True) # 模仿
        ChooseCard(4, 4) # 三叶草
        ChooseCard(4, 7) # 南瓜
        ChooseCard(5, 3) # 玉米
        ChooseCard(6, 8) # 炮

        sleep(0.5)
        LetsRock()
        # sleep(0.2)
        # Click(320, 400) # 有时候会出现警告窗口需要再点击一到多次YES
        sleep(4) # 等切换到游戏场景, FE再加两秒
        if InterfaceState() != 2: #按钮点成功
            break

        #把卡都点掉
        for i in range(0, 20):
            Card(1)
            sleep(0.2)
            

# 在r路c列释放樱桃
nowA = 0
def A(r, c):
    global nowA
    if nowA == 0:
        Card(5)
    else:
        Card(6)
    Pnt((r, c))
    nowA = (nowA+1)%2

# 在r c放南瓜
def Gua(r, c):
    Card(8)
    Pnt((r,c))
GuaList = [[1,1],[2,1],[5,1],[6,1],[3,9],[4,9]]

# 在r路c列释放核蘑菇
def N(r, c):
    if r in [3,4]:
        Card(3)
        Pnt((r, c))
    Card(2)
    Pnt((r, c))
    Card(4)
    Pnt((r, c))

ice = 0
def I(r,c):
    global ice
    if ice == 0:
        Card(1)
        Pnt((r, c))
        Card(4)
        Pnt((r, c))
        Card(6)
        Pnt((7-r, c))
    elif ice==1:
        Card(4)
        Pnt((7-r, c))
    ice = (ice+1)%2

def exPao(wave):
    for i in range(0,4):
        sleep(3.73)
        nextwave = False
        
        nextCount = 210
        if wave == 20:
            nextCount = 610
        for i in range(0, 22):
            wcd = WaveCountdown()
            if 0 < wcd <= nextCount:
                nextwave = True
                break
            sleep(0.1)

        if nextwave:
            print(wave, "wave finished, next wave", RedWordCountDown(), WaveCountdown(), InterfaceState(), FinishedWaveNum(), WordKind(), WordShow())
            break
        print(wave, "wave, expao", RedWordCountDown(), WaveCountdown(), InterfaceState(), FinishedWaveNum(), WordKind(), WordShow())
        Pao(2,9)
        Pao(5,9)
        Collect()
        
def exPao20():
    for i in range(0,4):
        sleep(3.73)
        nextwave = False
        for i in range(0, 22):
            if WordKind() == 12:
                nextwave = True
                break
            sleep(0.1)

        if nextwave:
            print(20, "wave finished, next wave", RedWordCountDown(), WaveCountdown(), FinishedWaveNum(), WordKind())
            break
        print(20, "wave, expao", RedWordCountDown(), WaveCountdown(), InterfaceState(), FinishedWaveNum(), WordKind())
        Pao(2,9)
        Pao(5,9)
        Collect()
        
collectArea = [ [(1,2),(1,3),(1,4),(2,2),(2,3),(2,4)]
            ,   [(5,2),(5,3),(5,4),(6,2),(6,3),(6,4)]
            ,   [(1,9),(2,9),(3,9),(4,9),(5,9),(6,9)]]
nowCollect = 0
def Collect():
    global nowCollect
    nowCollect = (nowCollect + 1)%3
    for area in collectArea:
        for block in area:
            row = block[0]
            col = block[1]
            Pnt((row-0.35, col-0.35))
            Pnt((row-0.35, col+0.35))
            Pnt((row+0.35, col+0.35))
            Pnt((row+0.35, col-0.35))
            Pnt(block)
            sleep(0.01)
            
#第十波用核弹消延迟           
NList = [[2,8],[5,8]]
nowN = 1

#防止炮自己炸自己放不出来，炮列表(3,6)(4,6)用(3,5)(4,5)代替
def ShanhuPao():
    if pvz.paoList[pvz.nowPao] == (3,7) or pvz.paoList[pvz.nowPao] == (3,8):
        print("shanhupao", pvz.paoList[pvz.nowPao], 4,7)
        for i in range(10):
            Pnt((3,8))
        Pnt((4,7))
        SafeClick()
        pvz.nowPao = (1+pvz.nowPao)%len(pvz.paoList)
    elif pvz.paoList[pvz.nowPao] == (4,7) or pvz.paoList[pvz.nowPao] == (4,8):
        print("shanhupao", pvz.paoList[pvz.nowPao], 3,7)
        for i in range(10):
            Pnt((4,8))
        Pnt((3,7))
        SafeClick()
        pvz.nowPao = (1+pvz.nowPao)%len(pvz.paoList)
    else:
        Pao(4,7)

nowPlantNum = 66 #最开始有66个固定植物
def CheckPlant():
    global nowPlantNum
    num = PlantNum()
    print("now plant", num)
    if 0 < num < nowPlantNum:
        ScreenShot("./screen/")
        nowPlantNum = num
    if num < 50 or InterfaceState() == 4: #僵尸进屋
        print("GameOver")
        exit()
    
def main():
    sleep(4) # 等四秒, 一般这段时间内开启录像
    ChoosingCard() # 选卡
    #补瓜
    for gua in GuaList:
        Gua(*gua)
        SafeClick()
    # wave的取值为1~20, 对应每次选卡共20波僵尸的处理
    for wave in range(1, 21):
        Collect()
        CheckPlant()
        print('wave: %s' % wave)
        # 常用预判时间95cs
        # 第10波僵尸出生点偏右, 推迟到55cs并用樱桃补刀来消除延迟
        # 第20波预判150cs可炮炸珊瑚
        if(wave == 20):
            preJudge(150, True)
        elif(wave == 10):
            preJudge(55, True)
        else:
            preJudge(85, (wave%10 == 0))
        print('mainthread afterpj')
        # 到达指定预判时间的操作
        if (wave == 10):
            Pao(2,9)
            Pao(5,9)
            # 第10波额外加个樱桃消除延迟
            # 炮飞行时间3.73s, 樱桃释放后0.98s爆炸
            # 在(3.73-0.98)s后释放樱桃让樱桃与玉米炮同时生效
            sleep(3.73-0.98 + 0.3)
            global nowN
            nowN = (nowN + 1)%2
            N(*NList[nowN])
            sleep(0.5)
            # 风扇吹走漏炸的气球
            Card(7)
            Pnt((1, 7))
        elif (wave == 20):
            # 第20波预判1.5s炮炸珊瑚, 等待0.9s后再炸前场
            print("zha shanhu", pvz.paoList[pvz.nowPao])
            ShanhuPao()
            
            sleep(0.9)
            Pao(2,9)
            Pao(5,9)
            sleep(1)
            exPao20()
        else:
            # 除以上特殊处理的波次(10/20/6/15)外其他均为95cs预判炮, 落点2-9和5-9
            Pao(2,9)
            Pao(5,9)
            # 第9/19波打完一对炮后还需要额外用炮收尾
            # 在对应波次的地方把pvz.nowPao变量加上额外需要的炮数, 让第10/20波自动发炮时选择的炮位相应地延后
            # 一般第9波打完两炮后还需要4门炮(加上冰瓜IO), 第9波打完两炮后还需要2门炮(自然出怪下)
            if (wave in [9,19]):
                exPao(wave)
            elif wave==1:
                '''
                sleep(3.73-0.98 + 1)
                A(2,9)
                '''


        # 每一波操作都要运行到本波刷新以后, 除第20波外通常用的是0.95s和0.55s预判
        # 所以每波至少要延迟0.95s来保证本次循环执行到本波刷新以后再执行下一个循环
        if not wave in [9,19,20,10]:
            sleep(3.8)
            delay = True
            for i in range(0, 14):
                if WaveCountdown() < 1000:
                    delay = False
                    break
                sleep(0.1)
            if delay:
                I(2,7)
                #sleep(1)
                #A(2,9)
                print("monster delay pao end", WaveCountdown())
                '''
                if WaveCountdown() > 1000:
                    sleep(2)
                    Pao(2,9)
                    Pao(5,9)
                    sleep(1)
                    '''
                

# 代码只在作为主程序运行时执行
if __name__ == '__main__':
    print('nowopen %s' % win32gui.GetWindowText(hwnd)) # 打印窗口标题
    NoPause()
    pvz.nowPao = 4
    sleep(2)
        
    while True:
        BackUp(r'./save/')
        main()
        sleep(8)

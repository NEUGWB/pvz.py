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
pvz.nowPao = 4

antiDelay = 0
ch = False

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
        sleep(5) # 等切换到游戏场景, FE再加两秒
        if InterfaceState() != 2: #按钮点成功
            break

        #把卡都点掉
        print(InterfaceState(), "InterfaceState()")
        for i in range(0, 20):
            Card(1)
            sleep(0.02)
            

# 在r路c列释放樱桃
def A(r, c):
    Card(5)
    Pnt((r, c))

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
        Pnt((1,1))
    elif ice==1:
        Card(4)
        Pnt((1,1))
    SafeClick()
    ice = (ice+1)%2

def exPao(wave):
    sleep(3.6)
    Collect()
    if wave == 20:
        Card(7)
        Pnt((1, 7))
    else:
        FixGua()
    def Pred_9_19():
        return 0 < WaveCountdown() < 210
    def Pred_20():
        return WordKind() == 12
        
    if wave == 20:
        pred = Pred_20
    else:
        pred = Pred_9_19
    checkTime = (2.5, 9, 0.1, 6)
    
    for i in range(0,4):
        nextwave = False
        for t in range(0, int(checkTime[i] * 100)):
            if pred():
                nextwave = True
                break
            sleep(0.01)

        if nextwave:
            print(wave, "wave finished, next wave", RedWordCountDown(), WaveCountdown(), InterfaceState(), FinishedWaveNum(), WordKind())
            break
        print(wave, "wave, expao", RedWordCountDown(), WaveCountdown(), InterfaceState(), FinishedWaveNum(), WordKind())
        Pao(2,9)
        Pao(5,9)
        
        Collect()
        CheckPlant()
        
collectArea = [ [(1,2),(1,3),(1,4),(2,2),(2,3),(2,4)]
            ,   [(5,2),(5,3),(5,4),(6,2),(6,3),(6,4)]
            ,   [(1,9),(2,9),(3,9),(4,9),(5,9),(6,9)]
            ,   [(1,1),(2,1),(5,1),(6,1),(1,8),(2,8),(5,8),(6,8),(6,9)]]
def Collect():
    for area in collectArea:
        for block in area:
            row = block[0]
            col = block[1]
            Pnt((row-0.33, col-0.33))
            Pnt((row-0.33, col+0.33))
            Pnt((row+0.33, col+0.33))
            Pnt((row+0.33, col-0.33))
            Pnt(block)
            SafeClick()
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

nowPlantNum = 65 #固定植物
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
#补瓜
def FixGua():
    for gua in GuaList:
        Gua(*gua)
        SafeClick()

def CheckDelay():
    sleep(3.73)
    Collect()
    delay = True
    for i in range(0, 140):
        if 0 < WaveCountdown() < 1000:
            delay = False
            break
        sleep(0.01)
    return delay
def AntiDelay():
    global antiDelay, ch
    print("anti delay, strategy:", antiDelay)
    if antiDelay == 4:
        sleep(1)
        A(2, 9)
    else:
        Pao(2,9)
        Pao(5,9)
        ch = True
    antiDelay = (antiDelay + 1)%3
    
def main():
    sleep(4) # 等四秒, 一般这段时间内开启录像
    ChoosingCard() # 选卡
    # wave的取值为1~20, 对应每次选卡共20波僵尸的处理
    global antiDelay, ch
    antiDelay = 0
    ch = False
    for wave in range(1, 21):
        CheckPlant()
        print('wave: %s' % wave)

        if ch:
            #预判冰，打CH6，实际上只能预判200
            preJudge(300)
            print("change6, ice", WaveCountdown())
            I(2, 7)
            sleep(3)
            print("ch ice effect", WaveCountdown())
            Collect()
            sleep(4.0)
            Pao(2, 9)
            Pao(5, 9)
            ch = False
            if wave in [9, 19, 20]:
                exPao(wave)
            else:
                delay = CheckDelay()
                if delay:
                    print("ch delay......", wave)
                    AntiDelay()
                '''
                sleep(3.6)
                delay = True
                Collect()
                for i in range(0, 140):
                    if 0 < WaveCountdown() < 1000:
                        delay = False
                        break
                    sleep(0.01)
                if delay:
                    if antiDelay == 2:
                        sleep(2)
                        A(2, 9)
                    else:
                        Pao(2,9)
                        Pao(5,9)
                        ch = True
                    antiDelay = (antiDelay + 1)%3'''
            continue
                    
        # 常用预判时间95cs
        # 第10波僵尸出生点偏右, 推迟到55cs并用樱桃补刀来消除延迟
        # 第20波预判150cs可炮炸珊瑚
        if(wave == 20):
            preJudge(150, True)
        elif(wave == 10):
            preJudge(55, True)
        else:
            preJudge(95, (wave%10 == 0))
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
            exPao(20)
        else:
            # 除以上特殊处理的波次(10/20/6/15)外其他均为95cs预判炮, 落点2-9和5-9
            Pao(2,9)
            Pao(5,9)
            # 第9/19波打完一对炮后还需要额外用炮收尾
            # 在对应波次的地方把pvz.nowPao变量加上额外需要的炮数, 让第10/20波自动发炮时选择的炮位相应地延后
            # 一般第9波打完两炮后还需要4门炮(加上冰瓜IO), 第9波打完两炮后还需要2门炮(自然出怪下)
            if (wave in [9,19]):
                exPao(wave)

        # 每一波操作都要运行到本波刷新以后, 除第20波外通常用的是0.95s和0.55s预判
        # 所以每波至少要延迟0.95s来保证本次循环执行到本波刷新以后再执行下一个循环
        if not wave in [9,19,20,10]:
            delay = CheckDelay()
            if delay:
                print("delay......", wave)
                AntiDelay()
            '''
            delay = True
            for i in range(0, 140):
                if 0 < WaveCountdown() < 1000:
                    delay = False
                    break
                sleep(0.01)
            if delay:
                if antiDelay == 2:
                    sleep(2)
                    A(2, 9)
                else:
                    Pao(2,9)
                    Pao(5,9)
                    ch = True
                antiDelay = (antiDelay + 1)%3
            else:
                print("no delay", i, WaveCountdown())'''

# 代码只在作为主程序运行时执行
if __name__ == '__main__':
    print('nowopen %s' % win32gui.GetWindowText(hwnd)) # 打印窗口标题
    NoPause()
    sleep(2)
        
    while True:
        BackUp(r'./save/')
        main()
        sleep(8)

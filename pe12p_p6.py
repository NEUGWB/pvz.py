# -*- coding: utf-8 -*- 

# 导入模块
import pvz
from pvz import *

# 场地, 可选值"DE""NE""PE""FE""RE""ME"
# 场上所有炮的位置列表, 一般以后轮坐标为准
pvz.scene = 'PE'
pvz.paoList = [(3,1),(4,1),(3,3),(4,3),(3,8),(4,8),(1,5),(2,5),(3,5),(4,5),(5,5),(6,5)]
pvz.nowPao = 10

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
    return UseCard(5, r, c)

# 在r c放南瓜
def Gua(r, c):
    return UseCard(8, r, c)

GuaList = [[1,1],[2,1],[5,1],[6,1],[3,9],[4,9]]

# 在r路c列释放核蘑菇
def N(r, c):
    UseCard(2, r, c)
    UseCard(4, r, c)

ice = 0
def I(r,c):
    global ice
    if ice == 0:
        UseCard(1, r, c)
        UseCard(4, r, c)
        UseCard(6, 1, 1)
    elif ice==1:
        UseCard(4, 1, 1)
    SafeClick()
    ice = (ice+1)%2

def exPao(wave):
    sleep(3.75)
    if wave == 20:
        UseCard(7, 1, 7)
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
    checkTime = (2.5, 10, 0.1, 6)
    
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
        
        CheckPlant()
        

#第十波用核弹消延迟           
NList = [[2,8],[5,8]]
nowN = 1

nowPlantNum = 65 #固定植物
def CheckPlant():
    global nowPlantNum
    num = PlantNum()
    if num == 0:
        return
    print("now plant", num)
    if num < nowPlantNum:
        nowPlantNum = num
    if num < 63 or InterfaceState() == 4: #僵尸进屋
        print("GameOver")
        TaskStop = True
        exit()
#补瓜
def FixGua():
    for gua in GuaList:
        Gua(*gua)
        SafeClick()

def CheckDelay():
    sleep(3.73)
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
    print("TaskEvent.clear()")
    TaskEvent.set()
    for wave in range(1, 21):
        CheckPlant()
        print('wave: %s' % wave)

        if ch:
            #预判冰，打CH6，实际上只能预判200
            preJudge(250)
            print("change6, ice", WaveCountdown())
            I(2, 7)
            sleep(3)
            print("ch ice effect", WaveCountdown())
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
            UseCard(7, 1, 7)
        elif (wave == 20):
            # 第20波预判1.5s炮炸珊瑚, 等待0.9s后再炸前场
            Pao(4,7,True)
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
    print("TaskEvent.clear()")
    TaskEvent.clear()        

# 代码只在作为主程序运行时执行
if __name__ == '__main__':
    print('nowopen %s' % win32gui.GetWindowText(hwnd)) # 打印窗口标题
    NoPause()
    sleep(2)
    
    
    TaskEvent.clear()
    backThread = threading.Thread(target = BackTask, name = "BackThread")
    backThread.setDaemon(True) # 后台线程, 主线程停止运行时后台线程同样退出
    backThread.start()
    
    while True:
        BackUp(r'./save/')
        
        main()
        sleep(8)

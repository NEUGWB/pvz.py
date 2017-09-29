# -*- coding: utf-8 -*- 
'''
作者: lmintlcx
日期: 2017-9-28 20:50
---
PE卖萌六炮
节奏 ch5: PP|I-PP|I-PP, (6|15|15)
视频 https://www.bilibili.com/video/av14888150/
'''

# 导入模块
import pvz
from pvz import *

# 场地, 可选值"DE""NE""PE""FE""RE""ME"
# 场上所有炮的位置列表, 一般以后轮坐标为准
pvz.scene = 'PE'
pvz.paoList = [(1,5),(2,5),(3,5),(4,5),(5,5),(6,5)]

# 选卡界面选十张卡
# 选择模仿者时`ChooseCard()`函数第三个参数为True
def ChoosingCard():
    ChooseCard(2, 7, True) # 模仿者寒冰菇
    ChooseCard(2, 7) # 寒冰菇
    ChooseCard(5, 4) # 咖啡豆
    ChooseCard(1, 3) # 樱桃
    ChooseCard(3, 2) # 倭瓜
    ChooseCard(4, 7) # 南瓜壳
    ChooseCard(4, 4) # 三叶草
    ChooseCard(2, 6) # 胆小菇
    ChooseCard(2, 2) # 阳光菇
    ChooseCard(2, 1) # 小喷菇

# 在有足够数量的安全的永久存冰位和临时存冰位的情况下, 每50+s存一次
# 卡槽1为复制冰, 2为原版冰. 永久存冰位2-1 5-1, 临时存冰位1-1 2-6
# 共存七次, 每次存两冰, 优先存原版冰, 优先存放在永久位
# 存冰函数只循环六次, 最后一次在20波冰杀小偷后再存
def FillIce():
    for i in range(6):
        sleep(0.1)
        Card(2)
        Pnt((2, 1))
        Pnt((5, 1))
        Pnt((1, 1))
        Pnt((6, 1))
        Card(1)
        Pnt((2, 1))
        Pnt((5, 1))
        Pnt((1, 1))
        Pnt((6, 1))
        sleep(50)

# 点冰, 优先点临时位
def Ice(): 
    Card(3)
    Pnt((6, 1))
    Pnt((1, 1))
    Pnt((5, 1))
    Pnt((2, 1))

def A(r, c): #A
    Card(4)
    Pnt((r, c))


def main():

    print('nowopen %s' % win32gui.GetWindowText(hwnd))
    sleep(4)
    ChoosingCard()
    sleep(0.5)
    LetsRock()
    # sleep(0.2)
    # Click(320, 400) # 有时候会出现警告窗口需要再点击一到多次YES
    sleep(4)

    # 存冰线程
    fillIce = threading.Thread(target=FillIce, name='FillIceThread')
    fillIce.start()

    # wave的取值为1~20, 对应每次选卡共20波僵尸的处理
    for wave in range(1, 21):
        print('wave: %s' % wave)
        # 常用预判时间95cs
        # 第10波僵尸出生点偏右, 推迟到55cs并用樱桃补刀来消除延迟
        # 第20波预判150cs可炮炸珊瑚
        if(wave == 20):
            preJudge(150, True)
        elif(wave == 10):
            preJudge(55, True)
        else:
            preJudge(95, wave%10 == 0)
        print('mainthread afterpj')
        # 到达指定预判时间的操作
        if wave in [10]:
            Pao(2, 9)
            Pao(5, 9)
            sleep(3.73-0.98)
            A(2,9) # 樱桃消延迟
            Card(7) # 风扇吹漏炸的气球
            Pnt((1, 7))
            sleep(6+0.55-2.98-(3.73-0.98)+0.2) # 0.2s预判冰
            Ice()
        elif wave in [20]:
            Pao(4, 7) # 炸珊瑚
            sleep(0.95)
            Pao(2, 9)
            Pao(5, 9)
            sleep(2)
            Ice() # 冰杀小偷
            # 最后一次存冰
            sleep(3)
            Card(2)
            Pnt((5, 1))
            Card(1)
            Pnt((2, 1))
        elif wave in [1, 4, 7, 13, 16, 19]:
            Pao(2, 9)
            Pao(5, 9)
            sleep(6+0.95-2.98+0.2) # 0.2s预判冰
            Ice()
            if wave in [19]:
                pvz.nowPao += 2
        elif wave in [2, 5, 8, 11, 14, 17]:
            sleep(15+0.95-2-3.73) # 波长15s
            Pao(2, 8.5)
            Pao(5, 8.5)
            sleep(3.73+2-2.98+0.2) # 0.2s预判冰
            Ice()
        elif wave in [3, 6, 9, 12, 15, 18]:
            sleep(15+0.95-2-3.73) # 波长15s
            Pao(2, 8.5)
            Pao(5, 8.5)
            if wave in [9]:
                pvz.nowPao += 4
        else:
            pass
        sleep(1)

if __name__ == '__main__':
    main()

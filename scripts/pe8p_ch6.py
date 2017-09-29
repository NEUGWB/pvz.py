# -*- coding: utf-8 -*- 
'''
作者: lmintlcx
日期: 2017-9-27 22:10
---
PE前置八炮
节奏 ch6: PP|I-PP|PP|I-PP, (6|12|6|12)
视频 https://www.bilibili.com/video/av14880401/
'''

# 导入模块
import pvz
from pvz import *

# 场地, 可选值"DE""NE""PE""FE""RE""ME"
# 场上所有炮的位置列表, 一般以后轮坐标为准
pvz.scene = 'PE'
pvz.paoList = [(3,1),(4,1),(3,3),(4,3),(1,5),(2,5),(5,5),(6,5)]

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
# 卡槽1为复制冰, 2为原版冰. 永久存冰位3-5 4-5, 临时存冰位1-7 2-7
# 存冰函数共有五次循环, 每次存两冰, 优先存原版冰, 优先存放在永久位
def FillIce():
    for i in range(5):
        sleep(0.1)
        Card(2)
        Pnt((4, 5))
        Pnt((3, 5))
        Pnt((2, 7))
        Pnt((1, 7))
        Card(1)
        Pnt((4, 5))
        Pnt((3, 5))
        Pnt((2, 7))
        Pnt((1, 7))
        sleep(50)

# 点冰, 优先点临时位
def Ice(): 
    Card(3)
    Pnt((1, 7))
    Pnt((2, 7))
    Pnt((3, 5))
    Pnt((4, 5))

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
            A(2,9)
            sleep(6+0.55-2.98-(3.73-0.98)+0.2) # 0.2s预判冰
            Ice()
        elif wave in [20]:
            Ice() #冰消珊瑚
        elif wave in [1, 3, 5, 7, 12, 14, 16, 18]:
            Pao(2, 9)
            Pao(5, 9)
            sleep(6+0.95-2.98+0.2) # 0.2s预判冰
            Ice()
        elif wave in [9]:
            Pao(2, 9)
            Pao(5, 9)
            if wave in [9]:
                pvz.nowPao += 4
        elif wave in [2, 4, 6, 8, 11, 13, 15, 17, 19]:
            sleep(12+0.95-2-3.73) # 波长12s
            Pao(2, 9)
            Pao(5, 9)
        else:
            pass
        sleep(1)

if __name__ == '__main__':
    main()

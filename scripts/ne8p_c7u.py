# -*- coding: utf-8 -*- 
'''
作者: lmintlcx
日期: 2017-9-27 23:10
---
NE前置八炮
节奏 C7u-56s: PP|I-PP|IPP-PP|PP|cccPP, (6|15|20|6|9)
视频 https://www.bilibili.com/video/av14611760/
'''

# 导入模块
import pvz
from pvz import *

# 场地, 可选值"DE""NE""PE""FE""RE""ME"
# 场上所有炮的位置列表, 一般以后轮坐标为准
pvz.scene = 'NE'
pvz.paoList = [(1,1),(1,5),(3,1),(3,5),(2,5),(4,5),(5,1),(5,5)]

# 选用这么复杂的节奏只是为了演示一些函数的用法

# 选卡界面选十张卡
# 选择模仿者时`ChooseCard()`函数第三个参数为True
def ChoosingCard():
    ChooseCard(2, 7, True) # 模仿者寒冰菇
    ChooseCard(2, 7) # 寒冰菇
    ChooseCard(2, 8) # 核蘑菇
    ChooseCard(1, 3) # 樱桃
    ChooseCard(3, 2) # 倭瓜
    ChooseCard(2, 4) # 墓碑
    ChooseCard(4, 4) # 三叶草
    ChooseCard(2, 6) # 胆小菇
    ChooseCard(2, 2) # 阳光菇
    ChooseCard(2, 1) # 小喷菇

# 在r路c列释放复制冰
def Ice1(r, c):
    Card(1)
    Pnt((r, c))

# 在r路c列释放原版冰
def Ice0(r, c):
    Card(2)
    Pnt((r, c))

# 在r路c列释放核蘑菇
def N(r, c):
    Card(3)
    Pnt((r, c))

# 在r路c列释放樱桃
def A(r, c):
    Card(4)
    Pnt((r, c))

# 中三路种垫材
# 加个延时避免短时间内有大量操作时出现卡帧
def DC_MJ():
    Card(8)
    Pnt((2, 9))
    sleep(0.001)
    Card(9)
    Pnt((3, 9))
    sleep(0.001)
    Card(10)
    Pnt((4, 9))

# 中三路铲垫材
# 加个延时避免短时间内有大量操作时出现卡帧
def DelDC():
    Card(12)
    Pnt((2, 9))
    sleep(0.001)
    Card(12)
    Pnt((3, 9))
    sleep(0.001)
    Card(12)
    Pnt((4, 9))

# 在前场有可能冒墓碑的区域种墓碑吞噬者
def Mubei():
    Card(6)
    for r in range(1,6):
        for c in range(7,10):
            Pnt((r, c))
    # Pnt((1, 7))
    # Pnt((1, 8))
    # Pnt((1, 9))
    # Pnt((2, 7))
    # Pnt((2, 8))
    # Pnt((2, 9))
    # Pnt((3, 7))
    # Pnt((3, 8))
    # Pnt((3, 9))
    # Pnt((4, 7))
    # Pnt((4, 8))
    # Pnt((4, 9))
    # Pnt((5, 7))
    # Pnt((5, 8))
    # Pnt((5, 9))


def main():

    print('nowopen %s' % win32gui.GetWindowText(hwnd))
    sleep(4)
    ChoosingCard()
    sleep(0.5)
    LetsRock()
    sleep(0.2)
    Click(320, 400) # 有时候会出现警告窗口需要再点击一到多次YES
    sleep(4)
    
    # wave的取值为1~20, 对应每次选卡共20波僵尸的处理
    for wave in range(1, 21):
        print('wave: %s' % wave)
        # 常用预判时间95cs
        # 第10/20波僵尸出生点偏右, 推迟到55cs预判
        if (wave == 10) or (wave == 20):
            preJudge(55, True)
        else:
            preJudge(95, False)
        print('mainthread afterpj')
        # 到达指定预判时间的操作
        if (wave == 10):
            Pao(2,9)
            Pao(4,9)
            sleep(3.73-0.98)
            A(2,9) # 樱桃消延迟
            Card(7)
            Pnt((1, 7)) # 风扇吹漏炸的气球
            sleep(6+0.55-3.2-1-(3.73-0.98)+0.5) # 0.5s预判冰
            Ice1(3,7) # 复制冰
        elif (wave == 1) or (wave == 6) or (wave == 15):
            Pao(2,9)
            Pao(4,9)
            sleep(6+0.95-3.2-1+0.5) # 0.5s预判冰
            Ice1(3,7) # 复制冰
        elif (wave == 2) or (wave == 7) or (wave == 11) or (wave == 16):
            sleep(15+0.95-2-3.73) # 波长15s
            Pao(2,8.5)
            Pao(4,8.5)
        elif (wave == 3) or (wave == 8) or (wave == 12) or (wave == 17):
            Pao(2,8)
            Pao(4,8)
            sleep(0.0) # 0.05s预判冰(0.95s预判, 冰菇1s后生效)
            Ice0(3,7) #原版冰
            sleep(20+0.95-2-3.73-0.0) # 波长20s
            Pao(2,8.5)
            Pao(4,8.5)
        elif (wave == 4) or (wave == 9) or (wave == 13) or (wave == 18):
            Pao(2,9)
            Pao(4,9)
            if(wave == 9): # 第9波收尾预留炮
                pvz.nowPao += 4
        elif (wave == 5) or (wave == 14) or (wave == 19):
            sleep(0.95+1.75) # 刷新后1.75s垫MJ
            DC_MJ()
            sleep(1) # 1s后铲去垫材
            DelDC()
            sleep(9+0.95-3.73-2-(0.95+1.75)-1) # 波长9s
            Pao(2,8.5)
            Pao(4,8.5)
            if (wave == 19):
                sleep(3.73+2+6+0.1-3.2-1)
                Ice1(3,7) # 冰杀漏炸的矿工
            if(wave == 19): # 第19波收尾预留炮
                pvz.nowPao += 2
        elif (wave == 20):
            Pao(2,9)
            Pao(4,9)
            sleep(5+0.55-1) # 刷新后5s冻住小偷
            Ice0(3,7)
            Ice0(3,8) # 种两次冰, 防止第一次正好种到墓碑上
            sleep(0.1)
            Mubei() # 吃墓碑
        else:
            pass
        sleep(1) # 保证每波的脚本运行到本波刷新以后

if __name__ == '__main__':
    main()

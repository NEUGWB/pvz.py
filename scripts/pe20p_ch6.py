# -*- coding: utf-8 -*- 
'''
作者: lmintlcx
日期: 2017-9-26 21:35
---
PE拦截二十炮
节奏 ch6: PPSDD|IPP-PPD|PPSDD|IPP-PPD, (6|12|6|12)
视频 https://www.bilibili.com/video/av14881393/
'''

# 导入模块
import pvz
from pvz import *

# 场地, 可选值"DE""NE""PE""FE""RE""ME"
# 场上所有炮的位置列表, 一般以后轮坐标为准
pvz.scene = 'PE'
pvz.paoList = [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(3,3),(4,3),(1,5), \
(2,5),(3,5),(4,5),(5,5),(6,5),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7)]

# 选卡界面选十张卡
# 选择模仿者时`ChooseCard()`函数第三个参数为True
def ChoosingCard():
    ChooseCard(5, 4) # 咖啡豆
    ChooseCard(2, 7) # 寒冰菇
    ChooseCard(2, 7, True) # 模仿者寒冰菇
    ChooseCard(1, 3) # 樱桃
    ChooseCard(3, 2) # 倭瓜
    ChooseCard(4, 7) # 南瓜壳
    ChooseCard(5, 2) # 花盆
    ChooseCard(2, 6) # 胆小菇
    ChooseCard(2, 2) # 阳光菇
    ChooseCard(2, 1) # 小喷菇

# 对于只有两个可用存冰位的阵型, 存冰规划如下
# 存冰在单独的线程里执行
# 第一次点冰至少2.98s后存复制冰, 18s(半个循环)后存原版冰
# (50.1-18)s后存复制冰, 18s后存原版冰, 重复此过程
# (注意中场第9波需要拖僵尸拖一段时间但是也不要太长)
def FillIce():
    sleep(3.5)
    Card(3) # 复制冰
    Pnt((3, 9))
    # Pnt((4, 9))
    sleep(18)
    Card(2) # 原版冰
    Pnt((3, 9))
    # Pnt((4, 9))
    for i in range(4):
        sleep(50.1-18)
        Card(3) # 复制冰
        Pnt((3, 9))
        Pnt((4, 9))
        sleep(18)
        Card(2) # 原版冰
        Pnt((3, 9))
        Pnt((4, 9))

# 点冰, 选咖啡豆后往所有的存冰位点一次
def Ice(): 
    Card(1)
    Pnt((3, 9))
    Pnt((4, 9))


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
        # 第10波僵尸出生点偏右, 推迟到55cs
        # 第20波预判150cs可炮炸珊瑚
        if(wave == 20):
            preJudge(150, True)
        elif(wave == 10):
            preJudge(55, True)
        else:
            preJudge(95, (wave%10 == 0))
        print('mainthread afterpj')
        # 到达指定预判时间的操作
        if wave in [1, 3, 5, 7, 9, 10, 12, 14, 16, 18]:
        # if (wave == 1) or (wave == 3) or (wave == 5) or (wave == 7) or (wave == 9) \
        # or (wave == 10) or (wave == 12) or (wave == 14) or (wave == 16) or (wave == 18):
            Pao(2,9)
            Pao(5,9)
            Pao(5,9)
            sleep(1.1)
            Pao(2,9)
            Pao(5,9)
            # 波长6s, 预判0.95s, 点下咖啡豆到生效2.98s
            # 0.5s预判冰, 即下一波在刷新后0.5s被冻住
            if (wave == 10): 
                sleep(6+0.55-1.1-2.98+0.5)
            else:
                sleep(6+0.95-1.1-2.98+0.5)
            Ice()
            if (wave == 1): 
                fillIce = threading.Thread(target=FillIce, name='FillIceThread')
                fillIce.start()
            if (wave == 9): # 第9波收尾预留炮
                pvz.nowPao += 6
        elif wave in [2, 4, 6, 8, 11, 13, 15, 17, 19]:
        # elif (wave == 2) or (wave == 4) or (wave == 6) or (wave == 8) \
        # or (wave == 11) or (wave == 13) or (wave == 15) or (wave == 17) or (wave == 19):
            Pao(2,8.5)
            Pao(5,8.5)
            # 波长12s, 预判0.95s, 玉米炮发射后3.73s生效, 激活到下一波刷出2s
            sleep(12+0.95-3.73-2)
            Pao(2,9)
            Pao(5,9)
            sleep(2.2)
            Pao(5,8)
            if (wave == 19): # 第19波收尾自动发炮并预留两炮
                sleep(3.73+2-2.2-0.95)
                Pao(2,9)
                Pao(5,9)
                Pao(5,9)
                sleep(1.1)
                Pao(2,9)
                Pao(5,9)
                pvz.nowPao += 2
        elif (wave == 20):
            # 两炮炸珊瑚
            Pao(4,6)
            Pao(4,8)
            sleep(0.9)
            Pao(2,9)
            Pao(5,9)
            Pao(2,9)
            Pao(5,9)
            sleep(1)
            Pao(2,9)
            Pao(5,9)
            Pao(2,9)
            Pao(5,9)
        else:
            pass
        sleep(1) # 保证每波的脚本运行到本波刷新以后

if __name__ == '__main__':
    main()

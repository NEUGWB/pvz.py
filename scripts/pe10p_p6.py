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
pvz.paoList = [(3,1),(4,1),(3,3),(4,3),(1,5),(2,5),(3,5),(4,5),(5,5),(6,5)]

# 选卡界面选十张卡
def ChoosingCard():
    ChooseCard(2, 7) # 寒冰菇
    ChooseCard(2, 8) # 核蘑菇
    ChooseCard(3, 1) # 睡莲
    ChooseCard(5, 4) # 咖啡豆
    ChooseCard(1, 3) # 樱桃
    ChooseCard(3, 2) # 倭瓜
    ChooseCard(4, 4) # 三叶草
    ChooseCard(2, 6) # 胆小菇
    ChooseCard(2, 2) # 阳光菇
    ChooseCard(2, 1) # 小喷菇

# 在r路c列释放樱桃
def A(r, c):
    Card(5)
    Pnt((r, c))

# 在r路c列释放核蘑菇
def N(r, c):
    Card(3)
    Pnt((r, c))
    Card(2)
    Pnt((r, c))
    Card(4)
    Pnt((r, c))

def main():
    print('nowopen %s' % win32gui.GetWindowText(hwnd)) # 打印窗口标题
    sleep(4) # 等四秒, 一般这段时间内开启录像
    ChoosingCard() # 选卡
    sleep(0.5) # 等半秒
    LetsRock() # 点 Let's Rock!
    # sleep(0.2)
    # Click(320, 400) # 有时候会出现警告窗口需要再点击一到多次YES
    sleep(4) # 等切换到游戏场景, FE再加两秒
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
            preJudge(95, (wave%10 == 0))
        print('mainthread afterpj')
        # 到达指定预判时间的操作
        if (wave == 10):
            Pao(2,9)
            Pao(5,9)
            # 第10波额外加个樱桃消除延迟
            # 炮飞行时间3.73s, 樱桃释放后0.98s爆炸
            # 在(3.73-0.98)s后释放樱桃让樱桃与玉米炮同时生效
            sleep(3.73-0.98)
            A(2,9)
            sleep(0.5)
            # 风扇吹走漏炸的气球
            Card(7)
            Pnt((1, 7))
        elif (wave == 20):
            # 第20波预判1.5s炮炸珊瑚, 等待0.9s后再炸前场
            Pao(4,7)
            sleep(0.9)
            Pao(2,9)
            Pao(5,9)
        elif (wave == 6) or (wave == 15):
            # 第6波和第15波核武代奏
            # 核弹与玉米炮生效时间相同, 同样在预判3.73s后
            # 嗑下咖啡豆到唤醒1.98s, 唤醒到生效1s
            # 第6波弹坑3-9, 第15波弹坑4-9
            sleep(3.73-1.98-1)
            if (wave == 6):
                N(3,9)
            else (wave == 15):
                N(4,9)
        else:
            # 除以上特殊处理的波次(10/20/6/15)外其他均为95cs预判炮, 落点2-9和5-9
            Pao(2,9)
            Pao(5,9)
            # 第9/19波打完一对炮后还需要额外用炮收尾
            # 在对应波次的地方把pvz.nowPao变量加上额外需要的炮数, 让第10/20波自动发炮时选择的炮位相应地延后
            # 一般第9波打完两炮后还需要4门炮(加上冰瓜IO), 第9波打完两炮后还需要2门炮(自然出怪下)
            if (wave == 9):
                pvz.nowPao += 4
            if (wave == 19):
                pvz.nowPao += 2
        # 每一波操作都要运行到本波刷新以后, 除第20波外通常用的是0.95s和0.55s预判
        # 所以每波至少要延迟0.95s来保证本次循环执行到本波刷新以后再执行下一个循环
        sleep(1)

# 代码只在作为主程序运行时执行
if __name__ == '__main__':
    main()

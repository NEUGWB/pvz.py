# -*- coding: utf-8 -*- 
'''
作者: lmintlcx
日期: 2017-9-26 21:35
---
PE双冰十六炮
节奏 ch6: PPDD|IPP-PP|PPDD|IPP-PP, (6|12|6|12)
视频 https://www.bilibili.com/video/av14877298/
'''

# 导入模块
import pvz
from pvz import *

# 场地, 可选值"DE""NE""PE""FE""RE""ME"
# 场上所有炮的位置列表, 一般以后轮坐标为准
pvz.scene = 'PE'
pvz.paoList = [(3,1),(4,1),(3,3),(4,3),(1,5),(2,5),(3,5),\
(4,5),(5,5),(6,5),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7)]

# 选卡界面选十张卡
# 选择模仿者时`ChooseCard()`函数第三个参数为True
def ChoosingCard():
    ChooseCard(5, 4) # 咖啡豆
    ChooseCard(2, 7) # 寒冰菇
    ChooseCard(2, 7, True) # 模仿者寒冰菇
    ChooseCard(1, 3) # 樱桃
    ChooseCard(3, 2) # 倭瓜
    ChooseCard(1, 4) # 坚果
    ChooseCard(5, 2) # 花盆
    ChooseCard(2, 6) # 胆小菇
    ChooseCard(2, 2) # 阳光菇
    ChooseCard(2, 1) # 小喷菇

# 存冰函数在单独的线程里执行
# 可用存冰位 1-1 2-1 5-1 6-1 1-2 6-2
# 每隔51秒往可用的位置存两个冰, 共存8个
# 中场临时存在1-2 6-2防小偷
# 最后一次存冰放在(wave = 20)里等小偷落靶后再进行
def FillIce():
    Card(2)
    Pnt((1, 1))
    Card(3)
    Pnt((6, 1))
    sleep(51)
    Card(2)
    Pnt((1, 2))
    Card(3)
    Pnt((6, 2))
    sleep(51)
    Card(2)
    Pnt((2, 1))
    Card(3)
    Pnt((1, 2))
    sleep(51)
    Card(2)
    Pnt((1, 1))
    Card(3)
    Pnt((6, 1))

# 点冰, 选咖啡豆后往所有的存冰位点一次
# 一般优先用掉临时存冰位的冰
# 中场有防小偷的需求所以先用掉第1列的冰
def Ice(): 
    Card(1)
    Pnt((1, 1))
    Pnt((2, 1))
    Pnt((5, 1))
    Pnt((6, 1))
    Pnt((1, 2))
    Pnt((6, 2))

# 在r路c列释放樱桃
def A(r, c):
    Card(4)
    Pnt((r, c))


def main():

    print('nowopen %s' % win32gui.GetWindowText(hwnd))
    sleep(4)
    ChoosingCard()
    sleep(0.5)
    LetsRock()
    sleep(0.2)
    Click(320, 400) # 有时候会出现警告窗口需要再点击一到多次YES
    sleep(4)
    
    # 进入游戏场景后开启存冰线程
    fillIce = threading.Thread(target=FillIce, name='FillIceThread')
    fillIce.setDaemon(True) # 后台线程, 主线程停止运行时后台线程同样退出
    fillIce.start()

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
        # 把相同操作的波次写在同一个if分支里
        if (wave == 1) or (wave == 3) or (wave == 5) or (wave == 7) or (wave == 9) \
        or (wave == 10) or (wave == 12) or (wave == 14) or (wave == 16) or (wave == 18):
            # 第1波PPDD, 刷新前0.95s两门预判炮PP
            Pao(2,9)
            Pao(5,9)
            sleep(0.8)
            # 之后接两门延迟炮DD, DD的作用是收撑杆并补刀红眼
            # 根据撸炮帖数据在刷新前0.15s之后发炮可全收撑杆, 即预判之后0.8s
            Pao(2,9)
            Pao(5,9)
            # 由于从点下咖啡豆到寒冰菇生效的时间较长, 第2波的预判冰点冰的操作放在第1波进行
            # 本波波长6s, 本波操作在刷新前0.95s进行, DD操作之前中途累计延时0.8s, 寒冰菇从点下咖啡豆到生效2.98s(唤醒1.98s+生效1s)
            # 采用0.3s预判冰, 即下一波在刷新后0.3s被冻住. 计算可知在DD操作之后(6+0.95-0.8-2.98+0.3)s点下咖啡豆即可实现
            if (wave == 10): 
                # 注意到第10波的预判时间是55cs而不是95cs, 对应第10波的代码`sleep(6+0.95-0.8-2.98+0.3)`要改成`sleep(6+0.55-0.8-2.98+0.3)`
                sleep(6+0.55-0.8-2.98+0.3)
            else:
                sleep(6+0.95-0.8-2.98+0.3)
            Ice() # 点冰
            # 运行到第9/19波时要额外留出一定的炮数手动收尾并给pvz.nowPao变量加上对应的炮数(这里是算好时间自动发炮收尾)
            if (wave == 9):
                sleep(2.98-0.2-0.95)
                Pao(2,9)
                Pao(5,9)
                sleep(12+0.95-3.73-2)
                Pao(2,9)
                Pao(5,9)
        elif (wave == 2) or (wave == 4) or (wave == 6) or (wave == 8) \
        or (wave == 11) or (wave == 13) or (wave == 15) or (wave == 17) or (wave == 19):
            # 第2波IPP-PP, 刷新前0.95s两门热过渡炮PP, 为了只消灭本波矿工冰车避免炸到刚冒头的其他僵尸将落点左移到8.5列
            Pao(2,8.5)
            Pao(5,8.5)
            # 本波波长是由激活炮的时机决定的, 波长12s, 预判0.95s, 热过渡PP操作之前累计延时0, 玉米炮发射后3.73s生效, 激活到下一波刷出2s
            # 计算得知在热过渡PP操作之后(12+0.95-0-3.73-2)s发射激活炮PP即可. 
            sleep(12+0.95-0-3.73-2)
            Pao(2,9)
            Pao(5,9)
            # 运行到第9/19波时要额外留出一定的炮数手动收尾并给pvz.nowPao变量加上对应的炮数(这里是算好时间自动发炮收尾)
            if (wave == 19):
                sleep(3.73+2-0.95)
                Pao(2,9)
                Pao(5,9)
                sleep(0.8)
                Pao(2,9)
                Pao(5,9)
                sleep(6-0.8)
                Pao(2,9)
                Pao(5,9)
        elif (wave == 20):
            # 第20波预判150cs炸珊瑚, 0.9s后两炮射向前场
            Pao(4,7)
            sleep(0.9)
            Pao(2,9)
            Pao(5,9)
            sleep(1)
            Pao(2,9)
            Pao(5,9)
            Pao(2,9)
            Pao(5,9)
            sleep(1)
            Pao(2,9)
            sleep(3.73-0.98)
            # 樱桃代一炮
            A(5, 9)
            sleep(0.1)
            # 等小偷落靶确定安全后再往2-1 5-1存两个冰
            Card(2)
            Pnt((5, 1))
            Card(3)
            Pnt((2, 1))
        else:
            pass
        # 每一波都要加个延时保证能运行到本波刷新点以后
        sleep(1)

if __name__ == '__main__':
    main()

import pvz
from pvz import *

print('nowopen %s' % win32gui.GetWindowText(hwnd)) # 打印窗口标题
sleep(2)
while True:
    print("shop")
    for i in range(0, 5):
        #MoveClick(760, 55) #shop
        MDOWN(760, 55)
        sleep(0.1)
        MUP(760, 55)
        sleep(0.5)
    sleep(1)
    for i in range(0,10):
        print("buy", i)
        Click(480, 355) #tree food
        sleep(0.2)
        MoveClick(315,395) #yes
        sleep(0.2)

    sleep(1)
    for i in range(0, 5):
        MoveClick(440, 555) #back
        sleep(0.5)

    sleep(1)
    for i in range(0,10):
        print("tree", i)
        Click(65, 40)
        Click(385, 360)
        sleep(3)

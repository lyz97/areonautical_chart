import turtle as t
from PIL import Image
import win32api, win32con
import math


def plot_scale(times):
    t.left(90)
    t.forward(5)
    t.write('0')
    t.left(180)
    t.forward(5)
    t.left(90)
    num = 1
    for i in range(times):
        t.forward(43)
        t.left(90)
        t.forward(5)
        t.left(90)
        t.penup()
        t.forward(10)
        t.write('{}00m'.format(num))
        num += 1
        t.left(180)
        t.forward(10)
        t.right(90)
        t.pendown()
        t.forward(5)
        t.left(90)

# a = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得屏幕分辨率X轴
# b = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 获得屏幕分辨率Y轴
# print(a, b)
# t.write('1200×30', font=('Times New Rome', 40, 'normal'))
t.bgcolor('white')
plot_scale(4)
ts = t.getscreen()

t.hideturtle()

t.mainloop()

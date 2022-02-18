import turtle as t
from PIL import Image
import win32api, win32con
import math
from matplotlib import pyplot as plt
from pylab import *
pi = 9
arr = 170  # 箭头角度
t.left(90)
t.forward(120)  # 第一个箭头长度

t.begin_fill()
t.left(arr)
t.forward(20)
t.left(270-arr)
t.forward(7)
t.left(270-arr)
t.forward(20)
t.end_fill()

t.penup()
t.forward(5)
t.left(90)
t.forward(2)
t.pendown()
t.write('N', font=('NEW TIMES ROME', 15, 'normal'))


t.penup()
t.seth(90)
t.goto(0, 0)
t.pendown()
t.left(pi)
t.forward(100)  # 第二个箭头长度
t.begin_fill()
t.left(arr)
t.forward(20)
t.left(270-arr)
t.forward(7)
t.left(270-arr)
t.forward(20)
t.end_fill()

t.hideturtle()

t.mainloop()

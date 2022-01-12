import re
from matplotlib import pyplot as plt
from PIL import Image
import turtle as t
import math
import pandas as pd
import os

index_print = ['四字码']


def get_data(f):
    df = pd.read_csv(f)
    a, b = df.shape
    # print(df)
    return df


def process_data(df):
    # ------------------------------------机场标高----------------------------------------------
    df1 = df['机场标高'].str.split('/', expand=True)
    df1.columns = ['机场标高/m', '机场标高/ft']
    df1 = df1['机场标高/m'].str.replace('m', '').astype('float')
    df['机场标高'] = df1

    # ------------------------------------跑道尺寸----------------------------------------------
    df2 = df['跑道尺寸'].str.extract(r'(\d+)(.\d+)', expand=False)
    df2['跑道尺寸'] = df2.apply(lambda x: x[0] + x[1], axis=1)
    df['跑道尺寸'] = df2['跑道尺寸']

    # ------------------------------------磁偏角-----------------------------------------------
    df3 = df['磁偏角'].str.extract(r'(\d+[.]?\d*)', expand=False)
    df['磁偏角'] = df3.astype('float')

    # -----------------------------------升降带-----------------------------------------------
    df4 = df['升降带'].str.extract(r'(\d+.).(\d+)')
    df4['升降带'] = df2.apply(lambda x: x[0] + x[1], axis=1)
    df['升降带'] = df4['升降带']

    return df


def plot_data(info):
    global index_print

    # 对数据库中的列名进行分别打印

    # ---------------------------表面类型和跑道尺寸-----------------------------
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.)
    ax.axis('off')

    surface_scale = str(info['跑道尺寸']) + '   ' + str(info['表面类型'])
    plt.title(str(surface_scale))

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '跑道尺寸和表面类型'), format='eps',
                dpi=1000)
    plt.close()
    # ---------------------------跑道长度-----------------------------
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.)
    ax.axis('off')

    plt.title(str(info['跑道长度']))

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '跑道长度'), format='eps', dpi=1000)

    plt.close()

    # ---------------------------升降带-----------------------------
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.)
    ax.axis('off')

    strip = 'Strip  ' + str(info['升降带'])
    plt.title(strip)

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '升降带'), format='eps', dpi=1000)

    plt.close()

    # ---------------------------机场标高-----------------------------
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.)
    ax.axis('off')

    try:
        elev = 'ELEV  ' + str(int(info['机场标高']))
        plt.title(elev)
    except ValueError:
        pass

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '机场标高'), format='eps', dpi=1000)

    plt.close()

    # ---------------------------跑道号1-----------------------------
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.)
    ax.axis('off')

    try:
        plt.title(str(int(info['跑道号1'])))
    except ValueError:
        pass

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '跑道号1'), format='eps', dpi=1000)

    plt.close()

    for index_ in index_print:
        rotation_rate = 0

        # image = Image.new(mode='RGBA', size=(400, 400))
        # plt.imshow(image)
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0.)

        # ax.scatter([1, 1], [1, 1])
        ax.axis('off')
        # plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.rcParams['axes.unicode_minus'] = False
        # ax.text(1, 1, text, fontsize=12, color="black", style="italic", weight="bold",
        #         verticalalignment='center', horizontalalignment='right', rotation=rotation_rate)

        plt.title(str(int(info['{}'.format(index_)])))

        plt.savefig('../pythonProject/airport_data/{}/test{}.eps'.format(info['机场名'], index_), format='eps', dpi=1000)
        plt.close()


def plot_runway(name, runway_scale, times, rotate, length, runway_path):
    """

    :param runway_path: 保存路径
    :param length: 虚线宽度
    :param runway_scale: 跑道尺寸，如'450x20'
    :param rotate: 跑道旋转度数

    :return:
    """
    t.reset()
    t.hideturtle()
    t.tracer(False)  # 不显示画图过程
    t.bgcolor('white')

    # 确认缩放倍数
    try:
        a, b = runway_scale.split('×')
        a = float(a) / (1.1 ** times)
        b = float(b) / (1.1 ** times)
    except AttributeError:
        print('{}信息缺失'.format(name))
        return

    t.fillcolor('black')
    t.setup(1000, 600, 0, 0)
    t.pensize(1)
    t.pencolor("black")
    t.begin_fill()
    t.left(360 - rotate + 90)  # 箭头左转rotate度
    t.penup()  # 抬起画笔
    t.goto(0, 0)  # 去坐标（70,0）
    t.pendown()  # 放下画笔

    # --------------------------------画矩形---------------------------
    t.forward(a / 2)  # 前进a像素
    t.left(90)  # 箭头左转90度
    t.forward(b)  # 前进b像素
    t.left(90)  # 箭头左转90度
    t.forward(a)  # 前进a像素
    t.left(90)  # 箭头左转90度
    t.forward(b)  # 前进b像素
    t.left(90)
    t.forward(a / 2)
    t.end_fill()

    # --------------------------------画虚线-----------------------------
    def dotted_line(l):
        for i in range(math.ceil(l / 6)):
            t.forward(3)
            t.penup()
            t.forward(3)
            t.pendown()

    def center_line(l):
        for i in range(math.ceil(l/14)):
            t.forward(7)
            t.penup()
            t.forward(7)
            t.pendown()

    # t.forward(length)
    # t.left(90)
    # t.forward(a)
    # t.left(90)
    # t.forward(b + 2 * length)
    # t.left(90)
    # t.forward(a)
    # t.left(90)
    # t.forward(b + 2 * length)
    t.left(180)
    t.penup()
    t.forward(a / 2)
    t.left(90)
    t.pendown()

    dotted_line(length)

    t.left(90)
    dotted_line(a)
    t.left(90)

    # 防止四舍五入后虚线不一样长
    dotted_line(length)
    t.penup()
    t.forward(b)
    t.pendown()
    dotted_line(length)

    t.left(90)
    dotted_line(a)
    t.left(90)

    # 防止四舍五入后虚线不一样长
    dotted_line(length)

    # 跑道中线
    t.penup()
    t.forward(b/2)
    t.pendown()
    t.left(90)
    t.pensize(2)
    t.pencolor('white')
    center_line(a)

    t.hideturtle()
    ts = t.getscreen()
    ts.getcanvas().postscript(file=runway_path)

    # t.done()


def evaluate_size(runway_length, alpha):
    """

    :param runway_length: 跑道长度
    :param alpha: 跑道角度
    :return: 缩小几倍
    """

    try:
        runway_length = float(runway_length)
    except AttributeError:
        return

    a = math.fabs(runway_length * math.sin(math.radians(alpha)))
    b = math.fabs(runway_length * math.cos(math.radians(alpha)))

    times = 1
    while (a > 500) or (b > 500):
        a = a / 1.1
        b = b / 1.1
        times += 1

    return times


def plot_scale(ture_distance_per_pix, save_path):
    ture_distance_per_centimetre = 43 * ture_distance_per_pix
    number_of_grid = 4

    t.reset()
    t.hideturtle()
    t.tracer(False)  # 不显示画图过程

    t.left(90)
    t.forward(5)
    t.write('0')
    t.left(180)
    t.forward(5)
    t.left(90)
    num = 1
    for i in range(number_of_grid):
        t.forward(43)
        t.left(90)
        t.forward(5)
        t.left(90)
        t.penup()
        t.forward(10)
        t.write('{}m'.format(ture_distance_per_centimetre))
        num += 1
        t.left(180)
        t.forward(10)
        t.right(90)
        t.pendown()
        t.forward(5)
        t.left(90)

    t.hideturtle()
    ts = t.getscreen()
    ts.getcanvas().postscript(file=save_path)


if __name__ == '__main__':
    filename = 'D:/ZY数据.csv'
    data = process_data(get_data(filename))
    pic = '../pythonProject/[3.1]阿荣通用机场.jpg'
    if os.path.isdir('../pythonProject/airport_data'):
        pass
    else:
        os.mkdir('../pythonProject/airport_data')

    # 转置
    # data = pd.DataFrame(data.values.T, index=data.columns, columns=data.index)
    # data.to_csv('data_pro.csv', encoding='utf_8_sig')
    # print(data)

    # for index, row in data.iterrows():
    #     print(index)

    for row_index, row in data.iterrows():
        if os.path.isdir('../pythonProject/airport_data/{}'.format(row['机场名'])):
            pass
        else:
            os.mkdir('../pythonProject/airport_data/{}'.format(row['机场名']))
        plot_data(row)
        # for key, item in row.items():
        #     print(key)
        runway_path = '../pythonProject/airport_data/{}/runway_pic.eps'.format(row['机场名'])
        runway_scale = row['跑道尺寸']
        rotate = row['真方位1']

        times = evaluate_size(row['跑道长度'], row['真方位1'])
        plot_runway(row['机场名'], runway_scale, times, rotate, 20, runway_path)
        scaling_bar_save_path = '../pythonProject/airport_data/{}/scaling.eps'.format(row['机场名'])
        plot_scale(times, scaling_bar_save_path)

    # plot_data(pic)

    # plot_runway('480x20', 30, (-170, -170), 20)

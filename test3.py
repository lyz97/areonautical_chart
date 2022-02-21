import re
from matplotlib import pyplot as plt
from PIL import Image
import turtle as t
import math
import pandas as pd
import os
import time
import plot_PCN


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
    df4['升降带'] = df4.apply(lambda x: x[0] + x[1], axis=1)
    df['升降带'] = df4['升降带']

    return df


def plot_data(info):
    """
    对数据库中的所有信息分别写进可编辑的.eps文件

    :param info: 一个机场的所有相关信息
    :return:
    """

    if info['真方位1'] < 180:
        rotation_rate = 360 - info['真方位1'] + 90
    elif info['真方位1'] > 180:
        rotation_rate = 360 - info['真方位1'] + 90 + 180

    # 打印的标题距离图片的上方的距离
    top_dis = 0.15

    # ---------------------------表面类型和跑道尺寸-----------------------------
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.)
    ax.axis('off')

    surface_scale = str(info['跑道尺寸']) + '   ' + str(info['表面类型'])

    # 防止出现显示不全的情况
    plt.gcf().subplots_adjust(top=top_dis)

    plt.title(str(surface_scale), rotation=rotation_rate)

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '跑道尺寸和表面类型'), format='eps',
                dpi=1000)
    plt.close()
    # ---------------------------跑道长度-----------------------------
    # fig, ax = plt.subplots()
    # fig.patch.set_alpha(0.)
    # ax.axis('off')
    #
    # # 防止出现显示不全的情况
    # plt.gcf().subplots_adjust(top=top_dis)
    #
    # plt.title(str(info['跑道长度']), rotation=rotation_rate)
    #
    # plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '跑道长度'), format='eps', dpi=1000)
    #
    # plt.close()

    # ---------------------------升降带-----------------------------
    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_alpha(0.)
    ax.axis('off')

    strip = 'Strip  ' + str(info['升降带'])

    # 防止出现显示不全的情况
    plt.gcf().subplots_adjust(top=top_dis)

    plt.title(strip, rotation=rotation_rate, fontsize='xx-large', fontweight='heavy')

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '升降带'), format='eps', dpi=1000)

    plt.close()

    # ---------------------------机场标高-----------------------------
    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_alpha(0.)
    ax.axis('off')

    try:
        elev = 'ELEV  ' + str(int(info['机场标高']))

        # 防止出现显示不全的情况
        plt.gcf().subplots_adjust(top=top_dis)

        plt.title(elev, rotation=rotation_rate, fontweight='heavy')
    except ValueError:
        pass

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '机场标高'), format='eps', dpi=1000)

    plt.close()

    # ---------------------------机场标高-----------------------------
    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_alpha(0.)
    ax.axis('off')

    try:
        # 防止出现显示不全的情况
        plt.gcf().subplots_adjust(top=top_dis)

        plt.title(str(info['真方位1']) + '°', rotation=rotation_rate)
    except ValueError:
        pass

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '真方位1'), format='eps', dpi=1000)

    plt.close()

    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_alpha(0.)
    ax.axis('off')

    try:
        # 防止出现显示不全的情况
        plt.gcf().subplots_adjust(top=top_dis)

        plt.title(str(info['真方位2']) + '°', rotation=rotation_rate)
    except ValueError:
        pass

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '真方位2'), format='eps', dpi=1000)

    plt.close()

    # ---------------------------跑道号-----------------------------
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.)
    ax.axis('off')

    try:
        # 防止出现显示不全的情况
        plt.gcf().subplots_adjust(top=top_dis)

        if int(info['跑道号1']) < 10:
            codes = '0' + str(int(info['跑道号1']))
        elif int(info['跑道号1']) > 10:
            codes = str(int(info['跑道号1']))

        plt.title(codes, rotation=rotation_rate + 90 + 180, fontsize='xx-large', fontweight='heavy')
    except ValueError:
        pass

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '跑道号1'), format='eps', dpi=1000)

    plt.close()

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.)
    ax.axis('off')

    try:
        # 防止出现显示不全的情况
        plt.gcf().subplots_adjust(top=top_dis)

        if int(info['跑道号2']) < 10:
            codes = '0' + str(int(info['跑道号2']))
        elif int(info['跑道号2']) > 10:
            codes = str(int(info['跑道号2']))

        plt.title(codes, rotation=rotation_rate + 90, fontsize='xx-large', fontweight='heavy')
    except ValueError:
        pass

    plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '跑道号2'), format='eps', dpi=1000)

    plt.close()

    # ---------------------------四字码-----------------------------
    # fig, ax = plt.subplots()
    # fig.patch.set_alpha(0.)
    # ax.axis('off')
    #
    # try:
    #     # 防止出现显示不全的情况
    #     plt.gcf().subplots_adjust(top=top_dis)
    #
    #     plt.title(str(info['四字码']))
    # except ValueError:
    #     pass
    #
    # plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '四字码'), format='eps', dpi=1000)
    #
    # plt.close()


    # ---------------------------说明-----------------------------
    # fig, ax = plt.subplots(figsize=(10, 10))
    # fig.patch.set_alpha(0.)
    # ax.axis('off')
    # # 中文
    #
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    #
    # plt.title('标高和跑道长度为米，方位为磁方位\n RWY: PCN 45/R/B/W/T', fontdict={'fontsize': 35})
    #
    # plt.savefig('../pythonProject/airport_data/pic.png', format='png')
    # plt.close()

    # t.write('标高和跑道长宽为米，方位为磁方位', move=False, align="left", font=("Arial", 8, "normal"))
    #
    # t.hideturtle()
    # ts = t.getscreen()
    # save_path = '../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '说明')
    # ts.getcanvas().postscript(file=save_path)

    # for index_ in index_print:
    #     rotation_rate = 0
    #
    #     # image = Image.new(mode='RGBA', size=(400, 400))
    #     # plt.imshow(image)
    #     fig, ax = plt.subplots()
    #     fig.patch.set_alpha(0.)
    #
    #     # ax.scatter([1, 1], [1, 1])
    #     ax.axis('off')
    #     # plt.rcParams['font.sans-serif'] = ['SimHei']
    #     # plt.rcParams['axes.unicode_minus'] = False
    #     # ax.text(1, 1, text, fontsize=12, color="black", style="italic", weight="bold",
    #     #         verticalalignment='center', horizontalalignment='right', rotation=rotation_rate)
    #
    #     plt.title(str(int(info['{}'.format(index_)])))
    #
    #     plt.savefig('../pythonProject/airport_data/{}/test{}.eps'.format(info['机场名'], index_), format='eps', dpi=1000)
    #     plt.close()

    # ------------------------------------磁偏角-------------------------------
    try:
        pi = int(info['磁偏角'])
        if pi < 3:
            pi = 3
        t.reset()
        t.hideturtle()
        t.tracer(False)  # 不显示画图过程

        arr = 170  # 箭头角度
        t.left(90)
        t.forward(120)  # 第一个箭头长度
        t.begin_fill()
        t.left(arr)
        t.forward(20)
        t.left(270 - arr)
        t.forward(7)
        t.left(270 - arr)
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
        t.left(270 - arr)
        t.forward(7)
        t.left(270 - arr)
        t.forward(20)
        t.end_fill()

        t.hideturtle()
        ts = t.getscreen()
        save_path = '../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '磁偏角')
        ts.getcanvas().postscript(file=save_path)

        fig, ax = plt.subplots()
        fig.patch.set_alpha(0.)
        ax.axis('off')

        try:
            # 防止出现显示不全的情况
            plt.gcf().subplots_adjust(top=top_dis)

            plt.title('VAR ' + str(int(info['磁偏角'])) + '° W', rotation=pi-90)
        except ValueError:
            pass

        plt.savefig('../pythonProject/airport_data/{}/{}.eps'.format(info['机场名'], '磁偏角数据'), format='eps', dpi=1000)

        plt.close()

    except ValueError:
        pass


def plot_runway(name, runway_scale, times, rotate, strip_scale, runway_path):
    """

    :param name: 机场名称
    :param times: 缩放倍数：1.1**times
    :param runway_path: 保存路径
    :param strip_scale: 升降带尺寸
    :param runway_scale: 跑道尺寸，如'450x20'
    :param rotate: 跑道旋转度数

    :return:
    """
    def dotted_line(l):
        for i in range(math.ceil(l / 10)):
            t.forward(5)
            t.penup()
            t.forward(5)
            t.pendown()

    def complete_dot(l):
        for i in range(math.ceil(l/10)):
            t.forward(10)

    t.reset()
    t.hideturtle()
    t.tracer(False)  # 不显示画图过程
    t.bgcolor('white')

    # 确认缩放倍数
    try:
        a, b = runway_scale.split('×')
        a = math.ceil(float(a) / (1.1 ** times))
        b = math.ceil(float(b) / (1.1 ** times))

        m, n = strip_scale.split('×')
        m = float(m) / (1.1 ** times)
        n = float(n) / (1.1 ** times)
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
    complete_dot(a / 2)  # 前进a像素
    t.left(90)  # 箭头左转90度
    complete_dot(b)  # 前进b像素
    t.left(90)  # 箭头左转90度
    complete_dot(a)  # 前进a像素
    t.left(90)  # 箭头左转90度
    complete_dot(b)  # 前进b像素
    t.left(90)
    complete_dot(a / 2)
    t.end_fill()

    # -----------------------------升降带-----------------------------
    x = (m - a) / 2
    y = (n - b) / 2

    x = math.ceil(x)
    y = math.ceil(y)

    t.left(180)
    t.penup()
    complete_dot(a/2)
    complete_dot(x)
    t.left(90)
    t.pendown()
    dotted_line(y)
    t.left(90)

    # 分开画防止四舍五入
    dotted_line(x)
    dotted_line(a)
    dotted_line(x)
    t.left(90)
    dotted_line(y)
    # dotted_line(b)
    dotted_line(b)
    dotted_line(y)
    t.pensize(1)
    t.left(90)
    dotted_line(x)
    dotted_line(a)
    dotted_line(x)
    t.left(90)
    dotted_line(y)
    dotted_line(b)

    # ------------------------跑道中线------------------------
    # t.penup()
    # t.forward(b/2)
    # t.pendown()
    # t.left(90)
    # t.pensize(2)
    # t.pencolor('white')
    # center_line(a)

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

    while (a < 300) and (b < 300):
        a = a * 1.1
        b = b * 1.1
        times -= 1

    return times


def plot_scale(ture_distance_per_pix, save_path):
    ture_distance_per_centimetre = int(43 * (1.1 ** ture_distance_per_pix))
    number_of_grid = 4

    t.reset()
    t.hideturtle()
    t.tracer(False)  # 不显示画图过程

    t.left(90)
    t.forward(5)
    t.write('0', font=('宋体', 12, 'normal'))
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
        t.write('{}m'.format(ture_distance_per_centimetre * num), font=('NEW TIMES ROME', 12, 'normal'))
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
    filename = 'D:/ZY数据1.csv'
    data = process_data(get_data(filename))
    # pic = '../pythonProject/[3.1]阿荣通用机场.jpg'
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

        plot_PCN.plot_PCN(row['机场名'], row['机坪PCN值'])

    plt.rc('font', family='Times New Roman')
    for row_index, row in data.iterrows():
        plot_data(row)
        # for key, item in row.items():
        #     print(key)
        runway_path = '../pythonProject/airport_data/{}/跑道.eps'.format(row['机场名'])
        runway_scale = row['跑道尺寸']
        rotate = row['真方位1']

        times = evaluate_size(row['跑道长度'], row['真方位1'])
        strip_scale = row['升降带']
        plot_runway(row['机场名'], runway_scale, times, rotate, strip_scale, runway_path)
        scaling_bar_save_path = '../pythonProject/airport_data/{}/比例尺.eps'.format(row['机场名'])
        plot_scale(times, scaling_bar_save_path)

    # plot_data(pic)

    # plot_runway('480x20', 30, (-170, -170), 20)

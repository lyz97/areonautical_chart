from PIL import ImageTk, Image
import tkinter
from tkinter import ttk, filedialog
import math


class PenData(object):
    def __init__(self):
        self.color = 'blue'
        self.mouse_position_x = None
        self.mouse_position_y = None
        self.is_dragging = False


def main():
    global img
    global list_points
    global dis_points
    pen_data = PenData()

    root = tkinter.Tk()
    root.geometry('1200x700')

    filename = '../pythonProject/airport/阿荣通用机场.jpg'
    im = Image.open(filename)
    width, height = im.size
    img = im.resize((900, int(900 / width * height)))

    main_frame = ttk.Frame(root, width=1000, height=int(1000 / width * height))
    main_frame.grid()

    filename_list = filename.split('/')
    for file in filename_list:
        if '.jpg' in file:
            file_name = file.strip('.jpg')

    label = ttk.Label(main_frame, text=file_name, font=10)
    label.grid(row=1, rowspan=1)


    # Make a tkinter.Canvas on a Frame.
    # Note that Canvas is a tkinter (NOT a ttk) class.

    canvas = tkinter.Canvas(main_frame, width=900, height=int(900 / width * height))
    canvas.image = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=canvas.image, anchor='nw')
    canvas.grid()

    son_frame = tkinter.Frame(main_frame)
    son_frame.grid(row=3, column=0, sticky=tkinter.NW)

    son1_frame = tkinter.Frame(main_frame)
    son1_frame.grid(row=3, column=0, sticky=tkinter.N)

    text1 = tkinter.Text(son1_frame, width=60, height=10)
    text1.grid()

    def clean_t():
        text1.delete(0.0, 'end')

    btn04 = ttk.Button(son1_frame, text='清空文本', command=clean_t)
    btn04.grid()

    text = tkinter.Text(main_frame, width=50, height=30)
    text.grid(row=2, column=1)

    entry1 = tkinter.Entry(son_frame)
    entry1.grid()

    def writing(event):
        t = entry1.get()
        canvas.create_text(event.x, event.y, text=t)


    # scroll = tkinter.Scrollbar()
    # # 放到窗口的右侧, 填充Y竖直方向
    # scroll.grid(row=2, column=4)
    #
    # # 两个控件关联
    # scroll.config(command=text.yview)
    # text.config(yscrollcommand=scroll.set)

    # Make callbacks for mouse events.
    canvas.bind('<Button-1>', lambda event: (left_mouse_click(main_frame, event), text.delete('1.0', 'end'),
                                             write_coordinate()))
    canvas.bind('<B1-Motion>',
                lambda event: left_mouse_drag(event, pen_data))
    canvas.bind('<B1-ButtonRelease>',
                lambda event: left_mouse_release(pen_data))  # @UnusedVariable
    canvas.bind('<Button-3>', lambda event: writing(event))

    def write_coordinate():
        for point in list_points:
            if '距离' in point:
                text.insert('insert', point)
                text.insert('insert', '\n')
            elif '距离' not in point:
                t = str(point)
                text.insert('insert', t)

    def clean_canvas():
        global img
        list_points.clear()
        text.delete('1.0', 'end')
        img = img.resize((900, int(900 / width * height)))
        canvas.image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')
        canvas.grid()

    btn02 = ttk.Button(son_frame, text='清空画布', command=clean_canvas)
    btn02.grid(sticky=tkinter.NE)

    def getfile():
        global img

        file_path = filedialog.askopenfilename(title='', filetypes=[('JPG', '*.jpg'), ('All Files', '*')])
        img = Image.open(file_path)
        width1, height1 = img.size
        img = img.resize((900, int(900 / width1 * height1)))
        canvas.image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')
        canvas.grid()

        filename_list = file_path.split('/')
        for file in filename_list:
            if '.jpg' in file:
                file_name = file.strip('.jpg')
        label['text'] = file_name
        # label = ttk.Label(main_frame, text=file_name, font=10)
        # label.grid(row=1, rowspan=1)

    btn01 = ttk.Button(son_frame, text='选择文件', command=getfile)
    btn01.grid(sticky=tkinter.NE)

    def clean_text():
        entry1.delete(0, 'end')

    btn03 = ttk.Button(son_frame, text='清空输入', command=clean_text)
    btn03.grid(row=0, column=2)

    root.mainloop()


def left_mouse_click(frame, event):
    global odd
    global x_last
    global y_last

    odd += 1
    canvas = event.widget
    scale = 5
    canvas.create_oval(event.x - scale, event.y - scale,
                       event.x + scale, event.y + scale,
                       fill='red', width=1)

    if odd % 2 == 0:
        canvas.create_line(event.x, event.y, x_last, y_last, fill='red', width=2, dash=(4, 4))
        distance = math.sqrt((event.x - x_last)**2 + (event.y - y_last)**2)
        get_coordinate(frame, event, distance)
        x_last = None
        y_last = None

    elif odd % 2 != 0:
        get_coordinate(frame, event, dis=0)

    x_last = event.x
    y_last = event.y


def left_mouse_drag(event, data):
    # data.mouse_position_x and _y keep track of the PREVIOUS mouse
    # position while we are dragging.
    canvas = event.widget
    if data.is_dragging:
        canvas.create_line(data.mouse_position_x, data.mouse_position_y,
                           event.x, event.y,
                           fill=data.color, width=2)
    else:
        data.is_dragging = True  # Start dragging

    data.mouse_position_x = event.x
    data.mouse_position_y = event.y


def left_mouse_release(data):
    data.is_dragging = False


def get_coordinate(frame, event, dis):
    global list_points
    global dis_points
    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="yellow")
    if dis:
        coordinate = '({}, {})'.format(event.x, event.y)
        # label1 = ttk.Label(frame, text=coordinate, style="BW.TLabel")
        # label1.grid(row=0, column=12)
        list_points.append((event.x, event.y))
        a = '{:.2f}'.format(dis)
        list_points.append('距离:' + a)
        dis_points.append(dis)

    elif not dis:
        coordinate = '({}, {})'.format(event.x, event.y)
        # label1 = ttk.Label(frame, text=coordinate, style="BW.TLabel")
        # label1.grid(row=0, column=12)
        list_points.append((event.x, event.y))


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
if __name__ == '__main__':
    list_points = []
    dis_points = []
    odd = 0
    x_last = 0
    y_last = 0
    main()
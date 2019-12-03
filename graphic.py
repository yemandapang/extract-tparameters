# *_*coding:utf-8 *_*
from tkinter import *
import random
import sys
import os
import easygui as g
sys.path.append("./para")
from PIL import Image, ImageTk

#  批处理
def run1():
    batch = 100
    send_dir = g.diropenbox('选择文件目录', '浏览文件夹', 'C:/Users/Administrator/Desktop')
    print(send_dir)
    start = 'the send_dir is '
    second = 'the batch is  '
    txt.insert(END, start)#   显示详情
    txt.insert(END, send_dir)   # 显示weight
    txt.insert(END, '\n')   # 换行
    txt.insert(END, second)#   显示详情
    txt.insert(END, str(batch))#   显示详情
    txt.insert(END, '\n')   # 换行
    txt.insert(END, '\n')  # 换行

#  单张
def run2():
    batch = 1
    receive_dir = g.diropenbox('选择文件目录', '浏览文件夹', 'C:/Users/Administrator/Desktop')
    print(receive_dir)
    start = 'the receive_dir is '
    second = 'the batch is  '
    txt.insert(END, start)#   显示详情
    txt.insert(END, receive_dir)   # 显示weight
    txt.insert(END, '\n')   # 换行
    txt.insert(END, second)#   显示详情
    txt.insert(END, str(batch))#   显示详情
    txt.insert(END, '\n')   # 换行
    txt.insert(END, '\n')  # 换行

#  发送数据给FPGA
def run3():
    i = 0
    while len(os.listdir(receive_dir)) != 100:
        i += 1
    i = 0
    ii = random.randint(0, len(os.listdir(receive_dir))-1)
    for r in os.listdir(receive_dir):
        i += 1
        if i == ii:
            for s in os.listdir(send_dir):
                if r == s:
                    # 显示fpga计算的原始图片
                    lb1 = Label(root, text='原始图片  ')
                    lb1.place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.1)
                    image_s = Image.open(os.path.join(send_dir, s))
                    image_s = ImageTk.PhotoImage(image=image_s)
                    lb2 = Label(image=image_s)
                    lb2.place(relx=0.1, rely=0.6)

                    # 显示fpga计算的预测图片
                    lb3 = Label(root, text='预测显示  ')
                    lb3.place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.1)
                    image_r = Image.open(os.path.join(receive_dir, r))
                    image_r = ImageTk.PhotoImage(image=image_r)
                    lb4 = Label(image=image_r)
                    lb4.place(relx=0.5, rely=0.6)
            break

root = Tk()
root.geometry('800x800')
root.title('上位机')

receive_dir = '/home/dapang/workspace/新建文件夹'
send_dir = ''
# inp1 = Entry(root)
# inp1.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.1)
# inp2 = Entry(root)
# inp2.place(relx=0.6, rely=0.1, relwidth=0.3, relheight=0.1)

# 批处理目录           run1()
btn1 = Button(root, text='批处理', command=run1)
btn1.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.1)

# 接收测试结果的目录            run2()
btn2 = Button(root, text='接收结果', command=run2)
btn2.place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.1)

# 发送目录给FPGA  run3()
btn3 = Button(root, text='计算', command=run3)
btn3.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.1)

# 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框
txt = Text(root)
txt.place(relx=0.1, rely=0.3, relwidth=0.8,relheight=0.1)

root.mainloop()
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key
import threading
import time


# 创建鼠标控制器
mouse = Controller()


class AutoClicker:
    def __init__(self):
        self.is_running = False
        self.button = None
        self.mode = None  # 'click' or 'hold'
    def start_clicking(self, button, interval, mode):
        self.is_running = True
        self.button = button
        if mode == 'hold':
            mouse.press(button)  # 按住鼠标键
            while self.is_running:
                time.sleep(1)
            mouse.release(button)   # 按住状态下的间隔
        elif mode == 'click':
            while self.is_running:
                mouse.click(button)  # 点击
                time.sleep(interval)  # 点击间隔
    def stop_clicking(self):
        self.is_running = False


def toggle_clicking():
    if auto_clicker.is_running:
        button1['bg'] = '#1d9f1a'
        button1['text'] = 'F4开始'
        auto_clicker.stop_clicking()
    else:
        button1['bg'] = '#b13b12'
        button1['text'] = 'F4中止'
        button = Button.left if left_var.get() else Button.right
        interval = float(interval_entry.get())
        mode = mode_var.get()  # 获取选择的模式
        auto_clicker_thread = threading.Thread(target=auto_clicker.start_clicking, args=(button, interval, mode))
        auto_clicker_thread.daemon = True
        auto_clicker_thread.start()


def on_press(key):
    global con_start
    if con_start:
        if key == Key.f4:  
            toggle_clicking()
        elif key == Key.f6: 
            choice1['state'] = NORMAL
            choice2['state'] = NORMAL
            choice3['state'] = NORMAL
            choice4['state'] = NORMAL
            button2['bg'] = '#1a9f9d'
            button2['text'] = '点击启动'
            button2['state'] = NORMAL
            interval_entry.config(state='normal')
            if auto_clicker.is_running:
                toggle_clicking()
            button1['bg'] = '#808080'
            con_start = False

# 控制输入为正float
def validate_input(new_value):
    if new_value == "":
        return True
    elif new_value == "-":
        return False
    try:
        float(new_value)
        return True
    except ValueError:
        return False


# 输入信息保存
def write():
    with open('click_1.txt', 'w') as file:
        file.write(interval_entry.get())

# 输入错误提示
def display_message():
    label.config(text="请先输入间隔,且不为0",font=("微软雅黑", 8), fg='#b13b12')
    label.place(x=80, y=40)
    root.after(2000, hide_message)


# 隐藏
def hide_message():
    label.place_forget()

# 主开关
con_start = False
def start():
    if interval_entry.get() == "":
        display_message()
        return
    write()
    global con_start
    interval_entry.config(state='disabled')
    choice1['state'] = DISABLED
    choice2['state'] = DISABLED
    choice3['state'] = DISABLED
    choice4['state'] = DISABLED
    button1['bg'] = '#1d9f1a'
    button2['bg'] = '#b13b12'
    button2['text'] = 'F6停止线程'
    button2["state"] = DISABLED
    con_start = True


# 创建主界面
root = tk.Tk()
root.title("鼠标连点器")
root.geometry('260x190')

# 创建 AutoClicker 实例
auto_clicker = AutoClicker()

# 创建选择左键或右键的变量
left_var = tk.BooleanVar(value=True)

# 创建选择模式的变量
mode_var = tk.StringVar(value='click')  # 默认模式为 'click'

# 读取上次的信息
with open('click_1.txt', 'r') as file:
    content = file.read()
vcmd = (root.register(validate_input), '%P')

# 创建输入框
tk.Label(root, text="点击间隔:").place(x=20, y=20)
interval_entry = tk.Entry(root, validate="key", validatecommand=vcmd, width=15)
interval_entry.place(x=90, y=20)
interval_entry.insert(0, content)  # 默认值

# 创建选择按钮
choice1 =  tk.Radiobutton(root, text="左键", variable=left_var, value=True)
choice1.place(x=60, y=60, relwidth=0.25, height=30)
choice2 = tk.Radiobutton(root, text="右键", variable=left_var, value=False)
choice2.place(x=140, y=60, relwidth=0.25, height=30 )
# 创建选择模式的单选按钮
choice3 =  tk.Radiobutton(root, text="连点", variable=mode_var, value='click')
choice3.place(x=60, y=90, relwidth=0.25, height=30)
choice4 = tk.Radiobutton(root, text="按住", variable=mode_var, value='hold')
choice4.place(x=140, y=90, relwidth=0.25, height=30 )
# 用于提示
label = tk.Label(root, text="")

# 启动键盘监听
listener = Listener(on_press=on_press)
listener.start()

# 功能、提示按钮
button1 = tk.Button(root, text='F4开始', font=("微软雅黑", 12), bg="#808080", relief="flat")
button2 = tk.Button(root, text='点击启动', font=("微软雅黑", 12), bg="#1a9f9d", command=start)
button1.place(x=120, y=155, relwidth=0.4, height=30)
button2.place(x=120, y=125, relwidth=0.4, height=30)
label2 = tk.Label(root, text="F6恢复→", font=("微软雅黑", 12))
label2.pack(pady=10)
label2.place(x=45,y=130)
label3 = tk.Label(root, text="s")
label3.pack(pady=10)
label3.place(x=200,y=20)

# 启动主循环
root.resizable(False, False)
root.mainloop()

from tkinter import *

root = Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
w = 600
h = 450
x = (screenWidth - w) / 2
y = (screenHeight - h) / 2
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def callback():
    print("你好~")


menubar = Menu(root)
menubar.add_command(label="撤销", command=callback)
menubar.add_command(label="重做", command=root.quit)

frame = Frame(root, width=100, height=100)
frame.pack()


def popup(event):
    menubar.post(event.x_root, event.y_root)


frame.bind("<Button-3>", popup)

root.config(menu=menubar)

mainloop()


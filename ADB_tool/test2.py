from tkinter import *

root = Tk()
root.geometry("400x200")


canvas = Canvas(root, width=150, height=150, bg="black", bd=2, relief="ridge")
canvas.place(x=20, y=20)

A = canvas.create_oval(20,20,30,30, outline='grey', fill="grey",tags='A')

B = canvas.create_oval(130,130,140,140, outline='grey', fill="grey",tags='B')

lbl = Label(root)
lbl.place(x=200, y=50, anchor="nw")

def on_enter(e):
    # find the canvas item below mouse cursor
    item = canvas.find_withtag("current")
    # get the tags for the item
    tags = canvas.gettags(item)
    # show it using the label
    lbl.config(text=tags[0])

def on_leave(e):
    # clear the label text
    lbl.config(text="")

for item in (A, B):
    canvas.tag_bind(item, "<Enter>", on_enter)
    canvas.tag_bind(item, "<Leave>", on_leave)

root.mainloop()
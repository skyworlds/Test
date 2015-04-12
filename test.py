#Test file open, save, write, read
from Tkinter import *
import tkFileDialog
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

#init
shape_list=[]

#function must def before it used
def save_draw():
    save_file = tkFileDialog.asksaveasfile(mode='w')
    for index in range(5):
        save_file.write(str(index)+"\n")
    save_file.flush()
    save_file.close()

def open_draw():
    global shape_list
    end = False
    open_file = tkFileDialog.askopenfile(mode='r')
    while not end:
        shape_str = open_file.readline(1024)
        print(shape_str)
        if shape_str == "":
            end = True
        else:
            shape_list.append(shape_str)
    open_file.close()

frame = simplegui.create_frame("test", 1000, 600)
frame.add_button("Save", save_draw)
frame.add_button("Open", open_draw)
root = Tk()
root.withdraw()
frame.start()

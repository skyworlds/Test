# Your Draw. You Can draw, your can play

from Tkinter import *
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import re
import tkFileDialog
import ast

#init
FRAME_WIDTH  = 1000
FRAME_HEIGHT = 600
COLOR_PICKER_WIDTH = 20
COLOR_PICKER_COLUMN = 2 
COLOR_PICKER_ROW = FRAME_HEIGHT / COLOR_PICKER_WIDTH

color_list=["AliceBlue", "AntiqueWhite", "Aqua", "Aquamarine", "Azure", "Beige", "Bisque",\
            "Black", "BlanchedAlmond", "Blue", "BlueViolet", "Brown", "BurlyWood", \
            "CadetBlue", "Chartreuse", "Chocolate", "Coral", "CornflowerBlue", "Cornsilk", \
            "Crimson", "Cyan", "DarkBlue", "DarkCyan", "DarkGoldenRod", "DarkGray", \
            "DarkGreen", "DarkKhaki", "DarkMagenta", "DarkOliveGreen", "DarkOrange", \
            "DarkOrchid", "DarkRed", "DarkSalmon", "DarkSeaGreen", "DarkSlateBlue", \
            "DarkSlateGray", "DarkTurquoise", "DarkViolet", "DeepPink", "DeepSkyBlue",\
            "DimGray", "DodgerBlue", "FireBrick", "FloralWhite", "ForestGreen", "Fuchsia", \
            "Gainsboro", "GhostWhite", "Gold", "GoldenRod", "Gray", "Green", "GreenYellow",\
            "HoneyDew", "HotPink", "IndianRed", "Indigo", "Ivory", "Khaki", "Lavender", \
            "LavenderBlush", "LawnGreen", "LemonChiffon", "LightBlue", "LightCoral", \
            "LightCyan", "LightGoldenRodYellow", "LightGray", "LightGreen", "LightPink", \
            "LightSalmon", "LightSeaGreen", "LightSkyBlue", "LightSlateGray", \
            "LightSteelBlue", "LightYellow", "Lime", "LimeGreen", "Linen", "Magenta", \
            "Maroon", "MediumAquaMarine", "MediumBlue", "MediumOrchid", "MediumPurple", \
            "MediumSeaGreen", "MediumSlateBlue", "MediumSpringGreen", "MediumTurquoise", \
            "MediumVioletRed", "MidnightBlue", "MintCream", "MistyRose", "Moccasin", \
            "NavajoWhite", "Navy", "OldLace", "Olive", "OliveDrab", "Orange", "OrangeRed", \
            "Orchid", "PaleGoldenRod", "PaleGreen", "PaleTurquoise", "PaleVioletRed", \
            "PapayaWhip", "PeachPuff", "Peru", "Pink", "Plum", "PowderBlue", "Purple", \
            "RebeccaPurple", "Red", "RosyBrown", "RoyalBlue", "SaddleBrown", "Salmon", \
            "SandyBrown", "SeaGreen", "SeaShell", "Sienna", "Silver", "SkyBlue", \
            "SlateBlue", "SlateGray", "Snow", "SpringGreen", "SteelBlue", "Tan", "Teal", \
            "Thistle", "Tomato", "Turquoise", "Violet", "Wheat", "White", "WhiteSmoke", \
            "Yellow","YellowGreen"]
shape_list=[]
drag_pos_list=[]
cur_shape="Circle"
play_mode=False
cur_color="Red"
cur_index=0
play_index=0
message=""
mouse_mode="click"
interval=1000
#set shape circle
def shape_circle():
    global cur_shape
    cur_shape = "Circle"

#set shape triangle
def shape_triangle():
    global cur_shape
    cur_shape = "Triangle"

#set shape square
def shape_square():
    global cur_shape
    cur_shape = "Square"

#Next 
def next():
    global cur_index, message
    if cur_index < len(shape_list):
        cur_index+=1
        if cur_index >= len(shape_list):
            show_message("No Next")
    else:
        show_message("No Next")

#Prev
def prev():
    global cur_index,message
    if cur_index >= 0:
        cur_index -= 1
        if cur_index <0:
            show_message("No Prev")
    else:
        show_message("No Prev")

#get square points list
def get_square_points(x, y, length):
    pos=[x,y]
    pos1=pos
    pos2=[pos[0], pos[1] + length]
    pos3=[pos[0] + length, pos[1] + length]
    pos4=[pos[0] + length, pos[1]]
    return [pos1, pos2, pos3, pos4, pos1]

#get triangle points list
def get_triangle_points(x, y, length):
    pos=[x,y]
    pos1=pos
    pos2=[pos[0]-length/2, pos[1]-length*math.sqrt(3)/2]
    pos3=[pos[0]+length/2, pos2[1]]
    return [pos1, pos2, pos3, pos1]

#color rgb reg
def color_rgb_reg(color):
    return re.match(r'#[0-9a-f]{6}', color, re.IGNORECASE)

#get picker points by index
def get_picker_points(index):
    column = index // COLOR_PICKER_ROW
    row = index % COLOR_PICKER_ROW
    pos = [COLOR_PICKER_WIDTH * column, COLOR_PICKER_WIDTH * row]
    return get_square_points(pos[0], pos[1], COLOR_PICKER_WIDTH)

#get color picker index
def get_color_picker_index(pos):
    column = pos[0] // COLOR_PICKER_WIDTH
    row = pos[1] // COLOR_PICKER_WIDTH
    index = column * COLOR_PICKER_ROW + row
    return index

#draw color picker
def draw_color_picker(canvas):
    for index in range(60):
        canvas.draw_polygon(get_picker_points(index), 2, "Black", color_list[index])


#draw 
def draw(canvas):
    global play_mode
    if( not play_mode):
        if(mouse_mode == "click"):
            if ((cur_index >= 0) and (cur_index < len(shape_list))):
                for cur_shape in shape_list[:cur_index+1]:
                    draw_shape(canvas, cur_shape)
        elif(mouse_mode == "drag"):
            for pos in drag_pos_list:
                canvas.draw_point([pos[0], pos[1]], pos[2])
    else:
        if ((play_index >= 0) and (play_index <= cur_index)):
            index = play_index
            while index >= 0:
                cur_shape = shape_list[index]
                draw_shape(canvas, cur_shape)
                index -= 1
    canvas.draw_text(message,[50,50],24,"Red")
    draw_color_picker(canvas)

#draw shape
def draw_shape(canvas, shape):
    if shape["shape"] == "Circle":
        canvas.draw_circle([shape["x"], shape["y"]], 30, 2, "Black", shape["color"])
    elif shape["shape"] == "Triangle":
        canvas.draw_polygon(get_triangle_points(shape["x"], shape["y"], 60), 2, "Black", shape["color"])
    elif shape["shape"] == "Square":
        canvas.draw_polygon(get_square_points(shape["x"], shape["y"], 60), 2, "Black", shape["color"])
    else:
        canvas.draw_point([shape["x"], shape["y"]], shape["color"])

#set color
def set_color(color):
    global cur_color, message
    if (color in color_list) or color_rgb_reg(color):
        cur_color = color
    else:
        show_message("Please Input Correct Color Name or RGB like #ff0000/#FF0000")
        color_input.set_text("")


#mouse click
def mouse_click(pos):
    global cur_color
    color_picker_index = get_color_picker_index(pos)
    if color_picker_index < 0 or color_picker_index >= COLOR_PICKER_ROW * COLOR_PICKER_COLUMN :
        shape={"x":pos[0], "y":pos[1], "shape":cur_shape, "color":cur_color}
        shape_list.append(shape)
        global cur_index,message,mouse_mode
        cur_index=len(shape_list) - 1
        messaage=""
        mouse_mode="click"
    else:
        cur_color = color_list[color_picker_index]

def drag(pos):
    special_pos=[pos[0], pos[1], cur_color]
    drag_pos_list.append(special_pos)
    global mouse_mode
    mouse_mode="drag"

# set interval
def set_interval(input_interval):
    if play_mode:
        show_message("Please don't Change Interval When Playing!")
        return
    global interval,message,timer
    try:
        interval = int(input_interval)
        timer = simplegui.create_timer(interval, timer_handler)
    except ValueError:
        show_message("Please Input a Integer for Interval!")
        interval_input.set_text("")

# play the draw 
def play_stop():
    global message,play_mode,play_index
    if play_stop_btn.get_text() == "Play":
        play_mode=True
        play_stop_btn.set_text("Stop")
        play_index = 0
        timer.start()
    elif play_stop_btn.get_text() == "Stop":
        show_message("Play Stoped by User")
        play_end()
        play_index = -1

# play end
def play_end():
    play_stop_btn.set_text("Play")
    timer.stop()
    global play_mode
    play_mode = False

# timer ticker
def timer_handler():
    global play_index
    if (play_index >= 0 and play_index < (len(shape_list) - 1)):
        play_index += 1
    else:
        show_message("Play End")
        play_end()

# show messaage
def show_message(msg):
    global message
    message = msg
    message_timer.start()
    
# message timer handler
def message_timer_handler():
    global message
    if message_timer.is_running():
        message_timer.stop()
    message = ""
    
#save shape_list to file
def save_draw():
    save_file = tkFileDialog.asksaveasfile(mode='w')
    save_file.write(str(shape_list))
    save_file.flush()
    save_file.close()
    
#open shape file and play
def open_draw():
    end = False
    shape_str = ""
    open_file = tkFileDialog.askopenfile(mode='r')
    while not end:
        read_str = open_file.readline(1024)
        print(shape_str)
        if not read_str:
            end = True
        else:
            shape_str += read_str
    open_file.close()
    print shape_str
    shape_list = ast.literal_eval(shape_str)
    play_stop()
    
#create frame
frame = simplegui.create_frame("Your Draw", FRAME_WIDTH, FRAME_HEIGHT)

#set background white
frame.set_canvas_background("White")

#add shape control buttons
frame.add_button("Circle", shape_circle)
frame.add_button("Triangle", shape_triangle)
frame.add_button("Square", shape_square)

#add color input
color_input = frame.add_input("Set Color", set_color, 200);

#add undo/redo button
frame.add_button("Prev", prev)
frame.add_button("Next", next)

# add timer interval input
interval_input = frame.add_input("Set Interval(ms)", set_interval, 200);

#add play btn
play_stop_btn = frame.add_button("Play", play_stop)

#add mouse click and draw
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_click)
frame.set_mousedrag_handler(drag)

#create timer
timer = simplegui.create_timer(interval, timer_handler)
message_timer = simplegui.create_timer(1500, message_timer_handler)

#add save and open button
frame.add_button("Save", save_draw)
frame.add_button("Open", open_draw)

# avoid empty tk dialog
root = Tk()
root.withdraw()

#start
frame.start()

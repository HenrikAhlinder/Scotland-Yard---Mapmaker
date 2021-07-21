import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk

from saver import Savefilemaker

root = Tk()

root.geometry('830x520')
root.configure(background='#F0F8FF')
root.title('Scotland yard - mapmaker')
canvas = Canvas(root, background="#a8ccfa", width=600, height=500)
template_frame = Frame(root, background="#fad6a8")
canvas.grid(row=0, column=0, rowspan=2)
template_frame.grid(row=1, column=1, padx=10)
# Houses spinboxes to decide grid size on canvas.
size_frame = Frame(root, background="#fad6a8")
size_frame.grid(row=0, column=1)

# Default gridsize
width, height = 5, 5

# The images to place.
stop_imagefile = "taxi.png"
placed_images = []

# The different transportation methods.
active_linetypes = []
startcoords = None  # If this is not none, place a line.


##################### Save and load maps ##########################
savestate = Savefilemaker((5, 5))


def load_map(width, height):
    """Loads a map from file."""
    # TODO: Finish this temporary function.
    global canvas
    canvas.delete("all")
    #gridsize, stops, lines = savestate.load(filename)
    make_rects(canvas, width, height)
    testtype, testcoords, stopsize = savestate.load("test")

    place_stop_coords(testtype, testcoords, stopsize)


def place_stop_coords(stoptype, coords, imsize):
    """Place a stop at given coordinates."""
    global canvas
    img = Image.open(stoptype + ".png")
    resized_image = resize_aspect(img, imsize[0], imsize[1])
    image = ImageTk.PhotoImage(resized_image)

    tags = ("stops", stoptype)
    placed_images.append(image)
    img = canvas.create_image(coords, anchor="center",
            image=image, tags=tags)


def resize_aspect(img, width, height):
    """Resize image but keep aspect ratio."""
    if width < height:
        scale_percent = width/float(img.size[0])
        v_size = int(width)
        h_size = int((float(img.size[1])*float(scale_percent)))
    else:
        scale_percent = height/float(img.size[1])
        v_size = int((float(img.size[0])*float(scale_percent)))
        h_size = int(height)

    return img.resize((v_size, h_size), Image.ANTIALIAS)


################## Canvas creation #####################################
canvas.update()

def place_stop(event):
    global canvas, placed_images, stop_imagefile, savestate
    rect = event.widget.find_withtag('current')[0]
    rect_coords = canvas.coords(rect)
    center = ((rect_coords[0]+rect_coords[2]) / 2,
              (rect_coords[1]+rect_coords[3]) / 2)

    rect_width = rect_coords[2]-rect_coords[0] - 3
    rect_height = rect_coords[3]-rect_coords[1] - 3

    img = Image.open(stop_imagefile)
    resized_image = resize_aspect(img, rect_width, rect_height)

    image = ImageTk.PhotoImage(resized_image)
    tags = ("stops", stop_imagefile[:-4])
    placed_images.append(image)
    image = canvas.create_image(center, anchor="center",
            image=image, tags=tags)

    savestate.add_stop(stop_imagefile[:-4], center, (rect_width, rect_height))

    return image

def remove_stop(event):
    global canvas
    image = event.widget.find_withtag('current')[0]
    canvas.delete(image)

def connect_line(event):
    """Start or stop connecting a line."""
    global canvas, active_linetypes, active_line, startcoords
    curr_stop = event.widget.find_withtag('current')[0]
    test = canvas.find_overlapping(event.x-3, event.y-3, event.x+3, event.y+3)
    curr_stop = test[0]
    coords = canvas.coords(curr_stop)
    center_coords = ((coords[0]+coords[2]) / 2,
                     (coords[1]+coords[3]) / 2)


    if startcoords is not None:
        if "taxiline" in active_linetypes:
            draw_taxiline(center_coords)
        if "busline" in active_linetypes:
            draw_busline(center_coords)
        if "undergroundline" in active_linetypes:
            draw_undergroundline(center_coords)

        startcoords = None
    else:
        startcoords = center_coords

    # Put the line below the stops.
    try:
        canvas.tag_lower("line", "stops")
    except:
        x=0

def draw_taxiline(endcoords):
    """Draw a taxiline. No offset on startcoords"""
    global canvas, startcoords
    start = startcoords
    edge = endcoords[0], startcoords[1]
    end = endcoords

    canvas.create_line(*startcoords, *edge, width=3, tags="line")
    canvas.create_line(*edge, *endcoords, width=3, tags="line")

def draw_busline(endcoords):
    """Draw a (green) busline. Slight offset downwards and leftwards from taxiline"""
    global canvas, startcoords
    # NOTE: The first line will always be vertical, second horizontal
    offset = 5 # Pixels
    start = startcoords[0], startcoords[1]+offset
    edge  = endcoords[0]-offset, startcoords[1]+offset
    end = endcoords[0]-offset, endcoords[1]

    canvas.create_line(*start, *edge, width=3, fill="green", tags="line")
    canvas.create_line(*edge, *end, width=3, fill="green", tags="line")
def draw_undergroundline(endcoords):
    """Draw a (green) busline. Slight offset upwards and rightwards from taxiline"""
    global canvas, startcoords
    offset = -5 # Pixels
    start = startcoords[0], startcoords[1]+offset
    edge  = endcoords[0]-offset, startcoords[1]+offset
    end = endcoords[0]-offset, endcoords[1]

    canvas.create_line(*start, *edge, width=3, fill="red", tags="line")
    canvas.create_line(*edge, *end, width=3, fill="red", tags="line")


def remove_line(event):
    """Remove a line from the board."""
    global canvas

    line = event.widget.find_withtag('current')[0]
    canvas.delete(line)


def make_rects(canvas, width, height):
    rects = []
    rect_width = canvas.winfo_width()/width
    rect_heigth = canvas.winfo_height()/height
    for rowno in range(height):
        ystart, ystop = rect_heigth*rowno, rect_heigth*(rowno+1)

        for columnno in range(width):
            xstart, xstop = rect_width*columnno, rect_width*(columnno+1)
            rects.append(canvas.create_rectangle(xstart, ystart, xstop, ystop,
                tags="place", fill="white"))



    return rects

rects = make_rects(canvas, width, height)
canvas.tag_bind("place", '<ButtonPress-1>', place_stop)
canvas.tag_bind("stops", '<ButtonPress-1>', remove_stop)
canvas.tag_bind("place", '<ButtonPress-3>', connect_line)
canvas.tag_bind("stops", '<ButtonPress-3>', connect_line)
canvas.tag_bind("line" , '<ButtonPress-3>', remove_line)


########################### Template area creation ###################################
busimage = PhotoImage(file="busstop.png")
undimage = PhotoImage(file="underground.png")
line_defaultback = "#dce2dd"
line_activeback = "#d3ae7e"

stoplabel = Label(template_frame, text="Type of stop (cumulative)",
        background="#fad6a8")
stoplabel.pack()
bus_template = Button(template_frame,
        image=busimage,
        command=lambda : template_onclick("busstop"))
bus_template.pack(anchor="n")

und_template = Button(template_frame,
        image=undimage,
        command=lambda : template_onclick("underground"))
und_template.pack(anchor="n")


linelabel = Label(template_frame, text="Type of line (cumulative)", pady=5,
        background="#fad6a8")
linelabel.pack()
taxiline = Button(template_frame,
            text="Taxiline",
            command=lambda : line_onclick("taxiline"),
            background=line_defaultback)
taxiline.pack()

busline = Button(template_frame,
            text="Busline",
            command=lambda : line_onclick("busline"),
            background=line_defaultback)
busline.pack()

undergroundline = Button(template_frame,
            text="Undergroundline",
            command=lambda : line_onclick("undergroundline"),
            background=line_defaultback)
undergroundline.pack()

# key: GUI_app, active.
templates = {
    "busstop":(bus_template, False),
    "underground":(und_template, False),
    "taxiline":(taxiline, False),
    "busline":(busline, False),
    "undergroundline":(undergroundline, False),
}


def template_onclick(template_string):
    global templates, stop_imagefile, undimage
    button, state = templates[template_string]

    # Turn off or on the selected template
    if state:
        button['relief'] = "raised"
        templates[template_string] = (button, False)
    else:
        button['relief'] = "sunken"
        templates[template_string] = (button, True)

    # Select the appropiate stop to draw.
    if templates["busstop"][1] and templates["underground"][1]:
        stop_imagefile = "both.png"
    elif templates["busstop"][1]:
        stop_imagefile = "busstop.png"
    elif templates["underground"][1]:
        stop_imagefile = "underground.png"
    else:
        stop_imagefile = "taxi.png"

def line_onclick(linetype):
    global active_linetypes, templates, line_defaultback
    button, state = templates[linetype]

    # Turn off or on the selected template
    if state:
        button['relief'] = "raised"
        button['bg'] = line_defaultback
        templates[linetype] = (button, False)

        active_linetypes.remove(linetype)
    else:
        button['relief'] = "sunken"
        button['bg'] = line_activeback
        templates[linetype] = (button, True)

        active_linetypes.append(linetype)

############################## Grid size spinboxes ########################

def change_size():
    """Applied by the button."""
    global canvas, width, height, placed_images
    placed_images.clear()
    canvas.delete("all")
    make_rects(canvas, int(width.get()), int(height.get()))
    load_map(int(width.get()), int(height.get()) )


size_lbl = Label(size_frame, text="Grid size", justify="center")
size_lbl.grid(row=0, column=0, columnspan=3)
width = StringVar(root, value=5)
height = StringVar(root, value=5)

width_lbl = Label(size_frame, text="Width")
height_lbl = Label(size_frame, text="Height")
width_spin = Spinbox(size_frame, textvariable=width, width=10, from_=0, to=50)
height_spin = Spinbox(size_frame, textvariable=height, width=10, from_=0, to=50)
width_lbl.grid(row=1, column=0)
height_lbl.grid(row=2, column=0)
width_spin.grid(row=1, column=1, columnspan=2)
height_spin.grid(row=2, column=1, columnspan=2)

change_size_btn = Button(size_frame, text="Apply", bg = "green",
                        command=change_size)
change_size_btn.grid(row=3, column=1)

taxiline.invoke()
root.mainloop()

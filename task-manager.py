########################################################################################################################################################################################################

        # Imports

from shlex import quote
from PIL import Image, ImageTk

import tkinter as tk
import os

########################################################################################################################################################################################################

        # Setup

    # Variables
root = tk.Tk() # Tkinter Root

section_display = [] # Array of Widgets for Sections
section_coords = [] # Array of Heights for Sections

plus_display = [] # Array of Widgets for <Add Section> Buttons
trash_display = [] # Array of Widgets for <Remove Section> Buttons

data = [] # Array of Widgets for Tasks #2D
checkmark_display = [] # Array of Widgets for <Delete Task> Buttons #2D
# Originally going to have a colour array. Too Bad!

dir = os.path.dirname(__file__)
data_dir = dir + "/.data.txt"

plus_img = Image.open(dir + "/.assets/plus.png")
plus_img = plus_img.resize((40,40), Image.ANTIALIAS)
plus_tk = ImageTk.PhotoImage(plus_img)

trash_img = Image.open(dir + "/.assets/trash.png")
trash_img = trash_img.resize((40,40), Image.ANTIALIAS)
trash_tk = ImageTk.PhotoImage(trash_img)

checkmark_img = Image.open(dir + "/.assets/checkmark.png")
checkmark_img = checkmark_img.resize((40,40), Image.ANTIALIAS)
checkmark_tk = ImageTk.PhotoImage(checkmark_img)

########################################################################################################################################################################################################

        # Functions

# stackoverflow.com/questions/44887576/
    # Implements Drag and Drop into a Class
class DragManager():
    def add_dragable(self, widget):
        # Bind Functions to Widget
        widget.bind("<ButtonPress-1>", self.on_start)
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)

        widget.configure(cursor="hand1")

    def on_start(self, event):
        widget = event.widget

        # Finds the widget in the data array
        for i in range(len(data)):
            for j in range(len(data[i])):
                if(data[i][j] == widget):
                    widget._data_section = i
                    widget._data_task = j
        
        ghost_task.tkraise()

    def on_drag(self, event):
        widget = event.widget

        ghost_task.place(x=widget.winfo_x()+event.x,y=widget.winfo_y()+event.y)

        root.update_idletasks()
        pass

    def on_drop(self, event):
        widget = event.widget

        y_level = widget.winfo_y() + event.y

        section_index = -1
        for i in range(len(section_coords)):
            if y_level < section_coords[i]:
                section_index = i
                break
        
        if section_index != -1 and section_index != widget._data_section:
            move_task(widget._data_section, widget._data_task, section_index)

        ghost_task.place(x=-168,y=-40)
        root.update()

        # Application Functions

    # Reads from .data.txt and converts to tasks and sections
def init():
    try:
        data_reader = open(data_dir, "r")
    # If no file is found, then one will be generated
    except FileNotFoundError:
        open(data_dir, "x")
        os.system("chflags hidden " + quote(data_dir))
        os.system("attrib +h " + quote(data_dir))

        data_reader = open(data_dir, "r")

    data_raw = data_reader.read().splitlines()
    for i in range(len(data_raw)):
        data_raw[i] = data_raw[i].split("•")
    for i in range(len(data_raw)):
        create_section()
        for j in range(len(data_raw[i])):
            data_raw[i][j] = data_raw[i][j].encode("utf-8").decode("unicode_escape")
            create_task(i, data_raw[i][j])
    
    data_reader.close()

    # Reads all Tasks and Writes to .data.txt
def on_close():
    data_writer = open(data_dir, "w")

    final = ""
    for lst in data:
        line = ""
        for widget in lst:
            line += widget.get("1.0", tk.END + "-1c").encode("unicode_escape").decode("utf-8") + "•"
        line = line[0:-1]
        final += line + "\n"
    final = final[0:-1]
    data_writer.write(final)
    

    print("Shutting Down!")
    root.destroy()

        # Task/Section Functions

# Can be optimzed by only updating all sections & tasks underneath the update call. Too Bad!
    # Updates the display, given "section_display" "plus_display" "trash_display" "data" "checkmark_display"
def update_display():
    section_coords.clear()

    pointer = 16

    for i in range(len(section_display)):
        section_display[i].place(x=16, y=pointer)

        root.update_idletasks()
        section_display[i].configure(height=72+(len(data[i])*56))
        root.update_idletasks()

        for j in range(len(data[i])):
            task_pointer = pointer + (j * 56) + 16
            data[i][j].place(x=32, y=task_pointer)

            checkmark_display[i][j].place(x=128, y=task_pointer)
        
        plus_display[i].place(x=128, y=section_display[i].winfo_height()+pointer-56)

        trash_display[i].place(x=32, y=section_display[i].winfo_height()+pointer-56)

        pointer += section_display[i].winfo_height() + 16
        section_coords.append(pointer - 16)
    
    section_plus.tkraise()

        # Task Functions

    # Moves task from section to section
def move_task(section_index_old, task_index, section_index):
    text = data[section_index_old][task_index].get("1.0", tk.END)

    del_task(section_index_old, task_index)

    create_task(section_index, text)

    update_display()

    # Generates a section
def create_section():
    data.append([])

    checkmark_display.append([])
    
    section_display.append(tk.Frame(root, bg="#96a3a3", height=72, width=168))

    plus_display.append(tk.Label(root, bg="#96a3a3", height=40, width=40, image=plus_tk))
    trash_display.append(tk.Label(root, bg="#96a3a3", height=40, width=40, image=trash_tk))

    newest_section = len(plus_display) - 1
    plus_display[newest_section].bind("<1>", lambda event: create_task(newest_section))
    trash_display[newest_section].bind("<1>", lambda event: del_section(newest_section))

    update_display()

    # Generates a task in a given section
def create_task(section_index, text=""):
    data[section_index].append(tk.Text(root, bg="white", height=2, width=12, highlightcolor="white", font=("Helvetica", 14)))
    dnd.add_dragable(data[section_index][len(data[section_index]) - 1])

    # WHY DO I HAVE TO COMPENSATE FOR A RANDOM +6 TO THE VALUES??
    checkmark_display[section_index].append(tk.Label(root, bg="white", height=34, width=34, image=checkmark_tk))

    newest_task = len(checkmark_display[section_index]) - 1
    checkmark_display[section_index][newest_task].bind("<1>", lambda event: del_task(section_index, newest_task))
    data[section_index][newest_task].insert(tk.END, text)

    update_display()

    # Deletes a section
def del_section(section_index):
    section_display[section_index].destroy()
    plus_display[section_index].destroy()
    trash_display[section_index].destroy()
    del section_display[section_index]
    del plus_display[section_index]
    del trash_display[section_index]

    for task in data[section_index]:
        task.destroy()
    del data[section_index]

    for checkmark in checkmark_display[section_index]:
        checkmark.destroy()
    del checkmark_display[section_index]

    for i in range(len(plus_display)):
        plus_display[i].unbind("<1>")
        trash_display[i].unbind("<1>")

        plus_display[i].bind("<1>", lambda event, i=i: create_task(i))
        trash_display[i].bind("<1>", lambda event, i=i: del_section(i))

    update_display()

    # Deletes a task in a given section
def del_task(section_index, task_index):
    data[section_index][task_index].destroy()
    del data[section_index][task_index]

    checkmark_display[section_index][task_index].destroy()
    del checkmark_display[section_index][task_index]

    for i in range(len(checkmark_display[section_index])):
        checkmark_display[section_index][i].unbind("<1>")
        checkmark_display[section_index][i].bind("<1>", lambda event, i=i: del_task(section_index, i))

    update_display()

########################################################################################################################################################################################################

        # Tkinter Menu

root.configure(bg="#b4f7ff")
root.geometry("200x640")

    # Create DragManager
dnd = DragManager()

    # Add "Create Section" Button
section_plus = tk.Label(height=40, width=40, image=plus_tk)
section_plus.bind("<1>", lambda event: create_section())

section_plus.place(x=144, y=584)

    # Add Ghost Task
ghost_task = tk.Frame(bg="#dddddd", height=40, width=136)

root.protocol("WM_DELETE_WINDOW", on_close)

init()

root.mainloop()
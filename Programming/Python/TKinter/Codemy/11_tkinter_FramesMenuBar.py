"""
Created on Thu Jun 8 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Frame, Menu, StringVar, Tk, Label, Button, Entry, filedialog, OptionMenu

root = Tk()

# Define and configure menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Function for the menus
def menu_func():
    return

def file_new():
    hide_all_frames()
    file_new_frame.pack(fill="both", expand=1)
    file_new_frame.pack_propagate(0)
    myLabel = Label(file_new_frame, text="You clicked File New Menu").pack()

def edit_cut():
    hide_all_frames()
    edit_cut_frame.pack(fill="both", expand=1)
    edit_cut_frame.pack_propagate(0)
    myLabel = Label(edit_cut_frame, text="You clicked Edit Cut Menu").pack()

# Hide all frames
def hide_all_frames():
    file_new_frame.pack_forget()
    edit_cut_frame.pack_forget()

#######
# Define a File menu item
file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)

# Add to File menu
file_menu.add_command(label="New...", command=file_new)
file_menu.add_separator()
file_menu.add_command(label="Quit...", command=root.quit)

#######
# Define a Edit menu item
edit_menu = Menu(my_menu)
my_menu.add_cascade(label="Edit", menu=edit_menu)

# Add to Edit menu
edit_menu.add_command(label="Cut...", command=edit_cut)
edit_menu.add_separator()
edit_menu.add_command(label="Copy...", command=menu_func)


#######
# Create some frames
file_new_frame = Frame(root, width=400, height=400, bg="red")
edit_cut_frame = Frame(root, width=400, height=400, bg="blue")



# Loop
root.mainloop()
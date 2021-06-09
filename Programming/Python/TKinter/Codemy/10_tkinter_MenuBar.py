"""
Created on Thu Jun 8 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Menu, StringVar, Tk, Label, Button, Entry, filedialog, OptionMenu

root = Tk()

# Define and configure menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Function for the menus
def menu_func():
    return

#######
# Define a File menu item
file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)

# Add to File menu
file_menu.add_command(label="New...", command=menu_func)
file_menu.add_separator()
file_menu.add_command(label="Quit...", command=menu_func)

#######
# Define a Edit menu item
edit_menu = Menu(my_menu)
my_menu.add_cascade(label="Edit", menu=edit_menu)

# Add to Edit menu
edit_menu.add_command(label="Cut...", command=menu_func)
edit_menu.add_separator()
edit_menu.add_command(label="Copy...", command=menu_func)



# Loop
root.mainloop()
"""
Created on Thu Jun 8 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Menu, Tk

from tkinterdnd2 import DND_FILES, TkinterDnD

from libs.frames.main_frame import MainFrame

root = TkinterDnD.Tk() #Tk()

# Define and configure menu
my_menu = Menu(root)
root.config(menu=my_menu)

mainframe = MainFrame(root)

#######
# Define a File menu item
file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)

# Add to File menu
file_menu.add_command(label="Open...", command=mainframe.open_img)
file_menu.add_separator()
file_menu.add_command(label="Quit...", command=root.quit)

# Loop
root.mainloop()
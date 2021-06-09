"""
Created on Thu Jun 8 10:00:19 2021

@author: Rodrigo
"""
from tkinter import Button, OptionMenu, PhotoImage, StringVar, Tk, Label, Frame, ttk

root = Tk()

def selected(event):
    myLabel = Label(root, text=clicked.get()).pack()

def comboclick(event):
    myLabel = Label(root, text=my_combo.get()).pack()

options = [0, 1, 2]

clicked = StringVar()

clicked.set(options[0])

drop = OptionMenu(root, clicked, *options, command=selected)
drop.pack(pady=20)

my_combo = ttk.Combobox(root, value=options)
my_combo.current(0)
my_combo.bind("<<ComboboxSelected>>", comboclick)
my_combo.pack()

# Loop
root.mainloop()
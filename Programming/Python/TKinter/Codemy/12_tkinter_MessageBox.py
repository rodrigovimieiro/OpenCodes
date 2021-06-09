#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 8 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Button, Tk, Toplevel, messagebox, Label, Frame

root = Tk()

messagebox.showinfo("showinfo", "Information")

def button_choice(in_label):

    pop.destroy()

    if in_label == "yes":
        my_label.config(text="Clicked yes")

    elif in_label == "no":
        my_label.config(text="Clicked no")



def clicker():

    global pop

    pop = Toplevel(root)

    pop.title("My popup")
    pop.geometry("250x150")
    pop.config(bg="Green")

    pop_label = Label(pop, text="Would you like do continue?")
    pop_button_yes = Button(pop, text="Yes", command=lambda:button_choice("yes"))
    pop_button_no = Button(pop, text="No", command=lambda:button_choice("no"))

    my_frame = Frame(pop, bg="white")
    my_frame.grid(row=0, column=0)

    pop_label.grid(row=0, column=0, padx=10, columnspan=2)
    pop_button_yes.grid(row=1, column=0, padx=10)
    pop_button_no.grid(row=1, column=1, padx=10)


    return

mybutton = Button(root, text="Click", command=clicker)
my_label = Label(root, text="nothing")

mybutton.grid(row=0, column=0, padx=10)
my_label.grid(row=1, column=0, padx=10)


# Loop
root.mainloop()
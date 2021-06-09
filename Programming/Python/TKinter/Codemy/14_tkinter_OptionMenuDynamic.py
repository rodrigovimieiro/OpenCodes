#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 11:41:53 2021

@author: Rodrigo

Source:
- https://stackoverflow.com/a/29563382/8682939
- https://stackoverflow.com/a/17581364/8682939

"""

from tkinter import Label, Event, Tk, StringVar, OptionMenu, Button

root = Tk()
choices = ('network one', 'network two', 'network three')
var = StringVar(root)

def run_choice(v):
    var.set(v)
    myLabel = Label(root, text=var.get()).grid()


def refresh():
    # Reset var and delete all old options
    var.set('')
    network_select['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to var)
    new_choices = ('one', 'two', 'three')
    for choice in new_choices:
        network_select['menu'].add_command(label=choice, command=lambda v=choice: run_choice(v))

network_select = OptionMenu(root, var, *choices, command=run_choice)
network_select.grid()

# I made this quick refresh button to demonstrate
Button(root, text='Refresh', command=refresh).grid()

root.mainloop()
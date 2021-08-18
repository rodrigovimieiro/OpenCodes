#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 11:41:53 2021

@author: Rodrigo

"""

from tkinter import Label, Event, Tk, StringVar, OptionMenu, Button, ttk

root = Tk()
choices = ('Monday', 'Friday')

def myfunc(event):
    myLabel = Label(root, text=myCombo.get()).grid()

myCombo = ttk.Combobox(root, value=choices)
myCombo.bind('<<ComboboxSelected>>', myfunc)
myCombo.grid()

root.mainloop()
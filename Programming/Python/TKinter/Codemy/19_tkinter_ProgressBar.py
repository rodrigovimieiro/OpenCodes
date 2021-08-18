#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 11:41:53 2021

@author: Rodrigo

"""

from tkinter import Label, Event, Tk, StringVar, OptionMenu, Button, ttk
import time
from tkinter.constants import HORIZONTAL

root = Tk()

def step():

    # my_progress['value'] += 20
    # my_progress.start(10)

    for x in range(5):
        my_progress['value'] += 20
        # root.update_idletasks()
        # time.sleep(1)

    return

def stop():
    my_progress.stop()
    return

my_progress = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')

my_button = Button(root, text='Step', command=step).pack()
my_button2 = Button(root, text='Stop', command=stop).pack()

my_progress.pack()

root.mainloop()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Tk, Label, Button, Entry, END

# Function for the Button
def button_numbers(mynumber):
    current = myEntry.get()
    myEntry.delete(0, END)
    myEntry.insert(0, current + str(mynumber))

def button_clear():
    myEntry.delete(0, END)

def button_sum():

    first_number = myEntry.get()

    global f_num

    f_num = int(first_number)

    myEntry.delete(0, END)


def button_equal():
    
    second_number = myEntry.get()

    myEntry.delete(0, END)

    answer = int(second_number) + f_num

    print(answer)

    myEntry.insert(0, str(answer))


root = Tk()
root.title("Simple Calculator Rodrigo")


myEntry = Entry(root, width=40, bg="White", fg="Black")
myEntry.get()

# Button Widget
button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: button_numbers(0))
button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: button_numbers(1))
button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: button_numbers(2))
button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: button_numbers(3))
button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: button_numbers(4))
button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: button_numbers(5))
button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: button_numbers(6))
button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: button_numbers(7))
button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: button_numbers(8))
button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: button_numbers(9))

button_plus = Button(root, text="+", padx=40, pady=20, command=button_sum)
button_equal = Button(root, text="=", padx=98, pady=20, command=button_equal)
button_clear = Button(root, text="Clear", padx=86, pady=20, command=button_clear)


# Place it on a grid
myEntry.grid(row=0, column=0, columnspan=3)

button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)
button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)
button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)
button_0.grid(row=4, column=0)

button_plus.grid(row=5, column=0)
button_equal.grid(row=5, column=1, columnspan=2)
button_clear.grid(row=4, column=1, columnspan=2)

# Loop
root.mainloop()
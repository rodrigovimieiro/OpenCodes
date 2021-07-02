from tkinter import Tk, Label, Button, Entry
from tkinter.constants import W

root = Tk()
root.geometry("400x400")

# Function for the Button
def myClick(event):
    myLabel1 = Label(root, text= "OK - x:" + str(event.x) + " y:" + str(event.y))
    myLabel1.grid(row=2, column=0)

# Button Widget
myButton = Button(root, text="Click me", padx=50, pady=15, command=myClick, fg="white", bg="blue")
# myButton.bind("<Button-2>", myClick)
# myButton.bind("<Enter>", myClick)
myButton.bind("<Leave>", myClick)
# myButton.bind("<Return>", myClick)

# Palce it on a grid
myButton.grid(row=1, column=0)

# Loop
root.mainloop()
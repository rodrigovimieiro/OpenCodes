#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 11:41:53 2021

@author: Rodrigo

"""

from tksheet import Sheet
import tkinter as tk


class demo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)
        self.sheet = Sheet(self.frame,
                           data = [[f"Row {r}, Column {c}\nnewline1\nnewline2" for c in range(50)] for r in range(500)])
        self.sheet.enable_bindings()
        self.sheet.extra_bindings([("all_select_events", self.sheet_select_event)])
        self.show_selections = tk.Label(self)
        self.frame.grid(row = 0, column = 0, sticky = "nswe")
        self.sheet.grid(row = 0, column = 0, sticky = "nswe")
        self.show_selections.grid(row = 1, column = 0, sticky = "nswe")

    def sheet_select_event(self, event = None):
        try:
            len(event)
        except:
            return
        try:
            if event[0] == "select_cell":
                self.show_selections.config(text = f"Cells: ({event[1] + 1},{event[2] + 1}) : ({event[1] + 1},{event[2] + 1})")
            elif "cells" in event[0]:
                self.show_selections.config(text = f"Cells: ({event[1] + 1},{event[2] + 1}) : ({event[3] + 1},{event[4]})")
            elif event[0] == "select_column":
                self.show_selections.config(text = f"Columns: {event[1] + 1} : {event[1] + 1}")
            elif "columns" in event[0]:
                self.show_selections.config(text = f"Columns: {event[1][0] + 1} : {event[1][-1] + 1}")
            elif event[0] == "select_row":
                self.show_selections.config(text = f"Rows: {event[1] + 1} : {event[1] + 1}")
            elif "rows" in event[0]:
                self.show_selections.config(text = f"Rows: {event[1][0] + 1} : {event[1][-1] + 1}")
            else:
                self.show_selections.config(text = "")
        except:
            self.show_selections.config(text = "")


app = demo()
app.mainloop()

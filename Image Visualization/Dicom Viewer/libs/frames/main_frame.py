
from tkinter import Frame, Label, Button, Entry, filedialog
from PIL import ImageTk, Image

import pydicom
import numpy as np
import cv2 

class MainFrame(Frame):
    def __init__(self, root):

        self.root = root
        
        ##########################################
        # Frames
        ##########################################

        self.build_frames()

        self.build_top_frame()
        self.build_btm_frame()

        ##########################################
        # Variables
        ##########################################

        self.scale_down = 0.3
        self.window_value = 4096
        self.level_value = 2048

        self.flag_invert = False


    def build_frames(self):

        self.top_frame = Frame(self.root)
        self.btm_frame = Frame(self.root)

        # Palce it on a grid
        self.top_frame.grid(row=0)
        self.btm_frame.grid(row=1)

    def build_top_frame(self):

        # Button Widget
        button_invert = Button(self.top_frame, text="Invert image", width = 35, height=2, command=self.func_button_invert)
        button_wl = Button(self.top_frame, text="Set WL", width = 35, height=2, command=self.func_button_wl)

        self.window_entry = Entry(self.top_frame, width=20, bg="White", fg="Black")
        self.level_entry = Entry(self.top_frame, width=20, bg="White", fg="Black")

        label_window = Label(self.top_frame, text= "Window", font=('TkDefaultFont',18))
        label_level = Label(self.top_frame, text= "Level", font=('TkDefaultFont',18))

        button_wl.grid(row=0, column=0, columnspan=2)
        button_invert.grid(row=1, column=0, columnspan=2)
        self.window_entry.grid(row=1, column=2)
        self.level_entry.grid(row=1, column=3)
        label_window.grid(row=0, column=2)
        label_level.grid(row=0, column=3)
        
    def build_btm_frame(self):

        # Tmp image just to get space
        img = np.zeros((250,250)).astype(np.uint8) * 128
        img2plot = ImageTk.PhotoImage(image=Image.fromarray(img))

        self.img_panel = Label(self.btm_frame, image=img2plot)
        self.img_panel.grid(row=0, column=0, columnspan=2)

        return

    ########## Button func ##########

    def func_button_invert(self):

        self.flag_invert = ~self.flag_invert

        self.update_img_frame(self.img)

    def func_button_wl(self):

        local_window_value = self.window_entry.get()
        local_level_value = self.level_entry.get()

        self.window_value = int(local_window_value)
        self.level_value = int(local_level_value)

        self.update_img_frame(self.img)

    ########## General func ##########

    def load_path(self):
                
        return filedialog.askopenfilename(initialdir="/~", title="Select a file", filetypes=[("DICOM files", "*.dcm"),("All files", "*")])

    def update_img_frame(self, img2plot):

        img2plot= self.process_wl(img2plot)
        img2plot = self.resize_img(img2plot)

        img2plot = ImageTk.PhotoImage(image=Image.fromarray(img2plot))
        self.img_panel.configure(image=img2plot)
        self.img_panel.image = img2plot

        return

    def process_wl(self, image):

        vmin = self.level_value - (self.window_value // 2)
        vmax = self.level_value + (self.window_value // 2)
        # print(vmin, vmax)

        img_processed = np.clip(image, vmin, vmax)
        img_processed = (img_processed - img_processed.min()) / (img_processed.max() - img_processed.min())
        img_processed *= 255
        img_processed = np.uint8(img_processed)

        print(self.flag_invert)
        if self.flag_invert:
            img_processed = img_processed.max() - img_processed

        return img_processed

    def resize_img(self, image):

        img_scaled = cv2.resize(image, None, fx= self.scale_down, fy= self.scale_down, interpolation= cv2.INTER_LINEAR)

        return img_scaled

    def open_img(self):

        img_path = self.load_path()
        self.img = pydicom.read_file(img_path).pixel_array

        self.update_img_frame(self.img)

        self.window_entry.insert(0, str(self.window_value))
        self.level_entry.insert(0, str(self.level_value))

        return


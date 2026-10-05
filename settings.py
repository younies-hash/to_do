from tkinter import Toplevel
import tkinter as tk

def setting_popup(parent, callback):
    settings_screen = Toplevel(parent)
    settings_screen.title = ' Settings'
    
    lbl = tk.Label(settings_screen, 'Resize').pack()
    menu = tk.OptionMenu()
    menu.pack()
    
    settings_screen.mainloop()


class UI_settings():
    def __init__(self, text_size, entry_x, entry_iy, add_x, add_y):
        self.text_size = text_size
        self.entry_x = entry_x 
        self.entry_iy = entry_iy
        self.add_x = add_x
        self.add_y = add_y

size1 = UI_settings(15, 30, 40, 10, 10)
size2 = UI_settings(15, 30, 40, 10, 10)
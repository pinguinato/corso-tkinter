""" Hello World application for Tkinter """
import tkinter as tk

# every tkinter program must have a root window
root = tk.Tk()

# example of label widget
label = tk.Label(root, text="Hello World!")
label.pack()

root.mainloop()
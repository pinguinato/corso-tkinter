""" Banana Survey """
import tkinter as tk

root = tk.Tk()

# set the title
root.title("Banana interest survey")
# set the root window size
root.geometry('640x480+300+300')
root.resizable(False, False)

####################
# WIDGET ###########
####################

# label title
title = tk.Label(
    root, 
    text='Please take the survey', 
    font=('Arial 16 bold'), 
    bg='brown', 
    fg='#FF0'
)

name_label = tk.Label(
    root, 
    text='What is your name', 
)

# simple text input box
name_inp = tk.Entry(root)

#title.pack()
#name_label.pack()
#name_inp.pack()


root.mainloop()

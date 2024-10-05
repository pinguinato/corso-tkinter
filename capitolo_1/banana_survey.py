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

name_label = tk.Label(root, text='What is your name')
# simple text input box
name_inp = tk.Entry(root)
# check button widget
eater_inp = tk.Checkbutton(root, text='Check this box if you eat bananas')
num_label = tk.Label(root, text='How many bananas do you eat per day?')
num_inp = tk.Spinbox(root, from_=0, to=1000, increment=1)
color_label = tk.Label(root, text='What is the best color for a banana?')
color_inp = tk.Listbox(root, height=1)
color_choices = ('Any', 'Green', 'Green-Yellow', 'Yellow', 'Brown-Spotted', 'Black')

for choice in color_choices:
    color_inp.insert(tk.END, choice)


#title.pack()
#name_label.pack()
#name_inp.pack()


##################
# EXECUTION ######
##################
root.mainloop()

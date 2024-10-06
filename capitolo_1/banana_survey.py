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

plantain_label = tk.Label(root, text='Do you eat plantains?')
plantain_frame = tk.Frame(root)
plantain_yes_inp = tk.Radiobutton(plantain_frame, text='Yes')
plantain_no_inp = tk.Radiobutton(plantain_frame, text='Ewww, not')

banana_haiku_label = tk.Label(root, text='Write a haiku about bananas')
banana_haiku_inp = tk.Text(root, height=3)
submit_btn = tk.Button(root, text='Submit Survey')
output_line = tk.Label(root, text='', anchor='w', justify='left')


####################
# WIDGET POSITION  #
####################
title.grid(columnspan=2)
name_label.grid(row=1, column=0)
name_inp.grid(row=1, column=1)
eater_inp.grid(row=2, columnspan=2, sticky='we')
name_label.grid(row=3, sticky=tk.W)
num_inp.grid(row=3, column=1, sticky=(tk.W + tk.E))
color_label.grid(row=4, columnspan=2, sticky=tk.W, pady=10)
color_inp.grid(row=5, columnspan=2, sticky=tk.W + tk.E, padx=25)
plantain_yes_inp.pack(side='left', fill='x', ipadx=10, ipady=5)
plantain_no_inp.pack(side='left', fill='x', ipadx=10, ipady=5)
plantain_label.grid(row=6, columnspan=2, sticky=tk.W)
plantain_frame.grid(row=7, columnspan=2, sticky=tk.W)
submit_btn.grid(row=99)
output_line.grid(row=100, columnspan=2, sticky='NSEW')
# adjust widget size 
root.columnconfigure(1, weight=1)
banana_haiku_label.grid(row=8, sticky=tk.W)
banana_haiku_inp.grid(row=9, columnspan=2, sticky='NSEW')
root.rowconfigure(99, weight=2)
root.rowconfigure(100, weight=1)

##################
# CALLBACK #######
##################
def on_submit():
    name = name_inp.get()
    number = num_inp.get()

    selected_idx = color_inp.curselection()
    
    if selected_idx:
        color = color_inp.get(selected_idx)
    else:
        color = ''
    
    haiku = banana_haiku_inp.get('1.0', tk.END)

    message = (
        f'Thanks for taking the survey, {name},\n'
        f'Enjoy your {number} {color} bananas!'
    )
    output_line.configure(text=message)
    print(haiku)


submit_btn.configure(command=on_submit)

##################
# EXECUTION ######
##################
root.mainloop()

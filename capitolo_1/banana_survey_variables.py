""" 
Banana Survey con uso delle variabili di controllo Tkinter 
Le variabili di controllo posso memorizzare
- valori stringa
- valori interi
- valori double
- valori booleani
hanno inoltre la possibilità di implementare, in più rispetto alle variabili normali Python:
- binding a 2 vie tra widget e variabile
- trace fa il bind tra un evento variabile e una callback
- relazioni tra i vari widgets
"""
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

# varibile tkinter tipo testo esempio
name_var = tk.StringVar(root)
name_label = tk.Label(root, text='What is your name')
# ecco come passare una varibile tkinter tipo testo
name_inp = tk.Entry(root, textvariable=name_var)
#print(name_var.get())
# esempio di variabile booleana, indicata per una checkbox che è come un on/off
eater_var = tk.BooleanVar()
# ecco come passarla
eater_inp = tk.Checkbutton(root, variable=eater_var, text='Check this box if you eat bananas')
# esempio di varibile numerica per settare un valore numerico di default
num_var = tk.IntVar(value=3)
num_label = tk.Label(root, text='How many bananas do you eat per day?')
# ed ecco come passare num_var al widget per impostare il valore di default
num_inp = tk.Spinbox(root, textvariable=num_var, from_=0, to=1000, increment=1)
color_var = tk.StringVar(value='Any')
color_label = tk.Label(root, text='What is the best color for a banana?')
# Option menu widget example
color_choices = ('Any', 'Green', 'Green-Yellow', 'Yellow', 'Brown-Spotted', 'Black')
color_inp = tk.OptionMenu(root, color_var, *color_choices)
# esempio di boolean var tkinter
plantain_var = tk.BooleanVar()
plantain_label = tk.Label(root, text='Do you eat plantains?')
plantain_frame = tk.Frame(root)

# come passare il valore boolean
plantain_yes_inp = tk.Radiobutton(plantain_frame, text='Yes', value=True, variable=plantain_var)
plantain_no_inp = tk.Radiobutton(plantain_frame, text='Ewww, not', value=False, variable=plantain_var)

banana_haiku_label = tk.Label(root, text='Write a haiku about bananas')
banana_haiku_inp = tk.Text(root, height=3)
submit_btn = tk.Button(root, text='Submit Survey')



output_var = tk.StringVar(value='')
output_line = tk.Label(root, text=output_var, anchor='w', justify='left')


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
banana_haiku_label.grid(row=8, sticky=tk.W)
banana_haiku_inp.grid(row=9, columnspan=2, sticky='NSEW')
submit_btn.grid(row=99)
output_line.grid(row=100, columnspan=2, sticky='NSEW')
# adjust widget size 
root.columnconfigure(1, weight=1)
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

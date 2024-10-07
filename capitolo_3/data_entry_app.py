""" The ABQ Data Entry application """

# librerie per i nostri widgets
import tkinter as tk
from tkinter import ttk
# libreria per generare date e stringhe data per i nostri nomi dei file
from datetime import datetime
# per il salvataggio dei file
from pathlib import Path
# per lavorare con i file csv
import csv

#########################
# Variabili Globali #####
#########################

variables = dict()
records_saved = 0

#########################
# Root Window ###########
#########################

root = tk.Tk()
root.title('ABQ Data Entry Application')
root.columnconfigure(0, weight=1)

#########################
# Heading     ###########
#########################

ttk.Label(root, text="ABQ Data Entry Application", font=("TkDefaultFont", 16)).grid()

#########################
# Data record form ######
#########################

drf = ttk.Frame(root)
drf.grid(padx=10, sticky=(tk.E + tk.W))
drf.columnconfigure(0, weight=1)

#################################################
# Data record form - Record information section #
#################################################

r_info = ttk.LabelFrame(drf, text='Record Information')
r_info.grid(sticky=(tk.W + tk.E))
for i in range(3):
    r_info.columnconfigure(i, weight=1)

# Date
variables['Date'] = tk.StringVar()
ttk.Label(r_info, text='Date').grid(row=0, column=0)
tk.Entry(r_info, textvariable=variables['Date']).grid(row=1, column=0, sticky=(tk.W + tk.E))

# Time
time_values = ['8:00', '12:00', '16:00', '20:00']
variables['Time'] = tk.StringVar()
ttk.Label(r_info, text='Time').grid(row=0, column=1)
ttk.Combobox(r_info, textvariable=variables['Time'], values=time_values).grid(row=1, column=1, sticky=(tk.W + tk.E))

# Technician
variables['Technician'] = tk.StringVar()
ttk.Label(r_info, text='Technician').grid(row=0, column=2)
ttk.Entry(r_info, textvariable=variables['Technician']).grid(row=1, column=2, sticky=(tk.W + tk.E))

# esecuzione
root.mainloop()

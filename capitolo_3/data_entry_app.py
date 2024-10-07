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






# esecuzione
root.mainloop()

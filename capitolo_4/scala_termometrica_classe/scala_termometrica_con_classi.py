"""
    Esercizio della scala termometrica svolto con le classi e Tkinter in Python
"""

import tkinter as tk

class ScalaTermometrica(tk.Frame):
    """ Realizza un frame con Label, input text e button per la scala termometrica """
    def __init__(self, parent, label, inp_temp, inp_args, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # definizione dei widget coinvolti

        self.input = inp_temp(self, **inp_args)
        self.label = tk.Label(self, text=label, anchor='w')

        self.columnconfigure(1, weight=1)
        self.label.grid(sticky=tk.E + tk.W)
        self.input.grid(row=0, column=1, sticky=tk.E + tk.W)


root = tk.Tk()

scala_termometrica = ScalaTermometrica(root, 'DEGREE FAHRENHEIT', tk.Entry, {'bg':'yellow'})
scala_termometrica.grid()

root.mainloop()
# combiniamo insieme un widget di input e una etichetta in modo da dimostrare come possiamo usare le classi con tkinter
# questo perché può essere un metodo per ridurre il codice boylerplate delle applicazioni GUI con widget come tkinter

import tkinter as tk

class LabelInput(tk.Frame):
    """ A label and input field combined together """
    def __init__(self, parent, label, inp_cls, inp_args, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # definizione dei 2 widget
        self.label = tk.Label(self, text=label, anchor='w')
        self.input = inp_cls(self, **inp_args)

        # posizionamento
        self.columnconfigure(1, weight=1)
        self.label.grid(sticky=tk.E + tk.W)
        self.input.grid(row=0, column=1, sticky=tk.E + tk.W)

        """
            Se vogliamo mettere l'etichetta sotto l'imput invece
            self.columnconfigure(0, weight=1)
            self.label.grid(sticky=tk.E + tk.W)
            self.input.grid(sticky=tk.E + tk.W)
        """


#Test
root = tk.Tk()

li1 = LabelInput(root, 'Name', tk.Entry, {'bg':'red'})
li1.grid()

age_var = tk.IntVar(root, value=21)
li2 = LabelInput(
    root, 'Age', tk.Spinbox,
    {'textvariable': age_var, 'from_': 10, 'to': 150}
)
li2.grid()



root.mainloop()

# tkinter_class_demo.py

import tkinter as tk
import json

class JSONVar(tk.StringVar):
    """ A tk variable that can hold dicts and lists """

    """
        1) metodo json.dumps() --> prende un oggetto Python come una lista, un dizionario, una stringa, un float
        e lo ritorna come una stringa in formato JSON
        2) metodo json.loads() --> prende una stringa JSON e ne ritorna un oggetto Python come liste, dizionario, 
        stringhe, dipende da cosa memorizzo nella stringa JSON.
    """


    """
        Intercetta il valore passato nell'oggetto e lo converte in JSON
        servendosi del metodo json.dumps
    """

    def __init__(self, *args, **kwargs):
        kwargs['value'] = json.dumps(kwargs.get('value'))
        super().__init__(*args, **kwargs)

    def set(self, value, *args, **kwargs):
        string = json.dumps(value)
        super().set(string, *args, **kwargs)

    def get(self, *args, **kwargs):
        string = super().get(*args, **kwargs)
        return json.loads(string)


root = tk.Tk()
var1 = JSONVar(root)
var1.set([1,2,3])
var2 = JSONVar(root, value={'a': 10, 'b': 15})

# stampa 2
print("Var1: ", var1.get()[1])
# stampa 15
print("Var2: ", var2.get()['b'])





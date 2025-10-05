"""
    Esercizio della scala termometrica svolto con le classi e Tkinter in Python
"""

import tkinter as tk
from tkinter import ttk

class ConverterApp(tk.Frame):
    """
     La classe principale dell'applicazione che contiene tutti i widget
     e la logica di conversione.
     """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid(row=0, column=0, padx=10, pady=10)

        # Variabili di controllo per l'input e l'output
        self.fahrenheit_value = tk.StringVar()
        self.celsius_value = tk.StringVar(value="\N{DEGREE CELSIUS}")

        # Creazione dei widget
        self.ent_temperature = ttk.Entry(
            self, width=10, textvariable=self.fahrenheit_value
        )
        self.lbl_temp_unit = ttk.Label(self, text="\N{DEGREE FAHRENHEIT}")
        self.btn_convert = ttk.Button(
            self, text="\N{RIGHTWARDS BLACK ARROW}", command=self._convert
        )
        self.lbl_result = ttk.Label(self, textvariable=self.celsius_value)

        # Posizionamento dei widget nella griglia
        self.ent_temperature.grid(row=0, column=0, sticky="e")
        self.lbl_temp_unit.grid(row=0, column=1, sticky="w")
        self.btn_convert.grid(row=0, column=2, padx=10)
        self.lbl_result.grid(row=0, column=3, padx=10)

    def _convert(self):
        """
        Converte il valore da Fahrenheit a Celsius.
        Gestisce gli errori di input non numerico.
        """
        try:
            fahrenheit = float(self.fahrenheit_value.get())
            celsius = (5 / 9) * (fahrenheit - 32)
            self.celsius_value.set(f"{round(celsius, 2)} \N{DEGREE CELSIUS}")
        except ValueError:
            # Se l'input non è un numero, mostra un errore
            self.celsius_value.set("Input non valido")




if __name__ == "__main__":
    # Blocco principale per avviare l'applicazione
    root = tk.Tk()
    root.title('Temperature Converter')
    root.resizable(width=False, height=False)

    # Crea un'istanza della nostra applicazione
    app = ConverterApp(root)

    # Avvia il loop principale
    root.mainloop()
"""
Questo script dimostra come creare un widget personalizzato e auto-validante
in Tkinter, seguendo i principi della programmazione a oggetti.

SCOPO DEL PROGRAMMA:
Il programma crea una finestra con un campo di testo speciale che accetta
al massimo 5 caratteri. Se l'utente tenta di inserirne di più, l'input
viene bloccato e dovrebbe apparire un messaggio di errore.

CLASSE `FiveCharEntry`:
Questa classe è il cuore del programma. È un esempio di come estendere
un widget base di Tkinter (`tk.Entry`) per creare un componente riutilizzabile
con una logica di validazione incapsulata.

ANALISI TECNICA:
1.  Eredita da `tk.Entry`: La nostra classe è a tutti gli effetti un campo
    di testo, ma con funzionalità aggiuntive.
2.  `self.error = tk.StringVar()`: All'interno del suo costruttore, la classe
    crea una propria `StringVar`. Questa variabile è il "canale di comunicazione"
    per i messaggi di errore. È un ottimo esempio di incapsulamento.
3.  `validatecommand`: È collegato al metodo `_validate`, che contiene la
    logica di validazione vera e propria (la lunghezza del testo non deve
    superare 5).
4.  `invalidcommand`: È collegato al metodo `_on_invalid`. Questo metodo
    viene eseguito automaticamente da Tkinter solo se `_validate` restituisce
    `False`. Il suo compito è impostare il messaggio di errore nella `StringVar`
    `self.error`.

Questo approccio permette di creare un widget "intelligente" che gestisce
da solo la propria validazione e i propri messaggi di errore, rendendo il
codice principale più pulito e semplice.
"""

import tkinter as tk

class FiveCharEntry(tk.Entry):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.error = tk.StringVar()
        self.configure(
            validate='all',
            validatecommand=(self.register(self._validate), '%P'),
            invalidcommand=(self.register(self._on_invalid), '%P')
        )

    def _validate(self, proposed):
        return len(proposed) <= 5

    def _on_invalid(self, proposed):
        self.error.set(
            f'{proposed} is too long, only 5 chars allowed'
        )


root = tk.Tk()
entry = FiveCharEntry(root)
error_label = tk.Label(
    root, textvariable=entry.error, foreground='red'
)
entry.grid()
error_label.grid()
root.mainloop()


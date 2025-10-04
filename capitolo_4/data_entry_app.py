"""
    ------------------------------------------------------
    Chapter 4 - data_entry_app.py with objects and classes
    ------------------------------------------------------
"""

from datetime import datetime
from pathlib import Path
import csv
import tkinter as tk
from tkinter import ttk

from mpmath.matrices.matrices import rowsep

"""
    SCOPO DELLA CLASSE `BoundText`:
    =============================
    Questa classe estende il widget standard `tk.Text` per aggiungere una
    funzionalità fondamentale che manca nativamente: il "two-way data binding"
    (collegamento dati a due vie) tramite l'opzione `textvariable`.

    In pratica, un'istanza di `BoundText` e una variabile di controllo di Tkinter
    (come `tk.StringVar`) rimangono costantemente sincronizzate:
    1.  Se la variabile viene modificata programmaticamente (es. `var.set(...)`),
        il testo nel widget si aggiorna automaticamente.
    2.  Se l'utente scrive o modifica il testo all'interno del widget,
        la variabile collegata viene aggiornata di conseguenza.

    COME FUNZIONA (ANALISI TECNICA):
    ================================
    Il two-way binding è implementato attraverso due meccanismi distinti:

    1.  Binding "dalla Variabile al Widget":
        - Nel costruttore `__init__`, viene impostato un "osservatore" (`trace`)
          sulla variabile tramite `self._variable.trace_add('write', ...)`.
        - Questo `trace` fa sì che, ogni volta che la variabile viene "scritta"
          (modificata), venga eseguito il metodo `_set_content`.
        - `_set_content` si occupa di cancellare il testo attuale del widget
          e inserire il nuovo valore preso dalla variabile.

    2.  Binding "dal Widget alla Variabile":
        - Nel metodo `_set_content`, il widget viene collegato all'evento
          virtuale `<<Modified>>` tramite `self.bind('<<Modified>>', ...)`.
        - Questo evento viene generato da Tkinter ogni volta che il contenuto
          del widget `Text` viene alterato (es. dall'utente che scrive).
        - L'evento scatena l'esecuzione del metodo `_set_var`, che a sua volta:
          a) Controlla se la modifica è reale con `self.edit_modified()`.
          b) Legge il nuovo contenuto del widget con `self.get(...)`.
          c) Aggiorna la variabile collegata con `self._variable.set(...)`.
          d) Resetta il flag di modifica con `self.edit_modified(False)` per
             essere pronti alla modifica successiva.

    CRITICITÀ - RISCHIO DI RICORSIONE INFINITA:
    ===========================================
    L'implementazione attuale, sebbene intelligente, presenta un serio rischio
    di ricorsione infinita che può bloccare l'applicazione.
    Il ciclo è il seguente:
    1. L'utente scrive -> `_set_var` viene chiamato.
    2. `_set_var` aggiorna la variabile.
    3. L'aggiornamento della variabile fa scattare il `trace` -> `_set_content` viene chiamato.
    4. `_set_content` modifica il widget.
    5. La modifica del widget fa scattare di nuovo l'evento `<<Modified>>`... e il ciclo ricomincia.
"""
class BoundText(tk.Text):
    """A Text widget with a bound variable"""
    def __init__(self, *args, textvariable=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._variable = textvariable
        if self._variable:
            self.insert('1.0', self._variable.get())
            self._variable.trace_add('write', self._set_content)

    def _set_content(self, *_):
        """Set the text contents to the variable"""
        self.delete('1.0', tk.END)
        self.insert('1.0', self._variable.get())
        self.bind('<<Modified>>', self._set_var)

    def _set_var(self, *_):
        """Set the variable to the text contents"""
        if self.edit_modified():
            content = self.get('1.0', 'end-1chars')
            self._variable.set(content)
            self.edit_modified(False)

"""
    SCOPO DELLA CLASSE `LabelInput`:
    ==============================
    Questa classe è un "compound widget" (widget composto) avanzato, progettata
    per standardizzare e semplificare drasticamente la creazione di form in Tkinter.
    L'idea è di incapsulare un'etichetta (`ttk.Label`) e un campo di input
    (come `ttk.Entry`, `ttk.Spinbox`, `ttk.Checkbutton`, ecc.) in un unico oggetto,
    gestendoli come una sola unità logica e visiva.

    Questo approccio offre vantaggi significativi:
    - Riduce il codice ripetitivo: Invece di creare e posizionare una Label
      e un widget di input separatamente per ogni campo, si crea una sola
      istanza di `LabelInput`.
    - Migliora la leggibilità e la manutenibilità: Il codice per la creazione
      dell'interfaccia diventa più pulito, dichiarativo e facile da modificare.
    - Aumenta la flessibilità: Grazie ai parametri `input_class` e
      `input_args`, la classe è estremamente versatile e può generare
      coppie label-input con quasi ogni tipo di widget `ttk`,
      configurandoli in modo personalizzato.

    COME FUNZIONA (ANALISI TECNICA):
    ===========================================
    - La classe eredita da `ttk.Frame`, agendo come un contenitore per
      la Label e l'input.

    - Il costruttore `__init__` è il cuore della classe e implementa una
      logica sofisticata per adattarsi a diversi tipi di widget:
        - `input_class`: Specifica quale widget di input creare (es. `ttk.Entry`).
        - `input_args`: Un dizionario di opzioni da passare al costruttore
          del widget di input (es. `{'values': ['A', 'B', 'C']}`).

    - La classe gestisce diversi casi in modo intelligente:
        1. Caso Generale (es. `ttk.Entry`, `ttk.Spinbox`, `ttk.Combobox`):
           - Crea una `ttk.Label` standard.
           - Crea il widget di input specificato, collegandolo alla `textvariable`.
           - Posiziona la Label sopra e l'input sotto, usando `grid`.

        2. Caso Speciale (`ttk.Checkbutton`, `ttk.Button`):
           - Riconosce che questi widget hanno già una loro etichetta (`text`).
           - Non crea una `ttk.Label` separata, ma passa il testo `label`
             direttamente all'argomento `text` del widget.

        3. Caso Speciale (`ttk.Radiobutton`):
           - Questa è la gestione più complessa. La classe si aspetta di
             trovare una lista di valori in `input_args['values']`.
           - Crea un `Frame` interno e, per ogni valore nella lista, crea
             un `ttk.Radiobutton` e lo impacchetta orizzontalmente (`side=tk.LEFT`).
             Questo permette di creare gruppi di radio button con una sola riga
             di codice.

    - La riga `self.variable.label_widget = self` è una tecnica avanzata:
      crea un riferimento incrociato che permette, partendo dalla variabile
      di controllo, di risalire al widget `LabelInput` che la gestisce.
      Questo può essere molto utile per la validazione degli errori (es.
      per cambiare il colore della label se il dato non è valido).

    - `def grid(...)`: La classe sovrascrive il metodo `grid` per impostare
      un valore di default per l'opzione `sticky`. Questo assicura che,
      per impostazione predefinita, ogni `LabelInput` si espanda per
      occupare tutta la larghezza disponibile, mantenendo l'interfaccia
      allineata e ordinata.
"""
class LabelInput(tk.Frame):
    """A widget containing a label and input togheter"""

    def __init__(
            self, parent, label, var, input_class=ttk.Entry,
            input_args=None, label_args=None, **kwargs
    ):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = var
        self.variable.label_widget = self

        if input_class in (ttk.Checkbutton, ttk.Button):
            input_args["text"] = label
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))

        if input_class in (
                ttk.Checkbutton, ttk.Button, ttk.Radiobutton
        ):
            input_args["variable"] = self.variable
        else:
            input_args["textvariable"] = self.variable

        if input_class == ttk.Radiobutton:
            self.input = tk.Frame(self)
            for v in input_args.pop('values', []):
                button = ttk.Radiobutton(
                    self.input, value=v, text=v, **input_args
                )
                button.pack(
                    side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill='x'
                )
        else:
            self.input = input_class(self, **input_args)
            self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
            self.columnconfigure(0, weight=1)


    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        """Override grid to add default sticky values"""
        super().grid(sticky=sticky, **kwargs)


class DataRecordForm(ttk.Frame):
    """Costruttore della classe DataRecordForm.

             Questo metodo viene eseguito alla creazione di un'istanza della classe
             e ha il compito fondamentale di inizializzare lo stato interno del form.

             ANALISI TECNICA:
             1.  `super().__init__(...)`: Chiama il costruttore della classe genitore
                 (`ttk.Frame`), assicurando che il nostro form sia a tutti gli effetti
                 un widget Frame di Tkinter, pronto per contenere altri widget.

             2.  `self._vars = {...}`: Questa è la parte più importante. Crea un
                 attributo di istanza privato (`_vars`) che funge da **modello dati
                 centralizzato** per l'intero form.
                 -   **Incapsulamento**: Sostituisce la vecchia variabile globale
                     `variables`, incapsulando lo stato all'interno dell'oggetto.
                     Questo è un principio chiave della programmazione a oggetti,
                     che rende il codice più sicuro, pulito e manutenibile.
                 -   **Struttura**: È un dizionario dove le chiavi sono i nomi
                     logici dei campi (es. 'Date', 'Humidity') e i valori sono le
                     variabili di controllo di Tkinter (`StringVar`, `IntVar`, etc.)
                     che verranno collegate ai widget di input.
                 -   **Fondamenta per la GUI**: Questo dizionario è la base su cui
                     verrà costruita dinamicamente l'intera interfaccia grafica.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._vars = {
            'Date': tk.StringVar(),
            'Time': tk.StringVar(),
            'Technician': tk.StringVar(),
            'Lab': tk.StringVar(),
            'Plot': tk.IntVar(),
            'Seed Sample': tk.StringVar(),
            'Humidity': tk.DoubleVar(),
            'Light': tk.DoubleVar(),
            'Temperature': tk.DoubleVar(),
            'Equipment Fault': tk.BooleanVar(),
            'Plants': tk.IntVar(),
            'Blossoms': tk.IntVar(),
            'Fruit': tk.IntVar(),
            'Min Height': tk.DoubleVar(),
            'Max Height': tk.DoubleVar(),
            'Med Height': tk.DoubleVar(),
            'Notes': tk.StringVar()
        }

        # ---------------------------------------------

        # Record Information
        r_info = self._add_frame("Record Information")

        #---------------------------------------------

        # Date
        LabelInput(
            r_info, "Date", var=self._vars["Date"]
        ).grid(row=0, column=0)

        # Time
        LabelInput(
            r_info, "Time", input_class=ttk.Combobox,
            var=self._vars["Time"],
            input_args={"values": ['8:00', '12:00', '16:00', '20:00']}
        ).grid(row=0, column=1)

        # Technician
        LabelInput(
            r_info, "Technician", var=self._vars["Technician"]
        ).grid(row=0, column=2)

        # ---------------------------------------------











    def _add_frame(self, label: str, cols: int = 3) -> ttk.LabelFrame:
        """Crea e configura un contenitore LabelFrame per raggruppare i widget.

        Questo è un metodo "helper" (di supporto) privato, progettato per
        ridurre la duplicazione del codice nella costruzione dell'interfaccia.
        Il suo compito è creare un `ttk.LabelFrame`, che è un contenitore
        con un bordo e un'etichetta, ideale per raggruppare sezioni
        logiche del form (es. "Record Information", "Environment Data").

        Args:
            label (str): Il testo da visualizzare come titolo del LabelFrame.
            cols (int, optional): Il numero di colonne che il layout a griglia
                all'interno del frame deve avere. Default a 3.

        Returns:
            ttk.LabelFrame: Il widget LabelFrame appena creato e configurato.
        """
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)

        # Questa è la parte fondamentale per un layout responsive:
        # Configura le colonne all'interno del frame affinché si espandano
        # in modo uniforme quando la finestra viene ridimensionata.
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame


"""
    ------------------------------------------------------
    Chapter 5 - data_entry_app.py with field validation
    ------------------------------------------------------
"""

from datetime import datetime
from pathlib import Path
import csv
import tkinter as tk
from tkinter import ttk, Radiobutton

from mpmath.matrices.matrices import rowsep
from pygments.styles.dracula import foreground
from sqlalchemy import column
from uri_template import validate

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
    """Un widget Text con una variabile collegata (two-way binding)."""
    def __init__(self, *args, textvariable=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._variable = textvariable
        if self._variable:
            # Imposta il contenuto iniziale e lega gli eventi in modo sicuro
            self.insert('1.0', self._variable.get())

            # 1. Binding: dalla Variabile al Widget
            self._variable.trace_add('write', self._from_var_to_widget)

            # 2. Binding: dal Widget alla Variabile
            self.bind('<<Modified>>', self._from_widget_to_var)

    def _from_var_to_widget(self, *_):
        """Aggiorna il widget quando la variabile cambia, evitando cicli."""
        widget_content = self.get('1.0', 'end-1c')
        var_content = self._variable.get()
        if widget_content != var_content:
            self.delete('1.0', tk.END)
            self.insert('1.0', var_content)

    def _from_widget_to_var(self, *_):
        """Aggiorna la variabile quando l'utente scrive nel widget."""
        if self.edit_modified():
            content = self.get('1.0', 'end-1c')
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

        # Assegna la variabile al widget di input
        if input_class == ttk.Radiobutton:
            # I Radiobutton non usano 'textvariable', ma 'variable' passata a ogni bottone.
            # La gestione è fatta nel ciclo qui sotto.
            pass
        elif input_class in (ttk.Checkbutton, ttk.Button):
            input_args['variable'] = self.variable
        else:
            # Per Entry, Combobox, Spinbox, etc.
            input_args["textvariable"] = self.variable

        if input_class == ttk.Radiobutton:
            self.input = tk.Frame(self)
            # Configura le colonne del frame interno per dare spazio ai bottoni
            values = input_args.pop('values', [])
            for i, v in enumerate(values):
                self.input.columnconfigure(i, weight=1)
                # Passa la variabile esplicitamente a ogni Radiobutton
                button = ttk.Radiobutton(self.input, value=v, text=v, variable=self.variable, **input_args)
                # Usa grid() invece di pack()
                button.grid(row=0, column=i, padx=10, sticky='ew')
            # Posiziona il frame contenitore dei radio button
            self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        else:
            self.input = input_class(self, **input_args)
            self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))


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

        # Lab
        LabelInput(
            r_info, "Lab", input_class=ttk.Radiobutton,
            var=self._vars["Lab"],
            input_args={"values": ["A", "B", "C"]}
        ).grid(row=1, column=0)

        # Plot
        LabelInput(
            r_info, "Plot", input_class=ttk.Combobox,
            var=self._vars["Plot"],
            input_args={"values": list(range(1,21))}
        ).grid(row=1, column=1)

        #Seed Sample
        LabelInput(
            r_info, "Seed Sample", var=self._vars["Seed Sample"]
        ).grid(row=1, column=2)

        # ---------------------------------------------

        # Environment Data
        e_info = self._add_frame("Environment Data")

        # ---------------------------------------------

        # Humidity
        LabelInput(
            e_info, "Humidity (g/m)", input_class=ttk.Spinbox,
            var=self._vars["Humidity"],
            input_args={"from_" : 0.5, "to" : 52.0, "increment" : .01}
        ).grid(row=0, column=0)

        # Light klx
        LabelInput(
            e_info, "Light (klx)", input_class=ttk.Spinbox,
            var=self._vars["Light"],
            input_args={"from_": 0, "to": 100, "increment": .01}
        ).grid(row=0, column=1)

        # Temperature
        LabelInput(
            e_info, "Temperature (Celsius)", input_class=ttk.Spinbox,
            var=self._vars["Temperature"],
            input_args={"from_": 4, "to": 40, "increment": .01}
        ).grid(row=0, column=2)

        # Equipment Fault
        LabelInput(
            e_info, "Equipment Fault", input_class=ttk.Checkbutton,
            var=self._vars["Equipment Fault"]
        ).grid(row=1, column=0, columnspan=3)

        # ---------------------------------------------

        p_info = self._add_frame("Plant Data")

        # ---------------------------------------------

        # Plants
        LabelInput(
            p_info, "Plants", input_class=ttk.Spinbox,
            var=self._vars["Plants"],
            input_args={"from_": 0, "to": 20}
        ).grid(row=0, column=0)

        # Blossoms
        LabelInput(
            p_info, "Blossoms", input_class=ttk.Spinbox,
            var=self._vars["Blossoms"],
            input_args={"from_": 0, "to": 1000}
        ).grid(row=0, column=1)

        # Fruit
        LabelInput(
            p_info, "Fruit", input_class=ttk.Spinbox,
            var=self._vars["Fruit"],
            input_args={"from_": 0, "to": 1000}
        ).grid(row=0, column=2)

        # Min Height
        LabelInput(
            p_info, "Min Height (cm)", input_class=ttk.Spinbox,
            var=self._vars["Min Height"],
            input_args={"from_": 0, "to": 1000, "increment": .01}
        ).grid(row=1, column=0)

        # Max Height
        LabelInput(
            p_info, "Max Height (cm)", input_class=ttk.Spinbox,
            var=self._vars["Max Height"],
            input_args={"from_": 0, "to": 1000, "increment": .01}
        ).grid(row=1, column=1)

        # Median Height
        LabelInput(
            p_info, "Med Height (cm)", input_class=ttk.Spinbox,
            var=self._vars["Med Height"],
            input_args={"from_": 0, "to": 1000, "increment": .01}
        ).grid(row=1, column=2)

        # ---------------------------------------------

        # Notes Section
        LabelInput(
            self, "Notes", input_class=BoundText,
            var=self._vars["Notes"],
            input_args={"width": 75, "height": 10}
        ).grid(sticky=tk.W, row=3, column=0)

        # ---------------------------------------------

        # final button section
        buttons = tk.Frame(self)
        buttons.grid(sticky=tk.W + tk.E, row=4)
        self.savebutton = ttk.Button(buttons, text="Save", command=self.master._on_save)
        self.savebutton.pack(side=tk.RIGHT)
        self.resetbutton = ttk.Button(buttons, text="Reset", command=self.reset)
        self.resetbutton.pack(side=tk.RIGHT)

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


    def reset(self):
        """Resetta tutti i campi del form al loro stato iniziale.

         Questo metodo viene chiamato quando l'utente preme il pulsante "Reset".
         Il suo compito è svuotare tutti i widget di input per preparare il form
         a un nuovo inserimento di dati.

         ANALISI TECNICA:
         -   Scorre tutte le variabili di controllo di Tkinter contenute nel
             dizionario `self._vars`.
         -   Per ogni variabile, applica la logica di reset corretta in base al
             suo tipo per evitare errori:
             - `BooleanVar` (per i Checkbutton) viene impostato a `False`.
             - `StringVar` (per Entry, Combobox di testo) viene impostato a una
               stringa vuota `''`.
             - `IntVar` e `DoubleVar` (per Spinbox, Combobox numerici) vengono
               impostati a `0`. Questo è fondamentale per evitare un errore
               `tk.TclError`, poiché queste variabili non accettano una stringa
               vuota come valore.
         """

        for var in self._vars.values():
            if isinstance(var, tk.BooleanVar):
                var.set(False)
            elif isinstance(var, (tk.IntVar, tk.DoubleVar)):
                var.set(0)
            else:
                var.set('')



    def get(self):
        """
        Recupera i dati da tutti i campi del form e li restituisce come dizionario.
        Questo metodo è il punto di contatto principale per ottenere lo stato
        corrente del form. Viene chiamato dalla logica di salvataggio per
        raccogliere i dati prima di scriverli su file.
        Implementa anche una logica di business specifica per il caso
        'Equipment Fault' e una validazione di base dei tipi di dato.
        Returns:
            dict: Un dizionario contenente i dati del form, con le chiavi
                           che corrispondono alle etichette dei campi.
        Raises:
            ValueError: Se un campo contiene un valore non valido (es. testo
            in un campo numerico), viene sollevata un'eccezione con un messaggio di errore descrittivo
        """
        data = dict()
        fault = self._vars['Equipment Fault'].get()
        for key, variable in self._vars.items():
            if fault and key in ('Light', 'Humidity', 'Temperature'):
                data[key] = ''
            else:
                try:
                    data[key] = variable.get()
                except tk.TclError:
                    message = f'Erro in field: {key}. Data was not saved!'
                    raise ValueError(message)

        return data




class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ABQ Data Entry Application")
        self.columnconfigure(0, weight=1)

        # define a title Label for the Application
        ttk.Label(
            self, text="ABQ Data Entry Application", font=("TkDefaultFont", 16)
        ).grid(row=0)

        # insert instnace of Data Record Form
        self.recordform = DataRecordForm(self)
        self.recordform.grid(row=1, padx=10, sticky=(tk.W + tk.E))

        # define a status bar
        self.status = tk.StringVar()
        ttk.Label(
            self, textvariable=self.status
        ).grid(sticky=(tk.W + tk.E), row=2, padx=10)

        self._record_saved = 0


    def _on_save(self):
        """Gestisce l'evento di click sul pulsante "Save".

        Questo metodo agisce come il "controllore" per l'operazione di salvataggio.
        Orchestra l'interazione tra il form (`DataRecordForm`) e la logica di
        scrittura su file, seguendo il principio della separazione delle competenze.

        ANALISI TECNICA:
        1.  **Recupero e Validazione**: Chiama il metodo `self.recordform.get()`
            per recuperare i dati. La chiamata è racchiusa in un blocco `try...except`
            per catturare i `ValueError` sollevati dal form in caso di dati
            non validi (es. testo in un campo numerico).
            - Se viene catturato un errore, il salvataggio viene interrotto,
              e il messaggio di errore viene mostrato nella barra di stato.

        2.  **Gestione del File**: Determina il nome del file CSV basandosi
            sulla data corrente (es. `abq_data_record_2023-10-27.csv`).
            Controlla se il file esiste già per decidere se scrivere o meno
            la riga di intestazione (header).

        3.  **Scrittura dei Dati**: Apre il file in modalità "append" (`'a'`) e
            usa `csv.DictWriter` per scrivere i dati. Questo approccio è
            robusto perché scrive i dati basandosi sui nomi delle colonne,
            indipendentemente dal loro ordine.

        4.  **Feedback e Reset**: Dopo un salvataggio riuscito, aggiorna la
            barra di stato con il conteggio dei record salvati e chiama
            `self.recordform.reset()` per preparare il form a un nuovo
            inserimento.
        """
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "abq_data_record_{}.csv".format(datestring)
        newfile = not Path(filename).exists()

        try:
            data = self.recordform.get()
        except ValueError as e:
            self.status.set(str(e))
            return  # Interrompe l'esecuzione in caso di errore

        with open(filename, 'a', newline='') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

        self._record_saved += 1
        self.status.set("{} records saved this session".format(self._record_saved))
        self.recordform.reset()


class ValidateMixin:
    """Un "Mixin" che aggiunge una funzionalità di validazione completa a un widget.

     Questa non è una classe pensata per essere usata da sola, ma per essere
     "mescolata" (da cui il nome Mixin) con altre classi di widget (come
     `ttk.Entry`, `ttk.Spinbox`) tramite ereditarietà multipla.

     Il suo scopo è automatizzare completamente la configurazione del sistema
     di validazione di Tkinter, lasciando alla classe figlia solo il compito
     di definire la logica di validazione specifica.

     ARCHITETTURA E FUNZIONAMENTO:
     -----------------------------
     1.  **`__init__`**: Il costruttore esegue tutta la configurazione:
         -   `self.error`: Garantisce che il widget abbia sempre una `StringVar`
             per i messaggi di errore.
         -   `super().__init__`: Chiama il costruttore della classe successiva
             nell'ordine di ereditarietà (es. `ttk.Entry`), assicurando che
             il widget venga creato correttamente.
         -   `self.register()`: Registra i metodi `_validate` e `_invalid`
             (che devono essere implementati dalla classe figlia) per renderli
             chiamabili da Tkinter.
         -   `self.configure()`: "Accende" il sistema di validazione sul widget,
             collegando gli eventi ai comandi registrati e specificando quali
             dati passare tramite i codici di sostituzione (`%P`, `%s`, ecc.).

     2.  **Metodi Segnaposto**: `_validate` e `_invalid` sono definiti qui
         con una logica di default (restituisce sempre `True`, non fa nulla
         in caso di errore). Questo previene errori se una classe figlia
         dimentica di sovrascriverli.

     ESEMPIO DI UTILIZZO:
     --------------------
     class ValidatedEntry(ValidateMixin, ttk.Entry):
         def _validate(self, *args):
             # ... logica di validazione specifica ...
         def _invalid(self, *args):
             # ... logica per gestire l'errore ...
     """
    def __init__(self, *args, error_var=None, **kwargs):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)

        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)

        self.configure(
            validate='all',
            validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
            invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d')
        )


    def _toggle_error(self, on=False):
        """Attiva o disattiva il feedback visivo di errore sul widget.

                 Questo è un metodo "helper" privato che centralizza la logica per
                 cambiare l'aspetto del widget stesso (in questo caso, il colore del
                 testo) per indicare uno stato di errore o uno stato normale.

                 Viene chiamato dai metodi di validazione per fornire un feedback
                 visivo immediato e inequivocabile direttamente sul campo errato.

                 Args:
                     on (bool, optional): Un flag booleano che determina lo stato.
                         - Se `True`, il testo del widget viene colorato di rosso.
                         - Se `False` (default), il testo del widget torna nero.
                 """
        self.configure(foreground=('red' if on else 'black'))


    def _validate(self, proposed, current, char, event, index, action):
        """Metodo "centralino" che orchestra il processo di validazione.

            Questo è il metodo principale chiamato da Tkinter per ogni evento di
            validazione. Non contiene la logica di validazione specifica, ma agisce
            come un "dispatcher": determina il tipo di evento e delega il lavoro
            ai metodi specializzati (`_key_validate` o `_focusout_validate`).

            Questo approccio, basato sul "Principio di Separazione delle Competenze",
            mantiene il Mixin pulito e permette alle classi figlie di sovrascrivere
            solo la logica di cui hanno bisogno.

            ANALISI TECNICA:
            1.  **Reset dello Stato di Errore**: All'inizio di ogni chiamata, resetta
                il messaggio di errore e il feedback visivo. Questo assicura che
                gli errori non siano "persistenti" e che lo stato venga
                rivalutato a ogni interazione.
            2.  **Controllo dello Stato 'DISABLED'**: Come prima cosa, controlla se
                il widget è disabilitato. In tal caso, la validazione viene saltata
                restituendo `True`. È una pratica robusta per evitare validazioni
                indesiderate.
            3.  **Delega basata sull'Evento**:
                - Se `event == 'focusout'`, delega la validazione al metodo
                  `_focusout_validate`.
                - Se `event == 'key'`, delega la validazione al metodo
                  `_key_validate`, passandogli tutti gli argomenti necessari.
            """
        self.error.set('')
        self._toggle_error()

        # if widget is disabled don't validate
        state = str(self.configure('state')[-1])
        if state == tk.DISABLED:
            return True

        valid = True
        if event == 'focusout':
            valid = self._focusout_validate(proposed=proposed, event=event)
        elif event == 'key':
            valid = self._key_validate(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )
        return valid


    def _focusout_validate(self, **kwargs):
        """Metodo segnaposto per la validazione all'uscita dal campo (focus-out).

                 Questo metodo è progettato per essere **sovrascritto** dalle classi
                 figlie che utilizzano il `ValidateMixin`.

                 Il suo scopo è contenere la logica di validazione che deve essere
                 eseguita solo quando l'utente ha finito di interagire con il widget
                 e sposta il focus altrove.

                 Esempi di utilizzo nelle classi figlie:
                 -   In un campo per date, controllerebbe che la data sia semanticamente
                     valida (es. "2023-02-30" non è valido).
                 -   In un campo obbligatorio, controllerebbe che il valore non sia vuoto.

                 Args:
                     **kwargs: Accetta qualsiasi argomento nominato per massima
                               flessibilità, anche se nella sua forma base non li usa.

                 Returns:
                     bool: Per default restituisce `True`, significando che, se non
                           sovrascritto, nessuna validazione specifica viene eseguita
                           al focus-out.
                 """
        return True

    def _key_validate(self, **kwargs):
        """Metodo segnaposto per la validazione a ogni pressione di un tasto.

                 Questo metodo è progettato per essere **sovrascritto** dalle classi
                 figlie che utilizzano il `ValidateMixin`.

                 Il suo scopo è contenere la logica di "Input Filtering", ovvero la
                 validazione che viene eseguita in tempo reale mentre l'utente digita.
                 È ideale per impedire fisicamente l'inserimento di caratteri non validi.

                 Esempi di utilizzo nelle classi figlie:
                 -   In un campo numerico, bloccherebbe l'inserimento di lettere.
                 -   In un campo per date con formato fisso, permetterebbe solo cifre
                     e trattini nelle posizioni corrette.

                 Args:
                     **kwargs: Accetta tutti gli argomenti di validazione (proposed,
                               current, char, ecc.) come argomenti nominati, offrendo
                               massima flessibilità alle classi figlie.

                 Returns:
                     bool: Per default restituisce `True`, significando che, se non
                           sovrascritto, qualsiasi carattere digitato è considerato
                           valido.
                 """
        return True


    def _invalid(self, proposed, current, char, event, index, action):
        """
            Gestore centrale per gli eventi di validazione.
            Questo metodo viene chiamato quando l'input nel widget non è valido.
            In base al tipo di evento ('focusout' o 'key'), delega la gestione
            al metodo specifico corrispondente.
        """
        if event == 'focusout':
            self._focusout_invalid(event=event)
        elif event == 'key':
            self._key_invalid(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )

    def _focusout_invalid(self, **kwargs):
        """
            Gestisce l'input non valido quando il widget perde il focus.
            Quando l'utente si sposta su un altro campo e il valore inserito
            non è valido, questo metodo viene invocato per mostrare un feedback
            visivo di errore (ad esempio, cambiando il colore del bordo).
        """
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        """
            Gestisce l'input non valido durante la digitazione (evento 'key').
            Per impostazione predefinita, questo metodo non fa nulla, ma può essere
            sovrascritto nelle sottoclassi per implementare una logica specifica,
            come impedire l'inserimento di caratteri non validi in tempo reale.
        """
        pass

    def trigger_focus_validation(self):
        """
            Attiva manualmente la validazione del widget come se avesse perso il focus.

            Questo metodo è utile per forzare il controllo di validità di un campo,
            ad esempio quando si preme un pulsante "Salva" e si vuole verificare
            che tutti i campi siano compilati correttamente prima di procedere.

            Simula un evento 'focusout', controlla se il contenuto attuale è valido
            e, in caso negativo, attiva il feedback visivo di errore.

            Restituisce:
                bool: True se il contenuto del widget è valido, altrimenti False.
        """
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid















if __name__ == "__main__":
    app = Application()
    app.mainloop()
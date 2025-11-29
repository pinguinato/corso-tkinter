import tkinter as tk
from tkinter import ttk
from datetime import datetime

# in questo modo importo il module dei widgets.py
from . import widgets as w
from .constants import FieldTypes as FT


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

    var_types = {
        FT.string: tk.StringVar,
        FT.string_list: tk.StringVar,
        FT.short_string_list: tk.StringVar,
        FT.iso_date_string: tk.StringVar,
        FT.long_string: tk.StringVar,
        FT.decimal: tk.DoubleVar,
        FT.integer: tk.IntVar,
        FT.boolean: tk.BooleanVar
    }

    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.model = model
        fields = self.model.fields

        """
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
        """

        # Create a dict to keep track of input widgets
        self._vars = {
            key: self.var_types[spec['type']]()
            for key, spec in fields.items()
        }

        # Build the form
        self.columnconfigure(0, weight=1)

        # ---------------------------------------------

        # Record Information
        r_info = self._add_frame("Record Information")

        # ---------------------------------------------

        # Date
        w.LabelInput(
            r_info, "Date",
            field_spec=fields['Date'],
            var=self._vars["Date"]
        ).grid(row=0, column=0)

        # Time
        w.LabelInput(
            r_info, "Time",
            field_spec=fields['Time'],
            var=self._vars["Time"]
        ).grid(row=0, column=1)

        # Technician
        w.LabelInput(
            r_info, "Technician",
            field_spec=fields['Technician'],
            var=self._vars["Technician"]
        ).grid(row=0, column=2)

        # ---------------------------------------------

        # Lab
        w.LabelInput(
            r_info, "Lab",
            field_spec=fields['Lab'],
            var=self._vars["Lab"]
        ).grid(row=1, column=0)

        # Plot
        w.LabelInput(
            r_info, "Plot",
            field_spec=fields['Plot'],
            var=self._vars["Plot"]
        ).grid(row=1, column=1)

        # Seed Sample
        w.LabelInput(
            r_info, "Seed Sample",
            field_spec=fields['Seed Sample'],
            var=self._vars["Seed Sample"]
        ).grid(row=1, column=2)

        # ---------------------------------------------

        # Environment Data
        e_info = self._add_frame("Environment Data")

        # ---------------------------------------------

        # Humidity
        w.LabelInput(
            e_info, "Humidity (g/m)", input_class=w.ValidatedSpinbox,
            var=self._vars["Humidity"],
            input_args={"from_" : 0.5, "to" : 52.0, "increment" : .01},
            disable_var=self._vars['Equipment Fault']
        ).grid(row=0, column=0)

        # Light klx
        w.LabelInput(
            e_info, "Light (klx)",
            var=self._vars["Light"],
            field_spec=fields['Light'],
            disable_var=self._vars['Equipment Fault']
        ).grid(row=0, column=1)

        # Temperature
        w.LabelInput(
            e_info, "Temperature (Celsius)",
            field_spec=fields['Temperature'],
            var=self._vars["Temperature"],
            disable_var=self._vars['Equipment Fault']
        ).grid(row=0, column=2)

        # Equipment Fault
        w.LabelInput(
            e_info, "Equipment Fault",
            field_spec=fields['Equipment Fault'],
            var=self._vars["Equipment Fault"]
        ).grid(row=1, column=0, columnspan=3)

        # ---------------------------------------------

        p_info = self._add_frame("Plant Data")

        # ---------------------------------------------

        # Plants
        w.LabelInput(
            p_info, "Plants",
            field_spec=fields['Plants'],
            var=self._vars["Plants"]
        ).grid(row=0, column=0)

        # Blossoms
        w.LabelInput(
            p_info, "Blossoms",
            field_spec=fields['Blossoms'],
            var=self._vars["Blossoms"]
        ).grid(row=0, column=1)

        # Fruit
        w.LabelInput(
            p_info, "Fruit",
            field_spec=fields['Fruit'],
            var=self._vars["Fruit"]
        ).grid(row=0, column=2)

        min_height_var = tk.DoubleVar(value='-infinity')
        max_height_var = tk.DoubleVar(value='infinity')

        # Min Height
        w.LabelInput(
            p_info, "Min Height (cm)", input_class=w.ValidatedSpinbox,
            var=self._vars["Min Height"],
            input_args={
                "from_": 0,
                "to": 1000,
                "increment": .01,
                "max_var": max_height_var,
                "focus_update_var": min_height_var
            }
        ).grid(row=1, column=0)

        # Max Height
        w.LabelInput(
            p_info, "Max Height (cm)", input_class=w.ValidatedSpinbox,
            var=self._vars["Max Height"],
            input_args={
                "from_": 0,
                "to": 1000,
                "increment": .01,
                "min_var": min_height_var,
                "focus_update_var": max_height_var
            }
        ).grid(row=1, column=1)

        # Median Height
        w.LabelInput(
            p_info, "Med Height (cm)", input_class=w.ValidatedSpinbox,
            var=self._vars["Med Height"],
            input_args={
                "from_": 0,
                "to": 1000,
                "increment": .01,
                "min_var": min_height_var,
                "max_var": max_height_var
            }
        ).grid(row=1, column=2)

        # ---------------------------------------------

        # Notes Section
        w.LabelInput(
            self, "Notes", input_class=w.BoundText,
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

        lab = self._vars['Lab'].get()
        time = self._vars['Time'].get()
        technician = self._vars['Technician'].get()
        try:
            plot = self._vars['Plot'].get()
        except tk.TclError:
            plot = ''
        plot_values = (self._vars['Plot'].label_widget.input.cget('values'))

        for var in self._vars.values():
            if isinstance(var, tk.BooleanVar):
                var.set(False)
            elif isinstance(var, (tk.IntVar, tk.DoubleVar)):
                var.set(0)
            else:
                var.set('')

        """
            Queste righe permettono di inserire in automatico la data ad ogni reset
            e posizionarsi con il focus sul campo Time direttamente
        """
        current_date = datetime.today().strftime('%Y-%m-%d')
        self._vars['Date'].set(current_date)
        self._vars['Time'].label_widget.input.focus()

        if plot not in ('', 0, plot_values[-1]):
            self._vars['Lab'].set(lab)
            self._vars['Time'].set(time)
            self._vars['Technician'].set(technician)
            next_plot_index = plot_values.index(str(plot)) + 1
            self._vars['Plot'].set(plot_values[next_plot_index])
            self._vars['Seed Sample'].label_widget.input.focus()

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
        data = {}
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

    def get_errors(self):
        """Forza una validazione completa su tutti i campi e restituisce gli errori.

         Questo metodo è cruciale per la validazione pre-salvataggio. Scorre
         tutti i widget del form, forza l'esecuzione della loro validazione
         "on focus-out" (anche se l'utente non ha lasciato il campo) e
         raccoglie tutti i messaggi di errore attivi in un dizionario.

         Returns:
             dict: Un dizionario dove le chiavi sono i nomi dei campi con errori
                   e i valori sono i rispettivi messaggi di errore.
                   Restituisce un dizionario vuoto se non ci sono errori.

         ANALISI TECNICA:
         1.  Iterazione: Scorre il dizionario `self._vars` per analizzare
             ogni campo del form.
         2.  Accesso ai Widget: Usa il riferimento `var.label_widget` per
             risalire dalla variabile di controllo al widget `LabelInput` e
             da lì al widget di input vero e proprio (`inp`) e alla sua
             variabile di errore (`error`).
         3.  Validazione Forzata: La parte più importante. `hasattr(...)`
             controlla se il widget di input ha un metodo `trigger_focusout_validation`.
             Se sì, lo chiama. Questo simula un evento "focus-out", forzando
             la validazione di regole come "campo obbligatorio" anche se
             l'utente è ancora posizionato su quel campo.
         4.  Raccolta degli Errori: Dopo la validazione forzata, controlla
             se la variabile di errore del widget contiene un messaggio. In caso
             affermativo, lo aggiunge al dizionario `errors`.
         """
        errors = {}
        for key, var in self._vars.items():
            inp = var.label_widget.input
            error = var.label_widget.error

            if hasattr(inp, 'trigger_focusout_validation'):
                inp.trigger_focusout_validation()
            if error.get():
                errors[key] = error.get()

        return errors

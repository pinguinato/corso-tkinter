import tkinter as tk
from tkinter import ttk
from datetime import datetime
from . import widgets as w
from .constants import FieldTypes as FT
from tkinter.simpledialog import Dialog  # Serve per la generazione della finestra di Login


class DataRecordForm(tk.Frame):
    """
  La classe che rappresenta la **Vista** (la "V" del pattern MVC) del form.

  Questa classe è responsabile della costruzione e della presentazione dell'interfaccia
  utente per l'inserimento dei dati. Eredita da `tk.Frame` per agire come
  un contenitore principale per tutti i widget del form.

  ARCHITETTURA E FUNZIONAMENTO:
  - **Data-Driven UI**: Un aspetto chiave della sua architettura è che costruisce
    dinamicamente i suoi widget basandosi sullo schema definito nel Modello
    (`model.fields`). Questo rende l'interfaccia flessibile e facile da
    modificare.
  - **Disaccoppiamento**: Non contiene logica di salvataggio su file. Comunica
    con il Controllore (la classe `Application`) in modo disaccoppiato,
    generando un evento virtuale `<<SaveRecord>>` quando l'utente richiede
    un salvataggio.
  - **Gestione dello Stato Interno**: Mantiene lo stato dei campi del form
    attraverso un dizionario di variabili Tkinter (`self._vars`).
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

    def _add_frame(self, label, cols=3):
        """
    Metodo "helper" per creare e configurare un `ttk.LabelFrame`.

    Questo metodo semplifica la creazione delle sezioni raggruppate del form,
    impostando un'etichetta e configurando le colonne interne per un layout
    responsive.

    Args:
        label (str): Il testo da visualizzare come titolo del frame.
        cols (int, optional): Il numero di colonne da configurare. Default a 3.

    Returns:
        ttk.LabelFrame: Il widget LabelFrame appena creato.
    """
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame

    def __init__(self, parent, model, *args, **kwargs):
        """
    Costruttore della classe `DataRecordForm`.

    Questo metodo costruisce l'intera interfaccia grafica del form in modo
    programmatico, basandosi sullo schema fornito dal `model`.
    """
        super().__init__(parent, *args, **kwargs)

        self.model = model
        fields = self.model.fields

        # Create a dict to keep track of input widgets
        self._vars = {
            key: self.var_types[spec['type']]()
            for key, spec in fields.items()
        }

        # Build the form
        self.columnconfigure(0, weight=1)

        # Record info section
        r_info = self._add_frame("Record Information")

        # line 1
        w.LabelInput(
            r_info, "Date",
            field_spec=fields['Date'],
            var=self._vars['Date'],
        ).grid(row=0, column=0)
        w.LabelInput(
            r_info, "Time",
            field_spec=fields['Time'],
            var=self._vars['Time'],
        ).grid(row=0, column=1)
        w.LabelInput(
            r_info, "Technician",
            field_spec=fields['Technician'],
            var=self._vars['Technician'],
        ).grid(row=0, column=2)
        # line 2
        w.LabelInput(
            r_info, "Lab",
            field_spec=fields['Lab'],
            var=self._vars['Lab'],
        ).grid(row=1, column=0)
        w.LabelInput(
            r_info, "Plot",
            field_spec=fields['Plot'],
            var=self._vars['Plot'],
        ).grid(row=1, column=1)
        w.LabelInput(
            r_info, "Seed Sample",
            field_spec=fields['Seed Sample'],
            var=self._vars['Seed Sample'],
        ).grid(row=1, column=2)

        # Environment Data
        e_info = self._add_frame("Environment Data")

        w.LabelInput(
            e_info, "Humidity (g/m³)",
            field_spec=fields['Humidity'],
            var=self._vars['Humidity'],
            disable_var=self._vars['Equipment Fault']
        ).grid(row=0, column=0)
        w.LabelInput(
            e_info, "Light (klx)",
            field_spec=fields['Light'],
            var=self._vars['Light'],
            disable_var=self._vars['Equipment Fault']
        ).grid(row=0, column=1)
        w.LabelInput(
            e_info, "Temperature (°C)",
            field_spec=fields['Temperature'],
            var=self._vars['Temperature'],
            disable_var=self._vars['Equipment Fault']
        ).grid(row=0, column=2)
        w.LabelInput(
            e_info, "Equipment Fault",
            field_spec=fields['Equipment Fault'],
            var=self._vars['Equipment Fault'],
        ).grid(row=1, column=0, columnspan=3)

        # Plant Data section
        p_info = self._add_frame("Plant Data")

        w.LabelInput(
            p_info, "Plants",
            field_spec=fields['Plants'],
            var=self._vars['Plants'],
        ).grid(row=0, column=0)
        w.LabelInput(
            p_info, "Blossoms",
            field_spec=fields['Blossoms'],
            var=self._vars['Blossoms'],
        ).grid(row=0, column=1)
        w.LabelInput(
            p_info, "Fruit",
            field_spec=fields['Fruit'],
            var=self._vars['Fruit'],
        ).grid(row=0, column=2)

        # Height data
        # create variables to be updated for min/max height
        # they can be referenced for min/max variables
        min_height_var = tk.DoubleVar(value='-infinity')
        max_height_var = tk.DoubleVar(value='infinity')

        w.LabelInput(
            p_info, "Min Height (cm)",
            field_spec=fields['Min Height'],
            var=self._vars['Min Height'],
            input_args={
                "max_var": max_height_var, "focus_update_var": min_height_var
            }).grid(row=1, column=0)
        w.LabelInput(
            p_info, "Max Height (cm)",
            field_spec=fields['Max Height'],
            var=self._vars['Max Height'],
            input_args={
                "min_var": min_height_var, "focus_update_var": max_height_var
            }).grid(row=1, column=1)
        w.LabelInput(
            p_info, "Median Height (cm)",
            field_spec=fields['Med Height'],
            var=self._vars['Med Height'],
            input_args={
                "min_var": min_height_var, "max_var": max_height_var
            }).grid(row=1, column=2)

        # Notes section
        w.LabelInput(
            self, "Notes", field_spec=fields['Notes'],
            var=self._vars['Notes'], input_args={"width": 85, "height": 10}
        ).grid(sticky="nsew", row=3, column=0, padx=10, pady=10)

        # buttons
        buttons = tk.Frame(self)
        buttons.grid(sticky=tk.W + tk.E, row=4)
        self.savebutton = ttk.Button(
            buttons, text="Save", command=self._on_save)
        self.savebutton.pack(side=tk.RIGHT)

        self.resetbutton = ttk.Button(
            buttons, text="Reset", command=self.reset)
        self.resetbutton.pack(side=tk.RIGHT)

        # default the form
        self.reset()

    def _on_save(self):
        """
    Genera un evento virtuale per notificare la richiesta di salvataggio.

    Questo è un punto chiave dell'architettura MVC. La Vista non esegue
    direttamente il salvataggio. Invece, genera un evento personalizzato
    `<<SaveRecord>>`. Sarà compito del Controllore (la classe `Application`)
    "ascoltare" questo evento e orchestrare l'operazione di salvataggio,
    mantenendo la Vista e il Modello disaccoppiati.
    """
        self.event_generate('<<SaveRecord>>')

    @staticmethod
    def tclerror_is_blank_value(exception):
        """
    Metodo statico per verificare se un `TclError` è causato da un valore vuoto.

    Tkinter solleva un `TclError` quando si cerca di ottenere un valore da una
    variabile numerica o booleana che è vuota. Questo metodo controlla se il
    messaggio dell'eccezione corrisponde a uno dei casi noti di "valore vuoto".
    """
        blank_value_errors = (
            'expected integer but got ""',
            'expected floating-point number but got ""',
            'expected boolean value but got ""'
        )
        is_bve = str(exception).strip() in blank_value_errors
        return is_bve

    def get(self):
        """
    Recupera i dati da tutti i campi del form e li restituisce come dizionario.

    Questo metodo scorre tutte le variabili Tkinter del form (`self._vars`),
    legge i loro valori e li inserisce in un dizionario Python standard.
    Gestisce con robustezza il caso in cui i campi numerici/booleani siano
    vuoti, restituendo `None` invece di causare un crash.
    """
        data = dict()
        for key, var in self._vars.items():
            try:
                data[key] = var.get()
            except tk.TclError as e:
                if self.tclerror_is_blank_value(e):
                    data[key] = None
                else:
                    raise e
        return data

    def reset(self):
        """
    Resetta il form a uno stato predefinito, implementando una logica "intelligente".

    A differenza di un semplice reset che svuota tutto, questo metodo:
    1. Salva i valori di alcuni campi ("Lab", "Time", "Technician", "Plot").
    2. Svuota tutti i campi.
    3. Imposta automaticamente la data corrente.
    4. Se non si era all'ultimo "Plot", ripristina i valori salvati e
       incrementa automaticamente il numero del "Plot", preparando il form
       per l'inserimento del record successivo nella sequenza.
    """
        lab = self._vars['Lab'].get()
        time = self._vars['Time'].get()
        technician = self._vars['Technician'].get()
        try:
            plot = self._vars['Plot'].get()
        except tk.TclError:
            plot = ''
        plot_values = self._vars['Plot'].label_widget.input.cget('values')

        # clear all values
        for var in self._vars.values():
            if isinstance(var, tk.BooleanVar):
                var.set(False)
            else:
                var.set('')

        # Autofill Date
        current_date = datetime.today().strftime('%Y-%m-%d')
        self._vars['Date'].set(current_date)
        self._vars['Time'].label_widget.input.focus()

        # check if we need to put our values back, then do it.
        if plot not in ('', 0, plot_values[-1]):
            self._vars['Lab'].set(lab)
            self._vars['Time'].set(time)
            self._vars['Technician'].set(technician)
            next_plot_index = plot_values.index(plot) + 1
            self._vars['Plot'].set(plot_values[next_plot_index])
            self._vars['Seed Sample'].label_widget.input.focus()

    def get_errors(self):
        """
    Forza una validazione completa su tutti i campi e restituisce gli errori.

    Questo metodo è cruciale per la validazione pre-salvataggio. Scorre
    tutti i widget del form, forza l'esecuzione della loro validazione
    "on focus-out" e raccoglie tutti i messaggi di errore attivi.

    Returns:
        dict: Un dizionario degli errori, vuoto se il form è valido.
    """
        errors = dict()
        for key, var in self._vars.items():
            inp = var.label_widget.input
            error = var.label_widget.error

            if hasattr(inp, 'trigger_focusout_validation'):
                inp.trigger_focusout_validation()
            if error.get():
                errors[key] = error.get()

        return errors


"""
  08/02/2026 - Finestra di Login - simpledialog
  Una finestra di Login che chiede nome ustente e password
"""


class LoginDialog(Dialog):

    def __init__(self, parent, title, error=''):
        self._pw = tk.StringVar()
        self._user = tk.StringVar()
        self._error = tk.StringVar(value=error)
        super().__init__(parent, title=title)

    def body(self, frame):
        ttk.Label(frame, text='Login to ABQ').grid(row=0)

        if self._error.get():
            ttk.Label(frame, textvariable=self._error).grid(row=1)

        user_inp = w.LabelInput(frame, 'User name:', input_class=w.RequiredEntry, var=self._user)
        user_inp.grid()
        w.LabelInput(frame, 'Password:', input_class=w.RequiredEntry, var=self._pw).grid()

        return user_inp.input

    """ Questa funzione fa l'overwrite dei bottoni Login e Cancel """
    def buttonbox(self):
        box = ttk.Frame(self)
        ttk.Button(
            box, text='Login', command=self.ok, default=tk.ACTIVE).grid(padx=5, pady=5)
        ttk.Button(
            box, text='Cancel', command=self.cancel).grid(row=1, column=1, padx=5, pady=5)
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.cancel)
        box.pack()

    """ Funzione che contiene la tupla dei dati di accesso """
    def apply(self):
        self.result = (self._user.get(), self._pw.get())

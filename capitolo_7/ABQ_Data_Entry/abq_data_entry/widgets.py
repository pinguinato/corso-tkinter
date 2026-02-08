import tkinter as tk
from tkinter import ttk
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .constants import FieldTypes as FT


##################
# Widget Classes #
##################

class ValidatedMixin:
    """
  Un "Mixin" che aggiunge una funzionalità di validazione completa a un widget.

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
  class ValidatedEntry(ValidatedMixin, ttk.Entry):
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
        """
    Attiva o disattiva il feedback visivo di errore sul widget.

    Questo è un metodo "helper" privato che centralizza la logica per
    cambiare l'aspetto del widget stesso (in questo caso, il colore del
    testo) per indicare uno stato di errore o uno stato normale.

    Args:
        on (bool, optional): Un flag booleano che determina lo stato.
            - Se `True`, il testo del widget viene colorato di rosso.
            - Se `False` (default), il testo del widget torna nero.
    """
        self.configure(foreground=('red' if on else 'black'))

    def _validate(self, proposed, current, char, event, index, action):
        """
    Metodo "centralino" che orchestra il processo di validazione.

    Questo è il metodo principale chiamato da Tkinter per ogni evento di
    validazione. Non contiene la logica di validazione specifica, ma agisce
    come un "dispatcher": determina il tipo di evento e delega il lavoro
    ai metodi specializzati (`_key_validate` o `_focusout_validate`).

    Questo approccio, basato sul "Principio di Separazione delle Competenze",
    mantiene il Mixin pulito e permette alle classi figlie di sovrascrivere
    solo la logica di cui hanno bisogno.

    ANALISI TECNICA:
    1.  **Reset dello Stato di Errore**: All'inizio di ogni chiamata, resetta
        il messaggio di errore e il feedback visivo.
    2.  **Controllo dello Stato 'DISABLED'**: Salta la validazione se il widget
        è disabilitato.
    3.  **Delega basata sull'Evento**: Chiama `_focusout_validate` o `_key_validate`
        a seconda del tipo di evento.
    """
        self.error.set('')
        self._toggle_error()

        valid = True
        # if the widget is disabled, don't validate
        state = str(self.configure('state')[-1])
        if state == tk.DISABLED:
            return valid

        if event == 'focusout':
            valid = self._focusout_validate(event=event)
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
        """
    Metodo segnaposto per la validazione all'uscita dal campo (focus-out).

    Questo metodo è progettato per essere **sovrascritto** dalle classi
    figlie. Il suo scopo è contenere la logica di validazione che deve essere
    eseguita solo quando l'utente ha finito di interagire con il widget.

    Returns:
        bool: Per default restituisce `True`, significando che, se non
              sovrascritto, nessuna validazione specifica viene eseguita.
    """
        return True

    def _key_validate(self, **kwargs):
        """
    Metodo segnaposto per la validazione a ogni pressione di un tasto.

    Questo metodo è progettato per essere **sovrascritto** dalle classi
    figlie. Il suo scopo è contenere la logica di "Input Filtering", ovvero la
    validazione che viene eseguita in tempo reale mentre l'utente digita.

    Returns:
        bool: Per default restituisce `True`, significando che, se non
              sovrascritto, qualsiasi carattere digitato è considerato valido.
    """
        return True

    def _invalid(self, proposed, current, char, event, index, action):
        """
    Gestore centrale per gli eventi di validazione fallita.

    Questo metodo viene chiamato da Tkinter quando `_validate` restituisce `False`.
    Agisce come un "dispatcher", determinando il tipo di evento che ha causato
    l'errore e delegando la gestione al metodo specifico (`_focusout_invalid`
    o `_key_invalid`).
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

    Per default, attiva semplicemente il feedback visivo di errore (testo rosso).
    Può essere sovrascritto dalle classi figlie per impostare messaggi di
    errore specifici.
    """
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        """
    Gestisce l'input non valido durante la digitazione.

    Per impostazione predefinita, questo metodo non fa nulla (`pass`), poiché
    la validazione su 'key' è spesso usata per bloccare l'input (prevenzione)
    e non richiede un feedback visivo aggiuntivo.
    """
        pass

    def trigger_focusout_validation(self):
        """
    Attiva manualmente la validazione "on focus-out" del widget.

    Questo metodo è fondamentale per la validazione pre-salvataggio. Simula
    un evento 'focusout' per forzare il controllo di validità del campo,
    anche se l'utente non lo ha ancora lasciato.

    Returns:
        bool: True se il contenuto del widget è valido, altrimenti False.
    """
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid


class DateEntry(ValidatedMixin, ttk.Entry):
    """
  Un widget ttk.Entry per l'inserimento di date nel formato AAAA-MM-GG.

  Questa classe garantisce che l'utente possa inserire solo date valide,
  fornendo due livelli di validazione:
  1. Validazione in tempo reale (`_key_validate`): controlla ogni carattere
     digitato per conformarsi alla struttura AAAA-MM-GG.
  2. Validazione al 'focus-out' (`_focusout_validate`): controlla la validità
     logica della data (es. che non sia '2023-02-30') quando l'utente
     lascia il campo.
  """

    def _key_validate(self, action, index, char, **kwargs):
        valid = True

        if action == '0':  # This is a delete action
            valid = True
        elif index in ('0', '1', '2', '3', '5', '6', '8', '9'):
            valid = char.isdigit()
        elif index in ('4', '7'):
            valid = char == '-'
        else:
            valid = False
        return valid

    def _focusout_validate(self, event):
        """
    Valida il contenuto del campo quando perde il focus.

    Controlla se il campo è vuoto (obbligatorio) e se la stringa
    corrisponde a una data valida.
    """
        valid = True
        if not self.get():
            self.error.set('A value is required')
            valid = False
        try:
            datetime.strptime(self.get(), '%Y-%m-%d')
        except ValueError:
            self.error.set('Invalid date')
            valid = False
        return valid


class RequiredEntry(ValidatedMixin, ttk.Entry):
    """
  Un widget ttk.Entry che richiede l'inserimento di un valore.

  Estende un normale campo di input aggiungendo una regola di validazione
  specifica: il campo non può essere lasciato vuoto. Mostra un messaggio
  di errore se l'utente lascia il campo vuoto.
  """

    def _focusout_validate(self, event):
        """
    Esegue la validazione quando il widget perde il focus.
    Controlla se il campo è vuoto.
    """
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')
        return valid


class ValidatedCombobox(ValidatedMixin, ttk.Combobox):
    """
  Un widget ttk.Combobox con validazione e autocompletamento.

  Questa classe estende ttk.Combobox per aggiungere due funzionalità:
  1. Validazione in tempo reale: durante la digitazione, il testo inserito
     viene confrontato con l'elenco di valori disponibili.
  2. Autocompletamento: se il testo digitato corrisponde in modo univoco
     all'inizio di una sola opzione, il campo viene autocompletato.
  3. Campo obbligatorio: la validazione al 'focus-out' garantisce che
     un valore sia stato selezionato.
  """

    def _key_validate(self, proposed, action, **kwargs):
        valid = True
        # if the user tries to delete,
        # just clear the field
        if action == '0':
            self.set('')
            return True

        # get our values list
        values = self.cget('values')
        # Do a case-insensitve match against the entered text
        matching = [
            x for x in values
            if x.lower().startswith(proposed.lower())
        ]
        if len(matching) == 0:
            valid = False
        elif len(matching) == 1:
            self.set(matching[0])
            self.icursor(tk.END)
            valid = False
        return valid

    def _focusout_validate(self, **kwargs):
        """
    Valida il campo quando perde il focus, assicurandosi che non sia vuoto.
    """
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')
        return valid


class ValidatedSpinbox(ValidatedMixin, ttk.Spinbox):
    """
  Un widget ttk.Spinbox con validazione numerica avanzata.

  Questa classe estende ttk.Spinbox per fornire una validazione robusta
  sia durante la digitazione che al momento della perdita del focus. Utilizza
  il tipo `Decimal` per gestire i numeri, garantendo un'alta precisione
  ed evitando i comuni errori di arrotondamento dei float.
  """

    def __init__(self, *args, min_var=None, max_var=None,
                 focus_update_var=None, from_='-Infinity', to='Infinity', **kwargs
                 ):
        """
    Inizializza lo Spinbox e imposta i binding dinamici per i limiti.

    Args:
        min_var/max_var: Variabili Tkinter per aggiornare dinamicamente i limiti.
        focus_update_var: Variabile per notificare ad altri widget un aggiornamento.
    """
        super().__init__(*args, from_=from_, to=to, **kwargs)
        increment = Decimal(str(kwargs.get('increment', '1.0')))
        self.precision = increment.normalize().as_tuple().exponent
        # there should always be a variable,
        # or some of our code will fail
        self.variable = kwargs.get('textvariable')
        if not self.variable:
            self.variable = tk.DoubleVar()
            self.configure(textvariable=self.variable)

        if min_var:
            self.min_var = min_var
            self.min_var.trace_add('write', self._set_minimum)
        if max_var:
            self.max_var = max_var
            self.max_var.trace_add('write', self._set_maximum)
        self.focus_update_var = focus_update_var
        self.bind('<FocusOut>', self._set_focus_update_var)

    def _set_focus_update_var(self, event):
        """
    Aggiorna la variabile di notifica esterna quando il widget perde il focus.

    Comunica ad altre parti dell'applicazione che l'utente ha terminato di
    modificare il valore e che tale valore è valido.
    """
        value = self.get()
        if self.focus_update_var and not self.error.get():
            self.focus_update_var.set(value)

    def _set_minimum(self, *_):
        """
    Callback per aggiornare dinamicamente il limite minimo dello Spinbox.
    """
        current = self.get()
        try:
            new_min = self.min_var.get()
            self.config(from_=new_min)
        except (tk.TclError, ValueError):
            pass
        if not current:
            self.delete(0, tk.END)
        else:
            self.variable.set(current)
        self.trigger_focusout_validation()

    def _set_maximum(self, *_):
        """
    Callback per aggiornare dinamicamente il limite massimo dello Spinbox.
    """
        current = self.get()
        try:
            new_max = self.max_var.get()
            self.config(to=new_max)
        except (tk.TclError, ValueError):
            pass
        if not current:
            self.delete(0, tk.END)
        else:
            self.variable.set(current)
        self.trigger_focusout_validation()

    def _key_validate(
            self, char, index, current, proposed, action, **kwargs
    ):
        """
    Valida l'input dell'utente durante la digitazione in tempo reale.

    Previene l'inserimento di caratteri che renderebbero il numero non valido,
    controllando il segno, il punto decimale, la precisione e i limiti
    superiori.
    """
        if action == '0':
            return True
        valid = True
        min_val = self.cget('from')
        max_val = self.cget('to')
        no_negative = min_val >= 0
        no_decimal = self.precision >= 0

        # First, filter out obviously invalid keystrokes
        if any([
            (char not in '-1234567890.'),
            (char == '-' and (no_negative or index != '0')),
            (char == '.' and (no_decimal or '.' in current))
        ]):
            return False

        # At this point, proposed is either '-', '.', '-.',
        # or a valid Decimal string
        if proposed in '-.':
            return True

        # Proposed is a valid Decimal string
        # convert to Decimal and check more:
        proposed = Decimal(proposed)
        proposed_precision = proposed.as_tuple().exponent

        if any([
            (proposed > max_val),
            (proposed_precision < self.precision)
        ]):
            return False

        return valid

    def _focusout_validate(self, **kwargs):
        """
    Esegue la validazione finale quando il widget perde il focus.

    Controlla la validità complessiva del valore inserito, verificando che
    sia un numero valido e che rientri nei limiti min/max, impostando
    un messaggio di errore specifico per ogni tipo di fallimento.
    """
        valid = True
        value = self.get()
        min_val = self.cget('from')
        max_val = self.cget('to')

        try:
            d_value = Decimal(value)
        except InvalidOperation:
            self.error.set(f'Invalid number string: {value}')
            return False

        if d_value < min_val:
            self.error.set(f'Value is too low (min {min_val})')
            valid = False
        if d_value > max_val:
            self.error.set(f'Value is too high (max {max_val})')
            valid = False

        return valid


class ValidatedRadioGroup(ttk.Frame):
    """
  Un widget composito che raggruppa dei Radiobutton e ne valida la selezione.

  Questa classe agisce come un contenitore (un ttk.Frame) per un insieme di
  widget ttk.Radiobutton, garantendo che l'utente effettui una selezione.
  Se l'utente lascia il gruppo senza aver selezionato un'opzione, viene
  mostrato un messaggio di errore.
  """

    def __init__(
            self, *args, variable=None, error_var=None,
            values=None, button_args=None, **kwargs
    ):
        """
    Inizializza il gruppo di Radiobutton.

    Args:
        variable: La variabile Tkinter da associare al gruppo.
        error_var: La StringVar in cui scrivere i messaggi di errore.
        values: Una lista di stringhe per i valori e il testo dei bottoni.
        button_args: Un dizionario di argomenti da passare a ogni Radiobutton.
    """
        super().__init__(*args, **kwargs)
        self.variable = variable or tk.StringVar()
        self.error = error_var or tk.StringVar()
        self.values = values or list()
        self.button_args = button_args or dict()

        for v in self.values:
            button = ttk.Radiobutton(
                self, value=v, text=v,
                variable=self.variable, **self.button_args
            )
            button.pack(
                side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill='x'
            )
        self.bind('<FocusOut>', self.trigger_focusout_validation)

    def trigger_focusout_validation(self, *_):
        """
    Esegue la validazione quando il widget perde il focus.

    Controlla se la variabile associata ha un valore. Se è vuota (nessun
    pulsante selezionato), imposta un messaggio di errore.
    """
        self.error.set('')
        if not self.variable.get():
            self.error.set('A value is required')


class BoundText(tk.Text):
    """
  Un widget tk.Text con una variabile collegata (two-way data binding).
  Mantiene il contenuto del widget e la `textvariable` sempre sincronizzati.
  """

    def __init__(self, *args, textvariable=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._variable = textvariable
        if self._variable:
            # insert any default value
            self.insert('1.0', self._variable.get())
            self._variable.trace_add('write', self._set_content)
            self.bind('<<Modified>>', self._set_var)

    def _set_var(self, *_):
        """Aggiorna la variabile quando l'utente scrive nel widget."""
        if self.edit_modified():
            content = self.get('1.0', 'end-1chars')
            self._variable.set(content)
            self.edit_modified(False)

    def _set_content(self, *_):
        """Aggiorna il widget quando la variabile viene modificata programmaticamente."""
        self.delete('1.0', tk.END)
        self.insert('1.0', self._variable.get())


###########################
# Compound Widget Classes #
###########################


class LabelInput(ttk.Frame):
    """
  Un "widget composto" che raggruppa un'etichetta e un widget di input.

  Questa classe è una "factory" che semplifica enormemente la costruzione
  del form. In base allo `field_spec` fornito dal modello, sceglie
  automaticamente la classe di widget validato più appropriata (`RequiredEntry`,
  `DateEntry`, etc.) e la crea, configurandola con le opzioni corrette.
  Gestisce anche la creazione dell'etichetta per il messaggio di errore e
  la logica di disabilitazione dinamica.
  """

    field_types = {
        FT.string: RequiredEntry,
        FT.string_list: ValidatedCombobox,
        FT.short_string_list: ValidatedRadioGroup,
        FT.iso_date_string: DateEntry,
        FT.long_string: BoundText,
        FT.decimal: ValidatedSpinbox,
        FT.integer: ValidatedSpinbox,
        FT.boolean: ttk.Checkbutton
    }

    def __init__(
            self,
            parent,
            label,
            var,
            input_class=None,
            input_args=None,
            label_args=None,
            field_spec=None,
            disable_var=None,
            **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = var
        self.variable.label_widget = self

        # Process the field spec to determine input_class and validation
        if field_spec:
            field_type = field_spec.get('type', FT.string)
            input_class = input_class or self.field_types.get(field_type)
            # min, max, increment
            if 'min' in field_spec and 'from_' not in input_args:
                input_args['from_'] = field_spec.get('min')
            if 'max' in field_spec and 'to' not in input_args:
                input_args['to'] = field_spec.get('max')
            if 'inc' in field_spec and 'increment' not in input_args:
                input_args['increment'] = field_spec.get('inc')
                # values
            if 'values' in field_spec and 'values' not in input_args:
                input_args['values'] = field_spec.get('values')

        # setup the label
        if input_class in (ttk.Checkbutton, ttk.Button):
            # Buttons don't need labels, they're built-in
            input_args["text"] = label
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))

        # setup the variable
        if input_class in (
                ttk.Checkbutton, ttk.Button, ttk.Radiobutton, ValidatedRadioGroup
        ):
            input_args["variable"] = self.variable
        else:
            input_args["textvariable"] = self.variable

        # Setup the input
        if input_class == ttk.Radiobutton:
            # for Radiobutton, create one input per value
            self.input = tk.Frame(self)
            for v in input_args.pop('values', []):
                button = input_class(
                    self.input, value=v, text=v, **input_args
                )
                button.pack(side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill='x')
        else:
            self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

        # Set up error handling & display
        self.error = getattr(self.input, 'error', tk.StringVar())
        ttk.Label(self, textvariable=self.error).grid(
            row=2, column=0, sticky=(tk.W + tk.E)
        )

        # Set up disable variable
        if disable_var:
            self.disable_var = disable_var
            self.disable_var.trace_add('write', self._check_disable)

    def _check_disable(self, *_):
        """
    Callback per abilitare/disabilitare dinamicamente il widget di input.

    Viene eseguito ogni volta che la `disable_var` (se fornita) cambia,
    permettendo a un widget di controllarne un altro.
    """
        if not hasattr(self, 'disable_var'):
            return

        if self.disable_var.get():
            self.input.configure(state=tk.DISABLED)
            self.variable.set('')
            self.error.set('')
        else:
            self.input.configure(state=tk.NORMAL)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        """
    Sovrascrive il metodo `grid` per impostare `sticky` di default.
    Questo assicura che il widget si espanda orizzontalmente.
    """
        super().grid(sticky=sticky, **kwargs)

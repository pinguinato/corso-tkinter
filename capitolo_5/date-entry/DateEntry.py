import tkinter as tk
from tkinter import ttk
from datetime import datetime




class DateEntry(ttk.Entry):

    def __init__(self, parent, *args, **kwargs):
        """Costruttore della classe DateEntry.

        Questo metodo inizializza il widget e, soprattutto, configura il
        complesso sistema di validazione di Tkinter, rendendo il widget
        "auto-validante".

        ANALISI TECNICA:
        1.  `super().__init__(...)`: Chiama il costruttore della classe genitore
            (`ttk.Entry`), assicurando che il nostro widget sia un campo di
            testo a tutti gli effetti.

        2.  `self.configure(...)`: Configura le opzioni di validazione:
            -   `validate='all'`: Attiva la validazione per tutti gli eventi
                rilevanti (`key`, `focusin`, `focusout`).
            -   `validatecommand`: Specifica il "comando di validazione".
                -   `self.register(self._validate)`: "Registra" il metodo Python
                    `_validate` in modo che possa essere chiamato dall'interprete
                    Tcl/Tk sottostante. È un passaggio obbligatorio.
                -   `'%S', '%i', '%V', '%d'`: Sono "codici di sostituzione" che
                    dicono a Tkinter quali informazioni passare al metodo
                    `_validate` al momento della chiamata (carattere, indice,
                    tipo di evento, tipo di azione).
            -   `invalidcommand`: Specifica il "comando di invalidità", che viene
                eseguito solo se `validatecommand` restituisce `False`.

        3.  `self.error = tk.StringVar()`: Crea una `StringVar` specifica per
            questa istanza del widget. Agisce come un "canale di comunicazione"
            per i messaggi di errore, permettendo a un'etichetta esterna di
            mostrare lo stato di errore del widget. È un ottimo esempio di
            incapsulamento.
        """
        super().__init__(parent, *args, **kwargs)
        self.configure(
            validate='all',
            validatecommand=(
                self.register(self._validate),
                '%S', '%i', '%V', '%d'
            ),
            invalidcommand=(self.register(self._on_invalid), '%V')
        )
        self.error = tk.StringVar()


    def _validate(self, char, index, event, action):
        """Metodo di validazione principale per il formato data YYYY-MM-DD.

            Questo metodo viene chiamato da Tkinter ogni volta che si verifica
            un evento di validazione (specificato in `validatecommand`).
            Implementa una validazione a due livelli:

            1.  **Validazione per 'key' (Input Filtering)**:
                -   **Scopo**: Impedire all'utente di inserire caratteri non validi
                    in posizioni specifiche, forzando il formato `YYYY-MM-DD`.
                -   **Logica**: Controlla la posizione del cursore (`index`) e il
                    carattere inserito (`char`). Permette solo cifre nelle posizioni
                    dei numeri e trattini `-` nelle posizioni dei separatori.
                    Permette sempre la cancellazione (`action == '0'`).

            2.  **Validazione per 'focusout' (Validazione Semantica)**:
                -   **Scopo**: Controllare che la data inserita, una volta completata,
                    sia una data reale e valida (es. non accetta "2023-02-30").
                -   **Logica**: Quando l'utente lascia il campo, il metodo tenta di
                    convertire l'intera stringa in un oggetto `datetime`. Se la
                    conversione fallisce (sollevando un `ValueError`), la data
                    non è valida.

            Args:
                char (str): Il carattere inserito (`%S`).
                index (str): L'indice della posizione del cursore (`%i`).
                event (str): Il tipo di evento che ha scatenato la validazione (`%V`).
                action (str): Il tipo di azione: '1' per inserimento, '0' per cancellazione (`%d`).

            Returns:
                bool: `True` se l'input è valido, `False` altrimenti.
            """
        self._toggle_error()
        valid = True

        if event == 'key':
            if action == '0':
                valid = True
            elif index in ('0', '1', '2', '3', '5', '6', '8', '9'):
                valid = char.isdigit()
            elif index in ('4', '7'):
                valid = char == '-'
            else:
                valid = False
        elif event == 'focusout':
            try:
                datetime.strptime(self.get(), '%Y-%m-%d')
            except ValueError:
                valid = False
        return valid


    def _on_invalid(self, event):
        """Gestisce il feedback visivo quando la validazione fallisce.

            Questo metodo viene chiamato automaticamente da Tkinter ogni volta che
            il `validatecommand` (`_validate`) restituisce `False`.
            Il suo unico compito è fornire un feedback all'utente, mostrando
            un messaggio di errore.

            Args:
                event (str): Il tipo di evento che ha causato il fallimento della
                             validazione (es. 'focusout', 'key'). Questo valore
                             viene passato da Tkinter tramite il codice di
                             sostituzione `%V`.

            LOGICA ATTUALE E LIMITAZIONI:
            - **Logica**: Il metodo controlla il tipo di evento e agisce solo se
              l'evento NON è di tipo 'key'. Questo significa che mostra un errore
              solo quando l'utente lascia il campo (`focusout`) con dati non validi.
            - **Limitazione (Bug Noto)**: Ignora completamente gli errori che si
              verificano durante la digitazione (`event == 'key'`). Di conseguenza,
              se l'utente preme un tasto non valido, l'input viene bloccato
              correttamente da `_validate`, ma questo metodo non fa nulla,
              non fornendo alcun feedback visivo immediato.
            - **Messaggio Generico**: Il messaggio di errore è sempre "Not a valid date",
              indipendentemente dalla natura specifica dell'errore.
            """
        if event != 'key':
            self._toggle_error('Not a valid date')



    def _toggle_error(self, error=''):
        """Gestisce la visualizzazione dello stato di errore del widget.

                 Questo è un metodo "helper" privato che centralizza la logica per
                 attivare o disattivare lo stato di errore del widget `DateEntry`.
                 Viene chiamato dai metodi di validazione per fornire un feedback
                 visivo e testuale all'utente.

                 Args:
                     error (str, optional): La stringa del messaggio di errore.
                         - Se viene fornita una stringa non vuota, il widget entra
                           nello stato di "errore".
                         - Se la stringa è vuota (default), il widget torna allo
                           stato "normale".

                 ANALISI TECNICA:
                 - `self.error.set(error)`: Aggiorna la variabile `StringVar` associata
                   al widget, che verrà usata da un'etichetta esterna per mostrare
                   il messaggio di errore.
                 - `self.config(...)`: Cambia il colore del testo (foreground) del
                   widget `Entry` stesso: rosso in caso di errore, nero altrimenti.
                   Questo fornisce un feedback visivo immediato e inequivocabile.
                 """
        self.error.set(error)
        self.config(foreground='red' if error else 'black')


if __name__ == '__main__':
    root = tk.Tk()
    entry = DateEntry(root)
    entry.pack()
    ttk.Label(
        textvariable=entry.error, foreground='red'
    ).pack()

    ttk.Entry(root).pack()
    root.mainloop()
"""
Questo script crea una finestra con tre campi di testo (Entry) per dimostrare
tre diversi aspetti del sistema di validazione di Tkinter.

1.  **Primo Campo (`entry`): Configurazione di Base**
    - **Scopo**: Dimostrare la configurazione minima per la validazione.
    - **Funzione**: `alway_good()` è la funzione di validazione, che restituisce sempre `True`.
    - **Logica**: Qualsiasi carattere inserito è considerato valido. Questo campo accetterà sempre qualsiasi input, dimostrando che il sistema è attivo.

2.  **Secondo Campo (`entry2`): Prevenzione dell'Input (Input Filtering)**
    - **Scopo**: Dimostrare una validazione che filtra l'input in tempo reale.
    - **Funzione**: `no_t_for_me(proposed)` è la funzione di validazione.
    - **Logica**: La funzione controlla se la lettera 't' è presente nella stringa "proposta" (`%P`). Se c'è, restituisce `False`, impedendo fisicamente all'utente di digitare quel carattere. Questo è un esempio di "prevenzione dell'errore".

3.  **Terzo Campo (`entry3`): Feedback Visivo con `invalidcommand`**
    - **Scopo**: Dimostrare come fornire un feedback visivo all'utente quando la validazione fallisce.
    - **Funzione di Validazione**: `only_five_chars(proposed)` controlla che il testo non superi i 5 caratteri.
    - **Funzione di Errore**: `only_five_chars_error(proposed)` viene eseguita solo se la validazione fallisce. Il suo compito è aggiornare un'etichetta (`Label`) con un messaggio di errore chiaro.
    - **Logica**: A differenza del secondo campo, l'utente *può* inserire un testo troppo lungo, ma non appena lo fa, `validatecommand` restituisce `False`, il testo non viene accettato e `invalidcommand` viene attivato, mostrando il messaggio di errore.
"""

import tkinter as tk

root = tk.Tk()

entry = tk.Entry(root)
entry.grid()


def alway_good():
    return True


validate_ref = root.register(alway_good)

entry.configure(
    validate='all',
    validatecommand=(validate_ref)
)

entry2 = tk.Entry(root)
entry2.grid(pady=10)


def no_t_for_me(proposed):
    return 't' not in proposed


validate2_ref = root.register(no_t_for_me)
entry2.configure(
    validate='all',
    validatecommand=(validate2_ref, '%P')
)

entry3 = tk.Entry()
entry3.grid()

entry3_error = tk.Label(root, fg='red')
entry3_error.grid()

def only_five_chars(proposed):
    return len(proposed) < 6


def only_five_chars_error(proposed):
    entry3_error.configure(
        text=f'"{proposed}" è troppo lungo, sono ammessi solo 5 caratteri.'
    )

validate3_ref = root.register(only_five_chars)
invalid3_ref = root.register(only_five_chars_error)

entry3.configure(
    validate='all',
    validatecommand=(validate3_ref, '%P'),
    invalidcommand=(invalid3_ref, '%P')
)

root.mainloop()

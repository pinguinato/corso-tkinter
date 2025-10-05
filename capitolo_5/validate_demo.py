"""
Questo script crea una finestra con due campi di testo (Entry) per dimostrare due diverse regole di validazione:
1.
Primo Campo (entry):
Scopo: Dimostrare la configurazione di base della validazione.
Funzione: alway_good() è la funzione di validazione, che restituisce sempre True.
Logica: Qualsiasi carattere inserito è considerato valido. Questo campo accetterà sempre qualsiasi input.

2.
Secondo Campo (entry2):
Scopo: Dimostrare una validazione più complessa che filtra l'input.
Funzione: no_t_for_me(proposed) è la funzione di validazione. Dovrebbe impedire all'utente di inserire la lettera 't'.
Logica: La funzione controlla se il carattere 't' è presente nella stringa "proposta" (proposed). Se non c'è, restituisce True (valido), altrimenti False (non valido).
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

root.mainloop()
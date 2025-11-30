# Importa le librerie necessarie.
# 'tkinter' è la libreria principale per le GUI, anche se qui non creiamo una finestra visibile.
# 'messagebox' è il sottomodulo specifico per le finestre di dialogo.
import tkinter as tk
from tkinter import messagebox

# Mostra una finestra di dialogo che pone una domanda con i pulsanti "Sì" e "No".
# La funzione `askyesno` mette in pausa l'esecuzione dello script finché l'utente non fa una scelta.
# - title: Il titolo della finestra di dialogo.
# - message: Il messaggio principale.
# - detail: Un testo aggiuntivo con dettagli.
# La funzione restituisce True se l'utente clicca "Sì", altrimenti False.
see_more = messagebox.askyesno(
    title='See more?',
    message='Would you like to see another box?',
    detail='Click NO to quit'
)

# Controlla la risposta dell'utente.
# 'if not see_more' è vero se l'utente ha cliccato "No" (quindi see_more è False).
if not see_more:
    # Se l'utente ha scelto "No", termina l'esecuzione dello script.
    exit()

# Questo codice viene eseguito solo se l'utente ha cliccato "Sì".
# Mostra una seconda finestra di dialogo, questa volta di tipo informativo.
# La funzione `showinfo` visualizza un messaggio con un'icona "info" e un pulsante "OK".
messagebox.showinfo(
    title='You got it',
    message="Ok, here's another dialog.",
    detail='Hope you like it'
)

"""
Punto di Ingresso Principale dell'Applicazione (Entry Point)

Questo script è il punto di avvio per l'intera applicazione "ABQ Data Entry".
Il suo unico scopo è quello di inizializzare e lanciare l'interfaccia grafica.

ANALISI TECNICA:
1.  `from abq_data_entry.application import Application`: Importa la classe
    principale `Application` dal modulo `application.py`, che si trova
    all'interno del package `abq_data_entry`. Questo è possibile grazie
    alla struttura a package del progetto.

2.  `app = Application()`: Crea un'istanza della classe `Application`.
    Questa azione avvia il costruttore `__init__` della classe, che a sua
    volta crea la finestra principale, il modello dei dati (Model) e
    il form di inserimento (View), assemblando tutti i componenti
    dell'applicazione.

3.  `app.mainloop()`: Avvia il ciclo principale degli eventi di Tkinter.
    Questa chiamata mette l'applicazione in attesa di interazioni da parte
    dell'utente (click, digitazione, etc.) e gestisce il rendering della
    finestra e dei suoi widget. Il programma terminerà solo quando la
    finestra principale verrà chiusa.

Mantenere questo file così semplice è una best practice di progettazione
software, poiché separa nettamente la logica di avvio dal resto del
codice dell'applicazione.
"""
from abq_data_entry.application import Application

# Crea un'istanza della classe principale dell'applicazione
app = Application()

# Avvia il ciclo degli eventi di Tkinter per mostrare la finestra e
# attendere l'interazione dell'utente.
app.mainloop()

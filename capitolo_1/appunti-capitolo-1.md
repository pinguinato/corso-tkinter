# Capitolo 1


## Hello World - il primo programma

        import tkinter as tk

        root = tk.Tk()

        # esempio di widget Tkinter
        label = tk.Label(root, text="Hello World!")
        label.pack()
        root.mainloop()s

## Importare Tkinter nei propri files, prima di tutto!

        import tkinter as tk

**Importante**

Ogni programma Tkinter necessita sempre di una **root** window per poterci posizionare i propri widgets:

        root = tk.Tk()

**Importante**

Possiamo eseguire il nostro programma Tkinter direttamente con questo comando alla fine del file:

        root.mainloop()


## Metodi di Tkinter usati per il posizionamento del layout nell'applicazione

- **pack()** semplice e molto usato per applicazioni dal layout molto semplice e con i widget in sequenza uno dietro l'altro. Il metodo è il più vecchio di tutti, non va bene per applicazioni grafiche molto complesse e variegate.
- **grid()** il migliore e il più usato in assoluto con Tkinter, si può usare per posizionare i propri widget come se si avesse davanti una griglia tabellare 2D.
- **place()** è la terza ed ultima opzione, permette di posizionare i widget secondo specifici pixel, ma è molto laborioso e non sempre efficace, non è raccomandato ed è il meno usato dei tre metodi.

## Le variabili di controllo Tkinter

Sono oggetti speciali di Tkinter, che ci permettono di salvare tipologie di dati come:

- **StringVar** ritorna una stringa
- **IntVar** ritorna un numero intero
- **DoubleVar** ritorna un numero float
- **BooleanVar** ritorna un valore booleano

Caratteristiche dell'uso delle variabili di controllo:

- 2 way binding tra la variabile e il widget
- trace sulla variabile
- relazioni tra i vari widgets

Le variabili Tkinter di controllo sono più potenti delle comuni variabili che si usano nel linguaggio Python in quanto sono pensate per operare al meglio con le applicazioni Tkinter e la libreria stessa.


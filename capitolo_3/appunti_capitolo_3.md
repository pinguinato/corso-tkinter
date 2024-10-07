# Capitolo 3

**MVP** Minimum viable product, non è production ready, ma va bene come demo per mostrare le potenzialità dell'applicazione.

## Ttk widget set

Le moderne applicazioni Tkinter tendono a preferire un set di widgets più indicato chiamato **Ttk**. Ttk è contenuto in Tkinter e raccoglie un insieme di widgets Tkinter che rispetto ai widgets di base sono più indicati per lo sviluppo di interfacce grafiche di ultima generazione per i moderni sistemi operativi Windows, Linux o Mac. 

### Come importare Ttk

        from tkinter import ttk

### Elenco di tipi di widgets Ttk

- Labels
- Date entry
- Text entry
- Number entry
- Check boxes
- Radio buttons
- Select List
- Long text entry
- Buttons
- Boxed frame con intestazione

#### Label widget

        myLabel = ttk.Label(root, text="Questa è una label")

#### Entry widget

        myEntry = ttk.Entry(root, textvariable = my_var, width=20)

#### Spinbox widget

        mySpinbox = ttk.Spinbox(root, to=100, increment=.01, textvariable=my_var, command=my_callback)

ecc...
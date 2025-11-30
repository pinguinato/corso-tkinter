# Capitolo 7: Finestre di Dialogo

Tkinter fornisce diversi sottomoduli per la creazione di finestre di dialogo standard, utili per interagire con l'utente. I principali sono:

- **`messagebox`**: Mostra finestre di dialogo per messaggi informativi, di avviso, di errore o per porre semplici domande (sì/no, ok/annulla).
- **`filedialog`**: Permette all'utente di selezionare file o directory dal proprio sistema (es. per aprire o salvare un file).
- **`simpledialog`**: Richiede all'utente l'immissione di un singolo dato, come una stringa, un numero intero o un numero decimale.

## Tkinter Messagebox

Per informare l'utente sullo stato dell'applicazione o per richiedere una conferma, il modulo `messagebox` è lo strumento ideale. Offre una vasta gamma di finestre di dialogo predefinite per diverse necessità.

Poiché `messagebox` è un sottomodulo, deve essere importato esplicitamente nel progetto per poter essere utilizzato:

```python
from tkinter import messagebox
```

### Funzioni e Utilizzo di `messagebox`

Il modulo `messagebox` offre diverse funzioni, che possiamo dividere in due categorie principali: quelle che **mostrano un'informazione** e quelle che **pongono una domanda** all'utente.

Tutte le funzioni condividono alcuni argomenti comuni:

-   `title`: Il testo da mostrare nella barra del titolo della finestra.
-   `message`: Il messaggio principale da visualizzare all'interno della finestra di dialogo.
-   `**options`: Argomenti opzionali per personalizzare la finestra, tra cui:
    -   `detail`: Un testo aggiuntivo per fornire maggiori dettagli, mostrato con un carattere più piccolo.
    -   `icon`: Specifica l'icona da mostrare (`info`, `warning`, `error`, `question`). Di norma, ogni funzione ha già un'icona predefinita appropriata.
    -   `parent`: La finestra "genitore" su cui centrare la finestra di dialogo.

#### 1. Finestre informative

Queste funzioni servono a comunicare un messaggio all'utente. L'esecuzione del programma viene messa in pausa finché l'utente non preme il pulsante.

-   `showinfo()`: Mostra un'icona "informazione" e un pulsante **OK**. Utile per messaggi generici, come "Operazione completata con successo".
-   `showwarning()`: Mostra un'icona "avviso" e un pulsante **OK**. Utile per avvertire l'utente di una situazione inaspettata ma non critica, come "Il campo nome non può essere vuoto".
-   `showerror()`: Mostra un'icona "errore" e un pulsante **OK**. Usata per comunicare che si è verificato un errore che impedisce il proseguimento, come "Impossibile connettersi al database".

#### 2. Finestre di domanda

Queste funzioni pongono una domanda all'utente e restituiscono un valore in base al pulsante premuto. Sono fondamentali per creare applicazioni interattive.

-   `askquestion()`: Mostra i pulsanti **Sì** e **No**. Restituisce le stringhe `'yes'` o `'no'`.
-   `askyesno()`: Mostra i pulsanti **Sì** e **No**. Restituisce i valori booleani `True` per Sì e `False` per No. **È spesso preferibile a `askquestion`** perché i booleani sono più facili da gestire nel codice.
-   `askokcancel()`: Mostra i pulsanti **OK** e **Annulla**. Restituisce `True` per OK e `False` per Annulla. Utile per chiedere conferma prima di un'azione (es. "Salvare le modifiche?").
-   `askretrycancel()`: Mostra i pulsanti **Riprova** e **Annulla**. Restituisce `True` per Riprova e `False` per Annulla. Ideale quando un'operazione fallisce e si vuole dare all'utente la possibilità di tentare di nuovo.
-   `askyesnocancel()`: Mostra tre pulsanti: **Sì**, **No** e **Annulla**. Restituisce `True` per Sì, `False` per No e `None` se l'utente preme Annulla o chiude la finestra.

### Esempio pratico

Vediamo come utilizzare alcune di queste funzioni in un semplice script Tkinter.

```python
import tkinter as tk
from tkinter import messagebox

# --- Funzioni associate ai pulsanti ---

def mostra_info():
    """Mostra una finestra di dialogo informativa."""
    messagebox.showinfo(
        title="Informazioni",
        message="Questa è un'applicazione di esempio.",
        detail="Creata per dimostrare l'uso delle messagebox in Tkinter."
    )

def simula_errore():
    """Mostra una finestra di dialogo di errore."""
    messagebox.showerror(
        title="Errore Fatale",
        message="Si è verificato un errore imprevisto!",
        detail="Impossibile completare l'operazione richiesta."
    )

def salva_modifiche():
    """Chiede conferma prima di un'azione e agisce in base alla risposta."""
    # askokcancel restituisce True se si preme OK, False se si preme Annulla.
    risposta = messagebox.askokcancel(
        title="Salvare le modifiche?",
        message="Hai delle modifiche non salvate. Vuoi salvarle?",
        icon=messagebox.WARNING  # Possiamo specificare un'icona diversa da quella di default
    )
    
    if risposta:
        # Qui andrebbe il codice per salvare i dati
        print("Azione confermata: salvataggio in corso...")
        messagebox.showinfo("Salvataggio", "Modifiche salvate con successo!")
    else:
        # L'utente ha premuto "Annulla"
        print("Azione annullata dall'utente.")

def chiedi_di_uscire():
    """Chiede conferma prima di chiudere l'applicazione."""
    # askyesno restituisce True per Sì e False per No.
    # È perfetto per le condizioni if.
    risposta = messagebox.askyesno(
        title="Conferma uscita",
        message="Sei sicuro di voler uscire dall'applicazione?"
    )
    if risposta:
        root.destroy()

# --- Creazione della finestra principale e dei widget ---

# 1. Finestra principale
root = tk.Tk()
root.title("Esempio Messagebox")
root.geometry("350x250")

# 2. Pulsanti per attivare le finestre di dialogo
tk.Button(root, text="Mostra Info", command=mostra_info).pack(pady=10, padx=20, fill=tk.X)
tk.Button(root, text="Salva Modifiche...", command=salva_modifiche).pack(pady=10, padx=20, fill=tk.X)
tk.Button(root, text="Simula Errore", command=simula_errore).pack(pady=10, padx=20, fill=tk.X)
tk.Button(root, text="Esci", command=chiedi_di_uscire).pack(pady=10, padx=20, fill=tk.X)

# 3. Avvio dell'applicazione
root.mainloop()
```

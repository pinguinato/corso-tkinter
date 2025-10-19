# Appunti Capitolo 6
 
 ## Organizzazione del Codice e Pattern Architetturali in Tkinter
 
 Man mano che un'applicazione cresce, la sua complessità aumenta. Un singolo file di codice diventa rapidamente difficile da leggere, modificare e mantenere. Per questo è fondamentale adottare un'architettura software ben definita fin dall'inizio.
 
 ### Il Principio della "Separazione delle Competenze" (Separation of Concerns)
 
 Il principio fondamentale per gestire la complessità è la **Separazione delle Competenze**. Questo significa che ogni parte del nostro programma dovrebbe avere una singola, chiara e ben definita responsabilità.
 
 Un'applicazione che segue questo principio è:
 - **Più facile da capire**: Si può ragionare su piccole parti isolate.
 - **Più facile da modificare**: Cambiare la grafica non dovrebbe rompere la logica di salvataggio dei dati.
 - **Più facile da testare e debuggare**.
 
 ### Il Pattern MVC (Model-View-Controller)
 
 Il **Model-View-Controller (MVC)** è un classico pattern architetturale, nato negli anni '70, che applica in modo strutturato la Separazione delle Competenze. Suddivide l'applicazione in tre componenti interconnessi:
 
 #### 1. Model (Il Modello)
 
 *   **Responsabilità**: Gestire i **dati** e la **logica di business**. È l'unica parte che "conosce" le regole dei dati. Non sa nulla di come i dati verranno mostrati.
 *   **Esempi nel nostro progetto**:
     *   La logica per salvare e caricare i dati da un file CSV.
     *   La struttura di un singolo record di dati.
     *   Le regole di validazione (es. "l'altezza massima non può essere inferiore alla minima").
 
 #### 2. View (La Vista)
 
 *   **Responsabilità**: Presentare i dati all'utente e catturare le sue interazioni (click, digitazione). È la parte "visibile" dell'applicazione. Non contiene logica di business.
 *   **Esempi nel nostro progetto**:
     *   La classe `DataRecordForm` e tutti i suoi widget (`LabelInput`, `DateEntry`, etc.).
     *   La disposizione dei widget nella finestra (il layout).
     *   La formattazione dei dati per la visualizzazione.
 
 #### 3. Controller (Il Controllore)
 
 *   **Responsabilità**: Agire da **intermediario**. Riceve gli input dell'utente dalla Vista, li elabora e comanda al Modello di aggiornarsi. Successivamente, dice alla Vista di aggiornare la sua presentazione in base ai nuovi dati del Modello.
 *   **Esempi nel nostro progetto**:
     *   La classe `Application`, che avvia tutto.
     *   Il metodo `_on_save`, che viene eseguito quando si clicca "Save".
     -   La creazione delle istanze della Vista e del Modello.
 
 ### MVC in Tkinter: una Sfida Comune
 
 In Tkinter la separazione tra Vista e Controllore non è sempre netta. A causa della sua natura event-driven (basata su eventi e callback), è molto comune che la logica del Controllore (es. i metodi `command` dei pulsanti) sia definita all'interno delle stesse classi della Vista.
 
 Nel nostro progetto, la classe `Application` agisce da Controllore principale, ma anche la classe `DataRecordForm` contiene logica di controllo (come il metodo `reset`). Questo non è un errore, ma un adattamento comune del pattern MVC al contesto di Tkinter. L'importante è mantenere la separazione più netta possibile tra la **logica dei dati (Model)** e la **logica dell'interfaccia (View/Controller)**.
 
 ### Prossimi Passi: Refactoring del Progetto
 
 Nel laboratorio di questo capitolo, applicheremo questi concetti per riorganizzare la nostra `data_entry_app.py` in una struttura multi-file, separando le responsabilità. 
 Non esiste una regola fissa da seguire per l'organizzazione di un prgetto in Tkinter, ma possiamo seguire delle convenzioni.
 
### Creare un Package Python
 
 Per organizzare il codice in modo logico, Python utilizza i **package**. 
 Un package non è altro che una directory che contiene moduli Python correlati (file `.py`) e un file speciale che la identifica come tale.
 
 #### Convenzioni di Nomenclatura
 
 Per convenzione (secondo la guida di stile PEP 8), i nomi dei package e dei moduli dovrebbero essere **corti, tutti in minuscolo**, 
 e le parole possono essere separate da un trattino basso (`_`) per migliorare la leggibilità.
 
 #### Struttura di un Package
 
 Perché Python riconosca una directory come un package, 
 questa deve contenere un file speciale chiamato `__init__.py`. La struttura minima è quindi:
 
 ```
 nome_del_package/
 ├── __init__.py
 └── modulo1.py
 └── modulo2.py
 ```
 
 #### Il Ruolo del File `__init__.py`
 
 Questo file, anche se vuoto, segnala a Python che la directory non è una semplice cartella, ma un package importabile.
 
 > **Buona pratica**: La community Python raccomanda di mantenere il file `__init__.py` **il più vuoto possibile**. Inserire molta logica in questo file può rendere gli import più lenti e nascondere la struttura dei moduli, rendendo il codice più difficile da capire. Se non hai un motivo specifico per aggiungervi codice, lascialo completamente vuoto.
 
 Un uso comune (ma da fare con moderazione) è quello di importare al suo interno le classi o funzioni più importanti dai sottomoduli, per semplificare l'accesso dall'esterno. Ad esempio, se `modulo1.py` contiene `MiaClasse`, potresti scrivere in `__init__.py`:
 
 `from .modulo1 import MiaClasse`
 
 Questo permetterebbe a un utente di importare la classe con `from nome_del_package import MiaClasse` 
 invece del più lungo `from nome_del_package.modulo1 import MiaClasse.
 
## Modulo in Python

Non è altro che un file **.py** all'interno di un package.

### Relative Imports (Import Relativi)

Quando si lavora all'interno di un package, è spesso necessario che un modulo importi classi o funzioni da un altro modulo *nello stesso package*. Per fare questo, si usano gli **import relativi**.

Un import relativo usa la notazione con il punto (`.`) per specificare la posizione del modulo da importare rispetto alla posizione del file corrente.

#### Sintassi del Punto

*   `from .nome_modulo import Oggetto`: Il singolo punto `.` significa "**dalla stessa directory (package) in cui si trova questo file**".
*   `from ..nome_modulo import Oggetto`: I due punti `..` significano "**dalla directory genitore (package genitore)**".

#### Esempio Concreto nel Nostro Progetto

Consideriamo la nostra struttura di file:

```
ABQ_Data_Entry/
└── abq_data_entry/
    ├── __init__.py
    ├── models.py
    ├── constants.py
    └── views.py
```

Siamo all'interno del file `models.py` e vogliamo importare la classe `FieldTypes` dal file `constants.py`.

Scriviamo:
```python
from .constants import FieldTypes as FT
```

Questo comando dice a Python:
> "Partendo dalla posizione del file attuale (`models.py`), guarda nella **stessa directory** (`.`), trova il file `constants.py` e importa da lì la classe `FieldTypes`."

#### Vantaggi degli Import Relativi

L'uso degli import relativi all'interno di un package lo rende **autonomo e portabile**. Potremmo rinominare la cartella principale `ABQ_Data_Entry` in qualsiasi altro modo, e tutti gli import interni continuerebbero a funzionare senza bisogno di modifiche, perché non dipendono dal percorso assoluto.
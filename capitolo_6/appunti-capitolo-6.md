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
 
 Nel laboratorio di questo capitolo, applicheremo questi concetti per riorganizzare la nostra `data_entry_app.py` in una struttura multi-file, separando le responsabilità:
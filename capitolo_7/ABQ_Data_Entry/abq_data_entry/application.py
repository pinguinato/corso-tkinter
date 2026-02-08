import tkinter as tk
from tkinter import ttk
from . import views as v
from . import models as m
from tkinter import messagebox # import che serve per le finistre di dialogo
from tkinter import filedialog # import che serve per le finistre di dialogo per i files


class Application(tk.Tk):
    """
    La classe principale dell'applicazione, che agisce da **Controllore** nel pattern MVC.

    Eredita da `tk.Tk` per essere la finestra radice dell'applicazione.

    Le sue responsabilità sono:
    -   Creare le istanze del Modello (`CSVModel`) e della Vista (`DataRecordForm`).
    -   Assemblare i componenti principali dell'interfaccia (il form, la barra di stato).
    -   Orchestrare le interazioni principali, come la gestione dell'evento di salvataggio.
    """

    def __init__(self, *args, **kwargs):
        """
        Costruttore della classe `Application`.

        Inizializza l'applicazione creando il Modello, la Vista e configurando
        la finestra principale.
        """

        super().__init__(*args, **kwargs)

        # 08/02/2026 questo codice permette il caricamento della form di Login prima di tutto
        self.withdraw()
        if not self._show_login():
            self.destroy()
            return
        self.deiconify()

        # 1. Crea l'istanza del Modello che gestirà la logica dei dati.
        self.model = m.CSVModel()

        self.title("ABQ Data Entry Application")
        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="ABQ Data Entry Application",
            font=("TkDefaultFont", 16)
        ).grid(row=0)

        # 2. Crea l'istanza della Vista (il form), passandole un riferimento a se stessa
        #    (il Controllore) e al Modello.
        self.recordform = v.DataRecordForm(self, self.model)
        self.recordform.grid(row=1, padx=10, sticky=(tk.W + tk.E))

        # 3. Collega l'evento personalizzato `<<SaveRecord>>` (generato dalla Vista)
        #    al metodo `_on_save` di questo Controllore.
        #    Questo è un ottimo esempio di decoupling tra Vista e Controllore.
        self.recordform.bind('<<SaveRecord>>', self._on_save)

        # 4. Crea la barra di stato per fornire feedback all'utente.
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)

        self._records_saved = 0

    def _on_save(self, *_):
        """
        Gestore dell'evento `<<SaveRecord>>`, chiamato quando la Vista richiede un salvataggio.

        Questo metodo orchestra il processo di salvataggio in modo sicuro e robusto.

        ANALISI TECNICA:
        1.  **Validazione pre-salvataggio**: Chiama `self.recordform.get_errors()`
            per verificare la presenza di errori di validazione nel form. Se ci
            sono errori, blocca il salvataggio e notifica l'utente.
        2.  **Recupero Dati**: Se non ci sono errori, recupera i dati dalla Vista
            tramite `self.recordform.get()`.
        3.  **Comando al Modello**: Comanda al Modello di salvare i dati tramite
            `self.model.save_record(data)`. Il Controllore non sa *come*
            vengono salvati i dati, delega semplicemente il compito.
        4.  **Feedback e Reset**: Aggiorna la barra di stato con un messaggio di
            successo e comanda alla Vista di resettarsi.
        """
        # 1. Validazione pre-salvataggio
        errors = self.recordform.get_errors()
        if errors:

            self.status.set(
                "Cannot save, error in fields: {}"
                .format(', '.join(errors.keys()))
            )

            # 1) 08/02/2026 Aggiunta di una finestra di dialogo per mostrare gli errori
            # per i campi che non sono ancora stati compilati
            message = "Cannot save record"
            detail = (
                "The following fields have errors: "
                "\n * {}".format('\n * '.join(errors.keys())))
            messagebox.showerror(
                title='Error ',
                message=message,
                detail=detail
            )

            return False

        # 2. e 3. Recupero dati e comando al Modello
        data = self.recordform.get()
        self.model.save_record(data)

        # 4. Feedback e Reset
        self._records_saved += 1
        self.status.set(
            f"{self._records_saved} records saved this session"
        )
        self.recordform.reset()
    
            
    def _on_file_select(self, *_):
        """ Handle the file->select action"""
        filename = filedialog.asksaveasfilename(
            title='Select the target file for saving records',
            defaultextension='.csv',
            filetypes=[('CSV', '*.csv', '*.CSV')],
        )
        if filename:
            self.model = m.CSVModel(filename=filename)


    """
        Metodo statico che serve soltanto per testare la finestra di Login
    """
    @staticmethod
    def _simple_login(username, password):
        return username == 'abq' and password == 'Flowers'


    """
        Metodo che serve a mostrare la form di Login
    """
    def _show_login(self):
        error = ''
        title = 'Login to ABQ Data Entry'
        while True:
            login = v.LoginDialog(self, title, error)
            if not login.result:
                return False
            username, password = login.result
            if self._simple_login(username, password):
                return True
            error = 'Login Failed'
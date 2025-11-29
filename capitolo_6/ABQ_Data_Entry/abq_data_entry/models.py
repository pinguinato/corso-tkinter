"""
        CSV File storage
"""

import csv
from pathlib import Path
from datetime import datetime
import os

from .constants import FieldTypes as FT


class CSVModel:
    """
         SCOPO DELLA CLASSE `CSVModel`:
         =============================
         Questa classe rappresenta il **Modello** (la "M" del pattern MVC) della
         nostra applicazione. Il suo unico scopo è definire la **struttura**, le
         **regole** e i **metadati** dei dati che l'applicazione gestisce.

         Non sa nulla dell'interfaccia grafica (la Vista); la sua sola
         responsabilità è essere l'autorità centrale sulla forma dei dati.

         ARCHITETTURA E FUNZIONAMENTO:
         -----------------------------
         1.  **`fields` (Dizionario-Schema)**: L'attributo di classe `fields` agisce
             come uno "schema" o un "blueprint" per un singolo record di dati.
             -   Le **chiavi** del dizionario (`"Date"`, `"Time"`, etc.) sono i nomi
                 canonici dei campi.
             -   I **valori** sono a loro volta dizionari che descrivono i metadati
                 e le regole di validazione per ogni campo:
                 -   `'req'`: Un booleano che indica se il campo è obbligatorio.
                 -   `'type'`: Usa l'enumerazione `FieldTypes` per definire il tipo
                     di dato (es. stringa, decimale, data ISO).
                 -   `'values'`: Una lista di valori consentiti, usata per campi
                     come `Combobox` o `Radiobutton`.
                 -   `'min'`, `'max'`, `'inc'`: Vincoli numerici per `Spinbox`.

         2.  **Separazione delle Competenze**: Definendo la struttura dei dati qui,
             la separiamo completamente dalla Vista. Se in futuro dovessimo
             cambiare una regola (es. aggiungere un nuovo "Lab"), dovremmo
             modificare solo questo file, senza toccare il codice dell'interfaccia.

         3.  **Evoluzione Futura**: Attualmente, la classe definisce solo lo schema.
             In futuro, conterrà anche i metodi per interagire con i dati, come
             `save_record(data)`, `get_all_records()`, etc.
    """
    fields = {
        "Date": {'req': True, 'type': FT.iso_date_string},
        "Time": {'req': True, 'type': FT.string_list, 'values': ['8:00', '12:00', '16:00', '20:00']},
        "Technician": {'req': True, 'type': FT.string},
        "Lab": {'req': True, 'type': FT.short_string_list, 'values': ['A', 'B', 'C']},
        "Plot": {'req': True, 'type': FT.string_list, 'values': [str(x) for x in range(1, 21)]},
        "Seed Sample": {'req': True, 'type': FT.string},
        "Humidity": {'req': True, 'type': FT.decimal, 'min': 0.5, 'max': 52.0, 'inc': 0.1},
        "Light": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 100.0, 'inc': 0.1},
        "Temperature": {'req': True, 'type': FT.decimal, 'min': 4, 'max': 40.0, 'inc': 0.1},
        "Equipment Fault": {'req': False, 'type': FT.boolean},
        "Plants": {'req': True, 'type': FT.integer, 'min': 0, 'max': 20},
        "Blossoms": {'req': True, 'type': FT.integer, 'min': 0, 'max': 1000},
        "Fruit": {'req': True, 'type': FT.integer, 'min': 0, 'max': 1000},
        "Min Height": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1000, 'inc': .01},
        "Max Height": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1000, 'inc': .01},
        "Med Height": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1000, 'inc': .01},
        "Notes": {'req': False, 'type': FT.long_string}
    }

    def __init__(self):
        """Costruttore della classe CSVModel.

                 Questo metodo inizializza il modello di dati per il salvataggio su file CSV.
                 Il suo compito principale è determinare il file di destinazione e,
                 fondamentalmente, verificare in anticipo di avere i permessi necessari
                 per scrivere su quel file, evitando errori a runtime durante il salvataggio.

                 ANALISI TECNICA:
                 1.  **Generazione del Nome File**: Crea un nome di file univoco per ogni
                     giorno, basandosi sulla data corrente (es. `abq_data_record_2023-10-27.csv`).
                     Questo organizza i dati in file giornalieri.

                 2.  **Controllo dei Permessi (Fail-Fast)**: Esegue una serie di controlli
                     preventivi utilizzando `os.access` per garantire che il file possa
                     essere scritto. Questo approccio "fail-fast" (fallisci subito) è
                     una pratica robusta che previene il fallimento dell'operazione di
                     salvataggio a metà, dopo che l'utente ha già inserito i dati.
                     I controlli sono:
                     -   **Se il file non esiste**: Verifica che la directory genitore sia
                         scrivibile (per poter creare il file).
                     -   **Se il file esiste già**: Verifica che il file stesso sia
                         scrivibile (per poter aggiungere nuove righe).

                 3.  **Sollevamento dell'Eccezione**: Se uno dei controlli sui permessi
                     fallisce, il costruttore solleva immediatamente una `PermissionError`,
                     bloccando la creazione dell'oggetto `CSVModel` e segnalando
                     chiaramente il problema all'avvio dell'applicazione.
        """
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "abq_data_record_{}.csv".format(datestring)
        self.file = Path(filename)

        file_exists = os.access(self.file, os.F_OK)
        parent_writeable = os.access(self.file.parent, os.W_OK)
        file_writeable = os.access(self.file, os.W_OK)
        if (
            (not file_exists and not parent_writeable) or
                (file_exists and not file_writeable)
        ):
            msg = f"Permission denied accessing file: {filename}"
            raise PermissionError

    """
    Salva un singolo record di dati nel file CSV.

             Questo metodo è responsabile della persistenza dei dati. Riceve un
             dizionario di dati e lo accoda al file CSV del giorno.

             Args:
                 data (dict): Un dizionario contenente i dati del record da salvare.

             ANALISI TECNICA:
             1.  **Controllo Esistenza File**: Determina se il file CSV esiste già.
                 Questa informazione è fondamentale per decidere se scrivere o meno
                 la riga di intestazione (header).
             2.  **Apertura Sicura del File**: Utilizza un `with open(...)` (context
                 manager) per aprire il file in modalità "append" (`'a'`). Questo
                 garantisce che il file venga chiuso automaticamente e in modo sicuro,
                 anche in caso di errori. `newline=''` è essenziale per la scrittura
                 di file CSV per evitare la creazione di righe vuote indesiderate.
             3.  **Uso di `csv.DictWriter`**: Invece di scrivere manualmente stringhe
                 separate da virgole, usa `csv.DictWriter`. Questo approccio è
                 molto più robusto perché si basa sui nomi dei campi definiti nello
                 schema del modello (`self.fields.keys()`), garantendo che i dati
                 vengano scritti nelle colonne corrette, indipendentemente
                 dall'ordine.
             4.  **Scrittura del Record**: Se il file è nuovo, scrive prima
                 l'intestazione. Successivamente, scrive il dizionario `data` come
                 una nuova riga nel file.
    """
    def save_record(self, data):
        newfile = not self.file.exists()

        with open(self.file, 'a', newline='') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
            if newfile:
                csvwriter.writeheader()

            csvwriter.writerow(data)
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

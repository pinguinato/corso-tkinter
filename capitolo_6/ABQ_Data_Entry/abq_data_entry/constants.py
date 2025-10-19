"""
    Questa classe è stata creata per indicare quali tipi i campi andiamo a salvare nel nostro modello.
"""

from enum import Enum, auto


class FieldTypes(Enum):
    """
         SCOPO DELLA CLASSE `FieldTypes`:
         ===============================
         Questa classe, basata su `Enum` (Enumerazione), definisce un insieme di
         costanti simboliche per rappresentare i diversi tipi di dati che i campi
         del nostro modello possono assumere.

         È un componente fondamentale del nostro **Modello Dati** (Model nel pattern MVC).

         PERCHÉ USARE UN'ENUMERAZIONE?
         -----------------------------
         Invece di usare stringhe di testo generiche (le cosiddette "magic strings")
         come "string" o "integer" nel codice, usiamo nomi simbolici come
         `FieldTypes.string` o `FieldTypes.integer`. Questo approccio offre
         vantaggi significativi:

         1.  **Leggibilità**: Il codice diventa più chiaro e auto-documentante.
         2.  **Manutenibilità**: Se un tipo deve essere rinominato, basta cambiarlo
             in un unico posto.
         3.  **Robustezza**: Riduce il rischio di errori di battitura, che non
             verrebbero rilevati fino all'esecuzione del programma. L'uso di un
             membro Enum inesistente genera un errore immediato.

         COME FUNZIONA:
         --------------
         -   `Enum`: È la classe base di Python per creare enumerazioni.
         -   `auto()`: È una funzione di supporto che assegna automaticamente un valore
             unico (di solito un intero progressivo) a ogni membro dell'enumerazione.
             Questo è utile perché a noi interessano i nomi simbolici, non i valori
             sottostanti.
    """
    string = auto()
    string_list = auto()
    short_string_list = auto()
    iso_date_string = auto()
    long_string = auto()
    decimal = auto()
    integer = auto()
    boolean = auto()

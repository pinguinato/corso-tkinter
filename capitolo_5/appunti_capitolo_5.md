# Appunti Capitolo 5

## Validazione dei Dati: Principi e Strategie

La validazione dei dati è un processo cruciale per garantire l'integrità e la coerenza delle informazioni raccolte tramite un'interfaccia grafica. Prima di scrivere qualsiasi codice, è fondamentale definire le **regole di validazione**: cosa è un dato accettabile e cosa non lo è?

La risposta a questa domanda definisce il comportamento del nostro form.

### Strategie Fondamentali di Validazione

Possiamo raggruppare le tecniche di validazione in quattro strategie principali:

1.  **Prevenzione dell'Errore (Input Filtering)**
    - **Cosa significa**: Impedire fisicamente all'utente di inserire dati non validi.
    - **Esempio pratico**: In un campo numerico, il programma ignora la pressione di tasti non numerici (come le lettere). L'utente non può commettere l'errore.
    - **Vantaggio**: È l'approccio meno frustrante per l'utente.

2.  **Feedback Visivo Immediato (Real-time Validation)**
    - **Cosa significa**: Fornire un riscontro visivo istantaneo non appena l'utente inserisce un dato non conforme.
    - **Esempio pratico**: Se un campo obbligatorio viene lasciato vuoto, la sua etichetta diventa rossa non appena l'utente passa al campo successivo.
    - **Vantaggio**: Guida l'utente alla correzione in tempo reale, senza attendere il salvataggio.

3.  **Messaggi di Errore Chiari**
    - **Cosa significa**: Quando un errore viene rilevato, comunicarlo all'utente in modo chiaro, conciso e costruttivo.
    - **Esempio pratico**: Invece di un generico "Errore", mostrare un messaggio specifico come "La data deve essere nel formato GG/MM/AAAA" in una barra di stato o vicino al campo errato.
    - **Vantaggio**: L'utente capisce subito cosa deve correggere.

4.  **Blocco della Sottomissione (Submission Gating)**
    - **Cosa significa**: Disabilitare il pulsante di salvataggio ("Save" o "Submit") finché tutti i campi del form non rispettano le regole di validazione.
    - **Esempio pratico**: Il pulsante "Save" rimane grigio e non cliccabile finché tutti i campi obbligatori non sono stati compilati correttamente.
    - **Vantaggio**: Garantisce che solo dati validi possano essere inviati, prevenendo errori a livello di sistema.

## La validazione in Tkinter

Tkinter offre un meccanismo di validazione integrato per i widget di input, basato principalmente su tre opzioni di configurazione:

-   `validate`: Specifica *quando* deve avvenire la validazione. La scelta del valore è fondamentale per implementare la strategia corretta. I valori possibili sono:

| Valore | Descrizione | Uso Tipico |
| :--- | :--- | :--- |
| `'none'` | Disabilita la validazione. | Default. |
| `'key'` | Valida a ogni pressione (o rilascio) di un tasto. | **Prevenzione dell'errore** (input filtering). |
| `'focusin'` | Valida quando il widget riceve il focus (viene selezionato). | Meno comune, utile per controlli all'ingresso. |
| `'focusout'` | Valida quando il widget perde il focus (l'utente lascia il campo). | **Feedback visivo** (real-time validation). |
| `'focus'` | Valida sia su `focusin` che su `focusout`. | Combinazione dei due eventi di focus. |
| `'all'` | Valida su `key`, `focusin` e `focusout`. | La scelta più completa e flessibile. |

> **Nota importante**: È possibile specificare un solo valore per `validate`. Tutti gli eventi attivati da quel valore (es. `key` e `focusout` per `'all'`) eseguiranno sempre la stessa funzione di validazione definita in `validatecommand`.

-   `validatecommand`: Specifica la *funzione* (o metodo) da chiamare per eseguire la logica di validazione. Questa funzione deve restituire `True` se il dato è valido e `False` altrimenti.

-   `invalidcommand`: Specifica la *funzione* da chiamare se la validazione fallisce (cioè se `validatecommand` restituisce `False`). È qui che tipicamente si implementa il **feedback visivo**, come cambiare il colore di un'etichetta.

Integrando questo sistema nelle nostre classi personalizzate (`LabelInput`), possiamo creare un sistema di validazione potente, riutilizzabile e facile da gestire.



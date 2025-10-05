# Corso Tkinter
 
 Repository di esercizi per il corso di programmazione di interfacce grafiche (GUI) in Python con la libreria Tkinter.
 
 A cura di Roberto Gianotto
 
 ---
 
 ## Prerequisiti
 
 Per eseguire gli esercizi di questo corso, è necessario avere Python installato sul proprio sistema e il modulo `tkinter`.
 
 ### Versioni di Python Utilizzate
 
 Gli esercizi sono stati testati con le seguenti versioni di Python, ma dovrebbero funzionare con qualsiasi versione di Python 3.7 o successiva.
 
 *   **Linux**: Python **3.10.12**
 *   **Windows**: Python **3.12**
 
 ### Verifica e Installazione di Tkinter
 
 `tkinter` è incluso nella libreria standard di Python, ma su alcuni sistemi operativi (in particolare Linux) potrebbe essere necessario installarlo separatamente.
 
 #### 1. Verifica della presenza di Tkinter
 
 Apri un terminale o prompt dei comandi ed esegui il comando appropriato per il tuo sistema. Se `tkinter` è installato correttamente, si aprirà una piccola finestra di test.
 
 *   **Su Windows, macOS e la maggior parte delle distribuzioni Linux:**
     ```bash
     python -m tkinter
     ```
 *   **Su alcune distribuzioni Linux più datate:**
     ```bash
     python3 -m tkinter
     ```
 
 #### 2. Installazione
 
 *   **Windows**: `tkinter` è **incluso di default** con l'installer ufficiale di Python. Se non lo hai, assicurati di aver scaricato Python dal sito ufficiale: python.org
 
 *   **macOS**: `tkinter` è **incluso di default** con l'installer ufficiale di Python per macOS scaricabile da python.org.
 
 *   **Linux (Debian/Ubuntu)**: Se il comando di verifica fallisce, puoi installare il modulo con `apt`.
     ```bash
     sudo apt update
     sudo apt install python3-tk
     ```
 
 *   **Linux (Fedora/CentOS/RHEL)**: Usa `dnf` (o `yum` su versioni più vecchie).
     ```bash
     sudo dnf install python3-tkinter
     
## Data Entry Application
  
 Il file `data_entry_app.py` rappresenta il progetto centrale e il vero laboratorio di questo corso.
  
 Attraverso i vari capitoli, questo singolo file evolverà da un semplice script procedurale a un'applicazione GUI completa e robusta, costruita secondo i moderni principi della programmazione a oggetti.
  
 L'obiettivo è esplorare, passo dopo passo, le tecniche per creare un'applicazione Tkinter professionale, manutenibile e ricca di funzionalità, tra cui:
  
 *   Struttura a classi e creazione di componenti riutilizzabili.
 *   Gestione avanzata del layout per interfacce responsive.
 *   Validazione dei dati in tempo reale per una migliore esperienza utente.
 *   Interazione con il file system per il salvataggio dei dati (CSV).

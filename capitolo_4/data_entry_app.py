"""
    ------------------------------------------------------
    Chapter 4 - data_entry_app.py with objects and classes
    ------------------------------------------------------

    Questo script definisce la classe `BoundText`, un widget personalizzato
    per la libreria grafica `tkinter`.

    SCOPO DELLA CLASSE:
    La classe `BoundText` estende il widget standard `tk.Text` per aggiungere
    una funzionalità fondamentale che manca nativamente: il "two-way data binding"
    (collegamento dati a due vie) tramite l'opzione `textvariable`.

    In pratica, un'istanza di `BoundText` e una variabile di controllo di Tkinter
    (come `tk.StringVar`) rimangono costantemente sincronizzate:
    1.  Se la variabile viene modificata programmaticamente (es. `var.set(...)`),
        il testo nel widget si aggiorna automaticamente.
    2.  Se l'utente scrive o modifica il testo all'interno del widget,
        la variabile collegata viene aggiornata di conseguenza.

    COME FUNZIONA (ANALISI TECNICA):
    Il two-way binding è implementato attraverso due meccanismi distinti:

    1.  Binding "dalla Variabile al Widget":
        - Nel costruttore `__init__`, viene impostato un "osservatore" sulla
          variabile tramite `self._variable.trace_add('write', ...)`.
        - Questo `trace` fa sì che, ogni volta che la variabile viene "scritta"
          (modificata), venga eseguito il metodo `_set_content`.
        - `_set_content` si occupa di cancellare il testo attuale del widget
          e inserire il nuovo valore preso dalla variabile.

    2.  Binding "dal Widget alla Variabile":
        - Sempre in `__init__` (nella versione corretta) o in `_set_content`
          (nella versione originale), il widget viene collegato all'evento
          virtuale `<<Modified>>` tramite `self.bind('<<Modified>>', ...)`.
        - Questo evento viene generato da Tkinter ogni volta che il contenuto
          del widget `Text` viene alterato.
        - L'evento scatena l'esecuzione del metodo `_set_var`, che a sua volta:
          a) Controlla se la modifica è reale con `self.edit_modified()`.
          b) Legge il nuovo contenuto del widget con `self.get(...)`.
          c) Aggiorna la variabile collegata con `self._variable.set(...)`.
          d) Resetta il flag di modifica con `self.edit_modified(False)` per
             evitare che l'evento si ripeta senza una nuova modifica.
"""

from datetime import datetime
from pathlib import Path
import csv
import tkinter as tk
from tkinter import ttk

class BoundText(tk.Text):
    """A Text widget with a bound variable"""
    def __init__(self, *args, textvariable=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._variable = textvariable
        if self._variable:
            self.insert('1.0', self._variable.get())
            self._variable.trace_add('write', self._set_content)

    def _set_content(self, *_):
        """Set the text contents to the variable"""
        self.delete('1.0', tk.END)
        self.insert('1.0', self._variable.get())
        self.bind('<<Modified>>', self._set_var)

    def _set_var(self, *_):
        """Set the variable to the text contents"""
        if self.edit_modified():
            content = self.get('1.0', 'end-1chars')
            self._variable.set(content)
            self.edit_modified(False)


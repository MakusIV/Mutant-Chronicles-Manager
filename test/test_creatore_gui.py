"""
Il meccanismo di esecuzione in background di `creatore_gui.py`.

`al_termine`/`in_caso_di_errore` sono funzioni Python semplici, non metodi di un
QObject: connesse direttamente al segnale del lavoro (che vive su un thread separato
dopo `moveToThread`), Qt non aveva un'affinità di thread su cui basare la scelta
automatica della connessione, e le eseguiva sul thread del lavoro invece che su quello
grafico. I widget toccati da lì non sono thread-safe: la corruzione non si manifestava
subito, ma al primo evento successivo sull'interfaccia — nella GUI reale, il cambio
scheda dopo la creazione di una collezione — con un segmentation fault.

Qui si verifica solo il meccanismo (`esegui_in_background`), isolato dalla generazione
di collezioni/mazzi: con una funzione fittizia, basta identificare il thread che esegue
il callback per sapere se il difetto è tornato.
"""

import threading

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import QCoreApplication, QEventLoop, QObject, QTimer

from source.gui.creatore_gui import esegui_in_background


@pytest.fixture
def app():
    return QCoreApplication.instance() or QCoreApplication([])


def _esegui_e_attendi(app, funzione, timeout_ms=5000):
    """
    Chiama `esegui_in_background` con `funzione` e restituisce (esito, thread, valore),
    dove `esito` è "completato" o "fallito" ed `esito` resta None se il timeout scatta
    prima che nessuno dei due si verifichi (il difetto che questo test previene non
    faceva mai scattare il callback, quindi un timeout è un fallimento, non un errore
    del test).

    Attende anche che `lavori_in_corso` torni vuota, cioè che il QThread abbia
    davvero finito (non solo che il callback sia scattato): uscire prima, lasciando
    che `finestra` — e con lei il QThread ancora in chiusura — vada distrutta,
    produce un `qFatal` Qt ("Destroyed while thread is still running"), un crash
    indipendente da quello che questo test verifica.
    """
    finestra = QObject()
    lavori_in_corso = []
    cattura = {"esito": None, "thread": None, "valore": None}

    loop = QEventLoop()

    def al_termine(risultato):
        cattura["esito"] = "completato"
        cattura["thread"] = threading.current_thread()
        cattura["valore"] = risultato

    def in_caso_di_errore(messaggio):
        cattura["esito"] = "fallito"
        cattura["thread"] = threading.current_thread()
        cattura["valore"] = messaggio

    esegui_in_background(finestra, lavori_in_corso, funzione, {}, al_termine, in_caso_di_errore)

    timer_controllo = QTimer()
    timer_controllo.setInterval(20)

    def controlla_se_finito():
        if not lavori_in_corso:
            timer_controllo.stop()
            loop.quit()

    timer_controllo.timeout.connect(controlla_se_finito)
    timer_controllo.start()

    # Rete di sicurezza: senza il ponte sul thread giusto, il callback non scattava mai
    # (visto durante la correzione: la prima versione della QueuedConnection restava in
    # attesa per sempre) — senza timeout il test resterebbe bloccato invece di fallire.
    QTimer.singleShot(timeout_ms, loop.quit)
    loop.exec()

    return cattura["esito"], cattura["thread"], cattura["valore"]


def test_al_termine_esegue_sul_thread_grafico(app):
    esito, thread, valore = _esegui_e_attendi(app, lambda: "ok")

    assert esito == "completato"
    assert thread is threading.main_thread(), (
        "al_termine è stato eseguito su un thread diverso da quello grafico: "
        "toccare i widget da lì corrompe l'interfaccia (segmentation fault differito)"
    )
    assert valore == "ok"


def test_in_caso_di_errore_esegue_sul_thread_grafico(app):
    def funzione_che_fallisce():
        raise ValueError("errore di prova")

    esito, thread, valore = _esegui_e_attendi(app, funzione_che_fallisce)

    assert esito == "fallito"
    assert thread is threading.main_thread(), (
        "in_caso_di_errore è stato eseguito su un thread diverso da quello grafico"
    )
    assert valore == "errore di prova"

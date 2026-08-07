"""
Interfaccia grafica per la creazione di collezioni e mazzi.

Raccoglie in un'unica finestra gli input richiesti da:

    - `crea_cartelle_collezioni` (opzione 1 del menu di `Creatore_Collezione.py`,
      "crea cartelle collezioni")
    - `crea_mazzo_da_cartella_collezione_con_parametri` (la logica dietro l'opzione 14
      del menu di `Creatore_Mazzo.py`, "Crea e salva mazzo da cartella collezioni")

sostituendo le sequenze di `input()` da terminale con campi e pulsanti. La finestra
include anche i pulsanti per aprire `visualizzatore_collezione.py` e
`visualizzatore_mazzo.py` sulle collezioni e sui mazzi appena creati, o su cartelle
già esistenti sotto `out/`.

Uso:

    .venv/bin/python source/gui/creatore_gui.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from source.cards.Arte import DisciplinaArte
from source.cards.Guerriero import Set_Espansione
from source.cards.Oscura_Simmetria import ApostoloOscuraSimmetria
from source.logic.Creatore_Collezione import crea_cartelle_collezioni
from source.logic.Creatore_Mazzo import (
    FAZIONI_DOOMTROOPER, crea_mazzo_da_cartella_collezione_con_parametri,
)
from source.gui.visualizzatore_collezione import cerca_collezioni
from source.gui.visualizzatore_mazzo import cerca_mazzi_disponibili

RADICE_PROGETTO = Path(__file__).resolve().parents[2]
PERCORSO_OUT = RADICE_PROGETTO / "out"
SCRIPT_VISUALIZZATORE_COLLEZIONE = Path(__file__).resolve().with_name("visualizzatore_collezione.py")
SCRIPT_VISUALIZZATORE_MAZZO = Path(__file__).resolve().with_name("visualizzatore_mazzo.py")

# Il "Nessuno" dell'enumerazione ha valore None: non è una scelta di orientamento
# selezionabile, è l'assenza di scelta (che nella GUI corrisponde a non spuntare nulla).
APOSTOLI_SELEZIONABILI = [apostolo for apostolo in ApostoloOscuraSimmetria if apostolo.value is not None]


# ================================================================================
# Esecuzione in background — a livello di modulo per poterla testare da sola,
# senza dover costruire un'intera collezione o un intero mazzo.
# ================================================================================

def esegui_in_background(finestra, lavori_in_corso: List[Any], funzione, kwargs: Dict[str, Any],
                          al_termine, in_caso_di_errore) -> None:
    """
    Avvia `funzione(**kwargs)` su un QThread e richiama `al_termine`/`in_caso_di_errore`
    in coda sul thread grafico.

    Args:
        finestra: la finestra principale (QMainWindow), usata come genitore del thread
            e del ponte, e per garantire che questi vivano sul thread grafico
        lavori_in_corso: lista viva per la durata della finestra, a cui viene aggiunta
            (e da cui viene tolta a fine lavoro) una voce per thread/lavoro/ponte —
            senza un riferimento esplicito, Python li raccoglierebbe a fine funzione
            lasciando i segnali penzolanti
        funzione, kwargs: la funzione da eseguire sul thread separato e i suoi argomenti
        al_termine, in_caso_di_errore: callback richiamate sul thread grafico, con il
            risultato o il messaggio di errore
    """
    from PySide6.QtCore import QObject, Qt, QThread, Signal

    class _LavoroBackground(QObject):
        """Esegue una funzione di creazione in un thread separato, per non bloccare
        l'interfaccia durante operazioni che richiedono decine di secondi (copia
        immagini, generazione PDF)."""

        completato = Signal(object)
        fallito = Signal(str)

        def __init__(self, funzione, kwargs: Dict[str, Any]) -> None:
            super().__init__()
            self._funzione = funzione
            self._kwargs = kwargs

        def esegui(self) -> None:
            try:
                risultato = self._funzione(**self._kwargs)
            except Exception as exc:  # difesa: le funzioni chiamate incapsulano già i propri errori
                self.fallito.emit(str(exc))
                return
            self.completato.emit(risultato)

    class _Ponte(QObject):
        """
        Destinatario sempre sul thread grafico, per instradare in coda i callback dei
        lavori in background.

        `al_termine`/`in_caso_di_errore` sono funzioni Python semplici, non metodi di un
        QObject: connesse direttamente al segnale di `_LavoroBackground` (che vive sul
        thread del lavoro, dopo `moveToThread`), Qt non ha un'affinità di thread su cui
        basare la scelta automatica della connessione e finiva per eseguirle sul thread
        del lavoro invece che su quello grafico. I widget non sono thread-safe: la
        corruzione non si manifestava subito, ma al primo evento successivo
        sull'interfaccia (il cambio scheda), con un segmentation fault.

        Il `_Ponte` risolve l'ambiguità: è creato qui, sul thread grafico, quindi la sua
        affinità è certa, e la connessione fra il suo segnale e il suo stesso metodo può
        essere messa esplicitamente in coda. Il primo salto (dal lavoro al ponte) resta
        senza destinatario certo, ma si limita a un `emit`, sempre sicuro da qualunque
        thread — nessun widget viene toccato prima del secondo salto.
        """

        inoltra = Signal(object, object)

        def __init__(self, parent: QObject) -> None:
            super().__init__(parent)
            self.inoltra.connect(self._esegui, Qt.ConnectionType.QueuedConnection)

        @staticmethod
        def _esegui(funzione, argomento) -> None:
            funzione(argomento)

    thread = QThread(finestra)
    lavoro = _LavoroBackground(funzione, kwargs)
    lavoro.moveToThread(thread)
    ponte = _Ponte(finestra)

    voce = (thread, lavoro, ponte)
    lavori_in_corso.append(voce)

    def pulisci() -> None:
        if voce in lavori_in_corso:
            lavori_in_corso.remove(voce)

    thread.started.connect(lavoro.esegui)
    lavoro.completato.connect(lambda risultato: ponte.inoltra.emit(al_termine, risultato))
    lavoro.fallito.connect(lambda messaggio: ponte.inoltra.emit(in_caso_di_errore, messaggio))
    lavoro.completato.connect(thread.quit)
    lavoro.fallito.connect(thread.quit)
    thread.finished.connect(pulisci)
    thread.start()


# ================================================================================
# STRATO DATI — ricerca cartelle, indipendente dall'interfaccia grafica
# ================================================================================

def cerca_cartelle_collezioni_esistenti() -> List[str]:
    """
    Elenca i nomi delle cartelle sotto out/ prodotte da `crea_cartelle_collezioni`
    (contengono cioè un file lista_collezioni.json).

    Returns:
        I nomi delle cartelle, relativi a out/, ordinati
    """
    if not PERCORSO_OUT.is_dir():
        return []
    return sorted(p.name for p in PERCORSO_OUT.iterdir()
                  if p.is_dir() and (p / "lista_collezioni.json").is_file())


def numero_collezioni_in_cartella(nome_cartella: str) -> int:
    """Conta le collezioni giocatore presenti in una cartella prodotta dall'opzione 1."""
    return len(cerca_collezioni(PERCORSO_OUT / nome_cartella))


def trova_mazzi(cartella: Path) -> List[Path]:
    """
    Individua le cartelle Mazzo_Giocatore_<N> raggiungibili da un percorso, qualunque
    sia il livello a cui punta: la cartella del mazzo stessa, quella che raccoglie le
    collezioni di più giocatori (out/Collezioni_<data>), o la radice out/.

    Args:
        cartella: Punto di partenza della ricerca

    Returns:
        Le cartelle Mazzo_Giocatore_<N> trovate, ordinate
    """
    if not cartella.is_dir():
        return []
    if next(cartella.glob("mazzo_giocatore_*.json"), None) is not None:
        return [cartella]
    diretti = sorted(p for p in cartella.glob("*/Mazzo_Giocatore_*") if p.is_dir())
    if diretti:
        return diretti
    return cerca_mazzi_disponibili(cartella)


def avvia_visualizzatore(script: Path, argomento: Path) -> None:
    """
    Apre uno dei due moduli di visualizzazione in un processo separato.

    Un processo separato, e non una chiamata diretta a `avvia_interfaccia` dei moduli
    di visualizzazione, perché Qt ammette un solo ciclo eventi per processo: se questa
    finestra è già in esecuzione (il caso normale, dato che il pulsante si preme da
    qui), un `QApplication.exec()` innescato dal visualizzatore verrebbe rifiutato come
    ciclo annidato — la finestra comparirebbe e sparirebbe subito, perché l'oggetto
    Python che la tiene in vita andrebbe distrutto non appena `avvia_interfaccia`
    ritorna. Lanciarlo come processo a sé, con il proprio ciclo eventi indipendente, è
    esattamente il modo in cui questi moduli sono già pensati per essere eseguiti da
    riga di comando.

    Args:
        script: Il file .py del visualizzatore da avviare
        argomento: La cartella da passargli come argomento
    """
    subprocess.Popen([sys.executable, str(script), str(argomento)])


# ================================================================================
# INTERFACCIA GRAFICA
# ================================================================================

def avvia_interfaccia() -> int:
    """
    Apre la finestra di creazione di collezioni e mazzi.

    Returns:
        Il codice di uscita dell'applicazione
    """
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import (
            QApplication, QCheckBox, QComboBox, QFileDialog, QFormLayout, QHBoxLayout,
            QInputDialog, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
            QMessageBox, QPushButton, QSpinBox, QTabWidget, QWidget,
        )
    except ImportError:
        print("PySide6 non è installato. Installalo nell'ambiente del progetto con:\n"
              "    .venv/bin/pip install PySide6-Essentials", file=sys.stderr)
        return 1

    # Riusa l'istanza esistente se c'è: Qt ne ammette una sola per processo.
    applicazione = QApplication.instance() or QApplication(sys.argv)

    finestra = QMainWindow()
    finestra.setWindowTitle("Creazione Collezioni e Mazzi")
    finestra.resize(760, 680)

    # Tiene in vita i lavori in corso: senza un riferimento esplicito, Python
    # raccoglierebbe thread e worker a fine funzione lasciando i segnali penzolanti.
    lavori_in_corso: List[Any] = []

    def lista_selezionabile(valori: List[str]) -> QListWidget:
        """Crea un elenco a scelta multipla tramite caselle di spunta."""
        lista = QListWidget()
        lista.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        for valore in valori:
            voce = QListWidgetItem(valore)
            voce.setFlags(voce.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            voce.setCheckState(Qt.CheckState.Unchecked)
            lista.addItem(voce)

        # Un click ovunque sulla riga alterna la spunta: cliccare esattamente sul
        # riquadro della casella è scomodo con elenchi di poche voci come questi.
        def alterna(voce_cliccata: QListWidgetItem) -> None:
            nuovo_stato = (Qt.CheckState.Unchecked if voce_cliccata.checkState() == Qt.CheckState.Checked
                           else Qt.CheckState.Checked)
            voce_cliccata.setCheckState(nuovo_stato)

        lista.itemClicked.connect(alterna)

        altezza = min(24 * len(valori) + 6, 160)
        lista.setMaximumHeight(max(altezza, 50))
        return lista

    def selezionati(lista: QListWidget) -> List[str]:
        return [lista.item(i).text() for i in range(lista.count())
                if lista.item(i).checkState() == Qt.CheckState.Checked]

    # ================================================================================
    # Scheda "Creazione Collezione" (opzione 1 di Creatore_Collezione.py)
    # ================================================================================

    scheda_collezione = QWidget()
    modulo_collezione = QFormLayout(scheda_collezione)

    campo_numero_giocatori = QSpinBox()
    campo_numero_giocatori.setRange(1, 999)
    campo_numero_giocatori.setValue(2)

    lista_espansioni_collezione = lista_selezionabile([e.value for e in Set_Espansione])
    lista_espansioni_collezione.setObjectName("lista_espansioni_collezione")

    campo_orientamento = QCheckBox("Orienta le collezioni verso combinazioni di fazioni")

    campo_nome_cartella = QLineEdit()
    campo_nome_cartella.setObjectName("campo_nome_cartella")
    campo_nome_cartella.setPlaceholderText("Collezioni_<data>_<ora>, se lasciato vuoto")

    pulsante_crea_collezione = QPushButton("Crea Collezioni")
    stato_collezione = QLabel("")
    stato_collezione.setObjectName("stato_collezione")
    stato_collezione.setWordWrap(True)
    pulsante_apri_collezione_creata = QPushButton("Apri Visualizzatore su questa creazione")
    pulsante_apri_collezione_creata.setEnabled(False)
    pulsante_apri_collezione_esistente = QPushButton("Apri Visualizzatore su una cartella esistente…")

    modulo_collezione.addRow("Numero giocatori:", campo_numero_giocatori)
    modulo_collezione.addRow("Espansioni:", lista_espansioni_collezione)
    modulo_collezione.addRow("", campo_orientamento)
    modulo_collezione.addRow("Nome cartella (opzionale):", campo_nome_cartella)
    modulo_collezione.addRow(pulsante_crea_collezione)
    modulo_collezione.addRow(stato_collezione)
    modulo_collezione.addRow(pulsante_apri_collezione_creata)
    modulo_collezione.addRow(pulsante_apri_collezione_esistente)

    percorso_collezione_creata: Dict[str, Optional[Path]] = {"valore": None}

    def crea_collezione() -> None:
        selezionate = selezionati(lista_espansioni_collezione)
        if not selezionate:
            QMessageBox.warning(finestra, "Espansioni mancanti", "Seleziona almeno un'espansione.")
            return

        pulsante_crea_collezione.setEnabled(False)
        pulsante_apri_collezione_creata.setEnabled(False)
        stato_collezione.setText("Creazione in corso…")

        kwargs = dict(
            numero_giocatori=campo_numero_giocatori.value(),
            espansioni=[Set_Espansione(v) for v in selezionate],
            orientamento=campo_orientamento.isChecked(),
            nome_cartella=(campo_nome_cartella.text().strip() or None),
            verbose=True,
        )

        def completata(risultato: Dict[str, Any]) -> None:
            pulsante_crea_collezione.setEnabled(True)
            if "errore" in risultato:
                stato_collezione.setText(f"❌ {risultato['errore']}")
                return

            percorso_collezione_creata["valore"] = Path(risultato["percorso_principale"])
            stato_collezione.setText(
                f"✅ {risultato['numero_collezioni']} collezioni create in "
                f"{risultato['percorso_principale']}")
            pulsante_apri_collezione_creata.setEnabled(True)

            # Rende subito disponibile la cartella appena creata nella scheda del mazzo.
            nome_cartella_creata = Path(risultato["percorso_principale"]).name
            if campo_cartella_collezioni.findText(nome_cartella_creata) < 0:
                campo_cartella_collezioni.addItem(nome_cartella_creata)
            campo_cartella_collezioni.setCurrentText(nome_cartella_creata)

        def fallita(messaggio: str) -> None:
            pulsante_crea_collezione.setEnabled(True)
            stato_collezione.setText(f"❌ Errore imprevisto: {messaggio}")

        esegui_in_background(finestra, lavori_in_corso, crea_cartelle_collezioni, kwargs, completata, fallita)

    def apri_collezione_creata() -> None:
        percorso = percorso_collezione_creata["valore"]
        if percorso is None:
            return
        if not cerca_collezioni(percorso):
            QMessageBox.warning(finestra, "Nessuna collezione",
                                 "La cartella creata non contiene collezioni leggibili.")
            return
        avvia_visualizzatore(SCRIPT_VISUALIZZATORE_COLLEZIONE, percorso)

    def apri_collezione_esistente() -> None:
        percorso = QFileDialog.getExistingDirectory(
            finestra, "Scegli la cartella della collezione", str(PERCORSO_OUT))
        if not percorso:
            return
        if not cerca_collezioni(Path(percorso)):
            QMessageBox.warning(finestra, "Nessuna collezione", f"Nessuna collezione trovata in {percorso}.")
            return
        avvia_visualizzatore(SCRIPT_VISUALIZZATORE_COLLEZIONE, Path(percorso))

    pulsante_crea_collezione.clicked.connect(crea_collezione)
    pulsante_apri_collezione_creata.clicked.connect(apri_collezione_creata)
    pulsante_apri_collezione_esistente.clicked.connect(apri_collezione_esistente)

    # ================================================================================
    # Scheda "Creazione Mazzo" (opzione 14 di Creatore_Mazzo.py)
    # ================================================================================

    scheda_mazzo = QWidget()
    modulo_mazzo = QFormLayout(scheda_mazzo)

    campo_cartella_collezioni = QComboBox()
    campo_cartella_collezioni.setObjectName("campo_cartella_collezioni")
    campo_cartella_collezioni.setEditable(True)
    campo_cartella_collezioni.addItems(cerca_cartelle_collezioni_esistenti())
    pulsante_sfoglia_cartella = QPushButton("Sfoglia…")

    riga_cartella = QWidget()
    disposizione_riga_cartella = QHBoxLayout(riga_cartella)
    disposizione_riga_cartella.setContentsMargins(0, 0, 0, 0)
    disposizione_riga_cartella.addWidget(campo_cartella_collezioni, 1)
    disposizione_riga_cartella.addWidget(pulsante_sfoglia_cartella)

    campo_numero_collezione = QSpinBox()
    campo_numero_collezione.setRange(1, 999)
    campo_numero_collezione.setValue(1)

    campo_carte_min = QSpinBox()
    campo_carte_min.setRange(1, 999)
    campo_carte_min.setValue(100)
    campo_carte_max = QSpinBox()
    campo_carte_max.setRange(1, 999)
    campo_carte_max.setValue(130)

    riga_carte = QWidget()
    disposizione_riga_carte = QHBoxLayout(riga_carte)
    disposizione_riga_carte.setContentsMargins(0, 0, 0, 0)
    disposizione_riga_carte.addWidget(QLabel("min"))
    disposizione_riga_carte.addWidget(campo_carte_min)
    disposizione_riga_carte.addWidget(QLabel("max"))
    disposizione_riga_carte.addWidget(campo_carte_max)
    disposizione_riga_carte.addStretch(1)

    lista_espansioni_mazzo = lista_selezionabile([e.value for e in Set_Espansione])
    lista_espansioni_mazzo.setObjectName("lista_espansioni_mazzo")

    campo_doomtrooper = QCheckBox("Doomtrooper")
    lista_fazioni_doomtrooper = lista_selezionabile([f.value for f in FAZIONI_DOOMTROOPER])
    lista_fazioni_doomtrooper.setEnabled(False)
    campo_doomtrooper.toggled.connect(lista_fazioni_doomtrooper.setEnabled)

    campo_fratellanza = QCheckBox("Fratellanza")
    lista_arti = lista_selezionabile([a.value for a in DisciplinaArte])
    lista_arti.setEnabled(False)
    campo_fratellanza.toggled.connect(lista_arti.setEnabled)

    campo_oscura_legione = QCheckBox("Oscura Legione")
    lista_apostoli = lista_selezionabile([a.value for a in APOSTOLI_SELEZIONABILI])
    lista_apostoli.setEnabled(False)
    campo_cultisti = QCheckBox("Includi Cultisti")
    campo_cultisti.setEnabled(False)

    def alterna_oscura_legione(attivo: bool) -> None:
        lista_apostoli.setEnabled(attivo)
        campo_cultisti.setEnabled(attivo)

    campo_oscura_legione.toggled.connect(alterna_oscura_legione)

    campo_eretici = QCheckBox("Includi Eretici")

    pulsante_crea_mazzo = QPushButton("Crea Mazzo")
    stato_mazzo = QLabel("")
    stato_mazzo.setObjectName("stato_mazzo")
    stato_mazzo.setWordWrap(True)
    pulsante_apri_mazzo_creato = QPushButton("Apri Visualizzatore su questo mazzo")
    pulsante_apri_mazzo_creato.setEnabled(False)
    pulsante_apri_mazzo_esistente = QPushButton("Apri Visualizzatore su una cartella esistente…")

    modulo_mazzo.addRow("Cartella collezioni:", riga_cartella)
    modulo_mazzo.addRow("Numero collezione (giocatore):", campo_numero_collezione)
    modulo_mazzo.addRow("Numero carte:", riga_carte)
    modulo_mazzo.addRow("Espansioni:", lista_espansioni_mazzo)
    modulo_mazzo.addRow(campo_doomtrooper)
    modulo_mazzo.addRow("Fazioni Doomtrooper (nessuna spunta = tutte):", lista_fazioni_doomtrooper)
    modulo_mazzo.addRow(campo_fratellanza)
    modulo_mazzo.addRow("Discipline Arte (nessuna spunta = tutte):", lista_arti)
    modulo_mazzo.addRow(campo_oscura_legione)
    modulo_mazzo.addRow("Apostoli (nessuna spunta = tutti):", lista_apostoli)
    modulo_mazzo.addRow("", campo_cultisti)
    modulo_mazzo.addRow("", campo_eretici)
    modulo_mazzo.addRow(pulsante_crea_mazzo)
    modulo_mazzo.addRow(stato_mazzo)
    modulo_mazzo.addRow(pulsante_apri_mazzo_creato)
    modulo_mazzo.addRow(pulsante_apri_mazzo_esistente)

    percorso_mazzo_creato: Dict[str, Optional[Path]] = {"valore": None}

    def aggiorna_numero_collezioni_massimo(nome_cartella: str) -> None:
        quante = numero_collezioni_in_cartella(nome_cartella.strip())
        if quante:
            campo_numero_collezione.setMaximum(quante)

    campo_cartella_collezioni.currentTextChanged.connect(aggiorna_numero_collezioni_massimo)
    aggiorna_numero_collezioni_massimo(campo_cartella_collezioni.currentText())

    def sfoglia_cartella_collezioni() -> None:
        percorso = QFileDialog.getExistingDirectory(
            finestra, "Scegli la cartella delle collezioni", str(PERCORSO_OUT))
        if percorso:
            campo_cartella_collezioni.setEditText(Path(percorso).name)

    def crea_mazzo() -> None:
        nome_cartella = campo_cartella_collezioni.currentText().strip()
        if not nome_cartella:
            QMessageBox.warning(finestra, "Cartella mancante",
                                 "Indica la cartella con le collezioni da cui creare il mazzo.")
            return
        selezionate = selezionati(lista_espansioni_mazzo)
        if not selezionate:
            QMessageBox.warning(finestra, "Espansioni mancanti", "Seleziona almeno un'espansione.")
            return
        if campo_carte_min.value() > campo_carte_max.value():
            QMessageBox.warning(finestra, "Intervallo non valido",
                                 "Il numero minimo di carte non può superare il massimo.")
            return
        if not (campo_doomtrooper.isChecked() or campo_fratellanza.isChecked()
                or campo_oscura_legione.isChecked()):
            QMessageBox.warning(finestra, "Nessuna fazione selezionata",
                                 "Seleziona almeno una tra Doomtrooper, Fratellanza e Oscura Legione: "
                                 "senza nessuna di queste il mazzo non avrebbe guerrieri.")
            return

        pulsante_crea_mazzo.setEnabled(False)
        pulsante_apri_mazzo_creato.setEnabled(False)
        stato_mazzo.setText("Creazione in corso…")

        kwargs = dict(
            cartella_collezioni=nome_cartella,
            numero_collezione=campo_numero_collezione.value(),
            numero_carte_min=campo_carte_min.value(),
            numero_carte_max=campo_carte_max.value(),
            espansioni=selezionate,
            doomtrooper=campo_doomtrooper.isChecked(),
            orientamento_doomtrooper=(selezionati(lista_fazioni_doomtrooper)
                                       if campo_doomtrooper.isChecked() else []),
            fratellanza=campo_fratellanza.isChecked(),
            orientamento_arte=(selezionati(lista_arti) if campo_fratellanza.isChecked() else []),
            oscura_legione=campo_oscura_legione.isChecked(),
            orientamento_apostolo=(selezionati(lista_apostoli) if campo_oscura_legione.isChecked() else []),
            orientamento_eretico=campo_eretici.isChecked(),
            orientamento_cultista=(campo_cultisti.isChecked() if campo_oscura_legione.isChecked() else False),
            verbose=True,
        )

        def completata(risultato: Dict[str, Any]) -> None:
            pulsante_crea_mazzo.setEnabled(True)
            if not risultato.get("successo"):
                stato_mazzo.setText(f"❌ {risultato.get('errore', 'Errore sconosciuto')}")
                return

            percorso_mazzo_creato["valore"] = Path(risultato["percorso_mazzo"])
            stato_mazzo.setText(
                f"✅ Mazzo creato con {risultato['numero_carte']} carte in "
                f"{risultato['percorso_mazzo']}")
            pulsante_apri_mazzo_creato.setEnabled(True)

        def fallita(messaggio: str) -> None:
            pulsante_crea_mazzo.setEnabled(True)
            stato_mazzo.setText(f"❌ Errore imprevisto: {messaggio}")

        esegui_in_background(finestra, lavori_in_corso, crea_mazzo_da_cartella_collezione_con_parametri,
                              kwargs, completata, fallita)

    def apri_mazzo_creato() -> None:
        percorso = percorso_mazzo_creato["valore"]
        if percorso is not None:
            avvia_visualizzatore(SCRIPT_VISUALIZZATORE_MAZZO, percorso)

    def apri_mazzo_esistente() -> None:
        percorso = QFileDialog.getExistingDirectory(
            finestra, "Scegli la cartella del mazzo (o una cartella che lo contiene)", str(PERCORSO_OUT))
        if not percorso:
            return
        trovati = trova_mazzi(Path(percorso))
        if not trovati:
            QMessageBox.warning(finestra, "Nessun mazzo", f"Nessun mazzo trovato in {percorso}.")
            return
        if len(trovati) == 1:
            avvia_visualizzatore(SCRIPT_VISUALIZZATORE_MAZZO, trovati[0])
            return

        nomi = [str(p.relative_to(PERCORSO_OUT)) if p.is_relative_to(PERCORSO_OUT) else str(p)
                for p in trovati]
        scelto, ok = QInputDialog.getItem(finestra, "Scegli il mazzo", "Mazzi trovati:", nomi, 0, False)
        if ok and scelto:
            avvia_visualizzatore(SCRIPT_VISUALIZZATORE_MAZZO, trovati[nomi.index(scelto)])

    pulsante_sfoglia_cartella.clicked.connect(sfoglia_cartella_collezioni)
    pulsante_crea_mazzo.clicked.connect(crea_mazzo)
    pulsante_apri_mazzo_creato.clicked.connect(apri_mazzo_creato)
    pulsante_apri_mazzo_esistente.clicked.connect(apri_mazzo_esistente)

    # ---- Assembla la finestra

    schede = QTabWidget()
    schede.addTab(scheda_collezione, "Creazione Collezione")
    schede.addTab(scheda_mazzo, "Creazione Mazzo")

    finestra.setCentralWidget(schede)
    finestra.show()
    return applicazione.exec()


# ================================================================================
# AVVIO DA RIGA DI COMANDO
# ================================================================================

def main() -> int:
    """Punto di ingresso da riga di comando."""
    return avvia_interfaccia()


if __name__ == "__main__":
    raise SystemExit(main())

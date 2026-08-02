"""
Visualizzatore grafico delle carte di un mazzo.

Legge la cartella prodotta dall'opzione 14 del menu di `Creatore_Mazzo.py`
("Crea e salva mazzo da cartella collezioni"), che ha questa struttura:

    out/<cartella_collezioni>/Collezione_Giocatore_<N>/Mazzo_Giocatore_<N>/
        mazzo_giocatore_<N>.json
        elenco_carte_mazzo_<N>.pdf
        Immagini_Mazzo_<N>/
            Guerriero/squadra/…    Guerriero/schieramento/…
            Equipaggiamento/…  Speciali/…  Arte/…  Oscura_Simmetria/…
            Fortificazioni/…   Reliquie/…  Warzone/…  Missioni/…

Uso:

    .venv/bin/python source/gui/visualizzatore_mazzo.py <cartella_mazzo>

Se il percorso non viene indicato, il modulo cerca i mazzi disponibili sotto `out/`
e ne propone l'elenco.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ordine con cui le tipologie vengono presentate nell'elenco.
ORDINE_TIPOLOGIE = [
    "Guerriero",
    "Equipaggiamento",
    "Arte",
    "Oscura Simmetria",
    "Speciale",
    "Fortificazione",
    "Reliquia",
    "Warzone",
    "Missione",
]

# La cartella immagini non usa gli stessi nomi delle chiavi del JSON.
CARTELLA_IMMAGINI_PER_TIPOLOGIA = {
    "Guerriero": "Guerriero",
    "Equipaggiamento": "Equipaggiamento",
    "Arte": "Arte",
    "Oscura Simmetria": "Oscura_Simmetria",
    "Speciale": "Speciali",
    "Fortificazione": "Fortificazioni",
    "Reliquia": "Reliquie",
    "Warzone": "Warzone",
    "Missione": "Missioni",
}

ESTENSIONI_IMMAGINE = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")


# ================================================================================
# STRATO DATI — indipendente dall'interfaccia grafica
# ================================================================================

@dataclass
class CartaMazzo:
    """Una carta del mazzo, con i dati necessari alla visualizzazione."""

    nome: str
    tipologia: str                      # Guerriero, Equipaggiamento, Speciale, …
    appartenenza: str                   # Squadra/Schieramento, oppure il sottotipo della carta
    fazione: str
    copie: int
    percorso_immagine: Optional[Path] = None
    dettagli: Dict[str, Any] = field(default_factory=dict)

    def chiave_ordinamento(self) -> tuple:
        """Ordina per posizione della tipologia e poi per nome."""
        posizione = (ORDINE_TIPOLOGIE.index(self.tipologia)
                     if self.tipologia in ORDINE_TIPOLOGIE else len(ORDINE_TIPOLOGIE))
        return (posizione, self.nome.lower())


def _formatta_fazioni(utilizzatori: Any) -> str:
    """
    Rende leggibile il campo `utilizzatori` delle carte di supporto.

    Nel JSON le fazioni sono serializzate come "Fazione.GENERICA": qui si
    riportano al nome leggibile ("Generica").

    Args:
        utilizzatori: Valore del campo `utilizzatori`

    Returns:
        Le fazioni separate da virgola, o "—" se il campo è assente
    """
    if not utilizzatori:
        return "—"

    if isinstance(utilizzatori, str):
        utilizzatori = [utilizzatori]

    nomi = []
    for voce in utilizzatori:
        testo = str(voce)
        if "." in testo:
            testo = testo.rsplit(".", 1)[1]
        nomi.append(testo.replace("_", " ").title())

    return ", ".join(nomi)


def trova_immagine(cartella_immagini: Path, tipologia: str, nome_carta: str,
                   sottocartella: str = "") -> Optional[Path]:
    """
    Individua il file immagine di una carta.

    La convenzione dei nomi file è quella di `ottieni_nome_file_immagine`
    (spazi sostituiti da underscore), ma la ricerca è tollerante rispetto a
    maiuscole/minuscole e all'estensione, perché i file provengono da fonti diverse.

    Args:
        cartella_immagini: Cartella `Immagini_Mazzo_<N>` del mazzo
        tipologia: Tipologia della carta (chiave di CARTELLA_IMMAGINI_PER_TIPOLOGIA)
        nome_carta: Nome della carta
        sottocartella: Eventuale sottocartella (per i Guerrieri: "squadra"/"schieramento")

    Returns:
        Il percorso dell'immagine, oppure None se non trovata
    """
    cartella = cartella_immagini / CARTELLA_IMMAGINI_PER_TIPOLOGIA.get(tipologia, tipologia)
    if sottocartella:
        cartella = cartella / sottocartella

    if not cartella.is_dir():
        return None

    atteso = nome_carta.replace(" ", "_").lower()

    for percorso in cartella.iterdir():
        if percorso.is_file() and percorso.stem.lower() == atteso:
            return percorso

    # Ripiego: alcune immagini possono trovarsi nella cartella della tipologia
    # anche quando è prevista una sottocartella.
    if sottocartella:
        return trova_immagine(cartella_immagini, tipologia, nome_carta)

    return None


def carica_mazzo(cartella_mazzo: Path) -> tuple[List[CartaMazzo], Dict[str, Any]]:
    """
    Carica le carte di un mazzo dalla sua cartella.

    Args:
        cartella_mazzo: Cartella `Mazzo_Giocatore_<N>`

    Returns:
        La lista delle carte ordinata per tipologia e nome, e i metadati del mazzo

    Raises:
        FileNotFoundError: se la cartella non contiene il JSON del mazzo
    """
    file_json = next(iter(sorted(cartella_mazzo.glob("mazzo_giocatore_*.json"))), None)
    if file_json is None:
        raise FileNotFoundError(
            f"Nessun file 'mazzo_giocatore_*.json' in {cartella_mazzo}. "
            "Indicare la cartella 'Mazzo_Giocatore_<N>' prodotta dall'opzione 14."
        )

    dati = json.loads(file_json.read_text(encoding="utf-8"))
    mazzo = dati.get("mazzo", {})

    cartella_immagini = next(iter(sorted(cartella_mazzo.glob("Immagini_Mazzo_*"))), None)

    carte: List[CartaMazzo] = []

    # Guerrieri: raggruppati per area e poi per fazione
    for area, fazioni in (mazzo.get("inventario_guerrieri") or {}).items():
        for fazione, elenco in (fazioni or {}).items():
            for nome, info in (elenco or {}).items():
                carte.append(CartaMazzo(
                    nome=nome,
                    tipologia="Guerriero",
                    appartenenza=area.capitalize(),
                    fazione=info.get("fazione") or fazione,
                    copie=int(info.get("copie", 0)),
                    percorso_immagine=(trova_immagine(cartella_immagini, "Guerriero", nome, area)
                                       if cartella_immagini else None),
                    dettagli=info,
                ))

    # Carte di supporto: raggruppate per tipologia
    for tipologia, elenco in (mazzo.get("inventario_supporto") or {}).items():
        for nome, info in (elenco or {}).items():
            # `tipo` è il sottotipo della carta ("Arma da Fuoco", "Città Corporazione"…).
            # Per alcune tipologie coincide col nome della tipologia stessa: in quel caso
            # ripeterlo nella colonna non aggiunge nulla.
            sottotipo = str(info.get("tipo") or info.get("classe") or "").strip()
            if not sottotipo or sottotipo.lower() == tipologia.lower():
                sottotipo = "—"

            carte.append(CartaMazzo(
                nome=nome,
                tipologia=tipologia,
                appartenenza=sottotipo,
                fazione=_formatta_fazioni(info.get("utilizzatori")),
                copie=int(info.get("copie", 0)),
                percorso_immagine=(trova_immagine(cartella_immagini, tipologia, nome)
                                   if cartella_immagini else None),
                dettagli=info,
            ))

    carte.sort(key=CartaMazzo.chiave_ordinamento)
    return carte, mazzo.get("metadati_mazzo", {})


def raggruppa_per_tipologia(carte: List[CartaMazzo]) -> Dict[str, List[CartaMazzo]]:
    """
    Raggruppa le carte per tipologia, conservando l'ordine di ORDINE_TIPOLOGIE.

    Args:
        carte: Lista di carte già ordinata

    Returns:
        Dizionario tipologia -> carte, con le tipologie vuote escluse
    """
    gruppi: Dict[str, List[CartaMazzo]] = {}
    for carta in carte:
        gruppi.setdefault(carta.tipologia, []).append(carta)
    return gruppi


def cerca_mazzi_disponibili(radice: Path) -> List[Path]:
    """
    Elenca le cartelle di mazzo presenti sotto una radice.

    Args:
        radice: Tipicamente la cartella `out/`

    Returns:
        Le cartelle `Mazzo_Giocatore_<N>` trovate, ordinate
    """
    if not radice.is_dir():
        return []
    return sorted(p for p in radice.glob("*/*/Mazzo_Giocatore_*") if p.is_dir())


# ================================================================================
# INTERFACCIA GRAFICA
# ================================================================================

def avvia_interfaccia(cartella_mazzo: Path) -> int:
    """
    Apre la finestra di visualizzazione del mazzo.

    Args:
        cartella_mazzo: Cartella `Mazzo_Giocatore_<N>`

    Returns:
        Il codice di uscita dell'applicazione
    """
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QFontMetrics, QImageReader, QPixmap
        from PySide6.QtWidgets import (
            QAbstractItemView, QApplication, QFrame, QHBoxLayout, QHeaderView, QLabel,
            QMainWindow, QScrollArea, QSizePolicy, QSplitter, QTreeWidget,
            QTreeWidgetItem, QVBoxLayout, QWidget,
        )
    except ImportError:
        print("PySide6 non è installato. Installalo nell'ambiente del progetto con:\n"
              "    .venv/bin/pip install PySide6-Essentials", file=sys.stderr)
        return 1

    carte, metadati = carica_mazzo(cartella_mazzo)
    gruppi = raggruppa_per_tipologia(carte)

    # Riusa l'istanza esistente se c'è: Qt ne ammette una sola per processo, e questo
    # permette di aprire la finestra anche da un contesto che ha già avviato Qt.
    applicazione = QApplication.instance() or QApplication(sys.argv)

    finestra = QMainWindow()
    numero = metadati.get("indice", "?")
    copie_totali = sum(c.copie for c in carte)
    finestra.setWindowTitle(
        f"Visualizzatore Mazzo — Giocatore {numero}  "
        f"({len(carte)} carte distinte, {copie_totali} copie)"
    )
    finestra.resize(1100, 720)

    def leggi_pixmap(percorso: Path) -> QPixmap:
        """
        Carica l'immagine di una carta applicandone l'orientamento EXIF.

        Alcune scansioni (7 carte Cybertronic e la Valkiria, nel materiale attuale)
        hanno i pixel memorizzati in orizzontale e un tag EXIF `Orientation` che ne
        dichiara la rotazione. Gli editor di immagini lo applicano; `QPixmap(percorso)`
        no, e la carta apparirebbe coricata. QImageReader.setAutoTransform applica
        esattamente la trasformazione dichiarata, senza toccare le carte che sono
        davvero in formato orizzontale (diverse Fortificazioni) e che non hanno il tag.

        Args:
            percorso: Percorso del file immagine

        Returns:
            Il pixmap orientato correttamente, nullo se l'immagine non è leggibile
        """
        lettore = QImageReader(str(percorso))
        lettore.setAutoTransform(True)
        immagine = lettore.read()
        return QPixmap.fromImage(immagine) if not immagine.isNull() else QPixmap()

    class EtichettaImmagine(QLabel):
        """
        Etichetta che mostra l'immagine della carta adattandola allo spazio disponibile.

        Conserva il pixmap originale e lo riscala a ogni ridimensionamento, senza mai
        far dipendere il proprio `sizeHint` dall'immagine: diversamente, impostare un
        pixmap più grande propagherebbe una richiesta di ingrandimento fino alla
        finestra. Con la finestra massimizzata quella richiesta non può essere
        soddisfatta e su Wayland produce un errore di protocollo
        ("xdg_surface buffer does not match the configured maximized state").
        """

        def __init__(self) -> None:
            super().__init__()
            self._originale = QPixmap()
            self.setMinimumSize(1, 1)
            self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        def imposta_immagine(self, pixmap: Optional[QPixmap]) -> None:
            """Imposta l'immagine da mostrare (None o pixmap nullo per svuotare)."""
            self._originale = pixmap if pixmap is not None else QPixmap()
            self._ridisegna()

        def resizeEvent(self, evento) -> None:      # noqa: N802 (nome imposto da Qt)
            super().resizeEvent(evento)
            self._ridisegna()

        def _ridisegna(self) -> None:
            if self._originale.isNull():
                super().setPixmap(QPixmap())
                return
            super().setPixmap(self._originale.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            ))

    # ---- Elenco delle carte, raggruppato per tipologia.
    # Appartenenza e fazione non compaiono come colonne: sono riportate nel pannello
    # di dettaglio sotto l'immagine, e toglierle lascia più spazio ai nomi delle carte.
    elenco = QTreeWidget()
    elenco.setColumnCount(2)
    elenco.setHeaderLabels(["Carta", "Copie"])
    elenco.setAlternatingRowColors(True)
    elenco.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    elenco.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    intestazione = elenco.header()
    # setStretchLastSection è attivo per impostazione predefinita e fa allargare l'ultima
    # colonna a tutto lo spazio residuo, ignorando la modalità di ridimensionamento: senza
    # disattivarlo la colonna delle copie occupa centinaia di pixel invece dei ~50 che servono.
    intestazione.setStretchLastSection(False)
    intestazione.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    intestazione.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)

    metriche = QFontMetrics(elenco.font())
    larghezza_copie = max(metriche.horizontalAdvance("999"),
                          metriche.horizontalAdvance("Copie")) + 24   # margini e spaziatura
    elenco.setColumnWidth(1, larghezza_copie)

    primo_elemento: Optional[QTreeWidgetItem] = None

    for tipologia in [t for t in ORDINE_TIPOLOGIE if t in gruppi] + \
                     [t for t in gruppi if t not in ORDINE_TIPOLOGIE]:
        carte_gruppo = gruppi[tipologia]
        copie_totali = sum(c.copie for c in carte_gruppo)
        nodo = QTreeWidgetItem(elenco, [f"{tipologia.upper()}  ({len(carte_gruppo)} carte, {copie_totali} copie)"])
        nodo.setFirstColumnSpanned(True)
        nodo.setExpanded(True)

        for carta in carte_gruppo:
            figlio = QTreeWidgetItem(nodo, [carta.nome, str(carta.copie)])
            figlio.setData(0, Qt.ItemDataRole.UserRole, carta)
            figlio.setTextAlignment(1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if primo_elemento is None:
                primo_elemento = figlio

    # ---- Pannello di dettaglio, con l'immagine della carta
    immagine = EtichettaImmagine()
    immagine.setStyleSheet("border: 1px solid palette(mid); background: palette(base);")

    dettaglio = QLabel()
    dettaglio.setTextFormat(Qt.TextFormat.RichText)
    dettaglio.setWordWrap(True)
    dettaglio.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    # Il testo del dettaglio cambia lunghezza da una carta all'altra (i nomi e gli
    # elenchi di fazioni possono andare a capo più volte). Racchiuderlo in un'area
    # scorrevole di altezza fissa fa sì che le dimensioni richieste dalla finestra
    # restino costanti durante lo scorrimento dell'elenco, senza però troncare il testo.
    area_dettaglio = QScrollArea()
    area_dettaglio.setWidget(dettaglio)
    area_dettaglio.setWidgetResizable(True)
    area_dettaglio.setFrameShape(QFrame.Shape.NoFrame)
    area_dettaglio.setFixedHeight(170)
    area_dettaglio.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)

    pannello = QWidget()
    disposizione_pannello = QVBoxLayout(pannello)
    disposizione_pannello.addWidget(immagine, stretch=1)
    disposizione_pannello.addWidget(area_dettaglio)

    def mostra_carta(elemento: Optional[QTreeWidgetItem], _precedente=None) -> None:
        """Aggiorna immagine e dettagli in base alla carta selezionata."""
        carta = elemento.data(0, Qt.ItemDataRole.UserRole) if elemento is not None else None

        if carta is None:                       # nodo di tipologia: nessun dettaglio
            immagine.imposta_immagine(None)
            immagine.setText("Seleziona una carta")
            dettaglio.setText("")
            return

        dettaglio.setText(
            f"<b style='font-size:14pt'>{carta.nome}</b><br><br>"
            f"<b>Tipologia:</b> {carta.tipologia}<br>"
            f"<b>Appartenenza:</b> {carta.appartenenza}<br>"
            f"<b>Fazione:</b> {carta.fazione}<br>"
            f"<b>Copie nel mazzo:</b> {carta.copie}<br>"
            f"<b>Espansione:</b> {carta.dettagli.get('set_espansione', '—')}<br>"
            f"<b>Rarità:</b> {carta.dettagli.get('rarity', '—')}"
        )

        if carta.percorso_immagine and carta.percorso_immagine.is_file():
            pixmap = leggi_pixmap(carta.percorso_immagine)
            if not pixmap.isNull():
                immagine.imposta_immagine(pixmap)
                return

        immagine.imposta_immagine(None)
        immagine.setText("Immagine non disponibile")

    elenco.currentItemChanged.connect(mostra_carta)

    divisore = QSplitter(Qt.Orientation.Horizontal)
    divisore.addWidget(elenco)
    divisore.addWidget(pannello)
    divisore.setStretchFactor(0, 3)
    divisore.setStretchFactor(1, 2)

    contenitore = QWidget()
    disposizione = QHBoxLayout(contenitore)
    disposizione.addWidget(divisore)
    finestra.setCentralWidget(contenitore)

    # Il fuoco sull'elenco fa sì che i tasti freccia funzionino subito,
    # senza dover prima cliccare sulla lista.
    if primo_elemento is not None:
        elenco.setCurrentItem(primo_elemento)
    elenco.setFocus()

    finestra.show()
    return applicazione.exec()


# ================================================================================
# AVVIO DA RIGA DI COMANDO
# ================================================================================

def main(argomenti: Optional[List[str]] = None) -> int:
    """
    Punto di ingresso da riga di comando.

    Args:
        argomenti: Argomenti (per default quelli passati al processo)

    Returns:
        Il codice di uscita
    """
    argomenti = sys.argv[1:] if argomenti is None else argomenti

    if argomenti:
        cartella = Path(argomenti[0]).expanduser()
        if not cartella.is_dir():
            print(f"Cartella non trovata: {cartella}", file=sys.stderr)
            return 1
        return avvia_interfaccia(cartella)

    radice = Path(__file__).resolve().parents[2] / "out"
    disponibili = cerca_mazzi_disponibili(radice)

    if not disponibili:
        print(f"Nessun mazzo trovato sotto {radice}.\n"
              "Crea prima un mazzo con l'opzione 14 di Creatore_Mazzo.py, oppure indica "
              "la cartella del mazzo:\n"
              "    .venv/bin/python source/gui/visualizzatore_mazzo.py <cartella_mazzo>",
              file=sys.stderr)
        return 1

    if len(disponibili) == 1:
        return avvia_interfaccia(disponibili[0])

    print("Mazzi disponibili:")
    for indice, percorso in enumerate(disponibili, 1):
        print(f"  {indice}. {percorso}")

    try:
        scelta = int(input("\nNumero del mazzo da visualizzare: "))
        return avvia_interfaccia(disponibili[scelta - 1])
    except (ValueError, IndexError):
        print("Scelta non valida.", file=sys.stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        return 130


if __name__ == "__main__":
    raise SystemExit(main())

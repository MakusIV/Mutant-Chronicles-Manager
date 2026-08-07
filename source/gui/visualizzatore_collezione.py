"""
Visualizzatore grafico delle carte di una collezione.

Legge le cartelle prodotte da `Creatore_Collezione.py`, che hanno questa struttura:

    out/Collezioni_<data>_<ora>/
        lista_collezioni.json
        Collezione_Giocatore_<N>/
            collezione_giocatore_<N>.json
            elenco_carte_giocatore_<N>.pdf
            Immagini/
                Guerriero/…  Equipaggiamento/…  Speciali/…  Arte/…
                Oscura_Simmetria/…  Fortificazioni/…  Reliquie/…  Warzone/…  Missioni/…
            Mazzo_Giocatore_<N>/        ← ignorata: la mostra visualizzatore_mazzo.py

Uso:

    .venv/bin/python source/gui/visualizzatore_collezione.py [cartella]

Il percorso può essere la cartella di una singola collezione (`Collezione_Giocatore_<N>`)
oppure quella che le raccoglie (`Collezioni_<data>`): nel secondo caso le collezioni dei
vari giocatori si scelgono da un menu a tendina nella finestra. Senza argomenti il modulo
cerca le collezioni disponibili sotto `out/`.

Rispetto a un mazzo una collezione è molto più ampia — nell'ordine delle centinaia di
carte distinte — quindi la finestra offre una casella di ricerca per nome, che il
visualizzatore dei mazzi non ha.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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

# Le chiavi del JSON sono minuscole e con underscore: qui diventano leggibili.
TIPOLOGIA_PER_CHIAVE = {
    "guerriero": "Guerriero",
    "equipaggiamento": "Equipaggiamento",
    "arte": "Arte",
    "oscura_simmetria": "Oscura Simmetria",
    "speciale": "Speciale",
    "fortificazione": "Fortificazione",
    "reliquia": "Reliquia",
    "warzone": "Warzone",
    "missione": "Missione",
}

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

# Le cinque Megacorporazioni, più le altre affiliazioni che compaiono come sotto-categoria.
CORPORAZIONI = ("Bauhaus", "Capitol", "Cybertronic", "Imperiale", "Mishima")

# Insieme delle fazioni considerate Doomtrooper (regolamento §6): quando una carta le
# abilita tutte, la sotto-categoria diventa "Doomtrooper" invece dell'elenco per esteso.
FAZIONI_DOOMTROOPER = frozenset(CORPORAZIONI) | {"Fratellanza", "Mercenario"}

SOTTOCATEGORIA_ASSENTE = "Non specificata"


# ================================================================================
# STRATO DATI — indipendente dall'interfaccia grafica
# ================================================================================

@dataclass
class CartaCollezione:
    """Una carta della collezione, con i dati necessari alla visualizzazione."""

    nome: str
    tipologia: str                      # Guerriero, Equipaggiamento, Speciale, …
    sottocategoria: str                 # Fazione, disciplina, apostolo… secondo la tipologia
    copie: int
    disciplina: str = ""                # solo per le carte Arte
    percorso_immagine: Optional[Path] = None
    dettagli: Dict[str, Any] = field(default_factory=dict)

    def chiave_ordinamento(self) -> tuple:
        """Ordina per tipologia, poi per sotto-categoria e infine per nome."""
        posizione = (ORDINE_TIPOLOGIE.index(self.tipologia)
                     if self.tipologia in ORDINE_TIPOLOGIE else len(ORDINE_TIPOLOGIE))
        # Le carte senza sotto-categoria vanno in fondo al proprio gruppo
        assente = self.sottocategoria == SOTTOCATEGORIA_ASSENTE
        return (posizione, assente, self.sottocategoria.lower(), self.nome.lower())


@dataclass
class Collezione:
    """Una collezione caricata, con i propri metadati."""

    giocatore: Any
    cartella: Path
    carte: List[CartaCollezione]
    orientamento: List[str]
    totali: Dict[str, Any]

    @property
    def copie_totali(self) -> int:
        return sum(c.copie for c in self.carte)


def _nomi_fazioni(fazioni_permesse: Any) -> List[str]:
    """
    Estrae i nomi leggibili delle fazioni dal campo `fazioni_permesse`.

    Nel JSON delle collezioni il campo è già una stringa leggibile con le fazioni
    separate da virgola ("Bauhaus, Mishima, …"), ma può arrivare anche come lista, o
    con la forma serializzata "Fazione.GENERICA" usata altrove nel progetto: sono
    gestite tutte, perché il costo è un paio di righe e il chiamante non deve saperlo.

    Args:
        fazioni_permesse: Valore del campo

    Returns:
        I nomi delle fazioni, ordinati e senza ripetizioni
    """
    if not fazioni_permesse:
        return []

    if isinstance(fazioni_permesse, str):
        voci = fazioni_permesse.split(",")
    else:
        voci = list(fazioni_permesse)

    nomi = []
    for voce in voci:
        testo = str(voce).strip()
        if not testo:
            continue
        if "." in testo and testo.split(".")[0] == "Fazione":
            testo = testo.rsplit(".", 1)[1].replace("_", " ").title()
        nomi.append(testo)
    return sorted(set(nomi))


def sottocategoria(tipologia: str, info: Dict[str, Any]) -> str:
    """
    Determina la sotto-categoria di una carta.

    Il criterio cambia con la tipologia:

    - **Guerriero** ed **Equipaggiamento**: la fazione dichiarata dalla carta.
    - **Arte**: la disciplina dell'incantesimo (Mentale, Cinetica, …).
    - **Oscura Simmetria**: l'Apostolo che concede il Dono, quando la carta ne dichiara uno.
    - **le altre**: la fazione abilitata all'uso, ricavata da `fazioni_permesse`. "Tutte"
      per le carte generiche, "Doomtrooper" quando sono abilitate tutte le fazioni
      Doomtrooper, altrimenti l'elenco delle fazioni.

    Args:
        tipologia: Tipologia della carta
        info: Il dizionario della carta letto dal JSON della collezione

    Returns:
        La sotto-categoria, o SOTTOCATEGORIA_ASSENTE se non ricavabile
    """
    if tipologia == "Arte":
        return str(info.get("disciplina") or "").strip() or SOTTOCATEGORIA_ASSENTE

    if tipologia == "Oscura Simmetria":
        apostolo = info.get("apostolo_padre") or info.get("apostolo")
        nome_apostolo = str(getattr(apostolo, "value", apostolo) or "").strip()
        if nome_apostolo and nome_apostolo.lower() not in ("none", "nessuno"):
            return nome_apostolo
        # Senza Apostolo il Dono è generico: viene dall'Oscura Simmetria in quanto tale
        return "Oscura Simmetria"

    # Guerriero ed Equipaggiamento dichiarano la propria fazione direttamente, le altre
    # tipologie l'elenco delle fazioni abilitate: le due forme passano dalla stessa
    # normalizzazione, altrimenti la medesima carta finirebbe sotto "Generica" o sotto
    # "Tutte" a seconda del campo da cui è stata letta.
    fazioni = _nomi_fazioni(info.get("fazione") or info.get("fazioni_permesse"))
    if not fazioni:
        return SOTTOCATEGORIA_ASSENTE
    if fazioni in (["Generica"], ["Tutte"]):
        return "Tutte"
    if set(fazioni) >= FAZIONI_DOOMTROOPER:
        return "Doomtrooper"
    # Il plurale vale per le carte, che sono *utilizzabili dai* Mercenari; un guerriero
    # invece *è* Mercenario, e va lasciato al singolare come le altre affiliazioni.
    if fazioni == ["Mercenario"] and tipologia != "Guerriero":
        return "Mercenari"
    return ", ".join(fazioni)


def trova_immagine(cartella_immagini: Path, tipologia: str, nome_carta: str) -> Optional[Path]:
    """
    Individua il file immagine di una carta.

    La convenzione dei nomi file è quella di `ottieni_nome_file_immagine` (spazi
    sostituiti da underscore), ma la ricerca è tollerante rispetto a maiuscole/minuscole
    e all'estensione, perché i file provengono da fonti diverse.

    Args:
        cartella_immagini: Cartella `Immagini` della collezione
        tipologia: Tipologia della carta (chiave di CARTELLA_IMMAGINI_PER_TIPOLOGIA)
        nome_carta: Nome della carta

    Returns:
        Il percorso dell'immagine, oppure None se non trovata
    """
    cartella = cartella_immagini / CARTELLA_IMMAGINI_PER_TIPOLOGIA.get(tipologia, tipologia)
    if not cartella.is_dir():
        return None

    atteso = nome_carta.replace(" ", "_").lower()
    for percorso in cartella.iterdir():
        if percorso.is_file() and percorso.stem.lower() == atteso:
            return percorso
    return None


def _file_json_collezione(cartella: Path) -> Optional[Path]:
    """Il JSON della collezione dentro una cartella `Collezione_Giocatore_<N>`."""
    candidati = sorted(cartella.glob("collezione_giocatore_*.json"))
    return candidati[0] if candidati else None


def carica_collezione(cartella: Path) -> Collezione:
    """
    Carica le carte di una collezione dalla sua cartella.

    Args:
        cartella: Cartella `Collezione_Giocatore_<N>`

    Returns:
        La collezione, con le carte già ordinate

    Raises:
        FileNotFoundError: se la cartella non contiene il JSON della collezione
    """
    percorso_json = _file_json_collezione(cartella)
    if percorso_json is None:
        raise FileNotFoundError(
            f"Nessun file collezione_giocatore_*.json in {cartella}")

    with percorso_json.open(encoding="utf-8") as sorgente:
        documento = json.load(sorgente)

    dati = documento.get("collezione", documento)
    cartella_immagini = cartella / "Immagini"

    carte: List[CartaCollezione] = []
    for chiave, blocco in (dati.get("carte_per_tipo") or {}).items():
        tipologia = TIPOLOGIA_PER_CHIAVE.get(chiave, chiave.replace("_", " ").title())

        for nome, info in (blocco.get("dettaglio_carte") or {}).items():
            # `dettaglio_carte` può contenere il dizionario completo della carta oppure
            # il solo numero di copie, secondo la versione che ha prodotto il file.
            if not isinstance(info, dict):
                info = {"nome": nome, "quantita": info}

            carte.append(CartaCollezione(
                nome=info.get("nome") or nome,
                tipologia=tipologia,
                sottocategoria=sottocategoria(tipologia, info),
                copie=int(info.get("quantita") or 0),
                disciplina=str(info.get("disciplina") or ""),
                percorso_immagine=trova_immagine(cartella_immagini, tipologia, nome),
                dettagli=info,
            ))

    carte.sort(key=CartaCollezione.chiave_ordinamento)

    orientamento = dati.get("orientamento") or {}
    return Collezione(
        giocatore=dati.get("id_giocatore",
                           documento.get("metadata", {}).get("id_giocatore", "?")),
        cartella=cartella,
        carte=carte,
        orientamento=list(orientamento.get("fazioni") or []),
        totali=dati.get("totali") or {},
    )


def raggruppa_per_tipologia(
        carte: List[CartaCollezione]) -> Dict[str, List[CartaCollezione]]:
    """
    Raggruppa le carte per tipologia, conservando l'ordine di ORDINE_TIPOLOGIE.

    Args:
        carte: Lista di carte già ordinata

    Returns:
        Dizionario tipologia -> carte, con le tipologie vuote escluse
    """
    gruppi: Dict[str, List[CartaCollezione]] = {}
    for carta in carte:
        gruppi.setdefault(carta.tipologia, []).append(carta)
    return gruppi


def cerca_collezioni(percorso: Path) -> List[Path]:
    """
    Elenca le cartelle di collezione a partire da un percorso.

    Accetta indifferentemente la cartella di una singola collezione, quella che le
    raccoglie, o la radice `out/`.

    Args:
        percorso: Cartella da cui partire

    Returns:
        Le cartelle `Collezione_Giocatore_<N>` trovate, ordinate
    """
    if not percorso.is_dir():
        return []

    # Già una singola collezione
    if _file_json_collezione(percorso) is not None:
        return [percorso]

    trovate = sorted(p for p in percorso.glob("Collezione_Giocatore_*")
                     if p.is_dir() and _file_json_collezione(p) is not None)
    if trovate:
        return trovate

    # Radice `out/`: le collezioni stanno un livello più sotto
    return sorted(p for p in percorso.glob("*/Collezione_Giocatore_*")
                  if p.is_dir() and _file_json_collezione(p) is not None)


# ================================================================================
# INTERFACCIA GRAFICA
# ================================================================================

def avvia_interfaccia(cartelle: List[Path]) -> int:
    """
    Apre la finestra di consultazione delle collezioni.

    Args:
        cartelle: Cartelle `Collezione_Giocatore_<N>` da rendere consultabili

    Returns:
        Il codice di uscita dell'applicazione
    """
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QImageReader, QPixmap
        from PySide6.QtWidgets import (
            QAbstractItemView, QApplication, QComboBox, QFrame, QHBoxLayout,
            QHeaderView, QLabel, QLineEdit, QMainWindow, QScrollArea, QSizePolicy,
            QSplitter, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,
        )
    except ImportError:
        print("PySide6 non è installato. Installalo nell'ambiente del progetto con:\n"
              "    .venv/bin/pip install PySide6-Essentials", file=sys.stderr)
        return 1

    collezioni = [carica_collezione(c) for c in cartelle]
    if not collezioni:
        print("Nessuna collezione da mostrare.", file=sys.stderr)
        return 1

    # Riusa l'istanza esistente se c'è: Qt ne ammette una sola per processo, e questo
    # permette di aprire la finestra anche da un contesto che ha già avviato Qt.
    applicazione = QApplication.instance() or QApplication(sys.argv)

    finestra = QMainWindow()
    finestra.resize(1150, 760)

    def leggi_pixmap(percorso: Path) -> QPixmap:
        """
        Carica l'immagine di una carta applicandone l'orientamento EXIF.

        Alcune scansioni hanno i pixel memorizzati in orizzontale e un tag EXIF
        `Orientation` che ne dichiara la rotazione. Gli editor di immagini lo applicano;
        `QPixmap(percorso)` no, e la carta apparirebbe coricata.
        `QImageReader.setAutoTransform` applica esattamente la trasformazione dichiarata,
        senza toccare le carte che sono davvero in formato orizzontale (diverse
        Fortificazioni) e che non hanno il tag.

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

    # ---- Barra superiore: scelta della collezione e ricerca per nome
    scelta_collezione = QComboBox()
    for collezione in collezioni:
        scelta_collezione.addItem(
            f"Giocatore {collezione.giocatore}  "
            f"({len(collezione.carte)} carte distinte, {collezione.copie_totali} copie)")
    scelta_collezione.setVisible(len(collezioni) > 1)

    ricerca = QLineEdit()
    ricerca.setPlaceholderText("Cerca una carta per nome…")
    ricerca.setClearButtonEnabled(True)

    barra = QWidget()
    disposizione_barra = QHBoxLayout(barra)
    disposizione_barra.setContentsMargins(0, 0, 0, 0)
    if len(collezioni) > 1:
        disposizione_barra.addWidget(QLabel("Collezione:"))
        disposizione_barra.addWidget(scelta_collezione, stretch=1)
    disposizione_barra.addWidget(ricerca, stretch=2)

    # ---- Elenco delle carte, raggruppato per tipologia e sotto-categoria
    elenco = QTreeWidget()
    elenco.setColumnCount(1)
    elenco.setHeaderLabels(["Carta"])
    elenco.setAlternatingRowColors(True)
    elenco.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    elenco.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    intestazione = elenco.header()
    intestazione.setStretchLastSection(True)
    intestazione.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

    # ---- Pannello di dettaglio, con l'immagine della carta
    immagine = EtichettaImmagine()
    immagine.setStyleSheet("border: 1px solid palette(mid); background: palette(base);")

    dettaglio = QLabel()
    dettaglio.setTextFormat(Qt.TextFormat.RichText)
    dettaglio.setWordWrap(True)
    dettaglio.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    # Il testo del dettaglio cambia lunghezza da una carta all'altra — qui c'è anche il
    # testo di regolamento, che per certe carte è lungo diverse righe. Racchiuderlo in
    # un'area scorrevole di altezza fissa fa sì che le dimensioni richieste dalla finestra
    # restino costanti durante lo scorrimento dell'elenco, senza però troncare il testo.
    area_dettaglio = QScrollArea()
    area_dettaglio.setWidget(dettaglio)
    area_dettaglio.setWidgetResizable(True)
    area_dettaglio.setFrameShape(QFrame.Shape.NoFrame)
    area_dettaglio.setFixedHeight(210)
    area_dettaglio.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)

    pannello = QWidget()
    disposizione_pannello = QVBoxLayout(pannello)
    disposizione_pannello.addWidget(immagine, stretch=1)
    disposizione_pannello.addWidget(area_dettaglio)

    def mostra_carta(elemento: Optional[QTreeWidgetItem], _precedente=None) -> None:
        """Aggiorna immagine e dettagli in base alla carta selezionata."""
        carta = elemento.data(0, Qt.ItemDataRole.UserRole) if elemento is not None else None

        if carta is None:                       # nodo di raggruppamento: nessun dettaglio
            immagine.imposta_immagine(None)
            immagine.setText("Seleziona una carta")
            dettaglio.setText("")
            return

        # La disciplina compare solo dove ha senso, cioè sulle carte Arte. Per quelle carte
        # la sotto-categoria è la disciplina stessa: mostrarle entrambe sarebbe una ripetizione.
        riga_disciplina = f"<b>Disciplina:</b> {carta.disciplina}<br>" if carta.disciplina else ""
        riga_categoria = ("" if carta.disciplina == carta.sottocategoria
                          else f"<b>Categoria:</b> {carta.sottocategoria}<br>")

        testo_carta = str(carta.dettagli.get("testo_carta") or "").strip()
        blocco_testo = (f"<br><div style='margin-top:6px'>{testo_carta}</div>"
                        if testo_carta else "")

        dettaglio.setText(
            f"<b style='font-size:14pt'>{carta.nome}</b><br><br>"
            f"<b>Tipologia:</b> {carta.tipologia}<br>"
            f"{riga_categoria}"
            f"{riga_disciplina}"
            f"<b>Copie nella collezione:</b> {carta.copie}<br>"
            f"<b>Espansione:</b> {carta.dettagli.get('set_espansione', '—')}<br>"
            f"<b>Rarità:</b> {carta.dettagli.get('rarity', '—')}<br>"
            f"<b>Valore strategico:</b> {carta.dettagli.get('valore_strategico', '—')}<br>"
            f"<b>Fondamentale:</b> {'Sì' if carta.dettagli.get('fondamentale') else 'No'}"
            f"{blocco_testo}"
        )

        if carta.percorso_immagine and carta.percorso_immagine.is_file():
            pixmap = leggi_pixmap(carta.percorso_immagine)
            if not pixmap.isNull():
                immagine.imposta_immagine(pixmap)
                return

        immagine.imposta_immagine(None)
        immagine.setText("Immagine non disponibile")

    def popola(indice: int) -> None:
        """Riempie l'elenco con le carte della collezione scelta."""
        collezione = collezioni[indice]
        gruppi = raggruppa_per_tipologia(collezione.carte)

        elenco.clear()
        primo_elemento: Optional[QTreeWidgetItem] = None

        for tipologia in ([t for t in ORDINE_TIPOLOGIE if t in gruppi]
                          + [t for t in gruppi if t not in ORDINE_TIPOLOGIE]):
            carte_gruppo = gruppi[tipologia]
            copie_gruppo = sum(c.copie for c in carte_gruppo)
            nodo = QTreeWidgetItem(
                elenco,
                [f"{tipologia.upper()}  ({len(carte_gruppo)} carte, {copie_gruppo} copie)"])
            nodo.setFirstColumnSpanned(True)
            nodo.setExpanded(True)

            # Secondo livello: la sotto-categoria, il cui significato dipende dalla tipologia
            # (fazione per guerrieri ed equipaggiamento, disciplina per l'Arte, Apostolo
            # concedente per l'Oscura Simmetria, fazioni abilitate per le altre).
            sottogruppi: Dict[str, List[CartaCollezione]] = {}
            for carta in carte_gruppo:
                sottogruppi.setdefault(carta.sottocategoria, []).append(carta)

            for nome_sotto, carte_sotto in sottogruppi.items():
                copie_sotto = sum(c.copie for c in carte_sotto)
                nodo_sotto = QTreeWidgetItem(
                    nodo, [f"{nome_sotto}  ({len(carte_sotto)} carte, {copie_sotto} copie)"])
                nodo_sotto.setFirstColumnSpanned(True)
                nodo_sotto.setExpanded(True)

                for carta in carte_sotto:
                    figlio = QTreeWidgetItem(nodo_sotto, [carta.nome])
                    figlio.setData(0, Qt.ItemDataRole.UserRole, carta)
                    if primo_elemento is None:
                        primo_elemento = figlio

        orientamento = ", ".join(collezione.orientamento) or "nessuno"
        finestra.setWindowTitle(
            f"Visualizzatore Collezione — Giocatore {collezione.giocatore}  "
            f"({len(collezione.carte)} carte distinte, {collezione.copie_totali} copie; "
            f"orientamento: {orientamento})")

        applica_ricerca(ricerca.text())
        if primo_elemento is not None and not primo_elemento.isHidden():
            elenco.setCurrentItem(primo_elemento)

    def applica_ricerca(testo: str) -> None:
        """
        Nasconde le carte il cui nome non contiene il testo cercato.

        I nodi di raggruppamento restano visibili solo se conservano almeno una carta,
        così l'albero non si riempie di intestazioni vuote.
        """
        cercato = testo.strip().lower()

        for indice_tipologia in range(elenco.topLevelItemCount()):
            nodo = elenco.topLevelItem(indice_tipologia)
            visibili_tipologia = 0

            for indice_sotto in range(nodo.childCount()):
                nodo_sotto = nodo.child(indice_sotto)
                visibili_sotto = 0

                for indice_carta in range(nodo_sotto.childCount()):
                    figlio = nodo_sotto.child(indice_carta)
                    corrisponde = not cercato or cercato in figlio.text(0).lower()
                    figlio.setHidden(not corrisponde)
                    visibili_sotto += int(corrisponde)

                nodo_sotto.setHidden(visibili_sotto == 0)
                visibili_tipologia += visibili_sotto

            nodo.setHidden(visibili_tipologia == 0)

    elenco.currentItemChanged.connect(mostra_carta)
    ricerca.textChanged.connect(applica_ricerca)
    scelta_collezione.currentIndexChanged.connect(popola)

    divisore = QSplitter(Qt.Orientation.Horizontal)
    divisore.addWidget(elenco)
    divisore.addWidget(pannello)
    divisore.setStretchFactor(0, 2)
    divisore.setStretchFactor(1, 3)

    contenitore = QWidget()
    disposizione = QVBoxLayout(contenitore)
    disposizione.addWidget(barra)
    disposizione.addWidget(divisore, stretch=1)
    finestra.setCentralWidget(contenitore)

    popola(0)

    # Il fuoco sull'elenco fa sì che i tasti freccia funzionino subito,
    # senza dover prima cliccare sulla lista.
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
        percorso = Path(argomenti[0]).expanduser()
        if not percorso.is_dir():
            print(f"Cartella non trovata: {percorso}", file=sys.stderr)
            return 1
        trovate = cerca_collezioni(percorso)
        if not trovate:
            print(f"Nessuna collezione trovata in {percorso}.", file=sys.stderr)
            return 1
        return avvia_interfaccia(trovate)

    radice = Path(__file__).resolve().parents[2] / "out"
    raccolte = sorted(p for p in radice.glob("Collezioni_*") if p.is_dir()) \
        if radice.is_dir() else []

    if not raccolte:
        print(f"Nessuna collezione trovata sotto {radice}.\n"
              "Creane una con Creatore_Collezione.py, oppure indica la cartella:\n"
              "    .venv/bin/python source/gui/visualizzatore_collezione.py <cartella>",
              file=sys.stderr)
        return 1

    if len(raccolte) == 1:
        return avvia_interfaccia(cerca_collezioni(raccolte[0]))

    print("Gruppi di collezioni disponibili:")
    for indice, percorso in enumerate(raccolte, 1):
        quante = len(cerca_collezioni(percorso))
        print(f"  {indice}. {percorso.name}  ({quante} collezioni)")

    try:
        scelta = int(input("\nNumero del gruppo da consultare: "))
        return avvia_interfaccia(cerca_collezioni(raccolte[scelta - 1]))
    except (ValueError, IndexError):
        print("Scelta non valida.", file=sys.stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        return 130


if __name__ == "__main__":
    raise SystemExit(main())

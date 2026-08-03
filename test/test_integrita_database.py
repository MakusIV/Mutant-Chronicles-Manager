"""
Integrità dei nove database di carte.

Riprende `strumenti/misure/validate.py` — il giro di `from_dict` su ogni carta, che
era uno strumento di misura una tantum — e i validatori già scritti dentro i moduli
`Database_*.py`, che finora si potevano invocare solo dalle voci di menu «dedicato
al test». Qui diventano asserzioni che girano da sole.
"""

import ast
import collections
import io
import contextlib
import importlib
import pathlib

import pytest

from conftest import DATABASE, carica_classe, carica_database

RADICE = pathlib.Path(__file__).resolve().parents[1]


# --------------------------------------------------------------------------
# Ogni carta del database dev'essere costruibile
# --------------------------------------------------------------------------


def _tutte_le_carte():
    for nome_tipo, modulo_db, variabile, modulo_classe, nome_classe in DATABASE:
        if nome_tipo == "Guerriero":
            continue  # i guerrieri hanno una factory propria, verificata più sotto
        database = carica_database(modulo_db, variabile)
        classe = carica_classe(modulo_classe, nome_classe)
        for chiave, dati in database.items():
            yield pytest.param(classe, chiave, dati, id=f"{nome_tipo}-{chiave}")


@pytest.mark.parametrize("classe,chiave,dati", list(_tutte_le_carte()))
def test_ogni_carta_e_costruibile_dal_database(classe, chiave, dati):
    """
    `from_dict` su ogni voce. È il test più grossolano e il più utile: intercetta
    campi mancanti, valori fuori dagli enum e refusi nei nomi delle chiavi, che
    altrimenti si manifestano solo quando qualcuno crea un mazzo che pesca quella carta.
    """
    carta = classe.from_dict(dati)
    assert carta is not None
    assert getattr(carta, "nome", None), f"{chiave}: la carta costruita non ha nome"


@pytest.mark.parametrize("nome_tipo,modulo_db,variabile,modulo_classe,nome_classe", DATABASE)
def test_il_database_non_e_vuoto(nome_tipo, modulo_db, variabile, modulo_classe, nome_classe):
    database = carica_database(modulo_db, variabile)
    assert len(database) > 0, f"il database {nome_tipo} è vuoto"


# --------------------------------------------------------------------------
# Nessuna chiave duplicata nei letterali di dizionario
# --------------------------------------------------------------------------
#
# Una chiave ripetuta in un letterale Python non è un errore: la seconda sovrascrive
# la prima in silenzio, e la carta perduta non compare da nessuna parte. Il censimento
# fatto a mano non aveva trovato duplicati; questo lo rende una verifica permanente.


@pytest.mark.parametrize("percorso", sorted(
    p.name for p in (RADICE / "source" / "data_base_cards").glob("Database_*.py")))
def test_nessuna_chiave_duplicata_nei_letterali(percorso):
    file = RADICE / "source" / "data_base_cards" / percorso
    albero = ast.parse(file.read_text(encoding="utf-8"))

    duplicati = []
    for nodo in ast.walk(albero):
        if not isinstance(nodo, ast.Dict):
            continue
        costanti = [c.value for c in nodo.keys
                    if isinstance(c, ast.Constant) and isinstance(c.value, str)]
        for chiave, quante in collections.Counter(costanti).items():
            if quante > 1:
                duplicati.append(f"riga {nodo.lineno}: {chiave!r} ripetuta {quante} volte")

    assert not duplicati, (
        f"{percorso}: chiavi ripetute in un letterale di dizionario, l'ultima "
        "sovrascrive le precedenti senza segnalarlo:\n  " + "\n  ".join(duplicati)
    )


# --------------------------------------------------------------------------
# I validatori già presenti nei moduli
# --------------------------------------------------------------------------

# Validatori che oggi non segnalano nulla: qualunque segnalazione è una regressione.
VALIDATORI_PULITI = [
    ("Speciale", "Database_Speciale", "verifica_integrita_database"),
    ("Guerriero", "Database_Guerriero", "valida_database"),
    ("Equipaggiamento", "Database_Equipaggiamento", "verifica_integrita_database_equipaggiamenti"),
    ("Fortificazione", "Database_Fortificazione", "verifica_integrita_database"),
    ("Oscura_Simmetria", "Database_Oscura_Simmetria", "verifica_integrita_database"),
]


def _esegui_validatore(modulo, funzione):
    """I validatori stampano un rapporto oltre a restituirlo: qui serve solo il valore."""
    modulo_importato = importlib.import_module(f"source.data_base_cards.{modulo}")
    with contextlib.redirect_stdout(io.StringIO()):
        return getattr(modulo_importato, funzione)()


def _segnalazioni(esito):
    return {categoria: valori for categoria, valori in esito.items()
            if isinstance(valori, (list, dict)) and valori}


@pytest.mark.parametrize("nome_tipo,modulo,funzione", VALIDATORI_PULITI,
                         ids=[v[0] for v in VALIDATORI_PULITI])
def test_i_validatori_esistenti_non_segnalano_nulla(nome_tipo, modulo, funzione):
    segnalazioni = _segnalazioni(_esegui_validatore(modulo, funzione))
    assert not segnalazioni, (
        f"{modulo}.{funzione}() segnala errori che prima non c'erano: {segnalazioni}"
    )


# `Migliorare Se Stesso` dichiara di potenziare C, S, A e V insieme, che il validatore
# non prevede. È l'unica segnalazione aperta su Arte: il test la fissa perché non se ne
# aggiungano altre, non perché vada bene così.
ARTE_SEGNALAZIONI_NOTE = {"statistiche_errate": ["Migliorare Se Stesso: C, S, A, V"]}


def test_arte_non_accumula_nuove_segnalazioni():
    segnalazioni = _segnalazioni(_esegui_validatore("Database_Arte", "valida_database_arte"))
    assert segnalazioni == ARTE_SEGNALAZIONI_NOTE, (
        "le segnalazioni del validatore Arte sono cambiate.\n"
        f"  attese: {ARTE_SEGNALAZIONI_NOTE}\n  trovate: {segnalazioni}"
    )


def test_ogni_warzone_e_validabile():
    """
    `valida_database_completo` mescola integrità e giudizi di bilanciamento — segnala
    «modificatori troppo potenti» e un costo azione che nessuna delle 14 Warzone
    rispetta — quindi non è utilizzabile come assert. Resta utile ciò che verifica per
    davvero: che ogni Warzone sia percorribile senza errori.
    """
    esito = _esegui_validatore("Database_Warzone", "valida_database_completo")
    assert esito["warzone_totali"] == len(carica_database(
        "source.data_base_cards.Database_Warzone", "DATABASE_WARZONE"))
    assert esito["warzone_totali"] > 0


# --------------------------------------------------------------------------
# Le factory di costruzione per nome
# --------------------------------------------------------------------------

FACTORY = [
    ("Guerriero", "Database_Guerriero", "GUERRIERI_DATABASE", "crea_guerriero_da_nome"),
    ("Speciale", "Database_Speciale", "DATABASE_SPECIALI", "crea_carta_da_database"),
    ("Arte", "Database_Arte", "CARTE_ARTE_DATABASE", "crea_carta_da_database"),
    ("Oscura_Simmetria", "Database_Oscura_Simmetria", "DATABASE_OSCURA_SIMMETRIA", "crea_carta_da_database"),
    ("Equipaggiamento", "Database_Equipaggiamento", "DATABASE_EQUIPAGGIAMENTO", "crea_equipaggiamento_da_database"),
    ("Fortificazione", "Database_Fortificazione", "DATABASE_FORTIFICAZIONI", "crea_fortificazione_da_database"),
    ("Reliquia", "Database_Reliquia", "DATABASE_RELIQUIE", "crea_reliquia_da_database"),
    ("Missione", "Database_Missione", "DATABASE_MISSIONI", "crea_missione_da_database"),
    ("Warzone", "Database_Warzone", "DATABASE_WARZONE", "crea_istanza_warzone"),
]


@pytest.mark.parametrize("nome_tipo,modulo,variabile,factory", FACTORY,
                         ids=[f[0] for f in FACTORY])
def test_la_factory_costruisce_ogni_chiave_del_database(nome_tipo, modulo, variabile, factory):
    """
    Le factory sono la via da cui passano collezioni e mazzi: se una chiave non è
    costruibile, la carta esiste nel database ma non entrerà mai in gioco.
    """
    modulo_importato = importlib.import_module(f"source.data_base_cards.{modulo}")
    database = getattr(modulo_importato, variabile)
    costruisci = getattr(modulo_importato, factory)

    mancanti = []
    with contextlib.redirect_stdout(io.StringIO()):
        for chiave in database:
            try:
                if costruisci(chiave) is None:
                    mancanti.append(chiave)
            except Exception as errore:  # noqa: BLE001 — va riportato, non propagato
                mancanti.append(f"{chiave} ({type(errore).__name__}: {errore})")

    assert not mancanti, (
        f"{factory}() non costruisce {len(mancanti)} carte su {len(database)}:\n  "
        + "\n  ".join(str(m) for m in mancanti[:20])
    )


@pytest.mark.parametrize("nome_tipo,modulo,variabile,factory", FACTORY,
                         ids=[f[0] for f in FACTORY])
def test_la_factory_rifiuta_un_nome_inesistente(nome_tipo, modulo, variabile, factory):
    """Il caso negativo: un nome che non esiste non deve produrre una carta."""
    modulo_importato = importlib.import_module(f"source.data_base_cards.{modulo}")
    costruisci = getattr(modulo_importato, factory)

    with contextlib.redirect_stdout(io.StringIO()):
        try:
            carta = costruisci("Carta Che Non Esiste Nel Database")
        except (KeyError, ValueError):
            return  # sollevare è una risposta accettabile
    assert carta is None, (
        f"{factory}() ha costruito qualcosa per un nome inesistente: {carta!r}"
    )

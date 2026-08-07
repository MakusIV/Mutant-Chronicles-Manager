"""
Il vocabolario di abilità e poteri, che pesa sulla **selezione** invece che sulla
compatibilità.

I due assi sono distinti e leggono campi diversi:

- la **compatibilità** (chi può ricevere la carta) legge `restrizioni_guerriero` e
  `fazioni_permesse` per l'Equipaggiamento, `restrizioni` e `keywords_richieste` per le
  Reliquie — verificati in `test_vocabolario_restrizioni.py`;
- la **selezione** (quanto vale la carta) legge `statistiche`, `modificatori_speciali` e
  `abilita_speciali` per l'Equipaggiamento, `modificatori` e `poteri` per le Reliquie.

Anche qui il confronto è su un vocabolario controllato: il punteggio riconosce i nomi
delle abilità per uguaglianza contro elenchi scritti nel codice. Un nome fuori
vocabolario non solleva errori — l'abilità semplicemente non contribuisce, e la carta
vale meno di quanto dovrebbe. È lo stesso difetto delle restrizioni inerti, spostato
dall'ammissibilità al punteggio.
"""

import collections

import pytest

from source.data_base_cards.Database_Equipaggiamento import DATABASE_EQUIPAGGIAMENTO
from source.data_base_cards.Database_Reliquia import DATABASE_RELIQUIE
from source.logic.vocabolario_potenza import VOCABOLARIO_EQUIPAGGIAMENTO, VOCABOLARIO_RELIQUIA


def _vocabolario_del_blocco(vocabolario):
    """
    I nomi che il punteggio riconosce, letti dalla tabella condivisa
    (source/logic/vocabolario_potenza.py) invece che dal codice del metodo.

    Leggerli dalla tabella invece di ricopiarli qui evita che le due liste
    divergano in silenzio: se una regola viene aggiunta o rinominata, il test se
    ne accorge. Prima dell'unificazione in vocabolario_potenza.py questa funzione
    estraeva le stringhe con una regex dal blocco if/elif in Creatore_Mazzo.py;
    ora il vocabolario è dati, non testo sorgente da scansionare.
    """
    return {nome.lower() for regole in vocabolario.values()
            for nomi, _, _ in regole for nome in nomi}


# --------------------------------------------------------------------------
# Equipaggiamento: `abilita_speciali`
# --------------------------------------------------------------------------

# Nomi presenti nel database che il punteggio non riconosce: l'abilità non aggiunge
# nulla alla potenza della carta. L'elenco è vuoto — tutte le abilità pesano — e
# `test_ogni_abilita_speciale_e_classificata` lo tiene tale: un nome nuovo che nessun
# ramo riconosce fa fallire quel test, e va corretto invece che aggiunto qui.
ABILITA_SENZA_PUNTEGGIO: dict[str, str] = {}


def _abilita_nei_dati():
    contate = collections.Counter()
    for dati in DATABASE_EQUIPAGGIAMENTO.values():
        for abilita in dati.get("abilita_speciali") or []:
            contate[str(abilita.get("nome", "")).lower().strip()] += 1
    return contate


def test_ogni_abilita_speciale_e_classificata():
    """
    Nessun nome di abilità sfugge alle due liste: o il punteggio lo riconosce, o è
    dichiarato qui come non contribuente, con la ragione scritta.
    """
    riconosciuti = _vocabolario_del_blocco(VOCABOLARIO_EQUIPAGGIAMENTO)
    non_classificate = [
        f"{nome!r} ({quante} abilità)"
        for nome, quante in _abilita_nei_dati().items()
        if nome not in riconosciuti and nome not in ABILITA_SENZA_PUNTEGGIO
    ]
    assert not non_classificate, (
        "abilità speciali il cui nome il punteggio non riconosce e che non sono "
        "dichiarate: la carta vale meno di quanto dovrebbe.\n  "
        + "\n  ".join(sorted(non_classificate))
    )


@pytest.mark.parametrize("nome,causa", sorted(ABILITA_SENZA_PUNTEGGIO.items()))
def test_le_abilita_senza_punteggio_sono_ancora_tali(nome, causa):
    """Sentinella: quando un nome viene allineato, questo test lo segnala."""
    riconosciuti = _vocabolario_del_blocco(VOCABOLARIO_EQUIPAGGIAMENTO)
    assert nome not in riconosciuti, (
        f"«{nome}» è ora riconosciuto ({causa}). Toglilo da ABILITA_SENZA_PUNTEGGIO.")
    assert nome in _abilita_nei_dati(), (
        f"«{nome}» non compare più nel database. Toglilo da ABILITA_SENZA_PUNTEGGIO.")


def test_nessuna_stringa_del_vocabolario_porta_maiuscole():
    """
    Il confronto avviene contro il nome dell'abilità **già abbassato a minuscolo**
    (vedi `applica_bonus_abilita` in vocabolario_potenza.py): una stringa del
    vocabolario con una maiuscola non potrebbe mai corrispondere, e la regola che
    la contiene sarebbe scritta ma irraggiungibile. Erano 19 stringhe in quattro
    blocchi — `"Incrementa Azioni"`, `"Attacca sempre per primo"`, `"Immune alle
    ferite durante il combattimento"` fra le altre — e valevano da sole 4 delle 12
    abilità senza punteggio, prima che venissero corrette.
    """
    from source.logic.vocabolario_potenza import (
        VOCABOLARIO_GUERRIERO, VOCABOLARIO_EQUIPAGGIAMENTO, VOCABOLARIO_FORTIFICAZIONE,
        VOCABOLARIO_RELIQUIA, VOCABOLARIO_WARZONE,
    )

    sospette = []
    tabelle = [
        ("Guerriero", VOCABOLARIO_GUERRIERO),
        ("Equipaggiamento", VOCABOLARIO_EQUIPAGGIAMENTO),
        ("Fortificazione", VOCABOLARIO_FORTIFICAZIONE),
        ("Reliquia", VOCABOLARIO_RELIQUIA),
        ("Warzone", VOCABOLARIO_WARZONE),
    ]
    for etichetta, vocabolario in tabelle:
        for tipo, regole in vocabolario.items():
            for nomi, _, _ in regole:
                for stringa in nomi:
                    if any(carattere.isupper() for carattere in stringa):
                        sospette.append(f"{etichetta}[{tipo!r}]: {stringa!r}")

    assert not sospette, (
        "stringhe del vocabolario che il confronto in minuscolo non può raggiungere:\n  "
        + "\n  ".join(sospette))


# --------------------------------------------------------------------------
# Reliquia: `poteri`
# --------------------------------------------------------------------------

POTERI_SENZA_PUNTEGGIO: dict[str, str] = {}


def _poteri_nei_dati():
    contate = collections.Counter()
    for dati in DATABASE_RELIQUIE.values():
        for potere in dati.get("poteri") or []:
            contate[str(potere.get("nome", "")).lower().strip()] += 1
    return contate


def test_ogni_potere_di_reliquia_e_classificato():
    riconosciuti = _vocabolario_del_blocco(VOCABOLARIO_RELIQUIA)
    non_classificati = [
        f"{nome!r} ({quante} poteri)"
        for nome, quante in _poteri_nei_dati().items()
        if nome not in riconosciuti and nome not in POTERI_SENZA_PUNTEGGIO
    ]
    assert not non_classificati, (
        "poteri il cui nome il punteggio non riconosce e che non sono dichiarati:\n  "
        + "\n  ".join(sorted(non_classificati))
    )


@pytest.mark.parametrize("nome,causa", sorted(POTERI_SENZA_PUNTEGGIO.items()))
def test_i_poteri_senza_punteggio_sono_ancora_tali(nome, causa):
    riconosciuti = _vocabolario_del_blocco(VOCABOLARIO_RELIQUIA)
    assert nome not in riconosciuti, (
        f"«{nome}» è ora riconosciuto ({causa}). Toglilo da POTERI_SENZA_PUNTEGGIO.")
    assert nome in _poteri_nei_dati(), (
        f"«{nome}» non compare più nel database. Toglilo da POTERI_SENZA_PUNTEGGIO.")


# --------------------------------------------------------------------------
# Le convenzioni sulle statistiche
# --------------------------------------------------------------------------


@pytest.mark.parametrize("statistica,attesa", [
    # I due database usano convenzioni diverse: sigle per le Reliquie, nomi estesi per
    # l'Equipaggiamento. Entrambe devono essere riconosciute, altrimenti i modificatori
    # di un'intera tipologia smetterebbero di pesare senza che nulla lo segnali.
    ("C", True), ("S", True), ("A", True),
    ("combattimento", True), ("sparare", True), ("armatura", True),
    ("multiple: S, A, V", True),
    ("combattimento dell'avversario", True),
    # Il Valore non è una statistica di combattimento: resta fuori dal punteggio.
    ("V", False), ("valore", False),
])
def test_le_due_convenzioni_sulle_statistiche_sono_riconosciute(statistica, attesa):
    from source.logic.Creatore_Mazzo import statistica_di_combattimento

    assert statistica_di_combattimento(statistica) is attesa


def test_i_modificatori_delle_reliquie_usano_le_sigle():
    """Il presupposto del test qui sopra, verificato sui dati veri."""
    from source.logic.Creatore_Mazzo import statistica_di_combattimento

    ignorati = []
    for nome_carta, dati in DATABASE_RELIQUIE.items():
        for modificatore in dati.get("modificatori") or []:
            statistica = str(modificatore.get("statistica") or "")
            if statistica and not statistica_di_combattimento(statistica):
                ignorati.append(f"{nome_carta}: {statistica!r}")

    # Il Valore è escluso per scelta, quindi qui restano solo le statistiche su cui il
    # punteggio *dovrebbe* pesare.
    inattesi = [voce for voce in ignorati if not voce.rstrip("'").endswith("V")]
    assert not inattesi, (
        f"modificatori di Reliquia su statistiche non riconosciute: {inattesi}")


# --------------------------------------------------------------------------
# Campi letti ma privi di dati
# --------------------------------------------------------------------------


def test_requisiti_speciali_delle_reliquie_resta_vuoto():
    """
    `requisiti_speciali` è letto da `puo_essere_associata_a_guerriero` ma nessuna
    Reliquia lo popola: è codice pronto per dati che non esistono. Il test lo fissa
    perché, se un giorno il campo venisse riempito, la sua logica vada verificata —
    oggi non è esercitata da nulla.
    """
    popolati = {nome for nome, dati in DATABASE_RELIQUIE.items()
                if dati.get("requisiti_speciali")}
    assert not popolati, (
        "queste Reliquie ora dichiarano `requisiti_speciali`, la cui logica non è mai "
        f"stata esercitata: {sorted(popolati)}")

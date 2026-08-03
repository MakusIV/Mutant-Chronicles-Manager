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
import pathlib
import re

import pytest

from source.data_base_cards.Database_Equipaggiamento import DATABASE_EQUIPAGGIAMENTO
from source.data_base_cards.Database_Reliquia import DATABASE_RELIQUIE

RADICE = pathlib.Path(__file__).resolve().parents[1]
SORGENTE_PUNTEGGIO = (RADICE / "source" / "logic" / "Creatore_Mazzo.py").read_text(
    encoding="utf-8")


def _vocabolario_del_blocco(intestazione):
    """
    I nomi che il punteggio riconosce, letti dal blocco che li confronta.

    Estrarli dal codice invece di ricopiarli qui evita che le due liste divergano in
    silenzio: se un ramo viene aggiunto o rinominato, il test se ne accorge.
    """
    inizio = SORGENTE_PUNTEGGIO.index(intestazione)
    fine = SORGENTE_PUNTEGGIO.index("\n    def ", inizio)
    blocco = SORGENTE_PUNTEGGIO[inizio:fine]
    return {s.lower() for s in re.findall(r'"([a-zà-ù\' ]{4,})"', blocco)}


# --------------------------------------------------------------------------
# Equipaggiamento: `abilita_speciali`
# --------------------------------------------------------------------------

# Nomi presenti nel database che il punteggio non riconosce: l'abilità non aggiunge
# nulla alla potenza della carta. Vanno svuotati allineando il nome al vocabolario o
# aggiungendo il ramo, non allungati.
ABILITA_SENZA_PUNTEGGIO = {
    "assegna carte": "il ramo esistente è «assegna carta», al singolare",
    "lancia arte": "nessun ramo per questo nome nel blocco `arte`",
    "attacca sempre per primo": "il ramo affine è «permette ai guerrieri di attaccare per primi»",
    "immune alle ferite durante il combattimento":
        "il ramo lo cerca per sottostringa ma con la maiuscola: «Immune alle ferite…»",
    "incrementa azioni": "nessun ramo per questo nome",
    "attacca sempre per primo se sceglie di sparare": "nessun ramo per questo nome",
}


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
    riconosciuti = _vocabolario_del_blocco("# Bonus per abilita speciali")
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
    riconosciuti = _vocabolario_del_blocco("# Bonus per abilita speciali")
    assert nome not in riconosciuti, (
        f"«{nome}» è ora riconosciuto ({causa}). Toglilo da ABILITA_SENZA_PUNTEGGIO.")
    assert nome in _abilita_nei_dati(), (
        f"«{nome}» non compare più nel database. Toglilo da ABILITA_SENZA_PUNTEGGIO.")


def test_quante_abilita_restano_senza_punteggio():
    """Il conteggio, perché la misura resti sotto gli occhi: oggi sono 12 su 54."""
    riconosciuti = _vocabolario_del_blocco("# Bonus per abilita speciali")
    contate = _abilita_nei_dati()
    ignorate = sum(q for nome, q in contate.items() if nome not in riconosciuti)
    assert (ignorate, sum(contate.values())) == (12, 54), (
        f"la proporzione è cambiata: {ignorate} abilità senza punteggio su "
        f"{sum(contate.values())}")


# --------------------------------------------------------------------------
# Reliquia: `poteri`
# --------------------------------------------------------------------------

POTERI_SENZA_PUNTEGGIO = {
    "attacco in uscita da copertura": "nessun ramo per questo nome nel blocco `azioni`",
    "annulla effetto arte": "il ramo affine è «annulla immunita dell'Oscura simmetria»",
}


def _poteri_nei_dati():
    contate = collections.Counter()
    for dati in DATABASE_RELIQUIE.values():
        for potere in dati.get("poteri") or []:
            contate[str(potere.get("nome", "")).lower().strip()] += 1
    return contate


def test_ogni_potere_di_reliquia_e_classificato():
    riconosciuti = _vocabolario_del_blocco("# Bonus per poteri")
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
    riconosciuti = _vocabolario_del_blocco("# Bonus per poteri")
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

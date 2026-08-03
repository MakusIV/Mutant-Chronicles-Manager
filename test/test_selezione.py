"""
La selezione dei guerrieri e delle carte di supporto.

Qui non si verifica l'ammissibilità — quella è delegata al controllo carta-guerriero
già coperto da `test_restrizioni_associazione.py` — ma il **peso**: quali guerrieri e
quali carte l'orientamento del mazzo fa emergere. Un orientamento che non pesa nulla
non fa fallire niente, produce solo mazzi che ignorano ciò che si è chiesto.
"""

import ast
import pathlib
import random

import pytest

from source.cards.Guerriero import Set_Espansione
from source.data_base_cards.Database_Guerriero import GUERRIERI_DATABASE, crea_guerriero_da_nome
from source.logic.Creatore_Collezione import CollezioneGiocatore
from source.logic.Creatore_Mazzo import CreatoreMazzo

RADICE = pathlib.Path(__file__).resolve().parents[1]
ESPANSIONI = [s.value for s in Set_Espansione]


@pytest.fixture(scope="module")
def creatore():
    """Una collezione con 5 copie di ogni guerriero: isola la selezione dal caso."""
    collezione = CollezioneGiocatore(1)
    for nome in GUERRIERI_DATABASE:
        guerriero = crea_guerriero_da_nome(nome)
        if guerriero is not None:
            collezione.aggiungi_carta(guerriero, 5)
    return CreatoreMazzo(collezione)


def _seleziona(creatore, **orientamento):
    random.seed(42)
    squadra, schieramento = creatore.seleziona_guerrieri(
        espansioni_richieste=ESPANSIONI, numero_guerrieri_target=40, **orientamento)
    return [g.nome for g in squadra + schieramento]


# --------------------------------------------------------------------------


@pytest.mark.lento
def test_l_orientamento_cultista_fa_emergere_i_cultisti(creatore):
    """
    La condizione era `'Cultista' in guerriero.keywords`, ma la keyword è sempre
    «Cultista di <Apostolo>» e `in` su una lista confronta gli elementi interi: era
    sempre falsa, e BONUS_CULTISTA non veniva applicato a nessuno. Nessun errore, solo
    un orientamento che non orientava.
    """
    senza = _seleziona(creatore, doomtrooper=False, fratellanza=False, oscura_legione=True)
    con = _seleziona(creatore, doomtrooper=False, fratellanza=False, oscura_legione=True,
                     orientamento_cultista=True)

    cultisti_con = [n for n in con if n.startswith("Cultista")]
    cultisti_senza = [n for n in senza if n.startswith("Cultista")]

    assert len(cultisti_con) > len(cultisti_senza), (
        "chiedendo l'orientamento Cultista non ne emerge nessuno in più: "
        f"con={cultisti_con} senza={cultisti_senza}"
    )


@pytest.mark.lento
def test_l_orientamento_eretico_fa_emergere_gli_eretici(creatore):
    """Il controllo gemello, sulla keyword «Eretico», che invece è nuda e funziona."""
    eretici = {nome for nome, dati in GUERRIERI_DATABASE.items()
               if "Eretico" in (dati.get("keywords") or [])}

    senza = _seleziona(creatore, doomtrooper=False, fratellanza=False, oscura_legione=True)
    con = _seleziona(creatore, doomtrooper=False, fratellanza=False, oscura_legione=True,
                     orientamento_eretico=True)

    assert len([n for n in con if n in eretici]) > len([n for n in senza if n in eretici]), (
        "chiedendo l'orientamento Eretico non ne emerge nessuno in più"
    )


@pytest.mark.lento
@pytest.mark.xfail(strict=True, reason=(
    "`seleziona_guerrieri` sceglie il ramo di orientamento con un if/elif sulla fazione, "
    "e i Cultisti hanno fazione Oscura Legione: in un mazzo Doomtrooper non entrano mai, "
    "benché il testo li dichiari «CONSIDERATO UN DOOMTROOPER SENZA ICONA DI LEGAME» e "
    "lasci scegliere volta per volta. La doppia natura non è modellata"))
def test_i_cultisti_entrano_anche_in_un_mazzo_doomtrooper(creatore):
    selezionati = _seleziona(creatore, doomtrooper=True, fratellanza=False,
                             oscura_legione=False, orientamento_cultista=True)
    assert [n for n in selezionati if n.startswith("Cultista")]


# --------------------------------------------------------------------------
# La rete contro l'intera classe di difetti
# --------------------------------------------------------------------------

# Keyword composte: chi le cerca deve usare il prefisso o una sottostringa, mai
# l'appartenenza secca alla lista.
PREFISSI_COMPOSTI = ("Cultista", "Seguace")


def test_nessun_confronto_secco_su_keyword_composte():
    """
    `'Cultista' in guerriero.keywords` non solleva nulla e vale sempre False, perché
    nella lista c'è «Cultista di Semai». È lo stesso difetto trovato in due punti di
    `seleziona_guerrieri` e `seleziona_carte_supporto`, ed è invisibile a occhio:
    questo test lo cerca nell'albero sintattico di tutto il progetto.
    """
    sospetti = []
    for percorso in sorted(RADICE.glob("source/**/*.py")):
        albero = ast.parse(percorso.read_text(encoding="utf-8"))
        for nodo in ast.walk(albero):
            if not isinstance(nodo, ast.Compare) or len(nodo.ops) != 1:
                continue
            if not isinstance(nodo.ops[0], (ast.In, ast.NotIn)):
                continue
            sinistra, destra = nodo.left, nodo.comparators[0]
            # forma: "<costante>" in <qualcosa>.keywords
            if not (isinstance(sinistra, ast.Constant) and isinstance(sinistra.value, str)):
                continue
            if not (isinstance(destra, ast.Attribute) and destra.attr == "keywords"):
                continue
            valore = sinistra.value
            if valore in PREFISSI_COMPOSTI:
                sospetti.append(
                    f"{percorso.relative_to(RADICE)}:{nodo.lineno}: «{valore}» confrontata "
                    f"con `in` su keywords, ma la keyword completa è «{valore} di <Apostolo>»")

    assert not sospetti, (
        "confronti che risultano sempre falsi perché la keyword nel database è "
        "composta:\n  " + "\n  ".join(sospetti)
    )


def test_le_keyword_composte_del_database_hanno_sempre_il_complemento():
    """Il presupposto del test qui sopra: nessun guerriero porta il prefisso nudo."""
    nude = set()
    for nome, dati in GUERRIERI_DATABASE.items():
        for keyword in dati.get("keywords") or []:
            if keyword in PREFISSI_COMPOSTI:
                nude.add(f"{nome}: «{keyword}»")

    assert not nude, (
        "guerrieri con una keyword composta usata senza complemento — se è voluto, "
        f"i confronti secchi diventano leciti e questo test va rivisto: {sorted(nude)}"
    )

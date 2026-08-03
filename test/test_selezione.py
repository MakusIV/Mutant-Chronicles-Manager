"""
La selezione dei guerrieri e delle carte di supporto.

Qui non si verifica l'ammissibilità — quella è delegata al controllo carta-guerriero
già coperto da `test_restrizioni_associazione.py` — ma il **peso**: quali guerrieri e
quali carte l'orientamento del mazzo fa emergere. Un orientamento che non pesa nulla
non fa fallire niente, produce solo mazzi che ignorano ciò che si è chiesto.
"""

import ast
import importlib
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
    """
    Una collezione con 5 copie di ogni carta: isola la selezione dal caso.

    Serve anche l'equipaggiamento, non i soli guerrieri, perché i test sulla sinergia
    verificano quali carte di supporto emergono.
    """
    collezione = CollezioneGiocatore(1)

    equipaggiamento = importlib.import_module(
        "source.data_base_cards.Database_Equipaggiamento")
    fonti = [
        (GUERRIERI_DATABASE, crea_guerriero_da_nome),
        (equipaggiamento.DATABASE_EQUIPAGGIAMENTO,
         equipaggiamento.crea_equipaggiamento_da_database),
    ]
    for database, costruisci in fonti:
        for nome in database:
            carta = costruisci(nome)
            if carta is not None:
                collezione.aggiungi_carta(carta, 5)
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
# Bonus riservati a guerrieri specifici
# --------------------------------------------------------------------------
#
# Alcune carte concedono un potenziamento maggiore a un guerriero determinato — la
# Lancia Castigator dà +2 in C a ogni Doomtrooper e +4 a una Valchiria. La condizione
# lo dice in prosa e in maiuscolo; `guerrieri_avvantaggiati` ne è la forma
# confrontabile, ed è quella che il punteggio sa leggere.

CARTE_CON_SINERGIA = [
    ("Lancia Castigator", "Valkiria"),
    ("Azogar", "Valpurgius"),
    ("Tenuta da Battaglia", "Inquisitore"),
]


def _equipaggiamento(nome):
    modulo = importlib.import_module("source.data_base_cards.Database_Equipaggiamento")
    return modulo.crea_equipaggiamento_da_database(nome)


@pytest.mark.parametrize("nome_carta,nome_guerriero", CARTE_CON_SINERGIA,
                         ids=[c[0] for c in CARTE_CON_SINERGIA])
def test_la_sinergia_e_riconosciuta_solo_col_guerriero_giusto(creatore, nome_carta,
                                                              nome_guerriero):
    carta = _equipaggiamento(nome_carta)
    assert carta is not None

    con = [crea_guerriero_da_nome(nome_guerriero)]
    senza = [crea_guerriero_da_nome("Blood Beret")]

    assert creatore._bonus_condizionato_attivabile(carta, con), (
        f"{nome_carta}: la sinergia con {nome_guerriero} non viene riconosciuta")
    assert not creatore._bonus_condizionato_attivabile(carta, senza), (
        f"{nome_carta}: la sinergia scatta anche senza {nome_guerriero}")


def test_una_carta_senza_il_campo_non_attiva_mai_la_sinergia(creatore):
    """Il verso complementare: il bonus non deve comparire dal nulla."""
    carta = _equipaggiamento("Ticker")
    assert carta is not None
    assert not creatore._bonus_condizionato_attivabile(
        carta, [crea_guerriero_da_nome("Valkiria")])


def test_i_guerrieri_avvantaggiati_esistono_nel_database():
    """
    Il campo è una trascrizione della condizione in prosa: un refuso nel nome lo
    renderebbe inerte senza che nulla lo segnali — è il difetto che questa suite
    insegue da principio.
    """
    modulo = importlib.import_module("source.data_base_cards.Database_Equipaggiamento")
    sconosciuti = []
    for nome_carta, dati in modulo.DATABASE_EQUIPAGGIAMENTO.items():
        for modificatore in dati.get("modificatori_speciali") or []:
            for nome in modificatore.get("guerrieri_avvantaggiati") or []:
                if nome not in GUERRIERI_DATABASE:
                    sconosciuti.append(f"{nome_carta}: «{nome}»")

    assert not sconosciuti, (
        "nomi in `guerrieri_avvantaggiati` che non esistono fra i guerrieri: "
        f"{sconosciuti}")


def test_il_campo_accompagna_sempre_una_condizione_ristretta():
    """
    `guerrieri_avvantaggiati` ha senso solo su un modificatore che il punteggio non
    conteggia da sé: se la condizione non fosse «Uso ristretto:», il bonus verrebbe
    contato due volte.
    """
    modulo = importlib.import_module("source.data_base_cards.Database_Equipaggiamento")
    incoerenti = []
    for nome_carta, dati in modulo.DATABASE_EQUIPAGGIAMENTO.items():
        for modificatore in dati.get("modificatori_speciali") or []:
            if not (modificatore.get("guerrieri_avvantaggiati") or []):
                continue
            if "uso ristretto:" not in str(modificatore.get("condizione", "")).lower():
                incoerenti.append(f"{nome_carta}: {modificatore.get('condizione')!r}")

    assert not incoerenti, (
        "modificatori con `guerrieri_avvantaggiati` ma senza condizione «Uso ristretto:», "
        f"il cui bonus verrebbe conteggiato due volte: {incoerenti}")


@pytest.mark.lento
def test_la_sinergia_fa_salire_la_carta_in_classifica(creatore):
    """
    L'effetto sulla selezione, misurato a parità di squadra: cambia solo l'esito del
    rilevamento, così il confronto non risente del numero di guerrieri — che altrimenti
    sposterebbe il fattore di compatibilità di tutte le carte.
    """
    squadra = [g for g in (crea_guerriero_da_nome(n) for n in
                           ("Blood Beret", "Ussaro", "Sergente", "Valkiria")) if g]

    def posizione(sinergia_attiva):
        originale = CreatoreMazzo._bonus_condizionato_attivabile
        if not sinergia_attiva:
            CreatoreMazzo._bonus_condizionato_attivabile = lambda self, c, g: False
        try:
            random.seed(42)
            selezionate = creatore.seleziona_carte_supporto(
                squadra=squadra, schieramento=[], espansioni_richieste=ESPANSIONI,
                tipo_carta="equipaggiamento", doomtrooper=True, fratellanza=True,
                oscura_legione=False, numero_carte=200)
            nomi = [getattr(c, "nome", "") for c in selezionate]
            return nomi.index("Lancia Castigator") if "Lancia Castigator" in nomi else None
        finally:
            CreatoreMazzo._bonus_condizionato_attivabile = originale

    con = posizione(True)
    senza = posizione(False)
    assert con is not None and senza is not None, "la carta non compare in classifica"
    assert con < senza, (
        f"con la Valkiria in squadra la Lancia Castigator dovrebbe salire, "
        f"ma passa dalla posizione {senza} alla {con}")


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

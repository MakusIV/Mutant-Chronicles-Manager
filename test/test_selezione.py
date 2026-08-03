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
    speciale = importlib.import_module("source.data_base_cards.Database_Speciale")
    fortificazione = importlib.import_module(
        "source.data_base_cards.Database_Fortificazione")
    fonti = [
        (GUERRIERI_DATABASE, crea_guerriero_da_nome),
        (equipaggiamento.DATABASE_EQUIPAGGIAMENTO,
         equipaggiamento.crea_equipaggiamento_da_database),
        (speciale.DATABASE_SPECIALI, speciale.crea_carta_da_database),
        (fortificazione.DATABASE_FORTIFICAZIONI,
         fortificazione.crea_fortificazione_da_database),
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
def test_i_cultisti_entrano_anche_in_un_mazzo_doomtrooper(creatore):
    """
    «CONSIDERATO UN DOOMTROOPER SENZA ICONA DI LEGAME»: la keyword
    `Doomtrooper senza legame` traduce quella dichiarazione, e `seleziona_guerrieri` la
    legge. Prima il ramo di orientamento si sceglieva con un if/elif sulla sola fazione,
    e i Cultisti — che sono Oscura Legione — non entravano mai in un mazzo Doomtrooper.
    """
    selezionati = _seleziona(creatore, doomtrooper=True, fratellanza=False,
                             oscura_legione=False, orientamento_cultista=True)
    assert [n for n in selezionati if n.startswith("Cultista")]


@pytest.mark.lento
def test_i_cultisti_pesano_sulla_quota_dell_oscura_legione(creatore):
    """
    Il Cultista sta in Squadra ma è un guerriero dell'Oscura Legione: la quota che lo
    ospita è quella della sua fazione, non quella dell'area in cui è schierato.

    Contandolo fra i Doomtrooper finiva in competizione con loro per gli stessi posti, e
    in un mazzo a orientamento misto la Squadra si riempiva di Doomtrooper prima che
    arrivasse il suo turno: i Cultisti restavano fuori proprio quando erano la
    specializzazione richiesta.
    """
    # Il numero di guerrieri conta: troppo pochi e la Squadra non si satura, troppi e
    # avanza posto per tutti. A 30 le quote sono 15 e 15, e la Squadra si riempie di
    # Doomtrooper prima che arrivi il turno del secondo Cultista — la condizione in cui
    # il difetto si manifestava.
    random.seed(42)
    squadra, schieramento = creatore.seleziona_guerrieri(
        espansioni_richieste=ESPANSIONI, numero_guerrieri_target=30,
        doomtrooper=True,
        orientamento_doomtrooper=["Imperiale", "Cybertronic", "Mercenario"],
        fratellanza=False, oscura_legione=True,
        orientamento_apostolo=["Algeroth", "Ilian"],
        orientamento_eretico=True, orientamento_cultista=True)

    cultisti = {g.nome for g in squadra + schieramento if g.nome.startswith("Cultista")}
    assert len(cultisti) >= 2, (
        f"con due Apostoli orientati e la specializzazione Cultista attiva ne è entrato "
        f"solo: {sorted(cultisti)}")


@pytest.mark.lento
def test_i_cultisti_vanno_sempre_in_squadra(creatore):
    """
    «Puoi aggiungere il Cultista solo alla Tua Squadra»: non va nello Schieramento
    nemmeno in un mazzo orientato all'Oscura Legione, dove la sua fazione lo porterebbe.
    """
    for orientamento in [dict(doomtrooper=True, fratellanza=False, oscura_legione=False),
                         dict(doomtrooper=False, fratellanza=False, oscura_legione=True)]:
        random.seed(42)
        squadra, schieramento = creatore.seleziona_guerrieri(
            espansioni_richieste=ESPANSIONI, numero_guerrieri_target=40,
            orientamento_cultista=True, **orientamento)

        nello_schieramento = [g.nome for g in schieramento if g.nome.startswith("Cultista")]
        assert not nello_schieramento, (
            f"Cultisti finiti nello Schieramento con {orientamento}: {nello_schieramento}")


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
# Senza Fratellanza il mazzo rinuncia all'Arte
# --------------------------------------------------------------------------
#
# Le carte Arte occupano slot, e tenere le carte che le abilitano per i pochi guerrieri
# non della Fratellanza che le lanciano significa sperare che l'incantesimo e chi può
# lanciarlo escano in fasi Pescare vicine: una scommessa che, non riuscendo, satura la
# mano. La tipologia `arte` era già esclusa; mancavano le carte che la abilitano.


def _carte_che_abilitano_l_arte():
    from source.logic.Creatore_Mazzo import ABILITA_ARTE

    trovate = []
    for modulo, variabile in [("Database_Speciale", "DATABASE_SPECIALI"),
                              ("Database_Fortificazione", "DATABASE_FORTIFICAZIONI"),
                              ("Database_Reliquia", "DATABASE_RELIQUIE")]:
        database = getattr(importlib.import_module(f"source.data_base_cards.{modulo}"),
                           variabile)
        trovate += [nome for nome, dati in database.items()
                    if ABILITA_ARTE in (dati.get("keywords") or [])]
    return trovate


def test_le_carte_che_abilitano_l_arte_sono_marcate():
    """
    Il marcatore distingue chi **abilita** l'Arte da chi vi si **oppone**: la sola
    keyword «Arte» non basterebbe, perché la porta anche `Interferenza`, che annulla un
    incantesimo avversario e resta utile in un mazzo che all'Arte rinuncia.
    """
    marcate = _carte_che_abilitano_l_arte()
    assert len(marcate) == 17, f"le carte marcate sono {len(marcate)}: {sorted(marcate)}"

    speciale = importlib.import_module("source.data_base_cards.Database_Speciale")
    for nome in ("Interferenza", "Forza Di Volonta", "Distratto"):
        if nome in speciale.DATABASE_SPECIALI:
            assert nome not in marcate, (
                f"«{nome}» si oppone all'Arte, non la abilita: non va marcata")


@pytest.mark.lento
@pytest.mark.parametrize("tipologia", ["speciale", "fortificazione"])
def test_senza_fratellanza_niente_carte_che_abilitano_l_arte(creatore, tipologia):
    from source.logic.Creatore_Mazzo import ABILITA_ARTE

    squadra = [g for g in (crea_guerriero_da_nome(n) for n in
                           ("Blood Beret", "Ussaro", "Sergente")) if g]
    random.seed(42)
    selezionate = creatore.seleziona_carte_supporto(
        squadra=squadra, schieramento=[], espansioni_richieste=ESPANSIONI,
        tipo_carta=tipologia, doomtrooper=True, fratellanza=False,
        oscura_legione=False, numero_carte=200)

    abilitanti = [getattr(c, "nome", "?") for c in selezionate
                  if ABILITA_ARTE in (getattr(c, "keywords", None) or [])]
    assert not abilitanti, (
        f"un mazzo senza Fratellanza ha pescato carte che abilitano l'Arte: "
        f"{sorted(set(abilitanti))}")


@pytest.mark.lento
@pytest.mark.parametrize("seme", range(6))
def test_valpurgius_non_dipende_dall_arte(creatore, seme):
    """
    Valpurgius lancia l'Arte, ma vale per molto altro: è `fondamentale`, ha
    `valore_strategico` massimo ed è un Nefarita Seguace di Algeroth. La regola che
    esclude le carte dell'Arte senza Fratellanza riguarda le carte di supporto, non i
    guerrieri: chiedendo l'Oscura Legione con Algeroth deve entrare comunque.
    """
    random.seed(seme)
    squadra, schieramento = creatore.seleziona_guerrieri(
        espansioni_richieste=ESPANSIONI, numero_guerrieri_target=25,
        doomtrooper=False, fratellanza=False, oscura_legione=True,
        orientamento_apostolo=["Algeroth"])

    assert any(g.nome == "Valpurgius" for g in squadra + schieramento), (
        "Valpurgius non è stato selezionato con orientamento Oscura Legione e Algeroth")


def test_valpurgius_e_una_carta_fondamentale():
    """Il presupposto: se perdesse quei due attributi, la selezione cambierebbe."""
    dati = GUERRIERI_DATABASE["Valpurgius"]
    assert dati.get("fondamentale") is True
    assert dati.get("valore_strategico", 0) >= 8


@pytest.mark.lento
def test_con_la_fratellanza_quelle_carte_restano_disponibili(creatore):
    """Il verso complementare: la regola esclude, non cancella."""
    from source.logic.Creatore_Mazzo import ABILITA_ARTE

    squadra = [g for g in (crea_guerriero_da_nome(n) for n in
                           ("Mistico", "Custode dell'Arte", "Valkiria")) if g]
    random.seed(42)
    selezionate = creatore.seleziona_carte_supporto(
        squadra=squadra, schieramento=[], espansioni_richieste=ESPANSIONI,
        tipo_carta="fortificazione", doomtrooper=False, fratellanza=True,
        oscura_legione=False, numero_carte=200)

    abilitanti = [getattr(c, "nome", "?") for c in selezionate
                  if ABILITA_ARTE in (getattr(c, "keywords", None) or [])]
    assert abilitanti, (
        "con la Fratellanza le carte che abilitano l'Arte devono restare selezionabili")


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

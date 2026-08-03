"""
I vincoli verificati **carta per carta**, sui guerrieri veri del database.

`test_vocabolario_restrizioni.py` giudica una stringa alla volta e non basta: la
stessa stringa può essere ridondante su una carta e fatale su un'altra. `Solo
Doomtrooper` era innocuo su `Cospirazione Eretica`, che elenca le sette fazioni
Doomtrooper in `fazioni_permesse`, ed era l'unico vincolo dichiarato da `Quindici
Minuti Di Fama`, che invece dichiarava `fazioni_permesse = ['Generica']` — e
`Generica` è proprio il valore che disattiva il controllo di fazione. Quella carta
finiva addosso a 47 guerrieri dell'Oscura Legione.

Qui si guarda l'effetto complessivo: quali guerrieri reali possono ricevere la carta.
"""

import importlib

import pytest

from source.data_base_cards.Database_Guerriero import GUERRIERI_DATABASE, crea_guerriero_da_nome


def _guerrieri():
    for nome in GUERRIERI_DATABASE:
        guerriero = crea_guerriero_da_nome(nome)
        if guerriero is not None:
            yield nome, guerriero


GUERRIERI = list(_guerrieri())

DOOMTROOPER = {"Bauhaus", "Mishima", "Cybertronic", "Imperiale", "Capitol",
               "Mercenario", "Fratellanza"}


def _vale_come_doomtrooper(nome):
    """
    Vale come Doomtrooper chi appartiene alle sette fazioni **o** lo dichiara con la
    keyword «Doomtrooper senza legame» — i Cultisti, che sono Oscura Legione.
    """
    dati = GUERRIERI_DATABASE[nome]
    return (dati.get("fazione") in DOOMTROOPER
            or "Doomtrooper senza legame" in (dati.get("keywords") or []))


# --------------------------------------------------------------------------
# Nessuna carta deve restare senza destinatari
# --------------------------------------------------------------------------
#
# La rete di sicurezza contro le restrizioni contraddittorie. Il consumatore valuta le
# voci di `restrizioni` **in AND**: due condizioni che nessun guerriero soddisfa
# insieme — «Solo Doomtrooper» e «Solo Eretico» su `Cospirazione Eretica`, che il testo
# vuole in alternativa — rendono la carta ineseguibile senza sollevare alcun errore.
# È il difetto speculare a quello del permesso sempre concesso, e nessun test sul caso
# positivo di una singola restrizione lo avrebbe visto.

TIPI_ASSEGNABILI = [
    ("Speciale", "Database_Speciale", "DATABASE_SPECIALI", "crea_carta_da_database"),
    ("Equipaggiamento", "Database_Equipaggiamento", "DATABASE_EQUIPAGGIAMENTO",
     "crea_equipaggiamento_da_database"),
    ("Fortificazione", "Database_Fortificazione", "DATABASE_FORTIFICAZIONI",
     "crea_fortificazione_da_database"),
    ("Missione", "Database_Missione", "DATABASE_MISSIONI", "crea_missione_da_database"),
    ("Reliquia", "Database_Reliquia", "DATABASE_RELIQUIE", "crea_reliquia_da_database"),
    ("Warzone", "Database_Warzone", "DATABASE_WARZONE", "crea_istanza_warzone"),
    ("Oscura_Simmetria", "Database_Oscura_Simmetria", "DATABASE_OSCURA_SIMMETRIA",
     "crea_carta_da_database"),
]


@pytest.mark.parametrize("nome_tipo,modulo,variabile,factory", TIPI_ASSEGNABILI,
                         ids=[t[0] for t in TIPI_ASSEGNABILI])
def test_ogni_carta_ha_almeno_un_destinatario(nome_tipo, modulo, variabile, factory):
    from conftest import SPEC_CARTE

    modulo_db = importlib.import_module(f"source.data_base_cards.{modulo}")
    database = getattr(modulo_db, variabile)
    costruisci = getattr(modulo_db, factory)
    spec = SPEC_CARTE[nome_tipo]

    orfane = []
    for chiave in database:
        carta = costruisci(chiave)
        if carta is None:
            continue
        if not any(spec.permesso(carta, guerriero) for _, guerriero in GUERRIERI):
            orfane.append(chiave)

    assert not orfane, (
        f"{nome_tipo}: {len(orfane)} carte su {len(database)} non sono assegnabili a "
        f"nessuno dei {len(GUERRIERI)} guerrieri del database — le loro restrizioni si "
        f"escludono a vicenda:\n  " + "\n  ".join(orfane)
    )


# --------------------------------------------------------------------------
# Le carte corrette dopo il confronto fra testo e vincoli
# --------------------------------------------------------------------------


def _ammessi_di(tipo, modulo, factory, nome_carta, metodo):
    from conftest import SPEC_CARTE

    modulo_db = importlib.import_module(f"source.data_base_cards.{modulo}")
    carta = getattr(modulo_db, factory)(nome_carta)
    assert carta is not None, f"{nome_carta} non è costruibile"
    spec = SPEC_CARTE[tipo]
    return {nome for nome, guerriero in GUERRIERI if spec.permesso(carta, guerriero)}


def test_lancia_castigator_solo_ai_doomtrooper():
    """
    «ASSEGNABILE AD OGNI DOOMTROOPER»: il vincolo stava solo nel testo. Fra i
    destinatari rientrano i Cultisti, che pur essendo dell'Oscura Legione si dichiarano
    «Doomtrooper senza legame».
    """
    ammessi = _ammessi_di("Equipaggiamento", "Database_Equipaggiamento",
                          "crea_equipaggiamento_da_database", "Lancia Castigator", None)
    fuori = {n for n in ammessi if not _vale_come_doomtrooper(n)}
    assert not fuori, f"la ricevono anche guerrieri non Doomtrooper: {sorted(fuori)}"
    assert ammessi


def test_addestramento_speciale_solo_doomtrooper_non_personalita():
    """«OGNI DOOMTROOPER NON PERSONALITÀ»: le due condizioni sono cumulative."""
    ammessi = _ammessi_di("Speciale", "Database_Speciale", "crea_carta_da_database",
                          "Addestramento Speciale", None)
    for nome in ammessi:
        dati = GUERRIERI_DATABASE[nome]
        assert _vale_come_doomtrooper(nome), f"{nome} non vale come Doomtrooper"
        assert dati.get("tipo") != "Personalita" and \
            "Personalita" not in (dati.get("keywords") or []), f"{nome} è una Personalità"
    assert ammessi


def test_reintegrato_solo_ai_mercenari():
    """
    «GIOCABILE SU UN MERCENARIO». La restrizione c'era ma diceva «Solo su Mercenari»,
    e in `Speciale` il ramo corrispondente non esisteva affatto — a differenza delle
    altre cinque classi, che lo hanno.
    """
    ammessi = _ammessi_di("Speciale", "Database_Speciale", "crea_carta_da_database",
                          "Reintegrato", None)
    attesi = {nome for nome, dati in GUERRIERI_DATABASE.items()
              if dati.get("fazione") == "Mercenario"
              or "Mercenario" in (dati.get("keywords") or [])}
    assert ammessi == attesi, (
        f"ammessi a torto: {sorted(ammessi - attesi)}; "
        f"respinti a torto: {sorted(attesi - ammessi)}")


def test_nato_fortunato_esclude_la_fratellanza():
    """
    «UN DOOMTROOPER, NON DELLA FRATELLANZA». `fazioni_permesse` è DOOMTROOPER, che la
    Fratellanza la comprende: a escluderla dev'essere la restrizione, che però era
    scritta in una forma che nessun ramo riconosce.
    """
    ammessi = _ammessi_di("Speciale", "Database_Speciale", "crea_carta_da_database",
                          "Nato Fortunato", None)
    attesi = {nome for nome, dati in GUERRIERI_DATABASE.items()
              if dati.get("fazione") in DOOMTROOPER
              and dati.get("fazione") != "Fratellanza"}
    assert ammessi == attesi, (
        f"ammessi a torto: {sorted(ammessi - attesi)}; "
        f"respinti a torto: {sorted(attesi - ammessi)}")


def test_furga_750_va_ai_mercenari_oppure_agli_eretici():
    """
    «ASSEGNABILE AD OGNI MERCENARIO O ERETICO». In `Equipaggiamento` il ramo «Solo
    Mercenari» era valutato prima di «Solo Mercenari o Eretici», di cui è il prefisso,
    e la condizione dell'alternativa era scritta come un cumulo: gli Eretici che non
    fossero anche Mercenari venivano respinti.
    """
    ammessi = _ammessi_di("Equipaggiamento", "Database_Equipaggiamento",
                          "crea_equipaggiamento_da_database", "Furga 750", None)
    attesi = {nome for nome, dati in GUERRIERI_DATABASE.items()
              if dati.get("fazione") == "Mercenario"
              or "Mercenario" in (dati.get("keywords") or [])
              or "Eretico" in (dati.get("keywords") or [])}
    assert ammessi == attesi, (
        f"ammessi a torto: {sorted(ammessi - attesi)}; "
        f"respinti a torto: {sorted(attesi - ammessi)}")


def test_cecchino_e_giocabile_su_qualsiasi_personalita():
    """
    «GIOCABILE SU QUALSIASI PERSONALITÀ». La restrizione «Solo Personalita» pretendeva
    che il guerriero fosse Personalità **sia** nel `tipo` **sia** nelle keyword, ma nel
    database 27 Personalità su 29 portano il solo `tipo` e nessuna la sola keyword: la
    carta arrivava a 2 guerrieri invece che a tutti.
    """
    modulo = importlib.import_module("source.data_base_cards.Database_Speciale")
    carta = modulo.crea_carta_da_database("Cecchino")
    assert carta is not None

    from conftest import SPEC_CARTE
    spec = SPEC_CARTE["Speciale"]
    ammessi = {nome for nome, guerriero in GUERRIERI if spec.permesso(carta, guerriero)}
    personalita = {nome for nome, dati in GUERRIERI_DATABASE.items()
                   if dati.get("tipo") == "Personalita"
                   or "Personalita" in (dati.get("keywords") or [])}

    assert ammessi == personalita, (
        f"ammessi a torto: {sorted(ammessi - personalita)}; "
        f"respinti a torto: {sorted(personalita - ammessi)}")


def test_le_personalita_del_database_si_dichiarano_soprattutto_col_tipo():
    """
    Il presupposto della semantica scelta, verificato sui dati: se un giorno le
    Personalità venissero marcate solo con la keyword, il `tipo` da solo non basterebbe
    più a riconoscerle e questa asimmetria andrebbe rivista.
    """
    solo_tipo = {nome for nome, dati in GUERRIERI_DATABASE.items()
                 if dati.get("tipo") == "Personalita"
                 and "Personalita" not in (dati.get("keywords") or [])}
    solo_keyword = {nome for nome, dati in GUERRIERI_DATABASE.items()
                    if dati.get("tipo") != "Personalita"
                    and "Personalita" in (dati.get("keywords") or [])}

    assert solo_tipo, "nessuna Personalità dichiarata col solo tipo: la semantica va rivista"
    assert not solo_keyword, (
        f"Personalità dichiarate con la sola keyword: {sorted(solo_keyword)}")


def _missione(nome):
    modulo = importlib.import_module("source.data_base_cards.Database_Missione")
    return modulo.crea_missione_da_database(nome)


def _ammessi(carta):
    return {nome for nome, guerriero in GUERRIERI
            if carta.puo_essere_associata_a(guerriero).get("puo_assegnare")}


# --------------------------------------------------------------------------


def test_una_missione_senza_vincoli_e_aperta_a_tutti():
    """Il metro di paragone: `Dimostra Il Tuo Valore` non dichiara alcun vincolo."""
    ammessi = _ammessi(_missione("Dimostra Il Tuo Valore"))
    assert len(ammessi) == len(GUERRIERI)


def test_quindici_minuti_di_fama_esclude_le_personalita_e_nessun_altro():
    """
    Il testo la assegna «a un tuo guerriero non personalita», senza vincolo di fazione.
    Il vincolo sta in `restrizioni_guerriero`, che `puo_essere_associata_a` non leggeva:
    finché è rimasto inerte la missione era assegnabile a chiunque, Personalità comprese.
    """
    ammessi = _ammessi(_missione("Quindici Minuti Di Fama"))
    personalita = {nome for nome, dati in GUERRIERI_DATABASE.items()
                   if dati.get("tipo") == "Personalita"
                   or "Personalita" in (dati.get("keywords") or [])}

    respinti = {nome for nome, _ in GUERRIERI} - ammessi
    assert respinti == personalita, (
        "la missione deve respingere tutte e sole le Personalità.\n"
        f"  respinte a torto: {sorted(respinti - personalita)}\n"
        f"  ammesse a torto : {sorted(personalita - respinti)}"
    )


@pytest.mark.parametrize("nome_missione,fazione_attesa", [
    ("Lotta Fraticida", "Imperiale"),
    ("Offesa Al Cardinale", "Fratellanza"),
    ("Assedio Alla Cittadella", "Imperiale"),
])
def test_le_missioni_di_corporazione_ammettono_solo_quella_fazione(nome_missione, fazione_attesa):
    """
    Il vincolo è retto da `fazioni_permesse`, non dalla stringa «Solo <corporazione>»
    che queste carte ripetono in `restrizioni` e che nessun ramo legge.
    """
    ammessi = _ammessi(_missione(nome_missione))
    fuori_fazione = {nome for nome in ammessi
                     if GUERRIERI_DATABASE[nome].get("fazione") != fazione_attesa}

    assert not fuori_fazione, (
        f"{nome_missione} è riservata a {fazione_attesa} ma la ricevono anche: "
        f"{sorted(fuori_fazione)}"
    )
    assert ammessi, f"{nome_missione} non è assegnabile a nessun guerriero"


def test_portale_del_grande_conquistatore_vuole_un_nefarita_seguace_di_algeroth():
    ammessi = _ammessi(_missione("Portale Del Grande Conquistatore"))
    for nome in ammessi:
        keywords = GUERRIERI_DATABASE[nome].get("keywords") or []
        assert "Nefarita" in keywords and "Seguace di Algeroth" in keywords, (
            f"{nome} riceve il Portale senza essere un Nefarita Seguace di Algeroth: {keywords}"
        )


# --------------------------------------------------------------------------
# I Cultisti
# --------------------------------------------------------------------------


CULTISTI = sorted(nome for nome in GUERRIERI_DATABASE if nome.startswith("Cultista di"))


def test_i_cultisti_sono_eretici_e_seguaci_del_proprio_apostolo():
    assert CULTISTI, "nessun Cultista nel database"
    for nome in CULTISTI:
        keywords = GUERRIERI_DATABASE[nome].get("keywords") or []
        apostolo = nome.removeprefix("Cultista di ")
        assert "Eretico" in keywords, f"{nome} non è marcato Eretico"
        assert f"Seguace di {apostolo}" in keywords, f"{nome} non è Seguace di {apostolo}"


def test_solo_i_guerrieri_dichiarati_eretici_hanno_la_keyword():
    """
    `Apostata Rinnegato` la portava per contaminazione dal nome simile: il suo testo dice
    che non ha Legame, non che è un Eretico. `Apostata` invece apre con «CONSIDERATO UN
    ERETICO». La keyword decide chi riceve le carte «Solo Eretici», quindi un falso
    positivo apre un varco silenzioso.
    """
    sospetti = []
    for nome, dati in GUERRIERI_DATABASE.items():
        if "Eretico" not in (dati.get("keywords") or []):
            continue
        # Vale come dichiarazione il testo della carta, il tipo, il nome stesso
        # (il guerriero «Eretico»), o l'essere un Cultista: il regolamento li
        # considera Eretici per definizione.
        dichiarato = ("eretico" in (dati.get("testo_carta") or "").lower()
                      or dati.get("tipo") == "Eretico"
                      or "Eretico" in nome
                      or nome.startswith("Cultista di"))
        if not dichiarato:
            sospetti.append(nome)

    assert not sospetti, (
        "guerrieri con la keyword «Eretico» che il testo della carta non dichiara tali: "
        f"{sospetti}"
    )


def test_cospirazione_eretica_ammette_doomtrooper_oppure_eretici():
    """
    «ASSEGNABILE AD UN DOOMTROOPER O AD UN ERETICO»: le due condizioni sono in
    alternativa. Erano due voci separate in `restrizioni`, che il consumatore valuta in
    AND — e nessun guerriero è insieme Doomtrooper ed Eretico, quindi la missione non
    era assegnabile a nessuno. È l'errore speculare a quello di `Quindici Minuti Di
    Fama`: là nessun vincolo mordeva, qui mordevano tutti.
    """
    ammessi = _ammessi(_missione("Cospirazione Eretica"))
    attesi = {nome for nome, dati in GUERRIERI_DATABASE.items()
              if dati.get("fazione") in DOOMTROOPER
              or "Eretico" in (dati.get("keywords") or [])}

    assert ammessi == attesi, (
        "devono riceverla tutti i Doomtrooper e tutti gli Eretici, e nessun altro.\n"
        f"  ammessi a torto : {sorted(ammessi - attesi)}\n"
        f"  respinti a torto: {sorted(attesi - ammessi)}"
    )


# --------------------------------------------------------------------------
# La deroga sull'Apostolo
# --------------------------------------------------------------------------


DONI_APERTI = ["Portale Della Cura Oscura", "Legame Necrovisuale"]


@pytest.mark.parametrize("nome_carta", DONI_APERTI)
def test_la_deroga_sull_apostolo_allarga_i_destinatari(nome_carta):
    """
    «DONO DI ALGEROTH. Può solo essere assegnato a un Nefarita di qualsiasi Apostolo»:
    il dono è di Algeroth, ma il destinatario non deve esserne Seguace. Il vincolo sul
    Seguace non viene dalle restrizioni ma da `tipo` + `apostolo_padre`, quindi togliere
    la stringa non basta: serve la deroga esplicita, ed è questo a verificarla.

    Prima della correzione la carta arrivava al solo `Valpurgius`, l'unico Nefarita che
    è anche Seguace di Algeroth.
    """
    modulo = importlib.import_module("source.data_base_cards.Database_Oscura_Simmetria")
    carta = modulo.crea_carta_da_database(nome_carta)
    assert carta is not None

    ammessi = {nome for nome, guerriero in GUERRIERI
               if carta.puo_essere_associata_a_guerriero(guerriero).get("puo_lanciare")}
    nefariti = {nome for nome, dati in GUERRIERI_DATABASE.items()
                if "Nefarita" in (dati.get("keywords") or [])}

    assert ammessi == nefariti, (
        "devono riceverla tutti i Nefariti, di qualsiasi Apostolo, e nessun altro.\n"
        f"  ammessi a torto : {sorted(ammessi - nefariti)}\n"
        f"  respinti a torto: {sorted(nefariti - ammessi)}"
    )

    apostoli = {a for nome in ammessi
                for keyword in (GUERRIERI_DATABASE[nome].get("keywords") or [])
                if keyword.startswith("Seguace di ")
                for a in [keyword.removeprefix("Seguace di ")]}
    assert len(apostoli) > 1, (
        f"i destinatari seguono un solo Apostolo ({apostoli}): la deroga «di qualsiasi "
        f"Apostolo» non sta facendo nulla"
    )


def test_gli_altri_doni_restano_vincolati_al_proprio_apostolo():
    """Il contro-verso: la deroga non deve aver allentato i Doni che non la dichiarano."""
    modulo = importlib.import_module("source.data_base_cards.Database_Oscura_Simmetria")
    database = modulo.DATABASE_OSCURA_SIMMETRIA

    verificati = 0
    for nome_carta, dati in database.items():
        if dati.get("tipo") != "Dono degli Apostoli":
            continue
        if "Dono di qualsiasi Apostolo" in (dati.get("restrizioni") or []):
            continue
        apostolo = dati.get("apostolo_padre")
        if not apostolo:
            continue

        carta = modulo.crea_carta_da_database(nome_carta)
        estraneo = crea_guerriero_da_nome("Nefarita di Semai" if apostolo != "Semai"
                                          else "Nefarita di Demnogonis")
        assert not carta.puo_essere_associata_a_guerriero(estraneo).get("puo_lanciare"), (
            f"{nome_carta} è un Dono di {apostolo} ma lo riceve {estraneo.nome}"
        )
        verificati += 1

    assert verificati > 20, f"verificati solo {verificati} Doni: il filtro è troppo stretto"


def test_i_cultisti_ricevono_cospirazione_eretica_in_quanto_eretici():
    """
    I Cultisti sono «Doomtrooper senza icona di legame» e il modello non sa
    rappresentare quella doppia natura — hanno una fazione sola, Oscura Legione. Per
    questa carta non serve: la ricevono come Eretici, che è ciò che il testo chiede.
    """
    ammessi = _ammessi(_missione("Cospirazione Eretica"))
    assert set(CULTISTI) <= ammessi, (
        f"Cultisti esclusi: {sorted(set(CULTISTI) - ammessi)}"
    )

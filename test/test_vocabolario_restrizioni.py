"""
Il vocabolario delle restrizioni è chiuso: ogni stringa nei database dev'essere
riconosciuta da chi la consuma, oppure dichiarata qui come nota descrittiva.

I campi di restrizione sono vocabolario controllato letto dal codice, non testo
libero: una stringa che nessun ramo riconosce viene ignorata in silenzio e la carta
si comporta come se non avesse alcun vincolo. Un refuso — «Solo Eretico» invece di
«Solo Eretici», «dall'Oscura Legione» invece di «dalla» — non produce alcun errore,
solo un permesso concesso a chi non ne ha diritto.

Questi test percorrono i database veri: aggiungere una carta con una restrizione
scritta in un modo nuovo fa fallire `test_ogni_restrizione_e_classificata`, che è
esattamente il momento in cui conviene accorgersene.
"""

import ast
import collections
import importlib
import pathlib

import pytest

from conftest import SPEC_CARTE, crea_guerriero
from source.cards.Guerriero import Fazione, TipoGuerriero

OL = Fazione.OSCURA_LEGIONE


# --------------------------------------------------------------------------
# Dove i database tengono le stringhe di restrizione
# --------------------------------------------------------------------------
#
# Il nome del campo nel database non sempre coincide con quello letto dal codice:
# Missione, ad esempio, popola sia `restrizioni` sia `corporazioni_specifiche`, che
# usano due vocabolari diversi.

ORIGINI = [
    ("Speciale", "Database_Speciale", "DATABASE_SPECIALI", "restrizioni"),
    ("Equipaggiamento", "Database_Equipaggiamento", "DATABASE_EQUIPAGGIAMENTO", "restrizioni_guerriero"),
    ("Fortificazione", "Database_Fortificazione", "DATABASE_FORTIFICAZIONI", "restrizioni"),
    ("Missione", "Database_Missione", "DATABASE_MISSIONI", "restrizioni"),
    ("Missione", "Database_Missione", "DATABASE_MISSIONI", "corporazioni_specifiche"),
    ("Missione", "Database_Missione", "DATABASE_MISSIONI", "restrizioni_guerriero"),
    ("Reliquia", "Database_Reliquia", "DATABASE_RELIQUIE", "corporazioni_specifiche"),
    ("Warzone", "Database_Warzone", "DATABASE_WARZONE", "limiti_utilizzo"),
    ("Oscura_Simmetria", "Database_Oscura_Simmetria", "DATABASE_OSCURA_SIMMETRIA", "restrizioni"),
]


def _raccogli(struttura, campo, trovate):
    if isinstance(struttura, dict):
        for chiave, valore in struttura.items():
            if chiave == campo and isinstance(valore, list):
                trovate.extend(v for v in valore if isinstance(v, str))
            else:
                _raccogli(valore, campo, trovate)
    elif isinstance(struttura, list):
        for valore in struttura:
            _raccogli(valore, campo, trovate)


def restrizioni_nel_database(modulo, variabile, campo):
    database = getattr(importlib.import_module(f"source.data_base_cards.{modulo}"), variabile)
    trovate = []
    _raccogli(database, campo, trovate)
    return collections.Counter(trovate)


# --------------------------------------------------------------------------
# Le tre classificazioni
# --------------------------------------------------------------------------

# Testo di regolamento che non vincola *chi* può ricevere la carta: effetti sul
# gioco, limiti di quante copie schierarne, condizioni sullo stato del turno. Che
# non abbiano effetto sul permesso di assegnazione è corretto.
NOTE_DESCRITTIVE = {
    # Speciale — effetti e condizioni di gioco
    "Non può entrare in combattimento",
    "Impedisce l'aggiunta di altri guerrieri",
    "Solo difensore",
    "Solo su guerrieri in copertura",
    "Solo guerrieri al coperto",
    "Solo con mitragliatrici",
    "Deve rispettare l'ICONA del destinatario",
    "Massimo una Corvè per volta in gioco",
    # Condizioni sullo schieramento, non sul destinatario della carta
    "Devi avere un guerriero della Fratellanza nella tua squadra",
    "Richiede Seguace di Algeroth nello schieramento",
    "Richiede guerriero della Fratellanza",
    # Fortificazione — effetti perduranti e limiti di schieramento
    "Non c'è limite al numero di complessi Industriali che puoi avere in gioco contemporaneamente",
    "Non c'è limite al numero di Industrie Belliche che puoi avere in gioco contemporaneamente",
    "Puoi introdurre in gioco un solo Nascondiglio",
    "Non può cominciare un combattimento Corpo a Corpo",
    "Non potrà attaccare i nemici in Corpo a Corpo",
    "Potrà difendersi",
    "Può essere mossa su un altro guerriero al costo di un'Azione",
    "Potrai spostare la barriera su un altro guerriero al costo di un'Azione",
    "I prigionieri non possono attaccare o essere attaccati",
    "Quando lo imprigioni tutte le carte assegnate o associate al guerriero vengono scartate",
    # Warzone — vincolano le carte giocabili nell'area, non il guerriero che la occupa
    "VEICOLI non utilizzabili",
    "Armi da FUOCO non utilizzabili",
    "Armi da FUOCO/CORPO A CORPO non utilizzabili",
}

# Stringhe che il consumatore non legge ma il cui vincolo è comunque imposto per
# un'altra via, verificata da `test_il_vincolo_sull_apostolo_regge_sul_database`.
# Sono ridondanti, non difetti: eliminarle non cambierebbe il comportamento.
RIDONDANTI = {
    ("Oscura_Simmetria", f"Solo Seguaci di {apostolo}"):
        "Oscura Simmetria impone l'apostolo con tipo=Dono degli Apostoli e apostolo_padre, "
        "non con questa stringa"
    for apostolo in ("Algeroth", "Semai", "Muawijhe", "Ilian", "Demnogonis")
}

# Missione: il vincolo di fazione è retto da `fazioni_permesse`, letto alla fine di
# `puo_essere_associata_a`, e quello sull'apostolo da `corporazioni_specifiche`. Le
# stringhe qui sotto ripetono nel campo `restrizioni` un vincolo già imposto altrove:
# `test_ogni_missione_impone_i_vincoli_che_dichiara` lo verifica carta per carta sul
# database reale. La stessa stringa può essere ridondante su una carta e fatale su
# un'altra — `Solo Doomtrooper` lo era su `Quindici Minuti Di Fama`, dove nessun altro
# campo lo reggeva — quindi il giudizio va dato per carta, non per stringa.
RIDONDANTI.update({
    ("Missione", "Solo Imperiale"): "fazioni_permesse = ['Imperiale']",
    ("Missione", "Solo Fratellanza"): "fazioni_permesse = ['Fratellanza']",
    ("Missione", "Solo Seguaci di Algeroth"):
        "corporazioni_specifiche = ['Seguace di Algeroth'] impone la keyword",
    ("Missione", "Imperiale"): "fazioni_permesse = ['Imperiale']",
})

# Stringhe che non restringono ma *allargano*: dichiarano che un vincolo imposto
# altrove non si applica a questa carta. Non respingono nessuno — è il loro scopo —
# quindi la prova «respinge almeno un guerriero» non vale per loro. Ognuna dev'essere
# coperta da un test che ne verifica l'effetto: qui sotto
# `test_la_deroga_sull_apostolo_allarga_i_destinatari`.
DEROGHE = {
    ("Oscura_Simmetria", "Dono di qualsiasi Apostolo"):
        "disattiva il vincolo sui Seguaci dell'Apostolo che concede il Dono",
}

# Stringhe che vincolano il destinatario ma che nessun ramo riconosce: la carta si
# comporta come se non avesse restrizioni. Sono difetti accertati, elencati qui con
# la loro causa. Vanno svuotati correggendo il dato o il codice, non allungati.
RESTRIZIONI_IGNORATE = {
    # Fazioni che il consumatore di Speciale non tratta: gestisce Fratellanza,
    # Doomtrooper e Oscura Legione, non le singole corporazioni.
    ("Speciale", "Solo Mishima"): "Speciale non riconosce le singole corporazioni",
    ("Speciale", "Solo Cybertronic"): "Speciale non riconosce le singole corporazioni",
    ("Speciale", "Non utilizzabile su membri Cybertronic"): "nessun ramo per le singole corporazioni",
    ("Speciale", "Non utilizzabile su membri della Fratellanza"):
        "il ramo esistente è «Non utilizzabile dalla Fratellanza»",
    ("Speciale", "Non utilizzabile dall'Oscura Legione"):
        "il ramo esistente è «Non utilizzabile dalla Oscura Legione»: differisce per «dall'» contro «dalla»",
    ("Speciale", "Seguaci di Demnogonis"): "il ramo esistente è «Solo Seguaci di», manca «Solo»",
    # Nomi di guerriero specifico: nessuna classe confronta il nome del destinatario.
    ("Equipaggiamento", "Tutore"): "nessun ramo confronta il nome del guerriero",
    ("Equipaggiamento", "Arcangelo"): "nessun ramo confronta il nome del guerriero",
}


# --------------------------------------------------------------------------
# Il banco di prova
# --------------------------------------------------------------------------
#
# Guerrieri abbastanza diversi da far scattare qualunque restrizione implementata:
# se nessuno di loro viene respinto, la stringa non ha alcun effetto.

def _banco(nome_classe):
    guerrieri = [
        crea_guerriero("eretico", OL, ["Eretico"]),
        crea_guerriero("nefarita", OL, ["Nefarita"]),
        crea_guerriero("necromutante", OL, ["Necromutante"]),
        crea_guerriero("seguace-algeroth", OL, ["Seguace di Algeroth"]),
        crea_guerriero("seguace-semai", OL, ["Seguace di Semai"]),
        crea_guerriero("seguace-muawijhe", OL, ["Seguace di Muawijhe"]),
        crea_guerriero("seguace-demnogonis", OL, ["Seguace di Demnogonis"]),
        crea_guerriero("seguace-ilian", OL, ["Seguace di Ilian"]),
        crea_guerriero("oscura-legione", OL),
        crea_guerriero("personalita-ol", OL, ["Personalita"], TipoGuerriero.PERSONALITA),
        crea_guerriero("valore-alto", OL, [], TipoGuerriero.NORMALE, 9),
    ]
    if nome_classe == "Oscura_Simmetria":
        # Le carte Oscura Simmetria respingono chiunque non sia Oscura Legione: un
        # banco con altre fazioni le farebbe sembrare attive per il motivo sbagliato.
        return guerrieri
    return guerrieri + [
        crea_guerriero("capitol", Fazione.CAPITOL),
        crea_guerriero("fratellanza", Fazione.FRATELLANZA),
        crea_guerriero("mishima", Fazione.MISHIMA),
        crea_guerriero("cybertronic", Fazione.CYBERTRONIC),
        crea_guerriero("imperiale", Fazione.IMPERIALE),
        crea_guerriero("comandante", Fazione.CAPITOL, ["Comandante"]),
        crea_guerriero("mercenario", Fazione.MERCENARIO, ["Mercenario"]),
        crea_guerriero("personalita", Fazione.CAPITOL, ["Personalita"], TipoGuerriero.PERSONALITA),
    ]


def ha_effetto(nome_classe, campo, restrizione):
    """True se almeno un guerriero del banco si vede negare il permesso."""
    spec = SPEC_CARTE[nome_classe]
    carta = spec.costruisci()
    contenitore = carta.restrizioni if spec.annidato else carta
    setattr(contenitore, campo, [restrizione])
    return any(not spec.permesso(carta, g) for g in _banco(nome_classe))


def _stringhe_nei_database():
    for nome_classe, modulo, variabile, campo in ORIGINI:
        for restrizione in sorted(restrizioni_nel_database(modulo, variabile, campo)):
            yield nome_classe, campo, restrizione


# --------------------------------------------------------------------------


def test_ogni_restrizione_e_classificata():
    """Nessuna stringa nei database sfugge alle tre liste di questo file."""
    non_classificate = []
    for nome_classe, campo, restrizione in _stringhe_nei_database():
        if restrizione in NOTE_DESCRITTIVE:
            continue
        if (nome_classe, restrizione) in RESTRIZIONI_IGNORATE:
            continue
        if (nome_classe, restrizione) in RIDONDANTI:
            continue
        if (nome_classe, restrizione) in DEROGHE:
            continue
        if not ha_effetto(nome_classe, campo, restrizione):
            non_classificate.append(f"{nome_classe}.{campo}: {restrizione!r}")

    assert not non_classificate, (
        "Restrizioni presenti nei database che nessun ramo del codice riconosce e che "
        "non sono dichiarate né descrittive né difetti noti. La carta si comporta come "
        "se non avesse vincoli:\n  " + "\n  ".join(non_classificate)
    )


@pytest.mark.parametrize("nome_classe,campo,restrizione", [
    pytest.param(nome_classe, campo, restrizione, id=f"{nome_classe}-{restrizione[:45]}")
    for nome_classe, campo, restrizione in _stringhe_nei_database()
    if restrizione not in NOTE_DESCRITTIVE
    and (nome_classe, restrizione) not in RESTRIZIONI_IGNORATE
    and (nome_classe, restrizione) not in RIDONDANTI
    and (nome_classe, restrizione) not in DEROGHE
])
def test_le_restrizioni_in_uso_hanno_effetto(nome_classe, campo, restrizione):
    """Ogni restrizione normativa dei database respinge almeno un guerriero."""
    assert ha_effetto(nome_classe, campo, restrizione), (
        f"{nome_classe}.{campo}: la restrizione {restrizione!r} non respinge nessuno "
        f"dei {len(_banco(nome_classe))} guerrieri del banco: è inerte"
    )


def _campo_di_origine(nome_classe, restrizione):
    """Il campo del database in cui quella classe dichiara quella restrizione."""
    for classe, modulo, variabile, campo in ORIGINI:
        if classe == nome_classe and restrizione in restrizioni_nel_database(
                modulo, variabile, campo):
            return campo
    raise LookupError(f"{restrizione!r} non compare in nessun campo di {nome_classe}")


@pytest.mark.parametrize("chiave,causa", sorted(RESTRIZIONI_IGNORATE.items()))
def test_i_difetti_noti_sono_ancora_tali(chiave, causa):
    """
    Sentinella sull'elenco dei difetti: quando uno viene corretto questo test fallisce
    e ricorda di toglierlo da RESTRIZIONI_IGNORATE, così l'elenco resta veritiero.
    """
    nome_classe, restrizione = chiave
    campo = _campo_di_origine(nome_classe, restrizione)
    assert not ha_effetto(nome_classe, campo, restrizione), (
        f"{nome_classe}: {restrizione!r} adesso ha effetto ({causa}). "
        f"Toglila da RESTRIZIONI_IGNORATE."
    )


def _doni_di_apostolo():
    """Le carte Oscura Simmetria che dichiarano «Solo Seguaci di X» fra le restrizioni."""
    from source.data_base_cards.Database_Oscura_Simmetria import DATABASE_OSCURA_SIMMETRIA

    for nome, dati in DATABASE_OSCURA_SIMMETRIA.items():
        for restrizione in dati.get("restrizioni") or []:
            if restrizione.startswith("Solo Seguaci di"):
                yield nome, restrizione.split("Solo Seguaci di ")[1].strip()
                break


@pytest.mark.parametrize("nome_carta,apostolo", sorted(_doni_di_apostolo()))
def test_il_vincolo_sull_apostolo_regge_sul_database(nome_carta, apostolo):
    """
    La stringa «Solo Seguaci di X» è ridondante solo se `apostolo_padre` impone già il
    vincolo. Se un dono perdesse il tipo o l'apostolo, la stringa non lo salverebbe:
    questo test lo verifica sulla carta vera, non su una costruita per l'occasione.
    """
    from source.data_base_cards.Database_Oscura_Simmetria import DATABASE_OSCURA_SIMMETRIA, crea_carta_da_database

    carta = crea_carta_da_database(nome_carta)
    assert carta is not None, f"{nome_carta}: la carta non è costruibile dal database"

    # Alcune carte cumulano un secondo requisito (es. anche Nefarita): il guerriero
    # ammesso deve soddisfarli tutti, altrimenti il caso positivo fallisce per un
    # motivo diverso da quello sotto esame.
    altre = [r for r in DATABASE_OSCURA_SIMMETRIA[nome_carta].get("restrizioni") or []
             if not r.startswith("Solo Seguaci di")]
    keyword_extra = [k for k in ("Eretico", "Nefarita") if f"Solo {k}" in altre]

    altro_apostolo = "Ilian" if apostolo != "Ilian" else "Semai"
    ammesso = crea_guerriero("ammesso", OL, [f"Seguace di {apostolo}"] + keyword_extra)
    respinto = crea_guerriero("respinto", OL, [f"Seguace di {altro_apostolo}"] + keyword_extra)

    assert carta.puo_essere_associata_a_guerriero(ammesso).get("puo_lanciare"), (
        f"{nome_carta}: un Seguace di {apostolo} non può riceverla"
    )
    assert not carta.puo_essere_associata_a_guerriero(respinto).get("puo_lanciare"), (
        f"{nome_carta}: la riceve anche un Seguace di {altro_apostolo}, "
        f"quindi il vincolo sull'apostolo non è imposto da nessuna delle due vie"
    )


# --------------------------------------------------------------------------
# Campi popolati nei dati che nessun metodo di permesso legge
# --------------------------------------------------------------------------
#
# Un gradino sopra la singola stringa: se il consumatore non legge affatto il campo,
# ogni stringa che ci finisce dentro è inerte per costruzione. È così che il vincolo
# «Non Personalita» di `Quindici Minuti Di Fama` è rimasto senza effetto.

# Il metodo che decide il permesso, per ciascuna classe.
METODO_DI_PERMESSO = {
    "Speciale": "puo_essere_assegnato_a_guerriero",
    "Equipaggiamento": "puo_essere_assegnato_a_guerriero",
    "Fortificazione": "puo_essere_assegnato_a_guerriero",
    "Missione": "puo_essere_associata_a",
    "Reliquia": "puo_essere_associata_a_guerriero",
    "Warzone": "puo_essere_associata_a_guerriero",
    "Arte": "puo_essere_associata_a_guerriero",
    "Oscura_Simmetria": "puo_essere_associata_a_guerriero",
}

CAMPI_DI_RESTRIZIONE = ["restrizioni", "restrizioni_guerriero", "corporazioni_specifiche",
                        "limiti_utilizzo", "fazioni_permesse", "limitazioni"]

# `limitazioni` non sta al livello della carta ma dentro i singoli `poteri[N]` e
# `abilita_speciali[N]`: limita *quel* potere, non l'assegnazione della carta. Che il
# metodo di permesso non lo legga è corretto — quelle condizioni («Solo contro
# guerrieri dell'Oscura Legione», «Solo se assegnata a un Cardinale») sono materia di
# un motore di gioco, che questo progetto non ha: costruisce collezioni e mazzi, non
# simula partite. Le 189 carte che lo popolano non sono quindi 189 difetti.
CAMPI_NON_LETTI_ACCETTATI = {
    (classe, "limitazioni")
    for classe in ("Speciale", "Equipaggiamento", "Reliquia", "Arte", "Oscura_Simmetria")
}


def _campi_letti_dal_metodo(nome_classe):
    """Gli attributi che il metodo di permesso legge davvero, presi dall'albero sintattico."""
    import ast

    percorso = (pathlib.Path(__file__).resolve().parents[1]
                / "source" / "cards" / f"{nome_classe}.py")
    albero = ast.parse(percorso.read_text(encoding="utf-8"))
    metodo = METODO_DI_PERMESSO[nome_classe]
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.FunctionDef) and nodo.name == metodo:
            return {n.attr for n in ast.walk(nodo) if isinstance(n, ast.Attribute)}
    raise LookupError(f"{nome_classe} non ha il metodo {metodo}")


def _campi_popolati(nome_classe):
    origini = {(classe, modulo, variabile) for classe, modulo, variabile, _ in ORIGINI
               if classe == nome_classe}
    if not origini:
        return {}
    _, modulo, variabile = next(iter(origini))
    popolati = {}
    for campo in CAMPI_DI_RESTRIZIONE:
        quante = sum(restrizioni_nel_database(modulo, variabile, campo).values())
        if quante:
            popolati[campo] = quante
    return popolati


@pytest.mark.parametrize("nome_classe", sorted(METODO_DI_PERMESSO))
def test_nessun_campo_di_restrizione_resta_non_letto(nome_classe):
    if nome_classe not in {classe for classe, _, _, _ in ORIGINI}:
        pytest.skip(f"{nome_classe} non dichiara restrizioni nei dati")

    letti = _campi_letti_dal_metodo(nome_classe)
    ignorati = [
        f"{campo} ({quante} stringhe)"
        for campo, quante in _campi_popolati(nome_classe).items()
        if campo not in letti and (nome_classe, campo) not in CAMPI_NON_LETTI_ACCETTATI
    ]
    assert not ignorati, (
        f"{nome_classe}.{METODO_DI_PERMESSO[nome_classe]}() non legge campi che il "
        f"database popola, quindi il loro contenuto è inerte: {ignorati}"
    )


def test_l_elenco_dei_difetti_non_contiene_voci_scomparse():
    """Se una carta difettosa viene corretta nel database, l'elenco va ripulito."""
    presenti = {(nome_classe, restrizione)
                for nome_classe, _, restrizione in _stringhe_nei_database()}
    scomparse = sorted((set(RESTRIZIONI_IGNORATE) | set(RIDONDANTI) | set(DEROGHE))
                       - presenti)
    assert not scomparse, (
        "Voci di RESTRIZIONI_IGNORATE o RIDONDANTI che non compaiono più in nessun "
        f"database: {scomparse}"
    )

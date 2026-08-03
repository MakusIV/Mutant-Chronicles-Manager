"""
Le restrizioni di assegnazione: per ognuna, il caso positivo *e* quello negativo.

Tutti e sette i difetti di §10.9 avevano la stessa forma — il permesso valeva True
qualunque fosse il guerriero — e sarebbero caduti al primo caso negativo. Ogni test
qui sotto verifica entrambi i versi su una coppia di guerrieri che differiscono per
la sola caratteristica sotto esame.
"""

import pytest

from conftest import SPEC_CARTE, crea_guerriero
from source.cards.Guerriero import Fazione, TipoGuerriero

OL = Fazione.OSCURA_LEGIONE
CAPITOL = Fazione.CAPITOL
FRATELLANZA = Fazione.FRATELLANZA
MERCENARIO = Fazione.MERCENARIO


class Caso:
    """Una restrizione con la coppia di guerrieri che la mette alla prova."""

    def __init__(self, restrizione, ammesso, respinto, classi):
        self.restrizione = restrizione
        self.ammesso = ammesso      # deve ottenere il permesso
        self.respinto = respinto    # deve vederselo negare
        self.classi = classi        # classi carta che dichiarano di supportarla

    def __repr__(self):
        return self.restrizione


# Le classi che condividono il vocabolario di restrizioni a stringa. Oscura_Simmetria
# non è nell'elenco: usa un vocabolario proprio ed è verificata più sotto.
TUTTE = ["Speciale", "Equipaggiamento", "Fortificazione", "Reliquia", "Warzone"]

CASI = [
    Caso("Solo Eretici",
         dict(fazione=OL, keywords=["Eretico"]),
         dict(fazione=OL, keywords=[]),
         TUTTE),
    Caso("Solo Comandanti",
         dict(keywords=["Comandante"]),
         dict(keywords=[]),
         TUTTE),
    Caso("Solo Nefariti",
         dict(fazione=OL, keywords=["Nefarita"]),
         dict(fazione=OL, keywords=[]),
         TUTTE),
    # La coppia distingue due seguaci di apostoli diversi: se il confronto ignorasse
    # il nome dell'apostolo il test resterebbe verde con un guerriero senza keyword.
    Caso("Solo Seguaci di Algeroth",
         dict(fazione=OL, keywords=["Seguace di Algeroth"]),
         dict(fazione=OL, keywords=["Seguace di Semai"]),
         TUTTE),
    Caso("Solo Doomtrooper",
         dict(fazione=CAPITOL),
         dict(fazione=OL),
         TUTTE),
    Caso("Solo Oscura Legione",
         dict(fazione=OL),
         dict(fazione=CAPITOL),
         TUTTE),
    Caso("Solo Mercenari",
         dict(fazione=MERCENARIO, keywords=["Mercenario"]),
         dict(fazione=MERCENARIO, keywords=[]),
         ["Equipaggiamento", "Fortificazione", "Reliquia", "Warzone"]),
    # Va riconosciuta prima di "Solo Mercenari", di cui contiene il prefisso.
    Caso("Solo Mercenari o Eretici",
         dict(fazione=MERCENARIO, keywords=["Mercenario"]),
         dict(fazione=CAPITOL, keywords=[]),
         ["Equipaggiamento", "Fortificazione", "Reliquia", "Warzone", "Missione"]),
    Caso("Solo Personalita",
         dict(keywords=["Personalita"], tipo=TipoGuerriero.PERSONALITA),
         dict(keywords=[], tipo=TipoGuerriero.NORMALE),
         ["Speciale", "Equipaggiamento", "Fortificazione", "Reliquia", "Missione", "Warzone"]),
    Caso("Solo Fratellanza",
         dict(fazione=FRATELLANZA),
         dict(fazione=CAPITOL),
         ["Speciale"]),
    Caso("Solo Necromutanti",
         dict(fazione=OL, keywords=["Necromutante"]),
         dict(fazione=OL, keywords=[]),
         ["Speciale"]),
    Caso("Non utilizzabile da Personalita",
         dict(keywords=[], tipo=TipoGuerriero.NORMALE),
         dict(keywords=["Personalita"], tipo=TipoGuerriero.PERSONALITA),
         ["Speciale"]),
    Caso("Solo Nefarita",
         dict(fazione=OL, keywords=["Nefarita"]),
         dict(fazione=OL, keywords=[]),
         ["Missione"]),
]


# Difetti accertati, non attese sbagliate: il test resta scritto nel verso giusto e
# fallirà quando smetterà di fallire, così la correzione non passa inosservata.
# Vuoto: l'ultimo — `Warzone.py` usava `TipoGuerriero` senza importarlo — è stato
# corretto, e la restrizione «Solo Personalita» ora vale anche lì.
DIFETTI_NOTI: dict[tuple, str] = {}


def _parametri():
    for caso in CASI:
        for nome_classe in caso.classi:
            marcatori = []
            motivo = DIFETTI_NOTI.get((nome_classe, caso.restrizione))
            if motivo:
                marcatori.append(pytest.mark.xfail(strict=True, reason=motivo))
            yield pytest.param(nome_classe, caso, id=f"{nome_classe}-{caso.restrizione}",
                               marks=marcatori)


@pytest.mark.parametrize("nome_classe,caso", list(_parametri()))
def test_restrizione_concede_al_giusto_e_nega_agli_altri(nome_classe, caso):
    spec = SPEC_CARTE[nome_classe]
    carta = spec.costruisci(caso.restrizione)

    ammesso = crea_guerriero(nome="ammesso", **caso.ammesso)
    respinto = crea_guerriero(nome="respinto", **caso.respinto)

    assert spec.permesso(carta, ammesso), (
        f"{nome_classe} con «{caso.restrizione}» nega il permesso a un guerriero "
        f"che la soddisfa ({caso.ammesso})"
    )
    assert not spec.permesso(carta, respinto), (
        f"{nome_classe} con «{caso.restrizione}» concede il permesso a un guerriero "
        f"che non la soddisfa ({caso.respinto}): la restrizione è inerte"
    )


CLASSI_CON_SOLO_PERSONALITA = ["Speciale", "Equipaggiamento", "Fortificazione",
                               "Reliquia", "Missione", "Warzone"]

# Le tre forme in cui un guerriero può risultare Personalità, più il caso negativo.
# Nel database 27 Personalità su 29 portano il solo `tipo` e nessuna la sola keyword:
# pretendere entrambe le dichiarazioni lascerebbe fuori quasi tutte.
DICHIARAZIONI_PERSONALITA = [
    ("tipo e keyword", dict(keywords=["Personalita"], tipo=TipoGuerriero.PERSONALITA), True),
    ("il solo tipo", dict(keywords=[], tipo=TipoGuerriero.PERSONALITA), True),
    ("la sola keyword", dict(keywords=["Personalita"], tipo=TipoGuerriero.NORMALE), True),
    ("nessuna delle due", dict(keywords=[], tipo=TipoGuerriero.NORMALE), False),
]


@pytest.mark.parametrize("nome_classe", CLASSI_CON_SOLO_PERSONALITA)
@pytest.mark.parametrize("forma,caratteristiche,ammesso",
                         DICHIARAZIONI_PERSONALITA,
                         ids=[d[0] for d in DICHIARAZIONI_PERSONALITA])
def test_solo_personalita_basta_una_delle_due_dichiarazioni(nome_classe, forma,
                                                            caratteristiche, ammesso):
    """
    «Solo Personalita» ammette chi è Personalità per il `tipo` **oppure** per la keyword.
    Pretenderle entrambe rendeva `Cecchino` — «GIOCABILE SU QUALSIASI PERSONALITÀ» —
    assegnabile a 2 guerrieri su 29.
    """
    spec = SPEC_CARTE[nome_classe]
    carta = spec.costruisci("Solo Personalita")
    guerriero = crea_guerriero(nome=forma, **caratteristiche)

    assert spec.permesso(carta, guerriero) is ammesso, (
        f"{nome_classe}: un guerriero che dichiara {forma} dovrebbe "
        f"{'essere ammesso' if ammesso else 'essere respinto'}")


@pytest.mark.parametrize("forma,caratteristiche,e_personalita",
                         DICHIARAZIONI_PERSONALITA,
                         ids=[d[0] for d in DICHIARAZIONI_PERSONALITA])
def test_non_utilizzabile_da_personalita_esclude_con_le_stesse_forme(forma, caratteristiche,
                                                                    e_personalita):
    """
    Il verso opposto dev'essere simmetrico, altrimenti un guerriero che dichiara la
    Personalità in un modo solo verrebbe respinto da entrambe le carte: troppo poco
    Personalità per quelle riservate, troppo per quelle che la escludono.
    """
    spec = SPEC_CARTE["Speciale"]
    carta = spec.costruisci("Non utilizzabile da Personalita")
    guerriero = crea_guerriero(nome=forma, **caratteristiche)

    assert spec.permesso(carta, guerriero) is not e_personalita, (
        f"un guerriero che dichiara {forma} dovrebbe "
        f"{'essere respinto' if e_personalita else 'essere ammesso'}")


@pytest.mark.parametrize("nome_classe", TUTTE + ["Missione"])
def test_carta_senza_restrizioni_e_assegnabile_a_chiunque(nome_classe):
    """Il verso complementare: senza restrizioni non si nega niente a nessuno."""
    spec = SPEC_CARTE[nome_classe]
    carta = spec.costruisci()
    for fazione in (CAPITOL, OL, FRATELLANZA, MERCENARIO):
        guerriero = crea_guerriero(fazione=fazione)
        assert spec.permesso(carta, guerriero), (
            f"{nome_classe} senza restrizioni rifiuta un guerriero {fazione.value}"
        )


# --------------------------------------------------------------------------
# Il limite sul Valore: l'unica restrizione con un confine numerico
# --------------------------------------------------------------------------


@pytest.mark.parametrize("nome_classe",
                         ["Speciale", "Equipaggiamento", "Fortificazione", "Reliquia",
                          "Warzone", "Missione"])
@pytest.mark.parametrize("limite", [3, 4, 6])
def test_limite_di_valore_include_il_confine(nome_classe, limite):
    """«V <= N» ammette esattamente N ed esclude N+1: l'errore classico è l'off-by-one."""
    spec = SPEC_CARTE[nome_classe]
    carta = spec.costruisci(f"Assegnabile a guerrieri con V <= {limite}")

    assert spec.permesso(carta, crea_guerriero(valore=limite)), (
        f"{nome_classe}: «V <= {limite}» esclude un guerriero di valore {limite}"
    )
    assert spec.permesso(carta, crea_guerriero(valore=limite - 1)), (
        f"{nome_classe}: «V <= {limite}» esclude un guerriero di valore {limite - 1}"
    )
    assert not spec.permesso(carta, crea_guerriero(valore=limite + 1)), (
        f"{nome_classe}: «V <= {limite}» ammette un guerriero di valore {limite + 1}"
    )


# --------------------------------------------------------------------------
# Oscura Simmetria: vocabolario proprio
# --------------------------------------------------------------------------
#
# Il vincolo sull'apostolo non passa dalle stringhe di restrizione ma da
# `tipo = DONO_APOSTOLO` più `apostolo_padre`. Va esercitato per quella via.


def _dono(tipo=None, apostolo=None, restrizioni=()):
    from source.cards.Guerriero import ApostoloOscuraSimmetria, TipoOscuraSimmetria

    carta = SPEC_CARTE["Oscura_Simmetria"].costruisci(*restrizioni)
    if tipo is not None:
        carta.tipo = getattr(TipoOscuraSimmetria, tipo)
    if apostolo is not None:
        carta.apostolo_padre = getattr(ApostoloOscuraSimmetria, apostolo)
    return carta


def _puo_lanciare(carta, guerriero):
    return SPEC_CARTE["Oscura_Simmetria"].permesso(carta, guerriero)


def test_oscura_simmetria_solo_oscura_legione():
    carta = _dono()
    assert _puo_lanciare(carta, crea_guerriero(fazione=OL))
    assert not _puo_lanciare(carta, crea_guerriero(fazione=CAPITOL))
    assert not _puo_lanciare(carta, crea_guerriero(fazione=FRATELLANZA))


def test_dono_di_apostolo_solo_ai_suoi_seguaci():
    carta = _dono(tipo="DONO_APOSTOLO", apostolo="ALGEROTH")
    assert _puo_lanciare(carta, crea_guerriero(fazione=OL, keywords=["Seguace di Algeroth"]))
    # Seguace, ma di un altro apostolo: è il caso negativo che conta.
    assert not _puo_lanciare(carta, crea_guerriero(fazione=OL, keywords=["Seguace di Semai"]))
    assert not _puo_lanciare(carta, crea_guerriero(fazione=OL, keywords=[]))


def test_chi_riceve_ogni_dono_ignora_l_apostolo():
    """L'eccezione dichiarata con un'abilità «Dono degli Apostoli» (es. Billy)."""
    from source.cards.Guerriero import Abilita

    carta = _dono(tipo="DONO_APOSTOLO", apostolo="ALGEROTH")
    billy = crea_guerriero(
        fazione=OL, keywords=[],
        abilita=[Abilita(nome="Doni", descrizione="Riceve i Doni di ogni Apostolo",
                         tipo="Dono degli Apostoli")])
    assert _puo_lanciare(carta, billy)


@pytest.mark.parametrize("restrizione,keyword_ammessa", [
    ("Solo Eretici", "Eretico"),
    ("Solo Nefarita", "Nefarita"),
])
def test_oscura_simmetria_restrizioni_per_keyword(restrizione, keyword_ammessa):
    carta = _dono(restrizioni=[restrizione])
    assert _puo_lanciare(carta, crea_guerriero(fazione=OL, keywords=[keyword_ammessa]))
    assert not _puo_lanciare(carta, crea_guerriero(fazione=OL, keywords=[]))


def test_oscura_simmetria_esclude_le_personalita():
    carta = _dono(restrizioni=["Non può essere usato su Personalita"])
    assert _puo_lanciare(carta, crea_guerriero(fazione=OL, tipo=TipoGuerriero.NORMALE))
    assert not _puo_lanciare(
        carta, crea_guerriero(fazione=OL, tipo=TipoGuerriero.PERSONALITA))


def test_guerriero_vincolato_ai_soli_doni_degli_apostoli():
    """Chi dichiara «Solo doni degli Apostoli» non può ricevere i doni generici."""
    vincolato = crea_guerriero(fazione=OL, restrizioni=["Solo doni degli Apostoli"])
    libero = crea_guerriero(fazione=OL)

    generico = _dono(tipo="GENERICA")
    assert _puo_lanciare(generico, libero)
    assert not _puo_lanciare(generico, vincolato)

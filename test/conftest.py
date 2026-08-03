"""
Impalcatura comune della suite.

Il principio che regge tutti i test di restrizione: **una coppia per volta**.
Per ogni restrizione si costruiscono due guerrieri che differiscono per la sola
caratteristica sotto esame — uno che la soddisfa e uno che non la soddisfa — e si
verifica che il permesso sia rispettivamente concesso e negato. Confrontare un
guerriero ammesso con uno respinto per *altri* motivi (la fazione sbagliata, ad
esempio) darebbe un test verde che non sta misurando nulla: è il modo in cui i
difetti di §10.9 sono passati inosservati, perché il permesso valeva sempre True.
"""

import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from source.cards.Guerriero import Fazione, Guerriero, TipoGuerriero  # noqa: E402


# --------------------------------------------------------------------------
# Guerrieri sintetici
# --------------------------------------------------------------------------
#
# Volutamente non presi dal database: un guerriero reale porta con sé keyword,
# abilità e fazione che il test non controlla, e basta che il database cambi
# perché un test superato inizi a misurare un'altra cosa.


def crea_guerriero(nome="Cavia", fazione=Fazione.CAPITOL, keywords=None,
                   tipo=TipoGuerriero.NORMALE, valore=1, restrizioni=None,
                   abilita=None):
    """Guerriero con le sole caratteristiche che il test dichiara."""
    g = Guerriero(nome, fazione, combattimento=1, sparare=1, armatura=1, valore=valore)
    g.keywords = list(keywords or [])
    g.tipo = tipo
    g.restrizioni = list(restrizioni or [])
    g.abilita = list(abilita or [])
    return g


@pytest.fixture
def guerriero():
    """La factory, per i test che ne costruiscono più di uno."""
    return crea_guerriero


# --------------------------------------------------------------------------
# Dove ciascuna classe carta tiene le proprie restrizioni
# --------------------------------------------------------------------------
#
# Il campo non è lo stesso ovunque: è la conseguenza della logica duplicata in sei
# classi invece che raccolta in un modulo condiviso. La tabella la rende esplicita,
# e serve anche da inventario di ciò che andrà unificato in `regole_associazione.py`.


class SpecCarta:
    """Come si costruisce una carta di un tipo e come le si chiede il permesso."""

    def __init__(self, nome, modulo, classe, campo, metodo, chiave, annidato=False):
        self.nome = nome
        self.modulo = modulo
        self.classe = classe
        self.campo = campo          # attributo che contiene le stringhe di restrizione
        self.metodo = metodo        # metodo che concede o nega il permesso
        self.chiave = chiave        # chiave del dizionario restituito
        self.annidato = annidato    # True se il campo sta dentro self.restrizioni

    def costruisci(self, *restrizioni):
        """Una carta nuda che porta solo le restrizioni indicate."""
        modulo = __import__(self.modulo, fromlist=["x"])
        carta = getattr(modulo, self.classe)("Carta di prova")
        contenitore = carta.restrizioni if self.annidato else carta
        setattr(contenitore, self.campo, list(restrizioni))
        return carta

    def permesso(self, carta, guerriero):
        """True se la carta può essere assegnata/associata al guerriero."""
        return bool(getattr(carta, self.metodo)(guerriero).get(self.chiave, False))

    def __repr__(self):
        return self.nome


SPEC_CARTE = {
    s.nome: s
    for s in [
        SpecCarta("Speciale", "source.cards.Speciale", "Speciale",
                  "restrizioni", "puo_essere_assegnato_a_guerriero", "puo_assegnare"),
        SpecCarta("Equipaggiamento", "source.cards.Equipaggiamento", "Equipaggiamento",
                  "restrizioni_guerriero", "puo_essere_assegnato_a_guerriero", "puo_assegnare"),
        SpecCarta("Fortificazione", "source.cards.Fortificazione", "Fortificazione",
                  "restrizioni", "puo_essere_assegnato_a_guerriero", "puo_assegnare"),
        SpecCarta("Missione", "source.cards.Missione", "Missione",
                  "restrizioni", "puo_essere_associata_a", "puo_assegnare"),
        SpecCarta("Reliquia", "source.cards.Reliquia", "Reliquia",
                  "corporazioni_specifiche", "puo_essere_associata_a_guerriero",
                  "puo_assegnare", annidato=True),
        SpecCarta("Warzone", "source.cards.Warzone", "Warzone",
                  "limiti_utilizzo", "puo_essere_associata_a_guerriero",
                  "puo_assegnare", annidato=True),
        SpecCarta("Oscura_Simmetria", "source.cards.Oscura_Simmetria", "Oscura_Simmetria",
                  "restrizioni", "puo_essere_associata_a_guerriero", "puo_lanciare"),
    ]
}


# --------------------------------------------------------------------------
# I database, per i test che li percorrono per intero
# --------------------------------------------------------------------------


DATABASE = [
    ("Arte", "source.data_base_cards.Database_Arte", "CARTE_ARTE_DATABASE",
     "source.cards.Arte", "Arte"),
    ("Speciale", "source.data_base_cards.Database_Speciale", "DATABASE_SPECIALI",
     "source.cards.Speciale", "Speciale"),
    ("Oscura_Simmetria", "source.data_base_cards.Database_Oscura_Simmetria", "DATABASE_OSCURA_SIMMETRIA",
     "source.cards.Oscura_Simmetria", "Oscura_Simmetria"),
    ("Fortificazione", "source.data_base_cards.Database_Fortificazione", "DATABASE_FORTIFICAZIONI",
     "source.cards.Fortificazione", "Fortificazione"),
    ("Reliquia", "source.data_base_cards.Database_Reliquia", "DATABASE_RELIQUIE",
     "source.cards.Reliquia", "Reliquia"),
    ("Missione", "source.data_base_cards.Database_Missione", "DATABASE_MISSIONI",
     "source.cards.Missione", "Missione"),
    ("Equipaggiamento", "source.data_base_cards.Database_Equipaggiamento", "DATABASE_EQUIPAGGIAMENTO",
     "source.cards.Equipaggiamento", "Equipaggiamento"),
    ("Warzone", "source.data_base_cards.Database_Warzone", "DATABASE_WARZONE",
     "source.cards.Warzone", "Warzone"),
    ("Guerriero", "source.data_base_cards.Database_Guerriero", "GUERRIERI_DATABASE",
     "source.cards.Guerriero", "Guerriero"),
]


def carica_database(nome_modulo, nome_variabile):
    return getattr(__import__(nome_modulo, fromlist=["x"]), nome_variabile)


def carica_classe(nome_modulo, nome_classe):
    return getattr(__import__(nome_modulo, fromlist=["x"]), nome_classe)

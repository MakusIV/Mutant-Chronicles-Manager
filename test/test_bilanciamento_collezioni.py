"""
Bilanciamento tra le collezioni dei giocatori.

Prima di questa correzione `seleziona_carte_casuali_per_tipo` non applicava alcun
tetto alle carte non fondamentali: il pool si riduceva a ogni giocatore elaborato,
quindi i primi ricevevano sistematicamente piu' carte degli ultimi (misurato:
squilibrio di 293-338 carte su 3 giocatori, semi fissi). Le Missioni erano il caso
peggiore: con una decina di copie totali, il sorteggio lasciava spesso un giocatore
a zero missioni.

I due gruppi di test sotto isolano le due correzioni separatamente (con database
finti, cosi' un cambiamento ai Database_*.py reali non altera cosa viene misurato)
e poi una verifica di integrazione sul database vero, a riprova che il collegamento
tra le parti funzioni davvero.
"""

import contextlib
import io
import random
from types import SimpleNamespace

import pytest

from source.cards.Guerriero import Set_Espansione
from source.logic import Creatore_Collezione as CC


# --------------------------------------------------------------------------
# distribuisci_missioni_round_robin
# --------------------------------------------------------------------------

class MissioneFinta:
    def __init__(self, nome):
        self.nome = nome


DB_MISSIONI_FINTO = {
    f"Missione {i}": {"set_espansione": "Base", "quantita": 1} for i in range(11)
}


@pytest.fixture
def missioni_finte(monkeypatch):
    monkeypatch.setattr(CC, "DATABASE_MISSIONI", DB_MISSIONI_FINTO)
    monkeypatch.setattr(CC, "crea_missione_da_database", lambda nome: MissioneFinta(nome))
    CC.resetta_tracciamento_quantita()


@pytest.mark.parametrize("numero_giocatori", [2, 3, 4, 5, 11, 12])
def test_missioni_scarto_massimo_di_una_tra_giocatori(missioni_finte, numero_giocatori):
    random.seed(numero_giocatori)  # un seme diverso per configurazione, non per fragilita'
    risultato = CC.distribuisci_missioni_round_robin(numero_giocatori, [Set_Espansione.BASE])
    conteggi = [len(v) for v in risultato.values()]
    assert len(conteggi) == numero_giocatori
    assert max(conteggi) - min(conteggi) <= 1


def test_missioni_distribuisce_tutto_il_pool_disponibile(missioni_finte):
    random.seed(0)
    risultato = CC.distribuisci_missioni_round_robin(3, [Set_Espansione.BASE])
    assert sum(len(v) for v in risultato.values()) == 11


def test_missioni_nessun_giocatore_a_zero_se_il_pool_basta(missioni_finte):
    random.seed(0)
    # 11 missioni per 5 giocatori: il pool basta per darne almeno una a ciascuno.
    risultato = CC.distribuisci_missioni_round_robin(5, [Set_Espansione.BASE])
    assert all(len(v) >= 1 for v in risultato.values())


def test_missioni_ignora_le_espansioni_non_richieste(monkeypatch):
    monkeypatch.setattr(CC, "DATABASE_MISSIONI",
                         {"Solo Warzone": {"set_espansione": "Warzone", "quantita": 5}})
    monkeypatch.setattr(CC, "crea_missione_da_database", lambda nome: MissioneFinta(nome))
    CC.resetta_tracciamento_quantita()
    random.seed(0)
    risultato = CC.distribuisci_missioni_round_robin(3, [Set_Espansione.BASE])
    assert all(len(v) == 0 for v in risultato.values())


def test_missioni_tiene_conto_delle_copie_gia_utilizzate(missioni_finte):
    CC.utilizza_carta("Missione 0", 1)  # una copia gia' consumata altrove
    random.seed(0)
    risultato = CC.distribuisci_missioni_round_robin(3, [Set_Espansione.BASE])
    assert sum(len(v) for v in risultato.values()) == 10


# --------------------------------------------------------------------------
# Opzione B: quantita' per le carte non fondamentali in seleziona_carte_casuali_per_tipo
# --------------------------------------------------------------------------

DB_CARTA_FINTA = {
    "Carta Unica": {"set_espansione": "Base", "quantita": 20, "fondamentale": False},
}


def crea_carta_finta(nome):
    return SimpleNamespace(nome=nome)


def test_quantita_non_supera_mai_il_tetto_di_collezione():
    random.seed(0)
    for _ in range(30):
        CC.resetta_tracciamento_quantita()
        risultato = CC.seleziona_carte_casuali_per_tipo(
            DB_CARTA_FINTA, crea_carta_finta, [Set_Espansione.BASE],
            fazioni_orientamento=None, min_carte=1, max_carte=1,
            numero_giocatori=3, numero_mazzo=0,
        )
        assert len(risultato) <= CC.MAX_COPIE_CARTA


def test_quantita_puo_essere_il_tetto_d_calcolato_sui_giocatori_rimasti(monkeypatch):
    """
    Forza random.choice a scegliere sempre il secondo candidato (il tetto `d`) per
    verificare che la formula sia quella attesa: d = round(max_disponibile / giocatori
    rimasti). Qui max_disponibile = min(MAX_COPIE_CARTA=6, 20) = 6, giocatori_rimasti
    = numero_giocatori(3) - numero_mazzo(0) = 3, quindi d = round(6/3) = 2.
    """
    scelta_originale = random.choice
    catturato = {}

    def scelta_fittizia(sequenza):
        if len(sequenza) == 2:
            catturato['d'] = sequenza[1]
            return sequenza[1]
        return scelta_originale(sequenza)

    monkeypatch.setattr(CC.random, "choice", scelta_fittizia)
    CC.resetta_tracciamento_quantita()
    random.seed(0)

    risultato = CC.seleziona_carte_casuali_per_tipo(
        DB_CARTA_FINTA, crea_carta_finta, [Set_Espansione.BASE],
        fazioni_orientamento=None, min_carte=1, max_carte=1,
        numero_giocatori=3, numero_mazzo=0,
    )

    assert catturato['d'] == 2
    assert len(risultato) == 2


# --------------------------------------------------------------------------
# Integrazione: sul database reale, con gli stessi semi usati per la misura manuale
# --------------------------------------------------------------------------

ESPANSIONI_INTEGRAZIONE = [Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE]


def _crea_collezioni_silenziose(numero_giocatori, seme):
    random.seed(seme)
    with contextlib.redirect_stdout(io.StringIO()):
        return CC.creazione_Collezione_Giocatore(numero_giocatori, ESPANSIONI_INTEGRAZIONE, orientamento=True)


@pytest.mark.parametrize("seme", [1, 2, 3])
def test_integrazione_squilibrio_sotto_soglia_di_sicurezza(seme):
    # Prima della correzione: 293-338. Soglia larga per non essere fragile ai semi,
    # ma sufficiente a far fallire il test se si torna al comportamento precedente.
    collezioni = _crea_collezioni_silenziose(3, seme)
    totali = [c.get_totale_carte() for c in collezioni]
    assert max(totali) - min(totali) < 200


@pytest.mark.parametrize("seme", [1, 2, 3])
def test_integrazione_nessun_giocatore_senza_missioni(seme):
    collezioni = _crea_collezioni_silenziose(3, seme)
    missioni = [len(c.carte.get('missione', [])) for c in collezioni]
    assert min(missioni) >= 1
    assert max(missioni) - min(missioni) <= 1

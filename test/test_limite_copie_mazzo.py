"""
Controllo finale del limite di 5 copie per carta sul mazzo prodotto (regolamento §2).

Il tetto è già applicato durante la selezione (`copie_ancora_ammesse`/`residuo` in
Creatore_Mazzo.py), ma nessun controllo verificava il mazzo finito in modo
indipendente da come è stato costruito. Qui si testa quel controllo, non la
selezione: le carte sono oggetti minimi con il solo attributo che la funzione
legge, cosi' un difetto nella selezione non puo' mascherare un difetto qui.
"""

from types import SimpleNamespace

from source.logic.Creatore_Mazzo import (
    MAX_COPIE_PER_CARTA_MAZZO,
    verifica_integrità_mazzi,
    verifica_limite_copie_mazzo,
)


def carta(nome):
    return SimpleNamespace(nome=nome)


def mazzo_vuoto(**override):
    base = {'squadra': [], 'schieramento': [], 'carte_supporto': [],
            'statistiche': {'guerrieri_squadra': 5, 'guerrieri_schieramento': 0,
                             'numero_totale_carte': 45}, 'errori': []}
    base.update(override)
    return base


def test_nessun_errore_entro_il_limite():
    mazzo = mazzo_vuoto(carte_supporto=[carta("Spada Antica")] * MAX_COPIE_PER_CARTA_MAZZO)
    assert verifica_limite_copie_mazzo(mazzo) == []


def test_errore_oltre_il_limite():
    mazzo = mazzo_vuoto(carte_supporto=[carta("Spada Antica")] * (MAX_COPIE_PER_CARTA_MAZZO + 1))
    errori = verifica_limite_copie_mazzo(mazzo)
    assert len(errori) == 1
    assert "Spada Antica" in errori[0]


def test_conta_su_tutte_e_tre_le_liste_del_mazzo():
    # Lo stesso nome sparso tra squadra/schieramento/carte_supporto deve sommarsi:
    # il limite è sul mazzo intero, non sulla singola area di gioco.
    mazzo = mazzo_vuoto(
        squadra=[carta("Guerriero X")] * 3,
        schieramento=[carta("Guerriero X")] * 2,
        carte_supporto=[carta("Guerriero X")] * 1,
    )
    errori = verifica_limite_copie_mazzo(mazzo)
    assert len(errori) == 1
    assert "6" in errori[0]


def test_carte_diverse_non_si_sommano_tra_loro():
    mazzo = mazzo_vuoto(carte_supporto=[carta("A")] * 5 + [carta("B")] * 5)
    assert verifica_limite_copie_mazzo(mazzo) == []


def test_verifica_integrità_mazzi_propaga_l_errore():
    mazzo_ok = mazzo_vuoto(carte_supporto=[carta("A")] * 5)
    mazzo_sforato = mazzo_vuoto(carte_supporto=[carta("A")] * 7)

    risultati = verifica_integrità_mazzi([mazzo_ok, mazzo_sforato])

    assert risultati['mazzi_validi'] == 1
    assert risultati['mazzi_con_errori'] == 1
    errori_secondo_mazzo = risultati['errori_trovati'][0]['errori']
    assert any("Limite di 5 copie" in e for e in errori_secondo_mazzo)

"""
Lettura del mazzo da parte del visualizzatore.

I test costruiscono il JSON su una cartella temporanea invece di leggere `out/`, che
è ignorata da git e cambia a ogni generazione: un test che dipendesse da quei file
passerebbe o fallirebbe a seconda di quali mazzi sono stati creati di recente.
"""

import json

import pytest

from source.gui.visualizzatore_mazzo import carica_mazzo, trova_immagine


def _carta(copie=1, fazione="Oscura Legione", **extra):
    dati = {"copie": copie, "fazione": fazione, "set_espansione": "Base",
            "rarity": "Common", "tipo": "Seguace", "quantita": copie}
    dati.update(extra)
    return dati


def _scrivi_mazzo(cartella, inventario_guerrieri, inventario_supporto=None):
    cartella.mkdir(parents=True, exist_ok=True)
    documento = {
        "metadata": {"indice": 1},
        "mazzo": {
            "inventario_guerrieri": inventario_guerrieri,
            "inventario_supporto": inventario_supporto or {},
        },
    }
    (cartella / "mazzo_giocatore_1.json").write_text(
        json.dumps(documento, ensure_ascii=False), encoding="utf-8")
    return cartella


# --------------------------------------------------------------------------


def test_l_apostolo_non_e_una_carta(tmp_path):
    """
    L'Oscura Legione ha un livello in più — l'Apostolo — che le altre fazioni non hanno:

        squadra > Cybertronic    > Cyril Dent            > {copie, …}
        squadra > Oscura Legione > Algeroth > Cultista…  > {copie, …}

    Senza attraversarlo, il nome dell'Apostolo veniva scambiato per quello di una carta:
    comparivano «Algeroth» e «Ilian» con zero copie — e «Algeroth» due volte, una per
    area — mentre i guerrieri veri sparivano dall'elenco.
    """
    cartella = _scrivi_mazzo(tmp_path / "Mazzo_Giocatore_1", {
        "squadra": {
            "Cybertronic": {"Cyril Dent": _carta(copie=1, fazione="Cybertronic")},
            "Oscura Legione": {"Algeroth": {"Cultista di Algeroth": _carta(copie=1)}},
        },
        "schieramento": {
            "Oscura Legione": {
                "Algeroth": {"Valpurgius": _carta(copie=1),
                             "Karnofago": _carta(copie=2)},
                "Ilian": {"Figlio di Ilian": _carta(copie=3)},
            },
        },
    })

    carte, _ = carica_mazzo(cartella)
    nomi = {c.nome for c in carte}

    assert "Algeroth" not in nomi and "Ilian" not in nomi, (
        f"i nomi degli Apostoli compaiono come carte: {sorted(nomi)}")
    assert nomi == {"Cyril Dent", "Cultista di Algeroth", "Valpurgius",
                    "Karnofago", "Figlio di Ilian"}
    assert sum(c.copie for c in carte) == 8


def test_le_copie_dei_guerrieri_annidati_sono_lette(tmp_path):
    """Il sintomo più visibile era la quantità a zero: si leggeva il nodo sbagliato."""
    cartella = _scrivi_mazzo(tmp_path / "Mazzo_Giocatore_1", {
        "schieramento": {"Oscura Legione": {"Ilian": {"Figlio di Ilian": _carta(copie=3)}}},
    })

    carte, _ = carica_mazzo(cartella)
    assert [(c.nome, c.copie) for c in carte] == [("Figlio di Ilian", 3)]


def test_la_struttura_piatta_continua_a_funzionare(tmp_path):
    """Le fazioni Doomtrooper non hanno il livello dell'Apostolo."""
    cartella = _scrivi_mazzo(tmp_path / "Mazzo_Giocatore_1", {
        "squadra": {"Imperiale": {"Comandante di Reparto": _carta(copie=2, fazione="Imperiale")}},
    })

    carte, _ = carica_mazzo(cartella)
    assert [(c.nome, c.copie, c.fazione) for c in carte] == [
        ("Comandante di Reparto", 2, "Imperiale")]


def test_l_immagine_si_trova_anche_in_un_altra_area(tmp_path):
    """
    L'esportazione colloca i Cultisti nello «schieramento», seguendo la fazione, mentre
    il mazzo li assegna alla «squadra», come vuole il loro testo. L'immagine è la stessa
    carta: cercarla solo nell'area dichiarata la perderebbe.
    """
    immagini = tmp_path / "Immagini_Mazzo_1" / "Guerriero"
    (immagini / "schieramento").mkdir(parents=True)
    atteso = immagini / "schieramento" / "Cultista_di_Algeroth.jpg"
    atteso.write_bytes(b"")

    trovata = trova_immagine(tmp_path / "Immagini_Mazzo_1", "Guerriero",
                             "Cultista di Algeroth", "squadra")
    assert trovata == atteso


def test_un_immagine_inesistente_resta_introvabile(tmp_path):
    """Il ripiego allarga la ricerca, non inventa corrispondenze."""
    (tmp_path / "Immagini_Mazzo_1" / "Guerriero" / "squadra").mkdir(parents=True)
    assert trova_immagine(tmp_path / "Immagini_Mazzo_1", "Guerriero",
                          "Guerriero Inesistente", "squadra") is None


@pytest.mark.lento
def test_l_esportazione_colloca_i_guerrieri_nell_area_del_mazzo(tmp_path, monkeypatch):
    """
    La sottocartella dell'immagine seguiva la **fazione**: i Cultisti finivano sotto
    «schieramento» mentre il mazzo li assegna alla «squadra», come vuole il loro testo,
    e l'immagine non si trovava dove il visualizzatore la cercava. Ora segue l'area.
    """
    from source.logic import Creatore_Mazzo
    from source.data_base_cards.Database_Guerriero import crea_guerriero_da_nome

    monkeypatch.setattr(Creatore_Mazzo, "PERCORSO_BASE_MAZZI", f"{tmp_path}/")

    cultista = crea_guerriero_da_nome("Cultista di Algeroth")
    oscura_legione = crea_guerriero_da_nome("Karnofago")
    doomtrooper = crea_guerriero_da_nome("Blood Beret")
    assert all((cultista, oscura_legione, doomtrooper))

    Creatore_Mazzo.esporta_immagini_mazzi([{
        "indice": 1,
        "squadra": [cultista, doomtrooper],
        "schieramento": [oscura_legione],
        "carte_supporto": [],
    }], verbose=False)

    guerrieri = next(tmp_path.rglob("Guerriero"), None)
    assert guerrieri is not None, "cartella Guerriero non creata"
    collocazione = {p.stem: p.parent.name for p in guerrieri.rglob("*") if p.is_file()}

    assert collocazione.get("Cultista_di_Algeroth") == "squadra", (
        f"il Cultista è finito in {collocazione.get('Cultista_di_Algeroth')!r}: "
        f"il mazzo lo assegna alla squadra")
    assert collocazione.get("Karnofago") == "schieramento"
    assert collocazione.get("Blood_Beret") == "squadra"


def test_un_mazzo_senza_json_e_un_errore_esplicito(tmp_path):
    cartella = tmp_path / "Mazzo_Giocatore_1"
    cartella.mkdir()
    with pytest.raises(FileNotFoundError):
        carica_mazzo(cartella)

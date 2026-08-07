"""
Caratterizzazione dei punteggi di potenza (`CreatoreMazzo.calcola_potenza_*`).

Nessun test esistente controllava i valori dei moltiplicatori usati da questi
metodi (`test_vocabolario_abilita.py` verifica solo che i nomi esistano nel
vocabolario, mai i moltiplicatori, e non copre Guerriero/Fortificazione/Warzone) —
a differenza della logica di compatibilità carta-guerriero, qui manca del tutto
una rete di sicurezza contro i cambi di comportamento.

Questo test fissa il punteggio attuale di ogni carta reale nei 5 database toccati
da un refactor pianificato (spostare il "blocco vocabolario" di
`calcola_potenza_{guerriero,equipaggiamento,fortificazione,reliquia,warzone}` in
un modulo condiviso). Deve passare *prima* di qualunque spostamento di codice, per
fissare il comportamento presente, e continuare a passare *dopo*, invariato, come
prova che lo spostamento non ha cambiato nulla.

Se una futura correzione cambia intenzionalmente un punteggio, va rigenerato il
file di riferimento eseguendo questo modulo direttamente:

    python3 test/test_potenza_carte.py

(scrive test/dati_test/potenze_golden.json — non ridirigere lo stdout: l'import
di Creatore_Collezione stampa due righe informative all'importazione, che
romperebbero il JSON se catturate con `>`) e il diff del file di riferimento va
incluso nella revisione della correzione.
"""

import json
import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RADICE))

from source.data_base_cards.Database_Guerriero import GUERRIERI_DATABASE, crea_guerriero_da_nome
from source.data_base_cards.Database_Equipaggiamento import DATABASE_EQUIPAGGIAMENTO
from source.data_base_cards.Database_Fortificazione import DATABASE_FORTIFICAZIONI
from source.data_base_cards.Database_Reliquia import DATABASE_RELIQUIE
from source.data_base_cards.Database_Warzone import DATABASE_WARZONE
from source.cards.Equipaggiamento import Equipaggiamento
from source.cards.Fortificazione import Fortificazione
from source.cards.Reliquia import Reliquia
from source.cards.Warzone import Warzone
from source.logic.Creatore_Mazzo import CreatoreMazzo

FILE_GOLDEN = RADICE / "test" / "dati_test" / "potenze_golden.json"

# (etichetta, database, funzione che costruisce la carta dal valore del database, metodo)
SORGENTI = [
    ("Guerriero", GUERRIERI_DATABASE, lambda nome, dati: crea_guerriero_da_nome(nome),
     "calcola_potenza_guerriero"),
    ("Equipaggiamento", DATABASE_EQUIPAGGIAMENTO, lambda nome, dati: Equipaggiamento.from_dict(dati),
     "calcola_potenza_equipaggiamento"),
    ("Fortificazione", DATABASE_FORTIFICAZIONI, lambda nome, dati: Fortificazione.from_dict(dati),
     "calcola_potenza_fortificazione"),
    ("Reliquia", DATABASE_RELIQUIE, lambda nome, dati: Reliquia.from_dict(dati),
     "calcola_potenza_reliquia"),
    ("Warzone", DATABASE_WARZONE, lambda nome, dati: Warzone.from_dict(dati),
     "calcola_potenza_warzone"),
]

CHIAVI_CACHE = ['Guerriero', 'Equipaggiamento', 'Fortificazione', 'Reliquia', 'Warzone',
                'Speciale', 'Arte', 'Oscura Simmetria', 'Missione']


def calcola_tutti_i_punteggi():
    """Ricalcola il punteggio di potenza di ogni carta reale nei 5 database."""
    cm = CreatoreMazzo.__new__(CreatoreMazzo)
    punteggi = {}
    for etichetta, database, costruisci, metodo in SORGENTI:
        for nome, dati in database.items():
            cm.potenze_calcolate = {chiave: {} for chiave in CHIAVI_CACHE}
            chiave = f"{etichetta}|{nome}"
            try:
                carta = costruisci(nome, dati)
                if carta is None:
                    punteggi[chiave] = "ERRORE: costruzione ha restituito None"
                    continue
                punteggi[chiave] = round(getattr(cm, metodo)(carta), 6)
            except Exception as e:
                punteggi[chiave] = f"ERRORE {type(e).__name__}: {e}"
    return punteggi


def test_punteggi_di_potenza_invariati():
    """
    Confronta i punteggi ricalcolati con il file di riferimento, carta per carta.
    Un fallimento qui significa che qualcosa ha cambiato il punteggio di potenza
    di almeno una carta reale — legittimo solo se è la correzione intenzionale
    che si sta verificando, nel qual caso il file di riferimento va rigenerato
    (vedi il docstring del modulo) e il diff incluso nella revisione.
    """
    assert FILE_GOLDEN.exists(), (
        f"Manca il file di riferimento {FILE_GOLDEN}. Generalo con:\n"
        f"  python3 test/test_potenza_carte.py > {FILE_GOLDEN}"
    )
    riferimento = json.loads(FILE_GOLDEN.read_text(encoding="utf-8"))
    attuale = calcola_tutti_i_punteggi()

    chiavi = set(riferimento) | set(attuale)
    diversi = sorted(
        k for k in chiavi
        if riferimento.get(k, "<mancante>") != attuale.get(k, "<mancante>")
    )

    dettaglio = "\n  ".join(
        f"{k}: riferimento={riferimento.get(k, '<mancante>')} attuale={attuale.get(k, '<mancante>')}"
        for k in diversi[:30]
    )
    assert not diversi, (
        f"{len(diversi)} punteggi di potenza sono cambiati rispetto al riferimento:\n  {dettaglio}"
    )


if __name__ == "__main__":
    punteggi = calcola_tutti_i_punteggi()
    FILE_GOLDEN.parent.mkdir(parents=True, exist_ok=True)
    FILE_GOLDEN.write_text(
        json.dumps(punteggi, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Scritte {len(punteggi)} voci in {FILE_GOLDEN}")

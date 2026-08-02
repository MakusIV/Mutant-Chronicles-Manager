"""Misura l'effetto dei difetti di Fascia 1 sui DUE livelli: Collezione e Mazzo."""
import sys, io, json, random, collections, contextlib
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from source.logic.Creatore_Collezione import creazione_Collezione_Giocatore
from source.logic.Creatore_Mazzo import crea_mazzo_da_gioco
from source.cards.Guerriero import Set_Espansione
from source.data_base_cards.Database_Arte import CARTE_ARTE_DATABASE as A

ESP = [Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE]

def misura():
    ris = {}
    random.seed(1234)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        collezioni = creazione_Collezione_Giocatore(4, ESP, orientamento=True)

    # ---- LIVELLO COLLEZIONE: l'orientamento è rispettato dai guerrieri? (§10.1)
    coll_stats = []
    for c in collezioni:
        orient = [f.value for f in (c.fazioni_orientamento or [])]
        g = c.carte.get('guerriero', [])
        tot = len(g)
        in_orient = sum(1 for x in g if x.fazione.value in orient)
        coll_stats.append({
            "orientamento": sorted(orient),
            "copie_guerriero": tot,
            "quota_in_orientamento": round(100*in_orient/tot, 1) if tot else 0.0,
            "fazioni": dict(collections.Counter(x.fazione.value for x in g)),
        })
    ris["collezioni"] = coll_stats

    # ---- LIVELLO COLLEZIONE, misura mirata: orientamento STRETTO su una sola fazione (§10.1)
    from source.logic.Creatore_Collezione import seleziona_carte_casuali_per_tipo, resetta_tracciamento_quantita
    from source.data_base_cards.Database_Guerriero import GUERRIERI_DATABASE, crea_guerriero_da_nome
    from source.cards.Guerriero import Fazione
    stretto = []
    for fazione in (Fazione.MISHIMA, Fazione.BAUHAUS, Fazione.CYBERTRONIC):
        random.seed(99)
        resetta_tracciamento_quantita()
        with contextlib.redirect_stdout(buf):
            carte = seleziona_carte_casuali_per_tipo(
                GUERRIERI_DATABASE, crea_guerriero_da_nome, ESP, [fazione],
                min_carte=60, max_carte=60, numero_giocatori=4, numero_mazzo=0)
        n = len(carte)
        giusti = sum(1 for c in carte if c.fazione == fazione)
        stretto.append({"fazione": fazione.value, "copie": n,
                        "della_fazione": giusti,
                        "quota": round(100*giusti/n, 1) if n else 0.0})
    ris["collezione_orientamento_stretto"] = stretto

    # ---- LIVELLO MAZZO: filtro espansioni (§10.2) e orientamento Arte (§10.3)
    mazzo_stats = []
    for c in collezioni:
        with contextlib.redirect_stdout(buf):
            m = crea_mazzo_da_gioco(c, 80, 60, ['Base'],          # <-- SOLO Base
                                    doomtrooper=True, fratellanza=True, oscura_legione=True,
                                    orientamento_arte=['Mentale', 'Cinetica'])
        tutte = list(m['squadra']) + list(m['schieramento']) + list(m['carte_supporto'])
        esp = collections.Counter(str(getattr(getattr(x, "set_espansione", "?"), "value", getattr(x, "set_espansione", "?"))) for x in tutte)
        arti = [x for x in m['carte_supporto'] if type(x).__name__ == 'Arte']
        disc = collections.Counter(x.disciplina.value for x in arti)
        in_disc = sum(v for k, v in disc.items() if k in ('Mentale', 'Cinetica'))
        mazzo_stats.append({
            "carte": len(tutte),
            "espansioni": dict(esp),
            "fuori_espansione_richiesta": sum(v for k, v in esp.items() if k != 'Base'),
            "carte_arte": len(arti),
            "arte_in_orientamento": in_disc,
            "quota_arte_in_orientamento": round(100*in_disc/len(arti), 1) if arti else 0.0,
            "discipline": dict(disc),
        })
    ris["mazzi"] = mazzo_stats
    return ris

if __name__ == "__main__":
    print(json.dumps(misura(), ensure_ascii=False, indent=1))

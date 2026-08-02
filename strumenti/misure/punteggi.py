"""Punteggi per Arte/Speciale/Oscura Simmetria + composizione dei mazzi reali."""
import sys, io, json, random, statistics, collections, contextlib
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from source.logic.Creatore_Mazzo import CreatoreMazzo, crea_mazzo_da_gioco
from source.logic.Creatore_Collezione import creazione_Collezione_Giocatore
from source.cards.Guerriero import Set_Espansione
from source.data_base_cards.Database_Speciale import DATABASE_SPECIALI as S
from source.data_base_cards.Database_Arte import CARTE_ARTE_DATABASE as A
from source.data_base_cards.Database_Oscura_Simmetria import DATABASE_OSCURA_SIMMETRIA as O
from source.cards.Speciale import Speciale
from source.cards.Arte import Arte
from source.cards.Oscura_Simmetria import Oscura_Simmetria

K = ['Guerriero','Equipaggiamento','Speciale','Arte','Oscura Simmetria','Fortificazione','Missione','Reliquia','Warzone']

def punteggi():
    cm = CreatoreMazzo.__new__(CreatoreMazzo)
    out = {}
    for nome, db, cls, met in [("Speciale",S,Speciale,"calcola_potenza_speciale"),
                               ("Arte",A,Arte,"calcola_potenza_arte"),
                               ("Oscura Simmetria",O,Oscura_Simmetria,"calcola_potenza_oscura_simmetria")]:
        vals = {}
        for k, v in db.items():
            cm.potenze_calcolate = {x: {} for x in K}
            try:
                vals[k] = round(getattr(cm, met)(cls.from_dict(v)), 4)
            except Exception as e:
                vals[k] = f"ERR {type(e).__name__}"
        num = [x for x in vals.values() if isinstance(x, float)]
        out[nome] = {"per_carta": vals,
                     "n": len(num), "min": min(num), "max": max(num),
                     "mediana": round(statistics.median(num), 3),
                     "distinti": len(set(num))}
    return out

def mazzi():
    random.seed(1234); buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        coll = creazione_Collezione_Giocatore(4, [Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE], orientamento=True)
        m = [crea_mazzo_da_gioco(c, 80, 60, ['Base','Inquisition'], doomtrooper=True, fratellanza=True,
                                 oscura_legione=True, orientamento_apostolo=['Algeroth']) for c in coll]
    res = []
    for x in m:
        sup = x['carte_supporto']
        nomi = collections.Counter(c.nome for c in sup if type(c).__name__ in ('Speciale','Arte','Oscura_Simmetria'))
        res.append({"carte": len(x['squadra'])+len(x['schieramento'])+len(sup),
                    "distinte_SAO": len(nomi), "top_SAO": [n for n,_ in nomi.most_common(6)]})
    return res

if __name__ == "__main__":
    print(json.dumps({"punteggi": punteggi(), "mazzi": mazzi()}, ensure_ascii=False))

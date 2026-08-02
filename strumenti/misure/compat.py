import sys, json, collections
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from source.data_base_cards.Database_Guerriero import GUERRIERI_DATABASE, crea_guerriero_da_nome

SPEC = [
 ("Speciale","source.data_base_cards.Database_Speciale","DATABASE_SPECIALI","crea_carta_da_database","puo_essere_assegnato_a_guerriero","puo_assegnare"),
 ("Equipaggiamento","source.data_base_cards.Database_Equipaggiamento","DATABASE_EQUIPAGGIAMENTO","crea_equipaggiamento_da_database","puo_essere_assegnato_a_guerriero","puo_assegnare"),
 ("Fortificazione","source.data_base_cards.Database_Fortificazione","DATABASE_FORTIFICAZIONI","crea_fortificazione_da_database","puo_essere_assegnato_a_guerriero","puo_assegnare"),
 ("Missione","source.data_base_cards.Database_Missione","DATABASE_MISSIONI","crea_missione_da_database","puo_essere_associata_a","puo_assegnare"),
 ("Arte","source.data_base_cards.Database_Arte","CARTE_ARTE_DATABASE","crea_carta_da_database","puo_essere_associata_a_guerriero","puo_lanciare"),
 ("Oscura_Simmetria","source.data_base_cards.Database_Oscura_Simmetria","DATABASE_OSCURA_SIMMETRIA","crea_carta_da_database","puo_essere_associata_a_guerriero","puo_lanciare"),
 ("Reliquia","source.data_base_cards.Database_Reliquia","DATABASE_RELIQUIE","crea_reliquia_da_database","puo_essere_associata_a_guerriero","puo_assegnare"),
 ("Warzone","source.data_base_cards.Database_Warzone","DATABASE_WARZONE","crea_istanza_warzone","puo_essere_associata_a_guerriero","puo_assegnare"),
]

# campione rappresentativo di guerrieri, uno per profilo rilevante
CAMPIONE = ["Blood Beret","Sergente","Billy","Eretico","Necromutante","Nefarita di Semai",
            "Legionario di Semai","Karnofago","Mercenario Ex-Bauhaus","Nicholai","Mortificator","Laura Vestale Benedetta",
            "Comandante di Reparto","Osservatore Tattico"]

def matrice():
    guerrieri = [(n, crea_guerriero_da_nome(n)) for n in CAMPIONE]
    guerrieri = [(n,g) for n,g in guerrieri if g]
    out = {}
    for nome, dbmod, dbname, fname, metodo, chiave in SPEC:
        m = __import__(dbmod, fromlist=['x']); db = getattr(m, dbname); mk = getattr(m, fname)
        for kcarta in db:
            c = mk(kcarta)
            if not c: continue
            for gn, g in guerrieri:
                try:
                    r = getattr(c, metodo)(g)
                    v = bool(r.get(chiave, False))
                except Exception as e:
                    v = f"ERR:{type(e).__name__}"
                out[f"{nome}|{kcarta}|{gn}"] = v
    return out

if __name__ == "__main__":
    print(json.dumps(matrice(), ensure_ascii=False, sort_keys=True))

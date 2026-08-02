"""Misura il deficit di slot e le proprieta' del mazzo, su collezioni e mazzi reali."""
import sys, io, json, random, collections, contextlib
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from source.logic.Creatore_Collezione import creazione_Collezione_Giocatore
from source.logic.Creatore_Mazzo import crea_mazzo_da_gioco
from source.cards.Guerriero import Set_Espansione

CONFIG = [
    ("Base+Inq", ['Base', 'Inquisition'], [Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE]),
    ("solo Base", ['Base'],               [Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE]),
]
CLASSE_A_TIPO = {'Equipaggiamento':'equipaggiamento','Fortificazione':'fortificazione','Speciale':'speciale',
                 'Missione':'missione','Arte':'arte','Oscura_Simmetria':'oscura_simmetria',
                 'Reliquia':'reliquia','Warzone':'warzone'}

def misura():
    ris = {}
    for etichetta, esp_mazzo, esp_coll in CONFIG:
        random.seed(1234)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            coll = creazione_Collezione_Giocatore(4, esp_coll, orientamento=True)
            mazzi = [crea_mazzo_da_gioco(c, 80, 60, esp_mazzo, doomtrooper=True, fratellanza=True,
                                         oscura_legione=True, orientamento_apostolo=['Algeroth'])
                     for c in coll]
        dati = []
        for m in mazzi:
            tutte = list(m['squadra']) + list(m['schieramento']) + list(m['carte_supporto'])
            cnt = collections.Counter(x.nome for x in tutte)
            esp = collections.Counter(str(getattr(getattr(x,'set_espansione','?'),'value',
                                                  getattr(x,'set_espansione','?'))) for x in tutte)
            per_tipo = collections.Counter(CLASSE_A_TIPO.get(type(x).__name__,'?') for x in m['carte_supporto'])
            dati.append({
                "carte": len(tutte),
                "sotto_minimo": len(tutte) < 60,
                "supporto": len(m['carte_supporto']),
                "per_tipo": dict(per_tipo),
                "max_copie": max(cnt.values()) if cnt else 0,
                "oltre_5_copie": sum(1 for v in cnt.values() if v > 5),
                "fuori_espansione": sum(v for k, v in esp.items() if k not in esp_mazzo),
                "errori": m.get('errori', []),
            })
        ris[etichetta] = dati
    return ris

if __name__ == "__main__":
    print(json.dumps(misura(), ensure_ascii=False, indent=1))

import sys, json
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from source.data_base_cards.Database_Equipaggiamento import DATABASE_EQUIPAGGIAMENTO as E
from source.data_base_cards.Database_Fortificazione import DATABASE_FORTIFICAZIONI as F
from source.data_base_cards.Database_Reliquia import DATABASE_RELIQUIE as R
from source.data_base_cards.Database_Warzone import DATABASE_WARZONE as W
from source.cards.Equipaggiamento import Equipaggiamento
from source.cards.Fortificazione import Fortificazione
from source.cards.Reliquia import Reliquia
from source.cards.Warzone import Warzone
from source.logic.Creatore_Mazzo import CreatoreMazzo

cm = CreatoreMazzo.__new__(CreatoreMazzo)
out = {}
for nome, db, cls, metodo in [
    ("Equipaggiamento", E, Equipaggiamento, "calcola_potenza_equipaggiamento"),
    ("Fortificazione",  F, Fortificazione,  "calcola_potenza_fortificazione"),
    ("Reliquia",        R, Reliquia,        "calcola_potenza_reliquia"),
    ("Warzone",         W, Warzone,         "calcola_potenza_warzone"),
]:
    for k, v in db.items():
        cm.potenze_calcolate = {x: {} for x in ['Guerriero','Equipaggiamento','Fortificazione','Reliquia','Warzone','Speciale','Arte','Oscura_Simmetria','Missione']}
        try:
            out[f"{nome}|{k}"] = round(getattr(cm, metodo)(cls.from_dict(v)), 4)
        except Exception as e:
            out[f"{nome}|{k}"] = f"ERRORE {type(e).__name__}: {e}"
print(json.dumps(out, ensure_ascii=False, indent=0, sort_keys=True))

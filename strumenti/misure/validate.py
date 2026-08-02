import sys, traceback
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from source.data_base_cards.Database_Arte import CARTE_ARTE_DATABASE
from source.data_base_cards.Database_Speciale import DATABASE_SPECIALI
from source.data_base_cards.Database_Oscura_Simmetria import DATABASE_OSCURA_SIMMETRIA
from source.data_base_cards.Database_Fortificazione import DATABASE_FORTIFICAZIONI
from source.data_base_cards.Database_Reliquia import DATABASE_RELIQUIE
from source.data_base_cards.Database_Missione import DATABASE_MISSIONI
from source.data_base_cards.Database_Equipaggiamento import DATABASE_EQUIPAGGIAMENTO
from source.data_base_cards.Database_Warzone import DATABASE_WARZONE

from source.cards.Arte import Arte
from source.cards.Speciale import Speciale
from source.cards.Oscura_Simmetria import Oscura_Simmetria as OscuraSimmetria
from source.cards.Fortificazione import Fortificazione
from source.cards.Reliquia import Reliquia
from source.cards.Missione import Missione
from source.cards.Equipaggiamento import Equipaggiamento
from source.cards.Warzone import Warzone

targets = [
    ("Arte", CARTE_ARTE_DATABASE, Arte),
    ("Speciale", DATABASE_SPECIALI, Speciale),
    ("OscuraSimmetria", DATABASE_OSCURA_SIMMETRIA, OscuraSimmetria),
    ("Fortificazione", DATABASE_FORTIFICAZIONI, Fortificazione),
    ("Reliquia", DATABASE_RELIQUIE, Reliquia),
    ("Missione", DATABASE_MISSIONI, Missione),
    ("Equipaggiamento", DATABASE_EQUIPAGGIAMENTO, Equipaggiamento),
    ("Warzone", DATABASE_WARZONE, Warzone),
]

for name, db, cls in targets:
    ok = fail = 0
    errs = []
    for key, data in db.items():
        try:
            cls.from_dict(data)
            ok += 1
        except Exception as e:
            fail += 1
            errs.append(f"    {key}: {type(e).__name__}: {e}")
    print(f"{name}: {ok} ok, {fail} FALLITE")
    for e in errs[:40]:
        print(e)

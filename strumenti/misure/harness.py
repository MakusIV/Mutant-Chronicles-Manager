import sys, random
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
random.seed(42)
from source.logic.Creatore_Collezione import CollezioneGiocatore
from source.logic.Creatore_Mazzo import CreatoreMazzo
from source.data_base_cards.Database_Guerriero import GUERRIERI_DATABASE, crea_guerriero_da_nome
from source.data_base_cards.Database_Speciale import DATABASE_SPECIALI, crea_carta_da_database as mk_spec
from source.data_base_cards.Database_Equipaggiamento import DATABASE_EQUIPAGGIAMENTO, crea_equipaggiamento_da_database as mk_eq
from source.data_base_cards.Database_Arte import CARTE_ARTE_DATABASE, crea_carta_da_database as mk_arte
from source.data_base_cards.Database_Oscura_Simmetria import DATABASE_OSCURA_SIMMETRIA, crea_carta_da_database as mk_os
from source.data_base_cards.Database_Fortificazione import DATABASE_FORTIFICAZIONI, crea_fortificazione_da_database as mk_fort

def collezione_completa():
    """Collezione che contiene 5 copie di OGNI carta: isola la logica di selezione dal caso."""
    c = CollezioneGiocatore(1)
    for db, mk in [(GUERRIERI_DATABASE, crea_guerriero_da_nome), (DATABASE_SPECIALI, mk_spec),
                   (DATABASE_EQUIPAGGIAMENTO, mk_eq), (CARTE_ARTE_DATABASE, mk_arte),
                   (DATABASE_OSCURA_SIMMETRIA, mk_os), (DATABASE_FORTIFICAZIONI, mk_fort)]:
        for nome in db:
            carta = mk(nome)
            if carta: c.aggiungi_carta(carta, 5)
    return c

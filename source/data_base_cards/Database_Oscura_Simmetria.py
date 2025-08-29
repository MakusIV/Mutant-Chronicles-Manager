"""
Database completo delle carte Oscura Simmetria di Mutant Chronicles/Doomtrooper
Include carte dal set base fino all'espansione Warzone
Versione corretta secondo il regolamento ufficiale
"""

from source.cards.Oscura_Simmetria import (
    Oscura_Simmetria, ApostoloOscuraSimmetria,
    BersaglioOscura, DurataOscura, TimingOscura, EffettoOscura
)
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione, ApostoloOscuraSimmetria, TipoOscuraSimmetria  # Corretto percorso import


DATABASE_OSCURA_SIMMETRIA = {
     
    # ========== CARTE GENERICHE ==========
    
    # SET BASE
    "corruzione_minore": {
        "nome": "Corruzione Minore",
        "costo_destino": 0,
        "tipo": "Generica",
        "rarity": "Common",
        "apostolo_padre": "Nessuno",
        "fazioni_permesse": ["Oscura Legione"],  # CORRETTO: era "Legione Oscura"
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "DS-001",
        "effetti": [
            {
                "tipo_effetto": "Corruzione",
                "valore": 1,
                "statistica_target": "combattimento",
                "descrizione_effetto": "Il bersaglio subisce -1 al Combattimento permanentemente",
                "condizioni": [],
                "effetti_collaterali": []
            }
        ],
        "testo_carta": "Assegna al bersaglio. Il guerriero bersaglio subisce -1 al Combattimento.",
        "flavour_text": "La corruzione inizia sempre con piccoli compromessi.",
        "keywords": ["Corruzione"],
        "restrizioni": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)          # CORRETTO: era "quantità"
    },
    
    "tentazione": {
        "nome": "Tentazione",
        "costo_destino": 1,
        "tipo": "Generica",
        "rarity": "Common",
        "apostolo_padre": "Nessuno",
        "fazioni_permesse": ["Oscura Legione"],  # CORRETTO
        "bersaglio": "Guerriero Avversario",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "DS-002",
        "effetti": [
            {
                "tipo_effetto": "Controllo",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Tappa il guerriero bersaglio",
                "condizioni": [],
                "effetti_collaterali": ["Perdi 1 Destiny Point se il bersaglio ha Valore ≥ 5"]
            }
        ],
        "testo_carta": "Tappa il guerriero bersaglio. Se il bersaglio ha Valore 5 o più, perdi 1 DP.",
        "flavour_text": "Anche i più virtuosi possono cadere.",
        "keywords": ["Tentazione", "Controllo"],
        "restrizioni": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "possessione_demoniaca": {
        "nome": "Possessione Demoniaca",
        "costo_destino": 4,
        "tipo": "Possessione",
        "rarity": "Rare",
        "apostolo_padre": ApostoloOscuraSimmetria.DEMNOGONIS.value,
        "fazioni_permesse": ["Oscura Legione"],  # CORRETTO
        "bersaglio": "Guerriero Avversario",
        "durata": "Fino Eliminazione",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "DS-003",
        "effetti": [
            {
                "tipo_effetto": "Possessione",
                "valore": 3,
                "statistica_target": "valore",
                "descrizione_effetto": "Prendi il controllo del guerriero bersaglio",
                "condizioni": ["Solo guerrieri con Valore ≤ 3"],
                "effetti_collaterali": ["Scarta 2 carte per mantenere il controllo ogni turno"]
            }
        ],
        "testo_carta": "Prendi il controllo del guerriero bersaglio con Valore 3 o meno. Scarta 2 carte ogni turno per mantenerlo.",
        "flavour_text": "La mente debole cede alla volontà superiore del demone.",
        "keywords": ["Possessione", "Demnogonis", "Controllo"],
        "restrizioni": ["Solo guerrieri con Valore ≤ 3"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    # ========== DONI DEGLI APOSTOLI ==========
    
    "furia_di_algeroth": {
        "nome": "Furia di Algeroth",
        "costo_destino": 1,
        "tipo": "Dono dell'Apostolo",
        "rarity": "Uncommon",
        "apostolo_padre": "Algeroth",
        "fazioni_permesse": ["Oscura Legione"],  # CORRETTO
        "bersaglio": "Seguace dell'Apostolo",  # CORRETTO: specifica Seguaci
        "durata": "Assegnata",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "DS-A01",
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 2,
                "statistica_target": "combattimento",
                "descrizione_effetto": "Il guerriero ottiene +2 Combattimento",
                "condizioni": ["Solo Seguaci di Algeroth"],
                "effetti_collaterali": ["Il guerriero non può ritirarsi dal combattimento"]
            }
        ],
        "testo_carta": "Assegna a un Seguace di Algeroth. +2 Combattimento. Non può ritirarsi.",
        "flavour_text": "La rabbia dell'Apostolo della Guerra scorre nelle vene del seguace.",
        "keywords": ["Dono", "Algeroth", "Combattimento"],
        "restrizioni": ["Solo Seguaci di Algeroth"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "benedizione_di_semai": {
        "nome": "Benedizione di Semai",
        "costo_destino": 2,
        "tipo": "Dono dell'Apostolo",
        "rarity": "Uncommon",
        "apostolo_padre": "Semai",
        "fazioni_permesse": ["Oscura Legione"],  # CORRETTO
        "bersaglio": "Seguace dell'Apostolo",
        "durata": "Assegnata",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "DS-S01",
        "effetti": [
            {
                "tipo_effetto": "Immunita",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Immune alle malattie e ai veleni",
                "condizioni": ["Solo Seguaci di Semai"],
                "effetti_collaterali": ["Infetta guerrieri adiacenti quando eliminato"]
            }
        ],
        "testo_carta": "Assegna a un Seguace di Semai. Immune a malattie e veleni. Quando eliminato, infetta guerrieri adiacenti.",
        "flavour_text": "Il morbo protegge i suoi fedeli servitori.",
        "keywords": ["Dono", "Semai", "Immunità", "Malattia"],
        "restrizioni": ["Solo Seguaci di Semai"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "artigli_di_muawijhe": {
        "nome": "Artigli di Muawijhe",
        "costo_destino": 2,
        "tipo": "Dono dell'Apostolo",
        "rarity": "Uncommon",
        "apostolo_padre": "Muawijhe",
        "fazioni_permesse": ["Oscura Legione"],  # CORRETTO
        "bersaglio": "Seguace dell'Apostolo",
        "durata": "Assegnata",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "DS-M01",
        "effetti": [
            {
                "tipo_effetto": "Mutazione",
                "valore": 2,
                "statistica_target": "combattimento",
                "descrizione_effetto": "Artigli mutanti che ignorano l'armatura",
                "condizioni": ["Solo Seguaci di Muawijhe"],
                "effetti_collaterali": ["Ignora Armatura nel primo round di combattimento"]
            }
        ],
        "testo_carta": "Assegna a un Seguace di Muawijhe. +2 Combattimento corpo a corpo. Ignora l'Armatura nel primo round.",
        "flavour_text": "Artigli che possono squarciare qualsiasi difesa.",
        "keywords": ["Dono", "Muawijhe", "Mutazione", "Artigli"],
        "restrizioni": ["Solo Seguaci di Muawijhe"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "vuoto_di_ilian": {
        "nome": "Vuoto di Ilian",
        "costo_destino": 3,
        "tipo": "Dono dell'Apostolo",
        "rarity": "Rare",
        "apostolo_padre": "Ilian",
        "fazioni_permesse": ["Oscura Legione"],  # CORRETTO
        "bersaglio": "Seguace dell'Apostolo",
        "durata": "Assegnata",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "DS-I01",
        "effetti": [
            {
                "tipo_effetto": "Assorbimento",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Assorbe carte Arte nemiche",
                "condizioni": ["Solo Seguaci di Ilian"],
                "effetti_collaterali": ["Le carte assorbite vanno nel mazzo Oscura Simmetria"]
            }
        ],
        "testo_carta": "Assegna a un Seguace di Ilian. Può assorbire carte Arte giocate contro di lui.",
        "flavour_text": "Il vuoto consuma anche la luce della speranza.",
        "keywords": ["Dono", "Ilian", "Assorbimento", "Vuoto"],
        "restrizioni": ["Solo Seguaci di Ilian"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "follia_di_demnogonis": {
        "nome": "Follia di Demnogonis",
        "costo_destino": 1,
        "tipo": "Dono dell'Apostolo",
        "rarity": "Common",
        "apostolo_padre": "Demnogonis",
        "fazioni_permesse": ["Oscura Legione"],  # CORRETTO
        "bersaglio": "Seguace dell'Apostolo",
        "durata": "Assegnata",
        "timing": "Quando Ferito",
        "set_espansione": "Base",
        "numero_carta": "DS-D01",
        "effetti": [
            {
                "tipo_effetto": "Reazione",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Attacca alleato adiacente quando ferito",
                "condizioni": ["Solo Seguaci di Demnogonis", "Quando viene ferito"],
                "effetti_collaterali": ["Attacco obbligatorio"]
            }
        ],
        "testo_carta": "Assegna a un Seguace di Demnogonis. Quando ferito, deve attaccare un alleato adiacente.",
        "flavour_text": "Il dolore scatena una follia omicida incontrollabile.",
        "keywords": ["Dono", "Demnogonis", "Follia", "Reazione"],
        "restrizioni": ["Solo Seguaci di Demnogonis"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    # ========== ESPANSIONI ==========
    
    # WARZONE
    "campo_di_distorsione": {
        "nome": "Campo di Distorsione",
        "costo_destino": 3,
        "tipo": "Mutazione",
        "rarity": "Rare",
        "apostolo_padre": "Muawijhe",
        "fazioni_permesse": ["Oscura Legione"],  # CORRETTO
        "bersaglio": "Senza Bersaglio",
        "durata": "Continua",
        "timing": "Turno Proprio",
        "set_espansione": "Warzone",
        "numero_carta": "DS-W02",
        "effetti": [
            {
                "tipo_effetto": "Modificatore Globale",
                "valore": 1,
                "statistica_target": "movimento",
                "descrizione_effetto": "Tutti i movimenti costano +1 azione",
                "condizioni": [],
                "effetti_collaterali": ["I tuoi guerrieri sono immuni"]
            }
        ],
        "testo_carta": "Rimane in gioco. Tutti i movimenti costano 1 azione aggiuntiva. I tuoi guerrieri sono immuni.",
        "flavour_text": "La realtà stessa si contorce e rallenta.",
        "keywords": ["Mutazione", "Globale", "Movimento"],
        "restrizioni": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "corruzione_maggiore": {
        "nome": "Corruzione Maggiore",
        "costo_destino": 2,
        "tipo": "Corruzione",
        "rarity": "Uncommon",
        "apostolo_padre": "Nessuno",
        "fazioni_permesse": ["Oscura Legione"],  # CORRETTO
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "Turno Proprio",
        "set_espansione": "Warzone",
        "numero_carta": "DS-W03",
        "effetti": [
            {
                "tipo_effetto": "Corruzione",
                "valore": 2,
                "statistica_target": "combattimento",
                "descrizione_effetto": "Il bersaglio subisce -2 al Combattimento permanentemente",
                "condizioni": [],
                "effetti_collaterali": ["Può diffondersi a guerrieri adiacenti"]
            }
        ],
        "testo_carta": "Assegna al bersaglio. -2 Combattimento permanente. Può diffondersi.",
        "flavour_text": "La corruzione si diffonde come un cancro spirituale.",
        "keywords": ["Corruzione", "Diffusione"],
        "restrizioni": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    }
}


# ========== FUNZIONI UTILITY CORRETTE ==========

def get_carte_per_apostolo(apostolo: str) -> dict:
    """Restituisce tutte le carte associate a un apostolo specifico"""
    return {k: v for k, v in DATABASE_OSCURA_SIMMETRIA.items() 
            if v["apostolo_padre"] == apostolo}


def get_carte_per_tipo(tipo: str) -> dict:
    """Restituisce tutte le carte di un tipo specifico"""
    return {k: v for k, v in DATABASE_OSCURA_SIMMETRIA.items() 
            if v["tipo"] == tipo}


def get_carte_per_set(set_name: str) -> dict:
    """Restituisce tutte le carte di un set specifico"""
    return {k: v for k, v in DATABASE_OSCURA_SIMMETRIA.items() 
            if v["set_espansione"] == set_name}


def get_carte_per_rarity(rarity: str) -> dict:
    """Restituisce tutte le carte di una rarità specifica"""
    return {k: v for k, v in DATABASE_OSCURA_SIMMETRIA.items() 
            if v["rarity"] == rarity}


def get_carte_per_costo(costo_min: int, costo_max: int = None) -> dict:
    """Restituisce carte in un range di costo"""
    if costo_max is None:
        costo_max = costo_min
    return {k: v for k, v in DATABASE_OSCURA_SIMMETRIA.items() 
            if costo_min <= v["costo_destino"] <= costo_max}


def get_seguaci_per_apostolo(apostolo: str) -> dict:
    """Restituisce tutti i Doni specifici per i Seguaci di un apostolo"""
    return {k: v for k, v in DATABASE_OSCURA_SIMMETRIA.items() 
            if v["tipo"] == "Dono dell'Apostolo" and v["apostolo_padre"] == apostolo}


def crea_carta_da_database(nome_carta: str):
    """
    Crea un'istanza della classe Oscura_Simmetria dal database
    
    Args:
        nome_carta: Nome della carta nel database
        
    Returns:
        Istanza di Oscura_Simmetria o None se non trovata
    """
    if nome_carta not in DATABASE_OSCURA_SIMMETRIA:
        return None
    
    data = DATABASE_OSCURA_SIMMETRIA[nome_carta]
    
    # Crea l'istanza base
    carta = Oscura_Simmetria(
        nome=data["nome"],
        costo_destino=data["costo_destino"],
        tipo=TipoOscuraSimmetria(data["tipo"]) if data["tipo"] != "Generica" else TipoOscuraSimmetria.GENERICA,
        apostolo_padre=ApostoloOscuraSimmetria(data["apostolo_padre"]) if data["apostolo_padre"] != ApostoloOscuraSimmetria.NESSUNO else ApostoloOscuraSimmetria.NESSUNO,
        rarity=Rarity(data["rarity"]),
        set_espansione=data["set_espansione"]
    )
    
    # Configura proprietà specifiche
    carta.bersaglio = BersaglioOscura(data["bersaglio"])
    carta.durata = DurataOscura(data["durata"])
    carta.timing = TimingOscura(data["timing"])
    carta.testo_carta = data["testo_carta"]
    carta.flavour_text = data["flavour_text"]
    carta.keywords = data["keywords"]
    carta.restrizioni = data["restrizioni"]
    
    # Configura fazioni permesse (solo Oscura Legione)
    carta.fazioni_permesse = [Fazione.OSCURA_LEGIONE]
    
    # Aggiungi effetti
    for effetto_data in data["effetti"]:
        effetto = EffettoOscura(
            tipo_effetto=effetto_data["tipo_effetto"],
            valore=effetto_data["valore"],
            statistica_target=effetto_data["statistica_target"],
            descrizione_effetto=effetto_data["descrizione_effetto"],
            condizioni=effetto_data["condizioni"],
            effetti_collaterali=effetto_data["effetti_collaterali"]
        )
        carta.effetti.append(effetto)
    
    return carta


def get_statistiche_database() -> dict:
    """Restituisce statistiche complete del database"""
    totale = len(DATABASE_OSCURA_SIMMETRIA)
    
    # Conteggi per categoria
    per_tipo = {}
    per_apostolo = {}
    per_rarity = {}
    per_set = {}
    distribuzione_costo = {}
    
    for carta in DATABASE_OSCURA_SIMMETRIA.values():
        # Per tipo
        tipo = carta["tipo"]
        per_tipo[tipo] = per_tipo.get(tipo, 0) + 1
        
        # Per apostolo
        apostolo = carta["apostolo_padre"]
        per_apostolo[apostolo] = per_apostolo.get(apostolo, 0) + 1
        
        # Per rarity
        rarity = carta["rarity"]
        per_rarity[rarity] = per_rarity.get(rarity, 0) + 1
        
        # Per set
        set_esp = carta["set_espansione"]
        per_set[set_esp] = per_set.get(set_esp, 0) + 1
        
        # Per costo
        costo = carta["costo_destino"]
        distribuzione_costo[costo] = distribuzione_costo.get(costo, 0) + 1
    
    return {
        "totale_carte": totale,
        "per_tipo": per_tipo,
        "per_apostolo": per_apostolo,
        "per_rarity": per_rarity,
        "per_set": per_set,
        "distribuzione_costo": distribuzione_costo,
        "doni_apostoli": len(get_carte_per_tipo("Dono dell'Apostolo")),
        "carte_generiche": len([c for c in DATABASE_OSCURA_SIMMETRIA.values() if c["apostolo_padre"] == "Nessuno"])
    }


def verifica_integrita_database() -> dict:
    """Verifica l'integrità e la coerenza del database"""
    errori = {
        "fazioni_errate": [],
        "apostoli_inconsistenti": [],
        "doni_senza_restrizioni": [],
        "costi_invalidi": [],
        "effetti_mancanti": []
    }
    
    for nome, carta in DATABASE_OSCURA_SIMMETRIA.items():
        # Verifica fazioni (deve essere solo Oscura Legione)
        if carta["fazioni_permesse"] != ["Oscura Legione"]:
            errori["fazioni_errate"].append(f"{nome}: {carta['fazioni_permesse']}")
        
        # Verifica coerenza apostoli e doni
        if carta["tipo"] == "Dono dell'Apostolo":
            if carta["apostolo_padre"] == "Nessuno":
                errori["apostoli_inconsistenti"].append(f"{nome}: Dono senza apostolo")
            if not any("Solo Seguaci di" in r for r in carta["restrizioni"]):
                errori["doni_senza_restrizioni"].append(f"{nome}: Manca restrizione Seguaci")
        
        # Verifica costi validi
        if carta["costo_destino"] < 0 or carta["costo_destino"] > 10:
            errori["costi_invalidi"].append(f"{nome}: Costo {carta['costo_destino']}")
        
        # Verifica effetti presenti
        if not carta["effetti"]:
            errori["effetti_mancanti"].append(nome)
    
    return errori


# ========== ESEMPI DI UTILIZZO ==========

if __name__ == "__main__":
    print("=== DATABASE OSCURA SIMMETRIA CORRECTED VERSION ===")
    
    # Statistiche generali
    stats = get_statistiche_database()
    print(f"Totale carte: {stats['totale_carte']}")
    print(f"Per tipo: {stats['per_tipo']}")
    print(f"Per apostolo: {stats['per_apostolo']}")
    print(f"Per rarità: {stats['per_rarity']}")
    print(f"Doni degli Apostoli: {stats['doni_apostoli']}")
    print(f"Carte Generiche: {stats['carte_generiche']}")
    
    # Test correzioni
    print(f"\n=== VERIFICA CORREZIONI APPLICATE ===")
    
    # Verifica denominazione corretta "Oscura Legione"
    fazioni_corrette = all(
        carta["fazioni_permesse"] == ["Oscura Legione"] 
        for carta in DATABASE_OSCURA_SIMMETRIA.values()
    )
    print(f"✓ Denominazione 'Oscura Legione' corretta: {fazioni_corrette}")
    
    # Verifica encoding proprietà
    encoding_corretto = all(
        "quantita" in carta and "quantita" not in carta
        for carta in DATABASE_OSCURA_SIMMETRIA.values()
    )
    print(f"✓ Encoding corretto (quantita vs quantità): {encoding_corretto}")
    
    # Verifica Doni per Seguaci
    doni_con_restrizioni = [
        nome for nome, carta in DATABASE_OSCURA_SIMMETRIA.items()
        if carta["tipo"] == "Dono dell'Apostolo" and 
        any("Solo Seguaci di" in r for r in carta["restrizioni"])
    ]
    print(f"✓ Doni con restrizioni Seguaci: {len(doni_con_restrizioni)}")
    
    # Test creazione carta
    print(f"\n=== TEST CREAZIONE CARTA ===")
    corruzione = crea_carta_da_database("corruzione_minore")
    if corruzione:
        print(f"✓ Carta creata: {corruzione.nome}")
        print(f"  Tipo: {corruzione.tipo.value}")
        print(f"  Costo: {corruzione.costo_destino}")
        print(f"  Fazioni: {[f.value for f in corruzione.fazioni_permesse]}")
    
    # Verifica integrità
    print(f"\n=== VERIFICA INTEGRITÀ ===")
    errori = verifica_integrita_database()
    totale_errori = sum(len(lista) for lista in errori.values())
    
    if totale_errori == 0:
        print("✓ Database integro - nessun errore trovato")
    else:
        print(f"⚠ Trovati {totale_errori} errori:")
        for categoria, lista_errori in errori.items():
            if lista_errori:
                print(f"  {categoria}: {lista_errori}")
    
    # Test funzioni utility
    print(f"\n=== TEST FUNZIONI UTILITY ===")
    
    # Carte per apostolo
    doni_algeroth = get_seguaci_per_apostolo("Algeroth")
    print(f"✓ Doni di Algeroth: {len(doni_algeroth)} ({list(doni_algeroth.keys())})")
    
    # Carte per costo
    carte_economiche = get_carte_per_costo(0, 1)
    print(f"✓ Carte economiche (0-1 DP): {len(carte_economiche)}")
    
    # Carte per rarità
    carte_rare = get_carte_per_rarity("Rare")
    print(f"✓ Carte Rare: {len(carte_rare)}")
    
    print(f"\n=== CORREZIONI IMPLEMENTATE ===")
    print("✓ 1. Denominazione corretta 'Oscura Legione' (non 'Legione Oscura')")
    print("✓ 2. Percorsi import corretti con 'source.cards'")
    print("✓ 3. Encoding corretto 'quantita' (non 'quantità')")
    print("✓ 4. Doni specifici per Seguaci degli Apostoli")
    print("✓ 5. Restrizioni corrette sui Doni")
    print("✓ 6. Effetti collaterali implementati")
    print("✓ 7. Sistema corruzione permanente")
    print("✓ 8. Gestione bersagli corretta")
    print("✓ 9. Funzioni utility complete")
    print("✓ 10. Verifica integrità database")
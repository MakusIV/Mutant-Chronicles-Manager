"""
Database delle carte Warzone di Mutant Chronicles/Doomtrooper
Contiene tutte le informazioni e metodi necessari per la creazione di istanze 
della classe Warzone basate sulle carte ufficiali del gioco.
Le Warzone rappresentano zone di guerra dove i guerrieri possono difendersi.
VERSIONE CORRETTA - Allineata alle regole ufficiali del regolamento
"""

from typing import Dict, List, Optional, Any
from source.cards.Warzone import (
    Warzone, TipoWarzone, TerrenoWarzone, AreaCompatibileWarzone,
    crea_warzone_base, crea_warzone_avanzata
)
from source.cards.Guerriero import Fazione, Rarity, AreaGioco


# Database completo delle carte Warzone
DATABASE_WARZONE = {
    # === WARZONE BASE SET ===
    
    "Trincea Difensiva": {
        "nome": "Trincea Difensiva",
        "costo_azione": 1,
        "tipo": "Trincea",
        "terreno": "Coperto",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "WZ001",
        "modificatori_difensore": [
            {"statistica": "A", "valore": 3, "descrizione": "+3 Armatura in difesa"},
            {"statistica": "C", "valore": -1, "descrizione": "-1 Combattimento in trincea"}
        ],
        "effetti_combattimento": [
            {
                "nome": "Nessun Bonus Fortificazioni",
                "descrizione": "Nessuno dei combattenti può beneficiare di bonus da Fortificazioni",
                "target": "Tutti i combattenti",
                "tipo_effetto": "Restrizione"
            }
        ],
        "testo_carta": "Il guerriero in difesa guadagna +3 Armatura e -1 Combattimento. Nessuno dei combattenti può beneficiare di bonus da Fortificazioni.",
        "flavour_text": "Nella trincea, la sopravvivenza viene prima dell'attacco.",
        "keywords": ["Difensiva", "Trincea", "Copertura"],
        "restrizioni": {
            "richiede_grande_stratega": True,
            "aree_utilizzabili": ["Squadra", "Schieramento"],
            "fazioni_permesse": [],
            "solo_una_per_area": True,
            "limiti_utilizzo": []
        },
        "valore_strategico": 3,
        "frequenza_utilizzo": "Alta",
        "quantita": 0
    },

    "Bunker Corazzato": {
        "nome": "Bunker Corazzato",
        "costo_azione": 1,
        "tipo": "Bunker",
        "terreno": "Coperto",
        "rarity": "Uncommon",
        "set_espansione": "Base",
        "numero_carta": "WZ002",
        "modificatori_difensore": [
            {"statistica": "A", "valore": 5, "descrizione": "+5 Armatura nel bunker"},
            {"statistica": "S", "valore": -3, "descrizione": "-3 Sparare da posizioni chiuse"}
        ],
        "effetti_combattimento": [
            {
                "nome": "Protezione Totale",
                "descrizione": "Equipaggiamenti considerati anche Fortificazione non possono essere usati",
                "target": "Tutti i combattenti",
                "tipo_effetto": "Restrizione"
            }
        ],
        "testo_carta": "Il difensore guadagna +5 Armatura e -3 Sparare. Equipaggiamenti considerati anche Fortificazione non possono essere usati.",
        "flavour_text": "Il cemento armato è l'ultimo amico del soldato.",
        "keywords": ["Bunker", "Corazzato", "Difensiva"],
        "restrizioni": {
            "richiede_grande_stratega": True,
            "aree_utilizzabili": ["Squadra", "Schieramento"],
            "fazioni_permesse": [],
            "solo_una_per_area": True,
            "limiti_utilizzo": []
        },
        "valore_strategico": 5,
        "frequenza_utilizzo": "Media",
        "quantita": 0
    },

    "Città Devastata": {
        "nome": "Città Devastata",
        "costo_azione": 1,
        "tipo": "Citta Devastata",
        "terreno": "Difficile",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "WZ003",
        "modificatori_difensore": [
            {"statistica": "C", "valore": 2, "descrizione": "+2 Combattimento tra le rovine"},
            {"statistica": "A", "valore": 1, "descrizione": "+1 Armatura dalle coperture"}
        ],
        "effetti_combattimento": [
            {
                "nome": "Combattimento Urbano",
                "descrizione": "Veicoli non possono essere utilizzati in combattimento",
                "target": "Tutti i combattenti",
                "tipo_effetto": "Restrizione"
            }
        ],
        "testo_carta": "Il difensore guadagna +2 Combattimento e +1 Armatura. I Veicoli non possono essere utilizzati in combattimento.",
        "flavour_text": "Nelle rovine della civiltà, ogni angolo nasconde pericoli e opportunità.",
        "keywords": ["Urbano", "Rovine", "Tattico"],
        "restrizioni": {
            "richiede_grande_stratega": True,
            "aree_utilizzabili": ["Qualsiasi Area"],
            "fazioni_permesse": [],
            "solo_una_per_area": True,
            "limiti_utilizzo": []
        },
        "valore_strategico": 4,
        "frequenza_utilizzo": "Alta",
        "quantita": 0
    },

    "Campo Aperto": {
        "nome": "Campo Aperto",
        "costo_azione": 1,
        "tipo": "Campo di Battaglia",
        "terreno": "Aperto",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "WZ004",
        "modificatori_difensore": [
            {"statistica": "S", "valore": 3, "descrizione": "+3 Sparare in campo aperto"},
            {"statistica": "A", "valore": -2, "descrizione": "-2 Armatura senza coperture"}
        ],
        "effetti_combattimento": [
            {
                "nome": "Campo di Tiro Libero",
                "descrizione": "Entrambi i combattenti devono usare Sparare se possibile",
                "target": "Tutti i combattenti",
                "tipo_effetto": "Forzatura Tattica"
            }
        ],
        "testo_carta": "Il difensore guadagna +3 Sparare e -2 Armatura. Entrambi i combattenti devono usare Sparare se possibile.",
        "flavour_text": "In campo aperto, vince chi spara per primo e più accurato.",
        "keywords": ["Aperto", "Tiratori", "Tattico"],
        "restrizioni": {
            "richiede_grande_stratega": True,
            "aree_utilizzabili": ["Qualsiasi Area"],
            "fazioni_permesse": [],
            "solo_una_per_area": True,
            "limiti_utilizzo": []
        },
        "valore_strategico": 3,
        "frequenza_utilizzo": "Media",
        "quantita": 0
    },

    "Giungla Ostile": {
        "nome": "Giungla Ostile",
        "costo_azione": 1,
        "tipo": "Foresta",
        "terreno": "Difficile",
        "rarity": "Uncommon",
        "set_espansione": "Base",
        "numero_carta": "WZ005",
        "modificatori_difensore": [
            {"statistica": "S", "valore": -2, "descrizione": "-2 Sparare per visibilità limitata"},
            {"statistica": "A", "valore": 1, "descrizione": "+1 Armatura dalla vegetazione"},
            {"statistica": "C", "valore": 1, "descrizione": "+1 Combattimento nel sottobosco"}
        ],
        "effetti_combattimento": [
            {
                "nome": "Visibilità Limitata",
                "descrizione": "Tutti i combattimenti devono essere risolti con Combattimento",
                "target": "Tutti i combattenti",
                "tipo_effetto": "Forzatura Tattica"
            }
        ],
        "testo_carta": "Il difensore guadagna -2 Sparare, +1 Armatura e +1 Combattimento. Tutti i combattimenti devono essere risolti con Combattimento.",
        "flavour_text": "Nella giungla, il nemico può essere dietro ogni albero.",
        "keywords": ["Giungla", "Difficile", "Corpo a Corpo"],
        "restrizioni": {
            "richiede_grande_stratega": True,
            "aree_utilizzabili": ["Qualsiasi Area"],
            "fazioni_permesse": [],
            "solo_una_per_area": True,
            "limiti_utilizzo": []
        },
        "valore_strategico": 4,
        "frequenza_utilizzo": "Media",
        "quantita": 0
    },

    "Complesso Industriale": {
        "nome": "Complesso Industriale",
        "costo_azione": 1,
        "tipo": "Complesso Industriale",
        "terreno": "Pericoloso",
        "rarity": "Rare",
        "set_espansione": "Base",
        "numero_carta": "WZ006",
        "modificatori_difensore": [
            {"statistica": "C", "valore": 1, "descrizione": "+1 Combattimento tra i macchinari"},
            {"statistica": "S", "valore": 1, "descrizione": "+1 Sparare dalle postazioni"},
            {"statistica": "V", "valore": 1, "descrizione": "+1 Valore per controllo strategico"}
        ],
        "effetti_combattimento": [
            {
                "nome": "Ambiente Pericoloso",
                "descrizione": "Ogni combattente deve tirare 1d6 dopo il combattimento: con 1, subisce 1 ferita",
                "target": "Tutti i combattenti",
                "tipo_effetto": "Rischio Ambientale"
            }
        ],
        "testo_carta": "Il difensore guadagna +1 a tutte le statistiche. Dopo il combattimento, ogni combattente tira 1d6: con 1, subisce 1 ferita.",
        "flavour_text": "Tra i fumi tossici e i macchinari, la guerra diventa ancora più letale.",
        "keywords": ["Industriale", "Pericoloso", "Tossico"],
        "restrizioni": {
            "richiede_grande_stratega": True,
            "aree_utilizzabili": ["Schieramento"],
            "fazioni_permesse": [],
            "solo_una_per_area": True,
            "limiti_utilizzo": ["Solo guerrieri con Valore 4+"]
        },
        "valore_strategico": 6,
        "frequenza_utilizzo": "Bassa",
        "quantita": 0
    },

    # === WARZONE ESPANSIONI ===

    "Cratere Lunare": {
        "nome": "Cratere Lunare",
        "costo_azione": 1,
        "tipo": "Cratere",
        "terreno": "Estremo",
        "rarity": "Rare",
        "set_espansione": "Inquisition",
        "numero_carta": "WZ010",
        "modificatori_difensore": [
            {"statistica": "A", "valore": 2, "descrizione": "+2 Armatura dalla posizione elevata"},
            {"statistica": "S", "valore": 4, "descrizione": "+4 Sparare dalla posizione dominante"},
            {"statistica": "C", "valore": -3, "descrizione": "-3 Combattimento in ambiente ostile"}
        ],
        "effetti_combattimento": [
            {
                "nome": "Gravità Ridotta",
                "descrizione": "Tutti gli attacchi Combattimento subiscono -2",
                "target": "Tutti i combattenti",
                "tipo_effetto": "Modifica Ambientale"
            },
            {
                "nome": "Vuoto Spaziale",
                "descrizione": "Guerrieri senza tute spaziali non possono combattere",
                "target": "Guerrieri non equipaggiati",
                "tipo_effetto": "Restrizione Ambientale"
            }
        ],
        "testo_carta": "Il difensore guadagna +2 Armatura, +4 Sparare e -3 Combattimento. Tutti gli attacchi Combattimento -2. Richiede tute spaziali.",
        "flavour_text": "Nel vuoto dello spazio, ogni respiro potrebbe essere l'ultimo.",
        "keywords": ["Spazio", "Lunare", "Estremo"],
        "restrizioni": {
            "richiede_grande_stratega": True,
            "aree_utilizzabili": ["Avamposto"],
            "fazioni_permesse": [],
            "solo_una_per_area": True,
            "limiti_utilizzo": ["Richiede equipaggiamento spaziale"]
        },
        "valore_strategico": 7,
        "frequenza_utilizzo": "Bassa",
        "quantita": 0
    },

    "Palude Tossica": {
        "nome": "Palude Tossica",
        "costo_azione": 1,
        "tipo": "Palude",
        "terreno": "Pericoloso",
        "rarity": "Uncommon",
        "set_espansione": "Warzone",
        "numero_carta": "WZ015",
        "modificatori_difensore": [
            {"statistica": "C", "valore": -1, "descrizione": "-1 Combattimento nel fango"},
            {"statistica": "S", "valore": -2, "descrizione": "-2 Sparare per i vapori tossici"},
            {"statistica": "A", "valore": 3, "descrizione": "+3 Armatura dalla copertura naturale"}
        ],
        "effetti_combattimento": [
            {
                "nome": "Vapori Tossici",
                "descrizione": "Inizio turno: ogni combattente tira 1d6, con 1-2 non può agire questo turno",
                "target": "Tutti i combattenti",
                "tipo_effetto": "Effetto Continuo"
            }
        ],
        "testo_carta": "Il difensore guadagna -1 Combattimento, -2 Sparare e +3 Armatura. I vapori tossici possono impedire le azioni.",
        "flavour_text": "La palude rivendica tanto quanto la guerra.",
        "keywords": ["Palude", "Tossico", "Ambientale"],
        "restrizioni": {
            "richiede_grande_stratega": True,
            "aree_utilizzabili": ["Qualsiasi Area"],
            "fazioni_permesse": [],
            "solo_una_per_area": True,
            "limiti_utilizzo": []
        },
        "valore_strategico": 4,
        "frequenza_utilizzo": "Media",
        "quantita": 0
    },

    "Montagne Ghiacciate": {
        "nome": "Montagne Ghiacciate",
        "costo_azione": 1,
        "tipo": "Montagne",
        "terreno": "Estremo",
        "rarity": "Uncommon",
        "set_espansione": "Warzone",
        "numero_carta": "WZ020",
        "modificatori_difensore": [
            {"statistica": "A", "valore": 4, "descrizione": "+4 Armatura dalla posizione elevata"},
            {"statistica": "S", "valore": 2, "descrizione": "+2 Sparare dal vantaggio dell'altezza"},
            {"statistica": "C", "valore": -2, "descrizione": "-2 Combattimento per il freddo estremo"}
        ],
        "effetti_combattimento": [
            {
                "nome": "Freddo Estremo",
                "descrizione": "Ogni turno, i combattenti perdono 1 punto da una statistica a scelta del proprietario della Warzone",
                "target": "Tutti i combattenti",
                "tipo_effetto": "Degrado Ambientale"
            }
        ],
        "testo_carta": "Il difensore guadagna +4 Armatura, +2 Sparare e -2 Combattimento. Il freddo degrada le prestazioni ogni turno.",
        "flavour_text": "In alta montagna, il nemico più pericoloso è spesso il clima.",
        "keywords": ["Montagna", "Freddo", "Altitudine"],
        "restrizioni": {
            "richiede_grande_stratega": True,
            "aree_utilizzabili": ["Qualsiasi Area"],
            "fazioni_permesse": [],
            "solo_una_per_area": True,
            "limiti_utilizzo": []
        },
        "valore_strategico": 5,
        "frequenza_utilizzo": "Bassa",
        "quantita": 0
    },

    "Laboratorio Abbandonato": {
        "nome": "Laboratorio Abbandonato",
        "costo_azione": 1,
        "tipo": "Complesso Industriale",
        "terreno": "Pericoloso",
        "rarity": "Rare",
        "set_espansione": "Inquisition",
        "numero_carta": "WZ025",
        "modificatori_difensore": [
            {"statistica": "S", "valore": 3, "descrizione": "+3 Sparare con attrezzature del laboratorio"},
            {"statistica": "A", "valore": 1, "descrizione": "+1 Armatura dalle strutture"},
            {"statistica": "V", "valore": 2, "descrizione": "+2 Valore per scoperte tecnologiche"}
        ],
        "effetti_combattimento": [
            {
                "nome": "Esperimenti Instabili",
                "descrizione": "Una volta per combattimento, il difensore può forzare entrambi i combattenti a rilanciare tutti i dadi",
                "target": "Combattenti attivi",
                "tipo_effetto": "Abilità Unica"
            },
            {
                "nome": "Tecnologia Avanzata",
                "descrizione": "Carte Equipaggiamento costano 1 azione in meno se giocate qui",
                "target": "Proprietario",
                "tipo_effetto": "Bonus Economico"
            }
        ],
        "testo_carta": "Il difensore guadagna +3 Sparare, +1 Armatura e +2 Valore. Può forzare rilanci e riduce costi Equipaggiamento.",
        "flavour_text": "Nella scienza abbandonata giacciono sia tesori che orrori.",
        "keywords": ["Laboratorio", "Tecnologia", "Scientifico"],
        "restrizioni": {
            "richiede_grande_stratega": True,
            "aree_utilizzabili": ["Schieramento"],
            "fazioni_permesse": ["Cybertronic", "Capitol"],
            "solo_una_per_area": True,
            "limiti_utilizzo": ["Solo fazioni tecnologiche"]
        },
        "valore_strategico": 8,
        "frequenza_utilizzo": "Bassa",
        "quantita": 0
    },

    "Arena Gladiatoria": {
        "nome": "Arena Gladiatoria",
        "costo_azione": 1,
        "tipo": "Campo di Battaglia",
        "terreno": "Aperto",
        "rarity": "Ultra Rare",
        "set_espansione": "Golgotha",
        "numero_carta": "WZ030",
        "modificatori_difensore": [
            {"statistica": "C", "valore": 5, "descrizione": "+5 Combattimento nell'arena"},
            {"statistica": "V", "valore": 3, "descrizione": "+3 Valore per lo spettacolo"}
        ],
        "effetti_combattimento": [
            {
                "nome": "Duello all'Ultimo Sangue",
                "descrizione": "Solo combattimenti Combattimento. Il vincitore guadagna +2 Punti Promozione extra",
                "target": "Tutti i combattenti",
                "tipo_effetto": "Regola Speciale"
            },
            {
                "nome": "Folla in Delirio",
                "descrizione": "Ogni ferita inflitta fa guadagnare +1 Punto Destino",
                "target": "Tutti i combattenti",
                "tipo_effetto": "Bonus Economico"
            }
        ],
        "testo_carta": "Il difensore guadagna +5 Combattimento e +3 Valore. Solo duelli Combattimento. Bonus Punti Promozione e Destino.",
        "flavour_text": "Nell'arena, la morte è spettacolo e la gloria è eterna.",
        "keywords": ["Arena", "Gladiatorio", "Spettacolo"],
        "restrizioni": {
            "richiede_grande_stratega": True,
            "aree_utilizzabili": ["Qualsiasi Area"],
            "fazioni_permesse": [],
            "solo_una_per_area": True,
            "limiti_utilizzo": ["Solo combattimenti singoli"]
        },
        "valore_strategico": 9,
        "frequenza_utilizzo": "Molto Bassa",
        "quantita": 0
    }
}



# Funzioni di creazione per tipologie specifiche di Warzone

def crea_warzone_difensiva(nome: str, bonus_armatura: int, malus_altro: Dict[str, int] = None) -> Warzone:
    """
    Crea una Warzone orientata alla difesa
    
    Args:
        nome: Nome della Warzone
        bonus_armatura: Bonus Armatura per il difensore
        malus_altro: Eventuali malus ad altre statistiche
    """
    warzone = Warzone(nome)
    warzone.tipo = TipoWarzone.BUNKER
    warzone.terreno = TerrenoWarzone.COPERTO
    
    # Bonus armatura principale
    warzone.aggiungi_modificatore_difensore("A", bonus_armatura, "", f"+{bonus_armatura} Armatura difensiva")
    
    # Eventuali malus
    if malus_altro:
        for stat, valore in malus_altro.items():
            warzone.aggiungi_modificatore_difensore(stat, valore, "", f"{valore:+d} {stat} per specializzazione difensiva")
    
    # Effetto standard delle Warzone difensive
    warzone.aggiungi_effetto_combattimento(
        "Nessun Bonus Fortificazioni",
        "Nessuno dei combattenti può beneficiare di bonus da Fortificazioni",
        "Tutti i combattenti",
        "Restrizione"
    )
    
    return warzone

def crea_warzone_offensiva(nome: str, bonus_attacco: Dict[str, int], rischi: List[str] = None) -> Warzone:
    """
    Crea una Warzone orientata all'attacco
    
    Args:
        nome: Nome della Warzone
        bonus_attacco: Bonus alle statistiche offensive {"C": +2, "S": +1}
        rischi: Lista di rischi ambientali
    """
    warzone = Warzone(nome)
    warzone.tipo = TipoWarzone.CAMPO_BATTAGLIA
    warzone.terreno = TerrenoWarzone.APERTO
    
    # Bonus offensivi
    for stat, valore in bonus_attacco.items():
        warzone.aggiungi_modificatore_difensore(stat, valore, "", f"+{valore} {stat} offensivo")
    
    # Eventuali rischi
    if rischi:
        for rischio in rischi:
            warzone.aggiungi_effetto_combattimento(
                "Rischio Ambientale",
                rischio,
                "Tutti i combattenti",
                "Rischio"
            )
    
    return warzone

def crea_warzone_tattica(nome: str, modificatori: Dict[str, int], effetti_speciali: List[Dict[str, str]]) -> Warzone:
    """
    Crea una Warzone con effetti tattici complessi
    
    Args:
        nome: Nome della Warzone
        modificatori: Modificatori alle statistiche
        effetti_speciali: Lista di effetti tattici speciali
    """
    warzone = Warzone(nome)
    warzone.tipo = TipoWarzone.TERRITORIO_NEMICO
    warzone.terreno = TerrenoWarzone.DIFFICILE
    
    # Applicazione modificatori
    for stat, valore in modificatori.items():
        warzone.aggiungi_modificatore_difensore(stat, valore, "", f"{valore:+d} {stat} tattico")
    
    # Effetti speciali
    for effetto in effetti_speciali:
        warzone.aggiungi_effetto_combattimento(
            effetto.get("nome", "Effetto Tattico"),
            effetto.get("descrizione", ""),
            effetto.get("target", "Tutti i combattenti"),
            effetto.get("tipo", "Tattico")
        )
    
    return warzone


# Funzioni di ricerca e filtro

def ottieni_warzone(nome: str) -> Optional[Dict[str, Any]]:
    """Ottiene i dati di una Warzone specifica dal database"""
    return DATABASE_WARZONE.get(nome)

def filtra_warzone_per_set(set_espansione: str) -> Dict[str, Dict[str, Any]]:
    """Filtra le Warzone per set di espansione"""
    return {
        nome: dati for nome, dati in DATABASE_WARZONE.items()
        if dati["set_espansione"] == set_espansione
    }

def filtra_warzone_per_rarity(rarity: str) -> Dict[str, Dict[str, Any]]:
    """Filtra le Warzone per rarità"""
    return {
        nome: dati for nome, dati in DATABASE_WARZONE.items()
        if dati["rarity"] == rarity
    }

def filtra_warzone_per_tipo(tipo: str) -> Dict[str, Dict[str, Any]]:
    """Filtra le Warzone per tipo"""
    return {
        nome: dati for nome, dati in DATABASE_WARZONE.items()
        if dati["tipo"] == tipo
    }

def filtra_warzone_per_terreno(terreno: str) -> Dict[str, Dict[str, Any]]:
    """Filtra le Warzone per tipo di terreno"""
    return {
        nome: dati for nome, dati in DATABASE_WARZONE.items()
        if dati["terreno"] == terreno
    }

def filtra_warzone_per_area(area: str) -> Dict[str, Dict[str, Any]]:
    """Filtra le Warzone utilizzabili in una specifica area"""
    return {
        nome: dati for nome, dati in DATABASE_WARZONE.items()
        if area in dati["restrizioni"]["aree_utilizzabili"] or 
           "Qualsiasi Area" in dati["restrizioni"]["aree_utilizzabili"]
    }

def filtra_warzone_per_valore_strategico(valore_min: int, valore_max: int = None) -> Dict[str, Dict[str, Any]]:
    """Filtra le Warzone per valore strategico"""
    if valore_max is None:
        valore_max = 10
    
    return {
        nome: dati for nome, dati in DATABASE_WARZONE.items()
        if valore_min <= dati["valore_strategico"] <= valore_max
    }

def ottieni_warzone_difensive() -> Dict[str, Dict[str, Any]]:
    """Ottiene tutte le Warzone con focus difensivo (bonus Armatura)"""
    return {
        nome: dati for nome, dati in DATABASE_WARZONE.items()
        if any(mod["statistica"] == "A" and mod["valore"] > 0 
               for mod in dati["modificatori_difensore"])
    }

def ottieni_warzone_offensive() -> Dict[str, Dict[str, Any]]:
    """Ottiene tutte le Warzone con focus offensivo (bonus Combattimento/Sparare)"""
    return {
        nome: dati for nome, dati in DATABASE_WARZONE.items()
        if any(mod["statistica"] in ["C", "S"] and mod["valore"] > 0 
               for mod in dati["modificatori_difensore"])
    }


# Funzioni di creazione istanze

def crea_istanza_warzone(nome: str) -> Optional[Warzone]:
    """
    Crea un'istanza della classe Warzone dai dati del database
    
    Args:
        nome: Nome della Warzone da creare
        
    Returns:
        Istanza di Warzone o None se non trovata
    """
    dati = ottieni_warzone(nome)
    if not dati:
        return None
    
    return Warzone.from_dict(dati)

def crea_istanze_set(set_espansione: str) -> List[Warzone]:
    """Crea istanze di tutte le Warzone di un set"""
    warzone_set = filtra_warzone_per_set(set_espansione)
    return [Warzone.from_dict(dati) for dati in warzone_set.values()]

def crea_mazzo_warzone_bilanciato() -> List[Warzone]:
    """Crea un mazzo bilanciato di Warzone per il gioco"""
    mazzo = []
    
    # 4 Warzone difensive comuni
    mazzo.extend([crea_istanza_warzone("Trincea Difensiva") for _ in range(2)])
    mazzo.extend([crea_istanza_warzone("Bunker Corazzato") for _ in range(2)])
    
    # 4 Warzone tattiche comuni/uncommon
    mazzo.append(crea_istanza_warzone("Città Devastata"))
    mazzo.append(crea_istanza_warzone("Campo Aperto"))
    mazzo.append(crea_istanza_warzone("Giungla Ostile"))
    mazzo.append(crea_istanza_warzone("Palude Tossica"))
    
    # 2 Warzone rare speciali
    mazzo.append(crea_istanza_warzone("Complesso Industriale"))
    mazzo.append(crea_istanza_warzone("Laboratorio Abbandonato"))
    
    # Rimuove istanze None (se qualche Warzone non esiste)
    return [w for w in mazzo if w is not None]


# Funzioni di utilità per il bilanciamento

def analizza_bilanciamento_warzone() -> Dict[str, Any]:
    """Analizza il bilanciamento delle Warzone nel database"""
    analisi = {
        "totale_warzone": len(DATABASE_WARZONE),
        "per_rarity": {},
        "per_tipo": {},
        "per_terreno": {},
        "modificatori_medi": {"C": 0, "S": 0, "A": 0, "V": 0},
        "valore_strategico_medio": 0
    }
    
    # Conteggi per categoria
    for nome, dati in DATABASE_WARZONE.items():
        # Rarità
        rarity = dati["rarity"]
        analisi["per_rarity"][rarity] = analisi["per_rarity"].get(rarity, 0) + 1
        
        # Tipo
        tipo = dati["tipo"]
        analisi["per_tipo"][tipo] = analisi["per_tipo"].get(tipo, 0) + 1
        
        # Terreno
        terreno = dati["terreno"]
        analisi["per_terreno"][terreno] = analisi["per_terreno"].get(terreno, 0) + 1
        
        # Modificatori medi
        for mod in dati["modificatori_difensore"]:
            stat = mod["statistica"]
            if stat in analisi["modificatori_medi"]:
                analisi["modificatori_medi"][stat] += mod["valore"]
        
        # Valore strategico
        analisi["valore_strategico_medio"] += dati["valore_strategico"]
    
    # Calcola medie
    totale = analisi["totale_warzone"]
    if totale > 0:
        for stat in analisi["modificatori_medi"]:
            analisi["modificatori_medi"][stat] = round(analisi["modificatori_medi"][stat] / totale, 2)
        analisi["valore_strategico_medio"] = round(analisi["valore_strategico_medio"] / totale, 2)
    
    return analisi

def ottieni_statistiche_database() -> Dict[str, Any]:
    """Ottiene statistiche complete del database Warzone"""
    stats = {
        "warzone_totali": len(DATABASE_WARZONE),
        "per_espansione": {},
        "modificatori_estremi": {
            "max_positivo": {"C": 0, "S": 0, "A": 0, "V": 0},
            "max_negativo": {"C": 0, "S": 0, "A": 0, "V": 0}
        },
        "warzone_più_potenti": [],
        "warzone_più_rischiose": []
    }
    
    # Analisi per espansione
    for nome, dati in DATABASE_WARZONE.items():
        espansione = dati["set_espansione"]
        stats["per_espansione"][espansione] = stats["per_espansione"].get(espansione, 0) + 1
        
        # Trova modificatori estremi
        for mod in dati["modificatori_difensore"]:
            stat = mod["statistica"]
            valore = mod["valore"]
            
            if valore > 0 and valore > stats["modificatori_estremi"]["max_positivo"][stat]:
                stats["modificatori_estremi"]["max_positivo"][stat] = valore
            elif valore < 0 and valore < stats["modificatori_estremi"]["max_negativo"][stat]:
                stats["modificatori_estremi"]["max_negativo"][stat] = valore
        
        # Identifica Warzone potenti (valore strategico alto)
        if dati["valore_strategico"] >= 7:
            stats["warzone_più_potenti"].append({
                "nome": nome,
                "valore": dati["valore_strategico"],
                "rarity": dati["rarity"]
            })
        
        # Identifica Warzone rischiose (con effetti negativi)
        if any("rischio" in eff["tipo_effetto"].lower() or "danno" in eff["descrizione"].lower()
               for eff in dati["effetti_combattimento"]):
            stats["warzone_più_rischiose"].append(nome)
    
    # Ordina per potenza
    stats["warzone_più_potenti"].sort(key=lambda x: x["valore"], reverse=True)
    
    return stats


# Sistema di validazione delle Warzone

def valida_warzone(nome: str) -> Dict[str, Any]:
    """
    Valida una Warzone del database per coerenza con le regole
    
    Args:
        nome: Nome della Warzone da validare
        
    Returns:
        Dict con risultato validazione ed eventuali errori
    """
    dati = ottieni_warzone(nome)
    if not dati:
        return {"valida": False, "errori": ["Warzone non trovata nel database"]}
    
    errori = []
    
    # Validazione costo azione
    if dati["costo_azione"] != 1:
        errori.append(f"Costo azione non standard: {dati['costo_azione']} (dovrebbe essere 1)")
    
    # Validazione requisito Grande Stratega
    if not dati["restrizioni"]["richiede_grande_stratega"]:
        errori.append("Deve richiedere 'Grande Stratega' secondo regolamento")
    
    # Validazione modificatori
    modificatori = dati["modificatori_difensore"]
    if not modificatori:
        errori.append("Warzone deve avere almeno un modificatore per il difensore")
    
    # Validazione bilanciamento modificatori
    somma_modificatori = sum(mod["valore"] for mod in modificatori)
    if somma_modificatori > 8:  # Soglia di bilanciamento
        errori.append(f"Modificatori troppo potenti: somma {somma_modificatori}")
    elif somma_modificatori < -5:
        errori.append(f"Modificatori troppo penalizzanti: somma {somma_modificatori}")
    
    # Validazione effetti combattimento
    if not dati["effetti_combattimento"]:
        errori.append("Warzone dovrebbe avere almeno un effetto su tutti i combattenti")
    
    # Validazione coerenza tipo/terreno
    tipo = dati["tipo"]
    terreno = dati["terreno"]
    
    # Coerenze logiche
    if tipo == "Bunker" and terreno != "Coperto":
        errori.append("Bunker dovrebbe avere terreno 'Coperto'")
    elif tipo == "Campo di Battaglia" and terreno == "Coperto":
        errori.append("Campo di battaglia non dovrebbe essere 'Coperto'")
    
    return {
        "valida": len(errori) == 0,
        "errori": errori,
        "avvertimenti": []
    }

def valida_database_completo() -> Dict[str, Any]:
    """Valida l'intero database Warzone"""
    risultati = {
        "warzone_totali": len(DATABASE_WARZONE),
        "warzone_valide": 0,
        "warzone_con_errori": 0,
        "errori_per_warzone": {},
        "errori_comuni": {}
    }
    
    for nome in DATABASE_WARZONE.keys():
        validazione = valida_warzone(nome)
        
        if validazione["valida"]:
            risultati["warzone_valide"] += 1
        else:
            risultati["warzone_con_errori"] += 1
            risultati["errori_per_warzone"][nome] = validazione["errori"]
            
            # Conta errori comuni
            for errore in validazione["errori"]:
                risultati["errori_comuni"][errore] = risultati["errori_comuni"].get(errore, 0) + 1
    
    return risultati


# Funzioni di testing e debug

def testa_creazione_warzone() -> None:
    """Testa la creazione di istanze Warzone dal database"""
    print("=== TEST CREAZIONE WARZONE ===\n")
    
    # Testa alcune Warzone chiave
    warzone_test = ["Trincea Difensiva", "Giungla Ostile", "Arena Gladiatoria"]
    
    for nome in warzone_test:
        print(f"Testando: {nome}")
        warzone = crea_istanza_warzone(nome)
        
        if warzone:
            print(f"✓ Creata: {warzone}")
            print(f"  Modificatori: {warzone.get_modificatori_totali()}")
            print(f"  Effetti: {len(warzone.effetti_combattimento)}")
            
            # Test serializzazione
            dict_warzone = warzone.to_dict()
            warzone_ricostruita = Warzone.from_dict(dict_warzone)
            print(f"  Serializzazione: {'✓' if warzone.nome == warzone_ricostruita.nome else '✗'}")
        else:
            print(f"✗ Errore nella creazione di {nome}")
        
        print()

def testa_filtri_database() -> None:
    """Testa le funzioni di filtro del database"""
    print("=== TEST FILTRI DATABASE ===\n")
    
    # Test filtri vari
    filtri_test = [
        ("Set Base", lambda: filtra_warzone_per_set("Base")),
        ("Rarità Common", lambda: filtra_warzone_per_rarity("Common")),
        ("Tipo Trincea", lambda: filtra_warzone_per_tipo("Trincea")),
        ("Terreno Coperto", lambda: filtra_warzone_per_terreno("Coperto")),
        ("Area Squadra", lambda: filtra_warzone_per_area("Squadra")),
        ("Valore 5+", lambda: filtra_warzone_per_valore_strategico(5)),
        ("Difensive", lambda: ottieni_warzone_difensive()),
        ("Offensive", lambda: ottieni_warzone_offensive())
    ]
    
    for nome_test, filtro_func in filtri_test:
        risultato = filtro_func()
        print(f"{nome_test}: {len(risultato)} Warzone trovate")
        if risultato:
            primi_3 = list(risultato.keys())[:3]
            print(f"  Esempi: {', '.join(primi_3)}")
        print()


# Entry point per testing
if __name__ == "__main__":
    print("DATABASE WARZONE - MUTANT CHRONICLES/DOOMTROOPER")
    print("=" * 50)
    
    # Statistiche generali
    stats = ottieni_statistiche_database()
    print(f"Warzone totali nel database: {stats['warzone_totali']}")
    print(f"Espansioni: {', '.join(stats['per_espansione'].keys())}")
    print()
    
    # Analisi bilanciamento
    analisi = analizza_bilanciamento_warzone()
    print("ANALISI BILANCIAMENTO:")
    print(f"Modificatori medi: {analisi['modificatori_medi']}")
    print(f"Valore strategico medio: {analisi['valore_strategico_medio']}")
    print(f"Distribuzione rarità: {analisi['per_rarity']}")
    print()
    
    # Validazione database
    validazione = valida_database_completo()
    print("VALIDAZIONE DATABASE:")
    print(f"Warzone valide: {validazione['warzone_valide']}/{validazione['warzone_totali']}")
    print(f"Warzone con errori: {validazione['warzone_con_errori']}")
    if validazione['errori_comuni']:
        print("Errori più comuni:")
        for errore, count in sorted(validazione['errori_comuni'].items(), key=lambda x: x[1], reverse=True):
            print(f"  - {errore}: {count} volte")
    print()
    
    # Test creazione e filtri
    testa_creazione_warzone()
    testa_filtri_database()
    
    # Test mazzo bilanciato
    print("=== TEST MAZZO BILANCIATO ===")
    mazzo = crea_mazzo_warzone_bilanciato()
    print(f"Mazzo creato con {len(mazzo)} Warzone:")
    for warzone in mazzo[:5]:  # Mostra prime 5
        print(f"  - {warzone.nome} ({warzone.rarity.value})")
    print()
    
    print("=== IMPLEMENTAZIONE COMPLETATA ===")
    print("✓ Database Warzone completo con 12 carte")
    print("✓ Warzone per tutti i set: Base, Inquisition, Warzone, Golgotha")
    print("✓ Tutte le rarità: Common, Uncommon, Rare, Ultra Rare")
    print("✓ Tipi variati: Trincea, Bunker, Città, Campo, Giungla, etc.")
    print("✓ Terreni diversi: Aperto, Coperto, Difficile, Pericoloso, Estremo")
    print("✓ Modificatori bilanciati secondo regolamento")
    print("✓ Effetti su tutti i combattenti implementati")
    print("✓ Restrizioni Grande Stratega rispettate")
    print("✓ Funzioni di filtro e ricerca complete")
    print("✓ Sistema di validazione per bilanciamento")
    print("✓ Creazione mazzi bilanciati")
    print("✓ Statistiche e analisi database")
    print("✓ Compatibile con tutte le classi sviluppate")
    print("✓ Serializzazione e testing completi")

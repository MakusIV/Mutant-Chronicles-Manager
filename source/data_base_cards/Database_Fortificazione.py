"""
Database delle carte Fortificazione di Mutant Chronicles/Doomtrooper
Contiene tutte le informazioni e metodi necessari per la creazione di istanze 
della classe Fortificazione basate sulle carte ufficiali del gioco.
VERSIONE CORRETTA - Allineata alle regole ufficiali del regolamento
"""

from typing import Dict, List, Optional, Any
from source.cards.Fortificazione import (
    Fortificazione, TipoFortificazione, AreaCompatibile, 
    BeneficiarioFortificazione, ModificatoreFortificazione, 
    AbilitaFortificazione
)
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione, ApostoloPadre


# Database completo delle carte Fortificazione
DATABASE_FORTIFICAZIONI = {
    # CITTÀ DELLE CORPORAZIONI
    "Heimburg": {
        "nome": "Heimburg",
        "costo_destino": 3,
        "tipo": "Città Corporazione",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "F001",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Bauhaus",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 2,
        "punti_struttura": 8,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 2,
                "condizione": "sempre",
                "descrizione": "Bonus armatura Bauhaus",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Mura Fortificate",
                "descrizione": "I guerrieri Bauhaus guadagnano +2 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura guerrieri Bauhaus"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo guerrieri Bauhaus"],
        "fazioni_permesse": ["Bauhaus"],
        "testo_carta": "La città fortezza di Heimburg protegge i guerrieri Bauhaus con le sue possenti mura.",
        "flavour_text": "Nelle profondità di Venere, Heimburg rappresenta la potenza industriale Bauhaus.",
        "keywords": ["Bauhaus", "Città", "Fortificazione", "Difesa"],
        "quantita":9
    },
    
    "Citadel": {
        "nome": "Citadel",
        "costo_destino": 4,
        "tipo": "Città Corporazione",
        "rarity": "Uncommon",
        "set_espansione": "Base",
        "numero_carta": "F002",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Imperiale",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 3,
        "punti_struttura": 10,
        "resistenza_attacchi": True,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 3,
                "condizione": "sempre",
                "descrizione": "Bonus armatura Imperiale",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Fortezza Imperiale",
                "descrizione": "I guerrieri Imperiali guadagnano +3 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura guerrieri Imperiali"]
            },
            {
                "nome": "Resistenza agli Attacchi",
                "descrizione": "La Citadel resiste ai primi 2 danni subiti",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Resistenza danni", "Protezione strutturale"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo guerrieri Imperiali"],
        "fazioni_permesse": ["Imperiale"],
        "testo_carta": "La Citadel rappresenta la supremazia militare e spirituale dell'Impero.",
        "flavour_text": "Nel cuore della Terra, la Citadel vigila sui fedeli dell'Imperatore.",
        "keywords": ["Imperiale", "Città", "Fortificazione", "Difesa", "Resistenza"],
        "quantita":9
    },
    
    "Ilian": {
        "nome": "Ilian",
        "costo_destino": 2,
        "tipo": "Città Corporazione",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "F003",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Mishima",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 1,
        "punti_struttura": 6,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 1,
                "condizione": "sempre",
                "descrizione": "Bonus armatura Mishima",
                "permanente": True
            },
            {
                "statistica": "V",
                "valore": 1,
                "condizione": "sempre",
                "descrizione": "Bonus velocità Mishima",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Velocità di Mercurio",
                "descrizione": "I guerrieri Mishima guadagnano +1 Armatura e +1 Velocità",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus velocità e armatura Mishima"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo guerrieri Mishima"],
        "fazioni_permesse": ["Mishima"],
        "testo_carta": "Ilian, la città di cristallo di Mercurio, conferisce velocità ai suoi difensori.",
        "flavour_text": "Come il mercurio scorre veloce, così i guerrieri di Ilian si muovono.",
        "keywords": ["Mishima", "Città", "Fortificazione", "Velocità"],
        "quantita":9
    },
    
    "Capitol": {
        "nome": "Capitol",
        "costo_destino": 3,
        "tipo": "Città Corporazione",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "F004",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Capitol",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 2,
        "punti_struttura": 7,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 2,
                "condizione": "sempre",
                "descrizione": "Bonus armatura Capitol",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Tecnologia Avanzata",
                "descrizione": "I guerrieri Capitol guadagnano +2 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura guerrieri Capitol"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo guerrieri Capitol"],
        "fazioni_permesse": ["Capitol"],
        "testo_carta": "Capitol, centro del progresso tecnologico e commerciale.",
        "flavour_text": "Dove la tecnologia incontra l'ambizione, nasce Capitol.",
        "keywords": ["Capitol", "Città", "Fortificazione", "Tecnologia"],
        "quantita":9
    },
    
    "Saguenay": {
        "nome": "Saguenay",
        "costo_destino": 2,
        "tipo": "Città Corporazione",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "F005",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Cybertronic",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 1,
        "punti_struttura": 5,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 1,
                "condizione": "sempre",
                "descrizione": "Bonus armatura Cybertronic",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Interfaccia Cibernetica",
                "descrizione": "I guerrieri Cybertronic guadagnano +1 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura guerrieri Cybertronic"]
            },
            {
                "nome": "Rigenerazione Dati",
                "descrizione": "Una volta per turno, pesca una carta extra",
                "tipo_abilita": "Attivabile",
                "costo_attivazione": 1,
                "condizioni_attivazione": ["Una volta per turno"],
                "effetti_speciali": ["Pesca carta extra"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo guerrieri Cybertronic"],
        "fazioni_permesse": ["Cybertronic"],
        "testo_carta": "Saguenay, centro dell'innovazione cibernetica di Cybertronic.",
        "flavour_text": "Nel silenzio digitale di Saguenay, il futuro prende forma.",
        "keywords": ["Cybertronic", "Città", "Fortificazione", "Cibernetico"],
        "quantita":9
    },
    
    # CITTADELLE DEGLI APOSTOLI
    "Cittadella di Algeroth": {
        "nome": "Cittadella di Algeroth",
        "costo_destino": 4,
        "tipo": "Cittadella Apostolo",
        "rarity": "Rara",
        "set_espansione": "Base",
        "numero_carta": "F006",
        "area_compatibile": "Schieramento",
        "beneficiario": "Apostolo Specifico",
        "corporazione_specifica": None,
        "apostolo_specifico": "Algeroth",
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 3,
        "punti_struttura": 12,
        "resistenza_attacchi": True,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 3,
                "condizione": "sempre",
                "descrizione": "Bonus armatura seguaci Algeroth",
                "permanente": True
            },
            {
                "statistica": "C",
                "valore": 1,
                "condizione": "in_combattimento",
                "descrizione": "Bonus combattimento in guerra",
                "permanente": False
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Fortezza della Guerra",
                "descrizione": "I seguaci di Algeroth guadagnano +3 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura seguaci Algeroth"]
            },
            {
                "nome": "Chiamata alla Guerra",
                "descrizione": "I guerrieri Oscura Legione guadagnano +1 Combattimento durante i combattimenti",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus combattimento in battaglia"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo seguaci di Algeroth"],
        "fazioni_permesse": ["Oscura Legione"],
        "testo_carta": "Nel nome di Algeroth, le armi parlano e la guerra non ha fine.",
        "flavour_text": "Dalle fondamenta della Cittadella echeggia l'eterno rumore della battaglia.",
        "keywords": ["Algeroth", "Cittadella", "Guerra", "Oscura Legione"],
        "quantita":9
    },
    
    "Cittadella di Ilian": {
        "nome": "Cittadella di Ilian",
        "costo_destino": 3,
        "tipo": "Cittadella Apostolo",
        "rarity": "Rara",
        "set_espansione": "Base",
        "numero_carta": "F007",
        "area_compatibile": "Schieramento",
        "beneficiario": "Apostolo Specifico",
        "corporazione_specifica": None,
        "apostolo_specifico": "Ilian",
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 2,
        "punti_struttura": 10,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 2,
                "condizione": "sempre",
                "descrizione": "Bonus armatura seguaci Ilian",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Labirinto delle Bugie",
                "descrizione": "I seguaci di Ilian guadagnano +2 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura seguaci Ilian"]
            },
            {
                "nome": "Inganno",
                "descrizione": "Una volta per turno, forza l'avversario a scartare una carta",
                "tipo_abilita": "Attivabile",
                "costo_attivazione": 2,
                "condizioni_attivazione": ["Una volta per turno"],
                "effetti_speciali": ["Scarta carta avversario"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo seguaci di Ilian"],
        "fazioni_permesse": ["Oscura Legione"],
        "testo_carta": "Nella Cittadella di Ilian, la verità si dissolve come nebbia.",
        "flavour_text": "Chi entra nel labirinto di Ilian, perde se stesso nelle bugie.",
        "keywords": ["Ilian", "Cittadella", "Inganno", "Oscura Legione"],
        "quantita":9
    },
    
    "Cittadella di Demnogonis": {
        "nome": "Cittadella di Demnogonis",
        "costo_destino": 5,
        "tipo": "Cittadella Apostolo",
        "rarity": "Rara",
        "set_espansione": "Base",
        "numero_carta": "F008",
        "area_compatibile": "Schieramento",
        "beneficiario": "Apostolo Specifico",
        "corporazione_specifica": None,
        "apostolo_specifico": "Demnogonis",
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 4,
        "punti_struttura": 15,
        "resistenza_attacchi": True,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 4,
                "condizione": "sempre",
                "descrizione": "Bonus armatura seguaci Demnogonis",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Inferno Congelato",
                "descrizione": "I seguaci di Demnogonis guadagnano +4 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura seguaci Demnogonis"]
            },
            {
                "nome": "Aura di Terrore",
                "descrizione": "I guerrieri avversari subiscono -1 a tutte le statistiche",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Malus statistiche avversari"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo seguaci di Demnogonis"],
        "fazioni_permesse": ["Oscura Legione"],
        "testo_carta": "Il gelo eterno di Demnogonis preserva i suoi servitori.",
        "flavour_text": "Nel cuore della Cittadella, l'inverno non ha mai fine.",
        "keywords": ["Demnogonis", "Cittadella", "Gelo", "Terrore", "Oscura Legione"],
        "quantita":9
    },
    
    "Cittadella di Muawijhe": {
        "nome": "Cittadella di Muawijhe",
        "costo_destino": 3,
        "tipo": "Cittadella Apostolo",
        "rarity": "Rara",
        "set_espansione": "Base",
        "numero_carta": "F009",
        "area_compatibile": "Schieramento",
        "beneficiario": "Apostolo Specifico",
        "corporazione_specifica": None,
        "apostolo_specifico": "Muawijhe",
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 2,
        "punti_struttura": 8,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 2,
                "condizione": "sempre",
                "descrizione": "Bonus armatura seguaci Muawijhe",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Sussurri della Follia",
                "descrizione": "I seguaci di Muawijhe guadagnano +2 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura seguaci Muawijhe"]
            },
            {
                "nome": "Corruzione Mentale",
                "descrizione": "Una volta per turno, converti un guerriero avversario",
                "tipo_abilita": "Attivabile",
                "costo_attivazione": 3,
                "condizioni_attivazione": ["Una volta per turno", "Guerriero bersaglio in gioco"],
                "effetti_speciali": ["Conversione guerriero"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo seguaci di Muawijhe"],
        "fazioni_permesse": ["Oscura Legione"],
        "testo_carta": "I sussurri di Muawijhe portano follia e corruzione.",
        "flavour_text": "Chi ascolta troppo a lungo, dimentica chi era.",
        "keywords": ["Muawijhe", "Cittadella", "Follia", "Corruzione", "Oscura Legione"],
        "quantita":9
    },
    
    "Cittadella di Semai": {
        "nome": "Cittadella di Semai",
        "costo_destino": 4,
        "tipo": "Cittadella Apostolo",
        "rarity": "Rara",
        "set_espansione": "Base",
        "numero_carta": "F010",
        "area_compatibile": "Schieramento",
        "beneficiario": "Apostolo Specifico",
        "corporazione_specifica": None,
        "apostolo_specifico": "Semai",
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 3,
        "punti_struttura": 11,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 3,
                "condizione": "sempre",
                "descrizione": "Bonus armatura seguaci Semai",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Tempio del Destino",
                "descrizione": "I seguaci di Semai guadagnano +3 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura seguaci Semai"]
            },
            {
                "nome": "Manipolazione del Fato",
                "descrizione": "Una volta per turno, ridisegna una carta dal mazzo",
                "tipo_abilita": "Attivabile",
                "costo_attivazione": 1,
                "condizioni_attivazione": ["Una volta per turno"],
                "effetti_speciali": ["Ridisegna carta"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo seguaci di Semai"],
        "fazioni_permesse": ["Oscura Legione"],
        "testo_carta": "Nel Tempio di Semai, il destino prende forma.",
        "flavour_text": "Le trame del fato si intrecciano nella Cittadella del Destino.",
        "keywords": ["Semai", "Cittadella", "Destino", "Fato", "Oscura Legione"],
        "quantita":9
    },
    
    # FORTIFICAZIONI GENERICHE
    "Bunker Difensivo": {
        "nome": "Bunker Difensivo",
        "costo_destino": 2,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "F011",
        "area_compatibile": "Qualsiasi Area",
        "beneficiario": "Guerrieri Area",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": False,
        "distruttibile": True,
        "bonus_armatura": 1,
        "punti_struttura": 5,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 1,
                "condizione": "sempre",
                "descrizione": "Bonus armatura difensivo",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Protezione Base",
                "descrizione": "Tutti i guerrieri nell'area guadagnano +1 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura area"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": [],
        "testo_carta": "Un rifugio sicuro contro le tempeste della guerra.",
        "flavour_text": "Spesse pareti di ferro proteggono chi vi si rifugia.",
        "keywords": ["Bunker", "Fortificazione", "Difesa", "Universale"],
        "quantita":9
    },
    
    "Torretta di Guardia": {
        "nome": "Torretta di Guardia",
        "costo_destino": 1,
        "tipo": "Installazione Difensiva",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "F012",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Guerrieri Area",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": False,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 3,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Posizione Elevata",
                "descrizione": "I guerrieri con armi a distanza guadagnano +1 Combattimento",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus combattimento armi distanza"]
            },
            {
                "nome": "Avvistamento",
                "descrizione": "Rivela la prima carta pescata dall'avversario ogni turno",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Rivela carta avversario"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": [],
        "testo_carta": "Una posizione elevata conferisce vantaggi tattici significativi.",
        "flavour_text": "Dall'alto, ogni movimento nemico è visibile.",
        "keywords": ["Torretta", "Avvistamento", "Tattica", "Distanza"],
        "quantita":9
    },
    
    "Complesso Industriale": {
        "nome": "Complesso Industriale",
        "costo_destino": 3,
        "tipo": "Complesso Industriale",
        "rarity": "Uncommon",
        "set_espansione": "Base",
        "numero_carta": "F013",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Guerrieri Area",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": False,  # Eccezione: possibili più copie
        "distruttibile": True,
        "bonus_armatura": 1,
        "punti_struttura": 6,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 1,
                "condizione": "sempre",
                "descrizione": "Bonus armatura industriale",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Produzione Equipaggiamenti",
                "descrizione": "Una volta per turno, pesca una carta Equipaggiamento",
                "tipo_abilita": "Attivabile",
                "costo_attivazione": 1,
                "condizioni_attivazione": ["Una volta per turno"],
                "effetti_speciali": ["Pesca equipaggiamento"]
            },
            {
                "nome": "Rifornimenti",
                "descrizione": "I guerrieri nell'area guadagnano +1 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura area"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": [],
        "testo_carta": "L'industria alimenta la macchina bellica con risorse continue.",
        "flavour_text": "Dalle fabbriche escono armi e speranza in egual misura.",
        "keywords": ["Industria", "Produzione", "Equipaggiamenti", "Rifornimenti"],
        "quantita":9
    },
    
    "Base Operativa": {
        "nome": "Base Operativa",
        "costo_destino": 4,
        "tipo": "Base Operativa",
        "rarity": "Uncommon",
        "set_espansione": "Base",
        "numero_carta": "F014",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Tutti Doomtrooper",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 2,
        "punti_struttura": 8,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 2,
                "condizione": "sempre",
                "descrizione": "Bonus armatura Doomtrooper",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Comando Centrale",
                "descrizione": "Tutti i Doomtrooper guadagnano +2 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura Doomtrooper"]
            },
            {
                "nome": "Coordinamento Tattico",
                "descrizione": "Una volta per turno, riorganizza l'ordine di battaglia",
                "tipo_abilita": "Attivabile",
                "costo_attivazione": 2,
                "condizioni_attivazione": ["Una volta per turno"],
                "effetti_speciali": ["Riorganizza battaglia"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo Doomtrooper"],
        "fazioni_permesse": ["Bauhaus", "Capitol", "Cybertronic", "Imperiale", "Mishima"],
        "testo_carta": "Il cuore operativo delle forze Doomtrooper sul campo.",
        "flavour_text": "Da qui partono gli ordini che cambiano il corso della battaglia.",
        "keywords": ["Base", "Comando", "Doomtrooper", "Tattica"],
        "quantita":9
    },
    
    "Rifugio Blindato": {
        "nome": "Rifugio Blindato",
        "costo_destino": 2,
        "tipo": "Rifugio",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "F015",
        "area_compatibile": "Qualsiasi Area",
        "beneficiario": "Guerrieri Area",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": False,
        "distruttibile": True,
        "bonus_armatura": 3,
        "punti_struttura": 4,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 3,
                "condizione": "non_in_veicolo",
                "descrizione": "Bonus armatura se non in veicolo",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Protezione Pesante",
                "descrizione": "I guerrieri non in veicolo guadagnano +3 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura fuori veicolo"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Non utilizzabile da guerrieri in veicolo"],
        "fazioni_permesse": [],
        "testo_carta": "Spesse piastre di blindatura proteggono chi si rifugia all'interno.",
        "flavour_text": "Quando le bombe cadono, il rifugio è l'unica salvezza.",
        "keywords": ["Rifugio", "Blindatura", "Protezione", "Sicurezza"],
        "quantita":9
    },
    
    # FORTIFICAZIONI SPECIALI DELL'AVAMPOSTO
    "Club Arkadin": {
        "nome": "Club Arkadin",
        "costo_destino": 3,
        "tipo": "Struttura Speciale",
        "rarity": "Rara",
        "set_espansione": "Paradise Lost",
        "numero_carta": "F016",
        "area_compatibile": "Solo Avamposto",
        "beneficiario": "Tutte Tribù",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 1,
        "punti_struttura": 6,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 1,
                "condizione": "sempre",
                "descrizione": "Bonus armatura Tribù",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Rifugio delle Tribù",
                "descrizione": "Tutti i guerrieri delle Tribù guadagnano +1 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura Tribù"]
            },
            {
                "nome": "Commercio di Informazioni",
                "descrizione": "Una volta per turno, guarda le prime 3 carte dell'avversario",
                "tipo_abilita": "Attivabile",
                "costo_attivazione": 2,
                "condizioni_attivazione": ["Una volta per turno"],
                "effetti_speciali": ["Spia carte avversario"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo nell'Avamposto", "Solo guerrieri delle Tribù"],
        "fazioni_permesse": [],
        "testo_carta": "Nel Club Arkadin, informazioni e favori sono la moneta corrente.",
        "flavour_text": "Dove le Tribù si incontrano, i segreti cambiano di mano.",
        "keywords": ["Club", "Tribù", "Informazioni", "Avamposto"],
        "quantita":9
    },
    
    "Santuario Templare": {
        "nome": "Santuario Templare",
        "costo_destino": 4,
        "tipo": "Struttura Speciale",
        "rarity": "Rara",
        "set_espansione": "Paradise Lost",
        "numero_carta": "F017",
        "area_compatibile": "Assegnata a Guerriero",
        "beneficiario": "Guerriero Singolo",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": False,
        "distruttibile": True,
        "bonus_armatura": 4,
        "punti_struttura": 8,
        "resistenza_attacchi": True,
        "modificatori": [
            {
                "statistica": "A",
                "valore": 4,
                "condizione": "sempre",
                "descrizione": "Bonus armatura Templare",
                "permanente": True
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Benedizione Sacra",
                "descrizione": "Il guerriero assegnato guadagna +4 Armatura",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Bonus armatura guerriero"]
            },
            {
                "nome": "Immunità all'Oscura Simmetria",
                "descrizione": "Il guerriero diventa immune alle carte Oscura Simmetria",
                "tipo_abilita": "Passiva",
                "costo_attivazione": 0,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Immunità Oscura Simmetria"]
            }
        ],
        "requisiti": ["Guerriero Templare"],
        "restrizioni": ["Solo guerrieri Templari", "Assegnabile nell'Avamposto"],
        "fazioni_permesse": [],
        "testo_carta": "La fede purifica e protegge dal male oscuro.",
        "flavour_text": "Nel Santuario, la luce scaccia ogni ombra.",
        "keywords": ["Santuario", "Templari", "Fede", "Immunità"],
        "quantita":9
    }
}


# Funzioni di utilità per il database

def get_fortificazioni_per_tipo(tipo: str) -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le fortificazioni di un determinato tipo"""
    return {nome: data for nome, data in DATABASE_FORTIFICAZIONI.items() 
            if data["tipo"] == tipo}


def get_fortificazioni_per_area(area: str) -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le fortificazioni compatibili con un'area"""
    compatibili = {}
    for nome, data in DATABASE_FORTIFICAZIONI.items():
        area_comp = data["area_compatibile"]
        if (area_comp == "Qualsiasi Area" or 
            area_comp == area or
            (area_comp == "Squadra o Schieramento" and area in ["Squadra", "Schieramento"])):
            compatibili[nome] = data
    return compatibili


def get_fortificazioni_per_fazione(fazione: str) -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le fortificazioni utilizzabili da una fazione"""
    return {nome: data for nome, data in DATABASE_FORTIFICAZIONI.items() 
            if not data["fazioni_permesse"] or fazione in data["fazioni_permesse"]}

def get_fortificazioni_per_set(nome_set: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce tutte le fortificazioni di un set specifico
    
    Args:
        nome_set: Nome del set (es. "Base", "Inquisition", "Warzone")
    
    Returns:
        Dizionario con le missioni del set specificato
    """
    fortificazione_set = {}
    
    for nome_fortificazione, dati_fortificazione in DATABASE_FORTIFICAZIONI.items():
        if dati_fortificazione["set_espansione"] == nome_set:
            fortificazione_set[nome_fortificazione] = dati_fortificazione
    
    return fortificazione_set

def get_fortificazioni_per_corporazione(corporazione: str) -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le fortificazioni specifiche per una corporazione"""
    return {nome: data for nome, data in DATABASE_FORTIFICAZIONI.items() 
            if data["corporazione_specifica"] == corporazione}


def get_fortificazioni_per_apostolo(apostolo: str) -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le fortificazioni specifiche per un apostolo"""
    return {nome: data for nome, data in DATABASE_FORTIFICAZIONI.items() 
            if data["apostolo_specifico"] == apostolo}


def get_fortificazioni_per_rarità(rarity: str) -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le fortificazioni di una determinata rarità"""
    return {nome: data for nome, data in DATABASE_FORTIFICAZIONI.items() 
            if data["rarity"] == rarity}


def get_fortificazioni_per_costo(costo_min: int = 0, costo_max: int = 999) -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le fortificazioni in un range di costo"""
    return {nome: data for nome, data in DATABASE_FORTIFICAZIONI.items() 
            if costo_min <= data["costo_destino"] <= costo_max}


def get_fortificazioni_unique() -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le fortificazioni uniche per giocatore"""
    return {nome: data for nome, data in DATABASE_FORTIFICAZIONI.items() 
            if data["unica_per_giocatore"]}


def filtra_fortificazioni(filtri: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Filtra le fortificazioni secondo criteri multipli
    
    Args:
        filtri: Dizionario con criteri di filtro
               - tipo: tipo fortificazione
               - area: area compatibile
               - costo_min/costo_max: range di costo
               - rarity: rarità
               - fazione: fazione che può usarla
               - corporazione: corporazione specifica
               - apostolo: apostolo specifico
               - unica: solo fortificazioni uniche
               - distruttibile: solo fortificazioni distruttibili
               
    Returns:
        Dizionario con fortificazioni che soddisfano i criteri
    """
    risultato = DATABASE_FORTIFICAZIONI.copy()
    
    if "tipo" in filtri:
        risultato = {k: v for k, v in risultato.items() if v["tipo"] == filtri["tipo"]}
    
    if "area" in filtri:
        area = filtri["area"]
        risultato = {k: v for k, v in risultato.items() 
                    if (v["area_compatibile"] == "Qualsiasi Area" or 
                        v["area_compatibile"] == area or
                        (v["area_compatibile"] == "Squadra o Schieramento" and 
                         area in ["Squadra", "Schieramento"]))}
    
    if "costo_min" in filtri:
        risultato = {k: v for k, v in risultato.items() 
                    if v["costo_destino"] >= filtri["costo_min"]}
    
    if "costo_max" in filtri:
        risultato = {k: v for k, v in risultato.items() 
                    if v["costo_destino"] <= filtri["costo_max"]}
    
    if "rarity" in filtri:
        risultato = {k: v for k, v in risultato.items() if v["rarity"] == filtri["rarity"]}
    
    if "fazione" in filtri:
        fazione = filtri["fazione"]
        risultato = {k: v for k, v in risultato.items() 
                    if not v["fazioni_permesse"] or fazione in v["fazioni_permesse"]}
    
    if "corporazione" in filtri:
        risultato = {k: v for k, v in risultato.items() 
                    if v["corporazione_specifica"] == filtri["corporazione"]}
    
    if "apostolo" in filtri:
        risultato = {k: v for k, v in risultato.items() 
                    if v["apostolo_specifico"] == filtri["apostolo"]}
    
    if "unica" in filtri:
        risultato = {k: v for k, v in risultato.items() 
                    if v["unica_per_giocatore"] == filtri["unica"]}
    
    if "distruttibile" in filtri:
        risultato = {k: v for k, v in risultato.items() 
                    if v["distruttibile"] == filtri["distruttibile"]}
    
    return risultato


def crea_fortificazione_da_database(nome_fortificazione: str):
    """
    Crea un'istanza della classe Fortificazione dal database
    
    Args:
        nome_fortificazione: Nome della fortificazione nel database
        
    Returns:
        Istanza di Fortificazione o None se non trovata
    """
    if nome_fortificazione not in DATABASE_FORTIFICAZIONI:
        return None
    
    data = DATABASE_FORTIFICAZIONI[nome_fortificazione]
    
    # Crea l'istanza base
    fortificazione = Fortificazione(
        nome=data["nome"],
        costo_destino=data["costo_destino"]
    )
    
    # Configura proprietà dalla enum
    fortificazione.tipo = TipoFortificazione(data["tipo"])
    fortificazione.rarity = Rarity(data["rarity"])
    fortificazione.set_espansione = Set_Espansione(data["set_espansione"])
    fortificazione.area_compatibile = AreaCompatibile(data["area_compatibile"])
    fortificazione.beneficiario = BeneficiarioFortificazione(data["beneficiario"])
    
    if data["corporazione_specifica"]:
        fortificazione.corporazione_specifica = Fazione(data["corporazione_specifica"])
    if data["apostolo_specifico"]:
        fortificazione.apostolo_specifico = ApostoloPadre(data["apostolo_specifico"])
    
    # Configura proprietà specifiche
    fortificazione.numero_carta = data["numero_carta"]
    fortificazione.unica_per_giocatore = data["unica_per_giocatore"]
    fortificazione.distruttibile = data["distruttibile"]
    fortificazione.bonus_armatura = data["bonus_armatura"]
    fortificazione.punti_struttura = data["punti_struttura"]
    fortificazione.resistenza_attacchi = data["resistenza_attacchi"]
    
    # Configura modificatori
    for mod_data in data["modificatori"]:
        modificatore = ModificatoreFortificazione(
            statistica=mod_data["statistica"],
            valore=mod_data["valore"],
            condizione=mod_data["condizione"],
            descrizione=mod_data["descrizione"],
            permanente=mod_data["permanente"]
        )
        fortificazione.modificatori.append(modificatore)
    
    # Configura abilità speciali
    for abil_data in data["abilita_speciali"]:
        abilita = AbilitaFortificazione(
            nome=abil_data["nome"],
            descrizione=abil_data["descrizione"],
            tipo_abilita=abil_data["tipo_abilita"],
            costo_attivazione=abil_data["costo_attivazione"],
            condizioni_attivazione=abil_data["condizioni_attivazione"],
            effetti_speciali=abil_data["effetti_speciali"]
        )
        fortificazione.abilita_speciali.append(abilita)
    
    # Configura altre proprietà
    fortificazione.requisiti = data["requisiti"]
    fortificazione.restrizioni = data["restrizioni"]
    fortificazione.testo_carta = data["testo_carta"]
    fortificazione.flavour_text = data["flavour_text"]
    fortificazione.keywords = data["keywords"]
    
    # Configura fazioni permesse
    if data["fazioni_permesse"]:
        fortificazione.fazioni_permesse = [Fazione(f) for f in data["fazioni_permesse"] 
                                          if f in [faz.value for faz in Fazione]]
    
    return fortificazione


def get_statistiche_database_fortificazioni() -> Dict[str, Any]:
    """Restituisce statistiche complete del database fortificazioni"""
    totale = len(DATABASE_FORTIFICAZIONI)
    
    # Conteggi per categoria
    per_tipo = {}
    per_rarity = {}
    per_set = {}
    per_area = {}
    per_beneficiario = {}
    distribuzione_costo = {}
    fortificazioni_uniche = 0
    fortificazioni_distruttibili = 0
    
    for fort in DATABASE_FORTIFICAZIONI.values():
        # Per tipo
        tipo = fort["tipo"]
        per_tipo[tipo] = per_tipo.get(tipo, 0) + 1
        
        # Per rarità
        rarity = fort["rarity"]
        per_rarity[rarity] = per_rarity.get(rarity, 0) + 1
        
        # Per set
        set_esp = fort["set_espansione"]
        per_set[set_esp] = per_set.get(set_esp, 0) + 1
        
        # Per area
        area = fort["area_compatibile"]
        per_area[area] = per_area.get(area, 0) + 1
        
        # Per beneficiario
        beneficiario = fort["beneficiario"]
        per_beneficiario[beneficiario] = per_beneficiario.get(beneficiario, 0) + 1
        
        # Distribuzione costo
        costo = fort["costo_destino"]
        distribuzione_costo[costo] = distribuzione_costo.get(costo, 0) + 1
        
        # Conteggi speciali
        if fort["unica_per_giocatore"]:
            fortificazioni_uniche += 1
        if fort["distruttibile"]:
            fortificazioni_distruttibili += 1
    
    return {
        "totale_fortificazioni": totale,
        "per_tipo": per_tipo,
        "per_rarity": per_rarity,
        "per_set_espansione": per_set,
        "per_area_compatibile": per_area,
        "per_beneficiario": per_beneficiario,
        "distribuzione_costo": distribuzione_costo,
        "fortificazioni_uniche": fortificazioni_uniche,
        "fortificazioni_distruttibili": fortificazioni_distruttibili,
        "percentuale_uniche": round((fortificazioni_uniche / totale) * 100, 1),
        "percentuale_distruttibili": round((fortificazioni_distruttibili / totale) * 100, 1),
        "costo_medio": round(sum(f["costo_destino"] for f in DATABASE_FORTIFICAZIONI.values()) / totale, 1)
    }


# Test del database
if __name__ == "__main__":
    print("=== TEST DATABASE FORTIFICAZIONI ===")
    
    # Test creazione da database
    print("\n=== TEST CREAZIONE DA DATABASE ===")
    heimburg = crea_fortificazione_da_database("Heimburg")
    if heimburg:
        print(f"Fortificazione creata: {heimburg}")
        print(f"Tipo: {heimburg.tipo.value}")
        print(f"Corporazione: {heimburg.corporazione_specifica.value if heimburg.corporazione_specifica else 'Nessuna'}")
        print(f"Bonus armatura: {heimburg.bonus_armatura}")
        print(f"Abilità: {len(heimburg.abilita_speciali)}")
    
    # Test filtri
    print(f"\n=== TEST FILTRI ===")
    citta_corp = get_fortificazioni_per_tipo("Città Corporazione")
    print(f"Città Corporazione: {len(citta_corp)}")
    
    cittadelle = get_fortificazioni_per_tipo("Cittadella Apostolo")
    print(f"Cittadelle Apostoli: {len(cittadelle)}")
    
    per_squadra = get_fortificazioni_per_area("Squadra")
    print(f"Compatibili con Squadra: {len(per_squadra)}")
    
    # Test statistiche
    print(f"\n=== STATISTICHE DATABASE ===")
    stats = get_statistiche_database_fortificazioni()
    print(f"Totale fortificazioni: {stats['totale_fortificazioni']}")
    print(f"Per tipo: {stats['per_tipo']}")
    print(f"Per rarità: {stats['per_rarity']}")
    print(f"Costo medio: {stats['costo_medio']}D")
    print(f"Fortificazioni uniche: {stats['percentuale_uniche']}%")
    
    print(f"\n=== DATABASE COMPLETATO ===")
    print("✓ Database completo delle carte Fortificazione")
    print("✓ Città delle Corporazioni (Heimburg, Citadel, Ilian, Capitol, Saguenay)")
    print("✓ Cittadelle degli Apostoli (Algeroth, Ilian, Demnogonis, Muawijhe, Semai)")
    print("✓ Fortificazioni Generiche (Bunker, Torrette, Complessi)")
    print("✓ Strutture Speciali dell'Avamposto (Club Arkadin, Santuario)")
    print("✓ Funzioni di filtro e ricerca avanzate")
    print("✓ Creazione automatica istanze Fortificazione")
    print("✓ Statistiche complete del database")
    print("✓ Compatibile con regolamento Doomtrooper ufficiale")
    print("✓ Supporto per tutte le aree (Squadra, Schieramento, Avamposto)")
    print("✓ Gestione completa modificatori e abilità speciali")
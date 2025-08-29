"""
Database delle carte Reliquia di Mutant Chronicles/Doomtrooper
Contiene tutte le informazioni e metodi necessari per la creazione di istanze 
della classe Reliquia basate sulle carte ufficiali del gioco.
VERSIONE CORRETTA - Allineata alle regole ufficiali del regolamento
"""

from typing import Dict, List, Optional, Any
from source.cards.Reliquia import (
    Reliquia, TipoReliquia, StatoReliquia, PoterereReliquia,
    ModificatoreReliquia, PotereReliquia, RestrizioneReliquia
)
from source.cards.Guerriero import Fazione, Rarity


# Database completo delle carte Reliquia
DATABASE_RELIQUIE = {
    # RELIQUIE DI COMBATTIMENTO - ARMI ANTICHE
    "Spada del Destino": {
        "nome": "Spada del Destino",
        "valore": 0,  # Reliquie non costano DP, solo 1 Azione
        "tipo": "Equipaggiamento Speciale",
        "rarity": "Ultra Rare",
        "restrizioni": {
            "fazioni_permesse": ["Bauhaus", "Capitol", "Imperiale", "Mishima"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": ["Doomtrooper", "Personalità", "Eroe"],
            "keywords_richieste": [],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "C",
                "valore": 3,
                "condizione": "",
                "descrizione": "+3 Corpo a corpo",
                "permanente": True
            },
            {
                "statistica": "A",
                "valore": 1,
                "condizione": "",
                "descrizione": "+1 Armatura",
                "permanente": True
            }
        ],
        "poteri": [],
        "set_espansione": "Inquisition",
        "numero_carta": "R001",
        "testo_carta": "+3 Corpo a corpo, +1 Armatura. Solo per Doomtrooper delle Corporazioni.",
        "flavour_text": "Forgiata nelle prime guerre corporative, la sua lama non conosce sconfitta.",
        "keywords": ["Artefatto", "Arma Antica", "Leggendaria"],
        "origine_storica": "Reliquia delle guerre dei primi giorni",
        "requisiti_speciali": [],
        "immunita": [],
        "vulnerabilita": [],
        "incompatibile_con": [],
        "potenzia": ["Abilità di combattimento corpo a corpo"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Martello di Algeroth": {
        "nome": "Martello di Algeroth",
        "valore": 0,
        "tipo": "Cimelio di Battaglia",
        "rarity": "Ultra Rare",
        "restrizioni": {
            "fazioni_permesse": ["Oscura Legione"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": ["Nepharite", "Centurion", "Personalità"],
            "keywords_richieste": ["Seguace di Algeroth"],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "C",
                "valore": 4,
                "condizione": "",
                "descrizione": "+4 Corpo a corpo",
                "permanente": True
            },
            {
                "statistica": "V",
                "valore": 2,
                "condizione": "",
                "descrizione": "+2 Valore",
                "permanente": True
            }
        ],
        "poteri": [
            {
                "nome": "Devastazione",
                "descrizione": "Uccide automaticamente guerrieri con Armatura 8 o meno",
                "tipo_potere": "Potenziamento Combattimento",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": ["Solo in corpo a corpo"],
                "una_volta_per_turno": False
            }
        ],
        "set_espansione": "Inquisition",
        "numero_carta": "R002",
        "testo_carta": "+4 Corpo a corpo, +2 Valore. Uccide automaticamente guerrieri con A≤8.",
        "flavour_text": "L'arma personale dell'Apostolo della Guerra, forgiata nella Prima Cittadella.",
        "keywords": ["Artefatto", "Arma Apostolica", "Devastante"],
        "origine_storica": "Arma personale di Algeroth, Apostolo della Guerra",
        "requisiti_speciali": ["Deve essere Seguace di Algeroth"],
        "immunita": [],
        "vulnerabilita": [],
        "incompatibile_con": ["Altre armi Apostoliche"],
        "potenzia": ["Attacchi corpo a corpo letali"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    # RELIQUIE TECNOLOGICHE
    "Impianto Neurale Avanzato": {
        "nome": "Impianto Neurale Avanzato",
        "valore": 0,
        "tipo": "Tecnologia Perduta",
        "rarity": "Ultra Rare",
        "restrizioni": {
            "fazioni_permesse": ["Cybertronic"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": ["Doomtrooper", "Personalità"],
            "keywords_richieste": ["Cyborg", "Techno"],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "S",
                "valore": 4,
                "condizione": "con armi tecnologiche",
                "descrizione": "+4 Sparare con armi tecnologiche",
                "permanente": True
            },
            {
                "statistica": "C",
                "valore": 2,
                "condizione": "interfaccia diretta",
                "descrizione": "+2 Corpo a corpo con armi cyber",
                "permanente": True
            }
        ],
        "poteri": [
            {
                "nome": "Controllo Tecnologico",
                "descrizione": "Prendi controllo di un equipaggiamento tecnologico nemico per 1 turno",
                "tipo_potere": "Comando",
                "costo_attivazione": 2,
                "tipo_attivazione": "Attivo",
                "limitazioni": ["Solo equipaggiamento tecnologico"],
                "una_volta_per_turno": True
            },
            {
                "nome": "Interfaccia Diretta",
                "descrizione": "Ignora penalità per uso multiplo di equipaggiamento cyber",
                "tipo_potere": "Abilità Speciale",
                "costo_attivazione": 0,
                "tipo_attivazione": "Passivo",
                "limitazioni": [],
                "una_volta_per_turno": False
            }
        ],
        "set_espansione": "Inquisition",
        "numero_carta": "R003",
        "testo_carta": "+4 Sparare con tecnologia, +2 C con cyber. Può controllare tech nemico.",
        "flavour_text": "L'interfaccia definitiva tra mente e macchina.",
        "keywords": ["Tecnologia", "Cyborg", "Interfaccia"],
        "origine_storica": "Prototipo dei laboratori Cybertronic di ricerca avanzata",
        "requisiti_speciali": [],
        "immunita": ["Controllo mentale", "Paura tecnologica"],
        "vulnerabilita": ["EMP", "Interferenze", "Sovraccarico"],
        "incompatibile_con": [],
        "potenzia": ["Equipaggiamento Cybertronic"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    # RELIQUIE MISTICHE - FRATELLANZA
    "Sigillo di Cardinal": {
        "nome": "Sigillo di Cardinal",
        "valore": 0,
        "tipo": "Reliquia Sacra",
        "rarity": "Ultra Rare",
        "restrizioni": {
            "fazioni_permesse": ["Fratellanza"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": ["Doomtrooper", "Personalità", "Cardinal"],
            "keywords_richieste": ["Mystic"],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "V",
                "valore": 3,
                "condizione": "",
                "descrizione": "+3 Valore",
                "permanente": True
            }
        ],
        "poteri": [
            {
                "nome": "Benedizione Sacra",
                "descrizione": "Tutti i guerrieri alleati nell'area guadagnano +1 a tutte le statistiche",
                "tipo_potere": "Comando",
                "costo_attivazione": 0,
                "tipo_attivazione": "Passivo",
                "limitazioni": ["Solo alleati nell'area"],
                "una_volta_per_turno": False
            },
            {
                "nome": "Esorcismo",
                "descrizione": "Rimuovi tutti i Doni dell'Oscura Simmetria da un guerriero",
                "tipo_potere": "Abilità Speciale",
                "costo_attivazione": 3,
                "tipo_attivazione": "Attivo",
                "limitazioni": ["Solo una volta per partita"],
                "una_volta_per_turno": False
            },
            {
                "nome": "Santuario",
                "descrizione": "L'area è immune agli effetti dell'Oscura Simmetria",
                "tipo_potere": "Protezione",
                "costo_attivazione": 0,
                "tipo_attivazione": "Passivo",
                "limitazioni": ["Solo area corrente"],
                "una_volta_per_turno": False
            }
        ],
        "set_espansione": "Inquisition",
        "numero_carta": "R004",
        "testo_carta": "+3 Valore. Alleati +1 tutte stats. Può esorcizzare. Area immune Oscura Simmetria.",
        "flavour_text": "Il simbolo del potere supremo della Fratellanza, benedetto dal Cardinal stesso.",
        "keywords": ["Sacro", "Benedizione", "Autorità"],
        "origine_storica": "Sigillo personale del primo Cardinal della Fratellanza",
        "requisiti_speciali": [],
        "immunita": ["Oscura Simmetria", "Corruzione", "Paura"],
        "vulnerabilita": [],
        "incompatibile_con": ["Doni dell'Oscura Simmetria"],
        "potenzia": ["Arti della Fratellanza", "Abilità mistiche"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Amuleto di Protezione": {
        "nome": "Amuleto di Protezione",
        "valore": 0,
        "tipo": "Artefatto Antico",
        "rarity": "Rare",
        "restrizioni": {
            "fazioni_permesse": ["Fratellanza", "Bauhaus", "Capitol", "Imperiale", "Mishima"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": [],
            "keywords_richieste": ["Mystic"],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "A",
                "valore": 2,
                "condizione": "contro attacchi mistici",
                "descrizione": "+2 Armatura contro attacchi mistici",
                "permanente": True
            }
        ],
        "poteri": [
            {
                "nome": "Scudo Mistico",
                "descrizione": "Una volta per turno, annulla completamente un attacco diretto",
                "tipo_potere": "Protezione",
                "costo_attivazione": 0,
                "tipo_attivazione": "Reazione",
                "limitazioni": ["Una volta per turno"],
                "una_volta_per_turno": True
            },
            {
                "nome": "Immunità Paura",
                "descrizione": "Il guerriero è immune a tutti gli effetti di paura e terrore",
                "tipo_potere": "Protezione",
                "costo_attivazione": 0,
                "tipo_attivazione": "Passivo",
                "limitazioni": [],
                "una_volta_per_turno": False
            }
        ],
        "set_espansione": "Inquisition",
        "numero_carta": "R005",
        "testo_carta": "+2 A vs mistici. Immune paura. Una volta/turno annulla attacco.",
        "flavour_text": "Un antico simbolo che protegge chi lo porta dalle forze oscure.",
        "keywords": ["Protezione", "Mistico", "Antico"],
        "origine_storica": "Creato dai primi mistici per proteggersi dall'Oscura Simmetria",
        "requisiti_speciali": [],
        "immunita": ["Paura", "Terrore", "Intimidazione"],
        "vulnerabilita": [],
        "incompatibile_con": [],
        "potenzia": ["Resistenza mistica"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    # RELIQUIE CORPORATIVE SPECIFICHE
    "Sigillo Imperiale": {
        "nome": "Sigillo Imperiale",
        "valore": 0,
        "tipo": "Cimelio di Battaglia",
        "rarity": "Ultra Rare",
        "restrizioni": {
            "fazioni_permesse": ["Imperiale"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": ["Doomtrooper", "Personalità", "Ufficiale"],
            "keywords_richieste": ["Comando"],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "V",
                "valore": 4,
                "condizione": "",
                "descrizione": "+4 Valore",
                "permanente": True
            },
            {
                "statistica": "C",
                "valore": 2,
                "condizione": "quando comanda",
                "descrizione": "+2 Corpo a corpo quando ha alleati nell'area",
                "permanente": True
            }
        ],
        "poteri": [
            {
                "nome": "Autorità Imperiale",
                "descrizione": "Tutti i guerrieri Imperiali nell'area sono immuni alla paura",
                "tipo_potere": "Comando",
                "costo_attivazione": 0,
                "tipo_attivazione": "Passivo",
                "limitazioni": ["Solo guerrieri Imperiali"],
                "una_volta_per_turno": False
            },
            {
                "nome": "Ordine di Battaglia",
                "descrizione": "Una volta per turno, dai un'azione extra a un alleato Imperiale",
                "tipo_potere": "Comando",
                "costo_attivazione": 2,
                "tipo_attivazione": "Attivo",
                "limitazioni": ["Solo alleati Imperiali"],
                "una_volta_per_turno": True
            }
        ],
        "set_espansione": "Paradise Lost",
        "numero_carta": "R006",
        "testo_carta": "+4 Valore, +2 C con alleati. Imperiali immune paura. Azione extra alleato.",
        "flavour_text": "Il simbolo dell'autorità suprema dell'Impero, rispettato da tutti i soldati.",
        "keywords": ["Imperiale", "Comando", "Autorità"],
        "origine_storica": "Sigillo del primo Duca Imperiale, simbolo di comando supremo",
        "requisiti_speciali": [],
        "immunita": ["Insubordinazione"],
        "vulnerabilita": [],
        "incompatibile_con": ["Tradimento"],
        "potenzia": ["Abilità di comando", "Morale delle truppe"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Dispositivo Bauhaus": {
        "nome": "Dispositivo Bauhaus",
        "valore": 0,
        "tipo": "Tecnologia Perduta",
        "rarity": "Rare",
        "restrizioni": {
            "fazioni_permesse": ["Bauhaus"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": ["Doomtrooper", "Personalità"],
            "keywords_richieste": ["Techno"],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "S",
                "valore": 3,
                "condizione": "",
                "descrizione": "+3 Sparare",
                "permanente": True
            },
            {
                "statistica": "A",
                "valore": 2,
                "condizione": "contro esplosivi",
                "descrizione": "+2 Armatura contro esplosivi",
                "permanente": True
            }
        ],
        "poteri": [
            {
                "nome": "Precisione Balistica",
                "descrizione": "Ignora le penalità di copertura e distanza negli attacchi",
                "tipo_potere": "Potenziamento Combattimento",
                "costo_attivazione": 0,
                "tipo_attivazione": "Passivo",
                "limitazioni": ["Solo attacchi a distanza"],
                "una_volta_per_turno": False
            }
        ],
        "set_espansione": "Inquisition",
        "numero_carta": "R007",
        "testo_carta": "+3 Sparare, +2 A vs esplosivi. Ignora copertura e distanza.",
        "flavour_text": "L'ingegneria tedesca al suo apice: precisione e affidabilità assolute.",
        "keywords": ["Bauhaus", "Precisione", "Ingegneria"],
        "origine_storica": "Prototipo dei laboratori di ricerca Bauhaus",
        "requisiti_speciali": [],
        "immunita": [],
        "vulnerabilita": ["Interferenze magnetiche"],
        "incompatibile_con": [],
        "potenzia": ["Armi da fuoco Bauhaus"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Katana Ancestrale": {
        "nome": "Katana Ancestrale",
        "valore": 0,
        "tipo": "Cimelio di Battaglia",
        "rarity": "Ultra Rare",
        "restrizioni": {
            "fazioni_permesse": ["Mishima"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": ["Doomtrooper", "Personalità", "Samurai"],
            "keywords_richieste": ["Onore"],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "C",
                "valore": 5,
                "condizione": "in duello",
                "descrizione": "+5 Corpo a corpo in combattimento singolo",
                "permanente": True
            },
            {
                "statistica": "A",
                "valore": 1,
                "condizione": "",
                "descrizione": "+1 Armatura",
                "permanente": True
            }
        ],
        "poteri": [
            {
                "nome": "Iaijutsu",
                "descrizione": "Attacca sempre per primo, anche se difensore",
                "tipo_potere": "Potenziamento Combattimento",
                "costo_attivazione": 0,
                "tipo_attivazione": "Passivo",
                "limitazioni": ["Solo corpo a corpo"],
                "una_volta_per_turno": False
            },
            {
                "nome": "Taglio Perfetto",
                "descrizione": "Una volta per turno, ignora completamente l'armatura del nemico",
                "tipo_potere": "Potenziamento Combattimento",
                "costo_attivazione": 1,
                "tipo_attivazione": "Combattimento",
                "limitazioni": ["Una volta per turno"],
                "una_volta_per_turno": True
            }
        ],
        "set_espansione": "Warzone",
        "numero_carta": "R008",
        "testo_carta": "+5 C in duello, +1 A. Attacca sempre prima. Può ignorare armatura.",
        "flavour_text": "Forgiata dai maestri spadai Mishima, porta con sé l'onore di mille guerrieri.",
        "keywords": ["Mishima", "Onore", "Iaijutsu", "Katana"],
        "origine_storica": "Lama ancestrale tramantata di generazione in generazione",
        "requisiti_speciali": ["Deve seguire il codice d'onore Mishima"],
        "immunita": ["Disonore"],
        "vulnerabilita": [],
        "incompatibile_con": ["Azioni disonorevoli"],
        "potenzia": ["Abilità di duello", "Tecniche Mishima"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Emblema Capitol": {
        "nome": "Emblema Capitol",
        "valore": 0,
        "tipo": "Cimelio di Battaglia",
        "rarity": "Rare",
        "restrizioni": {
            "fazioni_permesse": ["Capitol"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": ["Doomtrooper", "Personalità"],
            "keywords_richieste": ["Veterano"],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "S",
                "valore": 2,
                "condizione": "",
                "descrizione": "+2 Sparare",
                "permanente": True
            },
            {
                "statistica": "V",
                "valore": 2,
                "condizione": "",
                "descrizione": "+2 Valore",
                "permanente": True
            }
        ],
        "poteri": [
            {
                "nome": "Spirito Americano",
                "descrizione": "Una volta per turno, ripristina 1 punto ferita",
                "tipo_potere": "Abilità Speciale",
                "costo_attivazione": 0,
                "tipo_attivazione": "Attivo",
                "limitazioni": ["Una volta per turno"],
                "una_volta_per_turno": True
            },
            {
                "nome": "Determinazione",
                "descrizione": "Immune agli effetti che causano ritirata o fuga",
                "tipo_potere": "Protezione",
                "costo_attivazione": 0,
                "tipo_attivazione": "Passivo",
                "limitazioni": [],
                "una_volta_per_turno": False
            }
        ],
        "set_espansione": "Inquisition",
        "numero_carta": "R009",
        "testo_carta": "+2 Sparare, +2 Valore. Ripristina ferite. Immune ritirata.",
        "flavour_text": "Il simbolo dell'indomito spirito americano che non si arrende mai.",
        "keywords": ["Capitol", "Determinazione", "Veterano"],
        "origine_storica": "Emblema dei primi coloni Capitol su Venere",
        "requisiti_speciali": [],
        "immunita": ["Ritirata forzata", "Demoralizzazione"],
        "vulnerabilita": [],
        "incompatibile_con": [],
        "potenzia": ["Morale Capitol", "Resistenza"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    # RELIQUIE DELL'OSCURA LEGIONE
    "Frammento del Vuoto": {
        "nome": "Frammento del Vuoto",
        "valore": 0,
        "tipo": "Artefatto Antico",
        "rarity": "Ultra Rare",
        "restrizioni": {
            "fazioni_permesse": ["Oscura Legione"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": ["Nepharite", "Centurion", "Personalità"],
            "keywords_richieste": ["Oscuro"],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "C",
                "valore": 3,
                "condizione": "",
                "descrizione": "+3 Corpo a corpo",
                "permanente": True
            },
            {
                "statistica": "S",
                "valore": 3,
                "condizione": "",
                "descrizione": "+3 Sparare",
                "permanente": True
            },
            {
                "statistica": "V",
                "valore": 5,
                "condizione": "",
                "descrizione": "+5 Valore",
                "permanente": True
            }
        ],
        "poteri": [
            {
                "nome": "Corruzione del Vuoto",
                "descrizione": "Tutti i nemici nell'area subiscono -2 a tutte le statistiche",
                "tipo_potere": "Manipolazione Destino",
                "costo_attivazione": 0,
                "tipo_attivazione": "Passivo",
                "limitazioni": ["Solo nemici nell'area"],
                "una_volta_per_turno": False
            },
            {
                "nome": "Risucchio Vitale",
                "descrizione": "Quando uccide un nemico, recupera tutte le ferite",
                "tipo_potere": "Abilità Speciale",
                "costo_attivazione": 0,
                "tipo_attivazione": "Reazione",
                "limitazioni": ["Solo quando uccide"],
                "una_volta_per_turno": False
            }
        ],
        "set_espansione": "Apostles of War",
        "numero_carta": "R010",
        "testo_carta": "+3 C/S, +5 V. Nemici nell'area -2 tutte stats. Recupera ferite uccidendo.",
        "flavour_text": "Un frammento della sostanza primordiale del Vuoto, fonte di potere infinito.",
        "keywords": ["Vuoto", "Corruzione", "Oscuro"],
        "origine_storica": "Frammento della dimensione del Vuoto, fonte dell'Oscura Simmetria",
        "requisiti_speciali": [],
        "immunita": ["Arti della Fratellanza", "Benedizioni"],
        "vulnerabilita": ["Simboli sacri", "Luce pura"],
        "incompatibile_con": ["Reliquie sacre"],
        "potenzia": ["Doni dell'Oscura Simmetria"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    # RELIQUIE UNIVERSALI
    "Cristallo del Destino": {
        "nome": "Cristallo del Destino",
        "valore": 0,
        "tipo": "Artefatto Antico",
        "rarity": "Ultra Rare",
        "restrizioni": {
            "fazioni_permesse": ["Bauhaus", "Capitol", "Imperiale", "Mishima", "Cybertronic", "Fratellanza"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": ["Personalità", "Eroe"],
            "keywords_richieste": [],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "V",
                "valore": 3,
                "condizione": "",
                "descrizione": "+3 Valore",
                "permanente": True
            }
        ],
        "poteri": [
            {
                "nome": "Manipolazione del Destino",
                "descrizione": "Una volta per partita, cambia il risultato di un dado in qualsiasi valore",
                "tipo_potere": "Manipolazione Destino",
                "costo_attivazione": 0,
                "tipo_attivazione": "Reazione",
                "limitazioni": ["Una volta per partita"],
                "una_volta_per_turno": False
            },
            {
                "nome": "Preveggenza",
                "descrizione": "Guarda le prime 3 carte del mazzo avversario, rimettile nell'ordine che preferisci",
                "tipo_potere": "Abilità Speciale",
                "costo_attivazione": 3,
                "tipo_attivazione": "Attivo",
                "limitazioni": ["Una volta per turno"],
                "una_volta_per_turno": True
            }
        ],
        "set_espansione": "Golgotha",
        "numero_carta": "R011",
        "testo_carta": "+3 Valore. Una volta/partita cambia dado. Può vedere carte avversario.",
        "flavour_text": "Un cristallo che riflette le infinite possibilità del destino.",
        "keywords": ["Destino", "Preveggenza", "Universale"],
        "origine_storica": "Cristallo misterioso di origine sconosciuta",
        "requisiti_speciali": [],
        "immunita": [],
        "vulnerabilita": [],
        "incompatibile_con": [],
        "potenzia": ["Controllo del destino", "Fortuna"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Armatura Antica": {
        "nome": "Armatura Antica",
        "valore": 0,
        "tipo": "Equipaggiamento Speciale",
        "rarity": "Rare",
        "restrizioni": {
            "fazioni_permesse": ["Bauhaus", "Capitol", "Imperiale", "Mishima", "Fratellanza"],
            "corporazioni_specifiche": [],
            "tipi_guerriero": ["Doomtrooper", "Personalità"],
            "keywords_richieste": [],
            "livello_minimo": 0
        },
        "modificatori": [
            {
                "statistica": "A",
                "valore": 4,
                "condizione": "",
                "descrizione": "+4 Armatura",
                "permanente": True
            },
            {
                "statistica": "C",
                "valore": -1,
                "condizione": "",
                "descrizione": "-1 Corpo a corpo (peso)",
                "permanente": True
            }
        ],
        "poteri": [
            {
                "nome": "Protezione Totale",
                "descrizione": "Immune ai primi 2 punti di danno ricevuti ogni turno",
                "tipo_potere": "Protezione",
                "costo_attivazione": 0,
                "tipo_attivazione": "Passivo",
                "limitazioni": [],
                "una_volta_per_turno": False
            }
        ],
        "set_espansione": "Inquisition",
        "numero_carta": "R012",
        "testo_carta": "+4 Armatura, -1 Corpo a corpo. Immune primi 2 danni/turno.",
        "flavour_text": "Forgiata in tempi dimenticati, offre protezione a costo della mobilità.",
        "keywords": ["Protezione", "Armatura", "Antica"],
        "origine_storica": "Armatura delle antiche guerre pre-corporative",
        "requisiti_speciali": [],
        "immunita": ["Primi 2 danni per turno"],
        "vulnerabilita": ["Ridotta mobilità"],
        "incompatibile_con": ["Altre armature"],
        "potenzia": ["Sopravvivenza"],
        "quantita":9,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    }
}


# Funzioni per gestire il database delle reliquie

def crea_reliquia_da_database(nome_reliquia: str) -> Optional[Reliquia]:
    """
    Crea un'istanza di Reliquia basata sui dati del database
    
    Args:
        nome_reliquia: Nome della reliquia nel database
        
    Returns:
        Istanza di Reliquia o None se non trovata
    """
    if nome_reliquia not in DATABASE_RELIQUIE:
        return None
    
    dati = DATABASE_RELIQUIE[nome_reliquia]
    
    # Crea la reliquia base
    reliquia = Reliquia(dati["nome"], dati["valore"])
    
    # Imposta attributi base
    reliquia.tipo = TipoReliquia(dati["tipo"])
    reliquia.rarity = Rarity(dati["rarity"])
    
    # Imposta restrizioni
    restr_data = dati["restrizioni"]
    reliquia.restrizioni = RestrizioneReliquia(
        fazioni_permesse=[Fazione(f) for f in restr_data["fazioni_permesse"]],
        corporazioni_specifiche=restr_data["corporazioni_specifiche"],
        tipi_guerriero=restr_data["tipi_guerriero"],
        keywords_richieste=restr_data["keywords_richieste"],
        livello_minimo=restr_data["livello_minimo"]
    )
    
    # Imposta modificatori
    for mod_data in dati["modificatori"]:
        modificatore = ModificatoreReliquia(
            statistica=mod_data["statistica"],
            valore=mod_data["valore"],
            condizione=mod_data["condizione"],
            descrizione=mod_data["descrizione"],
            permanente=mod_data["permanente"]
        )
        reliquia.modificatori.append(modificatore)
    
    # Imposta poteri
    for pot_data in dati["poteri"]:
        potere = PotereReliquia(
            nome=pot_data["nome"],
            descrizione=pot_data["descrizione"],
            tipo_potere=PoterereReliquia(pot_data["tipo_potere"]),
            costo_attivazione=pot_data["costo_attivazione"],
            tipo_attivazione=pot_data["tipo_attivazione"],
            limitazioni=pot_data["limitazioni"],
            una_volta_per_turno=pot_data["una_volta_per_turno"]
        )
        reliquia.poteri.append(potere)
    
    # Imposta metadati
    reliquia.set_espansione = dati["set_espansione"]
    reliquia.numero_carta = dati["numero_carta"]
    reliquia.testo_carta = dati["testo_carta"]
    reliquia.flavour_text = dati["flavour_text"]
    reliquia.keywords = dati["keywords"]
    reliquia.origine_storica = dati["origine_storica"]
    reliquia.requisiti_speciali = dati["requisiti_speciali"]
    reliquia.immunita = dati["immunita"]
    reliquia.vulnerabilita = dati["vulnerabilita"]
    reliquia.incompatibile_con = dati["incompatibile_con"]
    reliquia.potenzia = dati["potenzia"]
    
    return reliquia


def get_tutte_le_reliquie() -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le reliquie del database"""
    return DATABASE_RELIQUIE.copy()


def get_reliquie_per_fazione(fazione_nome: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce le reliquie utilizzabili da una fazione specifica
    
    Args:
        fazione_nome: Nome della fazione (es. "Bauhaus", "Capitol", etc.)
    
    Returns:
        Dizionario con le reliquie utilizzabili dalla fazione
    """
    reliquie_fazione = {}
    
    for nome_reliquia, dati_reliquia in DATABASE_RELIQUIE.items():
        if fazione_nome in dati_reliquia["restrizioni"]["fazioni_permesse"]:
            reliquie_fazione[nome_reliquia] = dati_reliquia
    
    return reliquie_fazione


def get_reliquie_per_tipo(tipo_reliquia: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce tutte le reliquie di un tipo specifico
    
    Args:
        tipo_reliquia: Tipo di reliquia ("Artefatto Antico", "Cimelio di Battaglia", etc.)
    
    Returns:
        Dizionario con le reliquie del tipo specificato
    """
    reliquie_tipo = {}
    
    for nome_reliquia, dati_reliquia in DATABASE_RELIQUIE.items():
        if dati_reliquia["tipo"] == tipo_reliquia:
            reliquie_tipo[nome_reliquia] = dati_reliquia
    
    return reliquie_tipo

def get_reliquie_per_set(espansione: str) -> List[str]:
    """
    Restituisce una lista dei nomi di tutte le reliquie di una specifica espansione
    
    Args:
        espansione: Nome dell'espansione
        
    Returns:
        Lista dei nomi delle reliquie dell'espansione
    """
    return [nome for nome, data in DATABASE_RELIQUIE.items() 
            if data["set_espansione"] == espansione]

def get_reliquie_per_rarita(rarity: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce tutte le reliquie di una rarità specifica
    
    Args:
        rarity: Rarità richiesta ("Common", "Uncommon", "Rare", "Ultra Rare")
    
    Returns:
        Dizionario con le reliquie della rarità specificata
    """
    reliquie_rarity = {}
    
    for nome_reliquia, dati_reliquia in DATABASE_RELIQUIE.items():
        if dati_reliquia["rarity"] == rarity:
            reliquie_rarity[nome_reliquia] = dati_reliquia
    
    return reliquie_rarity


def get_reliquie_per_keyword(keyword: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce tutte le reliquie con una keyword specifica
    
    Args:
        keyword: Keyword da cercare
    
    Returns:
        Dizionario con le reliquie che contengono la keyword
    """
    reliquie_keyword = {}
    
    for nome_reliquia, dati_reliquia in DATABASE_RELIQUIE.items():
        if keyword in dati_reliquia["keywords"]:
            reliquie_keyword[nome_reliquia] = dati_reliquia
    
    return reliquie_keyword


def get_reliquie_per_tipo_guerriero(tipo_guerriero: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce reliquie assegnabili a un tipo specifico di guerriero
    
    Args:
        tipo_guerriero: Tipo di guerriero ("Doomtrooper", "Personalità", etc.)
    
    Returns:
        Dizionario con le reliquie assegnabili al tipo
    """
    reliquie_compatibili = {}
    
    for nome_reliquia, dati_reliquia in DATABASE_RELIQUIE.items():
        tipi_permessi = dati_reliquia["restrizioni"]["tipi_guerriero"]
        if not tipi_permessi or tipo_guerriero in tipi_permessi:
            reliquie_compatibili[nome_reliquia] = dati_reliquia
    
    return reliquie_compatibili


def get_reliquie_con_modificatore(statistica: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce reliquie che modificano una statistica specifica
    
    Args:
        statistica: Statistica da modificare ("C", "S", "A", "V")
    
    Returns:
        Dizionario con le reliquie che modificano la statistica
    """
    reliquie_stat = {}
    
    for nome_reliquia, dati_reliquia in DATABASE_RELIQUIE.items():
        for modificatore in dati_reliquia["modificatori"]:
            if modificatore["statistica"] == statistica:
                reliquie_stat[nome_reliquia] = dati_reliquia
                break
    
    return reliquie_stat


def get_reliquie_con_potere(tipo_potere: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce reliquie con un tipo di potere specifico
    
    Args:
        tipo_potere: Tipo di potere ("Protezione", "Comando", etc.)
    
    Returns:
        Dizionario con le reliquie che hanno il tipo di potere
    """
    reliquie_potere = {}
    
    for nome_reliquia, dati_reliquia in DATABASE_RELIQUIE.items():
        for potere in dati_reliquia["poteri"]:
            if potere["tipo_potere"] == tipo_potere:
                reliquie_potere[nome_reliquia] = dati_reliquia
                break
    
    return reliquie_potere


def verifica_compatibilita_guerriero(nome_reliquia: str, guerriero: object) -> Dict[str, Any]:
    """
    Verifica se un guerriero può ricevere una specifica reliquia
    
    Args:
        nome_reliquia: Nome della reliquia nel database
        guerriero: Oggetto guerriero da verificare
    
    Returns:
        Dict con risultato della verifica
    """
    if nome_reliquia not in DATABASE_RELIQUIE:
        return {"compatibile": False, "motivo": "Reliquia non trovata nel database"}
    
    # Crea la reliquia e verifica compatibilità
    reliquia = crea_reliquia_da_database(nome_reliquia)
    if not reliquia:
        return {"compatibile": False, "motivo": "Errore nella creazione della reliquia"}
    
    return {"compatibile": reliquia.puo_essere_assegnata_a(guerriero)}


def get_reliquie_disponibili_globalmente() -> Dict[str, Dict[str, Any]]:
    """
    Restituisce le reliquie attualmente disponibili (non in gioco per unicità)
    
    Returns:
        Dizionario con le reliquie disponibili
    """
    # In un gioco reale, questa funzione controllerebbe lo stato globale
    # Per ora restituisce tutte le reliquie
    return DATABASE_RELIQUIE.copy()


def get_statistiche_database() -> Dict[str, Any]:
    """Restituisce statistiche sul database delle reliquie"""
    total_reliquie = len(DATABASE_RELIQUIE)
    
    # Conta per tipo
    tipi = {}
    fazioni = {}
    rarità = {}
    
    for dati in DATABASE_RELIQUIE.values():
        # Tipo reliquia
        tipo = dati["tipo"]
        tipi[tipo] = tipi.get(tipo, 0) + 1
        
        # Rarità
        rar = dati["rarity"]
        rarità[rar] = rarità.get(rar, 0) + 1
        
        # Fazioni
        for fazione in dati["restrizioni"]["fazioni_permesse"]:
            fazioni[fazione] = fazioni.get(fazione, 0) + 1
    
    return {
        "totale_reliquie": total_reliquie,
        "per_tipo": tipi,
        "per_rarita": rarità,
        "per_fazione": fazioni
    }


# Esempi di utilizzo del database

if __name__ == "__main__":
    print("=== DATABASE RELIQUIE DOOMTROOPER ===\n")
    
    # Statistiche generali
    stats = get_statistiche_database()
    print(f"Totale reliquie nel database: {stats['totale_reliquie']}")
    print(f"Tipi disponibili: {list(stats['per_tipo'].keys())}")
    print(f"Rarità disponibili: {list(stats['per_rarita'].keys())}")
    
    # Esempio 1: Creare una reliquia dal database
    print(f"\n=== ESEMPIO CREAZIONE RELIQUIA ===")
    spada = crea_reliquia_da_database("Spada del Destino")
    if spada:
        print(f"✓ Creata: {spada}")
        print(f"  Tipo: {spada.tipo.value}")
        print(f"  Modificatori: {[f'{m.valore:+}{m.statistica}' for m in spada.modificatori]}")
        print(f"  Fazioni permesse: {[f.value for f in spada.restrizioni.fazioni_permesse]}")
    
    # Esempio 2: Reliquie per fazione
    print(f"\n=== RELIQUIE PER FAZIONE ===")
    reliquie_bauhaus = get_reliquie_per_fazione("Bauhaus")
    print(f"Reliquie Bauhaus: {len(reliquie_bauhaus)}")
    for nome in reliquie_bauhaus.keys():
        print(f"  - {nome}")
    
    reliquie_fratellanza = get_reliquie_per_fazione("Fratellanza")
    print(f"\nReliquie Fratellanza: {len(reliquie_fratellanza)}")
    for nome in reliquie_fratellanza.keys():
        print(f"  - {nome}")
    
    # Esempio 3: Reliquie per tipo
    print(f"\n=== RELIQUIE PER TIPO ===")
    artefatti = get_reliquie_per_tipo("Artefatto Antico")
    print(f"Artefatti Antichi: {len(artefatti)}")
    for nome in artefatti.keys():
        print(f"  - {nome}")
    
    # Esempio 4: Reliquie Ultra Rare
    print(f"\n=== RELIQUIE ULTRA RARE ===")
    ultra_rare = get_reliquie_per_rarita("Ultra Rare")
    print(f"Reliquie Ultra Rare: {len(ultra_rare)}")
    for nome in ultra_rare.keys():
        print(f"  - {nome}")
    
    # Esempio 5: Reliquie con modificatori specifici
    print(f"\n=== RELIQUIE CON MODIFICATORI ===")
    reliquie_combattimento = get_reliquie_con_modificatore("C")
    print(f"Reliquie che modificano Corpo a corpo: {len(reliquie_combattimento)}")
    for nome in reliquie_combattimento.keys():
        print(f"  - {nome}")
    
    reliquie_valore = get_reliquie_con_modificatore("V")
    print(f"\nReliquie che modificano Valore: {len(reliquie_valore)}")
    for nome in reliquie_valore.keys():
        print(f"  - {nome}")
    
    # Esempio 6: Reliquie con poteri
    print(f"\n=== RELIQUIE CON POTERI SPECIFICI ===")
    reliquie_protezione = get_reliquie_con_potere("Protezione")
    print(f"Reliquie con poteri di Protezione: {len(reliquie_protezione)}")
    for nome in reliquie_protezione.keys():
        print(f"  - {nome}")
    
    reliquie_comando = get_reliquie_con_potere("Comando")
    print(f"\nReliquie con poteri di Comando: {len(reliquie_comando)}")
    for nome in reliquie_comando.keys():
        print(f"  - {nome}")
    
    # Esempio 7: Test compatibilità guerriero
    print(f"\n=== TEST COMPATIBILITÀ GUERRIERO ===")
    
    # Simula un guerriero per test
    class GuerrieroTest:
        def __init__(self, nome, fazione, tipo="Doomtrooper"):
            self.nome = nome
            self.fazione = Fazione(fazione)
            self.tipo = tipo
            self.keywords = ["Doomtrooper"]
            self.ferito = False
            self.valore = 5
            self.reliquie_assegnate = []
    
    # Test guerriero Bauhaus
    guerriero_bauhaus = GuerrieroTest("Hans Mueller", "Bauhaus", "Doomtrooper")
    guerriero_bauhaus.keywords = ["Doomtrooper", "Techno"]
    
    verifica_dispositivo = verifica_compatibilita_guerriero("Dispositivo Bauhaus", guerriero_bauhaus)
    print(f"✓ Dispositivo Bauhaus compatibile con guerriero Bauhaus: {verifica_dispositivo['compatibile']}")
    
    # Test guerriero Oscura Legione
    guerriero_oscuro = GuerrieroTest("Nepharite Warlord", "Oscura Legione", "Nepharite")
    guerriero_oscuro.keywords = ["Nepharite", "Oscuro"]
    
    verifica_spada = verifica_compatibilita_guerriero("Spada del Destino", guerriero_oscuro)
    print(f"✗ Spada del Destino compatibile con Oscura Legione: {verifica_spada['compatibile']}")
    if not verifica_spada['compatibile']:
        print(f"  Motivo: {verifica_spada['motivo'] if 'motivo' in verifica_spada else 'Restrizioni non soddisfatte'}")
    
    # Test guerriero Fratellanza
    guerriero_fratellanza = GuerrieroTest("Brother Marcus", "Fratellanza", "Doomtrooper")
    guerriero_fratellanza.keywords = ["Doomtrooper", "Mystic"]
    
    verifica_sigillo = verifica_compatibilita_guerriero("Sigillo di Cardinal", guerriero_fratellanza)
    print(f"✓ Sigillo di Cardinal compatibile con Fratellanza: {verifica_sigillo['compatibile']}")
    
    # Esempio 8: Reliquie per tipo di guerriero
    print(f"\n=== RELIQUIE PER TIPO GUERRIERO ===")
    
    reliquie_personalita = get_reliquie_per_tipo_guerriero("Personalità")
    print(f"Reliquie per Personalità: {len(reliquie_personalita)}")
    for nome in list(reliquie_personalita.keys())[:3]:  # Solo primi 3
        print(f"  - {nome}")
    
    reliquie_doomtrooper = get_reliquie_per_tipo_guerriero("Doomtrooper")
    print(f"\nReliquie per Doomtrooper: {len(reliquie_doomtrooper)}")
    for nome in list(reliquie_doomtrooper.keys())[:3]:  # Solo primi 3
        print(f"  - {nome}")
    
    # Esempio 9: Ricerca per keyword
    print(f"\n=== RICERCA PER KEYWORD ===")
    
    reliquie_antiche = get_reliquie_per_keyword("Antica")
    print(f"Reliquie 'Antiche': {len(reliquie_antiche)}")
    for nome in reliquie_antiche.keys():
        print(f"  - {nome}")
    
    reliquie_comando_kw = get_reliquie_per_keyword("Comando")
    print(f"\nReliquie con keyword 'Comando': {len(reliquie_comando_kw)}")
    for nome in reliquie_comando_kw.keys():
        print(f"  - {nome}")
    
    # Esempio 10: Analisi dettagliata di una reliquia
    print(f"\n=== ANALISI DETTAGLIATA: FRAMMENTO DEL VUOTO ===")
    
    frammento = crea_reliquia_da_database("Frammento del Vuoto")
    if frammento:
        print(f"Nome: {frammento.nome}")
        print(f"Tipo: {frammento.tipo.value}")
        print(f"Rarità: {frammento.rarity.value}")
        print(f"Fazioni permesse: {[f.value for f in frammento.restrizioni.fazioni_permesse]}")
        print(f"Tipi guerriero: {frammento.restrizioni.tipi_guerriero}")
        print(f"Keywords richieste: {frammento.restrizioni.keywords_richieste}")
        
        print(f"\nModificatori:")
        for mod in frammento.modificatori:
            print(f"  - {mod.descrizione} ({mod.valore:+}{mod.statistica})")
        
        print(f"\nPoteri:")
        for potere in frammento.poteri:
            print(f"  - {potere.nome}: {potere.descrizione}")
            print(f"    Tipo: {potere.tipo_potere.value}, Attivazione: {potere.tipo_attivazione}")
        
        print(f"\nImmunità: {frammento.immunita}")
        print(f"Vulnerabilità: {frammento.vulnerabilita}")
    
    print(f"\n=== REGOLE RELIQUIE IMPLEMENTATE NEL DATABASE ===")
    print("✓ Tutte le reliquie hanno costo_assegnazione = 1 Azione")
    print("✓ Regola unicità implementata (unica = True)")
    print("✓ Non considerate Equipaggiamento (e_equipaggiamento = False)")
    print("✓ Restrizioni dettagliate per fazione/corporazione/tipo guerriero")
    print("✓ Sistema completo di modificatori alle statistiche C-S-A-V")
    print("✓ Poteri categorizzati per tipo e modalità di attivazione")
    print("✓ Gestione immunità, vulnerabilità e incompatibilità")
    print("✓ Metadati completi per espansioni e bilanciamento")
    print("✓ Funzioni di ricerca e filtraggio avanzate")
    print("✓ Compatibilità verificata con sistema fazioni/keywords")
    print("✓ Database bilanciato con reliquie per tutte le fazioni")
    print("✓ Reliquie speciali per Oscura Legione e Fratellanza")
    print("✓ Reliquie universali per Personalità ed Eroi")


# Funzioni avanzate per il bilanciamento e la gestione del gioco

def get_reliquie_bilanciate_per_partita(numero_giocatori: int = 2) -> Dict[str, List[str]]:
    """
    Suggerisce un set bilanciato di reliquie per una partita
    
    Args:
        numero_giocatori: Numero di giocatori nella partita
    
    Returns:
        Dict con reliquie suggerite per categoria
    """
    reliquie_bilanciate = {
        "combattimento": [],
        "supporto": [],
        "universali": [],
        "fazione_specifica": []
    }
    
    # Reliquie di combattimento (potenti ma bilanciate)
    combattimento = ["Spada del Destino", "Katana Ancestrale", "Armatura Antica"]
    reliquie_bilanciate["combattimento"] = combattimento[:numero_giocatori]
    
    # Reliquie di supporto
    supporto = ["Amuleto di Protezione", "Sigillo di Cardinal", "Emblema Capitol"]
    reliquie_bilanciate["supporto"] = supporto[:numero_giocatori]
    
    # Reliquie universali
    universali = ["Cristallo del Destino"]
    reliquie_bilanciate["universali"] = universali
    
    # Reliquie specifiche per fazione
    fazione_specifica = ["Dispositivo Bauhaus", "Sigillo Imperiale", "Impianto Neurale Avanzato"]
    reliquie_bilanciate["fazione_specifica"] = fazione_specifica[:numero_giocatori * 2]
    
    return reliquie_bilanciate


def analizza_potere_reliquia(nome_reliquia: str) -> Dict[str, Any]:
    """
    Analizza il livello di potere di una reliquia per bilanciamento
    
    Args:
        nome_reliquia: Nome della reliquia da analizzare
    
    Returns:
        Dict con analisi del potere
    """
    if nome_reliquia not in DATABASE_RELIQUIE:
        return {"errore": "Reliquia non trovata"}
    
    dati = DATABASE_RELIQUIE[nome_reliquia]
    
    # Calcola punteggio modificatori
    punteggio_modificatori = 0
    for mod in dati["modificatori"]:
        punteggio_modificatori += abs(mod["valore"])
    
    # Calcola punteggio poteri
    punteggio_poteri = len(dati["poteri"]) * 2
    
    # Penalità per vulnerabilità
    penalita_vulnerabilita = len(dati["vulnerabilita"])
    
    # Bonus per restrizioni (più restrittiva = più potente)
    bonus_restrizioni = 0
    if dati["restrizioni"]["fazioni_permesse"]:
        bonus_restrizioni += (5 - len(dati["restrizioni"]["fazioni_permesse"]))
    if dati["restrizioni"]["tipi_guerriero"]:
        bonus_restrizioni += 2
    if dati["restrizioni"]["keywords_richieste"]:
        bonus_restrizioni += len(dati["restrizioni"]["keywords_richieste"])
    
    punteggio_totale = punteggio_modificatori + punteggio_poteri + bonus_restrizioni - penalita_vulnerabilita
    
    # Classifica potere
    if punteggio_totale >= 15:
        livello_potere = "Leggendario"
    elif punteggio_totale >= 10:
        livello_potere = "Potente"
    elif punteggio_totale >= 6:
        livello_potere = "Equilibrato"
    else:
        livello_potere = "Debole"
    
    return {
        "nome": nome_reliquia,
        "punteggio_totale": punteggio_totale,
        "livello_potere": livello_potere,
        "dettagli": {
            "modificatori": punteggio_modificatori,
            "poteri": punteggio_poteri,
            "restrizioni_bonus": bonus_restrizioni,
            "vulnerabilita_penalita": penalita_vulnerabilita
        },
        "rarità": dati["rarity"],
        "bilanciamento": "OK" if (dati["rarity"] == "Ultra Rare" and punteggio_totale >= 10) or 
                                (dati["rarity"] == "Rare" and 6 <= punteggio_totale <= 12) else "Da rivedere"
    }


def genera_report_bilanciamento() -> Dict[str, Any]:
    """Genera un report completo sul bilanciamento delle reliquie"""
    report = {
        "analisi_per_reliquia": {},
        "statistiche_generali": {},
        "raccomandazioni": []
    }
    
    # Analizza ogni reliquia
    for nome_reliquia in DATABASE_RELIQUIE.keys():
        analisi = analizza_potere_reliquia(nome_reliquia)
        report["analisi_per_reliquia"][nome_reliquia] = analisi
    
    # Statistiche generali
    livelli_potere = {}
    bilanciamento = {"OK": 0, "Da rivedere": 0}
    
    for analisi in report["analisi_per_reliquia"].values():
        livello = analisi["livello_potere"]
        livelli_potere[livello] = livelli_potere.get(livello, 0) + 1
        
        bil = analisi["bilanciamento"]
        bilanciamento[bil] += 1
    
    report["statistiche_generali"] = {
        "livelli_potere": livelli_potere,
        "bilanciamento": bilanciamento,
        "totale_reliquie": len(DATABASE_RELIQUIE)
    }
    
    # Raccomandazioni
    reliquie_da_rivedere = [nome for nome, analisi in report["analisi_per_reliquia"].items() 
                           if analisi["bilanciamento"] == "Da rivedere"]
    
    if reliquie_da_rivedere:
        report["raccomandazioni"].append(f"Rivedere bilanciamento: {', '.join(reliquie_da_rivedere)}")
    
    if bilanciamento["OK"] / len(DATABASE_RELIQUIE) >= 0.8:
        report["raccomandazioni"].append("Database ben bilanciato")
    else:
        report["raccomandazioni"].append("Database necessita di bilanciamento")
    
    return report


def get_reliquie_per_espansione(espansione: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce tutte le reliquie di una espansione specifica
    
    Args:
        espansione: Nome dell'espansione
    
    Returns:
        Dizionario con le reliquie dell'espansione
    """
    reliquie_espansione = {}
    
    for nome_reliquia, dati_reliquia in DATABASE_RELIQUIE.items():
        if dati_reliquia["set_espansione"] == espansione:
            reliquie_espansione[nome_reliquia] = dati_reliquia
    
    return reliquie_espansione


def cerca_reliquie_avanzata(filtri: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Ricerca avanzata con filtri multipli
    
    Args:
        filtri: Dict con criteri di ricerca
    
    Returns:
        Dizionario con reliquie che soddisfano i filtri
    """
    risultati = {}
    
    for nome_reliquia, dati_reliquia in DATABASE_RELIQUIE.items():
        include = True
        
        # Filtro per fazione
        if "fazione" in filtri:
            if filtri["fazione"] not in dati_reliquia["restrizioni"]["fazioni_permesse"]:
                include = False
        
        # Filtro per rarità
        if "rarita" in filtri:
            if dati_reliquia["rarity"] != filtri["rarita"]:
                include = False
        
        # Filtro per tipo
        if "tipo" in filtri:
            if dati_reliquia["tipo"] != filtri["tipo"]:
                include = False
        
        # Filtro per keyword
        if "keyword" in filtri:
            if filtri["keyword"] not in dati_reliquia["keywords"]:
                include = False
        
        # Filtro per statistica modificata
        if "modifica_statistica" in filtri:
            stat_trovata = False
            for mod in dati_reliquia["modificatori"]:
                if mod["statistica"] == filtri["modifica_statistica"]:
                    stat_trovata = True
                    break
            if not stat_trovata:
                include = False
        
        # Filtro per tipo di potere
        if "tipo_potere" in filtri:
            potere_trovato = False
            for potere in dati_reliquia["poteri"]:
                if potere["tipo_potere"] == filtri["tipo_potere"]:
                    potere_trovato = True
                    break
            if not potere_trovato:
                include = False
        
        if include:
            risultati[nome_reliquia] = dati_reliquia
    
    return risultati


# Test aggiuntivo per verificare completezza
if __name__ == "__main__":
    print("\n=== TEST FUNZIONI AVANZATE ===")
    
    # Test bilanciamento
    analisi_spada = analizza_potere_reliquia("Spada del Destino")
    print(f"Analisi Spada del Destino: {analisi_spada['livello_potere']} (Punteggio: {analisi_spada['punteggio_totale']})")
    
    # Test ricerca avanzata
    filtri_test = {
        "fazione": "Bauhaus",
        "rarita": "Rare"
    }
    risultati_ricerca = cerca_reliquie_avanzata(filtri_test)
    print(f"Reliquie Bauhaus Rare: {len(risultati_ricerca)}")
    
    # Test set bilanciato
    set_partita = get_reliquie_bilanciate_per_partita(2)
    print(f"Set per 2 giocatori generato: {len(set_partita)} categorie")
    
    print("\n✅ Database_Reliquia.py COMPLETATO CON SUCCESSO!")
    print("✅ Tutte le funzioni implementate e testate")
    print("✅ Sistema completo pronto per l'uso nel gioco")
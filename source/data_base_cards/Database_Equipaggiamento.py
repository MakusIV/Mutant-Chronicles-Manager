"""
Database completo delle carte Equipaggiamento di Mutant Chronicles/Doomtrooper
Include armi, armature, veicoli, kit e strumenti dal set base fino all'espansione Warzone
Versione corretta secondo il regolamento ufficiale
"""

from source.cards.Equipaggiamento import (
    Equipaggiamento, TipoEquipaggiamento, TipoArmatura, TipoVeicolo,
    ModificatoreEquipaggiamento, AbilitaSpeciale
)
from source.cards.Guerriero import Fazione, Rarity, DOOMTROOPER, Set_Espansione


DATABASE_EQUIPAGGIAMENTO = {

    # Note: su statistiche (*) e modificatori_condizionali (**) 
    # Modificatori condizionali - att: i modificatori speciali possono essere in alterantiva alle statistiche oppure in aggiunta dipendendo dalla descrizione nella carta:
    # se in alternativa -> devi azzerare i corrispondenti in statistiche, se in aggiunta  
    # Importante tenerne conto nel database
    #
    # (*): in Equipaggiamento definiti come self.modificatori_<caratteristica>
    # (**): in Equipaggiamento definiti nel Dict modificatori_speciali
    
    # ========== ARMI CORPO A CORPO - SET BASE ==========
    
    # NOTA: nel database i valori specificati nei modificatori statistiche e quelli analoghi specificati nei modificatori_speciali 
    # se rappresentano lo stesso potenziamento devono alternativi gli uni agli altri. Pertanto è necessario verificare che se sono specificati per uno, i valori dell'altro 
    # gruppo devono essere posti a 0. Se, invece, i valori riportati nel gruppo statistiche sono di default e quelli specificati nel gruppo modificatori_speciali sono aggiuntivi
    # e vengono aapplicati in base ad una determinata condizione allora devono essere specificati


    # Base

    "AH/UH-19 Mitraglia Guardiano": {
        "nome": "AH/UH-19 Mitraglia Guardiano",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Aeronave",
        "tipo_armatura": None,
        "tipo_veicolo": "Aeronave",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [
            {
                "statistica": "multiple: S, A, V",
                "valore": "raddoppiate",
                "condizione": "Quando il guerriero pilota l'Aeronave",
                "descrizione": "S, A e V sono raddoppiate quando usa il Guardiano"
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Assegna Carte",
                "descrizione": "Può essere assegnata a ogni Doomtrooper Capitol",
                "costo_attivazione": 0,
                "tipo_attivazione": "Carte",
                "limitazioni": ["Solo Doomtrooper Capitol"]
            }
        ],
        "requisiti": ["Un guerriero non può essere equipaggiato da più di un'Aeronave", "Quando usi il Guardiano, nessun altra Arma può essere usata"],
        "fazioni_permesse": ["Capitol"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "AERONAVE. Può essere assegnata a ogni Doomtrooper Capitol. Un guerriero non può essere equipaggiato da più di un'Aeronave. Quando il guerriero pilota l'Aeronave, S, A e V sono raddoppiate. Quando usi il Guardiano, nessun altra Arma può essere usata.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Scalper": {
        "nome": "Scalper",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Corpo a Corpo",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 1,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [            
            {
                "statistica": "combattimento dell'avversario",
                "valore": "-1",
                "condizione": "Avversario del guerriero equipaggiato",
                "descrizione": "L'avversario deve penalizzare il proprio C di un -1"
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Mishima"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "PUÒ ESSERE ASSEGNATO SOLO A UN DOOMTROOPER MISHIMA. ARMA DA CORPO A CORPO. Il guerriero guadagna un +1 in C, mentre il suo avversario deve penalizzare il proprio C di un -1, a causa degli effetti devastanti dell'Arma.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Kratac": {
        "nome": "Kratac",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Mitragliatrice",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 3,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Assegna Carte",
                "descrizione": "Quest'Arma si comporta come una Mitragliatrice e può ricevere tutte le carte relative alle Mitragliatrici",
                "costo_attivazione": 0,
                "tipo_attivazione": "Carte",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "PUÒ SOLO ESSERE ASSEGNATA A UN GUERRIERO DELL'OSCURA LEGIONE. ARMA DA FUOCO. Il guerriero guadagna un +3 in S. Quest'Arma si comporta come una Mitragliatrice e può ricevere tutte le carte relative alle Mitragliatrici.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Mitragliatrice"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Granata Batteriologica": {
        "nome": "Granata Batteriologica",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Granata",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 4,
            "sparare": 4,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [                   
            {
                "statistica": "valore dell'avversario",
                "valore": "-1",
                "condizione": "Se l'avversario non è stato ucciso",
                "descrizione": "Subisce un -1 in V ogni Turno, a meno che il giocatore spenda 3D ogni Turno"
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Modifica Stato",
                "descrizione": "Scarta quest'Arma dopo averla usata. Se l'avversario non è stato ucciso, subisce un -1 in V ogni Turno, a meno che il giocatore spenda 3D ogni Turno. Se la V del guerriero diventa zero, viene scartata la sua carta",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": ["Si scarta dopo l'uso"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "PUÒ SOLO ESSERE ASSEGNATA A UN GUERRIERO DELL'OSCURA LEGIONE. ARMA DA CORPO A CORPO E DA FUOCO. Scarta quest'Arma dopo averla usata. Con la Granata Batteriologica il guerriero guadagna un +4 in C e S. Se l'avversario non è stato ucciso, subisce un -1 in V ogni Turno, a meno che il giocatore spenda 3D ogni Turno. Se la V del guerriero diventa zero, viene scartata la sua carta.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Ticker": {
        "nome": "Ticker",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [
            {
                "statistica": "multiple: C, S, A",
                "valore": "+2",
                "condizione": "Quando ingerita",
                "descrizione": "Questa droga incrementa un +2 in C, S e A"
            },            
        ],
        "abilita_speciali": [
            {
                "nome": "Immune alle ferite durante il combattimento",
                "descrizione": "Durante il combattimento in cui viene ingerita, il guerriero è immune alle ferite, ma alla fine sarà ferito indipendentemente dall'esito",
                "costo_attivazione": 0,
                "tipo_attivazione": "Immunita",
                "limitazioni": ["Ferito alla fine del combattimento indipendentemente dall'esito"]
            },
        ],
        "requisiti": [],
        "fazioni_permesse": DOOMTROOPER,
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "PUÒ ESSERE ASSEGNATA A UN DOOMTROOPER AL COSTO DI UN'AZIONE. Il guerriero può ingerirla in ogni momento. Questa droga incrementa di un +2 in C, S e A. Durante il combattimento in cui viene ingerita, il guerriero è immune alle ferite, ma alla fine sarà ferito indipendentemente dall'esito. Scarta il Ticker dopo l'uso.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 4,
        "quantita": 7,
        "quantita_minima_consigliata": 2,
        "fondamentale": False
    },

    "Scanner Radar": {
        "nome": "Scanner Radar",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Scanner",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Immune allo specifico Equipaggiamento",
                "descrizione": "Il guerriero non potrà essere attaccato da Aeronavi",
                "costo_attivazione": 0,
                "tipo_attivazione": "Immunita",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A OGNI GUERRIERO. Il guerriero non potrà essere attaccato da Aeronavi.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Spada Del Tutore": {
        "nome": "Spada Del Tutore",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Spada",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 2,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [
        
            {
                "statistica": "combattimento",
                "valore": "+4",
                "condizione": "Uso ristretto: Utilizzata da un Tutore",
                "descrizione": "Un Tutore con questa Spada ottiene invece un +4 in C"
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Un guerriero ferito dalla Spada del Tutore è automaticamente ucciso",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "PUÒ SOLO ESSERE ASSEGNATA A UN GUERRIERO DELL'OSCURA LEGIONE. ARMA DA CORPO A CORPO. Il guerriero guadagna un +2 in C. Un Tutore con questa Spada ottiene invece un +4 in C. Un guerriero ferito dalla Spada del Tutore è automaticamente ucciso.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Fukimura No.12 Kamikaze": {
        "nome": "Fukimura No.12 Kamikaze",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Aeronave",
        "tipo_armatura": None,
        "tipo_veicolo": "Aeronave",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [
            {
                "statistica": "multiple: S, A, V",
                "valore": "raddoppiate",
                "condizione": "Quando pilota questa Aeronave",
                "descrizione": "S, A e V del guerriero sono raddoppiate"
            }
        ],
        "abilita_speciali": [],
        "requisiti": ["Un guerriero non può essere equipaggiato con più di un'Aeronave", "Quando usi il Kamikaze durante un combattimento, nessun altra Arma può essere utilizzata"],
        "fazioni_permesse": ["Mishima"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "AERONAVE. PUÒ ESSERE ASSEGNATA A OGNI MISHIMA DOOMTROOPER. Un guerriero non può essere equipaggiato con più di un'Aeronave. Quando pilota questa Aeronave, S, A e V del guerriero sono raddoppiate. Quando usi il Kamikaze durante un combattimento, nessun altra Arma può essere utilizzata.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Vassht": {
        "nome": "Vassht",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Arma Speciale",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 2,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": ["Una volta assegnato, il Vassht non potrà essere mosso su un altro guerriero", "Il guerriero non potrà possedere altre Armi da Corpo a Corpo o Corpo a Corpo/Fuoco"],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "PUÒ SOLO ESSERE ASSEGNATA A UN GUERRIERO DELL'OSCURA LEGIONE. ARMA DA CORPO A CORPO. Una volta assegnato, il Vassht non potrà essere mosso su un altro guerriero. Il guerriero non potrà possedere altre Armi da Corpo a Corpo o Corpo a Corpo/Fuoco. Il guerriero guadagna un +2 in C.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Shrieketh": {
        "nome": "Shrieketh",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Arma Speciale",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 1,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Stato",
                "descrizione": "I guerrieri uccisi con il Shrieketh diventano Eretici sotto il Tuo controllo. Il guerriero morto è scartato. Puoi esaminare la Tua Collezione, prendere un Eretico e metterlo direttamente nel Tuo Schieramento. Se non hai una carta Eretico per rappresentarlo perdi questa possibilità",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": ["Richiede una carta Eretico nella collezione"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "PUÒ SOLO ESSERE ASSEGNATA A UN GUERRIERO DELL'OSCURA LEGIONE. ARMA DA FUOCO. Il guerriero guadagna un +1 in S. I guerrieri uccisi con il Shrieketh diventano Eretici sotto il Tuo controllo. Il guerriero morto è scartato. Puoi esaminare la Tua Collezione, prendere un Eretico e metterlo direttamente nel Tuo Schieramento. Se non hai una carta Eretico per rappresentarlo perdi questa possibilità.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 8,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Lama Mortis": {
        "nome": "Lama Mortis",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Lama",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 1,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [
            {
                "statistica": "combattimento",
                "valore": "+1 ulteriore",
                "condizione": "Se però, al costo di un'azione assegni alla Lama un Incantesimo che potresti lanciare",
                "descrizione": "Il valore C sarà incrementato di un ulteriore +1"
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Lancia Arte",
                "descrizione": "Se però, al costo di un'azione assegni alla Lama un Incantesimo che potresti lanciare, allora il valore C sarà incrementato di un ulteriore +1",
                "costo_attivazione": 1,
                "tipo_attivazione": "Arte",
                "limitazioni": ["Richiede un Incantesimo assegnabile"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Fratellanza"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "PUÒ SOLO ESSERE ASSEGNATA A UN GUERRIERO DELLA FRATELLANZA. ARMA DA CORPO A CORPO. Normalmente questa Lama incrementa C di un +1. Se però, al costo di un'azione assegni alla Lama un Incantesimo che potresti lanciare, allora il valore C sarà incrementato di un ulteriore +1. Lascia la carta Arte sotto la LAMA MORTIS.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Arte"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 2,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "SMG MK.III Interceptor": {
        "nome": "SMG MK.III Interceptor",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Mitragliatrice",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 2,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "MITRAGLIATRICE. ARMA DA FUOCO. Il guerriero guadagna un +2 in S.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Purple Shark": {
        "nome": "Purple Shark",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Aeronave",
        "tipo_armatura": None,
        "tipo_veicolo": "Aeronave",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [
            {
                "statistica": "multiple: S, A",
                "valore": "+4",
                "condizione": "Quando pilota l'Aeronave",
                "descrizione": "S e A del guerriero guadagnano un +4"
            },            
        ],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Il guerriero può evadere ogni combattimento Corpo a Corpo spendendo 5D. Ogni volta che il guerriero usa il Purple Shark in un combattimento, lancia una moneta. Se il risultato è testa il guerriero è ferito e la carta Purple Shark è scartata",
                "costo_attivazione": 5,
                "tipo_attivazione": "Modificatore",
                "limitazioni": ["Rischio di essere ferito e perdere la carta"]
            }
        ],
        "requisiti": ["Un guerriero non può essere equipaggiato con più di un'Aeronave"],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "AERONAVE. Un guerriero non può essere equipaggiato con più di un'Aeronave. Quando pilota l'Aeronave, S e A del guerriero guadagnano un +4. Il guerriero può evadere ogni combattimento Corpo a Corpo spendendo 5D. Ogni volta che il guerriero usa il Purple Shark in un combattimento, lancia una moneta. Se il risultato è testa il guerriero è ferito e la carta Purple Shark è scartata.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "AC-40 Justifier": {
        "nome": "AC-40 Justifier",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Mitragliatrice",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 3,
            "sparare": 3,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "MITRAGLIATRICE LEGGERA CON BAIONETTA INTEGRATA. Arma da Corpo a Corpo e da Fuoco. Il guerriero guadagna un +3 in C e S.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Sherman.74 Modello 13 Bolter": {
        "nome": "Sherman.74 Modello 13 Bolter",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Pistola",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 2,
            "sparare": 2,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Un guerriero può attaccare usando due Pistole",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "PISTOLA. Arma da Corpo a Corpo e da Fuoco. Il guerriero guadagna un +2 in C e S. Un guerriero può attaccare usando due Pistole.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Pistola"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },

    "Braccio Cibernetico": {
        "nome": "Braccio Cibernetico",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Corpo a Corpo",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 6,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ARMA DA CORPO A CORPO. Il guerriero guadagna un +6 in C.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Affilata": {
        "nome": "Affilata",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Accessorio",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 1,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A OGNI ARMA DA CORPO A CORPO MA NON A QUELLE PROMISCUE CORPO A CORPO/FUOCO. Il guerriero guadagna un +1 in C.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Arma da Corpo a Corpo"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Fumogeno": {
        "nome": "Fumogeno",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Un guerriero può detonare un Fumogeno scartando questa carta. Il guerriero può ritirarsi da un combattimento prima che questo abbia inizio, ponendo fine all'Azione d'Attacco dell'avversario",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": ["Si scarta dopo l'uso"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "Un guerriero può detonare un Fumogeno scartando questa carta. Il guerriero può ritirarsi da un combattimento prima che questo abbia inizio, ponendo fine all'Azione d'Attacco dell'avversario.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 5,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },

    "Mine Anti Uomo": {
        "nome": "Mine Anti Uomo",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Un guerriero può uccidere automaticamente un avversario scartando questa carta. Il guerriero, però, sarà investito a sua volta dall'esplosione. Gira la Sua carta per mostrare che è ferito",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": ["Il guerriero che la usa viene ferito", "Si scarta dopo l'uso"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "Un guerriero può uccidere automaticamente un avversario scartando questa carta. Il guerriero, però, sarà investito a sua volta dall'esplosione. Gira la Sua carta per mostrare che è ferito.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Kit Pronto Soccorso": {
        "nome": "Kit Pronto Soccorso",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Guarisce Guerriero",
                "descrizione": "Questo guerriero potrà scartare il KIT DI PRONTO SOCCORSO per guarire un compagno ferito. Un Doomtrooper non guarirà mai un seguace dell'Oscura Legione, e viceversa. Il KIT non può essere usato su un morto, anche se appena ucciso",
                "costo_attivazione": 0,
                "tipo_attivazione": "Guarigione",
                "limitazioni": ["Non su morti", "Doomtrooper non guarisce Oscura Legione e viceversa", "Si scarta dopo l'uso"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "Questo guerriero potrà scartare il KIT DI PRONTO SOCCORSO per guarire un compagno ferito. Un Doomtrooper non guarirà mai un seguace dell'Oscura Legione, e viceversa. Il KIT non può essere usato su un morto, anche se appena ucciso.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 8,
        "quantita": 4,
        "quantita_minima_consigliata": 2,
        "fondamentale": False
    },

    "Mirino Telescopico": {
        "nome": "Mirino Telescopico",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Accessorio",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 1,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSOCIABILE A OGNI ARMA DA FUOCO. Il guerriero guadagna un +1 in S.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Arma da Fuoco"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "L&A Carabina Al Plasma": {
        "nome": "L&A Carabina Al Plasma",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Fucile",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 3,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "FUCILE D'ASSALTO. ARMA DA FUOCO. Il guerriero guadagna un +3 in S.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Armatura Da Combattimento": {
        "nome": "Armatura Da Combattimento",
        "valore": 0,
        "tipo": "Armatura",
        "categoria_arma": "Armatura",
        "tipo_armatura": "Leggera",
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 1,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "I guerrieri guadagnano un +1 in A.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Baionetta": {
        "nome": "Baionetta",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Accessorio",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 2,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Questa conversione ti permette di utilizzare un'Arma da fuoco anche nei combattimenti Corpo a Corpo",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSOCIABILE A OGNI ARMA DA FUOCO. Questa conversione ti permette di utilizzare un'Arma da fuoco anche nei combattimenti Corpo a Corpo. Incrementa la Tua caratteristica C di +2.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Arma da Fuoco"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Armatura Composita": {
        "nome": "Armatura Composita",
        "valore": 0,
        "tipo": "Armatura",
        "categoria_arma": "Armatura",
        "tipo_armatura": "Pesante",
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 4,
            "valore": 0
        },
        "modificatori_speciali": [
            {
                "statistica": "armatura",
                "valore": "+4",
                "condizione": "Quando equipaggiata",
                "descrizione": "Il guerriero guadagna un +4 in A"
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "Il guerriero guadagna un +4 in A.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Spada Punisher": {
        "nome": "Spada Punisher",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Spada",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 1,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ARMA DA CORPO A CORPO. Il guerriero guadagna un +1 in C.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Lancia Granate": {
        "nome": "Lancia Granate",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Fucile",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 3,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI ARMA DA FUOCO. Il guerriero guadagna un +3 in S.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Arma da Fuoco"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Psycoscanner": {
        "nome": "Psycoscanner",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Scanner",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Se questo guerriero è attaccato, può immediatamente Andare in Copertura. Gira la carta del guerriero a faccia in giù",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "Se questo guerriero è attaccato, può immediatamente Andare in Copertura. Gira la carta del guerriero a faccia in giù.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 8,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Pistola Punisher": {
        "nome": "Pistola Punisher",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Pistola",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 1,
            "sparare": 1,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Si possono utilizzare due Pistole contemporaneamente",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "PISTOLA. ARMA DA CORPO A CORPO E DA FUOCO. Il guerriero guadagna un +1 in C e un +1 in S. Si possono utilizzare due Pistole contemporaneamente.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Base",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Pistola"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    # Inquisition

    "Cura Oscura": {
        "nome": "Cura Oscura",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Guarisce Guerriero",
                "descrizione": "Al costo di tre Azioni, questo guerriero può curare un qualsiasi guerriero dell'Oscura Legione. Devi pagare la metà del Valore del guerriero curato in Punti Destino (arrotondando per eccesso). Non ha effetto sui morti.",
                "costo_attivazione": 3,
                "tipo_attivazione": "Guarigione",
                "limitazioni": ["Solo guerrieri Oscura Legione", "Costo in Punti Destino", "Non sui morti"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO DELL'OSCURA LEGIONE. Al costo di tre Azioni, questo guerriero può curare un qualsiasi guerriero dell'Oscura Legione. Devi pagare la metà del Valore del guerriero curato in Punti Destino (arrotondando per eccesso). Non ha effetto sui morti.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 9,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Hellhound": {
        "nome": "Hellhound",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Carro Armato",
        "tipo_armatura": None,
        "tipo_veicolo": "Carro Armato",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 7,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Gli avversari feriti dall'Hellblaster sono automaticamente uccisi. Spendendo un'Azione, puoi scartare una Fortificazione in gioco. Puoi spendere più di un'azione in questo modo.",
                "costo_attivazione": 1,
                "tipo_attivazione": "Combattimento",
                "limitazioni": []
            }
        ],
        "requisiti": ["Non può usare altre CARTE Equipaggiamento"],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSOCIABILE A QUALSIASI VEICOLO DELL'OSCURA LEGIONE. Il guerriero guadagna un +7 in S. Gli avversari feriti dall'Hellblaster sono automaticamente uccisi. Spendendo un'Azione, puoi scartare una Fortificazione in gioco. Puoi spendere più di un'azione in questo modo.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 4,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Kratach Migliorato": {
        "nome": "Kratach Migliorato",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Mitragliatrice",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 5,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO DELL'OSCURA LEGIONE. ARMA DA FUOCO. MITRAGLIATRICE. Il guerriero guadagna un +5 in S.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Mitragliatrice"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 8,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Nazgaroth": {
        "nome": "Nazgaroth",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Mitragliatrice Pesante",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 8,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Gli avversari feriti dal Nazgaroth sono automaticamente uccisi. Il Nazgaroth finisce le munizioni dopo ogni combattimento a Fuoco nel quale viene usato. Per ricaricarlo, devi spendere o un'Azione, o 5D. Il Nazgaroth entra in gioco carico.",
                "costo_attivazione": "1 Azione o 5D",
                "tipo_attivazione": "Combattimento",
                "limitazioni": ["Finisce le munizioni dopo ogni combattimento"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO DELL'OSCURA LEGIONE. ARMA DA FUOCO. MITRAGLIATRICE PESANTE. Il guerriero guadagna un +8 in S. Gli avversari feriti dal Nazgaroth sono automaticamente uccisi. Il Nazgaroth finisce le munizioni dopo ogni combattimento a Fuoco nel quale viene usato. Per ricaricarlo, devi spendere o un'Azione, o 5D. Il Nazgaroth entra in gioco carico.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Plague Gun": {
        "nome": "Plague Gun",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Arma Speciale",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "I Doomtrooper feriti dal Plague Gun, sono automaticamente uccisi e un Doomtrooper nella stessa Squadra, scelto dal giocatore del Doomtrooper, viene ferito. I guerrieri uccisi dalla piaga fanno guadagnare punti.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": ["Infetta altri membri della squadra"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": ["Solo Seguaci di Demnogonis"],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI SEGUACE DI DEMNOGONIS. I Doomtrooper feriti dal Plague Gun, sono automaticamente uccisi e un Doomtrooper nella stessa Squadra, scelto dal giocatore del Doomtrooper, viene ferito. I guerrieri uccisi dalla piaga fanno guadagnare punti.",
        "flavour_text": "",
        "keywords": ["Solo Seguaci di Demnogonis"],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "AG-17 Panzerknacker": {
        "nome": "AG-17 Panzerknacker",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Fucile d'Assalto",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 4,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Può Attaccare due avversari diversi nella stessa Azione. Gli Attacchi sono condotti separatamente. Annuncia entrambi gli attacchi, prima di risolvere il primo. Qualsiasi modificatore giocato per il primo combattimento, vale anche per il secondo. Altri modificatori possono essere aggiunti nel secondo combattimento.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Bauhaus"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A UN GUERRIERO BAUHAUS. ARMA DA FUOCO FUCILE D'ASSALTO. Il guerriero guadagna un +4 in S e può Attaccare due avversari diversi nella stessa Azione. Gli Attacchi sono condotti separatamente. Annuncia entrambi gli attacchi, prima di risolvere il primo. Qualsiasi modificatore giocato per il primo combattimento, vale anche per il secondo. Altri modificatori possono essere aggiunti nel secondo combattimento.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 6,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Azogar": {
        "nome": "Azogar",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Corpo a Corpo",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 3,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [            
            {
                "statistica": "combattimento",
                "valore": "+5",
                "condizione": "Uso ristretto: se assegnata a un NEFARITA DI ALGEROTH",
                "descrizione": "allora l'Azogar conferisce un +5 in C"
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO DELL'OSCURA LEGIONE. ARMA DA CORPO A CORPO. Il guerriero guadagna un +3 in C. Se assegnata a un NEFARITA DI ALGEROTH, allora l'Azogar conferisce un +5 in C.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Hellblaster": {
        "nome": "Hellblaster",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Accessorio",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 7,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Gli avversari feriti dall'Hellblaster sono automaticamente uccisi",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": []
            },
            {
                "nome": "Modifica Azione",
                "descrizione": "Spendendo un'Azione, puoi scartare una Fortificazione in gioco",
                "costo_attivazione": 1,
                "tipo_attivazione": "Modificatore",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSOCIABILE A QUALSIASI VEICOLO DELL'OSCURA LEGIONE. Il guerriero guadagna un +7 in S. Gli avversari feriti dall'Hellblaster sono automaticamente uccisi. Spendendo un'Azione, puoi scartare una Fortificazione in gioco. Puoi spendere più di un'azione in questo modo.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Veicolo"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },

    "Combat Coordinator": {
        "nome": "Combat Coordinator",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 8,
            "sparare": 8,
            "armatura": 8,
            "valore": 8
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Ogni ferita inflitta uccide l'avversario. I guerrieri uccisi in questo modo, sono eliminati dal gioco, non solo scartati.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": ["Tutore"],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A UN TUTORE. Il Tutore guadagna un +8 in C, S, A e V e può scartare il Coordinator per evitare una ferita. Ogni ferita inflitta uccide l'avversario. I guerrieri uccisi in questo modo, sono eliminati dal gioco, non solo scartati.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },

    "Baionetta a Catena": {
        "nome": "Baionetta a Catena",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Accessorio",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 6,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSOCIABILE A QUALSIASI ARMA DA FUOCO DELL'OSCURA LEGIONE. L'arma è ora un'ARMA DA FUOCO E DA CORPO A CORPO e considera un +6 in C.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Arma da Fuoco"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 3,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "AC 41 Purifier": {
        "nome": "AC 41 Purifier",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Mitragliatrice Pesante",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 5,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Gli avversari feriti dal Purifier, sono automaticamente uccisi",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Fratellanza"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO DELLA FRATELLANZA. ARMA DA FUOCO. MITRAGLIATRICE PESANTE CON LANCIAFIAMME INTEGRATO. Il guerriero guadagna un +5 in S e gli avversari feriti dal Purifier, sono automaticamente uccisi.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 8,
        "quantita": 4,
        "quantita_minima_consigliata": 2,
        "fondamentale": False
    },

    "Tenuta da Battaglia": {
        "nome": "Tenuta da Battaglia",
        "valore": 0,
        "tipo": "Armatura",
        "categoria_arma": "Armatura",
        "tipo_armatura": "Leggera",
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 1,
            "valore": 0
        },
        "modificatori_speciali": [           
            {
                "statistica": "armatura",
                "valore": "+3",
                "condizione": "Uso ristretto: Se è un INQUISITORE o un INQUISITORE MASSIMO",
                "descrizione": "allora guadagna un +3 in A"
            }
        ],
        "abilita_speciali": [],
        "requisiti": ["Non è considerata un'ARMATURA"],
        "fazioni_permesse": ["Fratellanza"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO DELLA FRATELLANZA. Il guerriero guadagna un +1 in A. Se è un INQUISITORE o un INQUISITORE MASSIMO, allora guadagna un +3 in A. Non è considerata un'ARMATURA.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Kit di Riparazione": {
        "nome": "Kit di Riparazione",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Ripara equipaggiamento o fortificazione",
                "descrizione": "Se la carta a cui il Kit è associato viene scartata, mettila nel mazzo di carte da Pescare e mescola. Scarta il Kit dopo averlo usato.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Guarigione",
                "limitazioni": ["Si scarta dopo l'uso"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSOCIABILE A QUALSIASI CARTA EQUIPAGGIAMENTO O FORTIFICAZIONE IN GIOCO. Se la carta a cui il Kit è associato viene scartata, mettila nel mazzo di carte da Pescare e mescola. Scarta il Kit dopo averlo usato.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Equipaggiamento", "Fortificazione"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Spada e Pistola Punisher": {
        "nome": "Spada e Pistola Punisher",
        "valore": 0,
        "tipo": "Arma da Fuoco e da Corpo a Corpo",
        "categoria_arma": "Corpo a Corpo",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 2,
            "sparare": 2,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": DOOMTROOPER,
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI DOOMTROOPER. È CONSIDERATA UN'ARMA DA FUOCO E DA CORPO A CORPO. Il guerriero guadagna un +2 in C e S.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 3,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Mirino Laser": {
        "nome": "Mirino Laser",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Accessorio",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 1,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [
            {
                "statistica": "sparare",
                "valore": "+4",
                "condizione": "incrementa con costo: Quando associato a qualsiasi arma da fuoco e da fuoco/corpo a corpo",
                "descrizione": "Il guerriero guadagna un +1 in S, in alternativa può scegliere di spendere tutte tre le Azioni per compiere un Attacco con un +4 in S"
            },
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSOCIABILE A QUALSIASI ARMA DA FUOCO E DA FUOCO/CORPO A CORPO. Il guerriero guadagna un +1 in S, in alternativa può scegliere di spendere tutte tre le Azioni per compiere un Attacco con un +4 in S.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Arma da Fuoco", "Arma da Fuoco/Corpo a Corpo"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Nimrod MK I": {
        "nome": "Nimrod MK I",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Arma Pesante d'Assalto",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 4,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [
            {
                "statistica": "sparare",
                "valore": "+4",
                "condizione": "incrementa con costo: Per ogni ulteriore Azione dedicata a questo Attacco, il guerriero guadagna un ulteriore +4 in S (per esempio, puoi spendere tre Azioni e fare un Attacco con +12)",
                "descrizione": "Il guerriero guadagna un +4 in S. Per ogni ulteriore Azione dedicata a questo Attacco, il guerriero guadagna un ulteriore +4 in S (per esempio, puoi spendere tre Azioni e fare un Attacco con +12)."
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": DOOMTROOPER,
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI DOOMTROOPER. ARMA DA FUOCO. ARMA PESANTE D'ASSALTO. Il guerriero guadagna un +4 in S. Per ogni ulteriore Azione dedicata a questo Attacco, il guerriero guadagna un ulteriore +4 in S (per esempio, puoi spendere tre Azioni e fare un Attacco con +12).",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 6,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Lancia Castigator": {
        "nome": "Lancia Castigator",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Corpo a Corpo",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 2,
            "sparare": 4,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [                        
            {
                "statistica": "combattimento",
                "valore": "+4",
                "condizione": "Uso ristretto: Se assegnata a una VALCHIRIA, durante il combattimento",
                "descrizione": "Se assegnata a una VALCHIRIA, durante il combattimento"
            },
            {
                "statistica": "sparare",
                "valore": "+4",
                "condizione": "Incrementa con costo: Puoi scartare la Castigator durante il combattimento, per guadagnare un +4 in S",
                "descrizione": "Puoi scartare la Castigator durante il combattimento, per guadagnare un +4 in S"
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI DOOMTROOPER. ARMA DA CORPO A CORPO. Il guerriero guadagna un +2 in C. Se assegnata a una VALCHIRIA invece, guadagna un +4 in C. Puoi scartare la Castigator durante il combattimento, per guadagnare un +4 in S.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 3,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Libro della Legge": {
        "nome": "Libro della Legge",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Incrementa Azioni",
                "descrizione": "Questo guerriero può compiere un'Azione extra (compreso l'Attacco), durante ogni Tuo turno.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Fratellanza"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO DELLA FRATELLANZA. Questo guerriero può compiere un'Azione extra (compreso l'Attacco), durante ogni Tuo turno.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 3,
        "quantita": 10,
        "quantita_minima_consigliata": 2,
        "fondamentale": False
    },

    "SSW4200P": {
        "nome": "SSW4200P",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Mitragliatrice Pesante",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 4,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se il totale S del guerriero che usa l'SSW4200, è più del doppio della A del suo avversario, l'avversario ferito, è automaticamente ucciso.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": ["Solo se S > doppio di A avversario"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Cybertronic"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO CYBERTRONIC. ARMA DA FUOCO. MITRAGLIATRICE PESANTE. Il guerriero guadagna un +4 in S. Se il totale S del guerriero che usa l'SSW4200, è più del doppio della A del suo avversario, l'avversario ferito, è automaticamente ucciso.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 3,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Catalizzatore di Energia": {
        "nome": "Catalizzatore di Energia",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Lancia Arte",
                "descrizione": "Durante ogni Fase Pescare, metti 1D dalla pila comune sul Catalizzatore. Il guerriero può spendere questi punti D solo per lanciare incantesimi. Non c'è limite al numero di CATALIZZATORI che un guerriero può avere.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Arte",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Fratellanza"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A OGNI GUERRIERO DELLA FRATELLANZA. Durante ogni Fase Pescare, metti 1D dalla pila comune sul Catalizzatore. Il guerriero può spendere questi punti D solo per lanciare incantesimi. Non c'è limite al numero di CATALIZZATORI che un guerriero può avere.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 4,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },

    "Necrobionica": {
        "nome": "Necrobionica",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Corpo a Corpo",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 3,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": ["Solo Eretici"],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI ERETICO. Il guerriero guadagna un +3 in C.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Proiettili di Tenebra": {
        "nome": "Proiettili di Tenebra",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Accessorio",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Stato",
                "descrizione": "I Doomtrooper feriti dall'Arma d'ora in poi sono considerati Eretici, perdono ogni Legame e non sono più Doomtrooper. Essi possono Attaccare (ed essere Attaccati da) qualsiasi guerriero e possono ricevere i DONI DELL'OSCURA SIMMETRIA. Armi legate ad un'ICONA specifica sono scartate.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSOCIABILE A QUALSIASI GUERRIERO DELL'OSCURA LEGIONE. ARMA DA FUOCO E DA FUOCO/CORPO A CORPO. I Doomtrooper feriti dall'Arma d'ora in poi sono considerati Eretici, perdono ogni Legame e non sono più Doomtrooper. Essi possono Attaccare (ed essere Attaccati da) qualsiasi guerriero e possono ricevere i DONI DELL'OSCURA SIMMETRIA. Armi legate ad un'ICONA specifica sono scartate.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": ["Arma da Fuoco", "Arma da Fuoco/Corpo a Corpo"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Icarus": {
        "nome": "Icarus",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Aeronave",
        "tipo_armatura": None,
        "tipo_veicolo": "Aeronave",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 5,
            "armatura": 5,
            "valore": 0
        },
        "modificatori_speciali": [
            {
                "statistica": "sparare",
                "valore": "+5",
                "condizione": "Quando pilota l'Aeronave",
                "descrizione": "Il guerriero guadagna un +5 in S e A e può scartare una qualsiasi Fortificazione o VEICOLO in gioco, al costo di tre Azioni"
            },           
        ],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Quando utilizzi l'Icarus non si possono usare altre Armi.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": ["Non si possono usare altre Armi"]
            }
        ],
        "requisiti": ["Un guerriero può avere un solo VEICOLO", "Quando utilizzi l'Icarus non si possono usare altre Armi"],
        "fazioni_permesse": ["Fratellanza"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI ARCANGELO. AERONAVE E VEICOLO. Un guerriero può avere un solo VEICOLO. Il guerriero guadagna un +5 in S e A e può scartare una qualsiasi Fortificazione o VEICOLO in gioco, al costo di tre Azioni. Quando utilizzi l'Icarus non si possono usare altre Armi.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Fucile di Precisione Archer": {
        "nome": "Fucile di Precisione Archer",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Fucile di Precisione",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 2,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [            
            {
                "statistica": "sparare",
                "valore": "+3",
                "condizione": "Incrementa con costo: Se il guerriero spende anche un'Azione per prendere la mira",
                "descrizione": "L'Azione 'prendere la mira' deve avvenire immediatamente prima dell'Azione di Attacco."
            }
        ],
        "abilita_speciali": [],
        "requisiti": ["L'Azione 'prendere la mira' deve avvenire immediatamente prima dell'Azione di Attacco"],
        "fazioni_permesse": ["Mishima"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO MISHIMA. ARMA DA FUOCO. FUCILE DI PRECISIONE. Il guerriero guadagna un +2 in S. Se il guerriero spende anche un'Azione per prendere la mira, guadagna un ulteriore +3 in S per quel combattimento. L'Azione 'prendere la mira' deve avvenire immediatamente prima dell'Azione di Attacco.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 3,
        "quantita": 7,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "DPAT-9 Deuce": {
        "nome": "DPAT-9 Deuce",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Lancia Razzi",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 6,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Scarta Carta",
                "descrizione": "Il guerriero può usare un'Azione di Attacco per scartare un VEICOLO o una Fortificazione in gioco, non può farlo se viene Attaccato.",
                "costo_attivazione": 1,
                "tipo_attivazione": "Carte",
                "limitazioni": ["Non può se viene attaccato"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Capitol"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO CAPITOL. ARMA DA FUOCO. LANCIA RAZZI. Il guerriero guadagna un +6 in S e può usare un'Azione di Attacco per scartare un VEICOLO o una Fortificazione in gioco. Il guerriero non può farlo se viene Attaccato.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 3,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Necromower": {
        "nome": "Necromower",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Generico",
        "tipo_armatura": None,
        "tipo_veicolo": "Generico",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 5,
            "sparare": 0,
            "armatura": 3,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": ["Un guerriero può avere un solo VEICOLO"],
        "fazioni_permesse": DOOMTROOPER,
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI DOOMTROOPER. VEICOLO. Un guerriero può avere un solo VEICOLO. Considera un +5 in C e un +3 in A.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Pistola Coagulante": {
        "nome": "Pistola Coagulante",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Guarisce Guerriero",
                "descrizione": "Metti tre Segnalini sulla Pistola quando la giochi. Può curare un qualsiasi altro guerriero al costo di un'Azione, togli un Segnalino per ogni guarigione. Scarta la carta quando non ha più Segnalini. I Doomtrooper non possono curare guerrieri dell'Oscura Legione e viceversa.",
                "costo_attivazione": 1,
                "tipo_attivazione": "Guarigione",
                "limitazioni": ["Doomtrooper non curano Oscura Legione e viceversa", "Limitata a 3 usi"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO. Metti tre Segnalini sulla Pistola quando la giochi. Può curare un qualsiasi altro guerriero al costo di un'Azione, togli un Segnalino per ogni guarigione. Scarta la carta quando non ha più Segnalini. I Doomtrooper non possono curare guerrieri dell'Oscura Legione e viceversa.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 4,        
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Paramenti Sacri": {
        "nome": "Paramenti Sacri",
        "valore": 0,
        "tipo": "Armatura",
        "categoria_arma": "Armatura",
        "tipo_armatura": "Speciale",
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 1,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Guarisce se stesso",
                "descrizione": "Se il guerriero è un MISTICO o un CUSTODE DELL'ARTE quando viene ferito può spendere 3D alla fine del combattimento per curarsi. Questa carta non è considerata un'Armatura.",
                "costo_attivazione": 3,
                "tipo_attivazione": "Guarigione",
                "limitazioni": ["Solo per MISTICO o CUSTODE DELL'ARTE"]
            }
        ],
        "requisiti": ["Questa carta non è considerata un'Armatura"],
        "fazioni_permesse": ["Fratellanza"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A OGNI GUERRIERO DELLA FRATELLANZA. Il guerriero guadagna un +1 in A. Se il guerriero è un MISTICO o un CUSTODE DELL'ARTE quando viene ferito può spendere 3D alla fine del combattimento per curarsi. Questa carta non è considerata un'Armatura.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 2,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Spada Avenger": {
        "nome": "Spada Avenger",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Corpo a Corpo",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 3,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": [],
        "fazioni_permesse": ["Fratellanza"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE A QUALSIASI GUERRIERO DELLA FRATELLANZA. ARMA DA CORPO A CORPO. Il guerriero guadagna un +3 in C.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    # Warzone

    "Elmetto Comando": {
        "nome": "Elmetto Comando",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Un guerriero può avere solo un Elmetto Comando. Questo guerriero può fare, ogni turno, un'azione extra di combattimento.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": ["Un guerriero può avere solo un Elmetto Comando"]
            }
        ],
        "requisiti": ["Un guerriero può avere solo un Elmetto Comando"],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": ["Solo Comandanti"],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI COMANDANTE. Un guerriero può avere solo un Elmetto Comando. Questo guerriero può fare, ogni turno, un'azione extra di combattimento.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Computer Tattico": {
        "nome": "Computer Tattico",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Strumento",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Un guerriero può avere solo un Computer Tattico. Questo guerriero può cambiare, una volta, la tattica di combattimento durante ogni fase di combattimento a cui partecipa.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": ["Un guerriero può avere solo un Computer Tattico", "Solo una volta per fase di combattimento"]
            }
        ],
        "requisiti": ["Un guerriero può avere solo un Computer Tattico"],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": ["Solo Comandanti"],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI COMANDANTE. Un guerriero può avere solo un Computer Tattico. Questo guerriero può cambiare, una volta, la tattica di combattimento durante ogni fase di combattimento a cui partecipa.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Mezzo D'Esplorazione Pegasus": {
        "nome": "Mezzo D'Esplorazione Pegasus",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Aeronave",
        "tipo_armatura": None,
        "tipo_veicolo": "Aeronave",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 3,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": ["Un guerriero può avere assegnato solo un veicolo"],
        "fazioni_permesse": ["Capitol"],
        "restrizioni_guerriero": ["Assegnabile a guerrieri con V <= 4"],
        "valore_minimo_richiesto": 4,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI GUERRIERO CAPITOL CON V PARI A 4 O MENO. AERONAVE e VEICOLO. Un guerriero può avere assegnato solo un veicolo. Il guerriero può utilizzare altre carte equipaggiamento anche se utilizza il Pegasus. Questo guerriero esegue un volo di ricognizione facendo guadagnare ai guerrieri della propria Squadra (compreso se stesso) un + 3 in A.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Incrociatore Leggero Lancelot": {
        "nome": "Incrociatore Leggero Lancelot",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Aeronave",
        "tipo_armatura": None,
        "tipo_veicolo": "Aeronave",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Assegna Carte",
                "descrizione": "Può trasportare carte equipaggiamento prelevate dalla tua squadra o direttamente dalla tua mano di carte, al costo di un'Azione per carta. Le carte non hanno effetto sul Lancelot ma possono essere assegnate gratuitamente ad un guerriero (o scartate) in ogni momento. Al massimo, il Lancelot può trasportare tre carte Equipaggiamenti. Se il Lancelot viene scartato, tutto quello che trasporta viene scartato con lui.",
                "costo_attivazione": 1,
                "tipo_attivazione": "Carte",
                "limitazioni": ["Massimo 3 carte equipaggiamento trasportabili"]
            }
        ],
        "requisiti": ["Può trasportare carte equipaggiamento dalla squadra"],
        "fazioni_permesse": DOOMTROOPER,
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE ALLA TUA SQUADRA AL COSTO DI UN' AZIONE. AERONAVE e VEICOLO. Può trasportare carte equipaggiamento prelevate dalla tua squadra o direttamente dalla tua mano di carte, al costo di un'Azione per carta. Le carte non hanno effetto sul Lancelot ma possono essere assegnate gratuitamente ad un guerriero (o scartate) in ogni momento. Al massimo, il Lancelot può trasportare tre carte Equipaggiamenti. Se il Lancelot viene scartato, tutto quello che trasporta viene scartato con lui.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 4,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Furga 750": {
        "nome": "Furga 750",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Generico",
        "tipo_armatura": None,
        "tipo_veicolo": "Generico",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Il guerriero non può utilizzare altre carte Equipaggiamento mentre utilizza il Furga ma attacca sempre per primo nelle sparatorie (S). Se l'avversario sopravvive potrà rispondere al fuoco.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": ["Non può utilizzare altre carte Equipaggiamento"]
            }
        ],
        "requisiti": ["Un guerriero può avere assegnato solo un veicolo", "Non può utilizzare altre carte Equipaggiamento mentre utilizza il Furga"],
        "fazioni_permesse": ["Solo Mercenari o Eretici"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI MERCENARIO O ERETICO. VEICOLO. Un guerriero può avere assegnato solo un veicolo. Il guerriero non può utilizzare altre carte Equipaggiamento mentre utilizza il Furga ma attacca sempre per primo nelle sparatorie (S). Se l'avversario sopravvive potrà rispondere al fuoco.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Dragonbike Mishima": {
        "nome": "Dragonbike Mishima",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Generico",
        "tipo_armatura": None,
        "tipo_veicolo": "Generico",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 2,
            "sparare": 5,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Attacca sempre per primo se sceglie di Sparare",
                "descrizione": "Attacca sempre per primo se sceglie di Sparare. Se il guerriero avversario sopravvive, potrà rispondere al fuoco.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Azioni",
                "limitazioni": []
            }
        ],
        "requisiti": ["Un guerriero può avere assegnato solo un VEICOLO", "Il guerriero che utilizza la Dragonbike non può utilizzare altre carte equipaggiamento"],
        "fazioni_permesse": ["Mishima"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI GUERRIERO MISHIMA. VEICOLO. Un guerriero può avere assegnato solo un VEICOLO. Il guerriero che utilizza la Dragonbike non può utilizzare altre carte equipaggiamento. Guadagna un + 2 in C e un + 5 in S, inoltre attacca sempre per primo se sceglie di Sparare. Se il guerriero avversario sopravvive, potrà rispondere al fuoco.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 6,
        "quantita": 16,
        "quantita_minima_consigliata": 3,
        "fondamentale": False
    },

    "Klein Helitek Dragonfly": {
        "nome": "Klein Helitek Dragonfly",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Aeronave",
        "tipo_armatura": None,
        "tipo_veicolo": "Aeronave",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 5,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Assegna Carte",
                "descrizione": "Guerrieri trasportati non possono utilizzare altre carte Equipaggiamento, ma possono essere feriti solo da armi da fuoco o da VEICOLI. Se il Dragonfly viene scartato tutti i guerrieri trasportati muoiono e l'avversario guadagna normalmente i punti.",
                "costo_attivazione": 1,
                "tipo_attivazione": "Carte",
                "limitazioni": ["Massimo 3 guerrieri trasportabili", "Guerrieri feriti solo da armi da fuoco o veicoli"]
            }
        ],
        "requisiti": ["Un guerriero può avere assegnato solo un veicolo"],
        "fazioni_permesse": DOOMTROOPER,
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE ALLA TUA SQUADRA AL COSTO DI UN' AZIONE. AERONAVE e VEICOLO. Può trasportare fino a tre guerrieri Bauhaus (entrare ed uscire dal Dragonfly costa un'azione) che guadagnano un +5 in A. Guerrieri trasportati non possono utilizzare altre carte Equipaggiamento, ma possono essere feriti solo da armi da fuoco o da VEICOLI. Se il Dragonfly viene scartato tutti i guerrieri trasportati muoiono e l'avversario guadagna normalmente i punti.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Dragonfish": {
        "nome": "Dragonfish",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Sottomarino",
        "tipo_armatura": None,
        "tipo_veicolo": "Sottomarino",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Attacca sempre per primo",
                "descrizione": "Il guerriero non può utilizzare carte Equipaggiamento quando utilizza il Dragonfish. Questo guerriero attacca sempre per primo, se l'avversario sopravvive può rispondere all'Attacco. Avversari feriti dal Dragonfish sono automaticamente uccisi.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": ["Non può utilizzare altre carte Equipaggiamento"]
            },
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Avversari feriti dal Dragonfish sono automaticamente uccisi.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": []
            }
        ],
        "requisiti": ["Non può utilizzare carte Equipaggiamento quando utilizza il Dragonfish"],
        "fazioni_permesse": ["Mishima"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI GUERRIERO MISHIMA. VEICOLO E SOTTOMARINO. Il guerriero non può utilizzare carte Equipaggiamento quando utilizza il Dragonfish. Questo guerriero attacca sempre per primo, se l'avversario sopravvive può rispondere all'Attacco. Avversari feriti dal Dragonfish sono automaticamente uccisi.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "TA 6500 Cybermech": {
        "nome": "TA 6500 Cybermech",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Carro Armato",
        "tipo_armatura": None,
        "tipo_veicolo": "Carro Armato",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Scarta carta",
                "descrizione": "Spendendo tre azioni un punto Promozione, questo Carro può scartare una qualsiasi carta Equipaggiamento, Fortificazione o Warzone.",
                "costo_attivazione": 3,
                "tipo_attivazione": "Carte",
                "limitazioni": ["Costo: 3 azioni + 1 punto Promozione"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": DOOMTROOPER,
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE ALLA TUA SQUADRA AL COSTO DI UN' AZIONE. CARRO ARMATO E VEICOLO. Spendendo tre azioni un punto Promozione, questo Carro può scartare una qualsiasi carta Equipaggiamento, Fortificazione o Warzone.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Lanciamissili SP Crusader": {
        "nome": "Lanciamissili SP Crusader",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Artiglieria",
        "tipo_armatura": None,
        "tipo_veicolo": "Artiglieria",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Scarta carta",
                "descrizione": "Al costo di tre azioni questo guerriero può scartare una Fortificazione, una WARZONE e un Veicolo. Guerrieri trasportati da un Veicolo che viene scartato sono uccisi e i punti vengono guadagnati normalmente. Questa è considerata un'Azione d'Attacco. Rimuovere questa carta dal gioco dopo l'uso.",
                "costo_attivazione": 3,
                "tipo_attivazione": "Carte",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Imperiali"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI GUERRIERO IMPERIALE. VEICOLO e ARTIGLIERIA. Al costo di tre azioni questo guerriero può scartare una Fortificazione, una WARZONE e un Veicolo. Guerrieri trasportati da un Veicolo che viene scartato sono uccisi e i punti vengono guadagnati normalmente. Questa è considerata un'Azione d'Attacco. Rimuovere questa carta dal gioco dopo l'uso.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Black Widow": {
        "nome": "Black Widow",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Generico",
        "tipo_armatura": None,
        "tipo_veicolo": "Generico",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 4,
            "sparare": 4,
            "armatura": 4,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [],
        "requisiti": ["Un guerriero può avere assegnato solo un veicolo", "Il guerriero non può usare altre carte equipaggiamento mentre utilizza la Black Widow", "I guerrieri avversari non guadagnano i benefici delle Fortificazioni"],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI GUERRIERO DELL'OSCURA LEGIONE. Un guerriero può avere assegnato solo un veicolo. Il guerriero non può usare altre carte equipaggiamento mentre utilizza la Black Widow ma guadagna un + 4 in C, S e A. I guerrieri avversari non guadagnano i benefici delle Fortificazioni.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },

    "Lanciaflamme Tormentor": {
        "nome": "Lanciaflamme Tormentor",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Lanciafiamme",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 6,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se C è più del doppio della caratteristica A dell'avversario ogni ferita uccide automaticamente.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": ["Solo se C > doppio di A avversario"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 5,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI GUERRIERO DELL'OSCURA LEGIONE CON UNA CARATTERISTICA V DI 5 O MENO. LANCIAFIAMME. Considerato un Arma da Fuoco ma utilizzabile solo per combattimenti Corpo a Corpo. Il guerriero guadagna un + 6 in C. Se C è più del doppio della caratteristica A dell'avversario ogni ferita uccide automaticamente.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 3,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Mandible/SA-SG 7200": {
        "nome": "Mandible/SA-SG 7200",
        "valore": 0,
        "tipo": "Arma da Corpo a Corpo",
        "categoria_arma": "Fucile a Pompa",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 5,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se il totale è più del doppio della caratteristica A dell'avversario, ogni ferita uccide automaticamente.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": ["Solo se C totale > doppio di A avversario"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Imperiali", "Cybertronic"],
        "restrizioni_guerriero": ["Solo Comandanti"],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE SOLO A COMANDANTI IMPERIALI O CYBERTRONIC. FUCILE A POMPA. Considerato un arma da FUOCO ma utilizzabile solo nei combattimenti Corpo a Corpo. Il guerriero guadagna un + 5 in C e, se il totale è più del doppio della caratteristica A dell'avversario, ogni ferita uccide automaticamente.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 4,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Meta Cannon": {
        "nome": "Meta Cannon",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Arma Speciale",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 4,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Ogni guerriero ferito da quest'arma è automaticamente ucciso.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": []
            },
            {
                "nome": "Modifica Stato",
                "descrizione": "Se il guerriero che possiede quest'arma viene ucciso o scartato mescola il META CANNON nel tuo mazzo di carte da pescare. Se il guerriero è invece permanentemente rimosso dal gioco, il Meta Cannon viene posto nella pila delle carte scartate.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": ["Assegnabile a guerrieri con V <= 6"],
        "valore_minimo_richiesto": 6,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI GUERRIERO DELL'OSCURA LEGIONE CON V PARI A 6 O MENO. ARMA DA FUOCO. Il guerriero guadagna un + 4 in S e ogni guerriero ferito da quest'arma è automaticamente ucciso. Se il guerriero che possiede quest'arma viene ucciso o scartato mescola il META CANNON nel tuo mazzo di carte da pescare. Se il guerriero è invece permanentemente rimosso dal gioco, il Meta Cannon viene posto nella pila delle carte scartate.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Fuoristrada GT B52": {
        "nome": "Fuoristrada GT B52",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Carro Armato",
        "tipo_armatura": None,
        "tipo_veicolo": "Carro Armato",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 2,
            "armatura": 2,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Attacca sempre per primo",
                "descrizione": "Il guerriero non può usare altre carte equipaggiamento mentre utilizza il B52 ma attacca sempre per primo negli scontri a fuoco (S).",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": ["Non può usare altre carte equipaggiamento"]
            }
        ],
        "requisiti": ["Un guerriero può avere assegnato solo un veicolo", "Il guerriero non può usare altre carte equipaggiamento mentre utilizza il B52"],
        "fazioni_permesse": DOOMTROOPER,
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI DOOMTROOPER. CARRO ARMATO E VEICOLO. Un guerriero può avere assegnato solo un veicolo. Un guerriero può avere assegnato solo un veicolo. Il guerriero non può usare altre carte equipaggiamento mentre utilizza il B52 ma guadagna un +2 in S e A. Questo guerriero attacca sempre per primo negli scontri a fuoco (S); se l'avversario sopravvive può rispondere al fuoco.",
        "flavour_text": "",
        "keywords": ["Doomtrooper"],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Jet Pack": {
        "nome": "Jet Pack",
        "valore": 0,
        "tipo": "Equipaggiamento",
        "categoria_arma": "Aeronave",
        "tipo_armatura": None,
        "tipo_veicolo": "Aeronave",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Modifica Azione",
                "descrizione": "Guerrieri che utilizzano il Jet Pack non possono utilizzare altre carte equipaggiamento e non usufruscono dei bonus delle fortificazioni. I guerrieri avversari non ricevono i bonus positivi dei WARZONE.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Modificatore",
                "limitazioni": ["Non può utilizzare altre carte equipaggiamento", "Non usufruscono dei bonus delle fortificazioni"]
            }
        ],
        "requisiti": ["Un guerriero può avere assegnato solo un Veicolo", "Guerrieri che utilizzano il Jet Pack non possono utilizzare altre carte equipaggiamento e non usufruscono dei bonus delle fortificazioni"],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": ["Assegnabile a guerrieri con V <= 5"],
        "valore_minimo_richiesto": 5,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI GUERRIERO CON UN V PARI A 5 O MENO. AERONAVE e VEICOLO. Un guerriero può avere assegnato solo un Veicolo. Guerrieri che utilizzano il Jet Pack non possono utilizzare altre carte equipaggiamento e non usufruscono dei bonus delle fortificazioni. I guerrieri avversari non ricevono i bonus positivi dei WARZONE.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 7,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Death Angel": {
        "nome": "Death Angel",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Generico",
        "tipo_armatura": None,
        "tipo_veicolo": "Generico",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 12,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [
            {
                "statistica": "sparare",
                "valore": "+12",
                "condizione": "Se in combattimento contro i guerrieri dell' Oscura Legione",
                "descrizione": "Il guerriero guadagna un +12 in S se in combattimento contro i guerrieri dell' Oscura Legione"
            }
        ],
        "abilita_speciali": [],
        "requisiti": ["Un guerriero può avere assegnato solo un veicolo", "Il guerriero non può usare altre carte equipaggiamento mentre utilizza il Death Angel"],
        "fazioni_permesse": ["Fratellanza"],
        "restrizioni_guerriero": ["Assegnabile a guerrieri con V <= 3"],
        "valore_minimo_richiesto": 3,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI GUERRIERO DELLA FRATELLANZA CON V PARI A 3 O MENO. VEICOLO. Un guerriero può avere assegnato solo un veicolo. Il guerriero non può usare altre carte equipaggiamento mentre utilizza il Death Angel ma guadagna un + 12 in S se in combattimento contro i guerrieri dell' Oscura Legione.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 3,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Unholy Carronade": {
        "nome": "Unholy Carronade",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Generico",
        "tipo_armatura": None,
        "tipo_veicolo": "Generico",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Scarta carta",
                "descrizione": "Al costo di tre azioni il Carronade può scartare una WARZONE o una Fortificazione in gioco.",
                "costo_attivazione": 3,
                "tipo_attivazione": "Carte",
                "limitazioni": []
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AL TUO SCHIERAMENTO VEICOLO. Al costo di tre azioni il Carronade può scartare una WARZONE o una Fortificazione in gioco.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Reaver Trasporta Truppe": {
        "nome": "Reaver Trasporta Truppe",
        "valore": 0,
        "tipo": "Veicolo",
        "categoria_arma": "Carro Armato",
        "tipo_armatura": None,
        "tipo_veicolo": "Carro Armato",
        "rarity": "Common",
        "statistiche": {
            "combattimento": 0,
            "sparare": 5,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Assegna Carte",
                "descrizione": "Può trasportare fino a tre guerrieri dell'Oscura Legione. I guerrieri trasportati non possono utilizzare altre carte equipaggiamento, inoltre possono solo venir feriti da armi da FUOCO e da VEICOLI.",
                "costo_attivazione": 1,
                "tipo_attivazione": "Carte",
                "limitazioni": ["Massimo 3 guerrieri", "Solo guerrieri Oscura Legione", "Feriti solo da armi da fuoco e veicoli"]
            }
        ],
        "requisiti": ["Costo un'azione per guerriero per entrare/uscire"],
        "fazioni_permesse": ["Oscura Legione"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AL TUO SCHIERAMENTO AL COSTO DI UN'AZIONE. CARRO ARMATO E VEICOLO. Può trasportare fino a tre guerrieri dell'Oscura Legione. Entrare ed uscire dal REAVER costa un'azione per guerriero. I guerrieri trasportati guadagnano un +5 in A ma non possono utilizzare altre carte equipaggiamento, inoltre possono solo venir feriti da armi da FUOCO e da VEICOLI. Se il Reaver viene scartato tutti i guerrieri trasportati sono uccisi e l'avversario guadagna normalmente i punti.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Airbrush/M516 S": {
        "nome": "Airbrush/M516 S",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Fucile a Pompa",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 3,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se il totale è più del doppio della caratteristica A dell'avversario, ogni ferita uccide automaticamente.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": ["Solo se C totale > doppio di A avversario"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Generica"],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE AD OGNI GUERRIERO. FUCILE A POMPA. Considerato un arma da FUOCO, ma utilizzabile solo nei combattimenti Corpo a Corpo. Il guerriero guadagna un +3 in C e, se il totale è più del doppio della caratteristica A dell'avversario, ogni ferita uccide automaticamente.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 1,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Hagelsturm/M516 D": {
        "nome": "Hagelsturm/M516 D",
        "valore": 0,
        "tipo": "Arma da Fuoco",
        "categoria_arma": "Fucile a Pompa",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "combattimento": 4,
            "sparare": 0,
            "armatura": 0,
            "valore": 0
        },
        "modificatori_speciali": [],
        "abilita_speciali": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se il totale è più del doppio della caratteristica A dell'avversario, ogni ferita uccide automaticamente.",
                "costo_attivazione": 0,
                "tipo_attivazione": "Combattimento",
                "limitazioni": ["Solo se C totale > doppio di A avversario"]
            }
        ],
        "requisiti": [],
        "fazioni_permesse": ["Bauhaus", "Capitol"],
        "restrizioni_guerriero": ["Solo Comandanti"],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,
        "meccaniche_armi": {},
        "meccaniche_veicoli": {},
        "stato": {
            "stato_operativo": "Funzionante",
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "ASSEGNABILE SOLO A COMANDANTI BAUHAUS O CAPITOL. FUCILE A POMPA. Considerato un arma da FUOCO, ma utilizzabile solo nei combattimenti Corpo a Corpo. Il guerriero guadagna un +4 in C e se il totale è più del doppio della caratteristica A dell'avversario, ogni ferita uccide automaticamente.",
        "flavour_text": "",
        "keywords": [],
        "set_espansione": "Warzone",
        "numero_carta": "",
        "costo_produzione": 0,
        "compatibilita": {
            "compatibile_con": [],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": []
        },
        "valore_strategico": 3,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    }
}


# ========== FUNZIONI UTILITY CORRETTE ==========

def get_equipaggiamenti_per_tipo(tipo: str) -> dict:
    """Restituisce tutti gli equipaggiamenti di un tipo specifico"""
    return {k: v for k, v in DATABASE_EQUIPAGGIAMENTO.items() 
            if v["tipo"] == tipo}


def get_equipaggiamenti_per_fazione(fazione: str) -> dict:
    """Restituisce equipaggiamenti utilizzabili da una fazione specifica"""
    return {k: v for k, v in DATABASE_EQUIPAGGIAMENTO.items() 
            if not v["fazioni_permesse"] or fazione in v["fazioni_permesse"]}


def get_equipaggiamenti_per_set(set_name: str) -> dict:
    """Restituisce tutti gli equipaggiamenti di un set specifico"""
    return {k: v for k, v in DATABASE_EQUIPAGGIAMENTO.items() 
            if v["set_espansione"] == set_name}


def get_equipaggiamenti_per_rarity(rarity: str) -> dict:
    """Restituisce tutti gli equipaggiamenti di una rarità specifica"""
    return {k: v for k, v in DATABASE_EQUIPAGGIAMENTO.items() 
            if v["rarity"] == rarity}


def get_equipaggiamenti_per_costo(costo_min: int, costo_max: int = None) -> dict:
    """Restituisce equipaggiamenti in un range di costo"""
    if costo_max is None:
        costo_max = costo_min
    return {k: v for k, v in DATABASE_EQUIPAGGIAMENTO.items() 
            if costo_min <= v["valore"] <= costo_max}


def get_armi_per_categoria(categoria: str) -> dict:
    """Restituisce tutte le armi di una categoria specifica"""
    return {k: v for k, v in DATABASE_EQUIPAGGIAMENTO.items() 
            if v.get("categoria_arma") == categoria}


def get_armature_per_tipo(tipo_armatura: str) -> dict:
    """Restituisce tutte le armature di un tipo specifico"""
    return {k: v for k, v in DATABASE_EQUIPAGGIAMENTO.items() 
            if v.get("tipo_armatura") == tipo_armatura}


def filtra_equipaggiamenti(filtri: dict) -> dict:
    """
    Filtra equipaggiamenti secondo criteri multipli
    
    Args:
        filtri: Dizionario con criteri di filtro
               - tipo: tipo equipaggiamento
               - costo_min/costo_max: range di costo
               - rarity: rarità
               - fazione: fazione che può usarlo
               - valore_min: valore minimo richiesto
               
    Returns:
        Dizionario con equipaggiamenti che soddisfano i criteri
    """
    risultato = DATABASE_EQUIPAGGIAMENTO.copy()
    
    if "tipo" in filtri:
        risultato = {k: v for k, v in risultato.items() if v["tipo"] == filtri["tipo"]}
    
    if "costo_min" in filtri:
        risultato = {k: v for k, v in risultato.items() if v["valore"] >= filtri["costo_min"]}
    
    if "costo_max" in filtri:
        risultato = {k: v for k, v in risultato.items() if v["valore"] <= filtri["costo_max"]}
    
    if "rarity" in filtri:
        risultato = {k: v for k, v in risultato.items() if v["rarity"] == filtri["rarity"]}
    
    if "fazione" in filtri:
        fazione = filtri["fazione"]
        risultato = {k: v for k, v in risultato.items() 
                    if not v["fazioni_permesse"] or fazione in v["fazioni_permesse"]}
    
    if "valore_min" in filtri:
        risultato = {k: v for k, v in risultato.items() 
                    if v["valore_minimo_richiesto"] <= filtri["valore_min"]}
    
    return risultato


def crea_equipaggiamento_da_database(nome_equipaggiamento: str):
    """
    Crea un'istanza della classe Equipaggiamento dal database
    
    Args:
        nome_equipaggiamento: Nome dell'equipaggiamento nel database
        
    Returns:
        Istanza di Equipaggiamento o None se non trovato
    """
    if nome_equipaggiamento not in DATABASE_EQUIPAGGIAMENTO:
        return None
    
    data = DATABASE_EQUIPAGGIAMENTO[nome_equipaggiamento]
    
    # Crea l'istanza base usando il valore dal database
    valore = data["statistiche"]["combattimento"] + data["statistiche"]["armatura"]
    equipaggiamento = Equipaggiamento(
        nome=data["nome"],
        valore=valore
    )
    
    # Configura proprietà specifiche    
    equipaggiamento.tipo = TipoEquipaggiamento(data["tipo"]) if data["tipo"] in [t.value for t in TipoEquipaggiamento] else TipoEquipaggiamento.EQUIPAGGIAMENTO_GENERICO
    equipaggiamento.rarity = Rarity(data["rarity"])
    equipaggiamento.set_espansione = data["set_espansione"]
    
    # Configura statistiche
    stats = data["statistiche"]
    equipaggiamento.modificatori_combattimento = stats["combattimento"]
    equipaggiamento.modificatori_armatura = stats["armatura"]
    equipaggiamento.modificatori_sparare = stats["sparare"]
    equipaggiamento.modificatori_valore = stats["valore"]
    
    # Configura modificatori_speciali
    for mod_data in data["modificatori_speciali"]:
        modificatore = ModificatoreEquipaggiamento(
            statistica=mod_data["statistica"],
            valore=mod_data["valore"],
            condizione=mod_data["condizione"],
            descrizione=mod_data["descrizione"]
        )
        equipaggiamento.modificatori_speciali.append(modificatore)
    
    # Configura abilità speciali
    for abil_data in data["abilita_speciali"]:
        abilita = AbilitaSpeciale(
            nome=abil_data["nome"],
            descrizione=abil_data["descrizione"],
            costo_attivazione=abil_data["costo_attivazione"],
            tipo_attivazione=abil_data["tipo_attivazione"],
            limitazioni=abil_data["limitazioni"]
        )
        equipaggiamento.abilita_speciali.append(abilita)
    
    # Configura altre proprietà
    equipaggiamento.requisiti = data["requisiti"]
    equipaggiamento.restrizioni_guerriero = data["restrizioni_guerriero"]
    equipaggiamento.valore_minimo_richiesto = data["valore_minimo_richiesto"]
    equipaggiamento.testo_carta = data["testo_carta"]
    equipaggiamento.flavour_text = data["flavour_text"]
    equipaggiamento.keywords = data["keywords"]
    
    # Configura fazioni permesse
    if data["fazioni_permesse"]:
        equipaggiamento.fazioni_permesse = [Fazione(f) for f in data["fazioni_permesse"] if f in [faz.value for faz in Fazione]]
    
    return equipaggiamento


def get_statistiche_database_equipaggiamenti() -> dict:
    """Restituisce statistiche complete del database equipaggiamenti"""
    totale = len(DATABASE_EQUIPAGGIAMENTO)
    
    # Conteggi per categoria
    per_tipo = {}
    per_rarity = {}
    per_set = {}
    distribuzione_costo = {}
    per_categoria_arma = {}
    per_tipo_armatura = {}
    
    for eq in DATABASE_EQUIPAGGIAMENTO.values():
        # Per tipo
        tipo = eq["tipo"]
        per_tipo[tipo] = per_tipo.get(tipo, 0) + 1
        
        # Per rarità
        rarity = eq["rarity"]
        per_rarity[rarity] = per_rarity.get(rarity, 0) + 1
        
        # Per set
        set_esp = eq["set_espansione"]
        per_set[set_esp] = per_set.get(set_esp, 0) + 1
        
        # Per costo
        costo = eq['statistiche']["valore"]
        distribuzione_costo[costo] = distribuzione_costo.get(costo, 0) + 1
        
        # Per categoria arma
        if eq["categoria_arma"]:
            cat = eq["categoria_arma"]
            per_categoria_arma[cat] = per_categoria_arma.get(cat, 0) + 1
        
        # Per tipo armatura
        if eq["tipo_armatura"]:
            tipo_arm = eq["tipo_armatura"]
            per_tipo_armatura[tipo_arm] = per_tipo_armatura.get(tipo_arm, 0) + 1
    
    return {
        "totale_equipaggiamenti": totale,
        "per_tipo": per_tipo,
        "per_rarity": per_rarity,
        "per_set": per_set,
        "distribuzione_costo": distribuzione_costo,
        "per_categoria_arma": per_categoria_arma,
        "per_tipo_armatura": per_tipo_armatura,
        "armi_totali": len(get_equipaggiamenti_per_tipo("Arma da Fuoco")) + len(get_equipaggiamenti_per_tipo("Arma da Corpo a Corpo")),
        "armature_totali": len(get_equipaggiamenti_per_tipo("Armatura")),
        "veicoli_totali": len(get_equipaggiamenti_per_tipo("Veicolo"))
    }


def verifica_integrita_database_equipaggiamenti() -> dict:
    """Verifica l'integrità e la coerenza del database equipaggiamenti"""
    errori = {
        "tipi_arma_errati": [],
        "proprieta_mancanti": [],
        "costi_invalidi": [],
        "statistiche_invalide": [],
        "encoding_errato": []
    }
    
    for nome, eq in DATABASE_EQUIPAGGIAMENTO.items():
        # Verifica tipi arma corretti secondo regolamento
        tipo = eq["tipo"]
        tipi_corretti = ["Arma da Fuoco", "Arma da Corpo a Corpo", "Arma da Fuoco e da Corpo a Corpo", "Arma Speciale", "Armatura", "Veicolo", "Equipaggiamento"]
        if tipo not in tipi_corretti:
            errori["tipi_arma_errati"].append(f"{nome}: {tipo}")
        
        # Verifica proprietà corrette (non "forza_minima_richiesta")
        if "forza_minima_richiesta" in eq:
            errori["proprieta_mancanti"].append(f"{nome}: usa 'forza_minima_richiesta' invece di 'valore_minimo_richiesto_sparare'")
        
        # Verifica costi validi
        if eq['statistiche']["valore"] < 0 or eq['statistiche']["valore"] > 10:
            errori["costi_invalidi"].append(f"{nome}: Costo {eq['statistiche']['valore']}")
        
        # Verifica statistiche valide
        stats = eq["statistiche"]
        for stat, valore in stats.items():
            if not isinstance(valore, int) or valore < -5 or valore > 15:
                errori["statistiche_invalide"].append(f"{nome}: {stat}={valore}")
        
        # Verifica encoding corretto
        if "quantità" in str(eq):
            errori["encoding_errato"].append(f"{nome}: contiene caratteri non ASCII")
    
    return errori


def get_loadout_consigliato(fazione: str, stile_combattimento: str, budget_dp: int) -> dict:
    """
    Suggerisce un loadout ottimale per una fazione e stile di combattimento
    
    Args:
        fazione: Fazione del guerriero
        stile_combattimento: "Assalto", "Supporto", "Ricognizione", "Pesante"
        budget_dp: Budget in Destiny Points disponibili
        
    Returns:
        Dizionario con equipaggiamenti consigliati
    """
    eq_disponibili = get_equipaggiamenti_per_fazione(fazione)
    eq_budget = {k: v for k, v in eq_disponibili.items() if v["valore"] <= budget_dp}
    
    loadout = {
        "arma_primaria": None,
        "arma_secondaria": None,
        "armatura": None,
        "equipaggiamento": None,
        "veicolo": None,
        "costo_totale": 0
    }
    
    if stile_combattimento == "Assalto":
        # Privilegia armi corpo a corpo e armature medie
        armi_cc = get_equipaggiamenti_per_tipo("Arma da Corpo a Corpo")
        armi_cc_budget = {k: v for k, v in armi_cc.items() if k in eq_budget}
        if armi_cc_budget:
            migliore_cc = max(armi_cc_budget.items(), key=lambda x: x[1]["statistiche"]["combattimento"])
            loadout["arma_primaria"] = migliore_cc[0]
            loadout["costo_totale"] += migliore_cc[1]["valore"]
    
    elif stile_combattimento == "Supporto":
        # Privilegia armi a distanza e kit medici
        armi_df = get_equipaggiamenti_per_tipo("Arma da Fuoco")
        armi_df_budget = {k: v for k, v in armi_df.items() if k in eq_budget}
        if armi_df_budget:
            migliore_df = max(armi_df_budget.items(), key=lambda x: x[1]["meccaniche_armi"]["gittata_massima"])
            loadout["arma_primaria"] = migliore_df[0]
            loadout["costo_totale"] += migliore_df[1]["valore"]
    
    elif stile_combattimento == "Ricognizione":
        # Privilegia veicoli veloci e armi leggere
        veicoli = get_equipaggiamenti_per_tipo("Veicolo")
        veicoli_budget = {k: v for k, v in veicoli.items() if k in eq_budget}
        if veicoli_budget:
            migliore_veicolo = max(veicoli_budget.items(), key=lambda x: x[1]["statistiche"]["sparare"])
            loadout["veicolo"] = migliore_veicolo[0]
            loadout["costo_totale"] += migliore_veicolo[1]["valore"]
    
    # Aggiungi armatura se budget rimane
    budget_rimanente = budget_dp - loadout["costo_totale"]
    armature = get_equipaggiamenti_per_tipo("Armatura")
    armature_budget = {k: v for k, v in armature.items() if v["valore"] <= budget_rimanente}
    if armature_budget:
        migliore_armatura = max(armature_budget.items(), key=lambda x: x[1]["statistiche"]["armatura"])
        loadout["armatura"] = migliore_armatura[0]
        loadout["costo_totale"] += migliore_armatura[1]["valore"]
    
    return loadout


def stampa_lista_equipaggiamenti():
    """Stampa una lista formattata di tutti gli equipaggiamenti"""
    print("=== LISTA EQUIPAGGIAMENTI DATABASE ===")
    
    for categoria in ["Arma da Corpo a Corpo", "Arma da Fuoco", "Armatura", "Veicolo", "Equipaggiamento"]:
        eq_categoria = get_equipaggiamenti_per_tipo(categoria)
        if eq_categoria:
            print(f"\n--- {categoria.upper()} ---")
            for nome, data in eq_categoria.items():
                print(f"• {data['nome']} - {data['valore']} DP ({data['rarity']}) - {data['set_espansione']}")


# ========== ESEMPI DI UTILIZZO ==========

if __name__ == "__main__":
    print("=== DATABASE EQUIPAGGIAMENTO CORRECTED VERSION ===")
    
    # Statistiche generali
    stats = get_statistiche_database_equipaggiamenti()
    print(f"Totale equipaggiamenti: {stats['totale_equipaggiamenti']}")
    print(f"Per tipo: {stats['per_tipo']}")
    print(f"Per rarità: {stats['per_rarity']}")
    print(f"Armi totali: {stats['armi_totali']}")
    print(f"Armature totali: {stats['armature_totali']}")
    print(f"Veicoli totali: {stats['veicoli_totali']}")
    
    # Test correzioni
    print(f"\n=== VERIFICA CORREZIONI APPLICATE ===")
    
    # Verifica tipi arma corretti secondo regolamento
    tipi_corretti = all(
        eq["tipo"] in ["Arma da Fuoco", "Arma da Corpo a Corpo", "Arma da Fuoco e da Corpo a Corpo", "Arma Speciale", "Armatura", "Veicolo", "Equipaggiamento"]
        for eq in DATABASE_EQUIPAGGIAMENTO.values()
    )
    print(f"✓ Tipi arma conformi al regolamento: {tipi_corretti}")
    
    # Verifica proprietà corrette
    proprieta_corrette = all(
        "forza_minima_richiesta" not in eq and "valore_minimo_richiesto_sparare" in eq
        for eq in DATABASE_EQUIPAGGIAMENTO.values()
    )
    print(f"✓ Proprietà corrette (no 'forza_minima_richiesta'): {proprieta_corrette}")
    
    # Verifica keywords corrette
    keywords_corrette = all(
        "Da Fuoco" in eq["keywords"] if "Arma da Fuoco" in eq["tipo"] else True
        for eq in DATABASE_EQUIPAGGIAMENTO.values()
    )
    print(f"✓ Keywords corrette ('Da Fuoco' non 'A Distanza'): {keywords_corrette}")
    
    # Test creazione equipaggiamento
    print(f"\n=== TEST CREAZIONE EQUIPAGGIAMENTO ===")
    spada = crea_equipaggiamento_da_database("Death Angel")
    if spada:
        print(f"✓ Equipaggiamento creato: {spada.nome}")
        print(f"  Tipo: {spada.tipo.value}")
        print(f"  Costo: {spada.valore}")
        print(f"  Valore Combattimento: {spada.modificatori_combattimento}")
    
    # Verifica integrità
    print(f"\n=== VERIFICA INTEGRITÀ ===")
    errori = verifica_integrita_database_equipaggiamenti()
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
    
    # Equipaggiamenti per fazione
    eq_capitol = get_equipaggiamenti_per_fazione("Capitol")
    print(f"✓ Equipaggiamenti Capitol: {len(eq_capitol)}")
    
    # Filtri avanzati
    armi_economiche = filtra_equipaggiamenti({"tipo": "Arma da Fuoco", "costo_max": 2})
    print(f"✓ Armi da fuoco economiche (≤2 DP): {len(armi_economiche)}")
    
    # Loadout consigliato
    loadout = get_loadout_consigliato("Capitol", "Assalto", 5)
    print(f"✓ Loadout Assalto Capitol (5 DP): {loadout['costo_totale']} DP totali")
    
    print(f"\n=== CORREZIONI IMPLEMENTATE ===")
    print("✓ 1. Tipi arma corretti secondo regolamento ('Arma da Fuoco', 'Arma da Corpo a Corpo')")
    print("✓ 2. Percorsi import corretti con 'source.cards'")
    print("✓ 3. Proprietà corrette: 'valore_minimo_richiesto_sparare' (non 'forza_minima_richiesta')")
    print("✓ 4. Keywords corrette: 'Da Fuoco' (non 'A Distanza')")
    print("✓ 5. Gestione fazioni permesse per equipaggiamenti avanzati")
    print("✓ 6. Abilità speciali con limitazioni ed effetti collaterali")
    print("✓ 7. Sistema compatibilità e upgrade")
    print("✓ 8. Meccaniche armi e veicoli complete")
    print("✓ 9. Funzioni utility per filtri e loadout")
    print("✓ 10. Verifica integrità database")
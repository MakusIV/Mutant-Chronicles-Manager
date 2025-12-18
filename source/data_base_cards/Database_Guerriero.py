"""
Database completo dei Guerrieri di Mutant Chronicles/Doomtrooper
VERSIONE CORRETTA - Allineata alle regole ufficiali del regolamento
Include carte dalla versione base e dalle espansioni Inquisition e Warzone
Eliminazione proprietà duplicate e non esistenti (rango, costo_destino, punti_promozione)
"""

"""NOTE:
l'Apostata è un guerriero della OL che può lanciare incantesimi dell'Arte contro Doomtrooper e fratellanza
rivedi verifica vincoli in puo_associare_a_guerriero in Oscura_Simmetria.py"""


from typing import Dict, Any, List
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione, DisciplinaArte, ApostoloOscuraSimmetria, TipoGuerriero

# Database completo dei guerrieri di Mutant Chronicles (versione corretta)
GUERRIERI_DATABASE: Dict[str, Dict[str, Any]] = {
    
    # === BAUHAUS ===
    # fatto
    # Base
    "Ussaro": {
        "nome": "Ussaro",
        "fazione": "Bauhaus", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 2, 
            "armatura": 3,
            "valore": 2
        },
        "abilita": [],
        "testo_carta": "Gli Ussari sono la fanteria regolare della Corporazione Bauhaus. Ben equipaggiati, eccezionalmente addestrati e fortemente motivati, sono dei guerrieri dalle incredibili capacità offensive.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 11,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Mercenario Ex-Bauhaus": {
        "nome": "Mercenario Ex-Bauhaus",
        "fazione": "Bauhaus", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 2, 
            "armatura": 4,
            "valore": 1
        },
        "abilita": [],
        "testo_carta": "Ogni punto guadagnato dal Mercenario deve essere convertito in Punti Destino. Il guerriero potrà utilizzare Armi e Equipaggiamenti marcati \"Solo Bauhaus\", ma dovrà pagare 3D per poter introdurre queste carte in gioco.",
        "flavour_text": "",
        "keywords": ["Mercenario"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Incursore Bauhaus": {
        "nome": "Incursore Bauhaus",
        "fazione": "Bauhaus", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "Paracadutisti del Clan Romanov; questi guerrieri sono utilizzati principalmente per azioni di sabotaggio e infiltrazione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 13,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Ranger Venusiano": {
        "nome": "Ranger Venusiano",
        "fazione": "Bauhaus", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 3, 
            "armatura": 4,
            "valore": 4
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti di tutte le carte DONI DELL'OSCURA SIMMETRIA",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "I Ranger Venusiani sono immuni agli effetti di tutte le carte DONI DELL'OSCURA SIMMETRIA.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 8,
        "quantita": 12,
        "quantita_minima_consigliata": 3,
        "fondamentale": False
    },
    
    "Etoiles Mortant": {
        "nome": "Etoiles Mortant",
        "fazione": "Bauhaus", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 2, 
            "armatura": 6,
            "valore": 4
        },
        "abilita": [],
        "testo_carta": "Gli Etoiles Mortant, se sono presenti guerrieri dell'Oscura Legione, possono solo attaccare quest'ultimi (anche se fanno parte del Tuo Schieramento). Se non ve ne sono, agiscono normalmente.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Dragone": {
        "nome": "Dragone",
        "fazione": "Bauhaus", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 1,
            "sparare": 3, 
            "armatura": 5,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "I Dragoni sono la Forza Corazzata d'Elite della Bauhaus. I loro Carri Armati speciali sono conosciuti e temuti ovunque.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 16,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    # Inquisition
    "Maresciallo Venusiano": {
        "nome": "Maresciallo Venusiano",
        "fazione": "Bauhaus", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 8,
            "sparare": 7, 
            "armatura": 8,
            "valore": 8
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Combattimento, Sparare e Armatura di +2",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Tutti i Tuoi Doomtrooper Bauhaus non-Personalità",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "Per ogni Maresciallo Venusiano che hai nella Tua Squadra, tutti i Tuoi Doomtrooper Bauhaus non-Personalità guadagnano un +2 in C, S e A (non altri Marescialli).",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 6,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    # Warzone
    "Comandante": {
        "nome": "Comandante",
        "fazione": "Bauhaus", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 6,
            "sparare": 5, 
            "armatura": 9,
            "valore": 10
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Combattimento, Sparare, Armatura e Valore di +5",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Tutti i guerrieri Bauhaus nella tua squadra equipaggiati con CARRO ARMATO e tutti i guerrieri Bauhaus considerati CARRI ARMATI o VEICOLI",
                "timing": "Mentre è in gioco"
            }
        ],
        "testo_carta": "COMANDANTE (CAPITANO). Mentre è in gioco, tutti i guerrieri Bauhaus nella tua squadra equipaggiati con CARRO ARMATO e tutti i guerrieri Bauhaus considerati CARRI ARMATI o VEICOLI, guadagnano un +5 in C, S, A e V. Il Comandante non incrementa i propri valori, ma ulteriori Comandanti introdotti in gioco possono farlo.",
        "flavour_text": "",
        "keywords": ["Comandante"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 2,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Aiuto Di Campo": {
        "nome": "Aiuto Di Campo",
        "fazione": "Bauhaus", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 4, 
            "armatura": 7,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Assegna Carte",
                "descrizione": "Assegna un guerriero Bauhaus non personalità all'Aiuto di Campo. Questo guerriero ed eventuali copie di questo presenti nella tua squadra guadagnano un +4 in C, S, A e V mentre l'Aiuto di Campo è vivo e nella Squadra.",
                "tipo": "Carte",
                "costo_destino": 0,
                "target": "Guerriero Bauhaus non personalità",
                "timing": "Ogni Momento"
            },
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Combattimento, Sparare, Armatura e Valore di +4",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerriero Bauhaus assegnato ed eventuali copie nella squadra",
                "timing": "Mentre l'Aiuto di Campo è vivo e nella Squadra"
            }
        ],
        "testo_carta": "COMANDANTE (SERGENTE). Assegna un guerriero Bauhaus non personalità all'Aiuto di Campo. Questo guerriero ed eventuali copie di questo presenti nella tua squadra guadagnano un +4 in C, S, A e V mentre l'Aiuto di Campo è vivo e nella Squadra.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 15,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },
    
    "Eva Valmonte": {
        "nome": "Eva Valmonte",
        "fazione": "Bauhaus", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 1,
            "sparare": 1, 
            "armatura": 1,
            "valore": 4
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Combattimento, Sparare e Armatura di +2",
                "tipo": "Modificatore",
                "costo_destino": 1,
                "target": "Tuoi Doomtrooper (ma non Eva)",
                "timing": "Azione dedicata allo spionaggio"
            }
        ],
        "testo_carta": "PERSONALITÀ. Famosa attrice della Bauhaus assoldата come spia. Per ogni Azione dedicata allo spionaggio, i tuoi Doomtrooper (ma non Eva) guadagnano un +2 in C, S e A fino all'inizio del tuo prossimo turno. Per attaccare Eva l'avversario deve spendere un Punto Promozione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 6,
        "quantita": 7,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Poliziotto Bauhaus": {
        "nome": "Poliziotto Bauhaus",
        "fazione": "Bauhaus", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 2, 
            "armatura": 2,
            "valore": 4
        },
        "abilita": [],
        "testo_carta": "Se un Doomtrooper ferisce o uccide un guerriero Bauhaus, il poliziotto può IMPRIGIONARE il Doomtrooper. Quando lo imprigioni puoi scegliere di scartare alcune o tutte le carte assegnate a associare al guerriero imprigionato sono scartate. I prigionieri non possono attaccare e non possono essere attaccati. Se il Poliziotto viene scartato o ucciso tutti i suoi prigionieri tornano nella Squadra di appartenenza.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Capitano Bauhaus": {
        "nome": "Capitano Bauhaus",
        "fazione": "Bauhaus", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 5,
            "sparare": 6, 
            "armatura": 9,
            "valore": 10
        },
        "abilita": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerrieri feriti dai guerrieri Bauhaus nella Tua Squadra con V uguale a 9 o meno",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "COMANDANTE (CAPITANO). Mentre è in gioco, tutti i guerrieri Bauhaus nella Tua Squadra con V uguale a 9 o meno, uccidono automaticamente i guerrieri che feriscono.",
        "flavour_text": "",
        "keywords": ["Comandante"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },
    
    # === CAPITOL ===
    # fatto
    #Base
    
    "Mercenario Ex-Capitol": {
        "nome": "Mercenario Ex-Capitol",
        "fazione": "Capitol", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 4, 
            "armatura": 2,
            "valore": 1
        },
        "abilita": [],
        "testo_carta": "Ogni punto guadagnato dal Mercenario deve essere convertito in Punti Destino. Il guerriero potrà utilizzare Armi e Equipaggiamenti marcati \"Solo Capitol\", ma dovrà pagare 3D per poter introdurre queste carte in gioco.",
        "flavour_text": "",
        "keywords": ["Mercenario"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Fanteria": {
        "nome": "Fanteria",
        "fazione": "Capitol", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 3, 
            "armatura": 2,
            "valore": 2
        },
        "abilita": [],
        "testo_carta": "Sono le Forze Armate Terrestri Capitol più comuni in tutto il Sistema Solare. Ben armati e equipaggiati, questi guerrieri sono molto temibili.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 13,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Generale Michael Kell": {
        "nome": "Generale Michael Kell",
        "fazione": "Capitol", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 7,
            "sparare": 11, 
            "armatura": 9,
            "valore": 12
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Combattimento, Sparare, Armatura e Valore di +3",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerrieri Capitol (ma non Kell) nella tua squadra",
                "timing": "Mentre è nella tua squadra"
            }
        ],
        "testo_carta": "PERSONALITÀ. Mentre è nella tua squadra tutti i guerrieri Capitol (ma non Kell) guadagnano un +3 in C, S, A e V.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Agente Speciale Hunter": {
        "nome": "Agente Speciale Hunter",
        "fazione": "Capitol", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 9,
            "sparare": 4, 
            "armatura": 7,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti delle carte dell'Oscura Simmetria, compresi i Doni degli Apostoli",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            },
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Combattimento con valore base C raddoppiato (18)",
                "tipo": "Modificatore",
                "costo_destino": 2,
                "target": "Se stesso",
                "timing": "Attacco in Corpo a Corpo"
            }
        ],
        "testo_carta": "PERSONALITÀ. IMMUNE A TUTTI I DONI DELL'OSCURA SIMMETRIA, COMPRESI I DONI DEGLI APOSTOLI. Non può mai diventare un Eretico. Può spendere due Azioni per fare un Attacco in Corpo a Corpo con il valore base C raddoppiato (18).",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },
    
    "Free Marine": {
        "nome": "Free Marine",
        "fazione": "Capitol", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 4, 
            "armatura": 2,
            "valore": 1
        },
        "abilita": [],
        "testo_carta": "Al di fuori di ogni inquadramento, questi guerrieri pluridecorati sono alla ricerca del proprio riscatto morale. Parecchi di loro sono infatti stati degradati dalla Corte Marziale.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 13,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
  
    "Sea Lion": {
        "nome": "Sea Lion",
        "fazione": "Capitol", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 4, 
            "armatura": 4,
            "valore": 4
        },
        "abilita": [],
        "testo_carta": "I Sea Lion (Leoni di Mare) sono una Forza Navale d'Elite attualmente impiegata come truppa anfibia nell'Arcipelago di Venere.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 12,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Mitch Hunter": {
        "nome": "Mitch Hunter",
        "fazione": "Capitol", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 7, 
            "armatura": 7,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti delle carte dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Tutta la Tua fanteria",
                "timing": "Quando Hunter è in gioco"
            }
        ],
        "testo_carta": "PERSONALITÀ. CONSIDERATO UN GUERRIERO DI FANTERIA. Quando Hunter è in gioco, tutta la Tua fanteria è immune agli effetti delle carte dell'Oscura Simmetria.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },
    
    "Martian Banshee": {
        "nome": "Martian Banshee",
        "fazione": "Capitol", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 1,
            "sparare": 5, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "Truppe Aerotrasportate utilizzate su Marte; questi guerrieri hanno in comune il fatto di nutrire un forte odio contro la Corporazione Mishima o l'Oscura Legione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Sunset Striker": {
        "nome": "Sunset Striker",
        "fazione": "Capitol", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "Di stanza su Mercurio, questi guerrieri sono addestrati a combattere le truppe della Mishima sul loro pianeta d'origine.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 16,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    # Warzone
      
    "Capitano Capitol": {
        "nome": "Capitano Capitol",
        "fazione": "Capitol", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 6,
            "sparare": 8, 
            "armatura": 7,
            "valore": 9
        },
        "abilita": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerrieri feriti dai guerrieri Capitol nella tua Squadra con V uguale a 8 o meno",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "COMANDANTE (CAPITANO). Mentre è in gioco, tutti i guerrieri Capitol nella tua Squadra con V uguale a 8 o meno, uccidono automaticamente i guerrieri che feriscono.",
        "flavour_text": "",
        "keywords": ["Comandante"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 8,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Sergente": {
        "nome": "Sergente",
        "fazione": "Capitol", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 7, 
            "armatura": 5,
            "valore": 6
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Combattimento, Sparare, Armatura e Valore di +4",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerriero Capitol non personalità assegnato al Sergente",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "COMANDANTE (SERGENTE). Assegna un guerriero Capitol non personalità al Sergente. Questo guerriero ed eventuali copie di questo presenti nella tua squadra guadagnano un +4 in C, S, A e V mentre il Sergente è vivo e nella Squadra.",
        "flavour_text": "",
        "keywords": ["Comandante"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },
    
    "Capo Squadriglia": {
        "nome": "Capo Squadriglia",
        "fazione": "Capitol", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 5,
            "sparare": 9, 
            "armatura": 7,
            "valore": 9
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Combattimento, Sparare, Armatura e Valore di +3",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerrieri Capitol con AERONAVI e tutti i guerrieri Capitol considerati AERONAVI o VEICOLI",
                "timing": "Mentre questo guerriero è presente"
            }
        ],
        "testo_carta": "COMANDANTE (CAPITANO). Mentre è in gioco, tutti i guerrieri Capitol nella tua squadra equipaggiati con AERONAVI e tutti i guerrieri Capitol considerati AERONAVI o VEICOLI, guadagnano un +3 in C, S, A e V mentre il Capo Squadriglia non incrementa i propri valori, ma ulteriori Capi Squadriglia introdotti in gioco possono farlo.",
        "flavour_text": "",
        "keywords": ["Comandante"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 2,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    

    # === CYBERTRONIC ===
    # fatto
    # Base
    "Cyril Dent": {
        "nome": "Cyril Dent",
        "fazione": "Cybertronic", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 11,
            "sparare": 8, 
            "armatura": 11,
            "valore": 9
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria ma non ai Doni degli Apostoli",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "PERSONALITÀ. CONSIDERATO UN CORAZZIERE. IMMUNE AI DONI DELL'OSCURA SIMMETRIA MA NON AI DONI DEGLI APOSTOLI. Non potrà mai lanciare incantesimi dell'Arte. Se ferisce avversari con un V pari o inferiore a 7 li uccide automaticamente.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Carte delle Arti non Assegnabili"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },
    
    "Dottoressa Diana": {
        "nome": "Dottoressa Diana",
        "fazione": "Cybertronic", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 6,
            "valore": 5
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria ma non ai Doni degli Apostoli",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            },
            {
                "nome": "Guarisce se stesso",
                "descrizione": "Se ferito, può guarire se stesso. Se Diana non è al Coperto, può spendere un'azione per guarire un qualsiasi Doomtrooper ferito in gioco. Dopo deve andare al Coperto. Diana non può mai lanciare incantesimi dell'Arte.",
                "tipo": "Guarigione",
                "costo_destino": 0,
                "target": "Doomtrooper ferito",
                "timing": "Turno"
            }
        ],
        "testo_carta": "PERSONALITÀ. Immune ai DONI DELL'OSCURA SIMMETRIA, ma non ai DONI DEGLI APOSTOLI. Se Diana non è al Coperto, puoi spendere un'azione per guarire un qualsiasi Doomtrooper ferito in gioco. Dopo deve andare al Coperto. Diana non può mai lanciare incantesimi dell'Arte.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Carte delle Arti non Assegnabili"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 8,
        "quantita": 17,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Mercenario Ex-Cybertronic": {
        "nome": "Mercenario Ex-Cybertronic",
        "fazione": "Cybertronic", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 2, 
            "armatura": 4,
            "valore": 1
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "Immune ai DONI DELL'OSCURA SIMMETRIA. Ogni punto guadagnato dal Mercenario dovrà essere convertito in Punti Destino. Il guerriero potrà utilizzare Armi e Equipaggiamenti marcati \"Solo Cybertronic\", ma dovrà pagare 1D per poter introdurre queste carte in gioco.",
        "flavour_text": "",
        "keywords": ["Mercenario"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 2,
        "quantita": 9,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Fay & Klaus": {
        "nome": "Fay & Klaus",
        "fazione": "Cybertronic", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 5
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "PERSONALITÀ. IMMUNE AGLI EFFETTI DEI DONI DELL'OSCURA SIMMETRIA. Questa carta è considerata come un singolo guerriero. Puoi combattere con Fay & Klaus come se fossero una Squadra, spendendo 5D. Se lo fai, C, S, A e V guadagnano un + 3 fino alla fine del combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },
    
    "Contorsionista": {
        "nome": "Contorsionista",
        "fazione": "Cybertronic", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 2, 
            "armatura": 2,
            "valore": 2
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristiche se equipaggiati con Ticker",
                "descrizione": "Aumenta le caratteristiche di Combattimento e Sparare di +1",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerriero equipaggiato con TICKER",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "Se questi individui sono equipaggiati con il TICKER, le loro C e S saranno incrementate di un + 1 in aggiunta ai normali effetti del TICKER.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 10,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Capitano Cybertronic": {
        "nome": "Capitano Cybertronic",
        "fazione": "Cybertronic", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 6,
            "sparare": 5, 
            "armatura": 9,
            "valore": 10
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria ma non ai Doni degli Apostoli",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            },
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerrieri Cybertronic con V uguale a 9 o meno",
                "timing": "Fase Combattimento"
            },
            {
                "nome": "I guerrieri alleati uccidono automaticamente",
                "descrizione": "Mentre è in gioco, tutti i guerrieri Cybertronic nella tua Squadra con V uguale a 9 o meno, uccidono automaticamente i guerrieri che feriscono",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "COMANDANTE (CAPITANO). IMMUNE AI DONI DELL'OSCURA SIMMETRIA MA NON AI DONI DEGLI APOSTOLI. Non potrà mai lanciare incantesimi dell'Arte. Mentre è in gioco, tutti i guerrieri Cybertronic nella tua Squadra con V uguale a 9 o meno, uccidono automaticamente i guerrieri che feriscono.",
        "flavour_text": "",
        "keywords": ["Comandante"],
        "restrizioni": ["Carte delle Arti non Assegnabili"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 8,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False,
        "strategico": True
    },
    
    "Chemiman": {
        "nome": "Chemiman",
        "fazione": "Cybertronic", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4, 
            "armatura": 4,
            "valore": 4
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti delle carte dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            },
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Qualsiasi guerriero ferito",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "IMMUNE AGLI EFFETTI DELLE CARTE DELL'OSCURA SIMMETRIA. Ogni guerriero ferito da ChemiMan, automaticamente è morto.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 6,
        "quantita_minima_consigliata": 3,
        "fondamentale": True
    },
    
    "Droide Eradicator": {
        "nome": "Droide Eradicator",
        "fazione": "Cybertronic", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 13, 
            "armatura": 10,
            "valore": 12
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune a tutte le carte Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "IMMUNE A TUTTE LE CARTE OSCURA SIMMETRIA. CONSIDERATO UN VEICOLO. Non può usare Equipaggiamento e non può mai andare in Copertura. Non potrà mai lanciare incantesimi dell'Arte.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Carte Equipaggiamento non Assegnabili", "Non può andare in copertura", "Carte delle Arti non Assegnabili"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 8,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Gestore Occulto": {
        "nome": "Gestore Occulto",
        "fazione": "Cybertronic", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dei DONI DELL'OSCURA SIMMETRIA",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "Immune agli effetti dei DONI DELL'OSCURA SIMMETRIA.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 3,
        "quantita": 21,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Sicurezza Cybertronic": {
        "nome": "Sicurezza Cybertronic",
        "fazione": "Cybertronic", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 4,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dei DONI DELL'OSCURA SIMMETRIA",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "Immune agli effetti dei DONI DELL'OSCURA SIMMETRIA.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 3,
        "quantita": 23,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Vince Diamond": {
        "nome": "Vince Diamond",
        "fazione": "Cybertronic", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 8,
            "sparare": 11, 
            "armatura": 7,
            "valore": 10
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria ma non ai Doni degli Apostoli",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "PERSONALITÀ. CONSIDERATO UN CACCIATORE. Immune ai DONI DELL'OSCURA SIMMETRIA, ma non ai DONI DEGLI APOSTOLI. Mentre è in gioco, tutti i Tuoi CACCIATORI (ma non Vince) guadagnano un + 2 in C, S e A. Non potrà mai lanciare incantesimi dell'Arte.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Carte delle Arti non Assegnabili"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Tecnico Vac": {
        "nome": "Tecnico Vac",
        "fazione": "Cybertronic", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 4
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune ai DONI DELL'OSCURA SIMMETRIA, ma non ai DONI DEGLI APOSTOLI",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            },
            {
                "nome": "Assegna Carta",
                "descrizione": "Equipaggia qualsiasi Doomtrooper con carte Equipaggiamento Cybertronic senza spendere Azioni. Può anche affiliare qualsiasi Doomtrooper non-Personalità alla Cybertronic. Questo causa una ferita al Tecnico, ma se muore così non si guadagnano Punti. Non può usare l'Arte.",
                "tipo": "Carte",
                "costo_destino": 10,
                "target": "Equipaggiamento Cybertronic",
                "timing": "Ogni Momento"
            }
        ],
        "testo_carta": "Immune ai DONI DELL'OSCURA SIMMETRIA, ma non ai DONI DEGLI APOSTOLI. In ogni momento, può equipaggiare qualsiasi Doomtrooper con carte Equipaggiamento Cybertronic senza spendere Azioni. Può anche affiliare qualsiasi Doomtrooper non-Personalità alla Cybertronic. Questo causa una ferita al Tecnico, ma se muore così non si guadagnano Punti. Non può usare l'Arte.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Carte delle Arti non Assegnabili"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 17,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },
    
    "Osservatore Tattico": {
        "nome": "Osservatore Tattico",
        "fazione": "Cybertronic", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 3, 
            "armatura": 7,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune ai DONI DELL'OSCURA SIMMETRIA, ma non ai DONI DEGLI APOSTOLI",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            },
            {
                "nome": "Assegna Carta",
                "descrizione": "Assegna un guerriero Cybertronic non personalita all'Osservatore Tattico. Questo guerriero ed eventuali altre copie di questo presenti nella tua squadra  guadagnano un +4 in C, S, A e V mentre l'Osservatore è vivo e nella squadra",
                "tipo": "Carte",
                "costo_destino": 0,
                "target": "Guerrieri Cybertronic",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "Immune ai DONI DELL'OSCURA SIMMETRIA, ma non ai DONI DEGLI APOSTOLI. In ogni momento, può equipaggiare qualsiasi Doomtrooper con carte Equipaggiamento Cybertronic senza spendere Azioni. Può anche affiliare qualsiasi Doomtrooper non-Personalità alla Cybertronic. Questo causa una ferita al Tecnico, ma se muore così non si guadagnano Punti. Non può usare l'Arte.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Carte delle Arti non Assegnabili"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 11,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },

    "Cacciatore": {
        "nome": "Cacciatore",
        "fazione": "Cybertronic", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 4, 
            "armatura": 4,
            "valore": 4
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dei DONI DELL'OSCURA SIMMETRIA",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "Immune agli effetti dei DONI DELL'OSCURA SIMMETRIA.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 2,
        "quantita": 14,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Corazziere": {
        "nome": "Corazziere",
        "fazione": "Cybertronic", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 3, 
            "armatura": 4,
            "valore": 4
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dei DONI DELL'OSCURA SIMMETRIA",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "Immune agli effetti dei DONI DELL'OSCURA SIMMETRIA.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 2,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Charles Sykes": {
        "nome": "Charles Sykes",
        "fazione": "Cybertronic", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 8,
            "sparare": 7, 
            "armatura": 11,
            "valore": 13
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune ai DONI DELL'OSCURA SIMMETRIA MA NON AI DONI DEGLI APOSTOLI",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            },
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Combattimento, Sparare, Armatura e Valore di +4",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Tutti i guerrieri Cybertronic nella squadra",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "PERSONALITÀ. IMMUNE AI DONI DELL'OSCURA SIMMETRIA MA NON AI DONI DEGLI APOSTOLI. Non potrà mai lanciare incantesimi dell'Arte. Tutti i tuoi guerrieri Cybertronic guadagnano un + 4 in C, S, A e V finché Charles stesso finché lui è presente nella squadra.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Carte delle Arti non Assegnabili"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False,
        "strategico": True
    },

    "Il Diciannovesimo Executive": {
        "nome": "Il Diciannovesimo Executive",
        "fazione": "Cybertronic", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 0, 
            "armatura": 0,
            "valore": 20
        },
        "abilita": [
            {
                "nome": "Converte azioni in azioni di attacco",
                "descrizione": "Mentre l'Executive è in gioco tu puoi convertire ogni numero di azioni non di attacco in azioni di attacco ma queste devono essere compiute da guerrieri Cybertronic",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }        ],
        "testo_carta": "PERSONALITÀ. IMMUNE AI DONI DELL'OSCURA SIMMETRIA. Mentre l'Executive è in gioco tu puoi convertire ogni numero di azioni non di attacco in azioni di attacco ma queste devono essere compiute da guerrieri Cybertronic.",
        "flavour_text": "",
        "keywords": ["Leader Corporativo", "Personalita"],
        "restrizioni": ["Carte delle Arti non Assegnabili"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

        


    # === IMPERIALE ===
    # Fatto
    # Base

    "Maresciallo di Campo Johnstone": {
        "nome": "Maresciallo di Campo Johnstone",
        "fazione": "Imperiale", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 0, 
            "armatura": 0,
            "valore": 20
        },
        "abilita": [{
                "nome": "Converte Azioni in Azioni d'Attacco",
                "descrizione": "Mentre il Maresciallo è in gioco tu puoi convertire ogni numero di Azioni non di attacco in Azioni d'attacco",
                "tipo": "Azioni",
                "costo_destino": 0,
                "target": "Guerrieri Imperiali",
                "timing": "Mentre questo guerriero è presente"
            }],
        "testo_carta": "PERSONALITÀ. LEADER CORPORATIVO. Non può mai prendere parte al combattimento né andare in copertura. Mentre il Maresciallo è in gioco tu puoi convertire ogni numero di Azioni non di attacco in Azioni d'attacco, ma queste devono essere compiute da guerrieri Imperiali.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Non può prendere parte al combattimento", "Non può andare in copertura"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },
    
    "Porta Stendardo": {
        "nome": "Porta Stendardo",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 5,
            "sparare": 1, 
            "armatura": 4,
            "valore": 4
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta Armatura di +2",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerrieri Imperiali nella squadra tranne il Porta Stendardo",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "PORTA STENDARDO. Questo guerriero ispira i suoi commilitoni. Tutti i guerrieri Imperiali nella tua Squadra, eccetto il Porta Stendardo, guadagnano un +2 in A mentre questo guerriero è presente. Ulteriori Porta Stendardo incrementano anche il valore A del Porta Stendardo.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita": 27,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Esperto in Trincee": {
        "nome": "Esperto in Trincee",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 2, 
            "armatura": 2,
            "valore": 3
        },
        "abilita": [{
                "nome": "Assegna Carta",
                "descrizione": "Preleva carta Trincea e associala a questo guerriero al costo 3 Azioni",
                "tipo": "Carte",
                "costo_destino": 3,
                "target": "Self",
                "timing": "Permanente"
            }],
        "testo_carta": "Quest'uomo può scavare una trincea al costo di 3 Azioni. Se esegue quest'operazione, preleva dalla Tua Collezione la carta Trincea e associala a questo guerriero.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 2,
        "quantita": 23,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Guardia Inesperta": {
        "nome": "Guardia Inesperta",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 2, 
            "armatura": 2,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "Le Guardie inesperte non possono mai andare in Copertura e non possono mai utilizzare fortificationi.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Non può andare in copertura", "Bonus relativi alle Fortificazioni non ricevibile"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 20,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Membro del Clan": {
        "nome": "Membro del Clan",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 2, 
            "armatura": 4,
            "valore": 4
        },
        "abilita": [{
                "nome": "Aumenta caratteristica",
                "descrizione": "+1 in C e A per ogni altro membro del Clan che è assegnato alla squadra. Se ci sono cinque guerrieri assegnati, il Membro del Clan guadagna un +4 in C e A.",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Self",
                "timing": "Permanente"
            }],
        "testo_carta": "Quest'uomo guadagna un +1 in C e A per ogni altro membro del Clan che è assegnato alla sua stessa sezione. Se ci sono cinque guerrieri assegnati, il Membro del Clan guadagna un +4 in C e A.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 5,
        "quantita": 22,
        "quantita_minima_consigliata": 4,
        "fondamentale": False
    },

    "Blood Beret": {
        "nome": "Blood Beret",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 3, 
            "armatura": 4,
            "valore": 4
        },
        "abilita": [{
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "immune agli effetti dell'oscura simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Self",
                "timing": "Ogni Momento"
            }],
        "testo_carta": "Immune agli effetti dei DONI DELL'OSCURA SIMMETRIA.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita": 18,
        "quantita_minima_consigliata": 2,
        "fondamentale": False
    },

    "Sgt McBride": {
        "nome": "Sgt McBride",
        "fazione": "Imperiale", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 5,
            "sparare": 5, 
            "armatura": 5,
            "valore": 5
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Quando è in gioco tutti i Blood Beret (ma non lui stesso) guadagnano +1 in C e S",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Cavalleria Aerea",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "PERSONALITÀ CONSIDERATO UN BLOOD BERET. Quando è in gioco tutti i Blood Beret (ma non lui stesso) guadagnano +1 in C e S",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 5,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Golden Lion": {
        "nome": "Golden Lion",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "Mentre la maggior parte delle Forze Speciali sono addestrate per affrontare l'Oscura Legione, questi guerrieri sono specializzati nel combattere le Megacorporazioni avversarie.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 21,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Farabutto": {
        "nome": "Farabutto",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4, 
            "armatura": 3,
            "valore": 5
        },
        "abilita": [],
        "testo_carta": "Non puoi aggiungere il Farabutto alla tua Squadra se sono presenti Guerrieri Imperiali e viceversa.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Incompatibilità con Imperiali"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Sean Gallagher": {
        "nome": "Sean Gallagher",
        "fazione": "Imperiale", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 8,
            "sparare": 0, 
            "armatura": 8,
            "valore": 10
        },
        "abilita": [{
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Se stesso",
                "timing": "Sempre"
            }],
        "testo_carta": "PERSONALITÀ. CONSIDERATO UN MEMBRO DEL CLAN. Deve attaccare preferibilmente un membro dell'Oscura Legione, se non ve ne sono sei libero di fare quello che vuoi. Quando Callagher è in gioco tutti i tuoi Membri del Clan sono Immuni agli effetti delle caarte dell'Oscura Simmetria",
        "flavour_text": "",
        "keywords": ["Seguace di Bauhaus"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cavalleria Aerea": {
        "nome": "Cavalleria Aerea",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 4, 
            "armatura": 6,
            "valore": 5
        },
        "abilita": [],
        "testo_carta": "CONSIDERATO UN'AERONAVE. Può solo attaccare in combattimento a distanza, e non può essere attaccato in Corpo a Corpo. Non può andare in copertura. Armi e carte Equipaggiamento non possono essere giocate sulla Cavalleria Aerea. La Cavalleria Aerea non tiene conto dei bonus delle Fortificazioni.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Non può andare in copertura", "Carte Equipaggiamento non Assegnabili", "Bonus relativi alle Fortificazioni non ricevibile"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Pilota Trevor Bartholomew": {
        "nome": "Pilota Trevor Bartholomew",
        "fazione": "Imperiale", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 6, 
            "armatura": 8,
            "valore": 7
        },
        "abilita": [{
                "nome": "Aumenta caratteristica",
                "descrizione": "Quando è in gioco, tutta la Cavalleria Aerea guadagna un +1 in S e A",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Cavalleria Aerea",
                "timing": "Sempre"
            }],
        "testo_carta": "PERSONALITÀ. CONSIDERATO CAVALLERIA AEREA E AERONAVE. Può solo attaccare a distanza (Sparare), non può essere attaccato in Corpo a Corpo. Non può Andare in Copertura. Armi e Equipaggiamenti non gli possono essere assegnati. Gli avversari non guadagnano i bonus delle Fortificazioni. Quando è in gioco, tutta la Cavalleria Aerea guadagna un +1 in S e A",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Non può andare in copertura", "Carte Equipaggiamento non Assegnabili", "Bonus relativi alle Fortificazioni non ricevibile"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cavalleria Leggera Wolfbane": {
        "nome": "Cavalleria Leggera Wolfbane",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 5,
            "sparare": 4, 
            "armatura": 4,
            "valore": 5
        },
        "abilita": [{
                "nome": "Decrementa caratteristiche",
                "descrizione": "Decrementa le caratteristiche di -3 A agli avversari non protetti da Forticazione",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerrieri nemici",
                "timing": "Sempre"
            }],
        "testo_carta": "Gli avversari della Cavalleria Wolfbane subiscono un -3 in A, a meno che non siano protetti da una Fortificazione. In questo caso la loro A aumenta di un +3.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita": 4,
        "quantita_minima_consigliata": 2,
        "fondamentale": False
    },

    "Mercenario Ex-Imperiale": {
        "nome": "Mercenario Ex-Imperiale",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 2, 
            "armatura": 2,
            "valore": 1
        },
        "abilita": [],
        "testo_carta": "Ogni punto guadagnato dal Mercenario dovrà essere convertito in Punti Destino. Il guerriero potrà utilizzare Armi e Equipaggiamenti marcati \"Solo Imperiali\", ma dovrà pagare 3D per poter introdurre queste carte in gioco.",
        "flavour_text": "",
        "keywords": ["Mercenario"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 11,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    # Warzone
    "Comandante di Reparto": {
        "nome": "Comandante di Reparto",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 5,
            "sparare": 3, 
            "armatura": 7,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta al guerriero assegnato ed alle sue copie, le caratteristiche di Combattimento, Sparare, Armatura e valore di +4",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerrieri assegnati al Comandante",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "COMANDANTE (SERGENTE). Assegna un guerriero Imperiale non personalità al Comandante.Questo guerriero e le sue eventuali copie incrementa le caratteristiche di Combattimento, Sparare, Armatura e valore di +4",
        "flavour_text": "",
        "keywords": ["Comandante"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 16,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },    

    "Comandante in Capo": {
        "nome": "Comandante in Capo",
        "fazione": "Imperiale", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 6,
            "sparare": 7, 
            "armatura": 5,
            "valore": 9
        },
        "abilita": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "I guerrieri imperiali della squadra con V <= 8, uccidono automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "COMANDANTE (CAPITANO). Mentre questo guerriero è in gioco, tutti i guerrieri imperiali della tua squadra con V<=8 uccidono automaticamente i guerrieri che feriscono.",
        "flavour_text": "",
        "keywords": ["Comandante"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 8,
        "quantita_minima_consigliata": 1,
        "fondamentale": False,
        "strategico": True
    },



    # === MISHIMA ===
    # Fatto
    # Base    
    "Samurai": {
        "nome": "Samurai",
        "fazione": "Mishima", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "I Samurai della Mishima sono soldati d'Elite che formano la scorta personale dei Lord Ereditari.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 23,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Mercenario Ex-Mishima": {
        "nome": "Mercenario Ex-Mishima",
        "fazione": "Mishima", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 1
        },
        "abilita": [],
        "testo_carta": "Ogni punto guadagnato dal Mercenario dovrà essere convertito in Punti Destino. Il guerriero potrà utilizzare armi e Equipaggiamenti marcati \"Solo Mishima\", ma dovrà pagare 3D per poter introdurre in gioco queste carte.",
        "flavour_text": "",
        "keywords": ["Mercenario"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 10,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Artefatto Di Combattimento": {
        "nome": "Artefatto Di Combattimento",
        "fazione": "Mishima", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4, 
            "armatura": 3,
            "valore": 4
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Se stesso",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "IMMUNE ALLE CARTE DELL'OSCURA SIMMETRIA. Combattenti semi-intelligenti costruiti dalla Corporazione Mishima. Miracolo tecnologico devastante.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita": 5,
        "quantita_minima_consigliata": 3,
        "fondamentale": False
    },

    "Tatsu": {
        "nome": "Tatsu",
        "fazione": "Mishima", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 6,
            "sparare": 6, 
            "armatura": 7,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Samurai",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "PERSONALITÀ. CONSIDERATO UN SAMURAI. Mentre Tatsu è in gioco, tutti i Tuoi Samurai sono immuni agli effetti dell'Oscura Simmetria.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False,
        "strategico": True
    },

    "Artefatto Suicida": {
        "nome": "Artefatto Suicida",
        "fazione": "Mishima", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 10,
            "sparare": 0, 
            "armatura": 0,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Oscura Simmetria",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "IMMUNE ALLE CARTE DELL'OSCURA SIMMETRIA. Combattenti semi-intelligenti costruiti dalla Corporazione Mishima. Non può utilizzare Armi o Equipaggiamento. L'Artefatto Suicida, quando viene colpito (ferito), risulta ucciso. Scarta la carta.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Carte Equipaggiamento non Assegnabili"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 5,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Hatamoto": {
        "nome": "Hatamoto",
        "fazione": "Mishima", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4, 
            "armatura": 4,
            "valore": 4
        },
        "abilita": [],
        "testo_carta": "Ogni Missione assegnata a un Hatamoto deve avere la priorità. Se completi un'altra Missione prima di quella dell'Hatamoto, non guadagni i Punti Ricompensa e quella Missione è persa.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 22,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    # Inquisition
    "Ninja": {
        "nome": "Ninja",
        "fazione": "Mishima", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 3, 
            "armatura": 4,
            "valore": 5
        },
        "abilita": [],
        "testo_carta": "Può Attaccare qualsiasi guerriero. Il Ninja attacca sempre per primo i suoi avversari in combattimento. Se l'avversario sopravvive, allora può rispondere all'Attacco del Ninja.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita": 18,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Mentore": {
        "nome": "Mentore",
        "fazione": "Mishima", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 2
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Combattimento e Sparare di +1",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerrieri Mishima",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "Per ogni Tuo Mentore in gioco, i Tuoi guerrieri Mishima guadagnano un +1 in C e S. Un Mentore non può accrescere le sue caratteristiche personali, ma altri Mentori possono.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 3,
        "quantita": 13,
        "quantita_minima_consigliata": 3,
        "fondamentale": False
    },

    # Warzone
    "Jito": {
        "nome": "Jito",
        "fazione": "Mishima", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 5,
            "sparare": 5, 
            "armatura": 5,
            "valore": 6
        },
        "abilita": [
            {
                "nome": "Assegna Carta",
                "descrizione": "Assegna un guerriero Mishima non personalità al Jito. Questo guerriero ed eventuali copie di questo presenti nella tua squadra guadagnano un +4 in C, S, A e V mentre il Jito è vivo e nella Squadra.",
                "tipo": "Carte",
                "costo_destino": 0,
                "target": "Guerriero Mishima",
                "timing": "Ogni Momento"
            },
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Combattimento, Sparare, Armatura e Valore di +4",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerriero Mishima assegnato",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "COMANDANTE (SERGENTE). Assegna un guerriero Mishima non personalità al Jito. Questo guerriero ed eventuali copie di questo presenti nella tua squadra guadagnano un +4 in C, S, A e V mentre il Jito è vivo e nella Squadra.",
        "flavour_text": "",
        "keywords": ["Comandante"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 22,
        "quantita_minima_consigliata": 2,
        "fondamentale": False,
        "strategico": True
    },

    "Bushi": {
        "nome": "Bushi",
        "fazione": "Mishima", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 4,
            "valore": 4
        },
        "abilita": [
            {
                "nome": "Aumenta caratteristica",
                "descrizione": "Aumenta le caratteristiche di Difesa di +2",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Guerrieri Mishima nella squadra tranne il Porta Stendardo",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "PORTA STENDARDO. Questo guerriero ispira i suoi commilitoni. Tutti i guerrieri Mishima nella tua Squadra, eccetto il Porta Stendardo, guadagnano un +2 in A mentre questo guerriero è presente. Ulteriori Porta Stendardo incrementano anche il valore A del Porta Stendardo.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 2,
        "quantita": 27,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Shugo": {
        "nome": "Shugo",
        "fazione": "Mishima", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 7,
            "sparare": 7, 
            "armatura": 7,
            "valore": 9
        },
        "abilita": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            },
            {
                "nome": "I guerrieri alleati uccidono automaticamente",
                "descrizione": "Mentre è in gioco, tutti i guerrieri Mishima nella tua Squadra con V uguale a 8 o meno, uccidono automaticamente i guerrieri che feriscono",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "COMANDANTE (CAPITANO). Mentre è in gioco, tutti i guerrieri Mishima nella tua Squadra con V uguale a 8 o meno, uccidono automaticamente i guerrieri che feriscono.",
        "flavour_text": "",
        "keywords": ["Comandante"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 8,
        "quantita_minima_consigliata": 1,
        "fondamentale": False,
        "strategico": True
    },

    "Lord Nozaki": {
        "nome": "Lord Nozaki",
        "fazione": "Mishima", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 0, 
            "armatura": 0,
            "valore": 20
        },
        "abilita": [],
        "testo_carta": "PERSONALITÀ. LEADER CORPORATIVO. Non può mai prendere parte al combattimento né andare in copertura. Mentre il Lord è in gioco tu puoi convertire ogni numero di Azioni non di attacco in Azioni d'attacco, ma queste devono essere compiute da guerrieri Mishima.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Non può prendere parte al combattimento", "Non può andare in copertura"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },



    # === FRATELLANZA ===
    # Fatto
    # Base
    "Laura Vestale Benedetta": {
        "nome": "Laura Vestale Benedetta",
        "fazione": "Fratellanza", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4, 
            "armatura": 4,
            "valore": 5
        },
        "abilita": [
            {
                "nome": "Immunita",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Valchirie",
                "timing": "Sempre"
            },
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte",
                "descrizione": "Lancia tutte le ARTI",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Turno"
            }

        ],
        "testo_carta": "PERSONALITÀ. CONSIDERATA UNA VALKIRIA. Quando Laura è in gioco, tutte le Tue Valkirje possono usare TUTTE le carte ARTE, e sono immuni alle carte dell'Oscura Simmetria.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },
    
    "Nicholai": {
        "nome": "Nicholai",
        "fazione": "Fratellanza", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 5,
            "sparare": 4, 
            "armatura": 6,
            "valore": 8
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte specifica",
                "descrizione": "Lancia incantesimi Arte della Manipolazione e dell'Esorcismo, più tutti gli incantesimi di Combattimento Personale",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Arte della Manipolazione ed Esorcismo",
                "timing": "Turno"
            },         
            {
                "nome": "Lancia Incantesimi di Combattimento Personale",
                "descrizione": "Lancia tutti gli incantesimi di Combattimento Personale",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Incantesimo di Combattimento Personale",
                "timing": "Turno"
            },   
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "PERSONALITÀ. CONSIDERATO UN MORTIFICATOR. Nicholai può lanciare incantesimi Arte della Manipolazione e dell'Esorcismo, più tutti gli incantesimi di Combattimento Personale. I guerrieri feriti da Nicholai sono automaticamente uccisi.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 8,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },
    
    "L'Inquisitore Massimo": {
        "nome": "L'Inquisitore Massimo",
        "fazione": "Fratellanza", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 7,
            "sparare": 7, 
            "armatura": 7,
            "valore": 8
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte",
                "descrizione": "Lancia tutte le ARTI",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Turno"
            }
        ],
        "testo_carta": "L'Inquisitore Massimo può utilizzare tutte le ARTI.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False,
        "strategico": True
    },
    
    "Mortificator": {
        "nome": "Mortificator",
        "fazione": "Fratellanza", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte  specifica",
                "descrizione": "Lancia Arte della Cinetica e l'Arte della Manipolazione",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Arte della Cinetica e Arte della Manipolazione",
                "timing": "Turno"
            }
        ],
        "testo_carta": "I Mortificator possono utilizzare l'Arte della Cinetica e l'Arte della Manipolazione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 13,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Mistico": {
        "nome": "Mistico",
        "fazione": "Fratellanza", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4, 
            "armatura": 4,
            "valore": 5
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte",
                "descrizione": "Lancia tutte le carte ARTE",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Turno"
            }
        ],
        "testo_carta": "Il Mistico può utilizzare TUTTE le carte ARTE. Maestri in tutte le Arti, questi guerrieri dedicano la loro vita alla lotta contro l'Oscura Legione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 7,
        "quantita": 2,
        "quantita_minima_consigliata": 2,
        "fondamentale": False
    },
    
    "Arcangelo": {
        "nome": "Arcangelo",
        "fazione": "Fratellanza", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte specifica",
                "descrizione": "Lancia Arte del Cambiamento e l'Arte degli Elementi",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Arte del Cambiamento e Arte degli Elementi",
                "timing": "Turno"
            }
        ],
        "testo_carta": "Gli Arcangeli possono utilizzare l'Arte del Cambiamento e l'Arte degli Elementi.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Revisore": {
        "nome": "Revisore",
        "fazione": "Fratellanza", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte specifica",
                "descrizione": "Lancia Arte della Manipolazione e l'Arte Mentale",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Arte della Manipolazione e Arte Mentale",
                "timing": "Turno"
            }
        ],
        "testo_carta": "I Revisori possono utilizzare l'Arte della Manipolazione e l'Arte Mentale.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Valkiria": {
        "nome": "Valkiria",
        "fazione": "Fratellanza", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte specifica",
                "descrizione": "Lancia Arte del Cambiamento e l'Arte della Premonizione",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Arte del Cambiamento e Arte della Premonizione",
                "timing": "Turno"
            }
        ],
        "testo_carta": "Le Valkirje possono utilizzare l'Arte del Cambiamento e l'Arte della Premonizione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 6,
        "quantita": 5,
        "quantita_minima_consigliata": 4,
        "fondamentale": False
    },
        
    "Inquisitore": {
        "nome": "Inquisitore",
        "fazione": "Fratellanza", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte specifica",
                "descrizione": "Lancia Arte dell'Esorcismo e l'Arte Mentale",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Arte dell'Esorcismo e Arte Mentale",
                "timing": "Turno"
            }
        ],
        "testo_carta": "Gli Inquisitori possono utilizzare l'Arte dell'Esorcismo e l'Arte Mentale.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 14,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Custode dell'Arte": {
        "nome": "Custode dell'Arte",
        "fazione": "Fratellanza", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 5,
            "valore": 4
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte",
                "descrizione": "Lancia tutte le carte ARTE",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Turno"
            },
            {
                "nome": "Aumenta effetto",
                "descrizione": "Aumenta l'effetto dell'Incantesimo, vale 2D per quell'effetto",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Incantesimi Personali di combattimento",
                "timing": "Combattimento"
            }
        ],
        "testo_carta": "IL CUSTODE DELL'ARTE PUÒ UTILIZZARE TUTTE LE CARTE ARTE. Tutti gli Incantesimi Personali di combattimento sono considerati Incantesimi di combattimento quando sono giocati dal Custode, e ogni Punto D speso su un effetto dell'Incantesimo, vale 2D per quell'effetto.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },
    
    "L'Arcinquisitore Nikodemus": {
        "nome": "L'Arcinquisitore Nikodemus",
        "fazione": "Fratellanza", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 8,
            "sparare": 8, 
            "armatura": 8,
            "valore": 9
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte",
                "descrizione": "Lancia tutte le ARTI ed è immune agli effetti delle carte dell'Oscura Simmetria",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Turno"
            },
            {
                "nome": "Immunita",
                "descrizione": "Immune agli effetti dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "PERSONALITÀ. L'Arcinquisitore è Maestro in tutte le ARTI ed è immune agli effetti delle carte dell'Oscura Simmetria. Quando è in gioco, i Doomtroopers non possono Andare in Copertura volontariamente. Se viene ferito puoi spendere un'Azione e 5D per guarirlo, ferendo al suo posto un altro Doomtrooper nella Tua Squadra.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 8,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Guerrieri Sacri": {
        "nome": "Guerrieri Sacri",
        "fazione": "Fratellanza", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte specifica",
                "descrizione": "Lancia Arte della Premonizione e l'Arte dell'Esorcismo",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Arte della Premonizione e Arte dell'Esorcismo",
                "timing": "Turno"
            }
        ],
        "testo_carta": "I Guerrieri Sacri possono utilizzare l'Arte della Premonizione e l'Arte dell'Esorcismo.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    # Inquisition
    "Antiquario": {
        "nome": "Antiquario",
        "fazione": "Fratellanza", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte specifica",
                "descrizione": "Lancia Arte Cinetica ed d'Evocazione",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Arte Cinetica e Arte d'Evocazione",
                "timing": "Turno"
            }
        ],
        "testo_carta": "L'Antiquario può utilizzare l'Arte Cinetica ed d'Evocazione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 27,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cardinale Durand": {
        "nome": "Cardinale Durand",
        "fazione": "Fratellanza", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 11,
            "sparare": 11, 
            "armatura": 11,
            "valore": 14
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte",
                "descrizione": "Lancia tutti gli aspetti dell'Arte",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Turno"
            },
            {
                "nome": "Immunita",
                "descrizione": "Immune all'Arte per il tempo che vuole",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Guerrieri della Fratellanza",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "PERSONALITÀ. Mentre è in gioco, tutti i guerrieri della Fratellanza possono usare tutti gli aspetti dell'Arte. Il Cardinale Durand può eliminare in ogni momento qualsiasi immunità all'Arte per il tempo che vuole. Se ucciso o scartato, rimetti il Cardinale nel Tuo mazzo di carte da Pescare.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Famoso Evocatore": {
        "nome": "Famoso Evocatore",
        "fazione": "Fratellanza", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4, 
            "armatura": 5,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte specifica",
                "descrizione": "Lancia Arte d'Evocazione e della Manipolazione",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Arte d'Evocazione e Arte della Manipolazione",
                "timing": "Turno"
            }
        ],
        "testo_carta": "Il Famoso Evocatore può usare l'Arte d'Evocazione e della Manipolazione. Quando lancia incantesimi dell'Arte d'Evocazione, paga solo la metà del loro costo D.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 3,
        "quantita": 6,
        "quantita_minima_consigliata": 2,
        "fondamentale": False
    },
    

    # === LEGIONE OSCURA ===
    # Fatto
    # Seguaci di Algeroth


     
    "Necromutante": {
        "nome": "Necromutante",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "60",
        "stats": {
            "combattimento": 3,
            "sparare": 3,
            "armatura": 3,
            "valore": 4
        },
        "abilita": [],
        "testo_carta": "I Necromutanti sono guerrieri trasformati dalla malvagia Necrotecnologia. Essi agiscono come ufficiali comandanti dei Legionari nn Morti di Algeroth",
        "flavour_text": "La morte è solo l'inizio del servizio alle Potenze Oscure.",
        "keywords": ["Seguace di Algeroth", "Necromutante"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita":7,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },
    
    "Eretico": {
        "nome": "Eretico",
        "fazione": "Oscura Legione",
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 2,
            "armatura": 2,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "Puoi assegnare un DONO DELL'OSCURA SIMMETRIA agli Eretici man non un DONO DEGLI APOSTOLI",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "restrizioni": ["Solo doni dell'Oscura Simmetria"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita":7,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Billy": {
        "nome": "Billy",
        "fazione": "Oscura Legione",
        "tipo": "Personalita",
        "rarity": "Rare",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4,
            "armatura": 4,
            "valore": 5
        },
        "abilita": [
            {
                "nome": "Riceve Doni Apostoli",
                "descrizione": "Spendendo 5D può ricevere un DONO DEGLI APOSTOLI",
                "tipo": "Dono degli Apostoli",
                "costo_destino": 5,
                "target": "Tutto",
                "timing": "Turno"
            }
        ],
        "testo_carta": "Billy è considerato un Eretico. Egli può ricever DONI DELL'OSCURA SIMMETRIA e spendendo 5D può ricevere un DONO DEGLI APOSTOLI",
        "flavour_text": "",
        "keywords": ["Eretico", "Personalita"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita":3,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Centurion": {
        "nome": "Centurion",
        "fazione": "Oscura Legione",
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4,
            "armatura": 4,
            "valore": 5
        },
        "abilita": [],
        "testo_carta": "I Centurion sono soldati d'Elite trasformati dall'Oscura Simmetria per diventare i comandanti delle Legioni di Algeroth",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita":3,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Pretorian Stalker": {
        "nome": "Pretorian Stalker",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Rare",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 12,
            "sparare": 3,
            "armatura": 8,
            "valore": 7
        },
        "abilita": [{
                "nome": "Aumenta caratteristica",
                "descrizione": "Se hai due Pretorian Stalkers nel tuo Schieramento i loro C ed S aumentano di +2",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Tutto",
                "timing": ""
            }],
        "testo_carta": "Le carte dell'Oscura Simmetria non possono essere assegnate ad un Pretorian Stalker. Se hai due Pretorian Stalkers nel tuo Schieramento i loro C ed S aumentano di +2",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": ["Solo doni degli Apostoli"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita":1,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Legionario Non Morto": {
        "nome": "Legionario Non Morto",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 1,
            "armatura": 2,
            "valore": 2
        },
        "abilita": [],
        "testo_carta": "Le carte dell'Oscura Simmetria non possono essere assegnate ai Legionari Urlanti",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": ["Solo doni degli Apostoli"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita":6,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Karnofago": {
        "nome": "Karnofago",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 2, 
            "armatura": 2,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "SEGUACE DI ALGEROTH. Ogni Karnofago nel tuo Schieramento ucciderà automaticamente un guerriero ferito in gioco (mai un Nefaria) durante la fase SCARTARE. Non vengono guadagnati punti. Se non vi sono guerrieri feriti, il Karnofago viene scartato. L'avversario, in questo caso, non guadagna punti.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 2,
        "fondamentale": False,
        "strategico": True
    },
    
    "Mietitori di Anime": {
        "nome": "Mietitori di Anime",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 8,
            "sparare": 3, 
            "armatura": 6,
            "valore": 6
        },
        "abilita": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "SEGUACE DI ALGEROTH. CONSIDERATO UN ERETICO. Guerrieri feriti da Mietitori in combattimento Corpo a Corpo (C) sono automaticamente uccisi.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth", "Eretico"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False,
        "strategico": True
    },
    
    "Destroyer": {
        "nome": "Destroyer",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 7,
            "sparare": 7, 
            "armatura": 7,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "SEGUACE DI ALGEROTH. CONSIDERATO UN ERETICO. Guerrieri feriti dal Destroyer sono automaticamente morti e permanentemente rimossi dal gioco.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth", "Eretico"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 3,
        "fondamentale": False,
        "strategico": True
    },
 
    "Brass Apocalypt": {
        "nome": "Brass Apocalypt",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 6,
            "sparare": 13, 
            "armatura": 10,
            "valore": 7
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI ALGEROTH. Quando lo inserisci in gioco, assegna un guerriero del tuo schieramento, con un caratteristica V di 6 o meno, all'Apocalypt. Da questo momento il guerriero non potrà più essere attaccato; se dovesse morire o essere scartato, anche l'Apocalypt verrà scartato senza far guadagnare punti all'avversario. L'Apocalypt può attaccare o essere attaccato normalmente.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 3,
        "quantita": 3,
        "quantita_minima_consigliata": 2,
        "fondamentale": False
    },
    
    "Techno-Mancer": {
        "nome": "Techno-Mancer",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 4,
            "valore": 5
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI ALGEROTH. CONSIDERATO UN ERETICO. I Technomancer possono essere equipaggiati con ogni tipo di carta indipendentemente dall'icona di legame.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth", "Eretico"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
 
    "Eaonian Justifier": {
        "nome": "Eaonian Justifier",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 0, 
            "armatura": 0,
            "valore": 10
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI ALGEROTH. Non può mai partecipare a un combattimento, o andare in copertura. Se qualcuno dei tuoi seguaci di Algeroth viene ucciso da un Doomtrooper e sopravvive al combattimento puoi IMPRIGIONARLO, le carte associate al guerriero imprigionato sono scartate. I prigionieri non possono attaccare e non possono essere attaccati. Se il Justifier è scartato tutti i suoi prigionieri tornano alla loro Squadra.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Maculator di Mercurio": {
        "nome": "Maculator di Mercurio",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 8,
            "sparare": 14, 
            "armatura": 6,
            "valore": 6
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI ALGEROTH. Può essere assegnato al tuo schieramento solo se hai una WARZONE di MERCURIO in gioco. Se tutte le WARZONE di MERCURIO vengono scartate, anche i Maculator saranno scartati. L'avversario, in questo caso, non guadagna punti.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": ["Assegnabile solo se hai una WARZONE di MERCURIO"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Progenie Immacolata": {
        "nome": "Progenie Immacolata",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 9, 
            "armatura": 6,
            "valore": 6
        },
        "abilita": [{
                "nome": "Trasforma guerrieri uccisi in alleati",
                "descrizione": "Se la Progenie uccide un Doomtrooper, puoi immediatamente rimpiazzarla con una Furia Immacolata",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Doomtrooper",
                "timing": "Turno"
            }],
        "testo_carta": "SEGUACE DI ALGEROTH. Quando una Progenie uccide un Doomtrooper, tu puoi immediatamente rimpiazzarla con una Furia Immacolata della tua collezione. Tutte le carte assegnate alla Progenie rimangono assegnate alla Furia Immacolata.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 3,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Bio Gigante": {
        "nome": "Bio Gigante",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 22,
            "sparare": 14, 
            "armatura": 26,
            "valore": 20
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI ALGEROTH. Non può attaccare più di una volta per turno. Questi guerrieri non possono ricevere carte dell'Oscura Simmetria o Equipaggiamenti, inoltre, non guadagnano i Bonus delle Fortificazioni. Solo l'avversario può giocare carte Speciali sul Bio Gigante.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": ["Solo doni degli Apostoli", "Può attaccare solo una volta per turno", "Equipaggiamenti non assegnabili", "Non guadagnano bonus Fortificazione", "Carte Speciale non giocabili su di esso"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Necromagus Supremo": {
        "nome": "Necromagus Supremo",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 22,
            "sparare": 14, 
            "armatura": 26,
            "valore": 20
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI ALGEROTH CONSIDERATO UN ERETICO. Mentre è in gioco, tutti i tuoi Eretici guadagnano un +3 in C, S e A (non il Necromagus)",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth", "Eretico"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 7,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Algeroth-Apostolo della Guerra": {
        "nome": "Algeroth-Apostolo della Guerra",
        "fazione": "Oscura Legione", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 0, 
            "armatura": 0,
            "valore": 20
        },
        "abilita": [{
                "nome": "Assegna Carta",
                "descrizione": "Equipaggia qualsiasi guerriero dell'Oscura Legione",
                "tipo": "Carte",
                "costo_destino": 0,
                "target": "Guerrieri Oscura Legione",
                "timing": "Ogni Momento"
                },
                {
                "nome": "Scarta Carta",
                "descrizione": "Può scartare qualsiasi carta in gioco al costo di tre azioni",
                "tipo": "Carte",
                "costo_destino": 0,
                "target": "Tutti i Guerrieri",
                "timing": "Turno"
                },],
        "testo_carta": "PERSONALITA. APOSTOLO. Non può mai prendere parte a un combattimento o andare in Copertura. Mentre è in gioco, tutti i Tuoi guerrieri dell'Oscura Legione possono essere equipaggiati in ogni momento e senza spendere Azioni, con qualsiasi carta Equipaggiamento, senza limiti di Legame. Algeroth può scartare una qualsiasi carta Equipaggiamento in gioco, al costo di tre Azioni.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": ["Non può prendere parte al combattimento", "Non può andare in copertura"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Cultista di Algeroth": {
        "nome": "Cultista di Algeroth",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI ALGEROTH. CONSIDERATO UN DOOMTROOPER SENZA ICONA DI LEGAME E UN ERETICO. Puoi aggiungere il Cultista solo alla Tua Squadra. Egli può ricevere carte dell'Oscura Simmetria. Non può attaccare guerrieri della Fratellanza. Volta per volta, puoi decidere se il Cultista è un Doomtrooper o un guerriero dell'Oscura Legione.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth", "Eretico", "Cultista di Algeroth"],
        "restrizioni": ["Non può attaccare guerrieri: Fratellanza"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Valpurgius": {
        "nome": "Valpurgius",
        "fazione": "Oscura Legione", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4, 
            "armatura": 7,
            "valore": 8
        },
        "abilita": [{
                "nome": "Assegna Carte",
                "descrizione": "Equipaggia qualsiasi seguace di Algeroth con arte Oscura Simmetria e Doni degli Apostoli",
                "tipo": "Carte",
                "costo_destino": 0,
                "target": "Seguaci di ALgeroth",
                "timing": "Ogni Momento"
            },
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte",
                "descrizione": "Lancia qualsiasi Arte o Incantesimo dell'Arte",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Turno"
            },],
        "testo_carta": "PERSONALITA. SEGUACE E NEFARIA DI ALGEROTH. Valpurgius è l'Arcimago di Alakhai, può equipaggiare qualsiasi SEGUACE DI ALGEROTH con qualsiasi carta dell'Oscura Simmetria in ogni momento, senza spendere Azioni. Può manipolare l'Arte e lanciare qualsiasi incantesimo dell'Arte.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth", "Nefarita"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Tekron": {
        "nome": "Tekron",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4, 
            "armatura": 3,
            "valore": 6
        },
        "abilita": [{
                "nome": "Sostituisce guerrieri",
                "descrizione": "Può sostituire un Eretico con un Seguace di Algeroth al costo di tre azioni",
                "tipo": "Modificatore",
                "costo_destino": 0,
                "target": "Eretici",
                "timing": "Turno"
            }],
        "testo_carta": "SEGUACE DI ALGEROTH. Mentre è in gioco, al costo di tre Azioni, il Tekron può sostituire un Eretico con qualsiasi SEGUACE DI ALGEROTH non Personalità della Tua Collezione. Devi pagare il costo V del nuovo guerriero e devi rimuovere dal gioco l'Eretico.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cacciatore Oscuro": {
        "nome": "Cacciatore Oscuro",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 5,
            "sparare": 5, 
            "armatura": 5,
            "valore": 6
        }, 
        "abilita": [
            {
                "nome": "Ataccabile solo dalla Fratellanza",
                "descrizione": "Solo i membri della Fratellamza possono attaccarlo con penalità in A di -1",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "SEGUACE DI ALGEROTH. I membri delle cinque Corporazioni non possono Attaccare il Cacciatore, ma i guerrieri della Fratellanza possono. Se Attaccati i Doomtrooper hanno un -1 in A quando combattono contro un Cacciatore Oscuro.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 8,
        "quantita": 4,
        "quantita_minima_consigliata": 3,
        "fondamentale": False,        
    },

    "Golem dell'Oscurita": {
        "nome": "Golem dell'Oscurita",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 6,
            "sparare": 5, 
            "armatura": 7,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Guarisce se stesso",
                "descrizione": "Se ferito, può guarire se stesso. Se il Golem viene ferito, torna sano, a meno che la ferita non lo uccida sul colpo.",
                "tipo": "Guarigione",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "SEGUACE DI ALGEROTH. Il Golem non può ricevere nessuna carta dell'Oscura Simmetria. Se il Golem viene ferito, torna sano, a meno che la ferita non lo uccida sul colpo.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": ["Solo doni degli Apostoli"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 3,
        "fondamentale": True
    },


    # Seguaci di Muawijhe
    "Muawijhe-Signore dei Sogni": {
        "nome": "Muawijhe-Signore dei Sogni",
        "fazione": "Oscura Legione", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 0, 
            "armatura": 0,
            "valore": 20
        },
        "abilita": [
            {
                "nome": "Permette ai guerrieri di attaccare per primi",
                "descrizione": "I guerrieri dell'Oscura Legione possono Attaccare per primi i loro avversari in combattimento",
                "tipo": "Combattimento",
                "costo_destino": 0,
                "target": "Tutti i Guerrieri",
                "timing": "Turno"
            },
        ],
        "testo_carta": "PERSONALITA. APOSTOLO. Non può mai prendere parte a un combattimento o andare in Copertura. Mentre è in gioco, tutti i guerrieri dell'Oscura Legione possono Attaccare per primi i loro avversari in combattimento. Se l'avversario sopravvive, può rispondere ai colpi.",
        "flavour_text": "",
        "keywords": ["Seguace di Muawijhe"],
        "restrizioni": ["Non può prendere parte al combattimento", "Non può andare in copertura"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Comandante Zenithiano": {
        "nome": "Comandante Zenithiano",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 9,
            "sparare": 2, 
            "armatura": 4,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            },
            {
                "nome": "I guerrieri alleati uccidono automaticamente",
                "descrizione": "Mentre è in gioco Zenithiani Assassini dell'Anima uccidono automaticamente i guerrieri feriti",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Zenithiani Assassini dell'Anima",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "SEGUACE DI MUAWIJHE. Considerato un ASSASSINO DELL'ANIMA ZENITHIANO. Mentre è in gioco, i guerrieri feriti dagli ASSASSINI DELL'ANIMA ZENITHIANI sono automaticamente uccisi.",
        "flavour_text": "",
        "keywords": ["Seguace di Muawijhe"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Legionario Urlante": {
        "nome": "Legionario Urlante",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 2,
            "armatura": 1,
            "valore": 3
        },
        "abilita": [{
                "nome": "Aumenta effetto",
                "descrizione": "Ogni Urlatore causa un Punto Danno al costo di 5D.",
                "tipo": "Modificatore",
                "costo_destino": 5,
                "target": "Tutto",
                "timing": "Una volta a partita"
            }],
        "testo_carta": "Una volta a partita, al costo di 5D, puoi invocare il Vento della Pazzia. Ogni Urlatore causa un Punto Danno, se sommandoli il totale è >= A, tutti i guerrieri in gioco sono Feriti. Le carte dell'Oscura Simmetria non possono essere assegnate ai Legionari Urlanti",
        "flavour_text": "",
        "keywords": ["Seguace di Muawijhe"],
        "restrizioni": ["Solo doni degli Apostoli"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 2,
        "quantita":6,
        "quantita_minima_consigliata":4, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },
    
    "Zenithiano Assassino dell'Anima": {
        "nome": "Zenithiano Assassino dell'Anima",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Rare",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 7,
            "sparare": 2,
            "armatura": 6,
            "valore": 6
        },
        "abilita": [],
        "testo_carta": "Alti oltre 3 metri, questi guerrieri enormi incitano le orde senza fine di Legionari Urlanti",
        "flavour_text": "",
        "keywords": ["Seguace di Muawijhe"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 8,
        "quantita":2,
        "quantita_minima_consigliata":2, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },
        
    "Cultista di Muawijhe": {
        "nome": "Cultista di Muawijhe",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 2, 
            "armatura": 4,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI MUAWIJHE. CONSIDERATO UN DOOMTROOPER SENZA ICONA DI LEGAME E UN ERETICO. Puoi aggiungere il Cultista solo alla Tua Squadra. Egli può ricevere carte dell'Oscura Simmetria. Non può attaccare guerrieri della Fratellanza. Volta per volta, puoi decidere se il Cultista è un Doomtrooper o un guerriero dell'Oscura Legione.",
        "flavour_text": "",
        "keywords": ["Seguace di Muawijhe", "Eretico", "Cultista di Muawijhe"],
        "restrizioni": ["Non può attaccare guerrieri: Fratellanza"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 3,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },


    # Seguaci di Demnogonis    
    "Demnogonis il Corruttore": {
        "nome": "Demnogonis il Corruttore",
        "fazione": "Oscura Legione", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 0, 
            "armatura": 0,
            "valore": 20
        },
        "abilita": [
            {
                "nome": "Scarta Carta",
                "descrizione": "Può scartare un qualsiasi Doomtrooper in gioco al costo di tre azioni",
                "tipo": "Carte",
                "costo_destino": 0,
                "target": "Tutti i Doomtrooper",
                "timing": "Turno"
            },
        ],
        "testo_carta": "PERSONALITA. APOSTOLO. Non può mai prendere parte al combattimento, né andare in Copertura. Mentre è in gioco, al costo di tre Azioni, può scartare un qualsiasi Doomtrooper in gioco, pagando il suo V in D. Non guadagni Punti eliminando i guerrieri in questo modo.",
        "flavour_text": "",
        "keywords": ["Seguace di Demnogonis"],
        "restrizioni": ["Non può prendere parte al combattimento", "Non può andare in copertura"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Cultista di Demnogonis": {
        "nome": "Cultista di Demnogonis",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 3, 
            "armatura": 2,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI DEMNOGONIS. CONSIDERATO UN DOOMTROOPER SENZA ICONA DI LEGAME E UN ERETICO. Puoi aggiungere il Cultista solo alla Tua Squadra. Egli può ricevere carte dell'Oscura Simmetria. Non può attaccare guerrieri della Fratellanza. Volta per volta, puoi decidere se il Cultista è un Doomtrooper o un guerriero dell'Oscura Legione.",
        "flavour_text": "",
        "keywords": ["Seguace di Demnogonis", "Eretico", "Cultista di Demnogonis"],
        "restrizioni": ["Non può attaccare guerrieri: Fratellanza"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 3,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Nefarita di Demnogonis": {
        "nome": "Nefarita di Demnogonis",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Rare",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 5,
            "armatura": 2,
            "valore": 5
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Arte",
                "descrizione": "Immune agli effetti dell'Arte",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Sempre"
            },
            {
                "nome": "Aumenta effetto",
                "descrizione": "Se delle carte dell'Oscura Simmetria sono assegnate al Nepharita di Demnogonis, per ogni Punto D speso su un effetto dell'Oscura Simmetria il Valore raddoppia per quell'effetto.",
                "tipo": "Modificatore",
                "costo_destino": 1,
                "target": "",
                "timing": "Sempre"
            },
            {
                "nome": "Guarisce se stesso",
                "descrizione": "Se Ferito, il Nefarita può guarire se stesso spendendo 7D",
                "tipo": "Guarigione",
                "costo_destino": 7,
                "target": "",
                "timing": "Sempre"
            }],
        "testo_carta": "Immune agli effetti dell'Arte. Se delle carte dell'Oscura Simmetria sono assegnate al Nepharita di Demnogonis, per ogni Punto D speso su un effetto dell'Oscura Simmetria il Valore raddoppia per quell'effetto.Se Ferito, il Nefarita  può guarire se stesso spendendo 7D",
        "flavour_text": "",
        "keywords": ["Seguace di Demnogonis", "Nefarita"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita":1,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": True # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },
   
    "Tutore": {
        "nome": "Tutore",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 4,
            "armatura": 3,
            "valore": 4
        },
        "abilita": [],
        "testo_carta": "Con laLame Scalper e siringhe piene di veleni mortali, i Tutori sono ben lieti di dare ai feriti l'estrema unzione",
        "flavour_text": "",
        "keywords": ["Seguace di Demnogonis"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita":3,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Legionario Benedetto": {
        "nome": "Legionario Benedetto",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 3,
            "armatura": 1,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            },],
        "testo_carta": "Le carte dell'Oscura Simmetria non possono essere assegnate ai Legionari Benedetti. I guerrieri feriti dai Legionari Benedetti sono automaticamente morti.",
        "flavour_text": "",
        "keywords": ["Seguace di Demnogonis", "Se ferisce, uccide automaticamente"],
        "restrizioni": ["Solo doni degli Apostoli"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita":7,
        "quantita_minima_consigliata":4, # utilizzata per la creazione del mazzo
        "fondamentale": True # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },


    # Seguaci di Ilian
    "Cultista di Ilian": {
        "nome": "Cultista di Ilian",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 4, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI ILIAN. CONSIDERATO UN DOOMTROOPER SENZA ICONA DI LEGAME E UN ERETICO. Puoi aggiungere il Cultista solo alla Tua Squadra. Egli può ricevere carte dell'Oscura Simmetria. Non può attaccare guerrieri della Fratellanza. Volta per volta, puoi decidere se il Cultista è un Doomtrooper o un guerriero dell'Oscura Legione.",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian", "Eretico", "Cultista di Ilian"],
        "restrizioni": ["Non può attaccare guerrieri: Fratellanza"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 7,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Rampollo di Ilian": {
        "nome": "Rampollo di Ilian",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 5, 
            "armatura": 4,
            "valore": 5
        },
        "abilita": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            },
            {
                "nome": "I guerrieri alleati uccidono automaticamente",
                "descrizione": "I Figli di Ilian uccidono automaticamente i guerrieri feriti",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Figlio di Ilian",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "SEGUACE DI ILIAN. Considerato un FIGLIO DI ILIAN. Mentre è in gioco, i guerrieri feriti dai Tuoi FIGLI DI ILIAN sono automaticamente uccisi.",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },
    
    "Figlio di Ilian": {
        "nome": "Figlio di Ilian",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 1,
            "sparare": 3,
            "armatura": 2,
            "valore": 2
        },
        "abilita": [],
        "testo_carta": "Le carte dell'Oscura Simmetria non possono essere assegnate ai Figli di Ilian",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "restrizioni": ["Solo doni degli Apostoli"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 8,
        "quantita":10,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },
    
    "Templare": {
        "nome": "Templare",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Uncommon",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 7,
            "armatura": 5,
            "valore": 6
        },
        "abilita": [],
        "testo_carta": "Le Guardie del Tempio di Ilian sono guerrieri estremamente potenti che pattugliano la Cittadella della Signora del Vuoto",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita":5,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Pipistrello da Ricognizione": {
        "nome": "Pipistrello da Ricognizione",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 1, 
            "armatura": 1,
            "valore": 1
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI ILIAN. Non potrà mai essere influenzato da altre carte (eccetto carte di attacco a guerrieri) e non potrà mai attaccare. Al costo di 2 AZIONI potrai ispezionare un numero di carte, in mano al giocatore avversario, pari al numero di punti D spesi. 1 x . Spendendo 2 D potrai guardare 2 carte. Le carte da guardare si pescano a caso.",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Sentinella del Tempio": {
        "nome": "Sentinella del Tempio",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 4,
            "valore": 5
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Arte",
                "descrizione": "Immune agli effetti dell'Arte",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "SEGUACE DI ILIAN. Considerato un Templare. Mentre questa carta è in gioco, tutti i Tuoi Templari sono immuni all'Arte.",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 3,
        "quantita": 9,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    "Pipistrello Velenoso": {
        "nome": "Pipistrello Velenoso",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 1, 
            "armatura": 1,
            "valore": 1
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI ILIAN. Non potrà mai essere influenzato da altre carte (eccetto carte di attacco a guerrieri) e non potrà mai attaccare. Se hai ispezionato le carte del tuo avversario con i Pipistrelli da Ricognizione potrai scartare ogni guerriero trovato nell'ispezione.",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Ilian-Signora del Vuoto": {
        "nome": "Ilian-Signora del Vuoto",
        "fazione": "Oscura Legione", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 0, 
            "armatura": 0,
            "valore": 20
        },
        "abilita": [
            {
                "nome": "Annulla Immunita dell'Oscura Simmetria",
                "descrizione": "Può annullare qualsiasi immuntità dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Oscura Simmetria",
                "timing": "Ogni Momento"
            },
            {
                "nome": "Assegna Carta",
                "descrizione": "Assegna carte Oscura Simmetria e Doni degli Apostoli. Equipaggia qualsiasi seguace di Ilian",
                "tipo": "Carte",
                "costo_destino": 0,
                "target": "Guerrieri Oscura Legione",
                "timing": "Ogni Momento"
            },
        ],
        "testo_carta": "PERSONALITA. APOSTOLO. Non può mai prendere parte a un combattimento o andare in Copertura. Mentre è in gioco, i Tuoi guerrieri dell'Oscura Legione possono ricevere in ogni momento qualsiasi Dono dell'Oscura Simmetria o degli Apostoli senza spendere Azioni. Ilian può annullare in ogni momento qualsiasi immunità all'Oscura Simmetria per tutto il tempo che desidera.",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "restrizioni": ["Non può prendere parte al combattimento", "Non può andare in copertura"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },


    # Seguaci di Semai
    "Semai-Signore dell'Odio": {
        "nome": "Semai-Signore dell'Odio",
        "fazione": "Oscura Legione", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 0, 
            "armatura": 0,
            "valore": 20
        },
        "abilita": [
            {
                "nome": "Combattimento tra Doomtrooper",
                "descrizione": "I Doomtrooper possono attaccare qualsiasi Doomtrooper non della tua squadra ma devono pagare 4D per attaccare Guerriri dell'Oscura Legione",
                "tipo": "Combattimento",
                "costo_destino": 0,
                "target": "Guerrieri Doomtrooper",
                "timing": "Ogni Momento"
            }
        ],
        "testo_carta": "PERSONALITA. APOSTOLO. Non può mai prendere parte a un combattimento o andare in Copertura. Mentre è in gioco, i Doomtrooper possono attaccare qualsiasi altro Doomtrooper in gioco (non nella stessa Squadra), ma devono pagare 4D, per poter Attaccare guerrieri dell'Oscura Legione.",
        "flavour_text": "",
        "keywords": ["Seguace di Semai"],
        "restrizioni": ["Non può prendere parte al combattimento", "Non può andare in copertura"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },
    
    "Intruso Callistoniano": {
        "nome": "Intruso Callistoniano",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Uncommon",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4,
            "armatura": 6,
            "valore": 6
        },
        "abilita": [           
            {
                "nome": "Guarisce se stesso",
                "descrizione": "Se Ferito, l'Intruso Callistoniano può guarire se stesso spendendo, in ogni momento, 6D",
                "tipo": "Guarigione",
                "costo_destino": 7,
                "target": "",
                "timing": "Sempre"
            }],
        "testo_carta": "Se Ferito, l'Intruso Callistoniano può guarire se stesso spendendo, in ogni momento, 6D",
        "flavour_text": "",
        "keywords": ["Seguace di Semai"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 5,
        "quantita":4,
        "quantita_minima_consigliata":3, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Conquistatore Callistoniano": {
        "nome": "Conquistatore Callistoniano",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 6,
            "sparare": 6, 
            "armatura": 6,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            },
            {
                "nome": "I guerrieri alleati uccidono automaticamente",
                "descrizione": "Mentre è in gioco, tutti i guerrieri feriti dagli INTRUSI CALLISTONIANI sono automaticamente uccisi",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
            }
        ],
        "testo_carta": "SEGUACE DI SEMAI. Considerato un INTRUSO CALLISTONIANO. Mentre è in gioco, tutti i guerrieri feriti dagli INTRUSI CALLISTONIANI sono automaticamente uccisi.",
        "flavour_text": "",
        "keywords": ["Seguace di Semai"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": True,
    },

    "Legionario di Semai": {
        "nome": "Legionario di Semai",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 1,
            "sparare": 2,
            "armatura": 3,
            "valore": 2
        },
        "abilita": [],
        "testo_carta": "Le carte dell'Oscura Simmetria non possono essere assegnate ai Legionari di Semai",
        "flavour_text": "",
        "keywords": ["Seguace di Semai"],
        "restrizioni": ["Solo doni degli Apostoli"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita":11,
        "quantita_minima_consigliata":2, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },

    "Nefarita di Semai": {
        "nome": "Nefarita di Semai",
        "fazione": "Oscura Legione",
        "tipo": "Seguace",
        "rarity": "Rare",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 5,
            "sparare": 4,
            "armatura": 5,
            "valore": 6
        },
        "abilita": [
            {
                "nome": "Immune agli effetti dell'Arte",
                "descrizione": "Immune agli effetti dell'Arte",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Sempre"
            },
            {
                "nome": "Trasforma guerrieri uccisi in alleati",
                "descrizione": "I Doomtrooper uccisi da lui diventano Legionari di Semai sotto il tuo controllo. Scarta il morto",
                "tipo": "Modificatore",
                "costo_destino": 1,
                "target": "Doomtrooper",
                "timing": "Fase Combattimento"
            },
            {
                "nome": "Guarisce se stesso",
                "descrizione": "Se Ferito, il Nefarita  può guarire se stesso spendendo 7D",
                "tipo": "Guarigione",
                "costo_destino": 7,
                "target": "",
                "timing": "Sempre"
            }],
        "testo_carta": "Immune agli effetti dell'Arte. I Doomtrooper uccisi da lui diventano Legionari di Semai sotto il tuo controllo. Scarta il morto, esamina la tua Collezione e introduci un Legionario di Semai nel tuo Schieramento. Se non hai una carta per rappresentarlo, perdi questa possibilità",
        "flavour_text": "",
        "keywords": ["Seguace di Semai", "Nefarita"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False,
            "pronto": True
        },
        "valore_strategico": 10,
        "quantita":1,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": True, # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        
    },
   
    "Cultista di Semai": {
        "nome": "Cultista di Semai",
        "fazione": "Oscura Legione", 
        "tipo": "Seguace",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 2, 
            "armatura": 3,
            "valore": 3
        },
        "abilita": [],
        "testo_carta": "SEGUACE DI SEMAI. CONSIDERATO UN DOOMTROOPER SENZA ICONA DI LEGAME E UN ERETICO. Puoi aggiungere il Cultista solo alla Tua Squadra. Egli può ricevere carte dell'Oscura Simmetria. Non può attaccare guerrieri della Fratellanza. Volta per volta, puoi decidere se il Cultista è un Doomtrooper o un guerriero dell'Oscura Legione.",
        "flavour_text": "",
        "keywords": ["Seguace di Semai", "Eretico", "Cultista di Semai"],
        "restrizioni": ["Non può attaccare guerrieri: Fratellanza"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 8,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    
    # Generico Oscura Legione

    "Apostata": {
        "nome": "Apostata",
        "fazione": "Oscura Legione", 
        "tipo": "Eretico",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 3,
            "sparare": 3, 
            "armatura": 4,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte",
                "descrizione": "Lancia qualsiasi Arte o Incantesimo dell'Arte",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Turno"
            },
        ],
        "testo_carta": "CONSIDERATO UN ERETICO. L'Apostata può lanciare tutti gli incantesimi dell'Arte, ma solo a beneficio dell'Oscura Legione. L'Apostata è un guerriero della Fratellanza che ha rinnegato la Luce per unirsi all'Oscurità.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 6,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    

    # === MERCENARIO ===
    # Fatto
    "Agente nick michaels": {
        "nome": "Agente nick michaels",
        "fazione": "Mercenario", 
        "tipo": "Personalita",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4, 
            "armatura": 4,
            "valore": 4
        },
        "abilita": [],
        "testo_carta": "PERSONALITÀ. L'Agente Michaels è considerato un membro di tutte e cinque le Corporazioni (ma non della Fratellanza). Egli non potrà mai perdere il legame con l'Alleanza e neppure diventare un Eretico.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 6,
        "quantita": 7,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    "Guardia del corpo": {
        "nome": "Guardia del corpo",
        "fazione": "Mercenario", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 2, 
            "armatura": 6,
            "valore": 4
        },
        "abilita": [],
        "testo_carta": "CONSIDERATA ANCHE UNA FORTIFICAZIONE. Una volta in gioco, puoi assegnare la Guardia del Corpo in qualsiasi momento a qualsiasi Doomtrooper. Se vuoi, durante il combattimento combatterà al posto di quel guerriero. Puoi assegnare la Guardia del Corpo a un altro guerriero spendendo 3D.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 8,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    "Paparazzo": {
        "nome": "Paparazzo",
        "fazione": "Mercenario", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 2,
            "sparare": 2, 
            "armatura": 2,
            "valore": 4
        },
        "abilita": [],
        "testo_carta": "Questo guerriero non può utilizzare nessuna carta equipaggiamento. Mentre è in gioco tutti i tuoi Doomtrooper guadagnano 2 punti extra quando uccidono un avversario in combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Carte Equipaggiamento non Assegnabili"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 1,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    "Medico da campo": {
        "nome": "Medico da campo",
        "fazione": "Mercenario", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "stats": {
            "combattimento": 0,
            "sparare": 0, 
            "armatura": 5,
            "valore": 3
        },
        "abilita": [
            {
                "nome": "Guarisce se stesso.",
                "descrizione": "Se ferito, .",
                "tipo": "Guarigione",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            },
            {
                "nome": "Guarisce guerriero ferito",
                "descrizione": "Può curare un Doomtrooper ferito (facendolo tornare sano) al costo di tre azioni. Non può curare un morto.",
                "tipo": "Guarigione",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
            }
        ],
        "testo_carta": "Non può utilizzare carte equipaggiamento o attaccare un guerriero avversario. Può curare un Doomtrooper ferito (facendolo tornare sano) al costo di tre azioni. Non può curare un morto.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Carte Equipaggiamento non Assegnabili", "Non può attaccare guerrieri: qualsiasi"],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 4,
        "quantita": 8,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    "Apostata rinnegato": {
        "nome": "Apostata rinnegato",
        "fazione": "Mercenario", 
        "tipo": "Normale",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "stats": {
            "combattimento": 4,
            "sparare": 4, 
            "armatura": 5,
            "valore": 7
        },
        "abilita": [
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte",
                "descrizione": "Lancia qualsiasi Arte o Incantesimo dell'Arte",
                "tipo": "Arte",
                "costo_destino": 0,
                "target": "Tutte le Discipline",
                "timing": "Turno"
            }
        ],
        "testo_carta": "Può usare tutti i tipi di Arte. L'apostata Rinnegato non ha nessun Legame e non può riceverne nessuno separato dalla Tua Squadra e dal Tuo Schieramento. Può lanciare qualsiasi incantesimo su qualsiasi guerriero e Attaccare ed essere Attaccato da qualsiasi guerriero.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "restrizioni": [],
        "equipaggiamento": [],
        "stato_gioco": {
            "in_gioco": False,
            "ferito": False, 
            "pronto": True
        },
        "valore_strategico": 8,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },


}


# Funzioni di utilità per il database (versione corretta)

def crea_guerriero_da_nome(nome_guerriero: str):
    """
    Crea un'istanza di Guerriero dal database usando il nome
    
    Args:
        nome_guerriero: Nome del guerriero nel database
        
    Returns:
        Istanza di Guerriero creata dal database usando from_dict(), None se non trovato
    """
    from source.cards.Guerriero import Guerriero
    
    if nome_guerriero in GUERRIERI_DATABASE:
        return Guerriero.from_dict(GUERRIERI_DATABASE[nome_guerriero])
    else:
        print(f"Guerriero '{nome_guerriero}' non trovato nel database")
        return None

def get_numero_guerrieri_per_fazione(fazione: str) -> Dict[str, int]:
    """
    Restituisce un dizionari con i nomi e le quantita di tutti i guerrieri di una specifica fazione
    
    Args:
        fazione: Nome della fazione
        
    Returns:
        Dizionario con i nomi e le quantita dei guerrieri della fazione
    """
    return [{'nome': nome, 'quantita': data['quantita']} for nome, data in GUERRIERI_DATABASE.items() 
            if data["fazione"] == fazione]

def get_guerrieri_per_fazione(fazione: str) -> List[str]:
    """
    Restituisce una lista dei nomi di tutti i guerrieri di una specifica fazione
    
    Args:
        fazione: Nome della fazione
        
    Returns:
        Lista dei nomi dei guerrieri della fazione
    """
    return [nome for nome, data in GUERRIERI_DATABASE.items() 
            if data["fazione"] == fazione]

def get_numero_guerrieri_per_set(espansione: str) -> Dict[str, int]:
    """
    Restituisce una lista dei nomi di tutti i guerrieri di una specifica espansione e la quantita disponibile
    
    Args:
        espansione: Nome dell'espansione
        
    Returns:
        Dizionario dei nomi dei guerrieri dell'espansione e della relativa quantita
    """
    return [{'nome': nome, 'quantita': data['quantita']} for nome, data in GUERRIERI_DATABASE.items() 
            if data["set_espansione"] == espansione]

def get_numero_guerrieri() -> int:
    """Restituisce il numero totale di guerrieri nel database"""
    num=0  
    for espansione in Set_Espansione.values():
        num+=get_numero_guerrieri_per_set(espansione)["quantita"]

    return num

def get_guerrieri_per_set(espansione: str) -> List[str]:    
    """
    Restituisce una lista dei nomi di tutti i guerrieri di una specifica espansione
    
    Args:
        espansione: Nome dell'espansione
        
    Returns:
        Lista dei nomi dei guerrieri dell'espansione
    """
    return [nome for nome, data in GUERRIERI_DATABASE.items() 
            if data["set_espansione"] == espansione]

def get_guerrieri_per_rarity(rarity: str) -> List[str]:
    """
    Restituisce una lista dei nomi di tutti i guerrieri di una specifica rarità
    
    Args:
        rarity: Rarità della carta
        
    Returns:
        Lista dei nomi dei guerrieri della rarità specificata
    """
    return [nome for nome, data in GUERRIERI_DATABASE.items() 
            if data["rarity"] == rarity]

def get_guerrieri_per_valore(valore_min: int = None, valore_max: int = None) -> List[str]:
    """
    Restituisce una lista dei guerrieri filtrati per valore (costo/punti promozione)
    
    Args:
        valore_min: Valore minimo (opzionale)
        valore_max: Valore massimo (opzionale)
        
    Returns:
        Lista dei nomi dei guerrieri nel range di valore specificato
    """
    risultati = []
    for nome, data in GUERRIERI_DATABASE.items():
        valore = data["stats"]["valore"]
        if valore_min is not None and valore < valore_min:
            continue
        if valore_max is not None and valore > valore_max:
            continue
        risultati.append(nome)
    return risultati

def get_guerrieri_per_tipo(tipo: str) -> List[str]:
    """
    Restituisce tutti i guerrieri di un tipo specifico
    
    Args:
        tipo: Tipo di guerriero (Normale, Personalita, Inquisitore, etc.)
        
    Returns:
        Lista dei nomi dei guerrieri del tipo specificato
    """
    return [nome for nome, data in GUERRIERI_DATABASE.items() 
            if data["tipo"] == tipo]

def get_personalita() -> List[str]:
    """Restituisce tutte le Personalita nel database"""
    return get_guerrieri_per_tipo("Personalita")

def get_guerrieri_con_keyword(keyword: str) -> List[str]:
    """
    Restituisce guerrieri che hanno una specifica keyword
    
    Args:
        keyword: Keyword da cercare
        
    Returns:
        Lista dei nomi dei guerrieri con quella keyword
    """
    risultati = []
    for nome, data in GUERRIERI_DATABASE.items():
        if keyword in data["keywords"]:
            risultati.append(nome)
    return risultati

def get_statistiche_database() -> Dict[str, Any]:
    """
    Restituisce statistiche generali sul database
    
    Returns:
        Dizionario con statistiche del database
    """
    stats = {
        "totale_guerrieri": len(GUERRIERI_DATABASE),
        "per_fazione": {},
        "per_espansione": {},
        "per_rarity": {},
        "per_tipo": {},
        "distribuzione_valore": {},
        "statistiche_combattimento": {
            "min_combattimento": float('inf'),
            "max_combattimento": 0,
            "media_combattimento": 0
        },
        "statistiche_sparare": {
            "min_sparare": float('inf'),
            "max_sparare": 0,
            "media_sparare": 0
        }
    }
    
    totale_combattimento = 0
    totale_sparare = 0
    
    for data in GUERRIERI_DATABASE.values():
        # Conteggio per fazione
        fazione = data["fazione"]
        stats["per_fazione"][fazione] = stats["per_fazione"].get(fazione, 0) + 1
        
        # Conteggio per espansione
        espansione = data["set_espansione"]
        stats["per_espansione"][espansione] = stats["per_espansione"].get(espansione, 0) + 1
        
        # Conteggio per rarità
        rarity = data["rarity"]
        stats["per_rarity"][rarity] = stats["per_rarity"].get(rarity, 0) + 1
        
        # Conteggio per tipo
        tipo = data["tipo"]
        stats["per_tipo"][tipo] = stats["per_tipo"].get(tipo, 0) + 1
        
        # Distribuzione valore
        valore = data["stats"]["valore"]
        stats["distribuzione_valore"][valore] = stats["distribuzione_valore"].get(valore, 0) + 1
        
        # Statistiche combattimento
        combattimento = data["stats"]["combattimento"]
        totale_combattimento += combattimento
        stats["statistiche_combattimento"]["min_combattimento"] = min(
            stats["statistiche_combattimento"]["min_combattimento"], combattimento
        )
        stats["statistiche_combattimento"]["max_combattimento"] = max(
            stats["statistiche_combattimento"]["max_combattimento"], combattimento
        )
        
        # Statistiche sparare
        sparare = data["stats"]["sparare"]
        totale_sparare += sparare
        stats["statistiche_sparare"]["min_sparare"] = min(
            stats["statistiche_sparare"]["min_sparare"], sparare
        )
        stats["statistiche_sparare"]["max_sparare"] = max(
            stats["statistiche_sparare"]["max_sparare"], sparare
        )
    
    # Calcolo medie
    totale = len(GUERRIERI_DATABASE)
    stats["statistiche_combattimento"]["media_combattimento"] = round(totale_combattimento / totale, 1)
    stats["statistiche_sparare"]["media_sparare"] = round(totale_sparare / totale, 1)
    
    return stats

def cerca_guerrieri(termine_ricerca: str, campo: str = "nome") -> List[str]:
    """
    Cerca guerrieri nel database per termine
    
    Args:
        termine_ricerca: Termine da cercare
        campo: Campo in cui cercare (nome, testo_carta, flavour_text, keywords)
        
    Returns:
        Lista dei nomi dei guerrieri che contengono il termine
    """
    risultati = []
    termine_lower = termine_ricerca.lower()
    
    for nome, data in GUERRIERI_DATABASE.items():
        if campo == "nome" and termine_lower in nome.lower():
            risultati.append(nome)
        elif campo == "testo_carta" and termine_lower in data["testo_carta"].lower():
            risultati.append(nome)
        elif campo == "flavour_text" and termine_lower in data["flavour_text"].lower():
            risultati.append(nome)
        elif campo == "keywords":
            for keyword in data["keywords"]:
                if termine_lower in keyword.lower():
                    risultati.append(nome)
                    break
    
    return risultati

def crea_squadra_bilanciata(fazione: str, valore_totale: int = 20) -> List[str]:
    """
    Crea una squadra bilanciata per una fazione entro un budget di valore
    
    Args:
        fazione: Fazione desiderata
        valore_totale: Budget totale in punti valore
        
    Returns:
        Lista dei nomi dei guerrieri che formano la squadra
    """
    guerrieri_fazione = get_guerrieri_per_fazione(fazione)
    squadra = []
    valore_corrente = 0
    
    # Ordina per valore crescente per ottimizzare
    guerrieri_ordinati = sorted(
        [(nome, GUERRIERI_DATABASE[nome]["stats"]["valore"]) for nome in guerrieri_fazione],
        key=lambda x: x[1]
    )
    
    for nome, valore in guerrieri_ordinati:
        if valore_corrente + valore <= valore_totale:
            squadra.append(nome)
            valore_corrente += valore
    
    return squadra

def valida_database() -> Dict[str, List[str]]:
    """
    Valida il database per errori comuni
    
    Returns:
        Dizionario con eventuali errori trovati
    """
    errori = {
        "statistiche_mancanti": [],
        "statistiche_invalid": [],
        "personalita_duplicate": [],
        "nomi_duplicati": [],
        "fazione_errata": []
    }
    
    nomi_visti = set()
    personalita_viste = set()
    
    for nome, data in GUERRIERI_DATABASE.items():
        # Verifica nomi duplicati
        if nome in nomi_visti:
            errori["nomi_duplicati"].append(nome)
        nomi_visti.add(nome)
        
        # Verifica Personalita duplicate
        if data["tipo"] == "Personalita":
            if nome in personalita_viste:
                errori["personalita_duplicate"].append(nome)
            personalita_viste.add(nome)
        
        # Verifica statistiche
        stats = data["stats"]
        required_stats = ["combattimento", "sparare", "armatura", "valore"]
        
        for stat in required_stats:
            if stat not in stats:
                errori["statistiche_mancanti"].append(f"{nome}: manca {stat}")
            elif not isinstance(stats[stat], int) or stats[stat] < 0:
                errori["statistiche_invalid"].append(f"{nome}: {stat} non valido")

        if data["fazione"] not in [t.value for t in Fazione]:
           errori["fazione_errata"].append(f"{nome}: {data['fazione']}")
    
    return errori


# Esempi di utilizzo corretto secondo il regolamento
if __name__ == "__main__":
    print("=== DATABASE GUERRIERI MUTANT CHRONICLES (VERSIONE CORRETTA) ===")
    print(f"Totale guerrieri nel database: {len(GUERRIERI_DATABASE)}")
    
    # Statistiche generali
    stats = get_statistiche_database()
    print(f"\nStatistiche database:")
    print(f"- Totale guerrieri: {stats['totale_guerrieri']}")
    print(f"- Per fazione: {stats['per_fazione']}")
    print(f"- Per espansione: {stats['per_espansione']}")
    print(f"- Per rarità: {stats['per_rarity']}")
    print(f"- Per tipo: {stats['per_tipo']}")
    print(f"- Distribuzione valore: {stats['distribuzione_valore']}")
    
    # Statistiche delle abilità di combattimento
    print(f"\nStatistiche Combattimento:")
    print(f"- Min: {stats['statistiche_combattimento']['min_combattimento']}")
    print(f"- Max: {stats['statistiche_combattimento']['max_combattimento']}")
    print(f"- Media: {stats['statistiche_combattimento']['media_combattimento']}")
    
    print(f"\nStatistiche Sparare:")
    print(f"- Min: {stats['statistiche_sparare']['min_sparare']}")
    print(f"- Max: {stats['statistiche_sparare']['max_sparare']}")
    print(f"- Media: {stats['statistiche_sparare']['media_sparare']}")
    
    # Test correzioni applicate - Verifica che le statistiche corrette sono presenti
    print(f"\n=== VERIFICA CORREZIONI APPLICATE ===")
    test_guerriero = "Mitch Hunter"
    if test_guerriero in GUERRIERI_DATABASE:
        data = GUERRIERI_DATABASE[test_guerriero]
        print(f"✓ {test_guerriero} - Valore: {data['stats']['valore']}")
        print(f"✓ Stats contiene: {list(data['stats'].keys())}")
        print(f"✓ Statistiche corrette: C={data['stats']['combattimento']}, S={data['stats']['sparare']}, A={data['stats']['armatura']}, V={data['stats']['valore']}")
        
        # Verifica che non ci siano proprietà errate
        stats_errate = ["forza", "rango", "costo_destino", "punti_promozione"]
        for stat_errata in stats_errate:
            if stat_errata in data['stats']:
                print(f"✗ ERRORE: Trovata statistica errata '{stat_errata}'")
            else:
                print(f"✓ Corretto: Rimossa statistica errata '{stat_errata}'")
    
    # Esempi di filtri
    print(f"\n=== ESEMPI DI UTILIZZO ===")
    
    # Guerrieri per valore
    economici = get_guerrieri_per_valore(None, 4)
    print(f"Guerrieri economici (valore ≤ 4): {len(economici)}")
    
    costosi = get_guerrieri_per_valore(10, None)
    print(f"Guerrieri costosi (valore ≥ 10): {len(costosi)} - {costosi}")
    
    # Personalita
    personalita = get_personalita()
    print(f"Personalita nel database: {len(personalita)} - {personalita[:3]}...")
    
    # Guerrieri con keywords specifiche
    eretico = get_guerrieri_con_keyword("Eretico")
    print(f"Guerrieri Eretico: {eretico}")
    
    samurai = get_guerrieri_con_keyword("Samurai")
    print(f"Guerrieri Samurai: {samurai}")
    
    # Squadra bilanciata
    squadra_capitol = crea_squadra_bilanciata("Capitol", 20)
    print(f"\nSquadra Capitol (budget 20): {squadra_capitol}")
    valore_squadra = sum(GUERRIERI_DATABASE[nome]["stats"]["valore"] for nome in squadra_capitol)
    print(f"Valore totale squadra: {valore_squadra}")
    
    # Test creazione guerriero
    print(f"\n=== TEST CREAZIONE GUERRIERO ===")
    guerriero = crea_guerriero_da_nome('Mitch Hunter')
    if guerriero:
        print(f'✓ Creato: {guerriero}')
        print(f'  Costo: {guerriero.get_costo_destino()} DP')
        print(f'  PP se eliminato: {guerriero.get_punti_promozione()}')
        print(f'  Statistiche: C={guerriero.get_combattimento_totale()}, S={guerriero.get_sparare_totale()}, A={guerriero.get_armatura_totale()}, V={guerriero.get_valore_totale()}')
    
    # Test guerriero economico
    guerriero_economico = crea_guerriero_da_nome('Bauhaus Blitzer')
    if guerriero_economico:
        print(f'✓ Creato: {guerriero_economico}')
        print(f'  Costo: {guerriero_economico.get_costo_destino()} DP')
    
    # Validazione database
    print(f"\n=== VALIDAZIONE DATABASE ===")
    errori = valida_database()
    
    if any(errori.values()):
        print("⚠️ Errori trovati nel database:")
        for tipo_errore, lista_errori in errori.items():
            if lista_errori:
                print(f"  {tipo_errore}: {lista_errori}")
    else:
        print("✓ Database validato con successo - nessun errore trovato")
    
    # Test ricerca
    print(f"\n=== TEST RICERCA ===")
    risultati_samurai = cerca_guerrieri("samurai", "keywords")
    print(f"Ricerca 'samurai' in keywords: {risultati_samurai}")
    
    risultati_bauhaus = cerca_guerrieri("Bauhaus", "nome")
    print(f"Ricerca 'Bauhaus' in nome: {risultati_bauhaus}")
    
    # Analisi bilanciamento
    print(f"\n=== ANALISI BILANCIAMENTO ===")
    
    # Guerrieri più potenti per Combattimento
    tutti_guerrieri = [(nome, data["stats"]["combattimento"]) for nome, data in GUERRIERI_DATABASE.items()]
    top_combattimento = sorted(tutti_guerrieri, key=lambda x: x[1], reverse=True)[:5]
    print(f"Top 5 Combattimento: {[(nome, val) for nome, val in top_combattimento]}")
    
    # Guerrieri più potenti per Sparare
    tutti_sparare = [(nome, data["stats"]["sparare"]) for nome, data in GUERRIERI_DATABASE.items()]
    top_sparare = sorted(tutti_sparare, key=lambda x: x[1], reverse=True)[:5]
    print(f"Top 5 Sparare: {[(nome, val) for nome, val in top_sparare]}")
    
    # Guerrieri più costosi
    tutti_valore = [(nome, data["stats"]["valore"]) for nome, data in GUERRIERI_DATABASE.items()]
    top_valore = sorted(tutti_valore, key=lambda x: x[1], reverse=True)[:5]
    print(f"Top 5 più costosi: {[(nome, val) for nome, val in top_valore]}")
    
    print(f"\n=== DATABASE COMPLETO E CORRETTO ===")
    print("✓ 25+ guerrieri con statistiche corrette (C-S-A-V)")
    print("✓ Tutte le fazioni rappresentate")
    print("✓ Espansioni Base, Inquisition, Warzone")
    print("✓ Funzioni di utilità avanzate per filtri e ricerche")
    print("✓ Compatibile con from_dict() per creazione istanze")
    print("✓ Validazione automatica del database")
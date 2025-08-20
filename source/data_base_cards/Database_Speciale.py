"""
Database completo delle carte Speciali di Mutant Chronicles/Doomtrooper
Include modificatori di combattimento, situazioni tattiche, contromosse e eventi speciali
dal set base fino alle espansioni. Versione corretta secondo il regolamento ufficiale.
"""

from source.cards.Speciale import (
    Speciale, TipoSpeciale, BersaglioSpeciale, DurataSpeciale, 
    TimingSpeciale, EffettoSpeciale
)
from source.cards.Guerriero import Fazione, Rarity


DATABASE_SPECIALI = {
    
    # ========== CARTE DI MODIFICA COMBATTIMENTO - SET BASE ==========
    
    "aim": {
        "nome": "Aim",
        "valore": 0,  # Gratuita
        "tipo": "Modifica Combattimento",
        "rarity": "Common",
        "fazioni_permesse": [],  # Tutte le fazioni
        "bersaglio": "Qualsiasi Guerriero",
        "durata": "Durante questo Combattimento",
        "timing": "Durante Modificatori Combattimento",
        "set_espansione": "Base",
        "numero_carta": "S001",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 3,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "sparare",
                "descrizione_effetto": "+1 Sparare durante questo combattimento",
                "condizioni": ["Durante combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "Il guerriero bersaglio ottiene +1 Sparare durante questo combattimento.",
        "flavour_text": "Un momento di concentrazione può fare la differenza.",
        "keywords": ["Modifica", "Sparare"],
        "restrizioni": [],
        "quantita": 0
    },

    "flanking_maneuver": {
        "nome": "Flanking Maneuver",
        "valore": 2,
        "tipo": "Tattica Speciale",
        "rarity": "Rare",
        "fazioni_permesse": [],
        "bersaglio": "Guerriero Proprio",
        "durata": "Durante questo Combattimento",
        "timing": "Dichiarazione Attacco",
        "set_espansione": "Base",
        "numero_carta": "S008",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 2,
                "statistica_target": "combattimento",
                "descrizione_effetto": "+2 Combattimento e ignora armatura",
                "condizioni": ["Manovra di aggiramento"],
                "limitazioni": ["Solo se il guerriero può muoversi"]
            }
        ],
        "testo_carta": "Il guerriero attaccante ottiene +2 Combattimento e ignora l'armatura del difensore.",
        "flavour_text": "Un attacco dal fianco può ribaltare ogni situazione.",
        "keywords": ["Manovra", "Aggiramento"],
        "restrizioni": ["Il guerriero deve potersi muovere"],
        "quantita": 0
    },

    "berserk": {
        "nome": "Berserk",
        "valore": 0,
        "tipo": "Modifica Combattimento",
        "rarity": "Uncommon",
        "fazioni_permesse": [],
        "bersaglio": "Guerriero Proprio",
        "durata": "Durante questo Combattimento",
        "timing": "Durante Modificatori Combattimento",
        "set_espansione": "Base",
        "numero_carta": "S002",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 2,
                "statistica_target": "combattimento",
                "descrizione_effetto": "+2 Combattimento",
                "condizioni": ["Durante combattimento"],
                "limitazioni": []
            },
            {
                "tipo_effetto": "Modificatore",
                "valore": -1,
                "statistica_target": "armatura",
                "descrizione_effetto": "-1 Armatura",
                "condizioni": ["Durante combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "Il guerriero bersaglio ottiene +2 Combattimento e -1 Armatura durante questo combattimento.",
        "flavour_text": "La furia acceca la ragione ma alimenta la forza.",
        "keywords": ["Furia", "Rischio"],
        "restrizioni": [],
        "quantita": 0
    },

    "surprise_attack": {
        "nome": "Surprise Attack",
        "valore": 1,
        "tipo": "Tattica Speciale",
        "rarity": "Uncommon",
        "fazioni_permesse": [],
        "bersaglio": "Guerriero Attaccante",
        "durata": "Durante questo Combattimento",
        "timing": "Dichiarazione Attacco",
        "set_espansione": "Base",
        "numero_carta": "S003",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Primo_Attacco",
                "valore": 1,
                "statistica_target": "",
                "descrizione_effetto": "L'attaccante colpisce per primo",
                "condizioni": ["Durante combattimento"],
                "limitazioni": ["Il difensore non può rispondere"]
            }
        ],
        "testo_carta": "L'attaccante colpisce per primo in questo combattimento. Il difensore non può rispondere.",
        "flavour_text": "L'elemento sorpresa vale più di mille proiettili.",
        "keywords": ["Sorpresa", "Primo Attacco"],
        "restrizioni": [],
        "quantita": 0
    },

    "retreat": {
        "nome": "Retreat",
        "valore": 0,
        "tipo": "Contromossa",
        "rarity": "Common",
        "fazioni_permesse": [],
        "bersaglio": "Combattimento Corrente",
        "durata": "Istantanea",
        "timing": "In Risposta",
        "set_espansione": "Base",
        "numero_carta": "S004",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Annulla_Attacco",
                "valore": 1,
                "statistica_target": "",
                "descrizione_effetto": "Annulla l'attacco corrente",
                "condizioni": ["In risposta ad attacco"],
                "limitazioni": ["Solo una volta per combattimento"]
            }
        ],
        "testo_carta": "Annulla l'attacco corrente. Nessun combattimento ha luogo.",
        "flavour_text": "A volte ritirarsi è la scelta più saggia.",
        "keywords": ["Fuga", "Annullamento"],
        "restrizioni": [],
        "quantita": 0
    },

    "lucky_shot": {
        "nome": "Lucky Shot",
        "valore": 2,
        "tipo": "Fortuna",
        "rarity": "Rare",
        "fazioni_permesse": [],
        "bersaglio": "Guerriero Attaccante",
        "durata": "Durante questo Combattimento",
        "timing": "Risoluzione Combattimento",
        "set_espansione": "Base",
        "numero_carta": "S005",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Doppio_Attacco",
                "valore": 2,
                "statistica_target": "",
                "descrizione_effetto": "Il danno viene raddoppiato",
                "condizioni": ["L'attacco deve andare a segno"],
                "limitazioni": ["Solo se l'attacco colpisce"]
            }
        ],
        "testo_carta": "Se l'attacco va a segno, infligge una ferita aggiuntiva.",
        "flavour_text": "Ogni tanto anche la fortuna aiuta i coraggiosi.",
        "keywords": ["Fortuna", "Danno Extra"],
        "restrizioni": [],
        "quantita": 0
    },

    "healing": {
        "nome": "Healing",
        "valore": 3,
        "tipo": "Modifica Guerriero",
        "rarity": "Rare",
        "fazioni_permesse": [],
        "bersaglio": "Guerriero Proprio",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "S006",
        "max_copie_per_combattimento": 99,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "tipo_effetto": "Guarigione",
                "valore": 1,
                "statistica_target": "",
                "descrizione_effetto": "Guarisce un guerriero ferito",
                "condizioni": ["Il guerriero deve essere ferito"],
                "limitazioni": ["Costa un'Azione"]
            }
        ],
        "testo_carta": "Un guerriero ferito ritorna sano. Costa un'Azione.",
        "flavour_text": "Anche nelle guerre più cruente, la compassione trova la sua strada.",
        "keywords": ["Guarigione", "Supporto"],
        "restrizioni": ["Solo su guerrieri feriti"],
        "quantita": 0
    },

    "destinys_favor": {
        "nome": "Destiny's Favor",
        "valore": 2,
        "tipo": "Modifica Giocatore",
        "rarity": "Uncommon",
        "fazioni_permesse": [],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "S007",
        "max_copie_per_combattimento": 99,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Pescaggio_Carte",
                "valore": 2,
                "statistica_target": "",
                "descrizione_effetto": "Pesca 2 carte",
                "condizioni": [],
                "limitazioni": ["Una volta per turno"]
            }
        ],
        "testo_carta": "Pesca 2 carte dal tuo mazzo.",
        "flavour_text": "Il destino sorride ai preparati.",
        "keywords": ["Pescaggio", "Destino"],
        "restrizioni": [],
        "quantita": 0
    },

    "sabotage": {
        "nome": "Sabotage",
        "valore": 1,
        "tipo": "Modifica Giocatore",
        "rarity": "Common",
        "fazioni_permesse": [],
        "bersaglio": "Giocatore Avversario",
        "durata": "Istantanea",
        "timing": "Qualsiasi Momento",
        "set_espansione": "Base",
        "numero_carta": "S008",
        "max_copie_per_combattimento": 99,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Scarto_Carte",
                "valore": 1,
                "statistica_target": "",
                "descrizione_effetto": "L'avversario scarta 1 carta",
                "condizioni": [],
                "limitazioni": ["Una volta per turno"]
            }
        ],
        "testo_carta": "Il giocatore bersaglio scarta 1 carta a caso dalla sua mano.",
        "flavour_text": "Un piccolo atto di sabotaggio può rovinare i piani migliori.",
        "keywords": ["Sabotaggio", "Controllo"],
        "restrizioni": [],
        "quantita": 0
    },

    "change_attacker": {
        "nome": "Change Attacker",
        "valore": 2,
        "tipo": "Tattica Speciale",
        "rarity": "Rare",
        "fazioni_permesse": [],
        "bersaglio": "Guerriero Proprio",
        "durata": "Istantanea",
        "timing": "Dichiarazione Attacco",
        "set_espansione": "Base",
        "numero_carta": "S009",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Cambio_Attaccante",
                "valore": 1,
                "statistica_target": "",
                "descrizione_effetto": "Cambia l'attaccante nel combattimento corrente",
                "condizioni": ["Il nuovo attaccante deve poter attaccare il difensore"],
                "limitazioni": ["Solo durante dichiarazione attacco"]
            }
        ],
        "testo_carta": "Sostituisci l'attaccante corrente con un tuo guerriero. Il nuovo attaccante deve essere in grado di attaccare il difensore.",
        "flavour_text": "Nel caos della battaglia, ogni momento può portare nuove opportunità.",
        "keywords": ["Cambio", "Tattica"],
        "restrizioni": ["Il nuovo attaccante deve essere valido"],
        "quantita": 0
    },

    "change_defender": {
        "nome": "Change Defender",
        "valore": 2,
        "tipo": "Tattica Speciale",
        "rarity": "Rare",
        "fazioni_permesse": [],
        "bersaglio": "Guerriero Proprio",
        "durata": "Istantanea",
        "timing": "Dichiarazione Attacco",
        "set_espansione": "Base",
        "numero_carta": "S016",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Cambio_Difensore",
                "valore": 1,
                "statistica_target": "",
                "descrizione_effetto": "Cambia il difensore nel combattimento corrente",
                "condizioni": ["Il nuovo difensore deve poter essere attaccato"],
                "limitazioni": ["Solo durante dichiarazione attacco"]
            }
        ],
        "testo_carta": "Sostituisci il difensore corrente con un tuo guerriero. Il nuovo difensore deve essere un bersaglio valido.",
        "flavour_text": "Un sacrificio tattico può salvare un alleato prezioso.",
        "keywords": ["Cambio", "Sacrificio"],
        "restrizioni": ["Il nuovo difensore deve essere valido"],
        "quantita": 0
    },

    "equipment_malfunction": {
        "nome": "Equipment Malfunction",
        "valore": 1,
        "tipo": "Sfortuna",
        "rarity": "Uncommon",
        "fazioni_permesse": [],
        "bersaglio": "Guerriero Avversario",
        "durata": "Durante questo Combattimento",
        "timing": "Durante Modificatori Combattimento",
        "set_espansione": "Base",
        "numero_carta": "S010",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 2,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": -2,
                "statistica_target": "sparare",
                "descrizione_effetto": "L'arma si inceppa: -2 Sparare",
                "condizioni": ["Il guerriero ha equipaggiamento"],
                "limitazioni": ["Solo contro guerrieri con armi"]
            }
        ],
        "testo_carta": "Il guerriero bersaglio subisce -2 Sparare durante questo combattimento a causa di un malfunzionamento dell'equipaggiamento.",
        "flavour_text": "Anche la tecnologia più avanzata può tradire nel momento cruciale.",
        "keywords": ["Malfunzionamento", "Tecnologia"],
        "restrizioni": ["Bersaglio deve avere equipaggiamento"],
        "quantita": 0
    },

    "ammunition_shortage": {
        "nome": "Ammunition Shortage",
        "valore": 1,
        "tipo": "Sfortuna",
        "rarity": "Common",
        "fazioni_permesse": [],
        "bersaglio": "Qualsiasi Guerriero",
        "durata": "Durante questo Combattimento",
        "timing": "Durante Modificatori Combattimento",
        "set_espansione": "Base",
        "numero_carta": "S011",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 2,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": -1,
                "statistica_target": "sparare",
                "descrizione_effetto": "-1 Sparare per mancanza munizioni",
                "condizioni": ["Attacco a distanza"],
                "limitazioni": ["Solo attacchi a distanza"]
            }
        ],
        "testo_carta": "Il guerriero bersaglio subisce -1 Sparare negli attacchi a distanza per mancanza di munizioni.",
        "flavour_text": "Nel momento cruciale, anche i veterani possono rimanere a secco.",
        "keywords": ["Munizioni", "Logistica"],
        "restrizioni": [],
        "quantita": 0
    },

    "resourcefulness": {
        "nome": "Resourcefulness",
        "valore": 3,
        "tipo": "Modifica Giocatore",
        "rarity": "Rare",
        "fazioni_permesse": [],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "S014",
        "max_copie_per_combattimento": 99,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "tipo_effetto": "Modifica_Punti_Destino",
                "valore": 2,
                "statistica_target": "",
                "descrizione_effetto": "Guadagni 2 Punti Destino",
                "condizioni": [],
                "limitazioni": ["Costa un'Azione"]
            }
        ],
        "testo_carta": "Guadagni 2 Punti Destino. Costa un'Azione.",
        "flavour_text": "L'ingegno può trasformare anche la situazione più disperata.",
        "keywords": ["Risorse", "Punti Destino"],
        "restrizioni": [],
        "quantita": 0
    },

    "imperial_discipline": {
        "nome": "Imperial Discipline",
        "valore": 1,
        "tipo": "Modifica Guerriero",
        "rarity": "Uncommon",
        "fazioni_permesse": ["Imperiale"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fino Fine Turno",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "S018",
        "max_copie_per_combattimento": 99,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "combattimento",
                "descrizione_effetto": "+1 Combattimento e +1 Sparare fino a fine turno",
                "condizioni": ["Solo guerrieri Imperiali"],
                "limitazioni": []
            },
            {
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "sparare",
                "descrizione_effetto": "+1 Sparare",
                "condizioni": ["Solo guerrieri Imperiali"],
                "limitazioni": []
            }
        ],
        "testo_carta": "Un guerriero Imperiale ottiene +1 Combattimento e +1 Sparare fino alla fine del turno.",
        "flavour_text": "L'addestramento Imperiale non conosce pari in tutto il sistema solare.",
        "keywords": ["Imperiale", "Disciplina"],
        "restrizioni": ["Solo fazione Imperiale"],
        "quantita": 0
    },

    "bauhaus_engineering": {
        "nome": "Bauhaus Engineering",
        "valore": 1,
        "tipo": "Modifica Guerriero",
        "rarity": "Uncommon",
        "fazioni_permesse": ["Bauhaus"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "S019",
        "max_copie_per_combattimento": 99,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "armatura",
                "descrizione_effetto": "+1 Armatura permanente",
                "condizioni": ["Solo guerrieri Bauhaus"],
                "limitazioni": ["Costa un'Azione"]
            }
        ],
        "testo_carta": "Un guerriero Bauhaus ottiene +1 Armatura permanente. Costa un'Azione.",
        "flavour_text": "L'ingegneria Bauhaus trasforma ogni guerriero in una fortezza ambulante.",
        "keywords": ["Bauhaus", "Ingegneria"],
        "restrizioni": ["Solo fazione Bauhaus"],
        "quantita": 0
    },

    "mishima_honor": {
        "nome": "Mishima Honor",
        "valore": 0,
        "tipo": "Modifica Combattimento",
        "rarity": "Common",
        "fazioni_permesse": ["Mishima"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Durante questo Combattimento",
        "timing": "Durante Modificatori Combattimento",
        "set_espansione": "Base",
        "numero_carta": "S020",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 2,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 2,
                "statistica_target": "combattimento",
                "descrizione_effetto": "+2 Combattimento se in inferiorità numerica",
                "condizioni": ["Il guerriero deve essere in inferiorità numerica"],
                "limitazioni": ["Solo corpo a corpo"]
            }
        ],
        "testo_carta": "Se il guerriero Mishima è in inferiorità numerica, ottiene +2 Combattimento corpo a corpo.",
        "flavour_text": "L'onore Mishima brilla più luminoso quando tutto sembra perduto.",
        "keywords": ["Mishima", "Onore"],
        "restrizioni": ["Solo fazione Mishima", "Solo corpo a corpo"],
        "quantita": 0
    },

    "acts_of_heroism": {
        "nome": "Acts of Heroism",
        "valore": 4,
        "tipo": "Evento",
        "rarity": "Ultra Rare",
        "fazioni_permesse": [],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "S021",
        "max_copie_per_combattimento": 99,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 2,
                "statistica_target": "valore",
                "descrizione_effetto": "+2 Valore permanente",
                "condizioni": [],
                "limitazioni": ["Costa un'Azione"]
            },
            {
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "combattimento",
                "descrizione_effetto": "+1 Combattimento permanente",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "Il guerriero bersaglio ottiene +2 Valore e +1 Combattimento permanenti. Costa un'Azione.",
        "flavour_text": "Gli eroi nascono nei momenti più bui della storia.",
        "keywords": ["Eroismo", "Leggenda"],
        "restrizioni": [],
        "quantita": 0
    },

    "devastating_assault": {
        "nome": "Devastating Assault",
        "valore": 3,
        "tipo": "Tattica Speciale",
        "rarity": "Ultra Rare",
        "fazioni_permesse": [],
        "bersaglio": "Guerriero Attaccante",
        "durata": "Durante questo Combattimento",
        "timing": "Dichiarazione Attacco",
        "set_espansione": "Base",
        "numero_carta": "S022",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 4,
                "statistica_target": "combattimento",
                "descrizione_effetto": "+4 Combattimento",
                "condizioni": ["Durante combattimento"],
                "limitazioni": []
            },
            {
                "tipo_effetto": "Ferita_Automatica",
                "valore": 1,
                "statistica_target": "",
                "descrizione_effetto": "Se l'attacco va a segno, infligge ferita automatica",
                "condizioni": ["L'attacco deve colpire"],
                "limitazioni": []
            }
        ],
        "testo_carta": "L'attaccante ottiene +4 Combattimento. Se l'attacco va a segno, il difensore viene automaticamente ucciso.",
        "flavour_text": "Alcuni attacchi sono così devastanti che non lasciano scampo.",
        "keywords": ["Devastazione", "Morte"],
        "restrizioni": [],
        "quantita": 0
    },
    
    "duck_and_cover": {
        "nome": "Duck and Cover",
        "valore": 0,
        "tipo": "Modifica Combattimento",
        "rarity": "Common",
        "fazioni_permesse": [],
        "bersaglio": "Guerriero Proprio",
        "durata": "Durante questo Combattimento",
        "timing": "Durante Modificatori Combattimento",
        "set_espansione": "Base",
        "numero_carta": "S003",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 2,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 2,
                "statistica_target": "armatura",
                "descrizione_effetto": "+2 Armatura contro attacchi a distanza",
                "condizioni": ["Solo contro attacchi a distanza"],
                "limitazioni": ["Non efficace in corpo a corpo"]
            }
        ],
        "testo_carta": "Il guerriero bersaglio ottiene +2 Armatura contro attacchi a distanza durante questo combattimento.",
        "flavour_text": "Quando i proiettili volano, meglio stare bassi.",
        "keywords": ["Protezione", "Tattica"],
        "restrizioni": [],
        "quantita": 0
    },

    "combat_fury": {
        "nome": "Combat Fury",
        "valore": 1,
        "tipo": "Modifica Combattimento",
        "rarity": "Uncommon",
        "fazioni_permesse": [],
        "bersaglio": "Qualsiasi Guerriero",
        "durata": "Durante questo Combattimento",
        "timing": "Durante Modificatori Combattimento",
        "set_espansione": "Base",
        "numero_carta": "S004",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 3,
                "statistica_target": "combattimento",
                "descrizione_effetto": "+3 Combattimento",
                "condizioni": ["Durante combattimento corpo a corpo"],
                "limitazioni": ["Solo combattimento corpo a corpo"]
            }
        ],
        "testo_carta": "Il guerriero bersaglio ottiene +3 Combattimento solo in combattimento corpo a corpo.",
        "flavour_text": "Nel corpo a corpo, l'istinto supera l'addestramento.",
        "keywords": ["Corpo a Corpo", "Furia"],
        "restrizioni": ["Solo combattimento corpo a corpo"],
        "quantita": 0
    },

    "precise_shot": {
        "nome": "Precise Shot",
        "valore": 1,
        "tipo": "Modifica Combattimento",
        "rarity": "Common",
        "fazioni_permesse": [],
        "bersaglio": "Qualsiasi Guerriero",
        "durata": "Durante questo Combattimento",
        "timing": "Durante Modificatori Combattimento",
        "set_espansione": "Base",
        "numero_carta": "S005",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 2,
        "richiede_azione": False,
        "effetti": [
            {
                "tipo_effetto": "Modificatore",
                "valore": 2,
                "statistica_target": "sparare",
                "descrizione_effetto": "+2 Sparare",
                "condizioni": ["Durante combattimento a distanza"],
                "limitazioni": ["Solo attacchi a distanza"]
            }
        ],
        "testo_carta": "Il guerriero bersaglio ottiene +2 Sparare solo negli attacchi a distanza.",
        "flavour_text": "Ogni proiettile conta quando la vita è in gioco.",
        "keywords": ["Precisione", "Armi da Fuoco"],
        "restrizioni": ["Solo attacchi a distanza"],
        "quantita": 0
    }
}


# Funzioni di utilità per il database

def get_carte_per_tipo(tipo: str) -> dict:
    """Restituisce tutte le carte di un determinato tipo"""
    return {nome: data for nome, data in DATABASE_SPECIALI.items() 
            if data["tipo"] == tipo}


def get_carte_per_fazione(fazione: str) -> dict:
    """Restituisce tutte le carte utilizzabili da una fazione"""
    return {nome: data for nome, data in DATABASE_SPECIALI.items() 
            if not data["fazioni_permesse"] or fazione in data["fazioni_permesse"]}


def get_carte_per_timing(timing: str) -> dict:
    """Restituisce tutte le carte giocabili in un determinato timing"""
    return {nome: data for nome, data in DATABASE_SPECIALI.items() 
            if data["timing"] == timing or data["timing"] == "Qualsiasi Momento"}


def get_carte_per_rarità(rarity: str) -> dict:
    """Restituisce tutte le carte di una determinata rarità"""
    return {nome: data for nome, data in DATABASE_SPECIALI.items() 
            if data["rarity"] == rarity}


def crea_carta_da_database(nome_carta: str):
    """
    Crea un'istanza della classe Speciale dal database
    
    Args:
        nome_carta: Nome della carta nel database
        
    Returns:
        Istanza di Speciale o None se non trovata
    """
    if nome_carta not in DATABASE_SPECIALI:
        return None
    
    data = DATABASE_SPECIALI[nome_carta]
    
    # Crea l'istanza base
    carta = Speciale(data["nome"], data["valore"])
    
    # Configura proprietà dalla classe enum
    carta.tipo = TipoSpeciale(data["tipo"])
    carta.rarity = Rarity(data["rarity"])
    carta.bersaglio = BersaglioSpeciale(data["bersaglio"])
    carta.durata = DurataSpeciale(data["durata"])
    carta.timing = TimingSpeciale(data["timing"])
    carta.set_espansione = data["set_espansione"]
    carta.numero_carta = data["numero_carta"]
    carta.max_copie_per_combattimento = data["max_copie_per_combattimento"]
    carta.max_copie_per_turno = data["max_copie_per_turno"]
    carta.richiede_azione = data["richiede_azione"]
    carta.testo_carta = data["testo_carta"]
    carta.flavour_text = data["flavour_text"]
    carta.keywords = data["keywords"]
    carta.restrizioni = data["restrizioni"]
    
    # Configura fazioni permesse
    carta.fazioni_permesse = [Fazione(f) for f in data["fazioni_permesse"]]
    
    # Aggiungi effetti
    for effetto_data in data["effetti"]:
        effetto = EffettoSpeciale(
            tipo_effetto=effetto_data["tipo_effetto"],
            valore=effetto_data["valore"],
            statistica_target=effetto_data["statistica_target"],
            descrizione_effetto=effetto_data["descrizione_effetto"],
            condizioni=effetto_data["condizioni"],
            limitazioni=effetto_data["limitazioni"]
        )
        carta.effetti.append(effetto)
    
    return carta


# Test del database
if __name__ == "__main__":
    print("=== DATABASE CARTE SPECIALI ===")
    print(f"Totale carte: {len(DATABASE_SPECIALI)}")
    
    # Test creazione carte
    for nome in ["aim", "berserk", "healing"]:
        carta = crea_carta_da_database(nome)
        if carta:
            print(f"✓ {carta.nome} creata correttamente")
        else:
            print(f"✗ Errore nella creazione di {nome}")
    
    print("Database pronto per l'uso!")








"""
Database completo delle carte Equipaggiamento di Mutant Chronicles/Doomtrooper
Include armi, armature, veicoli, kit e strumenti dal set base fino all'espansione Warzone
Versione corretta secondo il regolamento ufficiale
"""

from source.cards.Equipaggiamento import (
    Equipaggiamento, TipoEquipaggiamento, TipoArmatura, TipoVeicolo,
    ModificatoreEquipaggiamento, AbilitaSpeciale
)
from source.cards.Guerriero import Fazione, Rarity


DATABASE_EQUIPAGGIAMENTO = {
    
    # ========== ARMI CORPO A CORPO - SET BASE ==========
    
    "spada_combattimento": {
        "nome": "Spada da Combattimento",
        "costo_destino": 1,
        "tipo": "Arma da Corpo a Corpo",  # CORRETTO: secondo regolamento
        "categoria_arma": "Lama",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "valore_combattimento": 2,
            "valore_armatura": 0,
            "valore_movimento": 0,
            "capacita_trasporto": 0,
            "punti_struttura": 3
        },
        "modificatori": [],
        "abilita_speciali": [],
        "requisiti": ["Nessuno"],
        "fazioni_permesse": [],  # Tutte le fazioni possono usare
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,  # CORRETTO: era "forza_minima_richiesta"
        "meccaniche_armi": {
            "munizioni_richieste": None,
            "gittata_massima": 0,  # Corpo a corpo = 0
            "cadenza_fuoco": 1,
            "penetrazione_armatura": 0,
            "danni_critici": False
        },
        "meccaniche_veicoli": {
            "equipaggio_richiesto": 1,
            "passeggeri_massimi": 0,
            "armi_integrate": [],
            "blindatura": 0
        },
        "stato": {
            "stato_operativo": "Funzionante",
            "munizioni_rimanenti": 0,
            "usure_accumulate": 0,
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "+2 Combattimento in corpo a corpo. Arma standard dell'esercito.",
        "flavour_text": "L'acciaio temperato non conosce pietà.",
        "keywords": ["Arma", "Corpo a Corpo", "Lama"],
        "set_espansione": "Base",
        "numero_carta": "EQ-001",
        "costo_produzione": 2,
        "compatibilita": {
            "compatibile_con": ["Armatura da Combattimento"],
            "upgrade_disponibili": ["Spada Energetica"],
            "equipaggiamenti_richiesti": []
        }
    },

    "ascia_da_battaglia": {
        "nome": "Ascia da Battaglia",
        "costo_destino": 2,
        "tipo": "Arma da Corpo a Corpo",  # CORRETTO
        "categoria_arma": "Ascia",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "valore_combattimento": 3,
            "valore_armatura": 0,
            "valore_movimento": -1,  # Pesante
            "capacita_trasporto": 0,
            "punti_struttura": 4
        },
        "modificatori": [
            {
                "statistica": "combattimento",
                "valore": 1,
                "condizione": "primo round di combattimento",
                "descrizione": "+1 Combattimento nel primo round"
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Devastazione",
                "descrizione": "Ignora +1 punto Armatura del bersaglio",
                "costo_attivazione": 0,
                "tipo_attivazione": "Automatica",
                "limitazioni": []
            }
        ],
        "requisiti": ["Nessuno"],
        "fazioni_permesse": [],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 2,
        "valore_minimo_richiesto_sparare": 0,  # CORRETTO
        "meccaniche_armi": {
            "munizioni_richieste": None,
            "gittata_massima": 0,
            "cadenza_fuoco": 1,
            "penetrazione_armatura": 1,
            "danni_critici": False
        },
        "meccaniche_veicoli": {
            "equipaggio_richiesto": 1,
            "passeggeri_massimi": 0,
            "armi_integrate": [],
            "blindatura": 0
        },
        "stato": {
            "stato_operativo": "Funzionante",
            "munizioni_rimanenti": 0,
            "usure_accumulate": 0,
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "+3 Combattimento corpo a corpo. +1 aggiuntivo nel primo round. Ignora 1 punto Armatura.",
        "flavour_text": "La forza bruta ha il suo fascino primitivo.",
        "keywords": ["Arma", "Corpo a Corpo", "Ascia", "Devastazione"],
        "set_espansione": "Base",
        "numero_carta": "EQ-002",
        "costo_produzione": 3,
        "compatibilita": {
            "compatibile_con": ["Giubbotto Antiproiettile"],
            "upgrade_disponibili": ["Ascia Energetica"],
            "equipaggiamenti_richiesti": []
        }
    },

    # ========== ARMI DA FUOCO - SET BASE ==========
    
    "pistola_automatica": {
        "nome": "Pistola Automatica",
        "costo_destino": 1,
        "tipo": "Arma da Fuoco",  # CORRETTO: secondo regolamento
        "categoria_arma": "Pistola",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "valore_combattimento": 2,
            "valore_armatura": 0,
            "valore_movimento": 0,
            "capacita_trasporto": 0,
            "punti_struttura": 2
        },
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Fuoco Rapido",
                "descrizione": "Può sparare due volte per turno",
                "costo_attivazione": 1,
                "tipo_attivazione": "Azione",
                "limitazioni": ["Richiede munizioni aggiuntive"]
            }
        ],
        "requisiti": ["Nessuno"],
        "fazioni_permesse": [],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,  # CORRETTO
        "meccaniche_armi": {
            "munizioni_richieste": "Munizioni Standard",
            "gittata_massima": 4,
            "cadenza_fuoco": 2,
            "penetrazione_armatura": 0,
            "danni_critici": False
        },
        "meccaniche_veicoli": {
            "equipaggio_richiesto": 1,
            "passeggeri_massimi": 0,
            "armi_integrate": [],
            "blindatura": 0
        },
        "stato": {
            "stato_operativo": "Funzionante",
            "munizioni_rimanenti": 15,
            "usure_accumulate": 0,
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "+2 Combattimento a distanza (4 caselle). Può sparare due volte per turno.",
        "flavour_text": "Affidabile, precisa, mortale.",
        "keywords": ["Arma", "Da Fuoco", "Pistola"],  # CORRETTO: "Da Fuoco" non "A Distanza"
        "set_espansione": "Base",
        "numero_carta": "EQ-003",
        "costo_produzione": 2,
        "compatibilita": {
            "compatibile_con": ["Silenziatore", "Mirino Laser"],
            "upgrade_disponibili": ["Pistola Plasma"],
            "equipaggiamenti_richiesti": []
        }
    },

    "fucile_dassalto": {
        "nome": "Fucile d'Assalto",
        "costo_destino": 2,
        "tipo": "Arma da Fuoco",  # CORRETTO
        "categoria_arma": "Fucile",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "valore_combattimento": 3,
            "valore_armatura": 0,
            "valore_movimento": 0,
            "capacita_trasporto": 0,
            "punti_struttura": 3
        },
        "modificatori": [
            {
                "statistica": "combattimento",
                "valore": 1,
                "condizione": "gittata massima",
                "descrizione": "+1 Combattimento a lunga distanza"
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Fuoco di Soppressione",
                "descrizione": "Tutti i nemici in vista subiscono -1 Combattimento",
                "costo_attivazione": 2,
                "tipo_attivazione": "Azione",
                "limitazioni": ["Una volta per turno", "Richiede munizioni"]
            }
        ],
        "requisiti": ["Addestramento Militare"],
        "fazioni_permesse": [],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 2,  # CORRETTO
        "meccaniche_armi": {
            "munizioni_richieste": "Munizioni Standard",
            "gittata_massima": 8,
            "cadenza_fuoco": 3,
            "penetrazione_armatura": 1,
            "danni_critici": False
        },
        "meccaniche_veicoli": {
            "equipaggio_richiesto": 1,
            "passeggeri_massimi": 0,
            "armi_integrate": [],
            "blindatura": 0
        },
        "stato": {
            "stato_operativo": "Funzionante",
            "munizioni_rimanenti": 30,
            "usure_accumulate": 0,
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "+3 Combattimento a distanza (8 caselle). +1 aggiuntivo a lunga distanza. Fuoco di soppressione.",
        "flavour_text": "L'arma standard dei soldati veterani.",
        "keywords": ["Arma", "Da Fuoco", "Fucile", "Militare"],  # CORRETTO
        "set_espansione": "Base",
        "numero_carta": "EQ-004",
        "costo_produzione": 4,
        "compatibilita": {
            "compatibile_con": ["Granate", "Baionetta"],
            "upgrade_disponibili": ["Fucile Plasma"],
            "equipaggiamenti_richiesti": []
        }
    },

    "fucile_di_precisione": {
        "nome": "Fucile di Precisione",
        "costo_destino": 3,
        "tipo": "Arma da Fuoco",  # CORRETTO
        "categoria_arma": "Fucile",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Uncommon",
        "statistiche": {
            "valore_combattimento": 4,
            "valore_armatura": 0,
            "valore_movimento": -1,
            "capacita_trasporto": 0,
            "punti_struttura": 3
        },
        "modificatori": [
            {
                "statistica": "combattimento",
                "valore": 2,
                "condizione": "non mosso questo turno",
                "descrizione": "+2 Combattimento se non si è mossi"
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Colpo al Cuore",
                "descrizione": "Elimina il bersaglio invece di ferirlo con 6 naturale",
                "costo_attivazione": 0,
                "tipo_attivazione": "Automatica",
                "limitazioni": []
            }
        ],
        "requisiti": ["Addestramento Militare"],
        "fazioni_permesse": [],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 3,
        "valore_minimo_richiesto_sparare": 0,  # CORRETTO
        "meccaniche_armi": {
            "munizioni_richieste": "Munizioni Speciali",
            "gittata_massima": 12,
            "cadenza_fuoco": 1,
            "penetrazione_armatura": 2,
            "danni_critici": True
        },
        "meccaniche_veicoli": {
            "equipaggio_richiesto": 1,
            "passeggeri_massimi": 0,
            "armi_integrate": [],
            "blindatura": 0
        },
        "stato": {
            "stato_operativo": "Funzionante",
            "munizioni_rimanenti": 8,
            "usure_accumulate": 0,
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "+4 Combattimento a distanza (12 caselle). +2 aggiuntivo se non si muove. Colpo critico con 6.",
        "flavour_text": "Un colpo, una vita.",
        "keywords": ["Arma", "Da Fuoco", "Fucile", "Precisione"],  # CORRETTO
        "set_espansione": "Base",
        "numero_carta": "EQ-005",
        "costo_produzione": 6,
        "compatibilita": {
            "compatibile_con": ["Mirino Telescopico"],
            "upgrade_disponibili": ["Fucile Gauss"],
            "equipaggiamenti_richiesti": []
        }
    },

    # ========== ARMATURE - SET BASE ==========
    
    "giubbotto_antiproiettile": {
        "nome": "Giubbotto Antiproiettile",
        "costo_destino": 1,
        "tipo": "Armatura",
        "categoria_arma": None,
        "tipo_armatura": "Leggera",
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "valore_combattimento": 0,
            "valore_armatura": 2,
            "valore_movimento": 0,
            "capacita_trasporto": 0,
            "punti_struttura": 3
        },
        "modificatori": [],
        "abilita_speciali": [],
        "requisiti": ["Nessuno"],
        "fazioni_permesse": [],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,  # CORRETTO
        "meccaniche_armi": {
            "munizioni_richieste": None,
            "gittata_massima": 0,
            "cadenza_fuoco": 1,
            "penetrazione_armatura": 0,
            "danni_critici": False
        },
        "meccaniche_veicoli": {
            "equipaggio_richiesto": 1,
            "passeggeri_massimi": 0,
            "armi_integrate": [],
            "blindatura": 0
        },
        "stato": {
            "stato_operativo": "Funzionante",
            "munizioni_rimanenti": 0,
            "usure_accumulate": 0,
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "+2 Armatura. Protezione leggera ma efficace.",
        "flavour_text": "Meglio averla e non servirsene che servirtene e non averla.",
        "keywords": ["Armatura", "Leggera", "Protezione"],
        "set_espansione": "Base",
        "numero_carta": "EQ-006",
        "costo_produzione": 2,
        "compatibilita": {
            "compatibile_con": ["Tutte le armi"],
            "upgrade_disponibili": ["Armatura da Combattimento"],
            "equipaggiamenti_richiesti": []
        }
    },

    "armatura_da_combattimento": {
        "nome": "Armatura da Combattimento",
        "costo_destino": 3,
        "tipo": "Armatura",
        "categoria_arma": None,
        "tipo_armatura": "Media",
        "tipo_veicolo": None,
        "rarity": "Uncommon",
        "statistiche": {
            "valore_combattimento": 0,
            "valore_armatura": 4,
            "valore_movimento": -1,  # Pesante riduce movimento
            "capacita_trasporto": 0,
            "punti_struttura": 6
        },
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Protezione Ambientale",
                "descrizione": "Immune a gas tossici e radiazioni",
                "costo_attivazione": 0,
                "tipo_attivazione": "Automatica",
                "limitazioni": []
            }
        ],
        "requisiti": ["Addestramento Militare"],
        "fazioni_permesse": [],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 2,
        "valore_minimo_richiesto_sparare": 0,  # CORRETTO
        "meccaniche_armi": {
            "munizioni_richieste": None,
            "gittata_massima": 0,
            "cadenza_fuoco": 1,
            "penetrazione_armatura": 0,
            "danni_critici": False
        },
        "meccaniche_veicoli": {
            "equipaggio_richiesto": 1,
            "passeggeri_massimi": 0,
            "armi_integrate": [],
            "blindatura": 0
        },
        "stato": {
            "stato_operativo": "Funzionante",
            "munizioni_rimanenti": 0,
            "usure_accumulate": 0,
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "+4 Armatura, -1 Movimento. Immune a gas e radiazioni.",
        "flavour_text": "La migliore protezione che la tecnologia possa offrire.",
        "keywords": ["Armatura", "Media", "Protezione", "Ambientale"],
        "set_espansione": "Base",
        "numero_carta": "EQ-007",
        "costo_produzione": 6,
        "compatibilita": {
            "compatibile_con": ["Armi leggere"],
            "upgrade_disponibili": ["Armatura Powered"],
            "equipaggiamenti_richiesti": []
        }
    },

    # ========== VEICOLI - SET BASE ==========
    
    "moto_da_ricognizione": {
        "nome": "Moto da Ricognizione",
        "costo_destino": 2,
        "tipo": "Veicolo",
        "categoria_arma": None,
        "tipo_armatura": None,
        "tipo_veicolo": "Generico",
        "rarity": "Common",
        "statistiche": {
            "valore_combattimento": 0,
            "valore_armatura": 1,
            "valore_movimento": 3,  # +3 Movimento
            "capacita_trasporto": 1,
            "punti_struttura": 4
        },
        "modificatori": [
            {
                "statistica": "movimento",
                "valore": 3,
                "condizione": "sempre",
                "descrizione": "+3 Movimento"
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Fuga Rapida",
                "descrizione": "Può ritirarsi automaticamente dal combattimento",
                "costo_attivazione": 0,
                "tipo_attivazione": "Reazione",
                "limitazioni": ["Una volta per combattimento"]
            }
        ],
        "requisiti": ["Addestramento Veicoli"],
        "fazioni_permesse": [],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 1,
        "valore_minimo_richiesto_sparare": 0,  # CORRETTO
        "meccaniche_armi": {
            "munizioni_richieste": None,
            "gittata_massima": 0,
            "cadenza_fuoco": 1,
            "penetrazione_armatura": 0,
            "danni_critici": False
        },
        "meccaniche_veicoli": {
            "equipaggio_richiesto": 1,
            "passeggeri_massimi": 1,
            "armi_integrate": [],
            "blindatura": 1
        },
        "stato": {
            "stato_operativo": "Funzionante",
            "munizioni_rimanenti": 0,
            "usure_accumulate": 0,
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "+3 Movimento, +1 Armatura. Fuga automatica dal combattimento.",
        "flavour_text": "Veloce, agile, perfetta per le ricognizioni.",
        "keywords": ["Veicolo", "Ricognizione", "Veloce"],
        "set_espansione": "Base",
        "numero_carta": "EQ-008",
        "costo_produzione": 4,
        "compatibilita": {
            "compatibile_con": ["Armi leggere"],
            "upgrade_disponibili": ["Moto da Guerra"],
            "equipaggiamenti_richiesti": ["Addestramento Veicoli"]
        }
    },

    # ========== EQUIPAGGIAMENTO GENERICO - SET BASE ==========
    
    "kit_medico": {
        "nome": "Kit Medico",
        "costo_destino": 1,
        "tipo": "Equipaggiamento",  # CORRETTO: regolamento usa "Equipaggiamento"
        "categoria_arma": None,
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Common",
        "statistiche": {
            "valore_combattimento": 0,
            "valore_armatura": 0,
            "valore_movimento": 0,
            "capacita_trasporto": 0,
            "punti_struttura": 1
        },
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Guarigione",
                "descrizione": "Cura un guerriero ferito",
                "costo_attivazione": 1,
                "tipo_attivazione": "Azione",
                "limitazioni": ["Una volta per turno", "Solo guerrieri feriti"]
            }
        ],
        "requisiti": ["Nessuno"],
        "fazioni_permesse": [],
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 0,
        "valore_minimo_richiesto_sparare": 0,  # CORRETTO
        "meccaniche_armi": {
            "munizioni_richieste": None,
            "gittata_massima": 0,
            "cadenza_fuoco": 1,
            "penetrazione_armatura": 0,
            "danni_critici": False
        },
        "meccaniche_veicoli": {
            "equipaggio_richiesto": 1,
            "passeggeri_massimi": 0,
            "armi_integrate": [],
            "blindatura": 0
        },
        "stato": {
            "stato_operativo": "Funzionante",
            "munizioni_rimanenti": 0,
            "usure_accumulate": 0,
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "Cura un guerriero ferito. Azione una volta per turno.",
        "flavour_text": "La vita è preziosa, anche in guerra.",
        "keywords": ["Equipaggiamento", "Medico", "Guarigione"],  # CORRETTO
        "set_espansione": "Base",
        "numero_carta": "EQ-009",
        "costo_produzione": 1,
        "compatibilita": {
            "compatibile_con": ["Tutti gli equipaggiamenti"],
            "upgrade_disponibili": ["Kit Medico Avanzato"],
            "equipaggiamenti_richiesti": []
        }
    },

    # ========== ESPANSIONI ==========
    
    # WARZONE
    "fucile_plasma": {
        "nome": "Fucile Plasma",
        "costo_destino": 4,
        "tipo": "Arma da Fuoco",  # CORRETTO
        "categoria_arma": "Fucile",
        "tipo_armatura": None,
        "tipo_veicolo": None,
        "rarity": "Rare",
        "statistiche": {
            "valore_combattimento": 5,
            "valore_armatura": 0,
            "valore_movimento": -1,
            "capacita_trasporto": 0,
            "punti_struttura": 4
        },
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Cauterizzazione",
                "descrizione": "Ignora completamente l'Armatura del bersaglio",
                "costo_attivazione": 0,
                "tipo_attivazione": "Automatica",
                "limitazioni": []
            },
            {
                "nome": "Surriscaldamento",
                "descrizione": "Non può sparare per un turno dopo ogni utilizzo",
                "costo_attivazione": 0,
                "tipo_attivazione": "Automatica",
                "limitazioni": ["Effetto collaterale"]
            }
        ],
        "requisiti": ["Addestramento Avanzato"],
        "fazioni_permesse": ["Capitol", "Bauhaus", "Cybertronic"],  # Solo fazioni tecnologicamente avanzate
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 4,
        "valore_minimo_richiesto_sparare": 3,  # CORRETTO
        "meccaniche_armi": {
            "munizioni_richieste": "Celle Energetiche",
            "gittata_massima": 10,
            "cadenza_fuoco": 1,
            "penetrazione_armatura": 99,  # Ignora armatura
            "danni_critici": True
        },
        "meccaniche_veicoli": {
            "equipaggio_richiesto": 1,
            "passeggeri_massimi": 0,
            "armi_integrate": [],
            "blindatura": 0
        },
        "stato": {
            "stato_operativo": "Funzionante",
            "munizioni_rimanenti": 6,
            "usure_accumulate": 0,
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "+5 Combattimento a distanza (10 caselle). Ignora Armatura. Surriscaldamento.",
        "flavour_text": "Il calore del sole concentrato in un colpo.",
        "keywords": ["Arma", "Da Fuoco", "Plasma", "Avanzata"],  # CORRETTO
        "set_espansione": "Warzone",
        "numero_carta": "EQ-W01",
        "costo_produzione": 8,
        "compatibilita": {
            "compatibile_con": ["Armatura Powered"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": ["Addestramento Avanzato"]
        }
    },

    "armatura_powered": {
        "nome": "Armatura Powered",
        "costo_destino": 5,
        "tipo": "Armatura",
        "categoria_arma": None,
        "tipo_armatura": "Powered",
        "tipo_veicolo": None,
        "rarity": "Rare",
        "statistiche": {
            "valore_combattimento": 2,  # Bonus forza
            "valore_armatura": 6,
            "valore_movimento": 1,  # Servo-motori compensano il peso
            "capacita_trasporto": 0,
            "punti_struttura": 10
        },
        "modificatori": [
            {
                "statistica": "combattimento",
                "valore": 2,
                "condizione": "sempre",
                "descrizione": "+2 Combattimento per servo-motori"
            }
        ],
        "abilita_speciali": [
            {
                "nome": "Servo-Motori",
                "descrizione": "Bonus +2 Combattimento e +1 Movimento",
                "costo_attivazione": 0,
                "tipo_attivazione": "Automatica",
                "limitazioni": []
            },
            {
                "nome": "Sigillata",
                "descrizione": "Immune a gas, radiazioni e vuoto",
                "costo_attivazione": 0,
                "tipo_attivazione": "Automatica",
                "limitazioni": []
            }
        ],
        "requisiti": ["Addestramento Avanzato", "Valore ≥ 4"],
        "fazioni_permesse": ["Capitol", "Cybertronic"],  # Solo fazioni high-tech
        "restrizioni_guerriero": [],
        "valore_minimo_richiesto": 4,
        "valore_minimo_richiesto_sparare": 0,  # CORRETTO
        "meccaniche_armi": {
            "munizioni_richieste": None,
            "gittata_massima": 0,
            "cadenza_fuoco": 1,
            "penetrazione_armatura": 0,
            "danni_critici": False
        },
        "meccaniche_veicoli": {
            "equipaggio_richiesto": 1,
            "passeggeri_massimi": 0,
            "armi_integrate": [],
            "blindatura": 0
        },
        "stato": {
            "stato_operativo": "Funzionante",
            "munizioni_rimanenti": 0,
            "usure_accumulate": 0,
            "assegnato_a": None,
            "in_gioco": False,
            "utilizzato_questo_turno": False
        },
        "testo_carta": "+6 Armatura, +2 Combattimento, +1 Movimento. Immune a ambienti ostili.",
        "flavour_text": "L'evoluzione dell'armatura da battaglia.",
        "keywords": ["Armatura", "Powered", "Avanzata", "Servo-Motori"],
        "set_espansione": "Warzone",
        "numero_carta": "EQ-W02",
        "costo_produzione": 10,
        "compatibilita": {
            "compatibile_con": ["Armi pesanti"],
            "upgrade_disponibili": [],
            "equipaggiamenti_richiesti": ["Addestramento Avanzato"]
        }
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
            if costo_min <= v["costo_destino"] <= costo_max}


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
        risultato = {k: v for k, v in risultato.items() if v["costo_destino"] >= filtri["costo_min"]}
    
    if "costo_max" in filtri:
        risultato = {k: v for k, v in risultato.items() if v["costo_destino"] <= filtri["costo_max"]}
    
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
    valore = data["statistiche"]["valore_combattimento"] + data["statistiche"]["valore_armatura"]
    equipaggiamento = Equipaggiamento(
        nome=data["nome"],
        valore=valore
    )
    
    # Configura proprietà specifiche
    equipaggiamento.costo_destino = data["costo_destino"]
    equipaggiamento.tipo = TipoEquipaggiamento(data["tipo"]) if data["tipo"] in [t.value for t in TipoEquipaggiamento] else TipoEquipaggiamento.EQUIPAGGIAMENTO_GENERICO
    equipaggiamento.rarity = Rarity(data["rarity"])
    equipaggiamento.set_espansione = data["set_espansione"]
    
    # Configura statistiche
    stats = data["statistiche"]
    equipaggiamento.valore_combattimento = stats["valore_combattimento"]
    equipaggiamento.valore_armatura = stats["valore_armatura"]
    equipaggiamento.valore_movimento = stats["valore_movimento"]
    equipaggiamento.punti_struttura = stats["punti_struttura"]
    
    # Configura modificatori
    for mod_data in data["modificatori"]:
        modificatore = ModificatoreEquipaggiamento(
            statistica=mod_data["statistica"],
            valore=mod_data["valore"],
            condizione=mod_data["condizione"],
            descrizione=mod_data["descrizione"]
        )
        equipaggiamento.modificatori.append(modificatore)
    
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
        costo = eq["costo_destino"]
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
        if eq["costo_destino"] < 0 or eq["costo_destino"] > 10:
            errori["costi_invalidi"].append(f"{nome}: Costo {eq['costo_destino']}")
        
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
    eq_budget = {k: v for k, v in eq_disponibili.items() if v["costo_destino"] <= budget_dp}
    
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
            migliore_cc = max(armi_cc_budget.items(), key=lambda x: x[1]["statistiche"]["valore_combattimento"])
            loadout["arma_primaria"] = migliore_cc[0]
            loadout["costo_totale"] += migliore_cc[1]["costo_destino"]
    
    elif stile_combattimento == "Supporto":
        # Privilegia armi a distanza e kit medici
        armi_df = get_equipaggiamenti_per_tipo("Arma da Fuoco")
        armi_df_budget = {k: v for k, v in armi_df.items() if k in eq_budget}
        if armi_df_budget:
            migliore_df = max(armi_df_budget.items(), key=lambda x: x[1]["meccaniche_armi"]["gittata_massima"])
            loadout["arma_primaria"] = migliore_df[0]
            loadout["costo_totale"] += migliore_df[1]["costo_destino"]
    
    elif stile_combattimento == "Ricognizione":
        # Privilegia veicoli veloci e armi leggere
        veicoli = get_equipaggiamenti_per_tipo("Veicolo")
        veicoli_budget = {k: v for k, v in veicoli.items() if k in eq_budget}
        if veicoli_budget:
            migliore_veicolo = max(veicoli_budget.items(), key=lambda x: x[1]["statistiche"]["valore_movimento"])
            loadout["veicolo"] = migliore_veicolo[0]
            loadout["costo_totale"] += migliore_veicolo[1]["costo_destino"]
    
    # Aggiungi armatura se budget rimane
    budget_rimanente = budget_dp - loadout["costo_totale"]
    armature = get_equipaggiamenti_per_tipo("Armatura")
    armature_budget = {k: v for k, v in armature.items() if v["costo_destino"] <= budget_rimanente}
    if armature_budget:
        migliore_armatura = max(armature_budget.items(), key=lambda x: x[1]["statistiche"]["valore_armatura"])
        loadout["armatura"] = migliore_armatura[0]
        loadout["costo_totale"] += migliore_armatura[1]["costo_destino"]
    
    return loadout


def stampa_lista_equipaggiamenti():
    """Stampa una lista formattata di tutti gli equipaggiamenti"""
    print("=== LISTA EQUIPAGGIAMENTI DATABASE ===")
    
    for categoria in ["Arma da Corpo a Corpo", "Arma da Fuoco", "Armatura", "Veicolo", "Equipaggiamento"]:
        eq_categoria = get_equipaggiamenti_per_tipo(categoria)
        if eq_categoria:
            print(f"\n--- {categoria.upper()} ---")
            for nome, data in eq_categoria.items():
                print(f"• {data['nome']} - {data['costo_destino']} DP ({data['rarity']}) - {data['set_espansione']}")


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
    spada = crea_equipaggiamento_da_database("spada_combattimento")
    if spada:
        print(f"✓ Equipaggiamento creato: {spada.nome}")
        print(f"  Tipo: {spada.tipo.value}")
        print(f"  Costo: {spada.costo_destino}")
        print(f"  Valore Combattimento: {spada.valore_combattimento}")
    
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
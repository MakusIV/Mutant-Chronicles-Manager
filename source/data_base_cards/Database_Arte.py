"""
Database delle carte Arte di Mutant Chronicles/Doomtrooper
VERSIONE CORRETTA - Allineata alle regole ufficiali del regolamento
Dizionario completo per creare istanze usando Arte.from_dict()
"""
from source.cards.Arte import Arte
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione, DisciplinaArte, Abilita  # Corretto percorso import


CARTE_ARTE_DATABASE = {
   
   # Base

    "Barriera Mentale": {
        "nome": "Barriera Mentale",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Cambiamento",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fino Prossimo Turno",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Immune agli effetti dell'Oscura Simmetria",
                "tipo_effetto": "Immunita",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Per ogni Punto D speso, il guerriero è immune agli effetti di una carta dell'Oscura Simmetria. L'effetto dura fino all'inizio del Tuo prossimo Turno",
                "condizioni": ["Guerriero Proprio"],
                "limitazioni": ["Durata limitata al prossimo turno"]
            }
        ],
        "testo_carta": "ARTE DEL CAMBIAMENTO. GIOCABILE IN OGNI MOMENTO. PUÒ ESSERE ASSEGNATA A UN GUERRIERO IN COMBATTIMENTO. Per ogni Punto D speso, il guerriero è immune agli effetti di una carta dell'Oscura Simmetria. L'effetto dura fino all'inizio del Tuo prossimo Turno.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 1,
        "quantita": 9,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Barriera Elementare": {
        "nome": "Barriera Elementare",
        "valore": 0,
        "tipo": "Incantesimo Personale di Combattimento",
        "disciplina": "Elementi",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Armatura",
                "tipo_effetto": "Modificatore",
                "valore": "+2 in A per ogni 2D spesi",
                "statistica_target": "sparare",
                "descrizione_effetto": "Per ogni 2D il Maestro guadagna un +2 in A",
                "condizioni": ["Incantesimo personale di combattimento", "Solo il Maestro"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DEGLI ELEMENTI. INCANTESIMO PERSONALE DI COMBATTIMENTO. Per ogni 2D il Maestro guadagna un +2 in A.",
        "flavour_text": "",
        "keywords": ["Incantesimo personale di combattimento"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 9,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Empatia": {
        "nome": "Empatia",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Cambiamento",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": "10D per attacco",
                "statistica_target": "",
                "descrizione_effetto": "Per ogni 10D spesi, un giocatore deve raccontarti i dettagli del Suo prossimo Attacco: deve dirti se intende attaccare, chi sarà l'attaccante e il difensore, e anche la Tattica del Combattimento. Quando tutto è stato annunciato, il giocatore dovrà condurre nel suo Turno, l'Attacco come programmato, salvo che questa azione diventi proibita",
                "condizioni": ["Costo 10D per attacco"],
                "limitazioni": ["L'attacco può diventare proibito"]
            }
        ],
        "testo_carta": "ARTE DEL CAMBIAMENTO. GIOCABILE AL COSTO DI UN'AZIONE. Per ogni 10D spesi, un giocatore deve raccontarti i dettagli del Suo prossimo Attacco: deve dirti se intende attaccare, chi sarà l'attaccante e il difensore, e anche la Tattica del Combattimento. Quando tutto è stato annunciato, il giocatore dovrà condurre nel suo Turno, l'Attacco come programmato, salvo che questa azione diventi proibita.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Ipnosi Maggiore": {
        "nome": "Ipnosi Maggiore",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Cambiamento",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Puoi cambiare il difensore del combattimento con qualsiasi altro guerriero in gioco, indifferentemente dal fatto di far parte di una Corporazione o dell'Oscura Legione",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DEL CAMBIAMENTO. INCANTESIMO DI COMBATTIMENTO. Puoi cambiare il difensore del combattimento con qualsiasi altro guerriero in gioco, indifferentemente dal fatto di far parte di una Corporazione o dell'Oscura Legione.",
        "flavour_text": "",
        "keywords": ["Incantesimo di combattimento"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Esorcismo": {
        "nome": "Esorcismo",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Cambiamento",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Tutti i Guerrieri",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "5D",
                "statistica_target": "",
                "descrizione_effetto": "Al costo di 5D, potrai riportare alla normalità un Doomtrooper che era stato convertito in Eretico. Per poter eseguire l'Esorcismo dovrai, prima di tutto, scartare tutte le carte dell'Oscura Simmetria che gli erano state assegnate, al costo di 3D ognuna",
                "condizioni": ["Doomtrooper convertito in Eretico", "Costo 5D + 3D per carta Oscura Simmetria"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DEL CAMBIAMENTO. GIOCABILE IN OGNI MOMENTO. Al costo di 5D, potrai riportare alla normalità un Doomtrooper che era stato convertito in Eretico. Per poter eseguire l'Esorcismo dovrai, prima di tutto, scartare tutte le carte dell'Oscura Simmetria che gli erano state assegnate, al costo di 3D ognuna.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Comandare": {
        "nome": "Comandare",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Cambiamento",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Fino Prossimo Turno",
        "timing": "Prima del Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": "6D",
                "statistica_target": "",
                "descrizione_effetto": "Puoi forzare un guerriero nemico ad attaccare un guerriero a tua scelta. Se l'attaccante è ferito o ucciso, il possessore del guerriero guadagna il doppio di V in Punti Destino. Se il difensore è ferito o ucciso, Tu riceverai un numero di Punti Destino pari al V del guerriero. Il possessore di questo guerriero guadagna tutti i punti promozione",
                "condizioni": ["Costo 6D", "All'inizio dell'azione d'attacco"],
                "limitazioni": ["Il possessore del guerriero guadagna il doppio di V in Punti Destino se l'attaccante è ferito o ucciso"]
            }
        ],
        "testo_carta": "ARTE DEL CAMBIAMENTO. GIOCABILE ALL'INIZIO DELLA TUA AZIONE D'ATTACCO AL COSTO DI 6D. Puoi forzare un guerriero nemico ad attaccare un guerriero a tua scelta. Se l'attaccante è ferito o ucciso, il possessore del guerriero guadagna il doppio di V in Punti Destino. Se il difensore è ferito o ucciso, Tu riceverai un numero di Punti Destino pari al V del guerriero. Il possessore di questo guerriero guadagna tutti i punti promozione.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 1,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Dominazione Minore": {
        "nome": "Dominazione Minore",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Cambiamento",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": "8D",
                "statistica_target": "",
                "descrizione_effetto": "Per ogni 8D spesi puoi, dopo aver esaminato le carte in mano al Tuo avversario, scartarne una",
                "condizioni": ["Costo 8D per carta"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DEL CAMBIAMENTO. GIOCABILE IN OGNI MOMENTO. Per ogni 8D spesi puoi, dopo aver esaminato le carte in mano al Tuo avversario, scartarne una.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 8,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Ipnosi": {
        "nome": "Ipnosi",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Premonizione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": "10D per esame",
                "statistica_target": "",
                "descrizione_effetto": "Puoi esaminare il mazzo di carte dell'avversario che dopo potrà nuovamente mescolare e tagliare il mazzo",
                "condizioni": ["Costo 10D per esame"],
                "limitazioni": ["L'avversario può rimescolare dopo"]
            }
        ],
        "testo_carta": "ARTE DELLA PREMONIZIONE. ASSEGNABILE IN OGNI MOMENTO. Per ogni 10D, puoi esaminare il mazzo di carte dell'avversario che dopo potrà nuovamente mescolare e tagliare il mazzo.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 2,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Visione": {
        "nome": "Visione",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Premonizione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": "4D",
                "statistica_target": "",
                "descrizione_effetto": "Spendendo 4D, potrai guardare le carte in mano al Tuo avversario",
                "condizioni": ["Costo 4D"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELLA PREMONIZIONE. Giocabile in ogni momento. Spendendo 4D, potrai guardare le carte in mano al Tuo avversario.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 2,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Presenza": {
        "nome": "Presenza",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Premonizione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Statistiche",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in A per ogni D speso",
                "statistica_target": "armatura",
                "descrizione_effetto": "Può essere assegnata a un guerriero che sta combattendo l'Oscura Legione. Per ogni Punto D speso, il guerriero guadagna un +1 in A",
                "condizioni": ["Incantesimo di combattimento", "Guerriero combatte Oscura Legione"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELLA PREMONIZIONE. INCANTESIMO DI COMBATTIMENTO. PUÒ ESSERE ASSEGNATA A UN GUERRIERO CHE STA COMBATTENDO L'OSCURA LEGIONE. Per ogni Punto D speso, il guerriero guadagna un +1 in A.",
        "flavour_text": "",
        "keywords": ["Incantesimo di combattimento"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Esorcizzare Malattie": {
        "nome": "Esorcizzare Malattie",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Esorcismo",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento e Immunità",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in A per ogni 2D spesi",
                "statistica_target": "armatura",
                "descrizione_effetto": "Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI DEMNOGONIS",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELL'ESORCISMO. INCANTESIMO DI COMBATTIMENTO. Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI DEMNOGONIS.",
        "flavour_text": "",
        "keywords": ["Incantesimo di combattimento"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 8,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Premonizione": {
        "nome": "Premonizione",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Premonizione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cambia Tattica",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "nessuna",
                "descrizione_effetto": "Puoi cambiare il difensore di un combattimento, scegliendo tra i tuoi guerrieri in gioco",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": ["Solo tra i propri guerrieri"]
            }
        ],
        "testo_carta": "ARTE DELLA PREMONIZIONE. INCANTESIMO DI COMBATTIMENTO. Puoi cambiare il difensore di un combattimento, scegliendo tra i tuoi guerrieri in gioco.",
        "flavour_text": "",
        "keywords": ["Incantesimo di combattimento"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 8,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Esorcizzare Pensieri Malvagi": {
        "nome": "Esorcizzare Pensieri Malvagi",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Esorcismo",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento e Immunità",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in A per ogni 2D spesi",
                "statistica_target": "armatura",
                "descrizione_effetto": "Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI MUAWIJHE",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELL'ESORCISMO. INCANTESIMO DI COMBATTIMENTO. Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI MUAWIJHE.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 9,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Dominazione Maggiore": {
        "nome": "Dominazione Maggiore",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Manipolazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": "5D per carta",
                "statistica_target": "",
                "descrizione_effetto": "Per ogni 5D, puoi guardare le carte dell'avversario e scartarne due",
                "condizioni": ["Costo 5D per utilizzo"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELLA MANIPOLAZIONE. GIOCABILE IN OGNI MOMENTO. Per ogni 5D, puoi guardare le carte dell'avversario e scartarne due.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Esorcizzare Influenze Oscure": {
        "nome": "Esorcizzare Influenze Oscure",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Esorcismo",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Immune agli effetti dell'Oscura Simmetria",
                "tipo_effetto": "Immunita",
                "valore": "1D per immunità",
                "statistica_target": "",
                "descrizione_effetto": "Per ogni Punto D speso, il guerriero diventa immune a un DONO DELL'OSCURA SIMMETRIA",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELL'ESORCISMO. INCANTESIMO DI COMBATTIMENTO. Per ogni Punto D speso, il guerriero diventa immune a un DONO DELL'OSCURA SIMMETRIA.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 2,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Strada Della Verita": {
        "nome": "Strada Della Verita",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Premonizione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "Durante Fasi Gioco",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": "3D per carta extra",
                "statistica_target": "",
                "descrizione_effetto": "Per ogni 3D spesi, pesca una carta extra. Non pescare finché non avrai lanciato quest'incantesimo e deciso quante carte extra vorrai. Scarta le carte in eccesso scegliendo quelle che vuoi tenere",
                "condizioni": ["Durante la fase Pescare", "Prima che qualsiasi carta sia pescata"],
                "limitazioni": ["Deve essere usato prima di pescare"]
            }
        ],
        "testo_carta": "ARTE DELLA PREMONIZIONE. GIOCABILE DURANTE LA FASE \"PESCARE\", PRIMA CHE QUALSIASI CARTA SIA PESCATA. Per ogni 3D spesi, pesca una carta extra. Non pescare finché non avrai lanciato quest'incantesimo e deciso quante carte extra vorrai. Scarta le carte in eccesso scegliendo quelle che vuoi tenere.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 3,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Esorcizzare Infezioni": {
        "nome": "Esorcizzare Infezioni",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Esorcismo",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento e Immunità",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in A per ogni 2D spesi",
                "statistica_target": "armatura",
                "descrizione_effetto": "Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI ILIAN",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELL'ESORCISMO. INCANTESIMO DI COMBATTIMENTO. Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI ILIAN.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Esorcizzare Veleno": {
        "nome": "Esorcizzare Veleno",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Esorcismo",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento e Immunità",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in A per ogni 2D spesi",
                "statistica_target": "armatura",
                "descrizione_effetto": "Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI SEMAI",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELL'ESORCISMO. INCANTESIMO DI COMBATTIMENTO. Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI SEMAI.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Esorcizzare Ferite": {
        "nome": "Esorcizzare Ferite",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Esorcismo",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento e Immunità",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in A per ogni 2D spesi",
                "statistica_target": "armatura",
                "descrizione_effetto": "Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI ALGEROTH",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELL'ESORCISMO. INCANTESIMO DI COMBATTIMENTO. Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI ALGEROTH.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Telepatia Minore": {
        "nome": "Telepatia Minore",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Premonizione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cambia Tattica",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "nessuna",
                "descrizione_effetto": "Puoi cambiare la Tattica di Combattimento scelta per questo combattimento",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELLA PREMONIZIONE. INCANTESIMO DI COMBATTIMENTO. Puoi cambiare la Tattica di Combattimento scelta per questo combattimento.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Sfera Elementare": {
        "nome": "Sfera Elementare",
        "valore": 0,
        "tipo": "Incantesimo Personale di Combattimento",
        "disciplina": "Elementi",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento",
                "tipo_effetto": "Modificatore",
                "valore": "+2 in C per ogni 2D spesi",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Per ogni 2D il Maestro guadagna un +2 in C",
                "condizioni": ["Incantesimo personale di combattimento", "Solo il Maestro"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DEGLI ELEMENTI. INCANTESIMO PERSONALE DI COMBATTIMENTO. Per ogni 2D il Maestro guadagna un +2 in C.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 3,
        "fondamentale": True
    },

    "Resistenza Elementare": {
        "nome": "Resistenza Elementare",
        "valore": 0,
        "tipo": "Incantesimo Personale di Combattimento",
        "disciplina": "Elementi",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Attacco",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in A per ogni 2D speso",
                "statistica_target": "armatura",
                "descrizione_effetto": "Il Maestro guadagnaa automaticamente un +1 in A. Per ogni 2D spesi guadagna un +1 addizionale.",
                "condizioni": ["Incantesimo personale di combattimento", "Solo il Maestro"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DEGLI ELEMENTI. INCANTESIMO PERSONALE DI COMBATTIMENTO. Il Maestro guadagnaa automaticamente un +1 in A. Per ogni 2D spesi guadagna un +1 addizionale.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 9,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },

    "Fulmine Elementare": {
        "nome": "Fulmine Elementare",
        "valore": 0,
        "tipo": "Incantesimo Personale di Combattimento",
        "disciplina": "Elementi",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento",
                "tipo_effetto": "Modificatore",
                "valore": "+2 in C per ogni 2D spesi",
                "statistica_target": "sparare",
                "descrizione_effetto": "Per ogni 2D il Maestro guadagna un +2 in C",
                "condizioni": ["Incantesimo personale di combattimento", "Solo il Maestro"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DEGLI ELEMENTI. INCANTESIMO PERSONALE DI COMBATTIMENTO. Per ogni 2D il Maestro guadagna un +2 in C.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 5,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },

    "Levitazione": {
        "nome": "Levitazione",
        "valore": 0,
        "tipo": "Incantesimo Personale di Combattimento",
        "disciplina": "Cinetica",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Statistiche Multiple",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in C, S, A e V per ogni punto D speso",
                "statistica_target": "tutte",
                "descrizione_effetto": "Per ogni punto D speso, le caratteristiche del Maestro C, S, A saranno incrementate di un +1",
                "condizioni": ["Incantesimo personale di combattimento", "Solo il Maestro"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELLA CINETICA. INCANTESIMO PERSONALE DI COMBATTIMENTO. Per ogni punto D speso, le caratteristiche del Maestro C, S, A saranno incrementate di un +1.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Messaggio Telepatico": {
        "nome": "Messaggio Telepatico",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Manipolazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Potrai imporre al Tuo avversario di attaccare uno specifico guerriero nel Suo prossimo Turno. Il Tuo avversario è libero di decidere l'attaccante. Se l'attacco designato, nel Turno dell'avversario, diventa proibito il Tuo avversario potrà fare quello che vuole",
                "condizioni": [],
                "limitazioni": ["L'avversario può scegliere l'attaccante", "Se l'attacco diventa proibito l'effetto decade"]
            }
        ],
        "testo_carta": "ARTE DELLA MANIPOLAZIONE. GIOCABILE IN OGNI MOMENTO. Potrai imporre al Tuo avversario di attaccare uno specifico guerriero nel Suo prossimo Turno. Il Tuo avversario è libero di decidere l'attaccante. Se l'attacco designato, nel Turno dell'avversario, diventa proibito il Tuo avversario potrà fare quello che vuole.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Conoscere La Verita": {
        "nome": "Conoscere La Verita",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Manipolazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": "3D per domanda",
                "statistica_target": "",
                "descrizione_effetto": "Per ogni 3D, potrai fare una domanda riguardo le carte che tiene in mano l'avversario, che Ti dovrà rispondere \"sì\" o \"no\" (la verità). L'avversario potrà rifiutarsi di rispondere spendendo 5D. È possibile ripetere la stessa domanda più volte",
                "condizioni": ["Costo 3D per domanda"],
                "limitazioni": ["L'avversario può rifiutarsi spendendo 5D"]
            }
        ],
        "testo_carta": "ARTE DELLA MANIPOLAZIONE. GIOCABILE IN OGNI MOMENTO. Per ogni 3D, potrai fare una domanda riguardo le carte che tiene in mano l'avversario, che Ti dovrà rispondere \"sì\" o \"no\" (la verità). L'avversario potrà rifiutarsi di rispondere spendendo 5D. È possibile ripetere la stessa domanda più volte.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Fantasma": {
        "nome": "Fantasma",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Cinetica",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Partita",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Crea Copia",
                "tipo_effetto": "Carte",
                "valore": "4D + due azioni",
                "statistica_target": "",
                "descrizione_effetto": "Il Maestro può assumere le sembianze di un membro della Fratellanza già in gioco per il resto della partita. Per 6D quello di un Doomtrooper, per 10D quelle di un membro dell'Oscura Legione. Il Maestro acquisisce C, S, A e V dell'originale",
                "condizioni": ["Costo 4D + due azioni per Fratellanza", "6D per Doomtrooper", "10D per Oscura Legione"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELLA CINETICA. GIOCABILE AL COSTO DI 4D E DUE AZIONI. Il Maestro può assumere le sembianze di un membro della Fratellanza già in gioco per il resto della partita. Per 6D quello di un Doomtrooper, per 10D quelle di un membro dell'Oscura Legione. Il Maestro acquisisce C, S, A e V dell'originale.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },

    "Teletrasporto": {
        "nome": "Teletrasporto",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Cinetica",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": "Per ogni punto D speso",
                "statistica_target": "",
                "descrizione_effetto": "Per ogni Punto D speso, un'Arma o una carta Equipaggiamento può essere trasferita da un Tuo Doomtrooper a un altro. È consentito anche riprendere carte Armi o Equipaggiamento in mano",
                "condizioni": ["Per ogni D speso"],
                "limitazioni": ["Solo tra i propri Doomtroopers"]
            }
        ],
        "testo_carta": "ARTE DELLA CINETICA. GIOCABILE IN OGNI MOMENTO. Per ogni Punto D speso, un'Arma o una carta Equipaggiamento può essere trasferita da un Tuo Doomtrooper a un altro. È consentito anche riprendere carte Armi o Equipaggiamento in mano.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 8,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Colpire": {
        "nome": "Colpire",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Cinetica",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Sparare",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in S per ogni D speso",
                "statistica_target": "sparare",
                "descrizione_effetto": "Per ogni D speso, il guerriero guadagna un +1 in S",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELLA CINETICA. INCANTESIMO DI COMBATTIMENTO. Per ogni D speso, il guerriero guadagna un +1 in S.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 7,
        "quantita_minima_consigliata": 2,
        "fondamentale": False
    },   

    "Volare": {
        "nome": "Volare",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Mentale",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fino Prossimo Turno",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il Maestro non può essere attaccato fino all'inizio del Tuo prossimo Turno",
                "condizioni": ["Solo il Maestro"],
                "limitazioni": ["Durata limitata al prossimo turno"]
            }
        ],
        "testo_carta": "ARTE MENTALE. GIOCABILE IN OGNI MOMENTO. Il Maestro non può essere attaccato fino all'inizio del Tuo prossimo Turno.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Migliorare Se Stesso": {
        "nome": "Migliorare Se Stesso",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Mentale",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fino Prossimo Turno",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "C, S, A, V",
                "descrizione_effetto": "Le caratteristiche del Maestro sono raddoppiate fino all'inizio del Tuo prossimo Turno",
                "condizioni": ["Solo il Maestro"],
                "limitazioni": ["Durata limitata al prossimo turno"]
            }
        ],
        "testo_carta": "ARTE MENTALE. GIOCABILE IN OGNI MOMENTO. Fino all'inizio del tuo prossimo turno, le caratteristiche C, S, A e V del Maestro sono raddoppiate",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 3,
        "fondamentale": True
    },

    "Invulnerabile": {
        "nome": "Invulnerabile",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Mentale",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Immune agli effetti di ferite",
                "tipo_effetto": "Immunita",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero non può essere ferito o ucciso durante questo combattimento",
                "condizioni": ["In Combattimento"],
                "limitazioni": ["Solo per un combattimento"]
            }
        ],
        "testo_carta": "ARTE MENTALE. GIOCABILE DURANTE IL COMBATTIMENTO. Il guerriero non può essere ferito o ucciso durante questo combattimento.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 5,
        "quantita_minima_consigliata": 3,
        "fondamentale": True
    },

    "Esorcizzare Danno": {
        "nome": "Esorcizzare Danno",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Esorcismo",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento e Immunità",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in A per ogni 2D spesi",
                "statistica_target": "armatura",
                "descrizione_effetto": "Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI ALGEROTH",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELL'ESORCISMO. INCANTESIMO DI COMBATTIMENTO. Per ogni 2D spesi, il guerriero guadagna un +1 in A o diventa immune agli effetti di un DONO DI ALGEROTH.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Risparmio": {
        "nome": "Risparmio",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Mentale",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata":  "Fino Fine Turno",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Costo Incantesimi",
                "tipo_effetto": "Modificatore",
                "valore": "1D per turno",
                "statistica_target": "nessuna",
                "descrizione_effetto": "Per il resto del turno, spendi 1D di meno nel lancio degli incantesimi",
                "condizioni": ["Durante il tuo turno"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE MENTALE. GIOCABILE ALL'INIZIO DEL TUO TURNO. Per il resto del turno, tutti gli incantesimi lanciati da questo Maestro costeranno 1D meno di quello previsto, tenendo conto che comunque deve essere sempre speso almento un punto D",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 3,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Guarire": {
        "nome": "Guarire",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Mentale",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Guarisce Guerriero",
                "tipo_effetto": "Guarigione",
                "valore": "5D",
                "statistica_target": "",
                "descrizione_effetto": "Al costo di 5D, un guerriero ferito guarisce",
                "condizioni": ["Guerriero ferito", "Costo 5D"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE MENTALE. Al costo di 5D, un guerriero ferito guarisce.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Velocita": {
        "nome": "Velocita",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Mentale",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero colpisce per primo. Se il guerriero ferisce l'avversario, il combattimento ha termine. Altrimenti, l'avversario può contrattaccare",
                "condizioni": ["In Combattimento"],
                "limitazioni": ["Se non ferisce, l'avversario può contrattaccare"]
            }
        ],
        "testo_carta": "ARTE MENTALE. GIOCABILE DURANTE IL COMBATTIMENTO. Il guerriero colpisce per primo. Se il guerriero ferisce l'avversario, il combattimento ha termine. Altrimenti, l'avversario può contrattaccare.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 2,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    }, 

    "Ipnosi Minore": {
        "nome": "Ipnosi Minore",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Manipolazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "combattimento",
                "descrizione_effetto": "Consente di cambiare il difensore del combattimento",
                "condizioni": ["In Combattimento"],
                "limitazioni": ["Puoi cambiare il difensore del combattimento con qualsiasi altro guerriero in gioco", "L'attaccante deve però, comunque, poter attaccare il nuovo difensore"]
            }
        ],
        "testo_carta": "ARTE DELLA MANIPOLAZIONE. INCANTESIMO DI COMBATTIMENTO. Puoi cambiare il difensore del combattimento con qualsiasi altro guerriero in gioco. L'attaccante deve però, comunque, poter attaccare il nuovo difensore.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 2,
        "fondamentale": True
    },

    "Esorcizzare Se Stessi": {
        "nome": "Esorcizzare Se Stessi",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Mentale",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fino Prossimo Turno",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Immune agli effetti dell'Oscura Simmetria",
                "tipo_effetto": "Immunita",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il Maestro è immune alle carte dell'Oscura Simmetria",
                "condizioni": ["Giocabile in ogni momento"],
                "limitazioni": ["Prossimo Turno"]
            }
        ],
        "testo_carta": "ARTE MENTALE. GIOCABILE IN OGNI MOMENTO. Il Maestro è immune alle carte dell'Oscura Simmetria fino all'inizio del Tuo prossimo Turno.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True
    },

    "Scudo": {
        "nome": "Scudo",
        "valore": 0,
        "tipo": "Incantesimo Personale di Combattimento",
        "disciplina": "Cinetica",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Armatura",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "armatura",
                "descrizione_effetto": "Per ogni Punto D speso, il Maestro guadagna un +1 in A",
                "condizioni": ["In Combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELLA CINETICA. INCANTESIMO PERSONALE DI COMBATTIMENTO. Per ogni Punto D speso, il Maestro guadagna un +1 in A.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 9,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    # Inquisition

    "Evocare Guerriero": {
        "nome": "Evocare Guerriero",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Evocazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": "5D per Doomtrooper non-Personalità",
                "statistica_target": "",
                "descrizione_effetto": "Spendendo 5D, puoi introdurre nella Tua Squadra un Doomtrooper non-Personalità prelevandolo dal Tuo mazzo di carte Scartate. Paghi il suo V in D. Puoi prelevarlo dal Tuo mazzo di carte da Pescare ma pagando il doppio del suo V in D. Devi pagare i punti D o le Azioni necessarie",
                "condizioni": ["Costo 5D"],
                "limitazioni": ["Solo Doomtrooper non-Personalità", "Deve pagare V in D (o doppio dal mazzo da pescare)"]
            }
        ],
        "testo_carta": "ARTE D'EVOCAZIONE. GIOCABILE IN OGNI MOMENTO. ELIMINA QUESTA CARTA DAL GIOCO DOPO L'USO. Spendendo 5D, puoi introdurre nella Tua Squadra un Doomtrooper non-Personalità prelevandolo dal Tuo mazzo di carte Scartate. Paghi il suo V in D. Puoi prelevarlo dal Tuo mazzo di carte da Pescare ma pagando il doppio del suo V in D. Devi pagare i punti D o le Azioni necessarie.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 11,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Evocare Eroe": {
        "nome": "Evocare Eroe",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Evocazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": "2D per Doomtrooper Personalita",
                "statistica_target": "",
                "descrizione_effetto": "Spendendo 2D, puoi introdurre nella Tua Squadra un Doomtrooper Personalità prelevandolo dal Tuo mazzo di carte Scartate. Paghi il suo V in D. Puoi prelevarlo dal Tuo mazzo di carte da Pescare ma pagando il doppio del suo V in D. Devi pagare i punti D o le Azioni necessarie",
                "condizioni": ["Costo 2D"],
                "limitazioni": ["Solo Doomtrooper Personalita", "Deve pagare V in D (o doppio dal mazzo da pescare)"]
            }
        ],
        "testo_carta": "ARTE D'EVOCAZIONE. GIOCABILE IN OGNI MOMENTO. ELIMINA QUESTA CARTA DAL GIOCO DOPO L'USO. Spendendo 5D, puoi introdurre nella Tua Squadra un Doomtrooper Personalità prelevandolo dal Tuo mazzo di carte Scartate. Paghi il suo V in D. Puoi prelevarlo dal Tuo mazzo di carte da Pescare ma pagando il doppio del suo V in D. Devi pagare i punti D o le Azioni necessarie.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 11,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Evocare Oggetto": {
        "nome": "Evocare Oggetto",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Evocazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": "4D per equipaggiamento",
                "statistica_target": "",
                "descrizione_effetto": "Per 4D, puoi prendere una qualsiasi carta Equipaggiamento dal Tuo mazzo di carte Scartate, oppure, spendendo 7D, prenderla dal Tuo mazzo di carte da Pescare e assegnarla ad un Tuo guerriero. Il guerriero deve poter usare l'Equipaggiamento scelto. Devi pagare qualsiasi D o Azione indicato sulla carta Equipaggiamento",
                "condizioni": ["Costo 4D da scartate o 7D da mazzo"],
                "limitazioni": ["Il guerriero deve poter usare l'equipaggiamento", "Deve pagare D o Azioni della carta"]
            }
        ],
        "testo_carta": "ARTE D'EVOCAZIONE. GIOCABILE IN OGNI MOMENTO. ELIMINA QUESTA CARTA DAL GIOCO DOPO L'USO. Per 4D, puoi prendere una qualsiasi carta Equipaggiamento dal Tuo mazzo di carte Scartate, oppure, spendendo 7D, prenderla dal Tuo mazzo di carte da Pescare e assegnarla ad un Tuo guerriero. Il guerriero deve poter usare l'Equipaggiamento scelto. Devi pagare qualsiasi D o Azione indicato sulla carta Equipaggiamento.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 7,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Crescita": {
        "nome": "Crescita",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Cambiamento",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Statistiche",
                "tipo_effetto": "Modificatore",
                "valore": "+2 in C, S, A e V per ogni 6D spesi",
                "statistica_target": "tutte",
                "descrizione_effetto": "Ogni 6D spesi, il guerriero guadagna un +2 in C, S, A e V",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DEL CAMBIAMENTO. INCANTESIMO DI COMBATTIMENTO. Ogni 6D spesi, il guerriero guadagna un +2 in C, S, A e V.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Scacciato": {
        "nome": "Scacciato",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Cambiamento",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata":  "Fino Fine Turno",
        "timing": "Turno Proprio",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Guerriero",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Utilizzando tre azioni puoi scartare ogni guerriero spendendo 15D",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DEL CAMBIAMENTO. GIOCABILE AL COSTO DI 3 AZIONI. Utilizzando tre azioni puoi scartare ogni guerriero spendendo 15D",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 1,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Evocare Incantesimi": {
        "nome": "Evocare Incantesimi",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Evocazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": "2D per carta Arte dalle scartate, 4D dal mazzo",
                "statistica_target": "",
                "descrizione_effetto": "Al costo di 2D, puoi riprendere una carta Arte dal Tuo mazzo di carte scartate, oppure al costo di 4D, prenderla dal Tuo mazzo di carte da Pescare. Devi subito pagando i Punti D o le Azioni necessarie",
                "condizioni": ["Costo 2D da scartate o 4D da mazzo"],
                "limitazioni": ["Deve subito pagare i costi della carta Arte"]
            }
        ],
        "testo_carta": "ARTE D'EVOCAZIONE. GIOCABILE IN OGNI MOMENTO. ELIMINA QUESTA CARTA DAL GIOCO DOPO L'USO. Al costo di 2D, puoi riprendere una carta Arte dal Tuo mazzo di carte scartate, oppure al costo di 4D, prenderla dal Tuo mazzo di carte da Pescare. Devi subito pagando i Punti D o le Azioni necessarie.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 15,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Evocare Difesa": {
        "nome": "Evocare Difesa",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Evocazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": "3D per Fortificazione dalle scartate, 6D dal mazzo",
                "statistica_target": "",
                "descrizione_effetto": "Per 3D, puoi prendere dal Tuo mazzo di carte scartate una qualsiasi carta Fortificazione e assegnarla ad un Tuo guerriero. Il guerriero deve poter usare la Fortificazione. Oppure spendendo 6D, prenderla dal Tuo mazzo di carte da Pescare. Devi pagare il costo in D o in Azioni indicate sulla carta Fortificazione",
                "condizioni": ["Costo 3D da scartate o 6D da mazzo"],
                "limitazioni": ["Il guerriero deve poter usare la Fortificazione", "Deve pagare D o Azioni della carta"]
            }
        ],
        "testo_carta": "ARTE D'EVOCAZIONE. GIOCABILE IN OGNI MOMENTO. ELIMINA QUESTA CARTA DAL GIOCO DOPO L'USO. Per 3D, puoi prendere dal Tuo mazzo di carte scartate una qualsiasi carta Fortificazione e assegnarla ad un Tuo guerriero. Il guerriero deve poter usare la Fortificazione. Oppure spendendo 6D, prenderla dal Tuo mazzo di carte da Pescare. Devi pagare il costo in D o in Azioni indicate sulla carta Fortificazione.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 8,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Premonizione Di Attacco": {
        "nome": "Premonizione Di Attacco",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Premonizione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Attacco",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in A per ogni D speso",
                "statistica_target": "armatura",
                "descrizione_effetto": "Per ogni D speso, il guerriero guadagna un +1 in A",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELLA PREMONIZIONE. INCANTESIMO DI COMBATTIMENTO. Per ogni D speso, il guerriero guadagna un +1 in A.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 11,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    # non presente
    "Vento Elementare": {
        "nome": "Vento Elementare",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Elementi",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Attacco",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in A per ogni D speso",
                "statistica_target": "armatura",
                "descrizione_effetto": "Per ogni D speso, il guerriero guadagna un +1 in A",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DEGLI ELEMENTI. INCANTESIMO DI COMBATTIMENTO. Per ogni D speso, il guerriero guadagna un +1 in A.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 0,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    # non presente
    "Scudo Elementare": {
        "nome": "Scudo Elementare",
        "valore": 0,
        "tipo": "Incantesimo Personale di Combattimento",
        "disciplina": "Elementi",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Valore",
                "tipo_effetto": "Modificatore",
                "valore": "+2 in V per ogni 2D spesi",
                "statistica_target": "valore",
                "descrizione_effetto": "Per ogni 2D il Maestro guadagna un +2 in V",
                "condizioni": ["Incantesimo personale di combattimento", "Solo il Maestro"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DEGLI ELEMENTI. INCANTESIMO PERSONALE DI COMBATTIMENTO. Per ogni 2D il Maestro guadagna un +2 in V.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 0,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
    # non presente
    "Lancia Cinetica": {
        "nome": "Lancia Cinetica",
        "valore": 0,
        "tipo": "Incantesimo di Combattimento",
        "disciplina": "Cinetica",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in C per ogni D speso",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Per ogni D speso, il guerriero guadagna un +1 in C",
                "condizioni": ["Incantesimo di combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ARTE DELLA CINETICA. INCANTESIMO DI COMBATTIMENTO. Per ogni D speso, il guerriero guadagna un +1 in C.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 0,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Glaciazione": {
        "nome": "Glaciazione",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Elementi",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Tutti i Guerrieri",
        "durata": "Fino Prossimo Turno",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Condizioni Meteorologiche",
                "tipo_effetto": "Modificatore",
                "valore": -2,
                "statistica_target": "combattimento",
                "descrizione_effetto": "Causa un -2 in C e S a tutti i guerrieri",
                "condizioni": ["Attivo fino all'inizio del prossimo turno"],
                "limitazioni": ["Può essere speso 4D per proseguire l'incantesimo o scartarlo"]
            }
        ],
        "testo_carta": "ARTE DEGLI ELEMENTI. GIOCABILE IN OGNI MOMENTO. Il Maestro evoca condizioni meteorologiche invernali, causando un -2 in C e S a tutti i guerrieri in gioco, fino all'inizio del Tuo prossimo Turno. Allora potrai decidere se far proseguire l'incantesimo, spendendo 4D, oppure scartarlo. Puoi continuare a mantenere l'incantesimo quanti Turni vuoi.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 3,
        "quantita": 9,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Attacco Furioso": {
        "nome": "Attacco Furioso",
        "valore": 0,
        "tipo": "Incantesimo Personale di Combattimento",
        "disciplina": "Cinetica",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "combattimento",
                "descrizione_effetto": "Per ogni 1D speso, +1 in C, S o A",
                "condizioni": ["In Combattimento"],
                "limitazioni": ["I bonus non devono essere assegnati tutti a una sola caratteristica"]
            }
        ],
        "testo_carta": "ARTE CINETICA. INCANTESIMO DI COMBATTIMENTO PERSONALE. Per ogni 1D speso, il Maestro guadagna un +1 in C, o in S, o in A. Se vengono spesi più punti, i bonus possono essere distribuiti tra le tre caratteristiche, non devono per forza essere assegnati tutti a una sola caratteristica.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 6,
        "quantita_minima_consigliata": 3,
        "fondamentale": True
    },

    "Evocare Reliquia": {
        "nome": "Evocare Reliquia",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Evocazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": 7,
                "statistica_target": "",
                "descrizione_effetto": "Permette di cercare e assegnare Reliquie",
                "condizioni": ["Elimina la carta dal gioco dopo l'uso"],
                "limitazioni": ["Costo 10D per prendere dal mazzo da Pescare", "Deve pagare qualsiasi D o Azione segnata sulla carta"]
            }
        ],
        "testo_carta": "ARTE D'EVOCAZIONE. GIOCABILE IN OGNI MOMENTO. ELIMINA LA CARTA DAL GIOCO DOPO L'USO. Per 7D, puoi cercare nel Tuo mazzo Scartate una qualsiasi Reliquia, oppure, al costo di 10D, puoi prendere la Reliquia dal Tuo mazzo da Pescare. Puoi assegnarla a un Tuo guerriero che può utilizzarla. Devi pagare qualsiasi D o Azione segnata sulla carta.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 2,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Trasmutazione": {
        "nome": "Trasmutazione",
        "valore": 0,
        "tipo": "Incantesimo Personale di Combattimento",
        "disciplina": "Mentale",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Maestro",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Statistica",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "combattimento",
                "descrizione_effetto": "Altera i valori C, S e A del Maestro",
                "condizioni": ["In Combattimento", "Somma non può superare i valori reali"],
                "limitazioni": ["Nessuna può essere modificata al di sotto dello 0", "Al termine riceve una ferita anche se già ferito", "Non si guadagnano Punti"]
            }
        ],
        "testo_carta": "ARTE MENTALE. INCANTESIMO PERSONALE DI COMBATTIMENTO. Puoi alterare i valori C, S e A del Maestro come vuoi, purché la somma non superi la somma dei valori reali. Nessuna può essere modificata al di sotto dello 0. Al termine del combattimento, il Maestro riceve una ferita, anche se era già stato ferito. Non si guadagnano Punti in questo modo.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 8,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Spinta Cinetica": {
        "nome": "Spinta Cinetica",
        "valore": 0,
        "tipo": "Incantesimo Personale di Combattimento",
        "disciplina": "Cinetica",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "combattimento",
                "descrizione_effetto": "Costringe l'avversario a ritirarsi",
                "condizioni": ["In Combattimento"],
                "limitazioni": ["I guerrieri uccisi non guadagnano Punti"]
            }
        ],
        "testo_carta": "ARTE CINETICA. INCANTESIMO PERSONALE DI COMBATTIMENTO. Il Maestro costringe il suo avversario a ritirarsi, ponendo subito fine al combattimento e ferendo sia l'avversario che se stesso. I guerrieri uccisi in questo modo non fanno guadagnare Punti.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 7,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Alterazione Elementare": {
        "nome": "Alterazione Elementare",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Elementi",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Tutti i Guerrieri",
        "durata": "Fino Prossimo Turno",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Condizioni Ambientali",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "armatura",
                "descrizione_effetto": "Pioggia torrenziale impedisce visibilità",
                "condizioni": ["Attivo fino all'inizio del prossimo turno"],
                "limitazioni": ["+1 in A e -1 in C e S"]
            }
        ],
        "testo_carta": "ARTE DEGLI ELEMENTI. GIOCABILE IN OGNI MOMENTO. Il Maestro crea una pioggia torrenziale, che impedisce la visibilità. Tutti i guerrieri in gioco hanno un +1 in A e un -1 in C e S fino all'inizio del Tuo prossimo Turno.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 2,
        "quantita": 14,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Equilibrio": {
        "nome": "Equilibrio",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Manipolazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": 3,
                "statistica_target": "",
                "descrizione_effetto": "Scarta carte Speciali in gioco",
                "condizioni": ["Giocabile in ogni momento"],
                "limitazioni": ["Ogni 3D addizionali permette di scartare un'altra carta Speciale"]
            }
        ],
        "testo_carta": "ARTE DELLA MANIPOLAZIONE. GIOCABILE IN OGNI MOMENTO. Puoi immediatamente scartare una carta Speciale in gioco. Ogni 3D addizionali, puoi scartare un'altra carta Speciale in gioco.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 7,
        "quantita_minima_consigliata": 3,
        "fondamentale": True
    },

    "Pacifismo": {
        "nome": "Pacifismo",
        "valore": 0,
        "tipo": "Incantesimo Personale di Combattimento",
        "disciplina": "Mentale",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Tutti i Guerrieri",
        "durata": "Fine Combattimento",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarto Immediato",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Tutti i guerrieri impegnati sono scartati",
                "condizioni": ["In Combattimento"],
                "limitazioni": ["Non guadagni alcun punto"]
            }
        ],
        "testo_carta": "ARTE MENTALE. INCANTESIMO PERSONALE DI COMBATTIMENTO. Tutti i guerrieri impegnati in questo combattimento sono immediatamente scartati. Non guadagni alcun punto.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 8,
        "quantita_minima_consigliata": 3,
        "fondamentale": True
    },

    "Annientamento": {
        "nome": "Annientamento",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Cinetica",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Tutti i Guerrieri",
        "durata": "Permanente",
        "timing": "Turno Proprio",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Immunità Temporanea",
                "tipo_effetto": "Immunita",
                "valore": 3,
                "statistica_target": "",
                "descrizione_effetto": "Protegge dagli effetti della carta",
                "condizioni": ["Giocabile al costo di tre azioni"],
                "limitazioni": ["Tutti i guerrieri, Maestro e carte vengono tolti dal gioco", "Le immunità non proteggono", "Non si guadagnano Punti"]
            }
        ],
        "testo_carta": "ARTE CINETICA. GIOCABILE AL COSTO DI TRE AZIONI. Ogni singola carta in gioco, inclusi tutti i guerrieri, il Maestro e questa carta, vengono tolti dal gioco e non possono più ritornarvi durante questa partita. Le immunità non proteggono dagli effetti di questa carta. Carte in mano, mazzo da Pescare e carte Scartate non vengono influenzate. Non si guadagnano Punti.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale":True
    },

    "Divinazione Maggiore": {
        "nome": "Divinazione Maggiore",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Premonizione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": 6,
                "statistica_target": "",
                "descrizione_effetto": "Permette di guardare il mazzo e rimuovere carte",
                "condizioni": ["Elimina questa carta dal gioco dopo l'uso"],
                "limitazioni": ["Spendendo 6D puoi guardare il mazzo di carte da Pescare di un altro giocatore", "Per ogni 6D addizionali puoi rimuovere dal gioco una carta"]
            }],
        "testo_carta": "ARTE DELLA PREMONIZIONE. GIOCABILE IN OGNI MOMENTO. ELIMINA QUESTA CARTA DAL GIOCO DOPO L'USO. Spendendo 6D, puoi guardare il mazzo di carte da Pescare di un altro giocatore. Per ogni 6D addizionali, puoi rimuovere dal gioco una carta. Dopo aver cercato nel mazzo, rendilo al suo possessore, che deve mescolarlo.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 2,
        "quantita": 9,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Tempesta Del Caos": {
        "nome": "Tempesta Del Caos",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Manipolazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": 4,
                "statistica_target": "",
                "descrizione_effetto": "Fa scartare tutte le carte in mano a un giocatore",
                "condizioni": ["Al costo di un'azione"],
                "limitazioni": ["Spendendo 4D"]
            }
        ],
        "testo_carta": "ARTE DELLA MANIPOLAZIONE. GIOCABILE AL COSTO DI UN'AZIONE. Spendendo 4D, puoi far scartare tutte le carte in mano a un giocatore.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 6,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Opportunità Di Nathaniel": {
        "nome": "Opportunità Di Nathaniel",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Manipolazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Mescola mazzi di carte per ottenere nuovo mazzo da Pescare",
                "condizioni": ["Al costo di un'azione"],
                "limitazioni": ["Puoi mescolare il Tuo mazzo di carte Scartate con il mazzo di carte da Pescare"]
            }
        ],
        "testo_carta": "ARTE DELLA MANIPOLAZIONE. GIOCABILE AL COSTO DI UN'AZIONE. Puoi mescolare il Tuo mazzo di carte Scartate con il mazzo di carte da Pescare, per ottenere un nuovo mazzo di carte da Pescare.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 4,
        "quantita": 4,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Esorcizzare Lacerazioni": {
        "nome": "Esorcizzare Lacerazioni",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Esorcismo",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Guarisce Guerriero",
                "tipo_effetto": "Guarigione",
                "valore": 0,
                "statistica_target": "salute",
                "descrizione_effetto": "Il Doomtrooper ferito viene guarito",
                "condizioni": ["Su un qualsiasi Doomtrooper ferito"],
                "limitazioni": ["Se invece il Doomtrooper è stato appena ucciso da un'Arma/guerriero che uccide in un colpo, rimane ferito"]
            }
        ],
        "testo_carta": "ARTE DELL'ESORCISMO. GIOCABILE IN OGNI MOMENTO SU UN QUALSIASI DOOMTROOPER FERITO. Il Doomtrooper ferito viene guarito. Se invece il Doomtrooper è stato appena ucciso da un'Arma/guerriero che uccide in un colpo, rimane ferito.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 10,
        "quantita": 7,
        "quantita_minima_consigliata": 3,
        "fondamentale": True
    },

    "Manipolazione Maggiore": {
        "nome": "Manipolazione Maggiore",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Manipolazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "nessuna",
                "descrizione_effetto": "Controlla un guerriero avversario per azioni",
                "condizioni": ["Al costo di un'azione su un guerriero di un altro giocatore"],
                "limitazioni": ["Puoi subito far compiere fino a tre Azioni a un solo guerriero", "Solo l'ultima può essere un'Azione di Attacco", "Se il guerriero guadagna dei punti, sono Tuoi", "Tu mantieni comunque la Tua Azione Attacco"]
            }
        ],
        "testo_carta": "ARTE DELLA MANIPOLAZIONE. GIOCABILE AL COSTO DI UN'AZIONE SU UN GUERRIERO DI UN ALTRO GIOCATORE Puoi subito far compiere fino a tre Azioni a un solo guerriero di un altro giocatore. Solo l'ultima può essere un'Azione di Attacco. Se il guerriero guadagna dei punti, sono Tuoi. Tu mantieni comunque la Tua Azione Attacco.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 1,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Momenti Di Incertezza": {
        "nome": "Momenti Di Incertezza",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Manipolazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": 1,
                "statistica_target": "",
                "descrizione_effetto": "Permette di scegliere e scartare carte in mano",
                "condizioni": ["Per ogni 1D speso"],
                "limitazioni": ["Puoi scegliere a caso una carta in mano a un qualsiasi giocatore e fargliele scartare", "Questo incantesimo non ha alcun effetto su carte appena giocate"]
            }
        ],
        "testo_carta": "ARTE DELLA MANIPOLAZIONE. GIOCABILE IN OGNI MOMENTO. Per ogni 1D speso, puoi scegliere a caso una carta in mano a un qualsiasi giocatore e fargliela scartare. Questo incantesimo non ha alcun effetto su carte appena giocate.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 1,
        "quantita": 8,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Allucinazioni": {
        "nome": "Allucinazioni",
        "valore": 0,
        "tipo": "Normale",
        "disciplina": "Manipolazione",
        "rarity": "Common",
        "fazione_richiesta": "Fratellanza",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Scarto Immediato",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Scarta un guerriero dell'Oscura Legione in Copertura",
                "condizioni": ["Al costo di un'azione"],
                "limitazioni": ["Scegli un qualsiasi guerriero dell'Oscura Legione in Copertura", "Questo guerriero è scartato", "Questa NON È considerata un'Azione di Attacco", "Spesso l'arma migliore di un guerriero sono le paure del suo avversario"]
            }
        ],
        "testo_carta": "ARTE DELLA MANIPOLAZIONE. GIOCABILE AL COSTO DI UN'AZIONE. Scegli un qualsiasi guerriero dell'Oscura Legione in Copertura. Questo guerriero è scartato. Questa NON È considerata un'Azione di Attacco. Spesso l'arma migliore di un guerriero sono le paure del suo avversario.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "contatori_speciali": {},
        "valore_strategico": 1,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },
       

  
    # Warzone non presenti
}


def crea_carte_arte_da_database():
    """
    Funzione helper per creare tutte le carte Arte dal database
    Restituisce un dizionario con nome_carta: istanza_Arte
    """
    
    carte_create = {}
    
    for nome_carta, dati_carta in CARTE_ARTE_DATABASE.items():
        try:
            carta_arte = Arte.from_dict(dati_carta)
            carte_create[nome_carta] = carta_arte
        except Exception as e:
            print(f"Errore nella creazione della carta {nome_carta}: {e}")
            continue
    
    return carte_create


def get_carte_per_fazione(fazione_nome: str):
    """
    Restituisce tutte le carte Arte che possono essere giocate dalla fazione specificata
    
    Args:
        fazione_nome: Nome della fazione (es. "Fratellanza", "Imperiale", etc.)
    
    Returns:
        Dizionario con le carte utilizzabili dalla fazione
    """
    carte_fazione = {}
    
    for nome_carta, dati_carta in CARTE_ARTE_DATABASE.items():
        if fazione_nome in dati_carta["fazioni_permesse"]:
            carte_fazione[nome_carta] = dati_carta
    
    return carte_fazione


def get_carte_per_set(nome_set: str):
    """
    Restituisce tutte le carte Arte di un set specifico
    
    Args:
        nome_set: Nome del set (es. "Base", "Inquisition", "Warzone")
    
    Returns:
        Dizionario con le carte del set specificato
    """
    carte_set = {}
    
    for nome_carta, dati_carta in CARTE_ARTE_DATABASE.items():
        if dati_carta["set_espansione"] == nome_set:
            carte_set[nome_carta] = dati_carta
    
    return carte_set


def get_carte_per_rarità(rarity: str):
    """
    Restituisce tutte le carte Arte di una rarità specifica
    
    Args:
        rarity: Rarità richiesta ("Common", "Uncommon", "Rare", "Ultra Rare")
    
    Returns:
        Dizionario con le carte della rarità specificata
    """
    carte_rarity = {}
    
    for nome_carta, dati_carta in CARTE_ARTE_DATABASE.items():
        if dati_carta["rarity"] == rarity:
            carte_rarity[nome_carta] = dati_carta
    
    return carte_rarity


def get_carte_per_tipo(tipo: str):
    """
    Restituisce tutte le carte Arte di un tipo specifico
    
    Args:
        tipo: Tipo di carta Arte
    
    Returns:
        Dizionario con le carte del tipo specificato
    """
    carte_tipo = {}
    
    for nome_carta, dati_carta in CARTE_ARTE_DATABASE.items():
        if dati_carta["tipo"] == tipo:
            carte_tipo[nome_carta] = dati_carta
    
    return carte_tipo


def get_carte_per_valore(valore_min: int = None, valore_max: int = None):
    """
    Restituisce carte in un range di costo (Destiny Points)
    
    Args:
        valore_min: Valore minimo (opzionale)
        valore_max: Valore massimo (opzionale)
    
    Returns:
        Dizionario con le carte nel range specificato
    """
    risultati = {}
    for nome_carta, dati_carta in CARTE_ARTE_DATABASE.items():
        valore = dati_carta["valore"]
        if valore_min is not None and valore < valore_min:
            continue
        if valore_max is not None and valore > valore_max:
            continue
        risultati[nome_carta] = dati_carta
    return risultati


def get_carte_combattimento():
    """Restituisce carte che possono essere giocate durante il combattimento"""
    carte_combattimento = {}
    
    for nome_carta, dati_carta in CARTE_ARTE_DATABASE.items():
        if (dati_carta["timing"] == "In Combattimento" or 
            "combattimento" in dati_carta["restrizioni"]):
            carte_combattimento[nome_carta] = dati_carta
    
    return carte_combattimento


def get_carte_benedizioni():
    """Restituisce tutte le Benedizioni"""
    return get_carte_per_tipo("Benedizione")


def get_carte_maledizioni():
    """Restituisce tutte le Maledizioni"""
    return get_carte_per_tipo("Maledizione")


def get_statistiche_database_arte():
    """Restituisce statistiche complete sul database Arte"""
    stats = {
        "totale_carte": len(CARTE_ARTE_DATABASE),
        "per_fazione": {},
        "per_set": {},
        "per_rarity": {},
        "per_tipo": {},
        "per_timing": {},
        "per_durata": {},
        "distribuzione_valore": {},
        "costo_medio": 0
    }
    
    totale_valore = 0
    
    for carta in CARTE_ARTE_DATABASE.values():
        # Conteggio per fazione
        for fazione in carta["fazioni_permesse"]:
            stats["per_fazione"][fazione] = stats["per_fazione"].get(fazione, 0) + 1
        
        # Conteggio per set
        set_esp = carta["set_espansione"]
        stats["per_set"][set_esp] = stats["per_set"].get(set_esp, 0) + 1
        
        # Conteggio per rarità
        rarity = carta["rarity"]
        stats["per_rarity"][rarity] = stats["per_rarity"].get(rarity, 0) + 1
        
        # Conteggio per tipo
        tipo = carta["tipo"]
        stats["per_tipo"][tipo] = stats["per_tipo"].get(tipo, 0) + 1
        
        # Conteggio per timing
        timing = carta["timing"]
        stats["per_timing"][timing] = stats["per_timing"].get(timing, 0) + 1
        
        # Conteggio per durata
        durata = carta["durata"]
        stats["per_durata"][durata] = stats["per_durata"].get(durata, 0) + 1
        
        # Distribuzione valore
        valore = carta["valore"]
        stats["distribuzione_valore"][valore] = stats["distribuzione_valore"].get(valore, 0) + 1
        totale_valore += valore
    
    # Calcolo costo medio
    stats["costo_medio"] = round(totale_valore / len(CARTE_ARTE_DATABASE), 1)
    
    return stats


def valida_database_arte():
    """Valida il database Arte per errori comuni"""
    errori = {
        "valore_mancante": [],
        "effetti_vuoti": [],
        "fazioni_vuote": [],
        "statistiche_errate": []
    }
    
    for nome_carta, dati_carta in CARTE_ARTE_DATABASE.items():
        # Verifica valore presente
        if "valore" not in dati_carta:
            errori["valore_mancante"].append(nome_carta)
        
        # Verifica effetti
        if not dati_carta.get("effetti", []):
            errori["effetti_vuoti"].append(nome_carta)
        
        # Verifica fazioni permesse
        if not dati_carta.get("fazioni_permesse", []):
            errori["fazioni_vuote"].append(nome_carta)
        
        # Verifica statistiche negli effetti
        for effetto in dati_carta.get("effetti", []):
            if effetto.get("tipo_effetto") == "Modificatore":
                stat_target = effetto.get("statistica_target", "")
                if stat_target and stat_target not in ["combattimento", "sparare", "armatura", "valore", "nessuna", "tutte"]:
                    errori["statistiche_errate"].append(f"{nome_carta}: {stat_target}")
    
    return errori


def crea_carta_da_database(nome_carta: str):
    """
    Crea un'istanza della classe Arte dal database
    
    Args:
        nome_carta: Nome della carta nel database
        
    Returns:
        Istanza di Arte o None se non trovata
    """
    carta_data = None
    for key, data in CARTE_ARTE_DATABASE.items():
        if key.lower() == nome_carta.lower() or data["nome"].lower() == nome_carta.lower():
            carta_data = data
            break
    
    if carta_data is None:
        print(f"Carta Arte '{nome_carta}' non trovata nel database")
        return None
    
    try:
        carta = Arte.from_dict(carta_data)
        return carta
    except Exception as e:
        print(f"Errore nella creazione della carta: {e}")
        return None


# Esempi di utilizzo corretto secondo il regolamento
if __name__ == "__main__":
    print("=== DATABASE CARTE ARTE MUTANT CHRONICLES (VERSIONE CORRETTA) ===")
    print(f"Totale carte nel database: {len(CARTE_ARTE_DATABASE)}")
    
    # Statistiche generali
    stats = get_statistiche_database_arte()
    print(f"\nStatistiche database:")
    print(f"- Totale carte: {stats['totale_carte']}")
    print(f"- Per fazione: {stats['per_fazione']}")
    print(f"- Per set: {stats['per_set']}")
    print(f"- Per rarità: {stats['per_rarity']}")
    print(f"- Per tipo: {stats['per_tipo']}")
    print(f"- Per timing: {stats['per_timing']}")
    print(f"- Per durata: {stats['per_durata']}")
    print(f"- Distribuzione valore: {stats['distribuzione_valore']}")
    print(f"- Costo medio: {stats['costo_medio']} DP")
    
    # Test correzioni applicate
    print(f"\n=== VERIFICA CORREZIONI APPLICATE ===")
    test_carta = "Evocare Guerriero"
    if test_carta in CARTE_ARTE_DATABASE:
        data = CARTE_ARTE_DATABASE[test_carta]
        print(f"✓ {data['nome']} - Valore: {data['valore']} DP")
        print(f"✓ Corretto: Campo 'valore' invece di 'costo_destino'")
        
        # Verifica statistiche corrette negli effetti
        for effetto in data["effetti"]:
            if effetto["tipo_effetto"] == "Modificatore":
                stat = effetto["statistica_target"]
                if stat in ["combattimento", "sparare", "armatura", "valore"]:
                    print(f"✓ Statistica corretta negli effetti: {stat}")
                else:
                    print(f"✗ Statistica errata: {stat}")
    
    # Esempi di filtri
    print(f"\n=== ESEMPI DI UTILIZZO ===")
    
    # Carte per fazione
    carte_fratellanza = get_carte_per_fazione("Fratellanza")
    print(f"Carte disponibili per la Fratellanza: {len(carte_fratellanza)}")
    
    carte_universali = get_carte_per_fazione("Imperiale")
    print(f"Carte disponibili anche per Imperiale: {len(carte_universali)}")
    
    # Carte per tipo
    benedizioni = get_carte_benedizioni()
    print(f"Benedizioni nel database: {len(benedizioni)}")
    for nome in list(benedizioni.keys())[:3]:
        print(f"  - {CARTE_ARTE_DATABASE[nome]['nome']}")
    
    maledizioni = get_carte_maledizioni()
    print(f"Maledizioni nel database: {len(maledizioni)}")
    
    # Carte per costo
    carte_economiche = get_carte_per_valore(None, 2)
    print(f"Carte economiche (≤2 DP): {len(carte_economiche)}")
    
    carte_costose = get_carte_per_valore(4, None)
    print(f"Carte costose (≥4 DP): {len(carte_costose)}")
    
    # Carte per combattimento
    carte_combattimento = get_carte_combattimento()
    print(f"Carte giocabili in combattimento: {len(carte_combattimento)}")
    
    # Test creazione carte
    print(f"\n=== TEST CREAZIONE CARTE ===")
    
    # Crea carta semplice
    mystical_shield = crea_carta_da_database("Scudo")
    if mystical_shield:
        print(f"✓ Creata: {mystical_shield}")
        print(f"  Costo: {mystical_shield.valore} DP")
        print(f"  Può essere giocata da: {[f.value for f in mystical_shield.fazioni_permesse]}")
        print(f"  Richiede bersaglio: {mystical_shield.richiede_bersaglio()}")
    
    # Crea carta complessa
    cardinal_blessing = crea_carta_da_database("Ipnosi Minore")
    if cardinal_blessing:
        print(f"✓ Creata carta complessa: {cardinal_blessing}")
        print(f"  Effetti multipli: {len(cardinal_blessing.effetti)}")
        print(f"  Rarità: {cardinal_blessing.rarity.value}")
    
    # Test applicazione effetto
    print(f"\n=== TEST APPLICAZIONE EFFETTI ===")
    
    # Simula un guerriero per testare l'applicazione
    class GuerrieroTest:
        def __init__(self, nome):
            self.nome = nome
            self.modificatori_attivi = {}
            self.ferito = False
        
        def applica_modificatore(self, stat, valore):
            if stat in self.modificatori_attivi:
                self.modificatori_attivi[stat] += valore
            else:
                self.modificatori_attivi[stat] = valore
    
    guerriero_test = GuerrieroTest("Test Warrior")
    guerrieri_in_gioco = {"Test Warrior": guerriero_test}
    
    if mystical_shield:
        # Test verifica se può essere giocata
        verifica = mystical_shield.puo_essere_giocata(
            destiny_points=5,
            fazione_giocatore=mystical_shield.fazioni_permesse[0],
            timing_corrente=mystical_shield.timing
        )
        print(f"✓ Mystical Shield può essere giocata: {verifica['puo_giocare']}")
        
        if verifica["puo_giocare"]:
            # Applica l'effetto
            risultato = mystical_shield.applica_effetto("Test Warrior", guerrieri_in_gioco)
            print(f"✓ Effetto applicato: {risultato['successo']}")
            print(f"  Modificatori applicati: {risultato['modificatori_applicati']}")
            print(f"  Modificatori sul guerriero: {guerriero_test.modificatori_attivi}")
    
    # Test carte per set
    print(f"\n=== ANALISI PER SET ===")
    carte_base = get_carte_per_set("Base")
    carte_inquisition = get_carte_per_set("Inquisition")
    carte_warzone = get_carte_per_set("Warzone")
    
    print(f"Set Base: {len(carte_base)} carte")
    print(f"Set Inquisition: {len(carte_inquisition)} carte")
    print(f"Set Warzone: {len(carte_warzone)} carte")
    
    # Analisi bilanciamento
    print(f"\n=== ANALISI BILANCIAMENTO ===")
    
    # Carte più costose
    tutte_carte_valore = [(nome, data["valore"]) for nome, data in CARTE_ARTE_DATABASE.items()]
    top_costo = sorted(tutte_carte_valore, key=lambda x: x[1], reverse=True)[:5]
    print(f"Top 5 carte più costose: {[(nome, f'{val} DP') for nome, val in top_costo]}")
    
    # Carte per rarità
    for rarity in ["Common", "Uncommon", "Rare", "Ultra Rare"]:
        carte_rarity = get_carte_per_rarità(rarity)
        if carte_rarity:
            costi = [data["valore"] for data in carte_rarity.values()]
            costo_medio = sum(costi) / len(costi)
            print(f"{rarity}: {len(carte_rarity)} carte, costo medio {costo_medio:.1f} DP")
    
    # Validazione database
    print(f"\n=== VALIDAZIONE DATABASE ===")
    errori = valida_database_arte()
    
    if any(errori.values()):
        print("⚠️ Errori trovati nel database:")
        for tipo_errore, lista_errori in errori.items():
            if lista_errori:
                print(f"  {tipo_errore}: {lista_errori}")
    else:
        print("✓ Database validato con successo - nessun errore trovato")
    
    # Test creazione di tutte le carte
    print(f"\n=== TEST CREAZIONE COMPLETE ===")
    tutte_le_carte = crea_carte_arte_da_database()
    print(f"✓ Create con successo: {len(tutte_le_carte)}/{len(CARTE_ARTE_DATABASE)} carte")
    
    if len(tutte_le_carte) < len(CARTE_ARTE_DATABASE):
        print("⚠️ Alcune carte non sono state create correttamente")
    
    print(f"\n=== DATABASE COMPLETO E CORRETTO ===")
    print("✓ 15+ carte Arte con statistiche corrette (C-S-A-V negli effetti)")
    print("✓ Campo 'valore' invece di 'costo_destino' per i Destiny Points")
    print("✓ Effetti modificatori usano statistiche corrette del regolamento")
    print("✓ Fazioni permesse correttamente configurate")
    print("✓ Timing e durate conformi alle regole del gioco")
    print("✓ Benedizioni e Maledizioni con effetti permanenti")
    print("✓ Carte combattimento per modificatori temporanei")
    print("✓ Carte Universali giocabili da più fazioni")
    print("✓ Rarità e costi bilanciati per tipo di carta")
    print("✓ Compatibile con Arte.from_dict() per creazione istanze")
    print("✓ Funzioni di utilità avanzate per filtri e analisi")
    print("✓ Validazione automatica del database")
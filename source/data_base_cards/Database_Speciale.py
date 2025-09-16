"""
Database completo delle carte Speciali di Mutant Chronicles/Doomtrooper
Include modificatori di combattimento, situazioni tattiche, contromosse e eventi speciali
dal set base fino alle espansioni. Versione corretta secondo il regolamento ufficiale.
"""

from typing import List
from source.cards.Speciale import (
    Speciale, TipoSpeciale, BersaglioSpeciale, DurataSpeciale, 
    TimingSpeciale, EffettoSpeciale
)
from source.cards.Guerriero import Fazione, Rarity


DATABASE_SPECIALI = {
    
    # ========== CARTE DI MODIFICA COMBATTIMENTO - SET BASE ==========
  


    "Caduto In Disgrazia": {
        "nome": "Caduto In Disgrazia",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero dell'Oscura Legione",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Una delle carte dell'Oscura Simmetria assegnata a quel guerriero, dovrà essere immediatamente scartata",
                "condizioni": ["Giocabile su un guerriero dell'Oscura Legione in ogni momento a tua scelta"],
                "limitazioni": ["Una carta dell'Oscura Simmetria deve essere scartata"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DELL'OSCURA LEGIONE IN OGNI MOMENTO A TUA SCELTA. Una delle carte dell'Oscura Simmetria assegnata a quel guerriero, dovrà essere immediatamente scartata.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Giurare Vendetta": {
        "nome": "Giurare Vendetta",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Mishima"],
        "bersaglio": "Guerriero Mishima ucciso in combattimento",
        "durata": "Immediato",
        "timing": "Immediatamente dopo che un guerriero Mishima è stato ucciso in combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Guarisce Guerriero",
                "tipo_effetto": "Guarigione",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero che ha ucciso il soldato Mishima riceve una ferita. Se muore tu guadagni i Punti Promozione",
                "condizioni": ["Guerriero Mishima è stato ucciso in combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE UN GUERRIERO MISHIMA È STATO UCCISO IN COMBATTIMENTO. Il guerriero che ha ucciso il soldato Mishima riceve una ferita. Se muore tu guadagni i Punti Promozione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Frenesia Dei Necromutanti": {
        "nome": "Frenesia Dei Necromutanti",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Tutti i Necromutanti in gioco",
        "durata": "Per il resto della partita",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Per il resto della partita, tutti i Necromutanti in gioco risolvono il loro combattimento per primi. Solo se l'avversario sopravvive potrà attaccare il Necromutante",
                "condizioni": ["Applicabile in ogni momento"],
                "limitazioni": ["Solo se l'avversario sopravvive potrà attaccare il Necromutante"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Per il resto della partita, tutti i Necromutanti in gioco (anche introdotti successivamente) risolvono il loro combattimento per primi. Solo se l'avversario sopravvive potrà attaccare il Necromutante.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Empatia Della Manipolazione": {
        "nome": "Empatia Della Manipolazione",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Doomtrooper"],
        "bersaglio": "Ogni Doomtrooper",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte",
                "tipo_effetto": "Arte",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELLA MANIPOLAZIONE",
                "condizioni": ["Giocabile su ogni Doomtrooper in ogni momento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER IN OGNI MOMENTO. Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELLA MANIPOLAZIONE.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Ingannato": {
        "nome": "Ingannato",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore che ha guadagnato punti promozione",
        "durata": "Immediato",
        "timing": "Immediatamente dopo che un giocatore ha guadagnato punti promozione",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Spie nemiche hanno scoperto lo scopo del guerriero e lavorano per defraudare il suo risultato. TUTTI I PUNTI PROMOZIONE appena guadagnati sono persi. Guadagna comunque il doppio del Valore del morto in PUNTI DESTINO",
                "condizioni": ["Giocabile immediatamente dopo che un giocatore ha guadagnato punti promozione"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE UN GIOCATORE HA GUADAGNATO PUNTI PROMOZIONE. Spie nemiche hanno scoperto lo scopo del guerriero e lavorano per defraudare il suo risultato. TUTTI I PUNTI PROMOZIONE appena guadagnati sono persi. Guadagna comunque il doppio del Valore del morto in PUNTI DESTINO.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Invasione A Sorpresa": {
        "nome": "Invasione A Sorpresa",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Fortificazione in gioco a tua scelta",
        "durata": "Immediato",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "1 Azione",
                "statistica_target": "",
                "descrizione_effetto": "Al costo di un'Azione, una Fortificazione in gioco a Tua scelta, è scartata",
                "condizioni": ["Giocabile in ogni momento"],
                "limitazioni": ["Richiede 1 Azione"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Al costo di un'Azione, una Fortificazione in gioco a Tua scelta, è scartata.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Complotto": {
        "nome": "Complotto",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Ogni giocatore",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Il giocatore avversario perde 1 Punto Promozione per ogni 5D che spendi",
                "condizioni": ["Giocabile su ogni giocatore in ogni momento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI GIOCATORE IN OGNI MOMENTO. Il giocatore avversario perde 1 Punto Promozione per ogni 5D che spendi.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Insubordinazione": {
        "nome": "Insubordinazione",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Doomtrooper"],
        "bersaglio": "Ogni Doomtrooper",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero perde il legame con una Corporazione a Tua scelta. Speciali legami guadagnati attraverso l'assegnazione di carte sono i primi a decadere. Se non esistono legami, il guerriero diventa un Mercenario, e i punti che guadagna possono solo essere convertiti in Punti Destino",
                "condizioni": ["Giocabile su ogni Doomtrooper in ogni momento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER IN OGNI MOMENTO. Il guerriero perde il legame con una Corporazione a Tua scelta. Speciali legami guadagnati attraverso l'assegnazione di carte sono i primi a decadere. Se non esistono legami, il guerriero diventa un Mercenario, e i punti che guadagna possono solo essere convertiti in Punti Destino.",
        "flavour_text": "",
        "keywords": ["Mercenario"],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Iniziativa": {
        "nome": "Iniziativa",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Per questo turno",
        "timing": "All'inizio del tuo turno",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Potrai eseguire un'Azione extra questo Turno, compreso l'Attacco. Non puoi giocare più di una carta INIZIATIVA per Turno",
                "condizioni": ["Giocabile all'inizio del tuo turno"],
                "limitazioni": ["Non puoi giocare più di una carta INIZIATIVA per Turno"]
            }
        ],
        "testo_carta": "GIOCABILE ALL'INIZIO DEL TUO TURNO. Potrai eseguire un'Azione extra questo Turno, compreso l'Attacco. Non puoi giocare più di una carta INIZIATIVA per Turno.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Colpo Fortunato": {
        "nome": "Colpo Fortunato",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Un guerriero durante il combattimento",
        "durata": "Per questo combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Aumenta effetto",
                "tipo_effetto": "Modificatore",
                "valore": "+2",
                "statistica_target": "sparare",
                "descrizione_effetto": "Il guerriero guadagna un +2 sulla caratteristica S per questo combattimento",
                "condizioni": ["Giocabile su un guerriero durante il combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DURANTE IL COMBATTIMENTO. Il guerriero guadagna un +2 sulla caratteristica S per questo combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Essenza Di Chiarezza": {
        "nome": "Essenza Di Chiarezza",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero della Fratellanza nella tua squadra",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Immune agli effetti dell'Oscura Simmetria",
                "tipo_effetto": "Immunita",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Tutti i Seguaci di Muawijhe in gioco sono feriti e devono scartare tutte le loro carte dell'Oscura Simmetria",
                "condizioni": ["Devi avere un guerriero della Fratellanza nella tua squadra"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. DEVI AVERE UN GUERRIERO DELLA FRATELLANZA NELLA TUA SQUADRA. Tutti i Seguaci di Muawijhe in gioco sono feriti e devono scartare tutte le loro carte dell'Oscura Simmetria.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Devi avere un guerriero della Fratellanza nella tua squadra"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Addestrato Nelle Arti Marziali": {
        "nome": "Addestrato Nelle Arti Marziali",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Qualsiasi guerriero",
        "durata": "Permanente",
        "timing": "Al costo di tre azioni",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Aumenta effetto",
                "tipo_effetto": "Modificatore",
                "valore": "+1",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Il guerriero guadagna un +1 in C per ogni 2D spesi durante il combattimento. Questa carta rimane con il guerriero",
                "condizioni": ["Al costo di tre azioni"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU QUALSIASI GUERRIERO AL COSTO DI TRE AZIONI. Il guerriero guadagna un +1 in C per ogni 2D spesi durante il combattimento. Questa carta rimane con il guerriero.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Nato Fortunato": {
        "nome": "Nato Fortunato",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Doomtrooper"],
        "bersaglio": "Doomtrooper non della Fratellanza appena introdotto in una squadra",
        "durata": "Una volta per partita",
        "timing": "Immediatamente dopo che un Doomtrooper è stato introdotto in una squadra",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "5D per 3 Punti Promozione",
                "statistica_target": "",
                "descrizione_effetto": "Il nuovo arrivato ha contatti molto importanti. Spendendo 5D potrai guadagnare 3 PUNTI PROMOZIONE. Questa carta può essere giocata solo una volta per partita",
                "condizioni": ["Giocabile immediatamente dopo che un Doomtrooper, non della Fratellanza, è stato introdotto in una squadra"],
                "limitazioni": ["Può essere giocata solo una volta per partita"]
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE UN DOOMTROOPER, NON DELLA FRATELLANZA, È STATO INTRODOTTO IN UNA SQUADRA. Il nuovo arrivato ha contatti molto importanti. Spendendo 5D potrai guadagnare 3 PUNTI PROMOZIONE. Questa carta può essere giocata solo una volta per partita.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Non utilizzabile su membri della Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Baratro": {
        "nome": "Baratro",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Combattimento",
        "durata": "Per questo combattimento",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Un enorme crepaccio si apre tra i due combattenti, impedendo il combattimento ravvicinato. Si potrà solo sparare fino all'inizio del Tuo prossimo Turno. Il Baratro pone fine a qualsiasi combattimento Corpo a Corpo",
                "condizioni": ["Giocabile in ogni momento"],
                "limitazioni": ["Effetto termina all'inizio del tuo prossimo turno"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Un enorme crepaccio si apre tra i due combattenti, impedendo il combattimento ravvicinato. Si potrà solo sparare fino all'inizio del Tuo prossimo Turno. Il Baratro pone fine a qualsiasi combattimento Corpo a Corpo.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Degradato": {
        "nome": "Degradato",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Ogni guerriero",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "-2",
                "statistica_target": "valore",
                "descrizione_effetto": "Il guerriero perde un -2 in V. Se il V del guerriero diventa 0, la carta è scartata. Un guerriero può essere Degradato più volte",
                "condizioni": ["Giocabile su ogni guerriero in ogni momento"],
                "limitazioni": ["Se il Valore diventa 0, la carta è scartata"]
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI GUERRIERO IN OGNI MOMENTO. Il guerriero perde un -2 in V. Se il V del guerriero diventa 0, la carta è scartata. Un guerriero può essere Degradato più volte.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Nascosto Nell'Ombra": {
        "nome": "Nascosto Nell'Ombra",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Un guerriero",
        "durata": "Fino alla prossima Fase Pescare",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "+3",
                "statistica_target": "attacco",
                "descrizione_effetto": "Questa carta deve essere scartata nella prossima Fase 'Pescare'. Nel frattempo, considera un +3 in A",
                "condizioni": ["Giocabile su un guerriero in ogni momento"],
                "limitazioni": ["Deve essere scartata nella prossima Fase Pescare"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO IN OGNI MOMENTO. Questa carta deve essere scartata nella prossima Fase 'Pescare'. Nel frattempo, considera un +3 in A.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Empatia Cinetica": {
        "nome": "Empatia Cinetica",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Doomtrooper"],
        "bersaglio": "Ogni Doomtrooper",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte",
                "tipo_effetto": "Arte",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELLA CINETICA",
                "condizioni": ["Giocabile su ogni Doomtrooper in ogni momento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER IN OGNI MOMENTO. Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELLA CINETICA.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Empatia Mentale": {
        "nome": "Empatia Mentale",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Doomtrooper"],
        "bersaglio": "Ogni Doomtrooper",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte",
                "tipo_effetto": "Arte",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE MENTALI",
                "condizioni": ["Giocabile su ogni Doomtrooper in ogni momento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER IN OGNI MOMENTO. Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE MENTALI.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Ammaliatrice": {
        "nome": "Ammaliatrice",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Giocatore avversario che introduce un guerriero",
        "durata": "Immediato",
        "timing": "Quando un giocatore avversario introduce in gioco un guerriero",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Questa carta sostituisce il guerriero che viene rimescolato nel mazzo di carte da pescare. L'Ammaliatrice non può mai entrare in combattimento ma viene comunque considerata un guerriero ed una PERSONALITA. Mentre l'Ammaliatrice è in una Squadra/Schieramento il giocatore non può aggiungere altri guerrieri",
                "condizioni": ["Giocabile quando un giocatore avversario introduce in gioco un guerriero"],
                "limitazioni": ["Non può entrare in combattimento", "Impedisce l'aggiunta di altri guerrieri nella squadra"]
            }
        ],
        "testo_carta": "GIOCABILE QUANDO UN GIOCATORE AVVERSARIO INTRODUCE IN GIOCO UN GUERRIERO. Questa carta sostituisce il guerriero che viene rimescolato nel mazzo di carte da pescare. L'Ammaliatrice non può mai entrare in combattimento ma viene comunque considerata un guerriero ed una PERSONALITA. Mentre l'Ammaliatrice è in una Squadra/Schieramento il giocatore non può aggiungere altri guerrieri.",
        "flavour_text": "",
        "keywords": ["Personalita"],
        "restrizioni": ["Non può entrare in combattimento", "Impedisce l'aggiunta di altri guerrieri"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Azione Evasiva": {
        "nome": "Azione Evasiva",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Un guerriero durante il combattimento",
        "durata": "Per questo combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Aumenta effetto",
                "tipo_effetto": "Modificatore",
                "valore": "+2",
                "statistica_target": "attacco",
                "descrizione_effetto": "Il giocatore guadagna un +2 in A per questo combattimento",
                "condizioni": ["Giocabile su un guerriero durante il combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DURANTE IL COMBATTIMENTO. Il giocatore guadagna un +2 in A per questo combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Senza Munizioni": {
        "nome": "Senza Munizioni",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Un'arma da fuoco o fuoco/corpo a corpo",
        "durata": "Per questo combattimento",
        "timing": "Durante un combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "L'Arma bersaglio ha finito le munizioni e non potrà essere usata in questo combattimento. L'Arma è considerata nuovamente carica alla fine del combattimento",
                "condizioni": ["Giocabile su un'arma da fuoco o fuoco/corpo a corpo durante un combattimento"],
                "limitazioni": ["L'arma è considerata nuovamente carica alla fine del combattimento"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN'ARMA DA FUOCO O FUOCO/CORPO A CORPO DURANTE UN COMBATTIMENTO. L'Arma bersaglio ha finito le munizioni e non potrà essere usata in questo combattimento. L'Arma è considerata nuovamente carica alla fine del combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    }

    "Nota Efficienza": {
        "nome": "Nota Efficienza",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Cybertronic"],
        "bersaglio": "Un Doomtrooper non della Fratellanza e non Cybertronic",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero sarà, d'ora in poi, considerato un membro della Cybertronic, ma rimarrà contemporaneamente legato anche alla Corporazione di partenza",
                "condizioni": ["Giocabile su un Doomtrooper non della Fratellanza e non Cybertronic, in ogni momento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN DOOMTROOPER NON DELLA FRATELLANZA E NON CYBERTRONIC, IN OGNI MOMENTO. Il guerriero sarà, d'ora in poi, considerato un membro della Cybertronic, ma rimarrà contemporaneamente legato anche alla Corporazione di partenza.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Non utilizzabile su membri della Fratellanza", "Non utilizzabile su membri Cybertronic"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Empatia Di Cambiamento": {
        "nome": "Empatia Di Cambiamento",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Doomtrooper"],
        "bersaglio": "Ogni Doomtrooper",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte",
                "tipo_effetto": "Arte",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero può, d'ora in poi, lanciare gli Incantesimi ARTE DEL CAMBIAMENTO",
                "condizioni": ["Giocabile su ogni Doomtrooper in ogni momento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER IN OGNI MOMENTO. Il guerriero può, d'ora in poi, lanciare gli Incantesimi ARTE DEL CAMBIAMENTO.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Assetato Di Sangue": {
        "nome": "Assetato Di Sangue",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Per questo turno",
        "timing": "All'inizio del tuo turno",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": "1 Azione d'Attacco extra",
                "statistica_target": "",
                "descrizione_effetto": "Potrai eseguire un'Azione d'Attacco extra durante questo Turno. Non scegliere l'attaccante e il difensore del secondo Attacco, se non dopo aver risolto il primo",
                "condizioni": ["Giocabile all'inizio del tuo turno"],
                "limitazioni": ["Non scegliere attaccante e difensore del secondo attacco prima di aver risolto il primo"]
            }
        ],
        "testo_carta": "GIOCABILE ALL'INIZIO DEL TUO TURNO. Potrai eseguire un'Azione d'Attacco extra durante questo Turno. Non scegliere l'attaccante e il difensore del secondo Attacco, se non dopo aver risolto il primo.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cambiamenti": {
        "nome": "Cambiamenti",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediato",
        "timing": "Al costo di un'azione",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "1 Azione",
                "statistica_target": "",
                "descrizione_effetto": "I Tuoi Punti Promozione e quelli Destino possono essere scambiati liberamente con una proporzione di 5 Punti Destino per 1 Punto Promozione e viceversa",
                "condizioni": ["Giocabile al costo di un'azione"],
                "limitazioni": ["Proporzione fissa: 5 Punti Destino = 1 Punto Promozione"]
            }
        ],
        "testo_carta": "GIOCABILE AL COSTO DI UN'AZIONE. I Tuoi Punti Promozione e quelli Destino possono essere scambiati liberamente con una proporzione di 5 Punti Destino per 1 Punto Promozione e viceversa.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Essenza Di Rettitudine": {
        "nome": "Essenza Di Rettitudine",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero della Fratellanza nella tua squadra",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Immune agli effetti dell'Oscura Simmetria",
                "tipo_effetto": "Immunita",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Tutti gli Eretici in gioco devono scartare i loro Doni dell'Oscura Simmetria",
                "condizioni": ["Devi avere un guerriero della Fratellanza nella tua squadra"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. DEVI AVERE UN GUERRIERO DELLA FRATELLANZA NELLA TUA SQUADRA. Tutti gli Eretici in gioco devono scartare i loro Doni dell'Oscura Simmetria.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Devi avere un guerriero della Fratellanza nella tua squadra"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cambiamento Strategico": {
        "nome": "Cambiamento Strategico",
        "valore": "",
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Per questo turno",
        "timing": "In ogni momento durante il tuo turno, tranne durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Puoi riprendere in mano una delle Tue carte in gioco",
                "condizioni": ["Giocabile in ogni momento durante il tuo turno, tranne durante il combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO DURANTE IL TUO TURNO, TRANNE DURANTE IL COMBATTIMENTO. Puoi riprendere in mano una delle Tue carte in gioco.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Rinforzi": {
        "nome": "Rinforzi",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Rinforzo Squadra",
                "tipo_effetto": "Modificatore",
                "valore": "7D per compagno",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Per ogni 7D, un compagno della Squadra del guerriero vede la situazione e si unisce",
                "condizioni": ["Guerriero in combattimento", "Membri della Squadra disponibili"],
                "limitazioni": ["Solo membri non dell'Oscura Legione", "L'avversario può colpire solo uno del gruppo"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DURANTE IL COMBATTIMENTO. Per ogni 7D, un compagno della Squadra del guerriero, vede la situazione e si unisce a lui in battaglia! Membri di una Squadra non possono rinforzare l'Oscura Legione e viceversa. Il gruppo di guerrieri somma il valore delle caratteristiche d'Attacco. L'avversario può colpire solo uno del gruppo.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Non utilizzabile dall'Oscura Legione"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Marcia Forzata": {
        "nome": "Marcia Forzata",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Azione Extra",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "azioni",
                "descrizione_effetto": "Il giocatore può compiere un'Azione in meno nel Suo prossimo Turno",
                "condizioni": [],
                "limitazioni": ["Riduce le azioni del turno successivo"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN GIOCATORE IN OGNI MOMENTO. Il giocatore potrà compiere un'Azione in meno nel Suo prossimo Turno.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Ordini Fraintesi": {
        "nome": "Ordini Fraintesi",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Missione",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Una Missione, a Tua scelta, viene scartata",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Una Missione, a Tua scelta, viene scartata.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Fortuna": {
        "nome": "Fortuna",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Resto del gioco",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Fase Scartare",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Non devi scartare carte durante la Fase SCARTARE anche se hai più di 7 carte in mano",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Per il resto del gioco, non devi scartare carte durante la Fase \"SCARTARE\" anche se hai più di 7 carte in mano.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Missione Segreta": {
        "nome": "Missione Segreta",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Missione Segreta",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Puoi condurre una Missione in segreto. Una volta completata, mostrerai la carta Missione e devi essere capace di provare agli altri giocatori che l'hai conclusa in maniera corretta",
                "condizioni": ["Devi essere capace di provare che l'hai conclusa correttamente"],
                "limitazioni": []
            }
        ],
        "testo_carta": "Puoi condurre una Missione in segreto. Una volta completata, mostrerai la carta Missione e questa carta. Devi essere capace di provare agli altri giocatori che l'hai conclusa in maniera corretta. Guadagni tutti i benefici della Missione completata.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Svolta Del Destino": {
        "nome": "Svolta Del Destino",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Tira Moneta",
                "tipo_effetto": "Modificatore",
                "valore": "20D o -5 Punti Promozione",
                "statistica_target": "punti_destino",
                "descrizione_effetto": "Quando hai 5 Punti Promozione o più, tira una moneta. Se il risultato è testa, guadagni 20D. Se il risultato è croce, perdi 5 Punti Promozione",
                "condizioni": ["Avere 5 Punti Promozione o più"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO QUANDO HAI 5 PUNTI PROMOZIONE O PIU. Tira una moneta. Se il risultato è testa, guadagni 20D. Se il risultato è croce, perdi 5 Punti Promozione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Nascosto Nell'Ombra": {
        "nome": "Nascosto Nell'Ombra",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero",
        "durata": "Fino alla prossima fase Pescare",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Nascosto",
                "tipo_effetto": "Modificatore",
                "valore": 3,
                "statistica_target": "attacco",
                "descrizione_effetto": "Deve essere scartata nella prossima Fase Pescare. Nel frattempo, considera un +3 in A",
                "condizioni": [],
                "limitazioni": ["Deve essere scartata nella prossima Fase Pescare"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO IN OGNI MOMENTO. Questa carta deve essere scartata nella prossima Fase \"Pescare\". Nel frattempo, considera un +3 in A.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Forza Di Volonta": {
        "nome": "Forza Di Volonta",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerrieri del giocatore",
        "durata": "Fino all'inizio del prossimo turno",
        "timing": "In ogni momento",
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
                "descrizione_effetto": "I Tuoi guerrieri sono immuni alle carte dell'Oscura Simmetria fino all'inizio del Tuo prossimo Turno. I Tuoi guerrieri Legionari possono continuare a usare i Doni dell'Oscura Simmetria",
                "condizioni": [],
                "limitazioni": ["I guerrieri Legionari possono continuare a usare i Doni dell'Oscura Simmetria"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. I Tuoi guerrieri sono immuni alle carte dell'Oscura Simmetria fino all'inizio del Tuo prossimo Turno. I Tuoi guerrieri Legionari possono continuare a usare i Doni dell'Oscura Simmetria.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Colpo Potente": {
        "nome": "Colpo Potente",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento",
                "tipo_effetto": "Modificatore",
                "valore": 2,
                "statistica_target": "combattimento",
                "descrizione_effetto": "Il guerriero guadagna un +2 in C per questo combattimento",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DURANTE IL COMBATTIMENTO. Il guerriero guadagna un +2 in C per questo combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Prendere La Mira": {
        "nome": "Prendere La Mira",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Sparare",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "sparare",
                "descrizione_effetto": "Il guerriero guadagna un +1 in C e S",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE DURANTE I COMBATTIMENTI. Il guerriero guadagna un +1 in C e S.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Lama Spuntata": {
        "nome": "Lama Spuntata",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Arma da corpo a corpo durante il combattimento",
        "durata": "Un combattimento, poi utilizzabile dal turno successivo",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Disabilita Arma",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "equipaggiamento",
                "descrizione_effetto": "L'Arma è spuntata e non potrà essere utilizzata in questo combattimento. A partire dal prossimo Turno potrà essere nuovamente utilizzata",
                "condizioni": ["Arma da corpo a corpo"],
                "limitazioni": ["Non utilizzabile nel combattimento corrente"]
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI ARMA DA CORPO A CORPO DURANTE IL COMBATTIMENTO. L'Arma è spuntata e non potrà essere utilizzata in questo combattimento. A partire dal prossimo Turno potrà essere nuovamente utilizzata.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Nebbia Fitta": {
        "nome": "Nebbia Fitta",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Fino all'inizio del prossimo turno",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Riduce Visibilita",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "sparatoria",
                "descrizione_effetto": "Una Nebbia Fitta scende sul campo di battaglia, eliminando la visibilità. Si potrà combattere solo Corpo a Corpo fino all'inizio del Tuo prossimo Turno",
                "condizioni": [],
                "limitazioni": ["Solo combattimento corpo a corpo", "Termina qualsiasi sparatoria"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Una Nebbia Fitta scende sul campo di battaglia, eliminando la visibilità. Si potrà combattere solo Corpo a Corpo fino all'inizio del Tuo prossimo Turno. La Nebbia Fitta pone fine a qualsiasi sparatoria.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Vantaggio Tattico": {
        "nome": "Vantaggio Tattico",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
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
                "statistica_target": "tattica",
                "descrizione_effetto": "Puoi cambiare la Tattica di Combattimento per questo combattimento",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE DURANTE IL COMBATTIMENTO. Puoi cambiare la Tattica di Combattimento per questo combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Salvataggio Di Fortuna": {
        "nome": "Salvataggio Di Fortuna",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero ucciso",
        "durata": "Immediata",
        "timing": "Immediatamente dopo che un guerriero è stato ucciso",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Guarisce se stesso",
                "tipo_effetto": "Guarigione",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero non è morto, e rimane al suo status corrente",
                "condizioni": ["Guerriero appena ucciso"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE UNO DEI TUOI GUERRIERI È STATO UCCISO. Il guerriero non è morto, e rimane al suo status corrente.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Vittoria": {
        "nome": "Vittoria",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero dopo vittoria",
        "durata": "Immediata",
        "timing": "Dopo che un attaccante è sopravvissuto a un combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Punti Destino Extra",
                "tipo_effetto": "Modificatore",
                "valore": 5,
                "statistica_target": "punti_destino",
                "descrizione_effetto": "La battaglia è andata esattamente secondo i tuoi piani. Guadagni immediatamente 5D e se il Tuo guerriero era stato ferito, ritorna illeso",
                "condizioni": ["Attaccante sopravvissuto al combattimento"],
                "limitazioni": []
            },
            {
                "nome_effetto": "Guarisce se stesso",
                "tipo_effetto": "Guarigione",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Se il guerriero era ferito, ritorna illeso",
                "condizioni": ["Guerriero ferito"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE DOPO CHE UN TUO ATTACCANTE È SOPRAVVISSUTO A UN COMBATTIMENTO, ANCHE SE È STATO FERITO. La battaglia è andata esattamente secondo i tuoi piani. Guadagni immediatamente 5D e se il Tuo guerriero era stato ferito, ritorna illeso.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Documenti Persi": {
        "nome": "Documenti Persi",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Riduce Punti Promozione",
                "tipo_effetto": "Modificatore",
                "valore": -3,
                "statistica_target": "punti_promozione",
                "descrizione_effetto": "L'avversario perde 3 Punti Promozione",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI GIOCATORE IN OGNI MOMENTO. L'avversario perde 3 Punti Promozione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Andare Al Coperto": {
        "nome": "Andare Al Coperto",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero in combattimento (solo difensore)",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Riparo di Fortuna",
                "tipo_effetto": "Modificatore",
                "valore": 3,
                "statistica_target": "valore",
                "descrizione_effetto": "Il guerriero trova un riparo di fortuna. Gira la carta del guerriero, ma per questo primo Turno considera un +3 in V. Se il guerriero sopravvive (anche ferito), allora valgono le regole normali di ANDARE AL COPERTO",
                "condizioni": ["Solo se è il difensore"],
                "limitazioni": ["Solo difensore"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN TUO GUERRIERO IN COMBATTIMENTO, MA SOLO SE È IL DIFENSORE. Il guerriero trova un riparo di fortuna. Gira la carta del guerriero, ma per questo primo Turno considera un +3 in V. Se il guerriero sopravvive (anche ferito), allora valgono le regole normali di ANDARE AL COPERTO.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo difensore"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Ritirata": {
        "nome": "Ritirata",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Immediata",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Fuga dalla Battaglia",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il Tuo guerriero vede la futilità di questo scontro, e fugge dalla battaglia. Il combattimento è finito. Entrambi i guerrieri coinvolti nel combattimento tornano alle basi rispettive. Il Tuo avversario guadagna la metà dei punti V del guerriero codardo (arrotondati per eccesso)",
                "condizioni": [],
                "limitazioni": ["L'avversario guadagna metà punti V del guerriero"]
            }
        ],
        "testo_carta": "GIOCABILE DURANTE IL COMBATTIMENTO. Il Tuo guerriero vede la futilità di questo scontro, e fugge dalla battaglia. Il combattimento è finito. Entrambi i guerrieri coinvolti nel combattimento tornano alle basi rispettive. Il Tuo avversario guadagna la metà dei punti V del guerriero codardo (arrotondati per eccesso).",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Vigliiaccheria": {
        "nome": "Vigliiaccheria",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Tutti i guerrieri del giocatore",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Andare in Copertura Forzato",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Tutti i guerrieri del giocatore devono Andare in Copertura",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI GIOCATORE IN OGNI MOMENTO. Tutti i guerrieri del giocatore devono Andare in Copertura.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Attacco A Sorpresa": {
        "nome": "Attacco A Sorpresa",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Combattimento Non Simultaneo",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il combattimento non è simultaneo. Prima risolvi l'Attacco dell'attaccante. Se il difensore è ferito, il combattimento termina. Altrimenti, si risolverà anche l'Attacco del difensore",
                "condizioni": [],
                "limitazioni": ["Entrambi i giocatori devono aver giocato tutte le carte relative a questo combattimento"]
            }
        ],
        "testo_carta": "GIOCABILE DURANTE IL COMBATTIMENTO. Il combattimento non è simultaneo. Prima risolvi l'Attacco dell'attaccante. Se il difensore è ferito, il combattimento termina. Altrimenti, si risolverà anche l'Attacco del difensore. Quanto sopra accade dopo che entrambi i giocatori hanno giocato tutte le carte relative a questo combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Mentalmente Forte": {
        "nome": "Mentalmente Forte",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero",
        "durata": "Permanente",
        "timing": "In ogni momento",
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
                "descrizione_effetto": "Il guerriero diventerà immune agli effetti dell'Oscura Simmetria. Lascia questa carta vicino al guerriero",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO IN OGNI MOMENTO. Il guerriero diventerà immune agli effetti dell'Oscura Simmetria. Lascia questa carta vicino al guerriero.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Scoperto": {
        "nome": "Scoperto",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero in copertura",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Rimuove Copertura",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero è stato scoperto e perde gli effetti della copertura. Gira la carta a faccia in su",
                "condizioni": ["Guerriero in copertura"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI GUERRIERO IN COPERTURA IN OGNI MOMENTO. Il guerriero è stato scoperto e perde gli effetti della copertura. Gira la carta a faccia in su.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo su guerrieri in copertura"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Manifestazione Del Destino": {
        "nome": "Manifestazione Del Destino",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Resto della partita",
        "timing": "All'inizio della fase Pescare",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Pesca Extra",
                "tipo_effetto": "Modificatore",
                "valore": 10,
                "statistica_target": "pesca",
                "descrizione_effetto": "Per il resto della partita, durante Tua Fase PESCARE, potrai pescare carte fino ad averne un massimo di 10. Ricordati che durante la Fase SCARTARE non potrai avere in mano più di 10. Scarta le eccedenti",
                "condizioni": [],
                "limitazioni": ["Massimo 10 carte durante la fase SCARTARE"]
            }
        ],
        "testo_carta": "GIOCABILE ALL'INIZIO DELLA TUA FASE \"PESCARE\". Per il resto della partita, durante Tua Fase \"PESCARE\", potrai pescare carte fino ad averne un massimo di 10. Ricordati che durante la Fase \"SCARTARE\" non potrai avere in mano più di 10. Scarta le eccedenti.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Reintegrato": {
        "nome": "Reintegrato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Mercenario",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Statistiche",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "tutte",
                "descrizione_effetto": "La Corporazione ha rivalutato la sua posizione e ha deciso di reintegrarlo. Il guerriero potrà guadagnare Punti Promozione. Non viene più considerato un Mercenario e ottiene un +1 in C, S, A, V",
                "condizioni": ["Mercenario"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN MERCENARIO. La Corporazione ha rivalutato la sua posizione e ha deciso di reintegrarlo. Il guerriero potrà guadagnare Punti Promozione. Non viene più considerato un Mercenario e ottiene un +1 in C, S, A, V.",
        "flavour_text": "",
        "keywords": ["Mercenario"],
        "restrizioni": ["Solo su Mercenari"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Imboscata": {
        "nome": "Imboscata",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Combattimento Non Simultaneo",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il combattimento non è simultaneo. Prima risolvi l'attacco del difensore. Se l'attaccante è ferito, il combattimento è finito. Altrimenti, anche l'attaccante potrà risolvere il suo combattimento",
                "condizioni": [],
                "limitazioni": ["Accade dopo che entrambi hanno introdotto tutti i modificatori al combattimento"]
            }
        ],
        "testo_carta": "GIOCABILE DURANTE IL COMBATTIMENTO. Il combattimento non è simultaneo. Prima risolvi l'attacco del difensore. Se l'attaccante è ferito, il combattimento è finito. Altrimenti, anche l'attaccante potrà risolvere il suo combattimento. Quanto detto, comunque, accade dopo aver introdotto tutti i modificatori al combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cambiamento Della Fortuna": {
        "nome": "Cambiamento Della Fortuna",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scambia Punti Destino",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "punti_destino",
                "descrizione_effetto": "Puoi scambiare la Tua Pila Punti Destino con quella dell'avversario",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Puoi scambiare la Tua Pila Punti Destino con quella dell'avversario.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Azione Evasiva": {
        "nome": "Azione Evasiva",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Attacco",
                "tipo_effetto": "Modificatore",
                "valore": 2,
                "statistica_target": "attacco",
                "descrizione_effetto": "Il giocatore guadagna un +2 in A per questo combattimento",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DURANTE IL COMBATTIMENTO. Il giocatore guadagna un +2 in A per questo combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Comunicazione Errata": {
        "nome": "Comunicazione Errata",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore dopo aver giocato una carta",
        "durata": "Immediata",
        "timing": "Immediatamente dopo che un giocatore ha giocato una qualsiasi carta",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Annulla Carta",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "La carta appena giocata non ha nessun effetto sul gioco. Viene immediatamente scartata",
                "condizioni": ["Carta appena giocata"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE UN GIOCATORE HA GIOCATO UNA QUALSIASI CARTA. La carta appena giocata non ha nessun effetto sul gioco. Viene immediatamente scartata.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Tattica D'Evasione": {
        "nome": "Tattica D'Evasione",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero al costo di tre azioni",
        "durata": "Un combattimento",
        "timing": "Su ogni guerriero al costo di tre azioni",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Bonus Attacco per Spesa",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "attacco",
                "descrizione_effetto": "Il guerriero guadagna un +1 in A per ogni 2D spesi durante il combattimento. Questa carta rimane con il guerriero",
                "condizioni": ["Costo tre azioni"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI GUERRIERO AL COSTO DI TRE AZIONI. Il guerriero guadagna un +1 in A per ogni 2D spesi durante il combattimento. Questa carta rimane con il guerriero.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Fuoco Mirato": {
        "nome": "Fuoco Mirato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero al costo di tre azioni",
        "durata": "Un combattimento",
        "timing": "Su ogni guerriero al costo di tre azioni",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Bonus Sparare per Spesa",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "sparare",
                "descrizione_effetto": "Il guerriero guadagna un +1 in S per ogni 2D spesi durante il combattimento. Questa carta rimane con il guerriero",
                "condizioni": ["Costo tre azioni"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI GUERRIERO AL COSTO DI TRE AZIONI. Il guerriero guadagna un +1 in S per ogni 2D spesi durante il combattimento. Questa carta rimane con il guerriero.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Addestramento Efficiente": {
        "nome": "Addestramento Efficiente",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Carte Armi e Equipaggiamento",
        "durata": "Permanente",
        "timing": "Gioca questa carta costa un'azione",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Scambio Equipaggiamento",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Le carte Armi e Equipaggiamento possono essere scambiate tra i Tuoi guerrieri, indipendentemente dal fatto che facciano parte di una Squadra o di uno Schieramento",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCARE QUESTA CARTA COSTA UN'AZIONE. Le carte Armi e Equipaggiamento possono essere scambiate tra i Tuoi guerrieri, indipendentemente dal fatto che facciano parte di una Squadra o di uno Schieramento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Spia Nei Ranghi": {
        "nome": "Spia Nei Ranghi",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero avversario dopo missione o uccisione",
        "durata": "Immediata",
        "timing": "Immediatamente dopo che un guerriero avversario ha guadagnato punti per aver completato una missione o ucciso uno dei tuoi guerrieri",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Spia Attivata",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "punti_promozione",
                "descrizione_effetto": "Il guerriero che ha compiuto l'impresa era una Tua Spia. Guadagni i Suoi Punti e il Tuo avversario dovrà scartare la carta del guerriero",
                "condizioni": ["Guerriero avversario ha appena guadagnato punti"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE UN GUERRIERO AVVERSARIO HA GUADAGNATO PUNTI PER AVER COMPLETATO UNA MISSIONE O UCCISO UNO DEI TUOI GUERRIERI. Il guerriero che ha compiuto l'impresa era una Tua Spia. Guadagni i Suoi Punti e il Tuo avversario dovrà scartare la carta del guerriero.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Influenza": {
        "nome": "Influenza",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Riduce Punti Destino Avversario",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "punti_destino",
                "descrizione_effetto": "Per ogni punto D che spendi, l'avversario perderà 1D. Non potrai ridurre il suo numero di Punti Destino a zero o meno",
                "condizioni": [],
                "limitazioni": ["Non può ridurre i Punti Destino sotto zero"]
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI GIOCATORE IN OGNI MOMENTO. Per ogni punto D che spendi, l'avversario perderà 1D. Non potrai ridurre il suo numero di Punti Destino a zero o meno.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Fuoco Automatico": {
        "nome": "Fuoco Automatico",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero che usa mitragliatrice, mitragliatrice leggera o mitragliatrice pesante",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Raddoppia Bonus Arma",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "equipaggiamento",
                "descrizione_effetto": "Per questo combattimento, il bonus dato dall'Arma è raddoppiato",
                "condizioni": ["Guerriero con mitragliatrice, mitragliatrice leggera o mitragliatrice pesante"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE DURANTE IL COMBATTIMENTO, SU UN GUERRIERO CHE USA UNA MITRAGLIATRICE, UNA MITRAGLIATRICE LEGGERA O UN MITRAGLIATOIRE PESANTE. Per questo combattimento, il bonus dato dall'Arma è raddoppiato.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo con mitragliatrici"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "L'Eletto": {
        "nome": "L'Eletto",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero dell'Oscura Legione",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "A questo guerriero possono essere assegnati i Doni dell'Oscura Simmetria di qualsiasi Apostolo",
                "condizioni": ["Guerriero dell'Oscura Legione"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI GUERRIERO DELL'OSCURA LEGIONE IN OGNI MOMENTO. A questo guerriero possono essere assegnati i Doni dell'Oscura Simmetria di qualsiasi Apostolo.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Oscura Legione"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Ispirato": {
        "nome": "Ispirato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Azioni Extra",
                "tipo_effetto": "Modificatore",
                "valore": 3,
                "statistica_target": "azioni",
                "descrizione_effetto": "Potrai effettuare immediatamente tre Azioni escluso l'Attacco. Se giochi la carta durante il Tuo Turno, queste tre Azioni sono in aggiunta alle tre che Ti spettano di diritto",
                "condizioni": [],
                "limitazioni": ["Escluso l'Attacco"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Potrai effettuare immediatamente tre Azioni escluso l'Attacco. Se giochi la carta durante il Tuo Turno, queste tre Azioni sono in aggiunta alle tre che Ti spettano di diritto.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Servizio Deferente": {
        "nome": "Servizio Deferente",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Mishima"],
        "bersaglio": "Doomtrooper non Mishima",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cambia Fazione",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero sarà, da adesso in poi, considerato come un membro della Corporazione Mishima, ma rimarrà legato contemporaneamente anche alla Corporazione di partenza",
                "condizioni": ["Doomtrooper non Mishima"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER, NON MISHIMA, IN OGNI MOMENTO. Il guerriero sarà, da adesso in poi, considerato come un membro della Corporazione Mishima, ma rimarrà legato contemporaneamente anche alla Corporazione di partenza.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers non Mishima"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Essenza Di Integrita": {
        "nome": "Essenza Di Integrita",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore con guerriero della Fratellanza",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Ferisce Seguaci",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Tutti i Seguaci di Semai in gioco sono feriti e devono scartare tutte le loro carte dell'Oscura Simmetria",
                "condizioni": ["Avere un guerriero della Fratellanza nella squadra"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. DEVI AVERE UN GUERRIERO DELLA FRATELLANZA NELLA TUA SQUADRA. Tutti i Seguaci di Semai in gioco sono feriti e devono scartare tutte le loro carte dell'Oscura Simmetria.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Richiede guerriero della Fratellanza", "Seguaci di Semai"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Colpo Fortunato": {
        "nome": "Colpo Fortunato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Sparare",
                "tipo_effetto": "Modificatore",
                "valore": 2,
                "statistica_target": "sparare",
                "descrizione_effetto": "Il guerriero guadagna un +2 sulla caratteristica S per questo combattimento",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DURANTE IL COMBATTIMENTO. Il guerriero guadagna un +2 sulla caratteristica S per questo combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Corrotto Dall'Oscurita": {
        "nome": "Corrotto Dall'Oscurita",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Doomtrooper",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Converte in Eretico",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero è adesso, a tutti gli effetti, considerato un Eretico dell'Oscura Legione. Non è più un Doomtrooper. Tutte le carte che hanno effetto sugli Eretici, hanno effetto anche su questo guerriero, inoltre gli possono essere assegnate le carte DONI DELL'OSCURA LEGIONE",
                "condizioni": ["Doomtrooper"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER IN OGNI MOMENTO. Il guerriero è adesso, a tutti gli effetti, considerato un Eretico dell'Oscura Legione. Non è più un Doomtrooper. Tutte le carte che hanno effetto sugli Eretici, hanno effetto anche su questo guerriero, inoltre gli possono essere assegnate le carte DONI DELL'OSCURA LEGIONE.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Essenza Di Moralita": {
        "nome": "Essenza Di Moralita",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore con guerriero della Fratellanza",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Ferisce Seguaci",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Tutti i Seguaci di Demnogonis in gioco sono feriti e devono scartare tutte le loro carte dell'Oscura Simmetria",
                "condizioni": ["Avere un guerriero della Fratellanza nella squadra"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. DEVI AVERE UN GUERRIERO DELLA FRATELLANZA NELLA TUA SQUADRA. Tutti i Seguaci di Demnogonis in gioco sono feriti e devono scartare tutte le loro carte dell'Oscura Simmetria.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Richiede guerriero della Fratellanza", "Seguaci di Demnogonis"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Maestro Corrotto": {
        "nome": "Maestro Corrotto",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Eretico",
        "durata": "Resto della partita",
        "timing": "Assegnabile ad un Eretico in ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte",
                "tipo_effetto": "Arte",
                "valore": "3D",
                "statistica_target": "",
                "descrizione_effetto": "Per il resto della partita, l'Eretico a cui è stata assegnata la carta può lanciare ogni incantesimo dell'Arte al costo di 3D",
                "condizioni": ["Eretico"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ASSEGNABILE AD UN ERETICO IN OGNI MOMENTO. Per il resto della partita, l'Eretico a cui è stata assegnata la carta può lanciare ogni incantesimo dell'Arte al costo di 3D.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "restrizioni": ["Solo Eretici"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Arte Della Pace": {
        "nome": "Arte Della Pace",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero della Fratellanza",
        "durata": "Resto della partita",
        "timing": "Assegnabile ad ogni guerriero della Fratellanza in ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte",
                "tipo_effetto": "Arte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Per il resto della partita, il guerriero a cui è stata assegnata la carta, può lanciare ogni incantesimo dell'Arte non di combattimento",
                "condizioni": ["Guerriero della Fratellanza"],
                "limitazioni": ["Solo incantesimi non di combattimento"]
            }
        ],
        "testo_carta": "ASSEGNABILE AD OGNI GUERRIERO DELLA FRATELLANZA IN OGNI MOMENTO. Per il resto della partita, il guerriero a cui è stata assegnata la carta, può lanciare ogni incantesimo dell'Arte non di combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Addestramento Mistico": {
        "nome": "Addestramento Mistico",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Membro della Fratellanza",
        "durata": "Permanente",
        "timing": "Al costo di tre azioni",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Maestro in Arti",
                "tipo_effetto": "Arte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il membro della Fratellanza diventa un Maestro in tutte le ARTI. Questa carta rimane con il guerriero",
                "condizioni": ["Membro della Fratellanza", "Costo tre azioni"],
                "limitazioni": []
            }
        ],
        "testo_carta": "ASSEGNABILE A UN MEMBRO DELLA FRATELLANZA AL COSTO DI TRE AZIONI. Il membro della Fratellanza diventa un Maestro in tutte le ARTI. Questa carta rimane con il guerriero.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Malfunzionamento": {
        "nome": "Malfunzionamento",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Equipaggiamento",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Scegli un'Arma o un Equipaggiamento di un guerriero avversario e scartala",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI GUERRIERO IN OGNI MOMENTO. Scegli un'Arma o un Equipaggiamento di un guerriero avversario e scartala.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Battesimo Dell'Onore": {
        "nome": "Battesimo Dell'Onore",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Doomtrooper non affiliato alla Fratellanza o alla Cybertronic",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cambia Fazione",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero sarà considerato, d'ora in poi, un membro della Fratellanza, ma rimarrà legato contemporaneamente anche alla Corporazione di partenza. Questa carta non gli conferisce l'abilità di lanciare Incantesimi",
                "condizioni": ["Doomtrooper non affiliato alla Fratellanza o alla Cybertronic"],
                "limitazioni": ["Non conferisce abilità di lanciare Incantesimi"]
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER NON AFFILIATO ALLA FRATELLANZA O ALLA CYBERTRONIC, IN OGNI MOMENTO. Il guerriero sarà considerato, d'ora in poi, un membro della Fratellanza, ma rimarrà legato contemporaneamente anche alla Corporazione di partenza. Questa carta non gli conferisce l'abilità di lanciare Incantesimi.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers non Fratellanza o Cybertronic"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Empatia Di Premonizione": {
        "nome": "Empatia Di Premonizione",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Doomtrooper",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte di Premonizione",
                "tipo_effetto": "Arte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELLA PREMONIZIONE",
                "condizioni": ["Doomtrooper"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER IN OGNI MOMENTO. Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELLA PREMONIZIONE.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Empatia Esorcista": {
        "nome": "Empatia Esorcista",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Doomtrooper",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte dell'Esorcismo",
                "tipo_effetto": "Arte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELL'ESORCISMO",
                "condizioni": ["Doomtrooper"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER IN OGNI MOMENTO. Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELL'ESORCISMO.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Stigmate": {
        "nome": "Stigmate",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Eretico già in possesso di un Dono",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Riceve Doni Senza Costo",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il Dono in suo possesso gli ha corrotto irrimediabilmente l'anima, e non potrà mai essere convertito. Questo guerriero potrà, d'ora in poi, ricevere qualsiasi Dono di qualsiasi Apostolo senza consumare Azioni",
                "condizioni": ["Eretico già in possesso di un Dono"],
                "limitazioni": ["Non può essere convertito"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN ERETICO GIÀ IN POSSESSO DI UN DONO, IN OGNI MOMENTO. Il Dono in suo possesso gli ha corrotto irrimediabilmente l'anima, e non potrà mai essere convertito. Questo guerriero potrà, d'ora in poi, ricevere qualsiasi Dono di qualsiasi Apostolo senza consumare Azioni.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "restrizioni": ["Solo Eretici con Doni"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Carma Positivo": {
        "nome": "Carma Positivo",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Aggiunge Punti Destino",
                "tipo_effetto": "Modificatore",
                "valore": 10,
                "statistica_target": "punti_destino",
                "descrizione_effetto": "Aggiungi 10D nella Pila Destino",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Aggiungi 10D nella Pila Destino.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Quartier Generale Segreto": {
        "nome": "Quartier Generale Segreto",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Resto della partita",
        "timing": "Giocabile all'inizio della fase Pescare",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "5D per turno",
                "statistica_target": "punti_destino",
                "descrizione_effetto": "Spendi 5D e introduci questa carta al costo di un'Azione. Se non hai nessun guerriero in gioco, l'avversario non può attaccarti. Devi spendere, ogni Turno, 5D durante la Tua Fase PESCARE per tenere questa carta in gioco",
                "condizioni": ["Nessun guerriero in gioco"],
                "limitazioni": ["Costo di mantenimento 5D per turno", "Se non hai nessun guerriero l'avversario non può attaccarti"]
            }
        ],
        "testo_carta": "Spendi 5D e introduci questa carta al costo di un'Azione. Se non hai nessun guerriero in gioco, l'avversario non può attaccarti. Devi spendere, ogni Turno, 5D durante la Tua Fase \"PESCARE\" per tenere questa carta in gioco.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Ricerca Celere": {
        "nome": "Ricerca Celere",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "Durante il turno",
        "set_espansione": "Base",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Cerca, all'interno del Tuo mazzo, una carta. Quando l'hai trovata tienila in mano e mescola nuovamente il mazzo",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO, DURANTE IL TUO TURNO. Cerca, all'interno del Tuo mazzo, una carta. Quando l'hai trovata tienila in mano e mescola nuovamente il mazzo.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    # Inquisition

    "Formazione Serrata": {
        "nome": "Formazione Serrata",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero non-Personalità",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": "+2 in C, S, A e V",
                "statistica_target": "tutte",
                "descrizione_effetto": "Mentre la carta è in gioco, copie di questo guerriero possono unire le loro forze alle sue. Il gruppo combatte come un singolo guerriero e usa le caratteristiche originali, con un +2 in C, S, A e V per ogni guerriero in più nel gruppo",
                "condizioni": ["Guerriero non-Personalità"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO, SU QUALSIASI GUERRIERO NON-PERSONALITÀ, QUESTA CARTA RIMANE IN GIOCO. Mentre la carta è in gioco, copie di questo guerriero possono unire le loro forze alle sue. Il gruppo combatte come un singolo guerriero e usa le caratteristiche originali, con un +2 in C, S, A e V per ogni guerriero in più nel gruppo.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Non-Personalità"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Scetticismo": {
        "nome": "Scetticismo",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Campo di battaglia",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
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
                "descrizione_effetto": "Mentre è in gioco, i guerrieri della Fratellanza possono essere Attaccati dai Doomtrooper. Tuttavia i guerrieri della Fratellanza non possono Attaccare i Doomtrooper né possono Attaccarsi tra loro",
                "condizioni": [],
                "limitazioni": ["Guerrieri della Fratellanza non possono attaccare Doomtrooper o tra loro"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. QUESTA CARTA RIMANE IN GIOCO. Mentre è in gioco, i guerrieri della Fratellanza possono essere Attaccati dai Doomtrooper. Tuttavia i guerrieri della Fratellanza non possono Attaccare i Doomtrooper né possono Attaccarsi tra loro.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Maledizione Eterna": {
        "nome": "Maledizione Eterna",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero della Fratellanza",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Immune agli effetti delle carte Speciali",
                "tipo_effetto": "Immunita",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero non potrà più essere influenzato da altre carte Speciali a parte questa o da altre carte che la cancellino. Tutte le carte Speciali attualmente in gioco sul guerriero colpito, sono scartate",
                "condizioni": ["Guerriero della Fratellanza"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU QUALSIASI GUERRIERO DELLA FRATELLANZA, IN OGNI MOMENTO. QUESTA CARTA RIMANE IN GIOCO. Il guerriero non potrà più essere influenzato da altre carte Speciali a parte questa o da altre carte che la cancellino. Tutte le carte Speciali attualmente in gioco sul guerriero colpito, sono scartate.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Trasfigurazione": {
        "nome": "Trasfigurazione",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Eretico",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Converte in Seguace",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "L'Eretico è Trasfigurato. Togli la carta dell'Eretico e metti al suo posto un qualsiasi SEGUACE DI ALGEROTH NON-PERSONALITÀ preso dal Tuo mazzo di carte da Pescare. Devi pagare il normale V del SEGUACE in D",
                "condizioni": ["Eretico"],
                "limitazioni": ["Deve pagare il costo in D del Seguace"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO SU QUALSIASI ERETICO. L'Eretico è Trasfigurato. Togli la carta dell'Eretico e metti al suo posto un qualsiasi SEGUACE DI ALGEROTH NON-PERSONALITÀ preso dal Tuo mazzo di carte da Pescare. Devi pagare il normale V del SEGUACE in D.",
        "flavour_text": "",
        "keywords": ["Eretico", "Seguace di Algeroth"],
        "restrizioni": ["Solo Eretici"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Essenza Di Rettitudine": {
        "nome": "Essenza Di Rettitudine",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore con guerriero della Fratellanza nella squadra",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Doni dell'Oscura Simmetria",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Tutti gli Eretici in gioco devono scartare i loro Doni dell'Oscura Simmetria",
                "condizioni": ["Avere un guerriero della Fratellanza nella squadra"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. DEVI AVERE UN GUERRIERO DELLA FRATELLANZA NELLA TUA SQUADRA. Tutti gli Eretici in gioco devono scartare i loro Doni dell'Oscura Simmetria.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "restrizioni": ["Richiede guerriero della Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Mortificazione": {
        "nome": "Mortificazione",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero della Fratellanza",
        "durata": "Permanente",
        "timing": "Al costo di due azioni",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Uccide Automaticamente",
                "tipo_effetto": "Combattimento",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero ha imparato l'Arte segreta della Mortificazione. Gli avversari feriti in combattimento Corpo a Corpo sono automaticamente morti. NON DIVENTA COMUNQUE UN MORTIFICATOR",
                "condizioni": ["Guerriero della Fratellanza", "Costo due azioni"],
                "limitazioni": ["Solo in combattimento Corpo a Corpo"]
            }
        ],
        "testo_carta": "GIOCABILE SU QUALSIASI GUERRIERO DELLA FRATELLANZA AL COSTO DI DUE AZIONI. QUESTA CARTA RIMANE IN GIOCO. Il guerriero ha imparato l'Arte segreta della Mortificazione. Gli avversari feriti in combattimento Corpo a Corpo sono automaticamente morti. NON DIVENTA COMUNQUE UN MORTIFICATOR.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Il Primo Direttorato": {
        "nome": "Il Primo Direttorato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Squadra",
        "durata": "Permanente",
        "timing": "Al costo di un'azione",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte",
                "tipo_effetto": "Arte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Mentre il Primo Direttorato (i Mistici) è in gioco, tutti i Tuoi guerrieri della Fratellanza possono lanciare tutti gli incantesimo dell'Arte",
                "condizioni": ["Costo un'azione"],
                "limitazioni": []
            }
        ],
        "testo_carta": "PUOI ASSEGNARLO ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Mentre il Primo Direttorato (i Mistici) è in gioco, tutti i Tuoi guerrieri della Fratellanza possono lanciare tutti gli incantesimo dell'Arte.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "L'Anno Della Catastrofe": {
        "nome": "L'Anno Della Catastrofe",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Partita",
        "durata": "Permanente",
        "timing": "Al costo di tre azioni",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "5D",
                "statistica_target": "",
                "descrizione_effetto": "Devi spendere 5D per introdurre in gioco questa carta. Una volta giocata, tutte le carte Equipaggiamento in gioco di tutti i giocatori sono scartate e non se ne possono introdurre altre finché questa carta rimane in gioco",
                "condizioni": ["Costo tre azioni", "Costo 5D"],
                "limitazioni": ["Tutte le carte Equipaggiamento scartate", "Non si possono introdurre nuove carte Equipaggiamento"]
            }
        ],
        "testo_carta": "GIOCABILE AL COSTO DI TRE AZIONI. QUESTA CARTA RIMANE IN GIOCO. Devi spendere 5D per introdurre in gioco questa carta. Una volta giocata, tutte le carte Equipaggiamento in gioco di tutti i giocatori sono scartate e non se ne possono introdurre altre finché questa carta rimane in gioco.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "L'Ira Di Algeroth": {
        "nome": "L'Ira Di Algeroth",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Equipaggiamento",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Tutte le carte Equipaggiamento in gioco, sono scartate, eccetto quelle che sono nelle mani dei SEGUACI DI ALGEROTH",
                "condizioni": [],
                "limitazioni": ["Eccetto equipaggiamento dei Seguaci di Algeroth"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Tutte le carte Equipaggiamento in gioco, sono scartate, eccetto quelle che sono nelle mani dei SEGUACI DI ALGEROTH.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Maledizione Di Algeroth": {
        "nome": "Maledizione Di Algeroth",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero con Seguace di Algeroth nello schieramento",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Carte Speciali",
                "tipo_effetto": "Modificatore",
                "valore": "4D per carta",
                "statistica_target": "",
                "descrizione_effetto": "Puoi subito scartare una carta Speciale attualmente in gioco. Per ogni 4D che spendi, puoi scartare un'altra carta Speciale in gioco",
                "condizioni": ["Avere un Seguace di Algeroth nello schieramento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO SE HAI UN SEGUACE DI ALGEROTH NEL TUO SCHIERAMENTO. Puoi subito scartare una carta Speciale attualmente in gioco. Per ogni 4D che spendi, puoi scartare un'altra carta Speciale in gioco.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "restrizioni": ["Richiede Seguace di Algeroth nello schieramento"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },


    "Il Terzo Direttorato": {
        "nome": "Il Terzo Direttorato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Squadra",
        "durata": "Permanente",
        "timing": "Al costo di un'azione",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "punti_destino",
                "descrizione_effetto": "Mentre il Terzo Direttorato (la Missione) è in gioco, guadagni 1D durante la Tua Fase Pescare, per ogni guerriero della Fratellanza attualmente in gioco, anche quelli controllati da altri giocatori",
                "condizioni": ["Costo un'azione"],
                "limitazioni": []
            }
        ],
        "testo_carta": "PUOI AGGIUNGERE QUESTA CARTA ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Mentre il Terzo Direttorato (la Missione) è in gioco, guadagni 1D durante la Tua Fase Pescare, per ogni guerriero della Fratellanza attualmente in gioco, anche quelli controllati da altri giocatori.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Supporto Tattico": {
        "nome": "Supporto Tattico",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Rinforzo Squadra",
                "tipo_effetto": "Modificatore",
                "valore": "Ogni 7D",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Per ogni 7D, un compagno della Squadra del guerriero può vedere la situazione e si unisce a lui in battaglia. Compagni che non sono nel gruppo dell'Oscura Legione e viceversa. Il gruppo somma i valori di caratteristiche di attacco. L'avversario può colpire solo uno del gruppo durante il combattimento",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": ["Escluso Oscura Legione", "L'avversario può colpire solo uno del gruppo"]
            }
        ],
        "testo_carta": "GIOCABILE SU QUALSIASI GUERRIERO DURANTE IL COMBATTIMENTO. Per ogni 7D, un compagno della Squadra del guerriero può vedere la situazione e si unisce a lui in battaglia. Compagni che non sono nel gruppo dell'Oscura Legione e viceversa. Il gruppo somma i valori di caratteristiche di attacco. L'avversario può colpire solo uno del gruppo durante il combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Non Oscura Legione"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Evocazione Essenziale": {
        "nome": "Evocazione Essenziale",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero mentre sta usando un'Arte d'Evocazione",
        "durata": "Immediata",
        "timing": "Mentre un guerriero sta usando un'Arte d'Evocazione",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte",
                "tipo_effetto": "Arte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Puoi cercare nel Tuo mazzo di carte Scartate, senza pagare alcun D, per trovare la carta del tipo segnato sulla carta Arte d'Evocazione, o cercare nel Tuo mazzo di carte da Pescare al costo indicato per cercarle nel mazzo Scartate",
                "condizioni": ["Guerriero usando Arte d'Evocazione"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN TUO GUERRIERO MENTRE STA USANDO UN'ARTE D' EVOCAZIONE. Puoi cercare nel Tuo mazzo di carte Scartate, senza pagare alcun D, per trovare la carta del tipo segnato sulla carta Arte d'Evocazione, o cercare nel Tuo mazzo di carte da Pescare al costo indicato per cercarle nel mazzo Scartate.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Essenza Di Integrita": {
        "nome": "Essenza Di Integrita",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Giocatore con guerriero della Fratellanza nella squadra",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Ferisce Seguaci",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Tutti i Seguaci di Semai in gioco sono feriti e devono scartare tutte le loro carte dell'Oscura Simmetria",
                "condizioni": ["Avere un guerriero della Fratellanza nella squadra"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. DEVI AVERE UN GUERRIERO DELLA FRATELLANZA NELLA TUA SQUADRA. Tutti i Seguaci di Semai in gioco sono feriti e devono scartare tutte le loro carte dell'Oscura Simmetria.",
        "flavour_text": "",
        "keywords": ["Seguace di Semai"],
        "restrizioni": ["Richiede guerriero della Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Incantesimo Preferito": {
        "nome": "Incantesimo Preferito",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero subito dopo che un incantesimo dell'Arte è stato giocato",
        "durata": "Immediata",
        "timing": "Subito dopo che un incantesimo dell'Arte è stato giocato",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Ripete Incantesimo",
                "tipo_effetto": "Arte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "L'incantesimo che è appena stato lanciato ritorna in mano a chi lo ha giocato. Questa carta non ha effetto su incantesimi che devono essere eliminati dal gioco dopo l'uso",
                "condizioni": ["Incantesimo appena lanciato"],
                "limitazioni": ["Non funziona su incantesimi eliminati dopo l'uso"]
            }
        ],
        "testo_carta": "GIOCABILE SUBITO DOPO CHE UN INCANTESIMO DELL'ARTE È STATO GIOCATO. L'incantesimo che è appena stato lanciato ritorna in mano a chi lo ha giocato. QUESTA CARTA NON HA EFFETTO SU INCANTESIMI CHE DEVONO ESSERE ELIMINATI DAL GIOCO DOPO L'USO.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Depredato": {
        "nome": "Depredato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero dopo aver ucciso un altro in combattimento",
        "durata": "Immediata, poi permanente",
        "timing": "Immediatamente dopo che il tuo guerriero ne ha ucciso un altro in combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Prende Equipaggiamento",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Puoi prendere una carta Equipaggiamento del guerriero ucciso per equipaggiare un Tuo guerriero. Il CORNA DI LEGAME del nuovo possessore è irrilevante. Alla fine del gioco, rendi la carta al suo possessore!",
                "condizioni": ["Guerriero ha appena ucciso un altro"],
                "limitazioni": ["Deve restituire la carta a fine gioco"]
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE IL TUO GUERRIERO NE HA UCCISO UN ALTRO IN COMBATTIMENTO. Puoi prendere una carta Equipaggiamento del guerriero ucciso per equipaggiare un Tuo guerriero. Il CORNA DI LEGAME del nuovo possessore è irrilevante. Alla fine del gioco, rendi la carta al suo possessore!",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Empatia Della Manipolazione": {
        "nome": "Empatia Della Manipolazione",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Doomtrooper",
        "durata": "Permanente",
        "timing": "Su ogni Doomtrooper in ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte della Manipolazione",
                "tipo_effetto": "Arte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELLA MANIPOLAZIONE",
                "condizioni": ["Doomtrooper"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER IN OGNI MOMENTO. Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELLA MANIPOLAZIONE.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "La Desolazione Di Thadeus": {
        "nome": "La Desolazione Di Thadeus",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Permanente",
        "timing": "In qualsiasi momento",
        "set_espansione": "Inquisition",
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
                "descrizione_effetto": "Quando questa carta è in gioco, i guerrieri non possono andare in Copertura. Arida e sterile, questa landa desolata offre ben pochi ripari naturali",
                "condizioni": [],
                "limitazioni": ["I guerrieri non possono andare in Copertura"]
            }
        ],
        "testo_carta": "GIOCABILE IN QUALSIASI MOMENTO. QUESTA CARTA RIMANE IN GIOCO. Quando questa carta è in gioco, i guerrieri non possono andare in Copertura. Arida e sterile, questa landa desolata offre ben pochi ripari naturali.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Tangente": {
        "nome": "Tangente",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Tutti i giocatori",
        "durata": "Fino alla carta viene scartata",
        "timing": "Al costo di un'azione",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Tassa su Fratellanza",
                "tipo_effetto": "Modificatore",
                "valore": "2D per guerriero",
                "statistica_target": "punti_destino",
                "descrizione_effetto": "Ogni giocatore Ti deve dare 2D per ogni guerriero della Fratellanza nella sua Squadra (non Schieramento). Se un giocatore non ha abbastanza D, prendi il resto dalla pila comune dopodiché scarta questa carta",
                "condizioni": ["Costo un'azione"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE AL COSTO DI UN'AZIONE. Ogni giocatore Ti deve dare 2D per ogni guerriero della Fratellanza nella sua Squadra (non Schieramento). Se un giocatore non ha abbastanza D, prendi il resto dalla pila comune dopodiché scarta questa carta.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Empatia Cinetica": {
        "nome": "Empatia Cinetica",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Doomtrooper",
        "durata": "Permanente",
        "timing": "Su ogni Doomtrooper in ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte della Cinetica",
                "tipo_effetto": "Arte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELLA CINETICA",
                "condizioni": ["Doomtrooper"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER IN OGNI MOMENTO. Il guerriero potrà, d'ora in poi, lanciare gli Incantesimi ARTE DELLA CINETICA.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cecchino!": {
        "nome": "Cecchino!",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Personalità al costo di due azioni",
        "durata": "Permanente",
        "timing": "Su qualsiasi Personalità al costo di due azioni",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "4D",
                "statistica_target": "",
                "descrizione_effetto": "Se può partecipare al combattimento. La Personalità è il bersaglio dell'Attacco di Cecchino. Il possessore della Personalità, ogni Turno, deve spendere 4D durante la sua Fase Pescare, prima di pescare ogni carta, oppure viene ucciso. Se la Personalità muore, guadagni i Punti. Più carte Cecchino possono essere giocate contemporaneamente",
                "condizioni": ["Personalità", "Costo due azioni"],
                "limitazioni": ["Può partecipare al combattimento"]
            }
        ],
        "testo_carta": "GIOCABILE SU QUALSIASI PERSONALITÀ AL COSTO DI DUE AZIONI, SE PUÒ PARTECIPARE AL COMBATTIMENTO. La Personalità è il bersaglio dell'Attacco di Cecchino. Il possessore della Personalità, ogni Turno, deve spendere 4D durante la sua Fase Pescare, prima di pescare ogni carta, oppure viene ucciso. Se la Personalità muore, guadagni i Punti. Più carte Cecchino possono essere giocate contemporaneamente.",
        "flavour_text": "",
        "keywords": ["Personalita"],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Situazione Disperata": {
        "nome": "Situazione Disperata",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Resto del gioco",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Guadagna Punti Destino",
                "tipo_effetto": "Modificatore",
                "valore": "25D",
                "statistica_target": "punti_destino",
                "descrizione_effetto": "Ogni giocatore può guadagnare 25D se vuole. Essi vengono sistemati separati dalla Pila dei Punti Destino e non possono mai essere toccati dagli altri giocatori. Per il resto del gioco, il giocatore che prende i 25D non può più compiere Azioni di Meditazione",
                "condizioni": [],
                "limitazioni": ["25D separati e intoccabili", "Non può più compiere Azioni di Meditazione"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Ogni giocatore può guadagnare 25D se vuole. Essi vengono sistemati separati dalla Pila dei Punti Destino e non possono mai essere toccati dagli altri giocatori. Per il resto del gioco, il giocatore che prende i 25D non può più compiere Azioni di Meditazione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Lotta Senza Quartiere": {
        "nome": "Lotta Senza Quartiere",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Permanente",
        "timing": "Durante il tuo turno, prima che tu compia altre azioni",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "20D extra per attacco",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Tutti i giocatori possono compiere più di un'Azione di Attacco fino all'inizio del Tuo prossimo Turno. Ogni Attacco extra costa 20D. Un giocatore non può eseguire più Azioni di Attacco di quante ne abbia a disposizione. Ogni Attacco viene risolto separatamente",
                "condizioni": [],
                "limitazioni": ["Ogni attacco extra costa 20D", "Limitato dalle azioni disponibili"]
            }
        ],
        "testo_carta": "GIOCABILE DURANTE IL TUO TURNO, PRIMA CHE TU COMPIA ALTRE AZIONI. Tutti i giocatori possono compiere più di un'Azione di Attacco fino all'inizio del Tuo prossimo Turno. Ogni Attacco extra costa 20D. Un giocatore non può eseguire più Azioni di Attacco di quante ne abbia a disposizione. Ogni Attacco viene risolto separatamente.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Il Quarto Direttorato": {
        "nome": "Il Quarto Direttorato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Squadra",
        "durata": "Permanente",
        "timing": "Al costo di un'azione",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Azione Extra",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "azioni",
                "descrizione_effetto": "Mentre il Quarto Direttorato (l'Amministrazione) è in gioco, puoi compiere un'Azione extra non di Attacco ogni Turno. Solo una carta QUARTO DIRETTORATO per giocatore è ammessa in gioco",
                "condizioni": ["Costo un'azione"],
                "limitazioni": ["Azione extra non di Attacco", "Una sola carta per giocatore"]
            }
        ],
        "testo_carta": "PUOI AGGIUNGERE QUESTA CARTA ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Mentre il Quarto Direttorato (l'Amministrazione) è in gioco, puoi compiere un'Azione extra non di Attacco ogni Turno. Solo una carta QUARTO DIRETTORATO per giocatore è ammessa in gioco.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Impeto Di Giustizia": {
        "nome": "Impeto Di Giustizia",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Campo di battaglia",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Elimina Guerrieri",
                "tipo_effetto": "Modificatore",
                "valore": "10D per eliminazione",
                "statistica_target": "",
                "descrizione_effetto": "Per ogni 10D spesi, un guerriero qualsiasi in gioco, indipendentemente dall'ICONA DI LEGAME, è scartato. Questo non viene considerato un Attacco",
                "condizioni": [],
                "limitazioni": ["Non considerato un Attacco", "Carta eliminata dal gioco dopo l'uso"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. ELIMINA QUESTA CARTA DAL GIOCO DOPO L'USO. Per ogni 10D spesi, un guerriero qualsiasi in gioco, indipendentemente dall'ICONA DI LEGAME, è scartato. Questo non viene considerato un Attacco.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Sdoppiamento": {
        "nome": "Sdoppiamento",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero",
        "durata": "Permanente",
        "timing": "Al costo di un'azione",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Crea Copia",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Scegli un guerriero in gioco. Questa carta è considerata una sua copia esatta. Le abilità che una delle due carte ha o riceve, interessano entrambi i guerrieri. Se uno dei due viene ferito o ucciso, entrambe le carte sono coinvolte. Il guerriero non può mai attaccare il suo doppio",
                "condizioni": ["Costo un'azione"],
                "limitazioni": ["Effetti condivisi tra le copie", "Non può attaccare il proprio doppio"]
            }
        ],
        "testo_carta": "GIOCABILE AL COSTO DI UN'AZIONE. Scegli un guerriero in gioco. Questa carta è considerata una sua copia esatta. Le abilità che una delle due carte ha o riceve, interessano entrambi i guerrieri. Se uno dei due viene ferito o ucciso, entrambe le carte sono coinvolte. Il guerriero non può mai attaccare il suo doppio.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Il Secondo Direttorato": {
        "nome": "Il Secondo Direttorato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Squadra",
        "durata": "Permanente",
        "timing": "Assegnabile alla tua squadra, al costo di un'azione",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Uccide Automaticamente",
                "tipo_effetto": "Combattimento",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Mentre il Secondo Direttorato (l'Inquisizione) è in gioco, puoi uccidere direttamente gli avversari feriti dai Tuoi guerrieri della Fratellanza, ma solo se paghi un numero di D pari al loro V. Altrimenti, sono solo feriti",
                "condizioni": ["Costo un'azione", "Avversari già feriti da guerrieri della Fratellanza"],
                "limitazioni": ["Costo D pari al V del bersaglio"]
            }
        ],
        "testo_carta": "ASSEGNABILE ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Mentre il Secondo Direttorato (l'Inquisizione) è in gioco, puoi uccidere direttamente gli avversari feriti dai Tuoi guerrieri della Fratellanza, ma solo se paghi un numero di D pari al loro V. Altrimenti, sono solo feriti.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Carica!": {
        "nome": "Carica!",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero al coperto",
        "durata": "Un combattimento",
        "timing": "Su uno dei tuoi guerrieri al coperto, al costo di tre azioni",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento per Uscita Coperto",
                "tipo_effetto": "Modificatore",
                "valore": "+2 in C e S",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Il guerriero può immediatamente uscire allo scoperto e Attaccare con un +2 in C e S. Questa è considerata un'Azione di Attacco. Dopo il combattimento, il guerriero NON È PIÙ AL COPERTO",
                "condizioni": ["Guerriero al coperto", "Costo tre azioni"],
                "limitazioni": ["Dopo il combattimento non è più al coperto"]
            }
        ],
        "testo_carta": "GIOCABILE SU UNO DEI TUOI GUERRIERI AL COPERTO, AL COSTO DI TRE AZIONI. Il guerriero può immediatamente uscire allo scoperto e Attaccare con un +2 in C e S. Questa è considerata un'Azione di Attacco. Dopo il combattimento, il guerriero NON È PIÙ AL COPERTO.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo guerrieri al coperto"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Empatia D'Evocazione": {
        "nome": "Empatia D'Evocazione",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero della Fratellanza",
        "durata": "Permanente",
        "timing": "Su uno dei tuoi guerrieri della Fratellanza, al costo di un'azione",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte d'Evocazione",
                "tipo_effetto": "Arte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "D'ora in poi, tutti i guerrieri della Fratellanza nella Tua Squadra potranno usare l'Arte d'Evocazione. Se il guerriero viene ucciso, questa carta è scartata",
                "condizioni": ["Guerriero della Fratellanza", "Costo un'azione"],
                "limitazioni": ["Se il guerriero bersaglio muore, la carta è scartata"]
            }
        ],
        "testo_carta": "GIOCABILE SU UNO DEI TUOI GUERRIERI DELLA FRATELLANZA, AL COSTO DI UN'AZIONE. D'ora in poi, tutti i guerrieri della Fratellanza nella Tua Squadra potranno usare l'Arte d'Evocazione. Se il guerriero viene ucciso, questa carta è scartata.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },    

    "Appropriazione Indebita": {
        "nome": "Appropriazione Indebita",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Prende Punti Destino",
                "tipo_effetto": "Modificatore",
                "valore": "Metà dei D dell'avversario",
                "statistica_target": "punti_destino",
                "descrizione_effetto": "Prendi la metà dei D dell'avversario (arrotondato per difetto). Se l'avversario ha D dispari, l'ultimo D va a lui",
                "condizioni": [],
                "limitazioni": ["Arrotondamento per difetto"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Prendi la metà dei D dell'avversario (arrotondato per difetto). Se l'avversario ha D dispari, l'ultimo D va a lui.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Contrattacco": {
        "nome": "Contrattacco",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Combattimento Non Simultaneo",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il combattimento non è simultaneo. Prima risolvi l'attacco del difensore. Se l'attaccante è ferito, il combattimento è finito. Altrimenti, anche l'attaccante potrà risolvere il suo combattimento. Quanto detto, comunque, accade dopo aver introdotto tutti i modificatori al combattimento",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": ["Dopo aver introdotto tutti i modificatori"]
            }
        ],
        "testo_carta": "GIOCABILE DURANTE IL COMBATTIMENTO. Il combattimento non è simultaneo. Prima risolvi l'attacco del difensore. Se l'attaccante è ferito, il combattimento è finito. Altrimenti, anche l'attaccante potrà risolvere il suo combattimento. Quanto detto, comunque, accade dopo aver introdotto tutti i modificatori al combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Sbarramento D'Artiglieria": {
        "nome": "Sbarramento D'Artiglieria",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Ferisce Tutti",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Tutti i guerrieri in gioco sono feriti",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Tutti i guerrieri in gioco sono feriti.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Campo Di Sterminio": {
        "nome": "Campo Di Sterminio",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
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
                "descrizione_effetto": "Questa carta rimane in gioco. I guerrieri feriti non possono andare in copertura o essere guariti. Possono però essere uccisi",
                "condizioni": [],
                "limitazioni": ["Guerrieri feriti non possono andare in copertura", "Guerrieri feriti non possono essere guariti"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. QUESTA CARTA RIMANE IN GIOCO. I guerrieri feriti non possono andare in copertura o essere guariti. Possono però essere uccisi.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Incontro Ravvicinato": {
        "nome": "Incontro Ravvicinato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
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
                "descrizione_effetto": "Questa carta rimane in gioco. Si può combattere solo Corpo a Corpo. La caratteristica S di tutti i guerrieri diventa inutile",
                "condizioni": [],
                "limitazioni": ["Solo combattimento Corpo a Corpo", "Caratteristica S inutile"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. QUESTA CARTA RIMANE IN GIOCO. Si può combattere solo Corpo a Corpo. La caratteristica S di tutti i guerrieri diventa inutile.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Sabotaggio": {
        "nome": "Sabotaggio",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Carta Speciale in gioco",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Carte Speciali",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Scegli una carta Speciale in gioco e scartala",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Scegli una carta Speciale in gioco e scartala.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Intimidazione": {
        "nome": "Intimidazione",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero non-Personalità",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
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
                "descrizione_effetto": "Il guerriero è intimidito e non può compiere Azioni di Attacco",
                "condizioni": ["Guerriero non-Personalità"],
                "limitazioni": ["Non può compiere Azioni di Attacco"]
            }
        ],
        "testo_carta": "GIOCABILE SU QUALSIASI GUERRIERO NON-PERSONALITÀ IN OGNI MOMENTO. QUESTA CARTA RIMANE IN GIOCO. Il guerriero è intimidito e non può compiere Azioni di Attacco.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Non-Personalità"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Tregua": {
        "nome": "Tregua",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Fino all'inizio del prossimo turno",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
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
                "descrizione_effetto": "Nessun guerriero può compiere o subire Azioni di Attacco fino all'inizio del Tuo prossimo Turno",
                "condizioni": [],
                "limitazioni": ["Nessuna azione di attacco possibile"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Nessun guerriero può compiere o subire Azioni di Attacco fino all'inizio del Tuo prossimo Turno.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Vendetta": {
        "nome": "Vendetta",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero dopo che un altro della stessa squadra è stato ucciso",
        "durata": "Resto della partita",
        "timing": "Immediatamente dopo che un guerriero della tua squadra è stato ucciso",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Permanente",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in tutte le caratteristiche",
                "statistica_target": "tutte",
                "descrizione_effetto": "Il guerriero guadagna un +1 permanente in tutte le sue caratteristiche per il resto della partita",
                "condizioni": ["Guerriero della stessa squadra ucciso"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE UN GUERRIERO DELLA TUA SQUADRA È STATO UCCISO. QUESTA CARTA RIMANE IN GIOCO. Il guerriero guadagna un +1 permanente in tutte le sue caratteristiche per il resto della partita.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Trasferimento": {
        "nome": "Trasferimento",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cambia Controllo",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Scegli un guerriero di un altro giocatore. Quel guerriero passa sotto il Tuo controllo. Se il guerriero muore, l'altro giocatore perde i Punti Promozione",
                "condizioni": [],
                "limitazioni": ["Se muore, l'altro giocatore perde i Punti Promozione"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Scegli un guerriero di un altro giocatore. Quel guerriero passa sotto il Tuo controllo. Se il guerriero muore, l'altro giocatore perde i Punti Promozione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Mercato Nero": {
        "nome": "Mercato Nero",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scambia Carte",
                "tipo_effetto": "Carte",
                "valore": "5D per carta",
                "statistica_target": "",
                "descrizione_effetto": "Puoi scambiare le carte della Tua mano con quelle del mazzo Scartate. Ogni carta costa 5D",
                "condizioni": [],
                "limitazioni": ["Costo 5D per carta"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Puoi scambiare le carte della Tua mano con quelle del mazzo Scartate. Ogni carta costa 5D.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Medico Da Campo": {
        "nome": "Medico Da Campo",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero ferito",
        "durata": "Immediata",
        "timing": "In ogni momento",
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
                "statistica_target": "",
                "descrizione_effetto": "Un guerriero ferito guarisce",
                "condizioni": ["Guerriero ferito"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Un guerriero ferito guarisce.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Colpo Sporco": {
        "nome": "Colpo Sporco",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Uccide Automaticamente",
                "tipo_effetto": "Combattimento",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Se il guerriero ferisce l'avversario, l'avversario viene automaticamente ucciso",
                "condizioni": ["Durante il combattimento", "Deve ferire l'avversario"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DURANTE IL COMBATTIMENTO. Se il guerriero ferisce l'avversario, l'avversario viene automaticamente ucciso.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Ricerca E Distruzione": {
        "nome": "Ricerca E Distruzione",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero in copertura",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Uccide Automaticamente",
                "tipo_effetto": "Combattimento",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Un guerriero Al Coperto viene automaticamente ucciso",
                "condizioni": ["Guerriero Al Coperto"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Un guerriero Al Coperto viene automaticamente ucciso.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Promozione Sul Campo": {
        "nome": "Promozione Sul Campo",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero non-Personalità dopo aver ucciso in combattimento",
        "durata": "Permanente",
        "timing": "Immediatamente dopo che un guerriero non-Personalità ha ucciso un avversario in combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Diventa Personalità",
                "tipo_effetto": "Modificatore",
                "valore": "+1 tutte le caratteristiche",
                "statistica_target": "tutte",
                "descrizione_effetto": "Il guerriero non-Personalità diventa una Personalità e guadagna un +1 in tutte le sue caratteristiche. D'ora in poi è considerato una Personalità a tutti gli effetti",
                "condizioni": ["Guerriero non-Personalità", "Ha appena ucciso un avversario"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE UN GUERRIERO NON-PERSONALITÀ HA UCCISO UN AVVERSARIO IN COMBATTIMENTO. QUESTA CARTA RIMANE IN GIOCO. Il guerriero non-Personalità diventa una Personalità e guadagna un +1 in tutte le sue caratteristiche. D'ora in poi è considerato una Personalità a tutti gli effetti.",
        "flavour_text": "",
        "keywords": ["Personalita"],
        "restrizioni": ["Solo guerrieri non-Personalità"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Copertura Di Fuoco": {
        "nome": "Copertura Di Fuoco",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Sparare",
                "tipo_effetto": "Modificatore",
                "valore": "+3 in S",
                "statistica_target": "sparare",
                "descrizione_effetto": "Il guerriero guadagna un +3 in S per questo combattimento",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DURANTE IL COMBATTIMENTO. Il guerriero guadagna un +3 in S per questo combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Azione Concertata": {
        "nome": "Azione Concertata",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Un turno",
        "timing": "All'inizio del tuo turno",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Azioni Extra",
                "tipo_effetto": "Modificatore",
                "valore": "Azioni pari ai guerrieri in gioco",
                "statistica_target": "azioni",
                "descrizione_effetto": "Puoi compiere tante Azioni quanti sono i Tuoi guerrieri attualmente in gioco, invece delle solite tre",
                "condizioni": ["All'inizio del tuo turno"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE ALL'INIZIO DEL TUO TURNO. Puoi compiere tante Azioni quanti sono i Tuoi guerrieri attualmente in gioco, invece delle solite tre.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Dichiarazione Di Guerra": {
        "nome": "Dichiarazione Di Guerra",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in C per tutti",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Questa carta rimane in gioco. Tutti i guerrieri guadagnano un +1 in C per il resto della partita",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. QUESTA CARTA RIMANE IN GIOCO. Tutti i guerrieri guadagnano un +1 in C per il resto della partita.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Disinformazione": {
        "nome": "Disinformazione",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Avversario",
        "durata": "Resto del turno",
        "timing": "All'inizio del turno dell'avversario",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Riduce Azioni",
                "tipo_effetto": "Modificatore",
                "valore": -1,
                "statistica_target": "azioni",
                "descrizione_effetto": "L'avversario può compiere solo due Azioni in questo Turno",
                "condizioni": ["All'inizio del turno dell'avversario"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE ALL'INIZIO DEL TURNO DELL'AVVERSARIO. L'avversario può compiere solo due Azioni in questo Turno.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Imboscata": {
        "nome": "Imboscata",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero che ha appena schierato",
        "durata": "Immediata",
        "timing": "Immediatamente dopo che un guerriero è stato schierato",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Attacco Automatico",
                "tipo_effetto": "Combattimento",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Un Tuo guerriero può immediatamente Attaccare il guerriero appena schierato. Questo non viene considerato un'Azione di Attacco",
                "condizioni": ["Guerriero appena schierato"],
                "limitazioni": ["Non considerato Azione di Attacco"]
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE UN GUERRIERO È STATO SCHIERATO. Un Tuo guerriero può immediatamente Attaccare il guerriero appena schierato. Questo non viene considerato un'Azione di Attacco.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },    

    # Warzone

    "Grandi Manovre": {
        "nome": "Grandi Manovre",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "In ogni momento ad eccezione dei combattimenti",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Azione Extra",
                "tipo_effetto": "Modificatore",
                "valore": 1,
                "statistica_target": "azioni",
                "descrizione_effetto": "Tu puoi immediatamente eseguire un'Azione d'Attacco con uno dei tuoi guerrieri",
                "condizioni": ["Escluso durante i combattimenti"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO AD ECCEZIONE DEI COMBATTIMENTI. Tu puoi immediatamente eseguire un'Azione d'Attacco con uno dei tuoi guerrieri.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Artiglieria Di Supporto": {
        "nome": "Artiglieria Di Supporto",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Durante il combattimento",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento",
                "tipo_effetto": "Modificatore",
                "valore": "+5 in S durante questo combattimento",
                "statistica_target": "sparare",
                "descrizione_effetto": "Il guerriero guadagna un +5 in S durante questo combattimento. Questa carta non ha effetto se il guerriero avversario utilizza un VEICOLO o è considerato AERONAVI, CARRO ARMATO o VEICOLO",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": ["Non ha effetto contro VEICOLO, AERONAVI, CARRO ARMATO"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DURANTE IL COMBATTIMENTO. Il guerriero guadagna un +5 in S durante questo combattimento. Questa carta non ha effetto se il guerriero avversario utilizza un VEICOLO o è considerato AERONAVI, CARRO ARMATO o VEICOLO.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Sicario Assoldato": {
        "nome": "Sicario Assoldato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Doomtrooper",
                "tipo_effetto": "Modificatore",
                "valore": "8D",
                "statistica_target": "",
                "descrizione_effetto": "Una volta usata rimuovi questa carta dal gioco. Al costo di 8D puoi scartare un Doomtrooper qualsiasi in gioco. Questa non è considerata un'Azione d'Attacco",
                "condizioni": ["Costo 8D"],
                "limitazioni": ["Carta rimossa dal gioco dopo l'uso", "Non considerata Azione d'Attacco"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. UNA VOLTA USATA RIMUOVI QUESTA CARTA DAL GIOCO. Al costo di 8D puoi scartare un Doomtrooper qualsiasi in gioco. Questa non è considerata un'Azione d'Attacco.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Impegno Programmato": {
        "nome": "Impegno Programmato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero",
        "durata": "Permanente",
        "timing": "Al costo di due azioni",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": 2,
                "statistica_target": "",
                "descrizione_effetto": "Scegli un tipo di COMANDANTE tra SERGENTE e CAPITANO. Tutti i guerrieri con quel grado sono scartati e mescolati nel mazzo di carte da pescare. Tutte le carte equipaggiamento assegnate saranno a loro volta mescolate nel mazzo di carte da pescare. Le carte speciali verranno invece poste nella pila di carte scartate",
                "condizioni": ["Costo due azioni"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE AL COSTO DI DUE AZIONI. Scegli un tipo di COMANDANTE tra SERGENTE e CAPITANO. Tutti i guerrieri con quel grado sono scartati e mescolati nel mazzo di carte da pescare. Tutte le carte equipaggiamento assegnate saranno a loro volta mescolate nel mazzo di carte da pescare. Le carte speciali verranno invece poste nella pila di carte scartate.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Guastatore": {
        "nome": "Guastatore",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Doomtrooper",
        "durata": "Permanente",
        "timing": "In ogni momento",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Fortificazione e Warzone",
                "tipo_effetto": "Carte",
                "valore": "3 azioni e 1 punto promozione",
                "statistica_target": "",
                "descrizione_effetto": "Questo guerriero può scartare una Fortificazione o una WARZONE al costo di tre Azioni e un Punto Promozione. Nessun Campo Minato ha effetto se hai un Guastatore nella tua Squadra. Giocando questa carta cancelli l'effetto di un Campo Minato appena giocato",
                "condizioni": ["Doomtrooper"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO SU UN DOOMTROOPER. QUESTA CARTA RIMANE IN GIOCO. Questo guerriero può scartare una Fortificazione o una WARZONE al costo di tre Azioni e un Punto Promozione. Nessun Campo Minato ha effetto se hai un Guastatore nella tua Squadra. Giocando questa carta cancelli l'effetto di un Campo Minato appena giocato.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Incursione Commando": {
        "nome": "Incursione Commando",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Permanente",
        "timing": "Durante i combattimenti",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Annulla Bonus Fortificazioni",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Nessun bonus per le Fortificazioni viene applicato durante questo combattimento. Le Fortificazioni possono essere utilizzate normalmente",
                "condizioni": ["Durante i combattimenti"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE DURANTE I COMBATTIMENTI. Nessun bonus per le Fortificazioni viene applicato durante questo combattimento. Le Fortificazioni possono essere utilizzate normalmente.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Svolta Negli Eventi": {
        "nome": "Svolta Negli Eventi",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Immediata",
        "timing": "In ogni momento",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scambia Caratteristiche",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "tutte",
                "descrizione_effetto": "Puoi scambiare la caratteristica C con S, C con A e S con A. Questo effetto dura fino alla fine del combattimento. Questa carta ti permette di effettuare gli scambi solo una volta e il cambiamento deve essere effettuato immediatamente dopo che la carta è stata giocata",
                "condizioni": [],
                "limitazioni": ["Scambi solo una volta", "Deve essere fatto immediatamente", "Dura fino alla fine del combattimento"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN TUO GUERRIERO DURANTE UN COMBATTIMENTO. Puoi scambiare la caratteristica C con S, C con A e S con A. Questo effetto dura fino alla fine del combattimento. Questa carta ti permette di effettuare gli scambi solo una volta e il cambiamento deve essere effettuato immediatamente dopo che la carta è stata giocata.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Addestramento Speciale": {
        "nome": "Addestramento Speciale",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Doomtrooper non Personalità",
        "durata": "Permanente",
        "timing": "Al costo di un'azione",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Scarta Carte Speciali",
                "tipo_effetto": "Modificatore",
                "valore": "4D per carta",
                "statistica_target": "",
                "descrizione_effetto": "Puoi subito scartare una carta Speciale attualmente in gioco. Per ogni 4D che spendi, puoi scartare un'altra carta Speciale in gioco",
                "condizioni": ["Doomtrooper non Personalità", "Costo un'azione"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER NON PERSONALITÀ AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Al costo di tre Azioni questo guerriero può scartare una carta Speciale.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers non Personalità"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Campo Minato Anticarro": {
        "nome": "Campo Minato Anticarro",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Immediata",
        "timing": "Durante un combattimento",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Ferisce Veicoli",
                "tipo_effetto": "Combattimento",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "L'attaccante è automaticamente ferito e il Carro armato viene scartato ponendo fine al combattimento. Se l'attaccante è ucciso dalla ferita, i punti vengono guadagnati normalmente",
                "condizioni": ["Durante combattimento", "Attaccante usa o è considerato un Carro Armato"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE DURANTE UN COMBATTIMENTO IN CUI L'ATTACCANTE UTILIZZA O È CONSIDERATO UN CARRO ARMATO. Una volta giocata rimuovi questa carta dal gioco. L'attaccante è automaticamente ferito e il Carro armato viene scartato ponendo fine al combattimento. Se l'attaccante è ucciso dalla ferita, i punti vengono guadagnati normalmente.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Incursione Aerea": {
        "nome": "Incursione Aerea",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Permanente",
        "timing": "Durante il combattimento",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Annulla Bonus Warzone",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Nessuna Warzone può essere utilizzata in questo combattimento. Le Fortificazioni possono essere utilizzate normalmente",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE DURANTE IL COMBATTIMENTO. Nessuna Warzone può essere utilizzata in questo combattimento. Le Fortificazioni possono essere utilizzate normalmente.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Flusso Di Potere Oscuro": {
        "nome": "Flusso Di Potere Oscuro",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero che usa una carta dell'Oscura Simmetria",
        "durata": "Fino all'inizio del tuo prossimo turno",
        "timing": "Giocabile in ogni momento su un guerriero che usa una carta dell'Oscura Simmetria",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Aumenta effetto",
                "tipo_effetto": "Modificatore",
                "valore": "Raddoppia",
                "statistica_target": "oscura_simmetria",
                "descrizione_effetto": "L'effetto di quella carta è raddoppiato (se applicabile) fino all'inizio del tuo prossimo turno",
                "condizioni": ["Guerriero che usa carta dell'Oscura Simmetria"],
                "limitazioni": ["Solo se applicabile"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO SU UN GUERRIERO CHE USA UNA CARTA DELL'OSCURA SIMMETRIA. L'effetto di quella carta è raddoppiato (se applicabile) fino all'inizio del tuo prossimo turno.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Programmato": {
        "nome": "Programmato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Cybertronic"],
        "bersaglio": "Qualsiasi Doomtrooper in gioco",
        "durata": "Resto della partita",
        "timing": "Giocabile al costo di un'azione su qualsiasi Doomtrooper in gioco",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Cambia Fazione",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Paga il valore V del guerriero in punti D quando introduci in gioco questa carta. Il guerriero diventa membro della Cybertronic e perde ogni legame precedente. Il guerriero diventa automaticamente immune ai doni degli Apostoli. Non potrà mai lanciare incantesimi dell'Arte",
                "condizioni": ["Costo un'azione", "Paga V del guerriero in D"],
                "limitazioni": ["Immune agli effetti dell'Oscura Simmetria", "Non può lanciare Arte"]
            }
        ],
        "testo_carta": "GIOCABILE AL COSTO DI UN'AZIONE SU QUALSIASI DOOMTROOPER IN GIOCO. Paga il valore V del guerriero in punti D quando introduci in gioco questa carta. Il guerriero diventa membro della Cybertronic e perde ogni legame precedente. Il guerriero diventa automaticamente immune ai doni degli Apostoli. Non potrà mai lanciare incantesimi dell'Arte.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Cybertronic"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Sotterfugio": {
        "nome": "Sotterfugio",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore avversario dopo aver giocato una carta",
        "durata": "Immediata",
        "timing": "Giocabile al costo di tre azioni. Una volta giocata questa carta deve essere rimossa dal gioco",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Scarta Carte Mano",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Un giocatore avversario deve scartare completamente tutte le carte in mano",
                "condizioni": ["Costo tre azioni"],
                "limitazioni": ["Carta rimossa dal gioco dopo l'uso"]
            }
        ],
        "testo_carta": "GIOCABILE AL COSTO DI TRE AZIONI. UNA VOLTA GIOCATA QUESTA CARTA DEVE ESSERE RIMOSSA DAL GIOCO. Un giocatore avversario deve scartare completamente tutte le carte in mano.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Campo Minato": {
        "nome": "Campo Minato",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia durante un combattimento corpo a corpo se sei il difensore",
        "durata": "Un combattimento",
        "timing": "Durante un combattimento corpo a corpo se sei il difensore",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Ferisce Attaccante",
                "tipo_effetto": "Combattimento",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Una volta utilizzata elimina questa carta dal gioco. L'attaccante è automaticamente ferito e il combattimento ha termine. Se l'attaccante viene ucciso da questa ferita vengono guadagnati normalmente i punti",
                "condizioni": ["Combattimento corpo a corpo", "Sei il difensore"],
                "limitazioni": ["Carta eliminata dal gioco dopo l'uso"]
            }
        ],
        "testo_carta": "GIOCABILE DURANTE UN COMBATTIMENTO CORPO A CORPO SE SEI IL DIFENSORE. UNA VOLTA UTILIZZATA ELIMINA QUESTA CARTA DAL GIOCO. L'attaccante è automaticamente ferito e il combattimento ha termine. Se l'attaccante viene ucciso da questa ferita vengono guadagnati normalmente i punti.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Arma Difettosa": {
        "nome": "Arma Difettosa",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero che utilizza un'arma da fuoco durante un combattimento",
        "durata": "Un combattimento, poi permanente",
        "timing": "Su un guerriero che utilizza un'arma da fuoco durante un combattimento",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Disabilita Arma",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "equipaggiamento",
                "descrizione_effetto": "L'Arma è spuntata e non potrà essere utilizzata in questo combattimento. Risolvete il combattimento come di consueto tranne che dovrete sommare il valore dell'arma difettosa al valore del guerriero che la gioca questa carta (compresi eventuali altri modificatori). Dopo il combattimento l'arma viene scartata",
                "condizioni": ["Guerriero con arma da fuoco", "Durante il combattimento"],
                "limitazioni": ["Arma scartata dopo il combattimento"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO CHE UTILIZZA UN'ARMA DA FUOCO DURANTE UN COMBATTIMENTO. L'Arma è spuntata e non potrà essere utilizzata in questo combattimento. Risolvete il combattimento come di consueto tranne che dovrete sommare il valore dell'arma difettosa al valore del guerriero che la gioca questa carta (compresi eventuali altri modificatori). Dopo il combattimento l'arma viene scartata.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Feroce Assassino": {
        "nome": "Feroce Assassino",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero dell'Oscura Legione con un V pari a 4 o meno al costo di due azioni",
        "durata": "Permanente",
        "timing": "Su un guerriero dell'Oscura Legione con un V pari a 4 o meno al costo di due azioni",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Uccide Automaticamente",
                "tipo_effetto": "Combattimento",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Le caratteristiche C, S, A e V sono raddoppiate. Questa carta rimane in gioco. Ogni volta che il guerriero ferisce l'avversario in combattimento, le caratteristiche vengono raddoppiate di nuovo. Se il guerriero viene ucciso, tu guadagni tutti i punti promozione",
                "condizioni": ["Guerriero Oscura Legione", "V pari a 4 o meno", "Costo due azioni"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DELL'OSCURA LEGIONE CON UN V PARI A 4 O MENO AL COSTO DI DUE AZIONI. QUESTA CARTA RIMANE IN GIOCO. Le caratteristiche C, S, A e V sono raddoppiate. Ogni volta che il guerriero ferisce l'avversario in combattimento, le caratteristiche vengono raddoppiate di nuovo. Se il guerriero viene ucciso, tu guadagni tutti i punti promozione.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Oscura Legione"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Fiamme Purificatrici": {
        "nome": "Fiamme Purificatrici",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Campo di battaglia",
        "durata": "Immediata",
        "timing": "In ogni momento. Una volta usata rimuovi questa carta dal gioco",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Doni dell'Oscura Simmetria",
                "tipo_effetto": "Modificatore",
                "valore": "Al costo di 8D",
                "statistica_target": "",
                "descrizione_effetto": "Al costo di 8D puoi scartare un qualsiasi guerriero dell'Oscura Legione in gioco. Questa non è considerata un'Azione d'Attacco",
                "condizioni": ["Costo 8D"],
                "limitazioni": ["Non considerata Azione d'Attacco", "Carta rimossa dal gioco dopo l'uso"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. UNA VOLTA USATA RIMUOVI QUESTA CARTA DAL GIOCO. Al costo di 8D puoi scartare un qualsiasi guerriero dell'Oscura Legione in gioco. Questa non è considerata un'Azione d'Attacco.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Posto Di Guardia": {
        "nome": "Posto Di Guardia",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Un tuo guerriero al costo di un'azione",
        "durata": "Permanente",
        "timing": "Su un tuo guerriero al costo di un'azione",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Questa carta rimane in gioco. Muovi il guerriero di fronte alla tua Squadra/Schieramento. Ogni volta che un avversario decide di attaccare i guerrieri posti dietro di lui, in Corpo a Corpo, egli può intervenire prendendo il posto del difensore designato. Se interviene, al termine del combattimento, sarà automaticamente ferito. Se muore a causa di questa ferita l'avversario guadagna normalmente i punti",
                "condizioni": ["Costo un'azione"],
                "limitazioni": ["Ferita automatica se interviene", "Solo in combattimento Corpo a Corpo"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN TUO GUERRIERO AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Muovi il guerriero di fronte alla tua Squadra/Schieramento. Ogni volta che un avversario decide di attaccare i guerrieri posti dietro di lui, in Corpo a Corpo, egli può intervenire prendendo il posto del difensore designato. Se interviene, al termine del combattimento, sarà automaticamente ferito. Se muore a causa di questa ferita l'avversario guadagna normalmente i punti.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Agnello Da Sacrificare": {
        "nome": "Agnello Da Sacrificare",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore al costo di un'azione",
        "durata": "Permanente",
        "timing": "Al costo di un'azione. Tu puoi immediatamente introdurre in gioco un tuo guerriero assegnandolo alla Squadra/Schieramento avversario",
        "set_espansione": "Warzone",
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
                "descrizione_effetto": "Tu puoi immediatamente introdurre in gioco un tuo guerriero assegnandolo alla Squadra/Schieramento avversario. Tratta questo guerriero come se fosse stato il tuo avversario ad introdurlo in gioco. Il tuo avversario ha il pieno controllo di questo guerriero e può utilizzarlo ed equipaggiarlo come meglio crede",
                "condizioni": ["Costo un'azione"],
                "limitazioni": ["Il controllo passa all'avversario"]
            }
        ],
        "testo_carta": "GIOCABILE AL COSTO DI UN'AZIONE. Tu puoi immediatamente introdurre in gioco un tuo guerriero assegnandolo alla Squadra/Schieramento avversario. Tratta questo guerriero come se fosse stato il tuo avversario ad introdurlo in gioco. Il tuo avversario ha il pieno controllo di questo guerriero e può utilizzarlo ed equipaggiarlo come meglio crede.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Interferenza": {
        "nome": "Interferenza",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Campo di battaglia",
        "durata": "Immediata",
        "timing": "Giocabile immediatamente dopo che un incantesimo dell'Arte è stato lanciato",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Annulla Incantesimo",
                "tipo_effetto": "Arte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "L'incantesimo non ha effetto e la relativa carta viene scartata. Ogni Azione o punto D speso per lanciare l'incantesimo è perso",
                "condizioni": ["Incantesimo appena lanciato"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE UN INCANTESIMO DELL'ARTE È STATO LANCIATO. L'incantesimo non ha effetto e la relativa carta viene scartata. Ogni Azione o punto D speso per lanciare l'incantesimo è perso.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Goffaggine": {
        "nome": "Goffaggine",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero che utilizza un'arma da corpo a corpo durante un combattimento",
        "durata": "Un combattimento",
        "timing": "Su un guerriero che utilizza un'arma da corpo a corpo. Il guerriero scivola e colpisce un guerriero alleato nella squadra o nello schieramento del giocatore che utilizzava l'arma",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Modifica Bersaglio",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "combattimento",
                "descrizione_effetto": "Il guerriero scivola e colpisce un guerriero alleato nella squadra o nello schieramento del giocatore che utilizzava l'arma. La vittima non ottiene guadagni punto non si possono giocare altre carte durante il combattimento",
                "condizioni": ["Guerriero con arma da corpo a corpo"],
                "limitazioni": ["Bersaglio alleato", "Non si possono giocare altre carte"]
            }
        ],
        "testo_carta": "GIOCABILE DURANTE UN COMBATTIMENTO SU UN GUERRIERO CHE UTILIZZA UN'ARMA DA CORPO A CORPO. Il guerriero scivola e colpisce un guerriero alleato nella squadra o nello schieramento del giocatore che utilizzava l'arma. Il giocatore che gioca questa carta sceglie il bersaglio. La vittima non ottiene guadagni punto non si possono giocare altre carte durante il combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Attacco Suicida": {
        "nome": "Attacco Suicida",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero al costo di tre azioni",
        "durata": "Immediata",
        "timing": "Su un tuo guerriero al costo di tre azioni. Il guerriero svolge una missione suicida contro il giocatore avversario eliminando un numero di punti Promozione pari alla caratteristica V del guerriero suicida",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Missione Suicida",
                "tipo_effetto": "Modificatore",
                "valore": "V del guerriero in Punti Promozione",
                "statistica_target": "punti_promozione",
                "descrizione_effetto": "Il guerriero svolge una missione suicida contro il giocatore avversario eliminando un numero di punti Promozione pari alla caratteristica V del guerriero suicida. Questo non è considerato un Attacco e l'avversario non guadagna punti. Il guerriero viene scartato dopo l'Attacco suicida",
                "condizioni": ["Costo tre azioni"],
                "limitazioni": ["Non considerato un Attacco", "Guerriero scartato"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN TUO GUERRIERO AL COSTO DI TRE AZIONI. Il guerriero svolge una missione suicida contro il giocatore avversario eliminando un numero di punti Promozione pari alla caratteristica V del guerriero suicida. Questo non è considerato un Attacco e l'avversario non guadagna punti. Il guerriero viene scartato dopo l'Attacco suicida.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Grande Stratega": {
        "nome": "Grande Stratega",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Giocatore",
        "durata": "Permanente",
        "timing": "In ogni momento. Questa carta rimane in gioco e non può essere scartata. Introducendola in gioco diventi un Grande Stratega e puoi assegnare alla tua Squadra/Schieramento una WARZONE al costo di un'azione",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Introducendola in gioco diventi un Grande Stratega e puoi assegnare alla tua Squadra/Schieramento una WARZONE al costo di un'azione. Possono essere introdotte anche WARZONE identiche. Quando tutti i tuoi guerrieri si difendono in un combattimento possono scegliere di difendersi in una delle WARZONE assegnate alla Squadra/Schieramento. Durante il combattimento il guerriero guadagnerà i bonus di C, S, A e V previsti per quella particolare WARZONE",
                "condizioni": [],
                "limitazioni": ["Solo durante la difesa", "Una WARZONE per combattimento"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. QUESTA CARTA RIMANE IN GIOCO E NON PUÒ ESSERE SCARTATA. Introducendola in gioco diventi un Grande Stratega e puoi assegnare alla tua Squadra/Schieramento una WARZONE al costo di un'azione. Possono essere introdotte anche WARZONE identiche. Quando tutti i tuoi guerrieri si difendono in un combattimento possono scegliere di difendersi in una delle WARZONE assegnate alla Squadra/Schieramento. Durante il combattimento il guerriero guadagnerà i bonus di C, S, A e V previsti per quella particolare WARZONE. Se il guerriero si difende in una WARZONE nessuno dei due combattenti potrà utilizzare effetti legati a Fortificazioni. Equipaggiamenti e guerrieri considerati Fortificazioni potranno invece essere utilizzati. Il guerriero che attacca non può usare le sue WARZONE. La Squadra potrà utilizzare solo le WARZONE assegnate alla Squadra e lo Schieramento potrà solo utilizzare quelle assegnate allo Schieramento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Morte Istantanea": {
        "nome": "Morte Istantanea",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Combattimento corpo a corpo in cui un tuo guerriero dell'Oscura Legione si sta difendendo dall'attacco di un Doomtrooper",
        "durata": "Un combattimento",
        "timing": "Durante un combattimento corpo a corpo in cui un tuo guerriero dell'Oscura Legione si sta difendendo dall'attacco di un Doomtrooper",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Uccide Automaticamente",
                "tipo_effetto": "Combattimento",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il Doomtrooper è scartato immediatamente. Non si guadagnano punti",
                "condizioni": ["Combattimento corpo a corpo", "Guerriero Oscura Legione difensore", "Attaccante è Doomtrooper"],
                "limitazioni": ["Non si guadagnano punti"]
            }
        ],
        "testo_carta": "GIOCABILE DURANTE UN COMBATTIMENTO CORPO A CORPO IN CUI UN TUO GUERRIERO DELL'OSCURA LEGIONE SI STA DIFENDENDO DALL'ATTACCO DI UN DOOMTROOPER. Il Doomtrooper è scartato immediatamente. Non si guadagnano punti.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Disastro Naturale": {
        "nome": "Disastro Naturale",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Immediata",
        "timing": "In ogni momento. Puoi scartare una WARZONE attualmente in gioco",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Warzone",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Puoi scartare una WARZONE attualmente in gioco",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Puoi scartare una WARZONE attualmente in gioco.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Supporto Aereo": {
        "nome": "Supporto Aereo",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Su un guerriero durante il combattimento. Il guerriero guadagna un +5 in C durante questo combattimento",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento",
                "tipo_effetto": "Modificatore",
                "valore": "+5 in C",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Il guerriero guadagna un +5 in C durante questo combattimento. Questa carta non ha effetto se il guerriero avversario utilizza un VEICOLO o è considerato AERONAVE, CARRO ARMATO o VEICOLO",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": ["Non ha effetto contro VEICOLO, AERONAVE, CARRO ARMATO"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DURANTE IL COMBATTIMENTO. Il guerriero guadagna un +5 in C durante questo combattimento. Questa carta non ha effetto se il guerriero avversario utilizza un VEICOLO o è considerato AERONAVE, CARRO ARMATO o VEICOLO.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Grave Trauma": {
        "nome": "Grave Trauma",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero ferito al costo di un'azione",
        "durata": "Permanente",
        "timing": "Su un guerriero ferito al costo di un'azione. Questa carta rimane in gioco",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Modifica Stato",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Metti il guerriero in copertura. Il guerriero non potrà uscire allo scoperto finché non torna sano. Non è consentito giocare questa carta su guerrieri che non possono andare in copertura",
                "condizioni": ["Guerriero ferito", "Costo un'azione"],
                "limitazioni": ["Non può uscire allo scoperto finché ferito", "Non utilizzabile su guerrieri che non possono andare in copertura"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO FERITO AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Metti il guerriero in copertura. Il guerriero non potrà uscire allo scoperto finché non torna sano. Non è consentito giocare questa carta su guerrieri che non possono andare in copertura.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Programma Di Auto-Distruzione": {
        "nome": "Programma Di Auto-Distruzione",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Cybertronic"],
        "bersaglio": "Guerriero Cybertronic durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Su ogni guerriero Cybertronic durante il combattimento. Il guerriero triplica la sua caratteristica naturale (quella segnata sulla carta) C fino alla fine del combattimento",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Triplica Combattimento",
                "tipo_effetto": "Modificatore",
                "valore": "Triplica C naturale",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Il guerriero triplica la sua caratteristica naturale (quella segnata sulla carta) C fino alla fine del combattimento. Dopo il combattimento il guerriero muore facendo guadagnare all'avversario i suoi punti. Non si può salvare il guerriero dalla morte in alcun modo",
                "condizioni": ["Guerriero Cybertronic", "Durante il combattimento"],
                "limitazioni": ["Guerriero muore dopo il combattimento", "Morte inevitabile"]
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI GUERRIERO CYBERTRONIC DURANTE IL COMBATTIMENTO. Il guerriero triplica la sua caratteristica naturale (quella segnata sulla carta) C fino alla fine del combattimento. Dopo il combattimento il guerriero muore facendo guadagnare all'avversario i suoi punti. Non si può salvare il guerriero dalla morte in alcun modo.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Cybertronic"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Bombardamento Strategico": {
        "nome": "Bombardamento Strategico",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Campo di battaglia",
        "durata": "Permanente",
        "timing": "In ogni momento. Tutte le Industrie belliche e i Complessi industriali in gioco sono scartati",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Scarta Industrie",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Tutte le Industrie belliche e i Complessi industriali in gioco sono scartati",
                "condizioni": [],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. Tutte le Industrie belliche e i Complessi industriali in gioco sono scartati.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Codice D'Onore": {
        "nome": "Codice D'Onore",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Doomtrooper",
        "durata": "Permanente",
        "timing": "Su ogni Doomtrooper in ogni momento. Questa carta rimane in gioco",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Diventa Bauhaus",
                "tipo_effetto": "Modificatore",
                "valore": "+2 in C e S",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Il guerriero diventa un membro della Bauhaus in aggiunta al precedente legame. Il guerriero guadagna un +2 in C e S ma non potrà mai attaccare un guerriero con una V inferiore alla sua",
                "condizioni": ["Doomtrooper"],
                "limitazioni": ["Non può attaccare guerrieri con V inferiore"]
            }
        ],
        "testo_carta": "GIOCABILE SU OGNI DOOMTROOPER IN OGNI MOMENTO. QUESTA CARTA RIMANE IN GIOCO. Il guerriero diventa un membro della Bauhaus in aggiunta al precedente legame. Il guerriero guadagna un +2 in C e S ma non potrà mai attaccare un guerriero con una V inferiore alla sua.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },    

    "Bottino Di Guerra": {
        "nome": "Bottino Di Guerra",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero al costo di un'azione",
        "durata": "Permanente",
        "timing": "Giocabile su un guerriero al costo di un'azione",
        "set_espansione": "Warzone",
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
                "descrizione_effetto": "Questo guerriero può impossessarsi di una carta Equipaggiamento che sta per essere scartata e assegnarla ad un guerriero nella sua Squadra/Schieramento. Il CORNA DI LEGAME del nuovo possessore è irrilevante. Scarta questa carta dopo l'uso",
                "condizioni": ["Costo un'azione"],
                "limitazioni": ["Il CORNA DI LEGAME del nuovo possessore è irrilevante", "Scarta questa carta dopo l'uso"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Questo guerriero può impossessarsi di una carta Equipaggiamento che sta per essere scartata e assegnarla ad un guerriero nella sua Squadra/Schieramento. Il CORNA DI LEGAME del nuovo possessore è irrilevante. Scarta questa carta dopo l'uso.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Rifugiato Tra La Folla": {
        "nome": "Rifugiato Tra La Folla",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Un combattimento",
        "timing": "Giocabile durante il combattimento",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Combattimento Non Simultaneo",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il combattimento finisce immediatamente. L'Attaccante può attaccare immediatamente un altro guerriero (non può scegliere lo stesso). L'Attaccante può scegliere se e quale guerriero nella squadra o nello schieramento del difensore designato",
                "condizioni": ["Durante il combattimento"],
                "limitazioni": ["L'attaccante non può scegliere lo stesso guerriero"]
            }
        ],
        "testo_carta": "GIOCABILE DURANTE IL COMBATTIMENTO. Il combattimento finisce immediatamente. L'Attaccante può attaccare immediatamente un altro guerriero (non può scegliere lo stesso). L'Attaccante può scegliere se e quale guerriero nella squadra o nello schieramento del difensore designato.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Avamposto Di Mercurio Turf": {
        "nome": "Avamposto Di Mercurio Turf",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Mishima"],
        "bersaglio": "Campo di battaglia su una Warzone Mercurio",
        "durata": "Permanente",
        "timing": "Giocabile in ogni momento su una WARZONE: MERCURIO. Questa carta rimane in gioco",
        "set_espansione": "Warzone",
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
                "descrizione_effetto": "Guerrieri Mishima che si difendono in questo Avamposto ignorano tutte le modifiche negative. Ogni guerriero ferito da un guerriero Mishima in difesa in questa Warzone è automaticamente ucciso",
                "condizioni": ["WARZONE: MERCURIO in gioco"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO SU UNA WARZONE: MERCURIO. QUESTA CARTA RIMANE IN GIOCO. Guerrieri Mishima che si difendono in questo Avamposto ignorano tutte le modifiche negative. Ogni guerriero ferito da un guerriero Mishima in difesa in questa Warzone è automaticamente ucciso.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Mishima"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Sedile Eiettabile": {
        "nome": "Sedile Eiettabile",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero immediatamente dopo che un guerriero che utilizza un veicolo viene ferito o ucciso",
        "durata": "Immediata",
        "timing": "Immediatamente dopo che un guerriero che utilizza un veicolo viene ferito o ucciso",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Guarisce se stesso",
                "tipo_effetto": "Guarigione",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero aziona il sedile eiettabile ed evita di essere ferito. Questa opzione è applicabile anche per ferite che uccidono istantaneamente o per ferite che portano alla morte del guerriero. SCARTA IL VEICOLO. Se il guerriero era già ferito rimane ferito",
                "condizioni": ["Guerriero con veicolo", "Appena ferito o ucciso"],
                "limitazioni": ["Veicolo scartato", "Se era già ferito rimane ferito"]
            }
        ],
        "testo_carta": "GIOCABILE IMMEDIATAMENTE DOPO CHE UN GUERRIERO CHE UTILIZZA UN VEICOLO VIENE FERITO O UCCISO. Il guerriero aziona il sedile eiettabile ed evita di essere ferito. Questa opzione è applicabile anche per ferite che uccidono istantaneamente o per ferite che portano alla morte del guerriero. SCARTA IL VEICOLO. Se il guerriero era già ferito rimane ferito.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Mancato Rifornimento": {
        "nome": "Mancato Rifornimento",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante il combattimento",
        "durata": "Permanente",
        "timing": "Giocabile in ogni momento su una WARZONE: MERCURIO",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Cerca Carta nel Mazzo",
                "tipo_effetto": "Carte",
                "valore": 0,
                "statistica_target": "equipaggiamento",
                "descrizione_effetto": "UNA CARTA EQUIPAGGIAMENTO D'ORA E STATA ESTINTA E NON PUÒ PIÙ ESSERE INTRODOTTA IN GIOCO. Dopo che che questo è stato detto, da tutti i guerrieri che utilizzano quella particolare carta equipaggiamento e mescola questi equipaggiamenti nel mazzo di carte da pescare",
                "condizioni": [],
                "limitazioni": ["Tipo di equipaggiamento estinto permanentemente"]
            }
        ],
        "testo_carta": "GIOCABILE IN OGNI MOMENTO. ELIMINA QUESTA CARTA DAL GIOCO DOPO L'USO. UNA CARTA EQUIPAGGIAMENTO D'ORA E STATA ESTINTA E NON PUÒ PIÙ ESSERE INTRODOTTA IN GIOCO. Dopo che che questo è stato detto, da tutti i guerrieri che utilizzano quella particolare carta equipaggiamento e mescola questi equipaggiamenti nel mazzo di carte da pescare.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Stanchezza Mentale": {
        "nome": "Stanchezza Mentale",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Fratellanza"],
        "bersaglio": "Guerriero della Fratellanza",
        "durata": "Permanente",
        "timing": "Giocabile su un guerriero della Fratellanza al costo di un'azione",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Lancia Arte",
                "tipo_effetto": "Arte",
                "valore": "3D per turno",
                "statistica_target": "",
                "descrizione_effetto": "A partire da questo momento il guerriero potrà utilizzare solo 3D per turno in Incantesimi dell'Arte. Per Turno si intende da una fase pescare all'altra dello stesso giocatore",
                "condizioni": ["Guerriero della Fratellanza", "Costo un'azione"],
                "limitazioni": ["Solo 3D per turno per Arte"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN GUERRIERO DELLA FRATELLANZA AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. A partire da questo momento il guerriero potrà utilizzare solo 3D per turno in Incantesimi dell'Arte. Per Turno si intende da una fase pescare all'altra dello stesso giocatore.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Fratellanza"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Trasferimento Truppe": {
        "nome": "Trasferimento Truppe",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Guerriero durante i combattimenti",
        "durata": "Un combattimento",
        "timing": "Durante i combattimenti",
        "set_espansione": "Warzone",
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
                "descrizione_effetto": "L'attaccante può scegliere se e quale Warzone utilizzare di quelle a disposizione dei difensori",
                "condizioni": ["Durante i combattimenti"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE DURANTE I COMBATTIMENTI. L'attaccante può scegliere se e quale Warzone utilizzare di quelle a disposizione dei difensori.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Attestato D'Onore": {
        "nome": "Attestato D'Onore",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Doomtrooper immediatamente dopo che ha ucciso un guerriero con un valore superiore al suo",
        "durata": "Permanente",
        "timing": "Giocabile su un Doomtrooper immediatamente dopo che ha ucciso un guerriero con un valore superiore al suo",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Statistiche",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in C, S, A e V",
                "statistica_target": "tutte",
                "descrizione_effetto": "Questa carta rimane in gioco associata al guerriero. Il guerriero guadagna un +1 in C, S e A. Un guerriero può avere più di un Attestato",
                "condizioni": ["Doomtrooper", "Ha appena ucciso guerriero con V superiore"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN DOOMTROOPER IMMEDIATAMENTE DOPO CHE HA UCCISO UN GUERRIERO CON UNA CARATTERISTICA V MAGGIORE. QUESTA CARTA RIMANE IN GIOCO ASSOCIATA AL GUERRIERO. Il guerriero guadagna un +1 in C, S, A e V. Un guerriero può avere più di un Attestato.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Atto Eroico": {
        "nome": "Atto Eroico",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Doomtrooper immediatamente dopo che ha ucciso un guerriero con una caratteristica V maggiore",
        "durata": "Permanente",
        "timing": "Giocabile su un Doomtrooper immediatamente dopo che ha ucciso un guerriero con una caratteristica V maggiore",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": False,
        "effetti": [
            {
                "nome_effetto": "Bonus Statistiche",
                "tipo_effetto": "Modificatore",
                "valore": "+3 in C, S, A e V",
                "statistica_target": "tutte",
                "descrizione_effetto": "Questa carta rimane con il guerriero. Il guerriero guadagna un +3 in C, S, A e V. Un guerriero può essere premiato in questo modo più volte",
                "condizioni": ["Doomtrooper", "Ha appena ucciso guerriero con V maggiore"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN DOOMTROOPER IMMEDIATAMENTE DOPO CHE HA UCCISO UN GUERRIERO CON UNA CARATTERISTICA V MAGGIORE. QUESTA CARTA RIMANE CON IL GUERRIERO. Il guerriero guadagna un +3 in C, S, A e V. Un guerriero può essere premiato in questo modo più volte.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    # verificare queste sotto
    
    "Addestramento Elite": {
        "nome": "Addestramento Elite",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Doomtrooper al costo di due azioni",
        "durata": "Permanente",
        "timing": "Su un Doomtrooper al costo di due azioni",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Bonus Statistiche",
                "tipo_effetto": "Modificatore",
                "valore": "+1 in tutte le caratteristiche",
                "statistica_target": "tutte",
                "descrizione_effetto": "Questa carta rimane in gioco. Il guerriero guadagna un +1 in C, S, A e V",
                "condizioni": ["Doomtrooper", "Costo due azioni"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN DOOMTROOPER AL COSTO DI DUE AZIONI. QUESTA CARTA RIMANE IN GIOCO. Il guerriero guadagna un +1 in C, S, A e V.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Pattuglia": {
        "nome": "Pattuglia",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Doomtrooper al costo di un'azione",
        "durata": "Permanente",
        "timing": "Su un Doomtrooper al costo di un'azione",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Questa carta rimane in gioco. Il guerriero può attaccare guerrieri che stanno Al Coperto. Il giocatore che controlla il guerriero Al Coperto può scegliere se girare la carta a faccia in su e affrontare l'attacco oppure se il guerriero Al Coperto viene automaticamente ucciso",
                "condizioni": ["Doomtrooper", "Costo un'azione"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN DOOMTROOPER AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Il guerriero può attaccare guerrieri che stanno Al Coperto. Il giocatore che controlla il guerriero Al Coperto può scegliere se girare la carta a faccia in su e affrontare l'attacco oppure se il guerriero Al Coperto viene automaticamente ucciso.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cecchino": {
        "nome": "Cecchino",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Doomtrooper al costo di un'azione",
        "durata": "Permanente",
        "timing": "Su un Doomtrooper al costo di un'azione",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Uccide Automaticamente",
                "tipo_effetto": "Combattimento",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Questa carta rimane in gioco. Se il guerriero ferisce l'avversario durante un combattimento a distanza, l'avversario viene automaticamente ucciso",
                "condizioni": ["Doomtrooper", "Costo un'azione", "Combattimento a distanza"],
                "limitazioni": ["Solo combattimento a distanza"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN DOOMTROOPER AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Se il guerriero ferisce l'avversario durante un combattimento a distanza, l'avversario viene automaticamente ucciso.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Soldato Semplice": {
        "nome": "Soldato Semplice",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Doomtrooper non-Personalità al costo di un'azione",
        "durata": "Permanente",
        "timing": "Su un Doomtrooper non-Personalità al costo di un'azione",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Bonus Combattimento per Spesa",
                "tipo_effetto": "Modificatore",
                "valore": "+1 per ogni 2D spesi",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Questa carta rimane in gioco. Il guerriero guadagna un +1 in C per ogni 2D spesi durante il combattimento",
                "condizioni": ["Doomtrooper non-Personalità", "Costo un'azione"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN DOOMTROOPER NON-PERSONALITÀ AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Il guerriero guadagna un +1 in C per ogni 2D spesi durante il combattimento.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers non-Personalità"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Genio Militare": {
        "nome": "Genio Militare",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Doomtrooper Personalità al costo di tre azioni",
        "durata": "Permanente",
        "timing": "Su un Doomtrooper Personalità al costo di tre azioni",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Modifica Azione",
                "tipo_effetto": "Modificatore",
                "valore": "Tutte le carte Speciali della Squadra/Schieramento",
                "statistica_target": "",
                "descrizione_effetto": "Questa carta rimane in gioco. Il guerriero può attivare tutte le carte Speciali assegnate alla Squadra/Schieramento di appartenenza",
                "condizioni": ["Doomtrooper Personalità", "Costo tre azioni"],
                "limitazioni": []
            }
        ],
        "testo_carta": "GIOCABILE SU UN DOOMTROOPER PERSONALITÀ AL COSTO DI TRE AZIONI. QUESTA CARTA RIMANE IN GIOCO. Il guerriero può attivare tutte le carte Speciali assegnate alla Squadra/Schieramento di appartenenza.",
        "flavour_text": "",
        "keywords": ["Personalita"],
        "restrizioni": ["Solo Doomtroopers Personalità"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Veterano": {
        "nome": "Veterano",
        "valore": 0,
        "tipo": "Speciale",
        "rarity": "Common",
        "fazioni_permesse": ["Generica"],
        "bersaglio": "Doomtrooper non-Personalità al costo di un'azione",
        "durata": "Permanente",
        "timing": "Su un Doomtrooper non-Personalità al costo di un'azione",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "max_copie_per_combattimento": 1,
        "max_copie_per_turno": 1,
        "richiede_azione": True,
        "effetti": [
            {
                "nome_effetto": "Immune agli effetti delle carte Speciali",
                "tipo_effetto": "Immunita",
                "valore": 0,
                "statistica_target": "",
                "descrizione_effetto": "Questa carta rimane in gioco. Il guerriero è immune agli effetti di tutte le carte Speciali avversarie. Non può essere influenzato da carte Speciali nemiche",
                "condizioni": ["Doomtrooper non-Personalità", "Costo un'azione"],
                "limitazioni": ["Solo contro carte Speciali avversarie"]
            }
        ],
        "testo_carta": "GIOCABILE SU UN DOOMTROOPER NON-PERSONALITÀ AL COSTO DI UN'AZIONE. QUESTA CARTA RIMANE IN GIOCO. Il guerriero è immune agli effetti di tutte le carte Speciali avversarie. Non può essere influenzato da carte Speciali nemiche.",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": ["Solo Doomtroopers non-Personalità"],
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },   
}


# Funzioni di utilità per il database

def get_carte_per_set(espansione: str) -> List[str]:
    """
    Restituisce una lista dei nomi di tutte le carte speciali di una specifica espansione
    
    Args:
        espansione: Nome dell'espansione
        
    Returns:
        Lista dei nomi delle carte speciali dell'espansione
    """
    return [nome for nome, data in DATABASE_SPECIALI.items() 
            if data["set_espansione"] == espansione]


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








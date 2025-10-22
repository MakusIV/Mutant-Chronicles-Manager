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
     
    
    # Base
 
    "Dormire": {
        "nome": "Dormire",
        "costo_destino": "1 Azione",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Muawijhe",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Addormentare Guerriero",
                "tipo_effetto": "Controllo",
                "valore": "1",
                "statistica_target": "azione",
                "descrizione_effetto": "Il guerriero addormentato non potrà attaccare o essere attaccato",
                "condizioni": ["Pagare 1 Azione"],
                "limitazioni": ["Il guerriero non può attaccare", "Il guerriero non può essere attaccato"],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI MUAWIJHE. Al costo di un'Azione questo guerriero può addormentare un guerriero avversario. Il guerriero addormentato non potrà attaccare o essere attaccato.",
        "flavour_text": "",
        "keywords": ["Seguace di Muawijhe"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Seguace di Muawijhe"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Cecità": {
        "nome": "Cecità",
        "costo_destino": "",
        "tipo": "Dono dell'Oscura Legione",
        "apostolo_padre": None,
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Penalità Caratteristiche",
                "tipo_effetto": "Modificatore",
                "valore": "-2",
                "statistica_target": "combattimento e sparare",
                "descrizione_effetto": "Gli avversari del guerriero soffrono un -2 di penalità sulle loro caratteristiche C e S",
                "condizioni": [],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DELL'OSCURA LEGIONE. Gli avversari del guerriero soffrono un -2 di penalità sulle loro caratteristiche C e S.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 8,
        "quantita": 6,
        "quantita_minima_consigliata": 3,
        "fondamentale": False       
    },
    
    "Terrore": {
        "nome": "Terrore",
        "costo_destino": "",
        "tipo": "Dono dell'Oscura Simmetria",
        "apostolo_padre": None,
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Paralizzare per Terrore",
                "tipo_effetto": "Controllo",
                "valore": "-1",
                "statistica_target": "azioni",
                "descrizione_effetto": "Gli avversari di questo guerriero sono paralizzati dal Terrore e subiscono un -1 in A",
                "condizioni": [],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DELL'OSCURA SIMMETRIA. Gli avversari di questo guerriero sono paralizzati dal Terrore e subiscono un -1 in A.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 4,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Apertura Dimensionale": {
        "nome": "Apertura Dimensionale",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Ilian",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Uccide Automaticamente",
                "tipo_effetto": "Combattimento",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "I guerrieri feriti dal possessore di questo Dono sono automaticamente uccisi",
                "condizioni": ["Guerriero deve essere ferito dal possessore"],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI ILIAN. I guerrieri feriti dal possessore di questo Dono sono automaticamente uccisi.",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Ilian"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 2,
        "fondamentale": True       
    },
    
    "Fuoco Oscuro": {
        "nome": "Fuoco Oscuro",
        "costo_destino": "",
        "tipo": "Dono dell'Oscura Simmetria",
        "apostolo_padre": None,
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Crea Magico Fuoco Oscuro",
                "tipo_effetto": "Modificatore",
                "valore": "+1",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Nelle mani del guerriero si crea un Magico Fuoco Oscuro che gli conferisce un +1 in C",
                "condizioni": [],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DELL'OSCURA SIMMETRIA. Nelle mani del guerriero si crea un Magico Fuoco Oscuro che gli conferisce un +1 in C.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 4,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Disturbo": {
        "nome": "Disturbo",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Ilian",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Immune agli effetti dell'Oscura Simmetria",
                "tipo_effetto": "Immunita",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Il guerriero in possesso di questo Dono sarà immune agli effetti dell'Oscura Simmetria e alle Magiche Arti",
                "condizioni": [],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI ILIAN. Il guerriero in possesso di questo Dono sarà immune agli effetti dell'Oscura Simmetria e alle Magiche Arti.",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Ilian"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 1,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Fusione Mentale": {
        "nome": "Fusione Mentale",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Semai",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Bonus Caratteristiche",
                "tipo_effetto": "Modificatore",
                "valore": "+2",
                "statistica_target": "combattimento e sparare",
                "descrizione_effetto": "Il guerriero guadagna un +2 in C e S",
                "condizioni": [],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI SEMAI. Il guerriero guadagna un +2 in C e S.",
        "flavour_text": "",
        "keywords": ["Seguace di Semai"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Semai"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 8,
        "quantita": 3,
        "quantita_minima_consigliata": 2,
        "fondamentale": False       
    },
    
    "Illusione": {
        "nome": "Illusione",
        "costo_destino": "3 Punti Destino",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Semai",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Combattimento Corrente",
        "durata": "Istantanea",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Cancella Combattimento",
                "tipo_effetto": "Controllo",
                "valore": "3",
                "statistica_target": "destino",
                "descrizione_effetto": "Il guerriero può, in ogni momento, cancellare un combattimento nel quale è coinvolto. Tutte le carte giocate dai giocatori durante il combattimento sono scartate. La fase di combattimento è finita, e il guerriero deve immediatamente andare in copertura. Questo gli costerà 3D, ma non richiederà la spesa di alcuna Azione",
                "condizioni": ["Guerriero coinvolto in combattimento"],
                "limitazioni": ["Costa 3 Punti Destino", "Guerriero va automaticamente in copertura", "Non richiede spesa di Azioni"],
                "effetti_collaterali": ["Tutte le carte del combattimento sono scartate"]
            }
        ],	 
        "testo_carta": "DONO DI SEMAI. Il guerriero può, in ogni momento, cancellare un combattimento nel quale è coinvolto. Tutte le carte giocate dai giocatori durante il combattimento sono scartate. La fase di combattimento è finita, e il guerriero deve immediatamente andare in copertura. Questo gli costerà 3D, ma non richiederà la spesa di alcuna Azione.",
        "flavour_text": "",
        "keywords": ["Seguace di Semai"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Semai"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 2,
        "fondamentale": True       
    },
    
    "Resistere Al Dolore": {
        "nome": "Resistere Al Dolore",
        "costo_destino": "",
        "tipo": "Dono dell'Oscura Simmetria",
        "apostolo_padre": None,
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Bonus Azioni",
                "tipo_effetto": "Modificatore",
                "valore": "+1",
                "statistica_target": "azioni",
                "descrizione_effetto": "Il guerriero guadagna un +1 in A",
                "condizioni": [],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DELL'OSCURA SIMMETRIA. Il guerriero guadagna un +1 in A.",
        "flavour_text": "",
        "keywords": [],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": [],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 4,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Controllo Della Mente": {
        "nome": "Controllo Della Mente",
        "costo_destino": "3 Azioni",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Semai",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Fino Fine Turno",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Controlla Guerriero Nemico",
                "tipo_effetto": "Controllo",
                "valore": "3",
                "statistica_target": "azioni",
                "descrizione_effetto": "Una volta per Turno, al costo di 3 Azioni, puoi ordinare a un Guerriero nemico di attaccare o di non attaccare durante il Suo Turno. Chiaramente il giocatore avversario sarà libera di agire con gli altri guerrieri in Suo possesso",
                "condizioni": ["Una volta per turno", "Costo di 3 Azioni"],
                "limitazioni": ["Solo un guerriero nemico per turno", "Altri guerrieri dell'avversario rimangono liberi"],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI SEMAI. Una volta per Turno, al costo di 3 Azioni, puoi ordinare a un Guerriero nemico di attaccare o di non attaccare durante il Suo Turno. Chiaramente il giocatore avversario sarà libera di agire con gli altri guerrieri in Suo possesso.",
        "flavour_text": "",
        "keywords": ["Seguace di Semai"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Semai"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },

    "Deformazione": {
        "nome": "Deformazione",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Demnogonis",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Penalità Azioni",
                "tipo_effetto": "Modificatore",
                "valore": "-2",
                "statistica_target": "azioni",
                "descrizione_effetto": "Tutti i guerrieri che combattono contro il possessore di questo Dono ricevono una penalità di -2 in A",
                "condizioni": ["Guerrieri devono combattere contro il possessore"],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI DEMNOGONIS. Tutti i guerrieri che combattono contro il possessore di questo Dono ricevono una penalità di -2 in A.",
        "flavour_text": "",
        "keywords": ["Seguace di Demnogonis"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Demnogonis"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 8,
        "quantita": 2,
        "quantita_minima_consigliata": 2,
        "fondamentale": False       
    },
    
    "Sogni Orribili": {
        "nome": "Sogni Orribili",
        "costo_destino": "5 Punti Destino",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Muawijhe",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Invia Sogni Orribili",
                "tipo_effetto": "Controllo",
                "valore": "5",
                "statistica_target": "destino",
                "descrizione_effetto": "Spendendo 5D, in ogni momento, questo guerriero può inviare Sogni Orribili a un guerriero nemico, costringendo ad Andare in Copertura. Gira la carta del guerriero a faccia in giù",
                "condizioni": ["Costo di 5 Punti Destino", "In Ogni Momento"],
                "limitazioni": ["Guerriero bersaglio va in copertura", "Carta del guerriero girata a faccia in giù"],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI MUAWIJHE. Spendendo 5D, in ogni momento, questo guerriero può inviare Sogni Orribili a un guerriero nemico, costringendo ad Andare in Copertura. Gira la carta del guerriero a faccia in giù.",
        "flavour_text": "",
        "keywords": ["Seguace di Muawijhe"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Muawijhe"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 2,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Portale Della Cura Oscura": {
        "nome": "Portale Della Cura Oscura",
        "costo_destino": "3 Azioni",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Algeroth",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Nefarita",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Guarisce Nefarita",
                "tipo_effetto": "Guarigione",
                "valore": "3",
                "statistica_target": "azioni",
                "descrizione_effetto": "Può solo essere assegnato a un Nefarita di qualsiasi Apostolo. Se il Nefarita è ferito, può guarire al costo di tre Azioni",
                "condizioni": ["Solo Nefarita di qualsiasi Apostolo", "Nefarita deve essere ferito"],
                "limitazioni": ["Costa 3 Azioni"],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI ALGEROTH. Può solo essere assegnato a un Nefarita di qualsiasi Apostolo. Se il Nefarita è ferito, può guarire al costo di tre Azioni",
        "flavour_text": "",
        "keywords": ["Nefarita", "Seguace di Algeroth"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Algeroth", "Solo Nefarita"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 4,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Indigestione": {
        "nome": "Indigestione",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Algeroth",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Penalità Azioni Avversari",
                "tipo_effetto": "Modificatore",
                "valore": "-2",
                "statistica_target": "azioni",
                "descrizione_effetto": "Tutti gli avversari di questo guerriero subiscono una penalità un -2 in A",
                "condizioni": [],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI ALGEROTH. Tutti gli avversari di questo guerriero subiscono una penalità un -2 in A.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Algeroth"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 8,
        "quantita": 6,
        "quantita_minima_consigliata": 3,
        "fondamentale": False       
    },
    
    "Vento Della Pazzia": {
        "nome": "Vento Della Pazzia",
        "costo_destino": "1 Azione",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Muawijhe",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Tutti i Guerrieri",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Infligge Danno a Tutti",
                "tipo_effetto": "Combattimento",
                "valore": "1",
                "statistica_target": "azioni",
                "descrizione_effetto": "Una volta per Turno, al costo di un'Azione, questo guerriero può invocare il VENTO DELLA PAZZIA. Invocare il Vento non viene considerato un'Azione d'Attacco. Per ogni 5D spesi, è inflitto un Punto Danno su ogni guerriero in gioco, incluso l'Evocatore. Se i Punti Danno eguagliano o superano A, allora il guerriero è ferito",
                "condizioni": ["Una volta per turno", "Costo di 1 Azione per invocare", "5 Punti Destino per ogni punto danno"],
                "limitazioni": ["Non è considerata Azione d'Attacco", "Colpisce anche l'evocatore"],
                "effetti_collaterali": ["Tutti i guerrieri in gioco subiscono danno"]
            }
        ],	 
        "testo_carta": "DONO DI MUAWIJHE. Una volta per Turno, al costo di un'Azione, questo guerriero può invocare il VENTO DELLA PAZZIA. Invocare il Vento non viene considerato un'Azione d'Attacco. Per ogni 5D spesi, è inflitto un Punto Danno su ogni guerriero in gioco, incluso l'Evocatore. Se i Punti Danno eguagliano o superano A, allora il guerriero è ferito.",
        "flavour_text": "",
        "keywords": ["Seguace di Muawijhe"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Muawijhe"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 6,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Distorsione": {
        "nome": "Distorsione",
        "costo_destino": "10 Punti Destino",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Algeroth",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Equipaggiamento",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": "10",
                "statistica_target": "destino",
                "descrizione_effetto": "Spendendo in qualsiasi momento 10D, questo guerriero potrà scegliere un'Arma o una carta di Equipaggiamento in gioco e scartarla",
                "condizioni": ["Costo di 10 Punti Destino", "In qualsiasi momento"],
                "limitazioni": ["Solo Armi o Equipaggiamenti in gioco"],
                "effetti_collaterali": ["La carta scelta viene scartata"]
            }
        ],	 
        "testo_carta": "DONO DI ALGEROTH. Spendendo in qualsiasi momento 10D, questo guerriero potrà scegliere un'Arma o una carta di Equipaggiamento in gioco e scartarla.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Algeroth"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Ruggine": {
        "nome": "Ruggine",
        "costo_destino": "10 Punti Destino",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Demnogonis",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Equipaggiamento",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": "10",
                "statistica_target": "destino",
                "descrizione_effetto": "Spendendo 10D questo guerriero potrà scegliere un'Arma o una carta Equipaggiamento del nemico e scartarla",
                "condizioni": ["Costo di 10 Punti Destino"],
                "limitazioni": ["Solo Armi o Equipaggiamenti nemici"],
                "effetti_collaterali": ["La carta scelta viene scartata"]
            }
        ],	 
        "testo_carta": "DONO DI DEMNOGONIS. Spendendo 10D questo guerriero potrà scegliere un'Arma o una carta Equipaggiamento del nemico e scartarla.",
        "flavour_text": "",
        "keywords": ["Seguace di Demnogonis"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Demnogonis"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 1,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Deformazione Dimensionale": {
        "nome": "Deformazione Dimensionale",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Algeroth",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Uccide Automaticamente",
                "tipo_effetto": "Combattimento",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "I guerrieri feriti dal possessore di questo Dono sono automaticamente uccisi",
                "condizioni": ["Guerriero deve essere ferito dal possessore"],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI ALGEROTH. I guerrieri feriti dal possessore di questo Dono sono automaticamente uccisi.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Algeroth"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 2,
        "fondamentale": True       
    },
    
    "Mano Della Morte": {
        "nome": "Mano Della Morte",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Ilian",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Bonus Caratteristiche",
                "tipo_effetto": "Modificatore",
                "valore": "+2",
                "statistica_target": "combattimento e sparare",
                "descrizione_effetto": "Le C e S del guerriero guadagnano un bonus di un +2",
                "condizioni": [],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI ILIAN. Le C e S del guerriero guadagnano un bonus di un +2.",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Ilian"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 1,
        "quantita": 5,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Infezione": {
        "nome": "Infezione",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Demnogonis",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Uccide Automaticamente",
                "tipo_effetto": "Combattimento",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Gli avversari feriti da questo guerriero, sono automaticamente morti",
                "condizioni": ["Avversario deve essere ferito da questo guerriero"],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI DEMNOGONIS. Gli avversari feriti da questo guerriero, sono automaticamente morti.",
        "flavour_text": "",
        "keywords": ["Seguace di Demnogonis"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Demnogonis"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 2,
        "fondamentale": True       
    },
    
    "Legame Necrovisuale": {
        "nome": "Legame Necrovisuale",
        "costo_destino": "1 Azione",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Algeroth",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Giocatore Avversario",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Osserva Carte Avversario",
                "tipo_effetto": "Carte",
                "valore": "1",
                "statistica_target": "azioni",
                "descrizione_effetto": "Può solo essere assegnato a un Nefarita di qualsiasi Apostolo. Al costo di un'Azione, puoi guardare le carte in mano a un altro giocatore",
                "condizioni": ["Solo Nefarita di qualsiasi Apostolo", "Costo di 1 Azione"],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI ALGEROTH. Può solo essere assegnato a un Nefarita di qualsiasi Apostolo. Al costo di un'Azione, puoi guardare le carte in mano a un altro giocatore.",
        "flavour_text": "",
        "keywords": ["Nefarita", "Seguace di Algeroth"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Algeroth", "Solo Nefarita"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 6,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Confondere": {
        "nome": "Confondere",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Muawijhe",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Modifica Tattica Combattimento",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "combattimento",
                "descrizione_effetto": "Questo guerriero può cambiare la Tattica di Combattimento scelta per quel combattimento",
                "condizioni": [],
                "limitazioni": ["Solo per il combattimento corrente"],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI MUAWIJHE. Questo guerriero può cambiare la Tattica di Combattimento scelta per quel combattimento.",
        "flavour_text": "",
        "keywords": ["Seguace di Muawijhe"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Muawijhe"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True       
    },
    
    "Danza Folle": {
        "nome": "Danza Folle",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Muawijhe",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "In Combattimento",
        "set_espansione": "Base",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Penalità Caratteristiche Avversari",
                "tipo_effetto": "Modificatore",
                "valore": "-2",
                "statistica_target": "combattimento e sparare",
                "descrizione_effetto": "Tutti i guerrieri che combattono contro il possessore di questo Dono ricevono una penalità di -2 in C e S",
                "condizioni": ["Guerrieri devono combattere contro il possessore"],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI MUAWIJHE. Tutti i guerrieri che combattono contro il possessore di questo Dono ricevono una penalità di -2 in C e S.",
        "flavour_text": "",
        "keywords": ["Seguace di Muawijhe"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Muawijhe"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 8,
        "quantita": 3,
        "quantita_minima_consigliata": 2,
        "fondamentale": False       
    },

    # Inquisition

    "Evocazione Oscura": {
        "nome": "Evocazione Oscura",
        "costo_destino": "3 Azioni",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Algeroth",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Equipaggiamento",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Inquisition",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Cerca Carta Equipaggiamento",
                "tipo_effetto": "Carte",
                "valore": "3",
                "statistica_target": "azioni",
                "descrizione_effetto": "Al costo di tre Azioni, questo guerriero può cercare nel tuo mazzo di carte da Pescare una qualsiasi carta Equipaggiamento dell'Oscura Legione ed equipaggiarsi con quella. Scarta questa carta dopo l'uso.",
                "condizioni": ["Costo di 3 Azioni"],
                "limitazioni": ["Solo carta Equipaggiamento dell'Oscura Legione", "Scarta questa carta dopo l'uso"],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI ALGEROTH. Al costo di tre Azioni, questo guerriero può cercare nel tuo mazzo di carte da Pescare una qualsiasi carta Equipaggiamento dell'Oscura Legione ed equipaggiarsi con quella. Scarta questa carta dopo l'uso.",
        "flavour_text": "",
        "keywords": ["Seguace di Algeroth"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Algeroth"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 1,
        "quantita": 3,
        "quantita_minima_consigliata": 2,
        "fondamentale": True       
    },
    
    "Potere Mostruoso": {
        "nome": "Potere Mostruoso",
        "costo_destino": "",
        "tipo": "Dono dell'Oscura Simmetria",
        "apostolo_padre": None,
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Bonus Caratteristiche",
                "tipo_effetto": "Modificatore",
                "valore": "+2",
                "statistica_target": "combattimento, sparare, azioni e velocità",
                "descrizione_effetto": "Può solo essere assegnata agli Eretici. L'Eretico guadagna un +2 in C, S, A e V.",
                "condizioni": ["Solo Eretici"],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DELL'OSCURA SIMMETRIA. PUÒ SOLO ESSERE ASSEGNATA AGLI ERETICI. L'Eretico guadagna un +2 in C, S, A e V.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Eretici"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 8,
        "quantita": 3,
        "quantita_minima_consigliata": 2,
        "fondamentale": False       
    },
    
    "Forza Primordiale": {
        "nome": "Forza Primordiale",
        "costo_destino": "",
        "tipo": "Dono dell'Oscura Simmetria",
        "apostolo_padre": None,
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Bonus Caratteristiche",
                "tipo_effetto": "Modificatore",
                "valore": "+1",
                "statistica_target": "combattimento, sparare, azioni e velocità",
                "descrizione_effetto": "Può solo essere assegnata agli Eretici. L'Eretico guadagna un +1 in C, S, A e V.",
                "condizioni": ["Solo Eretici"],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DELL'OSCURA SIMMETRIA. PUÒ SOLO ESSERE ASSEGNATA AGLI ERETICI. L'Eretico guadagna un +1 in C, S, A e V.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Eretici"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 4,
        "quantita": 16,
        "quantita_minima_consigliata": 2,
        "fondamentale": False       
    },
    
    "Plagio": {
        "nome": "Plagio",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Ilian",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Tutti i Guerrieri",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Copia Abilità Guerriero",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "varie",
                "descrizione_effetto": "Scegli un guerriero non-Personalità in gioco. Il guerriero che riceve questo dono, ha ora tutte le abilità (non C, S, A e V) segnate sulla carta del guerriero scelto, finché questa carta è in gioco. Puoi scegliere il guerriero che desideri copiare solo al momento in cui giochi questa carta e non lo puoi più modificare in seguito.",
                "condizioni": ["Scegliere un guerriero non-Personalità in gioco"],
                "limitazioni": ["Non copia le caratteristiche C, S, A e V", "Non può modificare la scelta dopo aver giocato la carta"],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI ILIAN. Scegli un guerriero non-Personalità in gioco. Il guerriero che riceve questo dono, ha ora tutte le abilità (non C, S, A e V) segnate sulla carta del guerriero scelto, finché questa carta è in gioco. Puoi scegliere il guerriero che desideri copiare solo al momento in cui giochi questa carta e non lo puoi più modificare in seguito.",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Ilian", "Non può essere usato su Personalita"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 10,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": True       
    },
    
    "Autorità": {
        "nome": "Autorità",
        "costo_destino": "2 Azioni",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Semai",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Istantanea",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Osserva Carte Avversario",
                "tipo_effetto": "Carte",
                "valore": "2",
                "statistica_target": "azioni",
                "descrizione_effetto": "Al costo di due Azioni, questo guerriero Ti permette di vedere le carte in mano ad un Tuo avversario.",
                "condizioni": ["Costo di 2 Azioni"],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DI SEMAI. Al costo di due Azioni, questo guerriero Ti permette di vedere le carte in mano ad un Tuo avversario.",
        "flavour_text": "",
        "keywords": ["Seguace di Semai"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Semai"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 8,
        "quantita": 7,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Forza Empia": {
        "nome": "Forza Empia",
        "costo_destino": "",
        "tipo": "Dono dell'Oscura Simmetria",
        "apostolo_padre": None,
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Bonus Caratteristiche",
                "tipo_effetto": "Modificatore",
                "valore": "+4",
                "statistica_target": "combattimento, sparare, azioni e velocità",
                "descrizione_effetto": "Può solo essere assegnato agli Eretici. L'Eretico guadagna un +4 in C, S, A e V.",
                "condizioni": ["Solo Eretici"],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DELL'OSCURA SIMMETRIA. PUÒ SOLO ESSERE ASSEGNATO AGLI ERETICI. L'Eretico guadagna un +4 in C, S, A e V.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Eretici"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 10,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": True       
    },
    
    "Occhio Sacrilego": {
        "nome": "Occhio Sacrilego",
        "costo_destino": "",
        "tipo": "Dono dell'Oscura Simmetria",
        "apostolo_padre": None,
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Modifica Azione Avversari",
                "tipo_effetto": "Modificatore",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Può solo essere assegnato agli Eretici. Gli avversari dell'Eretico sono accecati. Se l'avversario non paga 3D, il combattimento termina dopo l'Attacco dell'Eretico e l'avversario non può contrattaccare. Se li paga il combattimento è normale.",
                "condizioni": ["Solo Eretici"],
                "limitazioni": ["Avversario deve pagare 3D per contrattaccare"],
                "effetti_collaterali": ["Se non paga, combattimento termina dopo attacco dell'Eretico"]
            }
        ],	 
        "testo_carta": "DONO DELL'OSCURA SIMMETRIA. PUÒ SOLO ESSERE ASSEGNATO AGLI ERETICI. Gli avversari dell'Eretico sono accecati. Se l'avversario non paga 3D, il combattimento termina dopo l'Attacco dell'Eretico e l'avversario non può contrattaccare. Se li paga il combattimento è normale.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Eretici"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 2,
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Forza Malvagia": {
        "nome": "Forza Malvagia",
        "costo_destino": "",
        "tipo": "Dono dell'Oscura Simmetria",
        "apostolo_padre": None,
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Guerriero Proprio",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Inquisition",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Bonus Caratteristiche",
                "tipo_effetto": "Modificatore",
                "valore": "+5",
                "statistica_target": "combattimento, sparare, azioni e velocità",
                "descrizione_effetto": "Può solo essere assegnato agli Eretici. L'Eretico guadagna un +5 in C, S, A e V.",
                "condizioni": ["Solo Eretici"],
                "limitazioni": [],
                "effetti_collaterali": []
            }
        ],	 
        "testo_carta": "DONO DELL'OSCURA SIMMETRIA. PUÒ SOLO ESSERE ASSEGNATA AGLI ERETICI. L'Eretico guadagna un +5 in C, S, A e V.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Eretici"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 2,
        "fondamentale": True       
    },
    
    "Occhio Malvagio": {
        "nome": "Occhio Malvagio",
        "costo_destino": "",
        "tipo": "Dono dell'Oscura Simmetria",
        "apostolo_padre": None,
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
       "bersaglio": "Guerriero Avversario",
        "durata": "Permanente",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Modifica Azione Avversari",
                "tipo_effetto": "Modificatore",
                "valore": "3",
                "statistica_target": "destino",
                "descrizione_effetto": "Può solo essere assegnato agli Eretici. Gli avversari dell'Eretico sono accecati. Se l'avversario non paga 3D, il combattimento termina dopo l'Attacco dell'Eretico e l'avversario non può contrattaccare. Se li paga il combattimento è normale.",
                "condizioni": ["Solo Eretici"],
                "limitazioni": ["Avversario deve pagare 3D per contrattaccare"],
                "effetti_collaterali": ["Se non paga, combattimento termina dopo attacco dell'Eretico"]
            }
        ],	 
        "testo_carta": "DONO DELL'OSCURA SIMMETRIA. PUÒ SOLO ESSERE ASSEGNATO AGLI ERETICI. Gli avversari dell'Eretico sono accecati. Se l'avversario non paga 3D, il combattimento termina dopo l'Attacco dell'Eretico e l'avversario non può contrattaccare. Se li paga il combattimento è normale.",
        "flavour_text": "",
        "keywords": ["Eretico"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Eretici"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 4,
        "quantita": 3,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Untore": {
        "nome": "Untore",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Demnogonis",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Doomtrooper",
        "durata": "Permanente",
        "timing": "In Combattimento",
        "set_espansione": "Inquisition",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Applica Segnalini",
                "tipo_effetto": "Modificatore",
                "valore": "-2",
                "statistica_target": "azioni",
                "descrizione_effetto": "Ogni Doomtrooper che combatte questo guerriero è infetto. Metti un Segnalino sul guerriero. I Segnalini danno un -2 in A e possono essere rimossi solo quando il giocatore deve mettere un Segnalino su un Doomtrooper non infetto durante ognuna delle sue Fasi Pescare. I Segnalini possono essere rimossi in ogni momento, spendendo 4D per ognuno.",
                "condizioni": ["Doomtrooper deve combattere questo guerriero"],
                "limitazioni": ["Solo sui Doomtroopers", "Segnalini danno -2 in A"],
                "effetti_collaterali": ["Segnalini rimossi solo in Fase Pescare o spendendo 4D"]
            }
        ],	 
        "testo_carta": "DONO DI DEMNOGONIS. Ogni Doomtrooper che combatte questo guerriero è infetto. Metti un Segnalino sul guerriero. I Segnalini danno un -2 in A A partire da questo momento, il giocatore deve mettere un Segnalino su un Doomtrooper non infetto durante ognuna delle sue Fasi Pescare. I Segnalini possono essere rimossi in ogni momento, spendendo 4D per ognuno.",
        "flavour_text": "",
        "keywords": ["Seguace di Demnogonis"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Demnogonis"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 2,
        "quantita": 6,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },
    
    "Urlo Lacerante": {
        "nome": "Urlo Lacerante",
        "costo_destino": "1 Azione",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Muawijhe",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Tutti i Guerrieri",
        "durata": "Istantanea",
        "timing": "Turno Proprio",
        "set_espansione": "Inquisition",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Infligge Segnalini Terrore",
                "tipo_effetto": "Controllo",
                "valore": "1",
                "statistica_target": "azioni",
                "descrizione_effetto": "Puoi urlare ad ogni numero di guerrieri, al costo complessivo di un'Azione. Metti un Segnalino su ogni guerriero terrorizzato. Ogni Urlo Ti costa 2D. I guerrieri terrorizzati devono spendere 4D per Attaccare. I Segnalini saranno rimossi all'inizio del Tuo prossimo Turno.",
                "condizioni": ["Costo complessivo di 1 Azione", "2 Punti Destino per ogni urlo"],
                "limitazioni": ["Guerrieri terrorizzati devono spendere 4D per attaccare"],
                "effetti_collaterali": ["Segnalini rimossi all'inizio del prossimo turno"]
            }
        ],	 
        "testo_carta": "DONO DI MUAWIJHE. Puoi urlare ad ogni numero di guerrieri, al costo complessivo di un'Azione. Metti un Segnalino su ogni guerriero terrorizzato. Ogni Urlo Ti costa 2D. I guerrieri terrorizzati devono spendere 4D per Attaccare. I Segnalini saranno rimossi all'inizio del Tuo prossimo Turno.",
        "flavour_text": "",
        "keywords": ["Seguace di Muawijhe"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Muawijhe"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 2,
        "quantita": 9,
        "quantita_minima_consigliata": 1,
        "fondamentale": False       
    },

    # Warzone

    "Il Potere Della Percezione": {
        "nome": "Il Potere Della Percezione",
        "costo_destino": "",
        "tipo": "Dono degli Apostoli",
        "apostolo_padre": "Ilian",
        "rarity": "Common",     
        "fazioni_permesse": ["Oscura Legione"],
        "bersaglio": "Giocatore Avversario",
        "durata": "Permanente",
        "timing": "In Ogni Momento",
        "set_espansione": "Warzone",
        "numero_carta": "",       
        "effetti": [
            {
                "nome_effetto": "Assegna Carte",
                "tipo_effetto": "Carte",
                "valore": "",
                "statistica_target": "",
                "descrizione_effetto": "Giocabile in qualsiasi momento mentre il tuo avversario prende una carta dal mazzo, dagli scarti o dalla collezione. Scartando questo dono il tuo avversario è costretto a eliminare la carta dal gioco. Non ti è concesso guardare la carta.",
                "condizioni": ["Avversario deve star prendendo una carta dal mazzo, scarti o collezione"],
                "limitazioni": ["Non puoi guardare la carta eliminata", "Scarta questo dono dopo l'uso"],
                "effetti_collaterali": ["La carta dell'avversario viene eliminata dal gioco"]
            }
        ],	 
        "testo_carta": "DONO DI ILIAN. Giocabile in qualsiasi momento mentre il tuo avversario prende una carta dal mazzo, dagli scarti o dalla collezione. Scartando questo dono il tuo avversario è costretto a eliminare la carta dal gioco. Non ti è concesso guardare la carta.",
        "flavour_text": "",
        "keywords": ["Seguace di Ilian"],
        "stato_gioco": {
            "in_gioco": False,
            "utilizzata": False,
            "bersagli_attuali": []
        },
        "restrizioni": ["Solo Seguaci di Ilian"],
        "corruzione_applicata": {},
        "mutazioni_applicate": {},
        "penalita_giocatore": {},
        "contatori_oscura": {},
        "livello_corruzione": 0,
        "valore_strategico": 10,
        "quantita": 2,
        "quantita_minima_consigliata": 1,
        "fondamentale": True       
    },

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
        apostolo_padre=ApostoloOscuraSimmetria(data["apostolo_padre"]) if data["apostolo_padre"] and data["apostolo_padre"] != ApostoloOscuraSimmetria.NESSUNO else ApostoloOscuraSimmetria.NESSUNO,
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
        "effetti_mancanti": [],
        "timing_errato": [],
        "durata_errata": [],
        "bersaglio_errato": []
    }
    
    for nome, carta in DATABASE_OSCURA_SIMMETRIA.items():
        # Verifica fazioni (deve essere solo Oscura Legione)
        if carta["fazioni_permesse"] != ["Oscura Legione"]:
            errori["fazioni_errate"].append(f"{nome}: {carta['fazioni_permesse']}")
        
        # Verifica coerenza apostoli e doni
        if carta["tipo"] == "Dono dell'Apostolo":
            if not carta["apostolo_padre"]:
                errori["apostoli_inconsistenti"].append(f"{nome}: Dono senza apostolo")
            if not any("Solo Seguaci di" in r for r in carta["restrizioni"]):
                errori["doni_senza_restrizioni"].append(f"{nome}: Manca restrizione Seguaci")
        
        if carta["timing"] not in [t.value for t in TimingOscura]:
           errori["timing_errato"].append(f"{nome}: {carta['timing']}")

        if carta["durata"] not in [t.value for t in DurataOscura]:
           errori["durata_errata"].append(f"{nome}: {carta['durata']}")

        if carta["bersaglio"] not in [t.value for t in BersaglioOscura]:
           errori["bersaglio_errato"].append(f"{nome}: {carta['bersaglio']}")


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
    
    
    # Carte per rarità
    carte_rare = get_carte_per_rarity("Rare")
    print(f"✓ Carte Rare: {len(carte_rare)}")
    
   
"""
Database delle carte Missione di Mutant Chronicles/Doomtrooper
Contiene tutte le informazioni e metodi necessari per la creazione di istanze 
della classe Missione basate sulle carte ufficiali del gioco.
VERSIONE CORRETTA - Allineata alle regole ufficiali del regolamento
"""

from typing import Dict, List, Optional, Any
from source.cards.Missione import (
    Missione, TipoMissione, DifficoltaMissione, TipoBersaglioMissione,
    ObiettivoMissione, RicompensaMissione, StatoMissione
)
from source.cards.Guerriero import Fazione, Rarity


# Database completo delle carte Missione
DATABASE_MISSIONI = {
    # MISSIONI GENERICHE - UCCISIONE
    "Caccia al Nemico": {
        "nome": "Caccia al Nemico",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Common",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Bauhaus", "Capitol", "Imperiale", "Mishima", "Cybertronic"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Uccidi 1 guerriero nemico",
            "tipo_obiettivo": "Uccidere",
            "valore_richiesto": 1,
            "condizioni_speciali": ["Guerriero nemico"]
        },
        "ricompensa": {
            "punti_promozione": 1,
            "punti_destino": 1,
            "carte_extra": 0,
            "effetti_speciali": [],
            "descrizione": "1 Punto Promozione e 1 Punto Destino"
        },
        "set_espansione": "Base",
        "numero_carta": "M002",
        "testo_carta": "Assegna questa missione a un tuo guerriero. Se quel guerriero uccide 1 guerriero nemico, guadagni 1 Punto Promozione e 1 Punto Destino.",
        "flavour_text": "La vendetta è un piatto che va servito freddo... e letale.",
        "keywords": ["Missione", "Uccisione"],
        "restrizioni": ["Solo Doomtrooper"],
        "condizioni_speciali": [],
        "quantita":9
    },

    "Eliminazione": {
        "nome": "Eliminazione",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Difficile",
        "rarity": "Uncommon",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Bauhaus", "Capitol", "Imperiale", "Mishima", "Cybertronic"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Uccidi 3 guerrieri nemici",
            "tipo_obiettivo": "Uccidere",
            "valore_richiesto": 3,
            "condizioni_speciali": ["Guerrieri nemici", "Stesso turno"]
        },
        "ricompensa": {
            "punti_promozione": 5,
            "punti_destino": 2,
            "carte_extra": 1,
            "effetti_speciali": [],
            "descrizione": "5 Punti Promozione, 2 Punti Destino e pesca 1 carta"
        },
        "set_espansione": "Base",
        "numero_carta": "M003",
        "testo_carta": "Assegna questa missione a un tuo guerriero. Se quel guerriero uccide 3 guerrieri nemici nello stesso turno, guadagni 5 Punti Promozione, 2 Punti Destino e peschi 1 carta.",
        "flavour_text": "Un massacro metodico che lascia il campo di battaglia cosparso di cadaveri.",
        "keywords": ["Missione", "Uccisione", "Difficile"],
        "restrizioni": ["Solo Doomtrooper"],
        "condizioni_speciali": ["Tutte le uccisioni nello stesso turno"],
        "quantita":9
    },

    # MISSIONI DI SOPRAVVIVENZA
    "Resistenza Eroica": {
        "nome": "Resistenza Eroica",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Common",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Bauhaus", "Capitol", "Imperiale", "Mishima", "Cybertronic"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Sopravvivi per 3 turni consecutivi",
            "tipo_obiettivo": "Sopravvivere",
            "valore_richiesto": 3,
            "condizioni_speciali": ["Turni consecutivi", "Sotto attacco"]
        },
        "ricompensa": {
            "punti_promozione": 2,
            "punti_destino": 1,
            "carte_extra": 0,
            "effetti_speciali": [],
            "descrizione": "2 Punti Promozione e 1 Punto Destino"
        },
        "set_espansione": "Base",
        "numero_carta": "M004",
        "testo_carta": "Assegna questa missione a un tuo guerriero. Se quel guerriero sopravvive per 3 turni consecutivi mentre è sotto attacco, guadagni 2 Punti Promozione e 1 Punto Destino.",
        "flavour_text": "La vera forza si manifesta quando tutto sembra perduto.",
        "keywords": ["Missione", "Sopravvivenza"],
        "restrizioni": ["Solo Doomtrooper"],
        "condizioni_speciali": ["Deve essere attaccato almeno una volta per turno"],
        "quantita":9
    },

    "Ultimo Baluardo": {
        "nome": "Ultimo Baluardo",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Difficile",
        "rarity": "Rare",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Bauhaus", "Capitol", "Imperiale", "Mishima", "Cybertronic"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Sopravvivi come unico guerriero in gioco per 2 turni",
            "tipo_obiettivo": "Sopravvivere",
            "valore_richiesto": 2,
            "condizioni_speciali": ["Unico guerriero", "Turni consecutivi"]
        },
        "ricompensa": {
            "punti_promozione": 4,
            "punti_destino": 3,
            "carte_extra": 2,
            "effetti_speciali": ["Immune alle Arti per 1 turno"],
            "descrizione": "4 Punti Promozione, 3 Punti Destino, pesca 2 carte e immunità alle Arti"
        },
        "set_espansione": "Base",
        "numero_carta": "M005",
        "testo_carta": "Assegna questa missione a un tuo guerriero. Se quel guerriero rimane come unico guerriero in gioco per 2 turni consecutivi, guadagni la ricompensa e diventa immune alle Arti per 1 turno.",
        "flavour_text": "Quando tutti cadono, uno solo rimane a difendere ciò che è giusto.",
        "keywords": ["Missione", "Sopravvivenza", "Eroica"],
        "restrizioni": ["Solo Doomtrooper"],
        "condizioni_speciali": ["Tutti gli altri guerrieri devono essere fuori gioco"],
        "quantita":9
    },

    # MISSIONI SPECIFICHE DELLE CORPORAZIONI
    "Operazione Heimburg": {
        "nome": "Operazione Heimburg",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Uncommon",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Bauhaus"],
        "corporazioni_specifiche": ["Bauhaus"],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Controlla una Fortificazione nemica per 1 turno",
            "tipo_obiettivo": "Controllare",
            "valore_richiesto": 1,
            "condizioni_speciali": ["Fortificazione nemica", "Controllo completo"]
        },
        "ricompensa": {
            "punti_promozione": 3,
            "punti_destino": 2,
            "carte_extra": 0,
            "effetti_speciali": ["Bonus Armatura +2 per 2 turni"],
            "descrizione": "3 Punti Promozione, 2 Punti Destino e +2 Armatura"
        },
        "set_espansione": "Base",
        "numero_carta": "M006",
        "testo_carta": "Solo guerrieri Bauhaus. Controlla una Fortificazione nemica per 1 turno completo. Ricompensa: 3 Punti Promozione, 2 Punti Destino e +2 Armatura per 2 turni.",
        "flavour_text": "L'ingegneria Bauhaus conquista anche le fortezze più imprendibili.",
        "keywords": ["Missione", "Bauhaus", "Controllo"],
        "restrizioni": ["Solo guerrieri Bauhaus"],
        "condizioni_speciali": ["Fortificazione deve essere controllata dall'avversario"],
        "quantita":9
    },

    "Assalto Capitol": {
        "nome": "Assalto Capitol",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Uncommon",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Capitol"],
        "corporazioni_specifiche": ["Capitol"],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Uccidi 2 guerrieri usando armi da fuoco",
            "tipo_obiettivo": "Uccidere",
            "valore_richiesto": 2,
            "condizioni_speciali": ["Solo con armi da fuoco", "Statistica Sparare"]
        },
        "ricompensa": {
            "punti_promozione": 3,
            "punti_destino": 1,
            "carte_extra": 0,
            "effetti_speciali": ["Bonus Sparare +2 per 2 turni"],
            "descrizione": "3 Punti Promozione, 1 Punto Destino e +2 Sparare"
        },
        "set_espansione": "Base",
        "numero_carta": "M007",
        "testo_carta": "Solo guerrieri Capitol. Uccidi 2 guerrieri usando la statistica Sparare. Ricompensa: 3 Punti Promozione, 1 Punto Destino e +2 Sparare per 2 turni.",
        "flavour_text": "La superiorità tecnologica Capitol si manifesta in ogni colpo sparato.",
        "keywords": ["Missione", "Capitol", "Armi da Fuoco"],
        "restrizioni": ["Solo guerrieri Capitol"],
        "condizioni_speciali": ["Uccisioni devono usare statistica Sparare"],
        "quantita":9
    },

    "Onore Imperiale": {
        "nome": "Onore Imperiale",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Uncommon",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Imperiale"],
        "corporazioni_specifiche": ["Imperiale"],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Vinci 3 combattimenti corpo a corpo",
            "tipo_obiettivo": "Vincere",
            "valore_richiesto": 3,
            "condizioni_speciali": ["Solo corpo a corpo", "Statistica Combattimento"]
        },
        "ricompensa": {
            "punti_promozione": 3,
            "punti_destino": 1,
            "carte_extra": 0,
            "effetti_speciali": ["Bonus Combattimento +2 per 2 turni"],
            "descrizione": "3 Punti Promozione, 1 Punto Destino e +2 Combattimento"
        },
        "set_espansione": "Base",
        "numero_carta": "M008",
        "testo_carta": "Solo guerrieri Imperiale. Vinci 3 combattimenti corpo a corpo. Ricompensa: 3 Punti Promozione, 1 Punto Destino e +2 Combattimento per 2 turni.",
        "flavour_text": "L'onore Imperiale si guadagna con il sangue e l'acciaio.",
        "keywords": ["Missione", "Imperiale", "Corpo a Corpo"],
        "restrizioni": ["Solo guerrieri Imperiale"],
        "condizioni_speciali": ["Combattimenti devono usare statistica Combattimento"],
        "quantita":9
    },

    "Via del Bushido": {
        "nome": "Via del Bushido",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Difficile",
        "rarity": "Rare",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Mishima"],
        "corporazioni_specifiche": ["Mishima"],
        "restrizioni_guerriero": ["Samurai", "Ninja"],
        "obiettivo": {
            "descrizione": "Uccidi un guerriero con valore superiore in singolo combattimento",
            "tipo_obiettivo": "Uccidere",
            "valore_richiesto": 1,
            "condizioni_speciali": ["Valore superiore", "Singolo combattimento", "Senza supporto"]
        },
        "ricompensa": {
            "punti_promozione": 4,
            "punti_destino": 2,
            "carte_extra": 1,
            "effetti_speciali": ["Onore Mishima: +1 a tutte le statistiche per 3 turni"],
            "descrizione": "4 Punti Promozione, 2 Punti Destino, 1 carta e Onore Mishima"
        },
        "set_espansione": "Base",
        "numero_carta": "M009",
        "testo_carta": "Solo Samurai o Ninja Mishima. Uccidi in singolo combattimento un guerriero con valore superiore al tuo. Ricompensa include Onore Mishima: +1 a tutte le statistiche per 3 turni.",
        "flavour_text": "La via del guerriero non conosce compromessi né paura.",
        "keywords": ["Missione", "Mishima", "Onore", "Bushido"],
        "restrizioni": ["Solo Samurai o Ninja Mishima"],
        "condizioni_speciali": ["Nessun supporto esterno", "Combattimento 1 vs 1"],
        "quantita":9
    },

    "Supremazia Cybertronic": {
        "nome": "Supremazia Cybertronic",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Uncommon",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Cybertronic"],
        "corporazioni_specifiche": ["Cybertronic"],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Controlla 2 Equipaggiamenti tecnologici simultaneamente",
            "tipo_obiettivo": "Controllare",
            "valore_richiesto": 2,
            "condizioni_speciali": ["Equipaggiamenti tecnologici", "Simultaneamente"]
        },
        "ricompensa": {
            "punti_promozione": 2,
            "punti_destino": 3,
            "carte_extra": 0,
            "effetti_speciali": ["Efficienza Tecnologica: -1 costo Equipaggiamenti per 3 turni"],
            "descrizione": "2 Punti Promozione, 3 Punti Destino e Efficienza Tecnologica"
        },
        "set_espansione": "Base",
        "numero_carta": "M010",
        "testo_carta": "Solo guerrieri Cybertronic. Controlla simultaneamente 2 Equipaggiamenti tecnologici. Ricompensa include Efficienza Tecnologica: -1 costo per equipaggiare per 3 turni.",
        "flavour_text": "La tecnologia Cybertronic trasforma ogni guerriero in una macchina perfetta.",
        "keywords": ["Missione", "Cybertronic", "Tecnologia"],
        "restrizioni": ["Solo guerrieri Cybertronic"],
        "condizioni_speciali": ["Equipaggiamenti devono essere attivi simultaneamente"],
        "quantita":9
    },

    # MISSIONI DELLA FRATELLANZA
    "Purificazione": {
        "nome": "Purificazione",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Common",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Fratellanza"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Uccidi 2 guerrieri dell'Oscura Legione",
            "tipo_obiettivo": "Uccidere",
            "valore_richiesto": 2,
            "condizioni_speciali": ["Solo Oscura Legione"]
        },
        "ricompensa": {
            "punti_promozione": 3,
            "punti_destino": 1,
            "carte_extra": 0,
            "effetti_speciali": ["Benedizione: Immune a 1 carta Oscura Simmetria"],
            "descrizione": "3 Punti Promozione, 1 Punto Destino e Benedizione"
        },
        "set_espansione": "Base",
        "numero_carta": "M011",
        "testo_carta": "Solo guerrieri della Fratellanza. Uccidi 2 guerrieri dell'Oscura Legione. Ricompensa include Benedizione: immune alla prossima carta Oscura Simmetria.",
        "flavour_text": "La Luce purifica tutto ciò che tocca, dissolvendo le ombre dell'oscurità.",
        "keywords": ["Missione", "Fratellanza", "Purificazione"],
        "restrizioni": ["Solo guerrieri della Fratellanza"],
        "condizioni_speciali": ["Solo guerrieri dell'Oscura Legione"],
        "quantita":9
    },

    "Esorcismo": {
        "nome": "Esorcismo",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Difficile",
        "rarity": "Rare",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Fratellanza"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": ["Inquisitore", "Mistico"],
        "obiettivo": {
            "descrizione": "Elimina 1 carta Oscura Simmetria in gioco",
            "tipo_obiettivo": "Eliminare",
            "valore_richiesto": 1,
            "condizioni_speciali": ["Carta Oscura Simmetria", "In gioco"]
        },
        "ricompensa": {
            "punti_promozione": 4,
            "punti_destino": 2,
            "carte_extra": 1,
            "effetti_speciali": ["Santificazione: +2 Armatura contro Oscura Legione per 3 turni"],
            "descrizione": "4 Punti Promozione, 2 Punti Destino, 1 carta e Santificazione"
        },
        "set_espansione": "Inquisition",
        "numero_carta": "M012",
        "testo_carta": "Solo Inquisitori o Mistici. Elimina 1 carta Oscura Simmetria in gioco. Ricompensa include Santificazione: +2 Armatura contro l'Oscura Legione per 3 turni.",
        "flavour_text": "L'oscurità non può resistere alla luce della vera fede.",
        "keywords": ["Missione", "Fratellanza", "Esorcismo"],
        "restrizioni": ["Solo Inquisitori o Mistici della Fratellanza"],
        "condizioni_speciali": ["Carta deve essere attualmente in gioco"],
        "quantita":9
    },

    # MISSIONI DELL'OSCURA LEGIONE
    "Corruzione": {
        "nome": "Corruzione",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Common",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Oscura_Legione"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Assegna 2 Doni Oscuri a guerrieri nemici",
            "tipo_obiettivo": "Corrompere",
            "valore_richiesto": 2,
            "condizioni_speciali": ["Doni Oscuri", "Guerrieri nemici"]
        },
        "ricompensa": {
            "punti_promozione": 3,
            "punti_destino": 2,
            "carte_extra": 0,
            "effetti_speciali": ["Favore Oscuro: -1 costo Doni Oscuri per 2 turni"],
            "descrizione": "3 Punti Promozione, 2 Punti Destino e Favore Oscuro"
        },
        "set_espansione": "Base",
        "numero_carta": "M013",
        "testo_carta": "Solo guerrieri dell'Oscura Legione. Assegna 2 Doni Oscuri a guerrieri nemici. Ricompensa include Favore Oscuro: -1 costo per assegnare Doni per 2 turni.",
        "flavour_text": "L'oscurità si diffonde come una malattia, corrompendo tutto ciò che tocca.",
        "keywords": ["Missione", "Oscura Legione", "Corruzione"],
        "restrizioni": ["Solo guerrieri dell'Oscura Legione"],
        "condizioni_speciali": ["Doni devono essere accettati dai bersagli"],
        "quantita":9
    },

    "Dominazione": {
        "nome": "Dominazione",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Difficile",
        "rarity": "Rare",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Oscura_Legione"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": ["Apostolo", "Nepharite"],
        "obiettivo": {
            "descrizione": "Controlla 3 aree del campo di battaglia",
            "tipo_obiettivo": "Controllare",
            "valore_richiesto": 3,
            "condizioni_speciali": ["Aree diverse", "Simultaneamente"]
        },
        "ricompensa": {
            "punti_promozione": 5,
            "punti_destino": 3,
            "carte_extra": 2,
            "effetti_speciali": ["Supremazia Oscura: +1 a tutte le statistiche per 3 turni"],
            "descrizione": "5 Punti Promozione, 3 Punti Destino, 2 carte e Supremazia Oscura"
        },
        "set_espansione": "Base",
        "numero_carta": "M014",
        "testo_carta": "Solo Apostoli o Nepharite. Controlla simultaneamente 3 aree diverse del campo di battaglia. Ricompensa include Supremazia Oscura: +1 a tutte le statistiche per 3 turni.",
        "flavour_text": "Quando l'oscurità regna suprema, ogni resistenza diventa futile.",
        "keywords": ["Missione", "Oscura Legione", "Dominazione"],
        "restrizioni": ["Solo Apostoli o Nepharite"],
        "condizioni_speciali": ["Controllo deve essere mantenuto per 1 turno completo"],
        "quantita":9
    },

    # MISSIONI PER IL GIOCATORE
    "Strategia Superiore": {
        "nome": "Strategia Superiore",
        "costo_azione": 1,
        "tipo": "Giocatore",
        "difficolta": "Normale",
        "rarity": "Uncommon",
        "bersaglio": "Giocatore Stesso",
        "fazioni_permesse": ["Bauhaus", "Capitol", "Imperiale", "Mishima", "Cybertronic"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Vinci 3 combattimenti nello stesso turno",
            "tipo_obiettivo": "Vincere",
            "valore_richiesto": 3,
            "condizioni_speciali": ["Stesso turno", "Guerrieri diversi"]
        },
        "ricompensa": {
            "punti_promozione": 4,
            "punti_destino": 2,
            "carte_extra": 1,
            "effetti_speciali": ["Comando Tattico: +1 Azione extra per 2 turni"],
            "descrizione": "4 Punti Promozione, 2 Punti Destino, 1 carta e Comando Tattico"
        },
        "set_espansione": "Base",
        "numero_carta": "M015",
        "testo_carta": "Assegna questa missione a te stesso. Se vinci 3 combattimenti con guerrieri diversi nello stesso turno, ottieni la ricompensa e Comando Tattico: +1 Azione per 2 turni.",
        "flavour_text": "Un vero stratega coordina ogni mossa per la vittoria totale.",
        "keywords": ["Missione", "Giocatore", "Strategia"],
        "restrizioni": ["Solo giocatori Doomtrooper"],
        "condizioni_speciali": ["Combattimenti con guerrieri diversi"],
        "quantita":9
    },

    "Risorse Infinite": {
        "nome": "Risorse Infinite",
        "costo_azione": 1,
        "tipo": "Giocatore",
        "difficolta": "Facile",
        "rarity": "Common",
        "bersaglio": "Giocatore Stesso",
        "fazioni_permesse": ["Bauhaus", "Capitol", "Imperiale", "Mishima", "Cybertronic"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Accumula 10 Punti Destino",
            "tipo_obiettivo": "Accumulare",
            "valore_richiesto": 10,
            "condizioni_speciali": ["Simultaneamente"]
        },
        "ricompensa": {
            "punti_promozione": 2,
            "punti_destino": 5,
            "carte_extra": 2,
            "effetti_speciali": [],
            "descrizione": "2 Punti Promozione, 5 Punti Destino e 2 carte"
        },
        "set_espansione": "Base",
        "numero_carta": "M016",
        "testo_carta": "Assegna questa missione a te stesso. Se accumuli 10 Punti Destino simultaneamente, guadagni 2 Punti Promozione, 5 Punti Destino aggiuntivi e peschi 2 carte.",
        "flavour_text": "Chi controlla le risorse, controlla il destino della battaglia.",
        "keywords": ["Missione", "Giocatore", "Risorse"],
        "restrizioni": ["Solo giocatori Doomtrooper"],
        "condizioni_speciali": ["Punti Destino devono essere presenti simultaneamente"],
        "quantita":9
    },

    # MISSIONI DELLE TRIBÙ
    "Chiamata della Terra": {
        "nome": "Chiamata della Terra",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Uncommon",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Tribù"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": ["Mutante", "Ferals"],
        "obiettivo": {
            "descrizione": "Sopravvivi in Avamposto per 4 turni",
            "tipo_obiettivo": "Sopravvivere",
            "valore_richiesto": 4,
            "condizioni_speciali": ["Solo in Avamposto", "Turni consecutivi"]
        },
        "ricompensa": {
            "punti_promozione": 3,
            "punti_destino": 2,
            "carte_extra": 0,
            "effetti_speciali": ["Comunione con la Terra: +2 Armatura e +1 Combattimento per 3 turni"],
            "descrizione": "3 Punti Promozione, 2 Punti Destino e Comunione con la Terra"
        },
        "set_espansione": "Warzone",
        "numero_carta": "M017",
        "testo_carta": "Solo Mutanti o Ferals. Sopravvivi in Avamposto per 4 turni consecutivi. Ricompensa include Comunione con la Terra: +2 Armatura e +1 Combattimento per 3 turni.",
        "flavour_text": "La Terra riconosce i suoi figli e li protegge da ogni minaccia.",
        "keywords": ["Missione", "Tribù", "Sopravvivenza"],
        "restrizioni": ["Solo Mutanti o Ferals delle Tribù"],
        "condizioni_speciali": ["Deve rimanere in Avamposto per tutta la durata"],
        "quantita":9
    },

    # MISSIONI EPICHE E RARE
    "Leggenda Vivente": {
        "nome": "Leggenda Vivente",
        "costo_azione": 2,
        "tipo": "Guerriero",
        "difficolta": "Epica",
        "rarity": "Ultra Rare",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Bauhaus", "Capitol", "Imperiale", "Mishima", "Cybertronic", "Fratellanza"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": ["Personalità", "Eroe"],
        "obiettivo": {
            "descrizione": "Uccidi 5 guerrieri senza morire",
            "tipo_obiettivo": "Uccidere",
            "valore_richiesto": 5,
            "condizioni_speciali": ["Senza morire", "In una singola partita"]
        },
        "ricompensa": {
            "punti_promozione": 8,
            "punti_destino": 5,
            "carte_extra": 3,
            "effetti_speciali": ["Status Leggendario: +2 a tutte le statistiche permanente"],
            "descrizione": "8 Punti Promozione, 5 Punti Destino, 3 carte e Status Leggendario"
        },
        "set_espansione": "Base",
        "numero_carta": "M018",
        "testo_carta": "Solo Personalità o Eroi. Uccidi 5 guerrieri senza morire in una singola partita. Ricompensa include Status Leggendario: +2 permanente a tutte le statistiche.",
        "flavour_text": "Quando la morte stessa si inchina al tuo cospetto, sei diventato una leggenda.",
        "keywords": ["Missione", "Epica", "Leggenda"],
        "restrizioni": ["Solo Personalità o Eroi"],
        "condizioni_speciali": ["Il guerriero non deve mai morire durante la missione"],
        "quantita":9
    }
}


# Funzioni per gestire il database delle missioni

def crea_missione_da_database(nome_missione: str) -> Optional[Missione]:
    """
    Crea un'istanza di Missione basata sui dati del database
    
    Args:
        nome_missione: Nome della missione nel database
        
    Returns:
        Istanza di Missione o None se non trovata
    """
    if nome_missione not in DATABASE_MISSIONI:
        return None
    
    dati = DATABASE_MISSIONI[nome_missione]
    
    # Crea la missione base
    missione = Missione(dati["nome"], dati["costo_azione"])
    
    # Imposta attributi base
    missione.tipo = TipoMissione(dati["tipo"])
    missione.difficolta = DifficoltaMissione(dati["difficolta"])
    missione.rarity = Rarity(dati["rarity"])
    missione.bersaglio = TipoBersaglioMissione(dati["bersaglio"])
    
    # Imposta restrizioni
    missione.fazioni_permesse = [Fazione(f) for f in dati["fazioni_permesse"]]
    missione.corporazioni_specifiche = dati["corporazioni_specifiche"]
    missione.restrizioni_guerriero = dati["restrizioni_guerriero"]
    
    # Imposta obiettivo
    obj_data = dati["obiettivo"]
    missione.aggiorna_obiettivo(
        obj_data["descrizione"],
        obj_data["tipo_obiettivo"],
        obj_data["valore_richiesto"],
        obj_data["condizioni_speciali"]
    )
    
    # Imposta ricompensa
    ric_data = dati["ricompensa"]
    missione.aggiorna_ricompensa(
        ric_data["punti_promozione"],
        ric_data["punti_destino"],
        ric_data["carte_extra"],
        ric_data["effetti_speciali"],
        ric_data["descrizione"]
    )
    
    # Imposta metadati
    missione.set_espansione = dati["set_espansione"]
    missione.numero_carta = dati["numero_carta"]
    missione.testo_carta = dati["testo_carta"]
    missione.flavour_text = dati["flavour_text"]
    missione.keywords = dati["keywords"]
    missione.restrizioni = dati["restrizioni"]
    missione.condizioni_speciali = dati["condizioni_speciali"]
    
    return missione


def get_tutte_le_missioni() -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le missioni del database"""
    return DATABASE_MISSIONI.copy()


def get_missioni_per_fazione(fazione_nome: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce le missioni utilizzabili da una fazione specifica
    
    Args:
        fazione_nome: Nome della fazione (es. "Bauhaus", "Capitol", etc.)
    
    Returns:
        Dizionario con le missioni utilizzabili dalla fazione
    """
    missioni_fazione = {}
    
    for nome_missione, dati_missione in DATABASE_MISSIONI.items():
        if fazione_nome in dati_missione["fazioni_permesse"]:
            missioni_fazione[nome_missione] = dati_missione
    
    return missioni_fazione


def get_missioni_per_tipo(tipo_missione: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce tutte le missioni di un tipo specifico
    
    Args:
        tipo_missione: Tipo di missione ("Guerriero", "Giocatore", "Avversario")
    
    Returns:
        Dizionario con le missioni del tipo specificato
    """
    missioni_tipo = {}
    
    for nome_missione, dati_missione in DATABASE_MISSIONI.items():
        if dati_missione["tipo"] == tipo_missione:
            missioni_tipo[nome_missione] = dati_missione
    
    return missioni_tipo


def get_missioni_per_difficolta(difficolta: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce tutte le missioni di una difficoltà specifica
    
    Args:
        difficolta: Difficoltà richiesta ("Facile", "Normale", "Difficile", "Epica")
    
    Returns:
        Dizionario con le missioni della difficoltà specificata
    """
    missioni_difficolta = {}
    
    for nome_missione, dati_missione in DATABASE_MISSIONI.items():
        if dati_missione["difficolta"] == difficolta:
            missioni_difficolta[nome_missione] = dati_missione
    
    return missioni_difficolta


def get_missioni_per_set(nome_set: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce tutte le missioni di un set specifico
    
    Args:
        nome_set: Nome del set (es. "Base", "Inquisition", "Warzone")
    
    Returns:
        Dizionario con le missioni del set specificato
    """
    missioni_set = {}
    
    for nome_missione, dati_missione in DATABASE_MISSIONI.items():
        if dati_missione["set_espansione"] == nome_set:
            missioni_set[nome_missione] = dati_missione
    
    return missioni_set


def get_missioni_per_rarità(rarity: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce tutte le missioni di una rarità specifica
    
    Args:
        rarity: Rarità richiesta ("Common", "Uncommon", "Rare", "Ultra Rare")
    
    Returns:
        Dizionario con le missioni della rarità specificata
    """
    missioni_rarity = {}
    
    for nome_missione, dati_missione in DATABASE_MISSIONI.items():
        if dati_missione["rarity"] == rarity:
            missioni_rarity[nome_missione] = dati_missione
    
    return missioni_rarity


def get_missioni_per_ricompensa_promozione(min_punti: int = None, max_punti: int = None) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce missioni in un range di Punti Promozione
    
    Args:
        min_punti: Punti Promozione minimi (opzionale)
        max_punti: Punti Promozione massimi (opzionale)
    
    Returns:
        Dizionario con le missioni nel range specificato
    """
    risultati = {}
    for nome_missione, dati_missione in DATABASE_MISSIONI.items():
        punti = dati_missione["ricompensa"]["punti_promozione"]
        if min_punti is not None and punti < min_punti:
            continue
        if max_punti is not None and punti > max_punti:
            continue
        risultati[nome_missione] = dati_missione
    return risultati


def get_missioni_uccisione() -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le missioni che richiedono uccisioni"""
    missioni_uccisione = {}
    
    for nome_missione, dati_missione in DATABASE_MISSIONI.items():
        if dati_missione["obiettivo"]["tipo_obiettivo"] == "Uccidere":
            missioni_uccisione[nome_missione] = dati_missione
    
    return missioni_uccisione


def get_missioni_sopravvivenza() -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le missioni di sopravvivenza"""
    missioni_sopravvivenza = {}
    
    for nome_missione, dati_missione in DATABASE_MISSIONI.items():
        if dati_missione["obiettivo"]["tipo_obiettivo"] == "Sopravvivere":
            missioni_sopravvivenza[nome_missione] = dati_missione
    
    return missioni_sopravvivenza


def get_missioni_controllo() -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le missioni di controllo"""
    missioni_controllo = {}
    
    for nome_missione, dati_missione in DATABASE_MISSIONI.items():
        if dati_missione["obiettivo"]["tipo_obiettivo"] == "Controllare":
            missioni_controllo[nome_missione] = dati_missione
    
    return missioni_controllo


def get_missioni_per_keyword(keyword: str) -> Dict[str, Dict[str, Any]]:
    """
    Restituisce tutte le missioni con una keyword specifica
    
    Args:
        keyword: Keyword da cercare
    
    Returns:
        Dizionario con le missioni che contengono la keyword
    """
    missioni_keyword = {}
    
    for nome_missione, dati_missione in DATABASE_MISSIONI.items():
        if keyword in dati_missione["keywords"]:
            missioni_keyword[nome_missione] = dati_missione
    
    return missioni_keyword


def get_missioni_con_effetti_speciali() -> Dict[str, Dict[str, Any]]:
    """Restituisce tutte le missioni che danno effetti speciali come ricompensa"""
    missioni_effetti = {}
    
    for nome_missione, dati_missione in DATABASE_MISSIONI.items():
        if dati_missione["ricompensa"]["effetti_speciali"]:
            missioni_effetti[nome_missione] = dati_missione
    
    return missioni_effetti


def verifica_compatibilita_guerriero(nome_missione: str, guerriero: object) -> Dict[str, Any]:
    """
    Verifica se un guerriero può ricevere una specifica missione
    
    Args:
        nome_missione: Nome della missione nel database
        guerriero: Oggetto guerriero da verificare
    
    Returns:
        Dict con risultato della verifica
    """
    if nome_missione not in DATABASE_MISSIONI:
        return {"compatibile": False, "motivo": "Missione non trovata nel database"}
    
    # Crea la missione e verifica compatibilità
    missione = crea_missione_da_database(nome_missione)
    if not missione:
        return {"compatibile": False, "motivo": "Errore nella creazione della missione"}
    
    return {"compatibile": missione.puo_essere_assegnata_a(guerriero)}


def get_statistiche_database() -> Dict[str, Any]:
    """Restituisce statistiche sul database delle missioni"""
    total_missioni = len(DATABASE_MISSIONI)
    
    # Conta per tipo
    tipi = {}
    difficolta = {}
    fazioni = {}
    rarità = {}
    
    for dati in DATABASE_MISSIONI.values():
        # Tipo missione
        tipo = dati["tipo"]
        tipi[tipo] = tipi.get(tipo, 0) + 1
        
        # Difficoltà
        diff = dati["difficolta"]
        difficolta[diff] = difficolta.get(diff, 0) + 1
        
        # Rarità
        rar = dati["rarity"]
        rarità[rar] = rarità.get(rar, 0) + 1
        
        # Fazioni
        for fazione in dati["fazioni_permesse"]:
            fazioni[fazione] = fazioni.get(fazione, 0) + 1
    
    return {
        "totale_missioni": total_missioni,
        "per_tipo": tipi,
        "per_difficolta": difficolta,
        "per_rarita": rarità,
        "per_fazione": fazioni
    }


# Esempi di utilizzo del database

if __name__ == "__main__":
    print("=== DATABASE MISSIONI DOOMTROOPER ===\n")
    
    # Statistiche generali
    stats = get_statistiche_database()
    print(f"Totale missioni nel database: {stats['totale_missioni']}")
    print(f"Tipi disponibili: {list(stats['per_tipo'].keys())}")
    print(f"Difficoltà disponibili: {list(stats['per_difficolta'].keys())}")
    
    # Esempio 1: Creare una missione dal database
    print(f"\n=== ESEMPIO CREAZIONE MISSIONE ===")
    caccia = crea_missione_da_database("Caccia al Nemico")
    if caccia:
        print(f"✓ {caccia}")
        print(f"  Obiettivo: {caccia.obiettivo.descrizione}")
        print(f"  Ricompensa: {caccia.ricompensa.punti_promozione} Punti Promozione")
    
    # Esempio 2: Missioni per fazione specifica
    print(f"\n=== MISSIONI BAUHAUS ===")
    missioni_bauhaus = get_missioni_per_fazione("Bauhaus")
    for nome in list(missioni_bauhaus.keys())[:3]:  # Prime 3
        print(f"• {nome}")
    
    # Esempio 3: Missioni per difficoltà
    print(f"\n=== MISSIONI DIFFICILI ===")
    missioni_difficili = get_missioni_per_difficolta("Difficile")
    for nome in missioni_difficili.keys():
        print(f"• {nome}")
    
    # Esempio 4: Missioni di uccisione
    print(f"\n=== MISSIONI DI UCCISIONE ===")
    missioni_uccisione = get_missioni_uccisione()
    for nome in list(missioni_uccisione.keys())[:4]:  # Prime 4
        print(f"• {nome}")
    
    # Esempio 5: Missioni con effetti speciali
    print(f"\n=== MISSIONI CON EFFETTI SPECIALI ===")
    missioni_speciali = get_missioni_con_effetti_speciali()
    for nome, dati in list(missioni_speciali.items())[:3]:  # Prime 3
        effetti = ", ".join(dati["ricompensa"]["effetti_speciali"])
        print(f"• {nome}: {effetti}")
    
    # Esempio 6: Test compatibilità con guerriero
    print(f"\n=== TEST COMPATIBILITÀ ===")
    
    # Simula un guerriero per il test
    class GuerrieroTest:
        def __init__(self, nome, fazione):
            self.nome = nome
            self.fazione = fazione
            self.keywords = []
    
    guerriero_bauhaus = GuerrieroTest("Blitzer Test", Fazione.BAUHAUS)
    
    # Test alcune missioni
    missioni_test = ["Operazione Heimburg", "Caccia al Nemico", "Via del Bushido"]
    
    for nome_missione in missioni_test:
        compatibilita = verifica_compatibilita_guerriero(nome_missione, guerriero_bauhaus)
        status = "✓" if compatibilita["compatibile"] else "✗"
        print(f"{status} {nome_missione}: {compatibilita.get('motivo', 'Compatibile')}")


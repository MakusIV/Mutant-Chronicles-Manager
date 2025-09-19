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
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione, ApostoloPadre, CorporazioneSpecifica


# Database completo delle carte Fortificazione
DATABASE_FORTIFICAZIONI = {
    
    "Cittadella Di Algeroth": {
        "nome": "Cittadella Di Algeroth",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Schieramento",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Seguaci di Algeroth",
        "apostolo_specifico": "Algeroth",
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Tutti i Seguaci di Algeroth nel Tuo Schieramento guadagnano un +2 in A mentre la Cittadella di Algeroth è in gioco",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Oscura Legione"],
        "testo_carta": "QUESTA CARTA PUÒ ESSERE ASSEGNATA ALLA TUA SQUADRA AL COSTO DI UN'AZIONE. Tutti i Seguaci di Algeroth nel Tuo Schieramento guadagnano un +2 in A mentre la Cittadella di Algeroth è in gioco.",
        "flavour_text": "",
        "keywords": ["Algeroth", "Seguace di Algeroth", "Cittadella", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "La Cattedrale Di Longshore": {
        "nome": "La Cattedrale Di Longshore",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Lancia Arte",
                "descrizione": "Mentre in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte degli Elementi",
                "tipo_abilita": "Arte",
                "costo_attivazione": None,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Permette uso Arte degli Elementi"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Doomtrooper"],
        "testo_carta": "ASSEGNABILE ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. Mentre in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte degli Elementi. Puoi avere solo una Cattedrale di Longshore in gioco.",
        "flavour_text": "",
        "keywords": ["Cattedrale", "Longshore", "Arte", "Elementi", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "La Cattedrale Di Heimburg": {
        "nome": "La Cattedrale Di Heimburg",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Lancia Arte",
                "descrizione": "Mentre è in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte dell'Esorcismo",
                "tipo_abilita": "Arte",
                "costo_attivazione": None,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Permette uso Arte dell'Esorcismo"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Doomtrooper"],
        "testo_carta": "PUOI ASSEGNARLA ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. Mentre è in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte dell'Esorcismo. Puoi solo avere una Cattedrale di Heimburg in gioco.",
        "flavour_text": "",
        "keywords": ["Cattedrale", "Heimburg", "Arte", "Esorcismo", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "San Dorado": {
        "nome": "San Dorado",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Capitol",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Tutti i Tuoi membri della Corporazione Capitol guadagnano un +2 in A mentre San Dorado è in gioco",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Capitol"],
        "testo_carta": "QUESTA CARTA PUÒ ESSERE ASSEGNATA ALLA TUA SQUADRA AL COSTO DI UN'AZIONE. CITTÀ CAPITOL. Tutti i Tuoi membri della Corporazione Capitol guadagnano un +2 in A mentre San Dorado è in gioco.",
        "flavour_text": "",
        "keywords": ["Capitol", "Città", "San Dorado", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Complesso Industriale": {
        "nome": "Complesso Industriale",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": False,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": ["Non c'è limite al numero di complessi Industriali che puoi avere in gioco contemporaneamente"],
        "fazioni_permesse": ["Tutte"],
        "testo_carta": "PUOI AGGIUNGERE QUESTA CARTA ALLA TUA SQUADRA O AL TUO SCHIERAMENTO, AL COSTO DI UN'AZIONE. Mentre il Complesso Industriale è in gioco, guadagni 3D ogni tua Fase Pescare. Non c'è limite al numero di complessi Industriali che puoi avere in gioco contemporaneamente.",
        "flavour_text": "",
        "keywords": ["Industriale", "Complesso", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Longshore": {
        "nome": "Longshore",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Mishima",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Tutti i Tuoi membri della Corporazione Mishima guadagnano un +2 in A mentre Longshore è in gioco",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Mishima"],
        "testo_carta": "QUESTA CARTA PUÒ ESSERE ASSEGNATA ALLA TUA SQUADRA AL COSTO DI UN'AZIONE. CITTÀ MISHIMA. Tutti i Tuoi membri della Corporazione Mishima guadagnano un +2 in A mentre Longshore è in gioco.",
        "flavour_text": "",
        "keywords": ["Mishima", "Città", "Longshore", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Trincea": {
        "nome": "Trincea",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": False,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Il guerriero guadagna un +2 in A, e un +2 in C",
                "permanente": True
            },
            {
                "statistica": "C",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Il guerriero guadagna un +2 in A, e un +2 in C",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": ["Non può cominciare un combattimento Corpo a Corpo", "Può essere mossa su un altro guerriero al costo di un'Azione"],
        "fazioni_permesse": ["Tutte"],
        "testo_carta": "ASSEGNA QUESTA CARTA A UN GUERRIERO AL COSTO DI UN'AZIONE. Il guerriero trova protezione in una Trincea. Questo guerriero guadagna un +2 in A, e un +2 in C. Il guerriero non può cominciare un combattimento Corpo a Corpo, (ma può difendersi se è attaccato). Questa carta può essere mossa su un altro guerriero al costo di un'Azione.",
        "flavour_text": "",
        "keywords": ["Trincea", "Protezione", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Campo Di Prigionia": {
        "nome": "Campo Di Prigionia",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Warzone",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": ["I prigionieri non possono attaccare o essere attaccati", "Quando lo imprigioni tutte le carte assegnate o associate al guerriero vengono scartate"],
        "fazioni_permesse": ["Tutte"],
        "testo_carta": "AL COSTO DI UN'AZIONE PUÒ ESSERE ASSEGNATO ALLA TUA SQUADRA. Se uno dei tuoi Doomtrooper ferisce (non uccide) un guerriero Doomtrooper avversario e sopravvive allo scontro, può imprigionarlo. Quando lo imprigioni tutte le carte assegnate o associate al guerriero vengono scartate. I prigionieri non possono attaccare o essere attaccati. Se il Campo di Prigionia viene scartato tutti i suoi prigionieri tornano nella Squadra di appartenenza.",
        "flavour_text": "",
        "keywords": ["Prigionia", "Campo", "Prigionieri", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cattedrale": {
        "nome": "Cattedrale",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Fratellanza",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Tutti i Tuoi membri della Fratellanza guadagnano un +2 in A mentre la CATTEDRALE è in gioco",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Fratellanza"],
        "testo_carta": "QUESTA CARTA PUÒ ESSERE ASSEGNATA A UNA TUA SQUADRA AL COSTO DI UN'AZIONE. CITTÀ DELLA FRATELLANZA. Tutti i Tuoi membri della Fratellanza guadagnano un +2 in A mentre la CATTEDRALE è in gioco.",
        "flavour_text": "",
        "keywords": ["Fratellanza", "Cattedrale", "Città", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Industria Bellica": {
        "nome": "Industria Bellica",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": False,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": ["Non c'è limite al numero di Industrie Belliche che puoi avere in gioco contemporaneamente"],
        "fazioni_permesse": ["Tutte"],
        "testo_carta": "PUOI AGGIUNGERE QUESTA CARTA ALLA TUA SQUADRA O AL TUO SCHIERAMENTO, AL COSTO DI UN'AZIONE. Mentre l'Industria Bellica è in gioco, guadagni 1D durante la Tua Fase Pescare. Non c'è limite al numero di Industrie Belliche che puoi avere in gioco contemporaneamente.",
        "flavour_text": "",
        "keywords": ["Industria", "Bellica", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Luna": {
        "nome": "Luna",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+1",
                "condizione": "sempre",
                "descrizione": "Per il resto della partita, tutti i tuoi guerrieri guadagnano un +1 in A",
                "permanente": True
            },
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "Mercenari",
                "descrizione": "Tutti i tuoi Mercenari guadagnano +2 in A",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Tutte"],
        "testo_carta": "GIOCABILE AL COSTO DI UN'AZIONE Per il resto della partita, tutti i tuoi guerrieri guadagnano un +1 in A; tutti i tuoi Mercenari guadagnano +2 in A.",
        "flavour_text": "",
        "keywords": ["Luna", "Mercenari", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "La Cattedrale Di Burroughs": {
        "nome": "La Cattedrale Di Burroughs",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Lancia Arte",
                "descrizione": "Mentre è in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte della Premonizione",
                "tipo_abilita": "Arte",
                "costo_attivazione": None,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Permette uso Arte della Premonizione"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Doomtrooper"],
        "testo_carta": "PUOI AGGIUNGERLA ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. Mentre è in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte della Premonizione. Puoi solo avere una Cattedrale Burroughs in gioco.",
        "flavour_text": "",
        "keywords": ["Cattedrale", "Burroughs", "Arte", "Premonizione", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "La Cattedrale Di Volksburg": {
        "nome": "La Cattedrale Di Volksburg",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Lancia Arte",
                "descrizione": "Mentre è in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte Cinetica",
                "tipo_abilita": "Arte",
                "costo_attivazione": None,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Permette uso Arte Cinetica"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Doommtrooper"],
        "testo_carta": "PUOI ASSEGNARE QUESTA CARTA ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. Mentre è in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte Cinetica. Puoi solo avere una Cattedrale Volksburg in gioco.",
        "flavour_text": "",
        "keywords": ["Cattedrale", "Volksburg", "Arte", "Cinetica", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Fogne": {
        "nome": "Fogne",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Schieramento",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Eretici",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Andare in Copertura",
                "descrizione": "I tuoi Eretici possono uscire dalla Copertura e Attaccare nello stesso Turno",
                "tipo_abilita": "Movimento",
                "costo_attivazione": "1 Azione",
                "condizioni_attivazione": [],
                "effetti_speciali": ["Entrambe le operazioni costano un'Azione"]
            }
        ],
        "requisiti": [],
        "restrizioni": ["Solo Eretici"],
        "fazioni_permesse": ["Tutte"],
        "testo_carta": "PUOI AGGIUNGERE QUESTA CARTA AL TUO SCHIERAMENTO, AL COSTO DI UN'AZIONE. Mentre la carta è in gioco, i tuoi Eretici possono uscire dalla Copertura e Attaccare nello stesso Turno. Entrambe le operazioni costano un'Azione.",
        "flavour_text": "",
        "keywords": ["Fogne", "Eretici", "Copertura", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "La Cattedrale Di Fukido": {
        "nome": "La Cattedrale Di Fukido",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Lancia Arte",
                "descrizione": "Mentre è in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte Mentale",
                "tipo_abilita": "Arte",
                "costo_attivazione": None,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Permette uso Arte Mentale"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Doomtrooper"],
        "testo_carta": "PUOI ASSEGNARLA ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. Mentre è in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte Mentale. Puoi solo avere una Cattedrale Fukido in gioco.",
        "flavour_text": "",
        "keywords": ["Cattedrale", "Fukido", "Arte", "Mentale", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Heimburg": {
        "nome": "Heimburg",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Bauhaus",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Tutti i Tuoi membri della Corporazione Bauhaus guadagnano un +2 in A mentre Heimburg è in gioco",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Bauhaus"],
        "testo_carta": "QUESTA CARTA PUÒ ESSERE ASSEGNATA ALLA TUA SQUADRA AL COSTO DI UN'AZIONE. CITTÀ BAUHAUS. Tutti i Tuoi membri della Corporazione Bauhaus guadagnano un +2 in A mentre Heimburg è in gioco.",
        "flavour_text": "",
        "keywords": ["Bauhaus", "Città", "Heimburg", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cittadella Di Muawijhe": {
        "nome": "Cittadella Di Muawijhe",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Schieramento",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Seguaci di Muawijhe",
        "apostolo_specifico": "Muawijhe",
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Tutti i Seguaci di Muawijhe guadagnano un +2 in A mentre la CITTADELLA DI MUAWIJHE è in gioco",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Oscura Legione"],
        "testo_carta": "QUESTA CARTA PUÒ ESSERE ASSEGNATA A UNA TUA SQUADRA AL COSTO DI UN'AZIONE. Tutti i Seguaci di Muawijhe guadagnano un +2 in A mentre la CITTADELLA DI MUAWIJHE è in gioco.",
        "flavour_text": "",
        "keywords": ["Muawijhe", "Seguace di Muawijhe", "Cittadella", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Barriera Rinforzata": {
        "nome": "Barriera Rinforzata",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Squadra o Schieramento",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": False,
        "distruttibile": True,
        "bonus_armatura": 1,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+1",
                "condizione": "sempre",
                "descrizione": "Il guerriero è protetto dietro una barriera in cemento armato e filo spinato guadagnando un +1 in A",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": ["Non potrà attaccare i nemici in Corpo a Corpo", "Potrà difendersi", "Potrai spostare la barriera su un altro guerriero al costo di un'Azione"],
        "fazioni_permesse": ["Tutte"],
        "testo_carta": "ASSOCIARE QUESTA CARTA A UN GUERRIERO COSTA UN'AZIONE. Il guerriero è protetto dietro una barriera in cemento armato e filo spinato guadagnando un +1 in A. Il guerriero non potrà attaccare i nemici in Corpo a Corpo, ma potrà difendersi. Potrai spostare la barriera su un altro guerriero al costo di un'Azione.",
        "flavour_text": "",
        "keywords": ["Barriera", "Rinforzata", "Protezione", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Nascondiglio": {
        "nome": "Nascondiglio",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Schieramento",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Eretici",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Tutti i Tuoi Eretici guadagnano un +2 in A",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": ["Puoi introdurre in gioco un solo Nascondiglio"],
        "fazioni_permesse": ["Oscura Legione"],
        "testo_carta": "PUOI AGGIUNGERE QUESTA CARTA AL TUO SCHIERAMENTO AL COSTO DI UN'AZIONE. Mentre è in gioco, tutti i Tuoi Eretici guadagnano un +2 in A. Puoi introdurre in gioco un solo Nascondiglio.",
        "flavour_text": "",
        "keywords": ["Nascondiglio", "Eretici", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "La Cattedrale Di Gibson": {
        "nome": "La Cattedrale Di Gibson",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Lancia Arte",
                "descrizione": "Mentre è in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte del Cambiamento",
                "tipo_abilita": "Arte",
                "costo_attivazione": None,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Permette uso Arte del Cambiamento"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Doomtrooper"],
        "testo_carta": "PUOI ASSEGNARLA ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. Mentre è in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte del Cambiamento. Puoi solo avere una Cattedrale Gibson in gioco.",
        "flavour_text": "",
        "keywords": ["Cattedrale", "Gibson", "Arte", "Cambiamento", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Cittadella Di Semai": {
        "nome": "Cittadella Di Semai",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Schieramento",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Seguaci di Semai",
        "apostolo_specifico": "Semai",
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Tutti i Seguaci di Semai nel Tuo Schieramento guadagnano un +2 in A mentre la CITTADELLA DI SEMAI è in gioco",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Oscura Legione"],
        "testo_carta": "QUESTA CARTA PUÒ ESSERE ASSEGNATA A UNA TUA SQUADRA AL COSTO DI UN'AZIONE. Tutti i Seguaci di Semai nel Tuo Schieramento guadagnano un +2 in A mentre la CITTADELLA DI SEMAI è in gioco.",
        "flavour_text": "",
        "keywords": ["Semai", "Seguace di Semai", "Cittadella", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Gli Archivi Di Pietra": {
        "nome": "Gli Archivi Di Pietra",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Lancia Arte",
                "descrizione": "Mentre in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte d'Evocazione",
                "tipo_abilita": "Arte",
                "costo_attivazione": None,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Permette uso Arte d'Evocazione"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Doomtrooper"],
        "testo_carta": "PUOI AGGIUNGERE QUESTA CARTA ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. Mentre in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte d'Evocazione. Puoi solo avere un Archivio di Pietra in gioco.",
        "flavour_text": "",
        "keywords": ["Archivi", "Pietra", "Arte", "Evocazione", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "La Riserva Del Cardinale": {
        "nome": "La Riserva Del Cardinale",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Protezione Punti",
                "descrizione": "I Punti Destino e i Punti Promozione guadagnati, non possono essere influenzati da carte degli altri giocatori",
                "tipo_abilita": "Protezione",
                "costo_attivazione": None,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Immunità da interferenze sui punti"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Doomtrooper"],
        "testo_carta": "PUOI ASSEGNARLA ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. Mentre in gioco, i Punti Destino e i Punti Promozione guadagnati, non possono essere influenzati da carte degli altri giocatori. Puoi solo avere una Riserva in gioco.",
        "flavour_text": "",
        "keywords": ["Riserva", "Cardinale", "Protezione", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Quartier Generale": {
        "nome": "Quartier Generale",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Cybertronic",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Tutti i Tuoi membri della Corporazione Cybertronic guadagnano un +2 in A mentre il Quartier Generale è in gioco",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Cybertronic"],
        "testo_carta": "QUESTA CARTA PUÒ ESSERE ASSEGNATA ALLA TUA SQUADRA AL COSTO DI UN'AZIONE. CITTÀ CYBERTRONIC. Tutti i Tuoi membri della Corporazione Cybertronic guadagnano un +2 in A mentre il Quartier Generale è in gioco.",
        "flavour_text": "",
        "keywords": ["Cybertronic", "Quartier Generale", "Città", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "Fukido": {
        "nome": "Fukido",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Base",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Corporazione Specifica",
        "corporazione_specifica": "Imperiale",
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [
            {
                "statistica": "A",
                "valore": "+2",
                "condizione": "sempre",
                "descrizione": "Tutti i Tuoi membri della Corporazione Imperiale guadagnano un +2 in A mentre Fukido è in gioco",
                "permanente": True
            }
        ],
        "abilita_speciali": [],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Imperiale"],
        "testo_carta": "QUESTA CARTA PUÒ ESSERE ASSEGNATA ALLA TUA SQUADRA AL COSTO DI UNA AZIONE. CITTÀ IMPERIALE. Tutti i Tuoi membri della Corporazione Imperiale guadagnano un +2 in A mentre Fukido è in gioco.",
        "flavour_text": "",
        "keywords": ["Imperiale", "Fukido", "Città", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
    },

    "La Cattedrale Di San Dorado": {
        "nome": "La Cattedrale Di San Dorado",
        "costo_destino": 0,
        "tipo": "Fortificazione Generica",
        "rarity": "Common",
        "set_espansione": "Inquisition",
        "numero_carta": "",
        "area_compatibile": "Squadra",
        "beneficiario": "Tutti",
        "corporazione_specifica": None,
        "apostolo_specifico": None,
        "unica_per_giocatore": True,
        "distruttibile": True,
        "bonus_armatura": 0,
        "punti_struttura": 0,
        "resistenza_attacchi": False,
        "modificatori": [],
        "abilita_speciali": [
            {
                "nome": "Lancia Arte",
                "descrizione": "Mentre in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte della Manipolazione",
                "tipo_abilita": "Arte",
                "costo_attivazione": None,
                "condizioni_attivazione": [],
                "effetti_speciali": ["Permette uso Arte della Manipolazione"]
            }
        ],
        "requisiti": [],
        "restrizioni": [],
        "fazioni_permesse": ["Doomtrooper"],
        "testo_carta": "PUOI AGGIUNGERLA ALLA TUA SQUADRA, AL COSTO DI UN'AZIONE. Mentre in gioco, tutti i Tuoi Doomtrooper possono usare l'Arte della Manipolazione. Puoi solo avere una Cattedrale di San Dorado in gioco.",
        "flavour_text": "",
        "keywords": ["Cattedrale", "San Dorado", "Arte", "Manipolazione", "Fortificazione"],
        "quantita": 1,
        "quantita_minima_consigliata": 1,
        "fondamentale": False
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
        fortificazione.corporazione_specifica = (data["corporazione_specifica"])
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


def verifica_integrita_database() -> dict:
    """Verifica l'integrità e la coerenza del database"""
    errori = {
        "area_compatibile_errata": [],
        "beneficiario_errato": [],
        "corporazione_specifica_errata": [],
        "apostolo_inconsistente": [],
        
    }
    
    for nome, carta in DATABASE_FORTIFICAZIONI.items():
       
        
        if carta["area_compatibile"] not in [t.value for t in AreaCompatibile]:
           errori["area_compatibile_errata"].append(f"{nome}: {carta['area_compatibile']}")

        if carta["beneficiario"] not in [t.value for t in BeneficiarioFortificazione]:
           errori["beneficiario_errato"].append(f"{nome}: {carta['beneficiario']}")

        if carta["beneficiario"] == "Corporazione Specifica":
                      
           corporazioni = [t.value for t in CorporazioneSpecifica]
           corporazioni.extend(t.value for t in Fazione)
           
           if carta["corporazione_specifica"] not in corporazioni:
                errori["corporazione_specifica_errata"].append(f"{nome}: {carta['corporazione_specifica']}")

        if carta["apostolo_specifico"] and carta["apostolo_specifico"] not in [t.value for t in ApostoloPadre]:
           errori["apostolo_inconsistente"].append(f"{nome}: {carta['apostolo_specifico']}")


    
    return errori



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
    
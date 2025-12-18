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
from source.cards.Guerriero import Fazione, Rarity, DOOMTROOPER


# Database completo delle carte Missione
DATABASE_MISSIONI = {
    # MISSIONI GENERICHE - UCCISIONE
    "Quindici Minuti Di Fama": {
        "nome": "Quindici Minuti Di Fama",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Common",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Generica"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": ["Non Personalita"],
        "obiettivo": {
            "descrizione": "Uccidi un guerriero personalita nemico",
            "tipo_obiettivo": "Uccidere",
            "valore_richiesto": 1,
            "condizioni_speciali": ["Guerriero personalita nemico"]
        },
        "ricompensa": {
            "punti_promozione": 4,
            "punti_destino": 4,
            "carte_extra": 0,
            "effetti_speciali": [],
            "descrizione": "4 punti in più rispetto al normale V"
        },
        "set_espansione": "Base",
        "numero_carta": "M002",
        "testo_carta": "Assegna questa missione a un tuo guerriero non personalita. Il guerriero deve uccidere un guerriero personalita nemico. Se ci riesce, guadagni 4 Punti in più rispetto al normale V",
        "flavour_text": "La vendetta è un piatto che va servito freddo... e letale.",
        "keywords": ["Missione", "Uccisione"],
        "restrizioni": ["Solo Doomtrooper"],
        "condizioni_speciali": [],
        "valore_strategico": 4,
        "quantita":1,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        ,        
    },

    "Lotta Fraticida": {
        "nome": "Lotta Fraticida",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Difficile",
        "rarity": "Uncommon",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Imperiale"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Il guerriero deve uccidere un guerriero imperiale per completare la missione",
            "tipo_obiettivo": "Uccidere",
            "valore_richiesto": 0,
            "condizioni_speciali": ["guerriero imperiale", "Stesso turno"]
        },
        "ricompensa": {
            "punti_promozione": 2,
            "punti_destino": 2,
            "carte_extra": 0,
            "effetti_speciali": [],
            "descrizione": "il doppio del valore V del guerriero ucciso"
        },
        "set_espansione": "Base",
        "numero_carta": "M003",
        "testo_carta": "Assegnabile ad un qualsiasi guerriero imperiale. Il guerriero deve uccidere un guerriero imperiale per completare la missione e per guadagniare due volte il valore V del guerriero ucciso. Il guerriero attaccante non può essere identico al guerriero difensore",
        "flavour_text": "Un massacro metodico che lascia il campo di battaglia cosparso di cadaveri.",
        "keywords": ["Missione", "Uccisione", "Difficile"],
        "restrizioni": ["Solo Imperiale"],
        "condizioni_speciali": [],
        "valore_strategico": 1,
        "quantita":3,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        ,        
    },

   
    "Cospirazione Eretica": {
        "nome": "Cospirazione Eretica",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Common",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": DOOMTROOPER,
        "corporazioni_specifiche": ["Eretico"],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Uccideri una personalita della fratellanza. Una volta completata la missione, tutti i tuoi guerrieri nella squadra (se la missione era assegnata ad un Doomtrooper) oppure del tuo schieramento (se era assegnata ad un Eretico) saranno immuni a tutti gli effetti delle arti",
            "tipo_obiettivo": "Uccisione",
            "valore_richiesto": 0,
            "condizioni_speciali": []
        },
        "ricompensa": {
            "punti_promozione": 0,
            "punti_destino": 0,
            "carte_extra": 0,
            "effetti_speciali": [],
            "descrizione": "Una volta completata la missione, tutti i tuoi guerrieri nella squadra (se la missione era assegnata ad un Doomtrooper) oppure del tuo schieramento (se era assegnata ad un Eretico) saranno immuni a tutti gli effetti delle arti"
        },
        "set_espansione": "Warzone",
        "numero_carta": "M004",
        "testo_carta": "ASSEGNABILE AD UN DOOMTROOPER O AD UN ERETICO. Per completare questa missione devi uccidere una personalita della fratellanza. Una volta completata la missione, tutti i tuoi guerrieri nella squadra (se la missione era assegnata ad un Doomtrooper) oppure del tuo schieramento (se era assegnata ad un Eretico) saranno immuni a tutti gli effetti delle arti.",
        "flavour_text": "La vera forza si manifesta quando tutto sembra perduto.",
        "keywords": ["Eretico"],
        "restrizioni": ["Solo Doomtrooper", "Solo Eretico"],
        "condizioni_speciali": [],
        "valore_strategico": 1,
        "quantita":2,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        ,        
    },

    "Dimostra Il Tuo Valore": {
        "nome": "Dimostra Il Tuo Valore",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Difficile",
        "rarity": "Rare",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Generica"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Scegli un guerriero avversario con una V almeno due volte più grande di questo guerriero. Il tuo guerriero deve uccidere il suo avversario e sopravvivere al combattimento per completare la missione. Se riesce guadagna tre volte la V del guerriero ucciso",
            "tipo_obiettivo": "Uccisione",
            "valore_richiesto": 0,
            "condizioni_speciali": []
        },
        "ricompensa": {
            "punti_promozione": 0,
            "punti_destino": 0,
            "carte_extra": 0,
            "effetti_speciali": [],
            "descrizione": "Il tuo guerriero deve uccidere il suo avversario e sopravvivere al combattimento per completare la missione. Se riesce guadagna tre volte la V del guerriero ucciso"
        },
        "set_espansione": "Base",
        "numero_carta": "M005",
        "testo_carta": "Assegna questa missione a un tuo guerriero. Scegli un guerriero avversario con una V almeno due volte più grande di questo guerriero. Il tuo guerriero deve uccidere il suo avversario e sopravvivere al combattimento per completare la missione. Se riesce guadagna tre volte la V del guerriero ucciso",
        "flavour_text": "",
        "keywords": ["Missione", "Sopravvivenza"],
        "restrizioni": [],
        "condizioni_speciali": ["Tutti gli altri guerrieri devono essere fuori gioco"],
        "valore_strategico": 6,
        "quantita":1,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        ,        
    },

    "Offesa Al Cardinale": {
        "nome": "Offesa Al Cardinale",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Uncommon",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Fratellanza"],
        "corporazioni_specifiche": [],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Dovrai convertire un membro della fratellanza in un Eretico per completare la missione e guadagnare 5 punti promozione",
            "tipo_obiettivo": "Conversione",
            "valore_richiesto": 1,
            "condizioni_speciali": []
        },
        "ricompensa": {
            "punti_promozione": 5,
            "punti_destino": 0,
            "carte_extra": 0,
            "effetti_speciali": [],
            "descrizione": "5 punti promozione"
        },
        "set_espansione": "Base",
        "numero_carta": "M006",
        "testo_carta": "Assegnabile ad ogni giocatore. Dovrai convertire un membro della fratellanza in un Eretico per completare la missione e guadagnare 5 punti promozione",
        "flavour_text": "L'ingegneria Bauhaus conquista anche le fortezze più imprendibili.",
        "keywords": ["Missione", "Eretico"],
        "restrizioni": ["Solo Fratellanza"],
        "condizioni_speciali": [],
        "valore_strategico": 1,
        "quantita":2,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        ,        
    },

    "Portale Del Grande Conquistatore": {
        "nome": "Portale Del Grande Conquistatore",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Uncommon",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Oscura Legione"],
        "corporazioni_specifiche": ["Seguace di Algeroth"],
        "restrizioni_guerriero": ["Solo Nefarita"],
        "obiettivo": {
            "descrizione": "Questo Nefarita deve uccidere un guerriero della Fratellanza con V tre volte più grande cme sacrificio. Non guadagni punti deel guerriero ucciso ma tutti i guerrieri in gioco della frtellanza perdono la capacità di usare le arti per tutta la partita",
            "tipo_obiettivo": "Uccidere",
            "valore_richiesto": 2,
            "condizioni_speciali": []
        },
        "ricompensa": {
            "punti_promozione": 0,
            "punti_destino": 0,
            "carte_extra": 0,
            "effetti_speciali": [],
            "descrizione": "Tutti i guerrieri in gioco della frtellanza perdono la capacità di usare le arti per tutta la partita"
        },
        "set_espansione": "Base",
        "numero_carta": "M007",
        "testo_carta": "ASSEGNABILE AD UN NEFARITA DI ALGEROTH SOLO SE UNA CITTADELLA DI ALGEROTH E' NEL TUO SCHIERAMENTO. Questo Nefarita deve uccidere un guerriero della Fratellanza con V tre volte più grande cme sacrificio. Non guadagni punti deel guerriero ucciso ma tutti i guerrieri in gioco della frtellanza perdono la capacità di usare le arti per tutta la partita",
        "flavour_text": "La superiorità tecnologica Capitol si manifesta in ogni colpo sparato.",
        "keywords": ["Missione", "Capitol", "Armi da Fuoco"],
        "restrizioni": ["Solo Nefarita", "Solo Seguaci di Algeroth"],
        "condizioni_speciali": [],
        "valore_strategico": 1,
        "quantita":1,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        ,        
    },

    "Assedio Alla Citadella": {
        "nome": "Assedio Alla Citadella",
        "costo_azione": 1,
        "tipo": "Guerriero",
        "difficolta": "Normale",
        "rarity": "Uncommon",
        "bersaglio": "Proprio Guerriero",
        "fazioni_permesse": ["Imperiale"],
        "corporazioni_specifiche": ["Imperiale"],
        "restrizioni_guerriero": [],
        "obiettivo": {
            "descrizione": "Devi distruggere una Citadella degli Apostoli Oscuri in gioco per completare la missione e ricevere 3 ounti promozione",
            "tipo_obiettivo": "Distruggere",
            "valore_richiesto": 0,
            "condizioni_speciali": []
        },
        "ricompensa": {
            "punti_promozione": 3,
            "punti_destino": 0,
            "carte_extra": 0,
            "effetti_speciali": [],
            "descrizione": "3 Punti Promozione"
        },
        "set_espansione": "Base",
        "numero_carta": "M008",
        "testo_carta": "ASSEGNABILE AD OGNI GIOCATORE. Devi distruggere una Citadella degli Apostoli Oscuri in gioco per completare la missione e ricevere 3 ounti promozione",
        "flavour_text": "",
        "keywords": [],
        "restrizioni": [],
        "condizioni_speciali": [],
        "valore_strategico": 1,
        "quantita":1,
        "quantita_minima_consigliata":1, # utilizzata per la creazione del mazzo
        "fondamentale": False # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)        ,        
    },

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
    return Missione.from_dict(dati)


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


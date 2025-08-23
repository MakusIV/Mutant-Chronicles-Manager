"""
Manager_Gioco.py
Modulo per la gestione delle funzionalità del gioco Mutant Chronicles/Doomtrooper
Implementa la creazione di collezioni di giocatori secondo le regole ufficiali del regolamento.

Autore: AI Assistant
Data: 2025
Versione: 1.0
"""

import random
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any, Union
from enum import Enum
import json
from collections import defaultdict

# Import delle classi delle carte (solo le classi, non le funzioni di creazione)
from source.cards.Guerriero import (
    Guerriero, Fazione, Set_Espansione, Rarity, TipoGuerriero
)
from source.cards.Equipaggiamento import Equipaggiamento
from source.cards.Speciale import Speciale
from source.cards.Fortificazione import Fortificazione
from source.cards.Missione import Missione
from source.cards.Arte import Arte
from source.cards.Oscura_Simmetria import Oscura_Simmetria
from source.cards.Reliquia import Reliquia
from source.cards.Warzone import Warzone

# Import dei database
from source.data_base_cards.Database_Guerriero import (
    GUERRIERI_DATABASE, get_numero_guerrieri_per_fazione, get_numero_guerrieri_per_set, get_guerrieri_per_fazione, get_guerrieri_per_set,
    crea_guerriero_da_nome as crea_guerriero_da_database
)
from source.data_base_cards.Database_Equipaggiamento import (
    DATABASE_EQUIPAGGIAMENTO, get_equipaggiamenti_per_fazione, get_equipaggiamenti_per_set,
    crea_equipaggiamento_da_database
)
from source.data_base_cards.Database_Speciale import (
    DATABASE_SPECIALI, get_carte_per_fazione as get_speciali_per_fazione, 
    get_carte_per_set as get_speciali_per_set,
    crea_carta_da_database as crea_speciale_da_database
)
from source.data_base_cards.Database_Fortificazione import (
    DATABASE_FORTIFICAZIONI, get_fortificazioni_per_fazione, get_fortificazioni_per_set,
    crea_fortificazione_da_database
)
from source.data_base_cards.Database_Missione import (
    DATABASE_MISSIONI, get_missioni_per_fazione, get_missioni_per_set,
    crea_missione_da_database
)
from source.data_base_cards.Database_Arte import (
    CARTE_ARTE_DATABASE, get_carte_per_fazione as get_arte_per_fazione,
    get_carte_per_set as get_arte_per_set,
    crea_carta_da_database as crea_arte_da_database
)
from source.data_base_cards.Database_Oscura_Simmetria import (
    DATABASE_OSCURA_SIMMETRIA, get_carte_per_apostolo as get_oscura_per_apostolo,
    get_carte_per_set as get_oscura_per_set,
    crea_carta_da_database as crea_oscura_simmetria_da_database
)
from source.data_base_cards.Database_Reliquia import (
    DATABASE_RELIQUIE, get_reliquie_per_fazione, get_reliquie_per_set,
    crea_reliquia_da_database as crea_reliquia_da_database
)
from source.data_base_cards.Database_Warzone import (
    DATABASE_WARZONE, filtra_warzone_per_fazione, filtra_warzone_per_set,
    ottieni_warzone as crea_warzone_da_database
)



NUMERO_CARTE_DISPONIBILI = {
    'Guerriero': 31,
    'Equipaggiamento': 11,
    'Speciale': 22,
    'Arte': 15,
    'Oscura Simmetria': 10,
    'Fortificazione': 20,
    'Missione': 17,
    'Reliquia': 12,
    'Warzone': 11,
}

LIMITI_CARTE_COLLEZIONE = { # rappresentano i valori per nomi di guerriero consentti, considera che poi si aggiungono il numero minimo di copie per carta
            'Guerriero': {'min': 13 , 'max': 17 },
            'Equipaggiamento': {'min': 5 , 'max': 6  },
            'Speciale': {'min': 10 , 'max':   12},
            'Arte': {'min': 7 , 'max': 8  },
            'Oscura Simmetria': {'min': 5 , 'max': 6  },
            'Fortificazione': {'min': 9 , 'max': 11  },
            'Missione': {'min': 7 , 'max': 9  },
            'Reliquia': {'min': 5 , 'max': 7  },
            'Warzone': {'min': 5 , 'max': 6  },
        }

# percentuale distribuzione carte per collezione/mazzo gioco
LIMITI_CARTE_MAZZO = {
    'Guerriero': {'min': int(0.19 * NUMERO_CARTE_DISPONIBILI['Guerriero']) , 'max': int(0.22 * NUMERO_CARTE_DISPONIBILI['Guerriero']) },
    'Equipaggiamento': {'min': int(0.10 * NUMERO_CARTE_DISPONIBILI['Equipaggiamento']) , 'max': int(0.13 * NUMERO_CARTE_DISPONIBILI['Equipaggiamento']) },
    'Speciale': {'min': int(0.40 * NUMERO_CARTE_DISPONIBILI['Speciale']) , 'max': int(0.45 * NUMERO_CARTE_DISPONIBILI['Speciale']) },
    'Arte': {'min': int(0.05 * NUMERO_CARTE_DISPONIBILI['Arte']) , 'max': int(0.07 * NUMERO_CARTE_DISPONIBILI['Arte']) },
    'Oscura Simmetria': {'min': int(0.05 * NUMERO_CARTE_DISPONIBILI['Oscura Simmetria']) , 'max': int(0.07 * NUMERO_CARTE_DISPONIBILI['Oscura Simmetria']) },
    'Fortificazione': {'min': int(0.07 * NUMERO_CARTE_DISPONIBILI['Fortificazione']) , 'max': int(0.10 * NUMERO_CARTE_DISPONIBILI['Fortificazione']) },
    'Missione': {'min': int(0.05 * NUMERO_CARTE_DISPONIBILI['Missione']) , 'max': int(0.07 * NUMERO_CARTE_DISPONIBILI['Missione']) },
    'Reliquia': {'min': int(0.05 * NUMERO_CARTE_DISPONIBILI['Reliquia']) , 'max': int(0.07 * NUMERO_CARTE_DISPONIBILI['Reliquia']) },
    'Warzone': {'min': int(0.05 * NUMERO_CARTE_DISPONIBILI['Warzone']) , 'max': int(0.07 * NUMERO_CARTE_DISPONIBILI['Warzone']) },
}


# Serializzatore personalizzato per gestire enum e altri oggetti non serializzabili
class EnumJSONEncoder(json.JSONEncoder):
    """
    Encoder JSON personalizzato per gestire enum e altri oggetti non serializzabili.
    Converte automaticamente gli enum nei loro valori stringa.
    """
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        # Se è un oggetto con attributo 'value', usa quello
        elif hasattr(obj, 'value'):
            return obj.value
        # Altrimenti usa il serializzatore di default
        return super().default(obj)


class TipoCombinazioneFazionePerMazzo(Enum):
    """Combinazioni di fazioni per collezioni orientate"""
    FRATELLANZA_DOOMTROOPER_FREELANCER = ("Fratellanza", "Doomtrooper", "Freelancer")
    FRATELLANZA_OSCURA_LEGIONE_FREELANCER = ("Fratellanza", "Oscura Legione", "Freelancer") 
    DOOMTROOPER_OSCURA_LEGIONE_FREELANCER = ("Doomtrooper", "Oscura Legione", "Freelancer")



class TipoCombinazioneFazione(Enum):
    """Combinazioni di fazioni per collezioni orientate"""
    FRATELLANZA_DOOMTROOPER_FREELANCER = ("Fratellanza", "Doomtrooper", "Freelancer")
    FRATELLANZA_OSCURA_LEGIONE_FREELANCER = ("Fratellanza", "Oscura Legione", "Freelancer") 
    DOOMTROOPER_OSCURA_LEGIONE_FREELANCER = ("Doomtrooper", "Oscura Legione", "Freelancer")


class StatisticheCollezione:
    """Classe per tracciare le statistiche di una collezione"""
    
    def __init__(self):
        self.guerrieri = 0
        self.equipaggiamenti = 0
        self.speciali = 0
        self.fortificazioni = 0
        self.missioni = 0
        self.arte = 0
        self.oscura_simmetria = 0
        self.reliquie = 0
        self.warzone = 0
        self.totale_carte = 0
        self.valore_totale_dp = 0
        self.per_fazione = defaultdict(int)
        self.per_set = defaultdict(int)
        self.per_rarity = defaultdict(int)
    
    def aggiorna_statistiche(self, carta: Any, quantita: int = 1):
        """Aggiorna le statistiche della collezione"""
        tipo_carta = type(carta).__name__.lower()
        
        if tipo_carta == "guerriero":
            self.guerrieri += quantita
        elif tipo_carta == "equipaggiamento":
            self.equipaggiamenti += quantita
        elif tipo_carta == "speciale":
            self.speciali += quantita
        elif tipo_carta == "fortificazione":
            self.fortificazioni += quantita
        elif tipo_carta == "missione":
            self.missioni += quantita
        elif tipo_carta == "arte":
            self.arte += quantita
        elif tipo_carta == "oscura_simmetria":
            self.oscura_simmetria += quantita
        elif tipo_carta == "reliquia":
            self.reliquie += quantita
        elif tipo_carta == "warzone":
            self.warzone += quantita
        
        self.totale_carte += quantita
        
        # Aggiorna valore in DP se disponibile
        if hasattr(carta, 'valore'):
            self.valore_totale_dp += carta.valore * quantita
        elif hasattr(carta, 'costo_destino'):
            self.valore_totale_dp += carta.costo_destino * quantita
        
        # Aggiorna contatori per fazione, set e rarità
        if hasattr(carta, 'fazione'):
            self.per_fazione[carta.fazione.value] += quantita
        if hasattr(carta, 'set_espansione'):
            self.per_set[carta.set_espansione] += quantita
        if hasattr(carta, 'rarity'):
            self.per_rarity[carta.rarity.value] += quantita
    
    def __str__(self) -> str:
        return f"""Statistiche Collezione:
- Guerrieri: {self.guerrieri}
- Equipaggiamenti: {self.equipaggiamenti}
- Speciali: {self.speciali}
- Fortificazioni: {self.fortificazioni}
- Missioni: {self.missioni}
- Arte: {self.arte}
- Oscura Simmetria: {self.oscura_simmetria}
- Reliquie: {self.reliquie}
- Warzone: {self.warzone}
- Totale carte: {self.totale_carte}
- Valore totale DP: {self.valore_totale_dp}
- Per fazione: {dict(self.per_fazione)}
- Per set: {dict(self.per_set)}
- Per rarità: {dict(self.per_rarity)}"""


class CollezioneGiocatore:
    """
    Rappresenta una collezione completa di carte di un giocatore.
    
    NOTA IMPORTANTE: Questa è la collezione di tutte le carte possedute dal giocatore,
    non il mazzo da gioco (che deve avere minimo 5 guerrieri secondo il regolamento).
    Dal CollezioneGiocatore, il giocatore potrà successivamente creare mazzi da gioco
    specifici selezionando un sottoinsieme delle carte disponibili.
    """
    
    def __init__(self, id_giocatore: int):
        self.id_giocatore = id_giocatore
        self.carte = {
            'guerriero': [],
            'equipaggiamento': [],
            'speciale': [],
            'fortificazione': [],
            'missione': [],
            'arte': [],
            'oscura_simmetria': [],
            'reliquia': [],
            'warzone': []
        }
        self.fazioni_orientamento = []  # Fazioni per orientamento
        self.statistiche = StatisticheCollezione()
        self.inventario_quantita = defaultdict(int)  # Traccia quantità per carta
    
    def aggiungi_carta(self, carta: Any, quantita: int = 1):
        """Aggiunge una carta alla collezione"""
        tipo_carta = type(carta).__name__.lower()
        
        if tipo_carta in self.carte:
            for _ in range(quantita):
                self.carte[tipo_carta].append(carta)
            
            self.statistiche.aggiorna_statistiche(carta, quantita)
            self.inventario_quantita[carta.nome] += quantita
    
    def get_carte_per_tipo(self, tipo_carta: str) -> List[Any]:
        """Restituisce le carte di un tipo specifico"""
        return self.carte.get(tipo_carta, [])
    
    def get_totale_carte(self) -> int:
        """Restituisce il numero totale di carte nella collezione"""
        return sum(len(carte) for carte in self.carte.values())
    
    def export_to_dict(self) -> Dict[str, Any]:
        """Esporta la collezione in formato dizionario"""
        return {
            'id_giocatore': self.id_giocatore,
            'fazioni_orientamento': [f.value if hasattr(f, 'value') else str(f) for f in self.fazioni_orientamento],
            'statistiche': {
                'guerrieri': self.statistiche.guerrieri,
                'equipaggiamenti': self.statistiche.equipaggiamenti,
                'speciali': self.statistiche.speciali,
                'fortificazioni': self.statistiche.fortificazioni,
                'missioni': self.statistiche.missioni,
                'arte': self.statistiche.arte,
                'oscura_simmetria': self.statistiche.oscura_simmetria,
                'reliquie': self.statistiche.reliquie,
                'warzone': self.statistiche.warzone,
                'totale_carte': self.statistiche.totale_carte,
                'valore_totale_dp': self.statistiche.valore_totale_dp,
                'per_fazione': dict(self.statistiche.per_fazione),
                'per_set': dict(self.statistiche.per_set),
                'per_rarity': dict(self.statistiche.per_rarity)
            },
            'inventario_quantita': dict(self.inventario_quantita)
        }
    
    def __str__(self) -> str:
        fazioni_str = ", ".join([f.value if hasattr(f, 'value') else str(f) for f in self.fazioni_orientamento])
        return f"""Collezione Giocatore {self.id_giocatore}:
Fazioni orientamento: {fazioni_str}
{self.statistiche}"""


# Tracciamento globale delle quantità utilizzate
QUANTITA_UTILIZZATE = defaultdict(int)


def resetta_tracciamento_quantita():
    """Resetta il tracciamento delle quantità utilizzate"""
    global QUANTITA_UTILIZZATE
    QUANTITA_UTILIZZATE.clear()


# ==================== FUNZIONI DI CREAZIONE CARTE ====================
# Le funzioni di creazione utilizzano i database esistenti:
# - crea_guerriero_da_database: alias per crea_guerriero_da_nome da Database_Guerriero
# - crea_equipaggiamento_da_database: già presente in Database_Equipaggiamento  
# - crea_speciale_da_database: alias per crea_carta_da_database da Database_Speciale
# - crea_fortificazione_da_database: già presente in Database_Fortificazione
# - crea_missione_da_database: già presente in Database_Missione
# - crea_arte_da_database: alias per crea_carta_da_database da Database_Arte
# - crea_oscura_simmetria_da_database: alias per crea_carta_da_database da Database_Oscura_Simmetria
# - crea_reliquia_da_database: implementata qui usando Reliquia.from_dict()
# - crea_warzone_da_database: implementata qui usando Warzone.from_dict()


def resetta_tracciamento_quantita():
    """Resetta il tracciamento delle quantità utilizzate"""
    global QUANTITA_UTILIZZATE
    QUANTITA_UTILIZZATE.clear()


def verifica_quantita_disponibile(nome_carta: str, database: Dict, quantita_richiesta: int = 1) -> bool:
    """Verifica se la quantità richiesta di una carta è disponibile"""
    if nome_carta not in database:
        return False
    
    quantita_disponibile = database[nome_carta].get('quantita', 0)
    quantita_gia_utilizzata = QUANTITA_UTILIZZATE[nome_carta]
    
    return (quantita_disponibile - quantita_gia_utilizzata) >= quantita_richiesta


def utilizza_carta(nome_carta: str, quantita: int = 1):
    """Registra l'utilizzo di una quantità di carte"""
    QUANTITA_UTILIZZATE[nome_carta] += quantita


def seleziona_carte_casuali_per_tipo(
    database: Dict,
    funzione_creazione: callable,
    set_espansioni: List[Set_Espansione],
    fazioni_orientamento: List[Fazione] = None,
    min_carte: int = 5,
    max_carte: int = 15,
    probabilita_orientamento: float = 0.7
) -> List[Any]:
    """
    Seleziona carte casuali per tipo (Guerriero, Equipaggiamento, ecc) da un database rispettando quantità e orientamento
    """
    carte_selezionate = []

    # Filtra carte per set espansioni
    carte_disponibili = {}
    for nome, dati in database.items():
        if dati.get('set_espansione') in [s.value for s in set_espansioni]:
            if verifica_quantita_disponibile(nome, database):
                carte_disponibili[nome] = dati
    
    if not carte_disponibili:
        return carte_selezionate
    
    # Determina numero di carte da selezionare
    num_carte = random.randint(min_carte, max_carte)
    
    # Separa carte per orientamento se specificato
    carte_orientate = {}
    carte_generiche = {}
    
    if fazioni_orientamento:
        for nome, dati in carte_disponibili.items():
            # Verifica se la carta supporta le fazioni di orientamento   
            if 'fazione' in dati:     # Guerriero     
                fazioni_permesse = dati.get('fazioni_permesse', [])            
            elif 'fazioni_permesse' in dati:  # Speciale, Equipaggiamento, Foritficazione, Missione, Oscura_Simmetria       
                fazioni_permesse = dati.get('fazioni_permesse', [])            
            elif 'restrizioni' in dati: # Reliquia, Warzone     
                fazioni_permesse = dati['restrizioni'].get('fazioni_permesse', [])            
            
            if any(f.value in fazioni_permesse for f in fazioni_orientamento):
                carte_orientate[nome] = dati
            else:
                carte_generiche[nome] = dati
    else:
        carte_generiche = carte_disponibili
    
    # Seleziona carte privilegiando l'orientamento
    for _ in range(num_carte):
        if not carte_disponibili:
            break
        
        # Decide se usare orientamento o carte generiche
        usa_orientamento = (
            fazioni_orientamento and 
            carte_orientate and 
            random.random() < probabilita_orientamento
        )
        
        if usa_orientamento:
            pool_carte = carte_orientate
        else:
            pool_carte = carte_generiche if carte_generiche else carte_orientate
        
        if not pool_carte:
            continue
        
        # Seleziona carta casuale
        nome_carta = random.choice(list(pool_carte.keys()))
        dati_carta = pool_carte[nome_carta]
        
        # Determina quantità da aggiungere (1-3 copie)
        max_quantita_disponibile = min(
            5,  # Massimo 5 copie per carta- qui utilizza la quantita minima consigliata
            dati_carta.get('quantita', 0) - QUANTITA_UTILIZZATE[nome_carta]
        )
        
        #if max_quantita_disponibile <= 0:
            # Rimuovi carte non più disponibili
        if nome_carta in carte_orientate:
            del carte_orientate[nome_carta]
        if nome_carta in carte_generiche:
            del carte_generiche[nome_carta]
        #    continue
        
        quantita = random.randint(1, max_quantita_disponibile)
        
        # Crea e aggiungi carte
        for _ in range(quantita):
            try:
                carta = funzione_creazione(nome_carta)
                if carta:
                    carte_selezionate.append(carta)
            except Exception as e:
                print(f"Errore nella creazione di {nome_carta}: {e}")
                continue
        
        # Registra utilizzo
        utilizza_carta(nome_carta, quantita)
        
        # Rimuovi se quantità esaurita
        if not verifica_quantita_disponibile(nome_carta, database):
            if nome_carta in carte_orientate:
                del carte_orientate[nome_carta]
            if nome_carta in carte_generiche:
                del carte_generiche[nome_carta]
    
    return carte_selezionate


def genera_fazioni_orientamento_casuali() -> Tuple[Fazione, ...]:
    """Genera una combinazione casuale di fazioni per l'orientamento"""
    combinazioni = list(TipoCombinazioneFazione)
    combinazione_scelta = random.choice(combinazioni)
    
    # Converte i nomi delle fazioni in enum Fazione
    fazioni = []
    for nome_fazione in combinazione_scelta.value:
        try:
            # Gestisce i mapping speciali
            if nome_fazione == "Doomtrooper":
                # Doomtrooper comprende le corporazioni
                fazioni.extend([Fazione.BAUHAUS, Fazione.CAPITOL, Fazione.IMPERIALE, 
                               Fazione.MISHIMA, Fazione.CYBERTRONIC])
            else:
                fazione = Fazione(nome_fazione)
                fazioni.append(fazione)
        except ValueError:
            print(f"Fazione non riconosciuta: {nome_fazione}")
            continue
    
    return tuple(fazioni)


def creazione_Collezione_Giocatore(
    numero_giocatori: int,
    espansioni: List[Set_Espansione],
    orientamento: bool = False
) -> List[CollezioneGiocatore]:
    """
    Crea un numero di collezioni uguale al parametro specificato.
    
    Args:
        numero_giocatori: Numero di collezioni da creare
        espansioni: Lista delle espansioni da cui selezionare le carte
        orientamento: Se True, orienta le collezioni verso fazioni specifiche
        
    Returns:
        Lista di collezioni create
        
    Note:
        La CollezioneGiocatore rappresenta tutte le carte possedute da un giocatore,
        non la collezione da gioco (che ha il vincolo di minimo 5 guerrieri).
        Dalla CollezioneGiocatore il giocatore potrà poi creare mazzi da gioco specifici.
    """
    
    if numero_giocatori <= 0:
        raise ValueError("Il numero di giocatori deve essere positivo")
    

    if not espansioni:
        raise ValueError("Deve essere specificata almeno un'espansione")
    
    # Valida espansioni
    espansioni_valide = []
    for esp in espansioni:
        if isinstance(esp, Set_Espansione):
            espansioni_valide.append(esp)
        elif isinstance(esp, str):
            try:
                espansioni_valide.append(Set_Espansione(esp))
            except ValueError:
                print(f"Espansione non valida ignorata: {esp}")
        else:
            print(f"Tipo espansione non riconosciuto ignorato: {esp}")
    
    if not espansioni_valide:
        raise ValueError("Nessuna espansione valida specificata")
    
    # Resetta tracciamento quantità
    resetta_tracciamento_quantita()
    
    collezioni = []
    fazioni_utilizzate = set()  # Per evitare duplicati nell'orientamento
    
    print(f"Creazione di {numero_giocatori} collezioni...")
    print(f"Espansioni: {[e.value for e in espansioni_valide]}")
    print(f"Orientamento: {'Sì' if orientamento else 'No'}")
    
    for i in range(numero_giocatori):
        print(f"\nCreando collezione per Giocatore {i+1}...")
        
        collezione = CollezioneGiocatore(i + 1)
        #numero_guerrieri = {}

        # Genera orientamento se richiesto
        if orientamento:
            fazioni_orientamento = None
            tentativi = 0
            max_tentativi = 10
            
            while tentativi < max_tentativi:                
                fazioni_candidate = genera_fazioni_orientamento_casuali()                   
                
                # Crea chiave unica per evitare duplicati
                chiave_fazioni = tuple(sorted([f.value for f in fazioni_candidate]))
                
                if chiave_fazioni not in fazioni_utilizzate:
                    fazioni_orientamento = fazioni_candidate
                    fazioni_utilizzate.add(chiave_fazioni)                    
                    break
                
                tentativi += 1
            
            if fazioni_orientamento:
                """
                # calcolo quantità guerrieri per nome                
                for fazione in fazioni_orientamento:                    
                    guerrieri_fazione = get_numero_guerrieri_per_fazione(fazione = fazione)
                    for nome, data in guerrieri_fazione:
                        numero_guerrieri[nome]=data['quantita']
                """
                collezione.fazioni_orientamento = list(fazioni_orientamento)    
                print(f"Orientamento: {[f.value for f in fazioni_orientamento]}")
            else:               
                
                print("Impossibile assegnare orientamento unico, procedendo senza orientamento")
        """
        else:
            guerrieri_espansioni = {}
            for espansione in espansioni_valide:
                guerrieri_espansioni.update( get_numero_guerrieri_per_set( espansione = espansioni ) )
                
                for nome, data in guerrieri_espansioni:
                        numero_guerrieri[nome]=data['quantita']

            numero_guerrieri = {}
        """
        """
        min_carte = 0.9/( numero_giocatori )
        max_carte = 1.1/( numero_giocatori )

        limiti_carte = {
            'Guerriero': {'min': int(min_carte * NUMERO_CARTE_DISPONIBILI['Guerriero']) , 'max': int(max_carte * NUMERO_CARTE_DISPONIBILI['Guerriero']) },
            'Equipaggiamento': {'min': int(min_carte * NUMERO_CARTE_DISPONIBILI['Equipaggiamento']) , 'max': int(max_carte * NUMERO_CARTE_DISPONIBILI['Equipaggiamento']) },
            'Speciale': {'min': int(min_carte * NUMERO_CARTE_DISPONIBILI['Speciale']) , 'max': int(max_carte * NUMERO_CARTE_DISPONIBILI['Speciale']) },
            'Arte': {'min': int(min_carte * NUMERO_CARTE_DISPONIBILI['Arte']) , 'max': int(max_carte * NUMERO_CARTE_DISPONIBILI['Arte']) },
            'Oscura Simmetria': {'min': int(min_carte * NUMERO_CARTE_DISPONIBILI['Oscura Simmetria']) , 'max': int(max_carte * NUMERO_CARTE_DISPONIBILI['Oscura Simmetria']) },
            'Fortificazione': {'min': int(min_carte * NUMERO_CARTE_DISPONIBILI['Fortificazione']) , 'max': int(max_carte * NUMERO_CARTE_DISPONIBILI['Fortificazione']) },
            'Missione': {'min': int(min_carte * NUMERO_CARTE_DISPONIBILI['Missione']) , 'max': int(max_carte * NUMERO_CARTE_DISPONIBILI['Missione']) },
            'Reliquia': {'min': int(min_carte * NUMERO_CARTE_DISPONIBILI['Reliquia']) , 'max': int(max_carte * NUMERO_CARTE_DISPONIBILI['Reliquia']) },
            'Warzone': {'min': int(min_carte * NUMERO_CARTE_DISPONIBILI['Warzone']) , 'max': int(max_carte * NUMERO_CARTE_DISPONIBILI['Warzone']) },
        }
        """
        

        # Seleziona carte per ogni tipo
        
        # 1. Guerrieri
        print("Selezionando Guerrieri...")
        guerrieri = seleziona_carte_casuali_per_tipo(
            GUERRIERI_DATABASE,
            crea_guerriero_da_database, # funzione da utilizzare
            espansioni_valide,
            collezione.fazioni_orientamento,
            min_carte=LIMITI_CARTE_COLLEZIONE['Guerriero']['min'],
            max_carte=LIMITI_CARTE_COLLEZIONE['Guerriero']['max']
        )
        for guerriero in guerrieri:
            collezione.aggiungi_carta(guerriero)
        
        # 2. Equipaggiamenti
        print("Selezionando Equipaggiamenti...")
        equipaggiamenti = seleziona_carte_casuali_per_tipo(
            DATABASE_EQUIPAGGIAMENTO,
            crea_equipaggiamento_da_database,
            espansioni_valide,
            collezione.fazioni_orientamento,
            min_carte=LIMITI_CARTE_COLLEZIONE['Equipaggiamento']['min'],
            max_carte=LIMITI_CARTE_COLLEZIONE['Equipaggiamento']['max']
        )
        for equipaggiamento in equipaggiamenti:
            collezione.aggiungi_carta(equipaggiamento)
        
        # 3. Carte Speciali
        print("Selezionando Carte Speciali...")
        speciali = seleziona_carte_casuali_per_tipo(
            DATABASE_SPECIALI,
            crea_speciale_da_database,
            espansioni_valide,
            collezione.fazioni_orientamento,
            min_carte=LIMITI_CARTE_COLLEZIONE['Speciale']['min'],
            max_carte=LIMITI_CARTE_COLLEZIONE['Speciale']['max']
        )
        for speciale in speciali:
            collezione.aggiungi_carta(speciale)
        
        # 4. Fortificazioni
        print("Selezionando Fortificazioni...")
        fortificazioni = seleziona_carte_casuali_per_tipo(
            DATABASE_FORTIFICAZIONI,
            crea_fortificazione_da_database,
            espansioni_valide,
            collezione.fazioni_orientamento,
            min_carte=LIMITI_CARTE_COLLEZIONE['Fortificazione']['min'],
            max_carte=LIMITI_CARTE_COLLEZIONE['Fortificazione']['max']
        )
        for fortificazione in fortificazioni:
            collezione.aggiungi_carta(fortificazione)
        
        # 5. Missioni
        print("Selezionando Missioni...")
        missioni = seleziona_carte_casuali_per_tipo(
            DATABASE_MISSIONI,
            crea_missione_da_database,
            espansioni_valide,
            collezione.fazioni_orientamento,
            min_carte=LIMITI_CARTE_COLLEZIONE['Missione']['min'],
            max_carte=LIMITI_CARTE_COLLEZIONE['Missione']['max']
        )
        for missione in missioni:
            collezione.aggiungi_carta(missione)
        
        # 6. Arte
        print("Selezionando Arte...")
        arte = seleziona_carte_casuali_per_tipo(
            CARTE_ARTE_DATABASE,
            crea_arte_da_database,
            espansioni_valide,
            collezione.fazioni_orientamento,
            min_carte=LIMITI_CARTE_COLLEZIONE['Arte']['min'],            
            max_carte=LIMITI_CARTE_COLLEZIONE['Arte']['max']
        )
        for carta_arte in arte:
            collezione.aggiungi_carta(carta_arte)
        
        # 7. Oscura Simmetria
        print("Selezionando Oscura Simmetria...")
        oscura_simmetria = seleziona_carte_casuali_per_tipo(
            DATABASE_OSCURA_SIMMETRIA,
            crea_oscura_simmetria_da_database,
            espansioni_valide,
            collezione.fazioni_orientamento,
            min_carte=LIMITI_CARTE_COLLEZIONE['Oscura Simmetria']['min'],
            max_carte=LIMITI_CARTE_COLLEZIONE['Oscura Simmetria']['max']
        )
        for carta_oscura in oscura_simmetria:
            collezione.aggiungi_carta(carta_oscura)
        
        # 8. Reliquie
        print("Selezionando Reliquie...")
        reliquie = seleziona_carte_casuali_per_tipo(
            DATABASE_RELIQUIE,
            crea_reliquia_da_database,
            espansioni_valide,
            collezione.fazioni_orientamento,
            min_carte=LIMITI_CARTE_COLLEZIONE['Reliquia']['min'],
            max_carte=LIMITI_CARTE_COLLEZIONE['Reliquia']['max']
        )
        for reliquia in reliquie:
            collezione.aggiungi_carta(reliquia)
        
        # 9. Warzone
        print("Selezionando Warzone...")
        warzone = seleziona_carte_casuali_per_tipo(
            DATABASE_WARZONE,
            crea_warzone_da_database,
            espansioni_valide,
            collezione.fazioni_orientamento,
            min_carte=LIMITI_CARTE_COLLEZIONE['Warzone']['min'],
            max_carte=LIMITI_CARTE_COLLEZIONE['Warzone']['max']
        )
        for carta_warzone in warzone:
            collezione.aggiungi_carta(carta_warzone)
        
        collezioni.append(collezione)
        print(f"Collezione Giocatore {i+1} completata: {collezione.get_totale_carte()} carte totali")
    
    print(f"\n=== CREAZIONE COMPLETATA ===")
    print(f"Create {len(collezioni)} collezioni")
    print(f"Quantità totali utilizzate: {dict(QUANTITA_UTILIZZATE)}")
    
    return collezioni


# ==================== FUNZIONI DI UTILITÀ ====================

def stampa_riepilogo_collezioni(collezioni: List[CollezioneGiocatore]):
    """Stampa un riepilogo delle collezioni create"""
    print(f"\n{'='*50}")
    print(f"RIEPILOGO {len(collezioni)} COLLEZIONI GIOCATORI")
    print(f"{'='*50}")
    
    for collezione in collezioni:
        print(f"\n{collezione}")
    
    # Statistiche aggregate
    totale_carte = sum(c.get_totale_carte() for c in collezioni)
    totale_valore = sum(c.statistiche.valore_totale_dp for c in collezioni)
    
    print(f"\n{'='*30}")
    print(f"STATISTICHE AGGREGATE")
    print(f"{'='*30}")
    print(f"Totale carte create: {totale_carte}")
    print(f"Valore totale DP: {totale_valore}")
    print(f"Media carte per collezione: {totale_carte / len(collezioni):.1f}")
    print(f"Media valore DP per collezione: {totale_valore / len(collezioni):.1f}")



def converti_enum_ricorsivo(obj: Any) -> Any:
    """
    Converte ricorsivamente tutti gli enum in un oggetto (dizionario, lista, ecc.) 
    nei loro valori stringa per renderli serializzabili in JSON.
    """
    if isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, dict):
        return {
            (k.value if isinstance(k, Enum) else k): converti_enum_ricorsivo(v) 
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [converti_enum_ricorsivo(item) for item in obj]
    elif hasattr(obj, 'value'):
        return obj.value
    else:
        return obj

def salva_collezioni_json(collezioni: List, filename: str = "collezioni_giocatori.json"):
    """
    Salva le collezioni in formato JSON con gestione corretta degli enum.
    
    Args:
        collezioni: Lista delle collezioni da salvare
        filename: Nome del file di output
    """
    try:
        # Prepara i dati per l'export
        dati_export = {
            'numero_collezioni': len(collezioni),
            'data_creazione': str(datetime.now()),
            'collezioni': [c.export_to_dict() for c in collezioni]
        }
        
        # Converte ricorsivamente tutti gli enum in valori stringa
        dati_puliti = converti_enum_ricorsivo(dati_export)
        
        # Salva usando l'encoder personalizzato come backup
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dati_puliti, f, indent=2, ensure_ascii=False, cls=EnumJSONEncoder)
        
        print(f"✅ Collezioni salvate con successo in {filename}")
        
    except Exception as e:
        print(f"❌ Errore durante il salvataggio JSON: {e}")
        
        # Tentativo di salvataggio di debug per capire il problema
        try:
            debug_filename = filename.replace('.json', '_debug.txt')
            with open(debug_filename, 'w', encoding='utf-8') as f:
                f.write(f"Errore durante serializzazione JSON: {e}\n\n")
                f.write(f"Numero collezioni: {len(collezioni)}\n")
                for i, c in enumerate(collezioni):
                    f.write(f"Collezione {i}: {type(c)} - {c.id_giocatore}\n")
            print(f"File di debug salvato in {debug_filename}")
        except Exception as debug_error:
            print(f"Errore anche nel debug: {debug_error}")

# Funzione alternativa più semplice per casi estremi
def salva_collezioni_json_semplice(collezioni: List, filename: str = "collezioni_giocatori_simple.json"):
    """
    Versione semplificata del salvataggio che converte tutto in stringa.
    Usare solo se la versione completa non funziona.
    """
    try:
        dati_semplici = {
            'numero_collezioni': len(collezioni),
            'data_creazione': str(datetime.now()),
            'collezioni': []
        }
        
        for c in collezioni:
            collezione_semplice = {
                'id_giocatore': c.id_giocatore,
                'fazioni_orientamento': [str(f) for f in c.fazioni_orientamento],
                'statistiche': {
                    'guerrieri': c.statistiche.guerrieri,
                    'equipaggiamenti': c.statistiche.equipaggiamenti,
                    'speciali': c.statistiche.speciali,
                    'fortificazioni': c.statistiche.fortificazioni,
                    'missioni': c.statistiche.missioni,
                    'arte': c.statistiche.arte,
                    'oscura_simmetria': c.statistiche.oscura_simmetria,
                    'reliquie': c.statistiche.reliquie,
                    'warzone': c.statistiche.warzone,
                    'totale_carte': c.statistiche.totale_carte,
                    'valore_totale_dp': c.statistiche.valore_totale_dp,
                    # Converte tutte le chiavi in stringa
                    'per_fazione': {str(k): v for k, v in c.statistiche.per_fazione.items()},
                    'per_set': {str(k): v for k, v in c.statistiche.per_set.items()},
                    'per_rarity': {str(k): v for k, v in c.statistiche.per_rarity.items()}
                },
                'totale_carte': c.get_totale_carte()
            }
            dati_semplici['collezioni'].append(collezione_semplice)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dati_semplici, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Collezioni salvate (versione semplice) in {filename}")
        
    except Exception as e:
        print(f"❌ Errore anche nella versione semplice: {e}")


def verifica_integrità_collezioni(collezioni: List[CollezioneGiocatore]) -> Dict[str, Any]:
    """Verifica l'integrità delle collezioni create"""
    risultati = {
        'collezioni_valide': 0,
        'collezioni_con_errori': 0,
        'errori_trovati': [],
        'collezioni_con_guerrieri': 0,
        'orientamento_applicato': 0
    }
    
    for collezione in collezioni:
        errori_collezione = []
        
        # Verifica presenza guerrieri (non più minimo obbligatorio)
        if collezione.statistiche.guerrieri > 0:
            risultati['collezioni_con_guerrieri'] += 1
        
        # Verifica orientamento
        if collezione.fazioni_orientamento:
            risultati['orientamento_applicato'] += 1
            
            # Verifica che l'orientamento sia effettivamente applicato
            fazioni_collezione = set(collezione.statistiche.per_fazione.keys())
            fazioni_orientamento = set(f.value for f in collezione.fazioni_orientamento)
            
            if not any(f in fazioni_collezione for f in fazioni_orientamento):
                errori_collezione.append(f"Collezione {collezione.id_giocatore}: orientamento non applicato correttamente")
        
        # Conta risultati
        if errori_collezione:
            risultati['collezioni_con_errori'] += 1
            risultati['errori_trovati'].extend(errori_collezione)
        else:
            risultati['collezioni_valide'] += 1
    
    return risultati


# ==================== ESEMPI E TEST ====================

def test_creazione_collezioni_base():
    """Test base per la creazione di collezioni"""
    print("\n" + "="*60)
    print("TEST: Creazione collezioni BASE (senza orientamento)")
    print("="*60)
    
    collezioni = creazione_Collezione_Giocatore(
        numero_giocatori=2,
        espansioni=[Set_Espansione.BASE],
        orientamento=False
    )
    
    stampa_riepilogo_collezioni(collezioni)
    
    integrità = verifica_integrità_collezioni(collezioni)
    print(f"\nRisultati verifica integrità: {integrità}")
    
    return collezioni


def test_creazione_collezioni_orientate():
    """Test per la creazione di collezioni con orientamento"""
    print("\n" + "="*60)
    print("TEST: Creazione collezioni ORIENTATE")
    print("="*60)
    
    collezioni = creazione_Collezione_Giocatore(
        numero_giocatori=3,
        espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
        orientamento=True
    )
    
    stampa_riepilogo_collezioni(collezioni)
    
    integrità = verifica_integrità_collezioni(collezioni)
    print(f"\nRisultati verifica integrità: {integrità}")
    
    return collezioni


def test_creazione_collezioni_multiple_espansioni():
    """Test per la creazione di collezioni con multiple espansioni"""
    print("\n" + "="*60)
    print("TEST: Creazione collezioni MULTIPLE ESPANSIONI")
    print("="*60)
    
    collezioni = creazione_Collezione_Giocatore(
        numero_giocatori=4,
        espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE],
        orientamento=True
    )
    
    stampa_riepilogo_collezioni(collezioni)
    
    integrità = verifica_integrità_collezioni(collezioni)
    print(f"\nRisultati verifica integrità: {integrità}")
    
    return collezioni


def test_creazione_collezioni_stress():
    """Test stress per verificare la gestione delle quantità"""
    print("\n" + "="*60)
    print("TEST: STRESS TEST - Molte collezioni")
    print("="*60)
    
    try:
        collezioni = creazione_Collezione_Giocatore(
            numero_giocatori=8,
            espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
            orientamento=True
        )
        
        stampa_riepilogo_collezioni(collezioni)
        
        integrità = verifica_integrità_collezioni(collezioni)
        print(f"\nRisultati verifica integrità: {integrità}")
        
        # Verifica se ci sono state limitazioni per quantità
        print(f"\nQuantità utilizzate totali:")
        for carta, quantita in sorted(QUANTITA_UTILIZZATE.items()):
            if quantita > 3:  # Mostra solo carte con alta utilizzazione
                print(f"  {carta}: {quantita}")
        
        return collezioni
        
    except Exception as e:
        print(f"Errore durante stress test: {e}")
        return []


def test_validazione_parametri():
    """Test per validazione parametri di input"""
    print("\n" + "="*60)
    print("TEST: Validazione parametri")
    print("="*60)
    
    # Test parametri non validi
    test_cases = [
        (0, [Set_Espansione.BASE], False, "numero_giocatori = 0"),
        (-1, [Set_Espansione.BASE], False, "numero_giocatori negativo"),
        (1, [], False, "espansioni vuote"),
        (1, ["INVALID"], False, "espansione non valida"),
        (1, [None], False, "espansione None")
    ]
    
    for num_giocatori, espansioni, orientamento, descrizione in test_cases:
        print(f"\nTestando: {descrizione}")
        try:
            collezioni = creazione_Collezione_Giocatore(num_giocatori, espansioni, orientamento)
            print(f"  ❌ Doveva fallire ma ha creato {len(collezioni)} collezioni")
        except Exception as e:
            print(f"  ✅ Fallito correttamente: {e}")
    
    # Test parametri validi edge case
    print(f"\nTestando: 1 giocatore, 1 espansione")
    try:
        collezioni = creazione_Collezione_Giocatore(1, [Set_Espansione.BASE], False)
        print(f"  ✅ Successo: {len(collezioni)} collezione creata")
        if collezioni[0].statistiche.guerrieri == 0:
            print(f"    ℹ️  Collezione senza guerrieri (OK per collezione giocatore)")
    except Exception as e:
        print(f"  ❌ Fallito inaspettatamente: {e}")


def analizza_bilanciamento_collezioni(collezioni: List[CollezioneGiocatore]):
    """Analizza il bilanciamento delle collezioni create"""
    print("\n" + "="*60)
    print("ANALISI BILANCIAMENTO COLLEZIONI")
    print("="*60)
    
    if not collezioni:
        print("Nessuna collezione da analizzare")
        return
    
    # Statistiche per tipo di carta
    stats_tipi = defaultdict(list)
    stats_valore = []
    stats_fazioni = defaultdict(list)
    
    for collezione in collezioni:
        stats = collezione.statistiche
        stats_tipi['guerrieri'].append(stats.guerrieri)
        stats_tipi['equipaggiamenti'].append(stats.equipaggiamenti)
        stats_tipi['speciali'].append(stats.speciali)
        stats_tipi['fortificazioni'].append(stats.fortificazioni)
        stats_tipi['missioni'].append(stats.missioni)
        stats_tipi['arte'].append(stats.arte)
        stats_tipi['oscura simmetria'].append(stats.oscura_simmetria)
        stats_tipi['reliquie'].append(stats.reliquie)
        stats_tipi['warzone'].append(stats.warzone)
        
        stats_valore.append(stats.valore_totale_dp)
        
        for fazione, count in stats.per_fazione.items():
            stats_fazioni[fazione].append(count)
    
    # Analisi distribuzione tipi di carte
    print("Distribuzione per tipo di carta:")
    for tipo, valori in stats_tipi.items():
        if valori:
            media = sum(valori) / len(valori)
            minimo = min(valori)
            massimo = max(valori)
            print(f"  {tipo.capitalize()}: min={minimo}, max={massimo}, media={media:.1f}")
    
    # Analisi valore collezioni
    if stats_valore:
        media_valore = sum(stats_valore) / len(stats_valore)
        min_valore = min(stats_valore)
        max_valore = max(stats_valore)
        print(f"\nValore DP collezioni:")
        print(f"  Min: {min_valore}, Max: {max_valore}, Media: {media_valore:.1f}")
        
        # Calcola varianza per verificare bilanciamento
        varianza = sum((v - media_valore) ** 2 for v in stats_valore) / len(stats_valore)
        deviazione_std = varianza ** 0.5
        print(f"  Deviazione standard: {deviazione_std:.1f}")
        
        if deviazione_std < media_valore * 0.2:
            print("  ✅ Collezioni ben bilanciate")
        else:
            print("  ⚠️ Collezioni potrebbero essere sbilanciate")
    
    # Analisi distribuzione fazioni
    print(f"\nDistribuzione fazioni:")
    for fazione, valori in stats_fazioni.items():
        if valori:
            media = sum(valori) / len(valori)
            presente_in = len([v for v in valori if v > 0])
            print(f"  {fazione}: media={media:.1f}, presente in {presente_in}/{len(collezioni)} collezioni")
    
    # Analisi guerrieri nelle collezioni
    guerrieri_valori = stats_tipi.get('guerrieri', [])
    if guerrieri_valori:
        collezioni_senza_guerrieri = len([v for v in guerrieri_valori if v == 0])
        if collezioni_senza_guerrieri > 0:
            print(f"\n⚠️  {collezioni_senza_guerrieri} collezioni senza guerrieri")
            print(f"   (OK per collezioni giocatore - potranno acquistare guerrieri separatamente)")


def esempio_utilizzo_completo():
    """Esempio completo di utilizzo del Manager_Gioco"""
    print("\n" + "="*80)
    print("ESEMPIO UTILIZZO COMPLETO - MANAGER_GIOCO")
    print("="*80)
    
    # Reset per esempio pulito
    resetta_tracciamento_quantita()
    
    print("1. Creazione collezioni per torneo 4 giocatori...")
    collezioni_torneo = creazione_Collezione_Giocatore(
        numero_giocatori=4,
        espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
        orientamento=True
    )
    
    print("\n2. Analisi dettagliata delle collezioni...")
    stampa_riepilogo_collezioni(collezioni_torneo)
    
    print("\n3. Verifica integrità...")
    integrità = verifica_integrità_collezioni(collezioni_torneo)
    print(f"Risultati integrità: {integrità}")
    
    print("\n4. Analisi bilanciamento...")
    analizza_bilanciamento_collezioni(collezioni_torneo)
    
    print("\n5. Dettaglio orientamenti utilizzati...")
    for collezione in collezioni_torneo:
        if collezione.fazioni_orientamento:
            fazioni_str = ", ".join([f.value for f in collezione.fazioni_orientamento])
            print(f"  Giocatore {collezione.id_giocatore}: {fazioni_str}")
        else:
            print(f"  Giocatore {collezione.id_giocatore}: Nessun orientamento")
    
    print("\n6. Esempio accesso alle carte...")
    collezione_esempio = collezioni_torneo[0]
    print(f"\nCollezione Giocatore 1:")
    print(f"  Guerrieri: {len(collezione_esempio.get_carte_per_tipo('guerrieri'))}")
    print(f"  Equipaggiamenti: {len(collezione_esempio.get_carte_per_tipo('equipaggiamenti'))}")
    
    # Mostra alcuni esempi di carte
    guerrieri = collezione_esempio.get_carte_per_tipo('guerrieri')
    if guerrieri:
        print(f"  Primo guerriero: {guerrieri[0].nome} ({guerrieri[0].fazione.value})")
    
    equipaggiamenti = collezione_esempio.get_carte_per_tipo('equipaggiamenti')
    if equipaggiamenti:
        print(f"  Primo equipaggiamento: {equipaggiamenti[0].nome}")
    
    return collezioni_torneo


def menu_interattivo():
    """Menu interattivo per testare le funzionalità"""
    
    while True:
        print("\n" + "="*60)
        print("MANAGER_GIOCO - MENU INTERATTIVO")
        print("="*60)
        print("1. Test creazione collezioni base")
        print("2. Test creazione collezioni orientate")
        print("3. Test multiple espansioni")
        print("4. Stress test")
        print("5. Test validazione parametri")
        print("6. Esempio utilizzo completo")
        print("7. Creazione personalizzata")
        print("8. Reset tracciamento quantità")
        print("0. Esci")
        
        scelta = input("\nScegli un'opzione: ").strip()
        
        if scelta == "0":
            print("Arrivederci!")
            break
        elif scelta == "1":
            test_creazione_collezioni_base()
        elif scelta == "2":
            test_creazione_collezioni_orientate()
        elif scelta == "3":
            test_creazione_collezioni_multiple_espansioni()
        elif scelta == "4":
            test_creazione_collezioni_stress()
        elif scelta == "5":
            test_validazione_parametri()
        elif scelta == "6":
            esempio_utilizzo_completo()
        elif scelta == "7":
            # Creazione personalizzata
            try:
                num = int(input("Numero giocatori: "))
                
                print("Espansioni disponibili:")
                for i, esp in enumerate(Set_Espansione):
                    print(f"  {i+1}. {esp.value}")
                
                esp_input = input("Scegli espansioni (numeri separati da virgola): ")
                esp_indices = [int(x.strip())-1 for x in esp_input.split(",")]
                espansioni = [list(Set_Espansione)[i] for i in esp_indices if 0 <= i < len(Set_Espansione)]
                
                orientamento = input("Orientamento (s/n): ").lower().startswith('s')
                
                collezioni = creazione_Collezione_Giocatore(num, espansioni, orientamento)
                stampa_riepilogo_collezioni(collezioni)
                
                salva = input("Salvare in JSON? (s/n): ").lower().startswith('s')
                if salva:
                    filename = f"collezioni_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    salva_collezioni_json(collezioni, filename)
                
            except Exception as e:
                print(f"Errore: {e}")
        elif scelta == "8":
            resetta_tracciamento_quantita()
            print("Tracciamento quantità resettato.")
        else:
            print("Opzione non valida.")
        
        input("\nPremi Invio per continuare...")



def test_creazioni_individuali():
    """Test delle singole funzioni di creazione carte"""
    print("Testando funzioni di creazione individuali...")
    
    test_cases = [
        ("Guerriero", crea_guerriero_da_database, "Bauhaus Blitzer"),
        ("Equipaggiamento", crea_equipaggiamento_da_database, "spada_combattimento"),
        ("Speciale", crea_speciale_da_database, "tactical_advance"),
        ("Fortificazione", crea_fortificazione_da_database, "Heimburg"),
        ("Missione", crea_missione_da_database, "recupero_intelligence"),
        ("Arte", crea_arte_da_database, "blessing_of_light"),
        ("Oscura Simmetria", crea_oscura_simmetria_da_database, "corruzione_minore"),
        ("Reliquia", crea_reliquia_da_database, "antica_reliquia"),
        ("Warzone", crea_warzone_da_database, "zona_guerra")
    ]
    
    for tipo_carta, funzione, nome_esempio in test_cases:
        try:
            carta = funzione(nome_esempio)
            if carta:
                print(f"  ✅ {tipo_carta}: {carta.nome}")
            else:
                print(f"  ⚠️ {tipo_carta}: carta '{nome_esempio}' non trovata (OK se non nel database)")
        except Exception as e:
            print(f"  ❌ {tipo_carta}: errore durante la creazione: {e}")
    
    print(f"\n{'='*80}")
    print("Per testare interattivamente, decommentare la riga seguente:")
    print("# menu_interattivo()")
    print(f"{'='*80}")
    
    # Per attivare il menu interattivo, decommenta la riga seguente:
    menu_interattivo()



# ==================== MAIN ====================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           MANAGER_GIOCO.PY                                  ║
║                    Mutant Chronicles / Doomtrooper                          ║
║                                                                              ║
║  Modulo per la creazione di collezioni giocatore secondo le regole          ║
║  ufficiali del regolamento Doomtrooper.                                     ║
║                                                                              ║
║  Funzionalità implementate:                                                  ║
║  • Creazione collezioni giocatore (non mazzi da gioco)                      ║
║  • Orientamento fazioni casuali (Fratellanza-Doomtrooper-Freelancer, etc.)  ║
║  • Selezione casuale carte da tutte le espansioni specificate               ║
║  • Verifica integrità e bilanciamento collezioni                            ║
║  • Export/Import JSON                                                        ║
║  • Sistema di test completo                                                  ║
║                                                                              ║
║  NOTA: CollezioneGiocatore = tutte le carte possedute                       ║
║        Mazzo da gioco = sottoinsieme con min 5 guerrieri (creato separatam.)║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("AVVIO DEMO AUTOMATICA...")
    
    # Demo rapida delle funzionalità principali
    try:
        print("\n🎯 Demo: Creazione collezioni base")
        demo_collezioni = creazione_Collezione_Giocatore(
            numero_giocatori=2,
            espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
            orientamento=False
        )
        print(f"✅ Create {len(demo_collezioni)} collezioni base")
        
        print("\n🎯 Demo: Creazione collezioni orientate")
        demo_orientate = creazione_Collezione_Giocatore(
            numero_giocatori=2,
            espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
            orientamento=True
        )
        print(f"✅ Create {len(demo_orientate)} collezioni orientate")
        
        print("\n🎯 Demo: Verifica integrità")
        integrità = verifica_integrità_collezioni(demo_orientate)
        print(f"✅ Verifica completata: {integrità['collezioni_valide']} valide su {len(demo_orientate)}")
        
        print(f"\n🎯 Demo completata con successo!")
        print(f"📊 Totale carte generate: {sum(c.get_totale_carte() for c in demo_collezioni + demo_orientate)}")
        
        print("\n🎯 Demo: Test funzioni di creazione individuali")
        test_creazioni_individuali()
        
    except Exception as e:
        print(f"❌ Errore durante la demo: {e}")


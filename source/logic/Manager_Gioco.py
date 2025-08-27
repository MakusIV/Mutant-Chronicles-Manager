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
from dataclasses import dataclass


# Import delle classi delle carte (solo le classi, non le funzioni di creazione)
from source.cards.Guerriero import (
    Guerriero, Fazione, Set_Espansione, Rarity, TipoGuerriero
)
from source.cards.Equipaggiamento import Equipaggiamento
from source.cards.Speciale import Speciale
from source.cards.Fortificazione import Fortificazione
from source.cards.Missione import Missione
from source.cards.Arte import Arte, DisciplinaArte
from source.cards.Oscura_Simmetria import Oscura_Simmetria, ApostoloOscuraSimmetria
from source.cards.Reliquia import Reliquia
from source.cards.Warzone import Warzone

# Import delle classi necessarie (assumi che siano disponibili)

from source.data_base_cards.Database_Arte import Database_Arte
from source.data_base_cards.Database_Oscura_Simmetria import Database_Oscura_Simmetria
from source.data_base_cards.Database_Equipaggiamento import Database_Equipaggiamento
from source.data_base_cards.Database_Speciale import Database_Speciale
from source.data_base_cards.Database_Fortificazione import Database_Fortificazione
from source.data_base_cards.Database_Reliquia import Database_Reliquia
from source.data_base_cards.Database_Warzone import Database_Warzone
from source.data_base_cards.Database_Missione import Database_Missione


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

PERCORSO_SALVATAGGIO = "out/"


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
    
   
        
    # Fix per il metodo aggiorna_statistiche nella classe StatisticheCollezione
    # Questo metodo deve gestire sia enum che stringhe per set_espansione

    def aggiorna_statistiche(self, carta: Any, quantita: int = 1):
        """Aggiorna le statistiche in base alla carta aggiunta"""
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
        
        # Aggiorna contatori per fazione, set e rarità con gestione sicura degli enum
        if hasattr(carta, 'fazione'):
            # Gestisce sia enum che stringhe per fazione
            fazione_key = carta.fazione.value if hasattr(carta.fazione, 'value') else str(carta.fazione)
            self.per_fazione[fazione_key] += quantita
            
        if hasattr(carta, 'set_espansione'):
            # Gestisce sia enum che stringhe per set_espansione - QUI È IL FIX PRINCIPALE
            if hasattr(carta.set_espansione, 'value'):
                # È un enum Set_Espansione
                set_key = carta.set_espansione.value
            else:
                # È già una stringa
                set_key = str(carta.set_espansione)
            self.per_set[set_key] += quantita
            
        if hasattr(carta, 'rarity'):
            # Gestisce sia enum che stringhe per rarity
            rarity_key = carta.rarity.value if hasattr(carta.rarity, 'value') else str(carta.rarity)
            self.per_rarity[rarity_key] += quantita

    # Alternativa più robusta usando try/except:
    def aggiorna_statistiche_robusta(self, carta: Any, quantita: int = 1):
        """Versione più robusta che gestisce tutti i casi possibili"""
        tipo_carta = type(carta).__name__.lower()
        
        # ... codice per aggiornare contatori per tipo carta ...
        
        # Aggiorna contatori per fazione con gestione errori
        if hasattr(carta, 'fazione'):
            try:
                fazione_key = carta.fazione.value
            except AttributeError:
                fazione_key = str(carta.fazione)
            self.per_fazione[fazione_key] += quantita
            
        # Aggiorna contatori per set_espansione con gestione errori
        if hasattr(carta, 'set_espansione'):
            try:
                set_key = carta.set_espansione.value
            except AttributeError:
                set_key = str(carta.set_espansione)
            self.per_set[set_key] += quantita
            
        # Aggiorna contatori per rarity con gestione errori
        if hasattr(carta, 'rarity'):
            try:
                rarity_key = carta.rarity.value
            except AttributeError:
                rarity_key = str(carta.rarity)
            self.per_rarity[rarity_key] += quantita

    # Funzione helper per convertire enum in stringa sicura
    def enum_to_string(obj):
        """Converte un enum in stringa in modo sicuro"""
        if hasattr(obj, 'value'):
            return obj.value
        else:
            return str(obj)


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
    
    #def __str__(self) -> str:
    #    fazioni_str = ", ".join([f.value if hasattr(f, 'value') else str(f) for f in self.fazioni_orientamento])
    #    return f"""Collezione Giocatore {self.id_giocatore}:
    #        Fazioni orientamento: {fazioni_str}
    #        {self.statistiche}"""

    #####################  AGGIUNTA ############################################

    # Metodi aggiuntivi da aggiungere alla classe CollezioneGiocatore
    # per migliorare la gestione dell'inventario

    def get_inventario_dettagliato(self) -> Dict[str, Dict[str, Any]]:
        """
        Restituisce l'inventario completo con dettagli per ogni carta.
        
        Returns:
            Dict: {nome_carta: {tipo, quantita, fazione (se guerriero), rarità, set, valore}}
        """
        inventario = {}
        
        for tipo_carta, liste_carte in self.carte.items():
            for carta in liste_carte:
                nome_carta = carta.nome
                
                if nome_carta not in inventario:
                    # Crea entry base
                    inventario[nome_carta] = {
                        'tipo': tipo_carta.capitalize(),
                        'quantita': 0,
                        'rarity': None,
                        'set_espansione': None,
                        'valore_dp': 0
                    }
                    
                    # Aggiunge fazione se è un guerriero
                    if tipo_carta == 'guerriero' and hasattr(carta, 'fazione'):
                        fazione = carta.fazione.value if hasattr(carta.fazione, 'value') else str(carta.fazione)
                        inventario[nome_carta]['fazione'] = fazione
                    
                    # Aggiunge rarità
                    if hasattr(carta, 'rarity'):
                        rarity = carta.rarity.value if hasattr(carta.rarity, 'value') else str(carta.rarity)
                        inventario[nome_carta]['rarity'] = rarity
                    
                    # Aggiunge set espansione
                    if hasattr(carta, 'set_espansione'):
                        set_esp = carta.set_espansione.value if hasattr(carta.set_espansione, 'value') else str(carta.set_espansione)
                        inventario[nome_carta]['set_espansione'] = set_esp
                    
                    # Aggiunge valore DP
                    if hasattr(carta, 'valore'):
                        inventario[nome_carta]['valore_dp'] = carta.valore
                    elif hasattr(carta, 'costo_destino'):
                        inventario[nome_carta]['valore_dp'] = carta.costo_destino
                
                # Incrementa quantità
                inventario[nome_carta]['quantita'] += 1
        
        return inventario

    def stampa_inventario_compatto(self):
        """
        Stampa una versione compatta dell'inventario organizzata per tipo.
        """
        print(f"\n📦 INVENTARIO COMPATTO - GIOCATORE {self.id_giocatore}")
        print("=" * 60)
        
        # Orientamento se presente
        if self.fazioni_orientamento:
            fazioni_str = ", ".join([f.value if hasattr(f, 'value') else str(f) for f in self.fazioni_orientamento])
            print(f"🎯 Orientamento: {fazioni_str}")
            print("-" * 60)
        
        tipi_carte = {
            'guerriero': '⚔️  Guerrieri',
            'equipaggiamento': '🛡️  Equipaggiamenti', 
            'speciale': '🎴 Speciali',
            'fortificazione': '🏰 Fortificazioni',
            'missione': '📜 Missioni',
            'arte': '✨ Arte',
            'oscura_simmetria': '🌑 Oscura Simmetria',
            'reliquia': '🏺 Reliquie',
            'warzone': '💥 Warzone'
        }
        
        for tipo_carta, icona_nome in tipi_carte.items():
            carte_tipo = self.carte.get(tipo_carta, [])
            if carte_tipo:
                # Conta le carte uniche
                carte_uniche = defaultdict(int)
                for carta in carte_tipo:
                    carte_uniche[carta.nome] += 1
                
                print(f"\n{icona_nome}: {len(carte_tipo)} carte ({len(carte_uniche)} uniche)")
                
                # Mostra le più comuni (>1 copia)
                carte_multiple = {nome: qty for nome, qty in carte_uniche.items() if qty > 1}
                if carte_multiple:
                    print("   Copie multiple:", end=" ")
                    items = [f"{nome}(x{qty})" for nome, qty in sorted(carte_multiple.items())]
                    print(", ".join(items[:3]))  # Mostra solo le prime 3
                    if len(items) > 3:
                        print(f"   ... e {len(items) - 3} altre")

    def get_statistiche_avanzate(self) -> Dict[str, Any]:
        """
        Calcola statistiche avanzate della collezione.
        
        Returns:
            Dict con statistiche dettagliate
        """
        stats = {
            'totale_carte': self.get_totale_carte(),
            'carte_uniche': 0,
            'valore_totale_dp': self.statistiche.valore_totale_dp,
            'distribuzione_rarità': defaultdict(int),
            'distribuzione_set': defaultdict(int),
            'distribuzione_fazioni': defaultdict(int),
            'guerrieri_per_fazione': defaultdict(int),
            'carta_più_comune': {'nome': '', 'quantita': 0},
            'carta_più_rara': {'nome': '', 'rarity': ''},
            'valore_medio_carta': 0
        }
        
        inventario = self.get_inventario_dettagliato()
        stats['carte_uniche'] = len(inventario)
        
        if stats['totale_carte'] > 0:
            stats['valore_medio_carta'] = stats['valore_totale_dp'] / stats['totale_carte']
        
        # Analizza ogni carta unica
        for nome_carta, info in inventario.items():
            # Distribuzione rarità
            if info['rarity']:
                stats['distribuzione_rarità'][info['rarity']] += info['quantita']
            
            # Distribuzione set
            if info['set_espansione']:
                stats['distribuzione_set'][info['set_espansione']] += info['quantita']
            
            # Distribuzione fazioni
            if 'fazione' in info and info['fazione']:
                stats['distribuzione_fazioni'][info['fazione']] += info['quantita']
                if info['tipo'] == 'Guerriero':
                    stats['guerrieri_per_fazione'][info['fazione']] += info['quantita']
            
            # Carta più comune
            if info['quantita'] > stats['carta_più_comune']['quantita']:
                stats['carta_più_comune'] = {
                    'nome': nome_carta,
                    'quantita': info['quantita'],
                    'tipo': info['tipo']
                }
            
            # Carta più rara (in termini di rarità, non quantità)
            rarità_priorità = {'Ultra Rare': 4, 'Rare': 3, 'Uncommon': 2, 'Common': 1}
            rarity_attuale = rarità_priorità.get(info.get('rarity', ''), 0)
            rarity_max = rarità_priorità.get(stats['carta_più_rara'].get('rarity', ''), 0)
            
            if rarity_attuale > rarity_max:
                stats['carta_più_rara'] = {
                    'nome': nome_carta,
                    'rarity': info['rarity'],
                    'tipo': info['tipo']
                }
        
        return stats

    def stampa_statistiche_avanzate(self):
        """
        Stampa statistiche avanzate della collezione.
        """
        stats = self.get_statistiche_avanzate()
        
        print(f"\n📊 STATISTICHE AVANZATE - GIOCATORE {self.id_giocatore}")
        print("=" * 65)
        
        print(f"📦 Carte totali: {stats['totale_carte']} ({stats['carte_uniche']} uniche)")
        print(f"💰 Valore totale: {stats['valore_totale_dp']} DP")
        print(f"💎 Valore medio/carta: {stats['valore_medio_carta']:.1f} DP")
        
        # Carta più comune
        if stats['carta_più_comune']['quantita'] > 1:
            comune = stats['carta_più_comune']
            print(f"🔄 Carta più comune: {comune['nome']} (x{comune['quantita']}, {comune['tipo']})")
        
        # Carta più rara
        if stats['carta_più_rara']['nome']:
            rara = stats['carta_più_rara']
            print(f"💎 Carta più rara: {rara['nome']} ({rara['rarity']}, {rara['tipo']})")
        
        # Distribuzione rarità
        if stats['distribuzione_rarità']:
            print(f"\n🌟 Distribuzione Rarità:")
            for rarity, count in sorted(stats['distribuzione_rarità'].items()):
                percentuale = (count / stats['totale_carte']) * 100
                print(f"   {rarity}: {count} carte ({percentuale:.1f}%)")
        
        # Distribuzione set
        if stats['distribuzione_set']:
            print(f"\n📚 Distribuzione Set:")
            for set_nome, count in sorted(stats['distribuzione_set'].items()):
                percentuale = (count / stats['totale_carte']) * 100
                print(f"   {set_nome}: {count} carte ({percentuale:.1f}%)")
        
        # Guerrieri per fazione
        if stats['guerrieri_per_fazione']:
            print(f"\n⚔️  Guerrieri per Fazione:")
            for fazione, count in sorted(stats['guerrieri_per_fazione'].items()):
                print(f"   {fazione}: {count} guerrieri")

    def cerca_carte(self, termine: str, tipo_carta: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Cerca carte nella collezione.
        
        Args:
            termine: Termine da cercare nei nomi delle carte
            tipo_carta: Tipo specifico di carta da cercare (opzionale)
        
        Returns:
            Lista di risultati con dettagli delle carte trovate
        """
        risultati = []
        inventario = self.get_inventario_dettagliato()
        termine_lower = termine.lower()
        
        for nome_carta, info in inventario.items():
            # Filtra per tipo se specificato
            if tipo_carta and info['tipo'].lower() != tipo_carta.lower():
                continue
            
            # Cerca nel nome
            if termine_lower in nome_carta.lower():
                risultato = info.copy()
                risultato['nome'] = nome_carta
                risultati.append(risultato)
        
        return risultati

    def __str__(self) -> str:
        """Rappresentazione string migliorata della collezione"""
        orientamento_str = ""
        if self.fazioni_orientamento:
            fazioni = [f.value if hasattr(f, 'value') else str(f) for f in self.fazioni_orientamento]
            orientamento_str = f" [🎯 {', '.join(fazioni)}]"
        
        return f"""🎮 Collezione Giocatore {self.id_giocatore}{orientamento_str}
                    📦 Totale carte: {self.get_totale_carte()}
                    💰 Valore: {self.statistiche.valore_totale_dp} DP
                    ⚔️  Guerrieri: {self.statistiche.guerrieri}
                    🛡️  Equipaggiamenti: {self.statistiche.equipaggiamenti}
                    🎴 Speciali: {self.statistiche.speciali}
                    🏰 Fortificazioni: {self.statistiche.fortificazioni}
                    📜 Missioni: {self.statistiche.missioni}
                    ✨ Arte: {self.statistiche.arte}
                    🌑 Oscura Simmetria: {self.statistiche.oscura_simmetria}
                    🏺 Reliquie: {self.statistiche.reliquie}
                    💥 Warzone: {self.statistiche.warzone}"""

    # Esempio di come aggiungere questi metodi alla classe esistente:
    """
    Per integrare questi metodi nella classe CollezioneGiocatore esistente,
    aggiungi il contenuto di questo file alla classe:

    class CollezioneGiocatore:
        # ... metodi esistenti ...
        
        # Aggiungi qui tutti i metodi sopra definiti
        get_inventario_dettagliato = get_inventario_dettagliato
        stampa_inventario_compatto = stampa_inventario_compatto
        get_statistiche_avanzate = get_statistiche_avanzate
        stampa_statistiche_avanzate = stampa_statistiche_avanzate
        cerca_carte = cerca_carte
        __str__ = __str__  # Sostituisce il __str__ esistente
    """

    print("Metodi per inventario dettagliato della CollezioneGiocatore creati.")
    print("Integrare questi metodi nella classe esistente per funzionalità avanzate.")

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
    
    # Determina numero di carte da selezionare per una stessa carta
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
            7,  # Massimo 7 copie per carta per collezione (considera mazzo max 5 carte e collezione di gioco: totale 25 carte). La quantità minima consigliata viene utilizzata per la creazione del mazzo
            dati_carta.get('quantita', 0) - QUANTITA_UTILIZZATE[nome_carta]
        )
        
        #if max_quantita_disponibile <= 0:
            # Rimuovi carte non più disponibili
        if nome_carta in carte_orientate:
            del carte_orientate[nome_carta] # elimina la carta e di conseguenza dal pool di scelta casuale: un solo prelievo
        if nome_carta in carte_generiche:
            del carte_generiche[nome_carta] # elimina la carta e di conseguenza dal pool di scelta casuale: un solo prelievo
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



#################################  AGGIUNTA ########################################################

def stampa_inventario_dettagliato(collezione):
    """
    Stampa l'inventario dettagliato della collezione con tipo di carta 
    e fazione per i guerrieri.
    
    Args:
        collezione: Oggetto CollezioneGiocatore
    """
    print(f"\n📦 INVENTARIO DETTAGLIATO - GIOCATORE {collezione.id_giocatore}")
    print("=" * 80)
    
    if collezione.fazioni_orientamento:
        fazioni_str = ", ".join([f.value if hasattr(f, 'value') else str(f) for f in collezione.fazioni_orientamento])
        print(f"🎯 Orientamento: {fazioni_str}")
        print("-" * 80)
    
    # Organizza le carte per tipo con informazioni dettagliate
    inventario_organizzato = organizza_inventario_per_tipo(collezione)
    
    # Stampa ogni tipo di carta
    for tipo_carta, carte_info in inventario_organizzato.items():
        if carte_info:
            print(f"\n🃏 {tipo_carta.upper()}: {len(carte_info)} carte")
            print("-" * 40)
            
            # Ordina per nome carta
            for nome_carta, info in sorted(carte_info.items()):
                quantita = info['quantita']
                esempi = info['esempi']
                
                # Costruisce la stringa di visualizzazione
                riga_base = f"  • {nome_carta} (x{quantita})"
                
                # Aggiunge informazioni specifiche per tipo
                if tipo_carta == "guerriero" and esempi:
                    # Per i guerrieri mostra la fazione
                    guerriero_esempio = esempi[0]
                    if hasattr(guerriero_esempio, 'fazione'):
                        fazione = guerriero_esempio.fazione.value if hasattr(guerriero_esempio.fazione, 'value') else str(guerriero_esempio.fazione)
                        riga_base += f" [{fazione}]"
                    
                    # Aggiunge rarità e set se disponibili
                    if hasattr(guerriero_esempio, 'rarity'):
                        rarity = guerriero_esempio.rarity.value if hasattr(guerriero_esempio.rarity, 'value') else str(guerriero_esempio.rarity)
                        riga_base += f" ({rarity})"
                    
                    if hasattr(guerriero_esempio, 'set_espansione'):
                        set_esp = guerriero_esempio.set_espansione.value if hasattr(guerriero_esempio.set_espansione, 'value') else str(guerriero_esempio.set_espansione)
                        riga_base += f" - {set_esp}"
                
                elif esempi:  # Per altri tipi di carta
                    carta_esempio = esempi[0]
                    info_extra = []
                    
                    # Aggiunge rarità se disponibile
                    if hasattr(carta_esempio, 'rarity'):
                        rarity = carta_esempio.rarity.value if hasattr(carta_esempio.rarity, 'value') else str(carta_esempio.rarity)
                        info_extra.append(rarity)
                    
                    # Aggiunge set se disponibile
                    if hasattr(carta_esempio, 'set_espansione'):
                        set_esp = carta_esempio.set_espansione.value if hasattr(carta_esempio.set_espansione, 'value') else str(carta_esempio.set_espansione)
                        info_extra.append(set_esp)
                    
                    # Aggiunge valore/costo se disponibile
                    if hasattr(carta_esempio, 'valore'):
                        info_extra.append(f"{carta_esempio.valore} DP")
                    elif hasattr(carta_esempio, 'costo_destino'):
                        info_extra.append(f"{carta_esempio.costo_destino} DP")
                    
                    if info_extra:
                        riga_base += f" ({', '.join(info_extra)})"
                
                print(riga_base)
    
    # Riepilogo finale
    print(f"\n📊 TOTALE: {collezione.get_totale_carte()} carte")
    print(f"💰 Valore totale: {collezione.statistiche.valore_totale_dp} DP")

def organizza_inventario_per_tipo(collezione):
    """
    Organizza l'inventario per tipo di carta con informazioni dettagliate.
    
    Returns:
        Dict con struttura: {tipo_carta: {nome_carta: {quantita: int, esempi: [carta]}}}
    """
    inventario = defaultdict(lambda: defaultdict(lambda: {'quantita': 0, 'esempi': []}))
    
    # Itera su tutti i tipi di carte
    for tipo_carta, liste_carte in collezione.carte.items():
        for carta in liste_carte:
            nome_carta = carta.nome
            inventario[tipo_carta][nome_carta]['quantita'] += 1
            
            # Mantiene solo un esempio di ogni carta per le info
            if len(inventario[tipo_carta][nome_carta]['esempi']) < 1:
                inventario[tipo_carta][nome_carta]['esempi'].append(carta)
    
    return dict(inventario)

def stampa_statistiche_fazioni(collezione):
    """
    Stampa statistiche dettagliate per fazione nella collezione.
    
    Args:
        collezione: Oggetto CollezioneGiocatore
    """
    print(f"\n🏛️ STATISTICHE PER FAZIONE - GIOCATORE {collezione.id_giocatore}")
    print("=" * 70)
    
    # Analizza carte per fazione
    stats_fazioni = analizza_carte_per_fazione(collezione)
    
    if not stats_fazioni:
        print("Nessuna carta con fazione trovata.")
        return
    
    # Stampa statistiche per ogni fazione
    for fazione, info in sorted(stats_fazioni.items()):
        print(f"\n🏺 {fazione}:")
        print(f"   Totale carte: {info['totale_carte']}")
        print(f"   Guerrieri: {info['guerrieri']}")
        print(f"   Altre carte: {info['altre_carte']}")
        print(f"   Valore DP: {info['valore_dp']}")
        
        if info['carte_dettagli']:
            print(f"   Dettaglio carte:")
            for nome_carta, quantita in sorted(info['carte_dettagli'].items()):
                if quantita > 0:
                    print(f"     • {nome_carta} (x{quantita})")

def analizza_carte_per_fazione(collezione):
    """
    Analizza le carte della collezione organizzandole per fazione.
    
    Returns:
        Dict con statistiche per fazione
    """
    stats_fazioni = defaultdict(lambda: {
        'totale_carte': 0,
        'guerrieri': 0,
        'altre_carte': 0,
        'valore_dp': 0,
        'carte_dettagli': defaultdict(int)
    })
    
    # Analizza tutti i tipi di carte
    for tipo_carta, liste_carte in collezione.carte.items():
        for carta in liste_carte:
            if hasattr(carta, 'fazione') and carta.fazione:
                fazione_nome = carta.fazione.value if hasattr(carta.fazione, 'value') else str(carta.fazione)
                
                # Aggiorna contatori
                stats_fazioni[fazione_nome]['totale_carte'] += 1
                stats_fazioni[fazione_nome]['carte_dettagli'][carta.nome] += 1
                
                if tipo_carta == 'guerriero':
                    stats_fazioni[fazione_nome]['guerrieri'] += 1
                else:
                    stats_fazioni[fazione_nome]['altre_carte'] += 1
                
                # Aggiunge valore
                if hasattr(carta, 'valore'):
                    stats_fazioni[fazione_nome]['valore_dp'] += carta.valore
                elif hasattr(carta, 'costo_destino'):
                    stats_fazioni[fazione_nome]['valore_dp'] += carta.costo_destino
    
    return dict(stats_fazioni)

def stampa_riepilogo_collezioni_migliorato(collezioni: List):
    """
    Stampa un riepilogo migliorato delle collezioni con inventari dettagliati.
    
    Args:
        collezioni: Lista di oggetti CollezioneGiocatore
    """
    print(f"\n{'='*80}")
    print(f"📋 RIEPILOGO DETTAGLIATO {len(collezioni)} COLLEZIONI GIOCATORI")
    print(f"{'='*80}")
    
    # Riepilogo compatto iniziale
    print(f"\n📊 PANORAMICA GENERALE:")
    print("-" * 50)
    
    totale_carte = 0
    totale_valore = 0
    
    for collezione in collezioni:
        carte_collezione = collezione.get_totale_carte()
        valore_collezione = collezione.statistiche.valore_totale_dp
        
        totale_carte += carte_collezione
        totale_valore += valore_collezione
        
        orientamento_str = ""
        if collezione.fazioni_orientamento:
            fazioni = [f.value if hasattr(f, 'value') else str(f) for f in collezione.fazioni_orientamento]
            orientamento_str = f" [🎯 {', '.join(fazioni)}]"
        
        print(f"  🎮 Giocatore {collezione.id_giocatore}: {carte_collezione} carte, {valore_collezione} DP{orientamento_str}")
    
    print(f"\n💯 STATISTICHE AGGREGATE:")
    print(f"   📦 Totale carte: {totale_carte}")
    print(f"   💰 Valore totale: {totale_valore} DP")
    print(f"   📈 Media carte/giocatore: {totale_carte / len(collezioni):.1f}")
    print(f"   💎 Media valore/giocatore: {totale_valore / len(collezioni):.1f} DP")
    
    # Inventari dettagliati per ogni collezione
    for collezione in collezioni:
        stampa_inventario_dettagliato(collezione)
        
        # Opzionale: statistiche fazioni solo se ci sono guerrieri
        if collezione.statistiche.guerrieri > 0:
            stampa_statistiche_fazioni(collezione)

def cerca_carte_in_collezione(collezione, termine_ricerca: str):
    """
    Cerca carte nella collezione che contengono il termine specificato.
    
    Args:
        collezione: Oggetto CollezioneGiocatore  
        termine_ricerca: Termine da cercare nei nomi delle carte
    
    Returns:
        Lista di risultati con informazioni dettagliate
    """
    risultati = []
    termine_lower = termine_ricerca.lower()
    
    for tipo_carta, liste_carte in collezione.carte.items():
        for carta in liste_carte:
            if termine_lower in carta.nome.lower():
                info_carta = {
                    'nome': carta.nome,
                    'tipo': tipo_carta,
                    'quantita': collezione.inventario_quantita.get(carta.nome, 0)
                }
                
                # Aggiunge info specifiche per guerrieri
                if tipo_carta == 'guerriero' and hasattr(carta, 'fazione'):
                    fazione = carta.fazione.value if hasattr(carta.fazione, 'value') else str(carta.fazione)
                    info_carta['fazione'] = fazione
                
                # Evita duplicati
                if not any(r['nome'] == carta.nome for r in risultati):
                    risultati.append(info_carta)
    
    return risultati

# Esempio di utilizzo
def esempio_inventario_dettagliato():
    """
    Esempio di come utilizzare le funzioni di inventario dettagliato.
    Questa funzione dovrebbe essere chiamata dopo aver creato alcune collezioni.
    """
    print("\n🔍 ESEMPIO UTILIZZO INVENTARIO DETTAGLIATO")
    print("=" * 60)
    print("Per utilizzare queste funzioni:")
    print("1. Crea alcune collezioni usando creazione_Collezione_Giocatore()")
    print("2. Chiama stampa_riepilogo_collezioni_migliorato(collezioni)")
    print("3. Per collezioni singole: stampa_inventario_dettagliato(collezione)")
    print("4. Per cercare carte: cerca_carte_in_collezione(collezione, 'termine')")

#########################################################


######################################## SALVATAGGIO JSON 



# Serializzatore personalizzato per gestire enum
class EnumJSONEncoder(json.JSONEncoder):
    """Encoder JSON personalizzato per gestire enum e altri oggetti non serializzabili."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        elif hasattr(obj, 'value'):
            return obj.value
        return super().default(obj)

def converti_enum_ricorsivo(obj: Any) -> Any:
    """Converte ricorsivamente tutti gli enum nei loro valori stringa."""
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

def crea_inventario_dettagliato_json(collezione) -> Dict[str, Any]:
    """
    Crea l'inventario dettagliato per una collezione in formato JSON.
    Struttura analoga a stampa_inventario_dettagliato().
    """
    inventario_json = {
        'id_giocatore': collezione.id_giocatore,
        'orientamento': {
            'attivo': bool(collezione.fazioni_orientamento),
            'fazioni': []
        },
        'carte_per_tipo': {},
        'statistiche_fazioni': {},
        'totali': {
            'carte_totali': collezione.get_totale_carte(),
            'valore_totale_dp': collezione.statistiche.valore_totale_dp,
            'carte_uniche': 0
        }
    }
    
    # Orientamento
    if collezione.fazioni_orientamento:
        inventario_json['orientamento']['fazioni'] = [
            f.value if hasattr(f, 'value') else str(f) 
            for f in collezione.fazioni_orientamento
        ]
    
    # Organizza carte per tipo con dettagli completi
    carte_uniche_totali = set()
    
    for tipo_carta, liste_carte in collezione.carte.items():
        if not liste_carte:
            continue
            
        # Conta carte per nome
        carte_conteggio = defaultdict(int)
        carte_esempi = {}
        
        for carta in liste_carte:
            carte_conteggio[carta.nome] += 1
            if carta.nome not in carte_esempi:
                carte_esempi[carta.nome] = carta
            carte_uniche_totali.add(carta.nome)
        
        # Crea struttura per tipo carta
        tipo_info = {
            'totale_carte': len(liste_carte),
            'carte_uniche': len(carte_conteggio),
            'dettaglio_carte': {}
        }
        
        # Dettagli per ogni carta unica
        for nome_carta, quantita in carte_conteggio.items():
            carta_esempio = carte_esempi[nome_carta]
            
            dettaglio_carta = {
                'nome': nome_carta,
                'quantita': quantita,
                'tipo': tipo_carta.capitalize()
            }
            
            # Informazioni base della carta
            if hasattr(carta_esempio, 'rarity'):
                dettaglio_carta['rarity'] = (
                    carta_esempio.rarity.value if hasattr(carta_esempio.rarity, 'value') 
                    else str(carta_esempio.rarity)
                )
            
            if hasattr(carta_esempio, 'set_espansione'):
                dettaglio_carta['set_espansione'] = (
                    carta_esempio.set_espansione.value if hasattr(carta_esempio.set_espansione, 'value')
                    else str(carta_esempio.set_espansione)
                )
            
            # Valore DP
            if hasattr(carta_esempio, 'valore'):
                dettaglio_carta['valore_dp'] = carta_esempio.valore
            elif hasattr(carta_esempio, 'costo_destino'):
                dettaglio_carta['valore_dp'] = carta_esempio.costo_destino
            else:
                dettaglio_carta['valore_dp'] = 0
            
            # Informazioni specifiche per guerrieri
            if tipo_carta == 'guerriero' and hasattr(carta_esempio, 'fazione'):
                dettaglio_carta['fazione'] = (
                    carta_esempio.fazione.value if hasattr(carta_esempio.fazione, 'value')
                    else str(carta_esempio.fazione)
                )
                
                # Statistiche combattimento per guerrieri
                if hasattr(carta_esempio, 'stats'):
                    dettaglio_carta['statistiche'] = {
                        'combattimento': getattr(carta_esempio.stats, 'combattimento', 0),
                        'sparare': getattr(carta_esempio.stats, 'sparare', 0),
                        'armatura': getattr(carta_esempio.stats, 'armatura', 0),
                        'valore': getattr(carta_esempio.stats, 'valore', 0)
                    }
            
            # Altre informazioni specifiche per tipo
            if hasattr(carta_esempio, 'testo_carta'):
                dettaglio_carta['testo_carta'] = carta_esempio.testo_carta
            
            if hasattr(carta_esempio, 'keywords'):
                dettaglio_carta['keywords'] = carta_esempio.keywords
            
            tipo_info['dettaglio_carte'][nome_carta] = dettaglio_carta
        
        inventario_json['carte_per_tipo'][tipo_carta] = tipo_info
    
    # Totale carte uniche
    inventario_json['totali']['carte_uniche'] = len(carte_uniche_totali)
    
    # Statistiche per fazione (analoga a stampa_statistiche_fazioni)
    inventario_json['statistiche_fazioni'] = crea_statistiche_fazioni_json(collezione)
    
    return inventario_json

def crea_statistiche_fazioni_json(collezione) -> Dict[str, Any]:
    """
    Crea statistiche per fazione in formato JSON.
    Analoga a stampa_statistiche_fazioni().
    """
    stats_fazioni = {}
    
    # Analizza carte per fazione
    for tipo_carta, liste_carte in collezione.carte.items():
        for carta in liste_carte:
            if hasattr(carta, 'fazione') and carta.fazione:
                fazione_nome = (
                    carta.fazione.value if hasattr(carta.fazione, 'value') 
                    else str(carta.fazione)
                )
                
                if fazione_nome not in stats_fazioni:
                    stats_fazioni[fazione_nome] = {
                        'totale_carte': 0,
                        'guerrieri': 0,
                        'altre_carte': 0,
                        'valore_dp': 0,
                        'dettaglio_carte': defaultdict(int),
                        'tipi_carte': defaultdict(int)
                    }
                
                # Aggiorna contatori
                stats_fazioni[fazione_nome]['totale_carte'] += 1
                stats_fazioni[fazione_nome]['dettaglio_carte'][carta.nome] += 1
                stats_fazioni[fazione_nome]['tipi_carte'][tipo_carta] += 1
                
                if tipo_carta == 'guerriero':
                    stats_fazioni[fazione_nome]['guerrieri'] += 1
                else:
                    stats_fazioni[fazione_nome]['altre_carte'] += 1
                
                # Valore DP
                if hasattr(carta, 'valore'):
                    stats_fazioni[fazione_nome]['valore_dp'] += carta.valore
                elif hasattr(carta, 'costo_destino'):
                    stats_fazioni[fazione_nome]['valore_dp'] += carta.costo_destino
    
    # Converte defaultdict in dict normali
    for fazione_info in stats_fazioni.values():
        fazione_info['dettaglio_carte'] = dict(fazione_info['dettaglio_carte'])
        fazione_info['tipi_carte'] = dict(fazione_info['tipi_carte'])
    
    return stats_fazioni

def crea_statistiche_aggregate_json(collezioni: List) -> Dict[str, Any]:
    """
    Crea statistiche aggregate per tutte le collezioni.
    Analoga alla sezione "STATISTICHE AGGREGATE" di stampa_riepilogo_collezioni_migliorato().
    """
    totale_carte = sum(c.get_totale_carte() for c in collezioni)
    totale_valore = sum(c.statistiche.valore_totale_dp for c in collezioni)
    
    statistiche_aggregate = {
        'panoramica_generale': {
            'numero_collezioni': len(collezioni),
            'totale_carte': totale_carte,
            'totale_valore_dp': totale_valore,
            'media_carte_per_collezione': totale_carte / len(collezioni) if collezioni else 0,
            'media_valore_per_collezione': totale_valore / len(collezioni) if collezioni else 0
        },
        'riepilogo_collezioni': [],
        'distribuzione_orientamenti': defaultdict(int),
        'distribuzione_globale': {
            'per_tipo': defaultdict(int),
            'per_fazione': defaultdict(int),
            'per_rarity': defaultdict(int),
            'per_set': defaultdict(int)
        }
    }
    
    # Riepilogo per ogni collezione
    for collezione in collezioni:
        carte_collezione = collezione.get_totale_carte()
        valore_collezione = collezione.statistiche.valore_totale_dp
        
        orientamento_info = {
            'attivo': bool(collezione.fazioni_orientamento),
            'fazioni': []
        }
        
        if collezione.fazioni_orientamento:
            fazioni = [
                f.value if hasattr(f, 'value') else str(f) 
                for f in collezione.fazioni_orientamento
            ]
            orientamento_info['fazioni'] = fazioni
            
            # Conta orientamenti
            orientamento_key = ', '.join(sorted(fazioni))
            statistiche_aggregate['distribuzione_orientamenti'][orientamento_key] += 1
        else:
            statistiche_aggregate['distribuzione_orientamenti']['Nessun orientamento'] += 1
        
        collezione_summary = {
            'id_giocatore': collezione.id_giocatore,
            'totale_carte': carte_collezione,
            'valore_dp': valore_collezione,
            'orientamento': orientamento_info
        }
        
        statistiche_aggregate['riepilogo_collezioni'].append(collezione_summary)
        
        # Aggiorna distribuzioni globali
        for tipo_carta, count in collezione.statistiche.__dict__.items():
            if isinstance(count, int) and count > 0:
                if tipo_carta not in ['totale_carte', 'valore_totale_dp']:
                    statistiche_aggregate['distribuzione_globale']['per_tipo'][tipo_carta] += count
        
        # Distribuzioni da defaultdict
        for fazione, count in collezione.statistiche.per_fazione.items():
            statistiche_aggregate['distribuzione_globale']['per_fazione'][str(fazione)] += count
        
        for rarity, count in collezione.statistiche.per_rarity.items():
            statistiche_aggregate['distribuzione_globale']['per_rarity'][str(rarity)] += count
        
        for set_esp, count in collezione.statistiche.per_set.items():
            statistiche_aggregate['distribuzione_globale']['per_set'][str(set_esp)] += count
    
    # Converte defaultdict in dict
    statistiche_aggregate['distribuzione_orientamenti'] = dict(statistiche_aggregate['distribuzione_orientamenti'])
    for key in statistiche_aggregate['distribuzione_globale']:
        statistiche_aggregate['distribuzione_globale'][key] = dict(statistiche_aggregate['distribuzione_globale'][key])
    
    return statistiche_aggregate

def salva_collezioni_json_migliorato(collezioni: List, filename: str = "collezioni_dettagliate.json"):
    """
    Salva le collezioni in formato JSON con struttura dettagliata.
    Equivalente JSON di stampa_riepilogo_collezioni_migliorato().
    """
    try:
        print(f"🔄 Creazione struttura JSON dettagliata per {len(collezioni)} collezioni...")
        
        # Struttura principale del JSON
        dati_export = {
            'metadata': {
                'versione': '2.0',
                'tipo_export': 'collezioni_dettagliate',
                'data_creazione': datetime.now().isoformat(),
                'numero_collezioni': len(collezioni),
                'descrizione': 'Export dettagliato collezioni con inventari completi e statistiche per fazione'
            },
            'statistiche_aggregate': crea_statistiche_aggregate_json(collezioni),
            'collezioni_dettagliate': []
        }
        
        # Aggiunge ogni collezione con inventario dettagliato
        for i, collezione in enumerate(collezioni):
            print(f"  📦 Processando collezione {i+1}/{len(collezioni)}...")
            inventario_dettagliato = crea_inventario_dettagliato_json(collezione)
            dati_export['collezioni_dettagliate'].append(inventario_dettagliato)
        
        # Converte enum ricorsivamente
        print("🔄 Conversione enum per compatibilità JSON...")
        dati_puliti = converti_enum_ricorsivo(dati_export)
        
        # Salva il file
        print(f"💾 Salvando in {PERCORSO_SALVATAGGIO+filename}...")
        with open(PERCORSO_SALVATAGGIO + filename, 'w', encoding='utf-8') as f:
            json.dump(dati_puliti, f, indent=2, ensure_ascii=False, cls=EnumJSONEncoder)
        
        # Statistiche del file salvato
        import os
        dimensione_file = os.path.getsize(PERCORSO_SALVATAGGIO + filename) / 1024  # KB
        
        print(f"✅ Collezioni salvate con successo!")
        print(f"   📄 File: {filename}")
        print(f"   📊 Dimensione: {dimensione_file:.1f} KB")
        print(f"   🎮 Collezioni: {len(collezioni)}")
        print(f"   📦 Carte totali: {sum(c.get_totale_carte() for c in collezioni)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante il salvataggio JSON: {e}")
        
        # Salvataggio di debug
        try:
            debug_filename = filename.replace('.json', '_debug.txt')
            with open(PERCORSO_SALVATAGGIO + debug_filename, 'w', encoding='utf-8') as f:
                f.write(f"Errore durante serializzazione JSON: {e}\n\n")
                f.write(f"Numero collezioni: {len(collezioni)}\n")
                for i, c in enumerate(collezioni):
                    f.write(f"Collezione {i}: ID {c.id_giocatore} - {c.get_totale_carte()} carte\n")
            print(f"📄 File di debug salvato in {debug_filename}")
        except Exception as debug_error:
            print(f"❌ Errore anche nel debug: {debug_error}")
        
        return False

def carica_collezioni_json_migliorato(filename: str) -> Optional[Dict[str, Any]]:
    """
    Carica collezioni dal formato JSON migliorato.
    """
    try:
        print(f"📂 Caricamento collezioni da {PERCORSO_SALVATAGGIO+filename}...")
        
        with open(PERCORSO_SALVATAGGIO + filename, 'r', encoding='utf-8') as f:
            dati = json.load(f)
        
        # Verifica formato
        if 'metadata' not in dati or dati.get('metadata', {}).get('tipo_export') != 'collezioni_dettagliate':
            print("⚠️  Attenzione: File potrebbe non essere in formato dettagliato")
        
        # Stampa info di caricamento
        metadata = dati.get('metadata', {})
        print(f"✅ Caricamento completato!")
        print(f"   📅 Creato: {metadata.get('data_creazione', 'N/A')}")
        print(f"   🎮 Collezioni: {metadata.get('numero_collezioni', 'N/A')}")
        print(f"   📦 Carte totali: {dati.get('statistiche_aggregate', {}).get('panoramica_generale', {}).get('totale_carte', 'N/A')}")
        
        return dati
        
    except FileNotFoundError:
        print(f"❌ File {PERCORSO_SALVATAGGIO+filename} non trovato!")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Errore nel parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"❌ Errore durante il caricamento: {e}")
        return None

def stampa_statistiche_da_json(dati_json: Dict[str, Any]):
    """
    Stampa statistiche dalle collezioni caricate da JSON.
    Equivalente di stampa_riepilogo_collezioni_migliorato() per dati JSON.
    """
    if not dati_json:
        print("❌ Nessun dato da visualizzare")
        return
    
    stats_aggregate = dati_json.get('statistiche_aggregate', {})
    panoramica = stats_aggregate.get('panoramica_generale', {})
    
    print(f"\n{'='*80}")
    print(f"📋 STATISTICHE DA JSON - {panoramica.get('numero_collezioni', 0)} COLLEZIONI")
    print(f"{'='*80}")
    
    print(f"📦 Totale carte: {panoramica.get('totale_carte', 0)}")
    print(f"💰 Valore totale: {panoramica.get('totale_valore_dp', 0)} DP")
    print(f"📈 Media carte/collezione: {panoramica.get('media_carte_per_collezione', 0):.1f}")
    print(f"💎 Media valore/collezione: {panoramica.get('media_valore_per_collezione', 0):.1f} DP")
    
    # Riepilogo collezioni
    print(f"\n📊 RIEPILOGO COLLEZIONI:")
    for collezione in stats_aggregate.get('riepilogo_collezioni', []):
        orientamento_str = ""
        if collezione.get('orientamento', {}).get('attivo'):
            fazioni = collezione.get('orientamento', {}).get('fazioni', [])
            orientamento_str = f" [🎯 {', '.join(fazioni)}]"
        
        print(f"  🎮 Giocatore {collezione.get('id_giocatore')}: {collezione.get('totale_carte')} carte, {collezione.get('valore_dp')} DP{orientamento_str}")

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


# ==================== ESEMPI E TEST PER COLLEZIONE GIOCATORE ====================

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
    
    stampa_riepilogo_collezioni_migliorato(collezioni)
    
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
    
    stampa_riepilogo_collezioni_migliorato(collezioni)
    
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
    
    stampa_riepilogo_collezioni_migliorato(collezioni)
    
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
        
        stampa_riepilogo_collezioni_migliorato(collezioni)
        
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

# Esempio di utilizzo
def esempio_salvataggio_migliorato():
    """
    Esempio di utilizzo delle funzioni di salvataggio migliorato.
    """
    print("\n🔍 ESEMPIO SALVATAGGIO JSON MIGLIORATO")
    print("=" * 60)
    print("1. Crea collezioni: collezioni = creazione_Collezione_Giocatore(...)")
    # Crea collezioni
    collezioni = creazione_Collezione_Giocatore(
            numero_giocatori=2,
            espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
            orientamento=True
        )
    # Stampa con visualizzazione migliorata
    stampa_riepilogo_collezioni_migliorato(collezioni)
    print("2. Salva dettagliato: salva_collezioni_json_migliorato(collezioni, 'collezioni_dettagliate.json')")
    # Salva con la STESSA struttura in JSON
    salva_collezioni_json_migliorato(collezioni, "collezioni_dettagliate.json")
    print("3. Carica: dati = carica_collezioni_json_migliorato('collezioni_dettagliate.json')")
    dati_json = carica_collezioni_json_migliorato("collezioni_dettagliate.json")
    print("4. Visualizza: stampa_statistiche_da_json(dati)")
    stampa_statistiche_da_json(dati_json)

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
    stampa_riepilogo_collezioni_migliorato(collezioni_torneo)
    
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
        print("9. Carica collezioni da JSON")
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
                stampa_riepilogo_collezioni_migliorato(collezioni)
                
                salva = input("Salvare in JSON? (s/n): ").lower().startswith('s')
                if salva:
                    filename = f"collezioni_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    salva_collezioni_json_migliorato(collezioni, filename)
                
            except Exception as e:
                print(f"Errore: {e}")
        elif scelta == "8":
            resetta_tracciamento_quantita()
            print("Tracciamento quantità resettato.")
        elif scelta == "9":
            try:
                num = str(input("nome file collezione: "))
                carica_collezioni_json_migliorato(num)
            except Exception as e:
                print(f"Errore: {e}")

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
    


################################ CREAZIONE MAZZO #################################################

"""
Manager_Gioco.py - Funzione per la creazione automatica di mazzi da collezione
Versione completa con tutti i criteri di selezione richiesti
"""



# ================================================================================
# COSTANTI PER LA DISTRIBUZIONE DEL TIPO DI CARTE NEL MAZZO
# ================================================================================

DISTRIBUZIONE_BASE = {
    'guerriero': (0.19, 0.24),          # 19-24%
    'equipaggiamento': (0.11, 0.16),    # 11-16%
    'speciale': (0.42, 0.47),           # 42-47%
    'oscura_simmetria': (0.09, 0.14),   # 9-14%
    'arte': (0.09, 0.14),               # 9-14%
    'reliquia': (0.05, 0.07),           # 5-7%
    'warzone': (0.05, 0.08),            # 5-8%
    'missione': 2                       # max 2 carte (numero fisso)
}

# Ridistribuzione quando Oscura Simmetria e/o Arte non sono utilizzate
RIDISTRIBUZIONE_PERCENTUALE = {
    'equipaggiamento': 0.40,  # 40% della percentuale mancante
    'speciale': 0.40,         # 40% della percentuale mancante
    'reliquia': 0.20          # 20% della percentuale mancante
}

# Fazioni Doomtrooper e Oscura Legione
FAZIONI_DOOMTROOPER = [
    Fazione.IMPERIALE, 
    Fazione.CAPITOL, 
    Fazione.MISHIMA,
    Fazione.BAUHAUS, 
    Fazione.CYBERTRONIC, 
    Fazione.FREELANCER
]

FAZIONI_FRATELLANZA = [Fazione.FRATELLANZA]
FAZIONI_OSCURA_LEGIONE = [Fazione.OSCURA_LEGIONE]

# ================================================================================
# CLASSE PRINCIPALE PER LA CREAZIONE DEL MAZZO
# ================================================================================

class CreatoreMazzo:
    """Classe per gestire la creazione del mazzo da collezione"""
    
    def __init__(self, collezione):
        """
        Inizializza il creatore del mazzo
        
        Args:
            collezione: Oggetto CollezioneGiocatore
        """
        self.collezione = collezione
        self.mazzo = {
            'squadra': [],      # Guerrieri Doomtrooper e Fratellanza
            'schieramento': [], # Guerrieri Oscura Legione
            'supporto': []      # Altre carte (Equipaggiamenti, Speciali, etc.)
        }
        self.carte_selezionate = defaultdict(int)  # Traccia carte già selezionate
        self.potenze_calcolate = {}  # Cache per i calcoli di potenza
        
    def calcola_potenza_guerriero(self, guerriero: Guerriero) -> float:
        """
        Calcola la potenza relativa di un guerriero
        
        Args:
            guerriero: Oggetto Guerriero
            
        Returns:
            float: Potenza relativa del guerriero (0-1)
        """
        if guerriero.nome in self.potenze_calcolate:
            return self.potenze_calcolate[guerriero.nome]
            
        # Calcola potenza assoluta
        combattimento = guerriero.stats.get('combattimento', 0)
        sparo = guerriero.stats.get('sparare', 0)
        armatura = guerriero.stats.get('armatura', 0)
        valore = guerriero.stats.get('valore', 1)
        
        if valore == 0:
            valore = 1  # Evita divisione per zero
            
        potenza_assoluta = ((combattimento + sparo + armatura) * 1.5) / valore
        
        # Bonus per abilità speciali
        for abilita in guerriero.abilita:
            # Potenziamento altri guerrieri
            if any(keyword in abilita.get('descrizione', '').lower() 
                   for keyword in ['tutti i guerrieri', 'alleati', 'guadagnano', '+1', '+2', '+3']):
                potenza_assoluta *= 1.3
                
            # Uccisione automatica
            if any(keyword in abilita.get('descrizione', '').lower() 
                   for keyword in ['uccide', 'elimina', 'distrugge', 'automaticamente']):
                potenza_assoluta *= 2.0
        
        # Normalizza rispetto al massimo della collezione
        max_potenza = self._calcola_max_potenza_guerrieri()
        if max_potenza > 0:
            potenza_relativa = potenza_assoluta / max_potenza
        else:
            potenza_relativa = 0.5
            
        self.potenze_calcolate[guerriero.nome] = min(potenza_relativa, 1.0)
        return self.potenze_calcolate[guerriero.nome]
    
    def _calcola_max_potenza_guerrieri(self) -> float:
        """Calcola la potenza massima tra tutti i guerrieri della collezione"""
        max_potenza = 0
        
        for guerriero in self.collezione.get_carte_per_tipo('guerriero'):
            combattimento = guerriero.stats.get('combattimento', 0)
            sparo = guerriero.stats.get('sparare', 0)
            armatura = guerriero.stats.get('armatura', 0)
            valore = guerriero.stats.get('valore', 1)
            
            if valore == 0:
                valore = 1
                
            potenza_assoluta = ((combattimento + sparo + armatura) * 1.5) / valore
            max_potenza = max(max_potenza, potenza_assoluta)
            
        return max_potenza
    
    def calcola_potenza_equipaggiamento(self, equipaggiamento: Equipaggiamento) -> float:
        """
        Calcola la potenza relativa di un equipaggiamento
        
        Args:
            equipaggiamento: Oggetto Equipaggiamento
            
        Returns:
            float: Potenza relativa (0-1)
        """
        potenza = 0
        
        # Somma modificatori statistiche
        for modifica in equipaggiamento.modifiche_guerriero:
            if modifica['tipo'] in ['combattimento', 'sparare', 'armatura']:
                potenza += abs(modifica['valore'])
        
        # Bonus per effetti speciali
        if hasattr(equipaggiamento, 'effetti_speciali'):
            for effetto in equipaggiamento.effetti_speciali:
                desc = effetto.get('descrizione', '').lower()
                if 'ferisce' in desc and 'automaticamente' in desc:
                    potenza *= 1.4
                elif 'uccide' in desc and 'automaticamente' in desc:
                    potenza *= 2.0
        
        # Se non influenza l'armatura
        influenza_armatura = any(m['tipo'] == 'armatura' for m in equipaggiamento.modifiche_guerriero)
        if not influenza_armatura:
            potenza = 0.5
        
        # Normalizza
        max_potenza = self._calcola_max_potenza_equipaggiamenti()
        if max_potenza > 0:
            return min(potenza / max_potenza, 1.0)
        return 0.5
    
    def _calcola_max_potenza_equipaggiamenti(self) -> float:
        """Calcola la potenza massima tra tutti gli equipaggiamenti"""
        max_potenza = 0
        
        for equip in self.collezione.get_carte_per_tipo('equipaggiamento'):
            potenza = sum(abs(m['valore']) for m in equip.modifiche_guerriero 
                         if m['tipo'] in ['combattimento', 'sparare', 'armatura'])
            max_potenza = max(max_potenza, potenza)
            
        return max_potenza
    
    def calcola_potenza_fortificazione(self, fortificazione: Fortificazione) -> float:
        """
        Calcola la potenza relativa di una fortificazione
        
        Args:
            fortificazione: Oggetto Fortificazione
            
        Returns:
            float: Potenza relativa (0-1)
        """
        armatura = fortificazione.bonus_armatura
        
        # Se ha valori differenziati, prendi il minore
        if hasattr(fortificazione, 'bonus_differenziati'):
            armatura = min(fortificazione.bonus_differenziati.values())
        
        # Se non influenza l'armatura
        if armatura == 0:
            return 0.5
        
        # Normalizza
        max_potenza = self._calcola_max_potenza_fortificazioni()
        if max_potenza > 0:
            return min(armatura / max_potenza, 1.0)
        return 0.5
    
    def _calcola_max_potenza_fortificazioni(self) -> float:
        """Calcola la potenza massima tra tutte le fortificazioni"""
        max_armatura = 0
        
        for fort in self.collezione.get_carte_per_tipo('fortificazione'):
            max_armatura = max(max_armatura, fort.bonus_armatura)
            
        return max_armatura
    
    def calcola_potenza_arte(self, arte: Arte) -> float:
        """
        Calcola la potenza relativa di una carta Arte
        
        Args:
            arte: Oggetto Arte
            
        Returns:
            float: Potenza relativa (0-1)
        """
        potenza = 0
        
        # Analizza effetti
        for effetto in arte.effetti:
            # Modificatori statistiche
            if effetto.tipo_effetto == "Modificatore":
                potenza += abs(effetto.valore)
            
            desc = effetto.descrizione.lower()
            
            # Effetti speciali
            if 'ferisce' in desc and 'automaticamente' in desc:
                potenza *= 1.4
            elif 'uccide' in desc:
                potenza *= 2.0
            elif 'scarta' in desc and 'guerriero' in desc:
                potenza = 1.5
            elif 'scarta' in desc and any(x in desc for x in ['equipaggiamento', 'fortificazione', 'reliquia', 'warzone']):
                potenza = 1.0
        
        # Default per effetti non contemplati
        if potenza == 0:
            potenza = 0.5
        
        # Normalizza
        max_potenza = self._calcola_max_potenza_arte()
        if max_potenza > 0:
            return min(potenza / max_potenza, 1.0)
        return 0.5
    
    def _calcola_max_potenza_arte(self) -> float:
        """Calcola la potenza massima tra tutte le carte Arte"""
        max_potenza = 0
        
        for arte in self.collezione.get_carte_per_tipo('arte'):
            potenza = sum(abs(e.valore) for e in arte.effetti if e.tipo_effetto == "Modificatore")
            max_potenza = max(max_potenza, potenza)
            
        return max_potenza if max_potenza > 0 else 1.0
    
    def calcola_potenza_oscura_simmetria(self, oscura: Oscura_Simmetria) -> float:
        """
        Calcola la potenza relativa di una carta Oscura Simmetria
        
        Args:
            oscura: Oggetto Oscura_Simmetria
            
        Returns:
            float: Potenza relativa (0-1)
        """
        potenza = 0
        
        # Analizza effetti
        for effetto in oscura.effetti:
            # Modificatori statistiche
            if hasattr(effetto, 'valore'):
                potenza += abs(effetto.valore)
            
            desc = effetto.descrizione_effetto.lower() if hasattr(effetto, 'descrizione_effetto') else ""
            
            # Effetti speciali
            if 'ferisce' in desc and 'automaticamente' in desc:
                potenza *= 1.4
            elif 'uccide' in desc:
                potenza *= 2.0
            elif 'scarta' in desc and 'guerriero' in desc:
                potenza = 1.5
            elif 'scarta' in desc:
                potenza = 1.0
        
        # Default per effetti non contemplati
        if potenza == 0:
            potenza = 0.5
        
        # Normalizza
        max_potenza = self._calcola_max_potenza_oscura_simmetria()
        if max_potenza > 0:
            return min(potenza / max_potenza, 1.0)
        return 0.5
    
    def _calcola_max_potenza_oscura_simmetria(self) -> float:
        """Calcola la potenza massima tra tutte le carte Oscura Simmetria"""
        max_potenza = 0
        
        for oscura in self.collezione.get_carte_per_tipo('oscura_simmetria'):
            potenza = sum(abs(e.valore) for e in oscura.effetti if hasattr(e, 'valore'))
            max_potenza = max(max_potenza, potenza)
            
        return max_potenza if max_potenza > 0 else 1.0
    
    def calcola_potenza_reliquia(self, reliquia: Reliquia) -> float:
        """
        Calcola la potenza relativa di una reliquia
        
        Args:
            reliquia: Oggetto Reliquia
            
        Returns:
            float: Potenza relativa (0-1)
        """
        potenza = 0
        
        # Somma modificatori statistiche
        if hasattr(reliquia, 'modifiche_guerriero'):
            for modifica in reliquia.modifiche_guerriero:
                if modifica['tipo'] in ['combattimento', 'sparare', 'armatura']:
                    potenza += abs(modifica['valore'])
        
        # Bonus per effetti speciali
        if hasattr(reliquia, 'effetti_speciali'):
            for effetto in reliquia.effetti_speciali:
                desc = effetto.get('descrizione', '').lower()
                if 'ferisce' in desc and 'automaticamente' in desc:
                    potenza *= 1.4
                elif 'uccide' in desc:
                    potenza *= 2.0
        
        # Se non influenza le statistiche base
        if potenza == 0:
            potenza = 0.5
        
        # Normalizza
        max_potenza = self._calcola_max_potenza_reliquie()
        if max_potenza > 0:
            return min(potenza / max_potenza, 1.0)
        return 0.5
    
    def _calcola_max_potenza_reliquie(self) -> float:
        """Calcola la potenza massima tra tutte le reliquie"""
        max_potenza = 0
        
        for reliquia in self.collezione.get_carte_per_tipo('reliquia'):
            if hasattr(reliquia, 'modifiche_guerriero'):
                potenza = sum(abs(m['valore']) for m in reliquia.modifiche_guerriero 
                             if m['tipo'] in ['combattimento', 'sparare', 'armatura'])
                max_potenza = max(max_potenza, potenza)
                
        return max_potenza if max_potenza > 0 else 1.0
    
    def calcola_potenza_warzone(self, warzone: Warzone) -> float:
        """
        Calcola la potenza relativa di una warzone
        
        Args:
            warzone: Oggetto Warzone
            
        Returns:
            float: Potenza relativa (0-1)
        """
        # Statistiche base della warzone
        combattimento = warzone.stats_difensori.get('combattimento', 0)
        sparo = warzone.stats_difensori.get('sparare', 0)
        armatura = warzone.stats_difensori.get('armatura', 0)
        
        potenza = combattimento + sparo + armatura
        
        # Bonus per fazioni/tipi specifici
        if hasattr(warzone, 'bonus_fazioni'):
            for bonus in warzone.bonus_fazioni.values():
                potenza += sum([bonus.get('combattimento', 0), 
                               bonus.get('sparare', 0), 
                               bonus.get('armatura', 0)])
        
        # Bonus per uccisione automatica
        if hasattr(warzone, 'effetti_combattimento'):
            for effetto in warzone.effetti_combattimento:
                if 'uccide' in effetto.descrizione.lower() and 'automaticamente' in effetto.descrizione.lower():
                    potenza *= 2.0
        
        # Default per warzone con effetti diversi
        if potenza == 0:
            potenza = 0.5
        
        # Normalizza
        max_potenza = self._calcola_max_potenza_warzone()
        if max_potenza > 0:
            return min(potenza / max_potenza, 1.0)
        return 0.5
    
    def _calcola_max_potenza_warzone(self) -> float:
        """Calcola la potenza massima tra tutte le warzone"""
        max_potenza = 0
        
        for warzone in self.collezione.get_carte_per_tipo('warzone'):
            potenza = (warzone.stats_difensori.get('combattimento', 0) + 
                      warzone.stats_difensori.get('sparare', 0) + 
                      warzone.stats_difensori.get('armatura', 0))
            max_potenza = max(max_potenza, potenza)
            
        return max_potenza if max_potenza > 0 else 1.0
    
    def filtra_carte_per_espansioni(self, carte: List[Any], espansioni_richieste: List[str]) -> List[Any]:
        """
        Filtra le carte per le espansioni richieste
        
        Args:
            carte: Lista di carte da filtrare
            espansioni_richieste: Lista delle espansioni richieste
            
        Returns:
            Lista di carte filtrate
        """
        if not espansioni_richieste:
            return carte
            
        carte_filtrate = []
        for carta in carte:
            if hasattr(carta, 'set_espansione'):
                set_carta = carta.set_espansione
                if hasattr(set_carta, 'value'):
                    set_carta = set_carta.value
                    
                if set_carta in espansioni_richieste:
                    carte_filtrate.append(carta)
                    
        return carte_filtrate
    
    def seleziona_guerrieri(self, 
                           espansioni_richieste: List[str],
                           orientamento_doomtrooper: List[str] = None,
                           orientamento_arte: List[str] = None,
                           orientamento_apostolo: List[str] = None,
                           orientamento_eretico: bool = False,
                           numero_guerrieri_target: int = 20) -> Tuple[List[Guerriero], List[Guerriero]]:
        """
        Seleziona i guerrieri per squadra e schieramento
        
        Args:
            espansioni_richieste: Lista espansioni richieste
            orientamento_doomtrooper: Fazioni Doomtrooper preferite
            orientamento_arte: Discipline arte preferite
            orientamento_apostolo: Apostoli preferiti
            orientamento_eretico: Se True, preferisce eretici
            numero_guerrieri_target: Numero target di guerrieri da selezionare
            
        Returns:
            Tupla (squadra, schieramento)
        """
        # Ottieni tutti i guerrieri disponibili e filtrali per espansione
        tutti_guerrieri = self.collezione.get_carte_per_tipo('guerriero')
        guerrieri_disponibili = self.filtra_carte_per_espansioni(tutti_guerrieri, espansioni_richieste)
        
        if not guerrieri_disponibili:
            return [], []
        
        # Separa guerrieri per categoria
        guerrieri_doomtrooper = []
        guerrieri_fratellanza = []
        guerrieri_oscura_legione = []
        guerrieri_eretici = []
        guerrieri_cultisti = []
        
        for guerriero in guerrieri_disponibili:
            # Controlla se è eretico
            if hasattr(guerriero, 'keywords') and 'Eretico' in guerriero.keywords:
                guerrieri_eretici.append(guerriero)
            
            # Controlla se è cultista (può essere sia Doomtrooper che Oscura Legione)
            if hasattr(guerriero, 'keywords'):
                for keyword in guerriero.keywords:
                    if 'Cultista di' in keyword:
                        guerrieri_cultisti.append(guerriero)
                        break
            
            # Categorizza per fazione
            if guerriero.fazione in FAZIONI_DOOMTROOPER:
                guerrieri_doomtrooper.append(guerriero)
            elif guerriero.fazione in FAZIONI_FRATELLANZA:
                guerrieri_fratellanza.append(guerriero)
            elif guerriero.fazione in FAZIONI_OSCURA_LEGIONE:
                guerrieri_oscura_legione.append(guerriero)
        
        # Calcola punteggi per ogni guerriero basati sugli orientamenti
        punteggi = {}
        
        for guerriero in guerrieri_disponibili:
            punteggio = self.calcola_potenza_guerriero(guerriero)
            
            # Bonus per orientamenti
            bonus_moltiplicatore = 1.0
            
            # Orientamento Doomtrooper
            if orientamento_doomtrooper and guerriero.fazione in FAZIONI_DOOMTROOPER:
                fazione_nome = guerriero.fazione.value if hasattr(guerriero.fazione, 'value') else str(guerriero.fazione)
                if fazione_nome in orientamento_doomtrooper:
                    bonus_moltiplicatore *= 2.0
            
            # Orientamento Arte (per guerrieri Fratellanza)
            if orientamento_arte and guerriero.fazione in FAZIONI_FRATELLANZA:
                for abilita in guerriero.abilita:
                    if abilita.get('tipo') == 'Arte':
                        disciplina = abilita.get('nome', '')
                        if disciplina in orientamento_arte or disciplina == DisciplinaArte.TUTTE.value:
                            bonus_moltiplicatore *= 2.0
                            break
            
            # Orientamento Apostolo (per guerrieri Oscura Legione)
            if orientamento_apostolo and guerriero.fazione in FAZIONI_OSCURA_LEGIONE:
                for apostolo in orientamento_apostolo:
                    if f"Seguace di {apostolo}" in guerriero.keywords:
                        bonus_moltiplicatore *= 2.0
                        break
            
            # Orientamento Eretico
            if orientamento_eretico and 'Eretico' in guerriero.keywords:
                bonus_moltiplicatore *= 2.0
            
            # Bonus per carte fondamentali
            if hasattr(guerriero, 'fondamentale') and guerriero.fondamentale:
                bonus_moltiplicatore *= 10.0  # Priorità massima
            
            punteggi[guerriero.nome] = punteggio * bonus_moltiplicatore
        
        # Ordina guerrieri per punteggio
        guerrieri_ordinati = sorted(guerrieri_disponibili, 
                                   key=lambda g: punteggi.get(g.nome, 0), 
                                   reverse=True)
        
        # Seleziona guerrieri garantendo distribuzione equa
        squadra = []
        schieramento = []
        
        # Prima seleziona le carte fondamentali
        for guerriero in guerrieri_ordinati:
            if hasattr(guerriero, 'fondamentale') and guerriero.fondamentale:
                quantita_richiesta = min(
                    getattr(guerriero, 'quantita_minima_consigliata', 1),
                    getattr(guerriero, 'quantita', 1)
                )
                
                for _ in range(quantita_richiesta):
                    if guerriero.fazione in FAZIONI_OSCURA_LEGIONE:
                        schieramento.append(guerriero)
                    else:
                        squadra.append(guerriero)
        
        # Poi seleziona gli altri guerrieri
        for guerriero in guerrieri_ordinati:
            if len(squadra) + len(schieramento) >= numero_guerrieri_target:
                break
                
            # Skip se già aggiunto come fondamentale
            if hasattr(guerriero, 'fondamentale') and guerriero.fondamentale:
                continue
            
            # Calcola quantità da aggiungere
            potenza = self.calcola_potenza_guerriero(guerriero)
            quantita_disponibile = getattr(guerriero, 'quantita', 1)
            quantita_consigliata = getattr(guerriero, 'quantita_minima_consigliata', 1)
            
            # Calcola numero di copie basato sulla potenza
            if potenza > 0.8:
                num_copie = min(5, quantita_disponibile, quantita_consigliata + 2)
            elif potenza > 0.5:
                num_copie = min(3, quantita_disponibile, quantita_consigliata)
            else:
                num_copie = min(1, quantita_disponibile)
            
            # Aggiungi con un po' di casualità
            num_copie = random.randint(1, num_copie)
            
            for _ in range(num_copie):
                if guerriero.fazione in FAZIONI_OSCURA_LEGIONE:
                    if len(schieramento) < numero_guerrieri_target // 3:  # ~33% Oscura Legione
                        schieramento.append(guerriero)
                else:
                    if len(squadra) < (numero_guerrieri_target * 2) // 3:  # ~67% Doomtrooper/Fratellanza
                        squadra.append(guerriero)
        
        return squadra, schieramento
    
    def seleziona_carte_supporto(self, 
                                squadra: List[Guerriero],
                                schieramento: List[Guerriero],
                                espansioni_richieste: List[str],
                                tipo_carta: str,
                                numero_carte: int) -> List[Any]:
        """
        Seleziona carte di supporto (Equipaggiamento, Speciale, etc.)
        
        Args:
            squadra: Guerrieri nella squadra
            schieramento: Guerrieri nello schieramento
            espansioni_richieste: Espansioni richieste
            tipo_carta: Tipo di carta da selezionare
            numero_carte: Numero di carte da selezionare
            
        Returns:
            Lista di carte selezionate
        """
        # Ottieni tutte le carte del tipo richiesto
        tutte_carte = self.collezione.get_carte_per_tipo(tipo_carta)
        carte_disponibili = self.filtra_carte_per_espansioni(tutte_carte, espansioni_richieste)
        
        if not carte_disponibili:
            return []
        
        carte_selezionate = []
        tutti_guerrieri = squadra + schieramento
        
        # Prima seleziona carte fondamentali
        for carta in carte_disponibili:
            if hasattr(carta, 'fondamentale') and carta.fondamentale:
                # Verifica compatibilità con i guerrieri
                if self._carta_compatibile_con_guerrieri(carta, tutti_guerrieri):
                    quantita_richiesta = min(
                        getattr(carta, 'quantita_minima_consigliata', 1),
                        getattr(carta, 'quantita', 1)
                    )
                    
                    for _ in range(quantita_richiesta):
                        carte_selezionate.append(carta)
        
        # Calcola potenza per ogni carta
        carte_con_punteggio = []
        
        for carta in carte_disponibili:
            # Skip carte fondamentali già aggiunte
            if hasattr(carta, 'fondamentale') and carta.fondamentale:
                continue
            
            # Verifica compatibilità
            if not self._carta_compatibile_con_guerrieri(carta, tutti_guerrieri):
                continue
            
            # Calcola potenza basata sul tipo
            if tipo_carta == 'equipaggiamento':
                potenza = self.calcola_potenza_equipaggiamento(carta)
            elif tipo_carta == 'fortificazione':
                potenza = self.calcola_potenza_fortificazione(carta)
            elif tipo_carta == 'arte':
                potenza = self.calcola_potenza_arte(carta)
            elif tipo_carta == 'oscura_simmetria':
                potenza = self.calcola_potenza_oscura_simmetria(carta)
            elif tipo_carta == 'reliquia':
                potenza = self.calcola_potenza_reliquia(carta)
            elif tipo_carta == 'warzone':
                potenza = self.calcola_potenza_warzone(carta)
            elif tipo_carta == 'speciale':
                potenza = 0.5  # Default per carte speciali
            elif tipo_carta == 'missione':
                potenza = 0.5  # Default per missioni
            else:
                potenza = 0.5
            
            carte_con_punteggio.append((carta, potenza))
        
        # Ordina per potenza
        carte_con_punteggio.sort(key=lambda x: x[1], reverse=True)
        
        # Seleziona carte
        for carta, potenza in carte_con_punteggio:
            if len(carte_selezionate) >= numero_carte:
                break
            
            # Calcola numero di copie
            quantita_disponibile = getattr(carta, 'quantita', 1)
            quantita_consigliata = getattr(carta, 'quantita_minima_consigliata', 1)
            
            if potenza > 0.7:
                num_copie = min(5, quantita_disponibile, quantita_consigliata + 1)
            elif potenza > 0.4:
                num_copie = min(3, quantita_disponibile, quantita_consigliata)
            else:
                num_copie = min(1, quantita_disponibile)
            
            # Aggiungi casualità
            num_copie = random.randint(1, min(num_copie, numero_carte - len(carte_selezionate)))
            
            for _ in range(num_copie):
                if len(carte_selezionate) < numero_carte:
                    carte_selezionate.append(carta)
        
        return carte_selezionate
    
    def _carta_compatibile_con_guerrieri(self, carta: Any, guerrieri: List[Guerriero]) -> bool:
        """
        Verifica se una carta è compatibile con i guerrieri nel mazzo
        
        Args:
            carta: Carta da verificare
            guerrieri: Lista dei guerrieri nel mazzo
            
        Returns:
            True se compatibile, False altrimenti
        """
        if not guerrieri:
            return False
        
        tipo_carta = type(carta).__name__.lower()
        
        # Verifica compatibilità per tipo
        if tipo_carta == 'arte':
            # Verifica se ci sono guerrieri che possono lanciare l'arte
            for guerriero in guerrieri:
                if hasattr(carta, 'puo_essere_associata_a_guerriero'):
                    risultato = carta.puo_essere_associata_a_guerriero(guerriero)
                    if risultato.get('puo_lanciare', False):
                        return True
            return False
            
        elif tipo_carta == 'oscura_simmetria':
            # Verifica se ci sono guerrieri Oscura Legione
            for guerriero in guerrieri:
                if guerriero.fazione in FAZIONI_OSCURA_LEGIONE:
                    if hasattr(carta, 'puo_essere_associata_a_guerriero'):
                        risultato = carta.puo_essere_associata_a_guerriero(guerriero)
                        if risultato.get('puo_lanciare', False) or risultato.get('puo_assegnare', False):
                            return True
            return False
            
        elif tipo_carta in ['equipaggiamento', 'reliquia']:
            # Verifica restrizioni di fazione/tipo
            if hasattr(carta, 'fazioni_permesse'):
                fazioni_guerrieri = set(g.fazione for g in guerrieri)
                if not any(f in carta.fazioni_permesse for f in fazioni_guerrieri):
                    return False
            
            if hasattr(carta, 'tipi_guerriero_permessi'):
                tipi_guerrieri = set()
                for g in guerrieri:
                    if hasattr(g, 'tipo'):
                        tipi_guerrieri.add(g.tipo)
                if not any(t in carta.tipi_guerriero_permessi for t in tipi_guerrieri):
                    return False
            
            return True
            
        elif tipo_carta == 'fortificazione':
            # Le fortificazioni sono generalmente utilizzabili
            return True
            
        elif tipo_carta == 'warzone':
            # Verifica se può essere assegnata ad almeno una fazione presente
            fazioni_presenti = set(g.fazione for g in guerrieri)
            for fazione in fazioni_presenti:
                if hasattr(carta, 'puo_essere_associata_a_fazione'):
                    risultato = carta.puo_essere_associata_a_fazione(fazione)
                    if risultato.get('puo_essere_associata', False):
                        return True
            return False
            
        elif tipo_carta in ['speciale', 'missione']:
            # Verifica restrizioni generiche
            if hasattr(carta, 'fazioni_permesse'):
                fazioni_guerrieri = set(g.fazione for g in guerrieri)
                if not any(f in carta.fazioni_permesse for f in fazioni_guerrieri):
                    return False
            return True
        
        return True
    
    def calcola_distribuzione_carte(self, 
                                   numero_totale: int,
                                   usa_fratellanza: bool,
                                   usa_oscura_legione: bool) -> Dict[str, int]:
        """
        Calcola la distribuzione delle carte nel mazzo
        
        Args:
            numero_totale: Numero totale di carte nel mazzo
            usa_fratellanza: Se True, include carte Arte
            usa_oscura_legione: Se True, include carte Oscura Simmetria
            
        Returns:
            Dizionario con numero di carte per tipo
        """
        distribuzione = {}
        
        # Calcola percentuali base
        for tipo, percentuale in DISTRIBUZIONE_BASE.items():
            if tipo == 'missione':
                distribuzione[tipo] = min(2, numero_totale // 30)  # Max 2 missioni
            else:
                min_perc, max_perc = percentuale
                perc_media = (min_perc + max_perc) / 2
                
                # Aggiungi casualità
                perc_finale = perc_media + random.uniform(-0.02, 0.02)
                perc_finale = max(min_perc, min(max_perc, perc_finale))
                
                distribuzione[tipo] = int(numero_totale * perc_finale)
        
        # Ridistribuisci se Arte o Oscura Simmetria non sono usate
        ridistribuzione_totale = 0
        
        if not usa_fratellanza:
            ridistribuzione_totale += distribuzione['arte']
            distribuzione['arte'] = 0
        
        if not usa_oscura_legione:
            ridistribuzione_totale += distribuzione['oscura_simmetria']
            distribuzione['oscura_simmetria'] = 0
        
        if ridistribuzione_totale > 0:
            # Ridistribuisci alle altre carte
            distribuzione['equipaggiamento'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['equipaggiamento'])
            distribuzione['speciale'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['speciale'])
            distribuzione['reliquia'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['reliquia'])
        
        # Assicura che il totale sia corretto
        totale_attuale = sum(distribuzione.values())
        differenza = numero_totale - totale_attuale
        
        if differenza > 0:
            distribuzione['speciale'] += differenza
        elif differenza < 0:
            # Riduci carte speciali se necessario
            distribuzione['speciale'] = max(0, distribuzione['speciale'] + differenza)
        
        return distribuzione


# ================================================================================
# FUNZIONE PRINCIPALE
# ================================================================================

def crea_mazzo_da_collezione(collezione: Any,
                            numero_carte_max: int,
                            numero_carte_min: int,
                            espansioni_richieste: List[str],
                            orientamento_doomtrooper: List[str] = None,
                            orientamento_arte: List[str] = None,
                            orientamento_apostolo: List[str] = None,
                            orientamento_eretico: bool = False) -> Dict[str, Any]:
    """
    Crea un mazzo ottimizzato dalla collezione del giocatore
    
    Args:
        collezione: Oggetto CollezioneGiocatore contenente tutte le carte
        numero_carte_max: Numero massimo di carte nel mazzo
        numero_carte_min: Numero minimo di carte nel mazzo
        espansioni_richieste: Lista delle espansioni da utilizzare (es: ['Base', 'Inquisition', 'Warzone'])
        orientamento_doomtrooper: Fazioni Doomtrooper preferite (opzionale)
        orientamento_arte: Discipline Arte preferite (opzionale)
        orientamento_apostolo: Apostoli preferiti (opzionale)
        orientamento_eretico: Se True, preferisce guerrieri eretici (opzionale)
        
    Returns:
        Dizionario contenente:
        - 'squadra': Lista dei guerrieri Doomtrooper/Fratellanza
        - 'schieramento': Lista dei guerrieri Oscura Legione
        - 'carte_supporto': Lista delle altre carte
        - 'statistiche': Statistiche del mazzo creato
        - 'errori': Eventuali errori o avvisi
    """
    
    # Validazione parametri
    if numero_carte_min > numero_carte_max:
        return {
            'squadra': [],
            'schieramento': [],
            'carte_supporto': [],
            'statistiche': {},
            'errori': ["Il numero minimo di carte non può essere maggiore del numero massimo"]
        }
    
    # Determina il numero target di carte
    numero_carte_target = random.randint(numero_carte_min, numero_carte_max)
    
    # Crea il creatore del mazzo
    creatore = CreatoreMazzo(collezione)
    
    # Determina se usare Fratellanza e Oscura Legione
    usa_fratellanza = orientamento_arte is not None and len(orientamento_arte) > 0
    usa_oscura_legione = orientamento_apostolo is not None and len(orientamento_apostolo) > 0
    
    # Se non specificato, controlla nella collezione
    if not usa_fratellanza:
        guerrieri_fratellanza = [g for g in collezione.get_carte_per_tipo('guerriero') 
                                 if g.fazione in FAZIONI_FRATELLANZA]
        usa_fratellanza = len(guerrieri_fratellanza) > 0
    
    if not usa_oscura_legione:
        guerrieri_oscura = [g for g in collezione.get_carte_per_tipo('guerriero') 
                           if g.fazione in FAZIONI_OSCURA_LEGIONE]
        usa_oscura_legione = len(guerrieri_oscura) > 0
    
    # Calcola distribuzione carte
    distribuzione = creatore.calcola_distribuzione_carte(
        numero_carte_target,
        usa_fratellanza,
        usa_oscura_legione
    )
    
    # Seleziona guerrieri
    numero_guerrieri = distribuzione['guerriero']
    squadra, schieramento = creatore.seleziona_guerrieri(
        espansioni_richieste,
        orientamento_doomtrooper,
        orientamento_arte,
        orientamento_apostolo,
        orientamento_eretico,
        numero_guerrieri
    )
    
    # Seleziona carte di supporto nell'ordine specificato
    carte_supporto = []
    
    # 1. Equipaggiamenti
    if distribuzione['equipaggiamento'] > 0:
        equipaggiamenti = creatore.seleziona_carte_supporto(
            squadra, schieramento, espansioni_richieste,
            'equipaggiamento', distribuzione['equipaggiamento']
        )
        carte_supporto.extend(equipaggiamenti)
    
    # 2. Fortificazioni
    fortificazioni = creatore.seleziona_carte_supporto(
        squadra, schieramento, espansioni_richieste,
        'fortificazione', distribuzione.get('fortificazione', 0)
    )
    carte_supporto.extend(fortificazioni)
    
    # 3. Speciali
    if distribuzione['speciale'] > 0:
        speciali = creatore.seleziona_carte_supporto(
            squadra, schieramento, espansioni_richieste,
            'speciale', distribuzione['speciale']
        )
        carte_supporto.extend(speciali)
    
    # 4. Missioni
    if distribuzione['missione'] > 0:
        missioni = creatore.seleziona_carte_supporto(
            squadra, schieramento, espansioni_richieste,
            'missione', distribuzione['missione']
        )
        carte_supporto.extend(missioni)
    
    # 5. Arte (se guerrieri Fratellanza presenti)
    if usa_fratellanza and distribuzione['arte'] > 0:
        arte = creatore.seleziona_carte_supporto(
            squadra, schieramento, espansioni_richieste,
            'arte', distribuzione['arte']
        )
        carte_supporto.extend(arte)
    
    # 6. Oscura Simmetria (se guerrieri Oscura Legione presenti)
    if usa_oscura_legione and distribuzione['oscura_simmetria'] > 0:
        oscura = creatore.seleziona_carte_supporto(
            squadra, schieramento, espansioni_richieste,
            'oscura_simmetria', distribuzione['oscura_simmetria']
        )
        carte_supporto.extend(oscura)
    
    # 7. Reliquie (se espansione Inquisition richiesta)
    if 'Inquisition' in espansioni_richieste and distribuzione['reliquia'] > 0:
        reliquie = creatore.seleziona_carte_supporto(
            squadra, schieramento, espansioni_richieste,
            'reliquia', distribuzione['reliquia']
        )
        carte_supporto.extend(reliquie)
    
    # 8. Warzone (se espansione Warzone richiesta)
    if 'Warzone' in espansioni_richieste and distribuzione['warzone'] > 0:
        warzone = creatore.seleziona_carte_supporto(
            squadra, schieramento, espansioni_richieste,
            'warzone', distribuzione['warzone']
        )
        carte_supporto.extend(warzone)
    
    # Calcola statistiche
    statistiche = {
        'numero_totale_carte': len(squadra) + len(schieramento) + len(carte_supporto),
        'guerrieri_squadra': len(squadra),
        'guerrieri_schieramento': len(schieramento),
        'carte_supporto': len(carte_supporto),
        'distribuzione_per_tipo': {},
        'fazioni_presenti': [],
        'espansioni_utilizzate': espansioni_richieste
    }
    
    # Conta carte per tipo
    for carta in carte_supporto:
        tipo = type(carta).__name__.lower()
        statistiche['distribuzione_per_tipo'][tipo] = statistiche['distribuzione_per_tipo'].get(tipo, 0) + 1
    
    # Identifica fazioni presenti
    fazioni_set = set()
    for guerriero in squadra + schieramento:
        fazioni_set.add(guerriero.fazione.value if hasattr(guerriero.fazione, 'value') else str(guerriero.fazione))
    statistiche['fazioni_presenti'] = list(fazioni_set)
    
    # Verifica errori o avvisi
    errori = []
    
    if len(squadra) < 5:
        errori.append("ATTENZIONE: La squadra ha meno di 5 guerrieri (minimo richiesto dal regolamento)")
    
    if statistiche['numero_totale_carte'] < numero_carte_min:
        errori.append(f"Il mazzo ha {statistiche['numero_totale_carte']} carte, meno del minimo richiesto ({numero_carte_min})")
    
    if statistiche['numero_totale_carte'] > numero_carte_max:
        errori.append(f"Il mazzo ha {statistiche['numero_totale_carte']} carte, più del massimo richiesto ({numero_carte_max})")
    
    # Costruisci il risultato finale
    risultato = {
        'squadra': squadra,
        'schieramento': schieramento,
        'carte_supporto': carte_supporto,
        'statistiche': statistiche,
        'errori': errori,
        'distribuzione_utilizzata': distribuzione
    }
    
    return risultato


# ================================================================================
# FUNZIONI DI UTILITÀ
# ================================================================================

def stampa_mazzo(mazzo: Dict[str, Any]) -> None:
    """
    Stampa il mazzo in formato leggibile
    
    Args:
        mazzo: Dizionario del mazzo creato
    """
    print("=" * 80)
    print("MAZZO CREATO")
    print("=" * 80)
    
    print(f"\n📊 STATISTICHE:")
    for chiave, valore in mazzo['statistiche'].items():
        print(f"  • {chiave}: {valore}")
    
    print(f"\n⚔️ SQUADRA ({len(mazzo['squadra'])} guerrieri):")
    for guerriero in mazzo['squadra']:
        print(f"  • {guerriero.nome} ({guerriero.fazione.value if hasattr(guerriero.fazione, 'value') else guerriero.fazione})")
    
    print(f"\n🌑 SCHIERAMENTO ({len(mazzo['schieramento'])} guerrieri):")
    for guerriero in mazzo['schieramento']:
        print(f"  • {guerriero.nome} ({guerriero.fazione.value if hasattr(guerriero.fazione, 'value') else guerriero.fazione})")
    
    print(f"\n🎴 CARTE SUPPORTO ({len(mazzo['carte_supporto'])} carte):")
    for carta in mazzo['carte_supporto'][:20]:  # Mostra solo le prime 20
        tipo = type(carta).__name__
        print(f"  • {carta.nome} ({tipo})")
    
    if len(mazzo['carte_supporto']) > 20:
        print(f"  ... e altre {len(mazzo['carte_supporto']) - 20} carte")
    
    if mazzo['errori']:
        print(f"\n⚠️ AVVISI:")
        for errore in mazzo['errori']:
            print(f"  • {errore}")
    
    print("=" * 80)




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

        print("\n🎯 Demo: Test salvataggio")
        esempio_salvataggio_migliorato()
        
        # Per attivare il menu interattivo, decommenta la riga seguente:
        menu_interattivo()

    except Exception as e:
        print(f"❌ Errore durante la demo: {e}")


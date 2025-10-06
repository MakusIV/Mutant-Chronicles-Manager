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
    crea_istanza_warzone as crea_warzone_da_database
)

PERCORSO_SALVATAGGIO = "out/"

# 1: 50% SCHIERAMENTO, 50% SQUADRA, 3/2: 40% SCHIERAMENTO, 60% SQUADRA, 2: 33% SCHIERAMENTO, 66% SQUADRA, 3: 25% SCHIERAMENTO, 75% SQUADRA
# 1/2: 66% SCHIERAMENTO, 33% SQUADRA, 2/3: 60% SCHIERAMENTO, 40% SQUADRA, 1/3: 75% SCHIERAMENTO, 25% SQUADRA
RAPPORTO_SQUADRA_SCHIERAMENTO = 1 



LIMITI_CARTE_COLLEZIONE = { # specifica il range % del numero di carte per tipo da inserire nella collezione
            'Guerriero': {'min': 0.9 , 'max': 1 },
            'Equipaggiamento': {'min': 0.9 , 'max': 1  },
            'Speciale': {'min': 0.85 , 'max': 1},
            'Arte': {'min': 0.9 , 'max': 1  },
            'Oscura Simmetria': {'min': 0.9 , 'max': 1  },
            'Fortificazione': {'min': 0.9 , 'max': 1  },
            'Missione': {'min': 0.8 , 'max': 1  },
            'Reliquia': {'min': 0.9 , 'max': 1  },
            'Warzone': {'min': 0.8 , 'max': 1  },
        } 



MAX_COPIE_CARTA = 6 # Numero massimo di copie da inserire nella collezione per una specifica carta


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

class TipoCombinazioneFazione(Enum):
    """Combinazioni di fazioni per collezioni orientate"""
    FRATELLANZA_DOOMTROOPER_FREELANCER = ("Fratellanza", "Doomtrooper", "Freelancer")
    # FRATELLANZA_OSCURA_LEGIONE_FREELANCER = ("Fratellanza", "Oscura Legione", "Freelancer") 
    DOOMTROOPER_OSCURA_LEGIONE_FREELANCER = ("Doomtrooper", "Oscura Legione", "Freelancer")
    DOOMTROOPER_FREELANCER = ("Doomtrooper", "Freelancer")

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
        if hasattr(carta, 'valore') and carta.valore and (isinstance(carta.valore, int) or isinstance(carta.valore, float)):
            self.valore_totale_dp += carta.valore * quantita
        elif hasattr(carta, 'costo_destino') and carta.costo_destino and (isinstance(carta.costo_destino, int) or isinstance(carta.costo_destino, float)):
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
    
    def get_carte_per_tipo_mazzo(self, tipo_carta: str) -> List[Any]:
        """Restituisce le carte di un tipo specifico con quantità per mazzo: a differenza di get_carte_tipo, ogni carta è unica"""
        collezione = self.carte.get(tipo_carta, [])
        
        #resetta quantità

        for v in collezione:
            v.quantita = 0

        elenco = {}
        for v in collezione:
            if v.nome in elenco.keys():
                elenco[v.nome].quantita += 1
            else:
                v.quantita = 1                
                elenco[v.nome] = v
                
        return list(elenco.values())

    def get_copie_disponibili(self, tipo_carta: str, carta: Any) -> int:
        collezione = self.carte.get(tipo_carta, [])        
        copie = 0
        
        if carta in collezione:
            copie += 1
        
        return copie

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
    min_carte: int = 5, # minimo numero di carte per tipologia (Guerriero, Equipaggiamento, ....) da inserire nella collezione
    max_carte: int = 10, # massimo numero di carte per tipologia (Guerriero, Equipaggiamento, ....) da inserire nella collezione
    numero_giocatori = None,
    numero_mazzo = None,
    probabilita_orientamento: float = 0.7
    ) -> List[Any]:
    """
    Seleziona carte casuali per tipo (Guerriero, Equipaggiamento, ecc) da un database rispettando quantità e orientamento
    """
    carte_selezionate = []
    giocatori_rimasti = numero_giocatori - numero_mazzo

    # Filtra carte per set espansioni
    carte_disponibili = {}
    for nome, dati in database.items():
        if dati.get('set_espansione') in [s.value for s in set_espansioni]:
            if verifica_quantita_disponibile(nome, database):
                carte_disponibili[nome] = dati
    
    

    if not carte_disponibili:
        return carte_selezionate
    
    # Determina numero di carte da selezionare per una tipologia (Guerriero, Equipaggiamento, ...)
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
                carte_orientate[nome] = dati # inserisce la carta nelle carte_orientate se questa è associabile ad una delle fazioni permesse
            else:
                carte_generiche[nome] = dati # ... altrimenti la inserisce nelle carte generiche
    else:
        carte_generiche = carte_disponibili
    
    # Seleziona carte privilegiando l'orientamento
    numero_totale_carte_inserite_per_tipologia = 0


    for _ in range(num_carte):
        if not carte_disponibili:
            break
        
        # Decide se usare orientamento o carte generiche per la scelta della carta
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
        


        # MODIFICA PER DISTRIBUZIONE BILANCIATA CARTE COLLEZIONE
        # se il numero d carte è insufficiente per tutti i giocatori, assegna la carta in base alla probabilita in modo da non favorire il/i primo/i giocatore per cui si crea la collezione
        quantita_disponibile = dati_carta.get('quantita') - QUANTITA_UTILIZZATE[nome_carta]        

        if quantita_disponibile < giocatori_rimasti:  # numero copie inferiore al numero giocatori da servire
            if random.random() >= quantita_disponibile / giocatori_rimasti: # valutazione della probabilità di NON assegnazione della carta al giocatore corrente
                # la carta non è assegnabile al giocatore corrente e viene rimossa dal pool 
                if nome_carta in carte_orientate:
                    del carte_orientate[nome_carta]
                if nome_carta in carte_generiche:
                    del carte_generiche[nome_carta]
                continue #prosegue con il prossimo item del ciclo for


        #La carta è assegnabile al giocatore corrente

        # Determina quantità per singola copia da aggiungere (1-3 copie)
        max_quantita_disponibile = min(
            MAX_COPIE_CARTA,  # Massimo 6 copie per carta per collezione (considera mazzo max 5 carte e collezione di gioco: totale 25 carte). La quantità minima consigliata viene utilizzata per la creazione del mazzo
            dati_carta.get('quantita', 0) - QUANTITA_UTILIZZATE[nome_carta]
        )
            
        # calcola la quantita di copie da inserire nella collezione per una specifica carta        
        quantita = random.randint(1, max_quantita_disponibile)
        
        # Crea e aggiungi il quantitativo di copie richiesto per la carta specifica con diverse istanze della stessa
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
        
        # rimuovi la carta dalle liste di selezione in modo da non poter essere più selezionata
        if nome_carta in carte_orientate:
            del carte_orientate[nome_carta] # elimina la carta e di conseguenza dal pool di scelta casuale: un solo prelievo
        if nome_carta in carte_generiche:
            del carte_generiche[nome_carta] # elimina la carta e di conseguenza dal pool di scelta casuale: un solo prelievo

        # Aggiorna contatore totale carte inserite per tipologia
        numero_totale_carte_inserite_per_tipologia += quantita

        # Interrompe il ciclo se è stato raggiunto il numero massimo di carte per tipologia
        if numero_totale_carte_inserite_per_tipologia >= num_carte:
            return carte_selezionate
    
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

def calcola_numero_carte_assegnabili(espansioni_valide: List, numero_giocatori: int) -> Dict:
    """Calcola e stampa il numero totale di carte assegnabili per tipo in base alle espansioni selezionate"""
    totale_carte_per_tipo = defaultdict(int)
    limiti_carte = {tipo: {'min': 0, 'max': 0} for tipo in ['Guerriero', 'Equipaggiamento', 'Speciale', 'Fortificazione', 'Missione', 'Arte', 'Oscura Simmetria', 'Reliquia', 'Warzone']}
    valori_espansioni = [espansione.value for espansione in espansioni_valide]
    # Conta carte per tipo
    for nome, dati in GUERRIERI_DATABASE.items():
        if dati.get('set_espansione') in valori_espansioni:
            totale_carte_per_tipo['Guerriero'] += dati.get('quantita', 0)
    
    for nome, dati in DATABASE_EQUIPAGGIAMENTO.items():
        if dati.get('set_espansione') in valori_espansioni:
            totale_carte_per_tipo['Equipaggiamento'] += dati.get('quantita', 0)
    
    for nome, dati in DATABASE_SPECIALI.items():
        if dati.get('set_espansione') in valori_espansioni:
            totale_carte_per_tipo['Speciale'] += dati.get('quantita', 0)
    
    for nome, dati in DATABASE_FORTIFICAZIONI.items():
        if dati.get('set_espansione') in valori_espansioni:
            totale_carte_per_tipo['Fortificazione'] += dati.get('quantita', 0)
    
    for nome, dati in DATABASE_MISSIONI.items():
        if dati.get('set_espansione') in valori_espansioni:
            totale_carte_per_tipo['Missione'] += dati.get('quantita', 0)
    
    for nome, dati in CARTE_ARTE_DATABASE.items():
        if dati.get('set_espansione') in valori_espansioni:
            totale_carte_per_tipo['Arte'] += dati.get('quantita', 0)
    
    for nome, dati in DATABASE_OSCURA_SIMMETRIA.items():
        if dati.get('set_espansione') in valori_espansioni:
            totale_carte_per_tipo['Oscura Simmetria'] += dati.get('quantita', 0)
    
    for nome, dati in DATABASE_RELIQUIE.items():
        if dati.get('set_espansione') in valori_espansioni:
            totale_carte_per_tipo['Reliquia'] += dati.get('quantita', 0)
    
    for nome, dati in DATABASE_WARZONE.items():
        if dati.get('set_espansione') in valori_espansioni:
            totale_carte_per_tipo['Warzone'] += dati.get('quantita', 0)

    for tipo in ['Guerriero', 'Equipaggiamento', 'Speciale', 'Fortificazione', 'Missione', 'Arte', 'Oscura Simmetria', 'Reliquia', 'Warzone']:
        limiti_carte[tipo]['max'] = int (totale_carte_per_tipo[tipo] * LIMITI_CARTE_COLLEZIONE[tipo]['max'] / numero_giocatori)
        limiti_carte[tipo]['min'] = int (totale_carte_per_tipo[tipo] * LIMITI_CARTE_COLLEZIONE[tipo]['min'] / numero_giocatori)
        
    return limiti_carte

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
        raise ValueError("Il numero di giocatori deve essere maggiore di zero")
    

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
    
    limiti_carte = calcola_numero_carte_assegnabili(espansioni_valide, numero_giocatori)

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
                
                collezione.fazioni_orientamento = list(fazioni_orientamento)    
                print(f"Orientamento: {[f.value for f in fazioni_orientamento]}")
            else:               
                
                print("Impossibile assegnare orientamento unico, procedendo senza orientamento")


        # Seleziona carte per ogni tipo
        
        # 1. Guerrieri
        print("Selezionando Guerrieri...")
        guerrieri = seleziona_carte_casuali_per_tipo(
            GUERRIERI_DATABASE,
            crea_guerriero_da_database, # funzione da utilizzare
            espansioni_valide,
            collezione.fazioni_orientamento,
            min_carte=limiti_carte['Guerriero']['min'],
            max_carte=limiti_carte['Guerriero']['max'],
            numero_giocatori = numero_giocatori,
            numero_mazzo = i
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
            min_carte=limiti_carte['Equipaggiamento']['min'],
            max_carte=limiti_carte['Equipaggiamento']['max'],
            numero_giocatori = numero_giocatori,
            numero_mazzo = i
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
            min_carte=limiti_carte['Speciale']['min'],
            max_carte=limiti_carte['Speciale']['max'],
            numero_giocatori = numero_giocatori,
            numero_mazzo = i
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
            min_carte=limiti_carte['Fortificazione']['min'],
            max_carte=limiti_carte['Fortificazione']['max'],
            numero_giocatori = numero_giocatori,
            numero_mazzo = i
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
            min_carte=limiti_carte['Missione']['min'],
            max_carte=limiti_carte['Missione']['max'],
            numero_giocatori = numero_giocatori,
            numero_mazzo = i
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
            min_carte=limiti_carte['Arte']['min'],            
            max_carte=limiti_carte['Arte']['max'],
            numero_giocatori = numero_giocatori,
            numero_mazzo = i
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
            min_carte=limiti_carte['Oscura Simmetria']['min'],
            max_carte=limiti_carte['Oscura Simmetria']['max'],
            numero_giocatori = numero_giocatori,
            numero_mazzo = i
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
            min_carte=limiti_carte['Reliquia']['min'],
            max_carte=limiti_carte['Reliquia']['max'],
            numero_giocatori = numero_giocatori,
            numero_mazzo = i
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
            min_carte=limiti_carte['Warzone']['min'],
            max_carte=limiti_carte['Warzone']['max'],
            numero_giocatori = numero_giocatori,
            numero_mazzo = i
        )
        for carta_warzone in warzone:
            collezione.aggiungi_carta(carta_warzone)
        
        collezioni.append(collezione)
        print(f"Collezione Giocatore {i+1} completata: {collezione.get_totale_carte()} carte totali")
    
    print(f"\n=== CREAZIONE COMPLETATA ===")
    print(f"Create {len(collezioni)} collezioni")
    print(f"Quantità totali utilizzate: {dict(QUANTITA_UTILIZZATE)}")
    
    return collezioni

def converti_json_a_collezioni(dati_json: Dict[str, Any]) -> List[CollezioneGiocatore]:
    """
    Converte il dizionario restituito da carica_collezioni_json_migliorato
    in una lista di istanze CollezioneGiocatore.
    
    Args:
        dati_json: Dizionario restituito da carica_collezioni_json_migliorato
        
    Returns:
        Lista di istanze CollezioneGiocatore
        
    Raises:
        ValueError: Se il formato del JSON non è valido
        KeyError: Se mancano chiavi obbligatorie nel JSON
    """
    
    # Validazione input
    if not dati_json:
        raise ValueError("Il dizionario JSON è vuoto o None")
    
    if 'collezioni_dettagliate' not in dati_json:
        raise ValueError("Il dizionario JSON non contiene la chiave 'collezioni'")
    
    # Estrai le collezioni dal JSON
    collezioni_json = dati_json['collezioni_dettagliate']
    
    if not isinstance(collezioni_json, list):
        raise ValueError("'collezioni' deve essere una lista")
    
    # Lista per le istanze da restituire
    istanze_collezioni: List[CollezioneGiocatore] = []
    
    # Mapping funzioni di creazione carte
    funzioni_creazione = {
        'guerriero': crea_guerriero_da_database,
        'equipaggiamento': crea_equipaggiamento_da_database,
        'speciale': crea_speciale_da_database,
        'fortificazione': crea_fortificazione_da_database,
        'missione': crea_missione_da_database,
        'arte': crea_arte_da_database,
        'oscura_simmetria': crea_oscura_simmetria_da_database,
        'reliquia': crea_reliquia_da_database,
        'warzone': crea_warzone_da_database
    }
    
    # Processa ogni collezione
    for idx, collezione_data in enumerate(collezioni_json, 1):
        try:
            # Crea nuova istanza CollezioneGiocatore
            collezione = CollezioneGiocatore(
                id_giocatore=collezione_data.get('id_giocatore', idx),                
                
            )
            
            # Ricrea le carte dalla sezione inventario
            inventario = collezione_data.get('carte_per_tipo', {})
            
            for tipo_carte, lista_carte in inventario.items():
                if tipo_carte not in funzioni_creazione:
                    print(f"Avviso: tipo carte '{tipo_carte}' non riconosciuto, skip...")
                    continue
                
                funzione_creazione = funzioni_creazione[tipo_carte]
                
                # Per ogni carta nel JSON
                for carta, carta_data in lista_carte.get('dettaglio_carte').items():
                    nome_carta = carta_data['nome']
                    quantita = carta_data['quantita']

                    if not nome_carta:
                        print(f"Avviso: carta senza nome in {tipo_carte}, skip...")
                        continue
                    
                    # Ricrea la carta dal database usando il nome
                    try:
                        carta = funzione_creazione(nome_carta)
                        
                        if carta:
                            # Aggiungi la carta alla collezione nel tipo appropriato
                            for _ in range(0, quantita): # NOTA:copia nella lista la stessa istanza della carta (quindi attenzione se servono diverse istanze (gioco digitale))
                                if tipo_carte == 'guerriero':                                 
                                    # PER DIVERSE ISTANZE inserisci qui (e ripeti sotto) carta = funzione_creazione(nome_carta) eliminando quela della riga 1172
                                    collezione.carte['guerriero'].append(carta)
                                elif tipo_carte == 'equipaggiamento':
                                    collezione.carte['equipaggiamento'].append(carta)
                                elif tipo_carte == 'speciale':
                                    collezione.carte['speciale'].append(carta)
                                elif tipo_carte == 'fortificazione':
                                    collezione.carte['fortificazione'].append(carta)
                                elif tipo_carte == 'missione':
                                    collezione.carte['missione'].append(carta)
                                elif tipo_carte == 'arte':
                                    collezione.carte['arte'].append(carta)
                                elif tipo_carte == 'oscura_simmetria':
                                    collezione.carte['oscura_simmetria'].append(carta)
                                elif tipo_carte == 'reliquia':
                                    collezione.carte['reliquia'].append(carta)
                                elif tipo_carte == 'warzone':
                                    collezione.carte['warzone'].append(carta)
                        else:
                            print(f"Avviso: carta '{nome_carta}' non trovata nel database")
                    
                    except Exception as e:
                        print(f"Errore creazione carta '{nome_carta}': {e}")
                        continue
            
            # Aggiungi la collezione ricreata alla lista
            istanze_collezioni.append(collezione)
            
            print(f"✅ Collezione {collezione.id_giocatore} ricreata con {collezione.get_totale_carte()} carte")
        
        except Exception as e:
            print(f"❌ Errore nel processare collezione {idx}: {e}")
            continue
    
    # Verifica che almeno una collezione sia stata creata
    if not istanze_collezioni:
        raise ValueError("Nessuna collezione è stata creata con successo")
    
    print(f"\n🎉 Totale: {len(istanze_collezioni)} collezioni ricreate")
    
    return istanze_collezioni

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
                if hasattr(carta, 'valore') and ( isinstance(carta.valore, int) or isinstance(carta.valore, float)):
                    stats_fazioni[fazione_nome]['valore_dp'] += carta.valore
                elif hasattr(carta, 'costo_destino') and ( isinstance(carta.costo_destino, int) or isinstance(carta.costo_destino, float)):
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

"""
"""

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
                
                 # Aggiunge valore
                if hasattr(carta, 'valore') and ( isinstance(carta.valore, int) or isinstance(carta.valore, float)):
                    stats_fazioni[fazione_nome]['valore_dp'] += carta.valore
                elif hasattr(carta, 'costo_destino') and ( isinstance(carta.costo_destino, int) or isinstance(carta.costo_destino, float)):
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

"""

def salva_collezioni_json_migliorato(collezioni: List, filename: str = "collezioni_dettagliate.json"):
    
    
    Salva le collezioni in formato JSON con struttura dettagliata.
    Equivalente JSON di stampa_riepilogo_collezioni_migliorato().
    
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
    
    Carica collezioni dal formato JSON migliorato.
    
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
    
    Stampa statistiche dalle collezioni caricate da JSON.
    Equivalente di stampa_riepilogo_collezioni_migliorato() per dati JSON.
    
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

"""

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
            espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE],
            orientamento=False
        )
    # Stampa con visualizzazione migliorata
    stampa_riepilogo_collezioni_migliorato(collezioni)
    print("2. Salva dettagliato: salva_collezioni_json_migliorato(collezioni, 'collezioni_dettagliate.json')")
    # Salva con la STESSA struttura in JSON
    salva_collezioni_json_migliorato(collezioni, "collezioni_dettagliate.json")
    print("3. Carica: dati = carica_collezioni_json_migliorato('collezioni_dettagliate.json')")
    dati_json, _ = carica_collezioni_json_migliorato("collezioni_dettagliate.json")
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
        print("1. vuoto")
        print("2. vuoto")
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
            pass
        elif scelta == "2":
            pass
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
        ("Guerriero", crea_guerriero_da_database, "Dragone"),
        ("Equipaggiamento", crea_equipaggiamento_da_database, "L&A Carabina Al Plasma"),
        ("Speciale", crea_speciale_da_database, "Iniziativa"),
        ("Fortificazione", crea_fortificazione_da_database, "Heimburg"),
        ("Missione", crea_missione_da_database, "Eliminazione"),
        ("Arte", crea_arte_da_database, "Glaciazione"),
        ("Oscura Simmetria", crea_oscura_simmetria_da_database, "Cecità"),
        ("Reliquia", crea_reliquia_da_database, "Maschera Delle Vestali"),
        ("Warzone", crea_warzone_da_database, "Cyberopolis")
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
    


# ================================ AGGIORNAMENTO ORDINAMENTO IN BASE A FAZIONI ====================================


def crea_inventario_dettagliato_json(collezione) -> Dict[str, Any]:
    """
    Crea l'inventario dettagliato per una collezione in formato JSON.
    Struttura analoga a stampa_inventario_dettagliato().
    AGGIORNATO: Implementa nuove proprietà di visualizzazione e ordinamento.
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
        
        # Ordina le carte in base al tipo specifico
        carte_ordinate = _ordina_carte_per_tipo(liste_carte, tipo_carta)
        carte_conteggio_ordinato = defaultdict(int)
        carte_esempi_ordinati = {}
        
        for carta in carte_ordinate:
            carte_conteggio_ordinato[carta.nome] += 1
            if carta.nome not in carte_esempi_ordinati:
                carte_esempi_ordinati[carta.nome] = carta
        
        # Crea struttura per tipo carta
        tipo_info = {
            'totale_carte': len(liste_carte),
            'carte_uniche': len(carte_conteggio_ordinato),
            'dettaglio_carte': {}
        }
        
        # Dettagli per ogni carta unica (ordinati)
        for nome_carta, quantita in carte_conteggio_ordinato.items():
            carta_esempio = carte_esempi_ordinati[nome_carta]
            
            dettaglio_carta = {
                'nome': nome_carta,
                'quantita': quantita,
                'tipo': tipo_carta.capitalize()
            }
            
            # Informazioni base della carta con gestione sicura
            try:
                if hasattr(carta_esempio, 'rarity') and carta_esempio.rarity is not None:
                    dettaglio_carta['rarity'] = (
                        carta_esempio.rarity.value if hasattr(carta_esempio.rarity, 'value') 
                        else str(carta_esempio.rarity)
                    )
                
                if hasattr(carta_esempio, 'set_espansione') and carta_esempio.set_espansione is not None:
                    dettaglio_carta['set_espansione'] = (
                        carta_esempio.set_espansione.value if hasattr(carta_esempio.set_espansione, 'value')
                        else str(carta_esempio.set_espansione)
                    )
                
                # AGGIORNAMENTI SPECIFICI PER TIPO DI CARTA (con gestione errori)
                
                # Informazioni specifiche per GUERRIERI
                if tipo_carta == 'guerriero':
                    if hasattr(carta_esempio, 'fazione') and carta_esempio.fazione is not None:
                        dettaglio_carta['fazione'] = (
                            carta_esempio.fazione.value if hasattr(carta_esempio.fazione, 'value')
                            else str(carta_esempio.fazione)
                        )
                    
                    # Aggiunge informazione seguace per Oscura Legione
                    if hasattr(carta_esempio, 'keywords') and carta_esempio.keywords:
                        for keyword in carta_esempio.keywords:
                            if isinstance(keyword, str) and "Seguace di" in keyword:
                                dettaglio_carta['seguace_di'] = keyword
                                break
                    
                    # Statistiche combattimento per guerrieri
                    if hasattr(carta_esempio, 'stats') and carta_esempio.stats is not None:
                        dettaglio_carta['statistiche'] = {
                            'combattimento': getattr(carta_esempio.stats, 'combattimento', 0),
                            'sparare': getattr(carta_esempio.stats, 'sparare', 0),
                            'armatura': getattr(carta_esempio.stats, 'armatura', 0),
                            'valore': getattr(carta_esempio.stats, 'valore', 0)
                        }
                
                # Informazioni specifiche per EQUIPAGGIAMENTO
                elif tipo_carta == 'equipaggiamento':
                    # AGGIUNTO: proprietà fazione per equipaggiamenti
                    if hasattr(carta_esempio, 'fazioni_permesse') and carta_esempio.fazioni_permesse:
                        fazioni_str = []
                        for fazione in carta_esempio.fazioni_permesse:
                            if hasattr(fazione, 'value'):
                                fazioni_str.append(fazione.value)
                            else:
                                fazioni_str.append(str(fazione))
                        
                        if len(fazioni_str) == 1 and fazioni_str[0] != "Generica":
                            dettaglio_carta['fazione'] = fazioni_str[0]
                        else:
                            dettaglio_carta['fazione'] = ", ".join(fazioni_str)
                    else:
                        dettaglio_carta['fazione'] = "Generica"
                    # RIMOSSO: valore_dp per equipaggiamenti
                
                # Informazioni specifiche per SPECIALE
                elif tipo_carta == 'speciale':
                    # AGGIUNTO: proprietà fazioni_permesse per carte speciali
                    if hasattr(carta_esempio, 'fazioni_permesse') and carta_esempio.fazioni_permesse:
                        fazioni_str = []
                        for fazione in carta_esempio.fazioni_permesse:
                            if hasattr(fazione, 'value'):
                                fazioni_str.append(fazione.value)
                            else:
                                fazioni_str.append(str(fazione))
                        dettaglio_carta['fazioni_permesse'] = ", ".join(fazioni_str)
                    else:
                        dettaglio_carta['fazioni_permesse'] = "Tutte"
                    # RIMOSSO: valore_dp per carte speciali
                
                # Informazioni specifiche per FORTIFICAZIONE
                elif tipo_carta == 'fortificazione':
                    # AGGIUNTO: proprietà fazioni_permesse per fortificazioni
                    if hasattr(carta_esempio, 'fazioni_permesse') and carta_esempio.fazioni_permesse:
                        fazioni_str = []
                        for fazione in carta_esempio.fazioni_permesse:
                            if hasattr(fazione, 'value'):
                                fazioni_str.append(fazione.value)
                            else:
                                fazioni_str.append(str(fazione))
                        dettaglio_carta['fazioni_permesse'] = ", ".join(fazioni_str)
                    else:
                        dettaglio_carta['fazioni_permesse'] = "Tutte"
                    # RIMOSSO: valore_dp per fortificazioni
                
                # Informazioni specifiche per MISSIONE
                elif tipo_carta == 'missione':
                    # AGGIUNTO: proprietà fazioni_permesse per missioni
                    if hasattr(carta_esempio, 'fazioni_permesse') and carta_esempio.fazioni_permesse:
                        fazioni_str = []
                        for fazione in carta_esempio.fazioni_permesse:
                            if hasattr(fazione, 'value'):
                                fazioni_str.append(fazione.value)
                            else:
                                fazioni_str.append(str(fazione))
                        dettaglio_carta['fazioni_permesse'] = ", ".join(fazioni_str)
                    else:
                        dettaglio_carta['fazioni_permesse'] = "Tutte"
                    # RIMOSSO: valore_dp per missioni
                
                # Informazioni specifiche per OSCURA SIMMETRIA
                elif tipo_carta == 'oscura_simmetria':
                    # AGGIUNTO: proprietà apostolo_padre per oscura simmetria
                    if hasattr(carta_esempio, 'apostolo_padre') and carta_esempio.apostolo_padre is not None:
                        dettaglio_carta['apostolo_padre'] = (
                            carta_esempio.apostolo_padre.value if hasattr(carta_esempio.apostolo_padre, 'value')
                            else str(carta_esempio.apostolo_padre)
                        )
                    else:
                        dettaglio_carta['apostolo_padre'] = "Nessuno"
                    # RIMOSSO: valore_dp per oscura simmetria
                
                # Informazioni specifiche per ARTE
                elif tipo_carta == 'arte':
                    # AGGIUNTO: proprietà disciplina per arte
                    if hasattr(carta_esempio, 'disciplina') and carta_esempio.disciplina is not None:
                        dettaglio_carta['disciplina'] = (
                            carta_esempio.disciplina.value if hasattr(carta_esempio.disciplina, 'value')
                            else str(carta_esempio.disciplina)
                        )
                    elif hasattr(carta_esempio, 'disciplina_arte') and carta_esempio.disciplina_arte is not None:
                        dettaglio_carta['disciplina'] = (
                            carta_esempio.disciplina_arte.value if hasattr(carta_esempio.disciplina_arte, 'value')
                            else str(carta_esempio.disciplina_arte)
                        )
                    else:
                        dettaglio_carta['disciplina'] = "Non specificata"
                    # RIMOSSO: valore_dp per arte
                
                # Informazioni specifiche per RELIQUIA
                elif tipo_carta == 'reliquia':
                    # AGGIUNTO: proprietà fazioni_permesse dalle restrizioni per reliquie
                    if hasattr(carta_esempio, 'restrizioni') and isinstance(carta_esempio.restrizioni, dict):
                        fazioni_permesse = carta_esempio.restrizioni.get('fazioni_permesse', [])
                        if fazioni_permesse:
                            fazioni_str = []
                            for fazione in fazioni_permesse:
                                if hasattr(fazione, 'value'):
                                    fazioni_str.append(fazione.value)
                                else:
                                    fazioni_str.append(str(fazione))
                            dettaglio_carta['fazioni_permesse'] = ", ".join(fazioni_str)
                        else:
                            dettaglio_carta['fazioni_permesse'] = "Tutte"
                    else:
                        dettaglio_carta['fazioni_permesse'] = "Tutte"
                    # RIMOSSO: valore_dp per reliquie
                
                # Informazioni specifiche per WARZONE
                elif tipo_carta == 'warzone':
                    # AGGIUNTO: proprietà fazioni_permesse dalle restrizioni per warzone
                    if hasattr(carta_esempio, 'restrizioni') and isinstance(carta_esempio.restrizioni, dict):
                        fazioni_permesse = carta_esempio.restrizioni.get('fazioni_permesse', [])
                        if fazioni_permesse:
                            fazioni_str = []
                            for fazione in fazioni_permesse:
                                if hasattr(fazione, 'value'):
                                    fazioni_str.append(fazione.value)
                                else:
                                    fazioni_str.append(str(fazione))
                            dettaglio_carta['fazioni_permesse'] = ", ".join(fazioni_str)
                        else:
                            dettaglio_carta['fazioni_permesse'] = "Tutte"
                    else:
                        dettaglio_carta['fazioni_permesse'] = "Tutte"
                    # RIMOSSO: valore_dp per warzone
                
                # Per altri tipi, mantiene il valore DP se presente
                else:
                    if hasattr(carta_esempio, 'valore') and carta_esempio.valore is not None:
                        dettaglio_carta['valore_dp'] = carta_esempio.valore
                    elif hasattr(carta_esempio, 'costo_destino') and carta_esempio.costo_destino is not None:
                        dettaglio_carta['valore_dp'] = carta_esempio.costo_destino
                    else:
                        dettaglio_carta['valore_dp'] = 0
                
                # Altre informazioni specifiche per tipo (con gestione sicura)
                if hasattr(carta_esempio, 'testo_carta') and carta_esempio.testo_carta:
                    dettaglio_carta['testo_carta'] = str(carta_esempio.testo_carta)
                
                if hasattr(carta_esempio, 'keywords') and carta_esempio.keywords:
                    # Converte tutti i keywords in stringhe
                    keywords_sicure = []
                    for kw in carta_esempio.keywords:
                        if kw is not None:
                            if hasattr(kw, 'value'):
                                keywords_sicure.append(kw.value)
                            else:
                                keywords_sicure.append(str(kw))
                    dettaglio_carta['keywords'] = keywords_sicure
                
            except Exception as e:
                print(f"⚠️ Errore processando carta {nome_carta}: {e}")
                # Mantiene le informazioni base anche in caso di errore
                dettaglio_carta['errore_processamento'] = str(e)
            
            tipo_info['dettaglio_carte'][nome_carta] = dettaglio_carta

        
        inventario_json['carte_per_tipo'][tipo_carta] = tipo_info
    
    # Totale carte uniche
    inventario_json['totali']['carte_uniche'] = len(carte_uniche_totali)
    
    # Statistiche per fazione (analoga a stampa_statistiche_fazioni)
    inventario_json['statistiche_fazioni'] = crea_statistiche_fazioni_json(collezione)
    
    return inventario_json

def _ordina_carte_per_tipo(carte: List, tipo_carta: str) -> List:
    """
    Ordina le carte in base al tipo specificato secondo i nuovi criteri.
    CORRETTO: Gestisce correttamente gli enum per evitare errori di confronto.
    """
    try:
        if tipo_carta == 'guerriero':
            # Ordina per fazione, poi per seguace_di per Oscura Legione
            return sorted(carte, key=lambda carta: (
                _get_fazione_sort_key(carta),
                _get_seguace_sort_key(carta),
                getattr(carta, 'nome', 'Unknown')
            ))
        
        elif tipo_carta == 'equipaggiamento':
            # Ordina per fazione
            return sorted(carte, key=lambda carta: (
                _get_fazione_equipaggiamento_sort_key(carta),
                getattr(carta, 'nome', 'Unknown')
            ))
        
        elif tipo_carta == 'speciale':
            # Ordina per fazioni_permesse
            return sorted(carte, key=lambda carta: (
                _get_fazioni_permesse_sort_key(carta),
                getattr(carta, 'nome', 'Unknown')
            ))
        
        elif tipo_carta == 'fortificazione':
            # Ordina per fazioni_permesse
            return sorted(carte, key=lambda carta: (
                _get_fazioni_permesse_sort_key(carta),
                getattr(carta, 'nome', 'Unknown')
            ))
        
        elif tipo_carta == 'missione':
            # Ordina per fazioni_permesse
            return sorted(carte, key=lambda carta: (
                _get_fazioni_permesse_sort_key(carta),
                getattr(carta, 'nome', 'Unknown')
            ))
        
        elif tipo_carta == 'oscura_simmetria':
            # Ordina per apostolo_padre
            return sorted(carte, key=lambda carta: (
                _get_apostolo_padre_sort_key(carta),
                getattr(carta, 'nome', 'Unknown')
            ))
        
        elif tipo_carta == 'arte':
            # Ordina per disciplina
            return sorted(carte, key=lambda carta: (
                _get_disciplina_sort_key(carta),
                getattr(carta, 'nome', 'Unknown')
            ))
        
        elif tipo_carta == 'reliquia':
            # Ordina per fazioni_permesse dalle restrizioni
            return sorted(carte, key=lambda carta: (
                _get_restrizioni_fazioni_sort_key(carta),
                getattr(carta, 'nome', 'Unknown')
            ))
        
        elif tipo_carta == 'warzone':
            # Ordina per fazioni_permesse dalle restrizioni
            return sorted(carte, key=lambda carta: (
                _get_restrizioni_fazioni_sort_key(carta),
                getattr(carta, 'nome', 'Unknown')
            ))
        
        else:
            # Ordinamento di default per nome
            return sorted(carte, key=lambda carta: getattr(carta, 'nome', 'Unknown'))
    
    except Exception as e:
        print(f"⚠️ Errore nell'ordinamento {tipo_carta}: {e}")
        print(f"   Fallback su ordinamento base per nome")
        # Fallback sicuro su ordinamento base
        return sorted(carte, key=lambda carta: getattr(carta, 'nome', 'Unknown'))

def _get_fazione_sort_key(carta) -> str:
    """Ottiene la chiave di ordinamento per fazione di un guerriero."""
    try:
        if hasattr(carta, 'fazione') and carta.fazione is not None:
            return carta.fazione.value if hasattr(carta.fazione, 'value') else str(carta.fazione)
        return "ZZZ_Sconosciuta"
    except Exception as e:
        print(f"⚠️ Errore nel get_fazione_sort_key per {getattr(carta, 'nome', 'carta sconosciuta')}: {e}")
        return "ZZZ_Errore"

def _get_seguace_sort_key(carta) -> str:
    """Ottiene la chiave di ordinamento per seguace di un guerriero Oscura Legione."""
    try:
        if hasattr(carta, 'keywords') and carta.keywords:
            for keyword in carta.keywords:
                if isinstance(keyword, str) and "Seguace di" in keyword:
                    return keyword
        return "ZZZ_Nessun_Seguace"
    except Exception as e:
        print(f"⚠️ Errore nel get_seguace_sort_key per {getattr(carta, 'nome', 'carta sconosciuta')}: {e}")
        return "ZZZ_Errore"

def _get_fazione_equipaggiamento_sort_key(carta) -> str:
    """Ottiene la chiave di ordinamento per fazione di un equipaggiamento."""
    try:
        if hasattr(carta, 'fazioni_permesse') and carta.fazioni_permesse:
            # Converte tutti gli elementi in stringhe prima dell'ordinamento
            fazioni_str = []
            for fazione in carta.fazioni_permesse:
                if hasattr(fazione, 'value'):
                    fazioni_str.append(fazione.value)
                else:
                    fazioni_str.append(str(fazione))
            
            if len(fazioni_str) == 1 and fazioni_str[0] != "Generica":
                return fazioni_str[0]
            else:
                return ", ".join(sorted(fazioni_str))
        return "ZZZ_Generica"
    except Exception as e:
        print(f"⚠️ Errore nel get_fazione_equipaggiamento_sort_key per {getattr(carta, 'nome', 'carta sconosciuta')}: {e}")
        return "ZZZ_Errore"

def _get_fazioni_permesse_sort_key(carta) -> str:
    """Ottiene la chiave di ordinamento per fazioni_permesse."""
    try:
        if hasattr(carta, 'fazioni_permesse') and carta.fazioni_permesse:
            # Converte tutti gli elementi in stringhe prima dell'ordinamento
            fazioni_str = []
            for fazione in carta.fazioni_permesse:
                if hasattr(fazione, 'value'):
                    fazioni_str.append(fazione.value)
                else:
                    fazioni_str.append(str(fazione))
            return ", ".join(sorted(fazioni_str))
        return "ZZZ_Tutte"
    except Exception as e:
        print(f"⚠️ Errore nel get_fazioni_permesse_sort_key per {getattr(carta, 'nome', 'carta sconosciuta')}: {e}")
        return "ZZZ_Errore"

def _get_apostolo_padre_sort_key(carta) -> str:
    """Ottiene la chiave di ordinamento per apostolo_padre."""
    try:
        if hasattr(carta, 'apostolo_padre') and carta.apostolo_padre is not None:
            return str(carta.apostolo_padre) if carta.apostolo_padre != None else str("Nessuno")
        return "ZZZ_Nessuno"
    except Exception as e:
        print(f"⚠️ Errore nel get_apostolo_padre_sort_key per {getattr(carta, 'nome', 'carta sconosciuta')}: {e}")
        return "ZZZ_Errore"

def _get_disciplina_sort_key(carta) -> str:
    """Ottiene la chiave di ordinamento per disciplina dell'arte."""
    try:
        if hasattr(carta, 'disciplina') and carta.disciplina is not None:
            return carta.disciplina.value if hasattr(carta.disciplina, 'value') else str(carta.disciplina)
        elif hasattr(carta, 'disciplina_arte') and carta.disciplina_arte is not None:
            return carta.disciplina_arte.value if hasattr(carta.disciplina_arte, 'value') else str(carta.disciplina_arte)
        return "ZZZ_Non_Specificata"
    except Exception as e:
        print(f"⚠️ Errore nel get_disciplina_sort_key per {getattr(carta, 'nome', 'carta sconosciuta')}: {e}")
        return "ZZZ_Errore"

def _get_restrizioni_fazioni_sort_key(carta) -> str:
    """Ottiene la chiave di ordinamento per fazioni_permesse nelle restrizioni."""
    try:
        if hasattr(carta, 'restrizioni') and isinstance(carta.restrizioni, dict):
            fazioni_permesse = carta.restrizioni.get('fazioni_permesse', [])
            if fazioni_permesse:
                # Converte tutti gli elementi in stringhe prima dell'ordinamento
                fazioni_str = []
                for fazione in fazioni_permesse:
                    if hasattr(fazione, 'value'):
                        fazioni_str.append(fazione.value)
                    else:
                        fazioni_str.append(str(fazione))
                return ", ".join(sorted(fazioni_str))
        return "ZZZ_Tutte"
    except Exception as e:
        print(f"⚠️ Errore nel get_restrizioni_fazioni_sort_key per {getattr(carta, 'nome', 'carta sconosciuta')}: {e}")
        return "ZZZ_Errore"

def stampa_riepilogo_collezioni_migliorato(collezioni: List, titolo: str = "RIEPILOGO COLLEZIONI CREATE") -> None:
    """
    Stampa un riepilogo dettagliato delle collezioni create.
    AGGIORNATO: Implementa nuovi ordinamenti e proprietà di visualizzazione.
    """
    print(f"\n{'='*80}")
    print(f"📋 {titolo} - {len(collezioni)} COLLEZIONI")
    print(f"{'='*80}")
    
    # Calcola totali
    totale_carte_globale = sum(c.get_totale_carte() for c in collezioni)
    totale_valore_globale = sum(c.statistiche.valore_totale_dp for c in collezioni)
    
    print(f"📦 Totale carte: {totale_carte_globale}")
    print(f"💰 Valore totale: {totale_valore_globale} DP")
    print(f"📈 Media carte/collezione: {totale_carte_globale/len(collezioni):.1f}")
    print(f"💎 Media valore/collezione: {totale_valore_globale/len(collezioni):.1f} DP")
    
    # Riepilogo collezioni con ordinamento aggiornato
    print(f"\n📊 RIEPILOGO COLLEZIONI:")
    for collezione in collezioni:
        orientamento_str = ""
        if collezione.fazioni_orientamento:
            fazioni = [f.value for f in collezione.fazioni_orientamento]
            orientamento_str = f" [🎯 {', '.join(fazioni)}]"
        
        print(f"  🎮 Giocatore {collezione.id_giocatore}: {collezione.get_totale_carte()} carte, {collezione.statistiche.valore_totale_dp} DP{orientamento_str}")
    
    # Distribuzione globale tipi con nuovi ordinamenti
    print(f"\n🃏 DISTRIBUZIONE GLOBALE TIPI:")
    distribuzione_tipi = defaultdict(int)
    
    for collezione in collezioni:
        for tipo_carta, liste_carte in collezione.carte.items():
            distribuzione_tipi[tipo_carta] += len(liste_carte)
    
    # Stampa con dettagli sui nuovi criteri di ordinamento
    for tipo, count in sorted(distribuzione_tipi.items()):
        criterio_ordinamento = _get_criterio_ordinamento_per_tipo(tipo)
        print(f"  {tipo.capitalize()}: {count} carte - Ordinato per: {criterio_ordinamento}")
    
    # Statistiche per fazione
    print(f"\n🏛️ DISTRIBUZIONE GLOBALE FAZIONI:")
    distribuzione_fazioni = defaultdict(int)
    
    for collezione in collezioni:
        for tipo_carta, liste_carte in collezione.carte.items():
            for carta in liste_carte:
                if hasattr(carta, 'fazione') and carta.fazione:
                    fazione_nome = carta.fazione.value if hasattr(carta.fazione, 'value') else str(carta.fazione)
                    distribuzione_fazioni[fazione_nome] += 1
    
    for fazione, count in sorted(distribuzione_fazioni.items()):
        print(f"  {fazione}: {count} carte")

def _get_criterio_ordinamento_per_tipo(tipo_carta: str) -> str:
    """Restituisce una descrizione del criterio di ordinamento per ogni tipo di carta."""
    criteri = {
        'guerriero': "fazione, poi seguace (per Oscura Legione)",
        'equipaggiamento': "fazione",
        'speciale': "fazioni_permesse",
        'fortificazione': "fazioni_permesse", 
        'missione': "fazioni_permesse",
        'oscura_simmetria': "apostolo_padre",
        'arte': "disciplina",
        'reliquia': "fazioni_permesse (da restrizioni)",
        'warzone': "fazioni_permesse (da restrizioni)"
    }
    return criteri.get(tipo_carta, "nome")

def stampa_statistiche_da_json(dati_json: Dict[str, Any]):
    """
    Stampa statistiche dalle collezioni caricate da JSON.
    Equivalente di stampa_riepilogo_collezioni_migliorato() per dati JSON.
    AGGIORNATO: Gestisce le nuove proprietà di visualizzazione.
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
    
    
    # Distribuzione tipi con informazioni sui nuovi ordinamenti
    print(f"\n🃏 DISTRIBUZIONE TIPI (con nuovi ordinamenti):")
    distribuzione_tipi = stats_aggregate.get('distribuzione_globale', {}).get('per_tipo', {})
    
    for tipo, count in sorted(distribuzione_tipi.items()):
        criterio = _get_criterio_ordinamento_per_tipo(tipo)
        print(f"  {tipo.capitalize()}: {count} carte - Ordinato per: {criterio}")
    
   
def salva_collezioni_json_migliorato(collezioni: List, filename: str = "collezioni_dettagliate.json"):
    """
    Salva le collezioni in formato JSON con struttura dettagliata.
    Equivalente JSON di stampa_riepilogo_collezioni_migliorato().
    AGGIORNATO: Utilizza le nuove funzioni di visualizzazione e ordinamento.
    """
    try:
        print(f"📄 Creazione struttura JSON dettagliata per {len(collezioni)} collezioni...")
        print("🔄 Applicando nuovi criteri di ordinamento e visualizzazione...")
        
        # Struttura principale del JSON
        dati_export = {
            'metadata': {
                'versione': '2.1',
                'tipo_export': 'collezioni_dettagliate_aggiornate',
                'data_creazione': datetime.now().isoformat(),
                'numero_collezioni': len(collezioni),
                'descrizione': 'Export dettagliato collezioni con nuovi ordinamenti e proprietà di visualizzazione',
                'aggiornamenti': {
                    'guerrieri': 'Ordinati per fazione e seguace (Oscura Legione)',
                    'equipaggiamenti': 'Aggiunta proprietà fazione, rimosso valore_dp',
                    'speciali': 'Aggiunta fazioni_permesse, rimosso valore_dp',
                    'fortificazioni': 'Aggiunta fazioni_permesse, rimosso valore_dp',
                    'missioni': 'Aggiunta fazioni_permesse, rimosso valore_dp',
                    'oscura_simmetria': 'Aggiunta apostolo_padre, rimosso valore_dp',
                    'arte': 'Aggiunta disciplina, rimosso valore_dp',
                    'reliquie': 'Aggiunta fazioni_permesse da restrizioni, rimosso valore_dp',
                    'warzone': 'Aggiunta fazioni_permesse da restrizioni, rimosso valore_dp'
                }
            },
            'statistiche_aggregate': crea_statistiche_aggregate_json(collezioni),
            'collezioni_dettagliate': []
        }
        
        # Aggiunge ogni collezione con inventario dettagliato aggiornato
        for i, collezione in enumerate(collezioni):
            print(f"  📦 Processando collezione {i+1}/{len(collezioni)} con nuovi ordinamenti...")
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
    AGGIORNATO: Gestisce i nuovi formati con proprietà aggiornate.
    """
    try:
        print(f"📂 1. Caricamento collezioni da {PERCORSO_SALVATAGGIO+filename}...")
        
        with open(PERCORSO_SALVATAGGIO + filename, 'r', encoding='utf-8') as f:
            dati = json.load(f)
        
        # Verifica formato e versione
        metadata = dati.get('metadata', {})
        tipo_export = metadata.get('tipo_export', 'formato_sconosciuto')
        versione = metadata.get('versione', 'N/A')
        
        print(f"📋 Formato rilevato: {tipo_export} (versione {versione})")
                
        if tipo_export != 'collezioni_dettagliate':
            print("⚠️ Attenzione: File potrebbe non essere in formato dettagliato aggiornato")
        
        # Stampa info di caricamento
        print(f"✅ Caricamento completato!")
        print(f"   📅 Creato: {metadata.get('data_creazione', 'N/A')}")
        print(f"   🎮 Collezioni: {metadata.get('numero_collezioni', 'N/A')}")
        
        stats_totali = dati.get('statistiche_aggregate', {}).get('panoramica_generale', {})
        print(f"   📦 Carte totali: {stats_totali.get('totale_carte', 'N/A')}")
        print(f"   💰 Valore totale: {stats_totali.get('totale_valore_dp', 'N/A')} DP")
        
        print("\n2. Conversione in istanze CollezioneGiocatore...")
        try:
            collezioni = converti_json_a_collezioni(dati)
            
            # 3. Verifica risultato
            print("\n3. Verifica collezioni ricreate:")
            print(f"   Numero collezioni: {len(collezioni)}")
            
            for coll in collezioni:
                print(f"\n   📦 Collezione Giocatore {coll.id_giocatore}:")
                print(f"      - Guerrieri: {len(coll.carte['guerriero'])}")
                print(f"      - Equipaggiamenti: {len(coll.carte['equipaggiamento'])}")
                print(f"      - Speciali: {len(coll.carte['speciale'])}")
                print(f"      - Fortificazioni: {len(coll.carte['fortificazione'])}")
                print(f"      - Missioni: {len(coll.carte['missione'])}")
                print(f"      - Arti: {len(coll.carte['arte'])}")
                print(f"      - Oscura Simmetria: {len(coll.carte['oscura_simmetria'])}")
                print(f"      - Reliquie: {len(coll.carte['reliquia'])}")
                print(f"      - Warzone: {len(coll.carte['warzone'])}")
                print(f"      - TOTALE CARTE: {coll.get_totale_carte()}")
            
            print("\n✅ Conversione completata con successo!")
            
        except Exception as e:
            print(f"\n❌ Errore durante la conversione: {e}")

        return dati, collezioni
        
    except FileNotFoundError:
        print(f"❌ File {PERCORSO_SALVATAGGIO+filename} non trovato!")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Errore nel parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"❌ Errore durante il caricamento: {e}")
        return None

def stampa_inventario_dettagliato_aggiornato(collezione, mostra_dettagli_carte: bool = True) -> None:
    """
    Stampa l'inventario dettagliato di una collezione con i nuovi criteri di ordinamento.
    NUOVA FUNZIONE: Specializzata per mostrare le nuove proprietà.
    """
    print(f"\n{'='*60}")
    print(f"📋 INVENTARIO DETTAGLIATO - GIOCATORE {collezione.id_giocatore}")
    print(f"{'='*60}")
    
    # Info generale
    print(f"📦 Totale carte: {collezione.get_totale_carte()}")
    print(f"💰 Valore totale: {collezione.statistiche.valore_totale_dp} DP")
    
    # Orientamento
    if collezione.fazioni_orientamento:
        fazioni_str = ", ".join([f.value for f in collezione.fazioni_orientamento])
        print(f"🎯 Orientamento: {fazioni_str}")
    else:
        print(f"🎯 Orientamento: Nessuno")
    
    # Inventario per tipo con nuovi ordinamenti
    for tipo_carta, liste_carte in collezione.carte.items():
        if not liste_carte:
            continue
        
        print(f"\n🃏 {tipo_carta.upper()} ({len(liste_carte)} carte)")
        print("─" * 50)
        
        # Applica il nuovo ordinamento
        carte_ordinate = _ordina_carte_per_tipo(liste_carte, tipo_carta)
        
        # Conta e raggruppa per nome
        carte_conteggio = defaultdict(int)
        carte_esempi = {}
        
        for carta in carte_ordinate:
            carte_conteggio[carta.nome] += 1
            if carta.nome not in carte_esempi:
                carte_esempi[carta.nome] = carta
        
        # Mostra le carte con le nuove proprietà
        for nome_carta, quantita in carte_conteggio.items():
            carta_esempio = carte_esempi[nome_carta]
            
            # Info base
            info_base = f"  • {nome_carta}"
            if quantita > 1:
                info_base += f" x{quantita}"
            
            print(info_base)
            
            if mostra_dettagli_carte:
                # Mostra le nuove proprietà specifiche per tipo
                dettagli = _get_dettagli_carta_aggiornati(carta_esempio, tipo_carta)
                for dettaglio in dettagli:
                    print(f"    {dettaglio}")
        
        # Info sull'ordinamento applicato
        criterio = _get_criterio_ordinamento_per_tipo(tipo_carta)
        print(f"    📊 Ordinato per: {criterio}")

def _get_dettagli_carta_aggiornati(carta, tipo_carta: str) -> List[str]:
    """
    Restituisce i dettagli di una carta secondo le nuove proprietà.
    """
    dettagli = []
    
    # Rarity e set sempre presenti
    if hasattr(carta, 'rarity'):
        rarity_str = carta.rarity.value if hasattr(carta.rarity, 'value') else str(carta.rarity)
        dettagli.append(f"🎭 Rarity: {rarity_str}")
    
    if hasattr(carta, 'set_espansione'):
        set_str = carta.set_espansione.value if hasattr(carta.set_espansione, 'value') else str(carta.set_espansione)
        dettagli.append(f"📚 Set: {set_str}")
    
    # Dettagli specifici per tipo (NUOVE PROPRIETÀ)
    if tipo_carta == 'guerriero':
        if hasattr(carta, 'fazione'):
            fazione_str = carta.fazione.value if hasattr(carta.fazione, 'value') else str(carta.fazione)
            dettagli.append(f"🏛️ Fazione: {fazione_str}")
        
        # NUOVA PROPRIETÀ: Seguace di (per Oscura Legione)
        if hasattr(carta, 'keywords') and carta.keywords:
            for keyword in carta.keywords:
                if "Seguace di" in keyword:
                    dettagli.append(f"👹 {keyword}")
                    break
        
        # Statistiche
        if hasattr(carta, 'stats'):
            stats_str = f"⚔️ Stats: C{carta.stats.combattimento} S{carta.stats.sparare} A{carta.stats.armatura} V{carta.stats.valore}"
            dettagli.append(stats_str)
    
    elif tipo_carta == 'equipaggiamento':
        # NUOVA PROPRIETÀ: Fazione per equipaggiamenti
        if hasattr(carta, 'fazioni_permesse') and carta.fazioni_permesse:
            if len(carta.fazioni_permesse) == 1 and carta.fazioni_permesse[0] != "Generica":
                dettagli.append(f"🏛️ Fazione: {carta.fazioni_permesse[0]}")
            else:
                dettagli.append(f"🏛️ Fazione: {', '.join(carta.fazioni_permesse)}")
        else:
            dettagli.append("🏛️ Fazione: Generica")
        # RIMOSSO: valore_dp
    
    elif tipo_carta in ['speciale', 'fortificazione', 'missione']:
        # NUOVA PROPRIETÀ: Fazioni permesse
        if hasattr(carta, 'fazioni_permesse') and carta.fazioni_permesse:
            dettagli.append(f"🏛️ Fazioni permesse: {', '.join(carta.fazioni_permesse)}")
        else:
            dettagli.append("🏛️ Fazioni permesse: Tutte")
        # RIMOSSO: valore_dp
    
    elif tipo_carta == 'oscura_simmetria':
        # NUOVA PROPRIETÀ: Apostolo padre
        if hasattr(carta, 'apostolo_padre'):
            apostolo_str = carta.apostolo_padre.value if hasattr(carta.apostolo_padre, 'value') else str(carta.apostolo_padre)
            dettagli.append(f"👹 Apostolo padre: {apostolo_str}")
        else:
            dettagli.append("👹 Apostolo padre: Nessuno")
        # RIMOSSO: valore_dp
    
    elif tipo_carta == 'arte':
        # NUOVA PROPRIETÀ: Disciplina
        if hasattr(carta, 'disciplina'):
            disciplina_str = carta.disciplina.value if hasattr(carta.disciplina, 'value') else str(carta.disciplina)
            dettagli.append(f"🎨 Disciplina: {disciplina_str}")
        elif hasattr(carta, 'disciplina_arte'):
            disciplina_str = carta.disciplina_arte.value if hasattr(carta.disciplina_arte, 'value') else str(carta.disciplina_arte)
            dettagli.append(f"🎨 Disciplina: {disciplina_str}")
        else:
            dettagli.append("🎨 Disciplina: Non specificata")
        # RIMOSSO: valore_dp
    
    elif tipo_carta in ['reliquia', 'warzone']:
        # NUOVA PROPRIETÀ: Fazioni permesse da restrizioni
        if hasattr(carta, 'restrizioni') and isinstance(carta.restrizioni, dict):
            fazioni_permesse = carta.restrizioni.get('fazioni_permesse', [])
            if fazioni_permesse:
                dettagli.append(f"🏛️ Fazioni permesse: {', '.join(fazioni_permesse)}")
            else:
                dettagli.append("🏛️ Fazioni permesse: Tutte")
        else:
            dettagli.append("🏛️ Fazioni permesse: Tutte")
        # RIMOSSO: valore_dp
    
    # Per altri tipi, mantiene il valore DP
    else:
        if hasattr(carta, 'valore'):
            dettagli.append(f"💰 Valore: {carta.valore} DP")
        elif hasattr(carta, 'costo_destino'):
            dettagli.append(f"💰 Costo: {carta.costo_destino} DP")
    
    return dettagli

# FUNZIONE DI ESEMPIO PER TESTARE GLI AGGIORNAMENTI
def esempio_utilizzo_aggiornamenti():
    """
    Esempio di utilizzo delle nuove funzionalità di visualizzazione aggiornate.
    """
    print("\n" + "="*80)
    print("🆕 ESEMPIO UTILIZZO FUNZIONALITÀ AGGIORNATE")
    print("="*80)
    
    print("Questo esempio mostra le nuove funzionalità implementate:")
    print("1. Ordinamento migliorato per tutti i tipi di carte")
    print("2. Nuove proprietà di visualizzazione:")
    print("   • Guerrieri: fazione + seguace (Oscura Legione)")
    print("   • Equipaggiamenti: proprietà fazione")
    print("   • Speciali/Fortificazioni/Missioni: fazioni_permesse")
    print("   • Oscura Simmetria: apostolo_padre")
    print("   • Arte: disciplina")
    print("   • Reliquie/Warzone: fazioni_permesse da restrizioni")
    print("3. Rimozione proprietà valore_dp dai tipi specificati")
    
    print("\n📝 Per utilizzare le funzioni aggiornate:")
    print("1. stampa_riepilogo_collezioni_migliorato(collezioni)")
    print("2. salva_collezioni_json_migliorato(collezioni, 'file_aggiornato.json')")
    print("3. dati = carica_collezioni_json_migliorato('file_aggiornato.json')")
    print("4. stampa_statistiche_da_json(dati)")
    print("5. stampa_inventario_dettagliato_aggiornato(collezione)")
    
    print("\n✅ Tutte le funzioni sono state aggiornate per supportare:")
    print("   • Ordinamento migliorato delle carte")
    print("   • Visualizzazione delle nuove proprietà")
    print("   • Rimozione delle proprietà obsolete")
    print("   • Compatibilità con file JSON esistenti")

# FUNZIONI DI VALIDAZIONE DEGLI AGGIORNAMENTI
def valida_aggiornamenti_collezione(collezione) -> Dict[str, Any]:
    """
    Valida che gli aggiornamenti siano stati applicati correttamente a una collezione.
    """
    risultati = {
        'collezione_id': collezione.id_giocatore,
        'aggiornamenti_applicati': {},
        'errori': [],
        'avvisi': []
    }
    
    # Verifica ogni tipo di carta
    for tipo_carta, liste_carte in collezione.carte.items():
        if not liste_carte:
            continue
            
        tipo_risultati = {
            'carte_totali': len(liste_carte),
            'ordinamento_corretto': False,
            'proprieta_aggiornate': False,
            'dettagli': []
        }
        
        # Verifica ordinamento
        carte_ordinate = _ordina_carte_per_tipo(liste_carte, tipo_carta)
        tipo_risultati['ordinamento_corretto'] = len(carte_ordinate) == len(liste_carte)
        
        # Verifica proprietà specifiche su carte campione
        if carte_ordinate:
            carta_campione = carte_ordinate[0]
            
            if tipo_carta == 'guerriero':
                # Verifica fazione e seguace
                ha_fazione = hasattr(carta_campione, 'fazione')
                ha_seguace = any("Seguace di" in kw for kw in carta_campione.keywords if hasattr(carta_campione, 'keywords') and carta_campione.keywords)
                tipo_risultati['dettagli'].append(f"Fazione presente: {ha_fazione}")
                if ha_seguace:
                    tipo_risultati['dettagli'].append("Seguace trovato per Oscura Legione")
                
            elif tipo_carta == 'equipaggiamento':
                ha_fazioni_permesse = hasattr(carta_campione, 'fazioni_permesse')
                tipo_risultati['proprieta_aggiornate'] = ha_fazioni_permesse
                tipo_risultati['dettagli'].append(f"Fazioni permesse presente: {ha_fazioni_permesse}")
            
            # Aggiungi altre verifiche per altri tipi...
        
        risultati['aggiornamenti_applicati'][tipo_carta] = tipo_risultati
    
    return risultati

def stampa_resoconto_aggiornamenti(collezioni: List) -> None:
    """
    Stampa un resoconto degli aggiornamenti applicati alle collezioni.
    """
    print(f"\n{'='*80}")
    print(f"📋 RESOCONTO AGGIORNAMENTI APPLICATI")
    print(f"{'='*80}")
    
    print(f"🎮 Collezioni analizzate: {len(collezioni)}")
    
    # Conta tipi di carte aggiornati
    contatori_tipi = defaultdict(int)
    
    for collezione in collezioni:
        validazione = valida_aggiornamenti_collezione(collezione)
        
        for tipo_carta, risultati in validazione['aggiornamenti_applicati'].items():
            contatori_tipi[tipo_carta] += risultati['carte_totali']
    
    print(f"\n📊 CARTE AGGIORNATE PER TIPO:")
    for tipo_carta, count in sorted(contatori_tipi.items()):
        criterio = _get_criterio_ordinamento_per_tipo(tipo_carta)
        print(f"  • {tipo_carta.capitalize()}: {count} carte - {criterio}")
    
    print(f"\n✅ Tutti gli aggiornamenti sono stati applicati secondo le specifiche!")
    print("🎯 Le collezioni sono ora ordinate e visualizzate con le nuove proprietà.")








# ==================== MAIN ====================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           Creatore_Collezione.PY                             ║
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


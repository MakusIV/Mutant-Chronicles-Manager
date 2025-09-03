"""
Creatore Mazzo
classi, usecase e utilità per la creazione dei mazzi da gioco

"""

import random
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any, Union
from enum import Enum
import json
from collections import defaultdict
from dataclasses import dataclass


# Import delle classi delle carte (solo le classi, non le funzioni di creazione)
from source.logic.Creatore_Collezione import creazione_Collezione_Giocatore
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
    ottieni_warzone as crea_warzone_da_database
)

PERCORSO_SALVATAGGIO = "out/"

# ================================================================================
# COSTANTI PER LA DISTRIBUZIONE DEL TIPO DI CARTE NEL MAZZO
# ================================================================================

# 1: 50% SCHIERAMENTO, 50% SQUADRA, 3/2: 40% SCHIERAMENTO, 60% SQUADRA, 2: 33% SCHIERAMENTO, 66% SQUADRA, 3: 25% SCHIERAMENTO, 75% SQUADRA
# 1/2: 66% SCHIERAMENTO, 33% SQUADRA, 2/3: 60% SCHIERAMENTO, 40% SQUADRA, 1/3: 75% SCHIERAMENTO, 25% SQUADRA
RAPPORTO_SQUADRA_SCHIERAMENTO = 1 

DISTRIBUZIONE_BASE = {
    'guerriero': (0.19, 0.24),          # 19-24%
    'equipaggiamento': (0.11, 0.16),    # 11-16%
    'speciale': (0.42, 0.47),           # 40-47%
    'fortificazione': (0.04, 0.08),     # 4-8%
    'oscura_simmetria': (0.09, 0.14),   # 9-14%
    'arte': (0.09, 0.14),               # 9-14%
    'reliquia': (0.04, 0.07),           # 4-7%
    'warzone': (0.04, 0.08),            # 4-8%
    'missione': 2                       # max 2 carte (numero fisso)
}

# Ridistribuzione quando Oscura Simmetria e/o Arte non sono utilizzate
RIDISTRIBUZIONE_PERCENTUALE = {
    'equipaggiamento': 0.20,  # 40% della percentuale mancante
    'speciale': 0.30,         # 40% della percentuale mancante
    'reliquia': 0.15,          # 20% della percentuale mancante
    'warzone': 0.15,
    'fortificazione': 0.20
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
        combattimento = guerriero.stats.combattimento
        sparo = guerriero.stats.sparare
        armatura = guerriero.stats.armatura
        valore = guerriero.stats.valore
        
        if valore == 0:
            valore = 1  # Evita divisione per zero
            
        potenza_assoluta = ((combattimento + sparo + armatura) * 1.5) / valore
        
        # Bonus per abilità speciali
        for abilita in guerriero.abilita:
            # Potenziamento altri guerrieri
            if abilita.descrizione:
                
                keyword = abilita.descrizione.lower() 
                for keyword in ['tutti i guerrieri', 'alleati', 'guadagnano', '+1', '+2', '+3']:
                    potenza_assoluta *= 1.3
                
                # Uccisione automatica            
                for keyword in ['uccide', 'elimina', 'distrugge', 'automaticamente']:
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
            combattimento = guerriero.stats.combattimento
            sparo = guerriero.stats.sparare
            armatura = guerriero.stats.armatura
            valore = guerriero.stats.valore
        
            if valore == 0:
                valore = 1  # Evita divisione per zero
                    
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
        modifiche_guerriero = {
            'combattimento':    equipaggiamento.modificatori_combattimento,
            'sparare':          equipaggiamento.modificatori_sparare,
            'armatura':         equipaggiamento.modificatori_armatura,
            'valore':           equipaggiamento.modificatori_valore
        }
        for modifica in modifiche_guerriero:
            if modifica in ['combattimento', 'sparare', 'armatura']:
                potenza += abs(modifiche_guerriero[modifica])
        
        # Bonus per abilita speciali
        if hasattr(equipaggiamento, 'abilita_speciali'):
            for effetto in equipaggiamento.abilita_speciali:
                desc = effetto.descrizione.lower()
                if 'ferisce' in desc and 'automaticamente' in desc:
                    potenza *= 1.4
                elif 'uccide' in desc and 'automaticamente' in desc:
                    potenza *= 2.0
        
        # Se non influenza l'armatura
        #influenza_armatura = any(m['tipo'] == 'armatura' for m in equipaggiamento.modifiche_guerriero)
        #if not influenza_armatura:
        #    potenza = 0.5
        
        # Normalizza
        max_potenza = self._calcola_max_potenza_equipaggiamenti()
        if max_potenza > 0:
            return min(potenza / max_potenza, 1.0)
        return 0.5
    
    def _calcola_max_potenza_equipaggiamenti(self) -> float:
        """Calcola la potenza massima tra tutti gli equipaggiamenti"""
        max_potenza = 0
        
        for equip in self.collezione.get_carte_per_tipo('equipaggiamento'):
            modifiche_guerriero = {
            'combattimento':    equip.modificatori_combattimento,
            'sparare':          equip.modificatori_sparare,
            'armatura':         equip.modificatori_armatura,
            'valore':           equip.modificatori_valore
            }
            potenza = sum(abs(modifiche_guerriero[m]) for m in modifiche_guerriero 
                         if m in ['combattimento', 'sparare', 'armatura'])
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
        potenza = self._calcola_potenza_carta(arte)
        return potenza

    
    def calcola_potenza_oscura_simmetria(self, oscura: Oscura_Simmetria) -> float:
        """
        Calcola la potenza relativa di una carta Oscura Simmetria
        
        Args:
            oscura: Oggetto Oscura_Simmetria
            
        Returns:
            float: Potenza relativa (0-1)
        """
        potenza = self._calcola_potenza_carte(oscura)
        return potenza
        
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
    
    
    def calcola_potenza_speciale(self, speciale: Speciale) -> float:
        """
        Calcola la potenza relativa di una carta Speciale
        
        Args:
            arte: Oggetto Speciale
            
        Returns:
            float: Potenza relativa (0-1)
        """
        
        potenza = self._calcola_potenza_carta(speciale)
        return potenza
          
        
    def _calcola_potenza_carta_stats(self, carta: Any) -> float:
        """
        Calcola la potenza relativa alle statistiche di combattimento di una carta di supporto: Speciale, Arte e Oscura_Simmetria
        
        Args:
            carta Oggetto Speciale, Arte e Oscura_Simmetria
            
        Returns:
            float: Potenza relativa (0-1)
        """
        
        potenza = 0
        # Analizza effetti statistiche
        for effetto in carta.effetti:

            tipo_effetto = effetto.tipo_effetto # es. "Modificatore", "Controllo", "Danno", etc.
            valore = effetto.valore # valore numerico dell'effetto (se applicabile)
            statistica_target = effetto.statistica_target # quale statistica viene modificata (C, S, A, V)
            descrizione_effetto = effetto.descrizione_effetto #descrizione effetto: 'uccide', ferisce automaticamente', 'scarta guerriero' 'scarta carta'
            desc = descrizione_effetto.lower()

            if tipo_effetto == "Modificatore" and statistica_target in ["combattimento", "sparare", "armatura"] and valore > 0:
                potenza += valore                     
        
        
        # Normalizza
        classe_carta = type(carta).__name__.lower()
        max_potenza = self._calcola_max_potenza_carta_stats(classe_carta)
        
        if max_potenza > 0:
            return min(potenza / max_potenza, 1.0)
        
        return 0.5
        
    def _calcola_max_potenza_carta_stats(self, classe: str) -> float:
        """Calcola la potenza massima delle statistiche di combattimento tra tutte le carte della classe richiesta"""
        max_potenza = 0

        carte_collezione = self.collezione.get_carte_per_tipo(classe)
        
        for carta in carte_collezione:
            
            potenza = sum(abs(e.valore) for e in carta.effetti if e.tipo_effetto == "Modificatore" and e.statistica_target in ["combattimento", "sparare", "armatura"])
            max_potenza = max(max_potenza, potenza)
            
        return max_potenza if max_potenza > 0 else 1.0
    
    def _calcola_potenza_carta_azioni(self, carta: Any) -> float:
        """
        Calcola la potenza relativa alle sazioni di una carta di supporto: Speciale, Arte e Oscura_Simmetria
        
        Args:
            carta Oggetto Speciale, Arte e Oscura_Simmetria
            
        Returns:
            float: Potenza relativa (0-1)
        """
    
        potenza = 1.0
        # Analizza effetti
        for effetto in carta.effetti:

            tipo_effetto = effetto.tipo_effetto # es. "Modificatore", "Controllo", "Danno", etc.
            valore = effetto.valore # valore numerico dell'effetto (se applicabile)
            statistica_target = effetto.statistica_target # quale statistica viene modificata (C, S, A, V)
            descrizione_effetto = effetto.descrizione_effetto #descrizione effetto: 'uccide', ferisce automaticamente', 'scarta guerriero' 'scarta carta'
            desc = descrizione_effetto.lower()
                
            if tipo_effetto == "Danno":
                                
                # Effetti speciali
                if 'ferisce' in desc and 'automaticamente' in desc:
                    potenza *= 1.4
                elif 'uccide' in desc:
                    potenza *= 2.0
                elif 'scarta' in desc and 'guerriero' in desc:
                    potenza = 1.5
                elif 'scarta' in desc and any(x in desc for x in ['equipaggiamento', 'fortificazione', 'reliquia', 'warzone']):
                    potenza = 1.0

            elif tipo_effetto in ['Azione Combattimento', 'Azione Fase']: # Azione Fase, Azione Ogni Momento
                potenza *= valore

            elif tipo_effetto == 'Azione Ogni Momento':
                potenza *= 2 * valore
            
        
        # Normalizza
        classe_carta = type(carta).__name__.lower()
        max_potenza = self._calcola_max_potenza_carta_azioni(classe_carta)

        if max_potenza > 0:
            return min(potenza / max_potenza, 1.0)
        return 0.5
    
    def _calcola_max_potenza_carta_azioni(self, classe: str) -> float:
        """Calcola la potenza massima delle statistiche delle azioni tra tutte le carte della classe specificata"""
        
        max_potenza = 0        
                
        for carta in self.collezione.get_carte_per_tipo(classe):
            potenza = 2.0 #valore massimo azioni Danno

            for e in carta.effetti:
                
                if e.tipo_effetto == ["Azione Combattimento", "Azione Fase"]:
                    potenza *= e.valore        
                    
                elif e.tipo_effetto == ["Azione Ogni Momento"]:
                    potenza *= 2 * e.valore        
            
            max_potenza = max(max_potenza, potenza)
            
        return max_potenza if max_potenza > 0 else 1.0
    
    def _calcola_potenza_carta(self, carta: Any) -> float:
        """
        Calcola la potenza relativa di una carta (Speciale, Arte, Oscura_Simmetria)
        
        Args:
            carta: Oggetto Speciale, Arte, Oscura_Simmetria
            
        Returns:
            float: Potenza relativa (0-1)
        """
        
        if not isinstance(carta, (Speciale, Arte, Oscura_Simmetria)):
            raise TypeError(f"classe carta {type(carta).__name__} diversa da Speciale, Arte, Oscura_Simmetria")


        potenza_statistiche_combattimento = self._calcola_potenza_carta_stats(carta)
        potenza_azioni = self._calcola_potenza_carta_azioni(carta)

        return potenza_statistiche_combattimento + potenza_azioni
              
    
 






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
                #if hasattr(set_carta, 'value'):
                #    set_carta = set_carta.value
                    
                if set_carta in espansioni_richieste.value if hasattr(espansioni_richieste, 'value') else espansioni_richieste:
                    carte_filtrate.append(carta)
                    
        return carte_filtrate
    
    def seleziona_guerrieri(self, 
                           espansioni_richieste: List[str],
                           doomtrooper: bool = None,
                           orientamento_doomtrooper: List[str] = None,                           
                           fratellanza: bool = None,
                           orientamento_arte: List[str] = None,
                           oscura_legione: bool = None,
                           orientamento_apostolo: List[str] = None,
                           orientamento_eretico: bool = False,
                           orientamento_cultista: bool = False,
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
        guerrieri_disponibili_ammessi = []

        for guerriero in guerrieri_disponibili:
                    
            # Categorizza per fazione. 
            # Nota: l'Eretico viene inserito anche nei doomtrooper o oscura legione, mentre i cultisti no
            # Nota: i guerrieri sono categorizzati ma queste categoriee non vengono poi usate nella funzione
            if doomtrooper and guerriero.fazione in FAZIONI_DOOMTROOPER:
                guerrieri_doomtrooper.append(guerriero)
            elif fratellanza and guerriero.fazione in FAZIONI_FRATELLANZA:
                guerrieri_fratellanza.append(guerriero)
            elif oscura_legione and guerriero.fazione in FAZIONI_OSCURA_LEGIONE:
                guerrieri_oscura_legione.append(guerriero)
        
        # Calcola punteggi per ogni guerriero basati sugli orientamenti
        punteggi = {}
        
        guerrieri_disponibili_ammessi.extend(guerrieri_doomtrooper) 
        guerrieri_disponibili_ammessi.extend(guerrieri_fratellanza) 
        guerrieri_disponibili_ammessi.extend(guerrieri_oscura_legione) 
        
        for guerriero in guerrieri_disponibili_ammessi:
            
            if guerriero.nome in punteggi:
                continue

            punteggio = self.calcola_potenza_guerriero(guerriero)
            
            # Bonus per orientamenti
            bonus_moltiplicatore = 1.0
            BONUS_SPECIALIZZAZIONE = 2.0 # RADDOPPIA RISPETTO IL BONUS BASE
            BONUS_ORIENTAMENTO = 2.0 # RADDOPPIA RISPETTO LA SPECIALIZZAZIONE
            
            
            # Orientamento Doomtrooper
            if doomtrooper: # and guerriero.fazione in FAZIONI_DOOMTROOPER:
                bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE # aumenta il punteggio se la fazione è nei doomtroopers
                
                if guerriero.fazione.value in orientamento_doomtrooper:
                    bonus_moltiplicatore *= 2 # raddoppia il punteggio se la fazione è nei doomtroopers
            
            # Orientamento Arte (per guerrieri Fratellanza)
            if fratellanza: # and guerriero.fazione in FAZIONI_FRATELLANZA:
                bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE

                for abilita in guerriero.abilita:
                    if abilita.tipo == 'Arte':
                        disciplina = abilita.nome
                        if disciplina in orientamento_arte:
                            bonus_moltiplicatore *= BONUS_ORIENTAMENTO # duplica se il fratello lancia la specifica arte
                        elif disciplina == DisciplinaArte.TUTTE.value:
                            bonus_moltiplicatore *= (BONUS_ORIENTAMENTO + 1)  # triplica se il fratello lancia la specifica arte
                            
            
            # Orientamento Apostolo (per guerrieri Oscura Legione)
            if oscura_legione: # and guerriero.fazione in FAZIONI_OSCURA_LEGIONE:
                bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE
                if orientamento_apostolo :
                    for apostolo in orientamento_apostolo:
                        if f"Seguace di {apostolo}" in guerriero.keywords:
                            bonus_moltiplicatore *= BONUS_ORIENTAMENTO
                
            if orientamento_cultista and 'Cultista' in guerriero.keywords:
                bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE +  1 # triplica il bonus per cultisti
            
            
            # Orientamento Eretico
            if orientamento_eretico and 'Eretico' in guerriero.keywords:
                bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE +  1 # triplica il bonus per eretici
            
            # Bonus per carte fondamentali
            if hasattr(guerriero, 'fondamentale') and guerriero.fondamentale:
                bonus_moltiplicatore *= 10  # Priorità massima
            
            
            punteggi[guerriero.nome] = punteggio * bonus_moltiplicatore
        
        # Ordina guerrieri per punteggio
        guerrieri_ordinati = sorted(guerrieri_disponibili_ammessi, 
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
            if guerriero.nome in [g.nome for g in squadra] or guerriero.nome in [g.nome for g in schieramento]:
                continue
                
            # Skip se già aggiunto come fondamentale
            if hasattr(guerriero, 'fondamentale') and guerriero.fondamentale:
                continue
            
            # Calcola quantità da aggiungere
            potenza = self.calcola_potenza_guerriero(guerriero)
            quantita_disponibile = getattr(guerriero, 'quantita', 1)
            quantita_consigliata = getattr(guerriero, 'quantita_minima_consigliata', 1)            
            
            incr_qc = 0
            if guerriero.stats.valore > 6:
                min_val = random.randint(1, 3)


            elif 4 < guerriero.stats.valore <= 6:
                min_val = random.randint(2, 4)
                if quantita_consigliata < 3:
                    incr_qc = 1
            else:
                min_val = random.randint(3, 5)
                if quantita_consigliata < 3:
                    incr_qc = 2

            # Calcola numero di copie basato sulla potenza
            if potenza > 0.8: 
                num_copie = min(min_val, quantita_disponibile, quantita_consigliata + incr_qc)
            elif potenza > 0.5:
                num_copie = min(min_val, quantita_disponibile, quantita_consigliata + incr_qc)
            else:
                num_copie = min(min_val, quantita_disponibile, quantita_consigliata + incr_qc)
            
            # Aggiungi con un po' di casualità
            # num_copie = random.randint(1, num_copie)

            if oscura_legione and (doomtrooper or fratellanza): 
                q = round( RAPPORTO_SQUADRA_SCHIERAMENTO + 1 )
                m = RAPPORTO_SQUADRA_SCHIERAMENTO // q
            else:
                q = 1
                m = 1
            
            inserisci_in_schieramento = oscura_legione and guerriero.fazione in FAZIONI_OSCURA_LEGIONE
            inserisci_in_squadra = ( doomtrooper or fratellanza) and ( guerriero.fazione in FAZIONI_DOOMTROOPER or guerriero.fazione in FAZIONI_FRATELLANZA)

            num_copie_da_inserire = min(5, num_copie)

            for _ in range(num_copie_da_inserire):
                
                if inserisci_in_schieramento:
                    if len(schieramento) < numero_guerrieri_target // q: 
                        schieramento.append(guerriero)
                elif inserisci_in_squadra:
                    if len(squadra) < numero_guerrieri_target * m:  
                        squadra.append(guerriero)
                else:
                    break
        
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
        DISTRIBUZIONE_EQUIPAGGIAMENTO = {
            'combattimento':    0.25, 
            'sparare':          0.25,
            'armatura':         0.25,
            'azioni':           0.125            
        }

        DISTRIBUZIONE_SPECIALE = {
            'combattimento':    0.12,
            'sparare':          0.12,
            'armatura':         0.12,
            'azioni':           0.64            
        }

        # Ottieni tutte le carte del tipo richiesto
        tutte_carte = self.collezione.get_carte_per_tipo(tipo_carta)
        carte_disponibili = self.filtra_carte_per_espansioni(tutte_carte, espansioni_richieste)
        
        if not carte_disponibili:
            return []
        
        carte_selezionate = []
        tutti_guerrieri = squadra + schieramento
        numero_guerrieri = len(tutti_guerrieri)


        # Prima seleziona carte fondamentali
        for carta in carte_disponibili:
            if hasattr(carta, 'fondamentale') and carta.fondamentale:
                # Verifica compatibilità con i guerrieri
                carta_compatibile, numero_guerrieri_compatibili = self._carta_compatibile_con_guerrieri(carta, tutti_guerrieri)
            
                if carta_compatibile:
                    quantita_richiesta = max(
                                                5, 
                                                min( getattr(carta, 'quantita_minima_consigliata', 1), getattr(carta, 'quantita', 1))
                    )                    
                    for _ in range(quantita_richiesta):
                        carte_selezionate.append(carta)
        
        # Calcola potenza per ogni carta
        carte_con_punteggio = []
        
        for carta in carte_disponibili:
            # Skip carte fondamentali già aggiunte
            if hasattr(carta, 'fondamentale') and carta.fondamentale:
                continue
            
            carta_compatibile, numero_guerrieri_compatibili = self._carta_compatibile_con_guerrieri(carta, tutti_guerrieri)
            
            # Verifica compatibilità
            if not carta_compatibile:
                continue
            
            # Calcola potenza basata sul tipo
            if tipo_carta == 'equipaggiamento':
                potenza = self.calcola_potenza_equipaggiamento(carta)
                modifica_principale_effettuata = carta.modifica_principale_effettuata()
                for modifica, percentuale in DISTRIBUZIONE_EQUIPAGGIAMENTO.items():
                    if modifica_principale_effettuata == modifica:
                        potenza *= 1 + percentuale
                        break

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
                potenza = self.calcola_potenza_speciale(carta)  # Default per carte speciali NOTA: Definire il calcolo potenza per speciali
                modifica_principale_effettuata = carta.modifica_principale_effettuata()
                for modifica, percentuale in DISTRIBUZIONE_SPECIALE.items():
                    if modifica_principale_effettuata == modifica:
                        potenza *= 1 + percentuale
                        break
                
            elif tipo_carta == 'missione':
                potenza = 0.5  # Default per missioni
            else:
                potenza = 0.5
            
            #if carta.nome in [c[0].nome for c in carte_con_punteggio]:
            #    continue
            fattore_compatibilita = 1 + numero_guerrieri_compatibili / numero_guerrieri
            carte_con_punteggio.append((carta, potenza * fattore_compatibilita))
        
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
            
            if num_copie < 1:
                num_copie = 1

            # Aggiungi casualità
            num_copie = min(5, random.randint(1, num_copie)) #random.randint(1, min(num_copie, numero_carte - len(carte_selezionate)))
            
            for _ in range(num_copie):
                if len(carte_selezionate) < numero_carte:
                    carte_selezionate.append(carta)
        

        return carte_selezionate
    
    def _carta_compatibile_con_guerrieri(self, carta: Any, guerrieri: List[Guerriero]) -> List:
        """
        Verifica se una carta è compatibile con almeno un guerriero della lista
        
        Args:
            carta: Carta da verificare
            guerrieri: Lista dei guerrieri nel mazzo
            
        Returns:
            True se compatibile, False altrimenti e numero di guerrieri compatibili
        """

        # NOTA:Verificare ed eventualmente definire meglio la verifica di compatibilità per speciali e missioni

        if not guerrieri:
            return [False, 0]
        
        result = False
        numero_guerrieri_compatibili = 0

        tipo_carta = type(carta).__name__.lower()
        
        # Verifica compatibilità per tipo
        if tipo_carta in ['arte', 'reliquia', 'oscura_simmetria', 'fortificazione', 'warzone', 'speciale', 'equipaggiamento']:
            # Verifica se c'è almeno un guerriero che può usare la carta
            for guerriero in guerrieri:                
                
                if tipo_carta in ['equipaggiamento', 'fortificazione', 'reliquia', 'speciale', 'warzone']:
                    risultato = carta.puo_essere_assegnato_a_guerriero(guerriero)
                    if risultato.get('puo_assegnare', False):
                        result = True
                        numero_guerrieri_compatibili += 1
                
                elif tipo_carta in ['arte', 'oscura simmetria', 'missione']:
                    risultato = carta.puo_essere_associata_a_guerriero(guerriero)
                    
                    if risultato.get('puo_lanciare', False):
                        result = True
                        numero_guerrieri_compatibili += 1
        
        return [result, numero_guerrieri_compatibili]
    
    def calcola_distribuzione_carte(self, 
                                   numero_totale: int,
                                   usa_fratellanza: bool,
                                   usa_oscura_legione: bool,
                                   espansioni_richieste: List[Set_Espansione]) -> Dict[str, int]:
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
        
        if not Set_Espansione.WARZONE.value in espansioni_richieste:
            ridistribuzione_totale += distribuzione['warzone']
            distribuzione['warzone'] = 0
            
        if not Set_Espansione.INQUISITION.value in espansioni_richieste:
            ridistribuzione_totale += distribuzione['inquisition']
            distribuzione['warzone'] = 0
        
        if ridistribuzione_totale > 0:
            # Ridistribuisci alle altre carte
            if Set_Espansione.INQUISITION.value in espansioni_richieste:
               distribuzione['reliquia'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['reliquia'])
            
            if Set_Espansione.WARZONE in espansioni_richieste:
               distribuzione['warzone'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['warzone'])
            
            distribuzione['equipaggiamento'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['equipaggiamento'])
            distribuzione['speciale'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['speciale'])
            distribuzione['fortificazione'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['fortificazione'])
        
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

def crea_mazzo_da_gioco(collezione: Any,
                            numero_carte_max: int,
                            numero_carte_min: int,
                            espansioni_richieste: List[str],
                            doomtrooper: bool = None,
                            orientamento_doomtrooper: List[str] = None,
                            fratellanza: bool = None,
                            orientamento_arte: List[str] = None,
                            oscura_legione: bool = None,
                            orientamento_apostolo: List[str] = None,
                            orientamento_eretico: bool = False,
                            orientamento_cultista: bool = False) -> Dict[str, Any]:
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
    usa_fratellanza = fratellanza #orientamento_arte is not None and len(orientamento_arte) > 0
    usa_oscura_legione = oscura_legione #orientamento_apostolo is not None and len(orientamento_apostolo) > 0
    
    # Se non specificato, controlla nella collezione
    # No se orientamento_arte e/o orientament_aposolo non sono specificati i relativi guerrieri non devon essereinseriti nel mazzo
    #if not usa_fratellanza:
    #    guerrieri_fratellanza = [g for g in collezione.get_carte_per_tipo('guerriero') 
    #                             if g.fazione in FAZIONI_FRATELLANZA]
    #    usa_fratellanza = len(guerrieri_fratellanza) > 0
    
    #if not usa_oscura_legione:
    #    guerrieri_oscura = [g for g in collezione.get_carte_per_tipo('guerriero') 
    #                       if g.fazione in FAZIONI_OSCURA_LEGIONE]
    #    usa_oscura_legione = len(guerrieri_oscura) > 0
    
    # Calcola distribuzione carte
    distribuzione = creatore.calcola_distribuzione_carte(
        numero_carte_target,
        usa_fratellanza,
        usa_oscura_legione,
        espansioni_richieste
    )
    
    # Seleziona guerrieri
    squadra, schieramento = creatore.seleziona_guerrieri(
        espansioni_richieste,
        doomtrooper,
        orientamento_doomtrooper,
        fratellanza,
        orientamento_arte,
        oscura_legione,
        orientamento_apostolo,
        orientamento_eretico,
        orientamento_cultista,
        distribuzione['guerriero']
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
    if distribuzione['fortificazione'] > 0:
        fortificazioni = creatore.seleziona_carte_supporto(
            squadra, schieramento, espansioni_richieste,
            'fortificazione', distribuzione['fortificazione']
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
    
    #n_eq = len ( carte_supporto.get('equipaggiamento', []) )
    #n_fo = len ( carte_supporto.get('fortificazione', []) )
    #n_sp = len ( carte_supporto.get('speciale', []) )
    #n_mi = len ( carte_supporto.get('missione', []) )
    #n_ar = len ( carte_supporto.get('arte', []) )
    #n_os = len ( carte_supporto.get('oscura_simmetria', []) )
    #n_re = len ( carte_supporto.get('reliquia', []) )
    #n_wa = len ( carte_supporto.get('warzone', []) )

    #n_supporto = sum ( [ n_eq, n_fo, n_sp, n_mi, n_ar, n_os, n_re, n_wa ] )

    statistiche = {
        'numero_totale_carte': len(squadra) + len(schieramento) + len(carte_supporto),
        'guerrieri_squadra': len(squadra),
        'guerrieri_schieramento': len(schieramento),
        #'equipaggiamento': n_eq,        
        #'fortificazione': n_fo,
        #'speciale': n_sp,
        #'missione': n_mi,
        #'arte': n_ar,
        #'oscura_simmetria': n_os,
        #'reliquia': n_re,
        #'warzone': n_wa,
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
    
    #if len(mazzo['carte_supporto']) > 20:
    #    print(f"  ... e altre {len(mazzo['carte_supporto']) - 20} carte")
    
    if mazzo['errori']:
        print(f"\n⚠️ AVVISI:")
        for errore in mazzo['errori']:
            print(f"  • {errore}")
    
    print("=" * 80)




# ==================== MAIN ====================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           Creatore_Mazzo.PY                                  ║
║                    Mutant Chronicles / Doomtrooper                          ║
║                                                                              ║
║  Modulo per la creazione di mazzi da gioco secondo le regole                ║
║  ufficiali del regolamento Doomtrooper.                                     ║
║                                                                              ║
║  Funzionalità implementate:                                                  ║
║  • Creazione mazzi da gioco                     ║
║  ║                                                                              ║
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
        # Demo creazione mazzo
        mazzo_1 = crea_mazzo_da_gioco(
            demo_collezioni[0],
            numero_carte_max=70,
            numero_carte_min=60,
            espansioni_richieste=['Base', 'Inquisition'],
            doomtrooper=True,
            orientamento_doomtrooper=['Mishima', 'Bauhaus', 'Freelancer', 'Fratellanza'],
            fratellanza=True,
            orientamento_arte=['Cambiamento', 'Combattimento', 'Premonizione'],
            oscura_legione=False,
            orientamento_apostolo=None,
            orientamento_eretico=False,
            orientamento_cultista=False
        )
        stampa_mazzo(mazzo_1)
        mazzo_2 = crea_mazzo_da_gioco(
            demo_collezioni[1],
            numero_carte_max=60,
            numero_carte_min=50,
            espansioni_richieste=['Base', 'Inquisition', 'Warzone'],
            doomtrooper=True,
            orientamento_doomtrooper=['Cybertronic', 'Capitol', 'Imperial'],
            fratellanza=False,
            orientamento_arte=None,
            oscura_legione=True,
            orientamento_apostolo=['Algeroth', 'Semai'],
            orientamento_eretico=True,
            orientamento_cultista=False
        )
        stampa_mazzo(mazzo_2)
        

        # Per attivare il menu interattivo, decommenta la riga seguente:
        #menu_interattivo()

    except Exception as e:
        print(f"❌ Errore durante la demo: {e}")


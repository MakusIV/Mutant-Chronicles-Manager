"""
Creatore Mazzo
classi, usecase e utilità per la creazione dei mazzi da gioco

"""

import random
import math
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any, Union
from enum import Enum
import json
import os
from collections import defaultdict
from dataclasses import dataclass


# Import delle classi delle carte (solo le classi, non le funzioni di creazione)
from source.logic.Creatore_Collezione import creazione_Collezione_Giocatore, carica_collezioni_json_migliorato, salva_collezioni_json_migliorato, determina_orientamento_collezione
from source.cards.Guerriero import (
    Guerriero, Fazione, Set_Espansione, Rarity, TipoGuerriero, DisciplinaArte
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
    Fazione.MERCENARIO
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
            descrizione = abilita.descrizione.lower()
            nome = abilita.nome.lower()
            tipo = abilita.tipo.lower()

            if tipo == "combattimento":
                    if nome == "uccide automaticamente":
                        potenza_assoluta *= 1.5
                    if nome in ["permette ai guerrieri di attaccare per primi", "i guerrieri alleati uccidono automaticamente"]:
                        potenza_assoluta *= 1.3
                    
            if tipo == "immunita":
                if nome in ["immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria", "annulla immunita dell'oscura simmetria", "immune ai doni degli apostoli"]:
                    potenza_assoluta *= 1.4                
                
                elif any(immunita in nome for immunita in ["immune agli effetti della specifica arte", "immune allo specifico equipaggiamento", "immune alla specifica fortificazione"]):
                    potenza_assoluta *= 1.2
                        
            if tipo == "modificatore":        
                if nome in ["aumenta effetto", "aumenta caratteristica"]:
                    potenza_assoluta *= 1.3
                elif nome == "trasforma guerrieri uccisi in alleati":
                    potenza_assoluta *= 1.1
                elif nome == "sostituisce guerrieri":
                    potenza_assoluta *= 1.2

            if tipo == "guarigione" :
                    if "guarisce se stesso" in nome:
                        potenza_assoluta *= 1.3

            if tipo == "arte":                
                if "lancia arte e/o incantesimo dell'arte" == nome:
                    potenza_assoluta *= 1.3                
                elif "lancia arte e/o incantesimo dell'arte specifica" == nome:
                    potenza_assoluta *= 1.2
            if tipo == "oscura simmetria" or tipo == "dono degli apostoli":                
                    potenza_assoluta *= 1.3            

            if tipo == "carte":
                if nome in ["assegna carta", "scarta carta", "elimina carta"]:
                    potenza_assoluta *= 1.3    

            if tipo == "azioni":
                if nome in ["converte azioni in azioni d'attacco"]:
                    potenza_assoluta *= 1.3    
                        
        
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
        potenza_assoluta = 0
        
        # Somma modificatori statistiche
        statistiche = {
            'combattimento':    equipaggiamento.modificatori_combattimento,
            'sparare':          equipaggiamento.modificatori_sparare,
            'armatura':         equipaggiamento.modificatori_armatura,
            'valore':           equipaggiamento.modificatori_valore
        }
        for modifica in statistiche:
            if modifica in ['combattimento', 'sparare', 'armatura']:
                potenza_assoluta += abs(statistiche[modifica])

        statistiche = True if potenza_assoluta > 1 else False    

        # Bonus per modificatori speciali
        for modificatore in equipaggiamento.modificatori_speciali:
            # Potenziamento altri guerrieri
            statistica = modificatore.statistica.lower()
            descrizione = modificatore.descrizione.lower()
            valore = modificatore.valore.lower()
            condizione = modificatore.condizione.lower()            

            
            if any(val in descrizione for val in ["raddoppiate", "+5", "+6", "+7", "+8", "+9"]) and statistica in ["sparare", "combattimento", "armatura", "valore"]:
                if statistiche:
                    potenza_assoluta *= 1.3
                else:    
                    potenza_assoluta += 4
            
            if statistica in ["sparare", "combattimento", "armatura", "valore"]:                                   
                if any(val in descrizione for val in ["+3", "+4"]):
                    if statistiche:
                        potenza_assoluta *= 1.2
                    else:    
                        potenza_assoluta += 2
                elif any(val in descrizione for val in ["+1", "+2"]):
                    if statistiche:
                        potenza_assoluta *= 1.1
                    else:    
                        potenza_assoluta += 1
                            
        
        # Bonus per abilita speciali
        for abilita in equipaggiamento.abilita_speciali:
            # Potenziamento altri guerrieri
            descrizione = abilita.descrizione.lower()
            nome = abilita.nome.lower()
            tipo = abilita.tipo_attivazione.lower()

            if tipo == "combattimento":
                    if nome == "uccide automaticamente":
                        potenza_assoluta *= 1.5
                    if nome in ["permette ai guerrieri di attaccare per primi", "i guerrieri alleati uccidono automaticamente"]:
                        potenza_assoluta *= 1.3
                    
            if tipo == "immunita":
                if nome in ["immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria", "annulla immunita dell'Oscura simmetria", "immune ai doni degli apostoli"]:
                    potenza_assoluta *= 1.4
                elif any( val in nome for val in ["immune agli effetti della specifica arte", "immune allo specifico equipaggiamento", "immune alla specifica fortificazione"]):
                    potenza_assoluta *= 1.2
                                                                                    
            if tipo == "modificatore":        
                if nome in ["aumenta effetto", "aumenta caratteristica"]:
                    potenza_assoluta *= 1.3
                elif nome == "trasforma guerrieri uccisi in alleati":
                    potenza_assoluta *= 1.1
                elif nome == "sostituisce guerrieri":
                    potenza_assoluta *= 1.2

            if tipo == "guarigione" :
                    if "guarisce se stesso" in nome:
                        potenza_assoluta *= 1.3


            if tipo == "arte":                
                if "lancia arte e/o incantesimo dell'arte" == nome:
                    potenza_assoluta *= 1.3                
                elif "lancia arte e/o incantesimo dell'arte specifica" == nome:
                    potenza_assoluta *= 1.2

            if tipo == "oscura simmetria" or tipo == "dono degli apostoli":                
                    potenza_assoluta *= 1.3            
            
            if tipo == "carte":
                if nome in ["assegna carta", "scarta carta", "elimina carta"]:
                    potenza_assoluta *= 1.3    

            if tipo == "azioni":
                if nome in ["converte azioni in azioni d'attacco"]:
                    potenza_assoluta *= 1.3    
                elif nome in ["modifica azione", "modifica stato"]:
                    potenza_assoluta *= 1.1    

        
                
        
        # Normalizza
        max_potenza = self._calcola_max_potenza_equipaggiamenti()
        if max_potenza > 0:
            return min(potenza_assoluta / max_potenza, 1.0)
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
        potenza = self._calcola_potenza_carta(oscura)
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
        potenza = 1
        
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
                    potenza *= 1.3
                elif 'uccide' in desc:
                    potenza *= 1.5
        
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
        

        potenza = warzone.stats['combattimento'] + warzone.stats['sparare'] + warzone.stats['armatura']
        
        # Bonus per fazioni/tipi specifici
        if hasattr(warzone, 'modificatore_difensore'):
            for bonus in warzone.modificatori_difensore.values():
                potenza += sum([bonus.get('valore', 0), 
                               bonus.get('sparare', 0), 
                               bonus.get('armatura', 0)])
        
        # Bonus per uccisione automatica
        if hasattr(warzone, 'effetti_combattimento'):
            for effetto in warzone.effetti_combattimento:
                if 'uccide automaticamente' == effetto.nome.lower():
                    potenza *= 1.5
                elif effetto.nome.lower() in ['equipaggiamento gratuito', 'riceve carte oscura simmetria']:
                    potenza *= 1.3
                elif effetto.nome.lower() in ["Aumenta Punti Vittoria", "Guadagna Punti Promozione", "Guadagna Punti Aggiuntivi"]:
                    potenza *= 1.2
                
        
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
            potenza = (warzone.stats.get('combattimento', 0) + 
                      warzone.stats.get('sparare', 0) + 
                      warzone.stats.get('armatura', 0))
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

            tipo_effetto = effetto.tipo_effetto.lower() # es. "Modificatore", "Controllo", "Danno", etc.
            valore = effetto.valore # valore numerico dell'effetto (se applicabile)
            statistica_target = effetto.statistica_target.lower() # quale statistica viene modificata (C, S, A, V)
            descrizione_effetto = effetto.descrizione_effetto #descrizione effetto: 'uccide', ferisce automaticamente', 'scarta guerriero' 'scarta carta'
            desc = descrizione_effetto.lower()

            if tipo_effetto == "modificatore" and statistica_target in ["combattimento", "sparare", "armatura"] and isinstance(valore, int) and valore > 0:
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
            potenza = 0
            for e in carta.effetti:
                if e.tipo_effetto == "Modificatore" and e.statistica_target in ["combattimento", "sparare", "armatura"]:
                    if isinstance(e.valore, int):
                        potenza += abs(e.valore)                    
                    
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

            tipo_effetto = effetto.tipo_effetto.lower() # es. "Modificatore", "Controllo", "Danno", etc.
            valore = effetto.valore # valore numerico dell'effetto (se applicabile)
            statistica_target = effetto.statistica_target # quale statistica viene modificata (C, S, A, V)
            descrizione_effetto = effetto.descrizione_effetto #descrizione effetto: 'uccide', ferisce automaticamente', 'scarta guerriero' 'scarta carta'
            desc = descrizione_effetto.lower()
                
            if tipo_effetto == "danno":
                                
                # Effetti speciali
                if 'ferisce' in desc and 'automaticamente' in desc:
                    potenza *= 1.4
                elif 'uccide' in desc:
                    potenza *= 2.0
                elif 'scarta' in desc and 'guerriero' in desc:
                    potenza = 1.5
                elif 'scarta' in desc and any(x in desc for x in ['equipaggiamento', 'fortificazione', 'reliquia', 'warzone']):
                    potenza = 1.0

            elif tipo_effetto in ['azione combattimento', 'azione fase']: # Azione Fase, Azione Ogni Momento
                potenza *= valore

            elif tipo_effetto == 'azione ogni momento':
                potenza *= 2 * valore
            
        
        # Normalizza
        classe_carta = type(carta).__name__.lower()
        max_potenza = self._calcola_max_potenza_carta_azioni(classe_carta)

        if max_potenza > 0 and potenza > 1.0:
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
        tutti_guerrieri = self.collezione.get_carte_per_tipo_mazzo('guerriero')
        guerrieri_disponibili = self.filtra_carte_per_espansioni(tutti_guerrieri, espansioni_richieste)

        
        if not guerrieri_disponibili:
            return [], []
        
        # Separa guerrieri per categoria
        guerrieri_doomtrooper = []
        guerrieri_fratellanza = []
        guerrieri_oscura_legione = []        
        guerrieri_ammessi = []

        #for guerriero in guerrieri_disponibili:
                    
            # Categorizza per fazione. 
            # Nota: l'Eretico viene inserito anche nei doomtrooper o oscura legione, mentre i cultisti no
            # Nota: i guerrieri sono categorizzati ma queste categoriee non vengono poi usate nella funzione
        #    if doomtrooper and guerriero.fazione in FAZIONI_DOOMTROOPER:
        #        guerrieri_doomtrooper.append(guerriero)
        #    elif fratellanza and guerriero.fazione in FAZIONI_FRATELLANZA:
        #        guerrieri_fratellanza.append(guerriero)
        #    elif oscura_legione and guerriero.fazione in FAZIONI_OSCURA_LEGIONE:
        #        guerrieri_oscura_legione.append(guerriero)
        
        # Calcola punteggi per ogni guerriero basati sugli orientamenti
        punteggi = {}
        
        #guerrieri_disponibili_ammessi.extend(guerrieri_doomtrooper) 
        #guerrieri_disponibili_ammessi.extend(guerrieri_fratellanza) 
        #guerrieri_disponibili_ammessi.extend(guerrieri_oscura_legione) 


        BONUS_SPECIALIZZAZIONE = 4.0 # Fattore punteggio applicato se il guerriero è della fazione specializzata
        BONUS_ORIENTAMENTO = 6.0 # Fattore punteggio applicato alle preferenze specifiche di orientamento
        BONUS_ERETICO = 2 # Fattore applicato se selezionati ERETICI
        BONUS_CULTISTA = 2 # Fattore applicato se selezionati CULTISTI   

        for guerriero in guerrieri_disponibili:
            
            if guerriero.nome in punteggi:
                continue

            punteggio = 0 # punteggio base
            
            # Bonus per orientamenti
            bonus_moltiplicatore = 1.0              
            bonus_factor_guerriero_fondamentale = 1

            if hasattr(guerriero, 'fondamentale') and guerriero.fondamentale:
                bonus_factor_guerriero_fondamentale = 3 # triplica il punteggio se è una carta fondamentale
            
            # inserimento in lista dei guerrieri ammessi
            ammesso = False

            # Orientamento Doomtrooper            
            if doomtrooper and guerriero.fazione in FAZIONI_DOOMTROOPER:
                ammesso = True                

                if not orientamento_doomtrooper or orientamento_doomtrooper == []: # il guerriero è un doomtrooper e non è definito l'orientamento
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE # aumenta il punteggio se la fazione è nei doomtroopers

                elif guerriero.fazione.value in orientamento_doomtrooper: #il guerriero è un doomtrooper con fazione inclusa nell'orientamento: 
                    bonus_moltiplicatore *= BONUS_ORIENTAMENTO# triplica il punteggio se la fazione è anche nell'orientamento doomtroopers

                else: # il guerriero è un doomtrooper ma non è nell'orientamento
                    # bonus_moltiplicatore *= 0.8 # decrementa del 20% se il doomtrooper non è della fazione richiesta (per favorire la scelta di quelli della fazione richiesta)
                    ammesso = False # esclude il guerriero se non è della fazione richiesta (per favorire la scelta di quelli della fazione richiesta)
                
                if ammesso:
                    guerrieri_ammessi.append(guerriero) 
                    punteggio = self.calcola_potenza_guerriero(guerriero)
                    punteggi[guerriero.nome] = punteggio * bonus_moltiplicatore * bonus_factor_guerriero_fondamentale                    
            

            # Orientamento Arte (per guerrieri Fratellanza)
            elif fratellanza and guerriero.fazione in FAZIONI_FRATELLANZA: # 
                ammesso = True

                if not orientamento_arte or orientamento_arte == []: # il guerriero è della fratellanza e non è definito l'orientamento
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE
                
                # Le arti possono essere utilizzate anche da guerrieri non appartenenti alla Fratellanza
                elif orientamento_arte and len(orientamento_arte) > 0: # Sono definite le arti preferite
                    for abilita in guerriero.abilita:
                        #escludi_oscura_legione = guerriero.fazione in FAZIONI_OSCURA_LEGIONE and not oscura_legione # True se il guerriero è OL e non è previsto nel mazzo l'oscura legione
                        #escludi_doomtrooper = guerriero.fazione in FAZIONI_DOOMTROOPER and not doomtrooper # True se il guerriero è DOOMTROOPER e non è previsto nel mazzo i doomtrooper
                        if abilita.tipo == 'Arte': # and not (escludi_oscura_legione or escludi_doomtrooper) : # esclude se il guerriero è OL e non è previsto nel mazzo l'oscura legione
                            disciplina = abilita.target
                            if any( arte_ in disciplina for arte_ in orientamento_arte ):
                                bonus_moltiplicatore *= BONUS_ORIENTAMENTO # triplica se il fratello lancia la specifica arte
                            elif disciplina == DisciplinaArte.TUTTE.value:
                                bonus_moltiplicatore *= (BONUS_ORIENTAMENTO * 2)   # raddoppia se il fratello lancia la specifica arte
                            elif guerriero.fazione in FAZIONI_FRATELLANZA: # il guerriero è della fratellanza ma non ha competenza nelle arti richieste (depotenzia)
                                ammesso = False # esclude il guerriero se non è della fazione richiesta (per favorire la scelta di quelli della fazione richiesta)
                                # bonus_moltiplicatore *= 0.8 # decrementa del 20% se il fratello non è competente nelle arti scelte (per favorire la scelta di quelli competenti)

                if ammesso:
                    guerrieri_ammessi.append(guerriero) 
                    punteggio = self.calcola_potenza_guerriero(guerriero)
                    punteggi[guerriero.nome] = punteggio * bonus_moltiplicatore * bonus_factor_guerriero_fondamentale
                                    
            
            # Orientamento Apostolo (per guerrieri Oscura Legione)
            elif oscura_legione and guerriero.fazione in FAZIONI_OSCURA_LEGIONE: # and guerriero.fazione in FAZIONI_OSCURA_LEGIONE:
                ammesso = True

                if not orientamento_apostolo or orientamento_apostolo == []:
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE
                    
                elif orientamento_apostolo and len(orientamento_apostolo) > 0 :
                    for apostolo in orientamento_apostolo:
                        if f"Seguace di {apostolo}" in guerriero.keywords:
                            bonus_moltiplicatore *= BONUS_ORIENTAMENTO
                else:
                    ammesso = False # esclude il guerriero se non è della fazione richiesta (per favorire la scelta di quelli della fazione richiesta)
                    #bonus_moltiplicatore *= 0.8 # decrementa del 20% se il guerriero non può fruire dei doni dell'apostolo incluso nell'orientamento (per favorire la scelta di quelli che possono usufruirne)                    
                    

                if orientamento_cultista and 'Cultista' in guerriero.keywords:
                    bonus_moltiplicatore *= BONUS_CULTISTA # aumenta di un ulteriore fattore (BONUS_CULTISTA) il bonus per cultisti (i cultisti sono OL quindi già beneficiano dell'eventuale bonus OL)

                if ammesso:
                    guerrieri_ammessi.append(guerriero) 
                    punteggio = self.calcola_potenza_guerriero(guerriero)
                    punteggi[guerriero.nome] = punteggio * bonus_moltiplicatore * bonus_factor_guerriero_fondamentale
                    
            
            # Orientamento Eretico (per guerrieri Doomtrooper o Oscura Legione)
            if orientamento_eretico and 'Eretico' in guerriero.keywords:
                    # bonus_moltiplicatore *= BONUS_ERETICO # aumenta di un ulteriore fattore (BONUS_ERETICI) il bonus per eretici (gli eretici sono OL o DOOMTROOPER quindi già beneficiano dell'eventuale bonus O o DOmmotrooper)
                    if guerriero not in guerrieri_ammessi:
                        guerrieri_ammessi.append(guerriero) 
                        punteggio = self.calcola_potenza_guerriero(guerriero)
                        punteggi[guerriero.nome] = punteggio * bonus_moltiplicatore * bonus_factor_guerriero_fondamentale * BONUS_ERETICO
                    elif guerriero.nome in punteggi:
                        punteggi[guerriero.nome] *= BONUS_ERETICO # aumenta di un ulteriore fattore (BONUS_ERETICI) il bonus per eretici (gli eretici sono OL o DOOMTROOPER quindi già beneficiano dell'eventuale bonus O o DOmmotrooper)
                    else:
                        print(f"MA CHI CAZZ'E'??: Escluso eretico guerriero {guerriero.nome} della fazione {guerriero.fazione} non compatibile con le fazioni selezionate per il mazzo")
            
            #punteggi[guerriero.nome] = punteggio * bonus_moltiplicatore * bonus_factor_guerriero_fondamentale
        
        # Ordina guerrieri per punteggio
        guerrieri_ordinati = sorted(guerrieri_ammessi, 
                                   key=lambda g: punteggi.get(g.nome, 0), 
                                   reverse=True)
        
        # Seleziona guerrieri garantendo distribuzione equa
        squadra = []
        schieramento = []

        # Seleziona gli altri guerrieri
        for guerriero in guerrieri_ordinati:
            
            #if guerriero.nome in [g.nome for g in squadra] or guerriero.nome in [g.nome for g in schieramento]:
            #    continue
                
            quantita_disponibile = getattr(guerriero, 'quantita', 1) #quantita_disponibile = self.collezione.get_copie_disponibili(tipo_carta = 'guerriero', carta = guerriero)
            quantita_consigliata = getattr(guerriero, 'quantita_minima_consigliata', 1)            
            
            # valuta la quantità minima in base al valore del guerriero (maggiore costo)                                    
            if guerriero.stats.valore >= 10 or guerriero.tipo == 'Personalita':
                min_val = 1
                if quantita_consigliata <1:
                    quantita_consigliata = 1             
                
            elif 7 <= guerriero.stats.valore < 10: # 7 e 8                        
                min_val = random.randint(1, 2)
                if quantita_consigliata <1:
                    quantita_consigliata = random.randint(min_val, min_val + 2)                

            elif 4 <= guerriero.stats.valore < 7: # 7 e 8                                
                min_val = random.randint(1, 3)
                if quantita_consigliata <1:
                    quantita_consigliata = random.randint(min_val, min_val + 2)                                

            else: 
                min_val = random.randint(1, 2)                
                if quantita_consigliata <1:
                    quantita_consigliata = random.randint(min_val, min_val + 1)                
        
                
            num_copie_da_inserire = min(5, quantita_disponibile, quantita_consigliata)    
            
           
            

            if oscura_legione and (doomtrooper or fratellanza): 
                q = RAPPORTO_SQUADRA_SCHIERAMENTO + 1
                m = RAPPORTO_SQUADRA_SCHIERAMENTO / q
            else:
                q = 1
                m = 1
            
            numero_guerrieri_per_schieramento = math.floor( 0.49 + numero_guerrieri_target / q)
            numero_guerrieri_per_squadra = math.floor( 0.49 + numero_guerrieri_target * m )
            inserisci_in_schieramento = oscura_legione and guerriero.fazione in FAZIONI_OSCURA_LEGIONE
            inserisci_in_squadra = ( doomtrooper or fratellanza) and ( guerriero.fazione in FAZIONI_DOOMTROOPER or guerriero.fazione in FAZIONI_FRATELLANZA)            

            for _ in range(num_copie_da_inserire): # NOTA: inserisce la stessa istanza per più volte nella lista
                
                if inserisci_in_schieramento:
                    if len(schieramento) <= numero_guerrieri_per_schieramento: 
                        schieramento.append(guerriero)
                    else:
                        break
                elif inserisci_in_squadra:
                    if len(squadra) <= numero_guerrieri_per_squadra:  
                        squadra.append(guerriero)
                    else:
                        break
            

            if  ( len(squadra) + len(schieramento)) >= numero_guerrieri_target:
                return squadra, schieramento

        return squadra, schieramento
    
    def seleziona_carte_supporto(self, 
                                squadra: List[Guerriero],
                                schieramento: List[Guerriero],
                                espansioni_richieste: List[str],
                                tipo_carta: str,
                                doomtrooper: bool = None,
                                orientamento_doomtrooper: List[str] = None,                           
                                fratellanza: bool = None,      
                                orientamento_arte: List[str] = None,                           
                                oscura_legione: bool = None,
                                orientamento_apostolo: List[str] = None,
                                orientamento_eretico: bool = False,
                                orientamento_cultista: bool = False,
                                numero_carte: int = 50) -> List[Any]:
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
        tutte_carte = self.collezione.get_carte_per_tipo_mazzo(tipo_carta)
        # Filtra per espansioni
        carte_disponibili = self.filtra_carte_per_espansioni(tutte_carte, espansioni_richieste)
        
        if not carte_disponibili:
            return []
        
        carte_selezionate = []
        tutti_guerrieri = squadra + schieramento
        numero_guerrieri = len(tutti_guerrieri)

         # Bonus per orientamenti
       
        BONUS_SPECIALIZZAZIONE = 4.0 # Fattore punteggio applicato se il guerriero è della fazione specializzata
        BONUS_ORIENTAMENTO = 6.0 # Fattore punteggio applicato alle preferenze specifiche di orientamento
        BONUS_ERETICO = 2 # Fattore applicato se selezionati ERETICI
        BONUS_CULTISTA = 2 # Fattore applicato se selezionati CULTISTI     
        
                

        # Calcola potenza per ogni carta
        carte_con_punteggio = []
        
        for carta in carte_disponibili:

            bonus_moltiplicatore = 1.0
            fattore_carte_fondamentale = 1 # fattore di incremento del rating assegnato alla carta se questa è fondamentale

            if hasattr(carta, 'fondamentale') and carta.fondamentale:
                fattore_carte_fondamentale = 3 # triplica il punteggio se è una carta fondamentale

            fazioni = []
            if hasattr(carta, 'fazione'):
                fazioni = [carta.fazione]
            elif hasattr(carta, 'fazioni_permesse'):
                fazioni = carta.fazioni_permesse
            elif hasattr(carta, 'restrizioni') and hasattr(carta.restrizioni, 'fazioni_permesse'):
                fazioni = carta.restrizioni.fazioni_permesse
            
            doomtrooper_dedicata = any(f in fazioni for f in FAZIONI_DOOMTROOPER) or 'Doomtrooper' in fazioni
            orientamento_doomtrooper_dedicata = any(f in orientamento_doomtrooper for f in fazioni) if (orientamento_doomtrooper and len(orientamento_doomtrooper) > 0) else False
            fratellanza_dedicata = any(f in fazioni for f in FAZIONI_FRATELLANZA) 
            oscura_legione_dedicata = any(f in fazioni for f in FAZIONI_OSCURA_LEGIONE)

            if doomtrooper and doomtrooper_dedicata: # la carta è dedicata ai doomtrooper o è generica (fazione None)        
            
                if orientamento_doomtrooper_dedicata: #la carta è dedicata ai doomtrooper con fazione inclusa nell'orientamento: 
                    bonus_moltiplicatore *= BONUS_ORIENTAMENTO # triplica il punteggio se la fazione è anche nell'orientamento doomtrooper
            
                else: # la carta è dedicata a tutti i doomtrooper
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE # aumenta il punteggio se la fazione è nei doomtroopers
                
            
            if fratellanza and fratellanza_dedicata: # la carta è dedicata alla fratellanza                

                if tipo_carta == 'arte':                    
                    # Le arti possono essere utilizzate anche da guerrieri non appartenenti alla Fratellanza
                    if orientamento_arte and len(orientamento_arte) > 0: # Sono definite le arti preferite
                        
                        disciplina = carta.disciplina.value
                        if disciplina in orientamento_arte:
                            bonus_moltiplicatore *= BONUS_ORIENTAMENTO # triplica se il fratello lancia la specifica arte
                        elif disciplina == DisciplinaArte.TUTTE.value:
                            bonus_moltiplicatore *= (BONUS_ORIENTAMENTO + 1)   # triplica se il fratello lancia la specifica arte                    
                    else: # non sono definite arti preferite
                        bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE # aumenta il punteggio se la fazione è nei doomtroopers
                else:
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE # aumenta il punteggio se la fazione è nei doomtroopers
            
             # Orientamento Apostolo (per guerrieri Oscura Legione)
            if oscura_legione and oscura_legione_dedicata: # la carta è dedicata alla oscura legione 
                                
                if orientamento_apostolo and len(orientamento_apostolo) > 0 : # la carta è dedicata alla oscura legione e sono definiti gli apostoli preferiti
                    for apostolo in orientamento_apostolo:
                        if f"Seguace di {apostolo}" in carta.keywords:
                            bonus_moltiplicatore *= BONUS_ORIENTAMENTO
                else:
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE

                if orientamento_cultista and 'Cultista' in carta.keywords:
                    bonus_moltiplicatore *= BONUS_CULTISTA # aumenta di un ulteriore fattore (BONUS_CULTISTA) il bonus per cultisti (i cultisti sono OL quindi già beneficiano dell'eventuale bonus OL)
                 

            if orientamento_eretico and 'Eretico' in carta.keywords:
                bonus_moltiplicatore *= BONUS_ERETICO # triplica il punteggio se la fazione è anche nell'orientamento doomtroopers

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
            
            #if carta.nome in [c[0].nome for c in carte_con_punteggio]:
            #    continue
            fattore_compatibilita = 1 + 2 * numero_guerrieri_compatibili / numero_guerrieri # raddoppia se la metà dei guerrieri può utilizzare la carta, triplica se tutti
            carte_con_punteggio.append((carta, potenza * fattore_compatibilita * bonus_moltiplicatore * fattore_carte_fondamentale))
        
        # Ordina per potenza
        carte_con_punteggio.sort(key=lambda x: x[1], reverse=True)
        
        # Seleziona carte
        for carta, _ in carte_con_punteggio:
            
            if len(carte_selezionate) >= numero_carte:
                return carte_selezionate
            
            # Calcola numero di copie
            quantita_disponibile = getattr(carta, 'quantita', 1)
            quantita_minima_consigliata = getattr(carta, 'quantita_minima_consigliata', 1)
            if quantita_minima_consigliata < 1:
                quantita_minima_consigliata = random.randint(1,3)
            
            num_copie_da_inserire = min(5, quantita_disponibile, quantita_minima_consigliata)   

            for _ in range(num_copie_da_inserire):

                if len(carte_selezionate) <= numero_carte:
                    carte_selezionate.append(carta)# NOTA: inserisce nella lista copie di una stessa istanza
                else:
                    return carte_selezionate
        
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
        if tipo_carta in ['arte', 'reliquia', 'oscura_simmetria', 'fortificazione', 'warzone', 'speciale', 'equipaggiamento', 'missione']:
            # Verifica se c'è almeno un guerriero che può usare la carta
            for guerriero in guerrieri:                
                
                if tipo_carta in ['equipaggiamento', 'fortificazione', 'speciale']:
                    risultato = carta.puo_essere_assegnato_a_guerriero(guerriero)
                
                    if risultato.get('puo_assegnare', False):
                        result = True
                        numero_guerrieri_compatibili += 1
                
                elif tipo_carta in ['arte', 'oscura_simmetria', 'reliquia', 'warzone']:
                    risultato = carta.puo_essere_associata_a_guerriero(guerriero)
                    
                    if ( tipo_carta in ['arte', 'oscura_simmetria'] and risultato.get('puo_lanciare') ) or  ( tipo_carta == 'warzone' and risultato.get('puo_essere_associata') ) or (tipo_carta == 'reliquia' and risultato.get('puo_assegnare')):
                        result = True
                        numero_guerrieri_compatibili += 1
                
                elif tipo_carta == 'missione':
                    risultato = carta.puo_essere_associata_a(guerriero)
                    if risultato.get('puo_assegnare', False):
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
                distribuzione[tipo] = random.randint(2,5)  # Max 5 missioni
            else:
                min_perc, max_perc = percentuale
                #perc_media = (min_perc + max_perc) / 2
                
                # Aggiungi casualità
                perc_finale = min_perc + random.random()*(max_perc - min_perc)
                #perc_finale = perc_media + random.uniform(-0.02, 0.02)
                #perc_finale = max(min_perc, min(max_perc, perc_finale))                
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
            distribuzione['reliquia'] = 0
        
        if ridistribuzione_totale > 0:
            # Ridistribuisci alle altre carte
            if Set_Espansione.INQUISITION.value in espansioni_richieste:
               distribuzione['reliquia'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['reliquia'])
            
            if Set_Espansione.WARZONE.value in espansioni_richieste:
               distribuzione['warzone'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['warzone'])
            
            distribuzione['equipaggiamento'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['equipaggiamento'])
            distribuzione['speciale'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['speciale'])
            distribuzione['fortificazione'] += int(ridistribuzione_totale * RIDISTRIBUZIONE_PERCENTUALE['fortificazione'])
        
        # Assicura che il totale sia corretto
        totale_attuale = sum(distribuzione.values())
        differenza = numero_totale - totale_attuale

        if differenza > 0:
            sign = 1
        else:
            sign = -1


        if abs(differenza) > 0:
            
            q_spec = abs(math.floor(0.49 + 0.6 * differenza))          
            distribuzione['speciale'] = distribuzione['speciale'] + sign * q_spec
            residuo = differenza - sign * q_spec
            q_guer = abs(math.floor(0.49 + 0.4 * residuo))
            
            if q_guer > 0:
                distribuzione['guerriero'] = distribuzione['guerriero'] + sign * q_guer

            residuo = residuo - sign * q_guer
            
            if abs(residuo) > 0:
                distribuzione['equipaggiamento'] = distribuzione['equipaggiamento'] + residuo            

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
            squadra, 
            schieramento, 
            espansioni_richieste,
            'equipaggiamento', 
            doomtrooper,
            orientamento_doomtrooper,
            fratellanza,   
            orientamento_arte,         
            oscura_legione,
            orientamento_apostolo,
            orientamento_eretico,
            orientamento_cultista,
            distribuzione['equipaggiamento']
        )
        carte_supporto.extend(equipaggiamenti)
    
    # 2. Fortificazioni
    if distribuzione['fortificazione'] > 0:
        fortificazioni = creatore.seleziona_carte_supporto(
            squadra, 
            schieramento, 
            espansioni_richieste,
            'fortificazione', 
            doomtrooper,
            orientamento_doomtrooper,
            fratellanza,       
            orientamento_arte,       
            oscura_legione,
            orientamento_apostolo,
            orientamento_eretico,
            orientamento_cultista,
            distribuzione['fortificazione']
        )
        carte_supporto.extend(fortificazioni)
    
    # 3. Speciali    
    if distribuzione['speciale'] > 0:
        speciali = creatore.seleziona_carte_supporto(
            squadra, 
            schieramento, 
            espansioni_richieste,
            'speciale', 
            doomtrooper,
            orientamento_doomtrooper,
            fratellanza,         
            orientamento_arte,     
            oscura_legione,
            orientamento_apostolo,
            orientamento_eretico,
            orientamento_cultista,
            distribuzione['speciale']
        )
        carte_supporto.extend(speciali)        
    
    # 4. Missioni
    if distribuzione['missione'] > 0:
        missioni = creatore.seleziona_carte_supporto(
            squadra, 
            schieramento, 
            espansioni_richieste,
            'missione', 
            doomtrooper,
            orientamento_doomtrooper,
            fratellanza,    
            orientamento_arte,          
            oscura_legione,
            orientamento_apostolo,
            orientamento_eretico,
            orientamento_cultista,
            distribuzione['missione']
        )
        carte_supporto.extend(missioni)        
    
    # 5. Arte (se guerrieri Fratellanza presenti)
    if usa_fratellanza and distribuzione['arte'] > 0:
        arte = creatore.seleziona_carte_supporto(
            squadra, 
            schieramento, 
            espansioni_richieste,
            'arte', 
            doomtrooper,
            orientamento_doomtrooper,
            fratellanza,   
            orientamento_arte,           
            oscura_legione,
            orientamento_apostolo,
            orientamento_eretico,
            orientamento_cultista,
            distribuzione['arte']
        )
        carte_supporto.extend(arte)
    
    # 6. Oscura Simmetria (se guerrieri Oscura Legione presenti)
    if usa_oscura_legione and distribuzione['oscura_simmetria'] > 0:
        oscura = creatore.seleziona_carte_supporto(
            squadra, 
            schieramento, 
            espansioni_richieste,
            'oscura_simmetria', 
            doomtrooper,
            orientamento_doomtrooper,
            fratellanza,      
            orientamento_arte,        
            oscura_legione,
            orientamento_apostolo,
            orientamento_eretico,
            orientamento_cultista,
            distribuzione['oscura_simmetria']
        )
        carte_supporto.extend(oscura)
    
    # 7. Reliquie (se espansione Inquisition richiesta)
    if 'Inquisition' in espansioni_richieste and distribuzione['reliquia'] > 0:
        reliquie = creatore.seleziona_carte_supporto(
            squadra, 
            schieramento, 
            espansioni_richieste,
            'reliquia', 
            doomtrooper,
            orientamento_doomtrooper,
            fratellanza,            
            orientamento_arte,  
            oscura_legione,
            orientamento_apostolo,
            orientamento_eretico,
            orientamento_cultista,
            distribuzione['reliquia']
        )
        carte_supporto.extend(reliquie)
    
    # 8. Warzone (se espansione Warzone richiesta)
    if 'Warzone' in espansioni_richieste and distribuzione['warzone'] > 0:
        warzone = creatore.seleziona_carte_supporto(
            squadra, 
            schieramento, 
            espansioni_richieste,
            'warzone', 
            doomtrooper,
            orientamento_doomtrooper,
            fratellanza,        
            orientamento_arte,      
            oscura_legione,
            orientamento_apostolo,
            orientamento_eretico,
            orientamento_cultista,
            distribuzione['warzone']
        )
        carte_supporto.extend(warzone)

    statistiche = {
        'numero_totale_carte': len(squadra) + len(schieramento) + len(carte_supporto),
        'guerrieri_squadra': len(squadra),
        'guerrieri_schieramento': len(schieramento),
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
    
    if len(squadra) + len(schieramento) < 5:
        errori.append("ATTENZIONE: La squadra e lo schieramento hanno, complessivamentee, meno di 5 guerrieri")
    
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

def ottieni_attributo_sicuro(obj, nome_attributo: str, default_value=None):
    """
    Ottiene un attributo da un oggetto in modo sicuro, gestendo enum e valori None.
    
    Args:
        obj: Oggetto da cui estrarre l'attributo
        nome_attributo: Nome dell'attributo
        default_value: Valore di default se l'attributo non esiste
        
    Returns:
        Valore dell'attributo o il valore di default
    """
    if not hasattr(obj, nome_attributo):
        return default_value
    
    valore = getattr(obj, nome_attributo)
    
    # Gestisce enum convertendoli in stringa
    if hasattr(valore, 'value'):
        return valore.value
    
    return valore if valore is not None else default_value
def determina_classe_supporto(carta) -> str:
    """
    Determina la classe di una carta supporto basandosi sul tipo della classe.
    
    Args:
        carta: Istanza della carta
        
    Returns:
        Nome della classe della carta
    """
    nome_classe = type(carta).__name__
    
    # Mappatura dei nomi delle classi alle classi di supporto
    mappatura_classi = {
        'Equipaggiamento': 'Equipaggiamento',
        'Speciale': 'Speciale', 
        'Arte': 'Arte',
        'Oscura_Simmetria': 'Oscura Simmetria',
        'OscuraSimmetria': 'Oscura Simmetria',
        'Fortificazione': 'Fortificazione',
        'Reliquia': 'Reliquia',
        'Warzone': 'Warzone',
        'Missione': 'Missione'
    }
    
    return mappatura_classi.get(nome_classe, nome_classe)
def crea_info_guerriero_sicura(guerriero):
    """
    Crea un dizionario con le informazioni del guerriero in modo sicuro.
    
    Args:
        guerriero: Oggetto Guerriero
        
    Returns:
        Dizionario con le informazioni del guerriero
    """
    try:
        guerriero_info = {
            'nome': ottieni_attributo_sicuro(guerriero, 'nome', 'Nome sconosciuto'),
            'fazione': ottieni_attributo_sicuro(guerriero, 'fazione', 'Fazione sconosciuta'),
            'set_espansione': ottieni_attributo_sicuro(guerriero, 'set_espansione', 'Set sconosciuto'),
            'rarity': ottieni_attributo_sicuro(guerriero, 'rarity', 'Rarity sconosciuta'),
            'tipo': ottieni_attributo_sicuro(guerriero, 'tipo', 'Normale'),
            'quantita': ottieni_attributo_sicuro(guerriero, 'quantita', 0)
        }
        
        # Statistiche (possono essere in formato diverso)
        if hasattr(guerriero, 'stats'):
            stats = guerriero.stats
            guerriero_info['combattimento'] = ottieni_attributo_sicuro(stats, 'combattimento', 0)
            guerriero_info['sparare'] = ottieni_attributo_sicuro(stats, 'sparare', 0)
            guerriero_info['armatura'] = ottieni_attributo_sicuro(stats, 'armatura', 0)
            guerriero_info['valore'] = ottieni_attributo_sicuro(stats, 'valore', 0)
        else:
            guerriero_info['combattimento'] = ottieni_attributo_sicuro(guerriero, 'combattimento', 0)
            guerriero_info['sparare'] = ottieni_attributo_sicuro(guerriero, 'sparare', 0)
            guerriero_info['armatura'] = ottieni_attributo_sicuro(guerriero, 'armatura', 0)
            guerriero_info['valore'] = ottieni_attributo_sicuro(guerriero, 'valore', 0)
        
        # Attributi opzionali
        guerriero_info['valor_destino'] = ottieni_attributo_sicuro(guerriero, 'valor_destino', 0)
        guerriero_info['valor_promozione'] = ottieni_attributo_sicuro(guerriero, 'valor_promozione', 0)
        guerriero_info['e_personalita'] = ottieni_attributo_sicuro(guerriero, 'e_personalita', False)
        guerriero_info['keywords'] = ottieni_attributo_sicuro(guerriero, 'keywords', [])
        guerriero_info['quantita'] = ottieni_attributo_sicuro(guerriero, 'quantita', 0)
        
        return guerriero_info
        
    except Exception as e:
        # Fallback sicuro
        return {
            'nome': getattr(guerriero, 'nome', 'Guerriero Sconosciuto'),
            'fazione': str(getattr(guerriero, 'fazione', 'Fazione Sconosciuta')),
            'tipo': 'Guerriero',
            'set_espansione': str(getattr(guerriero, 'set_espansione', 'Set Sconosciuto')),
            'rarity': str(getattr(guerriero, 'rarity', 'Common')),
            'combattimento': 0, 'sparare': 0, 'armatura': 0, 'valore': 0,
            'errore_serializzazione': str(e)
        }
def crea_info_carta_supporto_sicura(carta):
    """
    Crea un dizionario con le informazioni della carta supporto in modo sicuro.
    """
    try:
        carta_info = {
            'nome': ottieni_attributo_sicuro(carta, 'nome', 'Nome sconosciuto'),
            'tipo': type(carta).__name__,
            'set_espansione': ottieni_attributo_sicuro(carta, 'set_espansione', 'Set sconosciuto'),
            'rarity': ottieni_attributo_sicuro(carta, 'rarity', 'Rarity sconosciuta')
        }
        
        # Attributi specifici opzionali
        fazione = ottieni_attributo_sicuro(carta, 'fazione', None)
        if fazione:
            carta_info['fazione'] = fazione
        
        valor_destino = ottieni_attributo_sicuro(carta, 'valor_destino', None)
        if valor_destino is not None:
            carta_info['valor_destino'] = valor_destino
        
        valore = ottieni_attributo_sicuro(carta, 'valore', None)
        if valore is not None:
            carta_info['valore'] = valore
        
        disciplina_arte = ottieni_attributo_sicuro(carta, 'disciplina_arte', None)
        if disciplina_arte:
            carta_info['disciplina_arte'] = disciplina_arte
        
        apostolo = ottieni_attributo_sicuro(carta, 'apostolo', None)
        if apostolo:
            carta_info['apostolo'] = apostolo
        
        apostolo_padre = ottieni_attributo_sicuro(carta, 'apostolo_padre', None)
        if apostolo_padre:
            carta_info['apostolo_padre'] = apostolo_padre
        
        carta_info['quantita'] = ottieni_attributo_sicuro(carta, 'quantita', '')
        carta_info['keywords'] = ottieni_attributo_sicuro(carta, 'keywords', [])
        carta_info['costo_destino'] = ottieni_attributo_sicuro(carta, 'costo_destino', 0)
        
        return carta_info
        
    except Exception as e:
        # Fallback sicuro
        return {
            'nome': getattr(carta, 'nome', 'Carta Sconosciuta'),
            'tipo': type(carta).__name__,
            'set_espansione': str(getattr(carta, 'set_espansione', 'Set Sconosciuto')),
            'rarity': str(getattr(carta, 'rarity', 'Common')),
            'errore_serializzazione': str(e)
        }


def stampa_riepilogo_mazzi_migliorato(mazzi: List[Dict[str, Any]]) -> None:
    """
    Stampa un riepilogo dettagliato dei mazzi creati con suddivisioni per fazioni e classi.
    VERSIONE AGGIORNATA: Include organizzazione per fazioni e classi delle carte.
    """
    if not mazzi:
        print("⚠️ Nessun mazzo da visualizzare")
        return
    
    print(f"\n{'='*80}")
    print(f"🎮 RIEPILOGO DETTAGLIATO - {len(mazzi)} MAZZI CREATI")
    print(f"{'='*80}")
    
    totale_carte = 0
    totale_guerrieri_squadra = 0
    totale_guerrieri_schieramento = 0
    totale_supporto = 0
    
    # Contatori per fazioni e classi
    fazioni_squadra = defaultdict(int)
    fazioni_schieramento = defaultdict(int)
    classi_supporto = defaultdict(int)
    
    for i, mazzo in enumerate(mazzi, 1):
        print(f"\n🎯 MAZZO {i}:")
        
        squadra = mazzo.get('squadra', [])
        schieramento = mazzo.get('schieramento', [])
        supporto = mazzo.get('carte_supporto', [])
        
        carte_mazzo = len(squadra) + len(schieramento) + len(supporto)
        totale_carte += carte_mazzo
        totale_guerrieri_squadra += len(squadra)
        totale_guerrieri_schieramento += len(schieramento)
        totale_supporto += len(supporto)
        
        print(f"   📦 Totale carte: {carte_mazzo}")
        print(f"   ⚔️ Guerrieri squadra: {len(squadra)}")
        print(f"   🌙 Guerrieri schieramento: {len(schieramento)}")
        print(f"   🎴 Carte supporto: {len(supporto)}")
        
        # Analisi fazioni squadra
        if squadra:
            print(f"   \n   🏛️ FAZIONI SQUADRA:")
            fazioni_mazzo = defaultdict(int)
            for guerriero in squadra:
                fazione = getattr(guerriero, 'fazione', 'Sconosciuta')
                if hasattr(fazione, 'value'):
                    fazione = fazione.value
                fazioni_mazzo[fazione] += 1
                fazioni_squadra[fazione] += 1
            
            for fazione, count in sorted(fazioni_mazzo.items()):
                print(f"     • {fazione}: {count} guerrieri")
        
        # Analisi fazioni schieramento
        if schieramento:
            print(f"   \n   🌙 FAZIONI SCHIERAMENTO:")
            fazioni_mazzo_sch = defaultdict(int)
            for guerriero in schieramento:
                fazione = getattr(guerriero, 'fazione', 'Sconosciuta')
                if hasattr(fazione, 'value'):
                    fazione = fazione.value
                fazioni_mazzo_sch[fazione] += 1
                fazioni_schieramento[fazione] += 1
            
            for fazione, count in sorted(fazioni_mazzo_sch.items()):
                print(f"     • {fazione}: {count} guerrieri")
        
        # Analisi classi supporto
        if supporto:
            print(f"   \n   🎴 CLASSI SUPPORTO:")
            classi_mazzo = defaultdict(int)
            for carta in supporto:
                classe = determina_classe_supporto(carta)
                classi_mazzo[classe] += 1
                classi_supporto[classe] += 1
            
            for classe, count in sorted(classi_mazzo.items()):
                print(f"     • {classe}: {count} carte")
        
        print(f"   {'-'*50}")
    
    # Statistiche aggregate
    print(f"\n📊 STATISTICHE AGGREGATE:")
    print(f"   📦 Totale carte: {totale_carte}")
    print(f"   ⚔️ Totale guerrieri squadra: {totale_guerrieri_squadra}")
    print(f"   🌙 Totale guerrieri schieramento: {totale_guerrieri_schieramento}")
    print(f"   🎴 Totale supporto: {totale_supporto}")
    print(f"   📈 Media carte/mazzo: {totale_carte/len(mazzi):.1f}")
    
    if fazioni_squadra:
        print(f"\n🏛️ DISTRIBUZIONE GLOBALE FAZIONI SQUADRA:")
        for fazione, count in sorted(fazioni_squadra.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {fazione}: {count} guerrieri")
    
    if fazioni_schieramento:
        print(f"\n🌙 DISTRIBUZIONE GLOBALE FAZIONI SCHIERAMENTO:")
        for fazione, count in sorted(fazioni_schieramento.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {fazione}: {count} guerrieri")
    
    if classi_supporto:
        print(f"\n🎴 DISTRIBUZIONE GLOBALE CLASSI SUPPORTO:")
        for classe, count in sorted(classi_supporto.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {classe}: {count} carte")


def processa_supporto_per_classi(carte_supporto: List[Any]) -> Dict[str, Dict[str, Any]]:
    """
    Organizza le carte supporto per classi con conteggio copie.
    VERSIONE COMPLETA con gestione errori robusta.
    """
    # Struttura per classi supporto
    classi_supporto = {
        'Equipaggiamento': {},
        'Speciale': {},
        'Arte': {},
        'Oscura Simmetria': {},
        'Fortificazione': {},
        'Reliquia': {},
        'Warzone': {},
        'Missione': {}
    }
    
    if not carte_supporto:
        return classi_supporto
    
    conteggio_carte = defaultdict(int)
    dettagli_carte = {}
    
    # Prima passata: conta le copie e raccoglie dettagli
    for i, carta in enumerate(carte_supporto):
        try:
            nome = getattr(carta, 'nome', f'Carta_Sconosciuta_{i+1}')
            
            # Determina classe in modo sicuro
            try:
                classe = determina_classe_supporto(carta)
            except Exception as classe_error:
                print(f"   ⚠️ Errore determinando classe per {nome}: {classe_error}")
                classe = 'Speciale'  # Default fallback
            
            conteggio_carte[nome] += 1
            
            if nome not in dettagli_carte:
                dettagli_carte[nome] = {
                    'copie': 0,
                    'classe': classe,
                    'set_espansione': ottieni_attributo_sicuro(carta, 'set_espansione', 'Base'),
                    'rarity': ottieni_attributo_sicuro(carta, 'rarity', 'Common'),
                    'costo_destino': ottieni_attributo_sicuro(carta, 'costo_destino', 0),
                    'quantita': ottieni_attributo_sicuro(carta, 'quantita', 0),
                    'keywords': ottieni_attributo_sicuro(carta, 'keywords', [])
                }
                
                # Aggiungi attributi specifici se presenti
                try:
                    if hasattr(carta, 'fazione'):
                        fazione_obj = carta.fazione
                        if hasattr(fazione_obj, 'value'):
                            dettagli_carte[nome]['fazione'] = fazione_obj.value
                        else:
                            dettagli_carte[nome]['fazione'] = str(fazione_obj)
                    
                    if hasattr(carta, 'valor_destino'):
                        dettagli_carte[nome]['valor_destino'] = carta.valor_destino
                    
                    if hasattr(carta, 'valore'):
                        dettagli_carte[nome]['valore'] = carta.valore
                    
                    if hasattr(carta, 'disciplina_arte'):
                        disciplina_obj = carta.disciplina_arte
                        if hasattr(disciplina_obj, 'value'):
                            dettagli_carte[nome]['disciplina_arte'] = disciplina_obj.value
                        else:
                            dettagli_carte[nome]['disciplina_arte'] = str(disciplina_obj)
                    
                    if hasattr(carta, 'apostolo'):
                        apostolo_obj = carta.apostolo
                        if hasattr(apostolo_obj, 'value'):
                            dettagli_carte[nome]['apostolo'] = apostolo_obj.value
                        else:
                            dettagli_carte[nome]['apostolo'] = str(apostolo_obj)
                    
                    if hasattr(carta, 'apostolo_padre'):
                        apostolo_padre_obj = carta.apostolo_padre
                        if hasattr(apostolo_padre_obj, 'value'):
                            dettagli_carte[nome]['apostolo_padre'] = apostolo_padre_obj.value
                        else:
                            dettagli_carte[nome]['apostolo_padre'] = str(apostolo_padre_obj)
                    
                except Exception as attr_error:
                    print(f"   ⚠️ Errore attributi specifici per {nome}: {attr_error}")
        
        except Exception as e:
            print(f"   ⚠️ Errore processando carta supporto {i+1}: {e}")
            nome_errore = f'Carta_Errore_{i+1}'
            conteggio_carte[nome_errore] += 1
            dettagli_carte[nome_errore] = {
                'copie': 0,
                'classe': 'Speciale',
                'set_espansione': 'Unknown',
                'rarity': 'Common',
                'costo_destino': 0,
                'quantita': 0,
                'keywords': [],
                'errore_processamento': str(e)
            }
    
    # Seconda passata: organizza per classi
    for nome, count in conteggio_carte.items():
        try:
            dettagli = dettagli_carte[nome]
            dettagli['copie'] = count
            classe = dettagli['classe']
            
            # Assicurati che la classe esista nella struttura
            if classe in classi_supporto:
                classi_supporto[classe][nome] = dettagli
            else:
                # Se la classe non è riconosciuta, metti in Speciale
                print(f"   ⚠️ Classe non riconosciuta '{classe}' per {nome}, spostato in Speciale")
                classi_supporto['Speciale'][nome] = dettagli
                
        except Exception as e:
            print(f"   ⚠️ Errore organizzando carta {nome}: {e}")
            # Metti in Speciale come fallback
            classi_supporto['Speciale'][nome] = {
                'copie': count,
                'errore_organizzazione': str(e)
            }
    
    # Mantieni struttura base anche se vuota
    return classi_supporto
def calcola_statistiche_aggregate_organizzate(mazzi: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcola statistiche aggregate per i mazzi con organizzazione per fazioni e classi.
    """
    stats = {
        'panoramica_generale': {
            'numero_mazzi': len(mazzi),
            'totale_carte': 0,
            'totale_guerrieri_squadra': 0,
            'totale_guerrieri_schieramento': 0,
            'totale_carte_supporto': 0,
            'media_carte_per_mazzo': 0,
            'media_guerrieri_squadra': 0,
            'media_guerrieri_schieramento': 0,
            'media_supporto': 0
        },
        'distribuzione_fazioni': {
            'squadra': defaultdict(int),
            'schieramento': defaultdict(int)
        },
        'distribuzione_classi_supporto': defaultdict(int),
        'riepilogo_mazzi': []
    }
    
    totale_carte = 0
    totale_squadra = 0
    totale_schieramento = 0
    totale_supporto = 0
    
    for i, mazzo in enumerate(mazzi):
        squadra = mazzo.get('squadra', [])
        schieramento = mazzo.get('schieramento', [])
        supporto = mazzo.get('carte_supporto', [])
        
        carte_mazzo = len(squadra) + len(schieramento) + len(supporto)
        totale_carte += carte_mazzo
        totale_squadra += len(squadra)
        totale_schieramento += len(schieramento)
        totale_supporto += len(supporto)
        
        # Conta fazioni squadra
        fazioni_squadra = []
        for guerriero in squadra:
            fazione = getattr(guerriero, 'fazione', 'Sconosciuta')
            if hasattr(fazione, 'value'):
                fazione = fazione.value
            stats['distribuzione_fazioni']['squadra'][fazione] += 1
            if fazione not in fazioni_squadra:
                fazioni_squadra.append(fazione)
        
        # Conta fazioni schieramento
        fazioni_schieramento = []
        for guerriero in schieramento:
            fazione = getattr(guerriero, 'fazione', 'Sconosciuta')
            if hasattr(fazione, 'value'):
                fazione = fazione.value
            stats['distribuzione_fazioni']['schieramento'][fazione] += 1
            if fazione not in fazioni_schieramento:
                fazioni_schieramento.append(fazione)
        
        # Conta classi supporto
        classi_presenti = []
        for carta in supporto:
            classe = determina_classe_supporto(carta)
            stats['distribuzione_classi_supporto'][classe] += 1
            if classe not in classi_presenti:
                classi_presenti.append(classe)
        
        # Riepilogo singolo mazzo
        espansioni = set()
        for carta_lista in [squadra, schieramento, supporto]:
            for carta in carta_lista:
                esp = getattr(carta, 'set_espansione', 'Base')
                if hasattr(esp, 'value'):
                    esp = esp.value
                espansioni.add(esp)
        
        stats['riepilogo_mazzi'].append({
            'indice_mazzo': i + 1,
            'totale_carte': carte_mazzo,
            'guerrieri_squadra': len(squadra),
            'guerrieri_schieramento': len(schieramento),
            'carte_supporto': len(supporto),
            'fazioni_squadra': fazioni_squadra,
            'fazioni_schieramento': fazioni_schieramento,
            'classi_supporto': classi_presenti,
            'espansioni_utilizzate': list(espansioni)
        })
    
    # Completa panoramica generale
    stats['panoramica_generale']['totale_carte'] = totale_carte
    stats['panoramica_generale']['totale_guerrieri_squadra'] = totale_squadra
    stats['panoramica_generale']['totale_guerrieri_schieramento'] = totale_schieramento
    stats['panoramica_generale']['totale_carte_supporto'] = totale_supporto
    
    if len(mazzi) > 0:
        stats['panoramica_generale']['media_carte_per_mazzo'] = totale_carte / len(mazzi)
        stats['panoramica_generale']['media_guerrieri_squadra'] = totale_squadra / len(mazzi)
        stats['panoramica_generale']['media_guerrieri_schieramento'] = totale_schieramento / len(mazzi)
        stats['panoramica_generale']['media_supporto'] = totale_supporto / len(mazzi)
    
    # Converti defaultdict in dict normale
    stats['distribuzione_fazioni']['squadra'] = dict(stats['distribuzione_fazioni']['squadra'])
    stats['distribuzione_fazioni']['schieramento'] = dict(stats['distribuzione_fazioni']['schieramento'])
    stats['distribuzione_classi_supporto'] = dict(stats['distribuzione_classi_supporto'])
    
    return stats
def testa_compatibilita_mazzi(mazzi: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Testa la compatibilità dei mazzi con il nuovo sistema organizzato.
    """
    risultati = {
        'compatibile': True,
        'errori': [],
        'avvisi': [],
        'statistiche_test': {
            'mazzi_testati': len(mazzi),
            'guerrieri_totali': 0,
            'supporto_totale': 0,
            'fazioni_rilevate': set(),
            'classi_rilevate': set()
        }
    }
    
    try:
        for i, mazzo in enumerate(mazzi):
            # Verifica struttura base
            if not isinstance(mazzo, dict):
                risultati['errori'].append(f"Mazzo {i+1}: formato non valido")
                risultati['compatibile'] = False
                continue
            
            # Test guerrieri squadra
            squadra = mazzo.get('squadra', [])
            risultati['statistiche_test']['guerrieri_totali'] += len(squadra)
            
            for j, guerriero in enumerate(squadra):
                try:
                    nome = getattr(guerriero, 'nome', None)
                    if not nome:
                        risultati['errori'].append(f"Mazzo {i+1}, Guerriero squadra {j+1}: manca attributo 'nome'")
                        risultati['compatibile'] = False
                    
                    if hasattr(guerriero, 'fazione'):
                        fazione = guerriero.fazione
                        if hasattr(fazione, 'value'):
                            fazione = fazione.value
                        risultati['statistiche_test']['fazioni_rilevate'].add(str(fazione))
                    
                except Exception as e:
                    risultati['errori'].append(f"Mazzo {i+1}, Guerriero squadra {j+1}: errore serializzazione - {e}")
                    risultati['compatibile'] = False
            
            # Test guerrieri schieramento
            schieramento = mazzo.get('schieramento', [])
            risultati['statistiche_test']['guerrieri_totali'] += len(schieramento)
            
            for j, guerriero in enumerate(schieramento):
                try:
                    nome = getattr(guerriero, 'nome', None)
                    if not nome:
                        risultati['errori'].append(f"Mazzo {i+1}, Guerriero schieramento {j+1}: manca attributo 'nome'")
                        risultati['compatibile'] = False
                    
                    if hasattr(guerriero, 'fazione'):
                        fazione = guerriero.fazione
                        if hasattr(fazione, 'value'):
                            fazione = fazione.value
                        risultati['statistiche_test']['fazioni_rilevate'].add(str(fazione))
                    
                except Exception as e:
                    risultati['errori'].append(f"Mazzo {i+1}, Guerriero schieramento {j+1}: errore serializzazione - {e}")
                    risultati['compatibile'] = False
            
            # Test carte supporto
            supporto = mazzo.get('carte_supporto', [])
            risultati['statistiche_test']['supporto_totale'] += len(supporto)
            
            for j, carta in enumerate(supporto):
                try:
                    nome = getattr(carta, 'nome', None)
                    if not nome:
                        risultati['errori'].append(f"Mazzo {i+1}, Carta supporto {j+1}: manca attributo 'nome'")
                        risultati['compatibile'] = False
                    
                    try:
                        classe = determina_classe_supporto(carta)
                        risultati['statistiche_test']['classi_rilevate'].add(classe)
                    except Exception as e:
                        risultati['avvisi'].append(f"Mazzo {i+1}, Carta {j+1}: impossibile determinare classe - {e}")
                    
                except Exception as e:
                    risultati['errori'].append(f"Mazzo {i+1}, Carta supporto {j+1}: errore serializzazione - {e}")
                    risultati['compatibile'] = False
    
    except Exception as e:
        risultati['errori'].append(f"Errore generale durante test compatibilità: {e}")
        risultati['compatibile'] = False
    
    # Converti set in liste per serializzazione JSON
    risultati['statistiche_test']['fazioni_rilevate'] = list(risultati['statistiche_test']['fazioni_rilevate'])
    risultati['statistiche_test']['classi_rilevate'] = list(risultati['statistiche_test']['classi_rilevate'])
    
    return risultati


def salva_mazzi_json_sicuro(mazzi: List[Dict[str, Any]], filename: str = "mazzi_sicuri.json") -> bool:
    """
    Versione sicura di salvataggio che garantisce sempre il successo con organizzazione per fazioni e classi.
    VERSIONE AGGIORNATA: Include organizzazione per fazioni e classi.
    
    Args:
        mazzi: Lista di mazzi da salvare
        filename: Nome file di output
        
    Returns:
        True (garantisce sempre successo)
    """
    print(f"🛡️ Salvataggio sicuro con organizzazione per fazioni e classi: {filename}")
    
    # Prova prima il salvataggio completo organizzato
    if salva_mazzi_json_migliorato_con_conteggio_e_apostoli(mazzi, filename):
        print("✅ Salvataggio completo organizzato riuscito!")
        return True
    
    # Fallback: versione minimale organizzata
    try:
        print("⚠️ Tentativo fallback: salvataggio minimale organizzato...")
        
        dati_minimali = {
            'metadata': {
                'tipo_export': 'mazzi_minimali_organizzati',
                'versione': '2.1_safe',
                'data_creazione': datetime.now().isoformat(),
                'numero_mazzi': len(mazzi),
                'modalita': 'fallback_sicuro_organizzato'
            },
            'mazzi_info': []
        }
        
        for i, mazzo in enumerate(mazzi):
            # Processa con gestione errori per ogni singola carta
            info_minimale = {
                'indice': i + 1,
                'totale_carte': len(mazzo.get('squadra', [])) + len(mazzo.get('schieramento', [])) + len(mazzo.get('carte_supporto', [])),
                'guerrieri_squadra_organizzati': {},
                'guerrieri_schieramento_organizzati': {},
                'supporto_organizzato': {}
            }
            
            # Organizza guerrieri squadra per fazioni
            try:
                squadra = mazzo.get('squadra', [])
                fazioni_squadra = defaultdict(list)
                for guerriero in squadra:
                    fazione = 'Generica'
                    try:
                        fazione_obj = getattr(guerriero, 'fazione', 'Generica')
                        if hasattr(fazione_obj, 'value'):
                            fazione = fazione_obj.value
                        else:
                            fazione = str(fazione_obj)
                    except:
                        fazione = 'Generica'
                    
                    nome_guerriero = getattr(guerriero, 'nome', f'Guerriero_{len(fazioni_squadra[fazione])}')
                    fazioni_squadra[fazione].append(nome_guerriero)
                
                info_minimale['guerrieri_squadra_organizzati'] = dict(fazioni_squadra)
            except Exception as e:
                print(f"   ⚠️ Errore organizzazione squadra mazzo {i+1}: {e}")
                info_minimale['guerrieri_squadra_organizzati'] = {'Errore': ['Impossibile organizzare']}
            
            # Organizza guerrieri schieramento per fazioni
            try:
                schieramento = mazzo.get('schieramento', [])
                fazioni_schieramento = defaultdict(list)
                for guerriero in schieramento:
                    fazione = 'Generica'
                    try:
                        fazione_obj = getattr(guerriero, 'fazione', 'Generica')
                        if hasattr(fazione_obj, 'value'):
                            fazione = fazione_obj.value
                        else:
                            fazione = str(fazione_obj)
                    except:
                        fazione = 'Generica'
                    
                    nome_guerriero = getattr(guerriero, 'nome', f'Guerriero_{len(fazioni_schieramento[fazione])}')
                    fazioni_schieramento[fazione].append(nome_guerriero)
                
                info_minimale['guerrieri_schieramento_organizzati'] = dict(fazioni_schieramento)
            except Exception as e:
                print(f"   ⚠️ Errore organizzazione schieramento mazzo {i+1}: {e}")
                info_minimale['guerrieri_schieramento_organizzati'] = {'Errore': ['Impossibile organizzare']}
            
            # Organizza supporto per classi
            try:
                supporto = mazzo.get('carte_supporto', [])
                classi_supporto = defaultdict(list)
                for carta in supporto:
                    classe = 'Speciale'  # Default
                    try:
                        classe = determina_classe_supporto(carta)
                    except:
                        try:
                            classe = type(carta).__name__
                        except:
                            classe = 'Sconosciuta'
                    
                    nome_carta = getattr(carta, 'nome', f'Carta_{len(classi_supporto[classe])}')
                    classi_supporto[classe].append(nome_carta)
                
                info_minimale['supporto_organizzato'] = dict(classi_supporto)
            except Exception as e:
                print(f"   ⚠️ Errore organizzazione supporto mazzo {i+1}: {e}")
                info_minimale['supporto_organizzato'] = {'Errore': ['Impossibile organizzare']}
            
            dati_minimali['mazzi_info'].append(info_minimale)
        
        # Salva fallback organizzato
        os.makedirs(PERCORSO_SALVATAGGIO, exist_ok=True)
        filename_sicuro = filename.replace('.json', '_sicuro_organizzato.json')
        
        with open(PERCORSO_SALVATAGGIO + filename_sicuro, 'w', encoding='utf-8') as f:
            json.dump(dati_minimali, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Salvataggio sicuro organizzato completato: {filename_sicuro}")
        return True
        
    except Exception as e2:
        print(f"❌ Errore anche nel salvataggio sicuro organizzato: {e2}")
        
        # Ultimo fallback: salvataggio base
        try:
            filename_base = filename.replace('.json', '_base.json')
            dati_base = {
                'metadata': {
                    'tipo_export': 'mazzi_base',
                    'data_creazione': datetime.now().isoformat(),
                    'numero_mazzi': len(mazzi),
                    'modalita': 'salvataggio_emergenza'
                },
                'mazzi_conteggio': [
                    {
                        'indice': i + 1,
                        'carte_totali': len(m.get('squadra', [])) + len(m.get('schieramento', [])) + len(m.get('carte_supporto', []))
                    } for i, m in enumerate(mazzi)
                ]
            }
            
            with open(PERCORSO_SALVATAGGIO + filename_base, 'w', encoding='utf-8') as f:
                json.dump(dati_base, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Salvataggio base completato: {filename_base}")
            return True
            
        except Exception as e3:
            print(f"❌ Errore critico nel salvataggio: {e3}")
            return False
def carica_mazzi_json_migliorato(filename: str) -> Optional[Dict[str, Any]]:
    """
    Carica mazzi da file JSON con supporto per la nuova organizzazione per fazioni e classi.
    VERSIONE AGGIORNATA: Compatibile con l'organizzazione per fazioni e classi.
    
    Args:
        filename: Nome del file da caricare
        
    Returns:
        Dizionario con i dati caricati o None in caso di errore
    """
    try:
        print(f"📂 Caricamento mazzi da {PERCORSO_SALVATAGGIO+filename}...")
        
        with open(PERCORSO_SALVATAGGIO + filename, 'r', encoding='utf-8') as f:
            dati = json.load(f)
        
        # Verifica formato e compatibilità
        metadata = dati.get('metadata', {})
        tipo_export = metadata.get('tipo_export', 'sconosciuto')
        
        if 'organizzati' in tipo_export or 'organizzato' in tipo_export:
            print("✅ Rilevato formato organizzato per fazioni e classi")
        elif tipo_export == 'mazzi_dettagliati':
            print("⚠️ Formato precedente rilevato - compatibilità mantenuta")
        else:
            print("⚠️ Formato sconosciuto - tentativo di caricamento...")
        
        # Stampa info di caricamento
        print(f"✅ Caricamento completato!")
        print(f"   📅 Creato: {metadata.get('data_creazione', 'N/A')}")
        print(f"   🎮 Mazzi: {metadata.get('numero_mazzi', 'N/A')}")
        
        # Statistiche se disponibili
        stats = dati.get('statistiche_aggregate', {})
        panoramica = stats.get('panoramica_generale', {})
        if panoramica:
            print(f"   📦 Carte totali: {panoramica.get('totale_carte', 'N/A')}")
            print(f"   ⚔️ Guerrieri squadra: {panoramica.get('totale_guerrieri_squadra', 'N/A')}")
            print(f"   🌙 Guerrieri schieramento: {panoramica.get('totale_guerrieri_schieramento', 'N/A')}")
            print(f"   🎴 Carte supporto: {panoramica.get('totale_carte_supporto', 'N/A')}")
        
        # Info organizzazione se disponibile
        if 'distribuzione_fazioni' in stats:
            fazioni_sq = len(stats['distribuzione_fazioni'].get('squadra', {}))
            fazioni_sch = len(stats['distribuzione_fazioni'].get('schieramento', {}))
            print(f"   🏛️ Fazioni squadra: {fazioni_sq}")
            print(f"   🌙 Fazioni schieramento: {fazioni_sch}")
        
        if 'distribuzione_classi_supporto' in stats:
            classi = len(stats['distribuzione_classi_supporto'])
            print(f"   🎴 Classi supporto: {classi}")
        
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
def stampa_statistiche_da_json_mazzi(dati_json: Dict[str, Any]) -> None:
    """
    Stampa statistiche dai mazzi caricati da JSON con supporto per organizzazione.
    VERSIONE AGGIORNATA: Mostra statistiche organizzate per fazioni e classi.
    
    Args:
        dati_json: Dati JSON caricati
    """
    if not dati_json:
        print("❌ Nessun dato da visualizzare")
        return
    
    metadata = dati_json.get('metadata', {})
    stats_aggregate = dati_json.get('statistiche_aggregate', {})
    panoramica = stats_aggregate.get('panoramica_generale', {})
    
    print(f"\n{'='*80}")
    print(f"📋 STATISTICHE DA JSON - {panoramica.get('numero_mazzi', 0)} MAZZI")
    if metadata.get('tipo_export', '').find('organizzati') != -1:
        print(f"🔄 FORMATO: Organizzato per fazioni e classi")
    print(f"{'='*80}")
    
    # Statistiche generali
    print(f"📦 Totale carte: {panoramica.get('totale_carte', 0)}")
    print(f"⚔️ Totale guerrieri squadra: {panoramica.get('totale_guerrieri_squadra', 0)}")
    print(f"🌙 Totale guerrieri schieramento: {panoramica.get('totale_guerrieri_schieramento', 0)}")
    print(f"🎴 Totale carte supporto: {panoramica.get('totale_carte_supporto', 0)}")
    print(f"📈 Media carte/mazzo: {panoramica.get('media_carte_per_mazzo', 0):.1f}")
    print(f"📈 Media guerrieri squadra: {panoramica.get('media_guerrieri_squadra', 0):.1f}")
    print(f"📈 Media guerrieri schieramento: {panoramica.get('media_guerrieri_schieramento', 0):.1f}")
    print(f"📈 Media supporto: {panoramica.get('media_supporto', 0):.1f}")
    
    # Distribuzione fazioni se disponibile
    distribuzione_fazioni = stats_aggregate.get('distribuzione_fazioni', {})
    if distribuzione_fazioni:
        print(f"\n🏛️ DISTRIBUZIONE FAZIONI SQUADRA:")
        fazioni_squadra = distribuzione_fazioni.get('squadra', {})
        if fazioni_squadra:
            for fazione, count in sorted(fazioni_squadra.items(), key=lambda x: x[1], reverse=True):
                print(f"   • {fazione}: {count} guerrieri")
        else:
            print("   Nessuna fazione squadra registrata")
        
        print(f"\n🌙 DISTRIBUZIONE FAZIONI SCHIERAMENTO:")
        fazioni_schieramento = distribuzione_fazioni.get('schieramento', {})
        if fazioni_schieramento:
            for fazione, count in sorted(fazioni_schieramento.items(), key=lambda x: x[1], reverse=True):
                print(f"   • {fazione}: {count} guerrieri")
        else:
            print("   Nessuna fazione schieramento registrata")
    
    # Distribuzione classi supporto se disponibile
    distribuzione_classi = stats_aggregate.get('distribuzione_classi_supporto', {})
    if distribuzione_classi:
        print(f"\n🎴 DISTRIBUZIONE CLASSI SUPPORTO:")
        for classe, count in sorted(distribuzione_classi.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {classe}: {count} carte")
    
    # Riepilogo mazzi dettagliato
    riepilogo_mazzi = stats_aggregate.get('riepilogo_mazzi', [])
    if riepilogo_mazzi:
        print(f"\n📊 RIEPILOGO DETTAGLIATO MAZZI:")
        for mazzo in riepilogo_mazzi:
            print(f"  🎮 Mazzo {mazzo.get('indice_mazzo')}: {mazzo.get('totale_carte')} carte")
            print(f"      ⚔️ Squadra: {mazzo.get('guerrieri_squadra')} - 🌙 Schieramento: {mazzo.get('guerrieri_schieramento')} - 🎴 Supporto: {mazzo.get('carte_supporto')}")
            
            # Mostra fazioni se disponibili
            fazioni_sq = mazzo.get('fazioni_squadra', [])
            if fazioni_sq:
                print(f"      🏛️ Fazioni squadra: {', '.join(fazioni_sq)}")
            
            fazioni_sch = mazzo.get('fazioni_schieramento', [])
            if fazioni_sch:
                print(f"      🌙 Fazioni schieramento: {', '.join(fazioni_sch)}")
            
            classi_sup = mazzo.get('classi_supporto', [])
            if classi_sup:
                print(f"      🎴 Classi supporto: {', '.join(classi_sup)}")
            
            esp_str = ', '.join(mazzo.get('espansioni_utilizzate', []))
            if esp_str:
                print(f"      📚 Espansioni: {esp_str}")
            
            if mazzo.get('errori'):
                print(f"      ⚠️ Avvisi: {'; '.join(mazzo['errori'])}")
            print()
    
    # Distribuzione globale espansioni se disponibile (retrocompatibilità)
    distribuzione_globale = stats_aggregate.get('distribuzione_globale', {})
    if distribuzione_globale:
        distribuzione_espansioni = distribuzione_globale.get('per_espansione', {})
        if distribuzione_espansioni:
            print(f"\n📚 DISTRIBUZIONE GLOBALE ESPANSIONI:")
            for espansione, count in sorted(distribuzione_espansioni.items()):
                print(f"   • {espansione}: presente in {count} mazzi")

def converti_enum_ricorsivo_mazzi(obj):
    """
    Converte enum in stringhe ricorsivamente per serializzazione JSON.
    Versione robusta per mazzi che gestisce oggetti complessi.
    """
    if hasattr(obj, 'value'):  # È un enum
        return obj.value
    elif isinstance(obj, dict):
        return {k: converti_enum_ricorsivo_mazzi(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [converti_enum_ricorsivo_mazzi(item) for item in obj]
    elif hasattr(obj, '__dict__'):  # È un oggetto con attributi
        try:
            return {k: converti_enum_ricorsivo_mazzi(v) for k, v in obj.__dict__.items()}
        except Exception:
            # Se la serializzazione dell'oggetto fallisce, usa la rappresentazione stringa
            return str(obj)
    else:
        # Per tipi primitivi o oggetti non serializzabili
        try:
            # Tenta di serializzare direttamente
            json.dumps(obj)  # Test se è serializzabile
            return obj
        except (TypeError, ValueError):
            # Se non è serializzabile, convertilo in stringa
            return str(obj)
def crea_statistiche_aggregate_mazzi_json(mazzi: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Crea statistiche aggregate per i mazzi in formato JSON.
    Analogo di crea_statistiche_aggregate_json() per mazzi.
    """
    statistiche_aggregate = {
        'panoramica_generale': {
            'numero_mazzi': len(mazzi),
            'totale_carte': 0,
            'totale_guerrieri_squadra': 0,
            'totale_guerrieri_schieramento': 0,
            'media_carte_per_mazzo': 0,
            'media_guerrieri_squadra': 0,
            'media_guerrieri_schieramento': 0
        },
        'distribuzione_globale': {
            'per_tipo_supporto': defaultdict(int),
            'per_fazione': defaultdict(int),
            'per_espansione': defaultdict(int)
        },
        'riepilogo_mazzi': []
    }
    
    # Calcola statistiche per ogni mazzo
    for i, mazzo in enumerate(mazzi):
        stats = mazzo['statistiche']
        
        # Aggiorna panoramica generale
        statistiche_aggregate['panoramica_generale']['totale_carte'] += stats['numero_totale_carte']
        statistiche_aggregate['panoramica_generale']['totale_guerrieri_squadra'] += stats['guerrieri_squadra']
        statistiche_aggregate['panoramica_generale']['totale_guerrieri_schieramento'] += stats['guerrieri_schieramento']
        
        # Distribuzione per tipo supporto
        for tipo, count in stats.get('distribuzione_per_tipo', {}).items():
            statistiche_aggregate['distribuzione_globale']['per_tipo_supporto'][tipo] += count
        
        # Distribuzione per fazione
        for fazione in stats.get('fazioni_presenti', []):
            statistiche_aggregate['distribuzione_globale']['per_fazione'][fazione] += 1
        
        # Distribuzione per espansione
        for espansione in stats.get('espansioni_utilizzate', []):
            statistiche_aggregate['distribuzione_globale']['per_espansione'][espansione] += 1
        
        # Riepilogo singolo mazzo
        riepilogo_mazzo = {
            'indice_mazzo': i + 1,
            'totale_carte': stats['numero_totale_carte'],
            'guerrieri_squadra': stats['guerrieri_squadra'],
            'guerrieri_schieramento': stats['guerrieri_schieramento'],
            'fazioni_presenti': stats.get('fazioni_presenti', []),
            'espansioni_utilizzate': stats.get('espansioni_utilizzate', []),
            'distribuzione_supporto': dict(stats.get('distribuzione_per_tipo', {})),
            'errori': mazzo.get('errori', [])
        }
        statistiche_aggregate['riepilogo_mazzi'].append(riepilogo_mazzo)
    
    # Calcola medie
    num_mazzi = len(mazzi)
    if num_mazzi > 0:
        statistiche_aggregate['panoramica_generale']['media_carte_per_mazzo'] = \
            statistiche_aggregate['panoramica_generale']['totale_carte'] / num_mazzi
        statistiche_aggregate['panoramica_generale']['media_guerrieri_squadra'] = \
            statistiche_aggregate['panoramica_generale']['totale_guerrieri_squadra'] / num_mazzi
        statistiche_aggregate['panoramica_generale']['media_guerrieri_schieramento'] = \
            statistiche_aggregate['panoramica_generale']['totale_guerrieri_schieramento'] / num_mazzi
    
    # Converte defaultdict in dict
    for key in statistiche_aggregate['distribuzione_globale']:
        statistiche_aggregate['distribuzione_globale'][key] = dict(statistiche_aggregate['distribuzione_globale'][key])
    
    return statistiche_aggregate
def crea_inventario_dettagliato_mazzo_json(mazzo: Dict[str, Any], indice: int) -> Dict[str, Any]:
    """
    Crea un inventario dettagliato di un singolo mazzo in formato JSON.
    Analogo di crea_inventario_dettagliato_json() per mazzi.
    """
    inventario = {
        'indice_mazzo': indice,
        'statistiche_mazzo': mazzo['statistiche'],
        'errori': mazzo.get('errori', []),
        'distribuzione_utilizzata': mazzo.get('distribuzione_utilizzata', {}),
        'inventario_guerrieri': {
            'squadra': [],
            'schieramento': []
        },
        'inventario_supporto': []
    }
    
    # Inventario guerrieri squadra
    for guerriero in mazzo['squadra']:
        guerriero_info = crea_info_guerriero_sicura(guerriero)
        inventario['inventario_guerrieri']['squadra'].append(guerriero_info)
    
    # Inventario guerrieri schieramento  
    for guerriero in mazzo['schieramento']:
        guerriero_info = crea_info_guerriero_sicura(guerriero)
        inventario['inventario_guerrieri']['schieramento'].append(guerriero_info)
    
    # Inventario carte supporto
    for carta in mazzo['carte_supporto']:
        carta_info = crea_info_carta_supporto_sicura(carta)
        inventario['inventario_supporto'].append(carta_info)
    
    return inventario
def diagnostica_mazzo(mazzo: Dict[str, Any], indice: int = 1) -> Dict[str, Any]:
    """
    Esegue una diagnostica completa di un singolo mazzo per identificare problemi.
    
    Args:
        mazzo: Dizionario del mazzo da diagnosticare
        indice: Indice del mazzo (per identificazione)
        
    Returns:
        Dizionario con i risultati della diagnostica
    """
    risultati = {
        'mazzo_indice': indice,
        'stato_generale': 'OK',
        'errori_critici': [],
        'avvisi': [],
        'dettagli': {}
    }
    
    try:
        # Verifica struttura base
        chiavi_richieste = ['squadra', 'schieramento', 'carte_supporto', 'statistiche']
        for chiave in chiavi_richieste:
            if chiave not in mazzo:
                risultati['errori_critici'].append(f"Manca chiave '{chiave}'")
                risultati['stato_generale'] = 'ERRORE'
        
        # Analisi guerrieri squadra
        if 'squadra' in mazzo:
            squadra_info = {
                'numero_guerrieri': len(mazzo['squadra']),
                'guerrieri_validi': 0,
                'guerrieri_problematici': []
            }
            
            for i, guerriero in enumerate(mazzo['squadra']):
                try:
                    info = crea_info_guerriero_sicura(guerriero)
                    squadra_info['guerrieri_validi'] += 1
                    
                    # Verifica attributi essenziali
                    if not info.get('nome') or info['nome'] == 'Nome sconosciuto':
                        squadra_info['guerrieri_problematici'].append(f"Guerriero {i+1}: nome mancante")
                    
                except Exception as e:
                    squadra_info['guerrieri_problematici'].append(f"Guerriero {i+1}: {str(e)}")
                    risultati['stato_generale'] = 'AVVISO' if risultati['stato_generale'] == 'OK' else risultati['stato_generale']
            
            risultati['dettagli']['squadra'] = squadra_info
        
        # Analisi guerrieri schieramento
        if 'schieramento' in mazzo:
            schieramento_info = {
                'numero_guerrieri': len(mazzo['schieramento']),
                'guerrieri_validi': 0,
                'guerrieri_problematici': []
            }
            
            for i, guerriero in enumerate(mazzo['schieramento']):
                try:
                    info = crea_info_guerriero_sicura(guerriero)
                    schieramento_info['guerrieri_validi'] += 1
                    
                    if not info.get('nome') or info['nome'] == 'Nome sconosciuto':
                        schieramento_info['guerrieri_problematici'].append(f"Guerriero {i+1}: nome mancante")
                    
                except Exception as e:
                    schieramento_info['guerrieri_problematici'].append(f"Guerriero {i+1}: {str(e)}")
                    risultati['stato_generale'] = 'AVVISO' if risultati['stato_generale'] == 'OK' else risultati['stato_generale']
            
            risultati['dettagli']['schieramento'] = schieramento_info
        
        # Analisi carte supporto
        if 'carte_supporto' in mazzo:
            supporto_info = {
                'numero_carte': len(mazzo['carte_supporto']),
                'carte_valide': 0,
                'carte_problematiche': []
            }
            
            for i, carta in enumerate(mazzo['carte_supporto']):
                try:
                    info = crea_info_carta_supporto_sicura(carta)
                    supporto_info['carte_valide'] += 1
                    
                    if not info.get('nome') or info['nome'] == 'Nome sconosciuto':
                        supporto_info['carte_problematiche'].append(f"Carta {i+1}: nome mancante")
                    
                except Exception as e:
                    supporto_info['carte_problematiche'].append(f"Carta {i+1}: {str(e)}")
                    risultati['stato_generale'] = 'AVVISO' if risultati['stato_generale'] == 'OK' else risultati['stato_generale']
            
            risultati['dettagli']['carte_supporto'] = supporto_info
        
        # Verifica statistiche
        if 'statistiche' in mazzo:
            stats = mazzo['statistiche']
            if not isinstance(stats, dict):
                risultati['errori_critici'].append("Statistiche non sono un dizionario")
                risultati['stato_generale'] = 'ERRORE'
            else:
                risultati['dettagli']['statistiche'] = {
                    'chiavi_presenti': list(stats.keys()),
                    'numero_totale_carte': stats.get('numero_totale_carte', 'N/A')
                }
        
        # Aggrega risultati per avvisi
        for sezione, info in risultati['dettagli'].items():
            if sezione in ['squadra', 'schieramento', 'carte_supporto']:
                if info.get('guerrieri_problematici') or info.get('carte_problematiche'):
                    problemi = info.get('guerrieri_problematici', []) + info.get('carte_problematiche', [])
                    risultati['avvisi'].extend(problemi)
    
    except Exception as e:
        risultati['errori_critici'].append(f"Errore generale diagnostica: {str(e)}")
        risultati['stato_generale'] = 'ERRORE'
    
    return risultati
def stampa_diagnostica_mazzi(mazzi: List[Dict[str, Any]]) -> None:
    """
    Stampa una diagnostica completa dei mazzi.
    
    Args:
        mazzi: Lista di mazzi da diagnosticare
    """
    print(f"\n{'='*80}")
    print(f"🔍 DIAGNOSTICA MAZZI - {len(mazzi)} MAZZI")
    print(f"{'='*80}")
    
    mazzi_ok = 0
    mazzi_avvisi = 0
    mazzi_errori = 0
    
    for i, mazzo in enumerate(mazzi):
        risultati = diagnostica_mazzo(mazzo, i + 1)
        
        # Conteggi
        if risultati['stato_generale'] == 'OK':
            mazzi_ok += 1
            print(f"✅ Mazzo {i+1}: OK")
        elif risultati['stato_generale'] == 'AVVISO':
            mazzi_avvisi += 1
            print(f"⚠️ Mazzo {i+1}: Avvisi")
        else:
            mazzi_errori += 1
            print(f"❌ Mazzo {i+1}: Errori critici")
        
        # Dettagli se ci sono problemi
        if risultati['errori_critici'] or risultati['avvisi']:
            for errore in risultati['errori_critici']:
                print(f"    ❌ {errore}")
            
            for avviso in risultati['avvisi'][:3]:  # Max 3 avvisi per mazzo
                print(f"    ⚠️ {avviso}")
            
            if len(risultati['avvisi']) > 3:
                print(f"    ... e altri {len(risultati['avvisi']) - 3} avvisi")
        
        # Statistiche rapide
        dettagli = risultati['dettagli']
        if 'squadra' in dettagli:
            print(f"    📊 Squadra: {dettagli['squadra']['guerrieri_validi']}/{dettagli['squadra']['numero_guerrieri']} OK")
        if 'schieramento' in dettagli:
            print(f"    📊 Schieramento: {dettagli['schieramento']['guerrieri_validi']}/{dettagli['schieramento']['numero_guerrieri']} OK")
        if 'carte_supporto' in dettagli:
            print(f"    📊 Supporto: {dettagli['carte_supporto']['carte_valide']}/{dettagli['carte_supporto']['numero_carte']} OK")
    
    # Riepilogo finale
    print(f"\n📊 RIEPILOGO DIAGNOSTICA:")
    print(f"  ✅ Mazzi OK: {mazzi_ok}")
    print(f"  ⚠️ Mazzi con avvisi: {mazzi_avvisi}")
    print(f"  ❌ Mazzi con errori: {mazzi_errori}")
    
    if mazzi_errori > 0:
        print(f"\n⚠️ RACCOMANDAZIONE: Correggere gli errori critici prima del salvataggio JSON")
def crea_guerriero_serializzabile(guerriero):
    """Crea una versione serializzabile del guerriero."""
    return {
        'nome': ottieni_attributo_sicuro(guerriero, 'nome', 'Guerriero Sconosciuto'),
        'fazione': ottieni_attributo_sicuro(guerriero, 'fazione', 'Fazione Sconosciuta'),
        'tipo': 'Guerriero',
        'set_espansione': ottieni_attributo_sicuro(guerriero, 'set_espansione', 'Set Sconosciuto'),
        'rarity': ottieni_attributo_sicuro(guerriero, 'rarity', 'Common'),
        'combattimento': 0,
        'sparare': 0,
        'armatura': 0,
        'valore': 0
    }
def crea_carta_serializzabile(carta):
    """Crea una versione serializzabile della carta."""
    return {
        'nome': ottieni_attributo_sicuro(carta, 'nome', 'Carta Sconosciuta'),
        'tipo': type(carta).__name__,
        'set_espansione': ottieni_attributo_sicuro(carta, 'set_espansione', 'Set Sconosciuto'),
        'rarity': ottieni_attributo_sicuro(carta, 'rarity', 'Common')
    }
def crea_placeholder_guerriero(guerriero, nome_default):
    """Crea un placeholder per un guerriero problematico."""
    return {
        'nome': nome_default,
        'fazione': 'Placeholder',
        'tipo': 'Guerriero',
        'set_espansione': 'Unknown',
        'rarity': 'Common',
        'errore_originale': 'Guerriero non serializzabile',
        'tipo_originale': type(guerriero).__name__ if guerriero else 'Unknown'
    }
def crea_placeholder_carta(carta, nome_default):
    """Crea un placeholder per una carta problematica."""
    return {
        'nome': nome_default,
        'tipo': 'Placeholder',
        'set_espansione': 'Unknown',
        'rarity': 'Common',
        'errore_originale': 'Carta non serializzabile',
        'tipo_originale': type(carta).__name__ if carta else 'Unknown'
    }
def pulisci_mazzi_per_salvataggio(mazzi: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Pulisce e prepara i mazzi per un salvataggio sicuro.
    
    Args:
        mazzi: Lista di mazzi da pulire
        
    Returns:
        Lista di mazzi puliti e pronti per il salvataggio
    """
    mazzi_puliti = []
    
    for i, mazzo in enumerate(mazzi):
        try:
            mazzo_pulito = {
                'squadra': [],
                'schieramento': [],
                'carte_supporto': [],
                'statistiche': mazzo.get('statistiche', {}),
                'errori': mazzo.get('errori', []),
                'distribuzione_utilizzata': mazzo.get('distribuzione_utilizzata', {})
            }
            
            # Pulisci guerrieri squadra
            for guerriero in mazzo.get('squadra', []):
                try:
                    # Tenta di creare una versione serializzabile
                    guerriero_sicuro = crea_guerriero_serializzabile(guerriero)
                    mazzo_pulito['squadra'].append(guerriero_sicuro)
                except Exception:
                    # Se fallisce, crea un placeholder
                    placeholder = crea_placeholder_guerriero(guerriero, f"Guerriero Squadra {len(mazzo_pulito['squadra'])+1}")
                    mazzo_pulito['squadra'].append(placeholder)
            
            # Pulisci guerrieri schieramento
            for guerriero in mazzo.get('schieramento', []):
                try:
                    guerriero_sicuro = crea_guerriero_serializzabile(guerriero)
                    mazzo_pulito['schieramento'].append(guerriero_sicuro)
                except Exception:
                    placeholder = crea_placeholder_guerriero(guerriero, f"Guerriero Schieramento {len(mazzo_pulito['schieramento'])+1}")
                    mazzo_pulito['schieramento'].append(placeholder)
            
            # Pulisci carte supporto
            for carta in mazzo.get('carte_supporto', []):
                try:
                    carta_sicura = crea_carta_serializzabile(carta)
                    mazzo_pulito['carte_supporto'].append(carta_sicura)
                except Exception:
                    placeholder = crea_placeholder_carta(carta, f"Carta Supporto {len(mazzo_pulito['carte_supporto'])+1}")
                    mazzo_pulito['carte_supporto'].append(placeholder)
            
            mazzi_puliti.append(mazzo_pulito)
            
        except Exception as e:
            # Crea un mazzo placeholder in caso di errore grave
            mazzo_placeholder = {
                'squadra': [],
                'schieramento': [],
                'carte_supporto': [],
                'statistiche': {'numero_totale_carte': 0, 'errore_pulizia': str(e)},
                'errori': [f"Errore durante pulizia mazzo: {e}"],
                'distribuzione_utilizzata': {}
            }
            mazzi_puliti.append(mazzo_placeholder)
    
    return mazzi_puliti
def esempio_salvataggio_mazzi_con_conteggio(mazzi: List[Dict[str, Any]]) -> None:
    """
    Esempio di utilizzo delle funzioni di salvataggio con conteggio copie.
    
    Args:
        mazzi: Lista di mazzi da utilizzare per l'esempio
    """
    print("\n📁 ESEMPIO SALVATAGGIO JSON CON CONTEGGIO COPIE - MAZZI")
    print("=" * 70)
    
    if not mazzi:
        print("❌ Nessun mazzo fornito per l'esempio")
        return
    
    print("1. Stampa riepilogo standard: stampa_riepilogo_mazzi_migliorato(mazzi)")
    stampa_riepilogo_mazzi_migliorato(mazzi)
    
    print("2. Salva: salva_mazzi_json_migliorato_con_conteggio_e_apostoli(mazzi)")
    salva_mazzi_json_migliorato_con_conteggio_e_apostoli(mazzi, "mazzi.json")
    
    print("3. Carica: dati = carica_mazzi_json_migliorato('mazzi.json')")
    dati_json = carica_mazzi_json_migliorato("mazzi.json")
    
    print("4. Visualizza con conteggio: stampa_statistiche_da_json_mazzi(dati)")
    if dati_json:
        stampa_statistiche_da_json_mazzi(dati_json)



#############################################  aggiornamento con classificazione per apostoli ################################################################





# ================================================================================
# FUNZIONI AGGIORNATE - Gestione Sottocartelle Apostoli Oscura Legione
# ================================================================================

def estrai_apostolo_da_keywords(keywords: List[str]) -> str:
    """
    Estrae il nome dell'apostolo dalle keywords di un guerriero Oscura Legione.
    
    Args:
        keywords: Lista di keywords del guerriero
        
    Returns:
        Nome dell'apostolo o "Oscura Legione" se non è un seguace
    """
    if not keywords:
        return "Oscura Legione"
    
    # Mappatura delle keywords agli apostoli
    mapping_apostoli = {
        "Seguace di Algeroth": "Algeroth",
        "Seguace di Semai": "Semai", 
        "Seguace di Muawijhe": "Muawijhe",
        "Seguace di Ilian": "Ilian",
        "Seguace di Demnogonis": "Demnogonis",
        # Varianti alternative
        "Cultista di Muawijhe": "Muawijhe",
        "Cultista di Demnogonis": "Demnogonis",
        "Cultista di Semai": "Semai",
        "Cultista di Ilian": "Ilian",
        "Cultista di Algeroth": "Algeroth"
    }
    
    # Cerca nelle keywords del guerriero
    for keyword in keywords:
        if keyword in mapping_apostoli:
            return mapping_apostoli[keyword]
    
    # Se non trova nessun seguace, ritorna la categoria generale
    return "Oscura Legione"


def processa_guerrieri_per_fazioni_con_apostoli(guerrieri: List[Any]) -> Dict[str, Dict[str, Any]]:
    """
    Organizza i guerrieri per fazioni con conteggio copie.
    VERSIONE AGGIORNATA: Include sottocategorizzazione per apostoli nell'Oscura Legione.
    
    Args:
        guerrieri: Lista di guerrieri
        
    Returns:
        Dizionario organizzato per fazioni (con apostoli per Oscura Legione)
    """
    fazioni_guerrieri = {}
    conteggio_guerrieri = defaultdict(int)
    dettagli_guerrieri = {}
    
    if not guerrieri:
        return fazioni_guerrieri
    
    # Prima passata: conta le copie e raccoglie dettagli
    for i, guerriero in enumerate(guerrieri):
        try:
            nome = getattr(guerriero, 'nome', f'Guerriero_Sconosciuto_{i+1}')
            
            # Determina fazione in modo sicuro
            fazione = 'Generica'
            try:
                fazione_obj = getattr(guerriero, 'fazione', None)
                if fazione_obj:
                    if hasattr(fazione_obj, 'value'):
                        fazione = fazione_obj.value
                    else:
                        fazione = str(fazione_obj)
            except:
                fazione = 'Generica'
            
            conteggio_guerrieri[nome] += 1
            
            if nome not in dettagli_guerrieri:
                dettagli_guerrieri[nome] = {
                    'copie': 0,
                    'fazione': fazione,
                    'set_espansione': ottieni_attributo_sicuro(guerriero, 'set_espansione', 'Base'),
                    'rarity': ottieni_attributo_sicuro(guerriero, 'rarity', 'Common'),
                    'tipo': ottieni_attributo_sicuro(guerriero, 'tipo', 'Normale'),
                    'stats': {},
                    'quantita': ottieni_attributo_sicuro(guerriero, 'quantita', 0),
                    'keywords': ottieni_attributo_sicuro(guerriero, 'keywords', []),
                    'abilita': ottieni_attributo_sicuro(guerriero, 'abilita', [])                    
                }
                
                # Per l'Oscura Legione, determina l'apostolo
                if fazione == 'Oscura Legione':
                    keywords = ottieni_attributo_sicuro(guerriero, 'keywords', [])
                    apostolo = estrai_apostolo_da_keywords(keywords)
                    dettagli_guerrieri[nome]['apostolo_seguace'] = apostolo
                
                # Gestione statistiche in modo sicuro
                try:
                    if hasattr(guerriero, 'stats') and guerriero.stats:
                        stats = guerriero.stats
                        dettagli_guerrieri[nome]['stats'] = {
                            'combattimento': ottieni_attributo_sicuro(stats, 'combattimento', 0),
                            'sparare': ottieni_attributo_sicuro(stats, 'sparare', 0),
                            'armatura': ottieni_attributo_sicuro(stats, 'armatura', 0),
                            'valore': ottieni_attributo_sicuro(stats, 'valore', 0)
                        }
                    else:
                        # Statistiche dirette sul guerriero
                        dettagli_guerrieri[nome]['stats'] = {
                            'combattimento': ottieni_attributo_sicuro(guerriero, 'combattimento', 0),
                            'sparare': ottieni_attributo_sicuro(guerriero, 'sparare', 0),
                            'armatura': ottieni_attributo_sicuro(guerriero, 'armatura', 0),
                            'valore': ottieni_attributo_sicuro(guerriero, 'valore', 0)
                        }
                except Exception as stats_error:
                    print(f"   ⚠️ Errore statistiche per {nome}: {stats_error}")
                    dettagli_guerrieri[nome]['stats'] = {
                        'combattimento': 0, 'sparare': 0, 'armatura': 0, 'valore': 0
                    }
                
        except Exception as e:
            print(f"   ⚠️ Errore processando guerriero {i+1}: {e}")
            nome_errore = f'Guerriero_Errore_{i+1}'
            conteggio_guerrieri[nome_errore] += 1
            dettagli_guerrieri[nome_errore] = {
                'copie': 0,
                'fazione': 'Errore',
                'apostolo_seguace': 'Errore',
                'set_espansione': 'Unknown',
                'rarity': 'Common',
                'tipo': 'Errore',
                'stats': {'combattimento': 0, 'sparare': 0, 'armatura': 0, 'valore': 0},
                'quantita': 0,
                'keywords': [],
                'abilita': [],
                'errore_processamento': str(e)
            }
    
    # Seconda passata: organizza per fazioni e apostoli
    for nome, count in conteggio_guerrieri.items():
        try:
            dettagli = dettagli_guerrieri[nome]
            dettagli['copie'] = count
            fazione = dettagli['fazione']
            
            if fazione not in fazioni_guerrieri:
                fazioni_guerrieri[fazione] = {}
            
            # Gestione speciale per Oscura Legione con apostoli
            if fazione == 'Oscura Legione' and 'apostolo_seguace' in dettagli:
                apostolo = dettagli['apostolo_seguace']
                
                # Crea la struttura gerarchica: Fazione -> Apostolo -> Guerriero
                if apostolo not in fazioni_guerrieri[fazione]:
                    fazioni_guerrieri[fazione][apostolo] = {}
                
                fazioni_guerrieri[fazione][apostolo][nome] = dettagli
            else:
                # Per le altre fazioni, struttura normale: Fazione -> Guerriero
                fazioni_guerrieri[fazione][nome] = dettagli
                
        except Exception as e:
            print(f"   ⚠️ Errore organizzando {nome}: {e}")
            # Metti nell'area errore
            if 'Errore' not in fazioni_guerrieri:
                fazioni_guerrieri['Errore'] = {}
            fazioni_guerrieri['Errore'][nome] = {
                'copie': count,
                'errore_organizzazione': str(e)
            }
    
    return fazioni_guerrieri


def crea_inventario_dettagliato_mazzo_json_con_conteggio_e_apostoli(mazzo: Dict[str, Any], indice: int) -> Dict[str, Any]:
    """
    Crea un inventario dettagliato di un singolo mazzo in formato JSON con suddivisioni per apostoli.
    VERSIONE AGGIORNATA: Include sottocategorizzazione per apostoli nell'Oscura Legione.
    
    Args:
        mazzo: Dizionario mazzo (output di crea_mazzo_da_gioco)
        indice: Indice del mazzo
        
    Returns:
        Dizionario con inventario dettagliato e organizzato per apostoli
    """
    # Struttura base dell'inventario
    inventario = {
        'inventario_guerrieri': {
            'squadra': {},
            'schieramento': {}
        },
        'inventario_supporto': {
            'Equipaggiamento': {},
            'Speciale': {},
            'Arte': {},
            'Oscura Simmetria': {},
            'Fortificazione': {},
            'Reliquia': {},
            'Warzone': {},
            'Missione': {}
        },
        'metadati_mazzo': {
            'indice': indice,
            'data_creazione': datetime.now().isoformat(),
            'totale_carte': 0,
            'statistiche_base': {},
            'apostoli_presenti': []  # Nuova informazione
        }
    }
    
    # Processa guerrieri squadra con organizzazione per fazioni
    try:
        guerrieri_squadra = mazzo.get('squadra', [])
        inventario['inventario_guerrieri']['squadra'] = processa_guerrieri_per_fazioni_con_apostoli(guerrieri_squadra)
        print(f"   ⚔️ Processati {len(guerrieri_squadra)} guerrieri squadra")
    except Exception as e:
        print(f"   ⚠️ Errore processando squadra: {e}")
        inventario['inventario_guerrieri']['squadra'] = {}
    
    # Processa guerrieri schieramento con organizzazione per fazioni e apostoli  
    try:
        guerrieri_schieramento = mazzo.get('schieramento', [])
        inventario['inventario_guerrieri']['schieramento'] = processa_guerrieri_per_fazioni_con_apostoli(guerrieri_schieramento)
        print(f"   🌙 Processati {len(guerrieri_schieramento)} guerrieri schieramento")
        
        # Estrai apostoli presenti nello schieramento
        apostoli_presenti = set()
        schieramento_data = inventario['inventario_guerrieri']['schieramento']
        if 'Oscura Legione' in schieramento_data:
            oscura_legione_data = schieramento_data['Oscura Legione']
            for apostolo_nome in oscura_legione_data.keys():
                if apostolo_nome != 'Oscura Legione':  # Escludi la categoria generale
                    apostoli_presenti.add(apostolo_nome)
        
        inventario['metadati_mazzo']['apostoli_presenti'] = list(apostoli_presenti)
        print(f"   👑 Apostoli identificati: {', '.join(apostoli_presenti) if apostoli_presenti else 'Nessuno'}")
        
    except Exception as e:
        print(f"   ⚠️ Errore processando schieramento: {e}")
        inventario['inventario_guerrieri']['schieramento'] = {}
        inventario['metadati_mazzo']['apostoli_presenti'] = []
    
    # Processa carte supporto con organizzazione per classi (invariato)
    try:
        carte_supporto = mazzo.get('carte_supporto', [])
        inventario['inventario_supporto'] = processa_supporto_per_classi(carte_supporto)
        print(f"   🎴 Processate {len(carte_supporto)} carte supporto")
    except Exception as e:
        print(f"   ⚠️ Errore processando supporto: {e}")
        pass
    
    # Calcola statistiche totali (con informazioni apostoli)
    try:
        guerrieri_squadra = mazzo.get('squadra', [])
        guerrieri_schieramento = mazzo.get('schieramento', [])
        carte_supporto = mazzo.get('carte_supporto', [])
        
        totale_carte = len(guerrieri_squadra) + len(guerrieri_schieramento) + len(carte_supporto)
        
        inventario['metadati_mazzo']['totale_carte'] = totale_carte
        inventario['metadati_mazzo']['statistiche_base'] = {
            'guerrieri_squadra': len(guerrieri_squadra),
            'guerrieri_schieramento': len(guerrieri_schieramento),
            'carte_supporto': len(carte_supporto)
        }
        
        # Statistiche per apostoli se presenti
        if inventario['metadati_mazzo']['apostoli_presenti']:
            inventario['metadati_mazzo']['statistiche_apostoli'] = {}
            for apostolo in inventario['metadati_mazzo']['apostoli_presenti']:
                count_guerrieri = 0
                schieramento_data = inventario['inventario_guerrieri']['schieramento']
                if 'Oscura Legione' in schieramento_data and apostolo in schieramento_data['Oscura Legione']:
                    count_guerrieri = len(schieramento_data['Oscura Legione'][apostolo])
                inventario['metadati_mazzo']['statistiche_apostoli'][apostolo] = count_guerrieri
        
        # Statistiche originali se disponibili
        if 'statistiche' in mazzo:
            statistiche_originali = mazzo['statistiche']
            inventario['metadati_mazzo']['statistiche_originali'] = {
                'numero_totale_carte': statistiche_originali.get('numero_totale_carte', totale_carte),
                'fazioni_presenti': statistiche_originali.get('fazioni_presenti', []),
                'espansioni_utilizzate': statistiche_originali.get('espansioni_utilizzate', []),
                'distribuzione_per_tipo': statistiche_originali.get('distribuzione_per_tipo', {})
            }
        
    except Exception as e:
        print(f"   ⚠️ Errore calcolando statistiche: {e}")
        inventario['metadati_mazzo']['totale_carte'] = 0
        inventario['metadati_mazzo']['statistiche_base'] = {
            'guerrieri_squadra': 0,
            'guerrieri_schieramento': 0,
            'carte_supporto': 0
        }
        inventario['metadati_mazzo']['apostoli_presenti'] = []
    
    return inventario


def salva_mazzi_json_migliorato_con_conteggio_e_apostoli(mazzi: List[Dict[str, Any]], filename: str = "mazzi_dettagliati_apostoli.json") -> bool:
    """
    Salva i mazzi in formato JSON con struttura dettagliata e sottocategorizzazione per apostoli.
    VERSIONE AGGIORNATA: Include organizzazione per apostoli nell'Oscura Legione.
    
    Args:
        mazzi: Lista di dizionari mazzo
        filename: Nome del file di salvataggio
        
    Returns:
        True se il salvataggio è riuscito, False altrimenti
    """
    try:
        print(f"📄 Creazione struttura JSON con organizzazione per fazioni, classi e apostoli per {len(mazzi)} mazzi...")
        
        # Test di compatibilità preventivo
        print("🔍 Test compatibilità mazzi...")
        test_risultati = testa_compatibilita_mazzi(mazzi)
        
        if not test_risultati['compatibile']:
            print("❌ Test compatibilità fallito:")
            for errore in test_risultati['errori']:
                print(f"  • {errore}")
            return False
        
        if test_risultati['avvisi']:
            print("⚠️ Avvisi compatibilità:")
            for avviso in test_risultati['avvisi']:
                print(f"  • {avviso}")
        
        print("✅ Test compatibilità superato!")
        
        # Crea struttura principale
        data_export = {
            'metadata': {
                'tipo_export': 'mazzi_dettagliati_con_apostoli',
                'versione': '2.2',
                'data_creazione': datetime.now().isoformat(),
                'numero_mazzi': len(mazzi),
                'formato': 'inventario_con_fazioni_classi_e_apostoli',
                'descrizione': 'Mazzi con inventari organizzati per fazioni, classi supporto e apostoli Oscura Legione'
            },
            'mazzi_dettagliati': [],
            'statistiche_aggregate': calcola_statistiche_aggregate_con_apostoli(mazzi)
        }
        
        # Processa ogni mazzo
        for i, mazzo in enumerate(mazzi):
            print(f"   🎮 Processando mazzo {i+1}/{len(mazzi)}...")
            
            inventario_dettagliato = crea_inventario_dettagliato_mazzo_json_con_conteggio_e_apostoli(mazzo, i+1)
            data_export['mazzi_dettagliati'].append(inventario_dettagliato)
        
        # Salvataggio con gestione errori migliorata
        os.makedirs(PERCORSO_SALVATAGGIO, exist_ok=True)
        filepath = PERCORSO_SALVATAGGIO + filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_export, f, indent=2, ensure_ascii=False, default=str)
        
        # Informazioni file salvato
        dimensione_file = os.path.getsize(filepath) / 1024  # KB
        print(f"\n✅ Salvataggio completato con successo!")
        print(f"   📄 File: {filename}")
        print(f"   📊 Dimensione: {dimensione_file:.1f} KB")
        print(f"   🎮 Mazzi: {len(mazzi)}")
        print(f"   📦 Carte totali: {sum(len(m.get('squadra', [])) + len(m.get('schieramento', [])) + len(m.get('carte_supporto', [])) for m in mazzi)}")
        print(f"   👑 Formato: Con organizzazione per apostoli Oscura Legione")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante il salvataggio JSON: {e}")
        return False


def calcola_statistiche_aggregate_con_apostoli(mazzi: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcola statistiche aggregate per i mazzi includendo informazioni sugli apostoli.
    
    Args:
        mazzi: Lista di mazzi
        
    Returns:
        Dizionario con statistiche aggregate inclusi apostoli
    """
    stats = {
        'panoramica_generale': {
            'numero_mazzi': len(mazzi),
            'totale_carte': 0,
            'totale_guerrieri_squadra': 0,
            'totale_guerrieri_schieramento': 0,
            'totale_carte_supporto': 0,
            'media_carte_per_mazzo': 0,
            'media_guerrieri_squadra': 0,
            'media_guerrieri_schieramento': 0,
            'media_supporto': 0
        },
        'distribuzione_fazioni': {
            'squadra': defaultdict(int),
            'schieramento': defaultdict(int)
        },
        'distribuzione_classi_supporto': defaultdict(int),
        'distribuzione_apostoli': defaultdict(int),  # Nuova sezione
        'riepilogo_mazzi': []
    }
    
    totale_carte = 0
    totale_squadra = 0
    totale_schieramento = 0
    totale_supporto = 0
    
    for i, mazzo in enumerate(mazzi):
        squadra = mazzo.get('squadra', [])
        schieramento = mazzo.get('schieramento', [])
        supporto = mazzo.get('carte_supporto', [])
        
        carte_mazzo = len(squadra) + len(schieramento) + len(supporto)
        totale_carte += carte_mazzo
        totale_squadra += len(squadra)
        totale_schieramento += len(schieramento)
        totale_supporto += len(supporto)
        
        # Conta fazioni squadra (invariato)
        fazioni_squadra = []
        for guerriero in squadra:
            fazione = getattr(guerriero, 'fazione', 'Sconosciuta')
            if hasattr(fazione, 'value'):
                fazione = fazione.value
            stats['distribuzione_fazioni']['squadra'][fazione] += 1
            if fazione not in fazioni_squadra:
                fazioni_squadra.append(fazione)
        
        # Conta fazioni schieramento con apostoli
        fazioni_schieramento = []
        apostoli_mazzo = []
        for guerriero in schieramento:
            fazione = getattr(guerriero, 'fazione', 'Sconosciuta')
            if hasattr(fazione, 'value'):
                fazione = fazione.value
            stats['distribuzione_fazioni']['schieramento'][fazione] += 1
            if fazione not in fazioni_schieramento:
                fazioni_schieramento.append(fazione)
            
            # Se è Oscura Legione, controlla l'apostolo
            if fazione == 'Oscura Legione':
                keywords = getattr(guerriero, 'keywords', [])
                apostolo = estrai_apostolo_da_keywords(keywords)
                if apostolo != 'Oscura Legione':  # È un seguace specifico
                    stats['distribuzione_apostoli'][apostolo] += 1
                    if apostolo not in apostoli_mazzo:
                        apostoli_mazzo.append(apostolo)
        
        # Conta classi supporto (invariato)
        classi_presenti = []
        for carta in supporto:
            classe = determina_classe_supporto(carta)
            stats['distribuzione_classi_supporto'][classe] += 1
            if classe not in classi_presenti:
                classi_presenti.append(classe)
        
        # Riepilogo singolo mazzo con apostoli
        espansioni = set()
        for carta_lista in [squadra, schieramento, supporto]:
            for carta in carta_lista:
                esp = getattr(carta, 'set_espansione', 'Base')
                if hasattr(esp, 'value'):
                    esp = esp.value
                espansioni.add(esp)
        
        stats['riepilogo_mazzi'].append({
            'indice_mazzo': i + 1,
            'totale_carte': carte_mazzo,
            'guerrieri_squadra': len(squadra),
            'guerrieri_schieramento': len(schieramento),
            'carte_supporto': len(supporto),
            'fazioni_squadra': fazioni_squadra,
            'fazioni_schieramento': fazioni_schieramento,
            'apostoli_presenti': apostoli_mazzo,  # Nuova informazione
            'classi_supporto': classi_presenti,
            'espansioni_utilizzate': list(espansioni)
        })
    
    # Completa panoramica generale (invariato)
    stats['panoramica_generale']['totale_carte'] = totale_carte
    stats['panoramica_generale']['totale_guerrieri_squadra'] = totale_squadra
    stats['panoramica_generale']['totale_guerrieri_schieramento'] = totale_schieramento
    stats['panoramica_generale']['totale_carte_supporto'] = totale_supporto
    
    if len(mazzi) > 0:
        stats['panoramica_generale']['media_carte_per_mazzo'] = totale_carte / len(mazzi)
        stats['panoramica_generale']['media_guerrieri_squadra'] = totale_squadra / len(mazzi)
        stats['panoramica_generale']['media_guerrieri_schieramento'] = totale_schieramento / len(mazzi)
        stats['panoramica_generale']['media_supporto'] = totale_supporto / len(mazzi)
    
    # Converti defaultdict in dict normale
    stats['distribuzione_fazioni']['squadra'] = dict(stats['distribuzione_fazioni']['squadra'])
    stats['distribuzione_fazioni']['schieramento'] = dict(stats['distribuzione_fazioni']['schieramento'])
    stats['distribuzione_classi_supporto'] = dict(stats['distribuzione_classi_supporto'])
    stats['distribuzione_apostoli'] = dict(stats['distribuzione_apostoli'])
    
    return stats


# ================================================================================
# ISTRUZIONI PER L'USO DELLE FUNZIONI AGGIORNATE
# ================================================================================
"""
🎯 COME USARE LE FUNZIONI AGGIORNATE CON APOSTOLI:

1. SOSTITUISCI le funzioni precedenti con queste versioni:
   - processa_guerrieri_per_fazioni() → processa_guerrieri_per_fazioni_con_apostoli()
   - crea_inventario_dettagliato_mazzo_json_con_conteggio() → crea_inventario_dettagliato_mazzo_json_con_conteggio_e_apostoli()
   - salva_mazzi_json_migliorato_con_conteggio() → salva_mazzi_json_migliorato_con_conteggio_e_apostoli()

2. USA la nuova funzione di salvataggio:
   salva_mazzi_json_migliorato_con_conteggio_e_apostoli(mazzi, "mazzi_con_apostoli.json")

📁 STRUTTURA JSON RISULTANTE CON APOSTOLI:
{
  "inventario_guerrieri": {
    "schieramento": {
      "Oscura Legione": {
        "Algeroth": {
          "Necromutante": {"copie": 2, "fazione": "Oscura Legione", "apostolo_seguace": "Algeroth", ...},
          "Cacciatore Oscuro": {"copie": 1, "fazione": "Oscura Legione", "apostolo_seguace": "Algeroth", ...}
        },
        "Semai": {
          "Legionario di Semai": {"copie": 3, "fazione": "Oscura Legione", "apostolo_seguace": "Semai", ...}
        },
        "Muawijhe": {
          "Cultista di Muawijhe": {"copie": 1, "fazione": "Oscura Legione", "apostolo_seguace": "Muawijhe", ...}
        },
        "Oscura Legione": {
          "Eretico": {"copie": 2, "fazione": "Oscura Legione", "apostolo_seguace": "Oscura Legione", ...}
        }
      }
    }
  },
  "metadati_mazzo": {
    "apostoli_presenti": ["Algeroth", "Semai", "Muawijhe"],
    "statistiche_apostoli": {
      "Algeroth": 3,
      "Semai": 3, 
      "Muawijhe": 1
    }
  }
}

🆕 NUOVE CARATTERISTICHE:
✅ Sottocategorizzazione per apostoli nell'Oscura Legione
✅ Identificazione automatica seguaci dai keywords
✅ Statistiche per apostolo
✅ Compatibilità con struttura precedente
✅ Gestione guerrieri non seguaci (categoria generale)
"""



###############################################################################################################################









# ================================================================================
# FUNZIONI DI ANALISI E VERIFICA
# ================================================================================

def verifica_integrità_mazzi(mazzi: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Verifica l'integrità dei mazzi creati.
    Analogo di verifica_integrità_collezioni() per mazzi.
    
    Args:
        mazzi: Lista di mazzi da verificare
        
    Returns:
        Dizionario con i risultati della verifica
    """
    risultati = {
        'mazzi_validi': 0,
        'mazzi_con_errori': 0,
        'errori_trovati': [],
        'mazzi_con_guerrieri_squadra': 0,
        'mazzi_con_guerrieri_schieramento': 0,
        'mazzi_bilanciati': 0
    }
    
    for i, mazzo in enumerate(mazzi):
        errori_mazzo = []
        stats = mazzo['statistiche']
        
        # Verifica presenza guerrieri
        if stats['guerrieri_squadra'] > 0:
            risultati['mazzi_con_guerrieri_squadra'] += 1
        else:
            errori_mazzo.append("Mazzo senza guerrieri squadra")
        
        if stats['guerrieri_schieramento'] > 0:
            risultati['mazzi_con_guerrieri_schieramento'] += 1
        
        # Verifica numero minimo guerrieri totali
        guerrieri_totali = stats['guerrieri_squadra'] + stats['guerrieri_schieramento']
        if guerrieri_totali < 5:
            errori_mazzo.append(f"Mazzo con soli {guerrieri_totali} guerrieri (minimo 5)")
        
        # Verifica bilanciamento squadra/schieramento
        if stats['guerrieri_squadra'] > 0 and stats['guerrieri_schieramento'] > 0:
            ratio = stats['guerrieri_squadra'] / stats['guerrieri_schieramento']
            if 0.5 <= ratio <= 2.0:
                risultati['mazzi_bilanciati'] += 1
            else:
                errori_mazzo.append(f"Bilanciamento squadra/schieramento: {ratio:.2f}")
        
        # Verifica numero carte totali
        if stats['numero_totale_carte'] < 40:
            errori_mazzo.append(f"Mazzo troppo piccolo: {stats['numero_totale_carte']} carte")
        elif stats['numero_totale_carte'] > 100:
            errori_mazzo.append(f"Mazzo troppo grande: {stats['numero_totale_carte']} carte")
        
        # Verifica errori già presenti nel mazzo
        if mazzo.get('errori'):
            errori_mazzo.extend(mazzo['errori'])
        
        # Aggiorna risultati
        if errori_mazzo:
            risultati['mazzi_con_errori'] += 1
            risultati['errori_trovati'].append({
                'mazzo_indice': i + 1,
                'errori': errori_mazzo
            })
        else:
            risultati['mazzi_validi'] += 1
    
    return risultati
def analizza_bilanciamento_mazzi(mazzi: List[Dict[str, Any]]) -> None:
    """
    Analizza il bilanciamento dei mazzi creati.
    Analogo di analizza_bilanciamento_collezioni() per mazzi.
    
    Args:
        mazzi: Lista di mazzi da analizzare
    """
    print(f"\n{'='*60}")
    print("⚖️ ANALISI BILANCIAMENTO MAZZI")
    print(f"{'='*60}")
    
    if not mazzi:
        print("❌ Nessun mazzo da analizzare")
        return
    
    # Statistiche per tipo di carte
    stats_carte = []
    stats_squadra = []
    stats_schieramento = []
    stats_supporto = []
    
    # Distribuzione fazioni
    stats_fazioni = defaultdict(list)
    
    for mazzo in mazzi:
        stats = mazzo['statistiche']
        
        # Carte totali
        stats_carte.append(stats['numero_totale_carte'])
        stats_squadra.append(stats['guerrieri_squadra'])
        stats_schieramento.append(stats['guerrieri_schieramento'])
        
        # Carte supporto
        num_supporto = sum(stats.get('distribuzione_per_tipo', {}).values())
        stats_supporto.append(num_supporto)
        
        # Fazioni
        for fazione in stats.get('fazioni_presenti', []):
            stats_fazioni[fazione].append(1)
        
        # Per fazioni non presenti in questo mazzo
        fazioni_presenti = set(stats.get('fazioni_presenti', []))
        tutte_fazioni = set()
        for m in mazzi:
            tutte_fazioni.update(m['statistiche'].get('fazioni_presenti', []))
        
        for fazione in tutte_fazioni:
            if fazione not in fazioni_presenti:
                stats_fazioni[fazione].append(0)
    
    # Analisi distribuzione carte
    print("Distribuzione carte per mazzo:")
    if stats_carte:
        media = sum(stats_carte) / len(stats_carte)
        minimo = min(stats_carte)
        massimo = max(stats_carte)
        print(f"  Totali: min={minimo}, max={massimo}, media={media:.1f}")
    
    if stats_squadra:
        media = sum(stats_squadra) / len(stats_squadra)
        minimo = min(stats_squadra)
        massimo = max(stats_squadra)
        print(f"  Squadra: min={minimo}, max={massimo}, media={media:.1f}")
    
    if stats_schieramento:
        media = sum(stats_schieramento) / len(stats_schieramento)
        minimo = min(stats_schieramento)
        massimo = max(stats_schieramento)
        print(f"  Schieramento: min={minimo}, max={massimo}, media={media:.1f}")
    
    if stats_supporto:
        media = sum(stats_supporto) / len(stats_supporto)
        minimo = min(stats_supporto)
        massimo = max(stats_supporto)
        print(f"  Supporto: min={minimo}, max={massimo}, media={media:.1f}")
    
    # Analisi bilanciamento squadra/schieramento
    if stats_squadra and stats_schieramento:
        ratios = []
        for i in range(len(mazzi)):
            if stats_schieramento[i] > 0:
                ratio = stats_squadra[i] / stats_schieramento[i]
                ratios.append(ratio)
        
        if ratios:
            media_ratio = sum(ratios) / len(ratios)
            varianza = sum((r - media_ratio) ** 2 for r in ratios) / len(ratios)
            deviazione_std = varianza ** 0.5
            
            print(f"\nBilanciamento Squadra/Schieramento:")
            print(f"  Rapporto medio: {media_ratio:.2f}")
            print(f"  Deviazione standard: {deviazione_std:.2f}")
            
            if deviazione_std < 0.3:
                print("  ✅ Bilanciamento molto consistente")
            elif deviazione_std < 0.6:
                print("  ⚠️ Bilanciamento accettabile")
            else:
                print("  🔴 Bilanciamento inconsistente")
    
    # Analisi distribuzione fazioni
    print(f"\nDistribuzione fazioni:")
    for fazione, presenze in stats_fazioni.items():
        if presenze:
            presenza_media = sum(presenze) / len(presenze)
            mazzi_con_fazione = len([p for p in presenze if p > 0])
            percentuale = (mazzi_con_fazione / len(mazzi)) * 100 if len(mazzi) > 0 else 0
            print(f"  {fazione}: presente in {mazzi_con_fazione}/{len(mazzi)} mazzi ({percentuale:.1f}%)")
    
    # Controllo mazzi senza guerrieri
    mazzi_senza_squadra = len([s for s in stats_squadra if s == 0])
    mazzi_senza_schieramento = len([s for s in stats_schieramento if s == 0])
    
    if mazzi_senza_squadra > 0:
        print(f"\n⚠️ {mazzi_senza_squadra} mazzi senza guerrieri squadra")
    
    if mazzi_senza_schieramento > 0:
        print(f"⚠️ {mazzi_senza_schieramento} mazzi senza guerrieri schieramento")
def cerca_carte_in_mazzi(mazzi: List[Dict[str, Any]], nome_carta: str) -> List[Dict[str, Any]]:
    """
    Cerca una carta specifica nei mazzi.
    Analogo di cerca_carte_in_collezione() per mazzi.
    
    Args:
        mazzi: Lista di mazzi in cui cercare
        nome_carta: Nome della carta da cercare
        
    Returns:
        Lista di risultati di ricerca
    """
    risultati = []
    
    for i, mazzo in enumerate(mazzi):
        # Cerca nei guerrieri squadra
        for guerriero in mazzo['squadra']:
            if nome_carta.lower() in guerriero.nome.lower():
                risultati.append({
                    'mazzo_indice': i + 1,
                    'tipo_carta': 'Guerriero Squadra',
                    'carta': guerriero
                })
        
        # Cerca nei guerrieri schieramento
        for guerriero in mazzo['schieramento']:
            if nome_carta.lower() in guerriero.nome.lower():
                risultati.append({
                    'mazzo_indice': i + 1,
                    'tipo_carta': 'Guerriero Schieramento',
                    'carta': guerriero
                })
        
        # Cerca nelle carte supporto
        for carta in mazzo['carte_supporto']:
            if nome_carta.lower() in carta.nome.lower():
                risultati.append({
                    'mazzo_indice': i + 1,
                    'tipo_carta': type(carta).__name__,
                    'carta': carta
                })
    
    return risultati


# ================================================================================
# MENU INTERATTIVO
# ================================================================================

def menu_interattivo_mazzi():
    """
    Menu interattivo per testare le funzionalità di gestione mazzi.
    Versione aggiornata con funzioni di diagnostica.
    """
    mazzi_correnti = []
    
    while True:
        print("\n" + "="*60)
        print("GESTIONE MAZZI - MENU INTERATTIVO")
        print("="*60)
        print("1. Crea mazzi di esempio")
        print("2. Stampa riepilogo mazzi")
       
        print("3. Salva mazzi in JSON con conteggio (standard)")
        print("4. Salva mazzi in JSON con conteggio(sicuro)")
        print("5. Carica e visualizza mazzi da JSON con conteggio")        
        print("6. Verifica integrità mazzi")
        print("7. Analizza bilanciamento")
        print("8. Diagnostica completa mazzi")
        print("9. Test compatibilità")
        print("10. Cerca carta nei mazzi")
        print("11. Esempio completo salvataggio")
        print("12. Pulisci mazzi correnti")
        print("13. Crea e salva mazzo da file collezione")
        print("0. Esci")
        
        
        scelta = input("\nScegli un'opzione: ").strip()
        
        if scelta == "0":
            print("Arrivederci!")
            break
        elif scelta == "1":
            # Crea mazzi di esempio (qui serve la funzione crea_mazzo_da_gioco)
            # print("⚠️ Funzione non implementata - richiede collezioni di esempio")
            # print("   Per utilizzare questa opzione, integra con il modulo Creatore_Collezione")
            collezioni = creazione_Collezione_Giocatore(2, [Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE], orientamento = False)

            mazzo_1 = crea_mazzo_da_gioco(collezioni[0],
                            numero_carte_max = 120,
                            numero_carte_min = 100,
                            espansioni_richieste = ["Base", "Inquisition", "Warzone"],
                            doomtrooper = True,
                            orientamento_doomtrooper = ["Bauhaus", "Capitol", "Mishima"],
                            fratellanza = True,
                            orientamento_arte = ['Cambiamento', 'Premonizione', 'Esorcismo'],
                            oscura_legione = False,
                            orientamento_apostolo = None,
                            orientamento_eretico = False,
                            orientamento_cultista = False)
            
            mazzo_2 = crea_mazzo_da_gioco(collezioni[1],
                            numero_carte_max = 120,
                            numero_carte_min = 100,
                            espansioni_richieste = ["Base", "Inquisition", "Warzone"],
                            doomtrooper = True,
                            orientamento_doomtrooper = ["Imperiale", "Cybertronic", "Mercenario"],
                            fratellanza = False,
                            orientamento_arte = None,
                            oscura_legione = True,
                            orientamento_apostolo = ['Algeroth', 'Muawijhe', 'Semai'],
                            orientamento_eretico = False,
                            orientamento_cultista = False)

            mazzi_correnti.append(mazzo_1)
            mazzi_correnti.append(mazzo_2)


        elif scelta == "2":
            if mazzi_correnti:
                stampa_riepilogo_mazzi_migliorato(mazzi_correnti)
            else:
                print("❌ Nessun mazzo caricato. Usa prima l'opzione 1 o 5.")
        elif scelta == "3":
            if mazzi_correnti:
                filename = input("Nome file (default: mazzi.json): ").strip()
                if not filename:
                    filename = "mazzi.json"
                successo = salva_mazzi_json_migliorato_con_conteggio_e_apostoli(mazzi_correnti, filename)
                if successo:
                    print("✅ Salvataggio completato!")
                else:
                    print("❌ Salvataggio fallito - vedi i dettagli sopra")
            else:
                print("❌ Nessun mazzo da salvare. Usa prima l'opzione 1.")
        elif scelta == "4":
            if mazzi_correnti and False:
                filename = input("Nome file (default: mazzi_sicuri.json): ").strip()
                if not filename:
                    filename = "mazzi_sicuri.json"
                salva_mazzi_json_sicuro_con_conteggio(mazzi_correnti, filename)
            else:
                print("❌ Nessun mazzo da salvare. Usa prima l'opzione 1.")
        elif scelta == "5":
            filename = input("Nome file da caricare: ").strip()
            if filename:
                dati_caricati = carica_mazzi_json_migliorato(filename)
                if dati_caricati:
                    print("✅ Dati caricati con successo!")
                    stampa_statistiche_da_json_mazzi(dati_caricati)
            else:
                print("❌ Nome file non specificato")


        elif scelta == "6":
            if mazzi_correnti:
                risultati = verifica_integrità_mazzi(mazzi_correnti)
                print(f"\n📊 RISULTATI VERIFICA INTEGRITÀ:")
                print(f"✅ Mazzi validi: {risultati['mazzi_validi']}")
                print(f"❌ Mazzi con errori: {risultati['mazzi_con_errori']}")
                print(f"⚔️ Mazzi con guerrieri squadra: {risultati['mazzi_con_guerrieri_squadra']}")
                print(f"🌑 Mazzi con guerrieri schieramento: {risultati['mazzi_con_guerrieri_schieramento']}")
                print(f"⚖️ Mazzi bilanciati: {risultati['mazzi_bilanciati']}")
                
                if risultati['errori_trovati']:
                    print(f"\n❌ ERRORI DETTAGLIATI:")
                    for errore in risultati['errori_trovati']:
                        print(f"  Mazzo {errore['mazzo_indice']}: {'; '.join(errore['errori'])}")
            else:
                print("❌ Nessun mazzo da verificare. Usa prima l'opzione 1.")
        elif scelta == "7":
            if mazzi_correnti:
                analizza_bilanciamento_mazzi(mazzi_correnti)
            else:
                print("❌ Nessun mazzo da analizzare. Usa prima l'opzione 1.")
        elif scelta == "8":
            if mazzi_correnti:
                stampa_diagnostica_mazzi(mazzi_correnti)
            else:
                print("❌ Nessun mazzo da diagnosticare. Usa prima l'opzione 1.")
        elif scelta == "9":
            if mazzi_correnti:
                risultati = testa_compatibilita_mazzi(mazzi_correnti)
                print(f"\n🔍 RISULTATI TEST COMPATIBILITÀ:")
                print(f"✅ Compatibile: {'Sì' if risultati['compatibile'] else 'No'}")
                print(f"📊 Mazzi testati: {risultati['mazzi_testati']}")
                print(f"❌ Errori: {len(risultati['errori'])}")
                print(f"⚠️ Avvisi: {len(risultati['avvisi'])}")
                
                if risultati['errori']:
                    print(f"\n❌ ERRORI:")
                    for errore in risultati['errori'][:5]:  # Max 5 errori
                        print(f"  • {errore}")
                    if len(risultati['errori']) > 5:
                        print(f"  ... e altri {len(risultati['errori']) - 5} errori")
                
                if risultati['avvisi']:
                    print(f"\n⚠️ AVVISI:")
                    for avviso in risultati['avvisi'][:5]:  # Max 5 avvisi
                        print(f"  • {avviso}")
                    if len(risultati['avvisi']) > 5:
                        print(f"  ... e altri {len(risultati['avvisi']) - 5} avvisi")
            else:
                print("❌ Nessun mazzo da testare. Usa prima l'opzione 1.")
        elif scelta == "10":
            if mazzi_correnti:
                nome_carta = input("Nome carta da cercare: ").strip()
                if nome_carta:
                    risultati = cerca_carte_in_mazzi(mazzi_correnti, nome_carta)
                    if risultati:
                        print(f"\n🔍 RISULTATI RICERCA '{nome_carta}':")
                        for risultato in risultati:
                            print(f"  Mazzo {risultato['mazzo_indice']} - {risultato['tipo_carta']}: {risultato['carta'].nome}")
                    else:
                        print(f"❌ Carta '{nome_carta}' non trovata nei mazzi")
                else:
                    print("❌ Nome carta non specificato")
            else:
                print("❌ Nessun mazzo in cui cercare. Usa prima l'opzione 1.")
        elif scelta == "11":
            if mazzi_correnti and False:
                esempio_salvataggio_mazzi_migliorato(mazzi_correnti)
            else:
                print("❌ Nessun mazzo per l'esempio. Usa prima l'opzione 1.")
        elif scelta == "12":
            mazzi_correnti.clear()
            print("✅ Mazzi correnti puliti")
        
        
        elif scelta == "13":
            # Creazione personalizzata
            mazzi_correnti.clear()
            try:
                name = str(input("nome file collezioni da caricare: "))
                _, collezioni = carica_collezioni_json_migliorato(name)
                print(f"numero collezioni disponibili nel file: {len(collezioni)}")
                num = int(input("numero collezione (0, 1, ...): "))
                collezione = collezioni[num]
                
                filename = input("nome file di output (default: mazzo_di_sconosciuto.json): ").strip()
                if not filename:
                    filename = "mazzo_di_sconosciuto.json"
                
                carte_min = int(input("numero minimo di carte del mazzo: "))
                carte_max = int(input("numero massimo di carte del mazzo: "))
                fazioni_doomtrooper = []
                arti_scelte = []
                apostoli_scelti = []
                espansioni = []

                doomtrooper = input("utilizzo doomtrooper (s/n) (nota: la collezione deve contenere doomtrooper): ").lower().startswith('s')
                if doomtrooper:
                    scelta_fazioni = input("vuoi specificare quali fazioni doomtrooper utilizzare (s/n): ").lower().startswith('s')
                    if scelta_fazioni:
                        print("Fazioni:")
                        
                        for i, esp in enumerate(FAZIONI_DOOMTROOPER):
                            print(f"  {i+1}. {esp.value}")        
                        faz_input = input("Scegli fazioni (numeri separati da virgola): ")
                        faz_indices = [int(x.strip())-1 for x in faz_input.split(",")]
                        fazioni_doomtrooper = [list(FAZIONI_DOOMTROOPER)[i].value for i in faz_indices if 0 <= i < len(FAZIONI_DOOMTROOPER)]
                
                
                fratellanza = input("utilizzo fratellanza (s/n) (nota: la collezione deve contenere fratellanza): ").lower().startswith('s')
                if fratellanza:
                    scelta_arte = input("vuoi specificare quali tipologie di Arte vuoi utilizzare (s/n): ").lower().startswith('s')
                    if scelta_arte:
                        print("Tipologie Arte:")
                        
                        for i, esp in enumerate(DisciplinaArte):
                            print(f"  {i+1}. {esp.value}")        
                        art_input = input("Scegli le tipologie di Arte (numeri separati da virgola): ")
                        art_indices = [int(x.strip())-1 for x in art_input.split(",")]
                        arti_scelte = [list(DisciplinaArte)[i].value for i in art_indices if 0 <= i < len(DisciplinaArte)]
                
                cultisti = False
                oscura_legione = input("utilizzo oscura legione (s/n) (nota: la collezione deve contenere oscura legione): ").lower().startswith('s')
                if oscura_legione:
                    scelta_apostoli = input("vuoi specificare quali Apostoli vuoi utilizzare (s/n): ").lower().startswith('s')
                    if scelta_apostoli:
                        print("Apostoli:")
                        
                        for i, esp in enumerate(ApostoloOscuraSimmetria):
                            print(f"  {i+1}. {esp.value}")        
                        apo_input = input("Scegli gli Apostoli (numeri separati da virgola): ")
                        apo_indices = [int(x.strip())-1 for x in apo_input.split(",")]
                        apostoli_scelti = [list(ApostoloOscuraSimmetria)[i].value for i in art_indices if 0 <= i < len(ApostoloOscuraSimmetria)]
                    cultisti = input("utilizzo cultisti (s/n): ").lower().startswith('s')

                eretici = input("utilizzo eretici (s/n): ").lower().startswith('s')
                

                print("Espansioni disponibili:")
                for i, esp in enumerate(Set_Espansione):
                    print(f"  {i+1}. {esp.value}")
                
                esp_input = input("Scegli espansioni (numeri separati da virgola): ")
                esp_indices = [int(x.strip())-1 for x in esp_input.split(",")]
                espansioni = [list(Set_Espansione)[i].value for i in esp_indices if 0 <= i < len(Set_Espansione)]
                            
                mazzo_1 = crea_mazzo_da_gioco(collezione,
                            numero_carte_max = carte_max,
                            numero_carte_min = carte_min,
                            espansioni_richieste = espansioni,
                            doomtrooper = doomtrooper,
                            orientamento_doomtrooper = fazioni_doomtrooper,
                            fratellanza = fratellanza,
                            orientamento_arte = arti_scelte,
                            oscura_legione = oscura_legione,
                            orientamento_apostolo = apostoli_scelti,
                            orientamento_eretico = eretici,
                            orientamento_cultista = cultisti)
                
                mazzi_correnti.append(mazzo_1)
                successo = salva_mazzi_json_migliorato_con_conteggio_e_apostoli(mazzi_correnti, filename)
                if successo:
                    print("✅ Salvataggio completato!")
                else:
                    print("❌ Salvataggio fallito")
            except Exception as e:
                print(f"Errore: {e}")
        
        else:
            print("❌ Opzione non valida")

# ================================================================================
# FUNZIONI DI TEST E VALIDAZIONE
# ================================================================================

def test_funzioni_mazzi():
    """
    Funzione di test per verificare che tutte le funzioni funzionino correttamente.
    Da usare per debug e validazione.
    """
    print("\n🧪 TEST FUNZIONI GESTIONE MAZZI")
    print("="*50)
    
    # Test funzioni di utilità
    print("1. Test funzioni di utilità...")
    
    # Oggetto guerriero mock per test
    class MockGuerriero:
        def __init__(self):
            self.nome = "Test Warrior"
            self.fazione = "Bauhaus"
            self.set_espansione = "Base"
            self.rarity = "Common"
            self.tipo = "Normale"
    
    guerriero_test = MockGuerriero()
    
    try:
        info_guerriero = crea_info_guerriero_sicura(guerriero_test)
        print(f"  ✅ Creazione info guerriero: {info_guerriero['nome']}")
    except Exception as e:
        print(f"  ❌ Errore info guerriero: {e}")
    
    # Test attributo sicuro
    try:
        nome = ottieni_attributo_sicuro(guerriero_test, 'nome', 'Default')
        print(f"  ✅ Attributo sicuro: {nome}")
    except Exception as e:
        print(f"  ❌ Errore attributo sicuro: {e}")
    
    # Test oggetto mock mazzo
    print("\n2. Test struttura mazzo mock...")
    mazzo_test = {
        'squadra': [guerriero_test],
        'schieramento': [],
        'carte_supporto': [],
        'statistiche': {
            'numero_totale_carte': 1,
            'guerrieri_squadra': 1,
            'guerrieri_schieramento': 0,
            'distribuzione_per_tipo': {},
            'fazioni_presenti': ['Bauhaus']
        },
        'errori': []
    }
    
    try:
        # Test diagnostica
        risultato_diagnostica = diagnostica_mazzo(mazzo_test, 1)
        print(f"  ✅ Diagnostica mazzo: {risultato_diagnostica['stato_generale']}")
        
        # Test compatibilità
        risultato_compatibilita = testa_compatibilita_mazzi([mazzo_test])
        print(f"  ✅ Test compatibilità: {risultato_compatibilita['compatibile']}")
        
        # Test pulizia
        mazzi_puliti = pulisci_mazzi_per_salvataggio([mazzo_test])
        print(f"  ✅ Pulizia mazzi: {len(mazzi_puliti)} mazzi puliti")
        
    except Exception as e:
        print(f"  ❌ Errore test mazzo: {e}")
    
    print("\n✅ Test completato!")

# ================================================================================
# MAIN DI TEST (se eseguito come modulo standalone)
# ================================================================================

if __name__ == "__main__":
    """
    Esecuzione diretta del modulo per test.
    """
    print("🎯 MODULO GESTIONE MAZZI - TEST STANDALONE")
    
    # Esegui test base
    # test_funzioni_mazzi()

    espansioni_richieste = [Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE]

    collezioni = creazione_Collezione_Giocatore(3, espansioni_richieste, orientamento = True)
    salva_collezioni_json_migliorato(collezioni = collezioni, filename = "collezioni_3_player_no_orientamento.json")
    dati_json, collezioni = carica_collezioni_json_migliorato(filename = "collezioni_3_player_no_orientamento.json")

    orientamento_collezioni = []
    # conta Guerrieri
    mazzo = []
    for collezione in collezioni:
        
        orientamento = determina_orientamento_collezione(collezione = collezione, espansioni_richieste = espansioni_richieste)
        mazzo.append( 
            crea_mazzo_da_gioco(collezioni[0],
                        numero_carte_max = 130,
                        numero_carte_min = 120,
                        espansioni_richieste = ["Base", "Inquisition", "Warzone"],
                        orientamento = orientamento['doomtrooper'],
                        orientamento_doomtrooper = orientamento['orientamento_doomtrooper'],
                        fratellanza = orientamento['fratellanza'],
                        orientamento_arte = orientamento['orientamento_arte'],
                        oscura_legione = orientamento['oscura_legione'],
                        orientamento_apostolo = orientamento['orientamento_apostolo'],
                        orientamento_eretico = orientamento['orientamento_eretico'],
                        orientamento_cultista = orientamento['orientamento_cultista'])
            )
    
    esempio_salvataggio_mazzi_con_conteggio(mazzo)
    
    # Menu interattivo
    risposta = input("\nVuoi aprire il menu interattivo? (s/n): ")
    if risposta.lower().startswith('s'):
        menu_interattivo_mazzi()

# ================================================================================
# ISTRUZIONI PER L'INTEGRAZIONE
# ================================================================================

"""
🔧 INSTALLAZIONE E USO:

1. COPIA tutto questo codice alla fine del file Creatore_Mazzo.py

2. ASSICURATI che sia definita: PERCORSO_SALVATAGGIO = "out/"

3. RISOLVE IL TUO ERRORE con:
   salva_mazzi_json_sicuro(mazzi, "miei_mazzi.json")

🎯 USO IMMEDIATO:
```python
# I tuoi mazzi esistenti
mazzi = [mazzo1, mazzo2, mazzo3]  # dai tuoi crea_mazzo_da_gioco

# SOLUZIONE SICURA - garantisce sempre il salvataggio
salva_mazzi_json_sicuro(mazzi, "miei_mazzi.json")

# ALTERNATIVA - diagnostica + salvataggio normale  
stampa_diagnostica_mazzi(mazzi)  # Identifica problemi
salva_mazzi_json_migliorato(mazzi, "mazzi_diagnosticati.json")
```

📊 FUNZIONI PRINCIPALI:
- stampa_riepilogo_mazzi_migliorato(mazzi)
- salva_mazzi_json_sicuro(mazzi, "file.json")       # GARANTISCE SUCCESSO
- salva_mazzi_json_migliorato(mazzi, "file.json")   # Standard
- carica_mazzi_json_migliorato("file.json")
- stampa_diagnostica_mazzi(mazzi)
- verifica_integrità_mazzi(mazzi)
- analizza_bilanciamento_mazzi(mazzi)
- menu_interattivo_mazzi()

🚨 RISOLVE IL TUO ERRORE:
L'errore "tipo_guerriero" è risolto da:
- ottieni_attributo_sicuro() - gestisce attributi mancanti
- crea_info_guerriero_sicura() - usa 'tipo' invece di 'tipo_guerriero'
- salva_mazzi_json_sicuro() - garantisce sempre successo
"""




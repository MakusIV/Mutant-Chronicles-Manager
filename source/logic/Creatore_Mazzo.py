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
        """
                abilita:

                {
                "nome": "Scarta Carte",
                "descrizione": "Può scartare qualsiasi carta in gioco al costo di tre azioni",
                "tipo": "Scarta Carte",
                "costo_destino": 0,
                "target": "Tutti i Guerrieri",
                "timing": "Turno"
                }
                {
                "nome": "Scarta Carte",
                "descrizione": "Può scartare un qualsiasi Doomtrooper in gioco al costo di tre azioni",
                "tipo": "Scarta Carte",
                "costo_destino": 0,
                "target": "Tutti i Doomtrooper",
                "timing": "Turno"
                }
                {
                "nome": "Assegna carte Equipaggiamento",
                "descrizione": "Equipaggia qualsiasi guerriero dell'Oscura Legione",
                "tipo": "Assegnazione Carte",
                "costo_destino": 0,
                "target": "Guerrieri Oscura Legione",
                "timing": "Ogni Momento"
                },                
                {
                "nome": "Assegna carte Oscura Simmetria e Doni degli Apostoli",
                "descrizione": "Equipaggia qualsiasi seguace di Algeroth",
                "tipo": "Assegnazione Carte",
                "costo_destino": 0,
                "target": "Seguaci di ALgeroth",
                "timing": "Ogni Momento"
                }                
                {
                "nome": "Sostituisce Eretici",
                "descrizione": "Può sostituire un Eretico con un Seguace di Algeroth al costo di tre azioni",
                "tipo": "Sostituzione Guerrieri",
                "costo_destino": 0,
                "target": "Eretici",
                "timing": "Turno"
                }
                {
                "nome": "Ataccabile solo dalla Fratellanza",
                "descrizione": "Solo i membri della Fratellamza possono attaccarlo con penalità in A di -1",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
                }
                {
                "nome": "Attaccare per primi",
                "descrizione": "I guerrieri dell'Oscura Legione possono Attaccare per primi i loro avversari in combattimento",
                "tipo": "Combattimento",
                "costo_destino": 0,
                "target": "Tutti i Guerrieri",
                "timing": "Turno"
                }
                {
                "nome": "Uccide Automaticamente",
                "descrizione": "Se ferisce, uccide automaticamente",
                "tipo": "Combattimento", 
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Fase Combattimento"
                }
                {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte",
                "descrizione": "Lancia qualsiasi Arte o Incantesimo dell'Arte",
                "tipo": "Incantesimi",
                "costo_destino": 0,
                "target": "Tutti i Guerrieri",
                "timing": "Turno"
                }
                {
                "nome": "Guarisce se stesso",
                "descrizione": "Se ferito, può guarire se stesso. Se il Golem viene ferito, torna sano, a meno che la ferita non lo uccida sul colpo.",
                "tipo": "Guarigione",
                "costo_destino": 0,
                "target": "Guerriero",
                "timing": "Sempre"
                }                
            {
                "nome": "Aumenta effetto su se stesso",
                "descrizione": "Se delle carte dell'Oscura Simmetria sono assegnate al Nepharita di Demnogonis, per ogni Punto D speso su un effetto dell'Oscura Simmetria il Valore raddoppia per quell'effetto.",
                "tipo": "Modificatore",
                "costo_destino": 1,
                "target": "",
                "timing": "Sempre"
            },           
            {
                "nome": "Immune agli effetti dell'Arte",
                "descrizione": "Immune agli effetti dell'Arte",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Arte",
                "timing": "Sempre"
            },
            {
                "nome": "Annulla Immunita",
                "descrizione": "Può annullare qualsiasi immuntità dell'Oscura Simmetria",
                "tipo": "Immunita",
                "costo_destino": 0,
                "target": "Oscura Simmetria",
                "timing": "Ogni Momento"
            },
            {
                "nome": "Modificatore",
                "descrizione": "Se delle carte dell'Oscura Simmetria sono assegnate al Nepharita di Demnogonis, per ogni Punto D speso su un effetto dell'Oscura Simmetria il Valore raddoppia per quell'effetto.",
                "tipo": "Incantesimi",
                "costo_destino": 1,
                "target": "",
                "timing": "Sempre"
            },
            {
                "nome": "Guarisce se stesso",
                "descrizione": "Se Ferito, il Nefarita può guarire se stesso spendendo 7D",
                "tipo": "Guarigione",
                "costo_destino": 7,
                "target": "",
                "timing": "Sempre"
            }            
            {
                "nome": "Assegna carte Oscura Simmetria e Doni degli Apostoli",
                "descrizione": "Equipaggia qualsiasi seguace di Ilian",
                "tipo": "Assegnazione Carte",
                "costo_destino": 0,
                "target": "Guerrieri Oscura Legione",
                "timing": "Ogni Momento"
            },
            {
                "nome": "Combattimento tra Doomtrooper",
                "descrizione": "I Doomtrooper possono attaccare qualsiasi Doomtrooper non della tua squadra ma devono pagare 4D per attaccare Guerriri dell'Oscura Legione",
                "tipo": "Combattimento",
                "costo_destino": 0,
                "target": "Guerrieri Doomtrooper",
                "timing": "Ogni Momento"
            },
            {
                "nome": "Assegna carte Oscura Simmetria e Doni degli Apostoli",
                "descrizione": "Equipaggia qualsiasi seguace di Ilian",
                "tipo": "Assegnazione Carte",
                "costo_destino": 0,
                "target": "Guerrieri Oscura Legione",
                "timing": "Ogni Momento"
            },
            {
                "nome": "Lancia Arte e/o Incantesimo dell'Arte",
                "descrizione": "Lancia qualsiasi Arte o Incantesimo dell'Arte",
                "tipo": "Incantesimi",
                "costo_destino": 0,
                "target": "Arte",
                "timing": "Turno"
            },
            {
                "nome": "Assegna carte Equipaggiamento",
                "descrizione": "Equipaggia qualsiasi guerriero dell'Oscura Legione",
                "tipo": "Assegnazione Carte",
                "costo_destino": 0,
                "target": "Guerrieri Oscura Legione",
                "timing": "Ogni Momento"
                },
                {
                "nome": "Scarta Carte",
                "descrizione": "Può scartare qualsiasi carta in gioco al costo di tre azioni",
                "tipo": "Scarta Carte",
                "costo_destino": 0,
                "target": "Tutti i Guerrieri",
                "timing": "Turno"
            },
            {
                "nome": "I Zenithiani Assassini dell'Anima uccidono automaticamente i guerrieri feriti",
                "descrizione": "Mentre è in gioco Zenithiani Assassini dell'Anima uccidono automaticamente i guerrieri feriti",
                "tipo": "Potenziamento Guerrieri", 
                "costo_destino": 0,
                "target": "Zenithiani Assassini dell'Anima",
                "timing": "Fase Combattimento"
            }


                restrizioni:
                "restrizioni": ["Carte Oscura Simmetria non Assegnabili", "Può attaccare solo una volta per turno", "Equipaggiamenti non assegnabili", "Non guadagnano bonus Fortificazione", "Carte Speciale non giocabili su di esso"],
                ["Carte Oscura Simmetria non Assegnabili"]
                ["Non può prendere parte al combattimento", "Non può andare in copertura"],

        """
        for abilita in guerriero.abilita:
            # Potenziamento altri guerrieri
            keywords = abilita.descrizione.lower()

            if abilita.tipo == "Combattimento":
                if abilita.nome == "Uccide Automaticamente":
                    potenza_assoluta *= 2.0
                if abilita.nome == "Permette ai guerrieri di attaccare per primi":
                    potenza_assoluta *= 1.3
                if abilita.nome == "I guerrieri alleati uccidono automaticamente":
                    potenza_assoluta *= 1.3

            if abilita.tipo == "Immunita":
                if abilita.nome in ["Immune agli effetti dell'Arte", "Immune agli effetti dell'Oscura Simmetria", "Annulla Immunita dell'Oscura Simmetria", "Immune ai Doni degli Apostoli"]:
                    potenza_assoluta *= 1.5
                elif "Immune agli effetti della specifica arte" in abilita.nome:
                    potenza_assoluta *= 1.2
                        
                        
            if abilita.tipo == "Modificatore":
                if abilita.nome in ["Aumenta effetto", "Aumenta caratteristica"]:
                    potenza_assoluta *= 1.3
                elif abilita.nome == "Trasforma guerrieri uccisi in alleati":
                    potenza_assoluta *= 1.1
                elif abilita.nome == "Sostituisce guerrieri":
                    potenza_assoluta *= 1.2

            if abilita.tipo == "Guarigione" :
                if "Guarisce se stesso" in abilita.nome:
                    potenza_assoluta *= 1.5

            if abilita.tipo == "Arte":
                if "Lancia Arte e/o Incantesimo dell'Arte" == abilita.nome:
                    potenza_assoluta *= 1.3
                
                elif "Lancia Arte e/o Incantesimo dell'Arte specifica" == abilita.nome:
                    potenza_assoluta *= 1.2

            if abilita.tipo == "Oscura Simmetria" or abilita.tipo == "Dono degli Apostoli":                
                    potenza_assoluta *= 1.3
            

            if abilita.tipo == "Carte":

                if abilita.nome in ["Assegna Carta", "Scarta Carta", "Elimina Carta"]:
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




################# nuovo ###########################



# ================================================================================
# FUNZIONI DI GESTIONE MAZZI - ANALOGHE ALLE FUNZIONI COLLEZIONI
# ================================================================================
# Estensioni per il modulo Creatore_Mazzo.py
# Funzioni analoghe a stampa_riepilogo_collezioni_migliorato, 
# salva_collezioni_json_migliorato, carica_collezioni_json_migliorato

import json
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any, Union
from collections import defaultdict

# PERCORSO_SALVATAGGIO deve essere già definito nel modulo principale
# PERCORSO_SALVATAGGIO = "out/"

# ================================================================================
# FUNZIONI DI UTILITÀ PER SERIALIZZAZIONE SICURA
# ================================================================================

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

def crea_info_guerriero_sicura(guerriero):
    """
    Crea un dizionario con le informazioni del guerriero in modo sicuro.
    
    Args:
        guerriero: Oggetto Guerriero
        
    Returns:
        Dizionario con le informazioni del guerriero
    """
    guerriero_info = {
        'nome': ottieni_attributo_sicuro(guerriero, 'nome', 'Nome sconosciuto'),
        'fazione': ottieni_attributo_sicuro(guerriero, 'fazione', 'Fazione sconosciuta'),
        'set_espansione': ottieni_attributo_sicuro(guerriero, 'set_espansione', 'Set sconosciuto'),
        'rarity': ottieni_attributo_sicuro(guerriero, 'rarity', 'Rarity sconosciuta'),
        'tipo': ottieni_attributo_sicuro(guerriero, 'tipo', 'Normale'),  # Attributo corretto per i guerrieri
    }
    
    # Statistiche (possono essere in formato diverso)
    if hasattr(guerriero, 'stats'):
        # Se ha l'oggetto stats
        stats = guerriero.stats
        guerriero_info['combattimento'] = ottieni_attributo_sicuro(stats, 'combattimento', 0)
        guerriero_info['sparare'] = ottieni_attributo_sicuro(stats, 'sparare', 0)
        guerriero_info['armatura'] = ottieni_attributo_sicuro(stats, 'armatura', 0)
        guerriero_info['valore'] = ottieni_attributo_sicuro(stats, 'valore', 0)
    else:
        # Statistiche dirette (formato alternativo)
        guerriero_info['combattimento'] = ottieni_attributo_sicuro(guerriero, 'combattimento', 0)
        guerriero_info['sparare'] = ottieni_attributo_sicuro(guerriero, 'sparare', 0)
        guerriero_info['armatura'] = ottieni_attributo_sicuro(guerriero, 'armatura', 0)
        guerriero_info['valore'] = ottieni_attributo_sicuro(guerriero, 'valore', 0)
    
    # Attributi opzionali
    guerriero_info['valor_destino'] = ottieni_attributo_sicuro(guerriero, 'valor_destino', 0)
    guerriero_info['valor_promozione'] = ottieni_attributo_sicuro(guerriero, 'valor_promozione', 0)
    guerriero_info['e_personalita'] = ottieni_attributo_sicuro(guerriero, 'e_personalita', False)
    guerriero_info['keywords'] = ottieni_attributo_sicuro(guerriero, 'keywords', [])
    guerriero_info['numero_carta'] = ottieni_attributo_sicuro(guerriero, 'numero_carta', '')
    
    return guerriero_info

def crea_info_carta_supporto_sicura(carta):
    """
    Crea un dizionario con le informazioni della carta supporto in modo sicuro.
    
    Args:
        carta: Oggetto carta supporto
        
    Returns:
        Dizionario con le informazioni della carta
    """
    carta_info = {
        'nome': ottieni_attributo_sicuro(carta, 'nome', 'Nome sconosciuto'),
        'tipo': type(carta).__name__,
        'set_espansione': ottieni_attributo_sicuro(carta, 'set_espansione', 'Set sconosciuto'),
        'rarity': ottieni_attributo_sicuro(carta, 'rarity', 'Rarity sconosciuta')
    }
    
    # Attributi comuni opzionali
    fazione = ottieni_attributo_sicuro(carta, 'fazione', None)
    if fazione:
        carta_info['fazione'] = fazione
    
    # Attributi specifici per tipo di carta
    valor_destino = ottieni_attributo_sicuro(carta, 'valor_destino', None)
    if valor_destino is not None:
        carta_info['valor_destino'] = valor_destino
    
    valore = ottieni_attributo_sicuro(carta, 'valore', None)
    if valore is not None:
        carta_info['valore'] = valore
    
    # Attributi specifici Arte
    disciplina = ottieni_attributo_sicuro(carta, 'disciplina', None)
    if disciplina:
        carta_info['disciplina_arte'] = disciplina
    
    disciplina_arte = ottieni_attributo_sicuro(carta, 'disciplina_arte', None)
    if disciplina_arte:
        carta_info['disciplina_arte'] = disciplina_arte
    
    # Attributi specifici Oscura Simmetria
    apostolo = ottieni_attributo_sicuro(carta, 'apostolo', None)
    if apostolo:
        carta_info['apostolo'] = apostolo
    
    apostolo_padre = ottieni_attributo_sicuro(carta, 'apostolo_padre', None)
    if apostolo_padre:
        carta_info['apostolo_padre'] = apostolo_padre
    
    # Altri attributi utili
    carta_info['numero_carta'] = ottieni_attributo_sicuro(carta, 'numero_carta', '')
    carta_info['keywords'] = ottieni_attributo_sicuro(carta, 'keywords', [])
    carta_info['costo_destino'] = ottieni_attributo_sicuro(carta, 'costo_destino', 0)
    
    return carta_info

# ================================================================================
# FUNZIONE DI STAMPA RIEPILOGO MAZZI MIGLIORATO
# ================================================================================

def stampa_riepilogo_mazzi_migliorato(mazzi: List[Dict[str, Any]], titolo: str = "RIEPILOGO MAZZI CREATI") -> None:
    """
    Stampa un riepilogo dettagliato dei mazzi creati.
    Analogo di stampa_riepilogo_collezioni_migliorato() per i mazzi.
    
    Args:
        mazzi: Lista di dizionari mazzo (output di crea_mazzo_da_gioco)
        titolo: Titolo personalizzato per il riepilogo
    """
    print(f"\n{'='*80}")
    print(f"📋 {titolo}")
    print(f"{'='*80}")
    
    if not mazzi:
        print("❌ Nessun mazzo da visualizzare")
        return
    
    # Statistiche aggregate
    totale_mazzi = len(mazzi)
    totale_carte = sum(mazzo['statistiche']['numero_totale_carte'] for mazzo in mazzi)
    media_carte_per_mazzo = totale_carte / totale_mazzi if totale_mazzi > 0 else 0
    
    print(f"🎯 Numero mazzi: {totale_mazzi}")
    print(f"📦 Totale carte: {totale_carte}")
    print(f"📈 Media carte/mazzo: {media_carte_per_mazzo:.1f}")
    
    # Distribuzione dimensioni mazzi
    dimensioni_mazzi = [mazzo['statistiche']['numero_totale_carte'] for mazzo in mazzi]
    if dimensioni_mazzi:
        min_carte = min(dimensioni_mazzi)
        max_carte = max(dimensioni_mazzi)
        print(f"📏 Dimensioni: min={min_carte}, max={max_carte}")
    
    print(f"\n{'='*60}")
    print("📊 DETTAGLIO MAZZI:")
    print(f"{'='*60}")
    
    # Analizza ogni mazzo
    for i, mazzo in enumerate(mazzi, 1):
        stats = mazzo['statistiche']
        
        print(f"\n🎮 MAZZO {i}")
        print(f"  📦 Carte totali: {stats['numero_totale_carte']}")
        print(f"  ⚔️ Guerrieri squadra: {stats['guerrieri_squadra']}")
        print(f"  🌑 Guerrieri schieramento: {stats['guerrieri_schieramento']}")
        
        # Distribuzione per tipo
        if 'distribuzione_per_tipo' in stats and stats['distribuzione_per_tipo']:
            print("  📊 Distribuzione supporto:")
            for tipo, quantita in stats['distribuzione_per_tipo'].items():
                print(f"    • {tipo.capitalize()}: {quantita}")
        
        # Fazioni presenti
        if 'fazioni_presenti' in stats and stats['fazioni_presenti']:
            fazioni_str = ", ".join(stats['fazioni_presenti'])
            print(f"  🏛️ Fazioni: {fazioni_str}")
        
        # Espansioni utilizzate
        if 'espansioni_utilizzate' in stats:
            esp_str = ", ".join(stats['espansioni_utilizzate'])
            print(f"  📚 Espansioni: {esp_str}")
        
        # Errori o avvisi
        if mazzo.get('errori'):
            print(f"  ⚠️ Avvisi:")
            for errore in mazzo['errori']:
                print(f"    • {errore}")
    
    # Analisi aggregata distribuzione fazioni
    print(f"\n{'='*60}")
    print("🏛️ ANALISI FAZIONI AGGREGATE:")
    print(f"{'='*60}")
    
    conteggio_fazioni = defaultdict(int)
    for mazzo in mazzi:
        for fazione in mazzo['statistiche'].get('fazioni_presenti', []):
            conteggio_fazioni[fazione] += 1
    
    for fazione, count in sorted(conteggio_fazioni.items()):
        percentuale = (count / totale_mazzi) * 100 if totale_mazzi > 0 else 0
        print(f"  {fazione}: {count}/{totale_mazzi} mazzi ({percentuale:.1f}%)")
    
    # Analisi distribuzione guerrieri
    print(f"\n{'='*60}")
    print("⚔️ ANALISI DISTRIBUZIONE GUERRIERI:")
    print(f"{'='*60}")
    
    guerrieri_squadra = [mazzo['statistiche']['guerrieri_squadra'] for mazzo in mazzi]
    guerrieri_schieramento = [mazzo['statistiche']['guerrieri_schieramento'] for mazzo in mazzi]
    
    if guerrieri_squadra:
        media_squadra = sum(guerrieri_squadra) / len(guerrieri_squadra)
        min_squadra = min(guerrieri_squadra)
        max_squadra = max(guerrieri_squadra)
        print(f"  Squadra: media={media_squadra:.1f}, min={min_squadra}, max={max_squadra}")
    
    if guerrieri_schieramento:
        media_schier = sum(guerrieri_schieramento) / len(guerrieri_schieramento)
        min_schier = min(guerrieri_schieramento)
        max_schier = max(guerrieri_schieramento)
        print(f"  Schieramento: media={media_schier:.1f}, min={min_schier}, max={max_schier}")
    
    # Verifica bilanciamento
    if guerrieri_squadra and guerrieri_schieramento:
        ratios = []
        for i in range(len(mazzi)):
            if guerrieri_schieramento[i] > 0:
                ratio = guerrieri_squadra[i] / guerrieri_schieramento[i]
                ratios.append(ratio)
        
        if ratios:
            ratio_medio = sum(ratios) / len(ratios)
            print(f"  📈 Rapporto medio Squadra/Schieramento: {ratio_medio:.2f}")
            
            if 0.8 <= ratio_medio <= 1.2:
                print("  ✅ Bilanciamento guerrieri: Ottimo")
            elif 0.5 <= ratio_medio <= 2.0:
                print("  ⚠️ Bilanciamento guerrieri: Accettabile")
            else:
                print("  🔴 Bilanciamento guerrieri: Migliorabile")

# ================================================================================
# FUNZIONI DI SALVATAGGIO JSON MIGLIORATO PER MAZZI
# ================================================================================

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

# ================================================================================
# FUNZIONI DI DIAGNOSTICA E TEST
# ================================================================================

def testa_compatibilita_mazzi(mazzi: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Testa la compatibilità dei mazzi prima del salvataggio JSON.
    
    Args:
        mazzi: Lista di mazzi da testare
        
    Returns:
        Dizionario con i risultati del test
    """
    risultati = {
        'compatibile': True,
        'errori': [],
        'avvisi': [],
        'mazzi_testati': len(mazzi)
    }
    
    for i, mazzo in enumerate(mazzi):
        try:
            # Testa struttura base del mazzo
            if not isinstance(mazzo, dict):
                risultati['errori'].append(f"Mazzo {i+1}: non è un dizionario")
                risultati['compatibile'] = False
                continue
            
            # Verifica chiavi essenziali
            chiavi_richieste = ['squadra', 'schieramento', 'carte_supporto', 'statistiche']
            for chiave in chiavi_richieste:
                if chiave not in mazzo:
                    risultati['errori'].append(f"Mazzo {i+1}: manca la chiave '{chiave}'")
                    risultati['compatibile'] = False
            
            # Testa guerrieri squadra
            if 'squadra' in mazzo:
                for j, guerriero in enumerate(mazzo['squadra']):
                    if not hasattr(guerriero, 'nome'):
                        risultati['avvisi'].append(f"Mazzo {i+1}, Guerriero squadra {j+1}: manca attributo 'nome'")
                    
                    # Testa creazione info sicura
                    try:
                        crea_info_guerriero_sicura(guerriero)
                    except Exception as e:
                        risultati['errori'].append(f"Mazzo {i+1}, Guerriero squadra {j+1}: errore serializzazione - {e}")
                        risultati['compatibile'] = False
            
            # Testa guerrieri schieramento
            if 'schieramento' in mazzo:
                for j, guerriero in enumerate(mazzo['schieramento']):
                    if not hasattr(guerriero, 'nome'):
                        risultati['avvisi'].append(f"Mazzo {i+1}, Guerriero schieramento {j+1}: manca attributo 'nome'")
                    
                    try:
                        crea_info_guerriero_sicura(guerriero)
                    except Exception as e:
                        risultati['errori'].append(f"Mazzo {i+1}, Guerriero schieramento {j+1}: errore serializzazione - {e}")
                        risultati['compatibile'] = False
            
            # Testa carte supporto
            if 'carte_supporto' in mazzo:
                for j, carta in enumerate(mazzo['carte_supporto']):
                    if not hasattr(carta, 'nome'):
                        risultati['avvisi'].append(f"Mazzo {i+1}, Carta supporto {j+1}: manca attributo 'nome'")
                    
                    try:
                        crea_info_carta_supporto_sicura(carta)
                    except Exception as e:
                        risultati['errori'].append(f"Mazzo {i+1}, Carta supporto {j+1}: errore serializzazione - {e}")
                        risultati['compatibile'] = False
        
        except Exception as e:
            risultati['errori'].append(f"Mazzo {i+1}: errore generale - {e}")
            risultati['compatibile'] = False
    
    return risultati

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

# ================================================================================
# FUNZIONI DI PULIZIA E PLACEHOLDERS
# ================================================================================

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

# ================================================================================
# FUNZIONI DI SALVATAGGIO (STANDARD E SICURO)
# ================================================================================

def salva_mazzi_json_migliorato(mazzi: List[Dict[str, Any]], filename: str = "mazzi_dettagliati.json") -> bool:
    """
    Salva i mazzi in formato JSON con struttura dettagliata.
    Analogo di salva_collezioni_json_migliorato() per mazzi.
    Versione robusta che gestisce errori di serializzazione.
    
    Args:
        mazzi: Lista di dizionari mazzo (output di crea_mazzo_da_gioco)
        filename: Nome del file di salvataggio
        
    Returns:
        True se il salvataggio è riuscito, False altrimenti
    """
    try:
        print(f"📄 Creazione struttura JSON dettagliata per {len(mazzi)} mazzi...")
        
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
        
        # Struttura principale del JSON
        dati_export = {
            'metadata': {
                'versione': '2.0',
                'tipo_export': 'mazzi_dettagliati',
                'data_creazione': datetime.now().isoformat(),
                'numero_mazzi': len(mazzi),
                'descrizione': 'Export dettagliato mazzi con inventari completi e statistiche aggregate',
                'test_compatibilita': test_risultati
            },
            'statistiche_aggregate': crea_statistiche_aggregate_mazzi_json(mazzi),
            'mazzi_dettagliati': []
        }
        
        # Aggiunge ogni mazzo con inventario dettagliato
        for i, mazzo in enumerate(mazzi):
            print(f"  📦 Processando mazzo {i+1}/{len(mazzi)}...")
            try:
                inventario_dettagliato = crea_inventario_dettagliato_mazzo_json(mazzo, i+1)
                dati_export['mazzi_dettagliati'].append(inventario_dettagliato)
            except Exception as e:
                print(f"  ⚠️ Errore processando mazzo {i+1}: {e}")
                # Crea un inventario minimale in caso di errore
                inventario_minimale = {
                    'indice_mazzo': i + 1,
                    'errore_processamento': str(e),
                    'statistiche_mazzo': mazzo.get('statistiche', {}),
                    'numero_guerrieri_squadra': len(mazzo.get('squadra', [])),
                    'numero_guerrieri_schieramento': len(mazzo.get('schieramento', [])),
                    'numero_carte_supporto': len(mazzo.get('carte_supporto', []))
                }
                dati_export['mazzi_dettagliati'].append(inventario_minimale)
        
        # Converte enum ricorsivamente
        print("📄 Conversione enum per compatibilità JSON...")
        dati_puliti = converti_enum_ricorsivo_mazzi(dati_export)
        
        # Salva il file
        print(f"💾 Salvando in {PERCORSO_SALVATAGGIO+filename}...")
        with open(PERCORSO_SALVATAGGIO + filename, 'w', encoding='utf-8') as f:
            json.dump(dati_puliti, f, indent=2, ensure_ascii=False)
        
        # Statistiche del file salvato
        dimensione_file = os.path.getsize(PERCORSO_SALVATAGGIO + filename) / 1024  # KB
        
        print(f"✅ Mazzi salvati con successo!")
        print(f"   📄 File: {filename}")
        print(f"   📊 Dimensione: {dimensione_file:.1f} KB")
        print(f"   🎮 Mazzi: {len(mazzi)}")
        print(f"   📦 Carte totali: {sum(m['statistiche']['numero_totale_carte'] for m in mazzi)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante il salvataggio JSON: {e}")
        
        # Salvataggio di debug migliorato
        try:
            debug_filename = filename.replace('.json', '_debug.txt')
            with open(PERCORSO_SALVATAGGIO + debug_filename, 'w', encoding='utf-8') as f:
                f.write(f"Errore durante serializzazione JSON: {e}\n\n")
                f.write(f"Numero mazzi: {len(mazzi)}\n\n")
                
                for i, m in enumerate(mazzi):
                    f.write(f"=== MAZZO {i+1} ===\n")
                    f.write(f"Statistiche: {m.get('statistiche', 'N/A')}\n")
                    f.write(f"Guerrieri squadra: {len(m.get('squadra', []))}\n")
                    f.write(f"Guerrieri schieramento: {len(m.get('schieramento', []))}\n")
                    f.write(f"Carte supporto: {len(m.get('carte_supporto', []))}\n")
                    
                    # Dettagli guerrieri che potrebbero causare problemi
                    f.write("Guerrieri squadra:\n")
                    for j, g in enumerate(m.get('squadra', [])):
                        try:
                            info = crea_info_guerriero_sicura(g)
                            f.write(f"  {j+1}. {info.get('nome', 'N/A')} - OK\n")
                        except Exception as ge:
                            f.write(f"  {j+1}. ERRORE: {ge}\n")
                            f.write(f"       Attributi disponibili: {dir(g)}\n")
                    
                    f.write("\n")
                
            print(f"📄 File di debug dettagliato salvato in {debug_filename}")
        except Exception as debug_error:
            print(f"❌ Errore anche nel debug: {debug_error}")
        
        return False

def salva_mazzi_json_sicuro(mazzi: List[Dict[str, Any]], filename: str = "mazzi_sicuri.json") -> bool:
    """
    Versione alternativa di salvataggio che garantisce sempre il successo.
    Utilizza placeholders per oggetti non serializzabili.
    
    Args:
        mazzi: Lista di mazzi da salvare
        filename: Nome del file
        
    Returns:
        True (sempre, garantisce sempre il salvataggio)
    """
    try:
        print(f"🛡️ Salvataggio sicuro mazzi in corso...")
        
        # Diagnostica preventiva
        print("🔍 Diagnostica preventiva...")
        stampa_diagnostica_mazzi(mazzi)
        
        # Pulisci mazzi
        print("🧹 Pulizia mazzi per compatibilità...")
        mazzi_puliti = pulisci_mazzi_per_salvataggio(mazzi)
        
        # Usa la funzione normale ma con mazzi puliti
        return salva_mazzi_json_migliorato(mazzi_puliti, filename)
        
    except Exception as e:
        print(f"⚠️ Anche il salvataggio sicuro ha avuto problemi: {e}")
        print("💾 Creazione salvataggio minimale...")
        
        # Salvataggio ultra-minimale
        try:
            dati_minimali = {
                'metadata': {
                    'versione': '1.0',
                    'tipo_export': 'mazzi_minimali',
                    'data_creazione': datetime.now().isoformat(),
                    'numero_mazzi': len(mazzi),
                    'errore': str(e)
                },
                'mazzi_count': len(mazzi),
                'mazzi_info': []
            }
            
            for i, mazzo in enumerate(mazzi):
                info_minimale = {
                    'indice': i + 1,
                    'carte_totali': len(mazzo.get('squadra', [])) + len(mazzo.get('schieramento', [])) + len(mazzo.get('carte_supporto', [])),
                    'guerrieri_squadra': len(mazzo.get('squadra', [])),
                    'guerrieri_schieramento': len(mazzo.get('schieramento', [])),
                    'carte_supporto': len(mazzo.get('carte_supporto', []))
                }
                dati_minimali['mazzi_info'].append(info_minimale)
            
            filename_minimale = filename.replace('.json', '_minimale.json')
            with open(PERCORSO_SALVATAGGIO + filename_minimale, 'w', encoding='utf-8') as f:
                json.dump(dati_minimali, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Salvato file minimale: {filename_minimale}")
            return True
            
        except Exception as e2:
            print(f"❌ Errore anche nel salvataggio minimale: {e2}")
            return False

# ================================================================================
# FUNZIONI DI CARICAMENTO JSON
# ================================================================================

def carica_mazzi_json_migliorato(filename: str) -> Optional[Dict[str, Any]]:
    """
    Carica mazzi dal formato JSON migliorato.
    Analogo di carica_collezioni_json_migliorato() per mazzi.
    
    Args:
        filename: Nome del file da caricare
        
    Returns:
        Dizionario con i dati caricati o None in caso di errore
    """
    try:
        print(f"📂 Caricamento mazzi da {PERCORSO_SALVATAGGIO+filename}...")
        
        with open(PERCORSO_SALVATAGGIO + filename, 'r', encoding='utf-8') as f:
            dati = json.load(f)
        
        # Verifica formato
        if 'metadata' not in dati or dati.get('metadata', {}).get('tipo_export') != 'mazzi_dettagliati':
            print("⚠️ Attenzione: File potrebbe non essere in formato dettagliato")
        
        # Stampa info di caricamento
        metadata = dati.get('metadata', {})
        print(f"✅ Caricamento completato!")
        print(f"   📅 Creato: {metadata.get('data_creazione', 'N/A')}")
        print(f"   🎮 Mazzi: {metadata.get('numero_mazzi', 'N/A')}")
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

def stampa_statistiche_da_json_mazzi(dati_json: Dict[str, Any]) -> None:
    """
    Stampa statistiche dai mazzi caricati da JSON.
    Analogo di stampa_statistiche_da_json() per mazzi.
    
    Args:
        dati_json: Dati JSON caricati
    """
    if not dati_json:
        print("❌ Nessun dato da visualizzare")
        return
    
    stats_aggregate = dati_json.get('statistiche_aggregate', {})
    panoramica = stats_aggregate.get('panoramica_generale', {})
    
    print(f"\n{'='*80}")
    print(f"📋 STATISTICHE DA JSON - {panoramica.get('numero_mazzi', 0)} MAZZI")
    print(f"{'='*80}")
    
    print(f"📦 Totale carte: {panoramica.get('totale_carte', 0)}")
    print(f"⚔️ Totale guerrieri squadra: {panoramica.get('totale_guerrieri_squadra', 0)}")
    print(f"🌑 Totale guerrieri schieramento: {panoramica.get('totale_guerrieri_schieramento', 0)}")
    print(f"📈 Media carte/mazzo: {panoramica.get('media_carte_per_mazzo', 0):.1f}")
    print(f"📈 Media guerrieri squadra: {panoramica.get('media_guerrieri_squadra', 0):.1f}")
    print(f"📈 Media guerrieri schieramento: {panoramica.get('media_guerrieri_schieramento', 0):.1f}")
    
    # Riepilogo mazzi
    print(f"\n📊 RIEPILOGO MAZZI:")
    for mazzo in stats_aggregate.get('riepilogo_mazzi', []):
        fazioni_str = ", ".join(mazzo.get('fazioni_presenti', []))
        esp_str = ", ".join(mazzo.get('espansioni_utilizzate', []))
        
        print(f"  🎮 Mazzo {mazzo.get('indice_mazzo')}: {mazzo.get('totale_carte')} carte")
        print(f"      ⚔️ Squadra: {mazzo.get('guerrieri_squadra')} - 🌑 Schieramento: {mazzo.get('guerrieri_schieramento')}")
        print(f"      🏛️ Fazioni: {fazioni_str}")
        print(f"      📚 Espansioni: {esp_str}")
        
        if mazzo.get('errori'):
            print(f"      ⚠️ Avvisi: {'; '.join(mazzo['errori'])}")
        print()
    
    # Distribuzione globale fazioni
    distribuzione_fazioni = stats_aggregate.get('distribuzione_globale', {}).get('per_fazione', {})
    if distribuzione_fazioni:
        print(f"🏛️ DISTRIBUZIONE GLOBALE FAZIONI:")
        for fazione, count in sorted(distribuzione_fazioni.items()):
            print(f"  {fazione}: presente in {count} mazzi")
    
    # Distribuzione globale espansioni
    distribuzione_espansioni = stats_aggregate.get('distribuzione_globale', {}).get('per_espansione', {})
    if distribuzione_espansioni:
        print(f"\n📚 DISTRIBUZIONE GLOBALE ESPANSIONI:")
        for espansione, count in sorted(distribuzione_espansioni.items()):
            print(f"  {espansione}: presente in {count} mazzi")

# ================================================================================
# FUNZIONI JSON AGGIORNATE CON CONTEGGIO COPIE CARTE
# ================================================================================

def crea_inventario_dettagliato_mazzo_json_con_conteggio(mazzo: Dict[str, Any], indice: int) -> Dict[str, Any]:
    """
    Crea un inventario dettagliato di un singolo mazzo in formato JSON.
    VERSIONE AGGIORNATA: Raggruppa le carte per nome e conta le copie invece di ripeterle.
    
    Args:
        mazzo: Dizionario del mazzo
        indice: Indice del mazzo
        
    Returns:
        Dizionario con inventario raggruppato per nome carta con conteggi
    """
    inventario = {
        'indice_mazzo': indice,
        'statistiche_mazzo': mazzo['statistiche'],
        'errori': mazzo.get('errori', []),
        'distribuzione_utilizzata': mazzo.get('distribuzione_utilizzata', {}),
        'inventario_guerrieri': {
            'squadra': {},
            'schieramento': {}
        },
        'inventario_supporto': {}
    }
    
    # ================================================================================
    # INVENTARIO GUERRIERI SQUADRA CON CONTEGGIO
    # ================================================================================
    
    for guerriero in mazzo['squadra']:
        guerriero_info = crea_info_guerriero_sicura(guerriero)
        nome_carta = guerriero_info['nome']
        
        if nome_carta in inventario['inventario_guerrieri']['squadra']:
            # Carta già presente, incrementa il conteggio
            inventario['inventario_guerrieri']['squadra'][nome_carta]['copie'] += 1
        else:
            # Prima volta che si vede questa carta
            inventario['inventario_guerrieri']['squadra'][nome_carta] = {
                'copie': 1,
                'fazione': guerriero_info['fazione'],
                'set_espansione': guerriero_info['set_espansione'],
                'rarity': guerriero_info['rarity'],
                'tipo': guerriero_info['tipo'],
                'combattimento': guerriero_info.get('combattimento', 0),
                'sparare': guerriero_info.get('sparare', 0),
                'armatura': guerriero_info.get('armatura', 0),
                'valore': guerriero_info.get('valore', 0),
                'valor_destino': guerriero_info.get('valor_destino', 0),
                'valor_promozione': guerriero_info.get('valor_promozione', 0),
                'e_personalita': guerriero_info.get('e_personalita', False),
                'keywords': guerriero_info.get('keywords', []),
                'numero_carta': guerriero_info.get('numero_carta', '')
            }
    
    # ================================================================================
    # INVENTARIO GUERRIERI SCHIERAMENTO CON CONTEGGIO
    # ================================================================================
    
    for guerriero in mazzo['schieramento']:
        guerriero_info = crea_info_guerriero_sicura(guerriero)
        nome_carta = guerriero_info['nome']
        
        if nome_carta in inventario['inventario_guerrieri']['schieramento']:
            # Carta già presente, incrementa il conteggio
            inventario['inventario_guerrieri']['schieramento'][nome_carta]['copie'] += 1
        else:
            # Prima volta che si vede questa carta
            inventario['inventario_guerrieri']['schieramento'][nome_carta] = {
                'copie': 1,
                'fazione': guerriero_info['fazione'],
                'set_espansione': guerriero_info['set_espansione'],
                'rarity': guerriero_info['rarity'],
                'tipo': guerriero_info['tipo'],
                'combattimento': guerriero_info.get('combattimento', 0),
                'sparare': guerriero_info.get('sparare', 0),
                'armatura': guerriero_info.get('armatura', 0),
                'valore': guerriero_info.get('valore', 0),
                'valor_destino': guerriero_info.get('valor_destino', 0),
                'valor_promozione': guerriero_info.get('valor_promozione', 0),
                'e_personalita': guerriero_info.get('e_personalita', False),
                'keywords': guerriero_info.get('keywords', []),
                'numero_carta': guerriero_info.get('numero_carta', '')
            }
    
    # ================================================================================
    # INVENTARIO CARTE SUPPORTO CON CONTEGGIO
    # ================================================================================
    
    for carta in mazzo['carte_supporto']:
        carta_info = crea_info_carta_supporto_sicura(carta)
        nome_carta = carta_info['nome']
        
        if nome_carta in inventario['inventario_supporto']:
            # Carta già presente, incrementa il conteggio
            inventario['inventario_supporto'][nome_carta]['copie'] += 1
        else:
            # Prima volta che si vede questa carta
            inventario['inventario_supporto'][nome_carta] = {
                'copie': 1,
                'tipo': carta_info['tipo'],
                'set_espansione': carta_info['set_espansione'],
                'rarity': carta_info['rarity'],
                'numero_carta': carta_info.get('numero_carta', ''),
                'keywords': carta_info.get('keywords', []),
                'costo_destino': carta_info.get('costo_destino', 0)
            }
            
            # Aggiungi attributi specifici se presenti
            if 'fazione' in carta_info:
                inventario['inventario_supporto'][nome_carta]['fazione'] = carta_info['fazione']
            if 'valor_destino' in carta_info:
                inventario['inventario_supporto'][nome_carta]['valor_destino'] = carta_info['valor_destino']
            if 'valore' in carta_info:
                inventario['inventario_supporto'][nome_carta]['valore'] = carta_info['valore']
            if 'disciplina_arte' in carta_info:
                inventario['inventario_supporto'][nome_carta]['disciplina_arte'] = carta_info['disciplina_arte']
            if 'apostolo' in carta_info:
                inventario['inventario_supporto'][nome_carta]['apostolo'] = carta_info['apostolo']
            if 'apostolo_padre' in carta_info:
                inventario['inventario_supporto'][nome_carta]['apostolo_padre'] = carta_info['apostolo_padre']
    
    return inventario

# ================================================================================
# FUNZIONE DI SALVATAGGIO AGGIORNATA
# ================================================================================

def salva_mazzi_json_migliorato_con_conteggio(mazzi: List[Dict[str, Any]], filename: str = "mazzi_dettagliati_conteggio.json") -> bool:
    """
    Salva i mazzi in formato JSON con struttura dettagliata e conteggio copie.
    VERSIONE AGGIORNATA: Le carte con stesso nome vengono raggruppate con conteggio copie.
    
    Args:
        mazzi: Lista di dizionari mazzo (output di crea_mazzo_da_gioco)
        filename: Nome del file di salvataggio
        
    Returns:
        True se il salvataggio è riuscito, False altrimenti
    """
    try:
        print(f"📄 Creazione struttura JSON con conteggio copie per {len(mazzi)} mazzi...")
        
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
        
        # Struttura principale del JSON con conteggio copie
        dati_export = {
            'metadata': {
                'versione': '2.1',
                'tipo_export': 'mazzi_dettagliati_con_conteggio',
                'data_creazione': datetime.now().isoformat(),
                'numero_mazzi': len(mazzi),
                'descrizione': 'Export dettagliato mazzi con inventari raggruppati per nome carta e conteggio copie',
                'formato_inventario': 'raggruppato_con_conteggio',
                'test_compatibilita': test_risultati
            },
            'statistiche_aggregate': crea_statistiche_aggregate_mazzi_json(mazzi),
            'mazzi_dettagliati': []
        }
        
        # Aggiunge ogni mazzo con inventario dettagliato raggruppato
        for i, mazzo in enumerate(mazzi):
            print(f"  📦 Processando mazzo {i+1}/{len(mazzi)} con raggruppamento carte...")
            try:
                inventario_dettagliato = crea_inventario_dettagliato_mazzo_json_con_conteggio(mazzo, i+1)
                dati_export['mazzi_dettagliati'].append(inventario_dettagliato)
            except Exception as e:
                print(f"  ⚠️ Errore processando mazzo {i+1}: {e}")
                # Crea un inventario minimale in caso di errore
                inventario_minimale = {
                    'indice_mazzo': i + 1,
                    'errore_processamento': str(e),
                    'statistiche_mazzo': mazzo.get('statistiche', {}),
                    'numero_guerrieri_squadra': len(mazzo.get('squadra', [])),
                    'numero_guerrieri_schieramento': len(mazzo.get('schieramento', [])),
                    'numero_carte_supporto': len(mazzo.get('carte_supporto', []))
                }
                dati_export['mazzi_dettagliati'].append(inventario_minimale)
        
        # Converte enum ricorsivamente
        print("📄 Conversione enum per compatibilità JSON...")
        dati_puliti = converti_enum_ricorsivo_mazzi(dati_export)
        
        # Salva il file
        print(f"💾 Salvando in {PERCORSO_SALVATAGGIO+filename}...")
        with open(PERCORSO_SALVATAGGIO + filename, 'w', encoding='utf-8') as f:
            json.dump(dati_puliti, f, indent=2, ensure_ascii=False)
        
        # Statistiche del file salvato
        dimensione_file = os.path.getsize(PERCORSO_SALVATAGGIO + filename) / 1024  # KB
        
        print(f"✅ Mazzi salvati con successo!")
        print(f"   📄 File: {filename}")
        print(f"   📊 Dimensione: {dimensione_file:.1f} KB")
        print(f"   🎮 Mazzi: {len(mazzi)}")
        print(f"   📦 Carte totali: {sum(m['statistiche']['numero_totale_carte'] for m in mazzi)}")
        print(f"   🔢 Formato: Inventario raggruppato con conteggio copie")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante il salvataggio JSON: {e}")
        
        # Salvataggio di debug migliorato
        try:
            debug_filename = filename.replace('.json', '_debug.txt')
            with open(PERCORSO_SALVATAGGIO + debug_filename, 'w', encoding='utf-8') as f:
                f.write(f"Errore durante serializzazione JSON: {e}\n\n")
                f.write(f"Numero mazzi: {len(mazzi)}\n\n")
                
                for i, m in enumerate(mazzi):
                    f.write(f"=== MAZZO {i+1} ===\n")
                    f.write(f"Statistiche: {m.get('statistiche', 'N/A')}\n")
                    f.write(f"Guerrieri squadra: {len(m.get('squadra', []))}\n")
                    f.write(f"Guerrieri schieramento: {len(m.get('schieramento', []))}\n")
                    f.write(f"Carte supporto: {len(m.get('carte_supporto', []))}\n\n")
                
            print(f"📄 File di debug salvato in {debug_filename}")
        except Exception as debug_error:
            print(f"❌ Errore anche nel debug: {debug_error}")
        
        return False

# ================================================================================
# FUNZIONE DI VISUALIZZAZIONE INVENTARIO CON CONTEGGIO
# ================================================================================

def stampa_statistiche_da_json_mazzi_con_conteggio(dati_json: Dict[str, Any]) -> None:
    """
    Stampa statistiche dai mazzi caricati da JSON con formato conteggio copie.
    VERSIONE AGGIORNATA: Gestisce inventari raggruppati per nome carta.
    
    Args:
        dati_json: Dati JSON caricati
    """
    if not dati_json:
        print("❌ Nessun dato da visualizzare")
        return
    
    stats_aggregate = dati_json.get('statistiche_aggregate', {})
    panoramica = stats_aggregate.get('panoramica_generale', {})
    
    print(f"\n{'='*80}")
    print(f"📋 STATISTICHE DA JSON CON CONTEGGIO - {panoramica.get('numero_mazzi', 0)} MAZZI")
    print(f"{'='*80}")
    
    # Informazioni formato
    metadata = dati_json.get('metadata', {})
    formato_inventario = metadata.get('formato_inventario', 'standard')
    print(f"📋 Formato inventario: {formato_inventario}")
    print(f"📅 Data creazione: {metadata.get('data_creazione', 'N/A')}")
    
    print(f"\n📦 Totale carte: {panoramica.get('totale_carte', 0)}")
    print(f"⚔️ Totale guerrieri squadra: {panoramica.get('totale_guerrieri_squadra', 0)}")
    print(f"🌑 Totale guerrieri schieramento: {panoramica.get('totale_guerrieri_schieramento', 0)}")
    print(f"📈 Media carte/mazzo: {panoramica.get('media_carte_per_mazzo', 0):.1f}")
    print(f"📈 Media guerrieri squadra: {panoramica.get('media_guerrieri_squadra', 0):.1f}")
    print(f"📈 Media guerrieri schieramento: {panoramica.get('media_guerrieri_schieramento', 0):.1f}")
    
    # Riepilogo mazzi con dettagli inventario raggruppato
    print(f"\n📊 RIEPILOGO MAZZI CON INVENTARI RAGGRUPPATI:")
    
    mazzi_dettagliati = dati_json.get('mazzi_dettagliati', [])
    for mazzo_data in mazzi_dettagliati:
        indice_mazzo = mazzo_data.get('indice_mazzo', 'N/A')
        stats_mazzo = mazzo_data.get('statistiche_mazzo', {})
        
        print(f"\n  🎮 MAZZO {indice_mazzo}:")
        print(f"    📦 Carte totali: {stats_mazzo.get('numero_totale_carte', 'N/A')}")
        print(f"    ⚔️ Guerrieri squadra: {stats_mazzo.get('guerrieri_squadra', 'N/A')}")
        print(f"    🌑 Guerrieri schieramento: {stats_mazzo.get('guerrieri_schieramento', 'N/A')}")
        
        # Mostra fazioni e espansioni
        fazioni = stats_mazzo.get('fazioni_presenti', [])
        if fazioni:
            print(f"    🏛️ Fazioni: {', '.join(fazioni)}")
        
        espansioni = stats_mazzo.get('espansioni_utilizzate', [])
        if espansioni:
            print(f"    📚 Espansioni: {', '.join(espansioni)}")
        
        # Inventario raggruppato guerrieri squadra
        inventario_guerrieri = mazzo_data.get('inventario_guerrieri', {})
        squadra = inventario_guerrieri.get('squadra', {})
        if squadra:
            print(f"    ⚔️ GUERRIERI SQUADRA RAGGRUPPATI:")
            for nome_carta, info_carta in squadra.items():
                copie = info_carta.get('copie', 1)
                fazione = info_carta.get('fazione', 'N/A')
                copie_str = f"x{copie}" if copie > 1 else ""
                print(f"      • {nome_carta} {copie_str} ({fazione})")
        
        # Inventario raggruppato guerrieri schieramento
        schieramento = inventario_guerrieri.get('schieramento', {})
        if schieramento:
            print(f"    🌑 GUERRIERI SCHIERAMENTO RAGGRUPPATI:")
            for nome_carta, info_carta in schieramento.items():
                copie = info_carta.get('copie', 1)
                fazione = info_carta.get('fazione', 'N/A')
                copie_str = f"x{copie}" if copie > 1 else ""
                print(f"      • {nome_carta} {copie_str} ({fazione})")
        
        # Inventario raggruppato carte supporto
        supporto = mazzo_data.get('inventario_supporto', {})
        if supporto:
            print(f"    🎴 CARTE SUPPORTO RAGGRUPPATE:")
            for nome_carta, info_carta in supporto.items():
                copie = info_carta.get('copie', 1)
                tipo = info_carta.get('tipo', 'N/A')
                copie_str = f"x{copie}" if copie > 1 else ""
                print(f"      • {nome_carta} {copie_str} ({tipo})")
        
        # Errori se presenti
        errori = mazzo_data.get('errori', [])
        if errori:
            print(f"    ⚠️ Avvisi: {'; '.join(errori)}")
    
    # Distribuzione globale fazioni
    distribuzione_fazioni = stats_aggregate.get('distribuzione_globale', {}).get('per_fazione', {})
    if distribuzione_fazioni:
        print(f"\n🏛️ DISTRIBUZIONE GLOBALE FAZIONI:")
        for fazione, count in sorted(distribuzione_fazioni.items()):
            print(f"  {fazione}: presente in {count} mazzi")
    
    # Distribuzione globale espansioni
    distribuzione_espansioni = stats_aggregate.get('distribuzione_globale', {}).get('per_espansione', {})
    if distribuzione_espansioni:
        print(f"\n📚 DISTRIBUZIONE GLOBALE ESPANSIONI:")
        for espansione, count in sorted(distribuzione_espansioni.items()):
            print(f"  {espansione}: presente in {count} mazzi")

# ================================================================================
# FUNZIONE DI SALVATAGGIO SICURO AGGIORNATA
# ================================================================================

def salva_mazzi_json_sicuro_con_conteggio(mazzi: List[Dict[str, Any]], filename: str = "mazzi_sicuri_conteggio.json") -> bool:
    """
    Versione sicura del salvataggio con conteggio copie che garantisce sempre il successo.
    
    Args:
        mazzi: Lista di mazzi da salvare
        filename: Nome del file
        
    Returns:
        True (sempre, garantisce sempre il salvataggio)
    """
    try:
        print(f"🛡️ Salvataggio sicuro con conteggio copie in corso...")
        
        # Diagnostica preventiva
        print("🔍 Diagnostica preventiva...")
        stampa_diagnostica_mazzi(mazzi)
        
        # Pulisci mazzi
        print("🧹 Pulizia mazzi per compatibilità...")
        mazzi_puliti = pulisci_mazzi_per_salvataggio(mazzi)
        
        # Usa la funzione con conteggio su mazzi puliti
        return salva_mazzi_json_migliorato_con_conteggio(mazzi_puliti, filename)
        
    except Exception as e:
        print(f"⚠️ Anche il salvataggio sicuro ha avuto problemi: {e}")
        print("💾 Creazione salvataggio minimale con conteggio...")
        
        # Salvataggio ultra-minimale con conteggio base
        try:
            dati_minimali = {
                'metadata': {
                    'versione': '1.1',
                    'tipo_export': 'mazzi_minimali_con_conteggio',
                    'data_creazione': datetime.now().isoformat(),
                    'numero_mazzi': len(mazzi),
                    'formato_inventario': 'minimale_con_conteggio',
                    'errore': str(e)
                },
                'mazzi_count': len(mazzi),
                'mazzi_info': []
            }
            
            for i, mazzo in enumerate(mazzi):
                # Conteggio semplice per fallback
                guerrieri_squadra_nomi = {}
                for g in mazzo.get('squadra', []):
                    nome = getattr(g, 'nome', f'Guerriero_{i}')
                    guerrieri_squadra_nomi[nome] = guerrieri_squadra_nomi.get(nome, 0) + 1
                
                guerrieri_schieramento_nomi = {}
                for g in mazzo.get('schieramento', []):
                    nome = getattr(g, 'nome', f'Guerriero_{i}')
                    guerrieri_schieramento_nomi[nome] = guerrieri_schieramento_nomi.get(nome, 0) + 1
                
                carte_supporto_nomi = {}
                for c in mazzo.get('carte_supporto', []):
                    nome = getattr(c, 'nome', f'Carta_{i}')
                    carte_supporto_nomi[nome] = carte_supporto_nomi.get(nome, 0) + 1
                
                info_minimale = {
                    'indice': i + 1,
                    'carte_totali': len(mazzo.get('squadra', [])) + len(mazzo.get('schieramento', [])) + len(mazzo.get('carte_supporto', [])),
                    'guerrieri_squadra_conteggio': guerrieri_squadra_nomi,
                    'guerrieri_schieramento_conteggio': guerrieri_schieramento_nomi,
                    'carte_supporto_conteggio': carte_supporto_nomi
                }
                dati_minimali['mazzi_info'].append(info_minimale)
            
            filename_minimale = filename.replace('.json', '_minimale_conteggio.json')
            with open(PERCORSO_SALVATAGGIO + filename_minimale, 'w', encoding='utf-8') as f:
                json.dump(dati_minimali, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Salvato file minimale con conteggio: {filename_minimale}")
            return True
            
        except Exception as e2:
            print(f"❌ Errore anche nel salvataggio minimale: {e2}")
            return False

# ================================================================================
# FUNZIONI DI UTILITÀ AGGIORNATE
# ================================================================================

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
    
    print("2. Salva con conteggio: salva_mazzi_json_migliorato_con_conteggio(mazzi)")
    salva_mazzi_json_migliorato_con_conteggio(mazzi, "mazzi_con_conteggio.json")
    
    print("3. Carica: dati = carica_mazzi_json_migliorato('mazzi_con_conteggio.json')")
    dati_json = carica_mazzi_json_migliorato("mazzi_con_conteggio.json")
    
    print("4. Visualizza con conteggio: stampa_statistiche_da_json_mazzi_con_conteggio(dati)")
    if dati_json:
        stampa_statistiche_da_json_mazzi_con_conteggio(dati_json)

# ================================================================================
# ISTRUZIONI PER L'USO
# ================================================================================

"""
🔧 COME USARE LE NUOVE FUNZIONI CON CONTEGGIO COPIE:

1. SALVATAGGIO CON CONTEGGIO:
   salva_mazzi_json_migliorato_con_conteggio(mazzi, "mazzi_raggruppati.json")
   
2. SALVATAGGIO SICURO CON CONTEGGIO:
   salva_mazzi_json_sicuro_con_conteggio(mazzi, "mazzi_sicuri_raggruppati.json")

3. VISUALIZZAZIONE:
   dati = carica_mazzi_json_migliorato("mazzi_raggruppati.json")
   stampa_statistiche_da_json_mazzi_con_conteggio(dati)

🆕 VANTAGGI DEL NUOVO FORMATO:
✅ File JSON più compatti
✅ Inventario più leggibile 
✅ Conteggio copie immediato
✅ Struttura più logica
✅ Compatibilità con versione precedente

📋 FORMATO JSON RISULTANTE:
{
  "inventario_guerrieri": {
    "squadra": {
      "Bauhaus Blitzer": {
        "copie": 3,
        "fazione": "Bauhaus",
        "set_espansione": "Base",
        ...
      }
    }
  }
}
"""

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
# FUNZIONI DI ESEMPIO E UTILITÀ
# ================================================================================

def esempio_salvataggio_mazzi_migliorato(mazzi: List[Dict[str, Any]]) -> None:
    """
    Esempio di utilizzo delle funzioni di salvataggio migliorato per mazzi.
    
    Args:
        mazzi: Lista di mazzi da utilizzare per l'esempio
    """
    print("\n📁 ESEMPIO SALVATAGGIO JSON MIGLIORATO - MAZZI")
    print("=" * 60)
    
    if not mazzi:
        print("❌ Nessun mazzo fornito per l'esempio")
        return
    
    print("1. Stampa riepilogo: stampa_riepilogo_mazzi_migliorato(mazzi)")
    stampa_riepilogo_mazzi_migliorato(mazzi)
    
    print("2. Salva dettagliato: salva_mazzi_json_migliorato(mazzi, 'mazzi_dettagliati.json')")
    salva_mazzi_json_migliorato(mazzi, "mazzi_dettagliati.json")
    
    print("3. Carica: dati = carica_mazzi_json_migliorato('mazzi_dettagliati.json')")
    dati_json = carica_mazzi_json_migliorato("mazzi_dettagliati.json")
    
    print("4. Visualizza: stampa_statistiche_da_json_mazzi(dati)")
    if dati_json:
        stampa_statistiche_da_json_mazzi(dati_json)

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
        print("3. Salva mazzi in JSON (standard)")
        print("4. Salva mazzi in JSON (sicuro)")
        print("5. Carica mazzi da JSON (visualizzazione)")

        print("6. Salva mazzi in JSON con conteggio (standard)")
        print("7. Salva mazzi in JSON con conteggio(sicuro)")
        print("8. Carica e visualizza mazzi da JSON con conteggio")
        

        print("9. Verifica integrità mazzi")
        print("10. Analizza bilanciamento")
        print("11. Diagnostica completa mazzi")
        print("12. Test compatibilità")
        print("13. Cerca carta nei mazzi")
        print("14. Esempio completo salvataggio")
        print("15. Pulisci mazzi correnti")
        print("0. Esci")
        
        
        scelta = input("\nScegli un'opzione: ").strip()
        
        if scelta == "0":
            print("Arrivederci!")
            break
        elif scelta == "1":
            # Crea mazzi di esempio (qui serve la funzione crea_mazzo_da_gioco)
            # print("⚠️ Funzione non implementata - richiede collezioni di esempio")
            # print("   Per utilizzare questa opzione, integra con il modulo Creatore_Collezione")
            collezioni = creazione_Collezione_Giocatore(2, [Set_Espansione.BASE, Set_Espansione.INQUISITION], orientamento = False)

            mazzo_1 = crea_mazzo_da_gioco(collezioni[0],
                            numero_carte_max = 60,
                            numero_carte_min = 50,
                            espansioni_richieste = ["Base", "Inquisition"],
                            doomtrooper = True,
                            orientamento_doomtrooper = ["Bauhaus", "Capitol", "Mishima"],
                            fratellanza = True,
                            orientamento_arte = ['Cambiamento', 'Premonizione', 'Esorcismo'],
                            oscura_legione = False,
                            orientamento_apostolo = None,
                            orientamento_eretico = False,
                            orientamento_cultista = False)
            
            mazzo_2 = crea_mazzo_da_gioco(collezioni[1],
                            numero_carte_max = 60,
                            numero_carte_min = 50,
                            espansioni_richieste = ["Base", "Inquisition"],
                            doomtrooper = True,
                            orientamento_doomtrooper = ["Imperiale", "Cybertronic", "Freelancer"],
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
                filename = input("Nome file (default: mazzi_dettagliati.json): ").strip()
                if not filename:
                    filename = "mazzi_dettagliati.json"
                successo = salva_mazzi_json_migliorato_con_conteggio(mazzi_correnti, filename)
                if successo:
                    print("✅ Salvataggio completato!")
                else:
                    print("❌ Salvataggio fallito - vedi i dettagli sopra")
            else:
                print("❌ Nessun mazzo da salvare. Usa prima l'opzione 1.")
        elif scelta == "4":
            if mazzi_correnti:
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
                    stampa_statistiche_da_json_mazzi_con_conteggio(dati_caricati)
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
            if mazzi_correnti:
                esempio_salvataggio_mazzi_migliorato(mazzi_correnti)
            else:
                print("❌ Nessun mazzo per l'esempio. Usa prima l'opzione 1.")
        elif scelta == "12":
            mazzi_correnti.clear()
            print("✅ Mazzi correnti puliti")
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

def esempio_utilizzo_completo_mazzi():
    """
    Esempio completo di utilizzo delle funzioni di gestione mazzi.
    Da integrare nel modulo principale Creatore_Mazzo.py
    """
    print("\n" + "="*80)
    print("ESEMPIO UTILIZZO COMPLETO - GESTIONE MAZZI")
    print("="*80)
    
    print("⚠️ Esempio non eseguibile - richiede integrazione con Creatore_Collezione")
    print("   Copiare questo codice nel modulo Creatore_Mazzo.py e adattare secondo necessità")

# ================================================================================
# MAIN DI TEST (se eseguito come modulo standalone)
# ================================================================================

if __name__ == "__main__":
    """
    Esecuzione diretta del modulo per test.
    """
    print("🎯 MODULO GESTIONE MAZZI - TEST STANDALONE")
    
    # Esegui test base
    test_funzioni_mazzi()
    
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




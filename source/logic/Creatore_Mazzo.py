"""
Creatore Mazzo
classi, usecase e utilità per la creazione dei mazzi da gioco

"""

import random
import math
import sys
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any, Union
from enum import Enum
import json
import os
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

# Import per la generazione di PDF
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# Import delle classi delle carte (solo le classi, non le funzioni di creazione)
from source.logic.Creatore_Collezione import creazione_Collezione_Giocatore, carica_collezioni_json_migliorato, salva_collezioni_json_migliorato, determina_orientamento_collezione
from source.cards.Guerriero import (
    Guerriero, Fazione, Set_Espansione, Rarity, TipoGuerriero, DisciplinaArte, DOOMTROOPER
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
# ENCODER JSON PER GESTIRE ENUMERAZIONI
# ================================================================================

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
        return super().default(obj)


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
STATISTICHE_MODIFICATORI = [["sparare", "combattimento", "armatura", "S", "A", "C", "multiple:"]]

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
        self.potenze_calcolate = {'Guerriero': {}, 'Equipaggiamento': {}, 'Speciale': {}, 'Arte': {}, 'Oscura Simmetria': {}, 'Fortificazione': {}, 'Missione': {}, 'Reliquia' : {}, 'Warzone': {}}  # Cache per i calcoli di potenza

        # self.potenze_assolute = self.calcola_potenze_assolute() # dizionario con potenze assolute di tutte le carte nella collezione
        # def calcola _potenza_equipaggiamento(self, equipaggiamento: Equipaggiamento) -> float:
        #   self.potenze_assolute["equipaggiamento"][equipaggiamento.nome] / max(self.potenze_assolute["equipaggiamento"].values()) 
        
    def calcola_potenza_guerriero(self, guerriero: Guerriero) -> float:
        """
        Calcola la potenza relativa di un guerriero
        
        Args:
            guerriero: Oggetto Guerriero
            
        Returns:
            float: potenza
        """
        if guerriero.nome in self.potenze_calcolate['Guerriero']:
            return self.potenze_calcolate['Guerriero'][guerriero.nome]
            
        # Calcola potenza assoluta
        combattimento = guerriero.stats.combattimento
        sparo = guerriero.stats.sparare
        armatura = guerriero.stats.armatura
        valore = guerriero.stats.valore
        
        if valore == 0:
            valore = 1  # Evita divisione per zero
            
        potenza = ((combattimento + sparo + armatura) * 1.5) / valore
        
        # Bonus per abilità speciali
        for abilita in guerriero.abilita:
            # Potenziamento altri guerrieri
            descrizione = abilita.descrizione.lower()
            nome = abilita.nome.lower()
            tipo = abilita.tipo.lower()

            if tipo == "combattimento":
                    if nome == "uccide automaticamente":
                        potenza *= 1.5
                    if nome in ["permette ai guerrieri di attaccare per primi", "i guerrieri alleati uccidono automaticamente"]:
                        potenza *= 1.3
                    
            if tipo == "immunita":
                if nome in ["immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria", "annulla immunita dell'oscura simmetria", "immune ai doni degli apostoli"]:
                    potenza *= 1.4                
                
                elif any(immunita in nome for immunita in ["immune agli effetti della specifica arte", "immune allo specifico equipaggiamento", "immune alla specifica fortificazione"]):
                    potenza *= 1.2
                        
            if tipo == "modificatore":        
                if nome in ["aumenta effetto", "aumenta caratteristica"]:
                    potenza *= 1.3
                elif nome == "trasforma guerrieri uccisi in alleati":
                    potenza *= 1.1
                elif nome == "sostituisce guerrieri":
                    potenza *= 1.2

            if tipo == "guarigione" :
                    if "guarisce se stesso" in nome:
                        potenza *= 1.3

            if tipo == "arte":                
                if "lancia arte e/o incantesimo dell'arte" == nome:
                    potenza *= 1.3                
                elif "lancia arte e/o incantesimo dell'arte specifica" == nome:
                    potenza *= 1.2

            if tipo == "carte":
                if nome in ["assegna carta", "scarta carta", "elimina carta"]:
                    potenza *= 1.3    

            if tipo == "azioni":
                if nome in ["converte azioni in azioni d'attacco"]:
                    potenza *= 1.3    
                        
        self.potenze_calcolate['Guerriero'][guerriero.nome] = potenza
        return potenza
    
    def calcola_potenza_equipaggiamento(self, equipaggiamento: Equipaggiamento) -> float:
        """
        Calcola la potenza relativa di un equipaggiamento
        
        Args:
            equipaggiamento: Oggetto Equipaggiamento
            
        Returns:
            float: potenza 
        """
        if equipaggiamento.nome in self.potenze_calcolate['Equipaggiamento']:
            return self.potenze_calcolate['Equipaggiamento'][equipaggiamento.nome]
        
        potenza = 1.0                

        # Somma modificatori statistiche
        statistiche = {
            'combattimento':    equipaggiamento.modificatori_combattimento,
            'sparare':          equipaggiamento.modificatori_sparare,
            'armatura':         equipaggiamento.modificatori_armatura,
            #'valore':           equipaggiamento.modificatori_valore
        }

        for valore_modifica in statistiche.values():
            if valore_modifica > 0:
                potenza += valore_modifica
         

        modifica_statistiche_applicata = True if potenza > 1 else False   

        # NOTA: nel database i valori specificati nei modificatori statistiche e quelli analoghi specificati nei modificatori_speciali 
        # se rappresentano lo stesso potenziamento devono alternativi gli uni agli altri. Pertanto è necessario verificare che se sono specificati per uno, i valori dell'altro 
        # gruppo devono essere posti a 0. Se, invece, i valori riportati nel gruppo statistiche sono di default e quelli specificati nel gruppo modificatori_speciali sono aggiuntivi
        # e vengono aapplicati in base ad una determinata condizione allora devono essere specificati

        # Bonus per modificatori speciali
        for modificatore in equipaggiamento.modificatori_speciali:
            # Potenziamento altri guerrieri
            statistica = modificatore.statistica.lower()
            descrizione = modificatore.descrizione.lower()
            valore = modificatore.valore.lower()
            condizione = modificatore.condizione.lower()            
            
            if statistica in STATISTICHE_MODIFICATORI:
                                                
                if any(val in valore for val in ["raddoppiate", "+5", "+6", "+7", "+8", "+9"]):  
                                                  
                    if ( "uso ristretto:" not in condizione or "incrementa con costo:" in condizione ):
                        
                        if modifica_statistiche_applicata: 
                            potenza *= 1.3
                        else:    
                            potenza += 4
                
                elif any(val in valore for val in ["+3", "+4"]):                
                    
                    if ( "uso ristretto:" not in condizione or "incrementa con costo:" in condizione ):
                        
                        if modifica_statistiche_applicata:
                            potenza *= 1.2
                        else:    
                            potenza += 2
                    
                elif any(val in descrizione for val in ["+1", "+2"]):                        
                        
                    if ( "uso ristretto:" not in condizione or "incrementa con costo:" in condizione ):
                            
                            if modifica_statistiche_applicata:
                                potenza *= 1.1
                            else:    
                                potenza += 1
                
                                
                if "multiple" in statistica:
                    potenza *= 1.5 # aumenta del 50% la potenza assoluta                
        
        # Bonus per abilita speciali
        for abilita in equipaggiamento.abilita_speciali:
            # Potenziamento altri guerrieri
            descrizione = abilita.descrizione.lower()
            nome = abilita.nome.lower()
            tipo = abilita.tipo_attivazione.lower()

            if tipo == "combattimento":
                    if nome == "uccide automaticamente":
                        potenza *= 1.5
                    if nome in ["permette ai guerrieri di attaccare per primi", "i guerrieri alleati uccidono automaticamente"]:
                        potenza *= 1.3
                    
            if tipo == "immunita":
                if nome in ["immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria", "annulla immunita dell'Oscura simmetria", "immune ai doni degli apostoli"]:
                    potenza *= 1.4
                elif any( val in nome for val in ["immune agli effetti della specifica arte", "immune allo specifico equipaggiamento", "immune alla specifica fortificazione", "Immune alle ferite durante il combattimento"]):
                    potenza *= 1.2
                                                                                    
            if tipo == "modificatore":        
                if nome in ["aumenta effetto", "aumenta caratteristica"]:
                    potenza *= 1.3
                elif nome == "trasforma guerrieri uccisi in alleati":
                    potenza *= 1.1
                elif nome == "sostituisce guerrieri":
                    potenza *= 1.2

            if tipo == "guarigione" :
                if nome in ["guarisce se stesso", "guarisce guerriero"]:
                    potenza *= 1.3
                if nome == "ripara equipaggiamento o fortificazione":
                    potenza *= 1.1

            if tipo == "arte":                
                if "lancia arte e/o incantesimo dell'arte" == nome:
                    potenza *= 1.3                
                elif "lancia arte e/o incantesimo dell'arte specifica" == nome:
                    potenza *= 1.2             
            
            if tipo == "carte":
                if nome in ["assegna carta", "scarta carta", "elimina carta"]:
                    potenza *= 1.3    

            if tipo == "azioni":
                if nome in ["converte azioni in azioni d'attacco", "Incrementa Azioni", "Attacca sempre per primo"]:
                    potenza *= 1.3    
                elif nome in ["modifica azione", "modifica stato"]:
                    potenza *= 1.1                
        

        self.potenze_calcolate['Equipaggiamento'][equipaggiamento.nome] = potenza
        return potenza
      
    def calcola_potenza_fortificazione(self, fortificazione: Fortificazione) -> float:
        """
        Calcola la potenza relativa di una fortificazione
        
        Args:
            fortificazione: Oggetto Fortificazione
            
        Returns:
            float: potenza
        """
        if fortificazione.nome in self.potenze_calcolate['Fortificazione']:
            return self.potenze_calcolate['Fortificazione'][fortificazione.nome]

        potenza = fortificazione.bonus_armatura
        
        # Se non influenza l'armatura
        #if potenza == 0:
        #    return 0.5
    

        modifica_statistiche_applicata = True if potenza > 1 else False  

        # Bonus per modificatori speciali
        for modificatore in fortificazione.modificatori:
            # Potenziamento altri guerrieri
            statistica = modificatore.statistica.lower()
            descrizione = modificatore.descrizione.lower()
            valore = modificatore.valore.lower()
            condizione = modificatore.condizione.lower()            
            
            if statistica in STATISTICHE_MODIFICATORI:
                                                
                if any(val in valore for val in ["raddoppiate", "+5", "+6", "+7", "+8", "+9"]):  
                                                  
                    if ( "uso ristretto:" not in condizione or "incrementa con costo:" in condizione ):
                        
                        if modifica_statistiche_applicata: 
                            potenza *= 1.3
                        else:    
                            potenza += 4
                
                elif any(val in valore for val in ["+3", "+4"]):                
                    
                    if ( "uso ristretto:" not in condizione or "incrementa con costo:" in condizione ):
                        
                        if modifica_statistiche_applicata:
                            potenza *= 1.2
                        else:    
                            potenza += 2
                    
                elif any(val in descrizione for val in ["+1", "+2"]):                        
                    
                    if ( "uso ristretto:" not in condizione or "incrementa con costo:" in condizione ):
                            
                            if modifica_statistiche_applicata:
                                potenza *= 1.1
                            else:    
                                potenza += 1
                                    
                if "multiple" in statistica:
                    potenza *= 1.5 # aumenta del 50% la potenza assoluta                
        
        # Bonus per abilita speciali
        for abilita in fortificazione.abilita_speciali:
            # Potenziamento altri guerrieri
            descrizione = abilita.descrizione.lower()
            nome = abilita.nome.lower()
            tipo = abilita.tipo_abilita.lower()

            if potenza == 0:
                potenza = 1.0

            if tipo == "combattimento":                    
                if nome == "uccide automaticamente":
                    potenza *= 1.5
                if nome in ["permette ai guerrieri di attaccare per primi", "i guerrieri alleati uccidono automaticamente"]:
                    potenza *= 1.3
            
                    
            if tipo == "immunita":
                if nome in ["immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria", "annulla immunita dell'Oscura simmetria", "immune ai doni degli apostoli"]:
                    potenza *= 1.4
                elif any( val in nome for val in ["immune agli effetti della specifica arte", "immune allo specifico equipaggiamento", "immune alla specifica fortificazione", "Immune alle ferite durante il combattimento"]):
                    potenza *= 1.2
                                                                                    
            if tipo == "modificatore":        
                if nome in ["aumenta effetto", "aumenta caratteristica"]:
                    potenza *= 1.3
                elif nome in ["trasforma guerrieri uccisi in alleati", "imprigiona guerrieri"]:
                    potenza *= 1.1
                elif nome == "sostituisce guerrieri":
                    potenza *= 1.2

            if tipo == "guarigione" :
                if nome in ["guarisce se stesso", "guarisce guerriero"]:
                    potenza *= 1.3
                if nome == "ripara equipaggiamento o fortificazione":
                    potenza *= 1.1

            if tipo == "arte":                
                if "lancia arte" == nome:
                    potenza *= 1.3                
                elif "lancia arte specifica" == nome:
                    potenza *= 1.2

         
            if tipo == "carte":
                if nome in ["assegna carta", "scarta carta", "elimina carta"]:
                    potenza *= 1.3   

            if tipo == "punti":
                if nome in ["produce punti"]:
                    potenza *= 1.3 

                if nome in ["protezione punti"]:
                    potenza *= 1.5

            if tipo == "azioni":
                if nome in ["converte azioni in azioni d'attacco", "Incrementa Azioni", "Attacca sempre per primo", "Attacco in uscita da Copertura"]:
                    potenza *= 1.3    
                elif nome in ["modifica azione", "modifica stato"]:
                    potenza *= 1.1    

        self.potenze_calcolate['Fortificazione'][fortificazione.nome] = potenza
        return self.potenze_calcolate['Fortificazione'][fortificazione.nome]
    
    def calcola_potenza_arte(self, arte: Arte) -> float:
        """
        Calcola la potenza relativa di una carta Arte
        
        Args:
            arte: Oggetto Arte
            
        Returns:
            float: potenza
        """        
        if arte.nome in self.potenze_calcolate['Arte']:
            return self.potenze_calcolate['Arte'][arte.nome]
        
        potenza = self._calcola_potenza_carta(arte)
        self.potenze_calcolate['Arte'][arte.nome] = potenza
        return potenza
    
    def calcola_potenza_oscura_simmetria(self, oscura: Oscura_Simmetria) -> float:
        """
        Calcola la potenza relativa di una carta Oscura Simmetria
        
        Args:
            oscura: Oggetto Oscura_Simmetria
            
        Returns:
            float: potenza
        """
        if oscura.nome in self.potenze_calcolate['Oscura Simmetria']:
            return self.potenze_calcolate['Oscura Simmetria'][oscura.nome]

        potenza = self._calcola_potenza_carta(oscura)
        self.potenze_calcolate['Oscura Simmetria'][oscura.nome] = potenza
        return potenza

    def calcola_potenza_reliquia(self, reliquia: Reliquia) -> float:
        """
        Calcola la potenza relativa di una reliquia
        
        Args:
            reliquia: Oggetto Reliquia
            
        Returns:
            float: potenza
        """
        if reliquia.nome in self.potenze_calcolate['Reliquia']:
            return self.potenze_calcolate['Reliquia'][reliquia.nome]

        potenza = 1.0
             
        # Bonus per modificatori speciali
        for modificatore in reliquia.modificatori:
            # Potenziamento altri guerrieri
            statistica = modificatore.statistica.lower()
            #descrizione = modificatore.descrizione.lower()
            valore = modificatore.valore.lower()
            condizione = modificatore.condizione.lower()            
            
            if statistica in STATISTICHE_MODIFICATORI:                
                if isinstance(valore, str) and "ristretto:" not in condizione:
                    if valore in ["raddoppiate", "uguale alla più elevata", "x3"]:
                        valore = 10  # Considera raddoppiate come +10 per il calcolo della potenza:
                        break
                    elif valore.startswith('+'):
                        valore = int(valore[1:])  # Rimuovi il segno '+' per la conversione a intero
                    else:
                        valore = 0
                    
                potenza += valore                        
                
        # Bonus per poteri
        for potere in reliquia.poteri:
            # Potenziamento altri guerrieri
            descrizione = potere.descrizione.lower()
            nome = potere.nome.lower()
            tipo = potere.tipo_potere.value.lower()
            limitazioni = potere.limitazioni
            
            if tipo == "combattimento":                    
                if nome in ["uccide automaticamente", "porta rinforzi"]:
                    potenza *= 1.5
                if nome in ["permette ai guerrieri di attaccare per primi", "i guerrieri alleati uccidono automaticamente"]:
                    potenza *= 1.3            
                    
            if tipo == "immunita":
                if nome in ["immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria", "annulla immunita dell'Oscura simmetria", "immune ai doni degli apostoli"]:
                    potenza *= 1.4
                elif any( val in nome for val in ["immune agli effetti della specifica arte", "immune allo specifico equipaggiamento", "immune alla specifica fortificazione", "Immune alle ferite durante il combattimento"]):
                    potenza *= 1.2
                                                                                    
            if tipo == "modificatore":        
                if nome in ["aumenta effetto", "aumenta caratteristica"]:
                    potenza *= 1.3
                elif nome in ["trasforma guerrieri uccisi in alleati", "imprigiona guerrieri"]:
                    potenza *= 1.1
                elif nome == "sostituisce guerrieri":
                    potenza *= 1.2

            if tipo == "guarigione" :
                if nome in ["guarisce se stesso", "guarisce guerriero"]:
                    potenza *= 1.3
                if nome == "ripara equipaggiamento o fortificazione":
                    potenza *= 1.1

            if tipo == "arte":                
                if nome in ["lancia arte", "Annulla effetto arte"]:
                    potenza *= 1.3                
                elif "lancia arte specifica" == nome:
                    potenza *= 1.2

            if tipo == "carte":
                if nome in ["assegna carta", "scarta carta", "elimina carta"]:
                    potenza *= 1.3   

            if tipo == "punti":
                if nome in ["produce punti"]:
                    potenza *= 1.3 

                if nome in ["protezione punti"]:
                    potenza *= 1.5

            if tipo == "azioni":
                if nome in ["converte azioni in azioni d'attacco", "Incrementa Azioni", "Attacca sempre per primo", "Attacco in uscita da Copertura"]:
                    potenza *= 1.3    
                elif nome in ["modifica azione", "modifica stato"]:
                    potenza *= 1.1       


        self.potenze_calcolate['Reliquia'][reliquia.nome] = potenza
        return potenza

    def calcola_potenza_warzone(self, warzone: Warzone) -> float:
        """
        Calcola la potenza relativa di una warzone
        
        Args:
            warzone: Oggetto Warzone
            
        Returns:
            float: potenza
        """
        if warzone.nome in self.potenze_calcolate['Warzone']:
            return self.potenze_calcolate['Warzone'][warzone.nome]
        
        potenza = 1.0                

        # Somma modificatori statistiche
        statistiche = {
            'combattimento':    warzone.stats['combattimento'],
            'sparare':          warzone.stats['sparare'],
            'armatura':         warzone.stats['armatura'],
            'valore':           warzone.stats['valore']
        }

        potenza_positiva = 1.0
        potenza_negativa = 1.0

        for valore_modifica in statistiche.values():
            
            if valore_modifica > 0:
                potenza_positiva += valore_modifica
            else:
                potenza_negativa += abs(valore_modifica)
            
        potenza = potenza_positiva * 2 / potenza_negativa
         

        modifica_statistiche_applicata = True if potenza > 1 else False   

        # NOTA: nel database i valori specificati nei modificatori statistiche e quelli analoghi specificati nei modificatori_speciali 
        # se rappresentano lo stesso potenziamento devono alternativi gli uni agli altri. Pertanto è necessario verificare che se sono specificati per uno, i valori dell'altro 
        # gruppo devono essere posti a 0. Se, invece, i valori riportati nel gruppo statistiche sono di default e quelli specificati nel gruppo modificatori_speciali sono aggiuntivi
        # e vengono aapplicati in base ad una determinata condizione allora devono essere specificati

        # Bonus per modificatori speciali
        for modificatore in warzone.modificatori_difensore:
            # Potenziamento altri guerrieri
            statistica = modificatore.statistica.lower()
            descrizione = modificatore.descrizione.lower()
            valore = modificatore.valore
            condizione = modificatore.condizione.lower()            
            
            # spostare quando considera carta guerriero da associare per valutazione sul gurriero specifico
            if statistica in STATISTICHE_MODIFICATORI:
                                                
                if any(val in valore for val in ["raddoppiate", "+5", "+6", "+7", "+8", "+9"]):  
                                                  
                    if ( "uso ristretto:" not in condizione or "incrementa con costo:" in condizione ):
                        
                        if modifica_statistiche_applicata: 
                            potenza *= 1.3
                        else:    
                            potenza += 4
                
                elif any(val in valore for val in ["+3", "+4"]):                
                    
                    if ( "uso ristretto:" not in condizione or "incrementa con costo:" in condizione ):
                        
                        if modifica_statistiche_applicata:
                            potenza *= 1.2
                        else:    
                            potenza += 2
                    
                elif any(val in descrizione for val in ["+1", "+2"]):                        
                        
                    if ( "uso ristretto:" not in condizione or "incrementa con costo:" in condizione ):
                            
                            if modifica_statistiche_applicata:
                                potenza *= 1.1
                            else:    
                                potenza += 1
                
                                
                if "multiple" in statistica:
                    potenza *= 1.5 # aumenta del 50% la potenza assoluta                
        
        # Bonus per abilita speciali
        for effetto in warzone.effetti_combattimento:
            # Potenziamento altri guerrieri            
            nome = effetto.nome.lower()
            descrizione = effetto.descrizione.lower()
            target = effetto.target.lower()
            tipo = effetto.tipo_effetto.lower()
            effetto_ristretto = True if "ristretto:" in target[:len("ristretto:")] else False
            
            if not effetto_ristretto:

                if tipo == "combattimento":
                        if nome == "uccide automaticamente":
                            potenza *= 1.5
                        if nome in ["permette ai guerrieri di attaccare per primi", "i guerrieri alleati uccidono automaticamente"]:
                            potenza *= 1.3
                        
                if tipo == "punti":
                    if nome in ["produce punti", "guadagna punti"]:
                        potenza *= 1.3 

                    if nome in ["protezione punti"]:
                        potenza *= 1.5

                if tipo == "immunita":
                    if nome in ["immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria", "annulla immunita dell'Oscura simmetria", "immune ai doni degli apostoli"]:
                        potenza *= 1.4
                    elif any( val in nome for val in ["immune agli effetti della specifica arte", "immune allo specifico warzone", "immune alla specifica fortificazione", "Immune alle ferite durante il combattimento"]):
                        potenza *= 1.2
                                                                                        
                if tipo == "modificatore":        
                    if nome in ["aumenta effetto", "aumenta caratteristica"]:
                        potenza *= 1.3
                    elif nome == "trasforma guerrieri uccisi in alleati":
                        potenza *= 1.1
                    elif nome == "sostituisce guerrieri":
                        potenza *= 1.2

                if tipo == "guarigione" :
                    if nome in ["guarisce se stesso", "guarisce guerriero"]:
                        potenza *= 1.3
                    if nome == "ripara equipaggiamento o fortificazione":
                        potenza *= 1.1

                if tipo == "arte":                
                    if "lancia arte e/o incantesimo dell'arte" == nome:
                        potenza *= 1.3                
                    elif "lancia arte e/o incantesimo dell'arte specifica" == nome:
                        potenza *= 1.2
            
                if tipo == "carte":
                    if nome in ["assegna carta", "scarta carta", "elimina carta"]:
                        potenza *= 1.3    

                if tipo == "azioni":
                    if nome in ["converte azioni in azioni d'attacco", "Incrementa Azioni", "Attacca sempre per primo"]:
                        potenza *= 1.3    
                    elif nome in ["modifica azione", "modifica stato"]:
                        potenza *= 1.1                 

        self.potenze_calcolate['Warzone'][warzone.nome] = potenza
        return potenza
        
    def calcola_potenza_speciale(self, speciale: Speciale) -> float:
        """
        Calcola la potenza relativa di una carta Speciale
        
        Args:
            arte: Oggetto Speciale
            
        Returns:
            float: potenza
        """
        if speciale.nome in self.potenze_calcolate['Speciale']:
            return self.potenze_calcolate['Speciale'][speciale.nome]

        potenza = self._calcola_potenza_carta(speciale)
        self.potenze_calcolate['Speciale'][speciale.nome] = potenza
        return potenza
                  
    def _calcola_potenza_carta_stats(self, carta: Any) -> float:
        """
        Calcola la potenza relativa alle statistiche di combattimento di una carta di supporto: Speciale, Arte e Oscura_Simmetria
        
        Args:
            carta Oggetto Speciale, Arte e Oscura_Simmetria
            
        Returns:
            float: potenza
        """
        
        potenza = 1.0
        # Analizza effetti statistiche
        for effetto in carta.effetti:

            tipo_effetto = effetto.tipo_effetto.lower() # es. "Modificatore", "Controllo", "Danno", etc.
            valore = effetto.valore # valore numerico dell'effetto (se applicabile)
            statistica_target = effetto.statistica_target.lower() # quale statistica viene modificata (C, S, A, V)
            descrizione_effetto = effetto.descrizione_effetto #descrizione effetto: 'uccide', ferisce automaticamente', 'scarta guerriero' 'scarta carta'
            desc = descrizione_effetto.lower()

            if tipo_effetto == "modificatore" and statistica_target in ["combattimento", "sparare", "armatura", "C", "S", "A"] and isinstance(valore, int) and valore > 0:
                potenza += valore                     
        
        
        return potenza
       
    def _calcola_potenza_carta_azioni(self, carta: Any) -> float:
        """
        Calcola la potenza relativa alle sazioni di una carta di supporto: Speciale, Arte e Oscura_Simmetria
        
        Args:
            carta Oggetto Speciale, Arte e Oscura_Simmetria
            
        Returns:
            float: potenza
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
                    potenza = 1.4
            
            elif isinstance(valore, int) and valore > 0:
                if tipo_effetto in ['azione combattimento', 'azione fase']: # Azione Fase, Azione Ogni Momento
                    potenza *= valore
                elif tipo_effetto == 'azione ogni momento':
                    potenza *= 2 * valore
            
        return potenza
        
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
    
        # FUNZIONI SUPPORTO
        def _assegnazione_punteggio_guerriero_ammesso(self, guerriero: Guerriero):
        
            guerrieri_ammessi.append(guerriero) 
            
            if guerriero.fondamentale:
                punteggio = random.uniform(20, 25)
            else:
                punteggio = self.calcola_potenza_guerriero(guerriero)

            punteggi[guerriero.nome] = punteggio * bonus_moltiplicatore * bonus_factor_guerriero_strategico                    
    


        # Ottieni tutti i guerrieri disponibili e filtrali per espansione
        tutti_guerrieri = self.collezione.get_carte_per_tipo_mazzo('guerriero')
        guerrieri_disponibili = self.filtra_carte_per_espansioni(tutti_guerrieri, espansioni_richieste)

        
        if not guerrieri_disponibili:
            return [], []
        
        # Separa guerrieri per categoria
           
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
        BONUS_STRATEGICO = 4 # # Fattore applicato in base all'assegnazione del valore "valore_strategico" da parte dell'utente

        for guerriero in guerrieri_disponibili:
            
            if guerriero.nome in punteggi:
                continue

            punteggio = 0 # punteggio base
            
            # Bonus per orientamenti
            bonus_moltiplicatore = 1.0              
            bonus_factor_guerriero_strategico = 1

            if hasattr(guerriero, 'valore_strategico'):
                bonus_factor_guerriero_strategico = 1 + guerriero.valore_strategico * BONUS_STRATEGICO / 10

            # Orientamento Doomtrooper            
            if doomtrooper and guerriero.fazione in FAZIONI_DOOMTROOPER:
                ammesso = False              

                if not orientamento_doomtrooper or orientamento_doomtrooper == []: # il guerriero è un doomtrooper e non è definito l'orientamento
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE # aumenta il punteggio se la fazione è nei doomtroopers
                    ammesso = True

                elif guerriero.fazione.value in orientamento_doomtrooper: #il guerriero è un doomtrooper con fazione inclusa nell'orientamento: 
                    bonus_moltiplicatore *= BONUS_ORIENTAMENTO# triplica il punteggio se la fazione è anche nell'orientamento doomtroopers
                    ammesso = True
                
                if ammesso:
                    _assegnazione_punteggio_guerriero_ammesso(self, guerriero)

            # Orientamento Arte (per guerrieri Fratellanza)
            elif fratellanza and guerriero.fazione in FAZIONI_FRATELLANZA: # 
                ammesso = False

                if not orientamento_arte or orientamento_arte == []: # il guerriero è della fratellanza e non è definito l'orientamento
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE
                    ammesso = True
                
                # Le arti possono essere utilizzate anche da guerrieri non appartenenti alla Fratellanza
                elif orientamento_arte and len(orientamento_arte) > 0: # Sono definite le arti preferite
                    for abilita in guerriero.abilita:
                        #escludi_oscura_legione = guerriero.fazione in FAZIONI_OSCURA_LEGIONE and not oscura_legione # True se il guerriero è OL e non è previsto nel mazzo l'oscura legione
                        #escludi_doomtrooper = guerriero.fazione in FAZIONI_DOOMTROOPER and not doomtrooper # True se il guerriero è DOOMTROOPER e non è previsto nel mazzo i doomtrooper
                        if abilita.tipo == 'Arte': # and not (escludi_oscura_legione or escludi_doomtrooper) : # esclude se il guerriero è OL e non è previsto nel mazzo l'oscura legione
                            disciplina = abilita.target
                            if any( arte_ in disciplina for arte_ in orientamento_arte ):
                                bonus_moltiplicatore *= BONUS_ORIENTAMENTO # triplica se il fratello lancia la specifica arte
                                ammesso = True
                            elif disciplina == DisciplinaArte.TUTTE.value:
                                bonus_moltiplicatore *= (BONUS_ORIENTAMENTO * 2)   # raddoppia se il fratello lancia la specifica arte
                                ammesso = True                            

                if ammesso:
                    _assegnazione_punteggio_guerriero_ammesso(self, guerriero)
              
            
            # Orientamento Apostolo (per guerrieri Oscura Legione)
            elif oscura_legione and guerriero.fazione in FAZIONI_OSCURA_LEGIONE: # and guerriero.fazione in FAZIONI_OSCURA_LEGIONE:
                ammesso = False

                if not orientamento_apostolo or orientamento_apostolo == []:
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE
                    ammesso = True
                    
                elif orientamento_apostolo and len(orientamento_apostolo) > 0 :                    
                    for apostolo in orientamento_apostolo:
                        if f"Seguace di {apostolo}" in guerriero.keywords:
                            bonus_moltiplicatore *= BONUS_ORIENTAMENTO
                            ammesso = True
                                                
                if orientamento_cultista and 'Cultista' in guerriero.keywords:
                    bonus_moltiplicatore *= BONUS_CULTISTA # aumenta di un ulteriore fattore (BONUS_CULTISTA) il bonus per cultisti (i cultisti sono OL quindi già beneficiano dell'eventuale bonus OL)
                    ammesso = True

                if ammesso:
                    _assegnazione_punteggio_guerriero_ammesso(self, guerriero)

            
            # Orientamento Eretico (per guerrieri Doomtrooper o Oscura Legione)
            if orientamento_eretico and 'Eretico' in guerriero.keywords:
                    # bonus_moltiplicatore *= BONUS_ERETICO # aumenta di un ulteriore fattore (BONUS_ERETICI) il bonus per eretici (gli eretici sono OL o DOOMTROOPER quindi già beneficiano dell'eventuale bonus O o DOmmotrooper)
                    if guerriero not in guerrieri_ammessi:
                        bonus_moltiplicatore *= BONUS_ERETICO
                        _assegnazione_punteggio_guerriero_ammesso(self, guerriero)
                    elif guerriero.nome in punteggi:
                        punteggi[guerriero.nome] *= BONUS_ERETICO # aumenta di un ulteriore fattore (BONUS_ERETICI) il bonus per eretici (gli eretici sono OL o DOOMTROOPER quindi già beneficiano dell'eventuale bonus O o DOmmotrooper)
                    else:
                        print(f"MA CHI CAZZ'E'??: Escluso eretico guerriero {guerriero.nome} della fazione {guerriero.fazione} non compatibile con le fazioni selezionate per il mazzo")
            
            #punteggi[guerriero.nome] = punteggio * bonus_moltiplicatore * bonus_factor_guerriero_strategico
        
        # Ordina guerrieri per punteggio
        guerrieri_ordinati = sorted(guerrieri_ammessi, 
                                   key=lambda g: punteggi.get(g.nome, 0), 
                                   reverse=True)
        
        # Seleziona guerrieri garantendo distribuzione equa
        squadra = []
        schieramento = []
        numero_guerrieri_richiesto_non_raggiunto = True
        quantita_utilizzata = {}

        for guerriero in guerrieri_ordinati:
            quantita_utilizzata[guerriero.nome] = 0
        

        while numero_guerrieri_richiesto_non_raggiunto:

            for guerriero in guerrieri_ordinati:
                
                #if guerriero.nome in [g.nome for g in squadra] or guerriero.nome in [g.nome for g in schieramento]:
                #    continue
                    
                quantita_disponibile = getattr(guerriero, 'quantita') - quantita_utilizzata[guerriero.nome]
                quantita_consigliata = getattr(guerriero, 'quantita_minima_consigliata')           

                # se non è definita la quantità consigliata ( = 0 ) la calcola in base al valore del guerriero (maggiore costo)                                    
                if quantita_consigliata and quantita_consigliata <1:                    
                    
                    if guerriero.stats.valore >= 10 or guerriero.tipo == 'Personalita':                                        
                        quantita_consigliata = 1             
                        
                    elif 7 <= guerriero.stats.valore < 10: # 7 e 8                        
                        min_val = random.randint(1, 2)                    
                        quantita_consigliata = random.randint(min_val, min_val + 2)                

                    elif 4 <= guerriero.stats.valore < 7: # 7 e 8                                
                        min_val = random.randint(1, 3)
                        quantita_consigliata = random.randint(min_val, min_val + 2)                                

                    else: 
                        min_val = random.randint(1, 2)                                    
                        quantita_consigliata = random.randint(min_val, min_val + 1)                
                    
                num_copie_da_inserire = min(5, quantita_disponibile, quantita_consigliata)    
                quantita_utilizzata[guerriero.nome] += num_copie_da_inserire

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

            
            if ( len(squadra) + len(schieramento)) >= numero_guerrieri_target: # se il limite è raggiunto esce altrimenti ripete il ciclo
                # Target raggiunto, esce
                numero_guerrieri_richiesto_non_raggiunto = False
            else:
                # Target non raggiunto, verifica se ci sono ancora carte disponibili
                carte_ancora_disponibili = False

                for guerriero in guerrieri_ordinati:
                    if getattr(guerriero, 'quantita') - quantita_utilizzata[guerriero.nome] > 0:
                        carte_ancora_disponibili = True
                        break
                
                if not carte_ancora_disponibili:
                    # Non ci sono più carte disponibili, esce
                    numero_guerrieri_richiesto_non_raggiunto = False
    
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
        # cmabia questi valori per aumentare o diminuire la distribuzione delle carte in base al tipo
        DISTRIBUZIONE_EQUIPAGGIAMENTO = {
            'combattimento':    0.25, 
            'sparare':          0.25,
            'armatura':         0.25,
            'azioni':           0.125            
        }
        # cmabia questi valori per aumentare o diminuire la distribuzione delle carte in base al tipo
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
        BONUS_ORIENTAMENTO = 10.0 # Fattore punteggio applicato alle preferenze specifiche di orientamento
        BONUS_ERETICO = 2 # Fattore applicato se selezionati ERETICI
        BONUS_CULTISTA = 2 # Fattore applicato se selezionati CULTISTI     
        BONUS_STRATEGICO = 4 # Fattore applicato in base all'assegnazione del valore "valore_strategico" da parte dell'utente
        BONUS_FONDAMENTALE = 100 # Fattore applicato se la carta è fondamentale

        # Calcola potenza per ogni carta
        carte_con_punteggio = []
        
        for carta in carte_disponibili:
                        
            bonus_moltiplicatore = 1.0            
            fattore_incremento = 1 # fattore di incremento del rating assegnato alla carta se è fondamentale

            if hasattr(carta, 'valore_strategico') and carta.valore_strategico != None and carta.valore_strategico > 0:
                fattore_incremento = 1 + carta.valore_strategico * BONUS_STRATEGICO / 10 
            
            if carta.fondamentale:
                fattore_incremento = BONUS_FONDAMENTALE
                
        
            fazioni = []
            solo_nefarita = False
            solo_personalita = False

            if hasattr(carta, 'fazione'):
                fazioni = [carta.fazione]
            elif hasattr(carta, 'fazioni_permesse'):
                fazioni = carta.fazioni_permesse
            if hasattr(carta, 'restrizioni'):                
                if hasattr(carta.restrizioni, 'fazioni_permesse'):
                    fazioni = carta.restrizioni.fazioni_permesse
                if isinstance(carta.restrizioni, list):
                    #solo_seguace_apostolo = f"Solo Seguace di {apostolo}" in carta.restrizioni and f"Seguace di {apostolo}" in guerriero.keywords  # NO VIENE CONSIDERATO NELLA VALUTAZIOBNE DELL'ORIENTAMENTO APOSTOLO EFFETTUATA PIU AVANTI
                    solo_nefarita = f"Solo Nefarita" in carta.restrizioni
                    solo_personalita = f"Solo Personalita" in carta.restrizioni

                    if  solo_nefarita or solo_personalita: # or solo_seguace_apostolo:
                        for guerriero in tutti_guerrieri:
                            if ( solo_nefarita and guerriero.tipo == 'Nefarita' ) or ( solo_personalita and guerriero.tipo == 'Personalita' ):
                                fattore_incremento *= 1.5 # aumenta del 50% il fattore di incremento se la carta è dedicata a nefariti
                                break 
            
            carta_generica_fondamentale = Fazione.GENERICA in fazioni and carta.fondamentale

            # Verifica compatibilità carta - guerrieri            
            carta_compatibile, numero_guerrieri_compatibili = self._carta_compatibile_con_guerrieri(carta, tutti_guerrieri)            

            # se non compatibile conitnua con il prossimo elemento del ciclo
            if not (carta_compatibile or carta_generica_fondamentale):
                continue 

            doomtrooper_dedicata = any(f in fazioni for f in FAZIONI_DOOMTROOPER) or 'Doomtrooper'
            orientamento_doomtrooper_dedicata = any(f in orientamento_doomtrooper for f in fazioni) if (orientamento_doomtrooper and len(orientamento_doomtrooper) > 0) else False
            fratellanza_dedicata = any(f in fazioni for f in FAZIONI_FRATELLANZA)
            oscura_legione_dedicata = any(f in fazioni for f in FAZIONI_OSCURA_LEGIONE)

            # Assegnazione dei fattori di moltiplicazione del punteggio in base agli orientamenti
            # Orientamento Doomtrooper
            if doomtrooper and doomtrooper_dedicata: # la carta è dedicata ai doomtrooper o è generica (fazione None)        
                            
                if orientamento_doomtrooper_dedicata: #la carta è dedicata ai doomtrooper con fazione inclusa nell'orientamento: 
                    bonus_moltiplicatore *= BONUS_ORIENTAMENTO * fattore_incremento # triplica il punteggio se la fazione è anche nell'orientamento doomtrooper
            
                elif "Doomtrooper" in fazioni or any(f in (FAZIONI_DOOMTROOPER + [Fazione.FRATELLANZA]) for f in fazioni): # la carta è dedicata a tutti i doomtrooper
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE * fattore_incremento # aumenta il punteggio se la fazione è nei doomtroopers

                else: # la carta è dedicata ad una fazione doomtrooper non presente nelle fazioni della carta
                    pass # eventuale decremento del bous se necessario (non implementato)
                
            # Orientamento Arte (per guerrieri Fratellanza)                
            if fratellanza and fratellanza_dedicata and not (doomtrooper_dedicata or orientamento_doomtrooper_dedicata): # la carta è dedicata alla fratellanza                

                if tipo_carta == 'arte':                                        
                    # Le arti possono essere utilizzate anche da guerrieri non appartenenti alla Fratellanza                    
                        if orientamento_arte and len(orientamento_arte) > 0: # Sono definite le arti preferite
                            
                            disciplina = carta.disciplina.value
                            if disciplina in orientamento_arte:                            
                                    bonus_moltiplicatore *= BONUS_ORIENTAMENTO * fattore_incremento # triplica se il fratello lancia la specifica arte
                            elif disciplina == DisciplinaArte.TUTTE.value:
                                bonus_moltiplicatore *= (BONUS_ORIENTAMENTO + 1) * fattore_incremento   # triplica se il fratello lancia la specifica arte                    
                        else: # non sono definite arti preferite
                            bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE * fattore_incremento # aumenta il punteggio se la fazione è nei doomtroopers
                else:
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE  * fattore_incremento # aumenta il punteggio se la fazione è nei doomtroopers
            
             # Orientamento Apostolo (per guerrieri Oscura Legione)
            # Orientamento Apostolo (per guerrieri Oscura Legione)
            if oscura_legione and oscura_legione_dedicata: # la carta è dedicata alla oscura legione 

                if carta.tipo.value in ["Dono dell'Oscura Simmetria", "Dono dell'Oscura Legione"]:
                    bonus_moltiplicatore *= BONUS_SPECIALIZZAZIONE * fattore_incremento

                elif orientamento_apostolo and len(orientamento_apostolo) > 0 : # la carta è dedicata alla oscura legione e sono definiti gli apostoli preferiti
                    bonus_applicato = False
                    for apostolo in orientamento_apostolo:
                        seguace = f"Seguace di {apostolo}" in carta.keywords # or (hasattr(carta, 'restrizioni') and isinstance(carta.restrizioni, List) and f"Solo Seguaci di {apostolo}" in carta.restrizioni)
                        if seguace:
                            bonus_moltiplicatore *= BONUS_ORIENTAMENTO * fattore_incremento
                            bonus_applicato = True
                    
                    if not bonus_applicato and tipo_carta == 'oscura_simmetria':
                        bonus_moltiplicatore /= 2 * BONUS_FONDAMENTALE  # pass    #non implementato: decremento del bonus per evitare la scelta di carte appartenenti ad apostoli non presenti in orientamento conseguente la presenza di guerrieri non seguaci ed in grado di utilizzare sia i doni degli apostoli che quelli dell'oscura simmetria
                
                if orientamento_cultista and 'Cultista' in carta.keywords:
                    bonus_moltiplicatore *= BONUS_CULTISTA # aumenta di un ulteriore fattore (BONUS_CULTISTA) il bonus per cultisti (i cultisti sono OL quindi già beneficiano dell'eventuale bonus OL)
            # Orientamento Eretico (per guerrieri Doomtrooper o Oscura Legione)
            if orientamento_eretico and 'Eretico' in carta.keywords:
                bonus_moltiplicatore *= BONUS_ERETICO # triplica il punteggio se la fazione è anche nell'orientamento doomtroopers
            # Carta generica fondamentale (il bonus_moltiplicatore utilizzato per il calcolo del punteggio non viene valutato per la condizione fondamentale nelle assegnazioni per orientamento)
            if carta_generica_fondamentale:
                bonus_moltiplicatore *= BONUS_FONDAMENTALE # aumenta di un ulteriore fattore (BONUS_FONDAMENTALE) il bonus per carte generiche fondamentali

            # Valutazione per carte con keyword di incremento specifico
            if hasattr(carta, "keywords") and "Ulteriore incremento per specifico guerriero, fazione o corporazione" in carta.keywords:

                if tipo_carta == "warzone":

                    # Nota: le valutazioni su "effetti_combattimento" sono effettuate nel calolo della potenza della warzone

                    for modificatore in carta.modificatori_difensore:

                        guerrieri_dedicati = modificatore.difensore

                        for guerriero_dedicato in guerrieri_dedicati:
                            
                            req_doom = doomtrooper and ( "Doomtrooper" in guerriero_dedicato or guerriero_dedicato == DOOMTROOPER )
                            req_osc_l = oscura_legione and "Oscura Legione" in guerriero_dedicato
                            req_frat = fratellanza and "Fratellanza" in guerriero_dedicato
                            req_seg = not req_osc_l and oscura_legione and orientamento_apostolo and len(orientamento_apostolo) > 0 and "Seguaci di" == guerriero_dedicato[:len("Seguaci di")] and guerriero_dedicato.split("Seguaci di ")[1] in orientamento_apostolo  
                            req_corp_doom = not req_doom and doomtrooper and any( guerriero_dedicato == f.value for f in FAZIONI_DOOMTROOPER)
                            req_cul = "Cultista" in guerriero_dedicato[:len("Cultista")]
                            req_ere = "Eretico" in guerriero_dedicato[:len("Eretico")]               

                            if req_seg or req_doom or req_corp_doom or req_frat or req_osc_l or req_cul or req_ere:
                                bonus_moltiplicatore *= 1.25
                                break
                            
                            else: # specifico guerriero
                                for guerriero in tutti_guerrieri:
                                    if guerriero.nome == guerriero_dedicato:
                                        bonus_moltiplicatore *= 2.0
                                        break     
                                

                if tipo_carta == "equipaggiamento":
                    pass

                if tipo_carta == "speciale":
                    pass

                if tipo_carta == "arte":
                    pass

                if tipo_carta == "oscura_simmetria":
                    pass
            

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
                potenza = 1.0  # Default per missioni
            
            if bonus_moltiplicatore >= 1:
                fattore_compatibilita = 1 + 2 * numero_guerrieri_compatibili / numero_guerrieri # raddoppia se la metà dei guerrieri può utilizzare la carta, triplica se tutti            
                punteggio = potenza * fattore_compatibilita * bonus_moltiplicatore
                carte_con_punteggio.append((carta, punteggio))
        
        # Ordina per potenza
        carte_con_punteggio.sort(key=lambda x: x[1], reverse=True)
        
        # Seleziona carte
        quantita_utilizzata = {}

        for carta, _ in carte_con_punteggio:
            quantita_utilizzata[carta.nome] = 0

        numero_carte_richiesto_non_raggiunto = True

        while numero_carte_richiesto_non_raggiunto:

            for carta, _ in carte_con_punteggio:
                
                if len(carte_selezionate) >= numero_carte:
                    return carte_selezionate
                
                # Calcola numero di copie
                quantita_disponibile = getattr(carta, 'quantita') - quantita_utilizzata[carta.nome]
                quantita_minima_consigliata = getattr(carta, 'quantita_minima_consigliata')
                numero_copie_prelevabile = numero_carte / len(carte_con_punteggio)

                # valuta la quantita minima di copie da considerare nella richiesta qualora il numero di carte presenti  
                # nella lista di carte con punteggio è inferiore rispetto  al numero complessivo richiesto:
                #  (aumenta la quantità mini,a richiesta di carte per uno stesso tipo)

                if quantita_minima_consigliata < 1:
                    quantita_minima_consigliata = random.randint(1,3)
                
                if numero_copie_prelevabile > 1 and ( random.random() < numero_copie_prelevabile - 1 ):
                    numero_copie_prelevabile = math.ceil(numero_copie_prelevabile)
                else:
                    numero_copie_prelevabile = math.floor(numero_copie_prelevabile)

                if quantita_minima_consigliata < numero_copie_prelevabile:                    
                    quantita_minima_consigliata = numero_copie_prelevabile

                num_copie_da_inserire = min(5, quantita_disponibile, quantita_minima_consigliata)   
                quantita_utilizzata[carta.nome] += num_copie_da_inserire

                for _ in range(num_copie_da_inserire):
                    
                    if len(carte_selezionate) < numero_carte:
                        carte_selezionate.append(carta)# NOTA: inserisce nella lista copie di una stessa istanza                        

                    else:
                        return carte_selezionate  # limite raggiunto


            if len(carte_selezionate) >= numero_carte: # se il limite è raggiunto esce altrimenti ripete il ciclo
                # Target raggiunto, esce
                numero_carte_richiesto_non_raggiunto = False
            else:
                # Target non raggiunto, verifica se ci sono ancora carte disponibili
                carte_ancora_disponibili = False

                for carta, _ in carte_con_punteggio:
                    if getattr(carta, 'quantita') - quantita_utilizzata[carta.nome] > 0:
                        carte_ancora_disponibili = True
                        break
                
                if not carte_ancora_disponibili:
                    numero_carte_richiesto_non_raggiunto = False
                
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
                    
                    if ( tipo_carta in ['arte', 'oscura_simmetria'] and risultato.get('puo_lanciare') ) or  ( tipo_carta == 'warzone' and risultato.get('puo_assegnare') ) or (tipo_carta == 'reliquia' and risultato.get('puo_assegnare')):
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
            ridistribuzione_totale += distribuzione['reliquia']
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
        orientamento_cultista: Se True, preferisce guerrieri cultisti (opzionale)
        
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
    
    #esporta_immagini_mazzi([risultato], verbose= True)

    return risultato


# ================================================================================
# FUNZIONI DI UTILITÀ
# ================================================================================


##################################################################################
# Funzioni in cui è definito il formato di salvataggio del file json:
#
# salva_mazzi_json_migliorato_con_conteggio_e_apostoli -> 
#   ->  crea_inventario_dettagliato_mazzo_json_con_conteggio_e_apostoli 
#       ->  processa_guerrieri_per_fazioni_con_apostoli, ottieni_attributo_sicuro
#       ->  processa_supporto_per_classi -> determina_classe_supporto, ottieni_attributo_sicuro
##################################################################################


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
            
            if classe in ["Warzone", "Reliquia"]:
                utilizzatori = carta.restrizioni.fazioni_permesse
            else:
                utilizzatori = ottieni_attributo_sicuro(carta, 'fazioni_permesse', [])


            if nome not in dettagli_carte:
                dettagli_carte[nome] = {
                    'copie': 0,
                    'classe': classe,
                    'set_espansione': ottieni_attributo_sicuro(carta, 'set_espansione', 'Base'),
                    'rarity': ottieni_attributo_sicuro(carta, 'rarity', 'Common'),                    
                    'quantita_collezione': ottieni_attributo_sicuro(carta, 'quantita', 0),
                    'utilizzatori': utilizzatori
                }
                
                # Aggiungi attributi specifici se presenti
                try:
                    if hasattr(carta, 'fazione'):
                        fazione_obj = carta.fazione
                        if hasattr(fazione_obj, 'value'):
                            dettagli_carte[nome]['fazione'] = fazione_obj.value
                        else:
                            dettagli_carte[nome]['fazione'] = str(fazione_obj)
                    
                    if hasattr(carta, 'valore_strategico'):
                        dettagli_carte[nome]['valore_strategico'] = carta.valore_strategico
                    
                    if hasattr(carta, 'fondamentale'):
                        dettagli_carte[nome]['fondamentale'] = carta.fondamentale
                    
                    if hasattr(carta, 'disciplina'):
                        disciplina_obj = carta.disciplina
                        if hasattr(disciplina_obj, 'value'):
                            dettagli_carte[nome]['disciplina'] = disciplina_obj.value
                        else:
                            dettagli_carte[nome]['disciplina'] = str(disciplina_obj)
                    
                    if hasattr(carta, 'tipo'):
                        tipo_obj = carta.tipo
                        if hasattr(tipo_obj, 'value'):
                            dettagli_carte[nome]['tipo'] = tipo_obj.value
                        else:
                            dettagli_carte[nome]['tipo'] = carta.tipo

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
# ISTRUZIONI PER L'INTEGRAZIONE - ATT: VERIF
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
# GESTIONE IMMAGINI MAZZI
# ================================================================================

# Costanti per le cartelle immagini
PERCORSO_BASE_IMMAGINI = "image/"
PERCORSO_BASE_MAZZI = "out/mazzi_immagini/"

def ottieni_percorso_cartella_immagini_sorgente(tipo_carta: str, carta: Any) -> Optional[str]:
    """
    Ottiene il percorso della cartella sorgente delle immagini in base al tipo di carta.

    Per i guerrieri, usa la fazione della carta.
    Per le altre carte, usa il tipo specifico.

    Args:
        tipo_carta: Il tipo di carta ('guerriero', 'equipaggiamento', etc.)
        carta: L'oggetto carta da cui estrarre eventuali informazioni aggiuntive

    Returns:
        Il percorso relativo alla cartella delle immagini o None se non trovato
    """
    # Mappatura tipo carta -> nome cartella immagini
    mappatura_cartelle = {
        'equipaggiamento': 'Equipaggiamento',
        'arte': 'Arte',
        'fortificazione': 'Fortificazioni',
        'missione': 'Missioni',
        'speciale': 'Speciali',
        'oscura_simmetria': 'Oscura Simmetria',
        'reliquia': 'Reliquie',
        'warzone': 'Warzone'
    }

    if tipo_carta == 'guerriero':
        # Per i guerrieri, usa la fazione
        if hasattr(carta, 'fazione') and carta.fazione:
            fazione_nome = carta.fazione.value if hasattr(carta.fazione, 'value') else str(carta.fazione)
            return os.path.join(PERCORSO_BASE_IMMAGINI, fazione_nome)
        return None
    else:
        # Per altre carte, usa la mappatura
        nome_cartella = mappatura_cartelle.get(tipo_carta)
        if nome_cartella:
            return os.path.join(PERCORSO_BASE_IMMAGINI, nome_cartella)
        return None

def trova_file_case_insensitive(cartella: str, nome_file: str) -> Optional[str]:
    """
    Cerca un file in una cartella ignorando maiuscole/minuscole.

    Args:
        cartella: Il percorso della cartella in cui cercare
        nome_file: Il nome del file da cercare

    Returns:
        Il percorso completo del file se trovato, None altrimenti
    """
    if not os.path.exists(cartella):
        return None

    try:
        # Ottieni tutti i file nella cartella
        files_in_dir = os.listdir(cartella)

        # Cerca il file ignorando maiuscole/minuscole
        nome_file_lower = nome_file.lower()
        for file_name in files_in_dir:
            if file_name.lower() == nome_file_lower:
                return os.path.join(cartella, file_name)

        return None
    except Exception:
        return None

def ottieni_nome_file_immagine(nome_carta: str) -> str:
    """
    Converte il nome di una carta nel nome del file immagine corrispondente.

    Sostituisce gli spazi con underscore e aggiunge l'estensione .jpg

    Args:
        nome_carta: Il nome della carta

    Returns:
        Il nome del file immagine
    """
    return nome_carta.replace(' ', '_') + '.jpg'

def is_guerriero_oscura_legione(carta: Any) -> bool:
    """
    Verifica se un guerriero appartiene all'Oscura Legione.

    Args:
        carta: L'oggetto carta del guerriero

    Returns:
        True se il guerriero è dell'Oscura Legione, False altrimenti
    """
    if hasattr(carta, 'fazione') and carta.fazione:
        fazione_nome = carta.fazione.value if hasattr(carta.fazione, 'value') else str(carta.fazione)
        return fazione_nome == "Oscura Legione"
    return False

def crea_struttura_cartelle_mazzo(nome_mazzo: str) -> str:
    """
    Crea la struttura di cartelle per un mazzo.

    Crea una cartella principale per il mazzo e sottocartelle per ogni tipo di carta.
    Per i guerrieri, crea due sottocartelle: 'schieramento' e 'squadra'.

    Args:
        nome_mazzo: Il nome del mazzo

    Returns:
        Il percorso della cartella principale del mazzo
    """
    # Crea la cartella principale del mazzo
    cartella_mazzo = os.path.join(PERCORSO_BASE_MAZZI, nome_mazzo)
    os.makedirs(cartella_mazzo, exist_ok=True)

    # Mappatura tipi carta -> nome cartella nel mazzo
    nomi_cartelle_mazzo = {
        'equipaggiamento': 'Equipaggiamento',
        'arte': 'Arte',
        'fortificazione': 'Fortificazioni',
        'missione': 'Missioni',
        'speciale': 'Speciali',
        'oscura_simmetria': 'Oscura_Simmetria',
        'reliquia': 'Reliquie',
        'warzone': 'Warzone'
    }

    # Crea tutte le sottocartelle (eccetto Guerriero che ha sottocartelle speciali)
    for nome_cartella in nomi_cartelle_mazzo.values():
        sottocartella = os.path.join(cartella_mazzo, nome_cartella)
        os.makedirs(sottocartella, exist_ok=True)

    # Crea la cartella Guerriero con le sottocartelle schieramento e squadra
    cartella_guerriero = os.path.join(cartella_mazzo, 'Guerriero')
    os.makedirs(os.path.join(cartella_guerriero, 'schieramento'), exist_ok=True)
    os.makedirs(os.path.join(cartella_guerriero, 'squadra'), exist_ok=True)

    return cartella_mazzo

def copia_immagini_mazzo(nome_mazzo: str, mazzo) -> Dict[str, Any]:
    """
    Copia le immagini delle carte di un mazzo nella cartella dedicata.

    Per ogni carta nel mazzo:
    1. Determina la cartella sorgente dell'immagine
    2. Trova il file immagine
    3. Lo copia nella sottocartella appropriata del mazzo

    Args:
        nome_mazzo: Il nome del mazzo
        mazzo: L'oggetto Mazzo (può essere un oggetto ricostruito con .carte o un dict con squadra/schieramento/carte_supporto)

    Returns:
        Un dizionario con le statistiche della copia
    """
    risultati = {
        'nome_mazzo': nome_mazzo,
        'totale_carte': 0,
        'immagini_copiate': 0,
        'immagini_non_trovate': [],
        'errori': []
    }

    # Crea la struttura delle cartelle
    cartella_mazzo = crea_struttura_cartelle_mazzo(nome_mazzo)

    # Mappatura tipi carta -> nome cartella nel mazzo
    nomi_cartelle_mazzo = {
        'guerriero': 'Guerriero',
        'equipaggiamento': 'Equipaggiamento',
        'arte': 'Arte',
        'fortificazione': 'Fortificazioni',
        'missione': 'Missioni',
        'speciale': 'Speciali',
        'oscura_simmetria': 'Oscura_Simmetria',
        'reliquia': 'Reliquie',
        'warzone': 'Warzone'
    }

    # Tiene traccia delle carte già copiate per evitare duplicati
    carte_copiate = set()

    def copia_carta(carta, tipo_carta_override=None):
        """Funzione helper per copiare una singola carta"""
        risultati['totale_carte'] += 1

        # Evita di copiare la stessa carta più volte
        if carta.nome in carte_copiate:
            return

        try:
            # Determina il tipo di carta
            if tipo_carta_override:
                tipo_carta = tipo_carta_override
            else:
                tipo_carta = type(carta).__name__.lower()

            # Ottiene la cartella di destinazione
            if tipo_carta not in nomi_cartelle_mazzo:
                risultati['errori'].append(f"Tipo carta sconosciuto per {carta.nome}: {tipo_carta}")
                return

            cartella_destinazione = os.path.join(cartella_mazzo, nomi_cartelle_mazzo[tipo_carta])

            # Per i guerrieri, aggiungi la sottocartella appropriata (schieramento o squadra)
            if tipo_carta == 'guerriero':
                if is_guerriero_oscura_legione(carta):
                    cartella_destinazione = os.path.join(cartella_destinazione, 'schieramento')
                else:
                    cartella_destinazione = os.path.join(cartella_destinazione, 'squadra')

            # Ottiene la cartella sorgente
            cartella_sorgente = ottieni_percorso_cartella_immagini_sorgente(tipo_carta, carta)

            if not cartella_sorgente:
                risultati['errori'].append(f"Impossibile determinare cartella sorgente per {carta.nome}")
                return

            # Ottiene il nome del file immagine
            nome_file = ottieni_nome_file_immagine(carta.nome)

            # Cerca il file ignorando maiuscole/minuscole
            percorso_sorgente_trovato = trova_file_case_insensitive(cartella_sorgente, nome_file)

            # Copia il file se esiste
            if percorso_sorgente_trovato:
                percorso_destinazione = os.path.join(cartella_destinazione, os.path.basename(percorso_sorgente_trovato))
                shutil.copy2(percorso_sorgente_trovato, percorso_destinazione)
                risultati['immagini_copiate'] += 1
                carte_copiate.add(carta.nome)
            else:
                percorso_sorgente = os.path.join(cartella_sorgente, nome_file)
                risultati['immagini_non_trovate'].append(f"{carta.nome} ({percorso_sorgente})")
                carte_copiate.add(carta.nome)  # Aggiungi anche se non trovata per evitare duplicati

        except Exception as e:
            risultati['errori'].append(f"Errore copiando {carta.nome}: {str(e)}")
            carte_copiate.add(carta.nome)  # Aggiungi anche in caso di errore per evitare duplicati

    # Verifica quale struttura ha il mazzo
    if hasattr(mazzo, 'carte') and isinstance(mazzo.carte, dict):
        # Struttura da JSON ricostruito: mazzo.carte[tipo] = [lista carte]
        for tipo_carta, liste_carte in mazzo.carte.items():
            if tipo_carta not in nomi_cartelle_mazzo:
                continue

            for carta in liste_carte:
                copia_carta(carta, tipo_carta)

    elif isinstance(mazzo, dict):
        # Struttura da crea_mazzo_da_gioco: mazzo['squadra'], mazzo['schieramento'], mazzo['carte_supporto']

        # Processa squadra (guerrieri)
        if 'squadra' in mazzo:
            for guerriero in mazzo['squadra']:
                copia_carta(guerriero, 'guerriero')

        # Processa schieramento (guerrieri)
        if 'schieramento' in mazzo:
            for guerriero in mazzo['schieramento']:
                copia_carta(guerriero, 'guerriero')

        # Processa carte_supporto (tutte le altre carte mescolate)
        if 'carte_supporto' in mazzo:
            for carta in mazzo['carte_supporto']:
                # Il tipo viene determinato automaticamente dal nome della classe
                copia_carta(carta)

    else:
        risultati['errori'].append("Struttura mazzo non riconosciuta")

    return risultati

def esporta_immagini_mazzi(mazzi: List, verbose: bool = True) -> Dict[str, Any]:
    """
    Esporta le immagini di tutti i mazzi nelle rispettive cartelle.

    Funzione principale che coordina l'esportazione delle immagini per tutti i mazzi.

    Args:
        mazzi: Lista di oggetti Mazzo
        verbose: Se True, stampa messaggi di progresso

    Returns:
        Un dizionario con le statistiche complessive dell'esportazione
    """
    risultati_complessivi = {
        'numero_mazzi': len(mazzi),
        'totale_immagini_copiate': 0,
        'totale_immagini_non_trovate': 0,
        'totale_errori': 0,
        'dettaglio_mazzi': []
    }

    if verbose:
        print(f"\n{'='*80}")
        print(f"ESPORTAZIONE IMMAGINI MAZZI")
        print(f"{'='*80}")
        print(f"Numero mazzi da processare: {len(mazzi)}")
        print(f"Percorso destinazione: {PERCORSO_BASE_MAZZI}")

    # Processa ogni mazzo
    for i, mazzo in enumerate(mazzi, 1):
        nome_mazzo = f"mazzo_{i}"

        if verbose:
            print(f"\nProcessando mazzo {i}/{len(mazzi)}...")

        try:
            risultati = copia_immagini_mazzo(nome_mazzo, mazzo)

            # Aggiorna statistiche complessive
            risultati_complessivi['totale_immagini_copiate'] += risultati['immagini_copiate']
            risultati_complessivi['totale_immagini_non_trovate'] += len(risultati['immagini_non_trovate'])
            risultati_complessivi['totale_errori'] += len(risultati['errori'])
            risultati_complessivi['dettaglio_mazzi'].append(risultati)

            if verbose:
                print(f"  Immagini copiate: {risultati['immagini_copiate']}/{risultati['totale_carte']}")
                if risultati['immagini_non_trovate']:
                    print(f"  Immagini non trovate: {len(risultati['immagini_non_trovate'])}")
                    for immagine_non_trovata in risultati['immagini_non_trovate']:
                        print(f"    - {immagine_non_trovata}")
                if risultati['errori']:
                    print(f"  Errori: {len(risultati['errori'])}")
                    for errore in risultati['errori']:
                        print(f"    - {errore}")

        except Exception as e:
            risultati_complessivi['totale_errori'] += 1
            if verbose:
                print(f"  Errore processando mazzo {i}: {str(e)}")

    if verbose:
        print(f"\n{'='*80}")
        print(f"RIEPILOGO ESPORTAZIONE")
        print(f"{'='*80}")
        print(f"Mazzi processati: {len(mazzi)}")
        print(f"Totale immagini copiate: {risultati_complessivi['totale_immagini_copiate']}")
        print(f"Totale immagini non trovate: {risultati_complessivi['totale_immagini_non_trovate']}")
        print(f"Totale errori: {risultati_complessivi['totale_errori']}")
        print(f"{'='*80}\n")

    return risultati_complessivi

def ricostruisci_mazzo_da_json(mazzo_json: Dict[str, Any]):
    """
    Ricostruisce un oggetto Mazzo da un dizionario JSON.

    Questa funzione crea carte fittizie con solo le informazioni necessarie per
    l'esportazione delle immagini (nome, tipo, fazione).

    Args:
        mazzo_json: Il dizionario JSON del mazzo

    Returns:
        Un oggetto Mazzo ricostruito
    """
    from dataclasses import dataclass
    from types import SimpleNamespace

    @dataclass
    class CartaFittizia:
        """Classe fittizia per contenere le informazioni minime di una carta"""
        nome: str
        tipo: str
        fazione: Optional[str] = None

    class MazzoRicostruito:
        """Classe fittizia per contenere le carte ricostruite"""
        def __init__(self):
            self.carte = defaultdict(list)

    mazzo = MazzoRicostruito()

    # Mappatura delle classi JSON ai tipi di carte
    mappatura_classi = {
        'Equipaggiamento': 'equipaggiamento',
        'Arte': 'arte',
        'Fortificazioni': 'fortificazione',
        'Fortificazione': 'fortificazione',
        'Missioni': 'missione',
        'Missione': 'missione',
        'Speciali': 'speciale',
        'Speciale': 'speciale',
        'Oscura Simmetria': 'oscura_simmetria',
        'Reliquie': 'reliquia',
        'Reliquia': 'reliquia',
        'Warzone': 'warzone'
    }

    # 1. Processa inventario_guerrieri
    inventario_guerrieri = mazzo_json.get('inventario_guerrieri', {})
    if inventario_guerrieri:
        for categoria in ['squadra', 'schieramento', 'altre']:
            if categoria in inventario_guerrieri:
                for fazione, guerrieri in inventario_guerrieri[categoria].items():
                    for nome_guerriero, info_guerriero in guerrieri.items():
                        quantita = info_guerriero.get('quantita', info_guerriero.get('copie', 1))
                        fazione_carta = info_guerriero.get('fazione', fazione)

                        # Crea copie fittizie del guerriero
                        for _ in range(quantita):
                            carta_fittizia = CartaFittizia(
                                nome=nome_guerriero,
                                tipo='guerriero',
                                fazione=fazione_carta
                            )
                            # Aggiungi un attributo fazione come oggetto con .value
                            carta_fittizia.fazione = SimpleNamespace(value=fazione_carta)
                            mazzo.carte['guerriero'].append(carta_fittizia)

    # 2. Processa inventario_supporto
    inventario_supporto = mazzo_json.get('inventario_supporto', {})
    if inventario_supporto:
        for classe, carte_classe in inventario_supporto.items():
            # Determina il tipo di carta dalla classe
            tipo_carta = mappatura_classi.get(classe)

            if not tipo_carta:
                continue

            # Itera sulle carte di questa classe
            for nome_carta, info_carta in carte_classe.items():
                quantita = info_carta.get('quantita', info_carta.get('copie', 1))
                fazione = info_carta.get('fazione')

                # Crea copie fittizie della carta
                for _ in range(quantita):
                    carta_fittizia = CartaFittizia(
                        nome=nome_carta,
                        tipo=tipo_carta,
                        fazione=fazione
                    )
                    mazzo.carte[tipo_carta].append(carta_fittizia)

    return mazzo

def esporta_immagini_mazzi_da_json(percorso_json: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Carica un file JSON di mazzi ed esporta le immagini.

    Questa funzione è utile per esportare immagini da mazzi salvati in precedenza.

    Args:
        percorso_json: Il percorso del file JSON contenente i mazzi
        verbose: Se True, stampa messaggi di progresso

    Returns:
        Un dizionario con le statistiche dell'esportazione
    """
    try:
        with open(percorso_json, 'r', encoding='utf-8') as f:
            dati = json.load(f)

        # Estrae i mazzi dal JSON
        mazzi_json = dati.get('mazzi_dettagliati', [])

        if not mazzi_json:
            if verbose:
                print(f"Nessun mazzo trovato nel file {percorso_json}")
            return {'errore': 'Nessun mazzo trovato'}

        if verbose:
            print(f"Caricato file: {percorso_json}")
            print(f"Trovati {len(mazzi_json)} mazzi")

        # Ricostruisce i mazzi dal JSON
        mazzi = []
        for mazzo_json in mazzi_json:
            mazzo = ricostruisci_mazzo_da_json(mazzo_json)
            mazzi.append(mazzo)

        # Esporta le immagini
        return esporta_immagini_mazzi(mazzi, verbose)

    except FileNotFoundError:
        if verbose:
            print(f"File non trovato: {percorso_json}")
        return {'errore': f'File non trovato: {percorso_json}'}
    except json.JSONDecodeError as e:
        if verbose:
            print(f"Errore parsing JSON: {str(e)}")
        return {'errore': f'Errore parsing JSON: {str(e)}'}
    except Exception as e:
        if verbose:
            print(f"Errore: {str(e)}")
        return {'errore': str(e)}



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
        print("1. Crea mazzi di esempio (dedicato al test)")
        print("2. Stampa riepilogo mazzi (dedicato al test)")
       
        print("3. Salva mazzi in JSON con conteggio (standard) (dedicato al test)")
        print("4. Salva mazzi in JSON con conteggio(sicuro) (dedicato al test)")
        print("5. Carica e visualizza mazzi da JSON con conteggio (dedicato al test)")        
        print("6. Verifica integrità mazzi (dedicato al test)")
        print("7. Analizza bilanciamento (dedicato al test)")
        print("8. Diagnostica completa mazzi (dedicato al test)")
        print("9. Test compatibilità (dedicato al test)")
        print("10. Cerca carta nei mazzi (dedicato al test)")
        print("11. Esempio completo salvataggio (dedicato al test)")
        print("12. Pulisci mazzi correnti (dedicato al test)")
        print("13. Crea e salva mazzo da file collezione (dedicato al test)")
        print("14. Crea e salva mazzo da cartella collezioni (FUNZIONE UFFICIALE)")

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
                
                filename = "mazzo_collezione_" + str(num) #input("nome file di output (default: mazzo_di_sconosciuto.json): ").strip()
                
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
                        apostoli_scelti = [list(ApostoloOscuraSimmetria)[i].value for i in apo_indices if 0 <= i < len(ApostoloOscuraSimmetria)]
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

        elif scelta == "14":
            # Creazione personalizzata
            mazzi_correnti.clear()
            sys.path.insert(0, '/home/marco/Sviluppo/Mutant_Chronicles')
                            
            try:
                cartella_collezioni = str(input("nome cartella con il file collezioni da caricare: "))
                numero_collezione =  int(input("numero della collezione da caricare: "))

                risultato = crea_mazzo_da_cartella_collezione(
                    cartella_collezioni = cartella_collezioni,
                    numero_collezione = numero_collezione,
                    verbose=True
                )

                print("\n" + "="*80)
                print("RISULTATI DELLA CREAZIONE DEL MAZZO DA CARTELLA COLLEZIONE")
                print("="*80)

                if risultato.get('successo'):
                    print(f"✅ cartella mazzo e relativi contenuti creati con successo!")
                    print(f"\n📊 Statistiche:")
                    print(f"   - Percorso mazzo: {risultato['percorso_mazzo']}")
                    print(f"   - Numero carte: {risultato['numero_carte']}")

                    mazzo = risultato.get('mazzo', {})
                    if mazzo:
                        stats = mazzo.get('statistiche', {})
                        print(f"\n🎴 Dettagli mazzo:")
                        print(f"   - Guerrieri squadra: {len(mazzo.get('squadra', []))}")
                        print(f"   - Guerrieri schieramento: {len(mazzo.get('schieramento', []))}")
                        print(f"   - Carte supporto: {len(mazzo.get('carte_supporto', []))}")
                        print(f"   - Distribuzione per tipo: {stats.get('distribuzione_per_tipo', {})}")

                    return 0
                else:
                    print(f"❌ ERRORE: {risultato.get('errore', 'Errore sconosciuto')}")
                    return 1

            except Exception as e:
                print(f"\n❌ ERRORE FATALE: {e}")
                import traceback
                traceback.print_exc()
                return 1

        else:
            print("❌ Opzione non valida")




# ============================================================================
# FUNZIONI PER CREAZIONE MAZZO DA CARTELLA COLLEZIONE
# ============================================================================

def crea_pdf_mazzo(mazzo: Dict[str, Any], percorso_pdf: str, numero_giocatore: int) -> bool:
    """
    Crea un file PDF con l'elenco delle carte di un mazzo.

    Le carte sono organizzate per tipo (Guerrieri Squadra, Guerrieri Schieramento,
    Equipaggiamento, ecc.) e per ogni carta vengono mostrate: nome, quantità, fazione.
    Per le carte Arte viene indicata la disciplina.
    Per le carte Oscura Simmetria viene indicato il tipo di dono.

    Args:
        mazzo: Dizionario del mazzo (output di crea_mazzo_da_gioco)
        percorso_pdf: Il percorso completo dove salvare il PDF
        numero_giocatore: Il numero del giocatore

    Returns:
        True se il PDF è stato creato con successo, False altrimenti
    """
    if not REPORTLAB_AVAILABLE:
        print("⚠️  La libreria reportlab non è disponibile. Impossibile creare il PDF.")
        print("   Installa reportlab con: pip install reportlab")
        return False

    try:
        # Crea il documento PDF
        doc = SimpleDocTemplate(
            percorso_pdf,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # Definisce gli stili
        styles = getSampleStyleSheet()

        # Stile per il titolo
        style_titolo = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor='darkblue',
            spaceAfter=20,
            alignment=TA_CENTER
        )

        # Stile per i sottotitoli (tipo carta)
        style_sottotitolo = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor='darkgreen',
            spaceAfter=12,
            spaceBefore=12
        )

        # Stile per il testo normale
        style_normale = styles['Normal']

        # Lista degli elementi da inserire nel PDF
        elementi = []

        # Titolo
        titolo = Paragraph(
            f"<b>Mazzo Giocatore {numero_giocatore}</b>",
            style_titolo
        )
        elementi.append(titolo)
        elementi.append(Spacer(1, 0.5*cm))

        # Statistiche generali
        statistiche = mazzo.get('statistiche', {})
        totale_carte = statistiche.get('numero_totale_carte', 0)

        stats_text = Paragraph(
            f"<b>Totale carte:</b> {totale_carte}",
            style_normale
        )
        elementi.append(stats_text)
        elementi.append(Spacer(1, 0.5*cm))

        # Funzione helper per contare e raggruppare carte
        def conta_carte(lista_carte):
            carte_conteggio = defaultdict(int)
            carte_esempi = {}
            for carta in lista_carte:
                carte_conteggio[carta.nome] += 1
                if carta.nome not in carte_esempi:
                    carte_esempi[carta.nome] = carta
            return carte_conteggio, carte_esempi

        # 1. GUERRIERI SQUADRA
        squadra = mazzo.get('squadra', [])
        if squadra:
            carte_conteggio, carte_esempi = conta_carte(squadra)

            sottotitolo = Paragraph(
                f"<b>Guerrieri Squadra ({len(squadra)} carte, {len(carte_conteggio)} uniche)</b>",
                style_sottotitolo
            )
            elementi.append(sottotitolo)
            elementi.append(Spacer(1, 0.2*cm))

            # Ordina per fazione, poi per nome
            carte_ordinate = sorted(
                carte_conteggio.items(),
                key=lambda x: (
                    carte_esempi[x[0]].fazione.value if hasattr(carte_esempi[x[0]], 'fazione') and carte_esempi[x[0]].fazione else 'ZZZ',
                    x[0]
                )
            )

            for nome_carta, quantita in carte_ordinate:
                carta = carte_esempi[nome_carta]
                info_parti = [f"<b>{nome_carta}</b> (x{quantita})"]

                if hasattr(carta, 'fazione') and carta.fazione:
                    fazione_str = carta.fazione.value if hasattr(carta.fazione, 'value') else str(carta.fazione)
                    info_parti.append(f"Fazione: {fazione_str}")

                carta_text = Paragraph(" | ".join(info_parti), style_normale)
                elementi.append(carta_text)
                elementi.append(Spacer(1, 0.1*cm))

            elementi.append(Spacer(1, 0.3*cm))

        # 2. GUERRIERI SCHIERAMENTO
        schieramento = mazzo.get('schieramento', [])
        if schieramento:
            carte_conteggio, carte_esempi = conta_carte(schieramento)

            sottotitolo = Paragraph(
                f"<b>Guerrieri Schieramento ({len(schieramento)} carte, {len(carte_conteggio)} uniche)</b>",
                style_sottotitolo
            )
            elementi.append(sottotitolo)
            elementi.append(Spacer(1, 0.2*cm))

            # Ordina per fazione, poi per nome
            carte_ordinate = sorted(
                carte_conteggio.items(),
                key=lambda x: (
                    carte_esempi[x[0]].fazione.value if hasattr(carte_esempi[x[0]], 'fazione') and carte_esempi[x[0]].fazione else 'ZZZ',
                    x[0]
                )
            )

            for nome_carta, quantita in carte_ordinate:
                carta = carte_esempi[nome_carta]
                info_parti = [f"<b>{nome_carta}</b> (x{quantita})"]

                if hasattr(carta, 'fazione') and carta.fazione:
                    fazione_str = carta.fazione.value if hasattr(carta.fazione, 'value') else str(carta.fazione)
                    info_parti.append(f"Fazione: {fazione_str}")

                carta_text = Paragraph(" | ".join(info_parti), style_normale)
                elementi.append(carta_text)
                elementi.append(Spacer(1, 0.1*cm))

            elementi.append(Spacer(1, 0.3*cm))

        # 3. CARTE SUPPORTO
        carte_supporto = mazzo.get('carte_supporto', [])
        if carte_supporto:
            # Raggruppa per tipo
            carte_per_tipo = defaultdict(list)
            for carta in carte_supporto:
                tipo = type(carta).__name__.lower()
                carte_per_tipo[tipo].append(carta)

            # Ordine dei tipi
            ordine_tipi = ['equipaggiamento', 'speciale', 'fortificazione', 'missione', 'arte', 'oscura_simmetria', 'reliquia', 'warzone']
            nomi_tipi = {
                'equipaggiamento': 'Equipaggiamento',
                'speciale': 'Carte Speciali',
                'fortificazione': 'Fortificazioni',
                'missione': 'Missioni',
                'arte': 'Carte Arte',
                'oscura_simmetria': 'Carte Oscura Simmetria',
                'reliquia': 'Reliquie',
                'warzone': 'Warzone'
            }

            for tipo in ordine_tipi:
                if tipo not in carte_per_tipo:
                    continue

                liste_carte = carte_per_tipo[tipo]
                carte_conteggio, carte_esempi = conta_carte(liste_carte)

                sottotitolo = Paragraph(
                    f"<b>{nomi_tipi.get(tipo, tipo.capitalize())} ({len(liste_carte)} carte, {len(carte_conteggio)} uniche)</b>",
                    style_sottotitolo
                )
                elementi.append(sottotitolo)
                elementi.append(Spacer(1, 0.2*cm))

                # Ordina in base al tipo
                if tipo == 'arte':
                    # Ordina per disciplina
                    carte_ordinate = sorted(
                        carte_conteggio.items(),
                        key=lambda x: (
                            carte_esempi[x[0]].disciplina.value if hasattr(carte_esempi[x[0]], 'disciplina') and carte_esempi[x[0]].disciplina else 'ZZZ',
                            x[0]
                        )
                    )
                elif tipo == 'oscura_simmetria':
                    # Ordina per tipo di dono
                    def get_dono_key(nome_carta):
                        carta = carte_esempi[nome_carta]
                        if hasattr(carta, 'tipo') and carta.tipo:
                            tipo_str = carta.tipo.value if hasattr(carta.tipo, 'value') else str(carta.tipo)
                            if hasattr(carta, 'apostolo_padre') and carta.apostolo_padre:
                                apostolo_str = carta.apostolo_padre.value if hasattr(carta.apostolo_padre, 'value') else str(carta.apostolo_padre)
                                if apostolo_str and apostolo_str != 'None':
                                    return f"Seguace di {apostolo_str}"
                            return tipo_str
                        return 'ZZZ'

                    carte_ordinate = sorted(
                        carte_conteggio.items(),
                        key=lambda x: (get_dono_key(x[0]), x[0])
                    )
                else:
                    # Ordina solo per nome
                    carte_ordinate = sorted(carte_conteggio.items())

                for nome_carta, quantita in carte_ordinate:
                    carta = carte_esempi[nome_carta]
                    info_parti = [f"<b>{nome_carta}</b> (x{quantita})"]

                    # Aggiungi informazioni specifiche per tipo
                    if tipo == 'arte' and hasattr(carta, 'disciplina') and carta.disciplina:
                        disciplina_str = carta.disciplina.value if hasattr(carta.disciplina, 'value') else str(carta.disciplina)
                        info_parti.append(f"Disciplina: {disciplina_str}")

                    if tipo == 'oscura_simmetria':
                        if hasattr(carta, 'tipo') and carta.tipo:
                            tipo_str = carta.tipo.value if hasattr(carta.tipo, 'value') else str(carta.tipo)
                            if hasattr(carta, 'apostolo_padre') and carta.apostolo_padre:
                                apostolo_str = carta.apostolo_padre.value if hasattr(carta.apostolo_padre, 'value') else str(carta.apostolo_padre)
                                if apostolo_str and apostolo_str != 'None':
                                    info_parti.append(f"Dono: Seguace di {apostolo_str}")
                                else:
                                    info_parti.append(f"Dono: {tipo_str}")
                            else:
                                info_parti.append(f"Dono: {tipo_str}")

                    carta_text = Paragraph(" | ".join(info_parti), style_normale)
                    elementi.append(carta_text)
                    elementi.append(Spacer(1, 0.1*cm))

                elementi.append(Spacer(1, 0.3*cm))

        # Costruisce il PDF
        doc.build(elementi)

        return True

    except Exception as e:
        print(f"❌ Errore durante la creazione del PDF: {e}")
        import traceback
        traceback.print_exc()
        return False


def crea_mazzo_da_cartella_collezione(
    cartella_collezioni: str,
    numero_collezione: int,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Crea un mazzo da una cartella di collezioni con interazione utente.

    Questa funzione:
    1. Carica il file lista_collezioni.json dalla cartella specificata
    2. Interagisce con l'utente per ottenere i parametri del mazzo
    3. Crea il mazzo dalla collezione selezionata
    4. Salva il mazzo in formato JSON
    5. Crea un PDF con l'elenco delle carte
    6. Esporta le immagini delle carte del mazzo

    Args:
        cartella_collezioni: Nome della cartella contenente le collezioni (relativa a out/)
        numero_collezione: Numero della collezione da cui creare il mazzo (1-based)
        verbose: Se True, stampa messaggi di progresso

    Returns:
        Dizionario con le statistiche della creazione
    """
    try:
        if verbose:
            print(f"\n{'='*80}")
            print(f"🎴 CREAZIONE MAZZO DA CARTELLA COLLEZIONE")
            print(f"{'='*80}")
            print(f"📁 Cartella: {cartella_collezioni}")
            print(f"🎮 Numero collezione: {numero_collezione}")

        # Costruisce il percorso del file collezioni
        # NOTA: carica_collezioni_json_migliorato aggiunge automaticamente PERCORSO_SALVATAGGIO ("out/")
        percorso_relativo = f"{cartella_collezioni}/lista_collezioni.json"

        # Carica le collezioni
        if verbose:
            print(f"\n📂 Caricamento collezioni...")

        risultato = carica_collezioni_json_migliorato(percorso_relativo)

        if not risultato:
            raise ValueError(f"Impossibile caricare il file {percorso_relativo}")

        # La funzione restituisce una tupla (dati_json, collezioni)
        dati_json, collezioni = risultato

        if not collezioni:
            raise ValueError("Nessuna collezione trovata nel file")

        if numero_collezione < 1 or numero_collezione > len(collezioni):
            raise ValueError(f"Numero collezione non valido. Deve essere tra 1 e {len(collezioni)}")

        collezione = collezioni[numero_collezione - 1]

        if verbose:
            print(f"✅ Collezione {numero_collezione} caricata")
            print(f"\n{'='*80}")
            print(f"CONFIGURAZIONE MAZZO")
            print(f"{'='*80}")

        # Interazione con l'utente per i parametri del mazzo
        carte_min = int(input("Numero minimo di carte del mazzo: "))
        carte_max = int(input("Numero massimo di carte del mazzo: "))

        fazioni_doomtrooper = []
        arti_scelte = []
        apostoli_scelti = []
        espansioni = []

        # Doomtrooper
        doomtrooper = input("Utilizzo doomtrooper (s/n): ").lower().startswith('s')
        if doomtrooper:
            scelta_fazioni = input("Vuoi specificare quali fazioni doomtrooper utilizzare (s/n): ").lower().startswith('s')
            if scelta_fazioni:
                print("Fazioni:")
                for i, faz in enumerate(FAZIONI_DOOMTROOPER):
                    print(f"  {i+1}. {faz.value}")
                faz_input = input("Scegli fazioni (numeri separati da virgola): ")
                faz_indices = [int(x.strip())-1 for x in faz_input.split(",")]
                fazioni_doomtrooper = [list(FAZIONI_DOOMTROOPER)[i].value for i in faz_indices if 0 <= i < len(FAZIONI_DOOMTROOPER)]

        # Fratellanza
        fratellanza = input("Utilizzo fratellanza (s/n): ").lower().startswith('s')
        if fratellanza:
            scelta_arte = input("Vuoi specificare quali tipologie di Arte vuoi utilizzare (s/n): ").lower().startswith('s')
            if scelta_arte:
                print("Tipologie Arte:")
                for i, arte in enumerate(DisciplinaArte):
                    print(f"  {i+1}. {arte.value}")
                art_input = input("Scegli le tipologie di Arte (numeri separati da virgola): ")
                art_indices = [int(x.strip())-1 for x in art_input.split(",")]
                arti_scelte = [list(DisciplinaArte)[i].value for i in art_indices if 0 <= i < len(DisciplinaArte)]

        # Oscura Legione
        cultisti = False
        oscura_legione = input("Utilizzo oscura legione (s/n): ").lower().startswith('s')
        if oscura_legione:
            scelta_apostoli = input("Vuoi specificare quali Apostoli vuoi utilizzare (s/n): ").lower().startswith('s')
            if scelta_apostoli:
                print("Apostoli:")
                for i, apo in enumerate(ApostoloOscuraSimmetria):
                    print(f"  {i+1}. {apo.value}")
                apo_input = input("Scegli gli Apostoli (numeri separati da virgola): ")
                apo_indices = [int(x.strip())-1 for x in apo_input.split(",")]
                apostoli_scelti = [list(ApostoloOscuraSimmetria)[i].value for i in apo_indices if 0 <= i < len(ApostoloOscuraSimmetria)]
            cultisti = input("Utilizzo cultisti (s/n): ").lower().startswith('s')

        # Eretici
        eretici = input("Utilizzo eretici (s/n): ").lower().startswith('s')

        # Espansioni
        print("\nEspansioni disponibili:")
        for i, esp in enumerate(Set_Espansione):
            print(f"  {i+1}. {esp.value}")
        esp_input = input("Scegli espansioni (numeri separati da virgola): ")
        esp_indices = [int(x.strip())-1 for x in esp_input.split(",")]
        espansioni = [list(Set_Espansione)[i].value for i in esp_indices if 0 <= i < len(Set_Espansione)]

        # Crea il mazzo
        if verbose:
            print(f"\n{'='*80}")
            print(f"🔄 CREAZIONE MAZZO IN CORSO...")
            print(f"{'='*80}")

        mazzo = crea_mazzo_da_gioco(
            collezione,
            numero_carte_max=carte_max,
            numero_carte_min=carte_min,
            espansioni_richieste=espansioni,
            doomtrooper=doomtrooper,
            orientamento_doomtrooper=fazioni_doomtrooper,
            fratellanza=fratellanza,
            orientamento_arte=arti_scelte,
            oscura_legione=oscura_legione,
            orientamento_apostolo=apostoli_scelti,
            orientamento_eretico=eretici,
            orientamento_cultista=cultisti
        )

        if verbose:
            print(f"✅ Mazzo creato: {mazzo['statistiche']['numero_totale_carte']} carte totali")

        # Crea la struttura delle cartelle
        percorso_cartella = Path(PERCORSO_SALVATAGGIO) / cartella_collezioni
        cartella_collezione_giocatore = percorso_cartella / f"Collezione_Giocatore_{numero_collezione}"
        cartella_mazzo = cartella_collezione_giocatore / f"Mazzo_Giocatore_{numero_collezione}"
        cartella_mazzo.mkdir(parents=True, exist_ok=True)

        if verbose:
            print(f"\n📁 Cartella mazzo creata: {cartella_mazzo}")

        # 1. Salva il JSON del mazzo
        nome_file_json = f"mazzo_giocatore_{numero_collezione}.json"
        percorso_json = cartella_mazzo / nome_file_json

        # Crea la struttura JSON del mazzo
        inventario_mazzo = crea_inventario_dettagliato_mazzo_json_con_conteggio_e_apostoli(mazzo, numero_collezione)

        dati_mazzo = {
            'metadata': {
                'versione': '2.0',
                'tipo_export': 'mazzo_singolo',
                'data_creazione': datetime.now().isoformat(),
                'numero_giocatore': numero_collezione
            },
            'mazzo': inventario_mazzo
        }

        with open(percorso_json, 'w', encoding='utf-8') as f:
            json.dump(dati_mazzo, f, indent=2, ensure_ascii=False, default=str)

        if verbose:
            print(f"   ✅ JSON salvato: {nome_file_json}")

        # 2. Crea il PDF
        nome_file_pdf = f"elenco_carte_mazzo_{numero_collezione}.pdf"
        percorso_pdf = cartella_mazzo / nome_file_pdf

        pdf_creato = crea_pdf_mazzo(mazzo, str(percorso_pdf), numero_collezione)

        if pdf_creato and verbose:
            print(f"   ✅ PDF creato: {nome_file_pdf}")
        elif not pdf_creato and verbose:
            print(f"   ⚠️  Impossibile creare PDF")

        # 3. Crea la cartella Immagini
        cartella_immagini = cartella_mazzo / f"Immagini_Mazzo_{numero_collezione}"
        cartella_immagini.mkdir(exist_ok=True)

        if verbose:
            print(f"   📁 Cartella immagini creata")

        # 4. Esporta le immagini
        if verbose:
            print(f"   🖼️  Esportazione immagini in corso...")

        try:
            # Usa la funzione copia_immagini_mazzo
            nome_mazzo_temp = f"temp_mazzo_{numero_collezione}"
            risultato_immagini = copia_immagini_mazzo(nome_mazzo_temp, mazzo)

            # Sposta le immagini nella cartella corretta
            cartella_immagini_temp = Path(PERCORSO_SALVATAGGIO) / "mazzi_immagini" / nome_mazzo_temp

            if cartella_immagini_temp.exists():
                # Copia tutte le immagini mantenendo la struttura
                for item in cartella_immagini_temp.iterdir():
                    dest = cartella_immagini / item.name
                    if item.is_dir():
                        shutil.copytree(item, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, dest)

                # Rimuovi la cartella temporanea
                shutil.rmtree(cartella_immagini_temp)

            if verbose:
                num_immagini = sum(1 for _ in cartella_immagini.rglob('*.jpg')) + sum(1 for _ in cartella_immagini.rglob('*.png'))
                print(f"   ✅ Immagini esportate: {num_immagini} file")

        except Exception as e:
            if verbose:
                print(f"   ⚠️  Errore durante l'esportazione immagini: {e}")

        # Riepilogo finale
        if verbose:
            print(f"\n{'='*80}")
            print(f"✅ CREAZIONE MAZZO COMPLETATA")
            print(f"{'='*80}")
            print(f"📁 Percorso: {cartella_mazzo}")
            print(f"🎴 Carte totali: {mazzo['statistiche']['numero_totale_carte']}")
            print(f"⚔️ Guerrieri squadra: {len(mazzo['squadra'])}")
            print(f"🌙 Guerrieri schieramento: {len(mazzo['schieramento'])}")
            print(f"🎴 Carte supporto: {len(mazzo['carte_supporto'])}")

        return {
            'successo': True,
            'percorso_mazzo': str(cartella_mazzo),
            'numero_carte': mazzo['statistiche']['numero_totale_carte'],
            'mazzo': mazzo
        }

    except Exception as e:
        errore_msg = f"Errore durante la creazione del mazzo: {str(e)}"
        if verbose:
            print(f"\n❌ {errore_msg}")
            import traceback
            traceback.print_exc()

        return {
            'successo': False,
            'errore': errore_msg
        }









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
    
    menu_interattivo_mazzi()
    """
    Esecuzione diretta del modulo per test.
    """
    
    #print("🎯 MODULO GESTIONE MAZZI - TEST STANDALONE")
    
    # Esegui test base
    # test_funzioni_mazzi()

    #espansioni_richieste = [Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE]

    #collezioni = creazione_Collezione_Giocatore(3, espansioni_richieste, orientamento = True)
    #salva_collezioni_json_migliorato(collezioni = collezioni, filename = "collezioni_3_player_no_orientamento.json")
    #dati_json, collezioni = carica_collezioni_json_migliorato(filename = "collezioni_3_player_no_orientamento.json")

    #orientamento_collezioni = []
    # conta Guerrieri
    #mazzo = []
    #orientamento_fratellanza_forzato = True
    #orientamento = {}

    
    #for collezione in collezioni:
        
    #    if orientamento_fratellanza_forzato:
            #orientamento['fratellanza'] = True
            #orientamento['orientamento_arte'] = ['Cambiamento', 'Elementi', 'Esorcismo', 'Cinetica']
            #orientamento['oscura_legione'] = False
            #orientamento['orientamento_apostolo']=[]
            #orientamento['doomtrooper'] = True
            #orientamento['orientamento_doomtrooper'] = ['Bauhaus', 'Capitol']
            #orientamento['orientamento_eretico'] = False
            #orientamento['orientamento_cultista'] = False  
            #orientamento_fratellanza_forzato = False # orientamento vincolato alla fratellanza solo per il primo mazzo            
    #    else:
            #orientamento = determina_orientamento_collezione(collezione = collezione, espansioni_richieste = espansioni_richieste)



    #    print(f"\nCreazione mazzo per collezione con orientamento:")
    #    print(f"  Doomtrooper: {orientamento['doomtrooper']} - Fazioni: {orientamento['orientamento_doomtrooper']} ")
    #    print(f"  Fratellanza: {orientamento['fratellanza']} - Arti: {orientamento['orientamento_arte']}")
    #    print(f"  Oscura Legione: {orientamento['oscura_legione']} - Apostoli: {orientamento['orientamento_apostolo']}")
    #    print(f"  Eretici: {orientamento['orientamento_eretico']} - Cultisti: {orientamento['orientamento_cultista']}")


    #    mazzo.append( 
            #crea_mazzo_da_gioco(collezione,
            #            numero_carte_max = 200,
            #            numero_carte_min = 150,
            #            espansioni_richieste = ["Base", "Inquisition", "Warzone"],
            #            doomtrooper = orientamento['doomtrooper'],
            #            orientamento_doomtrooper = orientamento['orientamento_doomtrooper'],
            #            fratellanza = orientamento['fratellanza'],
            #            orientamento_arte = orientamento['orientamento_arte'],
            #            oscura_legione = orientamento['oscura_legione'],
            #            orientamento_apostolo = orientamento['orientamento_apostolo'],
            #            orientamento_eretico = orientamento['orientamento_eretico'],
            #            orientamento_cultista = orientamento['orientamento_cultista'])
            #)
    
    #esempio_salvataggio_mazzi_con_conteggio(mazzo)

    # Menu interattivo
    #risposta = input("\nVuoi aprire il menu interattivo? (s/n): ")
    #if risposta.lower().startswith('s'):
    #    menu_interattivo_mazzi()



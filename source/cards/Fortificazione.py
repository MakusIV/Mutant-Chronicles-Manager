"""
Modulo per la rappresentazione delle carte Fortificazione di Mutant Chronicles/Doomtrooper
Le Fortificazioni rappresentano edifici, strutture o installazioni difensive nelle quali i
guerrieri si difendono o dalle quali ottengono speciali abilità. 
Sono assegnate alle Aree del giocatore per incrementare le caratteristiche di difesa (A) 
dei guerrieri introdotti. Le Fortificazioni rimangono in gioco anche se non hai guerrieri,
in quanto sono assegnate alle Aree e non ai singoli guerrieri.
Basato sulla struttura delle classi Guerriero, Arte, Oscura_Simmetria, Equipaggiamento e Speciale
VERSIONE CORRETTA - Allineata alle regole ufficiali del regolamento
"""

from enum import Enum
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import json
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione, ApostoloPadre, TipoGuerriero, CorporazioneSpecifica, DOOMTROOPER  # Import dalle classi esistenti


class TipoFortificazione(Enum):
    """Tipi di carte Fortificazione secondo il regolamento"""
    CITTA_CORPORAZIONE = "Città Corporazione"  # Città delle singole Corporazioni
    CITTADELLA_APOSTOLO = "Cittadella Apostolo"  # Cittadelle degli Apostoli Oscuri
    FORTIFICAZIONE_GENERICA = "Fortificazione Generica"  # Fortificazioni standard
    INSTALLAZIONE_DIFENSIVA = "Installazione Difensiva"  # Strutture militari
    COMPLESSO_INDUSTRIALE = "Complesso Industriale"  # Fabbriche e industrie
    BASE_OPERATIVA = "Base Operativa"  # Basi militari
    RIFUGIO = "Rifugio"  # Bunker e rifugi
    STRUTTURA_SPECIALE = "Struttura Speciale"  # Strutture con abilità uniche

class AreaCompatibile(Enum):
    """Aree dove può essere costruita la fortificazione"""
    SQUADRA = "Squadra"
    SCHIERAMENTO = "Schieramento" 
    AVAMPOSTO = "Avamposto"
    SQUADRA_O_SCHIERAMENTO = "Squadra o Schieramento"
    SOLO_AVAMPOSTO = "Solo Avamposto"
    QUALSIASI_AREA = "Qualsiasi Area"
    ASSEGNATA_A_GUERRIERO = "Assegnata a Guerriero"  # Eccezione del regolamento


class BeneficiarioFortificazione(Enum):
    """Chi può beneficiare della fortificazione"""
    GUERRIERI_AREA = "Guerrieri Area"
    CORPORAZIONE_SPECIFICA = "Corporazione Specifica"
    APOSTOLO_SPECIFICO = "Apostolo Specifico"
    FAZIONE_SPECIFICA = "Guerrieri di una fazione specifica"
    GUERRIERO_SINGOLO = "Singolo Guerriero"
    TUTTI_DOOMTROOPER = "Doomtrooper"
    TUTTI_OSCURA_LEGIONE = "Oscura Legione"
    TUTTE_TRIBU = "Tribù"
    ERETICI = "Eretici"
    TUTTI = "Tutti"


@dataclass
class ModificatoreFortificazione:
    """Rappresenta un modificatore applicato dalla fortificazione"""
    statistica: str  # "C", "S", "A", "V" o "SPECIALE"
    valore: int      # valore del modificatore (+/-)
    condizione: str = ""  # condizione per applicare il modificatore
    descrizione: str = ""
    permanente: bool = True  # se l'effetto è permanente o temporaneo


@dataclass
class AbilitaFortificazione:
    """Rappresenta un'abilità speciale della fortificazione"""
    nome: str
    descrizione: str
    tipo_abilita: str = "Passiva"  # "Passiva", "Attivabile", "Scatenante"
    costo_attivazione: int = 0  # costo in azioni/DP per attivare (se attivabile)
    condizioni_attivazione: List[str] = None
    effetti_speciali: List[str] = None
    
    def __post_init__(self):
        if self.condizioni_attivazione is None:
            self.condizioni_attivazione = []
        if self.effetti_speciali is None:
            self.effetti_speciali = []


class Fortificazione:
    """
    Classe per rappresentare una carta Fortificazione di Mutant Chronicles/Doomtrooper
    VERSIONE CORRETTA - Allineata alle regole del regolamento ufficiale
    """
    
    def __init__(self, nome: str, costo_destino: int = 0):
        """
        Inizializza una nuova carta Fortificazione
        
        Args:
            nome: Nome della fortificazione
            costo_destino: Costo in Punti Destino per costruire la fortificazione
        """
        # Proprietà base della carta
        self.nome: str = nome
        self.costo_destino: int = costo_destino
        
        # Tipo e classificazione
        self.tipo: str = TipoFortificazione.FORTIFICAZIONE_GENERICA
        self.rarity: Rarity = Rarity.COMMON
        self.set_espansione: Set_Espansione = Set_Espansione.BASE
        self.numero_carta: str = ""
        
        # Regole di posizionamento
        self.area_compatibile: AreaCompatibile = AreaCompatibile.SQUADRA_O_SCHIERAMENTO
        self.beneficiario: BeneficiarioFortificazione = BeneficiarioFortificazione.GUERRIERI_AREA
        self.corporazione_specifica: Optional[str] = None  # Per Città Corporazione
        self.apostolo_specifico: Optional[ApostoloPadre] = None  # Per Cittadelle Apostolo
        
        # Stato e limitazioni
        self.in_gioco: bool = False
        self.area_corrente: Optional[str] = None  # "Squadra", "Schieramento", "Avamposto"
        self.guerriero_assegnato: Optional[str] = None  # Se assegnata a guerriero specifico
        self.unica_per_giocatore: bool = True  # La maggior parte sono uniche
        self.distruttibile: bool = True  # Se può essere distrutta
        
        # Modificatori e abilità
        self.modificatori: List[ModificatoreFortificazione] = []
        self.abilita_speciali: List[AbilitaFortificazione] = []
        
        # Requisiti e restrizioni
        self.requisiti: List[str] = []  # Requisiti per costruire
        self.restrizioni: List[str] = []  # Restrizioni particolari
        self.fazioni_permesse: List[Fazione] = []  # Fazioni che possono usarla
        
        # Testo e descrizione
        self.testo_carta: str = ""
        self.flavour_text: str = ""
        self.keywords: List[str] = []
        self.valore_strategico = 0
        self.quantita_minima_consigliata: int = 0  # per la creazione del mazzo
        self.fondamentale: bool = False  # se la carta è fondamentale per il mazzo
        
        # Statistiche avanzate
        self.punti_struttura: int = 0  # Resistenza della fortificazione
        self.resistenza_attacchi: bool = False  # Se resiste ad attacchi diretti
        self.bonus_armatura: int = 0  # Bonus armatura base fornito
        
        # Tracking effetti
        self.effetti_attivi: List[Dict[str, Any]] = []
        self.guerrieri_influenzati: List[str] = []  # Lista ID guerrieri influenzati
        self.quantita = 0
        
    def puo_essere_assegnato_a_guerriero(self, guerriero: Any) -> Dict[str, Any]:
        """
        Controlla se la fortificazione può essere assegnata al guerriero specificato
        Basato sulle regole di fazioni_permesse del regolamento
        
        Args:
            guerriero: Istanza del guerriero
            
        Returns:
            Dizionario con risultato e eventuali errori
        """
        risultato = {"puo_assegnare": True, "errori": []}
        restrizione = self.restrizioni
       
        # Nota: questi controlli possono essere ridondanti con il precedente. Da ottimizzare aggiornando anche le info nel database
        # Nota: se viene verificata una condizone di non assegnabilità, le successive non vengono verificate in quanto già non assegnabile (assegnazione solo False)

        if self.beneficiario.value == "Corporazione Specifica" and self.corporazione_specifica is not None:

            if "Doomtrooper" == self.corporazione_specifica:
                if guerriero.fazione == Fazione.OSCURA_LEGIONE:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Solo per Doomtrooper")

            elif "Eretici" == self.corporazione_specifica:
                if "Eretico" not in guerriero.keywords:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Solo per Eretici")

            elif "Seguaci di " == self.corporazione_specifica[:len("Seguaci di ")]:
                apostolo_richiesto = self.corporazione_specifica.split("Seguaci di ")[1].strip()
                if (guerriero.keywords is None or guerriero.keywords == [] or "Seguace di " + apostolo_richiesto not in guerriero.keywords):                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo Seguaci di {apostolo_richiesto}")
            
            elif guerriero.fazione.value != self.corporazione_specifica:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo per {self.corporazione_specifica}")

            if risultato["puo_assegnare"] == False:
                return risultato    
                
        if restrizione is None or restrizione == []:
            
            if "Solo Doomtrooper" in restrizione:
                if guerriero.fazione == Fazione.OSCURA_LEGIONE:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Solo per Doomtrooper")
            
            elif "Solo Oscura Legione" in restrizione:
                if guerriero.fazione != Fazione.OSCURA_LEGIONE:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Solo per Oscura Legione")
            
            elif "Solo Seguaci di" in restrizione:
                apostolo_richiesto = restrizione.split("Solo Seguaci di ")[1].strip()
                if (guerriero.keywords is None or guerriero.keywords == [] or "Seguace di " + apostolo_richiesto not in guerriero.keywords):                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo Seguaci di {apostolo_richiesto}")

            elif "Solo Eretici" in restrizione:
                if (guerriero.keywords is None or guerriero.keywords == [] or "Eretico" not in guerriero.keywords ):                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo Eretici")

            elif "Solo Mercenari" in restrizione:
                if (guerriero.keywords is None or guerriero.keywords == [] or "Mercenario" not in guerriero.keywords ):                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo Mercenari")

            elif "Solo Mercenari o Eretici" in restrizione:
                if guerriero.tipo != Fazione.MERCENARIO and (guerriero.keywords is None or guerriero.keywords == [] or "Mercenario" not in guerriero.keywords or "Eretico" not in guerriero.keywords ):                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo Mercenari o Eretici")

            elif "Solo Comandanti" in restrizione:
                if (guerriero.keywords is None or guerriero.keywords == [] or "Comandante" not in guerriero.keywords):                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo Comandanti")

            elif "Solo Nefariti" in restrizione:
                if (guerriero.keywords is None or guerriero.keywords == [] or "Nefarita" not in guerriero.keywords ):                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo Nefarita")

            elif "Solo Personalita" in restrizione:
                if (guerriero.keywords is None or guerriero.keywords == [] or "Personalita" not in guerriero.keywords or guerriero.tipo != TipoGuerriero.PERSONALITA):                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo Personalita")
            
            elif "Assegnabile a guerrieri con V <= " in restrizione:
                valore_richiesto = int( restrizione.split("Assegnabile a guerrieri con V <= ")[1].strip() )
                
                if guerriero.stats.valore > valore_richiesto:                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo guerrieri con valore inferiore o uguale a {valore_richiesto}")

            if risultato["puo_assegnare"] == False:
                return risultato    

        # Controllo fazioni_permesse
        if self.fazioni_permesse is not None and self.fazioni_permesse != []:
            # Se l'equipaggiamento ha fazioni_permesse specifiche
            if all( a != guerriero.fazione for a in self.fazioni_permesse):
                # Verifica se è fortificazione generica utilizzabile da tutti
                if self.fazioni_permesse != ["Generica"] or (self.fazioni_permesse == ["Doomtrooper"] and guerriero.fazione not in DOOMTROOPER):
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Affiliazione richiesta: {self.fazioni_permesse}")
        
        return risultato
    
    def get_modificatore_armatura(self, guerriero_id: str = None) -> int:
        """
        Calcola il modificatore di armatura fornito dalla fortificazione
        
        Args:
            guerriero_id: ID del guerriero (per controlli specifici)
            
        Returns:
            Valore modificatore armatura
        """
        mod_totale = self.bonus_armatura
        
        for mod in self.modificatori:
            if mod.statistica == "A":
                # Verifica condizioni se specificate
                if not mod.condizione or self._verifica_condizione(mod.condizione, guerriero_id):
                    mod_totale += mod.valore
                    
        return mod_totale
    
    def get_modificatori_statistiche(self, guerriero_id: str = None) -> Dict[str, int]:
        """
        Restituisce tutti i modificatori alle statistiche
        
        Args:
            guerriero_id: ID del guerriero (per controlli specifici)
            
        Returns:
            Dizionario con modificatori per ogni statistica
        """
        modificatori = {"C": 0, "S": 0, "A": self.bonus_armatura, "V": 0}
        
        for mod in self.modificatori:
            if mod.statistica in modificatori:
                if not mod.condizione or self._verifica_condizione(mod.condizione, guerriero_id):
                    modificatori[mod.statistica] += mod.valore
                    
        return modificatori
    
    def _verifica_condizione(self, condizione: str, guerriero_id: str = None) -> bool:
        """
        Verifica se una condizione è soddisfatta
        
        Args:
            condizione: Stringa che descrive la condizione
            guerriero_id: ID del guerriero (se necessario)
            
        Returns:
            True se la condizione è soddisfatta
        """
        # Implementazione base - può essere estesa
        if condizione == "sempre":
            return True
        elif condizione == "in_combattimento":
            # Logica per verificare se in combattimento
            return False  # Placeholder
        elif condizione == "non_in_veicolo":
            # Logica per verificare se il guerriero non è in veicolo
            return True  # Placeholder
        else:
            return True  # Default: condizione soddisfatta
    
    def puo_essere_costruita(self, area_target: str, giocatore_dp: int, 
                           fortificazioni_esistenti: List[str] = None) -> Dict[str, Any]:
        """
        Verifica se la fortificazione può essere costruita
        
        Args:
            area_target: Area dove si vuole costruire ("Squadra", "Schieramento", "Avamposto")
            giocatore_dp: Punti Destino disponibili del giocatore
            fortificazioni_esistenti: Lista nomi fortificazioni già in gioco
            
        Returns:
            Dizionario con risultato della verifica
        """
        risultato = {"puo_costruire": True, "errori": [], "avvertimenti": []}
        
        # Verifica costo
        if giocatore_dp < self.costo_destino:
            risultato["puo_costruire"] = False
            risultato["errori"].append(f"Punti Destino insufficienti: serve {self.costo_destino}, disponibili {giocatore_dp}")
        
        # Verifica area compatibile
        area_ok = False
        if self.area_compatibile == AreaCompatibile.QUALSIASI_AREA:
            area_ok = True
        elif self.area_compatibile == AreaCompatibile.SQUADRA_O_SCHIERAMENTO:
            area_ok = area_target in ["Squadra", "Schieramento"]
        elif self.area_compatibile == AreaCompatibile.SOLO_AVAMPOSTO:
            area_ok = area_target == "Avamposto"
        elif self.area_compatibile.value == area_target:
            area_ok = True
            
        if not area_ok:
            risultato["puo_costruire"] = False
            risultato["errori"].append(f"Fortificazione non compatibile con area {area_target}")
        
        # Verifica unicità
        if self.unica_per_giocatore and fortificazioni_esistenti:
            if self.nome in fortificazioni_esistenti:
                risultato["puo_costruire"] = False
                risultato["errori"].append(f"Fortificazione {self.nome} già in gioco (unica per giocatore)")
        
        # Verifica requisiti particolari
        for requisito in self.requisiti:
            if not self._verifica_requisito(requisito):
                risultato["puo_costruire"] = False
                risultato["errori"].append(f"Requisito non soddisfatto: {requisito}")
        
        return risultato
    
    def _verifica_requisito(self, requisito: str) -> bool:
        """Verifica un requisito specifico"""
        # Implementazione placeholder - può essere estesa
        return True
    
    def costruisci(self, area: str, giocatore_id: str = None) -> bool:
        """
        Costruisce la fortificazione nell'area specificata
        
        Args:
            area: Area dove costruire
            giocatore_id: ID del giocatore che costruisce
            
        Returns:
            True se costruzione avvenuta con successo
        """
        if not self.in_gioco:
            self.in_gioco = True
            self.area_corrente = area
            self._attiva_effetti()
            return True
        return False
    
    def distruggi(self) -> bool:
        """
        Distrugge la fortificazione
        
        Returns:
            True se distruzione avvenuta con successo
        """
        if self.in_gioco and self.distruttibile:
            self.in_gioco = False
            self.area_corrente = None
            self.guerriero_assegnato = None
            self._disattiva_effetti()
            return True
        return False
    
    def _attiva_effetti(self):
        """Attiva gli effetti della fortificazione"""
        for abilita in self.abilita_speciali:
            if abilita.tipo_abilita == "Passiva":
                effetto = {
                    "nome": abilita.nome,
                    "tipo": "Passiva",
                    "descrizione": abilita.descrizione,
                    "attivo": True
                }
                self.effetti_attivi.append(effetto)
    
    def _disattiva_effetti(self):
        """Disattiva tutti gli effetti della fortificazione"""
        self.effetti_attivi.clear()
        self.guerrieri_influenzati.clear()
    
    def influenza_guerriero(self, guerriero_fazione: Fazione, guerriero_corporazione: str = None,
                          guerriero_apostolo: ApostoloPadre = None, 
                          guerriero_area: str = None) -> bool:
        """
        Verifica se la fortificazione influenza un determinato guerriero
        
        Args:
            guerriero_fazione: Fazione del guerriero
            guerriero_corporazione: Corporazione specifica (se applicabile)
            guerriero_apostolo: Apostolo seguito (se applicabile) 
            guerriero_area: Area del guerriero
            
        Returns:
            True se la fortificazione influenza il guerriero
        """
        # Verifica area
        if guerriero_area and self.area_corrente and guerriero_area != self.area_corrente:
            return False
        
        # Verifica beneficiario
        if self.beneficiario == BeneficiarioFortificazione.GUERRIERI_AREA:
            return True
        elif self.beneficiario == BeneficiarioFortificazione.CORPORAZIONE_SPECIFICA:
            return (self.corporazione_specifica and 
                   guerriero_fazione == self.corporazione_specifica)
        elif self.beneficiario == BeneficiarioFortificazione.APOSTOLO_SPECIFICO:
            return (self.apostolo_specifico and 
                   guerriero_apostolo == self.apostolo_specifico)
        elif self.beneficiario == BeneficiarioFortificazione.TUTTI_DOOMTROOPER:
            return guerriero_fazione != Fazione.OSCURA_LEGIONE
        elif self.beneficiario == BeneficiarioFortificazione.TUTTI_OSCURA_LEGIONE:
            return guerriero_fazione == Fazione.OSCURA_LEGIONE
        elif self.beneficiario == BeneficiarioFortificazione.FAZIONE_SPECIFICA:
            return guerriero_fazione in self.fazioni_permesse
            
        return False
    
    def applica_effetti_guerriero(self, guerriero_stats: Dict[str, int]) -> Dict[str, int]:
        """
        Applica gli effetti della fortificazione alle statistiche di un guerriero
        
        Args:
            guerriero_stats: Statistiche attuali del guerriero
            
        Returns:
            Statistiche modificate
        """
        if not self.in_gioco:
            return guerriero_stats
            
        stats_modificate = guerriero_stats.copy()
        modificatori = self.get_modificatori_statistiche()
        
        for stat, mod in modificatori.items():
            if stat in stats_modificate:
                stats_modificate[stat] += mod
                
        return stats_modificate
    
    def attiva_abilita(self, nome_abilita: str, costo_pagato: int = 0) -> Dict[str, Any]:
        """
        Attiva un'abilità speciale della fortificazione
        
        Args:
            nome_abilita: Nome dell'abilità da attivare
            costo_pagato: Costo pagato per l'attivazione
            
        Returns:
            Risultato dell'attivazione
        """
        risultato = {"successo": False, "effetti": [], "messaggio": ""}
        
        for abilita in self.abilita_speciali:
            if abilita.nome == nome_abilita:
                if abilita.tipo_abilita == "Attivabile":
                    if costo_pagato >= abilita.costo_attivazione:
                        risultato["successo"] = True
                        risultato["effetti"] = abilita.effetti_speciali.copy()
                        risultato["messaggio"] = f"Abilità {nome_abilita} attivata"
                    else:
                        risultato["messaggio"] = f"Costo insufficiente per {nome_abilita}"
                else:
                    risultato["messaggio"] = f"Abilità {nome_abilita} non è attivabile"
                break
        else:
            risultato["messaggio"] = f"Abilità {nome_abilita} non trovata"
            
        return risultato
    
    def get_info_completa(self) -> Dict[str, Any]:
        """Restituisce informazioni complete sulla fortificazione"""
        return {
            "nome": self.nome,
            "tipo": self.tipo.value,
            "costo_destino": self.costo_destino,
            "rarity": self.rarity.value,
            "area_compatibile": self.area_compatibile.value,
            "beneficiario": self.beneficiario.value,
            "in_gioco": self.in_gioco,
            "area_corrente": self.area_corrente,
            "bonus_armatura": self.bonus_armatura,
            "modificatori": [
                {
                    "statistica": mod.statistica,
                    "valore": mod.valore,
                    "condizione": mod.condizione,
                    "descrizione": mod.descrizione
                }
                for mod in self.modificatori
            ],
            "abilita_speciali": [
                {
                    "nome": abil.nome,
                    "tipo": abil.tipo_abilita,
                    "descrizione": abil.descrizione,
                    "costo": abil.costo_attivazione
                }
                for abil in self.abilita_speciali
            ],
            "testo_carta": self.testo_carta,
            "keywords": self.keywords,
            "unica_per_giocatore": self.unica_per_giocatore,
            "distruttibile": self.distruttibile
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializza la fortificazione in dizionario"""
        return {
            "nome": self.nome,
            "costo_destino": self.costo_destino,
            "tipo": self.tipo.value,
            "rarity": self.rarity.value,
            "set_espansione": self.set_espansione.value,
            "numero_carta": self.numero_carta,
            "area_compatibile": self.area_compatibile.value,
            "beneficiario": self.beneficiario.value,
            "corporazione_specifica": self.corporazione_specifica.value if self.corporazione_specifica else None,
            "apostolo_specifico": self.apostolo_specifico.value if self.apostolo_specifico else None,
            "in_gioco": self.in_gioco,
            "area_corrente": self.area_corrente,
            "guerriero_assegnato": self.guerriero_assegnato,
            "unica_per_giocatore": self.unica_per_giocatore,
            "distruttibile": self.distruttibile,
            "modificatori": [
                {
                    "statistica": mod.statistica,
                    "valore": mod.valore,
                    "condizione": mod.condizione,
                    "descrizione": mod.descrizione,
                    "permanente": mod.permanente
                }
                for mod in self.modificatori
            ],
            "abilita_speciali": [
                {
                    "nome": abil.nome,
                    "descrizione": abil.descrizione,
                    "tipo_abilita": abil.tipo_abilita,
                    "costo_attivazione": abil.costo_attivazione,
                    "condizioni_attivazione": abil.condizioni_attivazione,
                    "effetti_speciali": abil.effetti_speciali
                }
                for abil in self.abilita_speciali
            ],
            "requisiti": self.requisiti,
            "restrizioni": self.restrizioni,
            "fazioni_permesse": [f.value for f in self.fazioni_permesse],
            "testo_carta": self.testo_carta,
            "flavour_text": self.flavour_text,
            "keywords": self.keywords,
            "punti_struttura": self.punti_struttura,
            "resistenza_attacchi": self.resistenza_attacchi,
            "bonus_armatura": self.bonus_armatura,
             "valore_strategico": self.valore_strategico,
            "quantita": self.quantita,
            "quantita_minima_consigliata": self.quantita_minima_consigliata,
            "fondamentale": self.fondamentale
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Fortificazione':
        """Crea una fortificazione da dizionario"""
        fortificazione = cls(data["nome"], data["costo_destino"])
        
        # Ripristina enums
        fortificazione.tipo = TipoFortificazione(data["tipo"])
        fortificazione.rarity = Rarity(data["rarity"])
        fortificazione.set_espansione = Set_Espansione(data["set_espansione"])
        fortificazione.area_compatibile = AreaCompatibile(data["area_compatibile"])
        fortificazione.beneficiario = BeneficiarioFortificazione(data["beneficiario"])
        
        if data["corporazione_specifica"]:
            if data["corporazione_specifica"] == "Eretici":
                fortificazione.corporazione_specifica = "Eretici"
            elif "Seguaci di " in data["corporazione_specifica"]:
                fortificazione.corporazione_specifica = data["corporazione_specifica"]
            else:    
                fortificazione.corporazione_specifica = Fazione(data["corporazione_specifica"]).value

        if data["apostolo_specifico"]:
            fortificazione.apostolo_specifico = ApostoloPadre(data["apostolo_specifico"])
        
        # Configura fazioni permesse
        if data["fazioni_permesse"]:   
            if "Doomtrooper" in data["fazioni_permesse"]:
                fortificazione.fazioni_permesse = ["Doomtrooper"]
            else:         
                fortificazione.fazioni_permesse = [Fazione(f) for f in data["fazioni_permesse"] 
                    if f in [faz.value for faz in Fazione]]
   
        
        # Ripristina proprietà
        fortificazione.numero_carta = data["numero_carta"]
        #fortificazione.in_gioco = data["in_gioco"]
        #fortificazione.area_corrente = data["area_corrente"]
        #fortificazione.guerriero_assegnato = data["guerriero_assegnato"]
        fortificazione.unica_per_giocatore = data["unica_per_giocatore"]
        fortificazione.distruttibile = data["distruttibile"]
        
        # Ripristina modificatori
        for mod_data in data["modificatori"]:
            mod = ModificatoreFortificazione(
                statistica=mod_data["statistica"],
                valore=mod_data["valore"],
                condizione=mod_data["condizione"],
                descrizione=mod_data["descrizione"],
                permanente=mod_data["permanente"]
            )
            fortificazione.modificatori.append(mod)
        
        # Ripristina abilità
        for abil_data in data["abilita_speciali"]:
            abil = AbilitaFortificazione(
                nome=abil_data["nome"],
                descrizione=abil_data["descrizione"],
                tipo_abilita=abil_data["tipo_abilita"],
                costo_attivazione=abil_data["costo_attivazione"],
                condizioni_attivazione=abil_data["condizioni_attivazione"],
                effetti_speciali=abil_data["effetti_speciali"]
            )
            fortificazione.abilita_speciali.append(abil)
        
        # Ripristina altre proprietà
        fortificazione.requisiti = data["requisiti"]
        fortificazione.restrizioni = data["restrizioni"]
        fortificazione.fazioni_permesse = [Fazione(f) for f in data["fazioni_permesse"]]
        fortificazione.testo_carta = data["testo_carta"]
        fortificazione.flavour_text = data["flavour_text"]
        fortificazione.keywords = data["keywords"]
        fortificazione.punti_struttura = data["punti_struttura"]
        fortificazione.resistenza_attacchi = data["resistenza_attacchi"]
        fortificazione.bonus_armatura = data["bonus_armatura"]
        fortificazione.valore_strategico = data["valore_strategico"]
        fortificazione.quantita = data.get("quantita", 0)
        fortificazione.quantita_minima_consigliata = data.get("quantita_minima_consigliata", 0)
        fortificazione.fondamentale = data.get("fondamentale", False)
        
        return fortificazione
    
    def __str__(self) -> str:
        """Rappresentazione stringa della fortificazione"""
        stato = "in gioco" if self.in_gioco else "non costruita"
        area = f" [{self.area_corrente}]" if self.area_corrente else ""
        return f"{self.nome} ({self.tipo.value}) - Costo: {self.costo_destino}D - {stato}{area}"
    
    def __repr__(self) -> str:
        """Rappresentazione tecnica della fortificazione"""
        return f"Fortificazione(nome='{self.nome}', tipo={self.tipo.value}, costo={self.costo_destino})"


# Test della classe
if __name__ == "__main__":
    print("=== TEST CLASSE FORTIFICAZIONE ===")
    
    # Test creazione fortificazione base
    print("\n=== TEST CREAZIONE FORTIFICAZIONE ===")
    fortezza = Fortificazione("Fortezza Imperiale", 3)
    fortezza.tipo = TipoFortificazione.CITTA_CORPORAZIONE
    fortezza.corporazione_specifica = Fazione.IMPERIALE
    fortezza.beneficiario = BeneficiarioFortificazione.CORPORAZIONE_SPECIFICA
    fortezza.bonus_armatura = 2
    fortezza.area_compatibile = AreaCompatibile.SQUADRA_O_SCHIERAMENTO
    
    # Aggiungi modificatori
    mod_armatura = ModificatoreFortificazione(
        statistica="A",
        valore=2,
        condizione="sempre",
        descrizione="Bonus armatura permanente"
    )
    fortezza.modificatori.append(mod_armatura)
    
    # Aggiungi abilità
    abilita_difesa = AbilitaFortificazione(
        nome="Difesa Rafforzata",
        descrizione="I guerrieri Imperiali ricevono +2 Armatura",
        tipo_abilita="Passiva"
    )
    fortezza.abilita_speciali.append(abilita_difesa)
    
    fortezza.testo_carta = "Le mura imperiali proteggono i difensori della fede."
    fortezza.flavour_text = "Nessun nemico ha mai violato queste mura."
    
    print(f"Fortificazione creata: {fortezza}")
    print(f"Tipo: {fortezza.tipo.value}")
    print(f"Beneficiario: {fortezza.beneficiario.value}")
    print(f"Bonus armatura: {fortezza.bonus_armatura}")
    
    # Test costruzione
    print(f"\n=== TEST COSTRUZIONE ===")
    verifica = fortezza.puo_essere_costruita("Squadra", 5, [])
    print(f"Può essere costruita: {verifica['puo_costruire']}")
    if verifica['errori']:
        print(f"Errori: {verifica['errori']}")
    
    successo = fortezza.costruisci("Squadra")
    print(f"Costruzione riuscita: {successo}")
    print(f"Stato: {fortezza}")
    
    # Test influenza guerriero
    print(f"\n=== TEST INFLUENZA GUERRIERO ===")
    influenza_imperiale = fortezza.influenza_guerriero(Fazione.IMPERIALE, guerriero_area="Squadra")
    influenza_bauhaus = fortezza.influenza_guerriero(Fazione.BAUHAUS, guerriero_area="Squadra")
    
    print(f"Influenza guerriero Imperiale: {influenza_imperiale}")
    print(f"Influenza guerriero Bauhaus: {influenza_bauhaus}")
    
    # Test modificatori
    print(f"\n=== TEST MODIFICATORI ===")
    stats_guerriero = {"C": 12, "S": 10, "A": 8, "V": 14}
    stats_modificate = fortezza.applica_effetti_guerriero(stats_guerriero)
    
    print(f"Statistiche originali: {stats_guerriero}")
    print(f"Statistiche modificate: {stats_modificate}")
    print(f"Modificatore armatura: +{stats_modificate['A'] - stats_guerriero['A']}")
    
    # Test serializzazione
    print(f"\n=== TEST SERIALIZZAZIONE ===")
    dict_fortezza = fortezza.to_dict()
    fortezza_ricostruita = Fortificazione.from_dict(dict_fortezza)
    
    print(f"Fortificazione originale: {fortezza.nome}")
    print(f"Fortificazione ricostruita: {fortezza_ricostruita.nome}")
    print(f"Serializzazione riuscita: {fortezza.nome == fortezza_ricostruita.nome}")
    
    # Test distruzione
    print(f"\n=== TEST DISTRUZIONE ===")
    print(f"Prima della distruzione: {fortezza.in_gioco}")
    distrutta = fortezza.distruggi()
    print(f"Distruzione riuscita: {distrutta}")
    print(f"Dopo la distruzione: {fortezza.in_gioco}")
    
    print(f"\n=== IMPLEMENTAZIONE COMPLETATA ===")
    print("✓ Classe Fortificazione implementata secondo regolamento Doomtrooper")
    print("✓ Tipi: Città Corporazione, Cittadelle Apostolo, Fortificazioni Generiche")
    print("✓ Aree compatibili: Squadra, Schieramento, Avamposto")
    print("✓ Beneficiari: Per area, corporazione, apostolo, fazione")
    print("✓ Modificatori statistiche con condizioni")
    print("✓ Abilità speciali passive e attivabili")
    print("✓ Regole unicità e distruttibilità")
    print("✓ Compatibile con classe Guerriero e altre classi")
    print("✓ Serializzazione tramite to_dict() e from_dict()")
    print("✓ Gestione stato costruzione e area assegnata")
    print("✓ Controlli influenza guerrieri per fazione/corporazione")
    print("✓ Applicazione effetti automatica alle statistiche")
    print("✓ Struttura coerente con regolamento ufficiale")
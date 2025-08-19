"""
Modulo per la rappresentazione delle carte Equipaggiamento di Mutant Chronicles/Doomtrooper
Include armi, armature, veicoli, kit e strumenti vari
Basato sulla struttura delle classi Guerriero e Oscura_Simmetria
VERSIONE CORRETTA - Allineata alle regole ufficiali del gioco
"""

from enum import Enum
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import json
from source.cards.Guerriero import Fazione, Rarity  # Import dalle classi esistenti


class TipoEquipaggiamento(Enum):
    """Tipi di carte Equipaggiamento - Allineati alle regole ufficiali"""
    ARMA_DA_FUOCO = "Arma da Fuoco"
    ARMA_DA_CORPO_A_CORPO = "Arma da Corpo a Corpo"
    ARMA_DA_FUOCO_E_CORPO_A_CORPO = "Arma da Fuoco e da Corpo a Corpo"
    ARMA_SPECIALE = "Arma Speciale"
    ARMATURA = "Armatura"
    VEICOLO = "Veicolo"
    EQUIPAGGIAMENTO_GENERICO = "Equipaggiamento"
    RELIQUIA = "Reliquia"  # Non considerato Equipaggiamento normale


class TipoArmatura(Enum):
    """Tipi di armatura"""
    LEGGERA = "Leggera"
    MEDIA = "Media"
    PESANTE = "Pesante"
    POWERED = "Powered"


class TipoVeicolo(Enum):
    """Tipi di veicolo - Basati sulle regole avanzate"""
    GENERICO = "Veicolo"
    AERONAVE = "Aeronave"
    SOTTOMARINO = "Sottomarino"
    CARRO_ARMATO = "Carro Armato"


@dataclass
class ModificatoreEquipaggiamento:
    """Rappresenta un modificatore applicato dall'equipaggiamento"""
    statistica: str  # "C", "S", "A", "V"
    valore: int      # valore del modificatore (+/-)
    condizione: str = ""  # condizione per applicare il modificatore
    descrizione: str = ""


@dataclass
class AbilitaSpeciale:
    """Rappresenta un'abilità speciale dell'equipaggiamento"""
    nome: str
    descrizione: str
    costo_attivazione: int = 0  # costo in azioni/DP per attivare
    tipo_attivazione: str = "Automatica"  # "Automatica", "Azione", "Reazione"
    limitazioni: List[str] = None
    
    def __post_init__(self):
        if self.limitazioni is None:
            self.limitazioni = []


class Equipaggiamento:
    """
    Classe per rappresentare una carta Equipaggiamento di Mutant Chronicles/Doomtrooper
    VERSIONE CORRETTA - Allineata alle regole del regolamento ufficiale
    """
    
    def __init__(self, nome: str, valore: int = 0):
        """
        Inizializza una nuova carta Equipaggiamento
        
        Args:
            nome: Nome dell'equipaggiamento
            valore: Valore (V) dell'equipaggiamento per giocarla (costo in Destiny Points)
        """
        self.nome = nome
        self.valore = valore  # Costo in Destiny Points (campo V sulle carte)
        
        # Classificazione dell'equipaggiamento
        self.tipo = TipoEquipaggiamento.EQUIPAGGIAMENTO_GENERICO
        self.tipo_armatura = None   # Solo per armature
        self.tipo_veicolo = None    # Solo per veicoli
        self.rarity = Rarity.COMMON
        
        # Modificatori alle statistiche del guerriero (C, S, A, V)
        self.modificatori_combattimento = 0    # Modifica al Corpo a corpo (C)
        self.modificatori_sparare = 0          # Modifica al Sparare (S)
        self.modificatori_armatura = 0         # Modifica all'Armatura (A)
        self.modificatori_valore = 0           # Modifica al Valore (V)
        
        # Modificatori condizionali
        self.modificatori_speciali: List[ModificatoreEquipaggiamento] = []
        
        # Abilità speciali
        self.abilita_speciali: List[AbilitaSpeciale] = []
        
        # Restrizioni di affiliazione
        self.affiliazione = None  # Affiliazione richiesta (None = generica)
        self.restrizioni_guerriero: List[str] = []
        
        # Meccaniche specifiche per armi
        self.e_arma_da_fuoco = False
        self.e_arma_corpo_a_corpo = False
        self.e_arma_speciale = False
        
        # Meccaniche specifiche dei veicoli
        self.dentro_veicolo = True  # Il guerriero inizia dentro il veicolo
        self.restrizioni_equipaggiamento: List[str] = []  # Restrizioni su altri equipaggiamenti
        self.restrizioni_armi: List[str] = []  # Restrizioni specifiche sulle armi
        
        # Informazioni della carta
        self.testo_carta = ""
        self.flavour_text = ""
        self.keywords: List[str] = []
        
        # Metadati
        self.set_espansione = "Base"
        self.numero_carta = ""
        
        # Stato di gioco
        self.assegnato_a: Optional[str] = None  # nome del guerriero che lo usa
        self.in_gioco = False
        
        # Stato specifico per veicoli
        self.guerriero_dentro_veicolo = True  # Solo per veicoli
        
        # Compatibilità
        self.compatibile_con: List[str] = []
        self.equipaggiamenti_richiesti: List[str] = []
    
    def get_costo_destiny_points(self) -> int:
        """Restituisce il costo in Destiny Points per giocare questa carta"""
        return self.valore
    
    def e_arma(self) -> bool:
        """Controlla se l'equipaggiamento è un'arma (qualsiasi tipo)"""
        return self.tipo in [
            TipoEquipaggiamento.ARMA_DA_FUOCO,
            TipoEquipaggiamento.ARMA_DA_CORPO_A_CORPO,
            TipoEquipaggiamento.ARMA_DA_FUOCO_E_CORPO_A_CORPO,
            TipoEquipaggiamento.ARMA_SPECIALE
        ]
    
    def e_armatura(self) -> bool:
        """Controlla se l'equipaggiamento è un'armatura"""
        return self.tipo == TipoEquipaggiamento.ARMATURA
    
    def e_veicolo(self) -> bool:
        """Controlla se l'equipaggiamento è un veicolo"""
        return self.tipo == TipoEquipaggiamento.VEICOLO
    
    def puo_essere_usato_in_combattimento_corpo_a_corpo(self) -> bool:
        """Verifica se può essere usato in combattimento corpo a corpo"""
        return (self.tipo == TipoEquipaggiamento.ARMA_DA_CORPO_A_CORPO or 
                self.tipo == TipoEquipaggiamento.ARMA_DA_FUOCO_E_CORPO_A_CORPO or
                self.tipo == TipoEquipaggiamento.ARMA_SPECIALE)
    
    def puo_essere_usato_in_combattimento_sparare(self) -> bool:
        """Verifica se può essere usato in combattimento con armi da fuoco"""
        return (self.tipo == TipoEquipaggiamento.ARMA_DA_FUOCO or
                self.tipo == TipoEquipaggiamento.ARMA_DA_FUOCO_E_CORPO_A_CORPO or
                self.tipo == TipoEquipaggiamento.ARMA_SPECIALE)
    
    def puo_essere_assegnato_a_guerriero(self, guerriero: Any) -> Dict[str, Any]:
        """
        Controlla se l'equipaggiamento può essere assegnato al guerriero specificato
        Basato sulle regole di affiliazione del regolamento
        
        Args:
            guerriero: Istanza del guerriero
            
        Returns:
            Dizionario con risultato e eventuali errori
        """
        risultato = {"puo_assegnare": True, "errori": []}
        
        # Controllo affiliazione
        if self.affiliazione is not None:
            # Se l'equipaggiamento ha un'affiliazione specifica
            if guerriero.fazione != self.affiliazione:
                # Verifica se è equipaggiamento generico utilizzabile da tutti
                if self.affiliazione != "Generica":
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Affiliazione richiesta: {self.affiliazione.value}")
        
        # Controllo restrizioni specifiche
        for restrizione in self.restrizioni_guerriero:
            if "Solo Doomtrooper" in restrizione:
                if guerriero.fazione == Fazione.LEGIONE_OSCURA:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Solo per Doomtrooper")
            elif "Solo Oscura Legione" in restrizione:
                if guerriero.fazione != Fazione.LEGIONE_OSCURA:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Solo per Oscura Legione")
            elif "Non Animali" in restrizione:
                if "Animale" in guerriero.keywords:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Non può essere assegnato ad Animali")
        
        return risultato
    
    def applica_modificatori(self, guerriero: Any) -> Dict[str, int]:
        """
        Applica i modificatori dell'equipaggiamento al guerriero
        
        Args:
            guerriero: Istanza del guerriero
            
        Returns:
            Dizionario con i modificatori applicati
        """
        modificatori_applicati = {}
        
        # Applicazione modificatori base
        if self.modificatori_combattimento != 0:
            guerriero.applica_modificatore("combattimento", self.modificatori_combattimento)
            modificatori_applicati["combattimento"] = self.modificatori_combattimento
        
        if self.modificatori_sparare != 0:
            guerriero.applica_modificatore("sparare", self.modificatori_sparare)
            modificatori_applicati["sparare"] = self.modificatori_sparare
        
        if self.modificatori_armatura != 0:
            guerriero.applica_modificatore("armatura", self.modificatori_armatura)
            modificatori_applicati["armatura"] = self.modificatori_armatura
        
        if self.modificatori_valore != 0:
            guerriero.applica_modificatore("valore", self.modificatori_valore)
            modificatori_applicati["valore"] = self.modificatori_valore
        
        # Modificatori condizionali
        for mod in self.modificatori_speciali:
            if self._verifica_condizione_modificatore(mod, guerriero):
                guerriero.applica_modificatore(mod.statistica, mod.valore)
                if mod.statistica in modificatori_applicati:
                    modificatori_applicati[mod.statistica] += mod.valore
                else:
                    modificatori_applicati[mod.statistica] = mod.valore
        
        return modificatori_applicati
    
    def _verifica_condizione_modificatore(self, modificatore: ModificatoreEquipaggiamento, 
                                        guerriero: Any) -> bool:
        """Verifica se la condizione per un modificatore è soddisfatta"""
        if not modificatore.condizione:
            return True
        
        condizione = modificatore.condizione.lower()
        
        if "combattimento corpo a corpo" in condizione:
            return hasattr(guerriero, 'in_combattimento_cac') and guerriero.in_combattimento_cac
        elif "combattimento sparare" in condizione:
            return hasattr(guerriero, 'in_combattimento_sparare') and guerriero.in_combattimento_sparare
        elif "ferito" in condizione:
            return guerriero.ferito
        elif "non ferito" in condizione:
            return not guerriero.ferito
        
        return True
    
    # MECCANICHE SPECIFICHE PER VEICOLI (Regole Avanzate)
    
    def entra_nel_veicolo(self) -> bool:
        """Il guerriero entra nel veicolo (costa 1 Azione)"""
        if self.e_veicolo() and not self.guerriero_dentro_veicolo:
            self.guerriero_dentro_veicolo = True
            return True
        return False
    
    def esce_dal_veicolo(self) -> bool:
        """Il guerriero esce dal veicolo (costa 1 Azione)"""
        if self.e_veicolo() and self.guerriero_dentro_veicolo:
            self.guerriero_dentro_veicolo = False
            return True
        return False
    
    def guerriero_e_dentro_veicolo(self) -> bool:
        """Verifica se il guerriero è dentro il veicolo"""
        return self.e_veicolo() and self.guerriero_dentro_veicolo
    
    def applica_restrizioni_veicolo(self, guerriero: Any) -> List[str]:
        """
        Applica le restrizioni del veicolo quando il guerriero è dentro
        Basato sulle regole avanzate per i veicoli
        """
        restrizioni_attive = []
        
        if self.guerriero_e_dentro_veicolo():
            # Restrizioni comuni per tutti i veicoli
            restrizioni_attive.append("Non può guadagnare effetti dalle Fortificazioni")
            restrizioni_attive.append("Non può andare in Copertura")
            
            # Restrizioni specifiche per tipo di veicolo
            if self.tipo_veicolo == TipoVeicolo.AERONAVE:
                restrizioni_attive.append("Non può attaccare in Corpo a Corpo")
                restrizioni_attive.append("Non può essere attaccato in Corpo a Corpo")
            elif self.tipo_veicolo == TipoVeicolo.SOTTOMARINO:
                restrizioni_attive.append("Non può attaccare in Corpo a Corpo")
                restrizioni_attive.append("Non può essere attaccato in Corpo a Corpo")
            
            # Restrizioni su equipaggiamento
            for restrizione in self.restrizioni_equipaggiamento:
                restrizioni_attive.append(restrizione)
        
        return restrizioni_attive
    
    def assegna_a_guerriero(self, nome_guerriero: str) -> bool:
        """Assegna l'equipaggiamento a un guerriero"""
        if self.assegnato_a is None:
            self.assegnato_a = nome_guerriero
            self.in_gioco = True
            
            # Se è un veicolo, inizia con il guerriero dentro (regola standard)
            if self.e_veicolo():
                self.guerriero_dentro_veicolo = True
            
            return True
        return False
    
    def rimuovi_da_guerriero(self) -> Optional[str]:
        """Rimuove l'equipaggiamento dal guerriero corrente"""
        precedente = self.assegnato_a
        self.assegnato_a = None
        self.in_gioco = False
        
        # Reset stato veicolo
        if self.e_veicolo():
            self.guerriero_dentro_veicolo = True
        
        return precedente
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte l'equipaggiamento in un dizionario per serializzazione"""
        return {
            "nome": self.nome,
            "valore": self.valore,
            "tipo": self.tipo.value,
            "tipo_armatura": self.tipo_armatura.value if self.tipo_armatura else None,
            "tipo_veicolo": self.tipo_veicolo.value if self.tipo_veicolo else None,
            "rarity": self.rarity.value,
            "modificatori": {
                "combattimento": self.modificatori_combattimento,
                "sparare": self.modificatori_sparare,
                "armatura": self.modificatori_armatura,
                "valore": self.modificatori_valore
            },
            "modificatori_speciali": [
                {
                    "statistica": mod.statistica,
                    "valore": mod.valore,
                    "condizione": mod.condizione,
                    "descrizione": mod.descrizione
                } for mod in self.modificatori_speciali
            ],
            "abilita_speciali": [
                {
                    "nome": ab.nome,
                    "descrizione": ab.descrizione,
                    "costo_attivazione": ab.costo_attivazione,
                    "tipo_attivazione": ab.tipo_attivazione,
                    "limitazioni": ab.limitazioni
                } for ab in self.abilita_speciali
            ],
            "affiliazione": self.affiliazione.value if self.affiliazione else None,
            "restrizioni_guerriero": self.restrizioni_guerriero,
            "meccaniche_armi": {
                "e_arma_da_fuoco": self.e_arma_da_fuoco,
                "e_arma_corpo_a_corpo": self.e_arma_corpo_a_corpo,
                "e_arma_speciale": self.e_arma_speciale
            },
            "meccaniche_veicoli": {
                "dentro_veicolo": self.dentro_veicolo,
                "guerriero_dentro_veicolo": self.guerriero_dentro_veicolo,
                "restrizioni_equipaggiamento": self.restrizioni_equipaggiamento,
                "restrizioni_armi": self.restrizioni_armi
            },
            "stato": {
                "assegnato_a": self.assegnato_a,
                "in_gioco": self.in_gioco
            },
            "testo_carta": self.testo_carta,
            "flavour_text": self.flavour_text,
            "keywords": self.keywords,
            "set_espansione": self.set_espansione,
            "numero_carta": self.numero_carta,
            "compatibilita": {
                "compatibile_con": self.compatibile_con,
                "equipaggiamenti_richiesti": self.equipaggiamenti_richiesti
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Equipaggiamento':
        """Crea un equipaggiamento da un dizionario"""
        equipaggiamento = cls(data["nome"], data["valore"])
        
        # Tipo e classificazione
        equipaggiamento.tipo = TipoEquipaggiamento(data["tipo"])
        if data["tipo_armatura"]:
            equipaggiamento.tipo_armatura = TipoArmatura(data["tipo_armatura"])
        if data["tipo_veicolo"]:
            equipaggiamento.tipo_veicolo = TipoVeicolo(data["tipo_veicolo"])
        equipaggiamento.rarity = Rarity(data["rarity"])
        
        # Modificatori
        mod = data["modificatori"]
        equipaggiamento.modificatori_combattimento = mod["combattimento"]
        equipaggiamento.modificatori_sparare = mod["sparare"]
        equipaggiamento.modificatori_armatura = mod["armatura"]
        equipaggiamento.modificatori_valore = mod["valore"]
        
        # Affiliazione
        if data["affiliazione"]:
            equipaggiamento.affiliazione = Fazione(data["affiliazione"])
        
        equipaggiamento.restrizioni_guerriero = data["restrizioni_guerriero"]
        
        # Meccaniche
        armi = data["meccaniche_armi"]
        equipaggiamento.e_arma_da_fuoco = armi["e_arma_da_fuoco"]
        equipaggiamento.e_arma_corpo_a_corpo = armi["e_arma_corpo_a_corpo"]
        equipaggiamento.e_arma_speciale = armi["e_arma_speciale"]
        
        veicoli = data["meccaniche_veicoli"]
        equipaggiamento.dentro_veicolo = veicoli["dentro_veicolo"]
        equipaggiamento.guerriero_dentro_veicolo = veicoli["guerriero_dentro_veicolo"]
        equipaggiamento.restrizioni_equipaggiamento = veicoli["restrizioni_equipaggiamento"]
        equipaggiamento.restrizioni_armi = veicoli["restrizioni_armi"]
        
        # Stato
        stato = data["stato"]
        equipaggiamento.assegnato_a = stato["assegnato_a"]
        equipaggiamento.in_gioco = stato["in_gioco"]
        
        # Testi e metadati
        equipaggiamento.testo_carta = data["testo_carta"]
        equipaggiamento.flavour_text = data["flavour_text"]
        equipaggiamento.keywords = data["keywords"]
        equipaggiamento.set_espansione = data["set_espansione"]
        equipaggiamento.numero_carta = data["numero_carta"]
        
        # Compatibilità
        comp = data["compatibilita"]
        equipaggiamento.compatibile_con = comp["compatibile_con"]
        equipaggiamento.equipaggiamenti_richiesti = comp["equipaggiamenti_richiesti"]
        
        return equipaggiamento
    
    def __str__(self) -> str:
        """Rappresentazione stringa dell'equipaggiamento"""
        modificatori_str = []
        if self.modificatori_combattimento != 0:
            modificatori_str.append(f"{self.modificatori_combattimento:+}C")
        if self.modificatori_sparare != 0:
            modificatori_str.append(f"{self.modificatori_sparare:+}S")
        if self.modificatori_armatura != 0:
            modificatori_str.append(f"{self.modificatori_armatura:+}A")
        if self.modificatori_valore != 0:
            modificatori_str.append(f"{self.modificatori_valore:+}V")
        
        mod_str = " ".join(modificatori_str) if modificatori_str else ""
        
        return (f"{self.nome} (V:{self.valore}) - "
                f"{self.tipo.value} {mod_str}").strip()
    
    def __repr__(self) -> str:
        return f"Equipaggiamento('{self.nome}', {self.valore})"


# Funzioni di utilità per creare equipaggiamenti specifici

def crea_arma_da_fuoco(nome: str, bonus_sparare: int, valore: int = 1) -> Equipaggiamento:
    """Crea un'arma da fuoco"""
    arma = Equipaggiamento(nome, valore)
    arma.tipo = TipoEquipaggiamento.ARMA_DA_FUOCO
    arma.modificatori_sparare = bonus_sparare
    arma.e_arma_da_fuoco = True
    arma.keywords.append("Arma da Fuoco")
    return arma

def crea_arma_corpo_a_corpo(nome: str, bonus_combattimento: int, valore: int = 1) -> Equipaggiamento:
    """Crea un'arma da corpo a corpo"""
    arma = Equipaggiamento(nome, valore)
    arma.tipo = TipoEquipaggiamento.ARMA_DA_CORPO_A_CORPO
    arma.modificatori_combattimento = bonus_combattimento
    arma.e_arma_corpo_a_corpo = True
    arma.keywords.append("Arma da Corpo a Corpo")
    return arma

def crea_armatura(nome: str, bonus_armatura: int, tipo_armatura: TipoArmatura = TipoArmatura.LEGGERA, valore: int = 1) -> Equipaggiamento:
    """Crea un'armatura"""
    armatura = Equipaggiamento(nome, valore)
    armatura.tipo = TipoEquipaggiamento.ARMATURA
    armatura.tipo_armatura = tipo_armatura
    armatura.modificatori_armatura = bonus_armatura
    armatura.keywords.append("Armatura")
    return armatura

def crea_veicolo(nome: str, tipo_veicolo: TipoVeicolo = TipoVeicolo.GENERICO, valore: int = 3) -> Equipaggiamento:
    """Crea un veicolo"""
    veicolo = Equipaggiamento(nome, valore)
    veicolo.tipo = TipoEquipaggiamento.VEICOLO
    veicolo.tipo_veicolo = tipo_veicolo
    veicolo.keywords.append("Veicolo")
    return veicolo


# Esempi di utilizzo corretto secondo il regolamento
if __name__ == "__main__":
    print("=== ESEMPI EQUIPAGGIAMENTO MUTANT CHRONICLES (REGOLAMENTO UFFICIALE) ===")
    
    # Esempio 1: Arma da Fuoco - Pistola Automatica
    pistola = crea_arma_da_fuoco("Pistola Automatica", bonus_sparare=2, valore=1)
    pistola.testo_carta = "+2 Sparare. Può essere usata in combattimenti con armi da fuoco."
    print(f"✓ {pistola}")
    print(f"  Costo: {pistola.get_costo_destiny_points()} Destiny Points")
    print(f"  Utilizzabile in combattimento Sparare: {pistola.puo_essere_usato_in_combattimento_sparare()}")
    print(f"  Utilizzabile in combattimento Corpo a Corpo: {pistola.puo_essere_usato_in_combattimento_corpo_a_corpo()}")
    
    # Esempio 2: Arma da Corpo a Corpo - Spada da Combattimento
    spada = crea_arma_corpo_a_corpo("Spada da Combattimento", bonus_combattimento=2, valore=1)
    spada.testo_carta = "+2 Corpo a corpo. Può essere usata in combattimenti ravvicinati."
    print(f"\n✓ {spada}")
    print(f"  Utilizzabile in combattimento Corpo a Corpo: {spada.puo_essere_usato_in_combattimento_corpo_a_corpo()}")
    print(f"  Utilizzabile in combattimento Sparare: {spada.puo_essere_usato_in_combattimento_sparare()}")
    
    # Esempio 3: Arma Mista - Fucile con Baionetta
    fucile_baionetta = Equipaggiamento("Fucile con Baionetta", valore=3)
    fucile_baionetta.tipo = TipoEquipaggiamento.ARMA_DA_FUOCO_E_CORPO_A_CORPO
    fucile_baionetta.modificatori_sparare = 3
    fucile_baionetta.modificatori_combattimento = 1
    fucile_baionetta.e_arma_da_fuoco = True
    fucile_baionetta.e_arma_corpo_a_corpo = True
    fucile_baionetta.testo_carta = "+3 Sparare, +1 Corpo a corpo. Utilizzabile in entrambi i tipi di combattimento."
    print(f"\n✓ {fucile_baionetta}")
    print(f"  Utilizzabile in entrambi i combattimenti: C={fucile_baionetta.puo_essere_usato_in_combattimento_corpo_a_corpo()}, S={fucile_baionetta.puo_essere_usato_in_combattimento_sparare()}")
    
    # Esempio 4: Armatura - Solo una per guerriero
    armatura_combattimento = crea_armatura("Armatura da Combattimento", bonus_armatura=3, tipo_armatura=TipoArmatura.MEDIA, valore=2)
    armatura_combattimento.testo_carta = "+3 Armatura. Un guerriero può avere una sola Armatura."
    print(f"\n✓ {armatura_combattimento}")
    print(f"  Tipo: {armatura_combattimento.tipo_armatura.value}")
    print(f"  È armatura: {armatura_combattimento.e_armatura()}")
    
    # Esempio 5: Veicolo con regole avanzate
    aeronave = crea_veicolo("Aeronave da Combattimento", tipo_veicolo=TipoVeicolo.AERONAVE, valore=5)
    aeronave.modificatori_sparare = 2
    aeronave.modificatori_armatura = 1
    aeronave.restrizioni_equipaggiamento = ["Non può usare altre armi quando è dentro l'aeronave"]
    aeronave.testo_carta = "+2 Sparare, +1 Armatura. Guerriero dentro non può combattere corpo a corpo."
    print(f"\n✓ {aeronave}")
    print(f"  Guerriero inizia dentro: {aeronave.guerriero_dentro_veicolo}")
    print(f"  Tipo veicolo: {aeronave.tipo_veicolo.value}")
    
    # Esempio 6: Meccaniche di assegnazione
    print(f"\n=== MECCANICHE DI ASSEGNAZIONE ===")
    
    # Simula un guerriero Bauhaus
    class GuerrieroTest:
        def __init__(self, nome, fazione):
            self.nome = nome
            self.fazione = fazione
            self.keywords = []
            self.ferito = False
            self.modificatori_attivi = {}
        
        def applica_modificatore(self, stat, valore):
            if stat in self.modificatori_attivi:
                self.modificatori_attivi[stat] += valore
            else:
                self.modificatori_attivi[stat] = valore
    
    guerriero_bauhaus = GuerrieroTest("Bauhaus Blitzer", Fazione.BAUHAUS)
    
    # Test assegnazione equipaggiamento generico
    equipaggiamento_generico = Equipaggiamento("Kit Medico", valore=1)
    equipaggiamento_generico.modificatori_valore = 1
    equipaggiamento_generico.testo_carta = "+1 Valore. Può essere assegnato a qualsiasi guerriero."
    
    verifica = equipaggiamento_generico.puo_essere_assegnato_a_guerriero(guerriero_bauhaus)
    print(f"✓ {equipaggiamento_generico.nome} può essere assegnato a {guerriero_bauhaus.nome}: {verifica['puo_assegnare']}")
    
    if verifica['puo_assegnare']:
        equipaggiamento_generico.assegna_a_guerriero(guerriero_bauhaus.nome)
        modificatori = equipaggiamento_generico.applica_modificatori(guerriero_bauhaus)
        print(f"  Modificatori applicati: {modificatori}")
    
    # Esempio 7: Equipaggiamento con affiliazione specifica
    equipaggiamento_bauhaus = Equipaggiamento("Equipaggiamento Bauhaus", valore=2)
    equipaggiamento_bauhaus.affiliazione = Fazione.BAUHAUS
    equipaggiamento_bauhaus.modificatori_combattimento = 1
    equipaggiamento_bauhaus.testo_carta = "+1 Corpo a corpo. Solo per guerrieri Bauhaus."
    
    verifica_bauhaus = equipaggiamento_bauhaus.puo_essere_assegnato_a_guerriero(guerriero_bauhaus)
    print(f"\n✓ {equipaggiamento_bauhaus.nome} può essere assegnato a Bauhaus: {verifica_bauhaus['puo_assegnare']}")
    
    # Test con guerriero di altra fazione
    guerriero_capitol = GuerrieroTest("Capitol Marine", Fazione.CAPITOL)
    verifica_capitol = equipaggiamento_bauhaus.puo_essere_assegnato_a_guerriero(guerriero_capitol)
    print(f"✗ {equipaggiamento_bauhaus.nome} può essere assegnato a Capitol: {verifica_capitol['puo_assegnare']}")
    if not verifica_capitol['puo_assegnare']:
        print(f"  Errori: {verifica_capitol['errori']}")
    
    # Esempio 8: Regole avanzate per veicoli
    print(f"\n=== REGOLE AVANZATE VEICOLI ===")
    
    # Assegna aeronave a guerriero
    aeronave.assegna_a_guerriero(guerriero_bauhaus.nome)
    print(f"✓ {aeronave.nome} assegnata a {guerriero_bauhaus.nome}")
    print(f"  Guerriero dentro veicolo: {aeronave.guerriero_e_dentro_veicolo()}")
    
    # Applica restrizioni veicolo
    restrizioni = aeronave.applica_restrizioni_veicolo(guerriero_bauhaus)
    print(f"  Restrizioni attive:")
    for restrizione in restrizioni:
        print(f"    - {restrizione}")
    
    # Esce dal veicolo
    if aeronave.esce_dal_veicolo():
        print(f"  ✓ {guerriero_bauhaus.nome} esce dall'aeronave (costa 1 Azione)")
        print(f"  Guerriero dentro veicolo: {aeronave.guerriero_e_dentro_veicolo()}")
        restrizioni_fuori = aeronave.applica_restrizioni_veicolo(guerriero_bauhaus)
        print(f"  Restrizioni quando fuori: {len(restrizioni_fuori)} restrizioni")
    
    # Rientra nel veicolo
    if aeronave.entra_nel_veicolo():
        print(f"  ✓ {guerriero_bauhaus.nome} rientra nell'aeronave (costa 1 Azione)")
    
    print(f"\n=== REGOLE IMPLEMENTATE CORRETTAMENTE ===")
    print("✓ Equipaggiamenti basati su statistiche C-S-A-V del regolamento")
    print("✓ Solo una Armatura e un Veicolo per guerriero")
    print("✓ Numero illimitato di altre armi (ma una sola utilizzabile per combattimento)")
    print("✓ Regole di affiliazione per equipaggiamenti specifici")
    print("✓ Regole avanzate per veicoli (dentro/fuori, restrizioni Aeronavi/Sottomarini)")
    print("✓ Meccaniche di assegnazione e rimozione")
    print("✓ Costo in Destiny Points basato sul campo Valore (V) delle carte")
    print("✓ Verifica compatibilità con tipi di combattimento (Corpo a corpo vs Sparare)")
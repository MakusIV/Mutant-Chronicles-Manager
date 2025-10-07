"""
Modulo per la rappresentazione delle carte Guerriero di Mutant Chronicles/Doomtrooper
Versione corretta - Implementa le regole ufficiali del gioco

"""

from enum import Enum
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
import json

class Set_Espansione(Enum):
    """Espansioni disponibili nel gioco"""
    BASE = "Base"
    INQUISITION = "Inquisition" 
    WARZONE = "Warzone"
    MORTIFICATOR = "Mortificator"
    GOLGOTHA = "Golgotha"
    APOCALYPSE = "Apocalypse"

class Fazione(Enum):
    """Fazioni disponibili nel gioco"""
    IMPERIALE = "Imperiale"
    BAUHAUS = "Bauhaus" 
    MISHIMA = "Mishima"
    CAPITOL = "Capitol"
    CYBERTRONIC = "Cybertronic"
    FRATELLANZA = "Fratellanza"
    OSCURA_LEGIONE = "Oscura Legione"  # Corretto da "OSCURA_LEGIONE"
    MERCENARIO = "Mercenario"
    GENERICA = "Generica"

class TipoGuerriero(Enum):
    """Tipi di guerriero"""
    NORMALE = "Normale"
    PERSONALITA = "Personalita"  # Corretto encoding
    WARLORD = "Warlord"
    SEGUACE = "Seguace"    
    APOSTOLO = "Apostolo"
    INQUISITORE = "Inquisitore"
    CACCIATORE_OSCURO = "Cacciatore Oscuro"
    MORTIFICATOR = "Mortificator"  # Aggiunto per regole speciali
    ERETICO = "Eretico"
    

class DisciplinaArte(Enum):
    """Discipline dell'Arte secondo il regolamento"""
    CAMBIAMENTO = "Cambiamento"
    ELEMENTI = "Elementi"
    ESORCISMO = "Esorcismo"
    CINETICA = "Cinetica"
    MANIPOLAZIONE = "Manipolazione"
    MENTALE = "Mentale"
    PREMONIZIONE = "Premonizione"
    EVOCAZIONE = "Evocazione"
    TUTTE = "Tutte le Discipline"

class DisciplinaArte_old(Enum):
    """Discipline dell'Arte secondo il regolamento"""
    CAMBIAMENTO = "Arte del Cambiamento"
    ELEMENTI = "Arte degli Elementi"
    ESORCISMO = "Arte dell'Esorcismo"
    CINETICA = "Arte della Cinetica"
    MANIPOLAZIONE = "Arte della Manipolazione"
    MENTALE = "Arte Mentale"
    PREMONIZIONE = "Arte della Premonizione"
    EVOCAZIONE = "Arte d'Evocazione"
    TUTTE = "Tutte le Discipline"

class TipoOscuraSimmetria(Enum):
    """Tipi di carte Oscura Simmetria"""
    GENERICA = "Generica"
    DONO_APOSTOLO = "Dono degli Apostoli"
    DONO_OSCURA_SIMMETRIA = "Dono dell'Oscura Simmetria"
    DONO_OSCURA_LEGIONE = "Dono dell'Oscura Legione"
   

class ApostoloOscuraSimmetria(Enum):
    """Apostoli Padri dell'Oscura Simmetria"""
    ALGEROTH = "Algeroth"      # Apostolo della Guerra
    SEMAI = "Semai"            # Apostolo della Peste
    MUAWIJHE = "Muawijhe"      # Apostolo delle Mutazioni
    ILIAN = "Ilian"            # Apostolo del Vuoto
    DEMNOGONIS = "Demnogonis"  # Apostolo della Follia
    NESSUNO = None        # Per carte generiche


class CorporazioneSpecifica(Enum):
    DOOMTROOPER = "Doomtrooper"
    ERETICI = "Eretici"
    CULTISTI = "Cultisti"
    SEGUACI_DI_SEMAI = "Seguaci di Semai"
    SEGUACI_DI_ILIAN = "Seguaci di Ilian"
    SEGUACI_DI_DEMNOGONIS = "Seguaci di Demnogonis"
    SEGUACI_DI_MUAWIJHE = "Seguaci di Muawijhe"
    SEGUACI_DI_ALGEROTH = "Seguaci di Algeroth"
    
DOOMTROOPER = ["Bauhaus", "Mishima", "Cybertronic", "Imperiale", "Capitol", "Mercenario", "Fratellanza"]

class Rarity(Enum):
    """Rarità delle carte"""
    COMMON = "Common"
    UNCOMMON = "Uncommon" 
    RARE = "Rare"
    ULTRA_RARE = "Ultra Rare"
    PROMO = "Promo"


class AreaGioco(Enum):
    """Aree di gioco secondo il regolamento"""
    SQUADRA = "Squadra"          # Per Doomtrooper
    SCHIERAMENTO = "Schieramento"  # Per Oscura Legione
    AVAMPOSTO = "Avamposto"      # Per Tribù
    FUORI_GIOCO = "Fuori Gioco"


class StatoGuerriero(Enum):
    """Stati possibili del guerriero"""
    SANO = "Sano"
    FERITO = "Ferito"
    MORTO = "Morto"
    IN_COPERTURA = "In Copertura"


class ApostoloPadre(Enum):
    """Apostoli Padri dell'Oscura Simmetria"""
    ALGEROTH = "Algeroth"      # Apostolo della Guerra
    SEMAI = "Semai"            # Apostolo della Peste
    MUAWIJHE = "Muawijhe"      # Apostolo delle Mutazioni
    ILIAN = "Ilian"            # Apostolo del Vuoto
    DEMNOGONIS = "Demnogonis"  # Apostolo della Follia
    NESSUNO = "Nessuno"        # Per carte generiche

@dataclass
class Statistiche:
    """
    Statistiche base di un guerriero secondo il regolamento ufficiale
    C-S-A-V: Combattimento, Sparare, Armatura, Valore
    """
    combattimento: int = 0  # C - Combat (corpo a corpo)
    sparare: int = 0        # S - Shooting (armi da fuoco) - CORRETTO da "forza"
    armatura: int = 0       # A - Armor (protezione)
    valore: int = 0         # V - Value (Destiny Points/Promotion Points)



@dataclass  
class Abilita:
    """Rappresenta un'abilità speciale di un guerriero"""
    nome: str
    descrizione: str
    tipo: str = ""  # es. "Attacco", "Difesa", "Speciale", etc.
    costo_destino: int = 0  # costo in punti destino per attivare l'abilità
    target: str = ""  # chi può essere targetato
    timing: str = ""  # quando può essere usata


class Guerriero:
    """
    Classe principale per rappresentare una carta Guerriero di Mutant Chronicles/Doomtrooper
    Versione corretta implementa le regole ufficiali del gioco
    """
    
    def __init__(self, nome: str, fazione: Fazione, 
                 combattimento: int = 0, sparare: int = 0, 
                 armatura: int = 0, valore: int = 0):
        """
        Inizializza un nuovo Guerriero
        
        Args:
            nome: Nome del guerriero
            fazione: Fazione di appartenenza
            combattimento: Statistica Combattimento (C) - corpo a corpo
            sparare: Statistica Sparare (S) - armi da fuoco
            armatura: Statistica Armatura (A) - protezione
            valore: Statistica Valore (V) - Destiny Points e Promotion Points
        """
        self.nome = nome
        self.fazione = fazione
        self.stats = Statistiche(combattimento, sparare, armatura, valore)
        
        # Attributi di gioco
        self.tipo = TipoGuerriero.NORMALE
        self.rarity = Rarity.COMMON
        
        # Abilità e testo della carta
        self.abilita: List[Abilita] = [] # La capacità di lanciare incantesimi dell'arte è definita qui
        self.testo_carta = ""
        self.flavour_text = ""
        
        # Attributi per espansioni
        self.set_espansione = Set_Espansione.BASE
        self.numero_carta = ""
        
        # Modificatori temporanei
        self.modificatori_attivi: Dict[str, int] = {}
        
        # Stato in gioco secondo il regolamento
        self.area_gioco = AreaGioco.FUORI_GIOCO
        self.stato = StatoGuerriero.SANO
        self.pronto = True  # può agire questo turno
        self.in_copertura = False
        self.bonus_copertura = 3  # +3 Armatura in copertura
        
        # Equipaggiamento e allegati
        self.equipaggiamento: List[str] = []
        self.allegati: List[str] = []
        self.veicolo_assegnato: Optional[str] = None
        self.dentro_veicolo = False  # Stato dentro/fuori veicolo
        
        # Attributi speciali per espansioni
        self.keywords: List[str] = [] # la specificazione di essere un seguace di un determinato apostolo è definita qui    " Seguace di Algeroth", etc.    
        self.restrizioni: List[str] = []
        
        # Gestione Personalità
        self.e_personalita = False
        self.quantita = 0
        self.quantita_minima_consigliata = 0  # utilizzata per la creazione del mazzo
        self.fondamentale = False  # utilizzata per la creazione del mazzo: indica se la carta è importante per la preparazione del mazzo (es. personaggi unici, carte speciali fondamentali)

    def get_costo_destino(self) -> int:
        """
        Restituisce il costo in Destiny Points per giocare questa carta
        """
        return self.stats.valore
    
    def get_punti_promozione(self) -> int:
        """
        Restituisce i Promotion Points guadagnati eliminando questa carta
        """
        return self.stats.valore
        
    def aggiungi_abilita(self, nome: str, descrizione: str, 
                        tipo: str = "", costo_destino: int = 0,
                        target: str = "", timing: str = "") -> None:
        """Aggiunge un'abilità al guerriero"""
        abilita = Abilita(nome, descrizione, tipo, costo_destino, target, timing)
        self.abilita.append(abilita)
    
    def get_combattimento_totale(self) -> int:
        """Restituisce il valore di combattimento con modificatori"""
        base = self.stats.combattimento
        modificatori = self.modificatori_attivi.get('combattimento', 0)
        return max(0, base + modificatori)  # Non può andare sotto 0
    
    def get_sparare_totale(self) -> int:
        """Restituisce il valore di sparare con modificatori"""
        base = self.stats.sparare
        modificatori = self.modificatori_attivi.get('sparare', 0)
        return max(0, base + modificatori)
        
    def get_armatura_totale(self) -> int:
        """Restituisce il valore di armatura con modificatori e bonus copertura"""
        base = self.stats.armatura
        modificatori = self.modificatori_attivi.get('armatura', 0)
        bonus_copertura = self.bonus_copertura if self.in_copertura else 0
        return max(0, base + modificatori + bonus_copertura)
        
    def get_valore_totale(self) -> int:
        """Restituisce il valore con modificatori"""
        base = self.stats.valore
        modificatori = self.modificatori_attivi.get('valore', 0)
        return max(1, base + modificatori)  # Minimo 1
    
    def applica_modificatore(self, stat: str, valore: int) -> None:
        """Applica un modificatore temporaneo a una statistica"""
        statistiche_valide = ['combattimento', 'sparare', 'armatura', 'valore']
        if stat in statistiche_valide:
            if stat in self.modificatori_attivi:
                self.modificatori_attivi[stat] += valore
            else:
                self.modificatori_attivi[stat] = valore
    
    def rimuovi_modificatori(self) -> None:
        """Rimuove tutti i modificatori temporanei"""
        self.modificatori_attivi.clear()
    
    def ha_keyword(self, keyword: str) -> bool:
        """Controlla se il guerriero ha una specifica keyword"""
        return keyword.lower() in [k.lower() for k in self.keywords]
    
    def puo_essere_equipaggiato(self, equipaggiamento: str) -> bool:
        """Controlla se può equipaggiare un determinato oggetto"""
        # Regole base del regolamento
        if "Veicolo" in equipaggiamento and self.veicolo_assegnato:
            return False  # Un guerriero può avere solo un veicolo
        if "Armatura" in equipaggiamento and len([e for e in self.equipaggiamento if "Armatura" in e]) > 0:
            return False  # Un guerriero può avere solo un'armatura
        return True
    
    def equipaggia(self, nome_equipaggiamento: str) -> bool:
        """Equipaggia un oggetto se possibile"""
        if self.puo_essere_equipaggiato(nome_equipaggiamento):
            self.equipaggiamento.append(nome_equipaggiamento)
            if "Veicolo" in nome_equipaggiamento:
                self.veicolo_assegnato = nome_equipaggiamento
                self.dentro_veicolo = False  # Inizialmente fuori dal veicolo
            return True
        return False
    
    def entra_nel_veicolo(self) -> bool:
        """Entra nel veicolo assegnato (costa 1 azione)"""
        if self.veicolo_assegnato and not self.dentro_veicolo and not self.in_copertura:
            self.dentro_veicolo = True
            return True
        return False
    
    def esce_dal_veicolo(self) -> bool:
        """Esce dal veicolo assegnato (costa 1 azione)"""
        if self.veicolo_assegnato and self.dentro_veicolo:
            self.dentro_veicolo = False
            return True
        return False
    
    def puo_attaccare(self, bersaglio: 'Guerriero') -> Dict[str, Any]:
        """
        Verifica se può attaccare il bersaglio secondo le regole del regolamento
        """
        risultato = {"puo_attaccare": True, "motivo": ""}
        
        # Regole di affiliazione dal regolamento
        if self.fazione == Fazione.FRATELLANZA:
            # Fratellanza può attaccare solo Oscura Legione (eccetto Mortificator)
            if bersaglio.fazione != Fazione.OSCURA_LEGIONE:
                risultato["puo_attaccare"] = False
                risultato["motivo"] = "Fratellanza può attaccare solo Oscura Legione"
            elif bersaglio.tipo == TipoGuerriero.MORTIFICATOR:
                risultato["puo_attaccare"] = False
                risultato["motivo"] = "Fratellanza non può attaccare Mortificator"
        
        elif self.tipo == TipoGuerriero.MORTIFICATOR:
            # Mortificator possono attaccare chiunque
            pass
        
        elif self.fazione == Fazione.OSCURA_LEGIONE:
            # Oscura Legione può attaccare chiunque
            pass
        
        elif self.fazione in [Fazione.IMPERIALE, Fazione.BAUHAUS, Fazione.MISHIMA, 
                              Fazione.CAPITOL, Fazione.CYBERTRONIC]:
            # Doomtrooper non possono attaccare stessa corporazione o Fratellanza
            if bersaglio.fazione == self.fazione:
                risultato["puo_attaccare"] = False
                risultato["motivo"] = "Non può attaccare la stessa corporazione"
            elif bersaglio.fazione == Fazione.FRATELLANZA and bersaglio.tipo != TipoGuerriero.MORTIFICATOR:
                risultato["puo_attaccare"] = False
                risultato["motivo"] = "Doomtrooper non può attaccare Fratellanza"
        
        # Verifica stato del guerriero
        if self.stato != StatoGuerriero.SANO and self.stato != StatoGuerriero.FERITO:
            risultato["puo_attaccare"] = False
            risultato["motivo"] = "Guerriero non in condizioni di attaccare"
        
        if not self.pronto:
            risultato["puo_attaccare"] = False
            risultato["motivo"] = "Guerriero non pronto"
        
        # Verifica aree di gioco
        if self.area_gioco == AreaGioco.AVAMPOSTO and bersaglio.area_gioco != AreaGioco.AVAMPOSTO:
            risultato["puo_attaccare"] = False
            risultato["motivo"] = "Dall'Avamposto si può attaccare solo altri guerrieri nell'Avamposto"
        
        elif self.area_gioco != AreaGioco.AVAMPOSTO and bersaglio.area_gioco == AreaGioco.AVAMPOSTO:
            risultato["puo_attaccare"] = False
            risultato["motivo"] = "Non si può attaccare direttamente l'Avamposto"
        
        return risultato
    
    def attacca(self, difensore: 'Guerriero', tattica: str = "C") -> Dict[str, Any]:
        """
        Esegue un attacco secondo le regole ufficiali del regolamento
        
        Args:
            difensore: Guerriero difensore
            tattica: "C" per Corpo a Corpo, "S" per Sparare
        """
        # Verifica preliminari
        verifica_attacco = self.puo_attaccare(difensore)
        if not verifica_attacco["puo_attaccare"]:
            return {"errore": verifica_attacco["motivo"]}
        
        if tattica not in ["C", "S"]:
            return {"errore": "Tattica deve essere 'C' (Corpo a Corpo) o 'S' (Sparare)"}
        
        # Verifica restrizioni veicoli per corpo a corpo
        if tattica == "C":
            if (self.dentro_veicolo and self.veicolo_assegnato and 
                any(tipo in self.veicolo_assegnato for tipo in ["Aeronave", "Sottomarino"])):
                return {"errore": "Non può attaccare corpo a corpo da Aeronave/Sottomarino"}
            
            if (difensore.dentro_veicolo and difensore.veicolo_assegnato and 
                any(tipo in difensore.veicolo_assegnato for tipo in ["Aeronave", "Sottomarino"])):
                return {"errore": "Non può attaccare corpo a corpo guerriero in Aeronave/Sottomarino"}
        
        # Determina valori di attacco
        if tattica == "C":
            valore_attacco_attaccante = self.get_combattimento_totale()
            valore_attacco_difensore = difensore.get_combattimento_totale()
        else:  # tattica == "S"
            valore_attacco_attaccante = self.get_sparare_totale()
            valore_attacco_difensore = difensore.get_sparare_totale()
        
        valore_difesa_attaccante = self.get_armatura_totale()
        valore_difesa_difensore = difensore.get_armatura_totale()
        
        # COMBATTIMENTO SIMULTANEO secondo il regolamento
        attaccante_colpisce = valore_attacco_attaccante >= valore_difesa_difensore
        difensore_colpisce = valore_attacco_difensore >= valore_difesa_attaccante
        
        risultato = {
            "tattica": tattica,
            "attaccante": self.nome,
            "difensore": difensore.nome,
            "valore_attacco_attaccante": valore_attacco_attaccante,
            "valore_difesa_difensore": valore_difesa_difensore,
            "valore_attacco_difensore": valore_attacco_difensore,
            "valore_difesa_attaccante": valore_difesa_attaccante,
            "attaccante_colpisce": attaccante_colpisce,
            "difensore_colpisce": difensore_colpisce,
            "punti_promozione_attaccante": 0,
            "punti_promozione_difensore": 0
        }
        
        # Applica ferite/eliminazioni SIMULTANEAMENTE
        if attaccante_colpisce:
            punti_guadagnati = difensore.subisci_ferita()
            risultato["punti_promozione_attaccante"] = punti_guadagnati
        
        if difensore_colpisce:
            punti_guadagnati = self.subisci_ferita()
            risultato["punti_promozione_difensore"] = punti_guadagnati
        
        # Il guerriero diventa non pronto dopo l'attacco
        self.pronto = False
        
        return risultato
    
    def subisci_ferita(self) -> int:
        """
        Subisce una ferita secondo le regole del regolamento
        Returns: Punti Promozione guadagnati da chi ha inflitto la ferita (0 se solo ferito)
        """
        if self.stato == StatoGuerriero.SANO:
            # Da sano a ferito
            self.stato = StatoGuerriero.FERITO
            return 0  # Non si guadagnano punti per ferire
        
        elif self.stato == StatoGuerriero.FERITO:
            # Da ferito a morto
            self.stato = StatoGuerriero.MORTO
            self.area_gioco = AreaGioco.FUORI_GIOCO
            punti = self.get_punti_promozione()
            self.esce_dal_gioco()
            return punti
        
        return 0
    
    def guarisci(self) -> bool:
        """Guarisce il guerriero se ferito"""
        if self.stato == StatoGuerriero.FERITO:
            self.stato = StatoGuerriero.SANO
            return True
        return False
    
    def vai_in_copertura(self) -> bool:
        """Manda il guerriero in copertura (+3 Armatura)"""
        if not self.in_copertura and self.area_gioco != AreaGioco.FUORI_GIOCO:
            self.in_copertura = True
            if self.dentro_veicolo:
                self.esce_dal_veicolo()  # Non può essere in copertura dentro un veicolo
            return True
        return False
    
    def esci_da_copertura(self) -> bool:
        """Fa uscire il guerriero dalla copertura"""
        if self.in_copertura:
            self.in_copertura = False
            return True
        return False
    
    def entra_in_gioco(self, area: AreaGioco, giocatore_destiny_points: int) -> bool:
        """
        Il guerriero entra in gioco nell'area specificata
        """
        costo = self.get_costo_destino()
        if giocatore_destiny_points >= costo:
            self.area_gioco = area
            self.stato = StatoGuerriero.SANO
            self.pronto = True
            self.in_copertura = False
            return True
        return False
    
    def trasferisci_area(self, nuova_area: AreaGioco) -> Dict[str, Any]:
        """
        Trasferisce il guerriero a una nuova area secondo le regole
        """
        risultato = {"successo": False, "costo_azioni": 0, "errori": []}
        
        # Verifica regole di trasferimento
        if self.area_gioco == AreaGioco.AVAMPOSTO and nuova_area != AreaGioco.AVAMPOSTO:
            # Tribù non possono lasciare l'Avamposto
            if any(tribu in self.keywords for tribu in ["Crescentian", "Figli di Rasputin", "Templari", "Triade Luterana"]):
                risultato["errori"].append("I guerrieri delle Tribù non possono lasciare l'Avamposto")
                return risultato
        
        # Calcola costo in azioni
        costo_base = 1
        if self.veicolo_assegnato:
            costo_base = 2  # Trasferimento con veicolo costa 2 azioni
        
        risultato["costo_azioni"] = costo_base
        
        # Esegui trasferimento
        self.area_gioco = nuova_area
        risultato["successo"] = True
        
        return risultato
    
    def esce_dal_gioco(self) -> int:
        """
        Il guerriero esce dal gioco
        """
        self.area_gioco = AreaGioco.FUORI_GIOCO
        self.stato = StatoGuerriero.MORTO
        self.rimuovi_modificatori()
        self.equipaggiamento.clear()
        self.allegati.clear()
        self.veicolo_assegnato = None
        self.dentro_veicolo = False
        return self.get_punti_promozione()
    
    def ripristina(self) -> None:
        """Ripristina il guerriero per il nuovo turno"""
        self.pronto = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte il guerriero in un dizionario per serializzazione"""
        return {
            "nome": self.nome,
            "fazione": self.fazione.value,
            "tipo": self.tipo.value,
            "rarity": self.rarity.value,
            "set_espansione": self.set_espansione,
            "numero_carta": self.numero_carta,
            "stats": {
                "combattimento": self.stats.combattimento,
                "sparare": self.stats.sparare,  # Corretto da "forza"
                "armatura": self.stats.armatura,
                "valore": self.stats.valore
            },
            "abilita": [
                {
                    "nome": ab.nome,
                    "descrizione": ab.descrizione,
                    "tipo": ab.tipo,
                    "costo_destino": ab.costo_destino,
                    "target": ab.target,
                    "timing": ab.timing
                } for ab in self.abilita
            ],
            "testo_carta": self.testo_carta,
            "flavour_text": self.flavour_text,
            "keywords": self.keywords,
            "restrizioni": self.restrizioni,
            "equipaggiamento": self.equipaggiamento,
            "stato_gioco": {
                "area_gioco": self.area_gioco.value,
                "stato": self.stato.value,
                "pronto": self.pronto,
                "in_copertura": self.in_copertura,
                "dentro_veicolo": self.dentro_veicolo,
                "veicolo_assegnato": self.veicolo_assegnato
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Guerriero':
        """Crea un Guerriero da un dizionario"""
        stats = data["stats"]
        
        # Gestisce sia il formato vecchio che nuovo
        sparare_value = stats.get("sparare", stats.get("forza", 0))
        
        guerriero = cls(
            nome=data["nome"],
            fazione=Fazione(data["fazione"]),
            combattimento=stats["combattimento"],
            sparare=sparare_value,  # Usa sparare o forza come fallback
            armatura=stats["armatura"],
            valore=stats["valore"]
        )
        
        guerriero.tipo = TipoGuerriero(data["tipo"])
        guerriero.rarity = Rarity(data["rarity"])
        guerriero.set_espansione = data["set_espansione"]
        guerriero.numero_carta = data["numero_carta"]
        guerriero.testo_carta = data["testo_carta"]
        guerriero.flavour_text = data["flavour_text"]
        guerriero.keywords = data["keywords"]
        guerriero.restrizioni = data["restrizioni"]
        guerriero.equipaggiamento = data["equipaggiamento"]
        guerriero.quantita = data.get("quantita", 0)
        guerriero.quantita_minima_consigliata = data.get("quantita_minima_consigliata", 0)
        guerriero.fondamentale = data.get("fondamentale", False)
        
        # Ripristina stato di gioco (con compatibilità)
        stato = data["stato_gioco"]
        if "area_gioco" in stato:
            guerriero.area_gioco = AreaGioco(stato["area_gioco"])
        else:
            # Compatibilità con formato vecchio
            guerriero.area_gioco = AreaGioco.SQUADRA if stato.get("in_gioco", False) else AreaGioco.FUORI_GIOCO
        
        if "stato" in stato:
            guerriero.stato = StatoGuerriero(stato["stato"])
        else:
            # Compatibilità con formato vecchio
            guerriero.stato = StatoGuerriero.FERITO if stato.get("ferito", False) else StatoGuerriero.SANO
        
        guerriero.pronto = stato.get("pronto", True)
        guerriero.in_copertura = stato.get("in_copertura", False)
        guerriero.dentro_veicolo = stato.get("dentro_veicolo", False)
        guerriero.veicolo_assegnato = stato.get("veicolo_assegnato")
        
        # Ricostruisce abilità
        for ab_data in data["abilita"]:
            guerriero.aggiungi_abilita(
                ab_data["nome"],
                ab_data["descrizione"],
                ab_data["tipo"],
                ab_data["costo_destino"],
                ab_data["target"],
                ab_data["timing"]
            )
        
        return guerriero
    
    def __str__(self) -> str:
        """Rappresentazione stringa del guerriero"""
        area_str = f" [{self.area_gioco.value}]" if self.area_gioco != AreaGioco.FUORI_GIOCO else ""
        stato_str = f" ({self.stato.value})" if self.stato != StatoGuerriero.SANO else ""
        copertura_str = " [Coperto]" if self.in_copertura else ""
        veicolo_str = f" [in {self.veicolo_assegnato}]" if self.dentro_veicolo else ""
        
        return (f"{self.nome} ({self.fazione.value}){area_str}{stato_str}{copertura_str}{veicolo_str} - "
                f"C:{self.get_combattimento_totale()} "
                f"S:{self.get_sparare_totale()} "
                f"A:{self.get_armatura_totale()} "
                f"V:{self.get_valore_totale()}")
    
    def __repr__(self) -> str:
        return f"Guerriero('{self.nome}', {self.fazione}, {self.stats.combattimento}, {self.stats.sparare}, {self.stats.armatura}, {self.stats.valore})"


# Funzioni di utilità per creare guerrieri specifici delle espansioni

def crea_guerriero_base(nome: str, fazione: Fazione, c: int, s: int, a: int, v: int) -> Guerriero:
    """Crea un guerriero della versione base"""
    guerriero = Guerriero(nome, fazione, c, s, a, v)
    guerriero.set_espansione = Set_Espansione.BASE
    return guerriero

def crea_guerriero_inquisition(nome: str, fazione: Fazione, c: int, s: int, a: int, v: int) -> Guerriero:
    """Crea un guerriero dell'espansione Inquisition"""
    guerriero = Guerriero(nome, fazione, c, s, a, v)
    guerriero.set_espansione = Set_Espansione.INQUISITION
    return guerriero

def crea_guerriero_warzone(nome: str, fazione: Fazione, c: int, s: int, a: int, v: int) -> Guerriero:
    """Crea un guerriero dell'espansione Warzone"""
    guerriero = Guerriero(nome, fazione, c, s, a, v)
    guerriero.set_espansione = Set_Espansione.INQUISITION 
    return guerriero

def crea_personalita(nome: str, fazione: Fazione, c: int, s: int, a: int, v: int) -> Guerriero:
    """Crea una Personalità (unica)"""
    guerriero = Guerriero(nome, fazione, c, s, a, v)
    guerriero.tipo = TipoGuerriero.PERSONALITA
    guerriero.e_personalita = True
    guerriero.keywords.append("Personalità")
    guerriero.restrizioni.append("Unico - Solo una copia in gioco")
    return guerriero


# Esempi di utilizzo corretto

if __name__ == "__main__":
    # Esempio guerriero base - usando le statistiche corrette C-S-A-V
    blitzer = crea_guerriero_base("Bauhaus Blitzer", Fazione.BAUHAUS, 12, 12, 10, 4)
    blitzer.rarity = Rarity.COMMON
    blitzer.testo_carta = "Guerriero standard della Bauhaus"
    
    print("=== ESEMPIO CORRETTO ===")
    print(f"Guerriero: {blitzer}")
    print(f"Costo per giocare (Destiny Points): {blitzer.get_costo_destino()}")
    print(f"Punti Promozione se eliminato: {blitzer.get_punti_promozione()}")
    print(f"Statistiche C-S-A-V: {blitzer.stats.combattimento}-{blitzer.stats.sparare}-{blitzer.stats.armatura}-{blitzer.stats.valore}")
    
    # Esempio di entrata in gioco
    print(f"\n=== MECCANICA DI GIOCO ===")
    destiny_points_giocatore = 5
    print(f"Giocatore ha {destiny_points_giocatore} Destiny Points")
    
    if blitzer.entra_in_gioco(AreaGioco.SQUADRA, destiny_points_giocatore):
        print(f"✓ {blitzer.nome} entra in gioco nella Squadra (costa {blitzer.get_costo_destino()} DP)")
        destiny_points_giocatore -= blitzer.get_costo_destino()
        print(f"Destiny Points rimanenti: {destiny_points_giocatore}")
    
    # Esempio di combattimento con tattiche
    comandante = crea_guerriero_base("Comandante Elite", Fazione.IMPERIALE, 16, 14, 12, 8)
    comandante.entra_in_gioco(AreaGioco.SQUADRA, 10)
    
    print(f"\n=== COMBATTIMENTO CON TATTICHE ===")
    print(f"Blitzer (Bauhaus): C{blitzer.get_combattimento_totale()} S{blitzer.get_sparare_totale()} A{blitzer.get_armatura_totale()}")
    print(f"Comandante (Imperiale): C{comandante.get_combattimento_totale()} S{comandante.get_sparare_totale()} A{comandante.get_armatura_totale()}")
    
    # Test combattimento corpo a corpo
    risultato_c = blitzer.attacca(comandante, "C")
    if "errore" not in risultato_c:
        print(f"Combattimento Corpo a Corpo:")
        print(f"  Blitzer colpisce: {risultato_c['attaccante_colpisce']}")
        print(f"  Comandante colpisce: {risultato_c['difensore_colpisce']}")
        print(f"  PP Blitzer: {risultato_c['punti_promozione_attaccante']}")
        print(f"  PP Comandante: {risultato_c['punti_promozione_difensore']}")
    
    print(f"\n=== CORREZIONI APPLICATE ===")
    print("✓ Statistica 'forza' corretta in 'sparare' (S)")
    print("✓ Implementate tattiche di combattimento C/S")
    print("✓ Combattimenti simultanei")
    print("✓ Sistema ferite: Sano → Ferito → Morto")
    print("✓ Gestione aree: Squadra/Schieramento/Avamposto")
    print("✓ Regole copertura (+3 Armatura)")
    print("✓ Regole veicoli avanzate")
    print("✓ Restrizioni di attacco per fazione")
    print("✓ Encoding corretto per 'Personalità'")
    print("✓ Denominazione corretta 'Oscura Legione'")
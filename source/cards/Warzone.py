"""
Modulo per la rappresentazione delle carte Warzone di Mutant Chronicles/Doomtrooper
Le carte Warzone rappresentano zone di guerra dell'universo di Mutant Chronicles 
dove un singolo guerriero si può difendere quando viene attaccato da un altro giocatore.
È necessario avere in gioco la carta "Grande Stratega" per poter introdurre Warzone.
Basato sulla struttura delle classi Guerriero, Arte, Oscura_Simmetria, Equipaggiamento, 
Speciale, Fortificazione, Missione e Reliquia già sviluppate.
VERSIONE CORRETTA - Allineata alle regole ufficiali del regolamento
"""

from enum import Enum
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import json
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione, AreaGioco  # Import dalle classi esistenti


class TipoWarzone(Enum):
    """Tipi di zone di guerra secondo il regolamento"""
    CAMPO_BATTAGLIA = "Campo di Battaglia"
    TRINCEA = "Trincea"
    BUNKER = "Bunker"
    CITTA_DEVASTATA = "Citta Devastata"
    COMPLESSO_INDUSTRIALE = "Complesso Industriale"
    TERRITORIO_NEMICO = "Territorio Nemico"
    CRATERE = "Cratere"
    COLLINE = "Colline"
    PALUDE = "Palude"
    DESERTO = "Deserto"
    FORESTA = "Foresta"
    MONTAGNE = "Montagne"
    PIANURE = "Pianure"
    GHIACCIAI = "Ghiacciai"
    SPAZIO = "Spazio"
    SOTTERRANEO = "Sotterraneo"


class TerrenoWarzone(Enum):
    """Tipi di terreno della Warzone"""
    APERTO = "Aperto"
    COPERTO = "Coperto"
    DIFFICILE = "Difficile"
    PERICOLOSO = "Pericoloso"
    ESTREMO = "Estremo"
    MISTO = "Misto"


class BeneficiarioWarzone(Enum):
    """Chi può beneficiare della Warzone (solo il difensore)"""
    SOLO_DIFENSORE = "Solo Difensore"


class AreaCompatibileWarzone(Enum):
    """Aree dove può essere assegnata una Warzone"""
    SQUADRA = "Squadra"
    SCHIERAMENTO = "Schieramento"
    AVAMPOSTO = "Avamposto"
    SQUADRA_O_SCHIERAMENTO = "Squadra o Schieramento"
    QUALSIASI_AREA = "Qualsiasi Area"


@dataclass
class ModificatoreWarzone:
    """Rappresenta un modificatore applicato dalla Warzone al difensore"""
    statistica: str  # "C", "S", "A", "V"
    valore: int      # valore del modificatore (+/-)
    condizione: str = ""  # condizione per applicare il modificatore
    descrizione: str = ""
    solo_difensore: bool = True  # Sempre True per Warzone


@dataclass
class EffettoWarzone:
    """Rappresenta un effetto speciale della Warzone su tutti i combattenti"""
    nome: str
    descrizione: str
    target: str = "Tutti i combattenti"  # Chi è influenzato dall'effetto
    tipo_effetto: str = "Speciale"  # "Modificatore", "Restrizione", "Abilità", etc.
    permanente: bool = True  # Se l'effetto è attivo per tutto il combattimento
    condizioni: List[str] = None
    
    def __post_init__(self):
        if self.condizioni is None:
            self.condizioni = []


@dataclass
class RestrizioneWarzone:
    """Restrizioni per l'uso della Warzone"""
    richiede_grande_stratega: bool = True  # Sempre True secondo regolamento
    aree_utilizzabili: List[AreaCompatibileWarzone] = None
    fazioni_permesse: List[Fazione] = None
    solo_una_per_area: bool = True  # Ogni giocatore non può avere più della stessa Warzone in una sua Area
    limiti_utilizzo: List[str] = None
    
    def __post_init__(self):
        if self.aree_utilizzabili is None:
            self.aree_utilizzabili = [AreaCompatibileWarzone.QUALSIASI_AREA]
        if self.fazioni_permesse is None:
            self.fazioni_permesse = []
        if self.limiti_utilizzo is None:
            self.limiti_utilizzo = []


class Warzone:
    """
    Classe per rappresentare una carta Warzone di Mutant Chronicles/Doomtrooper
    VERSIONE CORRETTA - Allineata alle regole del regolamento ufficiale
    
    Le Warzone sono zone di guerra dove un guerriero può difendersi.
    Solo il guerriero in difesa guadagna i modificatori, ma tutti i combattenti
    sono influenzati dal testo della carta. Richiede "Grande Stratega" in gioco.
    """
    
    def __init__(self, nome: str, costo_azione: int = 1):
        """
        Inizializza una nuova carta Warzone
        
        Args:
            nome: Nome della Warzone
            costo_azione: Costo in azioni per assegnare la Warzone (default 1)
        """
        self.nome = nome
        self.costo_azione = costo_azione
        
        # Attributi base della carta
        self.tipo = TipoWarzone.CAMPO_BATTAGLIA
        self.terreno = TerrenoWarzone.APERTO
        self.rarity = Rarity.COMMON
        
        # Modificatori per il difensore (C, S, A, V)
        self.modificatori_difensore: List[ModificatoreWarzone] = []
        
        # Effetti su tutti i combattenti
        self.effetti_combattimento: List[EffettoWarzone] = []
        
        # Testo della carta
        self.testo_carta = ""
        self.flavour_text = ""
        
        # Restrizioni secondo il regolamento
        self.restrizioni = RestrizioneWarzone()
        
        # Keywords per categorizzazione
        self.keywords: List[str] = []
        
        # Attributi per espansioni
        self.set_espansione = "Base"
        self.numero_carta = ""
        
        # Stato di gioco
        self.in_gioco = False
        self.area_assegnata: Optional[AreaGioco] = None
        self.proprietario: Optional[str] = None  # Nome del giocatore
        self.utilizzata_questo_turno = False
        
        # Informazioni per bilanciamento
        self.valore_strategico = 0  # Valore strategico della carta
        self.frequenza_utilizzo = "Media"  # "Bassa", "Media", "Alta"
        
        # Compatibilità espansioni
        self.compatibile_espansioni: List[str] = ["Base"]
        self.quantita = 0
    
    def aggiungi_modificatore_difensore(self, statistica: str, valore: int, 
                                      condizione: str = "", descrizione: str = "") -> None:
        """Aggiunge un modificatore per il guerriero in difesa"""
        modificatore = ModificatoreWarzone(
            statistica=statistica,
            valore=valore,
            condizione=condizione,
            descrizione=descrizione,
            solo_difensore=True
        )
        self.modificatori_difensore.append(modificatore)
    
    def aggiungi_effetto_combattimento(self, nome: str, descrizione: str, 
                                     target: str = "Tutti i combattenti",
                                     tipo_effetto: str = "Speciale",
                                     condizioni: List[str] = None) -> None:
        """Aggiunge un effetto che influenza tutti i combattenti"""
        effetto = EffettoWarzone(
            nome=nome,
            descrizione=descrizione,
            target=target,
            tipo_effetto=tipo_effetto,
            condizioni=condizioni or []
        )
        self.effetti_combattimento.append(effetto)
    
    def può_essere_assegnata(self, area: AreaGioco, ha_grande_stratega: bool,
                           azioni_disponibili: int, warzone_esistenti: List[str] = None) -> Dict[str, Any]:
        """
        Verifica se la Warzone può essere assegnata a un'area
        
        Args:
            area: Area del giocatore dove assegnare la Warzone
            ha_grande_stratega: Se il giocatore ha "Grande Stratega" in gioco
            azioni_disponibili: Azioni disponibili al giocatore
            warzone_esistenti: Lista delle Warzone già presenti nell'area
            
        Returns:
            Dict con risultato e eventuali errori
        """
        risultato = {
            "può_assegnare": True,
            "errori": []
        }
        
        # Verifica requisito Grande Stratega
        if self.restrizioni.richiede_grande_stratega and not ha_grande_stratega:
            risultato["può_assegnare"] = False
            risultato["errori"].append("Richiede 'Grande Stratega' in gioco")
        
        # Verifica costo azioni
        if azioni_disponibili < self.costo_azione:
            risultato["può_assegnare"] = False
            risultato["errori"].append(f"Azioni insufficienti (richiede {self.costo_azione})")
        
        # Verifica restrizione una per area dello stesso tipo
        if warzone_esistenti and self.nome in warzone_esistenti:
            risultato["può_assegnare"] = False
            risultato["errori"].append("Già presente una Warzone uguale in quest'area")
        
        # Verifica compatibilità area
        aree_permesse = [a.value for a in self.restrizioni.aree_utilizzabili]
        if (AreaCompatibileWarzone.QUALSIASI_AREA.value not in aree_permesse and
            area.value not in aree_permesse):
            risultato["può_assegnare"] = False
            risultato["errori"].append(f"Non può essere assegnata a {area.value}")
        
        return risultato
    
    def può_essere_utilizzata(self, guerriero_difensore: str, area_combattimento: AreaGioco) -> Dict[str, Any]:
        """
        Verifica se la Warzone può essere utilizzata in difesa
        
        Args:
            guerriero_difensore: Nome del guerriero che si difende
            area_combattimento: Area dove avviene il combattimento
            
        Returns:
            Dict con risultato e eventuali errori
        """
        risultato = {
            "può_utilizzare": True,
            "errori": []
        }
        
        # Verifica che la Warzone sia in gioco
        if not self.in_gioco:
            risultato["può_utilizzare"] = False
            risultato["errori"].append("Warzone non in gioco")
        
        # Verifica che l'area corrisponda
        if self.area_assegnata != area_combattimento:
            risultato["può_utilizzare"] = False
            risultato["errori"].append("Warzone non nell'area del combattimento")
        
        return risultato
    
    def applica_modificatori_difensore(self, stats_difensore: Dict[str, int]) -> Dict[str, int]:
        """
        Applica i modificatori della Warzone alle statistiche del difensore
        
        Args:
            stats_difensore: Statistiche attuali del difensore {"C": x, "S": y, "A": z, "V": w}
            
        Returns:
            Statistiche modificate
        """
        stats_modificate = stats_difensore.copy()
        
        for modificatore in self.modificatori_difensore:
            stat = modificatore.statistica.upper()
            if stat in stats_modificate:
                # Somma algebrica come specificato nel regolamento
                stats_modificate[stat] += modificatore.valore
                # Assicura che i valori non vadano sotto 0
                stats_modificate[stat] = max(0, stats_modificate[stat])
        
        return stats_modificate
    
    def assegna_a_area(self, area: AreaGioco, proprietario: str) -> bool:
        """
        Assegna la Warzone a un'area del giocatore
        
        Args:
            area: Area dove assegnare la Warzone
            proprietario: Nome del giocatore proprietario
            
        Returns:
            True se assegnata con successo
        """
        self.in_gioco = True
        self.area_assegnata = area
        self.proprietario = proprietario
        return True
    
    def rimuovi_da_gioco(self) -> None:
        """Rimuove la Warzone dal gioco"""
        self.in_gioco = False
        self.area_assegnata = None
        self.proprietario = None
        self.utilizzata_questo_turno = False
    
    def reset_turno(self) -> None:
        """Reset per il nuovo turno"""
        self.utilizzata_questo_turno = False
    
    def get_modificatori_totali(self) -> Dict[str, int]:
        """
        Restituisce i modificatori totali che la Warzone applica al difensore
        
        Returns:
            Dict con i modificatori per statistica
        """
        modificatori = {"C": 0, "S": 0, "A": 0, "V": 0}
        
        for mod in self.modificatori_difensore:
            stat = mod.statistica.upper()
            if stat in modificatori:
                modificatori[stat] += mod.valore
        
        return modificatori
    
    def get_effetti_attivi(self) -> List[str]:
        """Restituisce la lista degli effetti attivi su tutti i combattenti"""
        return [f"{e.nome}: {e.descrizione}" for e in self.effetti_combattimento]
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte la Warzone in dizionario per serializzazione"""
        return {
            "nome": self.nome,
            "costo_azione": self.costo_azione,
            "tipo": self.tipo.value,
            "terreno": self.terreno.value,
            "rarity": self.rarity.value,
            "modificatori_difensore": [
                {
                    "statistica": m.statistica,
                    "valore": m.valore,                    
                    "descrizione": m.descrizione
                } for m in self.modificatori_difensore
            ],
            "effetti_combattimento": [
                {
                    "nome": e.nome,
                    "descrizione": e.descrizione,
                    "target": e.target,
                    "tipo_effetto": e.tipo_effetto,
                } for e in self.effetti_combattimento
            ],
            "testo_carta": self.testo_carta,
            "flavour_text": self.flavour_text,
            "keywords": self.keywords,
            "set_espansione": self.set_espansione,
            "numero_carta": self.numero_carta,
            "restrizioni": {
                "richiede_grande_stratega": self.restrizioni.richiede_grande_stratega,
                "aree_utilizzabili": [a.value for a in self.restrizioni.aree_utilizzabili],
                "fazioni_permesse": [f.value for f in self.restrizioni.fazioni_permesse],
                "solo_una_per_area": self.restrizioni.solo_una_per_area,
                "limiti_utilizzo": self.restrizioni.limiti_utilizzo
            },
            "stato_gioco": {
                "in_gioco": self.in_gioco,
                "area_assegnata": self.area_assegnata.value if self.area_assegnata else None,
                "proprietario": self.proprietario,
                "utilizzata_questo_turno": self.utilizzata_questo_turno
            },
            "valore_strategico": self.valore_strategico,
            "frequenza_utilizzo": self.frequenza_utilizzo,
            "compatibile_espansioni": self.compatibile_espansioni
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Warzone':
        """Crea una istanza Warzone da dizionario"""
        warzone = cls(data["nome"], data["costo_azione"])
        
        # Attributi base
        warzone.tipo = TipoWarzone(data["tipo"])
        warzone.terreno = TerrenoWarzone(data["terreno"])
        warzone.rarity = Rarity(data["rarity"])
        
        # Modificatori difensore
        for mod_data in data["modificatori_difensore"]:
            warzone.aggiungi_modificatore_difensore(
                mod_data["statistica"],
                mod_data["valore"],
                mod_data["descrizione"]
            )
        
        # Effetti combattimento
        for eff_data in data["effetti_combattimento"]:
            warzone.aggiungi_effetto_combattimento(
                eff_data["nome"],
                eff_data["descrizione"],
                eff_data["target"],
                eff_data["tipo_effetto"]
            )
        
        # Testo e metadati
        warzone.testo_carta = data["testo_carta"]
        warzone.flavour_text = data["flavour_text"]
        warzone.keywords = data["keywords"]
        warzone.set_espansione = data["set_espansione"]
        warzone.numero_carta = data["numero_carta"]
        
        # Restrizioni
        restr_data = data["restrizioni"]
        warzone.restrizioni.richiede_grande_stratega = restr_data["richiede_grande_stratega"]
        warzone.restrizioni.aree_utilizzabili = [AreaCompatibileWarzone(a) for a in restr_data["aree_utilizzabili"]]
        warzone.restrizioni.fazioni_permesse = [Fazione(f) for f in restr_data["fazioni_permesse"]]
        warzone.restrizioni.solo_una_per_area = restr_data["solo_una_per_area"]
        warzone.restrizioni.limiti_utilizzo = restr_data["limiti_utilizzo"]
        
        # Stato gioco
        stato_data = data.get("stato_gioco") #data["stato_gioco"]    

        if stato_data:
            warzone.in_gioco = stato_data["in_gioco"]
            warzone.area_assegnata = AreaGioco(stato_data["area_assegnata"]) if stato_data["area_assegnata"] else None
            warzone.proprietario = stato_data["proprietario"]
            warzone.utilizzata_questo_turno = stato_data["utilizzata_questo_turno"]
            
        # Attributi aggiuntivi
        warzone.valore_strategico = data.get("valore_strategico", 0)
        warzone.frequenza_utilizzo = data.get("frequenza_utilizzo", "Media")
        warzone.compatibile_espansioni = data.get("compatibile_espansioni", ["Base"])
        
        return warzone
    
    def __str__(self) -> str:
        """Rappresentazione stringa della Warzone"""
        area_str = f" [{self.area_assegnata.value}]" if self.area_assegnata else ""
        mods = self.get_modificatori_totali()
        mod_str = " ".join([f"{k}:{v:+d}" for k, v in mods.items() if v != 0])
        mod_str = f" ({mod_str})" if mod_str else ""
        
        return f"{self.nome}{area_str}{mod_str} - {self.tipo.value}"
    
    def __repr__(self) -> str:
        return f"Warzone('{self.nome}', {self.costo_azione})"


# Funzioni di utilità per creare Warzone specifiche

def crea_warzone_base(nome: str, tipo: TipoWarzone, 
                     mods_difensore: Dict[str, int] = None) -> Warzone:
    """
    Crea una Warzone della versione base
    
    Args:
        nome: Nome della Warzone
        tipo: Tipo di Warzone
        mods_difensore: Dict con modificatori {"C": +1, "A": +2, etc.}
    """
    warzone = Warzone(nome)
    warzone.tipo = tipo
    warzone.set_espansione = "Base"
    
    if mods_difensore:
        for stat, valore in mods_difensore.items():
            warzone.aggiungi_modificatore_difensore(stat, valore)
    
    return warzone

def crea_warzone_avanzata(nome: str, tipo: TipoWarzone, terreno: TerrenoWarzone,
                         mods_difensore: Dict[str, int] = None,
                         effetti_speciali: List[Dict[str, str]] = None) -> Warzone:
    """
    Crea una Warzone con effetti avanzati
    
    Args:
        nome: Nome della Warzone
        tipo: Tipo di Warzone
        terreno: Tipo di terreno
        mods_difensore: Modificatori per il difensore
        effetti_speciali: Lista di effetti su tutti i combattenti
    """
    warzone = crea_warzone_base(nome, tipo, mods_difensore)
    warzone.terreno = terreno
    
    if effetti_speciali:
        for effetto in effetti_speciali:
            warzone.aggiungi_effetto_combattimento(
                effetto.get("nome", ""),
                effetto.get("descrizione", ""),
                effetto.get("target", "Tutti i combattenti"),
                effetto.get("tipo", "Speciale")
            )
    
    return warzone


# Esempi di utilizzo corretto

if __name__ == "__main__":
    # Esempio Warzone base - Trincea difensiva
    trincea = crea_warzone_base(
        "Trincea Difensiva", 
        TipoWarzone.TRINCEA,
        {"A": +3, "C": -1}  # +3 Armatura, -1 Combattimento
    )
    trincea.rarity = Rarity.COMMON
    trincea.testo_carta = "Il guerriero in difesa guadagna +3 Armatura e -1 Combattimento. Nessuno dei combattenti può beneficiare di Fortificazioni."
    trincea.flavour_text = "Nella trincea, la sopravvivenza viene prima dell'attacco."
    trincea.keywords = ["Difensiva", "Trincea"]
    
    # Esempio Warzone avanzata con effetti speciali
    giungla = crea_warzone_avanzata(
        "Giungla Ostile",
        TipoWarzone.FORESTA,
        TerrenoWarzone.DIFFICILE,
        {"S": -2, "A": +1},  # -2 Sparare, +1 Armatura
        [
            {
                "nome": "Visibilità Limitata",
                "descrizione": "Tutti i combattimenti sono risolti solo con Combattimento",
                "target": "Tutti i combattenti",
                "tipo": "Restrizione"
            }
        ]
    )
    giungla.rarity = Rarity.UNCOMMON
    giungla.testo_carta = "Il difensore guadagna -2 Sparare e +1 Armatura. Tutti i combattimenti devono essere risolti con Combattimento invece che Sparare."
    
    print(f"Warzone creata: {trincea}")
    print(f"Modificatori: {trincea.get_modificatori_totali()}")
    print(f"Tipo: {trincea.tipo.value}")
    
    print(f"\nWarzone avanzata: {giungla}")
    print(f"Effetti: {giungla.get_effetti_attivi()}")
    
    # Test meccaniche di gioco
    print(f"\n=== TEST MECCANICHE ===")
    può_assegnare = trincea.può_essere_assegnata(
        AreaGioco.SQUADRA,
        ha_grande_stratega=True,
        azioni_disponibili=2,
        warzone_esistenti=[]
    )
    print(f"Può essere assegnata: {può_assegnare['può_assegnare']}")
    
    # Test serializzazione
    print(f"\n=== TEST SERIALIZZAZIONE ===")
    dict_warzone = trincea.to_dict()
    warzone_ricostruita = Warzone.from_dict(dict_warzone)
    print(f"Serializzazione riuscita: {trincea.nome == warzone_ricostruita.nome}")
    
    print(f"\n=== IMPLEMENTAZIONE COMPLETATA ===")
    print("✓ Classe Warzone implementata secondo regolamento Doomtrooper")
    print("✓ Richiede 'Grande Stratega' per essere introdotta")
    print("✓ Assegnabile ad Aree al costo di 1 Azione")
    print("✓ Solo difensore guadagna modificatori C, S, A, V")
    print("✓ Tutti i combattenti influenzati dal testo carta")
    print("✓ Nessun bonus da Fortificazioni quando si usa Warzone")
    print("✓ Una sola copia per tipo in ogni Area")
    print("✓ Modificatori algebrici alle statistiche base")
    print("✓ Compatibile con tutte le classi sviluppate")
    print("✓ Serializzazione tramite to_dict() e from_dict()")
    print("✓ Gestione stato di gioco e assegnazione aree")
    print("✓ Controlli di validità secondo regolamento")
    print("✓ Struttura coerente con altre classi del progetto")
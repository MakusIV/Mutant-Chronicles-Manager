"""
Modulo per la rappresentazione delle carte Oscura Simmetria di Mutant Chronicles/Doomtrooper
Include sia le carte generiche che i Doni degli Apostoli
Versione corretta secondo il regolamento ufficiale
"""

from enum import Enum
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import json
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione, ApostoloOscuraSimmetria, TipoOscuraSimmetria , TipoGuerriero # Corretto percorso import



class BersaglioOscura(Enum):
    """Possibili bersagli delle carte Oscura Simmetria"""
    GUERRIERO_PROPRIO = "Guerriero Proprio"
    GUERRIERO_AVVERSARIO = "Guerriero Avversario"
    QUALSIASI_GUERRIERO = "Qualsiasi Guerriero"
    GUERRIERO_ATTACCANTE = "Guerriero Attaccante"
    GUERRIERO_DIFENSORE = "Guerriero Difensore"
    ENTRAMBI_COMBATTENTI = "Entrambi i Combattenti"
    TUTTI_GUERRIERI = "Tutti i Guerrieri"
    TUTTI_GUERRIERI_PROPRI = "Tutti i Guerrieri Propri"
    TUTTI_GUERRIERI_AVVERSARI = "Tutti i Guerrieri Avversari"
    GUERRIERO_OSCURA_LEGIONE = "Guerriero Oscura Legione"  # Corretto nome
    GUERRIERO_NON_OSCURA_LEGIONE = "Guerriero Non-Oscura Legione"
    SEGUACE_APOSTOLO = "Seguace dell'Apostolo"
    GIOCATORE = "Giocatore"
    ENTRAMBI_GIOCATORI = "Entrambi i Giocatori"
    SENZA_BERSAGLIO = "Senza Bersaglio"
    GIOCATORE_AVVERSARIO = "Giocatore Avversario"
    COMBATTIMENTO = "Combattimento Corrente"
    MERCENARIO = "Mercenario"
    ERETICO = "Eretico"
    GUERRIERO_FRATELLANZA = "Guerriero della Fratellanza"
    DOOMTROOPER = "Doomtrooper"
    PERSONALITA = "Personalita"
    EQUIPAGGIAMENTO = "Equipaggiamento"
    NEFARITA = "Nefarita"

class DurataOscura(Enum):
    """Durata dell'effetto delle carte Oscura Simmetria"""
    ISTANTANEA = "Istantanea"
    PERMANENTE = "Permanente"
    FINO_FINE_TURNO = "Fino Fine Turno"
    FINO_PROSSIMO_TURNO = "Fino Prossimo Turno"
    CONTINUA = "Continua"
    FINO_ELIMINAZIONE = "Fino Eliminazione"
    ASSEGNATA = "Assegnata"  # Per doni permanenti
    FINO_FINE_COMBATTIMENTO = "Fino Fine Combattimento"
    DURANTE_COMBATTIMENTO = "Durante questo Combattimento"

    
class TimingOscura(Enum):
    """Quando può essere giocata una carta Oscura Simmetria"""
    TURNO_PROPRIO = "Turno Proprio"
    TURNO_AVVERSARIO = "Turno Avversario"    
    IN_OGNI_MOMENTO = "In Ogni Momento"
    IN_COMBATTIMENTO = "In Combattimento"
    PRIMA_COMBATTIMENTO = "Prima del Combattimento"
    DOPO_COMBATTIMENTO = "Dopo il Combattimento"
    QUANDO_FERITO = "Quando Ferito"
    QUANDO_ELIMINATO = "Quando Eliminato"
    DURANTE_MODIFICATORI = "Durante Modificatori Combattimento"
    IN_RISPOSTA = "In Risposta"
    DICHIARAZIONE_ATTACCO = "Dichiarazione Attacco"
    RISOLUZIONE_COMBATTIMENTO = "Risoluzione Combattimento"


@dataclass
class EffettoOscura:
    """Rappresenta l'effetto di una carta Oscura Simmetria"""
    tipo_effetto: str  # es. "Corruzione", "Modificatore", "Danno", "Controllo", "Mutazione"
    valore: int = 0  # valore numerico dell'effetto
    statistica_target: str = ""  # quale statistica viene modificata
    descrizione_effetto: str = ""
    condizioni: List[str] = None  # condizioni per attivare l'effetto
    effetti_collaterali: List[str] = None  # effetti negativi per chi gioca la carta
    
    def __post_init__(self):
        if self.condizioni is None:
            self.condizioni = []
        if self.effetti_collaterali is None:
            self.effetti_collaterali = []


class Oscura_Simmetria:
    """
    Classe per rappresentare una carta Oscura Simmetria di Mutant Chronicles/Doomtrooper
    Include sia le carte generiche che i Doni degli Apostoli
    Versione corretta secondo il regolamento ufficiale
    """
    
    def __init__(self, nome: str, costo_destino: int = 0, tipo: Optional[TipoOscuraSimmetria] = TipoOscuraSimmetria.GENERICA, rarity: Optional[Rarity] = Rarity.COMMON, apostolo_padre: Optional[ApostoloOscuraSimmetria] = ApostoloOscuraSimmetria.NESSUNO, set_espansione: Optional[str] = Set_Espansione.BASE):
        """
        Inizializza una nuova carta Oscura Simmetria
        
        Args:
            nome: Nome della carta
            costo_destino: Costo in Destiny Points per giocare la carta
        """
        self.nome = nome
        self.costo_destino = costo_destino
        
        # Attributi base della carta
        self.tipo = tipo
        self.rarity = rarity
        self.apostolo_padre = apostolo_padre
        
        # Meccaniche di gioco
        self.bersaglio = BersaglioOscura.SENZA_BERSAGLIO
        self.durata = DurataOscura.ISTANTANEA
        self.timing = TimingOscura.TURNO_PROPRIO
        
        # Effetti della carta
        self.effetti: List[EffettoOscura] = []
        
        # Testo della carta
        self.testo_carta = ""
        self.flavour_text = ""
        
        # Restrizioni e permessi secondo il regolamento
        self.fazioni_permesse: List[Fazione] = [Fazione.OSCURA_LEGIONE]  # Solo Oscura Legione
        self.restrizioni: List[str] = []
        self.keywords: List[str] = []
        
        # Attributi per espansioni
        self.set_espansione = set_espansione
        self.numero_carta = ""
        
        # Stato di gioco
        self.in_gioco = False  # per carte con effetto permanente o assegnate
        self.utilizzata = False
        self.bersagli_attuali: List[str] = []  # nomi dei guerrieri targetati
        self.assegnata_a: Optional[str] = None  # Per doni assegnati
        
        # Meccaniche speciali Oscura Simmetria
        self.corruzione_applicata: Dict[str, int] = {}  # traccia corruzione sui guerrieri
        self.mutazioni_applicate: Dict[str, List[str]] = {}  # traccia mutazioni
        self.penalita_giocatore: Dict[str, int] = {}  # penalità per chi gioca la carta
        
        # Contatori per effetti speciali
        self.contatori_oscura: Dict[str, int] = {}
        self.livello_corruzione = 0  # per alcune carte progressive
        
        # Gestione immunità
        self.puo_essere_negata = True  # Alcune carte non possono essere negate
        self.valore_strategico = 0
        self.quantita = 0
        self.quantita_minima_consigliata = 0  # per la creazione del mazzo
        self.fondamentale = False  # se la carta è fondamentale per il mazzo
        

    def puo_essere_associata_a_fazione(self, fazione: Fazione) -> bool:
        """
        Controlla se la carta può essere giocata dalla fazione specificata
        Secondo il regolamento: solo Oscura Legione può usare carte Oscura Simmetria
        """
        return fazione in self.fazioni_permesse
    
    def puo_essere_associata_a_guerriero(self, guerriero: Any) -> Dict[str, Any]:
        """
        Verifica se il dono può essere assegnato al guerriero
        Secondo il regolamento: solo guerrieri Oscura Legione, con controlli per seguaci specifici
        """
        risultato = {"puo_lanciare": True, "errori": []}
        
        # Deve essere della Fratellanza o fazione permessa
        if not self.puo_essere_associata_a_fazione(guerriero.fazione):
            risultato["puo_lanciare"] = False
            risultato["errori"].append(f"Solo {[f.value for f in self.fazioni_permesse]} possono usare l'Oscura Simmetria")
    
        if (self.tipo == TipoOscuraSimmetria.GENERICA or self.tipo == TipoOscuraSimmetria.DONO_OSCURA_SIMMETRIA or self.tipo == TipoOscuraSimmetria.DONO_OSCURA_LEGIONE ) and "Solo doni degli Apostoli" in guerriero.restrizioni:
            risultato["puo_lanciare"] = False
            risultato["errori"].append(f"Il guerriero {guerriero.nome} non può usare le carte generiche dell'Oscura Simmetria")
    
        # Verifica seguaci degli apostoli
        if self.tipo == TipoOscuraSimmetria.DONO_APOSTOLO and self.apostolo_padre != ApostoloOscuraSimmetria.NESSUNO and "Solo doni dell'Oscura Simmetria" not in guerriero.restrizioni:
            seguace_richiesto = f"Seguace di {self.apostolo_padre.value}"
            if seguace_richiesto not in guerriero.keywords:
                risultato["puo_assegnare"] = False
                risultato["errori"].append(f"Solo seguaci di {self.apostolo_padre.value} possono ricevere questo dono")

        if "Solo Eretici" in self.restrizioni and "Eretico" not in guerriero.keywords:
            risultato["puo_assegnare"] = False
            risultato["errori"].append("Solo Eretici")

        if "Solo Nefarita" in self.restrizioni and "Nefarita" not in guerriero.keywords:
            risultato["puo_assegnare"] = False
            risultato["errori"].append("Solo Nefarita")

        if "Non può essere usato su Personalita" in self.restrizioni and guerriero.tipo == TipoGuerriero.PERSONALITA:   
            risultato["puo_assegnare"] = False
            risultato["errori"].append("Solo Non Personalita")
        
        return risultato
    
    # funzione di gioco
    def puo_essere_assegnata_a_guerriero(self, guerriero: Any) -> Dict[str, Any]:
        """
        Verifica se il dono può essere assegnato al guerriero
        Secondo il regolamento: solo guerrieri Oscura Legione, con controlli per seguaci specifici
        """        
        return self.puo_essere_associata_a_guerriero(guerriero)     
    
    def aggiungi_fazione_permessa(self, fazione: Fazione) -> None:
        """
        Aggiunge una fazione che può giocare questa carta
        ATTENZIONE: Uso molto limitato secondo il regolamento
        """
        if fazione not in self.fazioni_permesse:
            self.fazioni_permesse.append(fazione)
            self.restrizioni.append(f"Eccezione regolamento: {fazione.value} può usare questa carta")
    
    def rimuovi_fazione_permessa(self, fazione: Fazione) -> None:
        """Rimuove una fazione dalle fazioni permesse"""
        if fazione in self.fazioni_permesse and len(self.fazioni_permesse) > 1:
            self.fazioni_permesse.remove(fazione)
    
    def aggiungi_effetto(self, tipo_effetto: str, valore: int = 0,
                        statistica_target: str = "", descrizione: str = "",
                        condizioni: List[str] = None, effetti_collaterali: List[str] = None) -> None:
        """Aggiunge un effetto alla carta Oscura Simmetria"""
        effetto = EffettoOscura(
            tipo_effetto=tipo_effetto,
            valore=valore,
            statistica_target=statistica_target,
            descrizione_effetto=descrizione,
            condizioni=condizioni or [],
            effetti_collaterali=effetti_collaterali or []
        )
        self.effetti.append(effetto)
    
    def ha_keyword(self, keyword: str) -> bool:
        """Controlla se la carta ha una specifica keyword"""
        return keyword.lower() in [k.lower() for k in self.keywords]
    
    def e_dono_apostolo(self, apostolo: ApostoloOscuraSimmetria) -> bool:
        """Controlla se la carta è un dono dell'apostolo specificato"""
        return self.tipo == TipoOscuraSimmetria.DONO_APOSTOLO and self.apostolo_padre == apostolo
    
    def richiede_bersaglio(self) -> bool:
        """Controlla se la carta richiede un bersaglio per essere giocata"""
        return self.bersaglio != BersaglioOscura.SENZA_BERSAGLIO
    
    def bersaglio_valido(self, bersaglio: str, guerrieri_propri: List[str],
                        guerrieri_avversari: List[str], fazioni_guerrieri: Dict[str, str]) -> bool:
        """
        Controlla se un bersaglio è valido per questa carta Oscura Simmetria
        
        Args:
            bersaglio: Nome del guerriero bersaglio
            guerrieri_propri: Lista dei nomi dei guerrieri propri in gioco
            guerrieri_avversari: Lista dei nomi dei guerrieri avversari in gioco
            fazioni_guerrieri: Dizionario nome_guerriero -> fazione
        """
        if self.bersaglio == BersaglioOscura.SENZA_BERSAGLIO:
            return True
        elif self.bersaglio == BersaglioOscura.GUERRIERO_OSCURA_LEGIONE:
            return (bersaglio in (guerrieri_propri + guerrieri_avversari) and
                   fazioni_guerrieri.get(bersaglio) == "Oscura Legione")
        elif self.bersaglio == BersaglioOscura.GUERRIERO_NON_OSCURA_LEGIONE:
            return (bersaglio in (guerrieri_propri + guerrieri_avversari) and
                   fazioni_guerrieri.get(bersaglio) != "Oscura Legione")
        elif self.bersaglio == BersaglioOscura.GUERRIERO_PROPRIO:
            return bersaglio in guerrieri_propri
        elif self.bersaglio == BersaglioOscura.GUERRIERO_AVVERSARIO:
            return bersaglio in guerrieri_avversari
        elif self.bersaglio == BersaglioOscura.QUALSIASI_GUERRIERO:
            return bersaglio in (guerrieri_propri + guerrieri_avversari)
        elif self.bersaglio == BersaglioOscura.SEGUACE_APOSTOLO:
            # Verifica se è seguace dell'apostolo appropriato
            return (bersaglio in (guerrieri_propri + guerrieri_avversari) and
                   self.apostolo_padre != ApostoloOscuraSimmetria.NESSUNO)
        else:
            # Per bersagli multipli, sarà gestito dalla logica di gioco
            return True
    
    def puo_essere_giocata(self, destiny_points: int, fazione_giocatore: Fazione,
                          timing_corrente: TimingOscura, condizioni_gioco: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Controlla se la carta può essere giocata nel momento attuale
        
        Args:
            destiny_points: Punti Destino disponibili del giocatore
            fazione_giocatore: Fazione del giocatore
            timing_corrente: Timing corrente del gioco
            condizioni_gioco: Condizioni aggiuntive del gioco
            
        Returns:
            Dizionario con risultato e eventuali errori
        """
        risultato = {"puo_giocare": True, "errori": [], "avvertimenti": []}
        
        # Controllo costo
        if destiny_points < self.costo_destino:
            risultato["puo_giocare"] = False
            risultato["errori"].append(f"Destiny Points insufficienti: richiesti {self.costo_destino}, disponibili {destiny_points}")
        
        # Controllo fazione
        if not self.puo_essere_giocata_da_fazione(fazione_giocatore):
            risultato["puo_giocare"] = False
            risultato["errori"].append(f"Fazione {fazione_giocatore.value} non può giocare questa carta")
        
        # Controllo timing
        if self.timing != TimingOscura.QUALSIASI_MOMENTO and self.timing != timing_corrente:
            risultato["puo_giocare"] = False
            risultato["errori"].append(f"Timing non corretto: richiesto {self.timing.value}, attuale {timing_corrente.value}")
        
        # Controllo se già utilizzata
        if self.utilizzata and self.durata == DurataOscura.ISTANTANEA:
            risultato["puo_giocare"] = False
            risultato["errori"].append("Carta già utilizzata")
        
        # Controllo se già assegnata (per doni)
        if self.durata == DurataOscura.ASSEGNATA and self.assegnata_a:
            risultato["puo_giocare"] = False
            risultato["errori"].append("Dono già assegnato a un guerriero")
        
        # Avvertimento per effetti collaterali
        for effetto in self.effetti:
            if effetto.effetti_collaterali:
                risultato["avvertimenti"].extend([
                    f"Effetto collaterale: {collaterale}" for collaterale in effetto.effetti_collaterali
                ])
        
        return risultato
    
    def applica_effetto(self, bersaglio: Union[str, List[str]],
                       guerrieri_in_gioco: Dict[str, Any],
                       giocatore_corrente: str) -> Dict[str, Any]:
        """
        Applica l'effetto della carta Oscura Simmetria
        
        Args:
            bersaglio: Nome/i del/i bersaglio/i
            guerrieri_in_gioco: Dizionario dei guerrieri in gioco
            giocatore_corrente: Nome del giocatore che gioca la carta
            
        Returns:
            Risultato dell'applicazione dell'effetto
        """
        risultato = {
            "successo": True,
            "effetti_applicati": [],
            "effetti_collaterali_applicati": [],
            "errori": [],
            "modificatori_applicati": {},
            "corruzione_applicata": {},
            "mutazioni_applicate": {}
        }
        
        # Determina i bersagli effettivi
        bersagli_effettivi = []
        if isinstance(bersaglio, str):
            bersagli_effettivi = [bersaglio] if bersaglio != "" else []
        else:
            bersagli_effettivi = bersaglio
        
        # Verifica immunità
        bersagli_validi = []
        for nome_bersaglio in bersagli_effettivi:
            if nome_bersaglio in guerrieri_in_gioco:
                guerriero = guerrieri_in_gioco[nome_bersaglio]
                if self._verifica_immunita(guerriero):
                    risultato["errori"].append(f"{nome_bersaglio} è immune all'Oscura Simmetria")
                else:
                    bersagli_validi.append(nome_bersaglio)
        
        # Applica ogni effetto
        for effetto in self.effetti:
            try:
                effetto_risultato = self._applica_singolo_effetto(
                    effetto, bersagli_validi, guerrieri_in_gioco, giocatore_corrente
                )
                risultato["effetti_applicati"].append(effetto_risultato)
                
                # Traccia i vari tipi di modifiche
                if "modificatori" in effetto_risultato:
                    risultato["modificatori_applicati"].update(effetto_risultato["modificatori"])
                if "corruzione" in effetto_risultato:
                    risultato["corruzione_applicata"].update(effetto_risultato["corruzione"])
                if "mutazioni" in effetto_risultato:
                    risultato["mutazioni_applicate"].update(effetto_risultato["mutazioni"])
                
                # Applica effetti collaterali
                self._applica_effetti_collaterali(effetto, giocatore_corrente, risultato)
                
            except Exception as e:
                risultato["successo"] = False
                risultato["errori"].append(f"Errore applicando effetto {effetto.tipo_effetto}: {str(e)}")
        
        # Gestione stato carta secondo durata
        if self.durata == DurataOscura.ISTANTANEA:
            self.utilizzata = True
        elif self.durata == DurataOscura.ASSEGNATA:
            # Per doni assegnati
            if bersagli_validi:
                self.in_gioco = True
                self.assegnata_a = bersagli_validi[0]  # Primo bersaglio
                self.bersagli_attuali = [bersagli_validi[0]]
        elif self.durata in [DurataOscura.PERMANENTE, DurataOscura.CONTINUA]:
            self.in_gioco = True
            self.bersagli_attuali = bersagli_validi
        
        return risultato
    
    def _verifica_immunita(self, guerriero: Any) -> bool:
        """Verifica se il guerriero è immune all'Oscura Simmetria"""
        if not hasattr(guerriero, 'keywords'):
            return False
        
        # Immunità completa
        if "Immune all'Oscura Simmetria" in guerriero.keywords:
            return True
        
        # Immunità specifica ai doni
        if self.tipo == TipoOscuraSimmetria.GENERICA:
            if "Immune ai Doni dell'Oscura Simmetria" in guerriero.keywords:
                return True
        
        return False
    
    def _applica_singolo_effetto(self, effetto: EffettoOscura, bersagli: List[str],
                               guerrieri_in_gioco: Dict[str, Any], giocatore_corrente: str) -> Dict[str, Any]:
        """Applica un singolo effetto ai bersagli specificati"""
        risultato = {
            "tipo_effetto": effetto.tipo_effetto,
            "bersagli_interessati": [],
            "modificatori": {},
            "corruzione": {},
            "mutazioni": {}
        }
        
        for nome_bersaglio in bersagli:
            if nome_bersaglio in guerrieri_in_gioco:
                guerriero = guerrieri_in_gioco[nome_bersaglio]
                
                if effetto.tipo_effetto == "Modificatore" and effetto.statistica_target:
                    # Applica modificatore (generalmente negativo per Oscura Simmetria)
                    valore_effetto = effetto.valore
                    if effetto.statistica_target == "combattimento" and valore_effetto > 0:
                        valore_effetto = -abs(valore_effetto)  # Forza negativo per corruzione
                    
                    guerriero.applica_modificatore(effetto.statistica_target, valore_effetto)
                    risultato["bersagli_interessati"].append(nome_bersaglio)
                    risultato["modificatori"][nome_bersaglio] = {
                        effetto.statistica_target: valore_effetto
                    }
                
                elif effetto.tipo_effetto == "Corruzione":
                    # Applica corruzione permanente
                    corruzione_valore = abs(effetto.valore)  # Sempre positivo
                    if nome_bersaglio not in self.corruzione_applicata:
                        self.corruzione_applicata[nome_bersaglio] = 0
                    self.corruzione_applicata[nome_bersaglio] += corruzione_valore
                    
                    # Applica penalità basata sulla corruzione
                    penalita = min(corruzione_valore, 5)  # Massimo -5 per effetto
                    guerriero.applica_modificatore("combattimento", -penalita)
                    
                    risultato["bersagli_interessati"].append(nome_bersaglio)
                    risultato["corruzione"][nome_bersaglio] = corruzione_valore
                
                elif effetto.tipo_effetto == "Mutazione":
                    # Applica mutazione specifica
                    mutazione = effetto.descrizione_effetto or "Mutazione Casuale"
                    if nome_bersaglio not in self.mutazioni_applicate:
                        self.mutazioni_applicate[nome_bersaglio] = []
                    self.mutazioni_applicate[nome_bersaglio].append(mutazione)
                    
                    # Applica effetti meccanici delle mutazioni
                    self._applica_effetto_mutazione(mutazione, guerriero)
                    
                    risultato["bersagli_interessati"].append(nome_bersaglio)
                    risultato["mutazioni"][nome_bersaglio] = [mutazione]
                
                elif effetto.tipo_effetto == "Possessione":
                    # Prende controllo temporaneo del guerriero
                    if hasattr(guerriero, 'controllore_temporaneo'):
                        guerriero.controllore_temporaneo = giocatore_corrente
                    if not hasattr(guerriero, 'keywords'):
                        guerriero.keywords = []
                    guerriero.keywords.append("Posseduto")
                    risultato["bersagli_interessati"].append(nome_bersaglio)
                
                elif effetto.tipo_effetto == "Danno":
                    # Infligge danno diretto
                    if hasattr(guerriero, 'subisci_ferita'):
                        guerriero.subisci_ferita()
                        risultato["bersagli_interessati"].append(nome_bersaglio)
                
                elif effetto.tipo_effetto == "Controllo":
                    # Effetti di controllo oscuri
                    if effetto.descrizione_effetto == "tap" and guerriero.pronto:
                        guerriero.pronto = False
                        risultato["bersagli_interessati"].append(nome_bersaglio)
                    elif effetto.descrizione_effetto == "freeze":
                        if not hasattr(guerriero, 'keywords'):
                            guerriero.keywords = []
                        guerriero.keywords.append("Congelato")
                        risultato["bersagli_interessati"].append(nome_bersaglio)
        
        return risultato
    
    def _applica_effetto_mutazione(self, mutazione: str, guerriero: Any) -> None:
        """Applica gli effetti meccanici specifici delle mutazioni"""
        mutazione_lower = mutazione.lower()
        
        if "artigli" in mutazione_lower:
            guerriero.applica_modificatore("combattimento", 2)
            if not hasattr(guerriero, 'keywords'):
                guerriero.keywords = []
            guerriero.keywords.append("Artigli Mutanti")
        
        elif "armatura chitinosa" in mutazione_lower:
            guerriero.applica_modificatore("armatura", 3)
            if not hasattr(guerriero, 'keywords'):
                guerriero.keywords = []
            guerriero.keywords.append("Armatura Naturale")
        
        elif "degenerazione" in mutazione_lower:
            guerriero.applica_modificatore("sparare", -2)
            guerriero.applica_modificatore("combattimento", -1)
        
        elif "rigenerazione" in mutazione_lower:
            if not hasattr(guerriero, 'keywords'):
                guerriero.keywords = []
            guerriero.keywords.append("Rigenerazione")
        
        elif "carne fluida" in mutazione_lower:
            if not hasattr(guerriero, 'keywords'):
                guerriero.keywords = []
            guerriero.keywords.append("Carne Fluida")
    
    def _applica_effetti_collaterali(self, effetto: EffettoOscura, giocatore_corrente: str,
                                   risultato: Dict[str, Any]) -> None:
        """Applica gli effetti collaterali della carta al giocatore che la gioca"""
        for collaterale in effetto.effetti_collaterali:
            if "Perdi 1 Destiny Point" in collaterale:
                if giocatore_corrente not in self.penalita_giocatore:
                    self.penalita_giocatore[giocatore_corrente] = 0
                self.penalita_giocatore[giocatore_corrente] += 1
                risultato["effetti_collaterali_applicati"].append(f"{giocatore_corrente} perde 1 Destiny Point")
            
            elif "Perdi" in collaterale and "Destiny Point" in collaterale:
                # Estrae il numero di DP da perdere
                import re
                match = re.search(r'Perdi (\d+) Destiny Point', collaterale)
                if match:
                    dp_persi = int(match.group(1))
                    if giocatore_corrente not in self.penalita_giocatore:
                        self.penalita_giocatore[giocatore_corrente] = 0
                    self.penalita_giocatore[giocatore_corrente] += dp_persi
                    risultato["effetti_collaterali_applicati"].append(f"{giocatore_corrente} perde {dp_persi} Destiny Points")
            
            elif "Scarta" in collaterale:
                risultato["effetti_collaterali_applicati"].append(f"{giocatore_corrente} deve scartare carte secondo: {collaterale}")
            
            elif "Ferita casuale" in collaterale:
                risultato["effetti_collaterali_applicati"].append(f"Un guerriero casuale di {giocatore_corrente} viene ferito")
    
    def rimuovi_effetto(self, guerrieri_in_gioco: Dict[str, Any]) -> Dict[str, Any]:
        """Rimuove l'effetto della carta Oscura Simmetria (per effetti non permanenti)"""
        risultato = {"successo": True, "modificatori_rimossi": {}, "corruzione_rimossa": {}, "mutazioni_rimosse": {}}
        
        # La corruzione è generalmente permanente, ma alcuni effetti temporanei possono essere rimossi
        for nome_guerriero in self.bersagli_attuali:
            if nome_guerriero in guerrieri_in_gioco:
                guerriero = guerrieri_in_gioco[nome_guerriero]
                
                # Rimuovi keyword temporanee
                if hasattr(guerriero, 'keywords'):
                    keywords_da_rimuovere = ["Posseduto", "Congelato"]
                    for keyword in keywords_da_rimuovere:
                        if keyword in guerriero.keywords:
                            guerriero.keywords.remove(keyword)
                
                # Ripristina controllo normale
                if hasattr(guerriero, 'controllore_temporaneo'):
                    delattr(guerriero, 'controllore_temporaneo')
        
        # Reset stato carta
        self.in_gioco = False
        self.bersagli_attuali.clear()
        self.assegnata_a = None
        
        return risultato
    
    def get_livello_corruzione_totale(self) -> int:
        """Restituisce il livello totale di corruzione applicata da questa carta"""
        return sum(self.corruzione_applicata.values())
    
    def get_penalita_giocatore_totale(self, giocatore: str) -> int:
        """Restituisce le penalità totali applicate al giocatore specificato"""
        return self.penalita_giocatore.get(giocatore, 0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte la carta Oscura Simmetria in un dizionario per serializzazione"""
        return {
            "nome": self.nome,
            "costo_destino": self.costo_destino,
            "tipo": self.tipo.value,
            "rarity": self.rarity.value,
            "apostolo_padre": self.apostolo_padre.value,
            "fazioni_permesse": [f.value for f in self.fazioni_permesse],
            "bersaglio": self.bersaglio.value,
            "durata": self.durata.value,
            "timing": self.timing.value,
            "set_espansione": self.set_espansione,
            "numero_carta": self.numero_carta,
            "effetti": [
                {
                    "tipo_effetto": eff.tipo_effetto,
                    "valore": eff.valore,
                    "statistica_target": eff.statistica_target,
                    "descrizione_effetto": eff.descrizione_effetto,
                    "condizioni": eff.condizioni,
                    "effetti_collaterali": eff.effetti_collaterali
                } for eff in self.effetti
            ],
            "testo_carta": self.testo_carta,
            "flavour_text": self.flavour_text,
            "keywords": self.keywords,
            "restrizioni": self.restrizioni,
            "stato_gioco": {
                "in_gioco": self.in_gioco,
                "utilizzata": self.utilizzata,
                "bersagli_attuali": self.bersagli_attuali,
                "assegnata_a": self.assegnata_a
            },
            "corruzione_applicata": self.corruzione_applicata,
            "mutazioni_applicate": self.mutazioni_applicate,
            "penalita_giocatore": self.penalita_giocatore,
            "contatori_oscura": self.contatori_oscura,
            "livello_corruzione": self.livello_corruzione,
            "puo_essere_negata": self.puo_essere_negata,
            "valore_strategico": self.valore_strategico,
            "quantita": self.quantita,
            "quantita_minima_consigliata": self.quantita_minima_consigliata,
            "fondamentale": self.fondamentale
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Oscura_Simmetria':
        """Crea una carta Oscura Simmetria da un dizionario"""
        carta = cls(data["nome"], data["costo_destino"])
        
        carta.tipo = TipoOscuraSimmetria(data["tipo"])
        carta.rarity = Rarity(data["rarity"])
        carta.apostolo_padre = ApostoloOscuraSimmetria(data["apostolo_padre"])
        carta.fazioni_permesse = [Fazione(f) for f in data["fazioni_permesse"]]
        carta.bersaglio = BersaglioOscura(data["bersaglio"])
        carta.durata = DurataOscura(data["durata"])
        carta.timing = TimingOscura(data["timing"])
        carta.set_espansione = data["set_espansione"]
        carta.numero_carta = data["numero_carta"]
        carta.testo_carta = data["testo_carta"]
        carta.flavour_text = data["flavour_text"]
        carta.keywords = data["keywords"]
        carta.restrizioni = data["restrizioni"]
        #carta.corruzione_applicata = data["corruzione_applicata"]
        #carta.mutazioni_applicate = data["mutazioni_applicate"]
        #carta.penalita_giocatore = data["penalita_giocatore"]
        #carta.contatori_oscura = data["contatori_oscura"]
        #carta.livello_corruzione = data["livello_corruzione"]
        carta.valore_strategico = data["valore_strategico"]
        carta.quantita = data.get("quantita")
        carta.quantita_minima_consigliata = data.get("quantita_minima_consigliata")
        carta.fondamentale = data.get("fondamentale")
        
        # Gestione nuovi campi (compatibilità)
        #if "puo_essere_negata" in data:
        #    carta.puo_essere_negata = data["puo_essere_negata"]
        
        # Ripristina stato di gioco
        #stato = data["stato_gioco"]
        #carta.in_gioco = stato["in_gioco"]
        #carta.utilizzata = stato["utilizzata"]
        #carta.bersagli_attuali = stato["bersagli_attuali"]
        
        # Gestione nuovi campi stato
        #if "assegnata_a" in stato:
        #    carta.assegnata_a = stato["assegnata_a"]
        
        # Ricostruisce effetti
        for eff_data in data["effetti"]:
            carta.aggiungi_effetto(
                eff_data["tipo_effetto"],
                eff_data["valore"],
                eff_data["statistica_target"],
                eff_data["descrizione_effetto"],
                eff_data["condizioni"],
                eff_data["effetti_collaterali"]
            )
        
        return carta
    
    def __str__(self) -> str:
        """Rappresentazione stringa della carta Oscura Simmetria"""
        apostolo_str = f" - {self.apostolo_padre.value}" if self.apostolo_padre != ApostoloOscuraSimmetria.NESSUNO else ""
        fazioni_str = ", ".join([f.value for f in self.fazioni_permesse])
        assegnata_str = f" [→ {self.assegnata_a}]" if self.assegnata_a else ""
        return (f"{self.nome} (Costo: {self.costo_destino}) - "
                f"Tipo: {self.tipo.value}{apostolo_str} - "
                f"Fazioni: [{fazioni_str}]{assegnata_str}")
    
    def __repr__(self) -> str:
        return f"Oscura_Simmetria('{self.nome}', {self.costo_destino})"


# Funzioni di utilità per creare carte Oscura Simmetria specifiche

def crea_oscura_generica(nome: str, costo: int = 0) -> Oscura_Simmetria:
    """Crea una carta Oscura Simmetria generica"""
    carta = Oscura_Simmetria(nome, costo)
    carta.tipo = TipoOscuraSimmetria.GENERICA
    carta.fazioni_permesse = [Fazione.OSCURA_LEGIONE]
    carta.set_espansione = Set_Espansione.BASE
    return carta

def crea_dono_apostolo(nome: str, apostolo: ApostoloOscuraSimmetria, costo: int = 1) -> Oscura_Simmetria:
    """Crea un Dono specifico di un Apostolo"""
    carta = Oscura_Simmetria(nome, costo)
    carta.tipo = TipoOscuraSimmetria.DONO_APOSTOLO
    carta.apostolo_padre = apostolo
    carta.durata = DurataOscura.ASSEGNATA
    carta.bersaglio = BersaglioOscura.GUERRIERO_PROPRIO
    carta.fazioni_permesse = [Fazione.OSCURA_LEGIONE]
    carta.restrizioni.append(f"Solo Seguaci di {apostolo.value}")
    carta.set_espansione = Set_Espansione.BASE
    return carta

def crea_corruzione(nome: str, livello: int = 1, costo: int = 0) -> Oscura_Simmetria:
    """Crea una carta di Corruzione"""
    carta = crea_oscura_generica(nome, costo)
    carta.tipo = TipoOscuraSimmetria.DONO_APOSTOLO
    carta.bersaglio = BersaglioOscura.GUERRIERO_AVVERSARIO
    carta.durata = DurataOscura.PERMANENTE
    carta.aggiungi_effetto("Corruzione", livello, "combattimento", 
                          f"Corruzione livello {livello}")
    return carta


# Esempi di utilizzo corretto secondo il regolamento

if __name__ == "__main__":
    print("=== ESEMPI CARTE OSCURA SIMMETRIA CORRETTE ===")
    
    # Corruzione base
    corruzione_minore = crea_corruzione("Corruzione Minore", 1, 0)
    print(f"✓ {corruzione_minore}")
    print(f"  Può essere usata da: {[f.value for f in corruzione_minore.fazioni_permesse]}")
    
    # Dono di Algeroth
    furia_algeroth = crea_dono_apostolo("Furia di Algeroth", ApostoloOscuraSimmetria.ALGEROTH, 1)
    furia_algeroth.aggiungi_effetto("Modificatore", 2, "combattimento",
                                   "Il guerriero ottiene +2 Combattimento",
                                   [], ["Il guerriero non può ritirarsi dal combattimento"])
    print(f"✓ {furia_algeroth}")
    
   

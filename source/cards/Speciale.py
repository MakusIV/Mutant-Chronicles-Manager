"""
Modulo per la rappresentazione delle carte Speciali di Mutant Chronicles/Doomtrooper
Le carte Speciali costituiscono la maggior parte delle carte del gioco e possono essere utilizzate 
in modi diversi durante la partita e i combattimenti per apportare modifiche ai valori 
di combattimento di un singolo guerriero o per creare situazioni particolari.
Basato sulla struttura delle classi Guerriero, Arte, Oscura_Simmetria e Equipaggiamento
VERSIONE CORRETTA - Allineata alle regole ufficiali del regolamento
"""

from enum import Enum
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import json
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione, DOOMTROOPER  # Import dalle classi esistenti


class TipoSpeciale(Enum):
    """Tipi di carte Speciali secondo il regolamento"""
    MODIFICA_COMBATTIMENTO = "Modifica Combattimento"
    SITUAZIONE_TATTICA = "Situazione Tattica"
    MODIFICA_GUERRIERO = "Modifica Guerriero"
    MODIFICA_GIOCATORE = "Modifica Giocatore"
    CONTROMOSSA = "Contromossa"
    EVENTO = "Evento"
    FORTUNA = "Fortuna"
    SFORTUNA = "Sfortuna"
    TATTICA_SPECIALE = "Tattica Speciale"
    SPECIALE = "Speciale"


class BersaglioSpeciale(Enum):
    """Possibili bersagli delle carte Speciali"""
    GUERRIERO_PROPRIO = "Guerriero Proprio"
    GUERRIERO_AVVERSARIO = "Guerriero Avversario"
    QUALSIASI_GUERRIERO = "Qualsiasi Guerriero"
    GUERRIERO_ATTACCANTE = "Guerriero Attaccante"
    GUERRIERO_DIFENSORE = "Guerriero Difensore"
    ENTRAMBI_COMBATTENTI = "Entrambi i Combattenti"
    TUTTI_GUERRIERI = "Tutti i Guerrieri"
    TUTTI_GUERRIERI_PROPRI = "Tutti i Guerrieri Propri"
    TUTTI_GUERRIERI_AVVERSARI = "Tutti i Guerrieri Avversari"
    GIOCATORE = "Giocatore"
    GIOCATORE_AVVERSARIO = "Giocatore Avversario"
    ENTRAMBI_GIOCATORI = "Entrambi i Giocatori"
    COMBATTIMENTO = "Combattimento Corrente"
    SENZA_BERSAGLIO = "Senza Bersaglio"
    MERCENARIO = "Mercenario"
    ERETICO = "Eretico"
    GUERRIERO_FRATELLANZA = "Guerriero della Fratellanza"
    DOOMTROOPER = "Doomtrooper"
    PERSONALITA = "Personalita"
    EQUIPAGGIAMENTO = "Equipaggiamento"
    FORTIFICAZIONE = "Fortificazione"


class DurataSpeciale(Enum):
    """Durata dell'effetto delle carte Speciali"""
    ISTANTANEA = "Istantanea"
    FINO_FINE_TURNO = "Fino Fine Turno"
    FINO_FINE_COMBATTIMENTO = "Fino Fine Combattimento"
    DURANTE_COMBATTIMENTO = "Durante questo Combattimento"
    PERMANENTE = "Permanente"
    CONTINUA = "Continua"
    FINO_PROSSIMO_TURNO = "Fino Prossimo Turno"
    


class TimingSpeciale(Enum):
    """Quando può essere giocata una carta Speciale"""
    TURNO_PROPRIO = "Turno Proprio"
    TURNO_AVVERSARIO = "Turno Avversario"
    IN_OGNI_MOMENTO = "In Ogni Momento"
    IN_COMBATTIMENTO = "In Combattimento"
    DURANTE_MODIFICATORI = "Durante Modificatori Combattimento"
    PRIMA_COMBATTIMENTO = "Prima del Combattimento"
    DOPO_COMBATTIMENTO = "Dopo il Combattimento"
    DICHIARAZIONE_ATTACCO = "Dichiarazione Attacco"
    RISOLUZIONE_COMBATTIMENTO = "Risoluzione Combattimento"
    IN_RISPOSTA = "In Risposta"
    QUANDO_FERITO = "Quando Ferito"
    QUANDO_UCCISO = "Quando Ucciso"
    QUANDO_ELIMINATO = "Quando Eliminato"


@dataclass
class EffettoSpeciale:
    """Rappresenta l'effetto di una carta Speciale"""
    tipo_effetto: str  # es. "Modificatore", "Controllo", "Danno", etc.
    valore: int = 0  # valore numerico dell'effetto (se applicabile)
    statistica_target: str = ""  # quale statistica viene modificata (C, S, A, V)
    descrizione_effetto: str = ""
    condizioni: List[str] = None  # condizioni per attivare l'effetto
    limitazioni: List[str] = None  # limitazioni all'uso
    
    def __post_init__(self):
        if self.condizioni is None:
            self.condizioni = []
        if self.limitazioni is None:
            self.limitazioni = []


class Speciale:
    """
    Classe per rappresentare una carta Speciale di Mutant Chronicles/Doomtrooper
    
    Le carte Speciali costituiscono la maggior parte delle carte del gioco e sono carte molto
    particolari che possono essere utilizzate in modi diversi durante la partita e i combattimenti
    per apportare modifiche ai valori di combattimento di un singolo guerriero o per creare
    situazioni particolari. Sulle carte è indicato quando possono essere giocate, se su un
    singolo guerriero o sul giocatore direttamente.
    
    VERSIONE CORRETTA - Allineata alle regole del regolamento ufficiale
    """
    
    def __init__(self, nome: str, valore: int = 0):
        """
        Inizializza una nuova carta Speciale
        
        Args:
            nome: Nome della carta Speciale
            valore: Costo in Destiny Points per giocare la carta (se richiesto)
        """
        self.nome = nome
        self.valore = valore  # Costo in DP, 0 se gratuita
        
        # Attributi base della carta
        self.tipo = TipoSpeciale.MODIFICA_COMBATTIMENTO
        self.rarity = Rarity.COMMON
        
        # Meccaniche di gioco secondo il regolamento
        self.bersaglio = BersaglioSpeciale.SENZA_BERSAGLIO
        self.durata = DurataSpeciale.ISTANTANEA
        self.timing = TimingSpeciale.IN_OGNI_MOMENTO
        
        # Effetti della carta
        self.effetti: List[EffettoSpeciale] = []
        
        # Testo della carta
        self.testo_carta = ""
        self.flavour_text = ""
        
        # Restrizioni e permessi secondo il regolamento
        self.fazioni_permesse: List[Fazione] = []  # Vuoto = tutte le fazioni
        self.restrizioni: List[str] = []
        self.keywords: List[str] = []
        
        # Limitazioni di gioco
        self.max_copie_per_combattimento = 1  # Limite di copie giocabili nello stesso combattimento
        self.max_copie_per_turno = 1  # Limite di copie giocabili nello stesso turno
        self.richiede_azione = False  # Se costa un'azione per essere giocata
        
        # Attributi per espansioni
        self.set_espansione = Set_Espansione.BASE
        self.numero_carta = ""
        
        # Stato di gioco
        self.in_gioco = False  # per carte con effetto permanente
        self.utilizzata = False
        self.bersagli_attuali: List[str] = []  # nomi dei guerrieri targetati
        self.volte_giocata_questo_turno = 0
        self.volte_giocata_questo_combattimento = 0
        
        # Tracking modificatori per annullamento
        self.modificatori_applicati: Dict[str, Dict[str, int]] = {}
        
        # Contatori per effetti speciali
        self.contatori_speciali: Dict[str, int] = {}
        self.quantita = 0
        self.quantita_minima_consigliata = 0  # per la creazione del mazzo
        self.fondamentale = False  # se la carta è fondamentale per il mazzo
    

    def modifica_principale_effettuata(self) -> str:

        combattimento = 0
        sparare = 0
        armatura = 0
            
        for effetto in self.effetti:
        
            tipo_effetto = effetto.tipo_effetto # es. "Modificatore", "Controllo", "Danno", etc.
            valore = effetto.valore # valore numerico dell'effetto (se applicabile)
            statistica_target = effetto.statistica_target # quale statistica viene modificata (C, S, A, V)

            if tipo_effetto == "Modificatore" and statistica_target in ["combattimento", "sparare", "armatura"] and isinstance(valore, int) == True:
                            
                if statistica_target == 'combattimento':
                    combattimento = valore if valore > combattimento else combattimento
                elif statistica_target == 'sparare':
                    sparare = valore if valore > sparare else sparare
                elif statistica_target == 'armatura':
                    armatura = valore if valore > armatura else armatura
                
            else:
                return 'azioni'   

        if combattimento >= sparare and combattimento >= armatura:
            result = 'combattimento'
        elif sparare >= combattimento and sparare >= armatura:
            result = 'sparare'
        else:
            result = 'armatura'
        
        return result
            
    def get_costo_destino(self) -> int:
        """
        Restituisce il costo in Destiny Points per giocare questa carta
        """
        return self.valore
    
    def puo_essere_giocata_da_fazione(self, fazione: Fazione) -> bool:
        """
        Verifica se la carta può essere giocata dalla fazione specificata
        
        Args:
            fazione: Fazione che vuole giocare la carta
            
        Returns:
            True se la fazione può giocare la carta
        """
        # Se nessuna fazione specificata, tutte possono giocarla
        if not self.fazioni_permesse:
            return True
        
        return fazione in self.fazioni_permesse
    
    def puo_essere_assegnato_a_guerriero(self, guerriero: Any) -> Dict[str, Any]:
        """
        Controlla se la carta speciale può essere assegnata al guerriero specificato
        Basato sulle regole di fazioni_permesse del regolamento
        
        Args:
            guerriero: Istanza del guerriero
            
        Returns:
            Dizionario con risultato e eventuali errori
        """
        risultato = {"puo_assegnare": True, "errori": []}
        
        # Controllo fazioni_permesse
        if self.fazioni_permesse is not None and self.fazioni_permesse != []:
            # Se l'equipaggiamento ha fazioni_permesse specifiche
            if all( a != guerriero.fazione for a in self.fazioni_permesse):
                # Verifica se è equipaggiamento generico utilizzabile da tutti
                if self.fazioni_permesse != ["Generica"]:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Affiliazione richiesta: {self.fazioni_permesse}")
        
        # Controllo restrizioni specifiche
        for restrizione in self.restrizioni:
            if "Solo Doomtrooper" in restrizione: 
                if guerriero.fazione == Fazione.OSCURA_LEGIONE:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Solo per Doomtrooper")
            elif "Solo Oscura Legione" in restrizione:
                if guerriero.fazione != Fazione.OSCURA_LEGIONE:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Solo per Oscura Legione") 

            elif "Solo Fratellanza" in restrizione:
                if guerriero.fazione != Fazione.FRATELLANZA:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Solo per Fratellanza")                             

            elif "Solo Seguaci di" in restrizione:
                apostolo_richiesto = restrizione.split("Solo Seguaci di ")[1].strip()
                if (guerriero.keywords is None or guerriero.keywords == [] or guerriero.keywords != "Seguace di " + apostolo_richiesto):                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo Seguaci di {apostolo_richiesto}")
            
            elif "Solo Eretici" in restrizione:
                if (guerriero.keywords is None or guerriero.keywords == [] or guerriero.keywords != "Eretico" ):                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo Eretici")

            elif "Solo Personalita" in restrizione:
                if guerriero.tipo != "Personalita" or (guerriero.keywords and len(guerriero.keywords)>0 and "Personalita" not in guerriero.keywords ):                                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Solo Personalita")

            elif "Non utilizzabile da Personalita" in restrizione:            
                if guerriero.tipo == "Personalita" or (guerriero.keywords and len(guerriero.keywords)>0 and "Personalita" in guerriero.keywords ):                       
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append(f"Non utilizzabile da Personalita")

            elif "Non utilizzabile dalla Fratellanza" in restrizione:
                if guerriero.fazione == Fazione.FRATELLANZA:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Non utilizzabile dalla Fratellanza")

            elif "Non utilizzabile dalla Oscura Legione" in restrizione:
                if guerriero.fazione == Fazione.OSCURA_LEGIONE:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Non utilizzabile dalla Fratellanza")

            elif "Non utilizzabile dai Doomtroopers" in restrizione:
                if guerriero.fazione in DOOMTROOPER:
                    risultato["puo_assegnare"] = False
                    risultato["errori"].append("Non utilizzabile dalla Fratellanza")



            
            

        return risultato
     
    def puo_essere_giocata(self, destiny_points: int = 0, 
                          fazione_giocatore: Optional[Fazione] = None,
                          timing_corrente: Optional[TimingSpeciale] = None,
                          azioni_disponibili: int = 0,
                          condizioni_gioco: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Controlla se la carta può essere giocata nel momento attuale
        
        Args:
            destiny_points: Punti Destino disponibili del giocatore
            fazione_giocatore: Fazione del giocatore
            timing_corrente: Timing corrente del gioco
            azioni_disponibili: Azioni disponibili al giocatore
            condizioni_gioco: Condizioni aggiuntive del gioco
            
        Returns:
            Dizionario con risultato e eventuali errori
        """
        risultato = {"puo_giocare": True, "errori": [], "avvertimenti": []}
        
        # Controllo costo base
        if destiny_points < self.valore:
            risultato["puo_giocare"] = False
            risultato["errori"].append(f"Destiny Points insufficienti: richiesti {self.valore}, disponibili {destiny_points}")
        
        # Controllo azioni richieste
        if self.richiede_azione and azioni_disponibili < 1:
            risultato["puo_giocare"] = False
            risultato["errori"].append("Azione richiesta ma non disponibile")
        
        # Controllo fazione
        if fazione_giocatore and not self.puo_essere_giocata_da_fazione(fazione_giocatore):
            risultato["puo_giocare"] = False
            risultato["errori"].append(f"Fazione {fazione_giocatore.value} non può giocare questa carta")
        
        # Controllo timing
        if self.timing != TimingSpeciale.IN_OGNI_MOMENTO and self.timing != timing_corrente:
            risultato["puo_giocare"] = False
            risultato["errori"].append(f"Timing non corretto: richiesto {self.timing.value}, attuale {timing_corrente.value if timing_corrente else 'Non specificato'}")
        
        # Controllo se già utilizzata (per carte monouso)
        if self.utilizzata and self.durata == DurataSpeciale.ISTANTANEA:
            risultato["puo_giocare"] = False
            risultato["errori"].append("Carta già utilizzata")
        
        # Controllo limitazioni per turno
        if self.volte_giocata_questo_turno >= self.max_copie_per_turno:
            risultato["puo_giocare"] = False
            risultato["errori"].append(f"Limite di {self.max_copie_per_turno} copie per turno raggiunto")
        
        # Controllo limitazioni per combattimento (se in combattimento)
        if timing_corrente in [TimingSpeciale.IN_COMBATTIMENTO, TimingSpeciale.DURANTE_MODIFICATORI]:
            if self.volte_giocata_questo_combattimento >= self.max_copie_per_combattimento:
                risultato["puo_giocare"] = False
                risultato["errori"].append(f"Limite di {self.max_copie_per_combattimento} copie per combattimento raggiunto")
        
        # Controlli specifici per carte di combattimento
        if self.tipo == TipoSpeciale.MODIFICA_COMBATTIMENTO:
            if timing_corrente not in [TimingSpeciale.IN_COMBATTIMENTO, TimingSpeciale.DURANTE_MODIFICATORI]:
                risultato["puo_giocare"] = False
                risultato["errori"].append("Carte di modifica combattimento solo durante il combattimento")
        
        return risultato
    
    def applica_effetto(self, bersaglio: Union[str, List[str]],
                       guerrieri_in_gioco: Dict[str, Any],
                       giocatore_corrente: str,
                       stato_combattimento: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Applica l'effetto della carta Speciale
        
        Args:
            bersaglio: Nome/i del/i bersaglio/i
            guerrieri_in_gioco: Dizionario dei guerrieri in gioco
            giocatore_corrente: Nome del giocatore che gioca la carta
            stato_combattimento: Stato attuale del combattimento (se applicabile)
            
        Returns:
            Risultato dell'applicazione dell'effetto
        """
        risultato = {
            "successo": True,
            "effetti_applicati": [],
            "errori": [],
            "modificatori_applicati": {},
            "situazioni_create": [],
            "carte_pescate": 0,
            "carte_scartate": 0,
            "punti_destino_modificati": 0
        }
        
        # Determina i bersagli effettivi
        bersagli_effettivi = []
        if isinstance(bersaglio, str):
            bersagli_effettivi = [bersaglio] if bersaglio != "" else []
        else:
            bersagli_effettivi = bersaglio
        
        # Applica ogni effetto della carta
        for effetto in self.effetti:
            try:
                risultato_effetto = self._applica_singolo_effetto(
                    effetto, bersagli_effettivi, guerrieri_in_gioco, 
                    giocatore_corrente, stato_combattimento
                )
                
                # Aggrega i risultati
                risultato["effetti_applicati"].append(risultato_effetto["descrizione"])
                if risultato_effetto.get("modificatori"):
                    risultato["modificatori_applicati"].update(risultato_effetto["modificatori"])
                
            except Exception as e:
                risultato["errori"].append(f"Errore nell'applicazione dell'effetto {effetto.tipo_effetto}: {str(e)}")
                risultato["successo"] = False
        
        # Aggiorna stato della carta
        if risultato["successo"]:
            self.utilizzata = True
            self.volte_giocata_questo_turno += 1
            if stato_combattimento:
                self.volte_giocata_questo_combattimento += 1
            
            # Se ha effetti permanenti o continui, rimane in gioco
            if self.durata in [DurataSpeciale.PERMANENTE, DurataSpeciale.CONTINUA]:
                self.in_gioco = True
                self.bersagli_attuali = bersagli_effettivi
        
        return risultato
    
    def _applica_singolo_effetto(self, effetto: EffettoSpeciale,
                                bersagli: List[str],
                                guerrieri_in_gioco: Dict[str, Any],
                                giocatore_corrente: str,
                                stato_combattimento: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Applica un singolo effetto della carta
        
        Args:
            effetto: L'effetto da applicare
            bersagli: Lista dei bersagli
            guerrieri_in_gioco: Guerrieri attualmente in gioco
            giocatore_corrente: Giocatore che sta giocando la carta
            stato_combattimento: Stato del combattimento corrente
            
        Returns:
            Risultato dell'applicazione del singolo effetto
        """
        risultato = {
            "descrizione": effetto.descrizione_effetto,
            "modificatori": {},
            "successo": True
        }
        
        # Gestione modificatori statistiche
        if effetto.tipo_effetto == "Modificatore":
            for nome_bersaglio in bersagli:
                if nome_bersaglio in guerrieri_in_gioco:
                    guerriero = guerrieri_in_gioco[nome_bersaglio]
                    
                    # Applica il modificatore alla statistica target
                    if effetto.statistica_target in ["combattimento", "sparare", "armatura", "valore"]:
                        if nome_bersaglio not in self.modificatori_applicati:
                            self.modificatori_applicati[nome_bersaglio] = {}
                        
                        self.modificatori_applicati[nome_bersaglio][effetto.statistica_target] = effetto.valore
                        risultato["modificatori"][nome_bersaglio] = {effetto.statistica_target: effetto.valore}
                        
                        # Applica effettivamente il modificatore al guerriero (se il guerriero ha questo metodo)
                        if hasattr(guerriero, 'applica_modificatore_temporaneo'):
                            guerriero.applica_modificatore_temporaneo(effetto.statistica_target, effetto.valore)
        
        # Gestione effetti speciali di combattimento
        elif effetto.tipo_effetto in ["Cambio_Attaccante", "Cambio_Difensore", "Annulla_Attacco", "Primo_Attacco", "Doppio_Attacco"]:
            if stato_combattimento:
                # Modifica lo stato del combattimento
                risultato["modifica_combattimento"] = {
                    "tipo": effetto.tipo_effetto,
                    "valore": effetto.valore,
                    "descrizione": effetto.descrizione_effetto
                }
        
        # Gestione pescaggio/scarto carte
        elif effetto.tipo_effetto == "Pescaggio_Carte":
            risultato["carte_pescate"] = effetto.valore
        elif effetto.tipo_effetto == "Scarto_Carte":
            risultato["carte_scartate"] = effetto.valore
        
        # Gestione modifica Punti Destino
        elif effetto.tipo_effetto == "Modifica_Punti_Destino":
            risultato["punti_destino"] = effetto.valore
        
        # Gestione guarigione
        elif effetto.tipo_effetto == "Guarigione":
            for nome_bersaglio in bersagli:
                if nome_bersaglio in guerrieri_in_gioco:
                    guerriero = guerrieri_in_gioco[nome_bersaglio]
                    if hasattr(guerriero, 'stato') and hasattr(guerriero, 'guarisci'):
                        guerriero.guarisci()
                        risultato["guarigioni"] = risultato.get("guarigioni", 0) + 1
        
        return risultato
    
    def rimuovi_effetti(self, guerrieri_in_gioco: Dict[str, Any]) -> Dict[str, Any]:
        """
        Rimuove gli effetti della carta quando termina la sua durata
        
        Args:
            guerrieri_in_gioco: Dizionario dei guerrieri in gioco
            
        Returns:
            Risultato della rimozione degli effetti
        """
        risultato = {
            "successo": True,
            "modificatori_rimossi": {},
            "errori": []
        }
        
        # Rimuovi modificatori applicati ai guerrieri
        for nome_guerriero, modificatori in self.modificatori_applicati.items():
            if nome_guerriero in guerrieri_in_gioco:
                guerriero = guerrieri_in_gioco[nome_guerriero]
                
                for stat, valore in modificatori.items():
                    if hasattr(guerriero, 'rimuovi_modificatore_temporaneo'):
                        guerriero.rimuovi_modificatore_temporaneo(stat, valore)
                    
                risultato["modificatori_rimossi"][nome_guerriero] = modificatori
        
        # Reset stato carta
        self.in_gioco = False
        self.bersagli_attuali.clear()
        self.modificatori_applicati.clear()
        
        return risultato
    
    def reset_turno(self):
        """Reset contatori per nuovo turno"""
        self.volte_giocata_questo_turno = 0
        
        # Se era a durata di un turno, rimuovi dalla partita
        if self.durata == DurataSpeciale.FINO_FINE_TURNO and self.in_gioco:
            self.in_gioco = False
            self.utilizzata = False
    
    def reset_combattimento(self):
        """Reset contatori per nuovo combattimento"""
        self.volte_giocata_questo_combattimento = 0
        
        # Se era a durata di un combattimento, rimuovi dalla partita
        if self.durata == DurataSpeciale.DURANTE_COMBATTIMENTO and self.in_gioco:
            self.in_gioco = False
            self.utilizzata = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte la carta Speciale in un dizionario per serializzazione"""
        return {
            "nome": self.nome,
            "valore": self.valore,
            "tipo": self.tipo.value,
            "rarity": self.rarity.value,
            "fazioni_permesse": [f.value for f in self.fazioni_permesse],
            "bersaglio": self.bersaglio.value,
            "durata": self.durata.value,
            "timing": self.timing.value,
            "set_espansione": self.set_espansione,
            "numero_carta": self.numero_carta,
            "max_copie_per_combattimento": self.max_copie_per_combattimento,
            "max_copie_per_turno": self.max_copie_per_turno,
            "richiede_azione": self.richiede_azione,
            "effetti": [
                {
                    "tipo_effetto": eff.tipo_effetto,
                    "valore": eff.valore,
                    "statistica_target": eff.statistica_target,
                    "descrizione_effetto": eff.descrizione_effetto,
                    "condizioni": eff.condizioni,
                    "limitazioni": eff.limitazioni
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
                "volte_giocata_questo_turno": self.volte_giocata_questo_turno,
                "volte_giocata_questo_combattimento": self.volte_giocata_questo_combattimento
            },
            "contatori_speciali": self.contatori_speciali
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Speciale':
        """Crea una carta Speciale da un dizionario"""
        speciale = cls(data["nome"], data["valore"])
        
        speciale.tipo = TipoSpeciale(data["tipo"])
        speciale.rarity = Rarity(data["rarity"])
        speciale.fazioni_permesse = [Fazione(f) for f in data["fazioni_permesse"]]
        speciale.bersaglio = BersaglioSpeciale(data["bersaglio"])
        speciale.durata = DurataSpeciale(data["durata"])
        speciale.timing = TimingSpeciale(data["timing"])
        speciale.set_espansione = data["set_espansione"]
        speciale.numero_carta = data["numero_carta"]
        speciale.max_copie_per_combattimento = data.get("max_copie_per_combattimento", 1)
        speciale.max_copie_per_turno = data.get("max_copie_per_turno", 1)
        speciale.richiede_azione = data.get("richiede_azione", False)
        
        # Ricrea gli effetti
        for effetto_data in data["effetti"]:
            effetto = EffettoSpeciale(
                tipo_effetto=effetto_data["tipo_effetto"],
                valore=effetto_data["valore"],
                statistica_target=effetto_data["statistica_target"],
                descrizione_effetto=effetto_data["descrizione_effetto"],
                condizioni=effetto_data["condizioni"],
                limitazioni=effetto_data["limitazioni"]
            )
            speciale.effetti.append(effetto)
        
        speciale.testo_carta = data["testo_carta"]
        speciale.flavour_text = data["flavour_text"]
        speciale.keywords = data["keywords"]
        speciale.restrizioni = data["restrizioni"]
        speciale.quantita = data.get("quantita", 0)
        speciale.quantita_minima_consigliata = data.get("quantita_minima_consigliata", 0)
        speciale.fondamentale = data.get("fondamentale", False)
        
        # Ripristina stato di gioco se presente
        if "stato_gioco" in data:
            stato = data["stato_gioco"]
            speciale.in_gioco = stato["in_gioco"]
            speciale.utilizzata = stato["utilizzata"]
            speciale.bersagli_attuali = stato["bersagli_attuali"]
            speciale.volte_giocata_questo_turno = stato["volte_giocata_questo_turno"]
            speciale.volte_giocata_questo_combattimento = stato["volte_giocata_questo_combattimento"]
        
        speciale.contatori_speciali = data.get("contatori_speciali", {})
        
        return speciale
    
    def __str__(self) -> str:
        """Rappresentazione string della carta"""
        return f"Speciale: {self.nome} (V:{self.valore}) - {self.tipo.value}"
    
    def __repr__(self) -> str:
        """Rappresentazione dettagliata della carta"""
        return f"Speciale(nome='{self.nome}', valore={self.valore}, tipo='{self.tipo.value}', timing='{self.timing.value}')"


# Esempi di utilizzo e test della classe

if __name__ == "__main__":
    print("=== CLASSE SPECIALE - MUTANT CHRONICLES/DOOMTROOPER ===")
    print("Implementazione delle carte Speciali secondo il regolamento ufficiale\n")
    
    # Crea una carta di esempio
    carta_aim = Speciale("Aim", 0)
    carta_aim.tipo = TipoSpeciale.MODIFICA_COMBATTIMENTO
    carta_aim.bersaglio = BersaglioSpeciale.QUALSIASI_GUERRIERO
    carta_aim.durata = DurataSpeciale.DURANTE_COMBATTIMENTO
    carta_aim.timing = TimingSpeciale.DURANTE_MODIFICATORI
    carta_aim.rarity = Rarity.COMMON
    
    # Aggiungi effetto
    effetto_aim = EffettoSpeciale(
        tipo_effetto="Modificatore",
        valore=1,
        statistica_target="sparare",
        descrizione_effetto="+1 Sparare durante questo combattimento"
    )
    carta_aim.effetti.append(effetto_aim)
    carta_aim.testo_carta = "Il guerriero bersaglio ottiene +1 Sparare durante questo combattimento."
    carta_aim.flavour_text = "Un momento di concentrazione può fare la differenza."
    
    print(f"Carta creata: {carta_aim}")
    print(f"Tipo: {carta_aim.tipo.value}")
    print(f"Bersaglio: {carta_aim.bersaglio.value}")
    print(f"Timing: {carta_aim.timing.value}")
    print(f"Effetti: {len(carta_aim.effetti)}")
    print(f"Testo: {carta_aim.testo_carta}")
    
    # Test serializzazione
    print(f"\n=== TEST SERIALIZZAZIONE ===")
    dict_carta = carta_aim.to_dict()
    carta_ricostruita = Speciale.from_dict(dict_carta)
    
    print(f"Carta originale: {carta_aim.nome}")
    print(f"Carta ricostruita: {carta_ricostruita.nome}")
    print(f"Serializzazione riuscita: {carta_aim.nome == carta_ricostruita.nome}")
    
    # Test controlli di gioco
    print(f"\n=== TEST CONTROLLI DI GIOCO ===")
    risultato = carta_aim.puo_essere_giocata(
        destiny_points=5,
        fazione_giocatore=Fazione.IMPERIALE,
        timing_corrente=TimingSpeciale.DURANTE_MODIFICATORI,
        azioni_disponibili=1
    )
    
    print(f"Può essere giocata: {risultato['puo_giocare']}")
    if risultato['errori']:
        print(f"Errori: {risultato['errori']}")
    
    print(f"\n=== IMPLEMENTAZIONE COMPLETATA ===")
    print("✓ Classe Speciale implementata secondo regolamento Doomtrooper")
    print("✓ Tipi di carte: Modifica Combattimento, Situazione Tattica, Contromossa, etc.")
    print("✓ Timing corretto: In Combattimento, Qualsiasi Momento, Durante Modificatori")
    print("✓ Bersagli: Guerrieri, Giocatori, Combattimenti")
    print("✓ Effetti: Modificatori statistiche, Cambi tattici, Controllo carte")
    print("✓ Durata: Istantanea, Durante Combattimento, Permanente")
    print("✓ Limitazioni: Max copie per turno/combattimento")
    print("✓ Compatibile con classi Guerriero, Arte, Oscura_Simmetria")
    print("✓ Serializzazione tramite to_dict() e from_dict()")
    print("✓ Gestione stato di gioco e tracking effetti")
    print("✓ Controlli di validità secondo regolamento")
    print("✓ Reset automatico per turni e combattimenti")
    print("✓ Struttura coerente con altre classi del progetto")
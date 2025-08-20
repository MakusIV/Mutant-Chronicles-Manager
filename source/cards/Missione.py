"""
Classe Missione per Mutant Chronicles/Doomtrooper
Rappresenta le carte Missione del gioco, implementando le regole ufficiali del regolamento.
Le Missioni sono istruzioni speciali che possono essere assegnate a guerrieri o giocatori
per guadagnare ricompense extra e Punti Promozione.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import json
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione  # Import dalle classi esistenti



class TipoMissione(Enum):
    """Tipologie di Missioni"""
    GUERRIERO = "Guerriero"  # Assegnata a un guerriero specifico
    GIOCATORE = "Giocatore"  # Assegnata al giocatore
    AVVERSARIO = "Avversario"  # Assegnata all'avversario o suo guerriero


class DifficoltaMissione(Enum):
    """Difficoltà della missione"""
    FACILE = "Facile"
    NORMALE = "Normale"
    DIFFICILE = "Difficile"
    EPICA = "Epica"


class StatoMissione(Enum):
    """Stato attuale della missione"""
    NON_ASSEGNATA = "Non Assegnata"
    ASSEGNATA = "Assegnata"
    IN_CORSO = "In Corso"
    COMPLETATA = "Completata"
    FALLITA = "Fallita"


class TipoBersaglioMissione(Enum):
    """Chi può essere bersaglio della missione"""
    PROPRIO_GUERRIERO = "Proprio Guerriero"
    GIOCATORE_STESSO = "Giocatore Stesso"
    GUERRIERO_AVVERSARIO = "Guerriero Avversario"
    GIOCATORE_AVVERSARIO = "Giocatore Avversario"
    QUALSIASI = "Qualsiasi"



@dataclass
class ObiettivoMissione:
    """Obiettivo che deve essere completato per la missione"""
    descrizione: str
    tipo_obiettivo: str  # "Uccidere", "Sopravvivere", "Controllare", etc.
    valore_richiesto: int = 1  # Quantità richiesta (es. "uccidi 2 guerrieri")
    condizioni_speciali: List[str] = None
    
    def __post_init__(self):
        if self.condizioni_speciali is None:
            self.condizioni_speciali = []


@dataclass
class RicompensaMissione:
    """Ricompensa per completare la missione"""
    punti_promozione: int = 0
    punti_destino: int = 0
    carte_extra: int = 0
    effetti_speciali: List[str] = None
    descrizione: str = ""
    
    def __post_init__(self):
        if self.effetti_speciali is None:
            self.effetti_speciali = []


class Missione:
    """
    Classe principale per rappresentare una carta Missione di Mutant Chronicles/Doomtrooper
    Implementa le regole ufficiali del regolamento
    """
    
    def __init__(self, nome: str, costo_azione: int = 1):
        """
        Inizializza una nuova Missione
        
        Args:
            nome: Nome della missione
            costo_azione: Costo in azioni per assegnare la missione (default 1)
        """
        self.nome = nome
        self.costo_azione = costo_azione
        
        # Attributi base della carta
        self.tipo = TipoMissione.GUERRIERO
        self.difficolta = DifficoltaMissione.NORMALE
        self.rarity = Rarity.COMMON
        
        # Chi può ricevere/eseguire la missione
        self.bersaglio = TipoBersaglioMissione.PROPRIO_GUERRIERO
        self.fazioni_permesse: List[Fazione] = []  # Fazioni che possono ricevere la missione
        self.corporazioni_specifiche: List[str] = []  # Corporazioni specifiche
        self.restrizioni_guerriero: List[str] = []  # Tipi di guerriero richiesti
        
        # Obiettivo e ricompense
        self.obiettivo = ObiettivoMissione("Completa l'obiettivo", "Generico")
        self.ricompensa = RicompensaMissione()
        
        # Testo della carta
        self.testo_carta = ""
        self.flavour_text = ""
        
        # Attributi per espansioni
        self.set_espansione = Set_Espansione.BASE
        self.numero_carta = ""
        
        # Restrizioni e condizioni
        self.restrizioni: List[str] = []
        self.keywords: List[str] = []
        self.condizioni_speciali: List[str] = []
        
        # Stato di gioco secondo il regolamento
        self.stato = StatoMissione.NON_ASSEGNATA
        self.assegnata_a: Optional[str] = None  # Nome del guerriero o "giocatore"
        self.assegnata_da: Optional[str] = None  # Chi ha assegnato la missione
        self.turno_assegnazione: int = 0
        self.progresso_attuale: int = 0
        
        # Meccaniche speciali
        self.opzionale = True  # Secondo regolamento, espletare è sempre opzionale
        self.completamento_automatico = True  # Se raggiunge obiettivo, deve terminare
        self.unica_per_bersaglio = True  # Non più copie stessa missione a stesso bersaglio
        
        # Tracking effetti
        self.effetti_attivi: List[str] = []
        self.modificatori_applicati: Dict[str, int] = {}
        self.quantita = 0
        
    def puo_essere_assegnata_a(self, bersaglio: Union[str, object]) -> Dict[str, Any]:
        """
        Verifica se la missione può essere assegnata al bersaglio specificato
        
        Args:
            bersaglio: Stringa "giocatore" o oggetto Guerriero
            
        Returns:
            Dict con risultato della verifica
        """
        risultato = {"puo_assegnare": True, "motivo": ""}
        
        # Controlla se è già assegnata
        if self.stato != StatoMissione.NON_ASSEGNATA:
            risultato["puo_assegnare"] = False
            risultato["motivo"] = f"Missione già {self.stato.value.lower()}"
            return risultato
        
        # Se bersaglio è stringa "giocatore"
        if isinstance(bersaglio, str) and bersaglio.lower() == "giocatore":
            if self.tipo == TipoMissione.GUERRIERO:
                risultato["puo_assegnare"] = False
                risultato["motivo"] = "Missione deve essere assegnata a un guerriero"
                return risultato
        
        # Se bersaglio è un guerriero
        elif hasattr(bersaglio, 'fazione'):
            if self.tipo == TipoMissione.GIOCATORE:
                risultato["puo_assegnare"] = False
                risultato["motivo"] = "Missione deve essere assegnata al giocatore"
                return risultato
            
            # Controlla restrizioni di fazione
            if self.fazioni_permesse and bersaglio.fazione not in self.fazioni_permesse:
                risultato["puo_assegnare"] = False
                risultato["motivo"] = f"Fazione {bersaglio.fazione.value} non permessa"
                return risultato
            
            # Controlla restrizioni di corporazione
            if (self.corporazioni_specifiche and 
                hasattr(bersaglio, 'corporazione') and 
                bersaglio.corporazione not in self.corporazioni_specifiche):
                risultato["puo_assegnare"] = False
                risultato["motivo"] = f"Corporazione {bersaglio.corporazione} non permessa"
                return risultato
            
            # Controlla restrizioni di tipo guerriero
            for restrizione in self.restrizioni_guerriero:
                if hasattr(bersaglio, 'keywords') and restrizione not in bersaglio.keywords:
                    if hasattr(bersaglio, 'tipo') and restrizione not in str(bersaglio.tipo.value):
                        risultato["puo_assegnare"] = False
                        risultato["motivo"] = f"Guerriero deve essere {restrizione}"
                        return risultato
        
        return risultato
    
    def assegna_a(self, bersaglio: Union[str, object], assegnata_da: str = "giocatore") -> bool:
        """
        Assegna la missione al bersaglio specificato
        
        Args:
            bersaglio: Chi riceve la missione
            assegnata_da: Chi assegna la missione
            
        Returns:
            True se assegnazione riuscita
        """
        verifica = self.puo_essere_assegnata_a(bersaglio)
        if not verifica["puo_assegnare"]:
            return False
        
        # Assegna la missione
        self.stato = StatoMissione.ASSEGNATA
        self.assegnata_da = assegnata_da
        
        if isinstance(bersaglio, str):
            self.assegnata_a = bersaglio
        else:
            self.assegnata_a = bersaglio.nome
        
        self.progresso_attuale = 0
        return True
    
    def avanza_progresso(self, quantita: int = 1) -> Dict[str, Any]:
        """
        Avanza il progresso della missione
        
        Args:
            quantita: Quanto avanzare il progresso
            
        Returns:
            Dict con informazioni sul progresso
        """
        if self.stato != StatoMissione.ASSEGNATA:
            return {"progresso": False, "motivo": "Missione non assegnata"}
        
        self.progresso_attuale += quantita
        
        # Controlla se obiettivo raggiunto
        if self.progresso_attuale >= self.obiettivo.valore_richiesto:
            return self.completa_missione()
        
        return {
            "progresso": True, 
            "progresso_attuale": self.progresso_attuale,
            "richiesto": self.obiettivo.valore_richiesto,
            "completata": False
        }
    
    def completa_missione(self) -> Dict[str, Any]:
        """
        Completa la missione secondo le regole del regolamento
        
        Returns:
            Dict con informazioni sulla ricompensa
        """
        if self.stato != StatoMissione.ASSEGNATA:
            return {"completata": False, "motivo": "Missione non assegnata"}
        
        # Secondo regolamento: se raggiungi obiettivo, DEVE essere terminata
        self.stato = StatoMissione.COMPLETATA
        
        ricompensa_ottenuta = {
            "completata": True,
            "punti_promozione": self.ricompensa.punti_promozione,
            "punti_destino": self.ricompensa.punti_destino,
            "carte_extra": self.ricompensa.carte_extra,
            "effetti_speciali": self.ricompensa.effetti_speciali.copy(),
            "assegnata_a": self.assegnata_a
        }
        
        return ricompensa_ottenuta
    
    def fallisci_missione(self, motivo: str = "") -> bool:
        """
        Fa fallire la missione
        
        Args:
            motivo: Motivo del fallimento
            
        Returns:
            True se fallimento applicato
        """
        if self.stato == StatoMissione.ASSEGNATA:
            self.stato = StatoMissione.FALLITA
            return True
        return False
    
    def puo_essere_riassegnata(self) -> bool:
        """
        Secondo regolamento: una volta completata, può essere riassegnata
        """
        return self.stato in [StatoMissione.COMPLETATA, StatoMissione.FALLITA]
    
    def reset_per_riassegnazione(self) -> None:
        """
        Resetta la missione per una nuova assegnazione
        """
        if self.puo_essere_riassegnata():
            self.stato = StatoMissione.NON_ASSEGNATA
            self.assegnata_a = None
            self.assegnata_da = None
            self.progresso_attuale = 0
            self.turno_assegnazione = 0
            self.effetti_attivi.clear()
            self.modificatori_applicati.clear()
    
    def aggiorna_obiettivo(self, descrizione: str, tipo_obiettivo: str, 
                          valore_richiesto: int, condizioni: List[str] = None) -> None:
        """Aggiorna l'obiettivo della missione"""
        self.obiettivo = ObiettivoMissione(
            descrizione, tipo_obiettivo, valore_richiesto, 
            condizioni or []
        )
    
    def aggiorna_ricompensa(self, punti_promozione: int = 0, punti_destino: int = 0,
                           carte_extra: int = 0, effetti_speciali: List[str] = None,
                           descrizione: str = "") -> None:
        """Aggiorna la ricompensa della missione"""
        self.ricompensa = RicompensaMissione(
            punti_promozione, punti_destino, carte_extra,
            effetti_speciali or [], descrizione
        )
    
    def aggiungi_restrizione_fazione(self, fazione: Fazione) -> None:
        """Aggiunge una fazione permessa"""
        if fazione not in self.fazioni_permesse:
            self.fazioni_permesse.append(fazione)
    
    def aggiungi_restrizione_guerriero(self, tipo_guerriero: str) -> None:
        """Aggiunge una restrizione per tipo di guerriero"""
        if tipo_guerriero not in self.restrizioni_guerriero:
            self.restrizioni_guerriero.append(tipo_guerriero)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializza la missione in un dizionario"""
        return {
            "nome": self.nome,
            "costo_azione": self.costo_azione,
            "tipo": self.tipo.value,
            "difficolta": self.difficolta.value,
            "rarity": self.rarity.value,
            "bersaglio": self.bersaglio.value,
            "fazioni_permesse": [f.value for f in self.fazioni_permesse],
            "corporazioni_specifiche": self.corporazioni_specifiche,
            "restrizioni_guerriero": self.restrizioni_guerriero,
            "obiettivo": {
                "descrizione": self.obiettivo.descrizione,
                "tipo_obiettivo": self.obiettivo.tipo_obiettivo,
                "valore_richiesto": self.obiettivo.valore_richiesto,
                "condizioni_speciali": self.obiettivo.condizioni_speciali
            },
            "ricompensa": {
                "punti_promozione": self.ricompensa.punti_promozione,
                "punti_destino": self.ricompensa.punti_destino,
                "carte_extra": self.ricompensa.carte_extra,
                "effetti_speciali": self.ricompensa.effetti_speciali,
                "descrizione": self.ricompensa.descrizione
            },
            "set_espansione": self.set_espansione,
            "numero_carta": self.numero_carta,
            "testo_carta": self.testo_carta,
            "flavour_text": self.flavour_text,
            "keywords": self.keywords,
            "restrizioni": self.restrizioni,
            "condizioni_speciali": self.condizioni_speciali,
            "stato_gioco": {
                "stato": self.stato.value,
                "assegnata_a": self.assegnata_a,
                "assegnata_da": self.assegnata_da,
                "turno_assegnazione": self.turno_assegnazione,
                "progresso_attuale": self.progresso_attuale,
                "opzionale": self.opzionale,
                "completamento_automatico": self.completamento_automatico,
                "unica_per_bersaglio": self.unica_per_bersaglio
            },
            "effetti_attivi": self.effetti_attivi,
            "modificatori_applicati": self.modificatori_applicati
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Missione':
        """Crea una Missione da un dizionario"""
        missione = cls(data["nome"], data["costo_azione"])
        
        missione.tipo = TipoMissione(data["tipo"])
        missione.difficolta = DifficoltaMissione(data["difficolta"])
        missione.rarity = Rarity(data["rarity"])
        missione.bersaglio = TipoBersaglioMissione(data["bersaglio"])
        
        missione.fazioni_permesse = [Fazione(f) for f in data["fazioni_permesse"]]
        missione.corporazioni_specifiche = data["corporazioni_specifiche"]
        missione.restrizioni_guerriero = data["restrizioni_guerriero"]
        
        # Ricostruisce obiettivo
        obj_data = data["obiettivo"]
        missione.obiettivo = ObiettivoMissione(
            obj_data["descrizione"],
            obj_data["tipo_obiettivo"],
            obj_data["valore_richiesto"],
            obj_data["condizioni_speciali"]
        )
        
        # Ricostruisce ricompensa
        ric_data = data["ricompensa"]
        missione.ricompensa = RicompensaMissione(
            ric_data["punti_promozione"],
            ric_data["punti_destino"],
            ric_data["carte_extra"],
            ric_data["effetti_speciali"],
            ric_data["descrizione"]
        )
        
        missione.set_espansione = data["set_espansione"]
        missione.numero_carta = data["numero_carta"]
        missione.testo_carta = data["testo_carta"]
        missione.flavour_text = data["flavour_text"]
        missione.keywords = data["keywords"]
        missione.restrizioni = data["restrizioni"]
        missione.condizioni_speciali = data["condizioni_speciali"]
        
        # Ripristina stato di gioco
        stato = data["stato_gioco"]
        missione.stato = StatoMissione(stato["stato"])
        missione.assegnata_a = stato["assegnata_a"]
        missione.assegnata_da = stato["assegnata_da"]
        missione.turno_assegnazione = stato["turno_assegnazione"]
        missione.progresso_attuale = stato["progresso_attuale"]
        missione.opzionale = stato["opzionale"]
        missione.completamento_automatico = stato["completamento_automatico"]
        missione.unica_per_bersaglio = stato["unica_per_bersaglio"]
        
        missione.effetti_attivi = data["effetti_attivi"]
        missione.modificatori_applicati = data["modificatori_applicati"]
        
        return missione
    
    def __str__(self) -> str:
        """Rappresentazione stringa della missione"""
        stato_str = f" [{self.stato.value}]" if self.stato != StatoMissione.NON_ASSEGNATA else ""
        assegnata_str = f" -> {self.assegnata_a}" if self.assegnata_a else ""
        progresso_str = ""
        if self.stato == StatoMissione.ASSEGNATA:
            progresso_str = f" ({self.progresso_attuale}/{self.obiettivo.valore_richiesto})"
        
        return (f"{self.nome} ({self.tipo.value}){stato_str}{assegnata_str}{progresso_str} - "
                f"Ricompensa: {self.ricompensa.punti_promozione}P")
    
    def __repr__(self) -> str:
        return f"Missione('{self.nome}', tipo={self.tipo.value})"


# Funzioni di utilità per creare missioni specifiche

def crea_missione_uccisione(nome: str, bersagli_richiesti: int = 1, 
                           punti_promozione: int = 2) -> Missione:
    """Crea una missione di uccisione standard"""
    missione = Missione(nome)
    missione.aggiorna_obiettivo(
        f"Uccidi {bersagli_richiesti} guerriero/i",
        "Uccidere",
        bersagli_richiesti
    )
    missione.aggiorna_ricompensa(punti_promozione=punti_promozione)
    return missione

def crea_missione_sopravvivenza(nome: str, turni_richiesti: int = 3,
                               punti_promozione: int = 1) -> Missione:
    """Crea una missione di sopravvivenza"""
    missione = Missione(nome)
    missione.aggiorna_obiettivo(
        f"Sopravvivi per {turni_richiesti} turni",
        "Sopravvivere",
        turni_richiesti
    )
    missione.aggiorna_ricompensa(punti_promozione=punti_promozione)
    return missione

def crea_missione_corporazione(nome: str, fazione: Fazione, 
                              obiettivo_desc: str, punti_promozione: int = 2) -> Missione:
    """Crea una missione specifica per una corporazione"""
    missione = Missione(nome)
    missione.aggiungi_restrizione_fazione(fazione)
    missione.aggiorna_obiettivo(obiettivo_desc, "Speciale", 1)
    missione.aggiorna_ricompensa(punti_promozione=punti_promozione)
    return missione


# Esempi di utilizzo

if __name__ == "__main__":
    # Esempio 1: Missione di uccisione standard
    missione_caccia = crea_missione_uccisione("Caccia al Nemico", 2, 3)
    missione_caccia.testo_carta = "Uccidi 2 guerrieri nemici. Ricompensa: 3 Punti Promozione."
    print(f"✓ {missione_caccia}")
    
    # Esempio 2: Missione di sopravvivenza
    missione_resistenza = crea_missione_sopravvivenza("Resistenza Eroica", 4, 2)
    print(f"✓ {missione_resistenza}")
    
    # Esempio 3: Missione specifica Bauhaus
    missione_bauhaus = crea_missione_corporazione(
        "Operazione Heimburg", 
        Fazione.BAUHAUS,
        "Controlla una Fortificazione nemica",
        3
    )
    print(f"✓ {missione_bauhaus}")
    
    # Test meccaniche di assegnazione
    print(f"\n=== TEST ASSEGNAZIONE ===")
    
    # Simula un guerriero per il test
    class GuerrieroTest:
        def __init__(self, nome, fazione):
            self.nome = nome
            self.fazione = fazione
            self.keywords = []
    
    guerriero_bauhaus = GuerrieroTest("Blitzer Bauhaus", Fazione.BAUHAUS)
    
    # Test assegnazione corretta
    verifica = missione_bauhaus.puo_essere_assegnata_a(guerriero_bauhaus)
    print(f"Può assegnare a Bauhaus: {verifica['puo_assegnare']}")
    
    if verifica['puo_assegnare']:
        success = missione_bauhaus.assegna_a(guerriero_bauhaus)
        print(f"Missione assegnata: {success}")
        print(f"Stato missione: {missione_bauhaus}")
        
        # Test progresso
        progresso = missione_bauhaus.avanza_progresso(1)
        print(f"Missione completata: {progresso['completata']}")
        if progresso['completata']:
            print(f"Ricompensa: {progresso['punti_promozione']} Punti Promozione")
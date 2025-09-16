"""
Modulo per la rappresentazione delle carte Arte di Mutant Chronicles/Doomtrooper
Versione corretta secondo il regolamento ufficiale
"""

from enum import Enum
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import json
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione, DisciplinaArte, Abilita  # Corretto percorso import


class TipoArte(Enum):
    """Tipi di carte Arte"""
    NORMALE = "Normale"
    RITUALE = "Rituale"
    BENEDIZIONE = "Benedizione"
    MALEDIZIONE = "Maledizione"
    PROTEZIONE = "Protezione"
    INVOCAZIONE = "Invocazione"
    INCANTESIMO_COMBATTIMENTO = "Incantesimo di Combattimento"
    INCANTESIMO_PERSONALE = "Incantesimo Personale di Combattimento"



class BersaglioArte(Enum):
    """Possibili bersagli delle carte Arte"""
    GUERRIERO_PROPRIO = "Guerriero Proprio"
    GUERRIERO_AVVERSARIO = "Guerriero Avversario"
    QUALSIASI_GUERRIERO = "Qualsiasi Guerriero"
    TUTTI_GUERRIERI = "Tutti i Guerrieri"
    TUTTI_GUERRIERI_PROPRI = "Tutti i Guerrieri Propri"
    TUTTI_GUERRIERI_AVVERSARI = "Tutti i Guerrieri Avversari"
    GUERRIERO_FRATELLANZA = "Guerriero Fratellanza"
    GIOCATORE = "Giocatore"
    ENTRAMBI_GIOCATORI = "Entrambi i Giocatori"
    SENZA_BERSAGLIO = "Senza Bersaglio"
    MAESTRO = "Maestro che lancia l'incantesimo"


class DurataArte(Enum):
    """Durata dell'effetto delle carte Arte"""
    ISTANTANEA = "Istantanea"
    PERMANENTE = "Permanente"
    FINO_FINE_TURNO = "Fino Fine Turno"
    FINO_PROSSIMO_TURNO = "Fino Prossimo Turno"
    CONTINUA = "Continua"
    FINO_FINE_COMBATTIMENTO = "Fino Fine Combattimento"


class TimingArte(Enum):
    """Quando può essere giocata una carta Arte"""
    TURNO_PROPRIO = "Turno Proprio"
    TURNO_AVVERSARIO = "Turno Avversario"
    PROSSIMO_TURNO = "Prossimo Turno Proprio"
    IN_OGNI_MOMENTO = "In ogni momento"
    IN_COMBATTIMENTO = "In Combattimento"
    PRIMA_COMBATTIMENTO = "Prima del Combattimento"
    DOPO_COMBATTIMENTO = "Dopo il Combattimento"
    DURANTE_MODIFICATORI = "Durante Modificatori Combattimento"
    DURANTE_FASI_GIOCO = "Durante Fasi Gioco"
    PARTITA = "Partita"



class TipoIcona(Enum):
    """Tipo di icona per gestione post-gioco"""
    ASSEGNAZIONE = "Assegnazione"  # (+)
    SCARTO = "Scarto"              # (-)
    ELIMINAZIONE = "Eliminazione"  # (x)


@dataclass
class EffettoArte:
    """Rappresenta l'effetto di una carta Arte"""
    tipo_effetto: str  # es. "Modificatore", "Danno", "Guarigione", "Controllo"
    valore: int = 0  # valore numerico dell'effetto (se applicabile)
    statistica_target: str = ""  # quale statistica viene modificata
    descrizione_effetto: str = ""
    condizioni: List[str] = None  # condizioni per attivare l'effetto
    
    def __post_init__(self):
        if self.condizioni is None:
            self.condizioni = []


class Arte:
    """
    Classe per rappresentare una carta Arte di Mutant Chronicles/Doomtrooper
    Implementa le regole ufficiali del regolamento
    """
    
    def __init__(self, nome: str, valore: int = 0):
        """
        Inizializza una nuova carta Arte
        
        Args:
            nome: Nome della carta Arte
            valore: Costo in Destiny Points per giocare la carta
        """
        self.nome = nome
        self.valore = valore
        
        # Attributi base della carta
        self.tipo = TipoArte.NORMALE
        self.rarity = Rarity.COMMON
        self.disciplina = DisciplinaArte.CAMBIAMENTO
        
        # Meccaniche di gioco
        self.bersaglio = BersaglioArte.SENZA_BERSAGLIO
        self.durata = DurataArte.ISTANTANEA
        self.timing = TimingArte.TURNO_PROPRIO
        self.icona_gestione = TipoIcona.SCARTO
        
        # Effetti della carta
        self.effetti: List[EffettoArte] = []
        
        # Testo della carta
        self.testo_carta = ""
        self.flavour_text = ""
        
        # Restrizioni secondo il regolamento
        self.fazioni_permesse: List[Fazione] = [Fazione.FRATELLANZA]  # Solo Fratellanza di default
        self.restrizioni: List[str] = []
        self.keywords: List[str] = []
        self.maestri_richiesti: List[str] = []  # Quali maestri possono lanciare
        
        # Attributi per espansioni
        self.set_espansione = Set_Espansione.BASE
        self.numero_carta = ""
        
        # Stato di gioco
        self.in_gioco = False  # per carte con effetto permanente
        self.utilizzata = False
        self.bersagli_attuali: List[str] = []  # nomi dei guerrieri targetati
        self.punti_destino_spesi = 0  # Per incantesimi potenziabili
        
        # Modificatori applicati (per tracking)
        self.modificatori_applicati: Dict[str, Dict[str, int]] = {}
        
        # Contatori per effetti speciali
        self.contatori_speciali: Dict[str, int] = {}
        self.quantita = 0
        self.quantita_minima_consigliata = 0  # per la creazione del mazzo
        self.fondamentale = False  # se la carta è fondamentale per il mazzo

    def puo_essere_associata_a_fazione(self, fazione: Fazione) -> bool:
        """
        Controlla se la carta può essere associata dalla fazione specificata
        Secondo il regolamento: solo Fratellanza e pochi altri Doomtrooper
        """
        return fazione in self.fazioni_permesse
    
    def puo_essere_associata_a_guerriero(self, guerriero: Any) -> Dict[str, Any]:
        """
        Verifica se un guerriero può lanciare questo incantesimo
        Secondo il regolamento: deve essere un Maestro della disciplina richiesta
        """
        risultato = {"puo_lanciare": True, "errori": []}
        
        # Deve essere della Fratellanza o fazione permessa
        if not self.puo_essere_associata_a_fazione(guerriero.fazione) and "Apostata" not in guerriero.keywords:  # Apostata possono usare incantesimi dell'arte                
            risultato["puo_lanciare"] = False
            risultato["errori"].append(f"Solo {[f.value for f in self.fazioni_permesse]} ed gli Apostati possono usare l'Arte")
        
        # Verifica gestione della disciplina (se specificata)
        if len(guerriero.abilita) > 0:
            discipline_arte_guerriero = [abilita.nome for abilita in guerriero.abilita if abilita.tipo == "Arte"]   
            if [DisciplinaArte.TUTTE.value, self.disciplina.value] not in discipline_arte_guerriero:
                risultato["puo_lanciare"] = False
                risultato["errori"].append(f"Richiede disciplina in {self.disciplina.value}")      
        


        return risultato
    
    
    def puo_essere_giocata_da_guerriero(self, guerriero: Any) -> Dict[str, Any]:
        """
        Verifica se un guerriero può lanciare questo incantesimo
        Secondo il regolamento: deve essere un Maestro della disciplina richiesta
        """
        risultato = self.puo_essere_associata_a_guerriero(guerriero)
        
        # Deve essere della Fratellanza o fazione permessa
        if not self.puo_essere_associata_a_fazione(guerriero.fazione):
            risultato["puo_lanciare"] = False
            risultato["errori"].append(f"Solo {[f.value for f in self.fazioni_permesse]} possono usare l'Arte")
        
        # Deve essere nella Squadra (anche in copertura va bene)
        if hasattr(guerriero, 'area_gioco'):
            from source.cards.Guerriero import AreaGioco
            if guerriero.area_gioco not in [AreaGioco.SQUADRA]:
                risultato["puo_lanciare"] = False
                risultato["errori"].append("Il maestro deve essere nella Squadra per lanciare incantesimi")
        
        # Non può influenzare guerrieri Oscura Legione (tranne conversioni)
        if hasattr(guerriero, 'fazione') and guerriero.fazione == Fazione.OSCURA_LEGIONE:
            #if "Eretico" not in guerriero.keywords:  # Eretici possono usare su tutti
                risultato["puo_lanciare"] = False
                risultato["errori"].append("Fratellanza non può aiutare l'Oscura Legione")
        
        return risultato
    
    def aggiungi_fazione_permessa(self, fazione: Fazione) -> None:
        """Aggiunge una fazione che può giocare questa carta (rare eccezioni)"""
        if fazione not in self.fazioni_permesse:
            self.fazioni_permesse.append(fazione)
    
    def rimuovi_fazione_permessa(self, fazione: Fazione) -> None:
        """Rimuove una fazione dalle fazioni permesse"""
        if fazione in self.fazioni_permesse and len(self.fazioni_permesse) > 1:
            self.fazioni_permesse.remove(fazione)
    
    def aggiungi_effetto(self, tipo_effetto: str, valore: int = 0, 
                        statistica_target: str = "", descrizione: str = "",
                        condizioni: List[str] = None) -> None:
        """Aggiunge un effetto alla carta Arte"""
        effetto = EffettoArte(
            tipo_effetto=tipo_effetto,
            valore=valore,
            statistica_target=statistica_target,
            descrizione_effetto=descrizione,
            condizioni=condizioni or []
        )
        self.effetti.append(effetto)
    
    def ha_keyword(self, keyword: str) -> bool:
        """Controlla se la carta ha una specifica keyword"""
        return keyword.lower() in [k.lower() for k in self.keywords]
    
    def richiede_bersaglio(self) -> bool:
        """Controlla se la carta richiede un bersaglio per essere giocata"""
        return self.bersaglio != BersaglioArte.SENZA_BERSAGLIO
    
    def bersaglio_valido(self, bersaglio: str, guerrieri_propri: List[str], 
                        guerrieri_avversari: List[str], 
                        guerrieri_fratellanza: List[str] = None) -> bool:
        """
        Controlla se un bersaglio è valido per questa carta Arte
        
        Args:
            bersaglio: Nome del guerriero bersaglio
            guerrieri_propri: Lista dei nomi dei guerrieri propri in gioco
            guerrieri_avversari: Lista dei nomi dei guerrieri avversari in gioco
            guerrieri_fratellanza: Lista dei guerrieri della Fratellanza
        """
        if self.bersaglio == BersaglioArte.SENZA_BERSAGLIO:
            return True
        elif self.bersaglio == BersaglioArte.GUERRIERO_PROPRIO:
            return bersaglio in guerrieri_propri
        elif self.bersaglio == BersaglioArte.GUERRIERO_AVVERSARIO:
            return bersaglio in guerrieri_avversari
        elif self.bersaglio == BersaglioArte.QUALSIASI_GUERRIERO:
            return bersaglio in (guerrieri_propri + guerrieri_avversari)
        elif self.bersaglio == BersaglioArte.GUERRIERO_FRATELLANZA:
            return bersaglio in (guerrieri_fratellanza or [])
        else:
            # Per bersagli multipli, sarà gestito dalla logica di gioco
            return True
    
    def puo_essere_giocata(self, destiny_points: int, fazione_giocatore: Fazione,
                          timing_corrente: TimingArte, maestro: Any = None,
                          condizioni_gioco: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Controlla se la carta può essere giocata nel momento attuale
        
        Args:
            destiny_points: Punti Destino disponibili del giocatore
            fazione_giocatore: Fazione del giocatore
            timing_corrente: Timing corrente del gioco
            maestro: Guerriero che vuole lanciare l'incantesimo
            condizioni_gioco: Condizioni aggiuntive del gioco
            
        Returns:
            Dizionario con risultato e eventuali errori
        """
        risultato = {"puo_giocare": True, "errori": []}
        
        # Controllo costo base
        if destiny_points < self.valore:
            risultato["puo_giocare"] = False
            risultato["errori"].append(f"Destiny Points insufficienti: richiesti {self.valore}, disponibili {destiny_points}")
        
        # Controllo fazione
        if not self.puo_essere_associata_a_fazione(fazione_giocatore):
            risultato["puo_giocare"] = False
            risultato["errori"].append(f"Fazione {fazione_giocatore.value} non può giocare questa carta")
        
        # Controllo maestro (se specificato)
        if maestro:
            verifica_maestro = self.puo_essere_giocata_da_guerriero(maestro)
            if not verifica_maestro["puo_lanciare"]:
                risultato["puo_giocare"] = False
                risultato["errori"].extend(verifica_maestro["errori"])
        
        # Controllo timing
        if self.timing != TimingArte.QUALSIASI_MOMENTO and self.timing != timing_corrente:
            risultato["puo_giocare"] = False
            risultato["errori"].append(f"Timing non corretto: richiesto {self.timing.value}, attuale {timing_corrente.value}")
        
        # Controllo se già utilizzata (per carte monouso)
        if self.utilizzata and self.durata == DurataArte.ISTANTANEA:
            risultato["puo_giocare"] = False
            risultato["errori"].append("Carta già utilizzata")
        
        # Controlli specifici per incantesimi di combattimento
        if self.tipo in [TipoArte.INCANTESIMO_COMBATTIMENTO, TipoArte.INCANTESIMO_PERSONALE]:
            if timing_corrente != TimingArte.IN_COMBATTIMENTO:
                risultato["puo_giocare"] = False
                risultato["errori"].append("Incantesimi di combattimento solo durante il combattimento")
            
            if self.tipo == TipoArte.INCANTESIMO_PERSONALE and maestro:
                # Incantesimo personale: maestro deve essere coinvolto nel combattimento
                combattimento_attivo = condizioni_gioco.get("combattimento_attivo", {}) if condizioni_gioco else {}
                if (maestro.nome not in combattimento_attivo.get("attaccante", "") and 
                    maestro.nome not in combattimento_attivo.get("difensore", "")):
                    risultato["puo_giocare"] = False
                    risultato["errori"].append("Incantesimo personale: maestro deve essere coinvolto nel combattimento")
        
        return risultato
    
    def applica_effetto(self, bersaglio: Union[str, List[str]], 
                       guerrieri_in_gioco: Dict[str, Any],
                       punti_destino_extra: int = 0,
                       maestro: Any = None) -> Dict[str, Any]:
        """
        Applica l'effetto della carta Arte
        
        Args:
            bersaglio: Nome/i del/i bersaglio/i
            guerrieri_in_gioco: Dizionario dei guerrieri in gioco
            punti_destino_extra: Punti Destino extra spesi per potenziare
            maestro: Guerriero che lancia l'incantesimo
            
        Returns:
            Risultato dell'applicazione dell'effetto
        """
        risultato = {
            "successo": True,
            "effetti_applicati": [],
            "errori": [],
            "modificatori_applicati": {},
            "punti_destino_totali_spesi": self.valore + punti_destino_extra
        }
        
        # Salva i punti destino spesi per incantesimi potenziabili
        self.punti_destino_spesi = punti_destino_extra
        
        # Determina i bersagli effettivi
        bersagli_effettivi = []
        if isinstance(bersaglio, str):
            bersagli_effettivi = [bersaglio] if bersaglio != "" else []
        else:
            bersagli_effettivi = bersaglio
        
        # Verifica immunità all'Arte
        bersagli_validi = []
        for nome_bersaglio in bersagli_effettivi:
            if nome_bersaglio in guerrieri_in_gioco:
                guerriero = guerrieri_in_gioco[nome_bersaglio]
                if hasattr(guerriero, 'keywords') and "Immune all'Arte" in guerriero.keywords:
                    risultato["errori"].append(f"{nome_bersaglio} è immune all'Arte")
                else:
                    bersagli_validi.append(nome_bersaglio)
        
        # Applica ogni effetto
        for effetto in self.effetti:
            try:
                effetto_risultato = self._applica_singolo_effetto(
                    effetto, bersagli_validi, guerrieri_in_gioco, punti_destino_extra, maestro
                )
                risultato["effetti_applicati"].append(effetto_risultato)
                
                # Traccia i modificatori applicati
                if "modificatori" in effetto_risultato:
                    risultato["modificatori_applicati"].update(effetto_risultato["modificatori"])
                    
            except Exception as e:
                risultato["successo"] = False
                risultato["errori"].append(f"Errore applicando effetto {effetto.tipo_effetto}: {str(e)}")
        
        # Gestione post-effetto secondo l'icona
        if self.icona_gestione == TipoIcona.ASSEGNAZIONE:
            self.in_gioco = True
            self.bersagli_attuali = bersagli_validi
        elif self.icona_gestione == TipoIcona.SCARTO:
            self.utilizzata = True
        elif self.icona_gestione == TipoIcona.ELIMINAZIONE:
            self.utilizzata = True
            # La carta sarà eliminata dal gioco
        
        return risultato
    
    def _applica_singolo_effetto(self, effetto: EffettoArte, bersagli: List[str], 
                               guerrieri_in_gioco: Dict[str, Any], 
                               punti_destino_extra: int = 0,
                               maestro: Any = None) -> Dict[str, Any]:
        """Applica un singolo effetto ai bersagli specificati"""
        risultato = {
            "tipo_effetto": effetto.tipo_effetto,
            "bersagli_interessati": [],
            "modificatori": {}
        }
        
        for nome_bersaglio in bersagli:
            if nome_bersaglio in guerrieri_in_gioco:
                guerriero = guerrieri_in_gioco[nome_bersaglio]
                
                if effetto.tipo_effetto == "Modificatore" and effetto.statistica_target:
                    # Calcola valore con bonus da punti destino extra
                    valore_effetto = effetto.valore + punti_destino_extra
                    guerriero.applica_modificatore(effetto.statistica_target, valore_effetto)
                    risultato["bersagli_interessati"].append(nome_bersaglio)
                    risultato["modificatori"][nome_bersaglio] = {
                        effetto.statistica_target: valore_effetto
                    }
                    
                    # Traccia il modificatore per la rimozione successiva
                    if nome_bersaglio not in self.modificatori_applicati:
                        self.modificatori_applicati[nome_bersaglio] = {}
                    self.modificatori_applicati[nome_bersaglio][effetto.statistica_target] = valore_effetto
                
                elif effetto.tipo_effetto == "Guarigione":
                    if hasattr(guerriero, 'guarisci') and guerriero.guarisci():
                        risultato["bersagli_interessati"].append(nome_bersaglio)
                
                elif effetto.tipo_effetto == "Protezione":
                    # Aggiunge protezione speciale
                    if not hasattr(guerriero, 'protezioni_attive'):
                        guerriero.protezioni_attive = []
                    guerriero.protezioni_attive.append(effetto.descrizione_effetto)
                    risultato["bersagli_interessati"].append(nome_bersaglio)
                
                elif effetto.tipo_effetto == "Controllo":
                    # Effetti di controllo
                    if effetto.descrizione_effetto == "tap" and guerriero.pronto:
                        guerriero.pronto = False
                        risultato["bersagli_interessati"].append(nome_bersaglio)
                    elif effetto.descrizione_effetto == "untap" and not guerriero.pronto:
                        guerriero.pronto = True
                        risultato["bersagli_interessati"].append(nome_bersaglio)
                
                elif effetto.tipo_effetto == "Benedizione":
                    # Benedizioni permanenti
                    if not hasattr(guerriero, 'benedizioni_attive'):
                        guerriero.benedizioni_attive = []
                    guerriero.benedizioni_attive.append(self.nome)
                    risultato["bersagli_interessati"].append(nome_bersaglio)
        
        return risultato
    
    def rimuovi_effetto(self, guerrieri_in_gioco: Dict[str, Any]) -> Dict[str, Any]:
        """Rimuove l'effetto della carta Arte (per effetti non permanenti)"""
        risultato = {"successo": True, "modificatori_rimossi": {}}
        
        # Rimuovi modificatori applicati
        for nome_guerriero, modificatori in self.modificatori_applicati.items():
            if nome_guerriero in guerrieri_in_gioco:
                guerriero = guerrieri_in_gioco[nome_guerriero]
                for stat, valore in modificatori.items():
                    # Applica l'opposto del modificatore
                    guerriero.applica_modificatore(stat, -valore)
                    
                risultato["modificatori_rimossi"][nome_guerriero] = modificatori
        
        # Reset stato carta
        self.in_gioco = False
        self.bersagli_attuali.clear()
        self.modificatori_applicati.clear()
        self.punti_destino_spesi = 0
        
        return risultato
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte la carta Arte in un dizionario per serializzazione"""
        return {
            "nome": self.nome,
            "valore": self.valore,
            "tipo": self.tipo.value,
            "rarity": self.rarity.value,
            "disciplina": self.disciplina.value,
            "fazioni_permesse": [f.value for f in self.fazioni_permesse],
            "bersaglio": self.bersaglio.value,
            "durata": self.durata.value,
            "timing": self.timing.value,
            "icona_gestione": self.icona_gestione.value,
            "set_espansione": self.set_espansione,
            "numero_carta": self.numero_carta,
            "effetti": [
                {
                    "tipo_effetto": eff.tipo_effetto,
                    "valore": eff.valore,
                    "statistica_target": eff.statistica_target,
                    "descrizione_effetto": eff.descrizione_effetto,
                    "condizioni": eff.condizioni
                } for eff in self.effetti
            ],
            "testo_carta": self.testo_carta,
            "flavour_text": self.flavour_text,
            "keywords": self.keywords,
            "restrizioni": self.restrizioni,
            #"maestri_richiesti": self.maestri_richiesti,
            "stato_gioco": {
                "in_gioco": self.in_gioco,
                "utilizzata": self.utilizzata,
                "bersagli_attuali": self.bersagli_attuali,
                "punti_destino_spesi": self.punti_destino_spesi
            },
            "contatori_speciali": self.contatori_speciali
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Arte':
        """Crea una carta Arte da un dizionario"""
        arte = cls(data["nome"], data["valore"])
        
        arte.tipo = TipoArte(data["tipo"])
        arte.rarity = Rarity(data["rarity"])
        
        # Gestione disciplina (può non essere presente in dati vecchi)
        if "disciplina" in data:
            arte.disciplina = DisciplinaArte(data["disciplina"])
        
        arte.fazioni_permesse = [Fazione(f) for f in data["fazioni_permesse"]]
        arte.bersaglio = BersaglioArte(data["bersaglio"])
        arte.durata = DurataArte(data["durata"])
        arte.timing = TimingArte(data["timing"])
        
        # Gestione icona (può non essere presente in dati vecchi)
        if "icona_gestione" in data:
            arte.icona_gestione = TipoIcona(data["icona_gestione"])
        
        arte.set_espansione = data["set_espansione"]
        arte.numero_carta = data["numero_carta"]
        arte.testo_carta = data["testo_carta"]
        arte.flavour_text = data["flavour_text"]
        arte.keywords = data["keywords"]
        arte.restrizioni = data["restrizioni"]
        arte.quantita_minima_consigliata = data.get("quantita_minima_consigliata", 0)
        arte.fondamentale = data.get("fondamentale", False)
        
        # Gestione maestri richiesti (nuovo campo)
        #if "maestri_richiesti" in data:
        #    arte.maestri_richiesti = data["maestri_richiesti"]
        
        arte.contatori_speciali = data["contatori_speciali"]
        
        # Ripristina stato di gioco
        stato = data["stato_gioco"]
        arte.in_gioco = stato["in_gioco"]
        arte.utilizzata = stato["utilizzata"]
        arte.bersagli_attuali = stato["bersagli_attuali"]
        
        # Gestione punti destino spesi (nuovo campo)
        if "punti_destino_spesi" in stato:
            arte.punti_destino_spesi = stato["punti_destino_spesi"]
        
        # Ricostruisce effetti
        for eff_data in data["effetti"]:
            arte.aggiungi_effetto(
                eff_data["tipo_effetto"],
                eff_data["valore"],
                eff_data["statistica_target"],
                eff_data["descrizione_effetto"],
                eff_data["condizioni"]
            )
        
        return arte
    
    def __str__(self) -> str:
        """Rappresentazione stringa della carta Arte"""
        fazioni_str = ", ".join([f.value for f in self.fazioni_permesse])
        disciplina_str = f" ({self.disciplina.value})" if hasattr(self, 'disciplina') else ""
        return (f"{self.nome} (Costo: {self.valore}) - "
                f"Tipo: {self.tipo.value}{disciplina_str} - "
                f"Fazioni: [{fazioni_str}]")
    
    def __repr__(self) -> str:
        return f"Arte('{self.nome}', {self.valore})"


# Funzioni di utilità per creare carte Arte specifiche

def crea_arte_fratellanza(nome: str, costo: int = 0, disciplina: DisciplinaArte = DisciplinaArte.CAMBIAMENTO) -> Arte:
    """Crea una carta Arte standard della Fratellanza"""
    arte = Arte(nome, costo)
    arte.disciplina = disciplina
    arte.fazioni_permesse = [Fazione.FRATELLANZA]
    arte.set_espansione = Set_Espansione.BASE
    return arte

def crea_arte_universale(nome: str, costo: int = 0) -> Arte:
    """
    Crea una carta Arte che può essere giocata da più fazioni
    ATTENZIONE: Usare solo per casi speciali secondo il regolamento
    """
    arte = Arte(nome, costo)
    # Solo in casi eccezionali alcune carte possono essere usate da altre fazioni
    arte.fazioni_permesse = [Fazione.FRATELLANZA]  # Default solo Fratellanza
    arte.restrizioni.append("Verificare regolamento per fazioni aggiuntive")
    return arte

def crea_arte_inquisition(nome: str, costo: int = 0) -> Arte:
    """Crea una carta Arte dell'espansione Inquisition"""
    arte = Arte(nome, costo)
    arte.set_espansione = Set_Espansione.INQUISITION
    # Alcune carte Inquisition possono essere usate da Imperiale, ma raro
    arte.fazioni_permesse = [Fazione.FRATELLANZA]
    return arte

def crea_benedizione(nome: str, costo: int = 1, disciplina: DisciplinaArte = DisciplinaArte.CAMBIAMENTO) -> Arte:
    """Crea una carta Arte di tipo Benedizione"""
    arte = crea_arte_fratellanza(nome, costo, disciplina)
    arte.tipo = TipoArte.BENEDIZIONE
    arte.bersaglio = BersaglioArte.GUERRIERO_PROPRIO
    arte.durata = DurataArte.PERMANENTE
    arte.icona_gestione = TipoIcona.ASSEGNAZIONE
    arte.keywords.append("Benedizione")
    return arte

def crea_maledizione(nome: str, costo: int = 1, disciplina: DisciplinaArte = DisciplinaArte.MANIPOLAZIONE) -> Arte:
    """Crea una carta Arte di tipo Maledizione"""
    arte = crea_arte_fratellanza(nome, costo, disciplina)
    arte.tipo = TipoArte.MALEDIZIONE
    arte.bersaglio = BersaglioArte.GUERRIERO_AVVERSARIO
    arte.durata = DurataArte.PERMANENTE
    arte.icona_gestione = TipoIcona.ASSEGNAZIONE
    arte.keywords.append("Maledizione")
    return arte

def crea_incantesimo_combattimento(nome: str, costo: int = 1, 
                                 disciplina: DisciplinaArte = DisciplinaArte.CINETICA) -> Arte:
    """Crea un Incantesimo di Combattimento"""
    arte = crea_arte_fratellanza(nome, costo, disciplina)
    arte.tipo = TipoArte.INCANTESIMO_COMBATTIMENTO
    arte.timing = TimingArte.IN_COMBATTIMENTO
    arte.durata = DurataArte.FINO_FINE_COMBATTIMENTO
    arte.icona_gestione = TipoIcona.SCARTO
    arte.keywords.append("Incantesimo di Combattimento")
    return arte

def crea_incantesimo_personale(nome: str, costo: int = 1,
                              disciplina: DisciplinaArte = DisciplinaArte.CINETICA) -> Arte:
    """Crea un Incantesimo Personale di Combattimento"""
    arte = crea_arte_fratellanza(nome, costo, disciplina)
    arte.tipo = TipoArte.INCANTESIMO_PERSONALE
    arte.timing = TimingArte.IN_COMBATTIMENTO
    arte.durata = DurataArte.FINO_FINE_COMBATTIMENTO
    arte.icona_gestione = TipoIcona.SCARTO
    arte.bersaglio = BersaglioArte.SENZA_BERSAGLIO  # Solo su se stesso
    arte.keywords.append("Incantesimo Personale")
    arte.restrizioni.append("Solo se il maestro è coinvolto nel combattimento")
    return arte


# Esempi di utilizzo corretto secondo il regolamento

if __name__ == "__main__":
    print("=== ESEMPI CARTE ARTE CORRETTE ===")
    
    # Benedizione base
    mystical_shield = crea_benedizione("Mystical Shield", 1, DisciplinaArte.CAMBIAMENTO)
    mystical_shield.aggiungi_effetto("Modificatore", 1, "combattimento", 
                                    "Il guerriero ottiene +1 Combattimento")
    print(f"✓ {mystical_shield}")
    print(f"  Può essere usata da: {[f.value for f in mystical_shield.fazioni_permesse]}")
    
    # Incantesimo di combattimento potenziabile
    righteous_fury = crea_incantesimo_combattimento("Righteous Fury", 2, DisciplinaArte.CINETICA)
    righteous_fury.aggiungi_effetto("Modificatore", 3, "combattimento",
                                   "Combattimento +3 + punti destino extra spesi")
    righteous_fury.bersaglio = BersaglioArte.GUERRIERO_PROPRIO
    print(f"✓ {righteous_fury}")
    
    # Maledizione
    dark_curse = crea_maledizione("Dark Curse", 2, DisciplinaArte.MANIPOLAZIONE)
    dark_curse.aggiungi_effetto("Modificatore", -1, "combattimento",
                               "Il guerriero subisce -1 Combattimento")
    print(f"✓ {dark_curse}")
    
    print(f"\n=== CORREZIONI APPLICATE ===")
    print("✓ Restrizioni fazioni corrette: solo Fratellanza (salvo eccezioni)")
    print("✓ Aggiunte Discipline dell'Arte dal regolamento")
    print("✓ Implementati Incantesimi di Combattimento e Personali")
    print("✓ Gestione icone post-gioco: Assegnazione/Scarto/Eliminazione")
    print("✓ Incantesimi potenziabili con Punti Destino extra")
    print("✓ Verifica immunità all'Arte")
    print("✓ Maestri devono essere nella Squadra per lanciare")
    print("✓ Timing corretto per incantesimi di combattimento")
    print("✓ Percorsi import corretti con 'source.cards'")
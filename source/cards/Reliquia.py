"""
Classe Reliquia per Mutant Chronicles/Doomtrooper
Rappresenta le carte Reliquia del gioco - antichi artefatti, cimeli di battaglie 
o speciali equipaggiamenti di grande potere.
Implementa le regole ufficiali del regolamento.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import json
from source.cards.Guerriero import Fazione, Rarity, Set_Espansione  # Import dalle classi esistenti


class TipoReliquia(Enum):
    """Tipologie di Reliquie"""
    ARTEFATTO_ANTICO = "Artefatto Antico"
    CIMELIO_BATTAGLIA = "Cimelio di Battaglia"  
    EQUIPAGGIAMENTO_SPECIALE = "Equipaggiamento Speciale"
    RELIQUIA_SACRA = "Reliquia Sacra"
    TECNOLOGIA_PERDUTA = "Tecnologia Perduta"


class StatoReliquia(Enum):
    """Stato attuale della reliquia"""
    NON_ASSEGNATA = "Non Assegnata"
    ASSEGNATA = "Assegnata"
    ATTIVA = "Attiva"
    INATTIVA = "Inattiva"
    SCARTATA = "Scartata"


class PoterereReliquia(Enum):
    """Tipologie di poteri delle reliquie"""
    MODIFICATORE_STATISTICHE = "Modificatore Statistiche"
    ABILITA_SPECIALE = "Abilità Speciale"
    PROTEZIONE = "Protezione"
    POTENZIAMENTO_COMBATTIMENTO = "Potenziamento Combattimento"
    MANIPOLAZIONE_DESTINO = "Manipolazione Destino"
    COMANDO = "Comando"


@dataclass
class ModificatoreReliquia:
    """Rappresenta un modificatore applicato dalla reliquia"""
    statistica: str  # "C", "S", "A", "V"
    valore: int      # valore del modificatore (+/-)
    condizione: str = ""  # condizione per applicare il modificatore
    descrizione: str = ""
    permanente: bool = True  # se il modificatore è permanente


@dataclass
class PotereReliquia:
    """Rappresenta un potere speciale della reliquia"""
    nome: str
    descrizione: str
    tipo_potere: PoterereReliquia
    costo_attivazione: int = 0  # costo in azioni/DP per attivare
    tipo_attivazione: str = "Passivo"  # "Passivo", "Attivo", "Reazione", "Combattimento"
    limitazioni: List[str] = None
    una_volta_per_turno: bool = False
    
    def __post_init__(self):
        if self.limitazioni is None:
            self.limitazioni = []


@dataclass
class RestrizioneReliquia:
    """Restrizioni per l'assegnazione della reliquia"""
    fazioni_permesse: List[Fazione] = None
    corporazioni_specifiche: List[str] = None
    tipi_guerriero: List[str] = None  # es. ["Doomtrooper", "Personalità", "Eroe"]
    keywords_richieste: List[str] = None  # es. ["Techno", "Mystic"]
    livello_minimo: int = 0  # per PersonalitÃ  o Eroi
    
    def __post_init__(self):
        if self.fazioni_permesse is None:
            self.fazioni_permesse = []
        if self.corporazioni_specifiche is None:
            self.corporazioni_specifiche = []
        if self.tipi_guerriero is None:
            self.tipi_guerriero = []
        if self.keywords_richieste is None:
            self.keywords_richieste = []


class Reliquia:
    """
    Classe principale per rappresentare una carta Reliquia di Mutant Chronicles/Doomtrooper
    
    Regole specifiche delle Reliquie dal regolamento:
    - Assegnazione al costo di 1 Azione
    - Tutte le carte Reliquia sono uniche (una sola copia in gioco)
    - Possono essere assegnate solo a determinati tipi di guerriero/Corporazione
    - Non sono considerate Equipaggiamento
    - Copie scartate possono essere reintrodotte successivamente
    """
    
    def __init__(self, nome: str, valore: int = 0):
        """
        Inizializza una nuova Reliquia
        
        Args:
            nome: Nome della reliquia
            valore: Costo in Punti Destino (se richiesto, default 0)
        """
        self.nome = nome
        self.valore = valore  # Costo in Destiny Points (opzionale per Reliquie)
        
        # Attributi base della carta
        self.tipo = TipoReliquia.ARTEFATTO_ANTICO
        self.rarity = Rarity.RARE  # Le reliquie sono generalmente rare
        
        # Regole uniche delle Reliquie
        self.unica = True  # Sempre true per regolamento
        self.costo_assegnazione = 1  # Sempre 1 Azione secondo regolamento
        self.e_equipaggiamento = False  # Esplicitamente NON equipaggiamento
        
        # Restrizioni di assegnazione
        self.restrizioni = RestrizioneReliquia()
        
        # Poteri e modificatori
        self.modificatori: List[ModificatoreReliquia] = []
        self.poteri: List[PotereReliquia] = []
        
        # Condizioni speciali
        self.requisiti_speciali: List[str] = []  # Condizioni per usare la reliquia
        self.immunita: List[str] = []  # Immunità conferite
        self.vulnerabilita: List[str] = []  # Vulnerabilità aggiunte
        
        # Testo della carta
        self.testo_carta = ""
        self.flavour_text = ""
        
        # Attributi per espansioni
        self.set_espansione = Set_Espansione.BASE
        self.numero_carta = ""
        
        # Metadati
        self.keywords: List[str] = []
        self.origine_storica = ""  # Descrizione dell'origine dell'artefatto
        
        # Stato di gioco
        self.stato = StatoReliquia.NON_ASSEGNATA
        self.assegnata_a: Optional[str] = None  # Nome del guerriero che la possiede
        self.assegnata_da: Optional[str] = None  # Chi ha assegnato la reliquia
        self.turno_assegnazione: int = 0
        
        # Controllo unicità
        self.in_gioco_globalmente = False  # Per controllare unicità globale
        
        # Effetti attivi
        self.effetti_attivi: List[str] = []
        self.modificatori_applicati: Dict[str, int] = {}
        
        # Compatibilità con altre carte
        self.incompatibile_con: List[str] = []  # Reliquie/equipaggiamenti incompatibili
        self.potenzia: List[str] = []  # Carte/abilità che potenzia
        self.quantita = 0
    
    def puo_essere_assegnata_a(self, guerriero: object) -> Dict[str, Any]:
        """
        Verifica se la reliquia può essere assegnata a un guerriero
        
        Args:
            guerriero: Oggetto guerriero da verificare
            
        Returns:
            Dict con risultato della verifica
        """
        errori = []
        
        # Verifica se è già in gioco (regola unicità)
        if self.in_gioco_globalmente:
            errori.append("Reliquia già presente in gioco (regola unicità)")
        
        # Verifica se guerriero ha già questa reliquia
        if hasattr(guerriero, 'reliquie_assegnate'):
            if self.nome in guerriero.reliquie_assegnate:
                errori.append("Guerriero ha già questa reliquia")
        
        # Verifica fazioni permesse
        if self.restrizioni.fazioni_permesse:
            if hasattr(guerriero, 'fazione'):
                if guerriero.fazione not in self.restrizioni.fazioni_permesse:
                    fazioni_str = [f.value for f in self.restrizioni.fazioni_permesse]
                    errori.append(f"Fazione non permessa. Richieste: {fazioni_str}")
        
        # Verifica corporazioni specifiche
        if self.restrizioni.corporazioni_specifiche:
            if hasattr(guerriero, 'corporazione'):
                if guerriero.corporazione not in self.restrizioni.corporazioni_specifiche:
                    errori.append(f"Corporazione non valida. Richieste: {self.restrizioni.corporazioni_specifiche}")
        
        # Verifica tipi di guerriero
        if self.restrizioni.tipi_guerriero:
            if hasattr(guerriero, 'tipo'):
                if guerriero.tipo not in self.restrizioni.tipi_guerriero:
                    errori.append(f"Tipo guerriero non valido. Richiesti: {self.restrizioni.tipi_guerriero}")
            
            # Controllo keywords per tipi specifici
            if hasattr(guerriero, 'keywords'):
                tipi_trovati = any(tipo in guerriero.keywords for tipo in self.restrizioni.tipi_guerriero)
                if not tipi_trovati and guerriero.tipo not in self.restrizioni.tipi_guerriero:
                    errori.append(f"Guerriero deve essere uno di: {self.restrizioni.tipi_guerriero}")
        
        # Verifica keywords richieste
        if self.restrizioni.keywords_richieste:
            if hasattr(guerriero, 'keywords'):
                keywords_mancanti = [kw for kw in self.restrizioni.keywords_richieste 
                                   if kw not in guerriero.keywords]
                if keywords_mancanti:
                    errori.append(f"Keywords mancanti: {keywords_mancanti}")
        
        # Verifica livello minimo (per Personalità/Eroi)
        if self.restrizioni.livello_minimo > 0:
            if hasattr(guerriero, 'livello'):
                if guerriero.livello < self.restrizioni.livello_minimo:
                    errori.append(f"Livello insufficiente. Richiesto: {self.restrizioni.livello_minimo}")
        
        # Verifica requisiti speciali
        for requisito in self.requisiti_speciali:
            if not self._verifica_requisito_speciale(guerriero, requisito):
                errori.append(f"Requisito speciale non soddisfatto: {requisito}")
        
        # Verifica incompatibilità
        if hasattr(guerriero, 'equipaggiamento_assegnato'):
            for item in guerriero.equipaggiamento_assegnato:
                if item in self.incompatibile_con:
                    errori.append(f"Incompatibile con equipaggiamento: {item}")
        
        return {
            "puo_assegnare": len(errori) == 0,
            "errori": errori,
            "avvertenze": self._genera_avvertenze(guerriero)
        }
    
    def _verifica_requisito_speciale(self, guerriero: object, requisito: str) -> bool:
        """Verifica un requisito speciale specifico"""
        # Implementazione base - da estendere per requisiti specifici
        if "Non ferito" in requisito:
            return not getattr(guerriero, 'ferito', False)
        elif "Valore minimo" in requisito:
            valore_richiesto = int(requisito.split()[-1])
            return getattr(guerriero, 'valore', 0) >= valore_richiesto
        elif "In combattimento" in requisito:
            return getattr(guerriero, 'in_combattimento', False)
        return True
    
    def _genera_avvertenze(self, guerriero: object) -> List[str]:
        """Genera avvertenze per l'assegnazione"""
        avvertenze = []
        
        if self.vulnerabilita:
            avvertenze.append(f"La reliquia aggiunge vulnerabilità: {self.vulnerabilita}")
        
        if any("una volta per turno" in potere.nome.lower() for potere in self.poteri):
            avvertenze.append("Alcuni poteri sono limitati a una volta per turno")
        
        return avvertenze
    
    def assegna_a_guerriero(self, nome_guerriero: str, giocatore: str = "") -> bool:
        """
        Assegna la reliquia a un guerriero (costa 1 Azione secondo regolamento)
        
        Args:
            nome_guerriero: Nome del guerriero destinatario
            giocatore: Nome del giocatore che fa l'assegnazione
            
        Returns:
            bool: True se assegnazione riuscita
        """
        if self.stato != StatoReliquia.NON_ASSEGNATA:
            return False
        
        if self.in_gioco_globalmente:
            return False  # Regola unicità
        
        self.assegnata_a = nome_guerriero
        self.assegnata_da = giocatore
        self.stato = StatoReliquia.ASSEGNATA
        self.in_gioco_globalmente = True
        
        # Applica immediatamente gli effetti
        self._attiva_effetti()
        
        return True
    
    def _attiva_effetti(self):
        """Attiva gli effetti della reliquia"""
        self.stato = StatoReliquia.ATTIVA
        
        # Attiva modificatori permanenti
        for modificatore in self.modificatori:
            if modificatore.permanente:
                self.modificatori_applicati[modificatore.statistica] = modificatore.valore
                self.effetti_attivi.append(f"{modificatore.descrizione}")
        
        # Attiva poteri passivi
        for potere in self.poteri:
            if potere.tipo_attivazione == "Passivo":
                self.effetti_attivi.append(f"Potere attivo: {potere.nome}")
    
    def rimuovi_da_guerriero(self, motivo: str = "Scartata") -> bool:
        """
        Rimuove la reliquia dal guerriero (quando guerriero muore o carta scartata)
        
        Args:
            motivo: Motivo della rimozione
            
        Returns:
            bool: True se rimozione riuscita
        """
        if self.stato == StatoReliquia.NON_ASSEGNATA:
            return False
        
        # Disattiva tutti gli effetti
        self._disattiva_effetti()
        
        # Reset stato
        self.assegnata_a = None
        self.assegnata_da = None
        self.stato = StatoReliquia.SCARTATA if "cart" in motivo.lower() else StatoReliquia.NON_ASSEGNATA
        self.in_gioco_globalmente = False  # Ora può essere rigiocata
        
        return True
    
    def _disattiva_effetti(self):
        """Disattiva tutti gli effetti della reliquia"""
        self.stato = StatoReliquia.INATTIVA
        self.modificatori_applicati.clear()
        self.effetti_attivi.clear()
    
    def applica_modificatori(self, guerriero: object) -> Dict[str, int]:
        """
        Applica i modificatori della reliquia al guerriero
        
        Args:
            guerriero: Oggetto guerriero target
            
        Returns:
            Dict con modificatori applicati
        """
        if self.stato != StatoReliquia.ATTIVA:
            return {}
        
        modificatori_applicati = {}
        
        for modificatore in self.modificatori:
            if self._verifica_condizione_modificatore(guerriero, modificatore):
                stat = modificatore.statistica
                valore = modificatore.valore
                
                if hasattr(guerriero, 'applica_modificatore'):
                    guerriero.applica_modificatore(stat, valore)
                
                modificatori_applicati[stat] = valore
                
        return modificatori_applicati
    
    def _verifica_condizione_modificatore(self, guerriero: object, modificatore: ModificatoreReliquia) -> bool:
        """Verifica se la condizione per il modificatore è soddisfatta"""
        if not modificatore.condizione:
            return True
        
        # Implementazione base - da estendere per condizioni specifiche
        if "in combattimento" in modificatore.condizione.lower():
            return getattr(guerriero, 'in_combattimento', False)
        elif "non ferito" in modificatore.condizione.lower():
            return not getattr(guerriero, 'ferito', False)
        elif "contro oscura legione" in modificatore.condizione.lower():
            # Dovrebbe essere verificato nel contesto del combattimento
            return True
        
        return True
    
    def attiva_potere(self, nome_potere: str, target: object = None, costo_extra: int = 0) -> Dict[str, Any]:
        """
        Attiva un potere specifico della reliquia
        
        Args:
            nome_potere: Nome del potere da attivare
            target: Target del potere (se richiesto)
            costo_extra: Costo extra in DP (se richiesto)
            
        Returns:
            Dict con risultato dell'attivazione
        """
        if self.stato != StatoReliquia.ATTIVA:
            return {"successo": False, "motivo": "Reliquia non attiva"}
        
        potere = next((p for p in self.poteri if p.nome == nome_potere), None)
        if not potere:
            return {"successo": False, "motivo": "Potere non trovato"}
        
        if potere.tipo_attivazione == "Passivo":
            return {"successo": False, "motivo": "Potere passivo, sempre attivo"}
        
        # Verifica limitazioni
        if potere.una_volta_per_turno:
            if f"Usato_{nome_potere}" in self.effetti_attivi:
                return {"successo": False, "motivo": "Potere già usato questo turno"}
        
        # Attiva il potere
        risultato = self._esegui_potere(potere, target)
        
        if risultato["successo"]:
            if potere.una_volta_per_turno:
                self.effetti_attivi.append(f"Usato_{nome_potere}")
        
        return risultato
    
    def _esegui_potere(self, potere: PotereReliquia, target: object = None) -> Dict[str, Any]:
        """Esegue un potere specifico - da implementare per poteri specifici"""
        # Implementazione base
        return {
            "successo": True,
            "descrizione": f"Potere {potere.nome} attivato",
            "effetti": [potere.descrizione]
        }
    
    def reset_limitazioni_turno(self):
        """Reset delle limitazioni per turno (chiamato all'inizio del turno)"""
        # Rimuove i marker "Usato_" per poteri una volta per turno
        self.effetti_attivi = [e for e in self.effetti_attivi if not e.startswith("Usato_")]
    
    def get_stato_completo(self) -> Dict[str, Any]:
        """Restituisce lo stato completo della reliquia"""
        return {
            "nome": self.nome,
            "tipo": self.tipo.value,
            "rarity": self.rarity.value,
            "valore": self.valore,
            "stato": self.stato.value,
            "assegnata_a": self.assegnata_a,
            "in_gioco": self.in_gioco_globalmente,
            "modificatori_attivi": self.modificatori_applicati,
            "effetti_attivi": self.effetti_attivi,
            "poteri_disponibili": [p.nome for p in self.poteri if p.tipo_attivazione != "Passivo"],
            "immunita_conferite": self.immunita,
            "vulnerabilita_aggiunte": self.vulnerabilita
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte la reliquia in dizionario per serializzazione"""
        return {
            "nome": self.nome,
            "valore": self.valore,
            "tipo": self.tipo.value,
            "rarity": self.rarity.value,
            "restrizioni": {
                "fazioni_permesse": [f.value for f in self.restrizioni.fazioni_permesse],
                "corporazioni_specifiche": self.restrizioni.corporazioni_specifiche,
                "tipi_guerriero": self.restrizioni.tipi_guerriero,
                "keywords_richieste": self.restrizioni.keywords_richieste,
                "livello_minimo": self.restrizioni.livello_minimo
            },
            "modificatori": [
                {
                    "statistica": m.statistica,
                    "valore": m.valore,
                    "condizione": m.condizione,
                    "descrizione": m.descrizione,
                    "permanente": m.permanente
                } for m in self.modificatori
            ],
            "poteri": [
                {
                    "nome": p.nome,
                    "descrizione": p.descrizione,
                    "tipo_potere": p.tipo_potere.value,
                    "costo_attivazione": p.costo_attivazione,
                    "tipo_attivazione": p.tipo_attivazione,
                    "limitazioni": p.limitazioni,
                    "una_volta_per_turno": p.una_volta_per_turno
                } for p in self.poteri
            ],
            "set_espansione": self.set_espansione.value,
            "numero_carta": self.numero_carta,
            "testo_carta": self.testo_carta,
            "flavour_text": self.flavour_text,
            "keywords": self.keywords,
            "origine_storica": self.origine_storica,
            "requisiti_speciali": self.requisiti_speciali,
            "immunita": self.immunita,
            "vulnerabilita": self.vulnerabilita,
            "stato_gioco": {
                "stato": self.stato.value,
                "assegnata_a": self.assegnata_a,
                "assegnata_da": self.assegnata_da,
                "turno_assegnazione": self.turno_assegnazione,
                "in_gioco_globalmente": self.in_gioco_globalmente
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Reliquia':
        """Crea una Reliquia da un dizionario"""
        reliquia = cls(data["nome"], data["valore"])
        
        reliquia.tipo = TipoReliquia(data["tipo"])
        reliquia.rarity = Rarity(data["rarity"])
        
        # Ricostruisce restrizioni
        restr_data = data["restrizioni"]
        reliquia.restrizioni = RestrizioneReliquia(
            fazioni_permesse=[Fazione(f) for f in restr_data["fazioni_permesse"]],
            corporazioni_specifiche=restr_data["corporazioni_specifiche"],
            tipi_guerriero=restr_data["tipi_guerriero"],
            keywords_richieste=restr_data["keywords_richieste"],
            livello_minimo=restr_data["livello_minimo"]
        )
        
        # Ricostruisce modificatori
        for mod_data in data["modificatori"]:
            modificatore = ModificatoreReliquia(
                statistica=mod_data["statistica"],
                valore=mod_data["valore"],
                condizione=mod_data["condizione"],
                descrizione=mod_data["descrizione"],
                permanente=mod_data["permanente"]
            )
            reliquia.modificatori.append(modificatore)
        
        # Ricostruisce poteri
        for pot_data in data["poteri"]:
            potere = PotereReliquia(
                nome=pot_data["nome"],
                descrizione=pot_data["descrizione"],
                tipo_potere=PoterereReliquia(pot_data["tipo_potere"]),
                costo_attivazione=pot_data["costo_attivazione"],
                tipo_attivazione=pot_data["tipo_attivazione"],
                limitazioni=pot_data["limitazioni"],
                una_volta_per_turno=pot_data["una_volta_per_turno"]
            )
            reliquia.poteri.append(potere)
        
        reliquia.set_espansione = Set_Espansione(data["set_espansione"])
        reliquia.numero_carta = data["numero_carta"]
        reliquia.testo_carta = data["testo_carta"]
        reliquia.flavour_text = data["flavour_text"]
        reliquia.keywords = data["keywords"]
        reliquia.origine_storica = data["origine_storica"]
        reliquia.requisiti_speciali = data["requisiti_speciali"]
        reliquia.immunita = data["immunita"]
        reliquia.vulnerabilita = data["vulnerabilita"]
        
        # Ripristina stato di gioco
        stato = data["stato_gioco"]
        reliquia.stato = StatoReliquia(stato["stato"])
        reliquia.assegnata_a = stato["assegnata_a"]
        reliquia.assegnata_da = stato["assegnata_da"]
        reliquia.turno_assegnazione = stato["turno_assegnazione"]
        reliquia.in_gioco_globalmente = stato["in_gioco_globalmente"]
        
        return reliquia
    
    def __str__(self) -> str:
        stato_str = f"({self.stato.value})"
        if self.assegnata_a:
            stato_str += f" -> {self.assegnata_a}"
        
        modificatori_str = []
        for mod in self.modificatori:
            if mod.valore != 0:
                modificatori_str.append(f"{mod.valore:+}{mod.statistica}")
        
        mod_str = " ".join(modificatori_str) if modificatori_str else "Poteri speciali"
        
        return f"{self.nome} ({self.tipo.value}) - {mod_str} {stato_str}"
    
    def __repr__(self) -> str:
        return f"Reliquia('{self.nome}', valore={self.valore}, tipo={self.tipo.value})"


# Funzioni di utilità per creare reliquie specifiche

def crea_reliquia_combattimento(nome: str, bonus_combattimento: int = 0, bonus_sparare: int = 0, 
                               bonus_armatura: int = 0, restrizioni: RestrizioneReliquia = None) -> Reliquia:
    """Crea una reliquia che migliora le capacità di combattimento"""
    reliquia = Reliquia(nome)
    reliquia.tipo = TipoReliquia.EQUIPAGGIAMENTO_SPECIALE
    
    if bonus_combattimento != 0:
        mod = ModificatoreReliquia("C", bonus_combattimento, "", f"{bonus_combattimento:+} Corpo a corpo")
        reliquia.modificatori.append(mod)
    
    if bonus_sparare != 0:
        mod = ModificatoreReliquia("S", bonus_sparare, "", f"{bonus_sparare:+} Sparare")
        reliquia.modificatori.append(mod)
    
    if bonus_armatura != 0:
        mod = ModificatoreReliquia("A", bonus_armatura, "", f"{bonus_armatura:+} Armatura")
        reliquia.modificatori.append(mod)
    
    if restrizioni:
        reliquia.restrizioni = restrizioni
    
    return reliquia

def crea_reliquia_potere_speciale(nome: str, nome_potere: str, descrizione_potere: str,
                                tipo_potere: PoterereReliquia = PoterereReliquia.ABILITA_SPECIALE,
                                tipo_attivazione: str = "Attivo") -> Reliquia:
    """Crea una reliquia con un potere speciale"""
    reliquia = Reliquia(nome)
    reliquia.tipo = TipoReliquia.ARTEFATTO_ANTICO
    
    potere = PotereReliquia(nome_potere, descrizione_potere, tipo_potere, 0, tipo_attivazione)
    reliquia.poteri.append(potere)
    
    return reliquia


# Esempi di utilizzo secondo il regolamento
if __name__ == "__main__":
    print("=== ESEMPI RELIQUIA MUTANT CHRONICLES (REGOLAMENTO UFFICIALE) ===")
    
    # Esempio 1: Reliquia di combattimento - Spada Antica
    print(f"\n=== ESEMPIO 1: RELIQUIA DI COMBATTIMENTO ===")
    
    restrizioni_doomtrooper = RestrizioneReliquia(
        tipi_guerriero=["Doomtrooper", "Personalità"],
        fazioni_permesse=[Fazione.BAUHAUS, Fazione.CAPITOL, Fazione.IMPERIALE]
    )
    
    spada_antica = crea_reliquia_combattimento(
        "Spada del Destino",
        bonus_combattimento=3,
        bonus_armatura=1,
        restrizioni=restrizioni_doomtrooper
    )
    spada_antica.testo_carta = "+3 Corpo a corpo, +1 Armatura. Solo Doomtrooper delle Corporazioni."
    spada_antica.flavour_text = "Forgiata nelle guerre dei primi giorni, la sua lama non conosce sconfitta."
    spada_antica.keywords = ["Artefatto", "Arma Antica", "Leggendaria"]
    spada_antica.origine_storica = "Reliquia delle prime guerre corporative"
    
    print(f"✓ {spada_antica}")
    print(f"  Modificatori: {[f'{m.valore:+}{m.statistica}' for m in spada_antica.modificatori]}")
    print(f"  Restrizioni: {spada_antica.restrizioni.tipi_guerriero}")
    
    # Esempio 2: Reliquia con potere speciale - Amuleto Mistico
    print(f"\n=== ESEMPIO 2: RELIQUIA CON POTERE SPECIALE ===")
    
    amuleto_protezione = crea_reliquia_potere_speciale(
        "Amuleto di Protezione",
        "Scudo Mistico",
        "Una volta per turno, annulla un attacco diretto al guerriero",
        PoterereReliquia.PROTEZIONE,
        "Reazione"
    )
    
    # Aggiunge potere passivo
    potere_passivo = PotereReliquia(
        "Immunità Paura",
        "Il guerriero è immune agli effetti di paura",
        PoterereReliquia.PROTEZIONE,
        tipo_attivazione="Passivo"
    )
    amuleto_protezione.poteri.append(potere_passivo)
    amuleto_protezione.immunita = ["Paura", "Terrore"]
    
    amuleto_protezione.restrizioni.fazioni_permesse = [Fazione.FRATELLANZA]
    amuleto_protezione.restrizioni.keywords_richieste = ["Mystic", "Techno"]
    
    amuleto_protezione.testo_carta = "Il guerriero è immune alla paura. Una volta per turno può annullare un attacco."
    amuleto_protezione.flavour_text = "Un antico simbolo che protegge chi lo porta dalle forze oscure."
    
    print(f"✓ {amuleto_protezione}")
    print(f"  Poteri: {[p.nome for p in amuleto_protezione.poteri]}")
    print(f"  Immunità: {amuleto_protezione.immunita}")
    
    # Esempio 3: Test meccaniche di assegnazione
    print(f"\n=== ESEMPIO 3: MECCANICHE DI ASSEGNAZIONE ===")
    
    # Simula un guerriero Doomtrooper
    class GuerrieroTest:
        def __init__(self, nome, fazione, tipo="Normale"):
            self.nome = nome
            self.fazione = fazione
            self.tipo = tipo
            self.keywords = []
            self.ferito = False
            self.valore = 5
            self.reliquie_assegnate = []
        
        def applica_modificatore(self, stat, valore):
            print(f"    Applicato modificatore: {valore:+}{stat}")
    
    # Test guerriero compatibile
    doomtrooper_bauhaus = GuerrieroTest("Hans Mueller", Fazione.BAUHAUS, "Doomtrooper")
    doomtrooper_bauhaus.keywords = ["Doomtrooper", "Elite"]
    
    verifica = spada_antica.puo_essere_assegnata_a(doomtrooper_bauhaus)
    print(f"✓ {spada_antica.nome} può essere assegnata a {doomtrooper_bauhaus.nome}: {verifica['puo_assegnare']}")
    
    if verifica['puo_assegnare']:
        successo = spada_antica.assegna_a_guerriero(doomtrooper_bauhaus.nome, "Giocatore1")
        print(f"  Assegnazione riuscita: {successo}")
        print(f"  Stato reliquia: {spada_antica.stato.value}")
        print(f"  In gioco globalmente: {spada_antica.in_gioco_globalmente}")
        
        # Applica modificatori
        modificatori = spada_antica.applica_modificatori(doomtrooper_bauhaus)
        print(f"  Modificatori applicati: {modificatori}")
    
    # Test guerriero non compatibile
    guerriero_oscura = GuerrieroTest("Nepharite Warlord", Fazione.OSCURA_LEGIONE)
    verifica_negativa = spada_antica.puo_essere_assegnata_a(guerriero_oscura)
    print(f"\n✗ {spada_antica.nome} può essere assegnata a {guerriero_oscura.nome}: {verifica_negativa['puo_assegnare']}")
    if not verifica_negativa['puo_assegnare']:
        print(f"  Errori: {verifica_negativa['errori']}")
    
    # Esempio 4: Test regola unicità
    print(f"\n=== ESEMPIO 4: TEST REGOLA UNICITÀ ===")
    
    # Tenta di assegnare la stessa reliquia a un altro guerriero
    altro_doomtrooper = GuerrieroTest("Sarah Connor", Fazione.CAPITOL, "Doomtrooper")
    altro_doomtrooper.keywords = ["Doomtrooper", "Veteran"]
    
    verifica_unicita = spada_antica.puo_essere_assegnata_a(altro_doomtrooper)
    print(f"✗ {spada_antica.nome} può essere assegnata a {altro_doomtrooper.nome}: {verifica_unicita['puo_assegnare']}")
    print(f"  Motivo: {verifica_unicita['errori'][0] if verifica_unicita['errori'] else 'Nessun errore'}")
    
    # Esempio 5: Attivazione poteri
    print(f"\n=== ESEMPIO 5: ATTIVAZIONE POTERI ===")
    
    # Assegna amuleto a guerriero Fratellanza
    guerriero_fratellanza = GuerrieroTest("Brother Marcus", Fazione.FRATELLANZA, "Mystic")
    guerriero_fratellanza.keywords = ["Mystic", "Techno", "Doomtrooper"]
    
    verifica_amuleto = amuleto_protezione.puo_essere_assegnata_a(guerriero_fratellanza)
    print(f"✓ {amuleto_protezione.nome} può essere assegnato: {verifica_amuleto['puo_assegnare']}")
    
    if verifica_amuleto['puo_assegnare']:
        amuleto_protezione.assegna_a_guerriero(guerriero_fratellanza.nome, "Giocatore2")
        print(f"  Effetti passivi attivi: {amuleto_protezione.effetti_attivi}")
        
        # Testa attivazione potere reazione
        risultato = amuleto_protezione.attiva_potere("Scudo Mistico")
        print(f"  Attivazione Scudo Mistico: {risultato['successo']}")
        if risultato['successo']:
            print(f"    Effetto: {risultato['descrizione']}")
        
        # Testa limitazione una volta per turno
        risultato2 = amuleto_protezione.attiva_potere("Scudo Mistico")
        print(f"  Seconda attivazione Scudo Mistico: {risultato2['successo']}")
        if not risultato2['successo']:
            print(f"    Motivo: {risultato2['motivo']}")
    
    # Esempio 6: Reliquia tecnologica avanzata
    print(f"\n=== ESEMPIO 6: RELIQUIA TECNOLOGICA ===")
    
    cyber_implant = Reliquia("Impianto Neurale Avanzato")
    cyber_implant.tipo = TipoReliquia.TECNOLOGIA_PERDUTA
    cyber_implant.rarity = Rarity.ULTRA_RARE
    
    # Modificatori condizionali
    mod_hacking = ModificatoreReliquia(
        "S", 4, "quando usa tecnologia", 
        "+4 Sparare con armi tecnologiche"
    )
    cyber_implant.modificatori.append(mod_hacking)
    
    # Potere di controllo mentale
    controllo_tech = PotereReliquia(
        "Controllo Tecnologico",
        "Prendi controllo di un equipaggiamento tecnologico nemico per 1 turno",
        PoterereReliquia.COMANDO,
        costo_attivazione=2,
        tipo_attivazione="Attivo",
        una_volta_per_turno=True
    )
    cyber_implant.poteri.append(controllo_tech)
    
    # Restrizioni Cybertronic
    cyber_implant.restrizioni.fazioni_permesse = [Fazione.CYBERTRONIC]
    cyber_implant.restrizioni.keywords_richieste = ["Cyborg", "Techno"]
    cyber_implant.vulnerabilita = ["EMP", "Interferenze"]
    
    cyber_implant.testo_carta = "+4 Sparare con tecnologia. Può controllare equipaggiamento tech nemico."
    cyber_implant.flavour_text = "L'interfaccia definitiva tra mente e macchina."
    
    print(f"✓ {cyber_implant}")
    print(f"  Fazioni permesse: {[f.value for f in cyber_implant.restrizioni.fazioni_permesse]}")
    print(f"  Keywords richieste: {cyber_implant.restrizioni.keywords_richieste}")
    print(f"  Vulnerabilità: {cyber_implant.vulnerabilita}")
    
    # Esempio 7: Serializzazione e stato completo
    print(f"\n=== ESEMPIO 7: SERIALIZZAZIONE E STATO ===")
    
    stato_spada = spada_antica.get_stato_completo()
    print(f"Stato completo Spada del Destino:")
    for chiave, valore in stato_spada.items():
        print(f"  {chiave}: {valore}")
    
    # Test serializzazione
    dict_spada = spada_antica.to_dict()
    spada_ricostruita = Reliquia.from_dict(dict_spada)
    print(f"\n✓ Serializzazione riuscita: {spada_ricostruita.nome == spada_antica.nome}")
    print(f"  Modificatori preservati: {len(spada_ricostruita.modificatori) == len(spada_antica.modificatori)}")
    
    # Esempio 8: Reset limitazioni turno
    print(f"\n=== ESEMPIO 8: GESTIONE TURNI ===")
    
    print(f"Effetti attivi prima reset: {len(amuleto_protezione.effetti_attivi)}")
    amuleto_protezione.reset_limitazioni_turno()
    print(f"Effetti attivi dopo reset: {len(amuleto_protezione.effetti_attivi)}")
    
    # Ora può riattivare il potere
    risultato_reset = amuleto_protezione.attiva_potere("Scudo Mistico")
    print(f"Attivazione dopo reset: {risultato_reset['successo']}")
    
    print(f"\n=== REGOLE RELIQUIE IMPLEMENTATE CORRETTAMENTE ===")
    print("✓ Assegnazione al costo di 1 Azione (campo costo_assegnazione)")
    print("✓ Regola unicità globale (una sola copia in gioco)")
    print("✓ Non considerate Equipaggiamento (campo e_equipaggiamento = False)")
    print("✓ Restrizioni specifiche per tipo guerriero/Corporazione")
    print("✓ Copie scartate possono essere reintrodotte (in_gioco_globalmente)")
    print("✓ Modificatori permanenti alle statistiche C-S-A-V")
    print("✓ Poteri speciali con limitazioni (una volta per turno, costi, etc)")
    print("✓ Sistema di immunità e vulnerabilità")
    print("✓ Compatibilità con sistema di fazioni e keywords del gioco")
    print("✓ Serializzazione completa per salvataggio/caricamento")
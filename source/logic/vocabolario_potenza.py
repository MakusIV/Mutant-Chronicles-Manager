"""
vocabolario_potenza.py

Vocabolario condiviso dei bonus di potenza applicati da CreatoreMazzo.calcola_potenza_*
in base al tipo e al nome di un'abilità/potere/effetto di una carta.

5 metodi (calcola_potenza_{guerriero,equipaggiamento,fortificazione,reliquia,warzone} in
source/logic/Creatore_Mazzo.py) applicavano lo stesso schema — "se il tipo è X e il nome
è tra questi, moltiplica la potenza per N" — con liste di nomi copiate a mano e già
divergenti tra loro (es. "porta rinforzi" riconosciuto solo da Reliquia, "immune allo
specifico warzone" al posto di "...equipaggiamento" solo in Warzone). Questo modulo
sposta lo schema in un'unica funzione; le tabelle sotto riproducono esattamente le liste
di ciascun metodo così com'erano, comprese le divergenze — non è stata presa alcuna
decisione su quali siano intenzionali e quali no (vedi il piano di refactor:
riconciliarle richiede un giudizio di design del gioco, rimandato apposta).

calcola_potenza_{arte,oscura_simmetria,speciale} usano un vocabolario diverso e già
condiviso (_calcola_potenza_carta in Creatore_Mazzo.py) e non sono toccati da questo
modulo.
"""

from typing import Dict, List, Tuple

# (nomi che fanno scattare la regola, moltiplicatore, modalità di confronto).
# modalità "esatto": il nome dell'abilità deve comparire per intero in `nomi`
# (riproduce sia `nome == "x"` sia `nome in ["x", "y"]` dell'originale).
# modalità "sottostringa": basta che uno degli elementi di `nomi` compaia come
# sottostringa nel nome (riproduce gli `any(x in nome ...)` originali).
Regola = Tuple[Tuple[str, ...], float, str]
Vocabolario = Dict[str, List[Regola]]


def applica_bonus_abilita(potenza: float, tipo: str, nome: str, vocabolario: Vocabolario) -> float:
    """
    Applica al massimo un moltiplicatore: la prima regola del tipo corrente il cui
    nome corrisponde. Replica il comportamento originale — le regole all'interno di
    uno stesso tipo erano per lo più elif (solo una si applica), e dove non lo erano
    (es. "combattimento", "guarigione", "punti") gli insiemi di nomi non si
    sovrapponevano mai in nessuno dei 5 metodi, quindi valutarle come elif produce
    lo stesso risultato.
    """
    for nomi, moltiplicatore, modo in vocabolario.get(tipo, []):
        if modo == "esatto":
            colpisce = nome in nomi
        else:
            colpisce = any(frammento in nome for frammento in nomi)
        if colpisce:
            return potenza * moltiplicatore
    return potenza


VOCABOLARIO_GUERRIERO: Vocabolario = {
    "combattimento": [
        (("uccide automaticamente",), 1.5, "esatto"),
        (("permette ai guerrieri di attaccare per primi",
          "i guerrieri alleati uccidono automaticamente"), 1.3, "esatto"),
    ],
    "immunita": [
        (("immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria",
          "annulla immunita dell'oscura simmetria", "immune ai doni degli apostoli"), 1.4, "esatto"),
        (("immune agli effetti della specifica arte", "immune allo specifico equipaggiamento",
          "immune alla specifica fortificazione"), 1.2, "sottostringa"),
    ],
    "modificatore": [
        (("aumenta effetto", "aumenta caratteristica"), 1.3, "esatto"),
        (("trasforma guerrieri uccisi in alleati",), 1.1, "esatto"),
        (("sostituisce guerrieri",), 1.2, "esatto"),
    ],
    "guarigione": [
        (("guarisce se stesso",), 1.3, "sottostringa"),
    ],
    "arte": [
        (("lancia arte e/o incantesimo dell'arte",), 1.3, "esatto"),
        (("lancia arte e/o incantesimo dell'arte specifica",), 1.2, "esatto"),
    ],
    "carte": [
        (("assegna carta", "scarta carta", "elimina carta"), 1.3, "esatto"),
    ],
    "azioni": [
        (("converte azioni in azioni d'attacco",), 1.3, "esatto"),
    ],
}

VOCABOLARIO_EQUIPAGGIAMENTO: Vocabolario = {
    "combattimento": [
        (("uccide automaticamente",), 1.5, "esatto"),
        (("permette ai guerrieri di attaccare per primi",
          "i guerrieri alleati uccidono automaticamente"), 1.3, "esatto"),
    ],
    "immunita": [
        (("immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria",
          "annulla immunita dell'oscura simmetria", "immune ai doni degli apostoli"), 1.4, "esatto"),
        (("immune agli effetti della specifica arte", "immune allo specifico equipaggiamento",
          "immune alla specifica fortificazione", "immune alle ferite durante il combattimento"),
         1.2, "sottostringa"),
    ],
    "modificatore": [
        (("aumenta effetto", "aumenta caratteristica"), 1.3, "esatto"),
        (("trasforma guerrieri uccisi in alleati",), 1.1, "esatto"),
        (("sostituisce guerrieri",), 1.2, "esatto"),
    ],
    "guarigione": [
        (("guarisce se stesso", "guarisce guerriero"), 1.3, "esatto"),
        (("ripara equipaggiamento o fortificazione",), 1.1, "esatto"),
    ],
    "arte": [
        (("lancia arte e/o incantesimo dell'arte", "lancia arte"), 1.3, "esatto"),
        (("lancia arte e/o incantesimo dell'arte specifica",), 1.2, "esatto"),
    ],
    "carte": [
        (("assegna carta", "assegna carte", "scarta carta", "elimina carta"), 1.3, "esatto"),
    ],
    "azioni": [
        (("converte azioni in azioni d'attacco", "incrementa azioni", "attacca sempre per primo",
          "attacca sempre per primo se sceglie di sparare"), 1.3, "esatto"),
        (("modifica azione", "modifica stato"), 1.1, "esatto"),
    ],
}

VOCABOLARIO_FORTIFICAZIONE: Vocabolario = {
    "combattimento": [
        (("uccide automaticamente",), 1.5, "esatto"),
        (("permette ai guerrieri di attaccare per primi",
          "i guerrieri alleati uccidono automaticamente"), 1.3, "esatto"),
    ],
    "immunita": [
        (("immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria",
          "annulla immunita dell'oscura simmetria", "immune ai doni degli apostoli"), 1.4, "esatto"),
        (("immune agli effetti della specifica arte", "immune allo specifico equipaggiamento",
          "immune alla specifica fortificazione", "immune alle ferite durante il combattimento"),
         1.2, "sottostringa"),
    ],
    "modificatore": [
        (("aumenta effetto", "aumenta caratteristica"), 1.3, "esatto"),
        (("trasforma guerrieri uccisi in alleati", "imprigiona guerrieri"), 1.1, "esatto"),
        (("sostituisce guerrieri",), 1.2, "esatto"),
    ],
    "guarigione": [
        (("guarisce se stesso", "guarisce guerriero"), 1.3, "esatto"),
        (("ripara equipaggiamento o fortificazione",), 1.1, "esatto"),
    ],
    "arte": [
        (("lancia arte",), 1.3, "esatto"),
        (("lancia arte specifica",), 1.2, "esatto"),
    ],
    "carte": [
        (("assegna carta", "scarta carta", "elimina carta"), 1.3, "esatto"),
    ],
    "punti": [
        (("produce punti",), 1.3, "esatto"),
        (("protezione punti",), 1.5, "esatto"),
    ],
    "azioni": [
        (("converte azioni in azioni d'attacco", "incrementa azioni", "attacca sempre per primo",
          "attacco in uscita da copertura"), 1.3, "esatto"),
        (("modifica azione", "modifica stato"), 1.1, "esatto"),
    ],
}

VOCABOLARIO_RELIQUIA: Vocabolario = {
    "combattimento": [
        (("uccide automaticamente", "porta rinforzi"), 1.5, "esatto"),
        (("permette ai guerrieri di attaccare per primi",
          "i guerrieri alleati uccidono automaticamente"), 1.3, "esatto"),
    ],
    "immunita": [
        (("immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria",
          "annulla immunita dell'oscura simmetria", "immune ai doni degli apostoli"), 1.4, "esatto"),
        (("immune agli effetti della specifica arte", "immune allo specifico equipaggiamento",
          "immune alla specifica fortificazione", "immune alle ferite durante il combattimento"),
         1.2, "sottostringa"),
    ],
    "modificatore": [
        (("aumenta effetto", "aumenta caratteristica"), 1.3, "esatto"),
        (("trasforma guerrieri uccisi in alleati", "imprigiona guerrieri"), 1.1, "esatto"),
        (("sostituisce guerrieri",), 1.2, "esatto"),
    ],
    "guarigione": [
        (("guarisce se stesso", "guarisce guerriero"), 1.3, "esatto"),
        (("ripara equipaggiamento o fortificazione",), 1.1, "esatto"),
    ],
    "arte": [
        (("lancia arte", "annulla effetto arte"), 1.3, "esatto"),
        (("lancia arte specifica",), 1.2, "esatto"),
    ],
    "carte": [
        (("assegna carta", "scarta carta", "elimina carta"), 1.3, "esatto"),
    ],
    "punti": [
        (("produce punti",), 1.3, "esatto"),
        (("protezione punti",), 1.5, "esatto"),
    ],
    "azioni": [
        (("converte azioni in azioni d'attacco", "incrementa azioni", "attacca sempre per primo",
          "attacco in uscita da copertura"), 1.3, "esatto"),
        (("modifica azione", "modifica stato"), 1.1, "esatto"),
    ],
}

VOCABOLARIO_WARZONE: Vocabolario = {
    "combattimento": [
        (("uccide automaticamente",), 1.5, "esatto"),
        (("permette ai guerrieri di attaccare per primi",
          "i guerrieri alleati uccidono automaticamente"), 1.3, "esatto"),
    ],
    "punti": [
        (("produce punti", "guadagna punti"), 1.3, "esatto"),
        (("protezione punti",), 1.5, "esatto"),
    ],
    "immunita": [
        (("immune agli effetti dell'arte", "immune agli effetti dell'oscura simmetria",
          "annulla immunita dell'oscura simmetria", "immune ai doni degli apostoli"), 1.4, "esatto"),
        (("immune agli effetti della specifica arte", "immune allo specifico warzone",
          "immune alla specifica fortificazione", "immune alle ferite durante il combattimento"),
         1.2, "sottostringa"),
    ],
    "modificatore": [
        (("aumenta effetto", "aumenta caratteristica"), 1.3, "esatto"),
        (("trasforma guerrieri uccisi in alleati",), 1.1, "esatto"),
        (("sostituisce guerrieri",), 1.2, "esatto"),
    ],
    "guarigione": [
        (("guarisce se stesso", "guarisce guerriero"), 1.3, "esatto"),
        (("ripara equipaggiamento o fortificazione",), 1.1, "esatto"),
    ],
    "arte": [
        (("lancia arte e/o incantesimo dell'arte",), 1.3, "esatto"),
        (("lancia arte e/o incantesimo dell'arte specifica",), 1.2, "esatto"),
    ],
    "carte": [
        (("assegna carta", "scarta carta", "elimina carta"), 1.3, "esatto"),
    ],
    "azioni": [
        (("converte azioni in azioni d'attacco", "incrementa azioni", "attacca sempre per primo"),
         1.3, "esatto"),
        (("modifica azione", "modifica stato"), 1.1, "esatto"),
    ],
}

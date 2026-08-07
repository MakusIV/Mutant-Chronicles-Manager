"""
regole_associazione.py

Vocabolario condiviso delle stringhe di restrizione carta-guerriero.

Sei classi (Speciale, Equipaggiamento, Fortificazione, Missione, Reliquia, Warzone)
valutavano le stesse stringhe di restrizione ("Solo Doomtrooper", "Solo Mercenari",
...) con una propria catena if/elif copiata a mano, quasi identica ma non condivisa.
La prova che questo produce bug reali, non solo il rischio: la correzione dell'ordine
tra "Solo Mercenari o Eretici" e "Solo Mercenari" (di cui il primo è prefisso) per la
carta "Furga 750" è dovuta essere ri-applicata sapendo a memoria quali delle altre
classi avevano già l'ordine giusto.

Ogni classe resta responsabile del proprio campo (`restrizioni`,
`restrizioni_guerriero`, campi annidati sotto `self.restrizioni`) e della propria
chiave di ritorno (`puo_assegnare`/`puo_lanciare`) — questo modulo valuta solo il
contenuto delle stringhe di restrizione contro un guerriero, tutto il resto (controllo
fazioni_permesse, stato in gioco, blocchi di corporazione propri di una sola classe)
resta locale a ciascuna classe.

Arte.py e Oscura_Simmetria.py non usano questo modulo: la loro logica è
strutturalmente diversa (disciplina/abilità per Arte, controlli diretti per
membership per Oscura Simmetria), non una catena elif su stringhe di restrizione.
"""

from typing import Any, Dict, List

from source.cards.Guerriero import Fazione, TipoGuerriero, DOOMTROOPER, vale_come_doomtrooper


def valuta_restrizioni(restrizioni: List[str], guerriero: Any) -> Dict[str, Any]:
    """
    Valuta una lista di stringhe di restrizione contro un guerriero.

    Le restrizioni della lista sono in AND: tutte devono essere soddisfatte perché
    il guerriero sia idoneo. A differenza di alcune delle implementazioni originali,
    non si interrompe alla prima restrizione non soddisfatta: valuta l'intera lista
    e accumula in "errori" ogni motivo di rifiuto, non solo il primo — il risultato
    booleano non cambia, cambia solo quanto dettaglio viene riportato.

    Returns:
        {"puo_assegnare": bool, "errori": List[str]}
    """
    risultato: Dict[str, Any] = {"puo_assegnare": True, "errori": []}

    if not restrizioni:
        return risultato

    for restrizione in restrizioni:

        # Le condizioni composte vanno valutate prima delle rispettive forme
        # semplici, di cui sono un prefisso ("Solo Mercenari o Eretici" contiene
        # "Solo Mercenari"; "Solo Doomtrooper o Eretici" contiene "Solo Doomtrooper").
        if "Solo Doomtrooper o Eretici" in restrizione:
            e_doomtrooper = vale_come_doomtrooper(guerriero)
            e_eretico = bool(guerriero.keywords) and "Eretico" in guerriero.keywords
            if not (e_doomtrooper or e_eretico):
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Solo Doomtrooper o Eretici")

        elif "Solo Mercenari o Eretici" in restrizione:
            # Le due condizioni sono in alternativa: si nega solo a chi non
            # soddisfa né l'una né l'altra.
            e_mercenario = (guerriero.fazione == Fazione.MERCENARIO
                             or (bool(guerriero.keywords) and "Mercenario" in guerriero.keywords))
            e_eretico = bool(guerriero.keywords) and "Eretico" in guerriero.keywords
            if not (e_mercenario or e_eretico):
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Solo Mercenari o Eretici")

        elif "Solo Doomtrooper" in restrizione:
            # Un Cultista e' Oscura Legione ma vale come Doomtrooper: il suo
            # testo lo dichiara, e vale_come_doomtrooper lo riconosce.
            if not vale_come_doomtrooper(guerriero):
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
            if (not guerriero.keywords
                    or "Seguace di " + apostolo_richiesto not in guerriero.keywords):
                risultato["puo_assegnare"] = False
                risultato["errori"].append(f"Solo Seguaci di {apostolo_richiesto}")

        elif "Solo Eretici" in restrizione:
            if not guerriero.keywords or "Eretico" not in guerriero.keywords:
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Solo Eretici")

        elif "Solo Necromutanti" in restrizione:
            if not guerriero.keywords or "Necromutante" not in guerriero.keywords:
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Solo Necromutanti")

        elif "Solo Mercenari" in restrizione:
            # Il solo campo fazione non basta, e nemmeno la sola keyword: 5
            # guerrieri con fazione Mercenario non portano la keyword
            # "Mercenario" (es. Agente Nick Michaels), e 5 guerrieri "Ex-X
            # Mercenario" portano la keyword pur avendo un'altra fazione.
            if not (guerriero.fazione == Fazione.MERCENARIO
                    or (bool(guerriero.keywords) and "Mercenario" in guerriero.keywords)):
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Solo Mercenari")

        elif "Solo Comandant" in restrizione:  # copre "Comandante" e "Comandanti"
            if not guerriero.keywords or "Comandante" not in guerriero.keywords:
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Solo Comandanti")

        elif "Solo Nefarit" in restrizione:  # copre "Nefarita" e "Nefariti"
            if not guerriero.keywords or "Nefarita" not in guerriero.keywords:
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Solo Nefarita")

        elif "Non utilizzabile da Personalita" in restrizione:
            if (guerriero.tipo == TipoGuerriero.PERSONALITA
                    or (guerriero.keywords and "Personalita" in guerriero.keywords)):
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Non utilizzabile da Personalita")

        elif "Solo Personalita" in restrizione:
            # Basta una delle due dichiarazioni: nel database 27 Personalita' su
            # 29 portano il solo `tipo`, e nessuna la sola keyword. Pretenderle
            # entrambe lasciava fuori quasi tutte le Personalita' del gioco.
            if not (guerriero.tipo == TipoGuerriero.PERSONALITA
                    or (guerriero.keywords and "Personalita" in guerriero.keywords)):
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Solo Personalita")

        elif "Non utilizzabile dalla Fratellanza" in restrizione:
            if guerriero.fazione == Fazione.FRATELLANZA:
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Non utilizzabile dalla Fratellanza")

        elif "Non utilizzabile dalla Oscura Legione" in restrizione:
            if guerriero.fazione == Fazione.OSCURA_LEGIONE:
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Non utilizzabile dalla Oscura Legione")

        elif "Non utilizzabile dai Doomtroopers" in restrizione:
            # DOOMTROOPER è una lista di stringhe: va confrontata con fazione.value
            if guerriero.fazione.value in DOOMTROOPER:
                risultato["puo_assegnare"] = False
                risultato["errori"].append("Non utilizzabile dai Doomtrooper")

        elif "Assegnabile a guerrieri con V <= " in restrizione:
            valore_richiesto = int(
                restrizione.split("Assegnabile a guerrieri con V <= ")[1].strip()
            )
            if guerriero.stats.valore > valore_richiesto:
                risultato["puo_assegnare"] = False
                risultato["errori"].append(
                    f"Solo guerrieri con valore inferiore o uguale a {valore_richiesto}"
                )

    return risultato

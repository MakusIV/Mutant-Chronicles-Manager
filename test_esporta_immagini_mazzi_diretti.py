#!/usr/bin/env python3
"""
Script di test per verificare l'esportazione immagini passando direttamente
l'oggetto mazzo restituito da crea_mazzo_da_gioco().
"""

import sys
sys.path.append('/home/marco/Sviluppo/Mutant_Chronicles')

from source.logic.Creatore_Collezione import creazione_Collezione_Giocatore
from source.logic.Creatore_Mazzo import crea_mazzo_da_gioco, esporta_immagini_mazzi
from source.cards.Guerriero import Set_Espansione

def main():
    """Testa l'esportazione delle immagini da un mazzo creato direttamente."""

    print("Creazione collezione di test...")
    print("="*80)

    # Crea una collezione di test
    espansioni_richieste = [Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE]
    collezioni = creazione_Collezione_Giocatore(2, espansioni_richieste, orientamento=False)

    if not collezioni:
        print("Errore: Nessuna collezione creata")
        return

    
    print(f"Collezione creata con successo")

    mazzi = []

    print("\nCreazione mazzo da collezione...")
    print("="*80)

    # Crea un mazzo dalla collezione
    mazzo = crea_mazzo_da_gioco(
        collezioni[0],
        numero_carte_max=150,
        numero_carte_min=100,
        espansioni_richieste=["Base", "Inquisition", "Warzone"],
        doomtrooper=True,
        orientamento_doomtrooper=['Bauhaus', 'Capitol'],
        fratellanza=True,
        orientamento_arte=['Cambiamento', 'Elementi'],
        oscura_legione=False,
        orientamento_apostolo=[],
        orientamento_eretico=False,
        orientamento_cultista=False
    )

    print(f"Mazzo 1 creato:")
    print(f"  - Guerrieri squadra: {len(mazzo['squadra'])}")
    print(f"  - Guerrieri schieramento: {len(mazzo['schieramento'])}")
    print(f"  - Carte supporto: {len(mazzo['carte_supporto'])}")
    print(f"  - Totale: {mazzo['statistiche']['numero_totale_carte']} carte")

    mazzi.append(mazzo)

    # Crea un mazzo dalla collezione
    mazzo = crea_mazzo_da_gioco(
        collezioni[1],
        numero_carte_max=150,
        numero_carte_min=100,
        espansioni_richieste=["Base", "Inquisition", "Warzone"],
        doomtrooper=True,
        orientamento_doomtrooper=['Bauhaus', 'Capitol'],
        fratellanza=False,
        orientamento_arte=['Cambiamento', 'Elementi'],
        oscura_legione=True,
        orientamento_apostolo=["Algeroth", "Ilian", "Semai"],
        orientamento_eretico=True,
        orientamento_cultista=False
    )

    print(f"Mazzo 2 creato:")
    print(f"  - Guerrieri squadra: {len(mazzo['squadra'])}")
    print(f"  - Guerrieri schieramento: {len(mazzo['schieramento'])}")
    print(f"  - Carte supporto: {len(mazzo['carte_supporto'])}")
    print(f"  - Totale: {mazzo['statistiche']['numero_totale_carte']} carte")

    mazzi.append(mazzo)

    print("\nEsportazione immagini...")
    print("="*80)

    # Esporta le immagini passando il mazzo direttamente
    risultati = esporta_immagini_mazzi(mazzi, verbose=True)

    # Stampa riepilogo finale
    if 'errore' not in risultati:
        print("\n" + "="*80)
        print("TEST COMPLETATO CON SUCCESSO")
        print("="*80)
        print(f"Mazzi processati: {risultati['numero_mazzi']}")
        print(f"Immagini copiate: {risultati['totale_immagini_copiate']}")
        print(f"Immagini non trovate: {risultati['totale_immagini_non_trovate']}")
        print(f"Errori: {risultati['totale_errori']}")

        # Mostra dettagli del mazzo
        if risultati['dettaglio_mazzi']:
            dettaglio = risultati['dettaglio_mazzi'][0]
            print(f"\nDettagli mazzo_1:")
            print(f"  - Totale carte nel mazzo: {dettaglio['totale_carte']}")
            print(f"  - Immagini copiate: {dettaglio['immagini_copiate']}")
            print(f"  - Immagini non trovate: {len(dettaglio['immagini_non_trovate'])}")
    else:
        print("\n" + "="*80)
        print("TEST FALLITO")
        print("="*80)
        print(f"Errore: {risultati['errore']}")

if __name__ == "__main__":
    main()

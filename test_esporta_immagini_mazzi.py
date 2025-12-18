#!/usr/bin/env python3
"""
Script di test per le funzioni di esportazione immagini dei mazzi.
"""

import sys
sys.path.append('/home/marco/Sviluppo/Mutant_Chronicles')

from source.logic.Creatore_Mazzo import esporta_immagini_mazzi_da_json

def main():
    """Testa l'esportazione delle immagini da un file JSON di mazzi."""

    # Percorso del file JSON dei mazzi
    percorso_json = "out/mazzi.json"

    print(f"Test esportazione immagini da: {percorso_json}")
    print("="*80)

    # Esporta le immagini
    risultati = esporta_immagini_mazzi_da_json(percorso_json, verbose=True)

    # Stampa riepilogo finale
    if 'errore' not in risultati:
        print("\n" + "="*80)
        print("TEST COMPLETATO CON SUCCESSO")
        print("="*80)
        print(f"Mazzi processati: {risultati['numero_mazzi']}")
        print(f"Immagini copiate: {risultati['totale_immagini_copiate']}")
        print(f"Immagini non trovate: {risultati['totale_immagini_non_trovate']}")
        print(f"Errori: {risultati['totale_errori']}")
    else:
        print("\n" + "="*80)
        print("TEST FALLITO")
        print("="*80)
        print(f"Errore: {risultati['errore']}")

if __name__ == "__main__":
    main()

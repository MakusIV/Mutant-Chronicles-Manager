#!/usr/bin/env python3
"""
Test script per la funzione esporta_collezioni_giocatori
"""

import sys
sys.path.insert(0, '/home/marco/Sviluppo/Mutant_Chronicles')

from source.logic.Creatore_Collezione import crea_cartelle_collezioni
from source.cards.Guerriero import Set_Espansione

def main():
    print("="*80)
    print("TEST: esporta_collezioni_giocatori con 2 giocatori")
    print("="*80)

    # Test con 2 giocatori, espansione BASE
    risultato = crea_cartelle_collezioni(
        numero_giocatori=2,
        espansioni=[Set_Espansione.BASE],
        orientamento=False,
        nome_cartella="Test_2_Giocatori",
        verbose=True
    )

    print("\n" + "="*80)
    print("RISULTATI DEL TEST")
    print("="*80)

    if 'errore' in risultato:
        print(f"❌ ERRORE: {risultato['errore']}")
        return 1

    print(f"✅ Test completato con successo!")
    print(f"\n📊 Statistiche:")
    print(f"   - Timestamp: {risultato['timestamp']}")
    print(f"   - Numero collezioni: {risultato['numero_collezioni']}")
    print(f"   - Percorso principale: {risultato['percorso_principale']}")
    print(f"   - Collezioni esportate: {len(risultato['collezioni_esportate'])}")

    if risultato['errori']:
        print(f"\n⚠️  Errori riscontrati ({len(risultato['errori'])}):")
        for err in risultato['errori']:
            print(f"   - {err}")

    print(f"\n📁 Dettagli collezioni esportate:")
    for col in risultato['collezioni_esportate']:
        print(f"   Giocatore {col['id_giocatore']}:")
        print(f"      - Totale carte: {col['totale_carte']}")
        print(f"      - Valore DP: {col['valore_dp']}")
        print(f"      - Orientamento: {col['orientamento'] if col['orientamento'] else 'Nessuno'}")

    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ ERRORE FATALE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

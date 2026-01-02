#!/usr/bin/env python3
"""
Test script per la funzione crea_mazzo_da_cartella_collezione
"""

import sys
sys.path.insert(0, '/home/marco/Sviluppo/Mutant_Chronicles')

from source.logic.Creatore_Mazzo import crea_mazzo_da_cartella_collezione
from unittest.mock import patch
from io import StringIO

def main():
    print("="*80)
    print("TEST: crea_mazzo_da_cartella_collezione")
    print("="*80)
    print("Cartella: Collezioni_20260102_155823")
    print("Collezione: 1")
    print("="*80)

    # Simula input utente
    inputs = [
        "60",      # numero minimo carte
        "80",      # numero massimo carte
        "s",       # utilizzo doomtrooper
        "s",       # specificare fazioni doomtrooper
        "1,2,3",   # fazioni: Bauhaus, Capitol, Cybertronic
        "s",       # utilizzo fratellanza
        "n",       # non specificare tipologie Arte
        "n",       # non utilizzo oscura legione
        "n",       # non utilizzo eretici
        "1,2",     # espansioni: Base, Inquisition
    ]

    with patch('builtins.input', side_effect=inputs):
        try:
            risultato = crea_mazzo_da_cartella_collezione(
                cartella_collezioni="Collezioni_20260102_155823",
                numero_collezione=1,
                verbose=True
            )

            print("\n" + "="*80)
            print("RISULTATI DEL TEST")
            print("="*80)

            if risultato.get('successo'):
                print(f"✅ Test completato con successo!")
                print(f"\n📊 Statistiche:")
                print(f"   - Percorso mazzo: {risultato['percorso_mazzo']}")
                print(f"   - Numero carte: {risultato['numero_carte']}")

                mazzo = risultato.get('mazzo', {})
                if mazzo:
                    stats = mazzo.get('statistiche', {})
                    print(f"\n🎴 Dettagli mazzo:")
                    print(f"   - Guerrieri squadra: {len(mazzo.get('squadra', []))}")
                    print(f"   - Guerrieri schieramento: {len(mazzo.get('schieramento', []))}")
                    print(f"   - Carte supporto: {len(mazzo.get('carte_supporto', []))}")
                    print(f"   - Distribuzione per tipo: {stats.get('distribuzione_per_tipo', {})}")

                return 0
            else:
                print(f"❌ ERRORE: {risultato.get('errore', 'Errore sconosciuto')}")
                return 1

        except Exception as e:
            print(f"\n❌ ERRORE FATALE: {e}")
            import traceback
            traceback.print_exc()
            return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

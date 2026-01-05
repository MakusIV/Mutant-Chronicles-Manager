"""
Manager_Gioco.py
Modulo per la gestione delle funzionalità del gioco Mutant Chronicles/Doomtrooper
Implementa la creazione di collezioni di giocatori secondo le regole ufficiali del regolamento.

Autore: AI Assistant
Data: 2025
Versione: 1.0
"""


import sys
from datetime import datetime
import json
import shutil
from pathlib import Path


# Import delle classi delle carte (solo le classi, non le funzioni di creazione)
from source.logic.Creatore_Collezione import ( Set_Espansione, crea_cartelle_collezioni)

from source.logic.Creatore_Mazzo import (FAZIONI_DOOMTROOPER, crea_mazzo_da_cartella_collezione, carica_collezioni_json_migliorato, crea_mazzo_da_gioco, 
                                         crea_inventario_dettagliato_mazzo_json_con_conteggio_e_apostoli, crea_pdf_mazzo, copia_immagini_mazzo, stampa_mazzo)



PERCORSO_SALVATAGGIO = "out/"



# ==================== ESEMPI E TEST PER COLLEZIONE GIOCATORE ====================

def menu_interattivo():
    """Menu interattivo per testare le funzionalità"""
    
    while True:
        print("\n" + "="*60)
        print("MANAGER_GIOCO - MENU INTERATTIVO")
        print("="*60)       
        print("1. Creazione collezioni")
        print("2. Creazione mazzi")        
        print("3. Creazione automatica collezioni e mazzi:" \
        "mazzo 1, 5: Doomtrooper + Fratellanza," \
        "mazzo 2, 6: Doomtrooper + Oscura Legione + Eretici," \
        "mazzo 3, 7: Doomtrooper + Oscura Legione + Cultisti," \
        "mazzo 4, 8: Fratellanza + Oscura Legione + Eretici")
        print("0. Esci")
        
        scelta = input("\nScegli un'opzione: ").strip()
        
        if scelta == "0":
            print("Arrivederci!")
            break
        elif scelta == "1":
            # Creazione personalizzata
            try:
                num = int(input("Numero giocatori: "))
                
                print("Espansioni disponibili:")
                for i, esp in enumerate(Set_Espansione):
                    print(f"  {i+1}. {esp.value}")
                
                esp_input = input("Scegli espansioni (numeri separati da virgola): ")
                esp_indices = [int(x.strip())-1 for x in esp_input.split(",")]
                espansioni = [list(Set_Espansione)[i] for i in esp_indices if 0 <= i < len(Set_Espansione)]                
                orientamento = input("Orientamento (s/n): ").lower().startswith('s')           

                risultato = crea_cartelle_collezioni(
                    numero_giocatori=num,
                    espansioni=espansioni,
                    orientamento=orientamento,
                    nome_cartella=None,
                    verbose=True
                )

                print("\n" + "="*80)
                print("RISULTATI CREAZIONE COLLEZIONI E CARTELLE")
                print("="*80)

                if 'errore' in risultato:
                    print(f"❌ ERRORE: {risultato['errore']}")
                    return 1

                print(f"✅ Collezioni e cartelle create con successo!")
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

                
            except Exception as e:
                print(f"Errore: {e}")
            
        elif scelta == "2":
            # Creazione personalizzata         
            sys.path.insert(0, '/home/marco/Sviluppo/Mutant_Chronicles')
                            
            try:
                cartella_collezioni = str(input("nome cartella con il file collezioni da caricare: "))
                numero_collezione =  int(input("numero della collezione da caricare: "))

                risultato = crea_mazzo_da_cartella_collezione(
                    cartella_collezioni = cartella_collezioni,
                    numero_collezione = numero_collezione,
                    verbose=True
                )

                print("\n" + "="*80)
                print("RISULTATI DELLA CREAZIONE DEL MAZZO DA CARTELLA COLLEZIONE")
                print("="*80)

                if risultato.get('successo'):
                    print(f"✅ cartella mazzo e relativi contenuti creati con successo!")
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

                else:
                    print(f"❌ ERRORE: {risultato.get('errore', 'Errore sconosciuto')}")            

            except Exception as e:
                print(f"\n❌ ERRORE FATALE: {e}")
                import traceback
                traceback.print_exc()

            
        elif scelta == "3":
            # Creazione collezione   
            verbose = True               
            try:
                num = int(input("Numero giocatori: "))
                                
                espansioni = [Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE]                
                orientamento = 's'

                risultato = crea_cartelle_collezioni(
                    numero_giocatori=num,
                    espansioni=espansioni,
                    orientamento=orientamento,
                    nome_cartella="Collezioni Orientate_Automatiche",
                    verbose=verbose
                )

                print("\n" + "="*80)
                print("RISULTATI CREAZIONE COLLEZIONI E CARTELLE")
                print("="*80)

                if 'errore' in risultato:
                    print(f"❌ ERRORE: {risultato['errore']}")                    

                print(f"✅ Collezioni e cartelle create con successo!")
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

            except Exception as e:
                print(f"Errore: {e}")

            # Creazione mazzo         
            sys.path.insert(0, '/home/marco/Sviluppo/Mutant_Chronicles')
                            
            try:
                cartella_collezioni = "Collezioni Orientate_Automatiche"

                # Costruisce il percorso del file collezioni
                # NOTA: carica_collezioni_json_migliorato aggiunge automaticamente PERCORSO_SALVATAGGIO ("out/")
                percorso_relativo = f"{cartella_collezioni}/lista_collezioni.json"

                # Carica le collezioni
                if verbose:
                    print(f"\n📂 Caricamento collezioni...")

                risultato = carica_collezioni_json_migliorato(percorso_relativo)

                if not risultato:
                    raise ValueError(f"Impossibile caricare il file {percorso_relativo}")

                # La funzione restituisce una tupla (dati_json, collezioni)
                dati_json, collezioni = risultato

                if not collezioni:
                    raise ValueError("Nessuna collezione trovata nel file")
                
                opzioni_mazzo = {   1: {'doomtrooper': True, 'fratellanza': True, 'oscura_legione': False, 'eretici': False, 'cultisti': False},
                                    2: {'doomtrooper': True, 'fratellanza': False, 'oscura_legione': True, 'eretici': False, 'cultisti': True},
                                    3: {'doomtrooper': True, 'fratellanza': False, 'oscura_legione': True, 'eretici': True, 'cultisti': False},
                                    4: {'doomtrooper': False, 'fratellanza': True, 'oscura_legione': True, 'eretici': True, 'cultisti': False},
                                    5: {'doomtrooper': True, 'fratellanza': True, 'oscura_legione': False, 'eretici': False, 'cultisti': False},
                                    6: {'doomtrooper': True, 'fratellanza': False, 'oscura_legione': True, 'eretici': False, 'cultisti': True},
                                    7: {'doomtrooper': True, 'fratellanza': False, 'oscura_legione': True, 'eretici': True, 'cultisti': False},
                                    8: {'doomtrooper': False, 'fratellanza': True, 'oscura_legione': True, 'eretici': True, 'cultisti': False}
                                }

                for numero_collezione in range(1, num + 1):        
                
                    if verbose:
                        print(f"\n{'='*80}")
                        print(f"🎴 CREAZIONE MAZZO DA CARTELLA COLLEZIONE")
                        print(f"{'='*80}")
                        print(f"📁 Cartella: {cartella_collezioni}")
                        print(f"🎮 Numero collezione: {numero_collezione}")                   

                    if numero_collezione < 1 or numero_collezione > len(collezioni):
                        raise ValueError(f"Numero collezione non valido. Deve essere tra 1 e {len(collezioni)}")

                    collezione = collezioni[numero_collezione - 1]

                    if verbose:
                        print(f"✅ Collezione {numero_collezione} caricata")
                        print(f"\n{'='*80}")
                        print(f"CONFIGURAZIONE MAZZO")
                        print(f"{'='*80}")

                    # Interazione con l'utente per i parametri del mazzo
                    carte_min = 120
                    carte_max = 130

                    fazioni_doomtrooper = []
                    arti_scelte = []
                    apostoli_scelti = []                    
                                    
                    # Doomtrooper
                    doomtrooper = opzioni_mazzo[numero_collezione]['doomtrooper']                    
                    fratellanza = opzioni_mazzo[numero_collezione]['fratellanza']
                    oscura_legione = opzioni_mazzo[numero_collezione]['oscura_legione']
                    eretici = opzioni_mazzo[numero_collezione]['eretici']
                    cultisti = opzioni_mazzo[numero_collezione]['cultisti']


                    # Crea il mazzo
                    if verbose:
                        print(f"\n{'='*80}")
                        print(f"🔄 CREAZIONE MAZZO IN CORSO...")
                        print(f"{'='*80}")

                    mazzo = crea_mazzo_da_gioco(
                        collezione,
                        numero_carte_max=carte_max,
                        numero_carte_min=carte_min,
                        espansioni_richieste=espansioni,
                        doomtrooper=doomtrooper,
                        orientamento_doomtrooper=fazioni_doomtrooper,
                        fratellanza=fratellanza,
                        orientamento_arte=arti_scelte,
                        oscura_legione=oscura_legione,
                        orientamento_apostolo=apostoli_scelti,
                        orientamento_eretico=eretici,
                        orientamento_cultista=cultisti
                    )

                    if verbose:
                        print(f"✅ Mazzo creato: {mazzo['statistiche']['numero_totale_carte']} carte totali")

                    # Crea la struttura delle cartelle
                    percorso_cartella = Path(PERCORSO_SALVATAGGIO) / cartella_collezioni
                    cartella_collezione_giocatore = percorso_cartella / f"Collezione_Giocatore_{numero_collezione}"
                    cartella_mazzo = cartella_collezione_giocatore / f"Mazzo_Giocatore_{numero_collezione}"
                    cartella_mazzo.mkdir(parents=True, exist_ok=True)

                    if verbose:
                        print(f"\n📁 Cartella mazzo creata: {cartella_mazzo}")

                    # 1. Salva il JSON del mazzo
                    nome_file_json = f"mazzo_giocatore_{numero_collezione}.json"
                    percorso_json = cartella_mazzo / nome_file_json

                    # Crea la struttura JSON del mazzo
                    inventario_mazzo = crea_inventario_dettagliato_mazzo_json_con_conteggio_e_apostoli(mazzo, numero_collezione)

                    dati_mazzo = {
                        'metadata': {
                            'versione': '2.0',
                            'tipo_export': 'mazzo_singolo',
                            'data_creazione': datetime.now().isoformat(),
                            'numero_giocatore': numero_collezione
                        },
                        'mazzo': inventario_mazzo
                    }

                    with open(percorso_json, 'w', encoding='utf-8') as f:
                        json.dump(dati_mazzo, f, indent=2, ensure_ascii=False, default=str)

                    if verbose:
                        print(f"   ✅ JSON salvato: {nome_file_json}")

                    # 2. Crea il PDF
                    nome_file_pdf = f"elenco_carte_mazzo_{numero_collezione}.pdf"
                    percorso_pdf = cartella_mazzo / nome_file_pdf

                    pdf_creato = crea_pdf_mazzo(mazzo, str(percorso_pdf), numero_collezione)

                    if pdf_creato and verbose:
                        print(f"   ✅ PDF creato: {nome_file_pdf}")
                    elif not pdf_creato and verbose:
                        print(f"   ⚠️  Impossibile creare PDF")

                    # 3. Crea la cartella Immagini
                    cartella_immagini = cartella_mazzo / f"Immagini_Mazzo_{numero_collezione}"
                    cartella_immagini.mkdir(exist_ok=True)

                    if verbose:
                        print(f"   📁 Cartella immagini creata")

                    # 4. Esporta le immagini
                    if verbose:
                        print(f"   🖼️  Esportazione immagini in corso...")

                    try:
                        # Usa la funzione copia_immagini_mazzo
                        nome_mazzo_temp = f"temp_mazzo_{numero_collezione}"
                        risultato_immagini = copia_immagini_mazzo(nome_mazzo_temp, mazzo)

                        # Sposta le immagini nella cartella corretta
                        cartella_immagini_temp = Path(PERCORSO_SALVATAGGIO) / "mazzi_immagini" / nome_mazzo_temp

                        if cartella_immagini_temp.exists():
                            # Copia tutte le immagini mantenendo la struttura
                            for item in cartella_immagini_temp.iterdir():
                                dest = cartella_immagini / item.name
                                if item.is_dir():
                                    shutil.copytree(item, dest, dirs_exist_ok=True)
                                else:
                                    shutil.copy2(item, dest)

                            # Rimuovi la cartella temporanea
                            shutil.rmtree(cartella_immagini_temp)

                        if verbose:
                            num_immagini = sum(1 for _ in cartella_immagini.rglob('*.jpg')) + sum(1 for _ in cartella_immagini.rglob('*.png'))
                            print(f"   ✅ Immagini esportate: {num_immagini} file")

                    except Exception as e:
                        if verbose:
                            print(f"   ⚠️  Errore durante l'esportazione immagini: {e}")

                    # Riepilogo finale
                    if verbose:
                        print(f"\n{'='*80}")
                        print(f"✅ CREAZIONE MAZZO COMPLETATA")
                        print(f"{'='*80}")
                        print(f"📁 Percorso: {cartella_mazzo}")
                        print(f"🎴 Carte totali: {mazzo['statistiche']['numero_totale_carte']}")
                        print(f"⚔️ Guerrieri squadra: {len(mazzo['squadra'])}")
                        print(f"🌙 Guerrieri schieramento: {len(mazzo['schieramento'])}")
                        print(f"🎴 Carte supporto: {len(mazzo['carte_supporto'])}")

                    
            except Exception as e:
                errore_msg = f"Errore durante la creazione del mazzo: {str(e)}"
                if verbose:
                    print(f"\n❌ {errore_msg}")
                    import traceback
                    traceback.print_exc()

        else:
            print("Opzione non valida.")
        
        input("\nPremi Invio per continuare...")


# ==================== MAIN ====================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           MANAGER_GIOCO.PY                                  ║
║                    Mutant Chronicles / Doomtrooper                          ║
║                                                                              ║
║  Modulo per la creazione di collezioni e mazzi giocatore secondo le regole          ║
║  ufficiali del regolamento Doomtrooper.                                     ║
║                                                                              ║
║  Funzionalità implementate:                                                  ║
║  • Creazione collezioni giocatore
║  • Creazione mazzi giocatore  ║
║  • Creazione automatica collezioni e mazzi giocatore               ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    menu_interattivo()
    

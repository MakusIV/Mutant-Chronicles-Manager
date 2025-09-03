"""
Manager_Gioco.py
Modulo per la gestione delle funzionalità del gioco Mutant Chronicles/Doomtrooper
Implementa la creazione di collezioni di giocatori secondo le regole ufficiali del regolamento.

Autore: AI Assistant
Data: 2025
Versione: 1.0
"""

import random
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any, Union
from enum import Enum
import json
from collections import defaultdict
from dataclasses import dataclass


# Import delle classi delle carte (solo le classi, non le funzioni di creazione)
from source.logic.Creatore_Collezione import ( CollezioneGiocatore, Set_Espansione, creazione_Collezione_Giocatore, resetta_tracciamento_quantita, 
stampa_riepilogo_collezioni_migliorato, cerca_carte_in_collezione, salva_collezioni_json_migliorato,
carica_collezioni_json_migliorato, stampa_statistiche_da_json, verifica_integrità_collezioni, 
crea_guerriero_da_database, crea_equipaggiamento_da_database, crea_speciale_da_database, crea_reliquia_da_database,
crea_fortificazione_da_database, crea_arte_da_database, crea_missione_da_database, crea_oscura_simmetria_da_database,
crea_warzone_da_database)

from source.logic.Creatore_Mazzo import CreatoreMazzo, crea_mazzo_da_gioco, stampa_mazzo

"""
from source.cards.Guerriero import (
    Guerriero, Fazione, Set_Espansione, Rarity, TipoGuerriero
)
from source.cards.Equipaggiamento import Equipaggiamento
from source.cards.Speciale import Speciale
from source.cards.Fortificazione import Fortificazione
from source.cards.Missione import Missione
from source.cards.Arte import Arte, DisciplinaArte
from source.cards.Oscura_Simmetria import Oscura_Simmetria, ApostoloOscuraSimmetria
from source.cards.Reliquia import Reliquia
from source.cards.Warzone import Warzone



# Import dei database
from source.data_base_cards.Database_Guerriero import (
    GUERRIERI_DATABASE, get_numero_guerrieri_per_fazione, get_numero_guerrieri_per_set, get_guerrieri_per_fazione, get_guerrieri_per_set,
    crea_guerriero_da_nome as crea_guerriero_da_database
)
from source.data_base_cards.Database_Equipaggiamento import (
    DATABASE_EQUIPAGGIAMENTO, get_equipaggiamenti_per_fazione, get_equipaggiamenti_per_set,
    crea_equipaggiamento_da_database
)
from source.data_base_cards.Database_Speciale import (
    DATABASE_SPECIALI, get_carte_per_fazione as get_speciali_per_fazione, 
    get_carte_per_set as get_speciali_per_set,
    crea_carta_da_database as crea_speciale_da_database
)
from source.data_base_cards.Database_Fortificazione import (
    DATABASE_FORTIFICAZIONI, get_fortificazioni_per_fazione, get_fortificazioni_per_set,
    crea_fortificazione_da_database
)
from source.data_base_cards.Database_Missione import (
    DATABASE_MISSIONI, get_missioni_per_fazione, get_missioni_per_set,
    crea_missione_da_database
)
from source.data_base_cards.Database_Arte import (
    CARTE_ARTE_DATABASE, get_carte_per_fazione as get_arte_per_fazione,
    get_carte_per_set as get_arte_per_set,
    crea_carta_da_database as crea_arte_da_database
)
from source.data_base_cards.Database_Oscura_Simmetria import (
    DATABASE_OSCURA_SIMMETRIA, get_carte_per_apostolo as get_oscura_per_apostolo,
    get_carte_per_set as get_oscura_per_set,
    crea_carta_da_database as crea_oscura_simmetria_da_database
)
from source.data_base_cards.Database_Reliquia import (
    DATABASE_RELIQUIE, get_reliquie_per_fazione, get_reliquie_per_set,
    crea_reliquia_da_database as crea_reliquia_da_database
)
from source.data_base_cards.Database_Warzone import (
    DATABASE_WARZONE, filtra_warzone_per_fazione, filtra_warzone_per_set,
    ottieni_warzone as crea_warzone_da_database
)

"""

PERCORSO_SALVATAGGIO = "out/"




# Esempio di utilizzo
def esempio_inventario_dettagliato():
    """
    Esempio di come utilizzare le funzioni di inventario dettagliato.
    Questa funzione dovrebbe essere chiamata dopo aver creato alcune collezioni.
    """
    print("\n🔍 ESEMPIO UTILIZZO INVENTARIO DETTAGLIATO")
    print("=" * 60)
    print("Per utilizzare queste funzioni:")
    print("1. Crea alcune collezioni usando creazione_Collezione_Giocatore()")
    print("2. Chiama stampa_riepilogo_collezioni_migliorato(collezioni)")
    print("3. Per collezioni singole: stampa_inventario_dettagliato(collezione)")
    print("4. Per cercare carte: cerca_carte_in_collezione(collezione, 'termine')")




# ==================== ESEMPI E TEST PER COLLEZIONE GIOCATORE ====================

def test_creazione_collezioni_base():
    """Test base per la creazione di collezioni"""
    print("\n" + "="*60)
    print("TEST: Creazione collezioni BASE (senza orientamento)")
    print("="*60)
    
    collezioni = creazione_Collezione_Giocatore(
        numero_giocatori=2,
        espansioni=[Set_Espansione.BASE],
        orientamento=False
    )
    
    stampa_riepilogo_collezioni_migliorato(collezioni)
    
    integrità = verifica_integrità_collezioni(collezioni)
    print(f"\nRisultati verifica integrità: {integrità}")
    
    return collezioni


def test_creazione_collezioni_orientate():
    """Test per la creazione di collezioni con orientamento"""
    print("\n" + "="*60)
    print("TEST: Creazione collezioni ORIENTATE")
    print("="*60)
    
    collezioni = creazione_Collezione_Giocatore(
        numero_giocatori=3,
        espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
        orientamento=True
    )
    
    stampa_riepilogo_collezioni_migliorato(collezioni)
    
    integrità = verifica_integrità_collezioni(collezioni)
    print(f"\nRisultati verifica integrità: {integrità}")
    
    return collezioni


def test_creazione_collezioni_multiple_espansioni():
    """Test per la creazione di collezioni con multiple espansioni"""
    print("\n" + "="*60)
    print("TEST: Creazione collezioni MULTIPLE ESPANSIONI")
    print("="*60)
    
    collezioni = creazione_Collezione_Giocatore(
        numero_giocatori=4,
        espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE],
        orientamento=True
    )
    
    stampa_riepilogo_collezioni_migliorato(collezioni)
    
    integrità = verifica_integrità_collezioni(collezioni)
    print(f"\nRisultati verifica integrità: {integrità}")
    
    return collezioni


def test_creazione_collezioni_stress():
    """Test stress per verificare la gestione delle quantità"""
    print("\n" + "="*60)
    print("TEST: STRESS TEST - Molte collezioni")
    print("="*60)
    
    try:
        collezioni = creazione_Collezione_Giocatore(
            numero_giocatori=8,
            espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
            orientamento=True
        )
        
        stampa_riepilogo_collezioni_migliorato(collezioni)
        
        integrità = verifica_integrità_collezioni(collezioni)
        print(f"\nRisultati verifica integrità: {integrità}")
        
        # Verifica se ci sono state limitazioni per quantità
        print(f"\nQuantità utilizzate totali:")
        for carta, quantita in sorted(QUANTITA_UTILIZZATE.items()):
            if quantita > 3:  # Mostra solo carte con alta utilizzazione
                print(f"  {carta}: {quantita}")
        
        return collezioni
        
    except Exception as e:
        print(f"Errore durante stress test: {e}")
        return []


def test_validazione_parametri():
    """Test per validazione parametri di input"""
    print("\n" + "="*60)
    print("TEST: Validazione parametri")
    print("="*60)
    
    # Test parametri non validi
    test_cases = [
        (0, [Set_Espansione.BASE], False, "numero_giocatori = 0"),
        (-1, [Set_Espansione.BASE], False, "numero_giocatori negativo"),
        (1, [], False, "espansioni vuote"),
        (1, ["INVALID"], False, "espansione non valida"),
        (1, [None], False, "espansione None")
    ]
    
    for num_giocatori, espansioni, orientamento, descrizione in test_cases:
        print(f"\nTestando: {descrizione}")
        try:
            collezioni = creazione_Collezione_Giocatore(num_giocatori, espansioni, orientamento)
            print(f"  ❌ Doveva fallire ma ha creato {len(collezioni)} collezioni")
        except Exception as e:
            print(f"  ✅ Fallito correttamente: {e}")
    
    # Test parametri validi edge case
    print(f"\nTestando: 1 giocatore, 1 espansione")
    try:
        collezioni = creazione_Collezione_Giocatore(1, [Set_Espansione.BASE], False)
        print(f"  ✅ Successo: {len(collezioni)} collezione creata")
        if collezioni[0].statistiche.guerrieri == 0:
            print(f"    ℹ️  Collezione senza guerrieri (OK per collezione giocatore)")
    except Exception as e:
        print(f"  ❌ Fallito inaspettatamente: {e}")


def analizza_bilanciamento_collezioni(collezioni: List[CollezioneGiocatore]):
    """Analizza il bilanciamento delle collezioni create"""
    print("\n" + "="*60)
    print("ANALISI BILANCIAMENTO COLLEZIONI")
    print("="*60)
    
    if not collezioni:
        print("Nessuna collezione da analizzare")
        return
    
    # Statistiche per tipo di carta
    stats_tipi = defaultdict(list)
    stats_valore = []
    stats_fazioni = defaultdict(list)
    
    for collezione in collezioni:
        stats = collezione.statistiche
        stats_tipi['guerrieri'].append(stats.guerrieri)
        stats_tipi['equipaggiamenti'].append(stats.equipaggiamenti)
        stats_tipi['speciali'].append(stats.speciali)
        stats_tipi['fortificazioni'].append(stats.fortificazioni)
        stats_tipi['missioni'].append(stats.missioni)
        stats_tipi['arte'].append(stats.arte)
        stats_tipi['oscura simmetria'].append(stats.oscura_simmetria)
        stats_tipi['reliquie'].append(stats.reliquie)
        stats_tipi['warzone'].append(stats.warzone)
        
        stats_valore.append(stats.valore_totale_dp)
        
        for fazione, count in stats.per_fazione.items():
            stats_fazioni[fazione].append(count)
    
    # Analisi distribuzione tipi di carte
    print("Distribuzione per tipo di carta:")
    for tipo, valori in stats_tipi.items():
        if valori:
            media = sum(valori) / len(valori)
            minimo = min(valori)
            massimo = max(valori)
            print(f"  {tipo.capitalize()}: min={minimo}, max={massimo}, media={media:.1f}")
    
    # Analisi valore collezioni
    if stats_valore:
        media_valore = sum(stats_valore) / len(stats_valore)
        min_valore = min(stats_valore)
        max_valore = max(stats_valore)
        print(f"\nValore DP collezioni:")
        print(f"  Min: {min_valore}, Max: {max_valore}, Media: {media_valore:.1f}")
        
        # Calcola varianza per verificare bilanciamento
        varianza = sum((v - media_valore) ** 2 for v in stats_valore) / len(stats_valore)
        deviazione_std = varianza ** 0.5
        print(f"  Deviazione standard: {deviazione_std:.1f}")
        
        if deviazione_std < media_valore * 0.2:
            print("  ✅ Collezioni ben bilanciate")
        else:
            print("  ⚠️ Collezioni potrebbero essere sbilanciate")
    
    # Analisi distribuzione fazioni
    print(f"\nDistribuzione fazioni:")
    for fazione, valori in stats_fazioni.items():
        if valori:
            media = sum(valori) / len(valori)
            presente_in = len([v for v in valori if v > 0])
            print(f"  {fazione}: media={media:.1f}, presente in {presente_in}/{len(collezioni)} collezioni")
    
    # Analisi guerrieri nelle collezioni
    guerrieri_valori = stats_tipi.get('guerrieri', [])
    if guerrieri_valori:
        collezioni_senza_guerrieri = len([v for v in guerrieri_valori if v == 0])
        if collezioni_senza_guerrieri > 0:
            print(f"\n⚠️  {collezioni_senza_guerrieri} collezioni senza guerrieri")
            print(f"   (OK per collezioni giocatore - potranno acquistare guerrieri separatamente)")

# Esempio di utilizzo
def esempio_salvataggio_migliorato():
    """
    Esempio di utilizzo delle funzioni di salvataggio migliorato.
    """
    print("\n🔍 ESEMPIO SALVATAGGIO JSON MIGLIORATO")
    print("=" * 60)
    print("1. Crea collezioni: collezioni = creazione_Collezione_Giocatore(...)")
    # Crea collezioni
    collezioni = creazione_Collezione_Giocatore(
            numero_giocatori=2,
            espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
            orientamento=True
        )
    # Stampa con visualizzazione migliorata
    stampa_riepilogo_collezioni_migliorato(collezioni)
    print("2. Salva dettagliato: salva_collezioni_json_migliorato(collezioni, 'collezioni_dettagliate.json')")
    # Salva con la STESSA struttura in JSON
    salva_collezioni_json_migliorato(collezioni, "collezioni_dettagliate.json")
    print("3. Carica: dati = carica_collezioni_json_migliorato('collezioni_dettagliate.json')")
    dati_json = carica_collezioni_json_migliorato("collezioni_dettagliate.json")
    print("4. Visualizza: stampa_statistiche_da_json(dati)")
    stampa_statistiche_da_json(dati_json)

def esempio_utilizzo_completo():
    """Esempio completo di utilizzo del Manager_Gioco"""
    print("\n" + "="*80)
    print("ESEMPIO UTILIZZO COMPLETO - MANAGER_GIOCO")
    print("="*80)
    
    # Reset per esempio pulito
    resetta_tracciamento_quantita()
    
    print("1. Creazione collezioni per torneo 4 giocatori...")
    collezioni_torneo = creazione_Collezione_Giocatore(
        numero_giocatori=4,
        espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
        orientamento=True
    )
    
    print("\n2. Analisi dettagliata delle collezioni...")
    stampa_riepilogo_collezioni_migliorato(collezioni_torneo)
    
    print("\n3. Verifica integrità...")
    integrità = verifica_integrità_collezioni(collezioni_torneo)
    print(f"Risultati integrità: {integrità}")
    
    print("\n4. Analisi bilanciamento...")
    analizza_bilanciamento_collezioni(collezioni_torneo)
    
    print("\n5. Dettaglio orientamenti utilizzati...")
    for collezione in collezioni_torneo:
        if collezione.fazioni_orientamento:
            fazioni_str = ", ".join([f.value for f in collezione.fazioni_orientamento])
            print(f"  Giocatore {collezione.id_giocatore}: {fazioni_str}")
        else:
            print(f"  Giocatore {collezione.id_giocatore}: Nessun orientamento")
    
    print("\n6. Esempio accesso alle carte...")
    collezione_esempio = collezioni_torneo[0]
    print(f"\nCollezione Giocatore 1:")
    print(f"  Guerrieri: {len(collezione_esempio.get_carte_per_tipo('guerrieri'))}")
    print(f"  Equipaggiamenti: {len(collezione_esempio.get_carte_per_tipo('equipaggiamenti'))}")
    
    # Mostra alcuni esempi di carte
    guerrieri = collezione_esempio.get_carte_per_tipo('guerrieri')
    if guerrieri:
        print(f"  Primo guerriero: {guerrieri[0].nome} ({guerrieri[0].fazione.value})")
    
    equipaggiamenti = collezione_esempio.get_carte_per_tipo('equipaggiamenti')
    if equipaggiamenti:
        print(f"  Primo equipaggiamento: {equipaggiamenti[0].nome}")
    
    return collezioni_torneo

def menu_interattivo():
    """Menu interattivo per testare le funzionalità"""
    
    while True:
        print("\n" + "="*60)
        print("MANAGER_GIOCO - MENU INTERATTIVO")
        print("="*60)
        print("1. Test creazione collezioni base")
        print("2. Test creazione collezioni orientate")
        print("3. Test multiple espansioni")
        print("4. Stress test")
        print("5. Test validazione parametri")
        print("6. Esempio utilizzo completo")
        print("7. Creazione personalizzata")
        print("8. Reset tracciamento quantità")
        print("9. Carica collezioni da JSON")
        print("0. Esci")
        
        scelta = input("\nScegli un'opzione: ").strip()
        
        if scelta == "0":
            print("Arrivederci!")
            break
        elif scelta == "1":
            test_creazione_collezioni_base()
        elif scelta == "2":
            test_creazione_collezioni_orientate()
        elif scelta == "3":
            test_creazione_collezioni_multiple_espansioni()
        elif scelta == "4":
            test_creazione_collezioni_stress()
        elif scelta == "5":
            test_validazione_parametri()
        elif scelta == "6":
            esempio_utilizzo_completo()
        elif scelta == "7":
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
                
                collezioni = creazione_Collezione_Giocatore(num, espansioni, orientamento)
                stampa_riepilogo_collezioni_migliorato(collezioni)
                
                salva = input("Salvare in JSON? (s/n): ").lower().startswith('s')
                if salva:
                    filename = f"collezioni_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    salva_collezioni_json_migliorato(collezioni, filename)
                
            except Exception as e:
                print(f"Errore: {e}")
        elif scelta == "8":
            resetta_tracciamento_quantita()
            print("Tracciamento quantità resettato.")
        elif scelta == "9":
            try:
                num = str(input("nome file collezione: "))
                carica_collezioni_json_migliorato(num)
            except Exception as e:
                print(f"Errore: {e}")

        else:
            print("Opzione non valida.")
        
        input("\nPremi Invio per continuare...")

def test_creazioni_individuali():
    """Test delle singole funzioni di creazione carte"""
    print("Testando funzioni di creazione individuali...")
    
    test_cases = [
        ("Guerriero", crea_guerriero_da_database, "Bauhaus Blitzer"),
        ("Equipaggiamento", crea_equipaggiamento_da_database, "spada_combattimento"),
        ("Speciale", crea_speciale_da_database, "tactical_advance"),
        ("Fortificazione", crea_fortificazione_da_database, "Heimburg"),
        ("Missione", crea_missione_da_database, "recupero_intelligence"),
        ("Arte", crea_arte_da_database, "blessing_of_light"),
        ("Oscura Simmetria", crea_oscura_simmetria_da_database, "corruzione_minore"),
        ("Reliquia", crea_reliquia_da_database, "antica_reliquia"),
        ("Warzone", crea_warzone_da_database, "zona_guerra")
    ]
    
    for tipo_carta, funzione, nome_esempio in test_cases:
        try:
            carta = funzione(nome_esempio)
            if carta:
                print(f"  ✅ {tipo_carta}: {carta.nome}")
            else:
                print(f"  ⚠️ {tipo_carta}: carta '{nome_esempio}' non trovata (OK se non nel database)")
        except Exception as e:
            print(f"  ❌ {tipo_carta}: errore durante la creazione: {e}")
    
    print(f"\n{'='*80}")
    print("Per testare interattivamente, decommentare la riga seguente:")
    print("# menu_interattivo()")
    print(f"{'='*80}")
    




# ==================== MAIN ====================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           MANAGER_GIOCO.PY                                  ║
║                    Mutant Chronicles / Doomtrooper                          ║
║                                                                              ║
║  Modulo per la creazione di collezioni giocatore secondo le regole          ║
║  ufficiali del regolamento Doomtrooper.                                     ║
║                                                                              ║
║  Funzionalità implementate:                                                  ║
║  • Creazione collezioni giocatore (non mazzi da gioco)                      ║
║  • Orientamento fazioni casuali (Fratellanza-Doomtrooper-Freelancer, etc.)  ║
║  • Selezione casuale carte da tutte le espansioni specificate               ║
║  • Verifica integrità e bilanciamento collezioni                            ║
║  • Export/Import JSON                                                        ║
║  • Sistema di test completo                                                  ║
║                                                                              ║
║  NOTA: CollezioneGiocatore = tutte le carte possedute                       ║
║        Mazzo da gioco = sottoinsieme con min 5 guerrieri (creato separatam.)║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("AVVIO DEMO AUTOMATICA...")
    
    # Demo rapida delle funzionalità principali
    try:
        print("\n🎯 Demo: Creazione collezioni base")
        demo_collezioni = creazione_Collezione_Giocatore(
            numero_giocatori=2,
            espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
            orientamento=False
        )
        print(f"✅ Create {len(demo_collezioni)} collezioni base")
        
        print("\n🎯 Demo: Creazione collezioni orientate")
        demo_orientate = creazione_Collezione_Giocatore(
            numero_giocatori=2,
            espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION],
            orientamento=True
        )
        print(f"✅ Create {len(demo_orientate)} collezioni orientate")
        
        print("\n🎯 Demo: Verifica integrità")
        integrità = verifica_integrità_collezioni(demo_orientate)
        print(f"✅ Verifica completata: {integrità['collezioni_valide']} valide su {len(demo_orientate)}")
        
        print(f"\n🎯 Demo completata con successo!")
        print(f"📊 Totale carte generate: {sum(c.get_totale_carte() for c in demo_collezioni + demo_orientate)}")
        
        print("\n🎯 Demo: Test funzioni di creazione individuali")
        test_creazioni_individuali()

        print("\n🎯 Demo: Test salvataggio")
        esempio_salvataggio_migliorato()
        
        print("\n🎯 Demo: Creazione Mazzo non orientato")
        demo_orientate = creazione_Collezione_Giocatore(
            numero_giocatori=2,
            espansioni=[Set_Espansione.BASE, Set_Espansione.INQUISITION, Set_Espansione.WARZONE],
            orientamento=False
        )
        print(f"✅ Create {len(demo_orientate)} collezioni orientate")

        # Demo creazione mazzo
        mazzo_1 = crea_mazzo_da_gioco(
            demo_orientate[0],
            numero_carte_max=70,
            numero_carte_min=60,
            espansioni_richieste=['Base', 'Inquisition'],
            doomtrooper=True,
            orientamento_doomtrooper=['Mishima', 'Bauhaus', 'Freelancer', 'Fratellanza'],
            fratellanza=True,
            orientamento_arte=['Cambiamento', 'Combattimento', 'Premonizione'],
            oscura_legione=False,
            orientamento_apostolo=None,
            orientamento_eretico=False,
            orientamento_cultista=False
        )
        stampa_mazzo(mazzo_1)
        mazzo_2 = crea_mazzo_da_gioco(
            demo_orientate[1],
            numero_carte_max=60,
            numero_carte_min=50,
            espansioni_richieste=['Base', 'Inquisition', 'Warzone'],
            doomtrooper=True,
            orientamento_doomtrooper=['Cybertronic', 'Capitol', 'Imperial'],
            fratellanza=False,
            orientamento_arte=None,
            oscura_legione=True,
            orientamento_apostolo=['Algeroth', 'Semai'],
            orientamento_eretico=True,
            orientamento_cultista=False
        )
        stampa_mazzo(mazzo_2)
        

        # Per attivare il menu interattivo, decommenta la riga seguente:
        #menu_interattivo()

    except Exception as e:
        print(f"❌ Errore durante la demo: {e}")


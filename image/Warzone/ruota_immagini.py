#!/usr/bin/env python3
"""
Script per ruotare immagini JPEG in una cartella.

Uso:
    python ruota_immagini.py <percorso_cartella> <direzione>
    
Direzioni disponibili:
    - destra: rotazione di 90° in senso orario
    - sinistra: rotazione di 90° in senso antiorario
    - capovolgi: rotazione di 180°
"""

import argparse
import os
import sys
from pathlib import Path
from PIL import Image


def valida_cartella(percorso):
    """Verifica che il percorso sia una cartella esistente."""
    if not os.path.exists(percorso):
        print(f"Errore: La cartella '{percorso}' non esiste.")
        return False
    if not os.path.isdir(percorso):
        print(f"Errore: '{percorso}' non è una cartella.")
        return False
    return True


def trova_immagini_jpeg(cartella):
    """Trova tutti i file JPEG nella cartella."""
    estensioni_jpeg = {'.jpg', '.jpeg', '.JPG', '.JPEG'}
    immagini = []
    
    for file in os.listdir(cartella):
        percorso_completo = os.path.join(cartella, file)
        if os.path.isfile(percorso_completo):
            _, estensione = os.path.splitext(file)
            if estensione in estensioni_jpeg:
                immagini.append(percorso_completo)
    
    return immagini


def ruota_immagine(percorso_immagine, direzione):
    """
    Ruota un'immagine nella direzione specificata.
    
    Args:
        percorso_immagine: percorso completo dell'immagine
        direzione: 'destra', 'sinistra' o 'capovolgi'
    
    Returns:
        True se l'operazione ha successo, False altrimenti
    """
    try:
        # Apri l'immagine
        img = Image.open(percorso_immagine)
        
        # Determina l'angolo di rotazione
        # PIL ruota in senso antiorario, quindi:
        # - destra (orario) = -90° = 270°
        # - sinistra (antiorario) = 90°
        # - capovolgi = 180°
        if direzione == 'destra':
            img_ruotata = img.rotate(-90, expand=True)
        elif direzione == 'sinistra':
            img_ruotata = img.rotate(90, expand=True)
        elif direzione == 'capovolgi':
            img_ruotata = img.rotate(180, expand=True)
        else:
            print(f"Errore: direzione '{direzione}' non valida.")
            return False
        
        # Salva l'immagine sovrascrivendo l'originale
        # Mantieni la qualità e i metadati EXIF se possibile
        img_ruotata.save(
            percorso_immagine,
            quality=95,
            optimize=False,
            exif=img.info.get('exif', b'')
        )
        
        img.close()
        img_ruotata.close()
        
        return True
        
    except Exception as e:
        print(f"Errore durante la rotazione di '{percorso_immagine}': {e}")
        return False


def main():
    """Funzione principale dello script."""
    # Configura il parser degli argomenti
    parser = argparse.ArgumentParser(
        description='Ruota tutte le immagini JPEG in una cartella.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:
  python ruota_immagini.py ./foto destra
  python ruota_immagini.py /percorso/cartella sinistra
  python ruota_immagini.py ~/immagini capovolgi
        """
    )
    
    parser.add_argument(
        'cartella',
        help='Percorso della cartella contenente le immagini JPEG'
    )
    
    parser.add_argument(
        'direzione',
        choices=['destra', 'sinistra', 'capovolgi'],
        help='Direzione di rotazione: destra (90° orario), sinistra (90° antiorario), capovolgi (180°)'
    )
    
    # Parsing degli argomenti
    args = parser.parse_args()
    
    # Valida la cartella
    if not valida_cartella(args.cartella):
        sys.exit(1)
    
    # Trova tutte le immagini JPEG
    immagini = trova_immagini_jpeg(args.cartella)
    
    if not immagini:
        print(f"Nessuna immagine JPEG trovata nella cartella '{args.cartella}'.")
        sys.exit(0)
    
    print(f"Trovate {len(immagini)} immagini JPEG.")
    print(f"Rotazione: {args.direzione}")
    print("-" * 50)
    
    # Ruota ogni immagine
    successi = 0
    fallimenti = 0
    
    for i, percorso_img in enumerate(immagini, 1):
        nome_file = os.path.basename(percorso_img)
        print(f"[{i}/{len(immagini)}] Elaborando: {nome_file}...", end=' ')
        
        if ruota_immagine(percorso_img, args.direzione):
            print("✓ OK")
            successi += 1
        else:
            print("✗ ERRORE")
            fallimenti += 1
    
    # Riepilogo finale
    print("-" * 50)
    print(f"Completato: {successi} successi, {fallimenti} fallimenti")
    
    if fallimenti > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()

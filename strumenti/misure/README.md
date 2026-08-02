# Strumenti di misura

Script usati per verificare le correzioni alla logica di selezione delle carte, documentate
in `documentazione/ANALISI_LOGICA_COLLEZIONI_MAZZI.md`.

Servono a **misurare il comportamento del codice invece di dedurlo dalla lettura**: ogni
correzione a `Creatore_Collezione.py` / `Creatore_Mazzo.py` cambia la composizione di
collezioni e mazzi, e verificare che non vengano sollevate eccezioni non basta a dire che il
risultato sia migliore. Il metodo è sempre lo stesso: catturare una misura *prima* della
modifica, applicarla, ricatturare e confrontare.

Si eseguono dalla radice del repository:

```bash
python3 strumenti/misure/validate.py
```

| Script | A cosa serve |
|---|---|
| `validate.py` | Istanzia **tutte** le carte dei 9 database tramite `from_dict` e riporta i fallimenti per tipo. È il controllo più rapido dopo qualunque modifica ai `Database_*.py`: intercetta i valori fuori dal vocabolario degli enum, che altrimenti farebbero sparire la carta in silenzio. |
| `compat.py` | Costruisce la matrice di compatibilità carta × guerriero su un campione di guerrieri rappresentativi (Doomtrooper, Fratellanza con e senza "Tutte le Discipline", Oscura Legione, Seguaci, Eretici, Nefarita, Mercenari, Comandanti). Stampa JSON, pensato per essere diffato fra due esecuzioni. |
| `potenze.py` | Punteggi di potenza di Equipaggiamento, Fortificazione, Reliquia e Warzone. |
| `punteggi.py` | Punteggi di Speciale, Arte e Oscura Simmetria, con minimo/mediana/massimo e **numero di valori distinti** — l'indicatore che rivela quando una funzione di punteggio non discrimina. |
| `harness.py` | Costruisce una collezione di prova contenente ogni carta del database, per isolare la logica di selezione dalla casualità della generazione. Importato dagli altri script. |
| `fascia1.py` | Misura sui **due livelli**: quota di guerrieri nelle fazioni richieste (Collezione) e rispetto di espansione e orientamento Arte (Mazzo). |
| `redistrib.py` | Dimensione dei mazzi, composizione per tipo, copie massime per carta e mazzi sotto il minimo di 60 carte. Serve a verificare la ridistribuzione degli slot non riempiti. |
| `diffmap.py` | Associa ogni blocco del `git diff` dei `Database_*.py` alla carta a cui appartiene. Utile per rileggere una tornata di correzioni carta per carta. |

## Nota sui confronti

Le correzioni cambiano la sequenza di consumo del generatore casuale, quindi due esecuzioni
con lo stesso seme **non** producono "lo stesso mazzo corretto": il flusso diverge. I confronti
vanno fatti su proprietà aggregate (quote, conteggi, valori distinti, violazioni di vincolo),
non carta per carta.

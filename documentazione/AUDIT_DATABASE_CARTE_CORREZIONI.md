# Audit dei moduli `data_base_cards` vs immagini reali delle carte

> **Scopo del documento.** Questo file raccoglie i risultati di un audit completo (agosto 2026) che ha confrontato ogni singola voce dei moduli Python in `source/data_base_cards/` con la scansione reale della carta corrispondente in `image/`.
>
> **Stato: sessione di correzione applicata (2026-07-31).** Tutte le discrepanze **certe** (nessun dubbio, nessuna verifica visiva ulteriore necessaria) sono state corrette direttamente nei file `.py` e sono marcate **✅ APPLICATA** qui sotto. Le voci ⚪ **DA VERIFICARE**, quelle che il documento stesso segnalava come richiedenti un secondo controllo visivo o una decisione di design, e i casi con dati insufficienti per una correzione completa (es. carta mancante senza trascrizione integrale) **restano non applicate** e sono marcate **⏳ NON APPLICATA — richiede verifica**.
>
> **Copertura:** tutte le carte con immagine disponibile sono state controllate (~541 immagini totali su 9 moduli).
>
> **Legenda priorità:**
> - 🔴 **CRITICA** — l'effetto di gioco descritto nel database è sostanzialmente diverso da quello reale della carta (cambia le regole se usato per implementare il gioco).
> - 🟠 **MEDIA** — un valore numerico o un dettaglio meccanico è errato, ma l'effetto generale della carta resta riconoscibile.
> - 🟡 **BASSA** — refuso, differenza di accentazione/capitalizzazione, o dettaglio cosmetico senza impatto sulle regole.
> - ⚪ **DA VERIFICARE** — l'agente ha segnalato un sospetto (confidenza media, es. basato solo sul confronto tra icone) ma non una certezza; richiede un secondo controllo visivo prima di correggere.

---

## Indice

1. [Riepilogo per priorità](#1-riepilogo-per-priorità)
   - [1bis. Verifica di coerenza sui campi normalizzati](#1bis-verifica-di-coerenza-sui-campi-normalizzati-2026-08-01)
   - [1ter. Audit esteso dei campi normalizzati](#1ter-audit-esteso-dei-campi-normalizzati-2026-08-01-seconda-sessione)
   - [1quater. `"Luna"` e il conflitto di tipo su `modificatori[].valore`](#1quater-luna-e-il-conflitto-di-tipo-su-modificatorivalore-2026-08-01)
   - [1quinquies. Riattivazione di `STATISTICHE_MODIFICATORI`](#1quinquies-riattivazione-di-statistiche_modificatori-2026-08-01)
2. [Anomalie strutturali trasversali (chiavi duplicate)](#2-anomalie-strutturali-trasversali-chiavi-duplicate)
3. [Database_Warzone.py](#3-database_warzonepy)
4. [Database_Fortificazione.py](#4-database_fortificazionepy)
5. [Database_Missione.py](#5-database_missionepy)
6. [Database_Guerriero.py](#6-database_guerreiropy)
7. [Database_Reliquia.py](#7-database_reliquiapy)
8. [Database_Oscura_Simmetria.py](#8-database_oscura_simmetriapy)
   - [8bis. Cinque carte con `statistica_target` errato](#8bis-cinque-carte-con-statistica_target-errato-2026-08-02)
9. [Database_Arte.py](#9-database_artepy)
10. [Database_Equipaggiamento.py](#10-database_equipaggiamentopy)
11. [Database_Speciale.py](#11-database_specialepy)
12. [Problemi non-database (organizzazione file immagini)](#12-problemi-non-database-organizzazione-file-immagini)
13. [Voci ancora da verificare (riepilogo)](#13-voci-ancora-da-verificare-riepilogo)

---

## 1. Riepilogo per priorità

| Priorità | Numero di correzioni individuate | Applicate in questa sessione |
|---|---|---|
| 🔴 CRITICA | 9 (+5 trovate il 2026-08-02) | 14/14 ✅ (Necromagus Supremo il 2026-08-01; le 5 carte di §8bis il 2026-08-02) |
| 🟠 MEDIA | 23 (+1 trovata il 2026-08-02) | 21 (escluse le 3 legate a voci ⚪ o a decisioni di design; `"Untore"`/`bersaglio` aggiunta in §8bis) |
| 🟡 BASSA | ~36 | ~33 (escluse le voci esplicitamente deprioritizzate/opzionali) |
| ⚪ DA VERIFICARE | 8 | 0 (per definizione, richiedono un secondo controllo visivo) |
| Anomalie strutturali (chiavi duplicate) | 7 chiavi coinvolte | 7/7 ✅ (tutte risolte: 3 il 2026-07-31, altre 4 il 2026-08-01 dopo verifica diretta dell'utente) |
| Finding ritirati (non erano difetti reali) | 1 (Citadella Sanctum) | — |
| Carta mancante dal database | 1 (Famoso Collezionista) | 0 (dati insufficienti: testo carta troncato nell'audit originale) |

**Copertura audit per modulo:**

| Modulo | Carte controllate | Esito | Correzioni applicate |
|---|---|---|---|
| `Database_Warzone.py` | 14/14 | 0 discrepanze reali (1 finding iniziale ritirato, vedi §3) | — |
| `Database_Fortificazione.py` | 26/26 | 1 discrepanza | 1/1 ✅ |
| `Database_Missione.py` | 7/7 | 2 discrepanze | 2/2 ✅ + refusi minori |
| `Database_Guerriero.py` | 136/136 (tutte le fazioni, incluso Mishima e Mercenario) † | 20 discrepanze + refusi minori | 20/20 ✅ |
| `Database_Reliquia.py` | 18/18 | 2 discrepanze | 2/2 ✅ |
| `Database_Oscura_Simmetria.py` | 35/36 (1 immagine duplicata di categoria) | 1 discrepanza grave | 1/1 ✅ |
| `Database_Arte.py` | 61/66 (66 voci DB, 61 immagini, 3 dichiarate assenti, 2 senza immagine) | 8 discrepanze | 8/8 ✅ |
| `Database_Equipaggiamento.py` | 79/79 | 1 refuso + 4 da verificare | 0 (nessuna correzione certa da applicare) |
| `Database_Speciale.py` | 163/163 (180 chiavi dopo rimozione dei 7 duplicati) | 12 discrepanze + 1 carta mancante + 7 chiavi duplicate | 12/12 ✅ + 7/7 duplicati risolti |

\* **Nota storica: la fazione Mishima (`image/Mishima/`, 12 carte) non era stata verificata nel primo giro di audit.** L'agente originariamente incaricato ("Guerrieri parte 2") si era interrotto per un limite di spesa dopo aver completato solo Fratellanza (15/15 CONFORME); nella ripresa del lavoro era stato deliberatamente riassegnato solo su Oscura Legione + Mercenario, senza includere Mishima. **Il lotto Mishima è stato controllato in una sessione successiva (vedi §6, sottosezione Mishima): 11/12 conformi, 1 discrepanza minore trovata e corretta.**

† **Nota sul conteggio totale:** il primo giro di audit riportava un totale di 121 carte per `Database_Guerriero.py` (109 verificate + 12 Mishima non verificate), ma questo numero era già impreciso alla fonte — il conteggio reale delle chiavi nel dizionario `GUERRIERI_DATABASE` (confermato anche dal numero di immagini in ciascuna cartella `image/<Fazione>/`) è **136**: Bauhaus 12, Capitol 12, Cybertronic 17, Imperiale 16, Mishima 12, Fratellanza 15, Oscura Legione 47, Mercenario 5. Il Mercenario (5 carte) è stato riverificato punto per punto in una sessione successiva: tutte e 5 conformi a livello di `stats`/`testo_carta`, con una discrepanza strutturale minore in "Medico Da Campo" (vedi §6), ora corretta.

---

## 1bis. Verifica di coerenza sui campi normalizzati (2026-08-01)

Dopo la sessione di correzione, l'utente ha segnalato che alcuni campi dei dizionari `effetti`/`modificatori` **non sono testo libero**: sono letti/confrontati con valori esatti dal motore di gioco (`source/cards/*.py`, metodi `applica_effetto`) e dal calcolo del punteggio di potenza (`source/logic/Creatore_Mazzo.py`), quindi devono usare un vocabolario coerente col resto del database. In particolare:
- `tipo_effetto` è confrontato con valori esatti case-sensitive (es. in `Speciale.py`: `"Modificatore"`, `"Scarto_Carte"`, `"Guarigione"`, ecc.; in `Arte.py`: `"Modificatore"`, `"Guarigione"`, `"Protezione"`, `"Controllo"`, `"Benedizione"`).
- `statistica`/`statistica_target` hanno convenzioni specifiche per modulo: singola lettera maiuscola `"C"/"S"/"A"/"V"` per `Fortificazione.modificatori`; parola minuscola singola (`"combattimento"`, `"sparare"`, `"armatura"`) o `"tutte"` per l'insieme completo, nei moduli `Speciale`/`Arte`/`Oscura_Simmetria`.
- `nome_effetto`, `condizioni`, `limitazioni` sono invece — verificato direttamente nel codice — **non consumati da nessun confronto a valore esatto** in `Creatore_Mazzo.py`/`Manager_Gioco.py`/`source/cards/*.py`: restano liberi/descrittivi (solo `descrizione_effetto` era già sicuramente libero).

Verificando a ritroso le correzioni della sessione precedente contro queste convenzioni, sono state trovate e corrette **5 incoerenze introdotte per errore**:

| File | Carta | Campo | Valore errato introdotto | Valore corretto (coerente con le convenzioni esistenti nel DB) |
|---|---|---|---|---|
| `Database_Fortificazione.py` | `"Trincea"` | `modificatori[].statistica` (x2 voci) | `"armatura"`, `"combattimento"` (parole intere — convenzione presa per errore da un altro modulo) | `"A"`, `"C"` (lettera singola maiuscola, unica convenzione riscontrata nel resto del file) |
| `Database_Speciale.py` | `"Supporto Tattico"` | `effetti[].statistica_target` | `"multiple: combattimento, sparare"` (prefisso `"multiple:"` inesistente in questo modulo, preso da `Fortificazione.py`) | `"combattimento e sparare"` (stesso formato di 4 voci pre-esistenti nel database con due statistiche) |
| `Database_Arte.py` | `"Volare"` | `effetti[].statistica_target` (voce aggiunta) | `"multiple: C, S, A, V"` | `"tutte"` (convenzione dominante per "tutte e 4 le statistiche", 3 occorrenze pre-esistenti) |
| `Database_Speciale.py` | `"Mancato Rifornimento"` | `effetti[].tipo_effetto` | `"Contro-effetto"` (valore inventato, non riconosciuto dal motore) | `"Scarto_Carte"` (valore già gestito da `Speciale.applica_effetto`, semanticamente coerente: la carta scarta l'Equipaggiamento appena giocato) |
| `Database_Arte.py` | `"Premonizione Di Attacco"` | `effetti[].tipo_effetto` | `"Contro-effetto"` (idem) | `"Controllo"` (unico valore tra quelli gestiti da `Arte.applica_effetto` semanticamente vicino ad "annullare un'Azione di Attacco"; il motore non ha ancora un branch dedicato a questo effetto specifico, ma almeno il valore è nel vocabolario riconosciuto) |

Tutte e 5 sono state corrette. Le altre correzioni della sessione precedente sono state riverificate e **non presentano lo stesso problema** (i campi `tipo_effetto`/`statistica` toccati altrove erano lasciati invariati o già coerenti con le convenzioni pre-esistenti).

**Verifica capitalizzazione/accenti (segnalazione utente):** nessuna delle rinomine di chiave applicate nella sessione precedente (`Agente Nick Michaels`, `Guardia Del Corpo`, `Medico Da Campo`, `Apostata Rinnegato`, `Pergamena D'Invocazione Sacrilega`) introduce vocali accentate — solo capitalizzazione e un apostrofo, già usato altrove nel database (es. `"Attestato D'Onore"`). Il lookup dei file immagine (`trova_file_case_insensitive`) è case-insensitive quindi le differenze di capitalizzazione non causano problemi; l'unico impatto reale era il disallineamento del nome-file per la Pergamena (risolto, vedi §7).

---

## 1ter. Audit esteso dei campi normalizzati (2026-08-01, seconda sessione)

Estensione della verifica §1bis a **tutte** le proprietà lette dalla logica di costruzione mazzo e dal motore di gioco, non solo `effetti`/`modificatori`. Metodo: per ogni campo si è prima cercato il codice consumatore (`source/cards/X.py`, `Creatore_Mazzo.calcola_potenza_*`, `seleziona_carte_supporto`) per stabilire il formato realmente atteso, poi si sono confrontate contro di esso **solo le carte effettivamente modificate** nel correction pass del 2026-07-31 (ricavate dal diff Git, non dall'elenco a memoria).

**Nota di scoping:** `Database_Equipaggiamento.py` e `Database_Warzone.py` risultano *non modificati* dal correction pass (nessuna voce nel diff), quindi i campi elencati per quei due moduli non avevano nulla da verificare.

### Difetti trovati e corretti (6)

| Gravità | File | Carta | Campo | Problema | Correzione applicata |
|---|---|---|---|---|---|
| 🔴 | `Database_Arte.py` | `"Velocita"` | `tipo` | `"Incantesimo Personale di combattimento"` (minuscola) non è un valore dell'enum `TipoArte` → `Arte.from_dict` solleva `ValueError` e `crea_carta_da_database` restituisce `None`: **la carta era di fatto sparita dal gioco**, silenziosamente (l'eccezione è catturata e stampata) | `"Incantesimo Personale di Combattimento"` |
| 🔴 | `Database_Fortificazione.py` | `"Trincea"` | `modificatori[].valore` | La correzione §1bis aveva sostituito `statistica: "multiple: A, C"` con due voci `"A"`/`"C"`, ma con `valore` **stringa** (`"+2"`, `"-2"`). `ModificatoreFortificazione.valore` è dichiarato `int` e viene sommato con `+=` in `get_modificatore_armatura`/`get_modificatori_statistiche` → **`TypeError`**. Finché `statistica` valeva `"multiple: A, C"` il confronto `== "A"` non scattava mai e il bug restava latente; separando le statistiche è diventato attivo. In più il `+2` in A risultava **contato due volte** (già presente in `bonus_armatura: 2`) | Un solo modificatore `{"statistica": "C", "valore": -2}` (int); il `+2` in A resta rappresentato da `bonus_armatura`, che è la convenzione dominante nel file (8 carte su 26 la usano da sola). Verificato: `get_modificatori_statistiche()` → `{'C': -2, 'S': 0, 'A': 2, 'V': 0}`, esattamente il testo della carta |
| 🟠 | `Database_Missione.py` | `"Portale Del Grande Conquistatore"` | `obiettivo.valore_richiesto` | Il campo era stato corretto da `2` a `3` interpretandolo come *soglia di Valore del bersaglio*, ma è documentato e usato come **quantità di bersagli** (`Missione.py:55`, e confrontato con `progresso_attuale >= valore_richiesto`). Con `3` la missione avrebbe richiesto 3 uccisioni invece di 1 | `valore_richiesto: 1` + `condizioni_speciali: ["Guerriero della Fratellanza con Valore 3 o più"]`, coerente con la convenzione di `"Quindici Minuti Di Fama"` (`val=1`, `cond=['Guerriero personalita nemico']`) |
| 🟠 | `Database_Guerriero.py` | `"Osservatore Tattico"` | `keywords` | Il `testo_carta` corretto dichiara `COMANDANTE (SERGENTE)` ma `keywords` era rimasto `[]`. `keywords` **è** consumato per valore esatto (`Equipaggiamento.py:246`, `Speciale.py:274-294`: `"Comandante" not in guerriero.keywords`) → le carte con restrizione "Solo Comandanti" non gli sarebbero mai state assegnabili | `keywords: ["Comandante"]`, come le altre 8 carte Comandante/Sergente del database |
| 🟡 | `Database_Guerriero.py` | `"Legionario Urlante"` | `abilita[].tipo` | Cambiato in `"Azioni"` per riflettere il costo in Azioni, ma il campo indica il **tipo di effetto**, non la valuta del costo: l'unica altra voce `"Azioni"` del database (`Maresciallo di Campo Johnstone`) è un'abilità che *converte* Azioni. Inoltre la coppia (`tipo`, `nome`) è letta a valore esatto in `Creatore_Mazzo._calcola_potenza_guerriero`: `"Azioni"` + `"Aumenta effetto"` non corrisponde a nulla, azzerando il bonus di potenza | Ripristinato `tipo: "Modificatore"` (coerente con `nome: "Aumenta effetto"`); restano corretti `descrizione` e `costo_destino: 0` (il costo è in Azioni, non in D) |
| 🟡 | `Database_Speciale.py` | `"Attestato D'Onore"` | `effetti[].statistica_target` | Il `valore` era stato corretto in `"+1 in C, S e A"` ma `statistica_target` era rimasto `"tutte"` (che significa tutte e quattro, V inclusa): record internamente contraddittorio | `"combattimento, sparare e armatura"`, formato già usato in `Database_Oscura_Simmetria.py` per insiemi parziali di statistiche |

### Campi verificati e risultati corretti (nessuna modifica necessaria)

- **`bersaglio` (Arte)** — `Arte.from_dict` lo converte con `BersaglioArte(...)`: `"Maestro"` **è** un valore valido dell'enum (`MAESTRO`) e ha già 12 occorrenze pre-esistenti; ricade nel ramo `else: return True` di `bersaglio_valido()`. Le modifiche a `"Colpire"` e `"Velocita"` sono corrette.
- **`fazioni_permesse`** — tutti i valori toccati (`"Oscura Legione"` per `"Ammaliatrice"`, la lista ridotta di `"Tessera Del Clan"`) sono stringhe valide dell'enum `Fazione`.
- **`tipo_attivazione` (Reliquia)** — `"Attivo"` per `"Pergamena D'Invocazione Sacrilega"` è nel vocabolario documentato (`"Passivo"/"Attivo"/"Reazione"/"Combattimento"`) e cambia correttamente il comportamento dei rami `== "Passivo"` in `Reliquia.py:398,493`.
- **`statistica_target: "equipaggiamento"` (`"Sabotaggio"`)** — non è un'invenzione: il valore era già presente 4 volte nel modulo prima della modifica.
- **`statistica_target: ""` (`"Premonizione Di Attacco"`)** — la stringa vuota è la convenzione dominante in `Database_Arte.py` per gli effetti senza statistica bersaglio (36 occorrenze contro 4 di `"nessuna"`).
- **`condizione: "sempre"` (`"Trincea"`)** — è esattamente il valore riconosciuto da `Fortificazione._verifica_condizione`.
- **`restrizioni` (Guerriero)** — nessun consumatore a valore esatto nel codice, ma è un vocabolario di fatto nei dati: le due stringhe usate per `"Il Diciannovesimo Executive"` (`"Non può prendere parte al combattimento"`, `"Non può andare in copertura"`) sono già presenti rispettivamente 8 e 12 volte.
- **Rinomine di chiave** — nessun riferimento hardcoded ai vecchi nomi in tutto il codice; tutte e 5 le immagini corrispondenti si risolvono correttamente via `trova_file_case_insensitive`.
- **Deduplicazione `Database_Speciale.py`** — tutte e 7 le chiavi coinvolte esistono ancora e puntano alla versione corretta (set di espansione atteso).

### Verifica finale

Istanziazione di **tutte** le carte di tutti e 9 i moduli tramite i rispettivi `from_dict`: **561/561 riuscite, 0 fallimenti** (Arte 66, Speciale 180, Oscura Simmetria 35, Fortificazione 26, Reliquia 18, Missione 7, Equipaggiamento 79, Warzone 14, Guerriero 136). Prima delle correzioni di questa sessione il totale era 560/561.

### Difetti pre-esistenti emersi durante l'audit (NON introdotti dal correction pass, non corretti)

Vanno annotati perché scoperti con lo stesso metodo, ma sono fuori dallo scope "correggere ciò che ho modificato io":

1. ~~**`"Luna"`**~~ — **corretto, vedi §1quater.**
2. ~~**`STATISTICHE_MODIFICATORI`**~~ — **corretto, vedi §1quinquies.**
2bis. ~~**Vocabolario e tipi degli `effetti`**~~ — **risolto il 2026-08-02.** Il problema era che `_calcola_potenza_carta_stats` contava un effetto solo con `valore` intero positivo e `statistica_target` fra sei valori esatti, mentre nei database `valore` è stringa in 67 casi su 187 (Speciale), 38 su 67 (Arte) e 35 su 35 (Oscura Simmetria); e che `_calcola_potenza_carta_azioni` cercava valori di `tipo_effetto` inesistenti. **La scelta è stata rendere tollerante il codice, non normalizzare i dati**, perché `tipo_effetto` e `statistica_target` sono consumati da `applica_effetto` nel motore di gioco: modificarli lì avrebbe rotto quel consumatore. Dettaglio in `ANALISI_LOGICA_COLLEZIONI_MAZZI.md` §18. Restava però un vero difetto **di dati**, individuato e corretto separatamente: le cinque carte di §8bis.
3. **`"Sabotaggio"` (`Database_Speciale.py`)** — ha `tipo_effetto: "Modificatore"` ma è semanticamente uno scarto di carte; la carta gemella `"Mancato Rifornimento"` usa correttamente `"Scarto_Carte"`. Da uniformare (valore pre-esistente, non toccato dal correction pass).
4. **`"Osservatore Tattico"` (`Database_Guerriero.py`)** — a differenza di `"Jito"` e `"Sergente"` gli manca la seconda abilità `{"nome": "Aumenta caratteristica", "tipo": "Modificatore"}` che rappresenta il `+4` conferito al guerriero assegnato. È un'omissione di dati, non un errore di formato.
5. **`"Aiuto Di Campo"` (`Database_Guerriero.py`)** — stesso problema di keywords dell'Osservatore Tattico: testo `COMANDANTE (SERGENTE)` ma `keywords: []`.
6. **`"Il Diciannovesimo Executive"`** — la riscrittura del `testo_carta` sulla base della scansione ha fatto perdere la restrizione `"Carte delle Arti non Assegnabili"` (sostituita dalle due restrizioni di combattimento/copertura). Se la scansione è corretta va bene così, ma vale un secondo sguardo dato che le altre Personalità Cybertronic la mantengono.

---

## 1quater. `"Luna"` e il conflitto di tipo su `modificatori[].valore` (2026-08-01)

Correggendo `"Luna"` è emerso che i **due** consumatori di `ModificatoreFortificazione.valore` pretendono tipi incompatibili:

| Consumatore | Riga | Operazione | Tipo richiesto |
|---|---|---|---|
| `Fortificazione.get_modificatore_armatura` / `get_modificatori_statistiche` | `Fortificazione.py:272,291` | `mod_totale += mod.valore` | **`int`** |
| `Creatore_Mazzo.calcola_potenza_fortificazione` | `Creatore_Mazzo.py:409` | `modificatore.valore.lower()` | **`str`** |

Nessun valore nel database poteva soddisfare entrambi: con `"+2"` (stringa) il motore di gioco sollevava `TypeError`, con `2` (int) il calcolo di potenza sollevava `AttributeError`. La dataclass dichiara `valore: int` e il motore di gioco è il consumatore semanticamente autorevole (deve sommare), mentre la riga di `Creatore_Mazzo.py` è chiaramente un copia-incolla da `calcola_potenza_equipaggiamento`, dove `valore` **è** legittimamente una stringa (può valere `"raddoppiate"`, `"uguale alla più elevata"`, `"x3"`).

**Risolto così:**
- `Database_Fortificazione.py` usa `int` per `modificatori[].valore` (`"Trincea"` → `-2`, `"Luna"` → `1`);
- `Creatore_Mazzo.py:409` diventa `str(modificatore.valore).lower()`, tollerante a entrambi i tipi, così la funzione resta valida anche per gli altri moduli.

**Valore di `"Luna"`.** La carta recita: *"tutti i tuoi guerrieri guadagnano un +1 in A; tutti i tuoi Mercenari guadagnano +2 in A"*. Il motore calcola `A = bonus_armatura + Σ(modificatori applicabili)`; con `bonus_armatura: 1` già a rappresentare il `+1` universale, il modificatore riservato ai Mercenari deve valere **`1`** (il delta), non `2`, altrimenti un Mercenario otterrebbe `+3`. La `descrizione` è stata esplicitata per evitare che qualcuno "ricorregga" il valore a 2 leggendo solo il testo della carta.

**`STATISTICHE_MODIFICATORI`:** l'avvertenza originariamente riportata qui è stata affrontata come intervento a sé — vedi **§1quinquies**.

**Limite del motore, non dei dati:** `Fortificazione._verifica_condizione` riconosce solo `"sempre"`, `"in_combattimento"` e `"non_in_veicolo"`, e per qualsiasi altra stringa ricade su `else: return True`. La condizione `"Uso ristretto: Mercenari"` di `"Luna"` quindi **non filtra nulla**: allo stato attuale il bonus viene applicato a ogni guerriero, non solo ai Mercenari. Il dato è corretto, manca l'implementazione del controllo (che richiede l'accesso al guerriero, oggi passato solo come `guerriero_id`).

---

## 1quinquies. Riattivazione di `STATISTICHE_MODIFICATORI` (2026-08-01)

Intervento a sé stante su `source/logic/Creatore_Mazzo.py`, eseguito con un confronto dei punteggi prima/dopo su tutte le 137 carte delle quattro categorie coinvolte.

### Il difetto

```python
STATISTICHE_MODIFICATORI = [["sparare", "combattimento", "armatura", "S", "A", "C", "multiple:"]]
```

Le parentesi esterne creano una lista con **un solo elemento**, a sua volta una lista. Il test usato in quattro punti — `if statistica in STATISTICHE_MODIFICATORI:` — confronta quindi una stringa con una lista e **non è mai vero**. I quattro blocchi interessati (`calcola_potenza_equipaggiamento`, `calcola_potenza_fortificazione`, `calcola_potenza_reliquia`, `calcola_potenza_warzone`) non venivano mai eseguiti: i modificatori di caratteristica non contribuivano al punteggio di potenza di nessuna di quelle carte.

### Perché non bastava togliere le parentesi

Riattivando il guard così com'era sarebbero emersi tre problemi già latenti:

1. **Confronto maiuscole/minuscole.** Il codice fa `statistica.lower()`, ma la lista conteneva `"S"`, `"A"`, `"C"` maiuscole: Fortificazione, Reliquia e Warzone — che usano proprio la convenzione a lettera singola — avrebbero continuato a non matchare. Solo Equipaggiamento (parole intere minuscole) si sarebbe riattivato.
2. **`"multiple:"` come elemento di lista.** Non può funzionare con un test di appartenenza: i valori reali sono `"multiple: S, A, V"`, serve un confronto per prefisso.
3. **Tipi e segni dei valori.** I confronti erano scritti per stringhe col segno (`"+3"`, `"+5"`…). Warzone (`int`) avrebbe sollevato `TypeError: argument of type 'int' is not iterable`, Fortificazione (`int`) `AttributeError` su `.lower()`, e una penalità come il `-2` in C della Trincea non doveva comunque aumentare la potenza. Inoltre `"+12"` non corrispondeva a nessuna soglia (nessuna sottostringa fra `"+5"` e `"+9"`) e finiva in fascia zero.

### Cosa è stato fatto

- `STATISTICHE_MODIFICATORI` è ora una lista piatta di token **minuscoli** (`["sparare", "combattimento", "armatura", "s", "a", "c"]`). Come nell'originale, `V`/`valore` resta escluso: è una statistica di costo, non di combattimento.
- Tre funzioni di modulo incapsulano le regole, prima ripetute (e divergenti) nei quattro blocchi:
  - `statistica_di_combattimento()` — appartenenza alla lista **oppure** prefisso `"multiple:"`;
  - `valore_numerico_modificatore()` — estrae l'intero da `int` o da stringa (`"+4"`, `"+1 ulteriore"`), `None` per i valori non numerici;
  - `livello_bonus_modificatore()` — classifica in tre fasce **su base numerica** conservando le soglie originali (≥5 o valore speciale → grande, 3–4 → media, 1–2 → piccola), e restituisce 0 per valori nulli o negativi;
  - `modificatore_utilizzabile()` — la regola `"uso ristretto:"` / `"incrementa con costo:"`, prima duplicata otto volte.
- Il metodo `CreatoreMazzo._applica_bonus_modificatore()` accorpa la scelta fra moltiplicatore (`×1.1/1.2/1.3`) e addendo (`+1/+2/+4`), identica nei tre blocchi a fasce.
- Nel blocco Reliquia — che ha una logica propria, additiva invece che a fasce — è stato corretto un `break` che usciva dal ciclo subito dopo aver impostato `valore = 10` per i valori speciali (`"raddoppiate"`, `"x3"`, `"uguale alla più elevata"`), impedendo così sia di sommarli sia di esaminare i modificatori successivi. Ora il `+10` viene effettivamente sommato e il ciclo prosegue.
- **Ramo `+1`/`+2`:** l'originale lo verificava su `descrizione` invece che su `valore` (verosimilmente un refuso, dato che gli altri due rami usano `valore`); ora tutte e tre le fasce leggono `valore`.

### Impatto misurato

Confronto automatico prima/dopo su tutte le carte: **23 punteggi su 137 sono cambiati, 0 errori**.

| Categoria | Carte | Punteggi cambiati | Esempi |
|---|---|---|---|
| Equipaggiamento | 79 | 10 | `Fukimura No.12 Kamikaze` 1.0 → 7.5; `Death Angel` 13.0 → 16.9 |
| Fortificazione | 26 | 0 | `Trincea` invariata (il `-2` è una penalità → fascia 0), `Luna` invariata (`"Uso ristretto:"` → esclusa) |
| Reliquia | 18 | 8 | `Frammento Del Vero Chip` 1.0 → 31.0 (4 statistiche `"uguale alla più elevata"`, di cui 3 rilevanti × +10) |
| Warzone | 14 | 5 | `Asteroide Infestato` 16.0 → 35.152 (tre modificatori da +5: `16 × 1.3³`) |

Tutte e 561 le carte continuano a istanziarsi correttamente e il calcolo di potenza gira senza errori anche sulle categorie non toccate (Speciale 180, Arte 66, Oscura Simmetria 35, Guerriero 136).

### Documento collegato

L'analisi della logica di selezione che consuma questi punteggi — e che ha reso evidente il problema — è in **`ANALISI_LOGICA_COLLEZIONI_MAZZI.md`** (seconda stesura, 2026-08-01). In particolare la §6 di quel documento riporta le scale di punteggio misurate per tutti e otto i tipi di carta, e la §10 elenca 8 difetti nuovi nei criteri di scelta, indipendenti dai dati.

### Da valutare in seguito

- **Scale non omogenee fra categorie.** Il blocco Reliquia somma i valori grezzi (fino a 31) mentre gli altri usano fasce moltiplicative (Equipaggiamento arriva a ~17). Era già così nel disegno originale, ma ora che il codice è vivo la differenza si vede: se i punteggi delle diverse categorie vengono confrontati fra loro nella selezione delle carte, la scala andrebbe uniformata.
- **`"ristretto:"` contro `"uso ristretto:"`.** Il blocco Reliquia esclude i modificatori la cui condizione contiene `"ristretto:"`, gli altri tre cercano `"uso ristretto:"`. Di conseguenza condizioni realmente restrittive ma formulate diversamente (es. `"Per Legionari non morti, Urlanti, Benedetti..."` del `"Globo Dei Servi Minori"`) vengono conteggiate a pieno valore.
- **Modificatori "dell'avversario".** `"combattimento dell'avversario"` e `"valore dell'avversario"` (Equipaggiamento) non corrispondono ad alcun token e restano esclusi, come nell'intento originale, benché siano potenziamenti effettivi.

---

## 2. Anomalie strutturali trasversali (chiavi duplicate)

**Problema:** in Python, quando una chiave stringa compare più volte in un dict-literal, l'ultima occorrenza sovrascrive silenziosamente le precedenti senza generare errori. Sono state trovate diverse chiavi duplicate in `Database_Speciale.py`. **Non è stato eseguito un censimento esaustivo di tutto il file** (né degli altri 8 moduli) — i casi sotto sono solo quelli incontrati incidentalmente durante l'audit.

Comando suggerito per un censimento completo in una sessione futura:
```bash
grep -oP '^\s{4}"\K[^"]+(?="\s*:\s*\{)' source/data_base_cards/Database_Speciale.py | sort | uniq -d
```

### Casi risolti in questa sessione ✅

| Chiave | Righe duplicate (ai tempi dell'audit) | Azione applicata |
|---|---|---|
| **Imboscata** | 1815, 5008 | ✅ Rimossa la voce a riga 5008 (descriveva una carta diversa, "Attacco Automatico" su Guerriero Avversario, non corrispondente all'immagine reale). Mantenuta la voce corretta ("Combattimento Non Simultaneo" su Guerriero Proprio, set Base). |
| **Azione Evasiva** | 686, 1885 | ✅ Rimossa la voce a riga 686 (contenuto meccanicamente equivalente, solo pulizia strutturale). Mantenuta la versione attiva a runtime. |
| **Colpo Fortunato** | 336, 2305 | ✅ Rimossa la voce a riga 336 (contenuto meccanicamente equivalente, solo pulizia strutturale). Mantenuta la versione attiva a runtime. |

### Altri casi risolti in sessione successiva ✅ (2026-08-01, dopo verifica diretta dell'utente)

| Chiave | Righe duplicate (ai tempi dell'audit) | Azione applicata |
|---|---|---|
| **Nascosto Nell'Ombra** | 512, 1108 (entrambe set Base — non è una divergenza Base/Inquisition) | ✅ Confermato dall'utente che `durata: "Fino Prossimo Turno"` (versione attiva, riga 1108) è coerente col testo carta ("deve essere scartata alla prossima Fase Pescare" = il turno successivo) — **nessuna modifica al contenuto**. Rimossa solo la voce duplicata a riga 512 (`durata`/`bersaglio`/`valore` leggermente diversi, versione non attiva a runtime). |
| **Empatia Cinetica** | 547 (Base), 3916 (Inquisition) | ✅ Confermato dall'utente: la carta esiste solo nell'espansione Inquisition, non nel set Base. Rimossa la voce Base (547); mantenuta la voce Inquisition (già quella attiva a runtime). |
| **Essenza Di Integrita** | 2202 (Base), 3741 (Inquisition) | ✅ Come sopra: rimossa la voce Base, mantenuta l'Inquisition (già attiva a runtime). |
| **Essenza Di Rettitudine** | 828 (Base), 3425 (Inquisition) | ✅ Come sopra: rimossa la voce Base, mantenuta l'Inquisition (già attiva a runtime). |

### Casi ancora NON risolti ⏳ — richiedono verifica

Nessuno rimasto per questo file specifico (i 4 casi sopra erano gli unici duplicati individuati nell'audit originale). Resta comunque valido il punto generale: **non è stato eseguito un censimento esaustivo** delle chiavi duplicate, né in `Database_Speciale.py` né negli altri 8 moduli (vedi comando grep suggerito sopra).

---

## 3. Database_Warzone.py

| # | Carta (chiave) | Priorità | Stato | Nota |
|---|---|---|---|---|
| 1 | ~~`"Citadella Sanctum"`~~ | — | ❌ **FINDING RITIRATO (2026-08-01)** | L'audit originale interpretava erroneamente `stats.valore: 2` come il campo che avrebbe dovuto rappresentare il moltiplicatore ×2 dei punti V. In realtà **il moltiplicatore è già correttamente descritto** in `effetti_combattimento[1]` (`"nome": "Aumenta Punti Vittoria"`, `"descrizione": "...guadagnano il doppio dei punti V dell'avversario"`) — un campo completamente separato da `stats.valore`, che rappresenta invece il normale valore V della Warzone stessa (nulla a che vedere col moltiplicatore). **Nessuna correzione necessaria**: la carta è già rappresentata correttamente. |

Nessun'altra discrepanza tra le 14 carte Warzone. Nota: il campo `rarity` è "Common" per tutte le 14 carte nel DB, e nessuna icona di rarità è risultata leggibile sulle scansioni — non correggibile con l'audit visivo disponibile, considerare NON VERIFICABILE.

---

## 4. Database_Fortificazione.py

| # | Carta (chiave) | Priorità | Stato | Nota |
|---|---|---|---|---|
| 1 | `"Trincea"` | 🔴 CRITICA | ✅ **APPLICATA** | Corretto il doppio bonus "+2 in A, e un +2 in C" nel compromesso difensivo reale "+2 in A, e un **-2 in C**". Il campo `modificatori` è stato riorganizzato in due voci separate (una per `armatura`, una per `combattimento`) per rappresentare i due valori distinti. |

Nessun'altra discrepanza tra le 26 carte Fortificazione.

---

## 5. Database_Missione.py

| # | Carta (chiave) | Priorità | Stato | Nota |
|---|---|---|---|---|
| 1 | `"Lotta Fraticida"` | 🟠 MEDIA | ✅ **APPLICATA** | "guerriero imperiale" → **"Doomtrooper Imperiale"** in `obiettivo.descrizione`, `condizioni_speciali` e `testo_carta`. |
| 2 | `"Portale Del Grande Conquistatore"` | 🔴 CRITICA | ✅ **APPLICATA** | Riscritta la condizione da "V tre volte più grande" (moltiplicatore) a **"Valore di 3 o più"** (soglia assoluta) in `obiettivo.descrizione` e `testo_carta`; aggiornato anche `valore_richiesto` da 2 a 3 per coerenza interna. Corretti anche i refusi "cme"→"come", "deel"→"del", "frtellanza"→"Fratellanza" nello stesso testo (incidentali, non esplicitamente elencati nell'audit originale ma nella stessa frase corretta). |

**Refusi minori applicati ✅:** "Assedio Alla Cittadella" — "Citadella"→"Cittadella", "ounti"→"punti" in `obiettivo.descrizione` e `testo_carta`.

**Non applicato ⏳:** "Cospirazione Eretica" ("competare") — l'audit originale specifica esplicitamente che è un refuso della carta fisica originale, da non correggere nel DB. Il `flavour_text` di diverse Missioni sembra inventato/non genuino — lasciato invariato, la decisione se rimuoverlo è di design/contenuto, non una correzione di fedeltà.

---

## 6. Database_Guerriero.py

### Capitol

| # | Carta (chiave) | Priorità | Stato | Nota |
|---|---|---|---|---|
| 1 | `"Sunset Striker"` | 🔴 CRITICA | ✅ **APPLICATA** | `stats.combattimento` 0 → 3 (C=S=A=V=3). |

### Cybertronic

| # | Carta (chiave) | Priorità | Stato | Nota |
|---|---|---|---|---|
| 2 | `"Charles Sykes"` | 🟠 MEDIA | ✅ **APPLICATA** | Bonus concesso "+4" → **"+3"** in `abilita[1].descrizione` e `testo_carta`; sistemato il refuso grammaticale "finché Charles stesso finché lui è presente" → "(non Charles stesso) finché lui è presente". |
| 3 | `"Il Diciannovesimo Executive"` | 🔴 CRITICA | ✅ **APPLICATA** | `testo_carta` sostituito con il testo reale ("LEADER CORPORATIVO. Non può mai prendere parte al combattimento né andare in copertura...", sul modello della voce gemella "Maresciallo di Campo Johnstone"); `restrizioni` aggiornate di conseguenza. |
| 4 | `"Osservatore Tattico"` | 🔴 CRITICA | ✅ **APPLICATA** | `testo_carta` sostituito (era testo copiato da "Tecnico Vac"); l'array `abilita` era già corretto. |
| 5 | `"Mercenario Ex-Cybertronic"` | 🟠 MEDIA | ✅ **APPLICATA** | "1D" → **"3D"** in `testo_carta`, coerente con gli altri "Mercenario Ex-X". |

### Imperiale — pattern sistematico di valori C/S/A/V permutati

Tutte e 8 le correzioni applicate ✅:

| # | Carta (chiave) | Priorità | Valori DB prima | Valori corretti applicati (C/S/A/V) |
|---|---|---|---|---|
| 6 | `"Blood Beret"` | 🔴 CRITICA | 4/3/4/4 | 4/4/3/4 |
| 7 | `"Comandante di Reparto"` | 🔴 CRITICA | 5/3/7/7 | 7/3/5/6 |
| 8 | `"Comandante in Capo"` | 🔴 CRITICA | 6/7/5/9 | 9/5/7/9 |
| 9 | `"Farabutto"` | 🔴 CRITICA | 4/4/3/5 | 5/3/4/4 |
| 10 | `"Guardia Inesperta"` | 🟠 MEDIA | 2/2/2/3 | 2/2/3/2 |
| 11 | `"Membro del Clan"` | 🟠 MEDIA | 3/2/4/4 | 4/2/3/3 |
| 12 | `"Sean Gallagher"` | 🔴 CRITICA | 8/0/8/10 | 10/3/8/8 |
| 13 | `"Sgt McBride"` | 🟡 BASSA | 5/5/5/5 | 5/5/4/5 |

### Oscura Legione

| # | Carta (chiave) | Priorità | Stato | Nota |
|---|---|---|---|---|
| 14 | `"Necromagus Supremo"` | 🔴 CRITICA | ✅ **APPLICATA (2026-08-01)** | `stats` C22/S14/A26/V20 (copiati per errore da "Bio Gigante") → **C4/S4/A5/V5**, confermati dall'utente dopo revisione diretta della carta. Il resto della voce (testo, keywords, abilità) era già conforme. |
| 15 | `"Legionario Non Morto"` | 🟠 MEDIA | ✅ **APPLICATA** | `testo_carta` auto-riferimento corretto: "Legionari Urlanti" → "Legionari non Morti". |
| 16 | `"Eaonian Justifier"` | 🔴 CRITICA | ✅ **APPLICATA** | Logica invertita corretta: "viene ucciso da" → "ferisce (non uccide)". |
| 17 | `"Cacciatore Oscuro"` | 🟠 MEDIA | ✅ **APPLICATA** | Penalità "-1 in A" → **"-3 in A"** in `testo_carta` e `abilita`. |
| 18 | `"Legionario Urlante"` | 🔴 CRITICA | ✅ **APPLICATA** | Costo "5D" → **"3 Azioni"** in `testo_carta` e `abilita[0]` (tipo di costo cambiato da Punti Destino ad Azioni; `costo_destino` impostato a 0, `tipo` ad "Azioni"). |

### Refusi minori — Oscura Legione e Mercenario, tutti applicati ✅

Prefisso di categoria aggiunto nel `testo_carta` (determinato dal campo `keywords` di ciascuna carta): Necromutante ("SEGUACE DI ALGEROTH." + typo "nn Morti"→"non Morti"), Billy ("PERSONALITA."), Centurion ("SEGUACE DI ALGEROTH."), Pretorian Stalker ("SEGUACE DI ALGEROTH."), Tutore ("SEGUACE DI DEMNOGONIS." + typo "laLame"→"Lame"), Legionario Benedetto ("SEGUACE DI DEMNOGONIS."), Figlio di Ilian ("SEGUACE DI ILIAN."), Templare ("SEGUACE DI ILIAN."), Intruso Callistoniano ("SEGUACE DI SEMAI."), Legionario di Semai ("SEGUACE DI SEMAI."), Nefarita di Semai ("SEGUACE DI SEMAI.").

Altri refusi isolati corretti: Eretico ("man"→"ma"), Karnofago ("Nefaria"→"Nefarita"), Valpurgius (target "ALgeroth"→"Algeroth"), Pipistrello da Ricognizione (frammento "1 x ." → "Es."), Apostata Rinnegato (aggiunta la parola mancante "Tienilo").

**Correzione di attribuzione:** l'audit originale segnalava il typo "Nepharita"→"Nefarita" sulla carta "Nefarita di Semai", ma il typo si trova in realtà su **"Nefarita di Demnogonis"** (2 occorrenze, in `abilita[1].descrizione` e `testo_carta`) — corretto lì. "Nefarita di Semai" non conteneva il typo ma mancava comunque il prefisso "SEGUACE DI SEMAI.", ora aggiunto.

Capitalizzazione chiavi Mercenario uniformata ✅: `"Agente nick michaels"` → `"Agente Nick Michaels"`; `"Guardia del corpo"` → `"Guardia Del Corpo"`; `"Medico da campo"` → `"Medico Da Campo"`; `"Apostata rinnegato"` → `"Apostata Rinnegato"`. (Verificato che nessun altro modulo del codice referenzia queste chiavi con la vecchia capitalizzazione.)

Fratellanza (15/15) e Bauhaus (12/12): nessuna discrepanza, nessuna azione richiesta.

### Mishima

| # | Carta (chiave) | Priorità | Stato | Nota |
|---|---|---|---|---|
| 19 | `"Mentore"` | 🟡 BASSA | ✅ **APPLICATA** | `stats.valore` 2 → **3** (la carta stampa C=S=A=V=3, tutti uguali). |

Le altre 11 carte Mishima (Samurai, Mercenario Ex-Mishima, Artefatto Di Combattimento, Tatsu, Artefatto Suicida, Hatamoto, Ninja, Jito, Bushi, Shugo, Lord Nozaki) sono conformi: nessuna discrepanza tra `stats`/`testo_carta` e le scansioni reali.

### Mercenario (5/5 verificate)

| # | Carta (chiave) | Priorità | Stato | Nota |
|---|---|---|---|---|
| 20 | `"Medico Da Campo"` | 🟠 MEDIA | ✅ **APPLICATA** | Rimossa la voce fantasma `abilita[0]` ("Guarisce se stesso." / "Se ferito, .", frase troncata) che descriveva un potere di auto-guarigione assente sulla carta reale. Resta valida solo la voce "Guarisce guerriero ferito". |

`stats` e `testo_carta` di tutte e 5 le carte Mercenario corrispondono esattamente alle scansioni.

---

## 7. Database_Reliquia.py

| # | Carta (chiave) | Priorità | Stato | Nota |
|---|---|---|---|---|
| 1 | `"Armatura Del Vero Assassino"` | 🟡 BASSA | ✅ **APPLICATA** | "ICONA DI LEGAMO" → "ICONA DI LEGAME" in `testo_carta`. Corretto incidentalmente anche "MORTIFICATOR" → "MORTIFICATORE" (typo adiacente nella stessa frase, già corretto nel campo gemello `poteri[0].descrizione`). |
| 2 | `"Pergamena Di Evocazione Sacrilega"` | 🔴 CRITICA | ✅ **APPLICATA** | Chiave e `nome` rinominati in **"Pergamena D'Invocazione Sacrilega"**; aggiunto il costo di attivazione mancante "al costo di tre Azioni" in `poteri[0].descrizione` e `testo_carta` (e `tipo_attivazione` corretto da "Passivo" ad "Attivo" di conseguenza); corretto "tuo scheramento" → "Tuo Schieramento". Verificato che nessun altro modulo referenzia la vecchia chiave. **Nota (2026-08-01):** la rinomina aveva disallineato il nome del file immagine corrispondente (la funzione `ottieni_nome_file_immagine` genera il nome file dal nome carta, e il matching è case-insensitive ma non tollera parole diverse) — rinominato di conseguenza `image/Reliquie/Pergamena_Di_Evocazione_Sacrilega.jpg` → `Pergamena_D'Invocazione_Sacrilega.jpg` per ripristinare la corrispondenza. |

**Non applicato ⏳:** "Armatura Di Empieta" — differenza di sola accentazione rispetto a "EMPIETÀ" sulla carta; l'audit la definisce esplicitamente opzionale ("valutare se armonizzare, impatta solo leggibilità").

---

## 8. Database_Oscura_Simmetria.py

| # | Carta (chiave) | Priorità | Stato | Nota |
|---|---|---|---|---|
| 1 | `"Occhio Sacrilego"` | 🔴 CRITICA | ✅ **APPLICATA** | `testo_carta` ed `effetti[0].descrizione_effetto` sostituiti con il testo reale, incondizionato ("Gli avversari dell'Eretico sono accecati e in combattimento non possono rispondere. L'Eretico colpisce sempre per primo..."), al posto del testo condizionato copiato per errore da "Occhio Malvagio" (voce gemella, non toccata: il suo testo era già corretto). Aggiornati anche `limitazioni` ed `effetti_collaterali` per coerenza con il nuovo effetto. |
| 2 | `"Terrore"`, `"Resistere Al Dolore"`, `"Deformazione"`, `"Indigestione"`, `"Untore"` | 🔴 CRITICA | ✅ **APPLICATA (2026-08-02)** | `effetti[0].statistica_target` corretto da `"azioni"` ad `"armatura"` — vedi §8bis |
| 3 | `"Untore"` | 🟠 MEDIA | ✅ **APPLICATA (2026-08-02)** | `bersaglio` corretto da `"Doomtrooper"` a `"Guerriero Avversario"` — vedi §8bis |

**Non applicato ⏳ (per scelta esplicita, non serve verifica):** differenze di sola accentazione ("Cecita"/"CECITÀ", "Autorita"/"AUTORITÀ") — scelta deliberata per compatibilità ASCII delle chiavi Python. "Il Potere Della Percezione" — il DB è già corretto ("Ilian"), non va toccato.

---

## 8bis. Cinque carte con `statistica_target` errato (2026-08-02)

### Il difetto

Cinque carte di `Database_Oscura_Simmetria.py` dichiarano `effetti[0].statistica_target = "azioni"`, ma il testo della carta parla esplicitamente di **A (Armatura)** e non menziona in alcun modo le azioni:

| Carta | `valore` | Testo della carta | `statistica_target` |
|---|---|---|---|
| `"Terrore"` | `-1` | "Gli avversari di questo guerriero sono paralizzati dal Terrore… **−1 in A**" | ~~`azioni`~~ → **`armatura`** |
| `"Resistere Al Dolore"` | `+1` | "Il guerriero guadagna un **+1 in A**" | ~~`azioni`~~ → **`armatura`** |
| `"Deformazione"` | `-2` | "Tutti i guerrieri che combattono contro il possessore di questo Dono… **−2 in A**" | ~~`azioni`~~ → **`armatura`** |
| `"Indigestione"` | `-2` | "Tutti gli avversari di questo guerriero subiscono una penalità un **−2 in A**" | ~~`azioni`~~ → **`armatura`** |
| `"Untore"` | `-2` | "I Segnalini danno un **−2 in A**" | ~~`azioni`~~ → **`armatura`** |

Il controllo è stato esteso a tutte le carte con `statistica_target = "azioni"` nei tre database che usano il campo (Speciale, Arte, Oscura Simmetria): **tutte le altre parlano davvero di azioni**. Il difetto è circoscritto a queste cinque.

### Perché è 🔴 critica e non solo un problema di punteggio

`Oscura_Simmetria._applica_singolo_effetto` (riga 450) passa `statistica_target` a `Guerriero.applica_modificatore`, che filtra così:

```python
statistiche_valide = ['combattimento', 'sparare', 'armatura', 'valore']
if stat in statistiche_valide:
    ...
```

Ogni altro valore viene **ignorato senza segnalazione**. Su queste cinque carte il modificatore non aveva quindi alcun effetto **nel motore di gioco**, non solo nel calcolo di potenza: cinque Doni dell'Oscura Simmetria erano di fatto inerti.

### Correzione collegata su `"Untore"`

Il campo `bersaglio` dichiarava la **fazione** colpita (`"Doomtrooper"`) invece della relazione con chi gioca la carta. Il testo — *"Ogni Doomtrooper che combatte questo guerriero è infetto"* — indica che il Dono si assegna a un proprio guerriero dell'Oscura Legione e colpisce gli avversari. Corretto in `"Guerriero Avversario"`, valore già usato da 14 carte dello stesso database e previsto dall'enum `BersaglioOscura`.

Serviva perché il calcolo di potenza inverte il segno dei modificatori sulle carte rivolte all'avversario (una penalità inflitta all'avversario è un vantaggio): senza la normalizzazione, `"Untore"` restava fuori da quel riconoscimento. Vedi `ANALISI_LOGICA_COLLEZIONI_MAZZI.md` §19 e §20.

### Verifica

Dopo la correzione, nessuna carta con `statistica_target = "azioni"` ha più un testo che cita `A`. Le 35 carte del database continuano a istanziarsi correttamente; i punteggi di `Terrore`, `Deformazione`, `Indigestione` e `Untore` passano dal minimo a valori proporzionati alla penalità inflitta all'avversario, e `Resistere Al Dolore` viene ora conteggiata come il bonus in Armatura che è.

---

## 9. Database_Arte.py

Tutte le 8 correzioni certe applicate ✅:

| # | Carta (chiave) | Priorità | Nota sulla correzione applicata |
|---|---|---|---|
| 1 | `"Colpire"` | 🟠 MEDIA | `tipo` → "Incantesimo Personale di Combattimento"; `bersaglio` → "Maestro"; testo aggiornato da "il guerriero" a "il Maestro". |
| 2 | `"Evocare Eroe"` | 🟠 MEDIA | "Spendendo 5D" → "Spendendo 2D" (coerente con `effetti.valore`); aggiunta la frase "Puoi evocare un solo guerriero." |
| 3 | `"Evocare Guerriero"` | 🟠 MEDIA | "5D" → "2D" in `testo_carta` ed `effetti`; aggiunta "Puoi evocare un solo guerriero." |
| 4 | `"Evocare Difesa"` | 🔴 CRITICA | Riscritto l'effetto: recupero/rigioco immediato di una Fortificazione dagli scarti, non più assegnazione condizionata a un guerriero. |
| 5 | `"Fantasma"` | 🟠 MEDIA | `tipo` → "Incantesimo di Combattimento Personale"; costo "4D e due Azioni" → solo **"4D"**; `richiede_azione` True → False. |
| 6 | `"Premonizione Di Attacco"` | 🔴 CRITICA (la più grave del modulo) | Effetto interamente riscritto: annulla un Attacco al costo di 6D prima che abbia inizio (anche contro avversari Immuni all'Arte), al posto del bonus "+1 in A per ogni D speso" copiato erroneamente da un'altra carta. |
| 7 | `"Velocita"` | 🟠 MEDIA | `tipo` → "Incantesimo Personale di combattimento"; `bersaglio` → "Maestro"; aggiunta la clausola mancante sul controllo del risultato per l'avversario dopo che entrambi i giocatori hanno giocato le carte di modifica al combattimento. |
| 8 | `"Volare"` | 🟠 MEDIA | Aggiunta la seconda parte mancante dell'effetto: "Se il Maestro attacca, guadagna un +2 in C, S, A e V" (sia in `testo_carta` sia come nuova voce in `effetti`). |

**Non applicate ⏳ (voci ⚪ da verificare, confidenza media):**
- `"Conoscere La Verita"` — possibile "Ti"/"Vi" da rileggere ad alta risoluzione.
- `"Scacciato"` — possibile clausola mancante da confermare.
- `"Esorcizzare Danno"` — sospetto doppione di "Esorcizzare Ferite", da verificare se è una carta distinta.
- `"Guarire"` — nessuna immagine trovata in `image/Arte/`, da verificare se la carta esiste.
- Note informative su incoerenze interne (`"Fulmine Elementare"`, `"Spinta Cinetica"`) — non derivano da un confronto con l'immagine, da verificare in sessione dedicata.

---

## 10. Database_Equipaggiamento.py

Nessuna correzione applicata in questa sessione: l'unico refuso rilevato ("Pistola Coagulante") è **già corretto nel DB** (il refuso è sulla carta fisica originale, non va copiato) — nessuna azione richiesta. Gli altri 4 casi restano ⏳ **DA VERIFICARE** (sospetta classificazione di fazione errata per icona osservata vs `fazioni_permesse: ["Generica"]`): `"AC-40 Justifier"`, `"Lancia Castigator"`, `"Elmetto Comando"`, `"Computer Tattico"` — richiedono un controllo mirato ad alta risoluzione perché il testo di alcune carte potrebbe legittimare "Generica" nonostante l'icona.

---

## 11. Database_Speciale.py

(Vedi anche [§2](#2-anomalie-strutturali-trasversali-chiavi-duplicate) per le chiavi duplicate di questo modulo.)

Tutte le 12 correzioni certe della tabella applicate ✅:

| # | Carta (chiave) | Priorità | Nota sulla correzione applicata |
|---|---|---|---|
| 1 | `"Ammaliatrice"` | 🟠 MEDIA | `fazioni_permesse` `["Generica"]` → **`["Oscura Legione"]`**. |
| 3 | `"Arma Difettosa"` | 🔴 CRITICA | Effetto invertito: ora "l'arma esplode attaccando chi la utilizza" (il portatore subisce l'attacco) invece di "arma disabilitata" (testo copiato da "Lama Spuntata"). |
| 4 | `"Attestato D'Onore"` | 🟠 MEDIA | Rimosso "e V" da `testo_carta` e da `effetti[0].valore`: il bonus reale è "+1 in C, S e A" (3 statistiche, non 4). |
| 5 | `"Incursione Commando"` | 🟡 BASSA | Rimossa la frase extra "Le Fortificazioni possono essere utilizzate normalmente" (copiata da "Incursione Aerea"). |
| 6 | `"Lotta Senza Quartiere"` | 🟠 MEDIA | Costo extra-attacco "20D" → **"2D"** (era un errore di un ordine di grandezza). |
| 7 | `"Mancato Rifornimento"` | 🔴 CRITICA | Effetto riscritto: ora è un contro-effetto reattivo che annulla istantaneamente una singola carta Equipaggiamento appena giocata, al posto del bando permanente di un intero tipo di equipaggiamento. Corretto anche il refuso "Dopo che che questo". |
| 8 | `"Programmato"` | 🔴 CRITICA | Invertita l'immunità: ora immune ai doni **minori dell'Oscura Simmetria** ma non ai doni degli Apostoli (era l'opposto; il campo `limitazioni` era già corretto, ora tutti i campi sono coerenti). |
| 9 | `"Rifugiato Tra La Folla"` | 🟡 BASSA | Rimossa la clausola finale extra sulla scelta del bersaglio da parte dell'Attaccante, assente sulla carta reale. |
| 10 | `"Sabotaggio"` | 🔴 CRITICA | Effetto riscritto: ora colpisce tutti i membri di una Corporazione/Fratellanza/Oscura Legione scelta (che devono scartare le carte Equipaggiamento), al posto dello scarto di una singola carta Speciale. |
| 11 | `"Supporto Tattico"` | 🔴 CRITICA | Costo e meccanica riscritti: **"2D per punto V del rinforzo"**, si sommano **C e S** (non solo A). |
| 12 | `"Svolta Negli Eventi"` | 🟡 BASSA | Aggiunta la clausola finale mancante "Non è concesso alterare la caratteristica V." |
| 13 | `"Tessera Del Clan"` | 🟠 MEDIA | Aggiunta l'esclusione "GIOCABILE SU OGNI DOOMTROOPER NON CYBERTRONIC" al testo; rimosso "Cybertronic" da `fazioni_permesse` (contraddizione diretta con l'immagine). |

**Non applicata ⏳:** #2 `"Famoso Collezionista"` (🔴 CRITICA, carta interamente assente dal database) — **non aggiunta** perché l'audit originale riporta solo un estratto troncato del testo carta ("D'ora in poi sei considerato un FAMOSO COLLEZIONISTA...") e nessun valore per gli altri campi obbligatori dello schema (stats, quantità, rarity, ecc.). Aggiungere una voce con dati incompleti/inventati sarebbe peggio che lasciarla assente — serve tornare all'immagine originale per una trascrizione completa.

**Non applicate ⏳ (voci ⚪ da verificare):** `"False Credenze"`, `"Fiamme Purificatrici"` (sospetta fazione "Fratellanza" invece di "Generica"), `"Feroce Assassino"` (possibile testo troncato nella foto).

**Non applicato per scelta esplicita (deprioritizzato nell'audit originale):** il punto esclamativo mancante nei titoli di 8 carte ("Ritirata"→"RITIRATA!", ecc.) — l'audit originale lo segnala come "probabilmente non prioritario", quindi lasciato invariato.

---

## 12. Problemi non-database (organizzazione file immagini)

**Non applicato ⏳** — non riguarda le correzioni ai moduli Python:

- `image/Oscura Simmetria/Pergamena_D'Evocazione_Sacrilega.jpeg` è un duplicato bit-per-bit di `image/Reliquie/Pergamena_Di_Evocazione_Sacrilega.jpg`. Andrebbe rimosso dalla cartella sbagliata, ma prima va verificato che non sia referenziato da nessun codice — non fatto in questa sessione (è una modifica al filesystem, non al database).

---

## 13. Voci ancora da verificare (riepilogo)

Elenco di tutto ciò che **richiede un secondo controllo visivo o una decisione di design** prima di poter essere corretto, per una sessione futura:

1. **§2** — Censimento esaustivo delle chiavi duplicate su tutti i 9 moduli (non solo Speciale) — i 7 duplicati noti sono tutti risolti, ma non è mai stata fatta una scansione sistematica completa.
2. **§7** — `"Armatura Di Empieta"`: armonizzazione accento (opzionale).
3. **§9** — 4 voci ⚪ in `Database_Arte.py` (`Conoscere La Verita`, `Scacciato`, `Esorcizzare Danno`, `Guarire`) + 2 incoerenze interne (`Fulmine Elementare`, `Spinta Cinetica`).
4. **§10** — 4 voci ⚪ in `Database_Equipaggiamento.py` (classificazione fazione: `AC-40 Justifier`, `Lancia Castigator`, `Elmetto Comando`, `Computer Tattico`).
5. **§11** — `"Famoso Collezionista"`: carta mancante, serve trascrizione completa dall'immagine (l'audit originale ha solo un estratto troncato).
6. **§11** — 3 voci ⚪ in `Database_Speciale.py` (`False Credenze`, `Fiamme Purificatrici`, `Feroce Assassino`).
7. **§11** — Punto esclamativo mancante nei titoli di 8 carte Speciale (cosmetico, deprioritizzato).
8. **§12** — File immagine duplicato (`Pergamena_D'Evocazione_Sacrilega.jpeg` in `Oscura Simmetria/`) da rimuovere (dopo verifica riferimenti nel codice).
9. **Nuovo, dall'audit esteso del 2026-08-01 (§1ter)** — 6 difetti pre-esistenti emersi ma non corretti perché fuori scope: `"Luna"` (stesso `TypeError` di Trincea), `STATISTICHE_MODIFICATORI` definita come lista di liste in `Creatore_Mazzo.py:150` (blocchi di punteggio sui modificatori tutti morti), `"Sabotaggio"` con `tipo_effetto` incoerente, `"Osservatore Tattico"` e `"Aiuto Di Campo"` con abilità/keyword mancanti, `"Il Diciannovesimo Executive"` con la restrizione sull'Arte persa nella riscrittura del testo. Dettagli in §1ter.
10. **Nuovo, dalla verifica del 2026-08-01 (§1bis)** — Il vocabolario di `tipo_effetto` effettivamente gestito da `source/cards/*.py` (`applica_effetto`) è più ristretto di quello già presente nel database (es. molti valori come `"Arte"`, `"Carte"`, `"Combattimento"`, `"Immunita"` compaiono nel DB ma non hanno un branch dedicato nel motore) — non è un difetto di questa sessione ma un gap pre-esistente più ampio, da valutare se estendere il motore o normalizzare il DB.

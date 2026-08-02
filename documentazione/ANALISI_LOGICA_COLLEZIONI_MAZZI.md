# Analisi della logica di creazione di Collezioni e Mazzi — Criteri di scelta delle carte

> **Scopo del documento.** Rendere **espliciti e inequivocabili** i criteri con cui `source/logic/Creatore_Collezione.py` e `source/logic/Creatore_Mazzo.py` scelgono le carte: quali filtri sono rigidi, quali sono solo preferenze, con quali formule vengono calcolati i punteggi e in che modo l'esito viene confrontato con le regole ufficiali raccolte in `documentazione/Manuale e faq/REGOLAMENTO_UNIFICATO.md`.
>
> **Metodo.** Ogni affermazione è stata verificata leggendo il codice sorgente e, dove il comportamento non è deducibile a vista, **eseguendo il codice** e misurandone l'output (le misure sono riportate nel testo). Non ci sono conclusioni dedotte dai commenti nel codice.
>
> **Revisione 2026-08-01 (seconda stesura).** Rianalisi completa rispetto alla prima versione del 2026-07-31. Sono stati trovati **8 difetti nuovi** che la prima stesura non aveva individuato, di cui 4 con impatto elevato sui criteri di scelta, ed è stata **corretta un'affermazione errata** della prima stesura (vedi [§9](#9-rettifiche-alla-stesura-precedente)). Nessuna modifica al codice di selezione è stata applicata: questo documento è la base per la successiva fase di ottimizzazione.

---

## Indice

1. [Executive summary](#1-executive-summary)
2. [Architettura e catena delle decisioni](#2-architettura-e-catena-delle-decisioni)
3. [Criteri di scelta — Collezione](#3-criteri-di-scelta--collezione)
4. [Criteri di scelta — Guerrieri del Mazzo](#4-criteri-di-scelta--guerrieri-del-mazzo)
5. [Criteri di scelta — Carte di supporto del Mazzo](#5-criteri-di-scelta--carte-di-supporto-del-mazzo)
6. [Le funzioni di punteggio: cosa misurano davvero](#6-le-funzioni-di-punteggio-cosa-misurano-davvero)
7. [Il modello di compatibilità carta↔guerriero](#7-il-modello-di-compatibilità-cartaguerriero)
8. [Confronto con il regolamento ufficiale](#8-confronto-con-il-regolamento-ufficiale)
9. [Rettifiche alla stesura precedente](#9-rettifiche-alla-stesura-precedente)
10. [Difetti individuati](#10-difetti-individuati)
11. [Priorità per la fase di ottimizzazione](#11-priorità-per-la-fase-di-ottimizzazione)

---

## 1. Executive summary

L'architettura a due livelli — Collezione (campionamento casuale orientato per fazione) → Mazzo (selezione a punteggio con filtro di compatibilità carta↔guerriero) — è **concettualmente corretta e allineata al regolamento**. Il modello di compatibilità in due strati (icona di affiliazione come filtro grossolano, testo della carta come filtro fine e prevalente) riproduce fedelmente il principio del regolamento §5 *"in caso di conflitto tra quanto scritto su una carta e una regola del manuale, vince sempre il testo della carta"*.

Il problema non è il disegno ma il fatto che **una quota consistente dei criteri dichiarati non è operativa**. Misurando il comportamento reale:

| Criterio dichiarato dal codice | Stato reale misurato |
|---|---|
| Orientamento di fazione della Collezione | ❌ **Inoperante per i Guerrieri**: con orientamento "Mishima", 79 guerrieri su 136 finiscono nel pool "orientato" mentre i Mishima reali sono 12 ([§10.1](#101-)) |
| Filtro per espansione richiesta nel Mazzo | ❌ **Inoperante**: una carta "Inquisition" supera un filtro "Base" ([§10.2](#102-)) |
| Bonus di orientamento Arte/Fratellanza sulle carte di supporto | ❌ **Codice morto** quando `doomtrooper=True` ([§10.3](#103-)) |
| Punteggio di potenza per Oscura Simmetria | ❌ **Costante 2.00 su tutte e 35 le carte**: nessuna discriminazione ([§6.3](#63-perché-tre-tipi-di-carta-hanno-un-punteggio-piatto)) |
| Punteggio di potenza per Arte e Speciale | ⚠️ Quasi piatto: solo 3 effetti su 67 (Arte) e 16 su 187 (Speciale) contribuiscono ([§6.3](#63-perché-tre-tipi-di-carta-hanno-un-punteggio-piatto)) |
| Restrizioni testuali ("Solo Comandanti", "Solo Nefarita", …) | ❌ **Inoperanti in 3 classi su 8**, difetti puntuali in altre 3 ([§10.9](#109-)) |
| Carte con fazione `Generica` associabili a qualsiasi guerriero (regolamento §6) | ❌ **Dichiarate incompatibili con tutti**: 134 Speciali, 28 Equipaggiamenti, 7 Fortificazioni ([§10.11](#1011--nuovo--confronto-stringaenum-tutte-le-carte-generiche-risultano-incompatibili)) |
| Euristica sulle copie consigliate dei guerrieri | ❌ **Irraggiungibile per qualsiasi valore intero** ([§10.5](#105-)) |
| `STATISTICHE_MODIFICATORI` (punteggio sui modificatori) | ✅ **Corretto il 2026-08-01** (vedi `AUDIT_DATABASE_CARTE_CORREZIONI.md` §1quinquies) |

La conseguenza pratica è che, oggi, **la scelta delle carte è governata da molti meno criteri di quanti il codice sembri applicare**: in larga parte da `fondamentale`, da `valore_strategico` assegnato a mano nel database, e dal caso. I due filtri concettualmente più importanti — orientamento e compatibilità testuale — sono in buona parte disattivati.

---

## 2. Architettura e catena delle decisioni

```
Database_*.py  (dati grezzi)
      │
      │  seleziona_carte_casuali_per_tipo()        ← campionamento casuale + orientamento fazione
      ▼
CollezioneGiocatore  (tutte le carte possedute da un giocatore)
      │
      │  determina_orientamento_collezione()       ← deduce l'orientamento dai guerrieri posseduti
      │  seleziona_guerrieri()                     ← punteggio guerriero × bonus orientamento
      │  seleziona_carte_supporto()                ← filtro compatibilità + punteggio × bonus
      ▼
Mazzo da gioco  (squadra + schieramento + carte di supporto)
```

Le decisioni si concentrano in **cinque funzioni**; tutto il resto dei due moduli (circa l'85% delle righe) è I/O, serializzazione JSON, stampa, PDF ed export immagini, e non influenza la scelta delle carte:

| Funzione | File:riga | Ruolo decisionale |
|---|---|---|
| `seleziona_carte_casuali_per_tipo` | `Creatore_Collezione.py:709` | Quali carte entrano nella Collezione |
| `determina_orientamento_collezione` | `Creatore_Collezione.py:1203` | Verso quali fazioni/apostoli/discipline è orientata la Collezione |
| `seleziona_guerrieri` | `Creatore_Mazzo.py:957` | Quali guerrieri entrano nel Mazzo e in quale Area |
| `seleziona_carte_supporto` | `Creatore_Mazzo.py:1218` | Quali carte non-guerriero entrano nel Mazzo |
| `_carta_compatibile_con_guerrieri` | `Creatore_Mazzo.py:1535` | Unico punto di dispatch della compatibilità carta↔guerriero |

---

## 3. Criteri di scelta — Collezione

`seleziona_carte_casuali_per_tipo` viene chiamata una volta per tipo di carta, per ciascun giocatore. I criteri, nell'ordine esatto in cui il codice li applica:

### 3.1 Filtro rigido: espansione e disponibilità residua

```python
if dati.get('set_espansione') in [s.value for s in set_espansioni]:      # riga 729
    if verifica_quantita_disponibile(nome, database):                    # riga 730
```
✅ Corretto. È l'**unico filtro veramente rigido** di questa funzione. `QUANTITA_UTILIZZATE` è un contatore globale che tiene traccia delle copie già distribuite agli altri giocatori, quindi le collezioni si "consumano" a vicenda il pool comune.

### 3.2 Quante carte: il target è in **copie**, non in carte distinte

`min_carte`/`max_carte` arrivano da `calcola_numero_carte_assegnabili`:

```
limite[tipo] = totale_copie_del_tipo_nelle_espansioni × LIMITI_CARTE_COLLEZIONE[tipo][min|max] ÷ numero_giocatori
```

Con espansione Base e 4 giocatori si ottiene, ad esempio: Guerriero 129–144, Speciale 61–72, Equipaggiamento 16–18, Missione 2–2, **Reliquia 0–0 e Warzone 0–0** (quelle carte non esistono nel set Base). `num_carte = random.randint(min, max)` è quindi il numero di **copie** da inserire, e il ciclo termina quando `numero_totale_carte_inserite_per_tipologia >= num_carte`. Il `for _ in range(num_carte)` che lo racchiude è solo un limite superiore al numero di estrazioni.

`LIMITI_CARTE_COLLEZIONE` (min 0.8–1.0, max 1.0) significa che **le collezioni assorbono quasi tutto il pool disponibile**: non è un campionamento parsimonioso, è una spartizione quasi completa del set fra i giocatori.

### 3.3 Tripartizione in pool e probabilità di orientamento

Le carte disponibili vengono divise in tre pool:

| Pool | Criterio |
|---|---|
| `carte_generiche_fondamentali` | `fondamentale=True` **e** `"Generica"` fra le fazioni permesse |
| `carte_orientate` | almeno una fazione della carta è nell'orientamento richiesto |
| `carte_generiche` | tutte le altre |

Ad ogni estrazione si sceglie il pool orientato con probabilità `probabilita_orientamento` (default **0.7**), altrimenti quello generico. Le carte fondamentali generiche vengono aggiunte al pool scelto ad ogni giro.

> ❌ **Questo criterio è rotto per i Guerrieri** — vedi [§10.1](#101-). E il meccanismo di aggiunta delle fondamentali ha un effetto collaterale non voluto — vedi [§10.4](#104-).

### 3.4 Equità fra giocatori

Se `quantita_disponibile < giocatori_rimasti` (con `giocatori_rimasti = numero_giocatori − indice_giocatore_corrente`), la carta viene **saltata** con probabilità `1 − quantita_disponibile / giocatori_rimasti`, e rimossa dal pool. Serve a non favorire i primi giocatori generati sulle carte scarse.

**Eccezione:** le carte `fondamentale=True` non vengono mai saltate, e ricevono `random.randint(1, round(disponibili / giocatori_rimasti))` copie invece di `random.randint(1, disponibili)` — cioè una razione, non una scorpacciata. ✅ Meccanismo corretto e ben congegnato.

### 3.5 Quante copie per carta

```
copie = random.randint(1, min(MAX_COPIE_CARTA=6, quantita_residua))     # carte normali
copie = random.randint(1, round(min(6, residua) / giocatori_rimasti))   # carte fondamentali
```
Ogni carta può essere estratta **una sola volta per collezione** (viene rimossa da tutti i pool dopo l'estrazione).

> ⚠️ Il limite `MAX_COPIE_CARTA = 6` supera il **massimo di 5 copie** stabilito dal regolamento §2. Il commento nel codice lo giustifica ("mazzo max 5 carte e collezione di gioco") ed è difendibile — la Collezione non è il Mazzo — ma va tenuto presente che a valle **né `seleziona_guerrieri` né `seleziona_carte_supporto` verificano il limite di 5 sul mazzo prodotto**: entrambe usano `min(5, …)` per singola tornata, ma il ciclo `while` esterno può servire la stessa carta in tornate successive. Da verificare in fase di ottimizzazione.

### 3.6 Come viene dedotto l'orientamento della Collezione

`determina_orientamento_collezione` misura il "peso" di ciascuna fazione come:

```
peso(fazione) = Σ  copie_in_collezione(guerriero) × V_base(guerriero)
```

cioè l'**investimento** nella fazione, non il semplice conteggio. Poi:

- Doomtrooper → si prendono le **prime 3** fazioni per peso;
- Fratellanza → le **prime 6** discipline d'Arte (dal campo `abilita[].target` dei guerrieri);
- Oscura Legione → i **primi 3** Apostoli (dalle keyword `Seguace di X`), più il conteggio separato dei `Cultista di X`;
- Eretici → conteggio a parte, per keyword `Eretico`.

Il confronto fra i tre totali produce una delle etichette di orientamento (`'oscura legione-doomtrooper'`, `'doomtrooper-fratellanza-oscura legione'`, …) e determina **quante** fazioni/apostoli/arti passare al costruttore di mazzi, con soglie a 0.66 e 0.5. La logica di riduzione (2 fazioni + 3 arti + 2 apostoli nel caso misto) è dichiaratamente intesa a *limitare la dispersione*, così che le carte di supporto scelte siano utilizzabili da più guerrieri.

✅ Criterio sensato e ben motivato. ❌ Ma il filtro per espansione al suo interno (riga 1213) è inoperante — vedi [§10.2](#102-).

---

## 4. Criteri di scelta — Guerrieri del Mazzo

`seleziona_guerrieri` (`Creatore_Mazzo.py:957`).

### 4.1 Ammissione: l'orientamento è un filtro RIGIDO, non una preferenza

Questo è il punto più frainteso della funzione. Un guerriero entra in `guerrieri_ammessi` **solo se** supera uno dei rami di orientamento; chi non lo supera è **escluso dal mazzo**, non semplicemente penalizzato:

| Ramo | Condizione di ammissione |
|---|---|
| Doomtrooper | `doomtrooper=True` **e** fazione in `FAZIONI_DOOMTROOPER`, **e** (`orientamento_doomtrooper` vuoto **oppure** la fazione è nell'elenco) |
| Fratellanza | `fratellanza=True` **e** fazione Fratellanza, **e** (`orientamento_arte` vuoto **oppure** il guerriero ha un'abilità `tipo=="Arte"` la cui `target` contiene una delle discipline richieste) |
| Oscura Legione | `oscura_legione=True` **e** fazione Oscura Legione, **e** (`orientamento_apostolo` vuoto **oppure** keyword `Seguace di X` con X nell'elenco) |
| Cultista | in aggiunta al ramo OL: `orientamento_cultista=True` e keyword `Cultista` |
| Eretico | ramo indipendente (`if`, non `elif`): keyword `Eretico`; se il guerriero era già ammesso ne **moltiplica** il punteggio, altrimenti lo ammette ex novo |

**Conseguenza da tenere presente:** specificare un `orientamento_doomtrooper` ristretto non "preferisce" quelle fazioni, le rende **le uniche ammesse**. Se l'orientamento non trova abbastanza guerrieri, il mazzo esce sotto target.

### 4.2 Formula del punteggio

```
punteggio(guerriero) = base × bonus_moltiplicatore × (1 + valore_strategico × 4/10)

  base = random.uniform(20, 25)                se fondamentale=True
       = calcola_potenza_guerriero(guerriero)  altrimenti          [mediana misurata: 4.57]

  bonus_moltiplicatore =  4.0  (BONUS_SPECIALIZZAZIONE)  fazione giusta, nessun orientamento specifico
                       =  6.0  (BONUS_ORIENTAMENTO)      fazione/apostolo nell'orientamento
                       = 12.0  (BONUS_ORIENTAMENTO × 2)  fratello con disciplina "Tutte le Discipline"
                       × 2     (BONUS_ERETICO)  se eretico e orientamento_eretico
                       × 2     (BONUS_CULTISTA) se cultista e orientamento_cultista
```

**`fondamentale` domina tutto:** 20–25 contro una mediana di 4.57 per la potenza calcolata significa che una carta fondamentale vale circa **5 volte** un guerriero medio, prima ancora dei moltiplicatori. È una scelta deliberata (garantire le carte chiave) ma va ricordata quando si valuta se i punteggi "funzionano": in pratica l'ordinamento è *prima tutte le fondamentali, poi il resto*.

### 4.3 Da punteggio a copie nel mazzo

L'ordinamento decrescente per punteggio determina **l'ordine di servizio**, poi:

```
copie_da_inserire = min(5, quantita_disponibile, quantita_minima_consigliata)
```

L'Area di destinazione è decisa dalla fazione — Doomtrooper/Fratellanza → **Squadra**, Oscura Legione → **Schieramento** — coerentemente con il regolamento §3. Le dimensioni target derivano da `RAPPORTO_SQUADRA_SCHIERAMENTO` (attualmente `1`, cioè 50/50 quando il mazzo è misto).

Un ciclo `while` esterno ripete l'intera lista finché non si raggiunge `numero_guerrieri_target` o finché non restano copie disponibili.

> ❌ L'euristica che dovrebbe calcolare `quantita_minima_consigliata` quando manca nel database è irraggiungibile, con un rischio di ciclo infinito — vedi [§10.5](#105-).

---

## 5. Criteri di scelta — Carte di supporto del Mazzo

`seleziona_carte_supporto` (`Creatore_Mazzo.py:1218`). È la funzione con i criteri più stratificati. Ordine esatto di applicazione:

### Passo 1 — Filtri rigidi

1. Espansione (`filtra_carte_per_espansioni`) — ❌ **inoperante**, vedi [§10.2](#102-).
2. **Compatibilità con almeno un guerriero del mazzo** (`_carta_compatibile_con_guerrieri`): se la carta non è compatibile con nessun guerriero **e** non è una "generica fondamentale", viene scartata (`continue`, riga 1323). Questo è **l'unico vero hard filter di compatibilità dell'intera pipeline**.
3. Un terzo filtro rigido, non dichiarato come tale: `if bonus_moltiplicatore >= 1:` (riga 1463). Le carte il cui moltiplicatore è sceso sotto 1 **non vengono aggiunte affatto** alla lista dei candidati — vedi [§10.6](#106-).

### Passo 2 — Fattore di incremento (qualità dichiarata dall'autore del database)

```
fattore_incremento = 1 + valore_strategico × 4/10        se valore_strategico > 0
fattore_incremento = 100  (BONUS_FONDAMENTALE)           se fondamentale=True   ← prevale
fattore_incremento × 1.5                                 se la carta è "Solo Nefarita"/"Solo Personalita"
                                                          e nel mazzo esiste un guerriero di quel tipo
```

### Passo 3 — Bonus di orientamento

```
BONUS_ORIENTAMENTO     = 10.0     carta della fazione/apostolo richiesto
BONUS_SPECIALIZZAZIONE =  4.0     carta della categoria giusta ma non dell'orientamento specifico
BONUS_ERETICO/CULTISTA =  2       keyword corrispondente
BONUS_FONDAMENTALE     = 100      carta generica fondamentale (ulteriore, oltre al fattore_incremento)
```
Ogni bonus è moltiplicato **anche** per `fattore_incremento`, quindi una carta fondamentale orientata arriva a `10 × 100 = 1000` di moltiplicatore, più il `× 100` finale per le generiche fondamentali.

> ❌ Il ramo Fratellanza/Arte di questo passo è codice morto quando `doomtrooper=True` — vedi [§10.3](#103-).
> ⚠️ Il ramo `oscura_simmetria` senza apostolo corrispondente applica `bonus_moltiplicatore /= 200`, che per il filtro del Passo 1.3 equivale a **escludere la carta** — vedi [§10.6](#106-).

### Passo 4 — Punteggio finale

```
fattore_compatibilita = 1 + 2 × guerrieri_compatibili / guerrieri_totali     ∈ [1, 3]
punteggio = potenza × fattore_compatibilita × bonus_moltiplicatore
```

`fattore_compatibilita` è l'unico punto in cui la compatibilità è un **gradiente** e non un sì/no: una carta usabile da tutti i guerrieri vale il triplo di una usabile da nessuno (ma quella usabile da nessuno è già stata scartata al Passo 1.2, quindi il range effettivo parte poco sopra 1).

Per Equipaggiamento e Speciale si applica in più un aggiustamento in base a `modifica_principale_effettuata()` (`+25%` combattimento/sparare/armatura, `+12.5%` azioni per l'Equipaggiamento; `+12%`/`+64%` per le Speciali), pensato per bilanciare la distribuzione fra carte d'attacco, difesa e azione.

### Passo 5 — Da punteggio a copie

```
quota_per_carta = numero_carte / numero_carte_candidate
copie = min(5, disponibili, max(quantita_minima_consigliata, quota_per_carta))
```

**Criterio da tenere ben presente:** poiché ogni carta candidata riceve almeno la propria quota, **quando il pool di candidati è piccolo l'ordinamento per punteggio non cambia quasi nulla della composizione** — tutte le carte entrano comunque. Il punteggio decide la composizione solo quando i candidati sono molti più delle carte richieste: allora l'ordine di servizio determina chi entra prima che si raggiunga `numero_carte`. È un comportamento ragionevole ma non è quello che il nome "punteggio" suggerisce, ed è il motivo per cui i difetti sui punteggi ([§6](#6-le-funzioni-di-punteggio-cosa-misurano-davvero)) hanno finora avuto effetti poco visibili.

---

## 6. Le funzioni di punteggio: cosa misurano davvero

### 6.1 Scale misurate

Punteggi calcolati su **tutte** le carte dei database (nessun filtro), con il codice attuale:

| Tipo | n | min | mediana | media | max |
|---|---:|---:|---:|---:|---:|
| Guerriero | 136 | 0.00 | 4.57 | 4.96 | 16.80 |
| Equipaggiamento | 79 | 1.00 | 4.00 | 5.41 | 37.50 |
| Fortificazione | 26 | 1.00 | 1.30 | 1.56 | 2.00 |
| Reliquia | 18 | 1.00 | 1.40 | 7.51 | 31.00 |
| Warzone | 14 | 4.00 | 9.68 | 14.38 | 36.00 |
| Speciale | 180 | 2.00 | 2.00 | 2.22 | 8.00 |
| Arte | 66 | 2.00 | 2.00 | 2.05 | 3.00 |
| Oscura Simmetria | 35 | 2.00 | 2.00 | **2.00** | 2.00 |

**Le scale non sono confrontabili fra loro.** Non è un problema finché i punteggi vengono usati *dentro* un tipo (ogni chiamata a `seleziona_carte_supporto` tratta un solo `tipo_carta`), ma diventa un problema se in futuro si volesse bilanciare il mazzo confrontando carte di tipi diversi: una Warzone mediana (9.68) "vale" quanto un Equipaggiamento eccellente, e cinque volte un'Arte eccellente.

### 6.2 Cosa misura ciascuna funzione

| Funzione | Formula di base | Fattori moltiplicativi |
|---|---|---|
| `calcola_potenza_guerriero` | `(C + S + A) × 1.5 / V` — **efficienza per punto Destino speso**, non potenza assoluta | abilità per coppia (`tipo`, `nome`): ×1.5 uccide automaticamente, ×1.4 immunità, ×1.3 modificatore/arte/carte/azioni, ×1.1–1.2 minori |
| `calcola_potenza_equipaggiamento` | `1 + Σ modificatori C/S/A positivi` | abilità speciali per `(tipo_attivazione, nome)`, ×1.1–1.5 |
| `calcola_potenza_fortificazione` | `1` + fasce dai modificatori | idem |
| `calcola_potenza_reliquia` | `1 + Σ valori dei modificatori` (+10 per "raddoppiate"/"x3"/"uguale alla più elevata") | poteri per `(tipo_potere, nome)` |
| `calcola_potenza_warzone` | `(Σ mod. positivi × 2) / (1 + Σ |mod. negativi|)` | fasce + effetti di combattimento |
| `calcola_potenza_arte` / `_oscura_simmetria` / `_speciale` | `_calcola_potenza_carta_stats + _calcola_potenza_carta_azioni` (1.0 + 1.0 di base) | — |

Il fatto che il punteggio del guerriero sia **diviso per V** è una scelta importante e corretta: premia l'efficienza economica, coerente con il regolamento §4 (V = Punti Destino da spendere). Nota però che V è anche ciò che l'avversario guadagna uccidendolo (§4), e questo lato del bilancio non è modellato.

### 6.3 Perché tre tipi di carta hanno un punteggio piatto

`_calcola_potenza_carta_stats` conta un effetto solo se soddisfa **tutte** queste condizioni:

```python
tipo_effetto.lower() == "modificatore"
statistica_target.lower() in ["combattimento","sparare","armatura","c","s","a"]
isinstance(valore, int) and valore > 0
```

Misurando i database:

| Tipo | effetti totali | `valore` di tipo `int` | effetti che superano **tutti** i filtri |
|---|---:|---|---:|
| Speciale | 187 | 120 int / 67 str | **16** |
| Arte | 67 | 29 int / 38 str | **3** |
| Oscura Simmetria | 35 | 0 int / **35 str** | **0** |

Per l'Oscura Simmetria **nessun effetto può mai contribuire**: tutti i `valore` sono stringhe (`"+2"`, `"3D"`, …). Da qui il punteggio costante 2.00 su tutte e 35 le carte, cioè **nessuna discriminazione fra una carta forte e una debole**.

`_calcola_potenza_carta_azioni` è nella stessa condizione: cerca `tipo_effetto` fra `'danno'`, `'azione combattimento'`, `'azione fase'`, `'azione ogni momento'`, ma nei database esistono solo `modificatore` (189), `carte` (44), `arte` (15), `combattimento` (14), `immunita` (10), `guarigione` (8), `controllo` (7), `scarto_carte` (1) e **una sola** occorrenza di `azione combattimento`. Su 282 carte, 281 escono con 1.0 fisso.

> È **la stessa famiglia di difetto** già corretta in `STATISTICHE_MODIFICATORI` (`AUDIT_DATABASE_CARTE_CORREZIONI.md` §1quinquies): un vocabolario atteso dal codice che non corrisponde a quello realmente presente nei dati, più un tipo (`int` contro `str`) non uniforme. Vale qui la stessa avvertenza: correggendolo, i punteggi di 282 carte cambiano in blocco e va fatto un confronto prima/dopo.

---

## 7. Il modello di compatibilità carta↔guerriero

### 7.1 I due livelli

**Livello 1 — icona di affiliazione.** `fazioni_permesse` (Equipaggiamento, Speciale, Arte, Oscura Simmetria) o `restrizioni.fazioni_permesse` (Fortificazione, Reliquia, Warzone). Il valore `"Generica"` corrisponde esattamente all'icona Generica del regolamento §6. ✅ Implementato correttamente in tutti i moduli.

**Livello 2 — testo della carta.** Una lista di stringhe standardizzate (`restrizioni`, `restrizioni_guerriero`, `restrizioni.limiti_utilizzo`) interpretate con `if "..." in restrizione:` e verificate contro `guerriero.keywords`, `guerriero.fazione`, `guerriero.tipo`, `guerriero.stats.valore`:

- `"Solo Doomtrooper"`, `"Solo Oscura Legione"`, `"Solo Fratellanza"`
- `"Solo Eretici"`, `"Solo Necromutanti"`, `"Solo Nefarita"`, `"Solo Comandanti"`, `"Solo Personalita"`
- `"Solo Seguaci di <Apostolo>"`, `"Solo Mercenari"`, `"Solo Mercenari o Eretici"`
- `"Assegnabile a guerrieri con V <= N"`
- `"Non utilizzabile da ..."`

Le `keywords` del guerriero sono la rappresentazione strutturata delle affermazioni in maiuscolo sul testo della carta (`SEGUACE DI ALGEROTH`, `COMANDANTE`, `PERSONALITÀ`, …) — motivo per cui l'allineamento fra `testo_carta` e `keywords` è un requisito di correttezza e non un dettaglio cosmetico (vedi il caso "Osservatore Tattico" in `AUDIT_DATABASE_CARTE_CORREZIONI.md` §1ter).

### 7.2 Il dispatch

`_carta_compatibile_con_guerrieri` (riga 1535) restituisce `[compatibile, numero_guerrieri_compatibili]` interrogando, per ciascun guerriero del mazzo:

| Tipo carta | Metodo invocato | Chiave letta dal risultato |
|---|---|---|
| equipaggiamento, fortificazione, speciale | `puo_essere_assegnato_a_guerriero()` | `puo_assegnare` |
| arte, oscura_simmetria | `puo_essere_associata_a_guerriero()` | `puo_lanciare` |
| reliquia, warzone | `puo_essere_associata_a_guerriero()` | `puo_assegnare` |
| missione | `puo_essere_associata_a()` | `puo_assegnare` |

✅ Il dispatch centralizzato è un buon punto di disegno. ❌ I metodi delegati sono difettosi in 6 classi su 8 — vedi [§10.9](#109-).

---

## 8. Confronto con il regolamento ufficiale

| Regola | Corrispondenza nel codice | Valutazione |
|---|---|---|
| §5 *"vince sempre il testo della carta"* | Modello a due livelli, `restrizioni` prevalenti sulla fazione | ✅ nel disegno · ❌ inoperante in 3 classi su 8 |
| §2 Mazzo ≥ 60 carte con ≥ 5 guerrieri; max 5 copie per carta | `numero_guerrieri_target` e `numero_carte` sono parametri liberi; `min(5, …)` per tornata ma il ciclo `while` può servire la stessa carta più volte | ⚠️ Nessuna **validazione finale** del mazzo prodotto contro i vincoli del regolamento |
| §3 Aree: Doomtrooper→Squadra, Oscura Legione→Schieramento, Tribù→Avamposto | `seleziona_guerrieri` instrada correttamente Squadra/Schieramento | ✅ per le due Aree implementate · ⚪ Avamposto/Tribù non modellati |
| §5 Equipaggiamenti: 1 sola Armatura, 1 solo Veicolo, N Armi ma una per combattimento | Nessun vincolo di questo tipo nella selezione | ⚪ Non modellato: il mazzo può contenere qualsiasi mix (accettabile, il vincolo è di gioco non di costruzione) |
| §5 Reliquie: tutte uniche | Nessun vincolo di unicità nella selezione delle copie | ⚠️ Il mazzo può ricevere più copie di una Reliquia, che in partita sarebbero ingiocabili |
| §5 Arti: lanciabili dalla Fratellanza e da pochi altri abilitati; suddivise per Disciplina | `Arte.puo_essere_associata_a_guerriero` verifica `abilita[].tipo == "Arte"` e la disciplina | ✅ nel disegno · ❌ confronto invertito ([§10.9](#109-)) |
| §5 Doni Oscura Simmetria: 3 livelli con requisiti crescenti | `TipoOscuraSimmetria` + keyword `Seguace di X` | ✅ nel disegno · ❌ chiave del risultato sbagliata ([§10.9](#109-)) |
| §5 Fortificazioni: si assegnano a un'Area, salvo eccezioni testuali | `Fortificazione.puo_essere_assegnato_a_guerriero` **consulta** `self.beneficiario` per il caso `Corporazione Specifica` (riga 162) | ✅ modellato — vedi la rettifica in [§9](#9-rettifiche-alla-stesura-precedente) |
| §5 Warzone: solo il Difensore ne beneficia | `modificatori_difensore` esiste ed è usato nel punteggio | ✅ modellato a livello di dati |
| §12 Chi può attaccare chi | `Guerriero.puo_attaccare` implementa le regole di ingaggio (Fratellanza↔OL, stessa Corporazione, Assassini) | ✅ corretto — non incide sulla selezione ma è un punto di forza |
| §6 Tribù di Dark Eden | `Fazione` non ha valori per le Tribù; nessuna carta nel database | ⚪ Copertura assente, coerente con i dati attuali |
| §23 Guerre Corporative (mazzo mono-affiliazione) | Nessuna classe né logica dedicata | ⚪ Fuori scope della versione attuale |

---

## 9. Rettifiche alla stesura precedente

La prima stesura (2026-07-31) conteneva due affermazioni da correggere:

1. **`Fortificazione.beneficiario` non è ignorato.** La stesura precedente affermava che *"`puo_essere_assegnato_a_guerriero` non lo consulta"*. In realtà lo consulta a `Fortificazione.py:162` (`if self.beneficiario.value == "Corporazione Specifica" and self.corporazione_specifica is not None:`), con un blocco completo che gestisce `"Doomtrooper"`, `"Eretici"`, `"Seguaci di X"` e la corrispondenza diretta di fazione, e che restituisce subito il risultato negativo. È il ramo `GUERRIERI_AREA` a non ricevere un trattamento distinto, non l'intero campo.

2. **Il difetto di `fazioni_permesse` in `Creatore_Collezione.py` era stato classificato come "impatto pratico basso"**, con la motivazione che il valore sarebbe comunque coerente con la carta corrente. È sbagliato: il ramo dei Guerrieri usa `.append()` e non `=`, quindi la lista **si accumula** per tutto il ciclo. L'impatto misurato è elevato — vedi [§10.1](#101-).

---

## 10. Difetti individuati

Ordinati per impatto sui criteri di scelta. Le voci marcate **NUOVO** non erano presenti nella stesura del 2026-07-31.

### 10.1 🔴 **NUOVO** — L'orientamento di fazione della Collezione non funziona per i Guerrieri

**File:** `Creatore_Collezione.py:747,753`

```python
fazioni_permesse = []                                   # riga 747: dichiarata FUORI dal ciclo
for nome, dati in carte_disponibili.items():
    if 'fazione' in dati:                               # ramo Guerriero
        fazioni_permesse.append(dati.get('fazione'))    # riga 753: APPEND, mai azzerata
    elif 'fazioni_permesse' in dati:
        fazioni_permesse = dati.get('fazioni_permesse', [])   # gli altri rami REASSEGNANO
```

Nel ramo Guerriero la lista **accumula** le fazioni di tutti i guerrieri già esaminati, invece di contenere quella del guerriero corrente. Dal momento in cui compare il primo guerriero della fazione richiesta, **ogni guerriero successivo** risulta "orientato".

**Misura:** con `fazioni_orientamento=[Mishima]` sul database attuale, **79 guerrieri su 136** finiscono in `carte_orientate`; i Mishima reali sono **12**. I 57 classificati correttamente sono solo quelli che precedono il primo Mishima nell'ordine del dizionario.

Gli altri tipi di carta non sono affetti (verificato: 23 Speciali orientate = 23 Speciali realmente Mishima).

**Impatto:** l'orientamento della Collezione — il criterio che dovrebbe caratterizzare ogni giocatore — è di fatto casuale proprio sul tipo di carta più importante. Correzione: `fazioni_permesse = [dati.get('fazione')]`.

### 10.2 🔴 **NUOVO** — Il filtro per espansione è un no-op

**File:** `Creatore_Mazzo.py:952` e `Creatore_Collezione.py:1213` (stessa riga, duplicata)

```python
if set_carta in espansioni_richieste.value if hasattr(espansioni_richieste, 'value') else espansioni_richieste:
```

L'espressione condizionale si raggruppa come `(set_carta in espansioni_richieste.value) if hasattr(...) else (espansioni_richieste)`. Quando `espansioni_richieste` è una lista normale — cioè **sempre**, nell'uso corrente — la condizione è la semplice verità della lista, quindi **ogni carta passa il filtro**.

**Verifica eseguita:** con `espansioni=['Base']` e `set_carta='Inquisition'` l'espressione vale `['Base']` → `True`, mentre il risultato corretto è `False`.

**Impatto:** `seleziona_guerrieri` e `seleziona_carte_supporto` ignorano completamente le espansioni richieste per il mazzo. La Collezione resta filtrata correttamente (il filtro alla riga 729 è scritto bene), quindi il danno è limitato ai casi in cui si chiede un mazzo ristretto a un sottoinsieme delle espansioni della collezione — ma in quei casi è totale. Correzione: `if set_carta in espansioni_richieste:` (o gestire esplicitamente il caso enum).

### 10.3 🔴 **NUOVO** — Il ramo Fratellanza/Arte delle carte di supporto è codice morto

**File:** `Creatore_Mazzo.py:1326`

```python
doomtrooper_dedicata = any(f in fazioni for f in FAZIONI_DOOMTROOPER) or 'Doomtrooper'
```

`or 'Doomtrooper'` è una stringa non vuota, quindi **`doomtrooper_dedicata` è sempre veritiera**, per qualsiasi carta. Due conseguenze:

1. il blocco `if doomtrooper and doomtrooper_dedicata:` (riga 1333) si applica a **tutte** le carte quando `doomtrooper=True`, anche a quelle di fazioni estranee;
2. il blocco Fratellanza alla riga 1345 è guardato da `not (doomtrooper_dedicata or orientamento_doomtrooper_dedicata)`, che è quindi **sempre falso**: **tutti i bonus di orientamento per Arte e Fratellanza non vengono mai applicati** nei mazzi che includono i Doomtrooper.

Correzione: rimuovere `or 'Doomtrooper'` (probabile residuo di un tentativo di trattare la stringa `"Doomtrooper"` come valore ammesso in `fazioni`, gestito comunque alla riga 1338).

### 10.4 🟠 **NUOVO** — `pool_carte.update()` contamina i pool di selezione

**File:** `Creatore_Collezione.py:789`

```python
pool_carte = carte_orientate  (oppure carte_generiche)
pool_carte.update(carte_generiche_fondamentali)
```

`pool_carte` è un **riferimento**, non una copia: l'`update` inserisce stabilmente le carte fondamentali dentro `carte_orientate` o `carte_generiche`. Dopo poche iterazioni entrambi i pool contengono le fondamentali, e la distinzione orientato/generico si annacqua: la probabilità effettiva di pescare una carta orientata non è più `probabilita_orientamento`. Correzione: costruire un pool temporaneo (`pool_carte = {**pool_scelto, **carte_generiche_fondamentali}`).

### 10.5 🟠 **NUOVO** — Euristica sulle copie dei guerrieri irraggiungibile, con rischio di ciclo infinito

**File:** `Creatore_Mazzo.py:1151`

```python
if quantita_consigliata and quantita_consigliata < 1:
```

Per un intero, `bool(q)` e `q < 1` non possono essere veri insieme: `q=0` è falsy, `q≥1` non è `<1`. Il blocco di 15 righe che calcola le copie consigliate in base al Valore del guerriero (righe 1151–1166) **non viene mai eseguito**.

Oggi non provoca danni perché nessun guerriero ha `quantita_minima_consigliata = 0` (distribuzione misurata: 105 carte con 1, 14 con 2, 13 con 3, 4 con 4). Ma se un solo guerriero avesse 0, `num_copie_da_inserire = min(5, disponibile, 0) = 0`: il mazzo non crescerebbe mai e la condizione di uscita `carte_ancora_disponibili` resterebbe vera → **ciclo `while` infinito**. Correzione: `if quantita_consigliata < 1:`.

### 10.6 🟠 **NUOVO** — Esclusione silenziosa tramite `bonus_moltiplicatore`

**File:** `Creatore_Mazzo.py:1377` e `1463`

Alla riga 1377, una carta Oscura Simmetria che non corrisponde ad alcun apostolo dell'orientamento subisce `bonus_moltiplicatore /= 2 * BONUS_FONDAMENTALE`, cioè **÷200**. Alla riga 1463 il candidato viene aggiunto solo `if bonus_moltiplicatore >= 1`. Il risultato è che quelle carte **non vengono penalizzate, vengono eliminate** — mentre il commento nel codice dice esplicitamente *"non implementato: decremento del bonus"*. Comportamento e intento dichiarato divergono; da decidere quale dei due si vuole.

Sempre alla riga 1463, `potenza` è assegnata solo dentro la catena `if/elif` sui tipi di carta: per un `tipo_carta` non previsto la variabile conserva il valore dell'iterazione precedente (o solleva `NameError` alla prima). Da rendere esplicito con un `else`.

### 10.7 🟡 **NUOVO** — Punteggi inerti per Arte, Speciale e Oscura Simmetria

Vedi [§6.3](#63-perché-tre-tipi-di-carta-hanno-un-punteggio-piatto). Non è un errore di sintassi ma un disallineamento fra il vocabolario/tipi attesi dal codice e quelli presenti nei database. Per l'Oscura Simmetria la funzione di punteggio non discrimina **nulla**.

### 10.8 🟡 **NUOVO** — Difetti minori della classe `CollezioneGiocatore`

- `get_copie_disponibili` (`Creatore_Collezione.py:348`) restituisce al massimo **1**: usa `if carta in collezione: copie += 1` invece di contare le occorrenze. Attualmente non è chiamata dai percorsi di selezione, ma è pronta a trarre in inganno.
- `aggiungi_carta` inserisce **N riferimenti allo stesso oggetto** (riga 319-320), e `get_carte_per_tipo_mazzo` sfrutta questo fatto mutando `carta.quantita`. Funziona, ma significa che ogni modifica a un'istanza di carta si propaga a tutte le sue "copie" in tutte le collezioni — una trappola per qualsiasi futura logica che voglia distinguere le singole copie.

### 10.9 ✅ Difetti nelle classi di `source/cards/` — **corretti tutti il 2026-08-02**

I sette difetti (a–g) più il difetto latente gemello di `Reliquia.py:211` sono stati **corretti in un unico intervento**, come richiesto dall'analisi: (a) da solo avrebbe attivato (c), che avrebbe bloccato ogni guerriero. Dettaglio dell'intervento e misure in **§13**. Segue la tabella originale dei difetti, a documentazione di cosa è stato risolto:

| # | File:riga | Difetto | Effetto |
|---|---|---|---|
| a | `Fortificazione.py:188` · `Speciale.py:255` · `Warzone.py:270` | Guardia invertita `is None or == []` | Il blocco delle restrizioni testuali gira **solo quando la lista è vuota**: non blocca mai nulla |
| b | `Reliquia.py:190,197` · `Warzone.py:263` | `!= None or != []` (serve `and`) | Sempre vero: innocuo ma stesso errore logico |
| c | `Speciale.py:314,319` · `Missione.py:158,163` | `guerriero.keywords != "Comandante"` (lista contro stringa) | Sempre vero: se il difetto (a) venisse corretto, bloccherebbe **tutti** i guerrieri |
| d | `Missione.py:156` | `"Seguace di" == [s[:10] for s in ...]` (stringa contro lista) | Ramo mai raggiunto; se lo fosse, `AttributeError` su `.split()` di una lista |
| e | `Missione.py:193` | `Tipobersaglio.PERSONALITA` — nome non definito | `NameError` se il ramo venisse raggiunto |
| f | `Oscura_Simmetria.py:167 vs 182,186,190,194` | Inizializza `puo_lanciare`, scrive `puo_assegnare` | 4 controlli su 5 (Seguace, Eretico, Nefarita, non-Personalità) **non filtrano nulla** |
| g | `Arte.py:173` | `any(... not in ...)` invece di `any(... in ...)` | Il controllo "il guerriero deve avere la disciplina" è **disattivato** |

Da notare che `Reliquia.py:211` contiene lo stesso difetto latente di (d): `self.restrizioni.fazioni_permesse.split(...)` su una lista.

### 10.11 🔴 **NUOVO** — Confronto stringa/enum: tutte le carte generiche risultano incompatibili

**File:** `Speciale.py:250` · `Equipaggiamento.py:146,277` · `Fortificazione.py:251`

```python
if self.fazioni_permesse != ["Generica"]:      # confronto con una lista di STRINGHE
```

Dopo `from_dict`, `fazioni_permesse` è una lista di membri dell'enum `Fazione`, cioè `[Fazione.GENERICA]`. Il confronto con `["Generica"]` (stringhe) è quindi **sempre vero**, e la clausola di scampo per le carte generiche — *"verifica se è equipaggiamento generico utilizzabile da tutti"*, come recita il commento nel codice — **non scatta mai**. Ogni carta con fazione `Generica` viene dichiarata incompatibile con ogni guerriero, in contrasto diretto con il regolamento §6, che definisce le carte Generiche come prive di legame di affiliazione.

`Missione.py:208` è l'**unica implementazione corretta** (`Fazione("Generica") not in self.fazioni_permesse`), ed è infatti l'unico tipo di carta in cui le generiche risultano correttamente compatibili.

**Misure** (guerriero di prova: un Doomtrooper Imperiale):

| Tipo | carte generiche nel DB | generiche risultate compatibili |
|---|---:|---:|
| Speciale | 134 / 180 | **0** |
| Equipaggiamento | 28 / 79 | **0** |
| Fortificazione | 7 / 26 | **0** |
| Missione | 2 / 7 | 2 ✅ |

**Effetto sulla selezione**, misurato simulando la sola correzione del confronto su `Speciale.py:250` (mazzo di 21 guerrieri misti):

| | Speciali compatibili | carte distinte nel mazzo | entrate dalla scappatoia |
|---|---:|---:|---:|
| Prima | 44 / 180 | 85 | 41 |
| Dopo | **180 / 180** | 180 | **0** |

Il bacino di candidati per le Speciali passa da 85 a 180: è la correzione con il maggior impatto sulla composizione dei mazzi fra tutte quelle individuate. Da applicare **insieme** a §10.9(a), perché oggi il valore "180 su 180" è a sua volta troppo permissivo — le restrizioni testuali che dovrebbero ridurlo sono disattivate.

### 10.10 ⚪ Pulizia

`Creatore_Mazzo.py:1121` contiene ancora una stampa di debug con linguaggio scurrile (`"MA CHI CAZZ'E'??"`). È peraltro **irraggiungibile**: il ramo `else` scatta solo se il guerriero è in `guerrieri_ammessi` ma non in `punteggi`, condizione che `_assegnazione_punteggio_guerriero_ammesso` rende impossibile. Da rimuovere insieme al ramo.

---

## 11. Priorità per la fase di ottimizzazione

Ordine consigliato, dal rapporto beneficio/rischio più alto al più basso.

**Fascia 1 — ripristinare i criteri che il codice intende già applicare** (correzioni di una riga, nessun cambio di disegno):

1. §10.1 `fazioni_permesse = [dati.get('fazione')]` — restituisce senso all'orientamento delle Collezioni.
2. §10.2 filtro espansioni, in entrambi i moduli.
3. §10.3 rimozione di `or 'Doomtrooper'` — riattiva l'orientamento Arte/Fratellanza.
4. §10.5 `if quantita_consigliata < 1:` — elimina il rischio di ciclo infinito.
5. §10.9 (a)+(b)+(c) — le guardie booleane e i confronti lista/stringa, da correggere **insieme**: (a) da sola riattiverebbe (c), che blocca tutti i guerrieri.
6. §10.9 (f) — chiave `puo_lanciare` in `Oscura_Simmetria.py`.
7. §10.9 (g) — inversione della logica delle discipline in `Arte.py`.

⚠️ Le voci 1, 2, 3 e 5 **cambiano la composizione dei mazzi generati**. Come già fatto per `STATISTICHE_MODIFICATORI`, conviene catturare un campione di mazzi prima e dopo e confrontarli, invece di verificare solo che il codice non sollevi eccezioni.

**Fascia 2 — decisioni di disegno da prendere prima di intervenire:**

8. §10.6 — la penalizzazione ÷200 deve escludere la carta o solo declassarla?
9. §10.7 — allineare vocabolario e tipi degli `effetti` fra codice e database, oppure rendere il codice tollerante come si è fatto per i modificatori. Impatta 282 carte in blocco.
10. §6.1 — se in futuro i punteggi verranno confrontati fra tipi di carta diversi, le scale vanno normalizzate (oggi variano da "costante 2.00" a "0–37.5").
11. §8 — aggiungere una **validazione finale del mazzo** contro i vincoli del regolamento §2 (≥60 carte, ≥5 guerrieri, ≤5 copie per carta, unicità delle Reliquie). Oggi non esiste alcun controllo di questo tipo.

**Fascia 1bis — difetti di `seleziona_carte_supporto` emersi dall'analisi dedicata (§12):**

7bis. §12.4 `ZeroDivisionError` con mazzo senza guerrieri — 4 righe di guardia.
7ter. §12.5 limite di 5 copie non imposto (violazione regolamento §2).
7quater. §12.2 dominanza di `BONUS_FONDAMENTALE` — decisione di bilanciamento.

**Fascia 3 — riduzione strutturale del rischio:**

12. Estrarre un modulo condiviso `source/cards/regole_associazione.py` con un'unica `verifica_restrizioni_guerriero(restrizioni, guerriero)`, richiamata da tutte e sei le classi che oggi reimplementano lo stesso ciclo `if/elif` con refusi diversi. È la causa strutturale dei difetti §10.9: sei copie della stessa regola significano sei occasioni di sbagliarla.
13. Suite di test parametrica su ciascuna stringa di restrizione, con **caso positivo e caso negativo** per ogni classe carta. Tutti i difetti di §10.9 sarebbero stati intercettati dal solo caso negativo, perché restituiscono sempre `True`.
14. §10.8 e §10.10 — pulizia.

---

## 12. Analisi dedicata di `seleziona_carte_supporto()`

Approfondimento richiesto il 2026-08-01. Tutte le cifre riportate sono **misurate** eseguendo la funzione su una collezione di prova contenente ogni carta del database (5 copie ciascuna, 12 dove indicato) e un mazzo di 21 guerrieri misti Squadra/Schieramento.

### 12.1 Struttura: quattro fasi

| Fase | Righe | Contenuto |
|---|---|---|
| A — Raccolta e filtri | 1261–1324 | carte del tipo richiesto → filtro espansione → calcolo `fattore_incremento` e `fazioni` → **filtro di compatibilità** |
| B — Punteggio | 1326–1466 | bonus di orientamento → bonus keyword → potenza specifica del tipo → punteggio finale |
| C — Ordinamento | 1469 | `sort` decrescente per punteggio |
| D — Allocazione copie | 1472–1533 | ciclo `while` a tornate, con quota per carta |

I due `DISTRIBUZIONE_*` dichiarati in testa alla funzione (righe 1246–1258) sono usati solo nella fase B, come aggiustamento percentuale della potenza.

### 12.2 Il punteggio è deciso quasi solo da `fondamentale`

```
punteggio = potenza × fattore_compatibilita × bonus_moltiplicatore
```

Ampiezza reale dei tre fattori:

| Fattore | Intervallo | Rapporto max/min |
|---|---|---|
| `potenza` (Speciale) | 2.00 – 8.00 | 4× |
| `fattore_compatibilita` | 1.00 – 3.00 | 3× |
| `bonus_moltiplicatore` | 1 – oltre 1000 | **oltre 1000×** |

`bonus_moltiplicatore` incorpora `fattore_incremento`, che vale `BONUS_FONDAMENTALE = 100` per le carte `fondamentale=True` (contro `1 + valore_strategico × 0.4`, cioè al massimo 5, per le altre). Moltiplicato per `BONUS_ORIENTAMENTO = 10` e per l'ulteriore `× 100` delle generiche fondamentali, il divario fra una carta fondamentale e una normale è di **due-tre ordini di grandezza**, mentre potenza e compatibilità insieme coprono al massimo un fattore 12.

**Misura:** chiedendo 40 carte Speciali, **le prime 22 carte servite sono tutte `fondamentale=True`**. Poiché il database contiene 48 Speciali fondamentali su 180, qualunque mazzo che richieda fino a ~48 carte Speciali è composto **esclusivamente** da carte fondamentali: potenza, compatibilità e orientamento non incidono sulla composizione finché ci sono fondamentali disponibili.

### 12.3 Tre filtri rigidi, di cui uno non dichiarato

1. **Espansione** (riga 1263) — inoperante, vedi [§10.2](#102-).
2. **Compatibilità con almeno un guerriero** (riga 1323): `if not (carta_compatibile or carta_generica_fondamentale)`. La condizione è **corretta e voluta**: entrano le carte compatibili più quelle generiche (per definizione associabili a qualsiasi guerriero) classificate `fondamentale`, cioè le carte indispensabili la cui quantità è limitata nella collezione.
   *Misura:* per le Speciali, **41 carte su 85** entrano dal ramo `carta_generica_fondamentale`, cioè il 48% delle copie. **Questo numero non è un difetto del filtro ma il sintomo del difetto §10.11**: le carte generiche vengono erroneamente dichiarate incompatibili, quindi la scappatoia — pensata come rete di sicurezza per casi rari — sta facendo da via d'ingresso principale. Corretto il §10.11, gli usi della scappatoia scendono a **0** (misurato).
   La scappatoia è comunque applicabile solo a Equipaggiamento, Speciale, Fortificazione e Missione: negli altri quattro database non esiste alcuna carta con fazione `Generica`, quindi `carta_generica_fondamentale` non può mai essere vera.
3. **`if bonus_moltiplicatore >= 1`** (riga 1463) — filtro non dichiarato come tale. Una carta il cui moltiplicatore è sceso sotto 1 non viene *declassata*, viene **eliminata**. ✅ **Risolto il 2026-08-01, vedi §12.10.**
   *Misura (prima della correzione):* con `tipo_carta='oscura_simmetria'` e `orientamento_apostolo=['Algeroth']`, **19 carte su 35 sparivano**. Il conto tornava esattamente: 25 carte sono di tipo `"Dono degli Apostoli"`, che non corrisponde ai due valori cercati alla riga 1365 (`"Dono dell'Oscura Simmetria"`, `"Dono dell'Oscura Legione"`), quindi finivano nel ramo `elif` dell'apostolo; di queste solo 6 hanno la keyword `Seguace di Algeroth`; le restanti **19** subivano `bonus_moltiplicatore /= 2 × BONUS_FONDAMENTALE` (÷200 → 0.005) e venivano scartate dal filtro.

   Da notare l'effetto collaterale del `if/elif` alla riga 1365: i **Doni degli Apostoli — i più potenti dei tre livelli previsti dal regolamento §5 — non ricevono mai il bonus di specializzazione Oscura Legione**, perché il test sul `tipo` cattura solo i doni generici.

### 12.4 🔴 `ZeroDivisionError` con un mazzo senza guerrieri

**Riga 1464:** `fattore_compatibilita = 1 + 2 * numero_guerrieri_compatibili / numero_guerrieri`

Se `squadra + schieramento` è vuoto, `_carta_compatibile_con_guerrieri` restituisce `[False, 0]` per ogni carta, ma le carte generiche fondamentali superano comunque il filtro della riga 1323 e arrivano alla riga 1464, dove `numero_guerrieri` vale 0.

**Verificato:** `ZeroDivisionError: division by zero` a `Creatore_Mazzo.py:1464`.

Per disegno **un mazzo non può esistere senza guerrieri**, quindi la collezione di partenza ne contiene sempre un certo numero. Il punto è che la condizione che innesca il crash **non è "collezione senza guerrieri"**: è "nessun guerriero *ammesso*". Poiché l'orientamento in `seleziona_guerrieri` è un filtro rigido ([§4.1](#41-ammissione-lorientamento-è-un-filtro-rigido-non-una-preferenza)), basta che l'orientamento richiesto non corrisponda ad alcun guerriero presente — un refuso nel nome di una fazione, o una collezione che semplicemente non contiene quella fazione — perché la funzione restituisca `[], []`.

**Verificato su una collezione contenente tutti i 136 guerrieri del database**: con un orientamento che non ne ammette nessuno, `seleziona_guerrieri` restituisce liste vuote e `seleziona_carte_supporto` va in `ZeroDivisionError`. `crea_mazzo_da_gioco` non contiene alcuna guardia fra le due chiamate (righe 1743–1761). Serve quindi una verifica esplicita che interrompa la creazione con un errore comprensibile invece di propagare l'eccezione.

### 12.5 🔴 Il limite di 5 copie per carta non è imposto

`num_copie_da_inserire = min(5, quantita_disponibile, quantita_minima_consigliata)` (riga 1506) limita la **singola tornata**, ma il ciclo `while` esterno ripercorre l'intera lista finché non si raggiunge `numero_carte` o non restano copie disponibili, accumulando su `quantita_utilizzata`.

**Nell'uso normale il limite risulta rispettato.** Misura sulla pipeline reale (collezione generata da `creazione_Collezione_Giocatore` per 3 giocatori, set Base; mazzo da 60–80 carte): collezione con **max 6 copie** per carta, mazzo prodotto con **max 3 copie** e **nessuna carta oltre le 5**. Il tetto effettivo è dato da `MAX_COPIE_CARTA = 6` in `Creatore_Collezione.py`, non da un controllo nel costruttore di mazzi.

**Ma non è garantito.** Il limite regge finché la collezione offre abbastanza carte distinte da coprire il fabbisogno. Misura con una collezione volutamente stretta (15 Speciali distinte × 6 copie, il massimo che il generatore reale può produrre):

| Carte richieste | Ottenute | Max copie per carta | Carte oltre 5 copie |
|---:|---:|---:|---:|
| 20 | 20 | 3 | 0 |
| 60 | 42 | **6** | **7** |
| 90 | 42 | **6** | **7** |

Quando il bacino si esaurisce, il ciclo `while` continua a servire le stesse carte fino a consumarne tutte le copie disponibili, arrivando a **6 copie** — una in più del massimo consentito dal regolamento §2. La violazione è quindi di **una sola copia** e si manifesta solo con collezioni povere rispetto alla dimensione di mazzo richiesta, non nella configurazione tipica.

> ⚠️ *Rettifica.* Una prima misura di questa analisi riportava "12 copie per carta": proveniva da una collezione sintetica costruita per il test, con 12 copie di ogni carta — una situazione che il generatore di collezioni reale **non può produrre**. La cifra corretta è 6.

### 12.6 L'ordinamento decide l'ordine di servizio, non la composizione

```
quota_per_carta = numero_carte / numero_carte_candidate          (riga 1489)
copie = min(5, disponibili, max(quantita_minima_consigliata, quota_per_carta))
```

Quando i candidati sono pochi rispetto alle carte richieste, ogni candidato riceve comunque la sua quota e **l'ordinamento non cambia la composizione del mazzo**. Conta solo quando i candidati sono molti di più: allora la funzione esce non appena raggiunge `numero_carte` e le carte in coda non vengono mai servite.

Da notare la casualità introdotta alla riga 1495: se `quantita_minima_consigliata` è 0 viene sostituita con `random.randint(1, 3)`, quindi **due esecuzioni con gli stessi ingressi producono mazzi diversi** anche a parità di punteggi.

### 12.7 Gli aggiustamenti `DISTRIBUZIONE_*` non differenziano nulla

L'aggiustamento `potenza *= 1 + percentuale` dipende da `modifica_principale_effettuata()`. Esiti reali su tutto il database:

| Tipo | `combattimento` | `sparare` | `armatura` | `azioni` |
|---|---:|---:|---:|---:|
| Speciale | 10 | 5 | **0** | **165** |
| Equipaggiamento | 55 | 24 | **0** | **0** |

- Per l'**Equipaggiamento** escono solo `combattimento` e `sparare`, a cui `DISTRIBUZIONE_EQUIPAGGIAMENTO` assegna lo stesso valore (0.25): l'aggiustamento è quindi un **+25% costante su ogni carta**, che non modifica alcun ordinamento. Le voci `armatura` e `azioni` sono codice morto.
- Per le **Speciali**, 165 carte su 180 ricadono in `azioni` (+64%), perché `Speciale.modifica_principale_effettuata` restituisce `'azioni'` non appena incontra un effetto che non sia un `Modificatore` con `valore` intero su C/S/A — condizione che, come misurato in [§6.3](#63-perché-tre-tipi-di-carta-hanno-un-punteggio-piatto), soddisfano solo 16 effetti su 187. Anche qui l'aggiustamento è quasi uniforme e la voce `armatura` non viene mai usata.

### 12.8 Verifiche che hanno dato esito positivo

- `carta.tipo.value` (riga 1365) è sicuro: tutti e otto i tipi di carta espongono `tipo` come enum.
- `fazioni` contiene sempre elementi `Fazione` (mai stringhe) per tutti e otto i tipi: il confronto `Fazione.GENERICA in fazioni` alla riga 1317 è corretto.
- `potenza` non inizializzata per un `tipo_carta` fuori dalla catena `if/elif`: il percorso **non è raggiungibile**, perché un tipo sconosciuto non supera il filtro di compatibilità e la lista dei candidati resta vuota (verificato con `tipo_carta='guerriero'`: nessuna eccezione, output vuoto).
- Il numero di carte richiesto viene rispettato esattamente quando la disponibilità lo consente (verificato su cinque tipi di carta).
- Il ciclo `while` termina sempre: la condizione `carte_ancora_disponibili` si basa su `quantita`, che decresce a ogni tornata.

### 12.9 Riepilogo per la fase di ottimizzazione

| Priorità | Punto | Tipo di intervento |
|---|---|---|
| 🔴 | §12.4 `ZeroDivisionError` | Correzione difensiva, 2 righe |
| 🟠 | §12.5 limite di 5 copie | Da imporre esplicitamente (`min(5, …)` cumulativo). Rispettato nell'uso tipico, violato di 1 copia con collezioni strette |
| 🔴 | §10.3 `or 'Doomtrooper'` | Correzione, 1 riga |
| 🟠 | §12.3 filtro `bonus >= 1` | **Decisione**: escludere o declassare? |
| 🟠 | §12.3 Doni degli Apostoli senza bonus OL | Correzione del test sul `tipo` |
| 🔴 | §10.11 confronto stringa/enum su `["Generica"]` | Correzione, 4 righe in 3 file — **il maggior impatto sulla composizione dei mazzi** |
| ⚪ | §12.2 dominanza di `fondamentale` | Nessun intervento: **confermato voluto dall'autore**, le carte `fondamentale` sono indispensabili e a quantità limitata, quindi vanno sempre incluse salvo incompatibilità |
| ⚪ | §12.3 scappatoia generica fondamentale | Nessun intervento: **condizione corretta per disegno**. Il 48% misurato è il sintomo di §10.11, non un difetto del filtro |
| 🟡 | §12.7 `DISTRIBUZIONE_*` inerti | Da rivedere insieme a §6.3 |
| 🟡 | §12.6 `random.randint` nell'allocazione | Rende i mazzi non riproducibili |

### 12.10 ✅ Implementato — declassamento dei Doni di Apostoli fuori orientamento (2026-08-01)

**Intento dichiarato dall'autore.** Se il mazzo è orientato, ad esempio, su Algeroth e Semai, non ha senso includervi Doni di altri Apostoli: nessun guerriero del mazzo potrebbe usarli. Le carte vanno quindi **declassate** nell'ordinamento. La logica deve però tenere conto delle **eccezioni**: guerrieri che, pur non essendo Seguaci di un Apostolo specifico, possono ricevere i Doni di qualsiasi Apostolo.

**Il marcatore dell'eccezione esisteva già nei dati.** `Billy` (Eretico, Personalità dell'Oscura Legione) ha un'abilità dichiarata così:

```json
{"nome": "Riceve Doni Apostoli", "tipo": "Dono degli Apostoli", "costo_destino": 5, ...}
```

È lo stesso schema con cui si dichiarano i guerrieri abilitati all'Arte (`abilita.tipo == "Arte"`), quindi non è stato necessario introdurre nuove convenzioni nel database. Analogamente, l'Apostolo di appartenenza della carta è già nel campo **`apostolo_padre`** (`None` per i Doni generici), che risulta **coerente con la keyword `Seguace di X` in tutte e 35 le carte** — verificato, zero discrepanze.

**Cosa è stato modificato.** Due metodi nuovi in `CreatoreMazzo`:

| Metodo | Risponde a |
|---|---|
| `_guerriero_riceve_doni_di_ogni_apostolo(guerriero)` | Il guerriero ha un'abilità di tipo `"Dono degli Apostoli"`? |
| `_dono_utilizzabile_dai_guerrieri(carta, guerrieri)` | Esiste nel mazzo un Seguace dell'Apostolo della carta, oppure un guerriero che fa eccezione? I Doni generici (`apostolo_padre` nullo) sono sempre utilizzabili |

e la riscrittura del ramo alle righe 1368–1377:

- l'Apostolo della carta si legge da `apostolo_padre` (con ripiego sulla keyword), non più solo dalle keyword;
- se l'Apostolo è nell'orientamento → bonus `BONUS_ORIENTAMENTO × fattore_incremento`, come prima;
- altrimenti, **solo se nessun guerriero del mazzo può ricevere il Dono**, il moltiplicatore viene diviso per `BONUS_ORIENTAMENTO` **con pavimento a 1.0**, così da declassare senza far scattare l'eliminazione della riga 1463;
- se un guerriero-eccezione rende la carta utilizzabile, **nessuna penalità**: la carta resta neutra e si colloca comunque dopo quelle in orientamento, che hanno il bonus ×10.

L'esclusione vera e propria resta compito del filtro di compatibilità (riga 1323), dove concettualmente appartiene — e che tornerà a funzionare per l'Oscura Simmetria una volta corretto §10.9(f).

**Misure.**

| Scenario (orientamento `['Algeroth']`, nessun troncamento) | Carte OS selezionabili |
|---|---|
| Prima | 16 / 35 (19 eliminate dal ÷200) |
| Dopo | **35 / 35**, con i Doni fuori orientamento in fondo all'ordinamento |

Ordine di servizio risultante: ai primi posti i Doni di Algeroth, poi i Doni generici, in coda i Doni di Demnogonis, Muawijhe e Ilian.

Prova con un mazzo di soli Seguaci di Algeroth e 12 carte richieste: selezionati **5 Doni di Algeroth + 2 generici**, **nessun** Dono di altri Apostoli. Aggiungendo Billy al mazzo, i Doni degli altri Apostoli cessano di essere penalizzati (diventano utilizzabili) pur restando dopo quelli in orientamento.

**Verifica end-to-end** sulla pipeline reale (collezione per 3 giocatori, set Base, mazzo 60–80 carte, `orientamento_apostolo=['Algeroth','Semai']`): mazzo di 72 carte, nessun errore, e le 7 carte Oscura Simmetria incluse sono **2 di Algeroth, 2 di Semai e 3 generiche** — nessun Dono di Apostoli fuori orientamento.

---

## 13. Correzione dei difetti §10.9 (2026-08-02)

Intervento unico su sei file di `source/cards/`, con misura della matrice di compatibilità prima e dopo.

### 13.1 Cosa è stato corretto

| # | File | Correzione |
|---|---|---|
| a | `Fortificazione.py` · `Speciale.py` · `Warzone.py` | Guardia invertita `is None or == []` → `is not None and != []`. In `Fortificazione` e `Warzone` il blocco trattava inoltre la lista di restrizioni **come se fosse una stringa**: è stato aggiunto il ciclo `for` mancante, allineandolo al pattern già corretto di `Equipaggiamento.py:210-212` |
| b | `Reliquia.py` · `Warzone.py` | `!= None or != []` → `is not None and != []` |
| c | `Speciale.py` · `Missione.py` | `guerriero.keywords != "Comandante"` → `"Comandante" not in guerriero.keywords` (4 occorrenze) |
| d | `Missione.py` | Sostituito `"Seguace di" == [s[:10] for s in ...]` con `corporazione.startswith("Seguace di")` dentro il ciclo, ed eliminato `self.restrizioni.fazioni_permesse.split(...)` (che avrebbe sollevato `AttributeError`: `self.restrizioni` è una `List[str]`) |
| e | `Missione.py` | `Tipobersaglio.PERSONALITA` → `TipoGuerriero.PERSONALITA`, con l'import mancante |
| f | `Oscura_Simmetria.py` | Le 4 scritture su `risultato["puo_assegnare"]` nel metodo `puo_essere_associata_a_guerriero` sono ora su `risultato["puo_lanciare"]`, la chiave che il chiamante legge |
| + | `Reliquia.py:211` | `self.restrizioni.fazioni_permesse.split(...)` → `corporazione.split(...)` sull'elemento del ciclo. Stesso difetto risolto anche nel gemello `Warzone.py:283` |
| g | `Arte.py` | Vedi §13.2: la correzione dell'operatore non bastava |

**Correzioni collaterali** rese necessarie dal fatto che i blocchi sono ora eseguiti davvero:

- `guerriero.tipo` è un enum `TipoGuerriero`, ma `Speciale.py` lo confrontava con la stringa `"Personalita"` (sempre falso). Corretto in due punti, con l'import mancante.
- Il ramo `"Solo Mercenari o Eretici"` era collocato **dopo** `"Solo Mercenari"`, di cui è un prefisso: era quindi irraggiungibile. Riordinato in `Fortificazione`, `Warzone`, `Reliquia`, `Missione`.
- Nello stesso ramo, `"Mercenario" not in kw or "Eretico" not in kw` è sempre vero per chiunque: bloccava tutti. Corretto in `and`.
- Due messaggi di errore in `Speciale.py` dicevano "Non utilizzabile dalla Fratellanza" nei rami Oscura Legione e Doomtrooper (copia-incolla). Corretti.

### 13.2 (g) — la correzione dell'operatore non era sufficiente

Il difetto documentato era `any(... not in ...)` al posto di `any(... in ...)`. Invertendo l'operatore, però, il risultato è stato **peggiore**: un Maestro non poteva lanciare nemmeno le carte della propria disciplina (misurato: Nicholai 0 carte su 18).

La causa è che il confronto avviene su una **lista**, dove `in` significa uguaglianza esatta, mentre i valori reali del campo `abilita.target` sono frasi che citano una o due discipline:

```
'Tutte le Discipline'                            (9 guerrieri)
'Arte della Manipolazione ed Esorcismo'
'Arte della Cinetica e Arte della Manipolazione'
"Arte Cinetica e Arte d'Evocazione"              ...
```

`"manipolazione" in ["arte della manipolazione ed esorcismo", ...]` è `False`. Serve un confronto **per sottostringa** su ciascun elemento:

```python
lancia_arte_specifica = any( disciplina.lower() in target
                             for target in discipline_arte_guerriero
                             for disciplina in (DisciplinaArte.TUTTE.value, self.disciplina.value) )
```

**Verifica per singolo Maestro** (66 carte Arte, 15 guerrieri Fratellanza):

| Maestro | Discipline dichiarate | Carte delle sue discipline | Carte di altre discipline |
|---|---|---:|---:|
| Laura Vestale Benedetta | Tutte le Discipline | 66 / 66 | — |
| Mortificator | Cinetica e Manipolazione | 19 / 19 | **0** / 47 |
| Arcangelo | Cambiamento ed Elementi | 16 / 16 | **0** / 50 |
| Antiquario | Cinetica ed Evocazione | 15 / 15 | **0** / 51 |
| Nicholai | Manipolazione ed Esorcismo **+ Incantesimi Personali** | 18 / 18 | 13 / 48 |

Tutti i Maestri lanciano ora **tutte e sole** le carte delle proprie discipline. L'unica eccezione, Nicholai, è **voluta**: possiede anche l'abilità "Incantesimo di Combattimento Personale", e il ramo `lancia_incantesimi_combattimento_personale` gli consente di lanciare qualsiasi carta di tipo *Incantesimo Personale di Combattimento* a prescindere dalla disciplina. Se questa lettura del regolamento §5 non è quella voluta, è il prossimo punto da rivedere.

### 13.3 Misure

Matrice completa carta × guerriero su un campione di 14 guerrieri rappresentativi (Doomtrooper, Fratellanza con e senza "Tutte le Discipline", Oscura Legione, Seguaci, Eretici, Nefarita, Mercenari, Comandanti): **5950 coppie, 0 eccezioni**.

Confronto prima/dopo sul campione iniziale (4675 coppie): **135 variazioni**.

| Tipo | Variazione | Coppie |
|---|---|---:|
| Oscura Simmetria | compatibile → **non** compatibile | 107 |
| Reliquia | non compatibile → **compatibile** | 22 |
| Speciale | compatibile → **non** compatibile | 5 |
| Missione | compatibile → **non** compatibile | 1 |

Le 107 variazioni sull'Oscura Simmetria sono l'effetto di (f): il vincolo "solo Seguaci di quello specifico Apostolo" finalmente filtra. Le 22 sulle Reliquie sono l'effetto di (b): con `or` il blocco girava sempre, anche a restrizioni vuote, bloccando carte che non avevano alcuna restrizione.

**Eccezione preservata:** il controllo sull'Apostolo in `Oscura_Simmetria.py` riconosce ora anche i guerrieri con abilità di tipo `"Dono degli Apostoli"` (es. Billy), coerentemente con la logica introdotta in §12.10. Senza questa aggiunta, la correzione di (f) avrebbe bloccato Billy contraddicendo il suo testo carta.

**Verifiche di non regressione:** tutte le 561 carte dei 9 database continuano a istanziarsi (0 fallimenti); la pipeline end-to-end genera correttamente 3 mazzi da 3 collezioni distinte (63–71 carte, nessun errore).

### 13.4 Cosa resta aperto

- **§10.11** (confronto `!= ["Generica"]` stringa/enum) **non è stato toccato**: era indicato come da applicare insieme a (a), quindi finché resta, le carte generiche di Speciale, Equipaggiamento e Fortificazione continuano a risultare incompatibili con ogni guerriero.
- §12.4 `ZeroDivisionError` con mazzo senza guerrieri ammessi.
- §12.5 limite di 5 copie non imposto — riscontrato di nuovo nella verifica end-to-end: uno dei tre mazzi generati contiene una carta in **6 copie**.

---

## 14. Correzione di §10.11 e pulizia §10.10 (2026-08-02)

### 14.1 §10.11 — confronto stringa/enum sulle carte generiche

Corretti i quattro punti in cui `fazioni_permesse` (lista di membri dell'enum `Fazione`) veniva confrontata con la lista di stringhe `["Generica"]`:

| File:riga | Correzione |
|---|---|
| `Speciale.py:250` | `!= ["Generica"]` → `!= [Fazione.GENERICA]` |
| `Equipaggiamento.py:279` | idem |
| `Fortificazione.py:254` | idem, più rimozione della clausola ridondante (vedi sotto) |
| `Equipaggiamento.py:147` | in `set_fazioni_permesse` il parametro è una **stringa singola**: `!= ["Generica"]` → `!= "Generica"` |

**Clausola rimossa in `Fortificazione.py`.** L'espressione era:

```python
if self.fazioni_permesse != ["Generica"] or (self.fazioni_permesse == ["Doomtrooper"] and guerriero.fazione not in DOOMTROOPER):
```

Il secondo operando è **logicamente irraggiungibile a prescindere dai dati**: se le fazioni valgono `["Doomtrooper"]` allora sono già diverse da `["Generica"]`, quindi il primo operando è vero e l'`or` cortocircuita. È inoltre inapplicabile ai dati reali — `"Doomtrooper"` non è un valore dell'enum `Fazione`, e nessuna delle 26 Fortificazioni lo usa (le carte per tutti i Doomtrooper elencano le 7 fazioni per esteso). Conteneva infine un terzo difetto: `guerriero.fazione not in DOOMTROOPER` confronta un enum con una lista di stringhe, ed è quindi sempre vero.

**Stesso difetto corretto in `Speciale.py:309`**, dove `guerriero.fazione in DOOMTROOPER` (enum contro lista di stringhe, sempre falso) rendeva inefficace il ramo `"Non utilizzabile dai Doomtroopers"` — difetto latente diventato raggiungibile con la correzione di §10.9(a). Ora confronta `guerriero.fazione.value`.

### 14.2 Misure

Matrice carta × guerriero su 14 guerrieri rappresentativi (5950 coppie, **0 eccezioni**):

| Tipo | Variazione | Coppie |
|---|---|---:|
| Speciale | non compatibile → **compatibile** | 1790 |
| Equipaggiamento | non compatibile → **compatibile** | 353 |
| Fortificazione | non compatibile → **compatibile** | 86 |

**Totale: 2229 coppie su 5950.** Le compatibilità complessive passano da 1014 a 3243. È di gran lunga la correzione con l'impatto maggiore sulla composizione dei mazzi, come previsto in §10.11.

**Verifica dei due strati insieme.** Il rischio segnalato era di passare da "troppo restrittivo" a "troppo permissivo". Misurato:

- *Strato 1 (fazione).* Le 134 Speciali generiche risultano ora compatibili con **127–128 guerrieri su 134** per ciascun profilo provato (Doomtrooper, Oscura Legione, Eretico, Fratellanza). Le 6-7 escluse sono quelle che portano anche una restrizione testuale: corretto.
- *Strato 2 (testo carta).* Prova con caso positivo **e** negativo per ciascuna restrizione, come raccomandato in §11 punto 13:

| Restrizione | Carta | Guerriero idoneo | Guerriero non idoneo | Esito |
|---|---|---|---|---|
| `Solo Eretici` | Maestro Corrotto | Billy (kw `Eretico`) → **True** | Blood Beret → **False** | ✅ |
| `Solo Oscura Legione` | L'Eletto | Karnofago → **True** | Blood Beret → **False** | ✅ |

I due strati funzionano ora come previsto dal regolamento §5-§6: la fazione filtra a grana grossa, il testo della carta prevale a grana fine.

### 14.3 §10.10 — pulizia

Rimossa da `seleziona_guerrieri` la stampa di debug con linguaggio scurrile, insieme al ramo `else` che la conteneva: era **irraggiungibile** (scattava solo se il guerriero risultava in `guerrieri_ammessi` ma non in `punteggi`, condizione che `_assegnazione_punteggio_guerriero_ammesso` rende impossibile, dato che popola entrambi). Il ramo `elif guerriero.nome in punteggi` è diventato quindi un `else` diretto, e i commenti ripetuti sono stati sostituiti da una nota unica. Verificato: nessuna occorrenza residua in tutto `source/`.

### 14.4 Non regressione

Tutte le 561 carte dei 9 database si istanziano (0 fallimenti). Pipeline end-to-end su 3 collezioni distinte: mazzi da 60, 67 e 72 carte, nessun errore, distribuzione dei tipi di supporto regolare.

### 14.5 Cosa resta aperto

- §12.4 `ZeroDivisionError` quando l'orientamento non ammette alcun guerriero.
- §12.5 limite di 5 copie non imposto.
- §6.3 / §10.7 punteggi inerti per Arte, Speciale e Oscura Simmetria (vocabolario e tipi degli `effetti`).
- §10.1 / §10.2 / §10.3 / §10.5 i quattro difetti di Fascia 1 nei due moduli di logica.
- §13.2 da decidere: se un Maestro con l'abilità "Incantesimo di Combattimento Personale" debba poter lanciare incantesimi personali **di qualsiasi disciplina** (comportamento attuale) o solo delle proprie.

---

## 15. Correzione di §12.4 e §12.5 (2026-08-02)

### 15.1 §12.4 — mazzo senza guerrieri ammessi

Il crash non nasceva da una collezione priva di guerrieri (impossibile per disegno) ma da una selezione **vuota**: poiché l'orientamento in `seleziona_guerrieri` è un filtro rigido, un orientamento che non corrisponde ad alcun guerriero della collezione produce `[], []`.

Correzione su due livelli:

1. **`crea_mazzo_da_gioco`** interrompe la creazione subito dopo `seleziona_guerrieri` se entrambe le liste sono vuote, restituendo la stessa struttura usata per gli altri errori di validazione, con il messaggio *"Nessun guerriero selezionabile: la collezione non contiene guerrieri compatibili con le fazioni e gli orientamenti richiesti"*. È il livello dove il vincolo appartiene: un mazzo non può esistere senza guerrieri (regolamento §2).
2. **`seleziona_carte_supporto`** conserva una guardia difensiva sul calcolo di `fattore_compatibilita` (`... if numero_guerrieri else 1.0`), per l'eventualità di un'invocazione diretta della funzione.

**Verificato:** lo scenario che prima sollevava `ZeroDivisionError` restituisce ora `squadra=0, schieramento=0` e l'elenco errori popolato, senza eccezioni.

### 15.2 §12.5 — limite di 5 copie per carta

Introdotta la costante `MAX_COPIE_PER_CARTA_MAZZO = 5` con riferimento esplicito al regolamento §2. Il difetto non era il `min(5, ...)` in sé ma il fatto che limitasse la **singola tornata**, mentre il ciclo `while` esterno ripercorre l'intera lista accumulando su `quantita_utilizzata`. La correzione scala il tetto di quanto già inserito:

```python
copie_ancora_ammesse = MAX_COPIE_PER_CARTA_MAZZO - quantita_utilizzata[nome]
num_copie_da_inserire = max(0, min(copie_ancora_ammesse, quantita_disponibile, quantita_consigliata))
```

applicata **in entrambi** i punti di selezione (`seleziona_guerrieri` e `seleziona_carte_supporto`).

**Condizione di terminazione aggiornata.** Con il solo cap, il ciclo `while` non sarebbe più terminato: la verifica `carte_ancora_disponibili` guardava `quantita - quantita_utilizzata > 0`, vero anche per una carta già a 5 copie ma con 6 disponibili, mentre `num_copie_da_inserire` sarebbe rimasto 0 all'infinito. Ora il residuo è calcolato come:

```python
residuo = min(quantita, MAX_COPIE_PER_CARTA_MAZZO) - quantita_utilizzata[nome]
```

**Misure sullo scenario che prima violava il limite** (collezione stretta: 15 Speciali distinte × 6 copie):

| Carte richieste | Prima: ottenute / max copie / oltre 5 | Dopo: ottenute / max copie / oltre 5 |
|---:|---|---|
| 20 | 20 / 3 / 0 | 20 / 2 / **0** |
| 60 | 42 / **6** / **7** | 60 / 5 / **0** |
| 90 | 42 / **6** / **7** | 65 / 5 / **0** |
| 100000 | — | 65 / 5 / **0** (termina) |

Lato guerrieri (4 guerrieri Imperiali × 6 copie): con target 25 e 60 si ottengono 20 guerrieri, cioè esattamente il massimo teorico 4 × 5, senza superare le 5 copie e senza bloccarsi.

**Verifica end-to-end su 4 collezioni:** mazzi da 62–77 carte, **0 violazioni del limite** (prima, con gli stessi parametri, uno dei mazzi conteneva una carta in 6 copie).

### 15.3 Nicholai — interpretazione confermata

La questione lasciata aperta in §13.2 è chiusa. L'utente conferma: un Maestro che possiede sia una o più discipline sia l'abilità *"Incantesimo di Combattimento Personale"* può lanciare gli incantesimi personali **di qualsiasi disciplina, purché siano incantesimi di combattimento**.

Il comportamento attuale del codice corrisponde già a questa lettura: **verificato** che tutte e 13 le carte lanciabili da Nicholai fuori dalle sue discipline (Cinetica, Elementi, Mentale) sono di tipo `Incantesimo Personale di Combattimento` — nessuna carta di altro tipo passa. Nessuna modifica necessaria.

---

## 16. Correzione dei quattro difetti di Fascia 1 (2026-08-02)

Correzioni applicate insieme, con confronto prima/dopo sui **due livelli distinti** della pipeline: la **Collezione** (sottoinsieme del totale delle carte dei moduli `data_base_cards`, scelto per criteri) e il **Mazzo** (sottoinsieme di una Collezione di riferimento).

### 16.1 Interventi

| # | File:riga | Correzione |
|---|---|---|
| §10.1 | `Creatore_Collezione.py:747-753` | `fazioni_permesse` è ora ricostruita a ogni carta (`= [dati.get('fazione')]`) invece di essere accumulata con `.append()` su una lista dichiarata fuori dal ciclo |
| §10.2 | `Creatore_Mazzo.py:1004` · `Creatore_Collezione.py:1218` | Sostituita l'espressione condizionale mal raggruppata con un confronto reale su un insieme di valori normalizzati |
| §10.3 | `Creatore_Mazzo.py:1386` | Rimosso `or 'Doomtrooper'` |
| §10.5 | `Creatore_Mazzo.py:1204` | `if q and q < 1:` → `if q < 1:` |

**Dettaglio su §10.2.** La correzione non poteva limitarsi a `if set_carta in espansioni_richieste`: `set_espansione` è una **stringa in sette classi carta su nove**, ma un enum `Set_Espansione` in `Fortificazione` e `Reliquia`. Un confronto diretto avrebbe escluso sistematicamente quelle due classi. Entrambi i lati vengono ora normalizzati al valore testuale:

```python
espansioni_valide = {str(getattr(e, 'value', e)) for e in espansioni_richieste}
set_carta = str(getattr(carta.set_espansione, 'value', carta.set_espansione))
```

### 16.2 Livello COLLEZIONE — §10.1

Misura mirata: chiamata diretta a `seleziona_carte_casuali_per_tipo` con orientamento su **una sola fazione** e 60 copie di guerrieri richieste (`probabilita_orientamento` = 0.7).

| Orientamento | Prima | Dopo |
|---|---|---|
| `[Mishima]` | 10/62 = **16.1%** | 36/61 = **59.0%** |
| `[Bauhaus]` | 3/61 = **4.9%** | 28/60 = **46.7%** |
| `[Cybertronic]` | 9/62 = **14.5%** | 33/60 = **55.0%** |

Prima della correzione l'orientamento era di fatto ignorato (la quota coincideva con la presenza casuale della fazione nel database). Ora la quota si avvicina alla probabilità richiesta; resta sotto il 70% perché il pool orientato si esaurisce — le carte di una singola fazione sono poche — e perché le carte generiche fondamentali vengono aggiunte al pool a ogni estrazione.

Con gli orientamenti generati automaticamente da `genera_fazioni_orientamento_casuali` l'effetto è meno visibile, perché quelle combinazioni comprendono 6-7 fazioni su 8: è il motivo per cui era servita una misura mirata.

### 16.3 Livello MAZZO — §10.2 e §10.3

Quattro mazzi generati dalle quattro collezioni, chiedendo **solo l'espansione Base** e orientamento Arte `['Mentale','Cinetica']`.

**§10.2 — rispetto dell'espansione richiesta:**

| | Prima: carte fuori da Base | Dopo |
|---|---|---|
| mazzo 1 | 30 su 60 (`Inquisition` 20, `Warzone` 10) | **0** su 73 |
| mazzo 2 | 43 su 75 (`Inquisition` 31, `Warzone` 12) | **0** su 66 |
| mazzo 3 | 31 su 61 (`Inquisition` 25, `Warzone` 6) | **0** su 62 |
| mazzo 4 | 35 su 72 (`Inquisition` 25, `Warzone` 10) | **0** su 62 |

Circa **metà di ogni mazzo** proveniva da espansioni non richieste.

**§10.3 — rispetto dell'orientamento Arte:**

| | Prima | Dopo |
|---|---|---|
| mazzo 1 | 1/6 = 16.7% | 5/7 = **71.4%** |
| mazzo 2 | 4/10 = 40.0% | 8/8 = **100%** |
| mazzo 3 | 4/8 = 50.0% | 0/0 — *(vedi sotto)* |
| mazzo 4 | 5/9 = 55.6% | 5/8 = **62.5%** |

**Il mazzo 3 esce con zero carte Arte, ed è corretto.** La sua squadra contiene 8 guerrieri (Cybertronic, Bauhaus, Mishima, Imperiale) e **nessun guerriero della Fratellanza**: senza Maestri, nessuna carta Arte è compatibile e il filtro di compatibilità le esclude tutte — coerente con il regolamento §5. Prima delle correzioni quel mazzo riceveva 8 carte Arte che nessuno avrebbe potuto lanciare.

### 16.4 §10.5 — euristica riattivata

Prova forzando `quantita_minima_consigliata = 0` su tutti i guerrieri della collezione, il caso che prima avrebbe prodotto un ciclo infinito:

| Target guerrieri | Ottenuti | Copie per carta |
|---:|---:|---|
| 8 | 8 | 2, 2, 4 |
| 20 | 15 | 5, 5, 5 |
| 40 | 15 | 5, 5, 5 |

Nessun blocco, e l'euristica assegna ora le copie in base al Valore del guerriero invece di lasciare 0. Il tetto delle 5 copie (§15.2) è rispettato.

### 16.5 Effetti collaterali da tenere presenti

Due conseguenze legittime ma da conoscere, emerse nella verifica:

1. **I mazzi possono risultare più piccoli del minimo richiesto.** Con il filtro espansioni finalmente operativo, una collezione povera nell'espansione richiesta produce meno candidati. Nella regressione finale una delle quattro collezioni ha prodotto un mazzo da 56 carte, con l'errore già previsto dal codice: *"Il mazzo ha 56 carte, meno del minimo richiesto (60)"*. Non è un difetto: è il vincolo che prima veniva aggirato includendo carte di altre espansioni.
2. **Le quote di `calcola_distribuzione_carte` possono restare non riempite.** La distribuzione assegna slot per tipo di carta *prima* di sapere quali guerrieri entreranno nel mazzo: se il mazzo non ha Maestri, i 6 slot per l'Arte del mazzo 3 semplicemente non vengono usati, e non sono redistribuiti fra gli altri tipi. È un'inefficienza da valutare in un intervento successivo.

### 16.6 Non regressione

Tutte le 561 carte dei 9 database si istanziano (0 fallimenti). Regressione finale su 4 collezioni (393–603 carte ciascuna) con mazzi su `['Base','Inquisition']`: **0 violazioni del limite di 5 copie, 0 carte fuori dalle espansioni richieste**, nessuna eccezione.

---

## 17. Ridistribuzione a posteriori degli slot non riempiti (2026-08-02)

### 17.1 Il problema

`calcola_distribuzione_carte` conteneva già una ridistribuzione, ma **a priori**: righe 1711–1740, redistribuisce le quote dei tipi esclusi *dalla richiesta* (niente Fratellanza → gli slot Arte vanno a equipaggiamento/speciale/fortificazione secondo `RIDISTRIBUZIONE_PERCENTUALE`). Funziona correttamente.

Mancava la ridistribuzione **a posteriori**: quando un tipo è richiesto ma non riesce a riempire la quota perché il pool compatibile è più piccolo. I due casi vivono in punti diversi — il primo in `calcola_distribuzione_carte`, che conosce la richiesta; il secondo solo in `crea_mazzo_da_gioco`, che conosce i risultati.

**Deficit misurato** su 4 mazzi, due configurazioni:

| Tipo | Richieste | Ottenute | Deficit |
|---|---:|---:|---:|
| Missione | 15 | 1 | **14** |
| Oscura Simmetria | 29 | 26 | 3 |
| Arte *(mazzo senza Maestri)* | 6–8 | 0 | 6–8 |
| **Totale** | 226 | 209 | **17 (7,5%)** |

Il grosso è strutturale su **Missione**: il database ne contiene 7 in tutto, ma la quota chiede `random.randint(2,5)` copie e quasi tutte risultano incompatibili.

### 17.2 La soluzione implementata

Gli otto blocchi ripetuti di `crea_mazzo_da_gioco` sono stati sostituiti da un ciclo su `tipi_ammessi` più una passata di compensazione. Regole concordate:

- **Ricevono solo i tipi che hanno saturato la quota.** Un tipo già in deficit ha esaurito il proprio pool compatibile e non ha altre carte da offrire.
- **I guerrieri restano fuori.** Aggiungerne cambierebbe la squadra e quindi la compatibilità di tutte le carte di supporto già scelte, obbligando a rifare l'intera pipeline.
- I pesi riusano `RIDISTRIBUZIONE_PERCENTUALE`, rinormalizzati sui soli tipi capienti; per i tipi assenti da quella tabella si usa `PESO_RIDISTRIBUZIONE_DEFAULT = 0.10`. Al massimo `MAX_GIRI_RIDISTRIBUZIONE = 2` giri.

**Perché la ri-selezione sostituisce il risultato invece di aggiungersi.** `seleziona_carte_supporto` conta le copie già inserite in una variabile **locale alla singola chiamata**. Concatenare i risultati di due chiamate per lo stesso tipo farebbe ripartire da zero quel conteggio, permettendo a una carta di superare le 5 copie e vanificando la correzione di §15.2. Ri-chiamando la funzione con la quota maggiorata e sostituendo il risultato, tutta la contabilità resta dentro una sola invocazione.

**Il residuo si misura sulla dimensione del mazzo, non sommando i deficit per tipo.** È l'errore in cui è incappata la prima stesura di questa modifica: un tipo strutturalmente incapiente come Missione conserva il proprio deficit a ogni giro, quindi sommando i deficit lo si compensava **due volte**. Nella misura intermedia i mazzi arrivavano a 82–86 carte contro un target massimo di 80. Legando il residuo a `numero_carte_target - totale_attuale` il problema sparisce, perché il totale viene ricalcolato a ogni giro. In più, la somma dei supplementi è limitata al residuo, così l'arrotondamento non può far sforare.

### 17.3 Misure

Quattro collezioni, mazzi con target 60–80 carte:

| Configurazione | | Prima | Dopo |
|---|---|---|---|
| **Base + Inquisition** | mazzi sotto il minimo | 0/4 | 0/4 |
| | carte totali | 273 | **299** |
| **solo Base** | mazzi sotto il minimo | **2/4** | **0/4** |
| | carte totali | 241 | **306** |

Dettaglio della configurazione più stretta ("solo Base"):

| | Prima | Dopo |
|---|---|---|
| mazzo 1 | 65 | 75 |
| mazzo 2 | 59 ⚠️ sotto il minimo | 77 |
| mazzo 3 | 60 | 75 |
| mazzo 4 | 57 ⚠️ sotto il minimo | 72 |

Nessun mazzo supera il massimo di 80. La composizione si sposta verso i tipi capienti: nel mazzo 1 di Base+Inquisition, equipaggiamento 7→9, fortificazione 4→6, speciale 29→33, arte 7→9, reliquia 4→6.

### 17.4 Non regressione

Regressione su 5 collezioni nella configurazione più stretta (`['Base']`): mazzi da 64–79 carte, **0 sotto il minimo, 0 sopra il massimo, 0 violazioni del limite di 5 copie, 0 carte fuori dall'espansione richiesta**, nessun errore. Tutte le 561 carte dei 9 database continuano a istanziarsi. Il costo dei giri di ri-selezione è trascurabile (l'intera generazione di 5 collezioni e 5 mazzi resta sotto il secondo), perché i punteggi sono già in cache in `potenze_calcolate`.

---

## 18. Punteggi di Arte, Speciale e Oscura Simmetria (§6.3 / §10.7) — corretto il 2026-08-02

### 18.1 Scelta di fondo: rendere tollerante il codice, non normalizzare i dati

`tipo_effetto` e `statistica_target` sono consumati dai metodi `applica_effetto` delle classi carta, cioè dal motore di gioco. Modificarli nei database per compiacere il calcolo di potenza avrebbe rotto quel consumatore. Si è quindi allineato **il codice di punteggio al vocabolario realmente presente nei dati**, come già fatto per `STATISTICHE_MODIFICATORI` in §1quinquies dell'audit.

### 18.2 `_calcola_potenza_carta_stats`

Il filtro richiedeva `isinstance(valore, int) and valore > 0` e un `statistica_target` fra sei valori esatti. Nei database `valore` è stringa in 67 casi su 187 (Speciale), 38 su 67 (Arte) e **35 su 35** (Oscura Simmetria); `statistica_target` conta 25 forme diverse, fra cui `"tutte"`, elenchi in linguaggio naturale (`"combattimento e sparare"`) e sinonimi (`"attacco"`, `"sparatoria"`).

Correzioni:
- `valore` normalizzato con `valore_numerico_modificatore()`, l'helper già introdotto in §1quinquies (gestisce `2` e `"+2"`);
- introdotta `numero_statistiche_combattimento()`, che conta **quante** statistiche C/S/A un effetto tocca: 0 per `""`/`"nessuna"`/`"varie"`, 3 per `"tutte"`, altrimenti il numero di statistiche canoniche citate, con i sinonimi raccolti in `SINONIMI_STATISTICHE_EFFETTI`;
- il contributo diventa `valore × numero_statistiche`: un `+2` su tutte le statistiche vale più di un `+2` su una sola.

### 18.3 `_calcola_potenza_carta_azioni`

La funzione cercava `tipo_effetto` fra `"danno"`, `"azione fase"` e `"azione ogni momento"`: **nessuno dei tre compare in alcuna carta**. I valori reali sono `Modificatore` (189), `Carte` (44), `Arte` (15), `Combattimento` (14), `Immunita` (10), `Guarigione` (8), `Controllo` (7), `Azione Combattimento` (1), `Scarto_Carte` (1). La funzione restituiva quindi 1.0 fisso per 281 carte su 282.

I rami sono stati riscritti sul vocabolario reale, riusando **gli stessi fattori che il modulo applica già alle abilità equivalenti di guerrieri ed equipaggiamenti**, così che le scale restino confrontabili: `Combattimento` ×2.0 se uccide, ×1.4 se ferisce automaticamente, ×1.5/×1.4 per gli scarti, ×1.2 altrimenti; `Carte`/`Scarto_Carte` ×1.3 (×1.5 se scarta un guerriero); `Immunita` ×1.4; `Guarigione` e `Arte` ×1.3; `Controllo` ×1.2; i tipi `Azione *` conservano il moltiplicatore numerico, raddoppiato per "ogni momento".

### 18.4 Misure

| Tipo | n | min | mediana | max | **valori distinti** |
|---|---:|---|---|---|---|
| Speciale | 180 | 2.0 → 2.0 | 2.0 → 2.0 | 8.0 → **11.0** | 7 → **13** |
| Arte | 66 | 2.0 → 2.0 | 2.0 → **2.3** | 3.0 → **8.0** | 2 → **9** |
| Oscura Simmetria | 35 | 2.0 → 2.0 | 2.0 → **2.2** | 2.0 → **12.0** | **1 → 10** |

L'Oscura Simmetria passa da **un solo valore per tutte e 35 le carte** a dieci livelli distinti. Verifica a campione della plausibilità:

- `Forza Malvagia` (+5 su più statistiche) → **12.0**, il punteggio più alto;
- `Forza Empia` (+4 sulle stesse) → **10.0**;
- `Cecita` (`valore` `-2`, penalità) → resta **2.0**, correttamente non premiata.

Nessun errore su 281 carte valutate. Nei mazzi la dimensione non cambia (76/63/77/70 identici prima e dopo) e l'ordine di servizio delle carte S/A/OS si riordina: come già documentato in §12.2, `fondamentale` domina il punteggio, quindi l'effetto sulla composizione resta contenuto — il beneficio è sul **ranking interno** fra carte non fondamentali.

### 18.5 Due limiti emersi, da valutare separatamente

1. **Quattro carte hanno un `statistica_target` incoerente col proprio testo.** `Forza Malvagia`, `Forza Empia` e altre due riportano `"combattimento, sparare, azioni e velocità"` mentre il testo carta dice "+N in **C, S, A e V**": "azioni e velocità" non corrisponde ad Armatura e Valore. Il valore corretto sarebbe `"tutte"`. Sono quindi contate 2 statistiche invece di 3 e le carte risultano sottostimate. È un difetto di **dati**, da trattare in `AUDIT_DATABASE_CARTE_CORREZIONI.md` verificando prima l'impatto su `Oscura_Simmetria.applica_effetto`.
2. **Le penalità inflitte all'avversario non sono valorizzate.** `statistica_target` non distingue se il modificatore agisce sul proprio guerriero o sull'avversario, quindi un `-2` è sempre scartato come penalità. `Cecita` (−2 a C ed S *degli avversari*) è di fatto un potenziamento, ma vale il minimo. Servirebbe un campo che distingua il bersaglio del modificatore.

### 18.6 Non regressione

561 carte istanziate, 0 fallimenti. Regressione su 5 collezioni con mazzi su `['Base']`: 64–79 carte, **0 sotto il minimo, 0 sopra il massimo, 0 violazioni del limite di 5 copie, 0 carte fuori espansione**, nessun errore.

---

## 19. Modificatori inflitti all'avversario (2026-08-02)

### 19.1 La segnalazione

La §18.5 affermava che per valorizzare le carte che *riducono* le caratteristiche dei guerrieri avversari "servirebbe un campo che distingua il bersaglio". **L'affermazione era sbagliata: quel campo esiste già**, anche se codificato in modi diversi a seconda del modulo. Su una carta rivolta all'avversario la convenzione di segno si inverte — più il modificatore è negativo, più la carta è efficace.

### 19.2 Situazione per tipo di carta

| Tipo | Dove è codificato il bersaglio | Modificatori negativi | Valutazione |
|---|---|---:|---|
| Speciale | campo `bersaglio` — 8 carte "Avversario" | 3 | da correggere |
| Arte | campo `bersaglio` — 5 carte | 1 | da correggere |
| Oscura Simmetria | campo `bersaglio` — 16 carte | 6 | da correggere |
| Equipaggiamento | nel **nome della statistica**: `"combattimento dell'avversario"` | 2 | da correggere, doppiamente: il nome non era nemmeno riconosciuto come statistica di combattimento |
| Fortificazione | `beneficiario` (Tutti / Corporazione Specifica) | 1 — `Trincea` `C −2` | ✅ già corretto: è una penalità al **proprio** guerriero, va scartata |
| Warzone | `modificatori_difensore`, sempre il proprio difensore | 3 — `Rifugio Sacro` | ✅ già corretto |
| Reliquia | — | 0 | non applicabile |

Tre tipi su sette erano quindi già trattati correttamente, perché in quei moduli un valore negativo è davvero una penalità subita.

### 19.3 Correzione

Tre funzioni di modulo nuove, più l'estensione di una esistente:

- `bersaglio_e_avversario(carta)` — legge il campo `bersaglio` di Speciale/Arte/Oscura Simmetria e riconosce le forme che contengono "Avversar";
- `statistica_penalizza_avversario(statistica)` — riconosce le forme `"<statistica> dell'avversario"` usate dall'Equipaggiamento;
- `valore_efficace_modificatore(valore, contro_avversario)` — restituisce il contributo col segno corretto: su bersaglio avversario inverte il segno, altrove scarta i negativi. È ora l'unico punto in cui la regola è espressa;
- `statistica_di_combattimento()` riconosce anche i nomi con suffisso (`"combattimento dell'avversario"`), che prima venivano scartati del tutto — chiude anche l'osservazione lasciata aperta in §1quinquies dell'audit;
- `livello_bonus_modificatore()` accetta il parametro `contro_avversario` e viene invocata con esso nei tre punti di calcolo (Equipaggiamento, Fortificazione, Warzone).

> ⚠️ **Falso positivo evitato.** La prima stesura del riconoscimento per prefisso usava tutti i valori di `STATISTICHE_MODIFICATORI`, incluse le sigle di una lettera: `"azioni"` inizia per `"a"` (armatura) e veniva quindi classificata come statistica di combattimento. Il controllo per prefisso è ora limitato ai nomi per esteso.

### 19.4 Misure

| Tipo | Distinti: originale → §18 → §19 | Max |
|---|---|---|
| Speciale | 7 → 13 → 13 | 8.0 → 11.0 → 11.0 |
| Arte | 2 → 9 → 9 | 3.0 → 8.0 → 8.0 |
| Oscura Simmetria | 1 → 10 → 10 | 2.0 → 12.0 → 12.0 |

Carte il cui punteggio cambia per effetto della sola gestione del bersaglio:

| Carta | Prima | Dopo |
|---|---|---|
| `Cecita` (−2 a C e S degli avversari) | 2.0 | **6.0** |
| `Danza Folle` (−2 a C e S degli avversari) | 2.0 | **6.0** |
| `Scalper` (−1 al combattimento dell'avversario) | escluso dal conteggio | **2.2** |
| `Granata Batteriologica` (−1 al valore dell'avversario) | escluso | **9.0** |

**Perché le altre carte con valori negativi non cambiano**, ed è corretto così: `Terrore`, `Deformazione` e `Indigestione` hanno `statistica_target = "azioni"`, che non è una statistica di combattimento (C/S/A) e quindi non contribuisce; `Untore` ha `bersaglio = "Doomtrooper"` invece di una forma "Avversario" — caso ambiguo, lasciato invariato e segnalato di seguito.

### 19.5 Resta da decidere

`Untore` (Oscura Simmetria, −2 a un Doomtrooper) dichiara il bersaglio per **fazione** anziché con "Avversario". Per un mazzo Oscura Legione un Doomtrooper è un avversario, ma la stessa carta letta da un mazzo misto non lo sarebbe necessariamente. Le opzioni sono normalizzare il campo `bersaglio` di quella carta oppure dedurre l'ostilità confrontando la fazione bersaglio con quelle del mazzo. Non affrontato: riguarda una sola carta e richiede una scelta di modello.

### 19.6 Non regressione

561 carte istanziate, 0 fallimenti. Cinque collezioni con mazzi su `['Base']`: 64–79 carte, **0 sotto il minimo, 0 sopra il massimo, 0 violazioni del limite di 5 copie, 0 carte fuori espansione**, nessun errore.

---

## 20. `Untore` e i pesi su bonus e penalità (2026-08-02)

### 20.1 `Untore`: bersaglio normalizzato

Il testo della carta — *"Ogni Doomtrooper che combatte questo guerriero è infetto"* — chiarisce che il Dono si assegna a un proprio guerriero dell'Oscura Legione e colpisce i Doomtrooper avversari. Il campo `bersaglio` dichiarava però la **fazione** (`"Doomtrooper"`) anziché la relazione, restando fuori dal riconoscimento introdotto in §19. Normalizzato a `"Guerriero Avversario"`, valore già usato da 14 carte dello stesso database e presente nell'enum `BersaglioOscura`.

### 20.2 Un difetto di dati emerso durante la correzione

Normalizzare il solo `bersaglio` non avrebbe però cambiato nulla: l'effetto di `Untore` dichiara `statistica_target = "azioni"`, che non è una statistica di combattimento. Ma il testo della carta dice *"I Segnalini danno un **-2 in A**"* — cioè Armatura.

Il controllo sistematico ha trovato **5 carte Oscura Simmetria** nella stessa condizione: `statistica_target = "azioni"` mentre il testo parla esplicitamente di `A` e non menziona affatto le azioni.

| Carta | Valore | Testo |
|---|---|---|
| `Terrore` | −1 | "…un −1 in A" |
| `Resistere Al Dolore` | +1 | "Il guerriero guadagna un +1 in A" |
| `Deformazione` | −2 | "…un −2 in A" |
| `Indigestione` | −2 | "…una penalità un −2 in A" |
| `Untore` | −2 | "I Segnalini danno un −2 in A" |

Tutte le altre carte con `"azioni"` parlano davvero di azioni: il difetto è circoscritto a queste cinque.

**L'impatto andava oltre il punteggio.** `Oscura_Simmetria._applica_singolo_effetto` passa `statistica_target` a `Guerriero.applica_modificatore`, che accetta solo `['combattimento', 'sparare', 'armatura', 'valore']` e **ignora silenziosamente** ogni altro valore: su quelle 5 carte il modificatore non aveva effetto nemmeno nel motore di gioco. Corretto in `"armatura"`.

### 20.3 Pesi su bonus e penalità

Molte carte potenziano una statistica penalizzandone contemporaneamente un'altra — il caso tipico è la `Trincea`, +2 in Armatura e −2 in Corpo a corpo. Fino ad ora la penalità veniva semplicemente **ignorata**, quindi la Trincea valeva quanto una Fortificazione che desse solo il +2.

Introdotti due pesi:

```python
PESO_MODIFICATORE_POSITIVO = 0.65
PESO_MODIFICATORE_NEGATIVO = 0.35
```

La penalità pesa, ma meno del bonus: è il giocatore a scegliere quando esporsi allo svantaggio. Conseguenze sulla struttura del codice:

- `valore_efficace_modificatore()` restituisce ora il contributo **con segno** (positivo = vantaggio per il giocatore, già invertito per le carte rivolte all'avversario) invece di scartare i negativi;
- `livello_bonus_modificatore()` restituisce una **fascia con segno** (±1 piccolo, ±2 medio, ±3 grande);
- `_applica_bonus_modificatore()` applica il peso corrispondente e riduce la potenza per le fasce negative, sia nella forma additiva sia in quella moltiplicativa;
- `_calcola_potenza_carta_stats()` somma `peso × valore × numero_statistiche`, dove il peso dipende dal segno;
- introdotta `POTENZA_MINIMA = 0.1`: una carta col saldo negativo resta in fondo alla graduatoria senza assumere valori nulli o negativi, che falserebbero i prodotti a valle.

### 20.4 Misure

**Tipi a fasce** — isolando il solo effetto del peso sulle penalità:

| Carta | Prima | Dopo |
|---|---|---|
| `Warzone / Rifugio Sacro` (3 penalità) | 32.000 | **28.756** |
| `Fortificazione / Trincea` (+2 A, −2 C) | 2.000 | **1.930** |

La verifica che conta: `Cattedrale` dà solo +2 in Armatura e vale **2.000**; la `Trincea` dà lo stesso +2 ma con un −2 in C e ora vale **1.930**, collocandosi correttamente **sotto** di essa. Prima erano pari.

**Speciale / Arte / Oscura Simmetria** — il peso 0.65 sui bonus deflaziona uniformemente la scala, lasciando invariato l'ordinamento, mentre le penalità introducono nuove distinzioni:

| Tipo | Carte con punteggio modificato | Max | Valori distinti |
|---|---:|---|---|
| Speciale | 28 su 180 | 11.0 → 7.85 | 13 → **14** |
| Arte | 21 su 66 | 8.0 → 5.9 | 9 → **10** |
| Oscura Simmetria | 13 su 35 | 12.0 → 8.5 | 10 → 10 |

### 20.5 Non regressione

561 carte istanziate, 0 fallimenti. Cinque collezioni con mazzi su `['Base']`: 64–79 carte, **0 sotto il minimo, 0 sopra il massimo, 0 violazioni del limite di 5 copie, 0 carte fuori espansione**, nessun errore.

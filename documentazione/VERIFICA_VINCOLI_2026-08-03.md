# Verifica dei vincoli di compatibilità — 3 agosto 2026

Relazione della verifica sistematica della logica di compatibilità carta-guerriero e
della selezione, condotta insieme alla stesura della suite di test (`test/`, 743 test).

**Da riprendere:** le carte elencate in [§1](#1-carte-da-correggere-nei-dati) e i difetti
di [§2](#2-difetti-di-codice-aperti) attendono una decisione. Ogni voce ha un test
sentinella che fallirà quando verrà corretta, così l'elenco non può restare disallineato.

---

## Il metodo

Il `testo_carta` è la **fonte autorevole**: le carte dichiarano le proprie condizioni in
apertura, in maiuscolo («ASSEGNABILE AD OGNI DOOMTROOPER»). I campi di restrizione sono
una trascrizione, e come ogni trascrizione può perdere pezzi o introdurre refusi.

Le nozioni di dominio che governano la lettura, chiarite durante la verifica:

- **`keywords` dice cosa un guerriero è oltre alla fazione**: `Eretico`, `Personalita`,
  `Comandante`, `Nefarita`, `Seguace di X`, `Cultista di X`. I vincoli su questi concetti
  vanno letti lì, non nella fazione né nel tipo.
- **Eretici**: Apostata, Billy, Destroyer, i cinque Cultisti, Mietitori di Anime,
  Techno-Mancer, Necromagus Supremo, Eretico. **`Apostata Rinnegato` non lo è** — il nome
  trae in inganno, e la keyword gli era stata attribuita per contaminazione.
- **I Cultisti sono «Doomtrooper senza icona di legame»**: il testo lascia scegliere volta
  per volta se valgono come Doomtrooper o come Oscura Legione. Il modello ha una fazione
  sola e fissa, quindi la doppia natura non è rappresentabile.
- **Le restrizioni multiple sono valutate in AND.** Quando il testo le vuole in
  alternativa serve una stringa sola con «o» — `Solo Mercenari o Eretici`,
  `Solo Doomtrooper o Eretici`.

---

## 1. Carte corrette dopo il confronto fra testo e vincoli

Tutte corrette il 2026-08-03, con test di regressione in
`test/test_vincoli_per_carta.py`.

| Carta | Tipo | Il testo dichiara | Come è stata corretta |
|---|---|---|---|
| `Lancia Castigator` | Equipaggiamento | «ASSEGNABILE AD OGNI DOOMTROOPER» | `restrizioni_guerriero: ["Solo Doomtrooper"]` — prima la ricevevano 47 guerrieri dell'Oscura Legione |
| `Addestramento Speciale` | Speciale | «OGNI DOOMTROOPER NON PERSONALITÀ» | aggiunto `Solo Doomtrooper` alla restrizione esistente: le condizioni sono cumulative |
| `Reintegrato` | Speciale | «GIOCABILE SU UN MERCENARIO» | **serviva anche il codice**: vedi sotto |
| `Nato Fortunato` | Speciale | «UN DOOMTROOPER, NON DELLA FRATELLANZA» | `Non utilizzabile su membri della Fratellanza` → `Non utilizzabile dalla Fratellanza`, la forma che il ramo riconosce |
| `Furga 750` | Equipaggiamento | «OGNI MERCENARIO O ERETICO» | **difetto di codice**, trovato correggendo le altre: vedi sotto |

**Su `Reintegrato` la diagnosi iniziale era sbagliata.** Diceva che il ramo era
`Solo Mercenari` e la stringa aveva un «su» di troppo: in realtà **`Speciale` non aveva
affatto quel ramo** — ce l'hanno le altre cinque classi, ed era stato attribuito per
analogia senza verificarlo. Corretto il dato *e* aggiunto il ramo mancante in
`Speciale.py`.

**`Furga 750`**, emersa correggendo le altre: in `Equipaggiamento.py` il ramo
`Solo Mercenari` era valutato **prima** di `Solo Mercenari o Eretici`, di cui è il
prefisso — le altre quattro classi hanno l'ordine giusto e un commento che avverte
proprio di questo — e la condizione dell'alternativa usava `or` dove le altre usano
`and`, trasformando l'alternativa in un cumulo. Gli Eretici che non fossero anche
Mercenari venivano respinti: da 10 a 22 destinatari.

### Escluse per scelta: le carte fuori espansione

`Intimidazione` e `Promozione Sul Campo` dichiarano «GUERRIERO NON-PERSONALITÀ» nel solo
campo `condizioni`, che nessuno legge, e restano scoperte: portano
`set_espansione = "Sconosciuto"`, quindi il filtro sulle espansioni le tiene fuori da
collezioni e mazzi, e non se ne trova la scansione. Le carte in quello stato sono **19**
(17 Speciali e 2 Arte); il valore è scritto in due modi — 18 usano `Sconosciuto`,
`Medico Da Campo` usa `Sconosciuta`. Il conteggio è fissato da
`test_le_carte_fuori_espansione_restano_note`.

### Da riverificare sulla scansione

- 11 voci già note: 4 in Arte, 4 in Equipaggiamento, 3 in Speciale.
- `Famoso Collezionista`: carta mancante dal database.
- `Il Diciannovesimo Executive`: la riscrittura ha fatto perdere
  `"Carte delle Arti non Assegnabili"`.

---

## 2. Difetti di codice aperti

Tutti marcati `xfail(strict=True)`: il test fallirà quando il difetto sarà corretto.

- 🟠 **`Warzone.py:317` usa `TipoGuerriero` senza importarlo**: `NameError` su
  `"Solo Personalita"`. Nessuna carta lo innesca oggi.
- 🟡 **Il controllo di disciplina in Arte è dentro `if len(guerriero.abilita) > 0`**: chi
  non ha abilità lo salta. Latente — nessun guerriero della Fratellanza ne è privo.
- 🟡 **I Cultisti non entrano mai in un mazzo Doomtrooper**: `seleziona_guerrieri` sceglie
  il ramo di orientamento con un `if/elif` sulla fazione. È la doppia natura non modellata.
- 🟡 **`Cospirazione Eretica` dipende dai Cultisti**: dopo la correzione della keyword
  dell'Apostata Rinnegato, sono loro i soli Eretici che potrebbero valere come Doomtrooper.

### Restrizioni che nessun ramo riconosce

In `test/test_vocabolario_restrizioni.py`, elenco `RESTRIZIONI_IGNORATE`. Refusi:
`Non utilizzabile dall'Oscura Legione` (il ramo dice `dalla`), `Solo su Mercenari`
(il ramo dice `Solo Mercenari`), `Seguaci di Demnogonis` (manca `Solo`). Concetti non
implementati: le singole corporazioni in Speciale, i nomi di guerriero in Equipaggiamento.

---

## 2-bis. I bonus riservati a un guerriero specifico

Alcune carte concedono un potenziamento maggiore a un guerriero determinato: la Lancia
Castigator dà +2 in C a ogni Doomtrooper e **+4 a una Valchiria**. Il pattern riguarda
**cinque carte** in due tipologie.

Il vocabolario controllato lo modellava già a metà: `statistiche` porta il bonus di
default, `modificatori_speciali` quello superiore con `condizione: "Uso ristretto: …"`,
e `modificatore_utilizzabile()` lo esclude dal punteggio perché non è garantito. Giusto
— ma il bonus restava ignorato anche quando il guerriero *era* nel mazzo.

Aggiunto il campo **`guerrieri_avvantaggiati`** al modificatore: la forma confrontabile
della condizione, che il testo esprime in prosa e in maiuscolo.

| Carta | Condizione nel testo | `guerrieri_avvantaggiati` |
|---|---|---|
| `Lancia Castigator` | «Se assegnata a una VALCHIRIA» | `["Valkiria"]` |
| `Azogar` | «se assegnata a un NEFARITA DI ALGEROTH» | `["Valpurgius"]` — l'unico Nefarita Seguace di Algeroth |
| `Tenuta da Battaglia` | «Se è un INQUISITORE o un INQUISITORE MASSIMO» | `["Inquisitore", "L'Inquisitore Massimo"]` |

Il consumo sta in `_bonus_condizionato_attivabile`, agganciato in
`seleziona_carte_supporto` accanto al precedente esatto — `_dono_utilizzabile_dai_guerrieri`,
che *declassa* i Doni che nessuno può ricevere: qui si *promuove*, col fattore
`BONUS_SINERGIA`. La potenza della carta non è toccata, perché è una proprietà
intrinseca e non può dipendere dal mazzo.

Misurato a parità di squadra: con la Valchiria presente, la Lancia Castigator sale
**dalla posizione 131 alla 106**.

**Restano fuori due carte**, che dichiarano la condizione in campi diversi:
`Paramenti Sacri` (in `abilita_speciali`, «Se il guerriero è un MISTICO o un CUSTODE
DELL'ARTE») e `Portatore Di Luce` (Reliquia, in `poteri`, «Se assegnata a un
CARDINALE»). Il punteggio valuta quei blocchi con logiche proprie: aggiungervi il campo
senza estendere anche il consumo creerebbe l'ennesimo dato che nessuno legge.

## 3. Correzioni già applicate

| Dove | Cosa |
|---|---|
| `Database_Guerriero.py` | `Apostata Rinnegato`: tolta la keyword `Eretico`, che il testo non dichiara |
| `Database_Missione.py` | `Quindici Minuti Di Fama`: tolta `Solo Doomtrooper`, errore; il vincolo vero è `Non Personalita` |
| `Missione.py` | `puo_essere_associata_a` ora legge **`restrizioni_guerriero`**, popolato ma mai consultato |
| `Database_Missione.py` + `Missione.py` | `Cospirazione Eretica`: le due restrizioni in AND la rendevano assegnabile a **nessuno**. Ora `Solo Doomtrooper o Eretici`, con ramo dedicato |
| `Database_Oscura_Simmetria.py` + `Oscura_Simmetria.py` | `Portale Della Cura Oscura` e `Legame Necrovisuale`: aggiunta la deroga `Dono di qualsiasi Apostolo`. Da 1 destinatario a tutti e 3 i Nefariti |
| `Creatore_Mazzo.py` | `'Cultista' in keywords` era **sempre falso** (la keyword è `Cultista di X`, e `in` su lista confronta gli elementi interi): `BONUS_CULTISTA` non si applicava a nessuno. Da 0 a 3 Cultisti selezionati |
| `Arte.py` | l'eccezione al controllo di fazione cercava la keyword `"Apostata"`, che **nessun guerriero possiede**: `Apostata`, `Apostata Rinnegato` e `Valpurgius` non potevano lanciare nessuna delle 66 Arti. Il criterio è ora l'abilità di tipo Arte che il guerriero dichiara — lo stesso campo che il controllo sulla disciplina già consulta. Copre tutti e tre, mentre la keyword avrebbe lasciato fuori Valpurgius, che non è un Apostata |

Sull'ultima: il criterio è **più permissivo** di quello che sostituisce — chiunque dichiari
un'abilità di tipo Arte lancia anche fuori fazione. `test_i_lanciatori_esterni_sono_soltanto_tre`
fissa l'elenco, così dare quell'abilità a un guerriero che non deve lanciare non passa
inosservato.

---

## 4. Ciò che è risultato corretto

Verificato e **non** difettoso, per non riaprirlo:

- **`limitazioni`** (189 carte in 5 tipi) non è letto dai metodi di permesso, ed è giusto:
  sta dentro `poteri[N]` e `abilita_speciali[N]`, quindi limita *quel potere*, non
  l'assegnazione. Sono condizioni da motore di gioco, che il progetto non ha.
- **`Equipaggiamento.requisiti` e `compatibile_con`** sono vincoli *fra carte* («un solo
  VEICOLO») — materia della validazione di mazzo, che non esiste ancora.
- **`Warzone.difensore` e `aree_utilizzabili`** sono modificatori di gioco.
- **Le 25 carte Oscura Simmetria con `Solo Seguaci di X`** reggono via
  `tipo = Dono degli Apostoli` + `apostolo_padre`: la stringa è ridondante.
- **Le restrizioni ridondanti di Missione** (`Solo Imperiale`, `Solo Fratellanza`, …):
  `fazioni_permesse` fa già il lavoro.
- **`seleziona_guerrieri` e `seleziona_carte_supporto` non filtrano, pesano**;
  l'ammissibilità è delegata a `Creatore_Mazzo.py:1868-1883`, che usa i metodi di permesso.
- Il validatore Warzone segnala «costo azione 0» su tutte e 14 le carte e giudizi di
  bilanciamento: è il validatore a non concordare con i dati.

---

## 5. Cosa resta fuori dalla verifica

Collezioni e mazzi come **prodotto finito**, esportazione, GUI. E le validazioni di mazzo
mai implementate: il limite di 5 copie come controllo finale e l'unicità delle Reliquie
(regolamento §5) — vanno scritte prima di poterne fare test.

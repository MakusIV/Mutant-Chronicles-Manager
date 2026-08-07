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
collezioni e mazzi, e non se ne trova la scansione. Le carte in quello stato sono **18**
(17 Speciali e 1 Arte — `"Esorcizzare Danno"`, l'altra, era un doppione di
`"Esorcizzare Ferite"` ed è stata rimossa); il valore è scritto in due modi — 17 usano
`Sconosciuto`, `Medico Da Campo` usa `Sconosciuta`. Il conteggio è fissato da
`test_le_carte_fuori_espansione_restano_note`.

### Da riverificare sulla scansione — aggiornato 2026-08-07

Riletture dirette delle scansioni (`image/`), con correzioni applicate dove confermate:

- **Arte, risolte**: `Conoscere La Verità` (refuso di trascrizione, "Ti" → "Vi");
  `Scacciato` (mancavano "indipendentemente dall'ICONA DI LEGAME" e "Non è
  considerato un Attacco" — `bersaglio` corretto in `Qualsiasi Guerriero`, valore già
  presente nel vocabolario `BersaglioArte`). `Esorcizzare Danno` era un doppione
  byte-per-byte di `Esorcizzare Ferite` (stesso `effetti`, stesso `testo_carta`,
  nessuna scansione propria) — rimossa. Restano 2 voci ⚪ non confermate:
  `Fulmine Elementare`, `Spinta Cinetica` (incoerenze interne tra `statistica_target`
  e il testo, non ancora riverificate sulla scansione).
- **Equipaggiamento, risolte**: `fazioni_permesse` di `Elmetto Comando` e
  `Computer Tattico` corretto in `Cybertronic` (icona confermata dall'utente).
  `AC-40 Justifier` e `Lancia Castigator` restano `Generica`: l'icona osservata è
  Fratellanza, ma nessun testo/FAQ la restringe (`Lancia Castigator` ha già
  `Solo Doomtrooper` in `restrizioni_guerriero`, e questo database non ha un valore
  collettivo "Doomtrooper" per `fazioni_permesse`).
- **Speciale**: `False Credenze` e `Fiamme Purificatrici` restano `Generica`.
  L'icona osservata è Fratellanza, ma **`fazioni_permesse` è un filtro rigido**:
  `Creatore_Mazzo._carta_compatibile_con_guerrieri` scarta una carta Speciale se
  nessun guerriero del mazzo soddisfa `puo_essere_assegnato_a_guerriero` — quindi
  vale solo quando l'effetto agisce sui *propri* guerrieri, non su quelli
  dell'avversario. Entrambe le carte colpiscono guerrieri altrui (False Credenze
  abilita il combattimento reciproco Fratellanza/Cybertronic, Fiamme
  Purificatrici scarta un guerriero dell'Oscura Legione): richiedere un
  guerriero Fratellanza in mazzo per usarle sarebbe stato un vincolo indebito.
  `Feroce Assassino` resta `Oscura Legione`, correttamente: potenzia un proprio
  guerriero, che deve appartenere a quella fazione.
- **`Famoso Collezionista`**: aggiunta. La scansione (`image/Speciali/`) era
  interamente leggibile, a differenza di quanto riportato dall'audit originale —
  vedi la voce nel database per il testo completo. `fazione = Generica,
  rarity = Common, quantita = 15, set_espansione = Inquisition` per conferma
  diretta dell'utente. Non modella l'effetto (assegnazione di Reliquie) nel motore:
  per regolamento la carta non è più necessaria per usare le Reliquie in gioco.
- **`Il Diciannovesimo Executive`**: **chiuso, nessuna correzione**. La scansione
  conferma il `testo_carta` già presente parola per parola, senza alcun riferimento
  all'Arte. La frase `"Carte delle Arti non Assegnabili"` compare in `restrizioni`
  di altre 8 carte del database, tutte Cybertronic ma non tutte Personalità
  (Cyril Dent, Dottoressa Diana, Capitano Cybertronic, Droide Eradicator, Vince
  Diamond, Tecnico Vac, Osservatore Tattico, Charles Sykes) — il testo reale su
  quelle carte è **"Non potrà mai lanciare incantesimi dell'arte"**, un concetto
  diverso da "non assegnabili" con cui la chiave era stata etichettata. Il
  Diciannovesimo Executive è un Leader Corporativo: non può combattere né andare in
  copertura (già corretto), e il testo non dice nulla sull'Arte. Resta aperta,
  fuori da questa sessione, la revisione della chiave/frase sulle altre 8 carte.

---

## 2. Difetti di codice — chiusi

Non restano `xfail`. Gli ultimi due sono stati corretti così:

**Il controllo di disciplina in Arte** era racchiuso in `if len(guerriero.abilita) > 0`, e
chi non aveva alcuna abilità lo saltava ottenendo il permesso per la sola fazione. Tolta
la guardia: senza abilità l'elenco delle discipline resta vuoto, i predicati risultano
falsi e il guerriero è respinto. Verificato a impatto nullo sui dati — 759 permessi prima
e dopo, perché i 47 guerrieri senza abilità sono tutti fuori dalla Fratellanza e già
respinti dal controllo di fazione.

**La doppia natura dei Cultisti** è ora rappresentata dalla keyword
`Doomtrooper senza legame`, trascrizione del loro testo («CONSIDERATO UN DOOMTROOPER
SENZA ICONA DI LEGAME E UN ERETICO»), letta da `vale_come_doomtrooper()` in
`Guerriero.py`. La funzione è usata in **tre punti**, perché correggerne uno solo avrebbe
prodotto incoerenza:

1. la **compatibilità** — i rami «Solo Doomtrooper» delle sei classi: prima un Cultista
   entrava in un mazzo Doomtrooper senza poter ricevere le 12 carte riservate ai
   Doomtrooper che quel mazzo contiene;
2. la **selezione** — `seleziona_guerrieri` sceglieva il ramo di orientamento con un
   `if/elif` sulla sola fazione. Il bonus Cultista è stato spostato fuori dai rami, come
   già quello Eretico, perché un Cultista valutato fra i Doomtrooper non raggiunge il
   ramo dell'Oscura Legione;
3. la **ripartizione squadra/schieramento** — il testo dice «Puoi aggiungere il Cultista
   solo alla Tua Squadra», e invece finiva nello Schieramento in ogni mazzo orientato
   all'Oscura Legione.

Restano Doomtrooper **generici**: ricevono le carte aperte a tutti i Doomtrooper ma, non
avendo icona di legame, non quelle riservate a una singola Megacorporazione — vincolo che
passa da `fazioni_permesse` ed è verificato da un test.

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

### La tassonomia dell'Oscura Simmetria

Il database raccoglie tutte le carte che il testo dichiara Doni **degli Apostoli**,
**dell'Oscura Simmetria** o **dell'Oscura Legione**. Le ultime due diciture indicano la
stessa cosa — 9 carte contro 1, quasi certamente un refuso di trascrizione — e il codice
le tratta già come equivalenti. La partizione che conta è un'altra:

| | Carte | `apostolo_padre` |
|---|---|---|
| Doni degli Apostoli | 25 | sì |
| doni generici | 10 | no |

Un guerriero può dichiarare due restrizioni **complementari**, che vanno trattate allo
stesso modo: `Solo doni degli Apostoli` esclude dai generici, `Solo doni dell'Oscura
Simmetria` esclude dai Doni degli Apostoli.

La seconda era però scritta come coda della condizione d'ingresso al blocco che verifica
il Seguace, dove agiva da **esenzione** anziché da esclusione: il guerriero `Eretico`,
l'unico che la dichiara, saltava la verifica e riceveva **23 Doni di Apostoli su 25**, di
Apostoli di cui non è Seguace. Ora ne riceve 0 e mantiene tutti e 10 i generici.

Chi è Seguace **e** Eretico — i Cultisti, `Destroyer` — riceve i Doni del proprio
Apostolo più i generici, e nient'altro: verificato.

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

### Il vocabolario del punteggio

Il secondo asse — quanto vale una carta, non chi può riceverla — confronta i nomi di
abilità e poteri per uguaglianza contro elenchi scritti nel codice. **12 abilità su 54 e
2 poteri su 17 non pesavano.** Due cause distinte:

- **19 stringhe del vocabolario portavano maiuscole**, in quattro blocchi
  (`"Incrementa Azioni"`, `"Attacca sempre per primo"`, `"Immune alle ferite durante il
  combattimento"`, …), mentre il confronto avviene contro il nome **già abbassato a
  minuscolo**: rami scritti e irraggiungibili. Abbassate tutte;
  `test_nessuna_stringa_del_vocabolario_porta_maiuscole` impedisce che tornino.
- **3 nomi non avevano alcun ramo** nel blocco Equipaggiamento: `"assegna carte"` (la
  variante al plurale di `"assegna carta"`, usata dai veicoli che ne trasportano più
  d'una), `"lancia arte"` (forma breve già riconosciuta dai blocchi di Reliquia e
  Fortificazione) e `"attacca sempre per primo se sceglie di sparare"` (variante
  condizionata). Aggiunti accanto ai nomi affini.

Ora tutte le 54 abilità e tutti i 17 poteri contribuiscono. Gli elenchi dei nomi
scoperti sono vuoti, e `test_ogni_abilita_speciale_e_classificata` li tiene tali: un
nome nuovo che nessun ramo riconosce fa fallire il test, e va corretto invece che
aggiunto all'elenco.

### «Solo Personalita»: basta una delle due dichiarazioni

**`Warzone.py` non importava `TipoGuerriero`**, quindi la restrizione «Solo Personalita»
sollevava `NameError` invece di verificare il tipo del guerriero. Aggiunto l'import.

Attivando quel controllo è emerso un problema più profondo, che riguardava tutte e sei
le classi. Un guerriero può risultare Personalità in due modi — il campo `tipo` e la
keyword — e il codice **le pretendeva entrambe**. I dati dicono il contrario:

| Come le Personalità si dichiarano | Quante |
|---|---|
| il solo `tipo` | **27** |
| `tipo` e keyword | 2 |
| la sola keyword | 0 |

`Cecchino`, il cui testo dice «GIOCABILE SU QUALSIASI PERSONALITÀ», arrivava così a
**2 guerrieri su 29**.

C'era anche una contraddizione fra i due versi: «Solo Personalita» pretendeva entrambe
le dichiarazioni mentre «Non utilizzabile da Personalita» ne bastava una, quindi un
guerriero col solo `tipo` — il caso normale — veniva respinto da **entrambe**: troppo
poco Personalità per le carte a loro riservate, troppo per quelle che le escludono.

Ora basta una delle due, in tutte le classi, e l'Oscura Simmetria guarda anche la
keyword oltre al `tipo`. `Cecchino` passa a 29 destinatari.

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

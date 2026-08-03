# Suite di test

Si esegue dalla radice del progetto:

```
.venv/bin/python -m pytest              # tutto
.venv/bin/python -m pytest -v           # un test per riga
.venv/bin/python -m pytest test/test_restrizioni_associazione.py
```

## Cosa copre

| File | Verifica |
|---|---|
| `test_restrizioni_associazione.py` | Per ogni restrizione e ogni classe carta: il caso positivo **e** quello negativo, su una coppia di guerrieri che differiscono per la sola caratteristica sotto esame. |
| `test_vocabolario_restrizioni.py` | Che ogni stringa di restrizione presente nei database sia riconosciuta da chi la consuma, o sia dichiarata descrittiva. Le stringhe ignorate in silenzio sono elencate con la loro causa. |
| `test_integrita_database.py` | `from_dict` e le factory su tutte le carte dei nove database, l'assenza di chiavi duplicate nei letterali, i validatori già presenti nei moduli `Database_*.py`. |

`conftest.py` tiene l'impalcatura: la factory di guerrieri sintetici e la tabella
`SPEC_CARTE`, che dice per ogni classe dove stanno le restrizioni e quale metodo
concede il permesso.

## Il principio

I sette difetti corretti in §10.9 avevano tutti la stessa forma: il permesso valeva
`True` qualunque fosse il guerriero. Un test che prova solo il caso positivo li
avrebbe lasciati passare tutti. **Ogni restrizione va verificata in entrambi i
versi**, e il guerriero del caso negativo deve differire da quello del caso positivo
per una sola caratteristica — altrimenti si finisce per misurare il filtro sbagliato.

## Guerrieri sintetici, non presi dal database

`crea_guerriero()` costruisce guerrieri con le sole caratteristiche che il test
dichiara. Un guerriero reale porta con sé keyword, abilità e fazione che il test non
controlla, e basta che il database cambi perché un test superato inizi a misurare
un'altra cosa. Dove invece conta il dato vero — il vincolo sull'apostolo dei Doni —
il test percorre il database reale, e lo dice.

## Gli elenchi da tenere veritieri

`test_vocabolario_restrizioni.py` contiene tre elenchi che vanno mantenuti:

- `NOTE_DESCRITTIVE` — testo di regolamento che non vincola chi riceve la carta;
- `RIDONDANTI` — stringhe il cui vincolo è imposto per un'altra via, verificata;
- `RESTRIZIONI_IGNORATE` — difetti accertati, ognuno con la sua causa.

Due test fanno da sentinella: uno fallisce quando un difetto viene corretto (così si
toglie dall'elenco), l'altro quando una voce sparisce dai database. Aggiungere una
carta con una restrizione scritta in modo nuovo fa fallire
`test_ogni_restrizione_e_classificata`, che è il momento giusto per accorgersene.

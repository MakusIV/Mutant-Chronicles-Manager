"""
Il testo della carta contro i vincoli che il codice impone davvero.

Le carte dichiarano le proprie condizioni in apertura del `testo_carta`, in maiuscolo:
«ASSEGNABILE AD OGNI DOOMTROOPER», «GIOCABILE SU UN MERCENARIO», «SOLO NEFARITA». È
la fonte autorevole — i campi di restrizione sono una trascrizione, e come ogni
trascrizione può perdere pezzi o introdurre refusi.

Questo confronto ha fatto emergere `Quindici Minuti Di Fama` (nessun vincolo
imposto), `Cospirazione Eretica` (vincoli in AND che si escludevano) e i due difetti
elencati qui sotto. È euristico — il testo è lingua naturale, non un vocabolario — e
per questo ogni scostamento va giudicato a mano prima di finire negli elenchi.
"""

import importlib
import re

import pytest

from conftest import SPEC_CARTE
from source.cards.Guerriero import DOOMTROOPER
from source.data_base_cards.Database_Guerriero import GUERRIERI_DATABASE, crea_guerriero_da_nome

GUERRIERI = [(nome, guerriero) for nome in GUERRIERI_DATABASE
             if (guerriero := crea_guerriero_da_nome(nome)) is not None]


def _dati(nome):
    return GUERRIERI_DATABASE[nome]


# I concetti del dominio e come si leggono su un guerriero. `Personalita` e le altre
# stanno nelle keyword, non nel tipo o nella fazione — è la regola che governa tutto.
CONCETTI = {
    "DOOMTROOPER": lambda n: _dati(n).get("fazione") in DOOMTROOPER,
    "FRATELLANZA": lambda n: _dati(n).get("fazione") == "Fratellanza",
    "OSCURA LEGIONE": lambda n: _dati(n).get("fazione") == "Oscura Legione",
    "ERETICO": lambda n: "Eretico" in (_dati(n).get("keywords") or []),
    "PERSONALITÀ": lambda n: (_dati(n).get("tipo") == "Personalita"
                              or "Personalita" in (_dati(n).get("keywords") or [])),
    "COMANDANTE": lambda n: "Comandante" in (_dati(n).get("keywords") or []),
    "NEFARITA": lambda n: "Nefarita" in (_dati(n).get("keywords") or []),
    "MERCENARIO": lambda n: (_dati(n).get("fazione") == "Mercenario"
                             or "Mercenario" in (_dati(n).get("keywords") or [])),
}

TIPI = [
    ("Speciale", "Database_Speciale", "DATABASE_SPECIALI", "crea_carta_da_database"),
    ("Equipaggiamento", "Database_Equipaggiamento", "DATABASE_EQUIPAGGIAMENTO",
     "crea_equipaggiamento_da_database"),
    ("Fortificazione", "Database_Fortificazione", "DATABASE_FORTIFICAZIONI",
     "crea_fortificazione_da_database"),
    ("Missione", "Database_Missione", "DATABASE_MISSIONI", "crea_missione_da_database"),
    ("Reliquia", "Database_Reliquia", "DATABASE_RELIQUIE", "crea_reliquia_da_database"),
    ("Warzone", "Database_Warzone", "DATABASE_WARZONE", "crea_istanza_warzone"),
    ("Oscura_Simmetria", "Database_Oscura_Simmetria", "DATABASE_OSCURA_SIMMETRIA",
     "crea_carta_da_database"),
]


# Scostamenti accertati come difetti: il testo dichiara un vincolo che nessun campo
# impone. Vanno svuotati correggendo il dato, non allungati.
VINCOLI_NON_IMPOSTI = {
    ("Speciale", "Reintegrato", "MERCENARIO"):
        "restrizioni dice «Solo su Mercenari», il ramo esistente è «Solo Mercenari» senza «su»",
    ("Speciale", "Nato Fortunato", "FRATELLANZA"):
        "fazioni_permesse include Fratellanza, che il testo esclude",
    ("Speciale", "Addestramento Speciale", "DOOMTROOPER"):
        "nessun campo impone «Doomtrooper»; fazioni_permesse è ['Generica']",
    ("Equipaggiamento", "Lancia Castigator", "DOOMTROOPER"):
        "nessuna restrizione dichiarata; fazioni_permesse è ['Generica']",
    ("Speciale", "Intimidazione", "PERSONALITÀ"):
        "«QUALSIASI GUERRIERO NON-PERSONALITÀ»: il vincolo è solo in `condizioni`, "
        "che nessun consumatore legge, e `restrizioni` è vuoto",
    ("Speciale", "Promozione Sul Campo", "PERSONALITÀ"):
        "«UN GUERRIERO NON-PERSONALITÀ»: stesso caso, il vincolo resta in `condizioni`",
}

# Scostamenti che non sono difetti: il concetto compare nel testo per una ragione
# diversa dal vincolo sul destinatario. Il confronto è euristico e questi sono i suoi
# limiti noti, non errori del codice.
FALSI_SCOSTAMENTI = {
    ("Speciale", "Morte Istantanea", "DOOMTROOPER"):
        "il Doomtrooper è l'attaccante da cui ci si difende, non chi riceve la carta",
    ("Equipaggiamento", "Furga 750", "ERETICO"):
        "«OGNI MERCENARIO O ERETICO» è un'alternativa: chi la riceve ne soddisfa una",
    ("Missione", "Cospirazione Eretica", "DOOMTROOPER"):
        "«UN DOOMTROOPER O UN ERETICO» è un'alternativa",
    ("Missione", "Cospirazione Eretica", "ERETICO"):
        "«UN DOOMTROOPER O UN ERETICO» è un'alternativa",
}


def _dichiarazione(testo):
    """L'apertura in maiuscolo, dove la carta dichiara le proprie condizioni."""
    trovato = re.match(r"^[^a-z]{12,}", testo or "")
    return trovato.group(0) if trovato else ""


def _scostamenti():
    """Ogni carta il cui testo nomina un concetto che il permesso non rispetta."""
    for tipo, modulo, variabile, factory in TIPI:
        modulo_db = importlib.import_module(f"source.data_base_cards.{modulo}")
        database = getattr(modulo_db, variabile)
        costruisci = getattr(modulo_db, factory)
        spec = SPEC_CARTE[tipo]

        for chiave, dati in database.items():
            dichiarazione = _dichiarazione(dati.get("testo_carta"))
            if not dichiarazione:
                continue
            carta = costruisci(chiave)
            if carta is None:
                continue
            try:
                ammessi = {n for n, g in GUERRIERI if spec.permesso(carta, g)}
            except Exception:  # noqa: BLE001 — coperto da test_ogni_carta_e_costruibile
                continue
            if not ammessi:
                continue

            for concetto, soddisfa in CONCETTI.items():
                if concetto not in dichiarazione:
                    continue
                negato = re.search(r"\bNON[^.]{0,25}" + re.escape(concetto),
                                   dichiarazione) is not None
                violano = {n for n in ammessi
                           if (soddisfa(n) if negato else not soddisfa(n))}
                if violano:
                    yield tipo, chiave, concetto, len(violano), len(ammessi)


SCOSTAMENTI = list(_scostamenti())


def test_nessuno_scostamento_nuovo_fra_testo_e_vincoli():
    """
    La rete: una carta il cui testo dichiara un vincolo che nessun campo impone finisce
    qui. Se lo scostamento è reale va in `VINCOLI_NON_IMPOSTI`, se è un limite del
    confronto va in `FALSI_SCOSTAMENTI` — con la ragione scritta, in entrambi i casi.
    """
    noti = set(VINCOLI_NON_IMPOSTI) | set(FALSI_SCOSTAMENTI)
    nuovi = [f"[{tipo}] {carta}: il testo dichiara «{concetto}» ma la ricevono "
             f"{quanti}/{totale} guerrieri che non lo soddisfano"
             for tipo, carta, concetto, quanti, totale in SCOSTAMENTI
             if (tipo, carta, concetto) not in noti]

    assert not nuovi, "scostamenti non ancora giudicati:\n  " + "\n  ".join(nuovi)


@pytest.mark.parametrize("chiave,causa", sorted(VINCOLI_NON_IMPOSTI.items()))
def test_i_vincoli_non_imposti_sono_ancora_tali(chiave, causa):
    """Sentinella: quando uno viene corretto, questo test lo segnala."""
    assert any((tipo, carta, concetto) == chiave
               for tipo, carta, concetto, _, _ in SCOSTAMENTI), (
        f"{chiave[1]}: il vincolo «{chiave[2]}» è ora imposto ({causa}). "
        f"Toglilo da VINCOLI_NON_IMPOSTI."
    )


def test_gli_elenchi_non_contengono_voci_scomparse():
    presenti = {(tipo, carta, concetto) for tipo, carta, concetto, _, _ in SCOSTAMENTI}
    scomparse = sorted((set(VINCOLI_NON_IMPOSTI) | set(FALSI_SCOSTAMENTI)) - presenti)
    assert not scomparse, (
        f"voci che non producono più uno scostamento, da rimuovere: {scomparse}"
    )

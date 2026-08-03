"""
Arte: l'unica classe carta che non passa dal vocabolario di restrizioni condiviso.

Il permesso di lanciare un incantesimo si decide su due assi, entrambi diversi da
quelli delle altre classi:

1. la **fazione** — di norma la sola Fratellanza, con un'eccezione per gli Apostati;
2. la **disciplina** — il guerriero deve dichiarare, fra le proprie abilità di tipo
   «Arte», un `target` che cita la disciplina dell'incantesimo o «Tutte le Discipline».

Il confronto sulla disciplina è per sottostringa, perché il `target` è una frase
(«Arte della Manipolazione ed Esorcismo») e non il nome nudo della disciplina.
"""

import pytest

from conftest import crea_guerriero
from source.cards.Guerriero import Abilita, Fazione
from source.data_base_cards.Database_Arte import CARTE_ARTE_DATABASE, crea_carta_da_database
from source.data_base_cards.Database_Guerriero import GUERRIERI_DATABASE, crea_guerriero_da_nome

FRATELLANZA = Fazione.FRATELLANZA

GUERRIERI = [(nome, guerriero) for nome in GUERRIERI_DATABASE
             if (guerriero := crea_guerriero_da_nome(nome)) is not None]


def _maestro(disciplina, fazione=FRATELLANZA, nome="maestro"):
    """Un guerriero che dichiara la disciplina indicata fra le proprie abilità."""
    return crea_guerriero(
        nome=nome, fazione=fazione,
        abilita=[Abilita(nome="Lancia Arte", descrizione="", tipo="Arte", target=disciplina)])


def _carte_per_disciplina():
    visto = {}
    for chiave in CARTE_ARTE_DATABASE:
        carta = crea_carta_da_database(chiave)
        if carta is not None:
            visto.setdefault(carta.disciplina.value, chiave)
    return sorted(visto.items())


# --------------------------------------------------------------------------


@pytest.mark.parametrize("disciplina,nome_carta", _carte_per_disciplina())
def test_serve_la_disciplina_giusta(disciplina, nome_carta):
    """Il caso positivo e quello negativo su una coppia che differisce solo di disciplina."""
    carta = crea_carta_da_database(nome_carta)
    altra = "Evocazione" if disciplina != "Evocazione" else "Cinetica"

    assert carta.puo_essere_associata_a_guerriero(_maestro(disciplina)).get("puo_lanciare"), (
        f"{nome_carta}: un maestro di {disciplina} non può lanciarla"
    )
    assert not carta.puo_essere_associata_a_guerriero(_maestro(altra)).get("puo_lanciare"), (
        f"{nome_carta} ({disciplina}) è lanciabile da un maestro di {altra}"
    )


@pytest.mark.parametrize("disciplina,nome_carta", _carte_per_disciplina())
def test_tutte_le_discipline_le_lancia_tutte(disciplina, nome_carta):
    carta = crea_carta_da_database(nome_carta)
    assert carta.puo_essere_associata_a_guerriero(
        _maestro("Tutte le Discipline")).get("puo_lanciare")


@pytest.mark.parametrize("disciplina,nome_carta", _carte_per_disciplina())
def test_il_target_e_confrontato_per_sottostringa(disciplina, nome_carta):
    """
    Il `target` dei guerrieri veri è una frase che cita una o due discipline, non il
    nome nudo: se il confronto tornasse a essere per uguaglianza, i maestri di due
    discipline smetterebbero di poter lanciare entrambe.
    """
    carta = crea_carta_da_database(nome_carta)
    maestro = _maestro(f"Arte della {disciplina} ed Esorcismo")
    assert carta.puo_essere_associata_a_guerriero(maestro).get("puo_lanciare"), (
        f"{nome_carta}: il target «Arte della {disciplina} ed Esorcismo» non è riconosciuto"
    )


@pytest.mark.parametrize("nome_carta", sorted(CARTE_ARTE_DATABASE))
def test_ogni_arte_ha_almeno_un_lanciatore(nome_carta):
    carta = crea_carta_da_database(nome_carta)
    assert carta is not None, f"{nome_carta} non è costruibile"
    assert any(carta.puo_essere_associata_a_guerriero(g).get("puo_lanciare")
               for _, g in GUERRIERI), (
        f"{nome_carta}: nessuno dei {len(GUERRIERI)} guerrieri del database può lanciarla"
    )


@pytest.mark.parametrize("fazione", [Fazione.CAPITOL, Fazione.OSCURA_LEGIONE,
                                     Fazione.MISHIMA])
def test_fuori_dalla_fratellanza_non_si_lancia_senza_l_abilita(fazione):
    """Chi non è della Fratellanza e non dichiara di saper lanciare l'Arte è respinto."""
    nome_carta = next(iter(CARTE_ARTE_DATABASE))
    carta = crea_carta_da_database(nome_carta)
    profano = crea_guerriero(nome="profano", fazione=fazione, abilita=[])

    assert not carta.puo_essere_associata_a_guerriero(profano).get("puo_lanciare"), (
        f"{nome_carta} è lanciabile da un guerriero {fazione.value} senza abilità di Arte"
    )


@pytest.mark.parametrize("fazione", [Fazione.CAPITOL, Fazione.OSCURA_LEGIONE,
                                     Fazione.MISHIMA])
def test_fuori_dalla_fratellanza_si_lancia_con_l_abilita(fazione):
    """
    Il verso complementare, che è il senso della correzione: la fazione non basta più a
    escludere: chi dichiara l'abilità lancia comunque, come l'Apostata Rinnegato, che è
    un Mercenario, e Valpurgius, che è dell'Oscura Legione.
    """
    nome_carta = next(iter(CARTE_ARTE_DATABASE))
    carta = crea_carta_da_database(nome_carta)
    maestro = _maestro(carta.disciplina.value, fazione=fazione)

    assert carta.puo_essere_associata_a_guerriero(maestro).get("puo_lanciare"), (
        f"{nome_carta}: un maestro {fazione.value} della disciplina giusta è respinto"
    )


# --------------------------------------------------------------------------
# Chi lancia l'Arte pur non essendo della Fratellanza
# --------------------------------------------------------------------------

# I tre guerrieri che dichiarano un'abilità di tipo «Arte» pur non essendo della
# Fratellanza, con la frase del testo che glielo riconosce.
LANCIATORI_ESTERNI = [
    ("Apostata", "può lanciare tutti gli incantesimi dell'Arte"),
    ("Apostata Rinnegato", "Può usare tutti i tipi di Arte"),
    ("Valpurgius", "Può manipolare l'Arte"),
]


@pytest.mark.parametrize("nome_guerriero,frase", LANCIATORI_ESTERNI,
                         ids=[g[0] for g in LANCIATORI_ESTERNI])
def test_i_lanciatori_esterni_possono_lanciare(nome_guerriero, frase):
    """
    Tutti e tre dichiarano un'abilità «Arte / Tutte le Discipline» e un testo che lo
    conferma, e nessuno dei tre poteva lanciare una sola delle 66 carte: l'eccezione al
    controllo di fazione cercava la keyword «Apostata», che nessun guerriero possiede.
    Ora il criterio è l'abilità dichiarata, che li copre tutti e tre — compreso
    Valpurgius, che un criterio sui nomi propri avrebbe lasciato fuori.
    """
    guerriero = crea_guerriero_da_nome(nome_guerriero)
    assert guerriero is not None

    lanciabili = [chiave for chiave in CARTE_ARTE_DATABASE
                  if (carta := crea_carta_da_database(chiave))
                  and carta.puo_essere_associata_a_guerriero(guerriero).get("puo_lanciare")]

    assert lanciabili, (
        f"{nome_guerriero} non può lanciare nessuna delle {len(CARTE_ARTE_DATABASE)} "
        f"carte Arte, ma il suo testo dice: «{frase}»"
    )


def test_i_lanciatori_esterni_sono_soltanto_tre():
    """
    Il criterio è più permissivo di quello che sostituisce — chiunque dichiari
    un'abilità di tipo Arte lancia anche fuori fazione — quindi va tenuto d'occhio: dare
    quell'abilità a un guerriero che non deve lanciare aprirebbe un varco in silenzio.
    """
    esterni = {nome for nome, guerriero in GUERRIERI
               if guerriero.fazione is not FRATELLANZA
               and any(abilita.tipo == "Arte" for abilita in guerriero.abilita)}

    assert esterni == {nome for nome, _ in LANCIATORI_ESTERNI}, (
        f"i guerrieri fuori Fratellanza che dichiarano di lanciare l'Arte sono cambiati: "
        f"{sorted(esterni)}")


def test_la_keyword_apostata_non_e_piu_necessaria():
    """
    Il criterio non deve tornare a dipendere da una keyword che i dati non hanno: era
    proprio l'assenza di «Apostata» dal database a rendere l'eccezione inerte.
    """
    portatori = {nome for nome, dati in GUERRIERI_DATABASE.items()
                 if "Apostata" in (dati.get("keywords") or [])}
    assert not portatori, (
        f"la keyword «Apostata» è comparsa su {sorted(portatori)}: se il criterio deve "
        f"tornare a usarla, va rivisto anche il caso di Valpurgius, che non è un Apostata")


@pytest.mark.parametrize("nome_guerriero,frase", LANCIATORI_ESTERNI,
                         ids=[g[0] for g in LANCIATORI_ESTERNI])
def test_i_lanciatori_esterni_dichiarano_l_abilita(nome_guerriero, frase):
    """Il presupposto del test qui sopra: l'abilità c'è, è il permesso a non seguirla."""
    guerriero = crea_guerriero_da_nome(nome_guerriero)
    assert any(abilita.tipo == "Arte" for abilita in guerriero.abilita), (
        f"{nome_guerriero} non dichiara alcuna abilità di tipo Arte"
    )


def test_senza_abilita_non_si_lancia():
    """
    Il controllo sulla disciplina stava dentro `if len(guerriero.abilita) > 0`: un
    guerriero senza alcuna abilità lo saltava e otteneva il permesso per la sola
    fazione. Non faceva danni — nessun guerriero della Fratellanza è privo di abilità —
    ma bastava aggiungerne uno per aprire il varco.
    """
    nome_carta = next(iter(CARTE_ARTE_DATABASE))
    carta = crea_carta_da_database(nome_carta)
    profano = crea_guerriero(nome="profano", fazione=FRATELLANZA, abilita=[])

    assert not carta.puo_essere_associata_a_guerriero(profano).get("puo_lanciare"), (
        "un guerriero della Fratellanza senza abilità di Arte non deve poter lanciare "
        "incantesimi: il controllo sulla disciplina è saltato quando `abilita` è vuota"
    )

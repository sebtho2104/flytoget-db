# flytoget-db

Et databaseprosjekt bygget for å øve på SQL, relasjonsmodellering og Python –
med et datasett inspirert av ekte togdrift hos Flytoget. Prosjektet startet
som en enkel øvelse i SQL-grunnlag, og har vokst til en fullstendig,
normalisert database med realistisk rutedata, prislogikk og et sett
spørringer som demonstrerer sentrale SQL-konsepter.

## Datamodell

| Tabell         | Beskrivelse                                                                        |
| -------------- | ---------------------------------------------------------------------------------- |
| `stasjoner`    | De 10 stasjonene på Flytoget-strekningen                                           |
| `tog`          | Fysiske togsett (type, antall seter)                                               |
| `avganger`     | Hver togtur, med fra/til-stasjon, tog, klokkeslett og plattform                    |
| `stopp`        | Hvert enkelt stopp en avgang gjør underveis, med ankomst-/avgangstid og rekkefølge |
| `priser`       | Grunnpriser per stasjon og billett-type                                            |
| `billetter`    | Solgte billetter, med kobling til stasjon, type og pris                            |
| `forsinkelser` | Registrerte forsinkelser knyttet til en avgang                                     |

**Normalisering:** `stasjoner` er brutt ut som egen tabell for å unngå at
stasjonsnavn gjentas. `stopp` fungerer som en bindingstabell mellom
`avganger` og `stasjoner` (mange-til-mange: en avgang har mange stopp, en
stasjon inngår i mange avganger), med `rekkefolge` og tidspunkt som ekstra
informasjon på selve koblingen.

Alle fremmednøkler håndheves aktivt via `PRAGMA foreign_keys = ON` i
`seed.py` – SQLite håndhever ikke dette som standard.

## Ruteinfo og prising

**Merk om datagrunnlaget:** Rutetidene er basert på ekte Flytoget-data hentet
i en periode med vedlikeholdsarbeid på deler av strekningen, og samsvarer
derfor ikke nøyaktig med normal drift. Antall togsett og avgangstider per
tognummer er heller ikke eksakte tall, men en representasjon av hvordan
oppsettet fungerer i praksis. Snutiden på 20 minutter er kun beregnet ved
endestasjonene – tidsbruk ved mellomstasjonene er ikke tatt med i
beregningen.

- **`ruter.py`** – genererer `stopp`-data automatisk fra `avganger`, basert
  på definerte ruter (Drammenstog, Direktetog, Stabekktog) med stasjon- og
  segmenttider.
- **`priser.py`** – genererer prisdata basert på avstand fra Gardermoen og
  billett-type (student/honnør/ungdom/vernepliktig/barn = halv pris,
  flytog-ansatt = gratis).

## Oppsett

```bash
python3 seed.py      # bygger og fyller flytoget.db fra bunnen av
python3 queries.py    # kjører eksempelspørringer mot databasen
```

`seed.py` sletter og gjenoppretter `flytoget.db` ved hver kjøring, slik at
den alltid gir et forutsigbart, rent utgangspunkt.

## Spørringene i queries.py demonstrerer

- `WHERE` – enkel filtrering
- `GROUP BY` + `AVG`/`SUM`/`COUNT` – aggregering
- `INNER JOIN` – både to og tre tabeller i samme spørring
- `LEFT JOIN` – inkludert forståelse for `COUNT(*)` vs. `COUNT(kolonne)`
  ved manglende matcher
- `ORDER BY` – med riktig valg av sorteringskolonne (f.eks. `rekkefolge`
  fremfor `stasjons_id` for å få faktisk reiserekkefølge)
- `HAVING` – filtrering etter gruppering
- `COALESCE` – håndtering av NULL-verdier
- `CASE WHEN` – betinget kategorisering direkte i spørringen
- `LIMIT` og `DISTINCT`

## Testing

Prosjektet har automatiserte enhetstester (`pytest`) for `priser.py` og
`ruter.py`, som dekker både forventet oppførsel og grensetilfeller.
Testene avdekket to reelle ting å rette underveis: én test bekreftet at
funksjonen ikke ved et uhell endrer på delte data mellom kall (noe som
kunne gitt feil resultat senere), og en annen test viste at en ukjent
`avgangs_id` ga feil resultat uten varsel — nå kaster koden en tydelig
feilmelding i stedet.

I tillegg finnes integrasjonstester (`test_integration.py`) som kjører
hele `seed.py`-prosessen fra start til slutt, og bekrefter at alt fungerer
riktig sammen – riktig antall rader i alle tabeller, ingen ugyldige
referanser mellom tabeller, at fremmednøkler faktisk håndheves, og at to
kjøringer av `seed.py` gir identisk resultat. Hver integrasjonstest kjører
i sin egen midlertidige mappe (`tmp_path`), slik at testene er fullstendig
uavhengige av hverandre og av den ekte databasefilen.

Kjør testene slik:

```bash
pip install -r requirements.txt
python -m pytest
```

## Prosjektstruktur

```

schema.sql – databasestruktur (alle CREATE TABLE-setninger)
seed.py – bygger databasen og fyller den med testdata
ruter.py – genererer stopp-data fra rutedefinisjoner
priser.py – genererer prisdata fra stasjon og billett-type
queries.py – eksempelspørringer mot den ferdige databasen
requirements.txt – Python-avhengigheter (pytest)
tests/
test_priser.py – enhetstester for prislogikk
test_ruter.py – enhetstester for rutegenerering
test_integration.py – integrasjonstester for hele seed-prosessen

```

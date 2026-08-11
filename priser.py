BASEPRIS = {
    10: 324,    # Drammen
    9: 308,     # Asker   
    8: 308,     # Sandvika
    7: 268,     # Lysaker
    6: 268,     # Stabekk
    5: 268,     # Skøyen
    4: 268,     # Nationaltheatret
    3: 268,     # Oslo S
    2: 210      # Lillestrøm
}
FULL_PRIS_TYPER = ["voksen", "hentebillett"]
HALV_PRIS_TYPER = ["student", "honnør", "ungdom", "vernepliktig", "barn"]
ANSATT_TYPE = ["flytog-ansatt"]

TYPE_FAKTOR = {}
for typer, faktor in [(FULL_PRIS_TYPER, 1.0), (HALV_PRIS_TYPER, 0.5), (ANSATT_TYPE, 0.0)]:
    for billett_type in typer:
        TYPE_FAKTOR[billett_type] = faktor

def lag_priser():
    priser = []
    pris_id = 1
    for stasjons_id, basepris in BASEPRIS.items():
        for billett_type, faktor in TYPE_FAKTOR.items():
            pris = round (basepris * faktor)
            priser.append((pris_id, stasjons_id, billett_type, pris))
            pris_id += 1
    return priser

def hent_pris(priser, stasjons_id, billett_type):
    for (_, sid, typ, pris) in priser:
        if sid == stasjons_id and typ == billett_type:
            return pris
    return 0
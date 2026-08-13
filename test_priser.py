from priser import lag_priser, hent_pris

def test_drammen_voksen_pris():
    priser = lag_priser()
    assert hent_pris(priser, 10, "voksen") == 324

def test_ugyldig_stasjon():
    priser = lag_priser()
    assert hent_pris (priser, 999, "voksen") == 0

def test_flytog_ansatt_alle_stasjoner():
    priser = lag_priser()
    for i in range (2,11):
        assert hent_pris(priser, i, "flytog-ansatt") == 0

def test_ungdom_pris_alle_stasjoner():
    priser = lag_priser()
    for i in range(2, 11):
        pris = hent_pris(priser, i, "ungdom")
        if i == 10:
            assert pris == 162
        elif 7 < i < 10:
            assert pris == 154
        elif 2 < i < 8:
            assert pris == 134
        else:
            assert pris == 105



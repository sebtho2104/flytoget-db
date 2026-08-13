import pytest
from ruter import rutetype, lag_stopp

def test_drammenstog_har_ni_stopp():
    avgang = [(3701, 1, 2, 10, 1, "06:00", 2)]
    stopp = lag_stopp(avgang)
    assert len(stopp) == 9

def test_første_stopp_ankomst_none():
    avgang = [(3701, 1, 2, 10, 1, "06:00", 2)]
    stopp = lag_stopp(avgang)
    assert stopp[0][4] is None  #sjekker element 5 i første rad

def test_siste_stopp_avgang_none():
    avgang = [(3723, 9, 1, 10, 1, '09:22', 2)]
    stopp = lag_stopp(avgang)
    assert stopp[-1][5] is None #sjekker element 6 i siste rad

def test_reversering_påvirker_ikke_senere_kall():
    avgang_retur = [(3702, 1, 1, 1, 10, '07:28', 1)]
    avgang_ut = [(3701, 1, 2, 10, 1, "06:00", 2)]
    lag_stopp(avgang_retur) #reverserer stasjons-logikken
    stopp_ut = lag_stopp(avgang_ut)
    assert stopp_ut[0][2] == 10 #sjekk om første stasjon fortsatt er Drammen

def test_invalid_avgangs_id():
    avgang = [(9999, 11, 1, 3, 1, '10:10', 2)]
    with pytest.raises(ValueError): #sjekker at denne koden som følger kaster ValueError
        lag_stopp(avgang)
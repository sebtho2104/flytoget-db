import pytest
import sys #sys.executable gives the correct Python-command no matter the OS/machine
import subprocess #makes it so the code starts and runs its own new programme
import sqlite3

@pytest.fixture(scope="module") #special function that only runs the first time its called
def kjørt_seed():
    resultat = subprocess.run([sys.executable, "seed.py"], capture_output = True, text = True) #start og kjør seed.py, og skriv ut utskriftene i terminalen
    return resultat

def test_seed_py_kjører_uten_feil(kjørt_seed):
    assert kjørt_seed.returncode == 0 #was the code successful?

@pytest.mark.parametrize("tabell, forventet_antall", [
    ("stasjoner", 10),
    ("tog", 13),
    ("avganger", 36)
])

def test_riktig_antall_stasjoner(kjørt_seed, tabell, forventet_antall):
    conn = sqlite3.connect("flytoget.db")
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {tabell}")
    assert cur.fetchone()[0] == forventet_antall
    conn.close()

def test_gjentatt_kjøring_gir_samme_resultat():
    subprocess.run([sys.executable, "seed.py"], capture_output=True, text=True)
    conn = sqlite3.connect("flytoget.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM avganger")
    avganger1 = cur.fetchall()
    conn.close()

    subprocess.run([sys.executable, "seed.py"], capture_output=True, text=True)
    conn = sqlite3.connect("flytoget.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM avganger")
    avganger2 = cur.fetchall()
    conn.close()

    assert avganger1 == avganger2

def test_ole_hansen_rett_pris(kjørt_seed):
    conn = sqlite3.connect("flytoget.db")
    cur = conn.cursor()
    cur.execute("SELECT pris FROM billetter WHERE kunde_navn = ? AND billett_type = ?", ("Ole Hansen", "voksen"))
    assert cur.fetchone()[0] == 324
    conn.close()

def test_ingen_avgang_uten_gyldig_tog(kjørt_seed):
    conn = sqlite3.connect("flytoget.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM avganger a LEFT JOIN tog t ON a.avgang_tog_nr = t.tog_nr WHERE t.tog_nr IS NULL")
    assert cur.fetchone()[0] == 0
    conn.close()

def test_foreign_keys_faktisk_håndheves(kjørt_seed):
    conn = sqlite3.connect("flytoget.db")
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON") #must set PRAGMA ON again, because it goes back to default OFF when seed.py ends
    with pytest.raises(sqlite3.IntegrityError): #waits for IntegrityError to occur
        cur.execute("INSERT INTO avganger (avgangs_id, avgang_tog_nr, antall_togsett, fra_stasjons_id, til_stasjons_id, avgangstid, plattform) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (9999, 999, 2, 1, 2, "06:00", 1)    
        )
    conn.close()
    

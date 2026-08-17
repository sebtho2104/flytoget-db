import pytest
import sys #sys.executable gives the correct Python-command no matter the OS/machine
import subprocess #makes it so the code starts and runs its own new programme
import sqlite3
import shutil #used to copy project files into the temporary test folder

@pytest.fixture
def kjørt_seed(tmp_path): #built in pytest fixture that gives one fresh, auto-clened folder per test
    for fil in ["seed.py", "schema.sql", "ruter.py", "priser.py"]:
        shutil.copy(fil, tmp_path / fil) #copies this file into tmp_path, keeping its original name
    resultat = subprocess.run([sys.executable, "seed.py"], capture_output = True, text = True, cwd = tmp_path) #start and run seed.py in tmp_path, and write the outputs to the terminal
    return resultat, tmp_path

def kjør_seed_i_mappe(mappe): #seperate helper since this specific test needs two fully independent runs to compare, not one shared run
    for fil in ["seed.py", "schema.sql", "ruter.py", "priser.py"]:
        shutil.copy(fil, mappe / fil)
    subprocess.run([sys.executable, "seed.py"], capture_output = True, text = True, cwd = mappe)

def test_seed_py_kjører_uten_feil(kjørt_seed):
    resultat, tmp_path = kjørt_seed #unpack both values from the ficture
    assert resultat.returncode == 0 #was the code successful?

@pytest.mark.parametrize("tabell, forventet_antall", [
    ("stasjoner", 10),
    ("tog", 13),
    ("avganger", 36)
])

def test_riktig_antall_stasjoner(kjørt_seed, tabell, forventet_antall):
    resultat, tmp_path = kjørt_seed
    conn = sqlite3.connect(tmp_path / "flytoget.db") #connect to the isolated temp database
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {tabell}")
    assert cur.fetchone()[0] == forventet_antall
    conn.close()

def test_gjentatt_kjøring_gir_samme_resultat(tmp_path_factory): #ifferent from tmp_path in the sense that I ask for new folders (can create more than one per test)
    mappe1 = tmp_path_factory.mktemp("kjøring1") #method to create a new real temporary folder
    kjør_seed_i_mappe(mappe1)
    conn = sqlite3.connect(mappe1 / "flytoget.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM avganger")
    avganger1 = cur.fetchall()
    conn.close()

    mappe2 = tmp_path_factory.mktemp("kjøring2")
    kjør_seed_i_mappe(mappe2)
    conn = sqlite3.connect(mappe2 / "flytoget.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM avganger")
    avganger2 = cur.fetchall()
    conn.close()

    assert avganger1 == avganger2

def test_ole_hansen_rett_pris(kjørt_seed):
    resultat, tmp_path = kjørt_seed
    conn = sqlite3.connect(tmp_path / "flytoget.db")
    cur = conn.cursor()
    cur.execute("SELECT pris FROM billetter WHERE kunde_navn = ? AND billett_type = ?", ("Ole Hansen", "voksen"))
    assert cur.fetchone()[0] == 324
    conn.close()

def test_ingen_avgang_uten_gyldig_tog(kjørt_seed):
    resultat, tmp_path = kjørt_seed
    conn = sqlite3.connect(tmp_path / "flytoget.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM avganger a LEFT JOIN tog t ON a.avgang_tog_nr = t.tog_nr WHERE t.tog_nr IS NULL")
    assert cur.fetchone()[0] == 0
    conn.close()

def test_foreign_keys_faktisk_håndheves(kjørt_seed):
    resultat, tmp_path = kjørt_seed
    conn = sqlite3.connect(tmp_path / "flytoget.db")
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON") #must set PRAGMA ON again, since it resets to default OFF for every new connection
    with pytest.raises(sqlite3.IntegrityError): #waits for IntegrityError to occur
        cur.execute("INSERT INTO avganger (avgangs_id, avgang_tog_nr, antall_togsett, fra_stasjons_id, til_stasjons_id, avgangstid, plattform) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (9999, 999, 2, 1, 2, "06:00", 1)    
        )
    conn.close()
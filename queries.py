import sqlite3

DB_FILE = "flytoget.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

resultater = []

def kjor_sporring(tittel, sql):
    cur.execute(sql)
    resultater.append((tittel, cur.fetchall()))

kjor_sporring ("All depatruters from Drammen", "SELECT * FROM avganger WHERE fra_stasjons_id = 10")

kjor_sporring ("Viser alle de unike billett-typene", "SELECT DISTINCT billett_type FROM billetter")

kjor_sporring ("Average delays per departure", "SELECT forsinkelse_avgangs_id, AVG(minutter_forsinket) FROM forsinkelser GROUP BY forsinkelse_avgangs_id")

kjor_sporring ("Ticket information together with departure station", "SELECT billett_id, billett_type, pris, stasjoner.navn from billetter INNER JOIN stasjoner ON billetter.billett_fra_id = stasjoner.stasjons_id")

kjor_sporring ("Full route for departure 3701 from Drammen to Gardemoen", "SELECT s.navn, ankomst_tid, avgangs_tid, rekkefolge FROM stopp INNER JOIN stasjoner as s ON stopp.stasjons_id=s.stasjons_id WHERE avgangs_id=3701 ORDER BY rekkefolge")

kjor_sporring ("Total sale per ticket type", "SELECT billett_type, SUM(pris) FROM billetter GROUP BY billett_type")

kjor_sporring ("Billetter solgt fra hver stasjon", "SELECT navn, count(b.billett_id) FROM stasjoner LEFT JOIN billetter as b ON stasjoner.stasjons_id=b.billett_fra_id GROUP BY navn")

kjor_sporring ("Billett id med kundenavn, eller 'Ukjent' om navn ikke er registrert", "SELECT billett_id, COALESCE(kunde_navn, 'Ukjent') FROM billetter")

kjor_sporring ("Avganger som i snitt har mer enn 10min forsinkelser på sine turer", "SELECT forsinkelse_avgangs_id, AVG(minutter_forsinket) FROM forsinkelser GROUP BY forsinkelse_avgangs_id HAVING AVG(minutter_forsinket > 10)")

kjor_sporring ("Hver registrerte forsinkelse med dato, minutter forsinket og tog type", "select t.tog_type, forsinkelse_dato, minutter_forsinket FROM forsinkelser INNER JOIN avganger as a ON forsinkelser.forsinkelse_avgangs_id=a.avgangs_id INNER JOIN tog as t ON a.avgang_tog_nr=t.tog_nr ORDER BY forsinkelse_id")

kjor_sporring ("Alle forsinkelser med en ny kategori som kategoriserer forsinkelsen utifra minutter forsinket", "SELECT forsinkelse_avgangs_id, minutter_forsinket, CASE WHEN minutter_forsinket < 5 THEN 'liten forsinkelse' WHEN minutter_forsinket <= 15 THEN 'middels forsinkelse' ELSE 'stor forsinkelse' END AS kategori FROM forsinkelser ORDER BY kategori")

kjor_sporring ("De tre største forsinkelsene", "SELECT forsinkelse_avgangs_id, minutter_forsinket FROM forsinkelser ORDER BY minutter_forsinket DESC LIMIT 3")

kjor_sporring ("Antall forsinkelser per tog type", "SELECT t.tog_type, COUNT(forsinkelse_id) FROM forsinkelser INNER JOIN avganger as a ON forsinkelser.forsinkelse_avgangs_id=a.avgangs_id INNER JOIN tog as t ON a.avgang_tog_nr=t.tog_nr GROUP BY t.tog_type")

for tittel, rader in resultater:
    print(f"{tittel}")
    for rad in rader: 
        print(rad)
    print()




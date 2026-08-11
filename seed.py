import os
import sqlite3
from ruter import lag_stopp
from priser import lag_priser, hent_pris

DB_FILE = "flytoget.db"

if os.path.exists(DB_FILE): # sjekker og sletter flytoget.db om den finnes
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE) # kobler til og lager (om det ikke finnes) database
cur = conn.cursor() # gjør det mulig å kjøre SQL gjennom tilkoblingen
cur.execute("PRAGMA foreign_keys = ON") #ensures foreign keys are actually enforced

with open("schema.sql") as f:
    cur.executescript(f.read()) # les all teksten fra filen, og kjør sql setningene i den

stasjoner = [
    (1, "Gardemoen"),
    (2, "Lillestrøm"),
    (3, "Oslo s"),
    (4, "Nationaltheatret"),
    (5, "Skøyen"),
    (6, "Stabekk"),
    (7, "Lysaker"),
    (8, "Sandvika"),
    (9, "Asker"),
    (10, "Drammen")
]

cur.executemany(
    "INSERT INTO stasjoner (stasjons_id, navn) VALUES (?, ?)", 
    stasjoner
)

tog = [
    (1, 78, 238), (2, 71, 250), (3, 78, 238), (4, 71, 250), (5, 78, 238),
    (6, 71, 250), (7, 78, 238), (8, 71, 250), (9, 78, 238), (10, 71, 250),
    (11, 78, 238), (12, 71, 250), (13, 78, 238)
]
cur.executemany(
    "INSERT INTO tog (tog_nr, tog_type, antall_seter) VALUES (?, ?, ?)", 
    tog
)

avganger = [
    (3701, 1, 2, 10, 1, '06:00', 2), (3702, 1, 1, 1, 10, '07:28', 1),
    (3703, 2, 2, 10, 1, '06:20', 2), (3704, 2, 1, 1, 10, '07:48', 1),
    (3705, 3, 1, 10, 1, '06:40', 2), (3706, 3, 1, 1, 10, '08:08', 1),
    (3707, 4, 1, 10, 1, '07:00', 2), (3708, 4, 1, 1, 10, '08:28', 1),
    (3709, 5, 1, 10, 1, '07:20', 2), (3710, 5, 1, 1, 10, '08:48', 1),
    (3711, 6, 1, 10, 1, '07:40', 2), (3712, 6, 1, 1, 10, '09:08', 1),
    (3713, 7, 1, 10, 1, '08:00', 2), (3714, 7, 1, 1, 10, '09:28', 1),
    (3715, 8, 1, 10, 1, '08:20', 2), (3716, 8, 1, 1, 10, '09:48', 1),
    (3717, 1, 1, 10, 1, '08:40', 2), (3718, 1, 1, 1, 10, '10:08', 1),
    (3719, 2, 1, 10, 1, '09:00', 2), (3720, 2, 1, 1, 10, '10:28', 1),
    (3721, 3, 1, 10, 1, '09:20', 2), (3722, 3, 1, 1, 10, '10:48', 1),
    (3723, 9, 1, 10, 1, '09:22', 2), (3724, 9, 1, 1, 10, '10:50', 1),
    (3725, 4, 1, 10, 1, '09:40', 2), (3726, 4, 1, 1, 10, '11:08', 1),
    (3727, 10, 1, 10, 1, '09:42', 2), (3728, 10, 1, 1, 10, '11:10', 1),
    (3729, 5, 1, 10, 1, '10:02', 2), (3730, 5, 2, 1, 10, '11:30', 1),
    (3731, 11, 1, 3, 1, '10:10', 2), (3732, 11, 1, 1, 3, '10:49', 1),
    (3733, 12, 1, 6, 1, '10:17', 2), (3734, 12, 1, 1, 6, '11:09', 1),
    (3735, 13, 1, 3, 1, '10:50', 2), (3736, 13, 1, 1, 3, '11:29', 1),
]
cur.executemany(
    "INSERT INTO avganger (avgangs_id, avgang_tog_nr, antall_togsett, fra_stasjons_id, til_stasjons_id, avgangstid, plattform) VALUES (?, ?, ?, ?, ?, ?, ?)", 
    avganger
    )

stopp = lag_stopp(avganger)
cur.executemany(
    "INSERT INTO stopp (stopp_id, avgangs_id, stasjons_id, rekkefolge, ankomst_tid, avgangs_tid) VALUES (?, ?, ?, ?, ?, ?)",
    stopp 
)

priser = lag_priser()
cur.executemany(
    "INSERT INTO priser (pris_id, stasjons_id, billett_type, pris) VALUES (?, ?, ?, ?)",
    priser,
)

billetter = [
    (1, 'Ole Hansen', 'voksen', 10, 1, '2025-05-01 08:15', '2025-07-30 08:15', 'ja', 324),
    (2, 'Kari Nilsen', 'student', 3, 1, '2025-05-03 09:30', '2025-08-01 09:30', 'ja', 134),
    (3, None, 'voksen', 1, 3, '2025-05-10 14:00', '2025-08-08 14:00', 'nei', 268),
    (4, 'Per Olsen', 'honnør', 9, 1, '2025-05-12 07:45', '2025-08-10 07:45', 'ja', 154),
    (5, 'Mona Berg', 'barn', 10, 1, '2025-05-15 12:00', '2025-08-13 12:00', 'nei', 0),
    (6, None, 'flytog-ansatt', 3, 1, '2025-05-18 06:30', '2025-08-16 06:30', 'ja', 0),
    (7, 'Jonas Aas', 'ungdom', 6, 1, '2025-05-20 16:20', '2025-08-18 16:20', 'ja', 134),
    (8, 'Ida Kristiansen', 'barn', 1, 10, '2025-05-22 11:10', '2025-08-20 11:10', 'nei', 162),
    (9, 'Erik Solheim', 'vernepliktig', 3, 1, '2025-05-25 18:00', '2025-08-23 18:00', 'ja', 134),
    (10, None, 'hentebillett', 1, 3, '2025-05-28 13:45', '2025-08-26 13:45', 'nei', 268),
]
cur.executemany(
    "INSERT INTO billetter (billett_id, kunde_navn, billett_type, billett_fra_id, billett_til_id, tid_kjøpt, tid_utløpt, aktivert, pris) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    billetter
)

conn.commit()
conn.close()
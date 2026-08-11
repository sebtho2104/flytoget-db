import os
import sqlite3
from datetime import datetime, timedelta
from ruter import lag_stopp

DB_FILE = "flytoget.db"

if os.path.exists(DB_FILE): # sjekker og sletter flytoget.db om den finnes
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE) # kobler til og lager (om det ikke finnes) database
cur = conn.cursor() # gjør det mulig å kjøre SQL gjennom tilkoblingen

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


conn.commit()
conn.close()
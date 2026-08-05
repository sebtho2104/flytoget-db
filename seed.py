import os
import sqlite3

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

cur.executemany("INSERT INTO stasjoner (stasjons_id, navn) VALUES (?, ?)", stasjoner)

tog = [
    (1, 78, 238),
    (2, 78, 238),
    (3, 78, 238),
    (4, 78, 238),
    (5, 78, 250),
    (6, 71, 250),
    (7, 71, 250),
    (8, 71, 250),
    (9, 71, 250),
    (10, 71, 250),
]

cur.executemany("INSERT INTO tog (tog_nr, tog_type, antall_seter) VALUES (?, ?, ?)", tog)

avganger = [
    (3701, 1, 2, 10, 1, '06:00', 2),
    (3702, 1, 2, 1, 10, '07:05', 1),
    (3703, 2, 2, 10, 1, '06:20', 2),
    (3704, 2, 2, 1, 10, '07:25', 1),
    (3705, 3, 2, 10, 1, '06:40', 2),
    (3706, 3, 2, 1, 10, '07:45', 1),
    (3707, 4, 2, 10, 1, '07:00', 2),
    (3708, 4, 2, 1, 10, '08:05', 1),
    (3709, 5, 2, 10, 1, '07:20', 2),
    (3710, 5, 2, 1, 10, '08:25', 1),
    (3711, 6, 2, 10, 1, '07:40', 2),
    (3712, 6, 2, 1, 10, '08:45', 1),
    (3713, 1, 2, 10, 1, '08:00', 2),
    (3714, 1, 2, 1, 10, '09:05', 1),
    (3715, 2, 2, 10, 1, '08:20', 2),
    (3716, 2, 2, 1, 10, '09:25', 1),
    (3717, 3, 2, 10, 1, '08:40', 2),
    (3718, 3, 2, 1, 10, '09:45', 1),
    (3719, 4, 2, 10, 1, '09:00', 2),
    (3720, 4, 2, 1, 10, '10:05', 1),
    (3721, 5, 2, 10, 1, '09:20', 2),
    (3722, 5, 2, 1, 10, '10:25', 1),
    (3723, 6, 2, 10, 1, '09:37', 2),
    (3724, 6, 2, 1, 10, '10:42', 1),
    (3725, 7, 2, 10, 1, '09:40', 2),
    (3726, 7, 2, 1, 10, '10:45', 1),
    (3727, 1, 2, 10, 1, '09:57', 2),
    (3728, 1, 2, 1, 10, '11:02', 1),
    (3729, 8, 1, 3, 1, '10:10', 2),
    (3730, 8, 1, 1, 3, '10:49', 1),
    (3731, 2, 2, 10, 1, '10:17', 2),
    (3732, 2, 2, 1, 10, '11:22', 1),
    (3733, 9, 1, 3, 1, '10:30', 2),
    (3734, 9, 1, 1, 3, '11:10', 1),
    (3735, 10, 1, 3, 1, '10:50', 2),
    (3736, 10, 1, 1, 3, '11:29', 1)
]

cur.executemany("INSERT INTO avganger (avgangs_id, avgang_tog_nr, antall_togsett, fra_stasjons_id, til_stasjons_id, avgangstid, plattform) VALUES (?, ?, ?, ?, ?, ?, ?)", avganger)

conn.commit()
conn.close()
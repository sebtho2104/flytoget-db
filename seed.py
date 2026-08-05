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

conn.commit()
conn.close()
import os
import sqlite3

DB_FILE = "flytoget.db"

if os.path.exists(DB_FILE): # sjekker og sletter flytoget.db om den finnes
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE) # kobler til og lager (om det ikke finnes) database
cur = conn.cursor() # gjør det mulig å kjøre SQL gjennom tilkoblingen

with open("schema.sql") as f:
    cur.executescript(f.read()) # les all teksten fra filen, og kjør sql setningene i den

import sqlite3

conn = sqlite3.connect("flytoget.db") # kobler til og lager (om det ikke finnes) database
cur = conn.cursor() # gjør det mulig å kjøre SQL gjennom tilkoblingen

with open("schema.sql") as f:
    cur.executescript(f.read()) # les all teksten fra filen, og kjør sql setningene i den

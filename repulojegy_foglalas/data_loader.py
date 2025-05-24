# data_loader.py

import sqlite3
from datetime import datetime, timedelta

from models.jarat import BelfoldiJarat, NemzetkoziJarat
from models.legitarsasag import LegiTarsasag
from models.jegy_foglalas import JegyFoglalas

DB_NAME = "foglalasok.db"


def initialize_database():
    """Létrehozza az adatbázis tábláit és feltölti alapadatokkal, ha szükséges."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Járatok tábla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jaratok (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipus TEXT NOT NULL,
            jaratszam TEXT NOT NULL,
            celallomas TEXT NOT NULL,
            jegyar INTEGER NOT NULL
        )
    ''')

    # Foglalások tábla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS foglalasok (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utas_nev TEXT NOT NULL,
            jarat_id INTEGER NOT NULL,
            datum TEXT NOT NULL,
            FOREIGN KEY (jarat_id) REFERENCES jaratok(id)
        )
    ''')

    # Csak akkor töltjük fel az alapadatokat, ha mindkét tábla üres
    cursor.execute("SELECT COUNT(*) FROM jaratok")
    jarat_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM foglalasok")
    foglalas_count = cursor.fetchone()[0]

    if jarat_count == 0 and foglalas_count == 0:
        cursor.executemany('''
            INSERT INTO jaratok (tipus, jaratszam, celallomas, jegyar)
            VALUES (?, ?, ?, ?)
        ''', [
            ("belfoldi", "BF123", "Budapest", 10000),
            ("nemzetkozi", "NZ456", "London", 35000),
            ("nemzetkozi", "NZ789", "Berlin", 28000),
        ])
        conn.commit()

        # Feltöltjük a foglalásokat is
        cursor.execute("SELECT id FROM jaratok")
        jarat_ids = [row[0] for row in cursor.fetchall()]
        nevek = ["Kovács Anna", "Nagy Béla", "Tóth Gábor", "Szabó Luca", "Varga Péter", "Oláh Zsófia"]
        for i in range(6):
            utas = nevek[i]
            jarat_id = jarat_ids[i % len(jarat_ids)]
            datum = (datetime.now() + timedelta(days=i + 1)).strftime("%Y-%m-%d")
            cursor.execute('''
                INSERT INTO foglalasok (utas_nev, jarat_id, datum)
                VALUES (?, ?, ?)
            ''', (utas, jarat_id, datum))
        conn.commit()

    conn.close()


def adatbetoltes():
    """Betölti a légitársaságot és a foglalásokat az adatbázisból."""
    initialize_database()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    legitarsasag = LegiTarsasag("PéldaLégitársaság")

    # Járatok betöltése
    cursor.execute("SELECT id, tipus, jaratszam, celallomas, jegyar FROM jaratok")
    rows = cursor.fetchall()
    jarat_dict = {}
    for row in rows:
        jarat_id, tipus, jaratszam, celallomas, jegyar = row
        if tipus == "belfoldi":
            jarat = BelfoldiJarat(jaratszam, celallomas, jegyar)
        elif tipus == "nemzetkozi":
            jarat = NemzetkoziJarat(jaratszam, celallomas, jegyar)
        else:
            continue
        legitarsasag.add_jarat(jarat)
        jarat_dict[jarat_id] = jarat

    # Foglalások betöltése
    cursor.execute("SELECT utas_nev, jarat_id, datum FROM foglalasok")
    foglalasok = []
    for utas_nev, jarat_id, datum_str in cursor.fetchall():
        jarat = jarat_dict.get(jarat_id)
        if jarat:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
            foglalas = JegyFoglalas(utas_nev, jarat, datum)
            foglalasok.append(foglalas)

    conn.close()
    return legitarsasag, foglalasok

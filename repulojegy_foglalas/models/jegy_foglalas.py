from datetime import datetime
import sqlite3
DB_NAME = "foglalasok.db"

class JegyFoglalas:
    """Egy repülőjegy-foglalás adatait tárolja."""
    def __init__(self, utas_nev, jarat, datum: datetime):
        self.utas_nev = utas_nev
        self.jarat = jarat
        self.datum = datum

    def get_foglalas_info(self):
        """Visszaadja a foglalás szöveges leírását."""
        return f"{self.utas_nev} - {self.jarat.get_info()} - {self.datum.strftime('%Y-%m-%d')}"

    @classmethod
    def get_foglalasok(cls, legitarsasag):
        """Lekéri az összes foglalást az adatbázisból."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        jaratok = legitarsasag.get_jaratok()
        cursor.execute("SELECT id, tipus, jaratszam, celallomas, jegyar FROM jaratok")
        jarat_id_map = {}
        for row in cursor.fetchall():
            jarat_id, tipus, jaratszam, celallomas, jegyar = row
            for jarat in jaratok:
                if jarat.jaratszam == jaratszam:
                    jarat_id_map[jarat_id] = jarat
                    break
        cursor.execute("SELECT id, utas_nev, jarat_id, datum FROM foglalasok")
        foglalasok = []
        for foglalas_id, utas_nev, jarat_id, datum_str in cursor.fetchall():
            jarat = jarat_id_map.get(jarat_id)
            if jarat:
                datum = datetime.strptime(datum_str, "%Y-%m-%d")
                foglalasok.append((foglalas_id, cls(utas_nev, jarat, datum)))
        conn.close()
        return foglalasok

    @classmethod
    def add_foglalas(cls, utas_nev, jarat, datum):
        """Új foglalást szúr be az adatbázisba."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM jaratok WHERE jaratszam = ?", (jarat.jaratszam,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False
        jarat_id = row[0]
        cursor.execute("INSERT INTO foglalasok (utas_nev, jarat_id, datum) VALUES (?, ?, ?)", (utas_nev, jarat_id, datum.strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete_foglalas(cls, foglalas_id):
        """Töröl egy foglalást az adatbázisból azonosító alapján."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM foglalasok WHERE id = ?", (foglalas_id,))
        conn.commit()
        conn.close()
        return True
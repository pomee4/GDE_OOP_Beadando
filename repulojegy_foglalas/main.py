from data_loader import adatbetoltes
from interface import felhasznaloi_felulet

def main():
    """Adatok betöltése"""
    legitarsasag, foglalasok = adatbetoltes()

    """Felhasználói felület indítása"""
    felhasznaloi_felulet(legitarsasag, foglalasok)

if __name__ == "__main__":
    main()
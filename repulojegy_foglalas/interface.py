import os
import sqlite3
from datetime import datetime
from models.jegy_foglalas import JegyFoglalas
from data_loader import DB_NAME, adatbetoltes

# Használt Színek, Stílusok ANSI kódjai
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
ENDC = '\033[0m'
BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Felhasználói felület kiírása
def felhasznaloi_felulet(legitarsasag, foglalasok):
    while True:
        clear_screen()
        print(f"{BOLD}{YELLOW}--- Repülőjegy Foglalási Rendszer ---{ENDC}")
        print(f"{GREEN}1.{ENDC} Jegy foglalása")
        print(f"{GREEN}2.{ENDC} Foglalás lemondása")
        print(f"{GREEN}3.{ENDC} Foglalások listázása")
        print(f"{GREEN}4.{ENDC} Kilépés")
        print(f"{YELLOW}{'-'*45}{ENDC}")
        valasz = input(f"{BOLD}Válassz egy lehetőséget (1-4): {ENDC}")

        if valasz == "1":
            clear_screen()
            jegy_foglalasa(legitarsasag)
        elif valasz == "2":
            clear_screen()
            foglalas_lemondasa(legitarsasag)
        elif valasz == "3":
            clear_screen()
            foglalasok_listazasa(legitarsasag)
            input(f"\n{BOLD}Nyomj Entert a folytatáshoz...{ENDC}")
        elif valasz == "4":
            print(f"{MAGENTA}Kilépés...{ENDC}")
            break
        else:
            print(f"{RED}Érvénytelen választás! Próbáld újra.{ENDC}")
            input(f"{BOLD}Nyomj Entert a folytatáshoz...{ENDC}")

def jegy_foglalasa(legitarsasag):
    utas_nev = input(f"{BOLD}Add meg az utas nevét: {ENDC}")
    print(f"\n{CYAN}Elérhető járatok:{ENDC}")
    jaratok = legitarsasag.get_jaratok()
    for i, jarat in enumerate(jaratok):
        print(f"{BOLD}{i + 1}.{ENDC} {jarat.get_info()}")
    try:
        valasztott_index = int(input(f"{BOLD}Válassz egy járatot (szám): {ENDC}")) - 1
        if valasztott_index < 0 or valasztott_index >= len(jaratok):
            print(f"{RED}Hibás járatszám.{ENDC}")
            return
    except ValueError:
        print(f"{RED}Érvénytelen bemenet.{ENDC}")
        return
    datum_str = input(f"{BOLD}Add meg az utazás dátumát (ÉÉÉÉ-HH-NN): {ENDC}")
    try:
        datum = datetime.strptime(datum_str, "%Y-%m-%d")
        if datum < datetime.now():
            print(f"{RED}Nem foglalható múltbeli dátumra.{ENDC}")
            return
    except ValueError:
        print(f"{RED}Hibás dátumformátum.{ENDC}")
        return
    jarat = jaratok[valasztott_index]
    siker = JegyFoglalas.add_foglalas(utas_nev, jarat, datum)
    if siker:
        print(f"{GREEN}Foglalás sikeres! Ár: {jarat.jegyar} Ft{ENDC}")
    else:
        print(f"{RED}Hiba: nem található a járat az adatbázisban.{ENDC}")

def foglalas_lemondasa(legitarsasag):
    foglalasok = JegyFoglalas.get_foglalasok(legitarsasag)
    if not foglalasok:
        print(f"{YELLOW}Nincsenek foglalások.{ENDC}")
        return
    print(f"\n{BOLD}{MAGENTA}--- Aktuális Foglalások ---{ENDC}")
    print(f"{CYAN}{'-'*60}{ENDC}")
    for i, (foglalas_id, foglalas) in enumerate(foglalasok):
        print(f"{BOLD}{i + 1}.{ENDC} {foglalas.get_foglalas_info()}")
    print(f"{CYAN}{'-'*60}{ENDC}")
    try:
        sorszam = int(input(f"{BOLD}Add meg a törlendő foglalás sorszámát: {ENDC}"))
        if sorszam < 1 or sorszam > len(foglalasok):
            print(f"{RED}Nem található ilyen sorszámú foglalás.{ENDC}")
            return
    except ValueError:
        print(f"{RED}Érvénytelen sorszám.{ENDC}")
        return
    torlendo_id = foglalasok[sorszam - 1][0]
    JegyFoglalas.delete_foglalas(torlendo_id)
    print(f"{GREEN}Foglalás törölve.{ENDC}")

def foglalasok_listazasa(legitarsasag):
    foglalasok = JegyFoglalas.get_foglalasok(legitarsasag)
    if not foglalasok:
        print(f"{YELLOW}Nincsenek foglalások.{ENDC}")
        return
    print(f"\n{BOLD}{MAGENTA}--- Aktuális Foglalások ---{ENDC}")
    print(f"{CYAN}{'='*60}{ENDC}")
    for i, (_, foglalas) in enumerate(foglalasok):
        print(f"{BOLD}{i + 1}.{ENDC} {foglalas.get_foglalas_info()}")
    print(f"{CYAN}{'='*60}{ENDC}")

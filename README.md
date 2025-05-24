# Repülőjegy Foglalási Rendszer

Ez a projekt egy egyszerű repülőjegy foglalási rendszer, amely lehetővé teszi járatokra jegy foglalását, foglalások lemondását, valamint az aktuális foglalások listázását. A rendszer Pythonban, objektumorientált szemlélettel készült, az adatokat SQLite adatbázisban tárolja.

## Fő funkciók
- Jegy foglalása belföldi vagy nemzetközi járatra
- Meglévő foglalás lemondása
- Aktuális foglalások listázása
- Adatvalidáció a járatok és dátumok ellenőrzésére

## Fő osztályok és szerkezet

- **Jarat (absztrakt osztály):** A járatok alapvető adatait és viselkedését írja le.
    - **BelfoldiJarat:** Belföldi járatot reprezentáló osztály.
    - **NemzetkoziJarat:** Nemzetközi járatot reprezentáló osztály.
- **LegiTarsasag:** Egy légitársaságot és annak járatait kezeli.
- **JegyFoglalas:** Egy utas foglalását tárolja egy adott járatra és időpontra.

## Fájlstruktúra

```
repulojegy_foglalas/
├── main.py                # Program belépési pontja
├── data_loader.py         # Adatbázis inicializálás, alapadatok betöltése
├── interface.py           # Parancssoros felhasználói felület
├── models/
│   ├── jarat.py           # Jarat, BelfoldiJarat, NemzetkoziJarat osztályok
│   ├── legitarsasag.py    # LegiTarsasag osztály
│   └── jegy_foglalas.py   # JegyFoglalas osztály és adatbázis műveletek
├── README.md              # Ez a leírás
└── adatok.txt             # Személyes adatok (név, szak, Neptun-kód)
```

## Adatbázis
- Az adatok a `foglalasok.db` SQLite adatbázisban tárolódnak.
- A rendszer első indításakor automatikusan létrejön a szükséges tábla és feltöltődik 3 járattal, valamint 6 foglalással.

## adatok.txt
A projekt gyökerében található `adatok.txt` tartalmazza a hallgató nevét, szakját és Neptun-kódját. Példa:

```
Készítette:
Név: Kovács Tamás
Szak: Mérnökinformatika
Neptun: IYWXUK
```

## Használat

1. Klónozd vagy másold a projektet a gépedre.
2. Győződj meg róla, hogy Python 3.8 vagy újabb verzió telepítve van.
3. Futtasd a programot a következő paranccsal:

```
python repulojegy_foglalas/main.py
```

A program parancssoros menüvel indul, ahol a következő lehetőségek közül választhatsz:
- Jegy foglalása
- Foglalás lemondása
- Foglalások listázása
- Kilépés

A menüpontokhoz tartozó utasításokat a képernyőn láthatod.

## OOP elvek
- A rendszer minden fő funkciója külön osztályban, jól elkülönítve valósul meg.
- Az öröklődés, absztrakció, polimorfizmus és kapszulázás elvei érvényesülnek.
- Az adatbázis-műveletek is a modellekhez tartoznak, így a logika átlátható és bővíthető.

## Megjegyzések
- A program kizárólag a Python beépített könyvtárait használja, külön csomag telepítése nem szükséges.
- A terminál színezést használ, amely a legtöbb modern parancssorban működik.

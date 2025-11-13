# Edzésterv nyílvántartó - DM

## Leírás
Ezzel a programmal edzésgyakorlatokat lehet nyílvántartani, progresszió követésének érdekében.

A programban:
- bal oldalt egy lista mutatja a felvett gyakorlatokat
- jobb oldalt egy űrlapon lehet megadni minden adatot a gyakorlattal kapcsolatban

Tárolt adatok:
- gyakorlat neve
- izomcsoport ami dolgozik a gyakorlat közben
- súly kg-ban
- sorozat
- ismétlés a sorozaton belül
- dátum
- megjegyzés ha rosszabb form-al vagy esetleg valami különös módon csináltuk a gyakorlatot
- létrehozás ideje

A gyakorlatokat a program a "gyakorlatok.json" fájlban tárolja

## Használt modulok
- "tkinter" - grafikus felület
- "json" - fájlba mentés / abból betöltés
- "datetime" - dátum és idő kezelésére
- "random" - motivációs üzenet véletlenszerű választására
- saját modul: "edzes_dm.py"
    - osztály: "GyakorlatDM"
    - függvények: "mentes_dm", "betoltes_dm"

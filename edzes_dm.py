import json
from datetime import datetime

class GyakorlatDM:
    def __init__(self, nev, izomcsoport, suly_kg, sorozat, ismetles, datum, megjegyzes):
        self.nev = nev
        self.izomcsoport = izomcsoport
        self.suly_kg = suly_kg
        self.sorozat = sorozat
        self.ismetles = ismetles
        self.datum = datum
        self.megjegyzes = megjegyzes
        self.letrehozas_ideje = datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        return {
            "nev": self.nev,
            "izomcsoport": self.izomcsoport,
            "suly_kg": self.suly_kg,
            "sorozat": self.sorozat,
            "ismetles": self.ismetles,
            "datum": self.datum,
            "megjegyzes": self.megjegyzes,
            "letrehozas_ideje": self.letrehozas_ideje,
        }

    @classmethod
    def from_dict(cls, adat):
        return cls(
            nev=adat.get("nev", ""),
            izomcsoport=adat.get("izomcsoport", ""),
            suly_kg=adat.get("suly_kg", 0),
            sorozat=adat.get("sorozat", 0),
            ismetles=adat.get("ismetles", 0),
            datum=adat.get("datum", ""),
            megjegyzes=adat.get("megjegyzes", ""),
        )


def mentes_dm(fajlnev, gyakorlatok):
    adatok = [gy.to_dict() for gy in gyakorlatok]
    szoveg = json.dumps(adatok, ensure_ascii=False, indent=2)
    with open(fajlnev, "w", encoding="utf-8") as f:
        f.write(szoveg)


def betoltes_dm(fajlnev):
    try:
        with open(fajlnev, "r", encoding="utf-8") as f:
            adatok = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    gyakorlatok = []
    for sor in adatok:
        gyakorlatok.append(GyakorlatDM.from_dict(sor))
    return gyakorlatok
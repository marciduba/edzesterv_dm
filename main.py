import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import random

from edzes_dm import GyakorlatDM, mentes_dm, betoltes_dm

class AppDM:
    def __init__(self, root):
        self.root = root
        self.root.title("Edzésterv nyílvántartó")
        self.root.geometry("800x500")
        self.root.minsize(700, 400)

        self.gyakorlatok = []
        self.kijelolt_index = None

        self._feluletes_felalitasa()
        self._betoltes_indulaskor()

    def _feluletes_felalitasa(self):
        fo_keret = tk.Frame(self.root)
        fo_keret.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        bal_keret = tk.Frame(fo_keret)
        bal_keret.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        jobb_keret = tk.Frame(fo_keret)
        jobb_keret.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(10, 0))

        lista_cimke = tk.Label(bal_keret, text="Gyakorlatok")
        lista_cimke.pack()

        self.lista = tk.Listbox(bal_keret, width=40, height=20)
        self.lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lista.bind("<<ListboxSelect>>", self._lista_kijeloles_valtozott)

        lista_gorgeto = tk.Scrollbar(bal_keret, orient = tk.VERTICAL)
        lista_gorgeto.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista.config(yscrollcommand=lista_gorgeto.set)
        lista_gorgeto.config(command=self.lista.yview)

        urlap = tk.Frame(jobb_keret)
        urlap.pack(fill=tk.BOTH, expand=True)

        tk.Label(urlap, text="Gyakorlat neve:").grid(row=0, column=0, sticky="w")
        tk.Label(urlap, text="Izomcsoport:").grid(row=1, column=0, sticky="w")
        tk.Label(urlap, text="Súly (kg):").grid(row=2, column=0, sticky="w")
        tk.Label(urlap, text="Sorozat").grid(row=3, column=0, sticky="w")
        tk.Label(urlap, text="Ismétlés:").grid(row=4, column=0, sticky="w")
        tk.Label(urlap, text="Dátum (ÉÉÉÉ-HH-NN)").grid(row=5, column=0, sticky="w")
        tk.Label(urlap, text="Megjegyzés").grid(row=6, column=0, sticky="nw")

        self.nev_var = tk.StringVar()
        self.izom_var = tk.StringVar()
        self.suly_var = tk.StringVar()
        self.sorozat_var = tk.StringVar()
        self.ismetles_var = tk.StringVar()
        self.datum_var = tk.StringVar()

        nev_mezo = tk.Entry(urlap, textvariable=self.nev_var)
        nev_mezo.grid(row=0, column=1, sticky="ew")

        izom_mezo = tk.Entry(urlap, textvariable=self.izom_var)
        izom_mezo.grid(row=1, column=1, sticky="ew")

        suly_mezo = tk.Entry(urlap, textvariable=self.suly_var)
        suly_mezo.grid(row=2, column=1, sticky="ew")

        sorozat_mezo = tk.Entry(urlap, textvariable=self.sorozat_var)
        sorozat_mezo.grid(row=3, column=1, sticky="ew")

        ismetles_mezo = tk.Entry(urlap, textvariable=self.ismetles_var)
        ismetles_mezo.grid(row=4, column=1, sticky="ew")

        self.datum_var.set(datetime.now().strftime("%Y-%m-%d"))
        datum_mezo = tk.Entry(urlap, textvariable=self.datum_var)
        datum_mezo.grid(row=5, column=1, sticky="ew")

        self.megjegyzes_mezo = tk.Text(urlap, height=5)
        self.megjegyzes_mezo.grid(row=6, column=1, sticky="nsew")

        urlap.columnconfigure(1, weight=1)
        urlap.rowconfigure(6, weight=1)

        gomb_keret = tk.Frame(jobb_keret)
        gomb_keret.pack(fill=tk.X, pady=(10, 0))

        uj_gomb = tk.Button(gomb_keret, text="Új gyakorlat", command=self.uj_gomb_lenyomva)
        uj_gomb.pack(side=tk.LEFT,)

        ment_gomb = tk.Button(gomb_keret, text="Mentés / módosítás", command=self.mentes_gomb_lenyomva)
        ment_gomb.pack(side=tk.LEFT, padx=5)

        torol_gomb = tk.Button(gomb_keret, text="Törlés", command=self.torles_gomb_lenyomva)
        torol_gomb.pack(side=tk.LEFT)

        menu = tk.Menu(self.root)
        fajl_menu = tk.Menu(menu, tearoff=0)
        fajl_menu.add_command(label="Mentés", command=self._mentes_fajlba)
        fajl_menu.add_command(label="Kilépés", command=self.root.destroy)
        menu.add_cascade(label="Fájl", menu=fajl_menu)

        self.root.config(menu=menu)

    def _lista_kijeloles_valtozott(self, event):
        if not self.lista.curselection():
            return
        index = self.lista.curselection()[0]
        self.kijelolt_index = index
        gy = self.gyakorlatok[index]
        self._urlap_kitoltese(gy)

    def _urlap_kitoltese(self, gyakorlat):
        self.nev_var.set(gyakorlat.nev)
        self.izom_var.set(gyakorlat.izomcsoport)
        self.suly_var.set(gyakorlat.suly_kg)
        self.sorozat_var.set(gyakorlat.sorozat)
        self.ismetles_var.set(gyakorlat.ismetles)
        self.datum_var.set(gyakorlat.datum)
        self.megjegyzes_mezo.delete("1.0", tk.END)
        self.megjegyzes_mezo.insert(tk.END, gyakorlat.megjegyzes)

    def uj_gomb_lenyomva(self):
        self.kijelolt_index = None
        self.nev_var.set("")
        self.izom_var.set("")
        self.suly_var.set("")
        self.sorozat_var.set("")
        self.ismetles_var.set("")
        self.datum_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.megjegyzes_mezo.delete("1.0", tk.END)

    def mentes_gomb_lenyomva(self):
        try:
            suly = float(self.suly_var.get()) if self.suly_var.get() else 0.0
            sorozat = int(self.sorozat_var.get()) if self.sorozat_var.get() else 0
            ismetles = int(self.ismetles_var.get()) if self.ismetles_var.get() else 0
        except ValueError:
            messagebox.showerror("Hiba", "A súly, sorozat és ismétlés mezőkben csak szám lehet.")
            return
        try:
            datum_obj = datetime.strptime(self.datum_var.get(), "%Y-%m-%d")
            datum_szoveg = datum_obj.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Hiba", "A dátum formátuma : ÉÉÉÉ-HH-NN, pl. 2025-03-15")
            return
        if not self.nev_var.get() or not self.izom_var.get():
            messagebox.showwarning("Hiányzó adat", "A gyakorlat neve és az izomcsoport kötelező.")
            return
        gy = GyakorlatDM(
            nev=self.nev_var.get(),
            izomcsoport=self.izom_var.get(),
            suly_kg=suly,
            sorozat=sorozat,
            ismetles=ismetles,
            datum=datum_szoveg,
            megjegyzes=self.megjegyzes_mezo.get("1.0", tk.END).strip()
        )
        if self.kijelolt_index is None:
            self.gyakorlatok.append(gy)
        else:
            self.gyakorlatok[self.kijelolt_index] = gy
        self._lista_frissitese()
        self._mentes_fajlba()
        motivaciok = [
            "Szép munka, ne add fel!",
            "Ma is tettél valamit magadért.",
            "Közelebb kerültél a célodhoz.",
            "Kis lépésekből lesz a nagy változás.",
            "Csak így tovább!"
        ]
        uzenet = random.choice(motivaciok)
        messagebox.showinfo("mentve", uzenet)

    def torles_gomb_lenyomva(self):
        if self.kijelolt_index is None:
            messagebox.showinfo("Nincs kijelölés", "Elöbb válassz ki egy gyakorlatot a listából.")
            return
        del self.gyakorlatok[self.kijelolt_index]
        self.kijelolt_index = None
        self._lista_frissitese()
        self.uj_gomb_lenyomva()
        self._mentes_fajlba()

    def _lista_frissitese(self):
        self.lista.delete(0, tk.END)
        for gy in self.gyakorlatok:
            sor = f"{gy.izomcsoport}: {gy.nev} {gy.suly_kg} kg - {gy.sorozat}x{gy.ismetles}"
            self.lista.insert(tk.END, sor)

    def _betoltes_indulaskor(self):
        self.gyakorlatok = betoltes_dm("gyakorlatok.json")
        self._lista_frissitese()

    def _mentes_fajlba(self):
        mentes_dm("gyakorlatok.json", self.gyakorlatok)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppDM(root)
    root.mainloop()


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# ------------------ Fachklassen ------------------

class Fahrzeug:
    def __init__(self, kennzeichen):
        self.kennzeichen = kennzeichen

    def typ(self):
        return "Fahrzeug"

class Auto(Fahrzeug):
    def typ(self):
        return "Auto"

class Motorrad(Fahrzeug):
    def typ(self):
        return "Motorrad"

class Parkhaus:
    def __init__(self, etagen, plaetze_pro_etage):
        self.etagen = etagen
        self.plaetze_pro_etage = plaetze_pro_etage
        self.plaetze = [["frei" for _ in range(plaetze_pro_etage)] for _ in range(etagen)]
        self.belegung = {}  # Kennzeichen -> (Etage, Platz)

    def einfahren(self, fahrzeug):
        kz = fahrzeug.kennzeichen
        if kz in self.belegung:
            return f"{kz} ist bereits im Parkhaus."

        for e, etage in enumerate(self.plaetze):
            for p, platz in enumerate(etage):
                if platz == "frei":
                    self.plaetze[e][p] = fahrzeug
                    self.belegung[kz] = (e, p)
                    return f"{fahrzeug.typ()} {kz} geparkt: Etage {e}, Platz {p}"
        return "Parkhaus ist voll!"

    def ausfahren(self, kennzeichen):
        pos = self.belegung.pop(kennzeichen, None)
        if not pos:
            return "Fahrzeug nicht gefunden."
        e, p = pos
        self.plaetze[e][p] = "frei"
        return f"{kennzeichen} hat das Parkhaus verlassen (Etage {e}, Platz {p})."

    def finde_fahrzeug(self, kennzeichen):
        pos = self.belegung.get(kennzeichen)
        if pos:
            return f"{kennzeichen} steht auf Etage {pos[0]}, Platz {pos[1]}."
        else:
            return "Fahrzeug nicht im Parkhaus."

    def freie_plaetze(self):
        frei = sum(platz == "frei" for etage in self.plaetze for platz in etage)
        return f"Freie Plätze gesamt: {frei}"

    def plaetze_uebersicht(self):
        """Gibt eine Textübersicht aller Plätze zurück."""
        lines = []
        for e, etage in enumerate(self.plaetze):
            lines.append(f"Etage {e}:")
            for p, platz in enumerate(etage):
                if platz == "frei":
                    info = "frei"
                else:
                    info = f"{platz.typ()} ({platz.kennzeichen})"
                lines.append(f"  Platz {p}: {info}")
            lines.append("")  # Leerzeile
        return "\n".join(lines)


# ------------------ GUI-Klasse ------------------

class ParkhausGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Parkhaus Verwaltung")
        self.root.configure(bg="#675b5b")
        self.parkhaus = None

        # ---------- Parkhaus Daten ----------
        self.frame_ph = tk.LabelFrame(root, text="Parkhaus Daten")
        self.frame_ph.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        tk.Label(self.frame_ph, text="EtagenAnzahl",).grid(row=0, column=0, padx=5, pady=5)
        self.entry_etagen = tk.Entry(self.frame_ph, width=10)
        self.entry_etagen.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_ph, text="ParkPlatzProEtage",).grid(row=0, column=2, padx=5, pady=5)
        self.entry_plaetze = tk.Entry(self.frame_ph, width=10)
        self.entry_plaetze.grid(row=0, column=3, padx=5, pady=5)

        self.btn_ph_anlegen = tk.Button(self.frame_ph, text="Einlegen", bg="#2e86ff",
                                        command=self.parkhaus_anlegen)
        self.btn_ph_anlegen.grid(row=0, column=4, padx=10, pady=5)

        # ---------- Fahrzeuge Daten ----------
        self.frame_fz = tk.LabelFrame(root, text="Fahrzeuge Daten")
        self.frame_fz.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        tk.Label(self.frame_fz, text="Kennzeichen",).grid(row=0, column=0, padx=5, pady=5)
        self.entry_kz_fz = tk.Entry(self.frame_fz, width=15)
        self.entry_kz_fz.grid(row=0, column=1, padx=5, pady=5)

        self.btn_auto_einlegen = tk.Button(self.frame_fz, text="Auto Einlegen", bg="#2e86ff",
                                           command=self.auto_einlegen)
        self.btn_auto_einlegen.grid(row=0, column=2, padx=10, pady=5)

        tk.Label(self.frame_fz, text="Kennzeichen",).grid(row=0, column=3, padx=5, pady=5)
        self.entry_kz_mot = tk.Entry(self.frame_fz, width=15)
        self.entry_kz_mot.grid(row=0, column=4, padx=5, pady=5)

        self.btn_mot_einlegen = tk.Button(self.frame_fz, text="Motorrad Einlegen", bg="#2e86ff",
                                          command=self.motorrad_einlegen)
        self.btn_mot_einlegen.grid(row=0, column=5, padx=10, pady=5)

        # ---------- Operationen ----------
        self.frame_ops = tk.LabelFrame(root, text="Operationen")
        self.frame_ops.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.frame_ops.columnconfigure(3, weight=1)
        self.frame_ops.rowconfigure(3, weight=1)

        # Links: Kennzeichen + Buttons
        tk.Label(self.frame_ops, text="Kennzeichen").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_kz_parken = tk.Entry(self.frame_ops, width=15)
        self.entry_kz_parken.grid(row=0, column=1, padx=5, pady=5)

        self.btn_parken = tk.Button(self.frame_ops, text="Parken", bg="#2e86ff",
                                    command=self.parken_auto_von_ops)
        self.btn_parken.grid(row=0, column=2, padx=10, pady=5)

        tk.Label(self.frame_ops, text="Kennzeichen").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_kz_aus = tk.Entry(self.frame_ops, width=15)
        self.entry_kz_aus.grid(row=1, column=1, padx=5, pady=5)

        self.btn_ausfahren = tk.Button(self.frame_ops, text="Rausfahren", bg="#2e86ff",
                                       command=self.ausfahren)
        self.btn_ausfahren.grid(row=1, column=2, padx=10, pady=5)

        tk.Label(self.frame_ops, text="Kennzeichen").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_kz_suchen = tk.Entry(self.frame_ops, width=15)
        self.entry_kz_suchen.grid(row=2, column=1, padx=5, pady=5)

        self.btn_suchen = tk.Button(self.frame_ops, text="Suchen", bg="#2e86ff",
                                    command=self.suchen)
        self.btn_suchen.grid(row=2, column=2, padx=10, pady=5)

        # Mitte / rechts: Status + Textfeld
        self.btn_status = tk.Button(self.frame_ops, text="PH Status", bg="#2e86ff",
                                    command=self.show_status)
        self.btn_status.grid(row=0, column=3, padx=10, pady=5, sticky="ne")

        self.text_plaetze = tk.Text(self.frame_ops, width=40, height=12)
        self.text_plaetze.grid(row=1, column=3, rowspan=3, padx=10, pady=5, sticky="nsew")

        # Unten: Filter
        self.filter_var = tk.StringVar(value="Auto")
        rb_auto = tk.Radiobutton(self.frame_ops, text="Autos", variable=self.filter_var, value="Auto")
        rb_mot = tk.Radiobutton(self.frame_ops, text="Motorräder", variable=self.filter_var, value="Motorrad")
        rb_auto.grid(row=4, column=0, padx=5, pady=5)
        rb_mot.grid(row=4, column=1, padx=5, pady=5)

        self.btn_filtern = tk.Button(self.frame_ops, text="Filtern", bg="#2e86ff",
                                     command=self.filtern)
        self.btn_filtern.grid(row=4, column=2, padx=10, pady=5)

        self.text_filter = tk.Text(self.frame_ops, width=60, height=4)
        self.text_filter.grid(row=5, column=0, columnspan=4, padx=10, pady=5, sticky="ew")

    # ---------- Methoden für Buttons ----------

    def check_parkhaus(self):
        if self.parkhaus is None:
            messagebox.showwarning("Kein Parkhaus", "Bitte zuerst Parkhaus anlegen.")
            return False
        return True

    def parkhaus_anlegen(self):
        try:
            etagen = int(self.entry_etagen.get())
            plaetze = int(self.entry_plaetze.get())
            if etagen <= 0 or plaetze <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Fehler", "Etagen und Plätze müssen positive ganze Zahlen sein.")
            return

        self.parkhaus = Parkhaus(etagen, plaetze)
        messagebox.showinfo("Parkhaus", f"Parkhaus mit {etagen} Etagen und {plaetze} Plätzen pro Etage angelegt.")
        self.update_plaetze_text()

    def auto_einlegen(self):
        if not self.check_parkhaus():
            return
        kz = self.entry_kz_fz.get().strip()
        if not kz:
            messagebox.showerror("Fehler", "Kennzeichen eingeben.")
            return
        msg = self.parkhaus.einfahren(Auto(kz))
        messagebox.showinfo("Auto Einlegen", msg)
        self.update_plaetze_text()

    def motorrad_einlegen(self):
        if not self.check_parkhaus():
            return
        kz = self.entry_kz_mot.get().strip()
        if not kz:
            messagebox.showerror("Fehler", "Kennzeichen eingeben.")
            return
        msg = self.parkhaus.einfahren(Motorrad(kz))
        messagebox.showinfo("Motorrad Einlegen", msg)
        self.update_plaetze_text()

    def parken_auto_von_ops(self):
        """Einfaches Parken als Auto über den unteren Bereich."""
        if not self.check_parkhaus():
            return
        kz = self.entry_kz_parken.get().strip()
        if not kz:
            messagebox.showerror("Fehler", "Kennzeichen eingeben.")
            return
        msg = self.parkhaus.einfahren(Auto(kz))
        messagebox.showinfo("Parken", msg)
        self.update_plaetze_text()

    def ausfahren(self):
        if not self.check_parkhaus():
            return
        kz = self.entry_kz_aus.get().strip()
        if not kz:
            messagebox.showerror("Fehler", "Kennzeichen eingeben.")
            return
        msg = self.parkhaus.ausfahren(kz)
        messagebox.showinfo("Rausfahren", msg)
        self.update_plaetze_text()

    def suchen(self):
        if not self.check_parkhaus():
            return
        kz = self.entry_kz_suchen.get().strip()
        if not kz:
            messagebox.showerror("Fehler", "Kennzeichen eingeben.")
            return
        msg = self.parkhaus.finde_fahrzeug(kz)
        messagebox.showinfo("Suche", msg)

    def show_status(self):
        if not self.check_parkhaus():
            return
        msg = self.parkhaus.freie_plaetze()
        messagebox.showinfo("Parkhaus Status", msg)
        self.update_plaetze_text()

    def update_plaetze_text(self):
        if not self.check_parkhaus():
            return
        self.text_plaetze.delete("1.0", tk.END)
        self.text_plaetze.insert(tk.END, self.parkhaus.plaetze_uebersicht())

    def filtern(self):
        if not self.check_parkhaus():
            return
        ziel_typ = self.filter_var.get()
        lines = [f"{ziel_typ}-Fahrzeuge im Parkhaus:\n"]
        for kz, (e, p) in self.parkhaus.belegung.items():
            fz = self.parkhaus.plaetze[e][p]
            if fz.typ() == ziel_typ:
                lines.append(f"{kz}: Etage {e}, Platz {p}")
        if len(lines) == 1:
            lines.append("keine gefunden.")
        self.text_filter.delete("1.0", tk.END)
        self.text_filter.insert(tk.END, "\n".join(lines))


# ------------------ Start ------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkhausGUI(root)
    root.mainloop()
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
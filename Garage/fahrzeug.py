class Fahrzeug:
    def __init__(self, kennzeichen):
        self.kennzeichen = kennzeichen

    def typ(self):
        return "Fahrzeug"
    def info(self):
        return f"{self.typ()} mit kennenzeichnen {self.kennzeichen}"
    
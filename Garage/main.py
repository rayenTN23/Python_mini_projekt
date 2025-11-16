from autos import Auto
from motorraeder import Motorrad
from parkhaus import Parkhaus

haus = Parkhaus(3,3)

# Fahrzeuge erstellen
a1 = Auto("K-AB123")
a2 = Auto("BN-XY999")
a3 = Auto("D-CD555")
m1 = Motorrad("K-MO01")
m2 = Motorrad("K-MO02")

# Einfahren
print("-"*32,"\n", " -"*28)
print(haus.einfahren(a1))
print(haus.einfahren(a2))
print(haus.einfahren(a3))
print(haus.einfahren(m1))
print(haus.einfahren(m2))

# Freie Plätze + Übersicht
print("-"*30)
print(haus.freie_plaetze())
print(haus.finde_fahrzeug("K-MO02"))

# Ausfahren
print("-"*30)
print(haus.ausfahren("K-MO02"))
print(haus.freie_plaetze())
print(" -"*26,"\n", "-"*30)
print(haus.einfahren(m2))
print(haus.freie_plaetze())
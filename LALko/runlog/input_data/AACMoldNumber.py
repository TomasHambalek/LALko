# Vytvoření seznamu pro G_VALUES (G00 až G50)
G_VALUES = []
for i in range(51):
    G_VALUES.append({"name": f"G{i:02d}"})

# Vytvoření seznamu pro Y_VALUES (Y00 až Y99)
Y_VALUES = []
for i in range(100):
    Y_VALUES.append({"name": f"Y{i:02d}"})

# Sloučení obou seznamů do jedné proměnné
AACMOLDNUMBER = G_VALUES + Y_VALUES
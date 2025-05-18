import pandas as pd
import json

# Charger le fichier JSON
with open("channels.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Convertir en DataFrame
df = pd.DataFrame(data)

# Sauvegarder au format Excel
df.to_excel("channels.xlsx", index=False)

import pandas as pd
import json

# Charger le fichier Excel
df = pd.read_excel("channels.xlsx")

# Convertir en JSON
json_data = df.to_json(orient="records", indent=1, force_ascii=False)

# Sauvegarder au format JSON
with open("channels_france.json", "w", encoding="utf-8") as file:
    file.write(json_data)

print("Conversion terminée : 'channels.xlsx' -> 'channels_france.json'")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL de la page contenant les tableaux
url = 'https://en.wikipedia.org/wiki/List_of_fake_news_websites'


# Envoyer une requête GET
response = requests.get(url)

# Liste pour stocker tous les DataFrames extraits
all_tables = []

if response.status_code == 200:
    # Parser le contenu HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trouver tous les tableaux
    tables = soup.find_all('table')
    
    # Parcourir tous les tableaux trouvés
    for i, table in enumerate(tables):
        # Extraire les en-têtes (limité aux 4 premières colonnes)
        headers = [header.text.strip() for header in table.find_all('th')[:4]]
        
        # Extraire les lignes de données
        rows = []
        for row in table.find_all('tr'):
            cells = [cell.text.strip() for cell in row.find_all('td')[:4]]
            if cells:  # Ignorer les lignes sans cellules
                rows.append(cells)
        
        # Si le tableau n'a pas d'en-têtes, générer des colonnes par défaut
        if not headers:
            headers = [f"Colonne {i+1}" for i in range(len(rows[0]))]  # Colonnes numérotées dynamiquement
        
        # Créer un DataFrame Pandas pour ce tableau
        try:
            df = pd.DataFrame(rows, columns=headers)
            all_tables.append(df)  # Ajouter ce DataFrame à la liste
        except ValueError as e:
            print(f"Erreur de colonnes pour le tableau {i+1}: {e}")
            continue  # Passer au tableau suivant si une erreur de colonnes se produit
    
    # Concaténer tous les DataFrames dans un seul
    final_df = pd.concat(all_tables, ignore_index=True)
    
    # Créer un dossier pour sauvegarder les fichiers CSV (si nécessaire)
    os.makedirs('fakenews', exist_ok=True)
    
    # Sauvegarder tous les tableaux concaténés dans un seul fichier CSV
    final_df.to_csv('fakenews/tableau.csv', index=False, encoding='utf-8')
    print(f"Tous les tableaux ont été sauvegardés dans 'fakenews/all_tables_combined.csv'.")
else:
    print(f"Échec de la requête, code: {response.status_code}")

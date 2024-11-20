import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = 'https://en.wikipedia.org/wiki/List_of_fake_news_websites'


response = requests.get(url)

all_tables = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    tables = soup.find_all('table')
    

    for i, table in enumerate(tables):
        headers = [header.text.strip() for header in table.find_all('th')[:4]]
        
        rows = []
        for row in table.find_all('tr'):
            cells = [cell.text.strip() for cell in row.find_all('td')[:4]]
            if cells: 
                rows.append(cells)
        
        if not headers:
            headers = [f"Colonne {i+1}" for i in range(len(rows[0]))] 
        
        try:
            df = pd.DataFrame(rows, columns=headers)
            all_tables.append(df)  
        except ValueError as e:
            print(f"Erreur de colonnes pour le tableau {i+1}: {e}")
            continue  

    final_df = pd.concat(all_tables, ignore_index=True)
    
    os.makedirs('fakenews', exist_ok=True)
    
    final_df.to_csv('fakenews/tableau.csv', index=False, encoding='utf-8')
    print(f"Le mining a été effectué avec succes")
else:
    print(f"Échec de la requête, code: {response.status_code}")

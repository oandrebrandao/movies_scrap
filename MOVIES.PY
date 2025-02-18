import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "https://imdb.com/chart/top/"
table_attribs = ['title', 'release_year', 'length', 'rating', 'score']
output_path = 'imdb_top250.csv'
db_name = 'top250.db'
table_name = 'Top_Movies'

def extract (url, table_attribs):
    '''Essa função extrai os dados do site IMDB e após as devidas validações, retorna um DataFrame com os dados extraídos.
    Parâmetros: url (str): URL do site a ser extraído
                table_attribs (list): Lista de strings com os nomes das colunas do DataFrame
                Retorno: df (DataFrame): DataFrame com os dados extraídos do site   
    This function extracts data from the IMDB website and after the necessary validations, returns a DataFrame with the extracted data.
    Parameters: url (str): URL of the site to be extracted 
                table_attribs (list): List of strings with the names of the DataFrame columns
                Return: df (DataFrame): DataFrame with the data extracted from the site'''
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        df = pd.DataFrame(columns=table_attribs)
        movies = soup.find_all('div', {'class': 'cli-children'}) 
        data = []
        for movie in movies:
            try:
                title = movie.find('h3', {'class':'ipc-title__text'}).text.split('.')[-1].strip() if movie.find('h3', {'class':'ipc-title__text'}) else None
                metadata_items = movie.find_all('span',{'class':'cli-title-metadata-item'})
                release_year = metadata_items[0].text.strip() if len(metadata_items) > 0 else None
                length = metadata_items[1].text.strip() if len(metadata_items) > 1 else None
                rating = metadata_items[2].text.strip() if len(metadata_items) > 2 else None
                score = movie.find('span', {'class':'ipc-rating-star--rating'}).text.strip() if movie.find('span', {'class':'ipc-rating-star--rating'}) else None
                data.append({'title': title, 'release_year': release_year, 'length': length, 'rating': rating, 'score': score})
            except AttributeError as e:
                print(f"Failed to retrieve the data. Error: {e}")
        df = pd.DataFrame(data, columns=table_attribs)
        return df
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

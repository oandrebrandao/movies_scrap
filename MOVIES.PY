from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import mysql.connector
 
 
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
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    first_height = driver.execute_script("return document.body.scrollHeight") 
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == first_height:
            break
        first_height = new_height
    
    page_source = driver.page_source
    driver.quit()
    soup = bs(page_source.content, 'html.parser')
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

def transform(df):
    ''' Essa função transforma os dados do data frame que representam números para os tipos corretos e converte as linhas da coluna 'length' para minutos
        Parametros: df: data frame
        Retorno: df: data frame
        
        This function transforms the data frame data that represents numbers to the correct types and converts the rows of the 'length' column to minutes
        Parameters: df: data frame  
        Return: df: data frame'''

    df['release_year'] = int(df['release_year']) if df['release_year'] else None
    df['length'] = int(df['length'].split('h')[0])*60 + int(df['length'].split('h')[1].strip('m')) if df['length'] else None
    df['score'] = float(df['score']) if df['score'] else None
    return df

def load_csv(df, output_path):
    ''' Essa função salva o data frame em um arquivo csv
        Parametros: df: data frame
                    output_path: string
        Retorno: None
        
        This function saves the data frame to a csv file
        Parameters: df: data frame
                    output_path: string
        Return: None'''
    
    df.to_csv(output_path, index=False)
    print(f'Data frame salvo em {output_path}')

def load_db(df, sql_connection, table_name):
    ''' Essa função salva o data frame em uma tabela de um banco de dados MySQL
       Parametros: df: data frame
                   sql_connection: string
                   table_name: string
        Retorno: None
        
        This function saves the data frame to a MySQL database table
        Parameters: df: data frame
                   sql_connection: string
                   table_name: string
        Return: None'''
    
    df.to_sql(table_name, sql_connection, if_exists ='replace',  index=False)


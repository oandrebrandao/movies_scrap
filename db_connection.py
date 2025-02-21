import mysql.connector
import os

def connect_db(db_name):
    '''Essa função conecta ao banco de dados e retorna a conexão
    Parâmetros: db_name (str): Nome do banco de dados
    Retorno: connection (obj): Conexão com o banco de dados
    This function connects to the database and returns the connection
    Parameters: db_name (str): Database name
    Return: connection (obj): Database connection'''
    con = {
        'host': 'localhost',
        'user': os.getenv('USER'),
        'password': os.getenv('SENHA'),
        'database': db_name,
        'raise_on_warnings': True
    }

    try:
        connection = mysql.connector.connect(**con)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}") 
        return None
    
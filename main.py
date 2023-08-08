from fastapi import FastAPI
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors

# Titulo y Descripcion
app = FastAPI(title='Proyecto Nº 1 Stram Games', description='API de datos y analalizis de juegos')

# Global variables
df = None
nn = None

@app.on_event("startup")
async def load_data():
    global df, nn
    df = pd.read_csv('steam_games_normalizado.csv')
    
@app.get('/')
async def read_root():
    return {'Mi primera API. Dirígite a /docs'}    

@app.get('/')
async def about():
    return {'Proyecto individual Nº1: Analisis de steam'}
   

#Funcion para devolver un top 5 de generos segun el año
@app.get('/{Year}')
def genero(Year:str):
    while True:
        if Year.isdigit():  # Verifica si es un número válido
            df_year = df[df['year'] == Year]
            top_generos = df_year['genres'].explode().value_counts().head(5).index.to_dict()
            return top_generos
        else:
            print("Error: El valor ingresado no es valido.")
            break

#Funcion para devolver los juegos de determinado año
@app.get('/app_game/{Year}')
def juegos(Year:str):
    while True:
        if Year.isdigit():  # Verifica si es un número válido
            df_year = df[df['year'] == Year]
            top_titulos_completos = df['app_game'].explode().value_counts().to_dict()
            
            return  print("Los juegos del año son:",top_titulos_completos)
        else:
            print("Error: El valor ingresado no es valido.")
            break

#Funcion que devuelve los 5 specs mas repetidos del año
@app.get('/specs/{Year}')
def specs(Year:str):
    while True:
        if Year.isdigit():  # Verifica si es un número válido
            df_year = df[df['year'] == Year]
            top_spesc=df_year['specs'].explode().value_counts().head(5).index.to_dict()
            return top_spesc
        else:
            print("Error: El valor ingresado no es valido.")
            break

#Funcion para los juegos que salieron con Early Access en el año
@app.get('/Early Access/{Year}')
def early_access(Year: str):
    if Year.isdigit():  # Verifica si es un número válido
        df_year = df[df['year'] == int(Year)]  # Convertir a entero
        df_early_access = df_year[df_year['early_access'] == True]
        count_early_access = df_early_access.shape[0]  # Contar la cantidad de filas

        return {'cantidad de juegos con early access': count_early_access}
    else:
        return {'error': "El valor ingresado no es válido."}
    
#Funcion para ver los sentiment del año
@app.get('/Sentiment/{Year}')
def Sentiment(Year:str):
    if Year.isdigit():  # Verifica si es un número válido
        df_year = df[df['year'] == int(Year)]  # Convertir a entero

        # Filtrar los títulos sin 'nan' y sin user reviews del 1 al 9
        filtered_titles = df_year[df_year['sentiment'].notna() & ~df_year['user reviews'].str.match(r'^[1-9]$')]['title']

        # Obtener los títulos más comunes
        top_titles = filtered_titles.value_counts().head(5).index.to_dict()

        return top_titles
    else:
        return {'error': "El valor ingresado no es válido."}

#Funcion para ver los titulos con mayor metascore en el año
@app.get('/Metascore/{Year}')
def metascore_by_year(Year: str):
    if Year.isdigit():  
        year_int = int(Year)
        df_year = df[df['year'] == year_int]

        # Filtra el DataFrame para los registros con metascore no nulo
        df_with_metascore = df_year[df_year['metascore'].notnull()]

        if df_with_metascore.empty:
            return {'message': f"No hay valores de metascore para el año {year_int}."}
        else:
            # Ordena el DataFrame por metascore en orden descendente
            df_sorted_by_metascore = df_with_metascore.sort_values(by='metascore', ascending=False)

            # Obtiene los títulos y metascores de los 5 juegos con el metascore más alto
            top_5_juegos = df_sorted_by_metascore.head(5)[['app_name', 'metascore']].to_dict(orient='records')

            return top_5_juegos
    else:
        return {'error': "El valor ingresado no es válido. Ingrese un año válido en formato numérico."}
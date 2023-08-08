from fastapi import FastAPI
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import pickle
# Titulo y Descripcion
app = FastAPI(title='Proyecto Nº 1 Stram Games', description='API de datos y analalizis de juegos')
with open('xgb_model.pkl', 'rb') as model_file:
    xgb_model = pickle.load(model_file)
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
@app.get('/Generos/{Year}')
def genero(Year: str):
    if Year.isdigit():
        df_year = df[df['year'] == Year]
        if not df_year.empty:
            top_generos = df_year['genres'].explode().value_counts().head(5).to_dict()
            return top_generos
        else:
            return {"error": f"No hay datos para el año {Year}."}
    else:
        return {"error": "El valor ingresado no es válido."}



#Funcion para devolver los juegos de determinado año

@app.get('/Title/{Year}')
def juegos(Year: str):
    if Year.isdigit():
        df_year = df[df['year'] == Year]
        if not df_year.empty:
            top_titulos_completos = df_year['app_game'].explode().value_counts().to_dict()
            return top_titulos_completos
        else:
            return {"error": f"No hay datos para el año {Year}."}
    else:
        return {"error": "El valor ingresado no es válido."}



#Funcion que devuelve los 5 specs mas repetidos del año
@app.get('/specs/{Year}')
def specs(Year:str):
    while True:
        if Year.isdigit():  # Verifica si es un número válido
            df_year = df[df['year'] == Year]
            top_spesc=df_year['specs'].explode().value_counts().head(5).to_dict()
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
        top_titles = filtered_titles.value_counts().head(5).to_dict()

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
    
    
#Modelo de Marchine Learning:
@app.get('/predict/{Year}')
def predic(Year:str):
    if Year.isdigit():
        # Aquí debes cargar los datos correspondientes al año desde tu DataFrame
        # y prepararlos para ser usados en el modelo para hacer la predicción.
        # Supongamos que X es tu conjunto de variables predictoras para el año dado.

        # Hacer la predicción de precio usando el modelo
        predicted_price = xgb_model.predict(X)

        # Calcular el RMSE (si tienes los valores reales de precio para ese año)
        # Supongamos que y_real es el vector con los precios reales.
        y_real = ...  # Cargar los valores reales de precio para el año dado
        rmse = mean_squared_error(y_real, predicted_price, squared=False)

        return {"predicted_price": predicted_price, "rmse": rmse}
    else:
        return {"error": "El valor ingresado no es válido."}

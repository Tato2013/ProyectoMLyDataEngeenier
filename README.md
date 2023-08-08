Sistema de Analisis de Juegos

Este proyecto es un sistema de analisis de juegos basado en la fecha y caracterizticas principales como ej: genero ,metascore . Toma la información de los juegos, para identificar sus caracterizticas similares a la que un usuario elige. 

Transformaciones de los datos Los datos utilizados en este proyecto provienen de un archivo json que contiene información de steam. Dataset

    Crear un data frame con las columnas que voy a usar release_date,genres,title,specs,early_access,sentiment,metascore,publisher,title y developer.. El resto se eliminan por no ser pedidas en los ejercicios y no se les encuentro un valor para utilizarlos en ML.

Dataset modificado

Cree un setiment_score para darle una puntuacion a ls sentiment despues hice un one-hot-enconding con genres para que me funionen como variable de tipo bin y poder utilizarlas en un modelo de regresion.

Sistema de precios se utilizo el sistema de xgboost para la prediccion de un precio segun un año determinado.Tambien se creo una columna year para simplicar las fechas de lanzamiento a solo los años de lanzamiento 

Además de la función principal de recomendación de películas, el proyecto también incluye varias funciones adicionales para interactuar con los datos de las películas. Estas funciones permiten:

    Obtener los 5 generos mas comunes durante el año.
    Obtener la cantidad de juegos que salienron en un año.
    Obtener los specs mas comunes en un año determinado.
    Obtener la cantidad de juegos que salieron con early access en un año.
    Obtener los sentiment de los usuarios en el año .
    Obtener los juegos con mejor metascore y cual es su metascore.

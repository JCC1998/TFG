import pandas as pd
from datetime import datetime as dt
import datetime
import numpy as np
import json
#import sys
#import matplotlib.pyplot as plt

#duracion_min = sys.maxsize
#duracion_max = 0
lista_matrices = []
MAX_SECONDS_DAY = 86400

# Cargamos mapa de APs
f = open("mapa_aps.txt", "r")
mapa_aps = json.loads(f.read())
f.close()
mapa_aps = np.array(mapa_aps)

for nfile in range(7):
    df = pd.read_csv("data/data_"+str(nfile)+".csv", names=["DateTime", "MAC", "AP", "API_time"])
    unique_macs = df["MAC"].unique()
    #print(unique_macs[0])
    #print(df[df["MAC"] == unique_macs[0]])  # Obtenemos todas las conexiones de un usuario
    # Calcular el tiempo que pasa en un AP, si sólo hay un caso o si hay más
    df["Duration"] = np.nan
    print("Inicio: "+str(df.isna().sum().sum()))
    for i in range(len(unique_macs)):
        ##conexiones = df[df["MAC"] == unique_macs[i]]
        lista_conexiones = df[df["MAC"] == unique_macs[i]].index
        if len(lista_conexiones) > 1:
            ##lista_time = list(conexiones["DateTime"])
            ##lista_ap = list(conexiones["AP"])
            lista_duracion = []
            ##for idx in range(len(lista_time) - 1):
            for idx in range(len(lista_conexiones) - 1):
                # Transformación string a datetime
                ##first = dt.strptime(lista_time[idx], '%Y-%m-%d %H:%M:%S')
                first = dt.strptime(df.at[lista_conexiones[idx], "DateTime"], '%Y-%m-%d %H:%M:%S')
                ##last = dt.strptime(lista_time[idx+1], '%Y-%m-%d %H:%M:%S')
                last = dt.strptime(df.at[lista_conexiones[idx+1], "DateTime"], '%Y-%m-%d %H:%M:%S')
                duration = last - first
                lista_duracion.append(duration)
                #print(str(duration))
                ##df.loc[(df['AP'] == lista_ap[idx]) & (df['DateTime'] == lista_time[idx]), 'Duration'] = duration.total_seconds()
                df.at[lista_conexiones[idx], "Duration"] = duration.total_seconds()
            # Calculamos la media de las duraciones del usuario
            average_duration = sum(lista_duracion, datetime.timedelta(0)) / len(lista_duracion)
            # Eliminamos los microsegundos/milisegundos
            average_duration = average_duration - datetime.timedelta(microseconds=average_duration.microseconds)
            #print(str(average_duration))
            #df.loc[(df['AP'] == lista_ap[len(lista_ap)-1]) & (df['DateTime'] == lista_time[len(lista_ap)-1]), 'Duration'] = average_duration.total_seconds()
            df.at[lista_conexiones[len(lista_conexiones)-1], "Duration"] = average_duration.total_seconds()
            #print(df[-df["Duration"].isna()])
        #print("------------------")
        if i % 1000 == 0:
            print("Iteracion: "+str(i))
    print("Final: "+str(df.isna().sum().sum()))
    print("Se han terminado todos los usuarios")
    # Valor mínimo y máximo del dataframe en segundos
    #new_min = df["Duration"].min()
    #new_max = df["Duration"].max()
    #print("Min: "+str(new_min)+", Max: "+str(new_max))

    '''
    if new_min < duracion_min:
        duracion_min = new_min
    if new_max > duracion_max:
        duracion_max = new_max
    '''

    # Conseguimos los APs en que su duración es 0
    lista = df[df["Duration"].isna()].index
    #temp_df = df[df["Duration"].isna()]
    #print(str(len(temp_df)))
    #temp_df = temp_df["AP"].unique()
    #print(temp_df)

    # Para cada AP en que la duración sea vacía, le asignamos la media
    print("Inicio: "+str(df.isna().sum().sum()))
    #for iterador in range(len(temp_df)):
        #print(df[df["Duration"].isna() & df["AP"] == temp_df[iterador]])
    #    print(temp_df[iterador]+":"+temp_df[iterador].mean())
    #    df.loc[df["Duration"].isna() & df["AP"] == temp_df[iterador], "Duration"] = df[df["AP"] == temp_df[iterador]].mean()

    for iterador in range(len(lista)):
        # todo: Posible optimizacion? Se calcula la media todas las veces que aparece el AP en el dataframe
        #  y creo que sólo es necesario que se realice una vez. Puede ser que funcione
        #  df.at[lista[iterador], "AP"].mean()? Así se ahorra tener que hacer para cada vez que aparezca el AP y disminuir
        #  el tiempo que tarde en ejecutarse -- Para usar .mean() es necesario tener un dataframe, lo creamos analizando
        #  todos los valores que tienen el mismo AP
        df.at[lista[iterador], "Duration"] = df[df["AP"] == df.at[lista[iterador], "AP"]].mean()
        # todo: df["Columna"].round().astype(int) para eliminar los decimales y redondear -- Se hace posteriormente

    print("Final: "+str(df.isna().sum().sum()))
    lista = df[df["Duration"].isna()].index
    df.drop(lista, inplace=True)
    print("Última pasada: "+str(df.isna().sum().sum()))
    # df.to_csv("data/data_"+0+"_duration.csv")

    # Creamos un dataframe que contiene la suma del tiempo total que pasa el usuario en el mismo AP
    # reset_index() sirve para que no cuente el nombre de la columan como una fila nueva.
    duration_df = df.groupby(["MAC", "AP"]).sum().reset_index()
    # Necesario para los casos en que tienen una conexión muy larga y luego se le añade la media, haciendo que supere el
    # máximo número de segundos que hay en un día.
    duration_df.loc[duration_df["Duration"] > MAX_SECONDS_DAY, "Duration"] = MAX_SECONDS_DAY
    # Para ordenar valores: duration_df.sort_values(by="Duration", ascending=False), asignando a otro df, o usar inplace

    # Hay que volver a calcular las MAC únicas porque algunas se han borrado antes porque no ha habido manera de
    # encontrar un tiempo que puedan estar en ese AP
    unique_macs = duration_df["MAC"].unique()
    for i in range(len(unique_macs)):
        lista_conexiones = duration_df[duration_df["MAC"] == unique_macs[i]].index
        matriz_usuario = np.zeros((len(mapa_aps), len(mapa_aps[0])))
        for iterador in range(len(lista_conexiones)):
            indices = np.argwhere(mapa_aps == duration_df.at[lista_conexiones[iterador], "AP"])
            # Dividimos entre 360 porque establecemos un rango de 6 minutos para convertir el tiempo de las duraciones
            # en segundos entre los rangos [0, 255] para la red neuronal
            valor = round(duration_df.at[lista_conexiones[iterador], "Duration"]/360)
            # Se realiza una suma de 1 para poder distinguir los casos en que las duraciones son menores de 6 minutos
            # con respecto al 0 de los APs en que el usuario no se ha conectado
            matriz_usuario[indices[0][0]][indices[0][1]] = valor + 1
        lista_matrices.append(matriz_usuario)


# test = np.array(lista_matrices)
# print(test.shape)
#imgplot = plt.imshow(lista_matrices[0], cmap="cool")
#plt.show()

np.save("dataset_duration", lista_matrices)
# todo: Guardar la lista de matrices en un archivo y empezar la red neuronal y su entrenamiento, así como el futuro
#  parser que dirá el AP conectado y el tiempo estimado que ha estado el usuario generado.

# Antes de hacer la regla de 3, hay que sumar las duraciones que tengan el mismo AP, después se podrá hacer la regla
# de 3. df.groupby(["MAC","AP"]).sum() funciona, ya que con el head(1000) antes había 30s y ahora hay 142s. Problemas con el nombre de las columnas
# Parece que lo fusiona  en una columna y no en las que se había asignado -- Solucionado con .reset_index() -- Hecho

# Guardar en una lista, df[df["Duration"].isna()] -- Hecho
# df.drop(lista[idx]) o intentar df.drop(lista, inplace = True),
# ya que se pueden borrar varios elementos creando una lista
# -----------------------------------------------------------------------------
# Realizar la media -- Hecho
# Para cada conexión, añadir el tiempo como una nueva columna del dataframe -- Hecho
# Una vez obtenido para cada valor, obtener el valor mínimo y el máximo -- Hecho
# Cargar el mapa de APs - Hecho
# todo: Hacer regla de 3 con los valores del colormap "cool" de matplotlib
#  Rellenar el mapa de APs del usuario
#  Juntarlos en una misma lista
#  Crear JSON que contenga la lista anterior y los valores de mínimo y máximo
#  Guardar en un archivo.


# Crear variables globales de valores mínimos y máximos de duracion, al principio con valores null -- Hecho
# Para cada archivo, comprobar si el valor mínimo es inferior o el valor máximo es superior -- Hecho
# Después realizar la regla de 3
# Guardar los valores mínimo y máximo en un archivo json

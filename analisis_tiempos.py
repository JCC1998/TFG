import pandas as pd
from datetime import datetime as dt
import datetime
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def analizar_duraciones(mapa_aps, sample_days):
    lista_matrices = []
    duraciones = []
    MAX_SECONDS_DAY = 86400

    for nfile in range(sample_days):
        print("Se ha empezado el archivo data_" + str(nfile))
        df = pd.read_csv("data/data_"+str(nfile)+".csv", names=["DateTime", "MAC", "AP", "API_time"])
        unique_macs = df["MAC"].unique()

        df["Duration"] = np.nan
        # print("Inicio: "+str(df.isna().sum().sum()))
        for i in tqdm(range(len(unique_macs))):
            lista_conexiones = df[df["MAC"] == unique_macs[i]].index
            # Calcular el tiempo que pasa en un AP, si sólo hay un caso o si hay más
            if len(lista_conexiones) > 1:
                lista_duracion = []
                for idx in range(len(lista_conexiones) - 1):
                    # Transformación string a datetime
                    first = dt.strptime(df.at[lista_conexiones[idx], "DateTime"], '%Y-%m-%d %H:%M:%S')
                    last = dt.strptime(df.at[lista_conexiones[idx+1], "DateTime"], '%Y-%m-%d %H:%M:%S')
                    duration = last - first
                    lista_duracion.append(duration)
                    df.at[lista_conexiones[idx], "Duration"] = duration.total_seconds()
                # Calculamos la media de las duraciones del usuario
                average_duration = sum(lista_duracion, datetime.timedelta(0)) / len(lista_duracion)
                # Eliminamos los microsegundos/milisegundos
                average_duration = average_duration - datetime.timedelta(microseconds=average_duration.microseconds)
                df.at[lista_conexiones[len(lista_conexiones) - 1], "Duration"] = average_duration.total_seconds()
            # if i % 1000 == 0:
            #    print("Iteracion: "+str(i))
        # print("Final: "+str(df.isna().sum().sum()))
        # print("Se han terminado todos los usuarios")

        # Conseguimos los APs en que su duración es 0
        lista = df[df["Duration"].isna()].index

        # Para cada AP en que la duración sea vacía, le asignamos la media
        # print("Inicio: "+str(df.isna().sum().sum()))

        for iterador in tqdm(range(len(lista))):
            df.at[lista[iterador], "Duration"] = df[df["AP"] == df.at[lista[iterador], "AP"]].mean()

        # print("Final: "+str(df.isna().sum().sum()))
        lista = df[df["Duration"].isna()].index
        df.drop(lista, inplace=True)
        # print("Última pasada: "+str(df.isna().sum().sum()))

        # Creamos un dataframe que contiene la suma del tiempo total que pasa el usuario en el mismo AP
        # reset_index() sirve para que no cuente el nombre de la columan como una fila nueva.
        duration_df = df.groupby(["MAC", "AP"]).sum().reset_index()
        # Necesario para los casos en que tienen una conexión muy larga y luego se le añade la media, haciendo que
        # supere el máximo número de segundos que hay en un día.
        duration_df.loc[duration_df["Duration"] > MAX_SECONDS_DAY, "Duration"] = MAX_SECONDS_DAY
        # Para ordenar valores: duration_df.sort_values(by="Duration", ascending=False),
        # asignando a otro df, o usar inplace

        # Hay que volver a calcular las MAC únicas porque algunas se han borrado antes
        # debido a que no ha habido manera de encontrar un tiempo que puedan estar en ese AP
        unique_macs = duration_df["MAC"].unique()
        for i in range(len(unique_macs)):
            lista_conexiones = duration_df[duration_df["MAC"] == unique_macs[i]].index
            matriz_usuario = np.zeros((len(mapa_aps), len(mapa_aps[0])))
            for iterador in range(len(lista_conexiones)):
                indices = np.argwhere(mapa_aps == duration_df.at[lista_conexiones[iterador], "AP"])
                # Dividimos entre 360 porque establecemos un rango de 6 minutos para convertir
                # el tiempo de las duraciones en segundos entre los rangos [0, 255] para la red neuronal
                valor = round(duration_df.at[lista_conexiones[iterador], "Duration"]/360)
                # Se realiza una suma de 1 para poder distinguir los casos en que las duraciones
                # son menores de 6 minutos con respecto al 0 de los APs en que el usuario no se ha conectado
                matriz_usuario[indices[0][0]][indices[0][1]] = valor + 1
                duraciones.append(valor + 1)
            lista_matrices.append(matriz_usuario)
    np.save("dataset_duration", lista_matrices)
    distribucion_acumulada(duraciones)


def distribucion_acumulada(lista):
    x = np.sort(lista)
    y = np.array(range(len(lista))) / float(len(lista))
    # x_max = len(np.unique(lista))

    fig, ax = plt.subplots()
    ax.set_xlim(0, 260)  # ¿Sustituir 260 por x_max?
    ax.plot(x, y)
    plt.title('Cumulative distribution function')

    ax.set_xlabel('intervals of 6 minutes')
    ax.set_ylabel('$p$')

    plt.show()

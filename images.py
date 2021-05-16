import pandas as pd
import numpy as np
import json
from tqdm import tqdm


def create_dataset(sample_days):

    mapa = create_mapa_aps()
    lst = []

    for i in tqdm(range(sample_days)):
        # print("S'ha començat l'arxiu " + str(i))
        # Hay que usar names y no columns para evitar eliminar el primer elemento
        df = pd.read_csv("data/data_"+str(i)+".csv", names=["date_time", "mac", "ap_name", "api_date"])
        # Importante usar unique() para evitar generar imágenes duplicadas.
        df_mac = pd.DataFrame(df['mac'].unique())
        for idx in range(len(df_mac)):
            img_array = np.zeros((len(mapa), len(mapa[0])))  # Inicialización de la matriz de la ruta
            img_array.fill(255)  # Llenamos los valores con 255, color blanco
            hashed = df['mac'] == df_mac.values[idx][0]
            # Obtención de todos los APs a los que se ha conectado el usuario
            df_ap = pd.DataFrame(df[hashed].ap_name)
            for iterator in range(len(df_ap)):
                # Obtención de los valores del array donde se encuentra el AP
                indices = np.argwhere(mapa == df_ap['ap_name'].values[iterator])
                img_array[indices[0][0]][indices[0][1]] = 0  # Píxel negro indicando el AP de la ruta
            lst.append(img_array)
        # print("S'ha acabat l'arxiu "+str(i))

    np.save("dataset", lst)


def create_mapa_aps():
    aps = pd.DataFrame(open("data/ap.txt", "r"))  # Dataframe de todas las APs
    aps.columns = ["ap"]
    lista = []
    for i in range(len(aps)):
        lista.append(aps["ap"][i].split(sep="-")[1])  # Añadimos a la lista las siglas de los edificios
    lista = np.unique(lista)  # Fusionamos las siglas repetidas

    n_aps = []
    aps["edificio"] = ""
    for idx_edificio in range(len(lista)):
        tam = 0
        for idx_ap in range(len(aps)):
            # Si el AP analizado pertenece al edificio que observamos, aumentamos el tamaño en 1
            if aps["ap"].values[idx_ap].split(sep="-")[1] == lista[idx_edificio]:
                tam = tam + 1
                aps["edificio"].values[idx_ap] = lista[idx_edificio]
        print("El edificio " + lista[idx_edificio] + " tiene " + str(tam) + " APs")
        n_aps.append(tam)  # Lista del número de APs por edificio

    filas = len(lista)
    columnas = max(n_aps)

    mapa = np.zeros((filas, columnas), dtype=object)

    for x in range(filas):
        for y in range(n_aps[x]):
            mapa[x][y] = aps[aps["edificio"] == lista[x]]["ap"].values[y].rstrip('\n')

    file = open("mapa_aps.txt", "w")
    file.write(json.dumps(mapa.tolist()))
    file.close()
    return mapa

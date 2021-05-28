import pandas as pd
import numpy as np
import tqdm
import matplotlib.pyplot as plt


def analizar_taxis(size):
    data = pd.read_csv("data/raw_trajectories.csv")
    min_latitude = data["latitude"].min()
    min_longitude = data["longitude"].min()
    max_latitude = data["latitude"].max()
    max_longitude = data["longitude"].max()

    diff_lat = max_latitude - min_latitude
    diff_lon = max_longitude - min_longitude

    print("Min lat: " + str(min_latitude)+", min lon: " + str(min_longitude) + ", max lat: " +
          str(max_latitude) + ", max alt: " + str(max_longitude))
    print("Diff lat: " + str(diff_lat) + ", Diff lon: " + str(diff_lon))
    print(str(len(data["taxi id"].unique())))

    lst_mapa = []
    id_list = data["taxi id"].unique()

    for i in range(len(id_list)):
        ruta_taxi = data[data["taxi id"] == id_list[i]].index
        mapa = np.zeros((size, size))
        mapa.fill(255)
        for j in range(len(ruta_taxi)):
            lat = data.at[ruta_taxi[j], "latitude"]
            lon = data.at[ruta_taxi[j], "longitude"]
            separacion_v = diff_lat/size
            separacion_h = diff_lon / size
            indices = get_closer_node(lat, lon, min_latitude, min_longitude, separacion_h, separacion_v, size)
            mapa[indices[0]][indices[1]] = 0

        lst_mapa.append(mapa)
    # imgplot = plt.imshow(lst_mapa[50], cmap="gray")
    # plt.show()
    # print(str(lst_mapa[50]))
    # print(str(data[data["taxi id"] == id_list[50]]))
    return lst_mapa


def get_closer_node(lat, lon, min_lat, min_lon, sep_h, sep_v, size):
    row = None  # Hay veces en que no se cumple la condición y vale None. Arreglado añadiendo igual a la condición
    col = None

    for fila in range(size):
        if lat <= min_lat + ((fila + 1) * sep_v):
            row = fila
            break
    for columna in range(size):
        if lon <= min_lon + ((columna + 1) * sep_h):
            col = columna
            break

    return [row, col]

import numpy as np
import json
import matplotlib.pyplot as plt


def parser(resultados):
    datos = np.reshape(resultados, (len(resultados)*len(resultados[0]), 19, 63))

    imagen = datos[317]
    imgplot = plt.imshow(imagen, cmap="cool")
    plt.show()

    f = open("mapa_aps.txt", "r")
    mapa = json.loads(f.read())
    f.close()

    mapa = np.array(mapa)
    # Obtenemos los APs dónde el tiempo es mayor que 0
    lista = mapa[imagen > 0]
    # Eliminamos los valores no válidos
    lista = list(filter('0'.__ne__, lista))
    indices = []
    # Para cada AP que hemos obtenido, conseguimos la fila y columna correspondiente para luego acceder a los tiempos
    for i in range(len(lista)):
        indices.append(np.argwhere(mapa == lista[i]))

    indices = np.array(indices)
    indices = np.reshape(indices, (len(indices), 2))
    # Para cada AP, especificamos el tiempo de la conexión
    tiempo_total = 0
    for iterador in range(len(lista)):
        tiempo = imagen[indices[iterador][0]][indices[iterador][1]]
        tiempo_total = tiempo_total + tiempo
        if tiempo == 1:
            print("El usuario se ha conectado al AP: " + lista[iterador] + " y ha estado menos de: " +
                  str(tiempo * 360) + " segundos")
        else:
            print("El usuario se ha conectado al AP: " + lista[iterador] + " y ha estado entre " +
                  str((tiempo - 1) * 360)+" segundos y " + str(tiempo * 360) + " segundos")

    print(str(tiempo_total * 360))

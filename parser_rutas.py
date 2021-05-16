import json
import numpy as np
import matplotlib.pyplot as plt


def mostrar_resultados(resultados):
    # Transformamos el array al tamaño deseado para trabajar mejor
    results = np.reshape(resultados, (len(resultados) * len(resultados[0]), 19, 63))

    # todo: Hacer que el script sea para todos los resultados que se han generado, no sólo para una única imagen

    # Escogemos imagen aleatoria
    image = results[250]
    imgplot = plt.imshow(image, cmap="gray")
    plt.show()
    filtered_image = image
    filtered_image[filtered_image < 10] = 0  # Asignación píxeles negros
    filtered_image[filtered_image >= 10] = 255  # Asignación píxeles blancos

    # Mostramos la imagen, hay que invertir los valores para que la imagen no se vea
    # la imagen negra y píxeles blancos para indicar los APs
    imgplot = plt.imshow(filtered_image, cmap="gray")
    plt.show()

    # Cargamos mapa de APs
    f = open("mapa_aps.txt", "r")
    mapa_aps = json.loads(f.read())
    f.close()

    mapa = np.array(mapa_aps)
    # Filtramos los APs que se han generado en el mapa de APs
    ruta = mapa[filtered_image == 0]
    # Eliminamos los valores no válidos
    ruta = list(filter('0'.__ne__, ruta))
    print("El usuario ha pasado por los APs:")
    print(ruta)

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


def parser(resultados, dim1, dim2):
    datos = resultados
    datos = np.reshape(datos, (len(datos)*len(datos[0]), dim1, dim2))
    for i in tqdm(range(len(datos))):
        imgplot = plt.imshow(datos[i], cmap="gray")
        plt.show()


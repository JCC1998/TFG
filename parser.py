import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

f = open("results.txt", "r")

results = json.loads(f.read())
f.close()

test = results[300][15]  # Se corresponde a una imagen
test2 = pd.DataFrame(test)
#print(test2)

# Guardamos una imagen aleatoria
test3 = np.array(results[300][15])

# Matriz  de numpy del mismo tamaño que el anterior, llenándolo de 0s
teest3 = np.zeros((len(test3), len(test3[0])))
for x in range(len(test3)):
    for y in range(len(test3[0])):
        # Asignando a la misma posición, el mismo valor
        teest3[x][y] = test3[x][y][0]
print(teest3)
im3 = np.array(teest3)
img3 = Image.fromarray(im3)
imgplot = plt.imshow(img3)
plt.show()

# Creando la imagen que se utilizará para filtrar
test5 = np.zeros((len(test3), len(test3[0])))
counter = 0
# Llenamos todos los píxeles en blanco
test5.fill(255)
for x in range(len(test3)):
    for y in range(len(test3[0])):
        # Si el valor es menor o igual a 5 (Casi negro)
        if test3[x][y][0] <= 20:
            # Asignamos un píxel negro a la posición de la matriz
            test5[x][y] = 0

print(test5)
im2 = np.array(test5)
img2 = Image.fromarray(im2)
imgplot = plt.imshow(img2)
plt.show()


f = open("mapa_aps.txt", "r")
mapa_aps = json.loads(f.read())
f.close()

# Matriz con las APs
mapa = np.array(mapa_aps)
lista = []
print("---------------------------")
for x in range(len(test5)):
    for y in range(len(test5[0])):
        # Si encontramos un píxel negro
        if test5[x][y] == 0:
            # Añadimos a la lista del AP la misma posición de la matriz de APs
            lista.append(mapa[x][y])
# Eliminamos los valores que no existen
lista = list(filter('0'.__ne__, lista))
print(lista)
s = "El usuario ha pasado por los APs: "
for iterator in range(len(lista)):
    s += str(lista[iterator]) + ", "
print(s)
print(len(np.where(test5 > 5)))


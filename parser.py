import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

#f = open("results.txt", "r")

#results = json.loads(f.read())
#f.close()

# Cargamos los datos
results = np.load("results.npy")
# Transformamos el array al tamaño deseado para trabajar mejor
results = np.reshape(results, (len(results)*len(results[0]), 19, 63))

# Escogemos imagen aleatoria
image = results[320]
filtered_image = image
filtered_image[filtered_image < 10] = 0  # Asignación píxeles negros
filtered_image[filtered_image >= 10] = 255 # Asignación píxeles blancos
#print(filtered_image)

#img = Image.fromarray(filtered_image)
#imgplot = plt.imshow(img, cmap="gray_r")
#plt.show()

# Mostramos la imagen, hay que invertir los valores para que la imagen no se vea
# la imagen negra y píxeles blancos para indicar los APs
imgplot = plt.imshow(-filtered_image, cmap="gray")
plt.show()

################### VERSIÓN ANGITUA ####################
# Creación matriz del tamaño de una imagen
#test = np.zeros((len(image), len(image[0])))
# Toda la imagen en blanco
# test.fill(255)
# canvis = 0
# for i in range(len(image)):
#    for j in range(len(image[0])):
#        if image[i][j] < 10:  Si está por vebajo del thershold, se asigna negro
#            canvis += 1  Aumenta el numero de cambios para tenerlo en cuenta
#            test[i][j] = 0
# print("--------------------" + str(canvis))
# print(test)
# img = Image.fromarray(test)
# imgplot = plt.imshow(img)
# plt.show()

# Guardamos una imagen aleatoria
# test3 = np.array(results[300][15])

# Matriz  de numpy del mismo tamaño que el anterior, llenándolo de 0s
#teest3 = np.zeros((len(test3), len(test3[0])))
#for x in range(len(test3)):
#    for y in range(len(test3[0])):
#        # Asignando a la misma posición, el mismo valor
#        teest3[x][y] = test3[x][y][0]
#print(teest3)
#im3 = np.array(teest3)
#img3 = Image.fromarray(im3)
#imgplot = plt.imshow(img3)
#plt.show()

# Creando la imagen que se utilizará para filtrar
#test5 = np.zeros((len(test3), len(test3[0])))
#counter = 0
## Llenamos todos los píxeles en blanco
#test5.fill(255)
#for x in range(len(test3)):
#    for y in range(len(test3[0])):
        # Si el valor es menor o igual a 5 (Casi negro)
#        if test3[x][y][0] <= 20:
            # Asignamos un píxel negro a la posición de la matriz
#            test5[x][y] = 0

#print(test5)
#im2 = np.array(test5)
#img2 = Image.fromarray(im2)
#imgplot = plt.imshow(img2)
#plt.show()

# Cargamos mapa de APs
f = open("mapa_aps.txt", "r")
mapa_aps = json.loads(f.read())
f.close()

# Matriz con las APs
mapa = np.array(mapa_aps)
lista = []
print("---------------------------")
for x in range(len(filtered_image)):
    for y in range(len(filtered_image[0])):
        # Si encontramos un píxel negro
        if filtered_image[x][y] == 0:
            # Añadimos a la lista del AP la misma posición de la matriz de APs
            lista.append(mapa[x][y])
# Eliminamos los valores que no existen
lista = list(filter('0'.__ne__, lista))
print(lista)
s = "El usuario ha pasado por los APs: "
for iterator in range(len(lista)):
    s += str(lista[iterator]) + ", "
print(s)
print(len(lista))


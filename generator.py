import keras
import numpy as np
import matplotlib.pyplot as plt

lst = []


def sample_images(generator, z_dim, tipo_mapa, image_grid_rows=4, image_grid_columns=4):
    global lst
    # Ruido aleatorio del sample
    z = np.random.normal(0, 1, (image_grid_rows * image_grid_columns, z_dim))
    # Genera las imagenes a partir del ruido aleatorio
    gen_imgs = generator.predict(z)
    # Reescala el pixel de la imagen a [0,1]
    gen_imgs = 0.5 * gen_imgs + 0.5
    # Establece la cuadricula de la imagen
    fig, axs = plt.subplots(image_grid_rows, image_grid_columns, figsize=(4, 4), sharey=True, sharex=True)
    cnt = 0
    for i in range(image_grid_rows):
        for j in range(image_grid_columns):
            # Muestra la cuadricula de imagenes
            axs[i, j].imshow(gen_imgs[cnt, :, :, 0], cmap=tipo_mapa)
            axs[i, j].axis('off')
            cnt += 1
    fig.show()
    support_imgs = np.uint8(gen_imgs * 255)
    lst.append(support_imgs)


def generar_imagenes(new_generator, dim1, dim2, tipo_mapa):
    z_dim = 100
    # Mostramos una matriz de 4x4 de las imagenes generadas por la GAN obtenida del archivo

    global lst
    sample_images(new_generator, z_dim, tipo_mapa)
    lst = np.reshape(lst, (len(lst)*len(lst[0]), dim1, dim2))
    for idx in range(len(lst)):
        imgplot = plt.imshow(lst[idx], cmap=tipo_mapa)
        plt.show()

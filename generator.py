import keras
import numpy as np
import matplotlib.pyplot as plt

# Cargamos el modelo de la GAN ya entrenado
new_generator = keras.models.load_model('generador.h5')
z_dim = 100

def sample_images(generator, image_grid_rows=4, image_grid_columns=4):
    # Ruido aleatorio del sample
    z = np.random.normal(0, 1, (image_grid_rows * image_grid_columns, z_dim))
    # Genera las imagenes a partir del ruido aleatorio
    gen_imgs = generator.predict(z)
    # Reescala el pixel de la imagen a [0,1]
    gen_imgs = 0.5*gen_imgs + 0.5
    # Establece la cuadricula de la imagen
    fig, axs = plt.subplots(image_grid_rows, image_grid_columns, figsize=(4, 4), sharey=True, sharex=True)
    cnt = 0
    for i in range(image_grid_rows):
        for j in range(image_grid_columns):
            # Muestra la cuadricula de imagenes
            axs[i, j].imshow(gen_imgs[cnt, :, :, 0], cmap='gray')
            axs[i, j].axis('off')
            cnt += 1
    fig.show()

# Mostramos una matriz de 4x4 de las imagenes generadas por la GAN obtenida del archivo
sample_images(new_generator)

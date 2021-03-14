import tensorflow as tf
from tensorflow.python.client import device_lib
from keras.models import Sequential
from keras.layers import Dense, Flatten, Reshape
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
import json
from PIL import Image
from datetime import datetime

tf.config.list_physical_devices('GPU')

print(device_lib.list_local_devices())

# Especificamos las dimensiones de las imágenes
img_rows = 19
img_cols = 63
channels = 1  # Este dato es para el rgb, en el caso de blanco y negro se podría eliminar para evitar problemas.

# Dimensiones de las imagenes de entrada
img_shape = (img_rows, img_cols, channels)
# Tamaño del vector de ruido, utilizado como input para el Generador
z_dim = 100

# Implementación del Generador


def build_generator(img_shape, z_dim):
    model = Sequential()
    # Capa totalmente conectada
    model.add(Dense(128, input_dim=z_dim))
    # Activación de Leaky ReLU
    model.add(LeakyReLU(alpha=0.01))
    # Capa de salida con la activación
    model.add(Dense(img_rows*img_cols*1, activation='tanh'))
    # Cambia el tamaño de la salida del Generador a las dimensiones de la imagen
    model.add(Reshape(img_shape))
    return model

# Implementación del Discriminador


def build_discriminator(img_shape):
    model = Sequential()
    # Aplana la entrada de la imagen
    model.add(Flatten(input_shape=img_shape))
    # Capas totalmente conectadas
    model.add(Dense(128))
    # Activación de Leaky ReLU
    model.add(LeakyReLU(alpha=0.01))
    # Capa de salida con activación sigmoidal
    model.add(Dense(1, activation='sigmoid'))
    return model


def build_gan(generator, discriminator):
    model = Sequential()
    model.add(generator)
    model.add(discriminator)
    return model


discriminator = build_discriminator(img_shape)
discriminator.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])
generator = build_generator(img_shape, z_dim)
discriminator.trainable = False
gan = build_gan(generator, discriminator)
gan.compile(loss='binary_crossentropy', optimizer=Adam())

# Entrenamiento

losses = []
accuracies = []
iteration_checkpoints = []

#f = open("dataset.npy", "r")
#dataset = json.loads(f.read())


def train(iterations, batch_size, sample_interval):
    print("Se ha empezado a entrenar la red neuronal")
    # Cargamos el MNIST dataset
    # (X_train, _), (_, _) = dataset
    X_train = np.load("dataset.npy")
    # Reescalamos la escala de grises a valores [1,-1]
    X_train = X_train / 127.5-1.0
    X_train = np.expand_dims(X_train, axis=3)
    # Etiquetas para las imagenes reales (1)
    real = np.ones((batch_size,1))
    # Etiquetas para las imagenes falsas (0)
    fake = np.zeros((batch_size, 1))

    for iteration in range(iterations):
        # Escogemos un batch aleatorio
        idx = np.random.randint(0,X_train.shape[0], batch_size)
        imgs = X_train[idx]
        # Generamos el batch de las imagenes falsas
        z = np.random.normal(0, 1, (batch_size, 100))
        gen_imgs = generator.predict(z)
        # Entrenamos el discriminador
        d_loss_real = discriminator.train_on_batch(imgs, real)
        d_loss_fake = discriminator.train_on_batch(gen_imgs, fake)
        d_loss, accuracy = 0.5*np.add(d_loss_real, d_loss_fake)
        # Generamos el batch de las imagenes falsas
        z = np.random.normal(0, 1, (batch_size, 100))
        gen_imgs = generator.predict(z)
        # Entrenamos el generador
        g_loss = gan.train_on_batch(z, real)

        if (iteration+1) % sample_interval == 0:
            # Guardamos las perdidas y aciertos para despues del entrenamiento
            losses.append((d_loss, g_loss))
            accuracies.append((100.0*accuracy))
            iteration_checkpoints.append(iteration + 1)
            # Salida del progreso de entrenamiento
            print("%d [D loss: %f, acc.: %2f%%] [G loss: %f]" % (iteration + 1, d_loss, 100.0*accuracy, g_loss))
            # Salida de las imagenes generadas
            sample_images(generator)

# Mostrar las imagenes generadas


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
            #axs[i, j].savefig("results/resultado_"+str(cnt)+"_"+str(datetime.now()))
            #im = Image.fromarray((gen_imgs*255).astype(np.uint8))
            #print(gen_imgs.shape)
            #im = np.squeeze(gen_imgs, axis=2)
            #new_im = Image.fromarray(im)
            #new_im.save("results/resultado_"+str(cnt)+"_"+str(datetime.now())+".jpg")

            # Normalizamos los valores porque son decimales
            #--------------support_imgs = np.uint8(gen_imgs[i][j] * 255)
            # Añadimos a la lista la imagen que ha generado, usando el método para pasarlo a string
            # lst.append(support_imgs.tolist())
            #---------------lst.append(support_imgs)
    fig.show()
    print(gen_imgs.shape)
    support_imgs = np.uint8(gen_imgs * 255)
    lst.append(support_imgs)


# Ejecutamos el modelo
# Establecemos los parametros
iterations = 40000
batch_size = 128
sample_interval = 1000
# Entrenamos la red neuronal
lst = []
train(iterations, batch_size, sample_interval)
#f = open("results.txt", "w")
#f.write(json.dumps(lst))
#f.close()

np.save("results", lst)

# Guardamos el generador en un archivo
generator.save('generador.h5')

import os
import files
import images
import neural_net
import numpy as np
import json
import parser_rutas
import generator
import analisis_tiempos
import keras
import parser_duration
import taxis
import parser_taxis
import glob
import informacio_entrenament
import random
import matplotlib.pyplot as plt


def cargar_mapa():
    f = open("mapa_aps.txt", "r")
    mapa_aps = json.loads(f.read())
    f.close()
    return np.array(mapa_aps)


if __name__ == '__main__':
    opcio = "Duracion"
    if opcio == "Rutas":
        print("Realizando análisis de las rutas")
        # Scripts del análisis de la UIB

        # Comprobación de si existen los archivos con los datos, en caso contrario, ejecutar script
        # IMPORTANTE!!!! Es necesario tener el xampp activado para poder acceder a la base de datos
        sample_days = 7
        if not (len(os.listdir("data/")) > 2):
            print("Obteniendo los datos de la BD")
            year = 2020
            month = 11
            day = 9
            files.create_data_files(year, month, day, sample_days)
        # Si no existe el archivo que contiene el dataset, hay que crearlo
        if not os.path.exists("dataset.npy"):
            print("Creando el dataset")
            images.create_dataset(sample_days)

        # Cargamos mapa de APs
        if not os.path.exists("mapa_aps.txt"):
            mapa = images.create_mapa_aps()
        else:
            mapa = cargar_mapa()

        ruta_aprendizaje = "learning/"
        if not os.path.exists("generador.h5"):
            dataset = np.load("dataset.npy")
            iteraciones = 30000
            ruta_generador = "generador"
            archivo_resultados = "results"

            for CleanUp in glob.glob(ruta_aprendizaje+"*.*"):
                # print(CleanUp)
                if not CleanUp.endswith('.gitignore'):
                    os.remove(CleanUp)

            neural_net.execute_neural_net(dataset, len(mapa), len(mapa[0]), iteraciones, ruta_aprendizaje,
                                          ruta_generador, archivo_resultados, tipo_mapa="gray")

        resultados = np.load("results.npy")
        parser_rutas.mostrar_resultados(resultados, len(mapa), len(mapa[0]))

        generador = keras.models.load_model('generador.h5', compile=False)
        generator.generar_imagenes(generador, len(mapa), len(mapa[0]), tipo_mapa="gray")

        informacio_entrenament.informacio_entrenament(ruta_aprendizaje)
        # Ejecutar files.py si no existen los datos. Necsario tener el xampp activado
        # Ejecutar imagenes.py para conseguir el dataset para la red neuronal
        # Ejecutar neural_net.py
        # Guardar el generator.py
        # Ejecutar parser_rutas.py

    elif opcio == "Duracion":
        print("Realizando análisis de las duraciones")
        # Comprobación de si existen los archivos con los datos, en caso contrario, ejecutar script
        # IMPORTANTE!!!! Es necesario tener el xampp activado para poder acceder a la base de datos
        sample_days = 7
        if not (len(os.listdir("data/")) > 2):
            print("Obteniendo los datos de la BD")
            year = 2020
            month = 11
            day = 9
            files.create_data_files(year, month, day, sample_days)

        if not os.path.exists("mapa_aps.txt"):
            mapa = images.create_mapa_aps()
        else:
            mapa = cargar_mapa()

        if not os.path.exists("dataset_duration.npy"):
            analisis_tiempos.analizar_duraciones(mapa, sample_days)

        ruta_aprendizaje = "learning_duration/"
        if not os.path.exists("generador_duration.h5"):
            dataset = np.load("dataset_duration.npy")
            iteraciones = 30000
            ruta_generador = "generador_duration"
            archivo_resultados = "results_duration"

            for CleanUp in glob.glob(ruta_aprendizaje+"*.*"):
                # print(CleanUp)
                if not CleanUp.endswith('.gitignore'):
                    os.remove(CleanUp)

            neural_net.execute_neural_net(dataset, len(mapa), len(mapa[0]), iteraciones, ruta_aprendizaje,
                                          ruta_generador, archivo_resultados, tipo_mapa="cool")

        generador = keras.models.load_model('generador_duration.h5', compile=False)
        generator.generar_imagenes(generador, len(mapa), len(mapa[0]), tipo_mapa="cool")

        resultados = np.load("results_duration.npy")
        parser_duration.parser(resultados, len(mapa), len(mapa[0]))

        informacio_entrenament.informacio_entrenament(ruta_aprendizaje)
        # Ejecutar análisis_tiempos.py
        # Ejecutar neural_net_duration.py
        # Guardar el generator_duration.py
        # Ejecutar parser_duration.py

    elif opcio == "Taxis":
        print("Realizando análisis de las rutas de taxis")
        size = 32
        ruta_aprendizaje = "learning_taxis/"
        if not os.path.exists("generador_taxis.h5"):
            data = taxis.analizar_taxis(size)
            dataset = np.array(data)
            iteraciones = 30000
            ruta_generador = "generador_taxis"
            archivo_resultados = "results_taxis"

            for CleanUp in glob.glob(ruta_aprendizaje+"*.*"):
                # print(CleanUp)
                if not CleanUp.endswith('.gitignore'):
                    os.remove(CleanUp)

            neural_net.execute_neural_net(dataset, len(dataset[0]), len(dataset[0][0]), iteraciones, ruta_aprendizaje,
                                          ruta_generador, archivo_resultados, tipo_mapa="gray")

        generador = keras.models.load_model("generador_taxis.h5", compile=False)
        generator.generar_imagenes(generador, size, size, tipo_mapa="gray")

        #resultados = np.load("results_taxis.npy")
        #parser_taxis.parser(resultados, size, size)
        informacio_entrenament.informacio_entrenament(ruta_aprendizaje)
        # Scripts de los taxis.
        # Análisis del dataset
        # Normalización de las coordenadas
        # Uso de la red neuronal
        # Parser de los resultados obtenidos
    elif opcio == "Experiment":
        dim = 28
        datos = []
        for i in range(50):
            a = np.zeros((dim, dim), int)
            a.fill(255)
            choice = random.randint(0, 1)
            if choice == 0:
                np.fill_diagonal(a, random.randint(0, 10))
            else:
                np.fill_diagonal(np.flipud(a), random.randint(0, 10))
            datos.append(a)
        datos = np.array(datos)
        print(datos[0])
        plt.imshow(datos[0], cmap="gray")
        plt.show()

        if not os.path.exists("generador_experiment.h5"):
            ruta = "experiment/"
            ruta_g = "generador_experiment"
            arch_result = "resultados_experiment"
            neural_net.execute_neural_net(datos, dim, dim, 10000, ruta, ruta_g, arch_result, tipo_mapa="gray")

        generador = keras.models.load_model("generador_experiment.h5")
        generator.generar_imagenes(generador, dim, dim, tipo_mapa="gray")

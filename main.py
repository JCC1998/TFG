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


def cargar_mapa():
    f = open("mapa_aps.txt", "r")
    mapa_aps = json.loads(f.read())
    f.close()
    return np.array(mapa_aps)


if __name__ == '__main__':
    opcion = "Duracion"
    if opcion == "Rutas":
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

        if not os.path.exists("generador.h5"):
            dataset = np.load("dataset.npy")
            iteraciones = 20000
            ruta_aprendizaje = "learning/"
            ruta_generador = "generador"
            archivo_resultados = "results"
            neural_net.execute_neural_net(dataset, len(mapa), len(mapa[0]), iteraciones, ruta_aprendizaje,
                                          ruta_generador, archivo_resultados, tipo_mapa="gray")

        resultados = np.load("results.npy")
        parser_rutas.mostrar_resultados(resultados)

        generador = keras.models.load_model('generador.h5')
        generator.generar_imagenes(generador, tipo_mapa="gray")
        # Ejecutar files.py si no existen los datos. Necsario tener el xampp activado
        # Ejecutar imagenes.py para conseguir el dataset para la red neuronal
        # Ejecutar neural_net.py
        # Guardar el generator.py
        # Ejecutar parser_rutas.py

    elif opcion == "Duracion":
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

        if not os.path.exists("generador_duration.h5"):
            analisis_tiempos.analizar_duraciones(mapa, sample_days)
            dataset = np.load("dataset_duration.npy")
            iteraciones = 20000
            ruta_aprendizaje = "learning_duration/"
            ruta_generador = "generador_duration"
            archivo_resultados = "results_duration"
            neural_net.execute_neural_net(dataset, len(mapa), len(mapa[0]), iteraciones, ruta_aprendizaje,
                                          ruta_generador, archivo_resultados, tipo_mapa="cool")

        generador = keras.models.load_model('generador_duration.h5')
        generator.generar_imagenes(generador, tipo_mapa="cool")

        resultados = np.load("results_duration.npy")
        parser_duration.parser(resultados)
        # Ejecutar análisis_tiempos.py
        # Ejecutar neural_net_duration.py
        # Guardar el generator_duration.py
        # Ejecutar parser_duration.py

    elif opcion == "Taxis":
        print("En proceso")
        # Scripts de los taxis.
        # Análisis del dataset
        # Normalización de las coordenadas
        # Uso de la red neuronal
        # Parser de los resultados obtenidos

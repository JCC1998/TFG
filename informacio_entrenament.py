import json
import matplotlib.pyplot as plt


def informacio_entrenament(folder):
    lista_d = []
    lista_a = []
    lista_g = []
    iteration = []
    path = folder + "info.json"
    file = json.load(open(path))
    for item in file['INFORMACION']:
        lista_d.append(item['Discriminator_loss'])
        lista_a.append(item['Accuracy'])
        lista_g.append(item['Generator_loss'])
        iteration.append(item['Iteration'] / 1000)

    grafica_discriminador(lista_d, iteration)
    grafica_accuracy(lista_a, iteration)
    grafica_generador(lista_g, iteration)


def grafica_discriminador(lista_d, iteration):
    fig, axis = plt.subplots()
    axis.plot(iteration, lista_d)
    plt.title('Discriminator loss while learning')

    axis.set_xlabel('Iteration (in thousands)')
    axis.set_ylabel('Loss')

    plt.show()


def grafica_accuracy(lista_a, iteration):
    fig, axis = plt.subplots()
    axis.plot(iteration, lista_a)
    plt.title('Accuracy rate while learning')

    axis.set_xlabel('Iteration (in thousands)')
    axis.set_ylabel('Accuracy')

    plt.show()


def grafica_generador(lista_g, iteration):
    fig, axis = plt.subplots()
    axis.plot(iteration, lista_g)
    plt.title('Generator loss while learning')

    axis.set_xlabel('Iteration (in thousands)')
    axis.set_ylabel('Loss')

    plt.show()

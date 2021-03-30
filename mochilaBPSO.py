import random
import os
import math
# import msvcrt

# Prints all the articles that can be inside the backpack
def printArticles(xArr, arr):
    total = 0
    for idx, value in enumerate(xArr):
        if value != 0: 
            total += value * arr[idx]['profit']
            print('\t{} veces el artículo {}'.format(value, idx+1))

    print('\nTotal ganado: ${}\n'.format(str(total)))
    return

# This is the Alorithm
# Returns the divided values by some criteria defined by voraSelection function
def getPartArr(xArr, arr):
    add = 0
    weight = int(input('\nIngrese peso máximo de la mochila (kg): '))
    while add < weight: 
        # Call the voraSelection function to select an id
        i = voraSelection(xArr, arr) 
        # If the sum of articles is still supported by the maximum weight of the backpack   
        if add + arr[i]['weight'] <= weight:
            xArr[i] = 1
            add = add + arr[i]['weight']
        # When articles need to be divided to be carried in the backpack
        else: 
            xArr[i] = (weight - add) / arr[i]['weight']
            add = weight
    return xArr

# Returns the values entered by the user
def enteries():
    valid = 'y'
    # Empty list
    arr = []
    # Cycle that stops until the user decides to stop entering data of the articles to be evaluated in the algorithm
    print('\nIngrese los datos de los artículos...')
    while True:
        profit  = int(input('\tIngrese costo: $'))
        weight = int(input('\tIngrese peso (kg): '))
        arr.append({'weight': weight, 'profit': profit})

        valid = input('Costo agregado, ¿Desea agregar otro? (y/n)')

        while valid != 'y' and valid != 'n' :
            valid = input('Entrada incorrecta, ¿Desea agregar otro? (y/n) ')
        if valid == 'n': break
    # Returns the list with the new articles data
    return arr

# Fill an array of 0 based on the length of another array.
def makeEmptyArr(arr):
    newArr = []
    for item in arr: newArr.append(0)
    return newArr

# Returns the index of the item which has the biggest relation between profit and weight
def voraSelection (xArr, arr):
    maxPer = 0
    sel = 0

    for idx, item in enumerate(arr):
        if xArr[idx] != 0 : continue
        per = item['profit'] / item['weight']
        if per > maxPer :
            sel = idx
            maxPer = per
    
    return sel
    
# Genera una matriz cuadrada (según el orden) con valores binarios
# aleatorios.
def matBinAleat(orden):
    matriz = [[0 for x in range(orden)] for y in range(orden)]
    for i in range (0, orden):
        for j in range (0, orden):
            matriz[i][j] = random.randint(0, 1)
    return matriz

# Genera una matriz cuadrada (según el orden) con valores reales en un
# rango de [-4, 4]
def matRealAleat(orden):
    matriz = [[0 for x in range(orden)] for y in range(orden)]
    for i in range (0, orden):
        for j in range (0, orden):
            matriz[i][j] = round(random.uniform(-4, 4), 2)
    return matriz


# Obtiene la imagen de la función sigmoide evaluada en un punto 
# específico
def sigmodie(vid):
    return 1 / 1 + math.exp(-vid)

# Sumatoria del producto de la ganancia de cada item del mapa arr por el elemento 
# correspondiente a la partícula de X o P
#       prtc es la partícula  de X o P
def fitness(arr, prtc):
    suma = 0
    for idx, selec in enumerate(prtc): # selec es un número binario de la partícula
        suma += selec * arr[idx]['profit']
    #     print (''' 
    #         Selec: {}
    #         Profit: {}
    #         Yes? {}
    #     '''.format(selec, arr[idx]['profit'], 'yes' if selec == 1 else 'no'))
    # print('Suma: {}'.format(suma))
    return suma


if __name__ == "__main__":
    
    # os.system('cls');
    # print('Funcionamiento\n  Obtiene el mayor coste dentro de una mochila dada una capacidad máxima.\n')
    # print('Selección\n  La selección de los artículos está definida por la mejor relación del precio respecto al peso.\n')
    # print('Datos por defecto:')
    # # Default data, stored by a list

    # DATASET: P01 is a set of 10 weights and profits for a knapsack
    # of capacity 165.
    # 1 1 1 1 0 1 0 0 0 0 optimal selection of weights   
    arr = [
        {'profit': 92, 'weight': 23},   # 1
        {'profit': 57, 'weight': 31},   # 1
        {'profit': 49, 'weight': 29},   # 1
        {'profit': 68, 'weight': 44},   # 1
        {'profit': 60, 'weight': 53},   # 0
        {'profit': 43, 'weight': 38},   # 1
        {'profit': 67, 'weight': 63},   # 0
        {'profit': 84, 'weight': 85},   # 0
        {'profit': 87, 'weight': 89},   # 0
        {'profit': 72, 'weight': 82}    # 0
    ]

    # Peso de inercia
    w = 0.721
    # Componentes cognitivo y social
    c1 = 2
    c2 = 2
    # Inicialización de las matrices
    xArr = matBinAleat(len(arr))
    pArr = xArr
    vArr = matRealAleat(len(arr))

    #Esta parte hay que agregarla a una función para poder retornar pArr[g] y fitness(pArr[g])
    # Además, los comentarios de 'Repite' y 'Hasta que se alcance la condición de paro' están porque no implementé dicha condición (hay que hacerlo (debe ser una clase de ciclo o asi, creo))

    # Repite
    
    # Recorre todas las partículas en arr y extrae el índice i
    for i, prtc in enumerate(arr):
        # Comparación de fitness en las dimensiones de X y P
        if fitness(arr, xArr[i]) > fitness(arr, pArr[i]):
            # Si el fitness en x es mayor que en p, cambia los elementos de X a P
            for d, elem in enumerate(xArr):
                pArr[i][d] = xArr[i][d]
        
        g = i # Almacena en g, el índice actual i
        # Para cada partícula
        for j, elem in enumerate(arr):
            # Si el fitnes de Pj es mejor que el de Pg, almacena en g, el índice j
            if fitness(arr, pArr[j]) > fitness(arr, pArr[g]):
                g = j
        # Números aleatoriamente distribuidos entre 0 y 1 y redondeados a dos decimales
        r1 = round(random.uniform(0, 1), 2)
        r2 = round(random.uniform(0, 1), 2)
        # Para cada dimensión (creo que las dimensiones son los elementos de cada partícula, alch no me acuerdo)
        for d, elem in enumerate(xArr):
            vArr[i][d] = w * vArr[i][d] + c1 * r1 * (pArr[i][d] - xArr[i][d]) + c2 * r2 * (pArr[g][d] - xArr[i][d])
            # Aquí no puse lo de Vid E (-Vmax, +Vmax)
            # Cambiar Xid a 1 si sigmoide de Vid es mayor; si el random es mayor, Xid será 0
            if random.int(0, 1) < sigmodie(vArr[i][d]): 
                xArr[i][d] = 1 
            else: 
                xArr[i][d] = 0

    # Hasta que se alcance la condición de paro

    


    # for idx, art in enumerate(arr):
    #     print('\t{}. Costo: ${}; Peso: {} kg'.format(idx + 1, art['profit'], art['weight']))
    # # To enter data manually
    # if input('\n¿Usar datos predeterminados? (y/n) ') != 'y' :
    #     arr  = enteries()
    # # Assign the divided values of the article
    # xArr = getPartArr(makeEmptyArr(arr), arr)

    # print('\nLos artículos que se puede llevar son: ')
    # printArticles(xArr, arr)
    # print("Programa finalizado.\nPresione una tecla para continuar...")
    # msvcrt.getch()
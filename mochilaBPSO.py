import random
import math
    
# Genera una matriz cuadrada (según el orden) con valores binarios
# aleatorios.
def matBinAleat(orden):
    matriz = [[0 for x in range(orden)] for y in range(orden)]
    for i in range (0, orden):
        for j in range (0, orden):
            matriz[i][j] = random.randint(0, 1)
    print(matriz)
    return matriz

# Genera una matriz cuadrada (según el orden) con valores reales en un
# rango de [-4, 4]
def matRealAleat(orden):
    matriz = [[0 for x in range(orden)] for y in range(orden)]
    for i in range (0, orden):
        for j in range (0, orden):
            # Números aleatoriamente distribuidos uniformemente entre -4 y 4 y redondeados a dos decimales
            matriz[i][j] = round(random.uniform(-4, 4), 2)
    print(matriz)
    return matriz


# Obtiene la imagen de la función sigmoide evaluada en un punto específico
def sigmoide(vid):
    return round(1 / (1 + math.exp(-vid)), 2)

# Sumatoria del producto de la ganancia de cada item del mapa arr por el elemento 
# correspondiente a la partícula de X o P
# prtc es la partícula  de X o P
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
    
    # print('Funcionamiento\n  Obtiene la mayor ganancia de artículos para llevar en una mochila dada una capacidad máxima, al evaluar una serie de opciones aleatorias.\n')
    # print('Selección\n  La selección de los artículos está definida por la mejor ganancia obtenida al llevar artículos por completo en la mochila.\n')
    # print('Datos por defecto:')

    # Datos predeterminados cargados en una lista (resultados esperados del BPSO)
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
    print(pArr)
    vArr = matRealAleat(len(arr))

    #Esta parte hay que agregarla a una función para poder retornar pArr[g] y fitness(pArr[g])
    # Además, los comentarios de 'Repite' y 'Hasta que se alcance la condición de paro' están porque no implementé dicha condición (hay que hacerlo (debe ser una clase de ciclo o asi, creo))

    # Repite
    
    # Recorre todas las partículas en arr y extrae el índice i
    for i, prtc in enumerate(arr):
        # Comparación de fitness en las dimensiones de X y P
        xFitAct = fitness(arr, xArr[i]) # Fitness de la partícula actual en matriz x
        pFitAct = fitness(arr, pArr[i]) # Fitness de la partícula actual en matriz p
        if xFitAct > pFitAct:
            # Si el fitness en x es mayor que en p, cambia los elementos de X a P
            for d, elem in enumerate(xArr):
                pArr[i][d] = xArr[i][d] # Actualización de la matriz p

        g = i # Almacena en g, el índice actual i (partícula líder actual)
        # Para cada partícula
        for j, elem in enumerate(arr):
            # Si el fitness de Pj es mejor que el de Pg, almacena en g, el índice j (partícula líder definitiva)
            pActFit = fitness(arr, pArr[j]) # Fitness de la partícula actual en matriz p
            pFitLider = fitness(arr, pArr[g]) # Fitness de la partícula líder marcada en matriz p
            if pActFit > pFitLider:
                g = j
        # Números aleatoriamente distribuidos uniformemente entre 0 y 1 y redondeados a dos decimales
        r1 = round(random.uniform(0, 1), 2)
        r2 = round(random.uniform(0, 1), 2)
        # Para cada dimensión
        for d, elem in enumerate(xArr):
            vArr[i][d] = round(w * vArr[i][d] + c1 * r1 * (pArr[i][d] - xArr[i][d]) + c2 * r2 * (pArr[g][d] - xArr[i][d]), 2)
            # Cambiar Xid a 1 si sigmoide de Vid es mayor; si el random es mayor, Xid será 0
            xRandom = round(random.uniform(0, 1), 2)
            xSigmoide = sigmoide(vArr[i][d])
            if xRandom < xSigmoide: 
                xArr[i][d] = 1 
            else: 
                xArr[i][d] = 0

    # Hasta que se alcance la condición de paro
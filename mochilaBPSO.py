import random
import math
    
# Genera una matriz cuadrada (según el orden) con valores binarios
# aleatorios.
def matBinAleat(orden):
    matriz = [[0 for x in range(orden)] for y in range(orden)]
    for i in range (0, orden):
        for j in range (0, orden):
            matriz[i][j] = random.randint(0, 1)
    # print(matriz)
    return matriz

# Genera una matriz cuadrada (según el orden) con valores reales en un
# rango de [-4, 4]
def matRealAleat(orden):
    matriz = [[0 for x in range(orden)] for y in range(orden)]
    for i in range (0, orden):
        for j in range (0, orden):
            # Números aleatoriamente distribuidos uniformemente entre -4 y 4 y redondeados a dos decimales
            matriz[i][j] = round(random.uniform(-4, 4), 2)
    # print(matriz)
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
        suma += selec * arr[idx]['ganancia']
    #     print (''' 
    #         Selec: {}
    #         Profit: {}
    #         Yes? {}
    #     '''.format(selec, arr[idx]['profit'], 'yes' if selec == 1 else 'no'))
    # print('Suma: {}'.format(suma))
    return suma
# Devuelve la relación de pesos respecto al fitness. Lo mismo que el fitness, pero con pesos
def fitnessPesos(arr, prtc):
    suma = 0
    for idx, selec in enumerate(prtc): # selec es un número binario de la partícula
        # print('{} * {} = {}'.format(selec, arr[idx]['weight'], selec * arr[idx]['weight']))
        suma += selec * arr[idx]['peso']
    # print('SUM: {}'.format(suma))
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
        {'ganancia': 92, 'peso': 23},   # 1
        {'ganancia': 57, 'peso': 31},   # 1
        {'ganancia': 49, 'peso': 29},   # 1
        {'ganancia': 68, 'peso': 44},   # 1
        {'ganancia': 60, 'peso': 53},   # 0
        {'ganancia': 43, 'peso': 38},   # 1
        {'ganancia': 67, 'peso': 63},   # 0
        {'ganancia': 84, 'peso': 85},   # 0
        {'ganancia': 87, 'peso': 89},   # 0
        {'ganancia': 72, 'peso': 82}    # 0
    ]

    # Capacidad de la mochila
    maxWeight = 165
    # Peso de inercia
    w = 0.721
    # Componentes cognitivo y social
    c1 = 2
    c2 = 2
    # Inicialización de las matrices
    xArr = matBinAleat(len(arr))
    pArr = xArr
    # print(pArr)
    vArr = matRealAleat(len(arr))

    #Esta parte hay que agregarla a una función para poder retornar pArr[g] y fitness(pArr[g])
    # Además, los comentarios de 'Repite' y 'Hasta que se alcance la condición de paro' están porque no implementé dicha condición (hay que hacerlo (debe ser una clase de ciclo o asi, creo))

    fitnessPgMax = 0 # Fitness máximo
    pesosPgMax   = 0 # Peso máximo en relación al fitness
    cntMax       = 0 # Cuenta la cantidad de veces que se ha obtenido un máximo
    
    contador     = 0 # Cantidad de recorridos para cada partícula

    repetir      = True # Bandera de repetición
    
    while repetir:
        contador += 1
        # Recorre todas las partículas en arr y extrae el índice i
        for i, prtc in enumerate(xArr):
            # Comparación de fitness en las dimensiones de X y P
            xFitAct = fitness(arr, xArr[i]) # Fitness de la partícula actual en matriz x
            pFitAct = fitness(arr, pArr[i]) # Fitness de la partícula actual en matriz p
            if xFitAct > pFitAct:
                # Si el fitness en x es mayor que en p, cambia los elementos de X a P
                for d, elem in enumerate(xArr[i]):
                    pArr[i][d] = xArr[i][d] # Actualización de la matriz p

            g = i # Almacena en g, el índice actual i (partícula líder actual)
            # Para cada partícula
            for j, elem in enumerate(pArr):
                # Si el fitness de Pj es mejor que el de Pg, almacena en g, el índice j (partícula líder definitiva)
                pActFit = fitness(arr, pArr[j]) # Fitness de la partícula actual en matriz p
                pFitLider = fitness(arr, pArr[g]) # Fitness de la partícula líder marcada en matriz p
                if pActFit > pFitLider:
                    g = j
            
            # Para cada dimensión
            for d, elem in enumerate(xArr):
                # Números aleatoriamente distribuidos uniformemente entre 0 y 1 y redondeados a dos decimales
                r1 = round(random.uniform(0, 1), 2)
                r2 = round(random.uniform(0, 1), 2)
                # Cálculo de velocidad
                vArr[i][d] = round(w * vArr[i][d] + c1 * r1 * (pArr[i][d] - xArr[i][d]) + c2 * r2 * (pArr[g][d] - xArr[i][d]), 2)
                # Cambiar Xid a 1 si sigmoide de Vid es mayor; si el random es mayor, Xid será 0
                xRandom = round(random.uniform(0, 1), 2)
                xSigmoide = sigmoide(vArr[i][d])
                if xRandom < xSigmoide: 
                    xArr[i][d] = 1 
                else: 
                    xArr[i][d] = 0
            
            #CONDICIÓN DE PARO

            fitnessPg = fitness(arr, pArr[g]) # Almacena el fitness(Pg)
            pesosPg = fitnessPesos(arr, pArr[g]) # Almacena el la relación de peso con  fitness(Pg)
            
            # Obtendrá el fitnes máximo de la iteración, así como el peso y partículas asociadas
            if (fitnessPg >= fitnessPgMax) and (maxWeight >= pesosPg):
                fitnessPgMax = fitnessPg
                maximos = {
                    'ganancia'    : fitnessPg,
                    'peso'        : pesosPg, 
                    'particula'   : pArr[g],
                    'velocidades' : vArr[g],
                    'repeticiones': contador
                }

                cntMax += 1
            if cntMax > len(arr):
                repetir = False

    print('peso: {}'.format(maximos['peso']))
    print('ganancia: {}'.format(maximos['ganancia']))
    print('partícula: {}'.format(maximos['particula']))
    print('repeticiones: {}'.format(maximos['repeticiones']))

    # Hasta que se alcance la condición de paro
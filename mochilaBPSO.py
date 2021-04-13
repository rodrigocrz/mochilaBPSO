import random
import math

#Ingreso de datos por parte del usuario
def enteries():
    valid = 's'
    arr = []
    # Cycle that stops until the user decides to stop entering data of the articles to be evaluated in the algorithm
    print('\nIngrese los datos de los artículos...')
    while True:
        ganancia  = int(input('\tIngrese ganancia: '))
        peso = int(input('\tIngrese peso: '))
        arr.append({'ganancia': ganancia, 'peso': peso})

        valid = input('Elemento agregado, ¿Desea agregar otro? (s/n)')

        while valid != 's' and valid != 'n' :
            valid = input('Entrada incorrecta, ¿Desea agregar otro? (s/n) ')
        if valid == 'n': break
    # Returns the list with the new articles data
    return arr
    
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
            # Números aleatoriamente distribuidos uniformemente entre -4 y 4 y redondeados a dos decimales
            matriz[i][j] = round(random.uniform(-4, 4), 2)
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
    return suma
# Devuelve la relación de pesos respecto al fitness. Lo mismo que el fitness, pero con pesos
def fitnessPesos(arr, prtc):
    suma = 0
    for idx, selec in enumerate(prtc):
        suma += selec * arr[idx]['peso']
    return suma

def imprimeDatos(diccio):
    cadena = ''
    for idx, part in enumerate(diccio): 
        cadena += ' {}. Ganancia: {}; Peso: {}\n'.format(idx + 1, part['ganancia'], part['peso'])
    print(cadena)
        

def imprimeEntre(datos):
    cadena = 'Datos finales: '
    for elem in datos: cadena += str(elem) + ' '
    print(cadena + '\n')
    

    
def BPSO():
    iteraciones = 100000
    # Datos predeterminados cargados en una lista (resultados esperados del BPSO)
    # DATASET: P02 is a set of 5 weights and profits for a knapsack of capacity 26.
    # 0, 1, 1, 1, 0 optimal selection of weights   
    arr = [
        {'ganancia': 24, 'peso': 12},   # 0
        {'ganancia': 13, 'peso':  7},   # 1
        {'ganancia': 23, 'peso': 11},   # 1
        {'ganancia': 15, 'peso':  8},   # 1
        {'ganancia': 16, 'peso':  9}    # 0
    ]
    datosEntre = [0, 1, 1, 1, 0] # Datos de entrenamiento
    
    maxWeight = 26 # Capacidad de la mochila
    print('\n Peso por defecto para estos datos: {}'.format(maxWeight))

    imprimeDatos(arr)
    imprimeEntre(datosEntre)

    # Preguntamos al usuario si desea usar los datos por defecto
    manual = False if input('\n¿Usar datos predeterminados? (s/n) ') == 's' else True
    if  manual:
        arr  = enteries()
        # Capacidad de la mochila
        maxWeight = int(input('\nIngrese peso máximo de la mochila: '))

    # Preguntamos si desea usar los datos de entrenamiento(salida)
    entrenar = bool(True if input('¿Usar datos de salida (entrenamiento)?(s/n) ') == 's' else False)

    if entrenar and manual:
        datosEntre =[]
        for idx, num in enumerate(range(len(arr))):
            selec = int(input('Ingrese dato (0/1) de selección del elemento {}: '.format(idx + 1)))
            datosEntre.append(selec)
    elif not entrenar:
        iteraciones = int(input('Número máximo de iteraciones: '))

    if manual: 
        print('NUEVOS DATOS')
        imprimeDatos(arr)
        imprimeEntre(datosEntre)


    maximos = { 'ganancia': None, 'peso': None, 'particula': None, 'velocidades': None, 'repeticiones': None } # Inicialización del diccionario de máximos
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
    coincidencias= 0 # Cuenta la cantidad de veces que se ha obtenido un máximo
    
    contador     = 0 # Cantidad de recorridos para cada partícula
    
    while True:
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
                fitnessPgMax = fitnessPg #Define el fitness máximo para agregarlo al diccionario 'maximos'
                coincidencias += 1 # Cuenta las veces que selecciona un máximo

                maximos = {
                    'ganancia'    : fitnessPg,
                    'peso'        : pesosPg, 
                    'particula'   : pArr[g],
                    'velocidades' : vArr[g],
                    'repeticiones': contador
                }

                # En caso que el usuario haya aceptado usar datos de entrenamiento
                if entrenar and maximos['particula'] == datosEntre:
                    return maximos
                if coincidencias > len(arr) or iteraciones == contador:
                    maximos['repeticiones'] = contador
                    return maximos

        if iteraciones == contador:
            maximos['repeticiones'] = contador
            return maximos
            
    

    # Hasta que se alcance la condición de paro

if __name__ == "__main__":
    print('PSO Binario (BPSO).\n')
    print('Funcionamiento\n  -> Obtiene el mayor coste dentro de una mochila dada una capacidad máxima.<-\n  -> En base al algoritmo de BPSO<- \n')
    print('Datos por defecto:')
    maximos = BPSO()
    print('peso:         {}'.format(maximos['peso']))
    print('ganancia:     {}'.format(maximos['ganancia']))
    print('partícula:    {}'.format(maximos['particula']))
    print('repeticiones: {}'.format(maximos['repeticiones']))
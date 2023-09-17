import random
import matplotlib.pyplot as plt

# Define el número de juegos a simular
NUM_JUEGOS = 20000
NUM_RONDAS = 10

# Función para calcular la suerte de un jugador en una ronda
def calcular_suerte():
    return random.uniform(1, 3)

# Función para calcular el puntaje de un jugador en una ronda
def calcular_puntaje(genero, diana):
    probabilidad_acierto = 0
    puntaje = 0

    if diana == 'central':
        probabilidad_acierto = 0.3 if genero == 'Mujer' else 0.2
        puntaje = 10
    elif diana == 'intermedia':
        probabilidad_acierto = 0.38 if genero == 'Mujer' else 0.33
        puntaje = 9
    elif diana == 'exterior':
        probabilidad_acierto = 0.27 if genero == 'Mujer' else 0.4
        puntaje = 8
    elif diana == 'error':
        probabilidad_acierto = 0.05 if genero == 'Mujer' else 0.07
        puntaje = 0

    if random.random() < probabilidad_acierto:
        return puntaje
    else:
        return 0

# Función para simular un lanzamiento en una ronda
def simular_lanzamiento(jugador, diana):
    if jugador['resistencia'] < 5:
        return 0  # No puede lanzar si su resistencia es menor a 5
    jugador['resistencia'] -= 5
    return calcular_puntaje(jugador['genero'], diana)

# Función para simular una ronda
def simular_ronda(equipo1, equipo2):
    dianas = ['central', 'intermedia', 'exterior', 'error']

    # Inicializar experiencia de los jugadores en esta ronda
    experiencia_anterior_e1 = [jugador['experiencia'] for jugador in equipo1]
    experiencia_anterior_e2 = [jugador['experiencia'] for jugador in equipo2]

    for diana in dianas:
        lanzamiento_extra = None
        if equipo1[0]['ganadas_consecutivas'] >= 3:
            lanzamiento_extra = random.choice(equipo1)
        elif equipo2[0]['ganadas_consecutivas'] >= 3:
            lanzamiento_extra = random.choice(equipo2)

        for i, jugador in enumerate(equipo1):
            jugador['suerte'] = calcular_suerte()
            if jugador == lanzamiento_extra:
                puntaje_extra = simular_lanzamiento(jugador, diana)
                jugador['puntaje_extra'] += puntaje_extra
            puntaje = simular_lanzamiento(jugador, diana)
            jugador['puntaje'] += puntaje

            # Actualizar experiencia del jugador
            if puntaje > 0:
                jugador['experiencia'] += 1

        for i, jugador in enumerate(equipo2):
            jugador['suerte'] = calcular_suerte()
            if jugador == lanzamiento_extra:
                puntaje_extra = simular_lanzamiento(jugador, diana)
                jugador['puntaje_extra'] += puntaje_extra
            puntaje = simular_lanzamiento(jugador, diana)
            jugador['puntaje'] += puntaje

            # Actualizar experiencia del jugador
            if puntaje > 0:
                jugador['experiencia'] += 1

    # Reiniciar la resistencia de los jugadores al final de la ronda
    for jugador in equipo1 + equipo2:
        jugador['resistencia'] -= random.randint(1, 2)  # Pierden 1 o 2 puntos de resistencia por cansancio

    # Implementa la lógica para determinar al ganador de la ronda individual
    puntajes_e1 = sum(jugador['puntaje'] for jugador in equipo1)
    puntajes_e2 = sum(jugador['puntaje'] for jugador in equipo2)

    if puntajes_e1 > puntajes_e2:
        equipo1[0]['ganadas_consecutivas'] += 1
    elif puntajes_e2 > puntajes_e1:
        equipo2[0]['ganadas_consecutivas'] += 1
    else:
        equipo1[0]['ganadas_consecutivas'] = 0
        equipo2[0]['ganadas_consecutivas'] = 0

# Función para simular un juego completo
def simular_juego():
    equipo1 = generar_equipo()
    equipo2 = generar_equipo()

    for ronda in range(NUM_RONDAS):
        # Verificar que la resistencia de los jugadores sea mayor o igual a 5 antes de la ronda
        for jugador in equipo1 + equipo2:
            if jugador['resistencia'] < 5:
                jugador['resistencia'] = 5

        simular_ronda(equipo1, equipo2)

    # Reiniciar la resistencia de los jugadores al final del juego
    for jugador in equipo1 + equipo2:
        jugador['resistencia'] = random.randint(35 - 10, 35 + 10)

    # Implementa la lógica para determinar al ganador del juego y acumular experiencia
    puntajes_e1 = sum(jugador['puntaje'] + jugador['puntaje_extra'] for jugador in equipo1)
    puntajes_e2 = sum(jugador['puntaje'] + jugador['puntaje_extra'] for jugador in equipo2)

    ganador = None
    if puntajes_e1 > puntajes_e2:
        ganador = "Equipo 1"
    elif puntajes_e2 > puntajes_e1:
        ganador = "Equipo 2"

    if ganador:
        for jugador in equipo1:
            if jugador['experiencia'] == 9:
                jugador['resistencia'] -= 1
        for jugador in equipo2:
            if jugador['experiencia'] == 9:
                jugador['resistencia'] -= 1

    return equipo1, equipo2, puntajes_e1, puntajes_e2, ganador

# Función para generar un equipo con características aleatorias
def generar_equipo():
    equipo = []

    generos_disponibles = ['Hombre', 'Mujer']

    # Asegura al menos un hombre o una mujer en el equipo
    genero1 = random.choice(generos_disponibles)
    generos_disponibles.remove(genero1)
    genero2 = random.choice(generos_disponibles)

    # Genera los primeros jugadores
    jugador1 = {'resistencia': random.randint(35 - 10, 35 + 10), 'experiencia': 0, 'suerte': calcular_suerte(),
                'genero': genero1, 'puntaje': 0, 'ganadas_consecutivas': 0, 'puntaje_extra': 0}
    jugador2 = {'resistencia': random.randint(35 - 10, 35 + 10), 'experiencia': 0, 'suerte': calcular_suerte(),
                'genero': genero2, 'puntaje': 0, 'ganadas_consecutivas': 0, 'puntaje_extra': 0}
    equipo.append(jugador1)
    equipo.append(jugador2)

    # Genera los otros jugadores asegurando máximo 3 hombres o 3 mujeres por equipo
    for _ in range(3):
        genero = random.choice(generos_disponibles)
        jugador = {'resistencia': random.randint(35 - 10, 35 + 10), 'experiencia': 0, 'suerte': calcular_suerte(),
                    'genero': genero, 'puntaje': 0, 'ganadas_consecutivas': 0, 'puntaje_extra': 0}
        equipo.append(jugador)

    return equipo

# Función principal de simulación
def simulacion():
    ganadores_juegos = []
    ganadores_experiencia = []
    puntajes_finales = {'Equipo 1': 0, 'Equipo 2': 0}
    genero_victorias = {'Mujeres': 0, 'Hombres': 0}

    # Lista para registrar los puntajes de cada jugador en cada juego
    puntajes_por_juego = {'Equipo 1': [[] for _ in range(NUM_JUEGOS)], 'Equipo 2': [[] for _ in range(NUM_JUEGOS)]}

    for juego in range(NUM_JUEGOS):
        equipo1, equipo2, puntajes_e1, puntajes_e2, ganador = simular_juego()
        ganadores_juegos.append(ganador)

        # Determinar el jugador con más experiencia en cada juego y registrarlos
        jugadores_mas_experimentados_e1 = [jugador for jugador in equipo1 if
                                            jugador['experiencia'] == max(jugador['experiencia'] for jugador in equipo1)]
        jugadores_mas_experimentados_e2 = [jugador for jugador in equipo2 if
                                            jugador['experiencia'] == max(jugador['experiencia'] for jugador in equipo2)]

        jugador_mas_experimentado_e1 = random.choice(jugadores_mas_experimentados_e1)
        jugador_mas_experimentado_e2 = random.choice(jugadores_mas_experimentados_e2)

        if jugador_mas_experimentado_e1['experiencia'] > jugador_mas_experimentado_e2['experiencia']:
            ganadores_experiencia.append(
                f"Jugador {equipo1.index(jugador_mas_experimentado_e1) + 1} - Equipo 1")
        elif jugador_mas_experimentado_e2['experiencia'] > jugador_mas_experimentado_e1['experiencia']:
            ganadores_experiencia.append(
                f"Jugador {equipo2.index(jugador_mas_experimentado_e2) + 1} - Equipo 2")
        else:
            ganadores_experiencia.append("Empate")  # En caso de empate, registra un empate

        puntajes_finales['Equipo 1'] += puntajes_e1
        puntajes_finales['Equipo 2'] += puntajes_e2

        genero_ganador = "Hombres" if ganador == "Equipo 2" else "Mujeres" if ganador == "Equipo 1" else "Empate"
        if genero_ganador != "Empate":
            genero_victorias[genero_ganador] += 1

        # Registrar los puntajes de cada jugador en este juego
        for i, jugador in enumerate(equipo1):
            puntajes_por_juego['Equipo 1'][juego].append(jugador['puntaje'] + jugador['puntaje_extra'])
        for i, jugador in enumerate(equipo2):
            puntajes_por_juego['Equipo 2'][juego].append(jugador['puntaje'] + jugador['puntaje_extra'])

    # Imprimir resultados finales
    print("Ganadores de juegos:", ganadores_juegos)
    print("Jugador más experimentado por juego:", ganadores_experiencia)
    print("Puntajes finales:", puntajes_finales)
    print("Género con más victorias en cada juego y en total:", genero_victorias)

    # Genera la gráfica de evolución de puntos de los jugadores
    for equipo in ['Equipo 1', 'Equipo 2']:
        for jugador_idx in range(5):
            puntos_jugador = [puntajes_por_juego[equipo][juego][jugador_idx] for juego in range(NUM_JUEGOS) if
                              len(puntajes_por_juego[equipo][juego]) > jugador_idx]
            plt.plot(range(len(puntos_jugador)), puntos_jugador,
                     label=f'Jugador {jugador_idx + 1} - {equipo}')

        plt.xlabel('Juego')
        plt.ylabel('Puntos')
        plt.title(f'Puntos por Jugador en Cada Juego - {equipo}')
        plt.legend()
        plt.show()

        colores = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b', 'g', 'r']

# Llama a la función principal de simulación
simulacion()

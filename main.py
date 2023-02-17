"""
Necesitamos

    Tiempo para completar el juego base (min)
    Tiempo para completar completamente el juego (min)
    Número de expansiones
    Si tiene o no multijugador


    Puntuación del juego
"""
import json


# Funciones auxiliares
def entrada_valida(dato):
    try:
        if (dato['Review_score'] == 0 or
                dato['Stats']['Single-Player']['Main Story']['Average'] == '--' or
                dato['Stats']['Single-Player']['Completionist']['Average'] == '--'):
            return False
    except KeyError:
        return False
    return True


def parsea_hora(str_hora):
    tokens = str_hora.split(' ')
    if len(tokens) == 2:
        return int(tokens[0][:-1]) * 60 + int(tokens[1][:-1])
    elif tokens[0][-1] == 'h':
        return int(tokens[0][:-1]) * 60
    else:
        return int(tokens[0][:-1])




# Cargamos los datos
with open('datos.jsonlines') as f:
    d_entrada = json.load(f)

d_salida = []

for entrada in d_entrada:
    if entrada_valida(entrada) is False:
        continue

    salida = dict()

    # Nombre del juego
    salida['nombre'] = entrada['Name']

    # Tiempo para completar el juego base (min)
    str_aux = entrada['Stats']['Single-Player']['Main Story']['Average']
    salida['t_juego'] = parsea_hora(str_aux)

    # Tiempo para completar completamente el juego (min)
    str_aux = entrada['Stats']['Single-Player']['Completionist']['Average']
    salida['t_juego_completo'] = parsea_hora(str_aux)

    # Número de expansiones
    try:
        salida['n_dlcs'] = len(entrada['Stats']['Additional Content'])
    except KeyError:
        salida['n_dlcs'] = 0

    # Si tiene o no multijugador
    try:
        aux = entrada['Stats']['Multi-Player']
        salida['multijugador'] = 's'
    except KeyError:
        salida['multijugador'] = 'n'

    # Puntuación del juego
    salida['puntuacion'] = 'Muy bueno' if entrada['Review_score'] >= 85 else (
        'Bueno' if entrada['Review_score'] >= 70 else ('Regular' if entrada['Review_score'] >= 50 else 'Malo'))
    d_salida += [salida]

# Guardamos los datos en un fichero csv
with open('datos.csv', 'w') as f:
    f.write('t_juego,t_juego_completo,n_dlcs,multijugador,puntuacion\n')
    for salida in d_salida:
        f.write('{},{},{},{},{}\n'.format(salida['t_juego'],
                                          salida['t_juego_completo'],
                                          salida['n_dlcs'],
                                          salida['multijugador'],
                                          salida['puntuacion']))

    print('Se han procesado {} entradas'.format(len(d_salida)))

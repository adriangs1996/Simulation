"""
Este modulo ofrece facilidades para el calculo de
integrales basandose en el Metodo de Monte Carlo.
Haremos una funcion para calcular una integral
de forma general y compararemos los resultados
con los devueltos por el modulo scipy.integrate.quad
"""

from math import inf
from numpy.random import random


def integral(a, b, func, iters=1000):
    '''
    Calcula la integral f(x) en el intervalo
    [a, b].

    Parameters
    ----------
    a : Limite inferior de la integral

    b : Limite superior de la integral

    func : Objeto que se pueda invocar o funcion de una variable

    Returns
    -------
    r : Numero aproximando el valor de la integral

    Los puntos a y b pueden ser +-inf.
    '''
    if func is None:
        raise Exception("Must provide a valid function.")

    # Definamos los cambios de variables para llevar la integral
    # al rango [0, 1]
    h = None

    if a == 0 and b == 1:
        h = func

    elif a > -inf and b < +inf:
        h = lambda y: func((a + (b - a) * y) * (b - a))

    elif a > -inf and b == +inf:
        h = lambda y: func(1 / y + a - 1) / y**2

    elif a == -inf and b < +inf:
        h = lambda y: func(b + 1 - 1 / y) / y**2

    elif a == -inf and b == +inf:
        return integral(a, 0, func, iters) + integral(0, b, func, iters)

    r = sum(h(random()) for _ in range(iters)) / iters
    return r

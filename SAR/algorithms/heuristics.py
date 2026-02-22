from typing import Any, Tuple
from algorithms import utils
from algorithms.problems import MultiSurvivorProblem
import math


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem):
    """
    The Manhattan distance heuristic.
    """
    if type(state) == tuple and len(state) == 2 and type(state[0]) == int and type(state[1]) == int:
        posicion = state
    else:
        posicion = state[0]

    if hasattr(problem, "goal"):
        xg, yg = problem.goal
        x, y = posicion
        return abs(x - xg) + abs(y - yg)

    if hasattr(problem, "goals"):
        x, y = posicion
        mejor = None
        for xg, yg in problem.goals:
            d = abs(x - xg) + abs(y - yg)
            if mejor is None or d < mejor:
                mejor = d
        return mejor if mejor is not None else 0

    return 0



def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.
    """
    if type(state) == tuple and len(state) == 2 and type(state[0]) == int and type(state[1]) == int:
        posicion = state
    else:
        posicion = state[0]

    if hasattr(problem, "goal"):
        xg, yg = problem.goal
        x, y = posicion
        dx = x - xg
        dy = y - yg
        return math.sqrt(dx * dx + dy * dy)

    if hasattr(problem, "goals"):
        x, y = posicion
        mejor = None
        for xg, yg in problem.goals:
            dx = x - xg
            dy = y - yg
            d = math.sqrt(dx * dx + dy * dy)
            if mejor is None or d < mejor:
                mejor = d
        return mejor if mejor is not None else 0

    return 0


def survivorHeuristic(state: Tuple[Tuple, Any], problem: MultiSurvivorProblem):
    """
    Your heuristic for the MultiSurvivorProblem.

    state: (position, survivors_grid)
    problem: MultiSurvivorProblem instance

    This must be admissible and preferably consistent.

    Hints:
    - Use problem.heuristicInfo to cache expensive computations
    - Go with some simple heuristics first, then build up to more complex ones
    - Consider: distance to nearest survivor + MST of remaining survivors
    - Balance heuristic strength vs. computation time (do experiments!)
    """
    posicion, grilla = state

    if hasattr(grilla, "asList"):
        sobrevivientes = grilla.asList()
    else:
        sobrevivientes = []
        try:
            for i in range(len(grilla)):
                for j in range(len(grilla[0])):
                    if grilla[i][j]:
                        sobrevivientes.append((i, j))
        except Exception:
            sobrevivientes = []

    if len(sobrevivientes) == 0:
        return 0

    x0, y0 = posicion
    mas_cerca = None
    for xs, ys in sobrevivientes:
        d = abs(x0 - xs) + abs(y0 - ys)
        if mas_cerca is None or d < mas_cerca:
            mas_cerca = d
    if mas_cerca is None:
        mas_cerca = 0

    if len(sobrevivientes) == 1:
        return mas_cerca

    lista = sobrevivientes[:]
    visitados = []
    visitados.append(lista[0])

    costo_mst = 0

    while len(visitados) < len(lista):
        mejor_dist = None
        mejor_nodo = None

        for a in visitados:
            xa, ya = a
            for b in lista:
                if b in visitados:
                    continue
                xb, yb = b
                dist = abs(xa - xb) + abs(ya - yb)
                if mejor_dist is None or dist < mejor_dist:
                    mejor_dist = dist
                    mejor_nodo = b

        costo_mst += mejor_dist
        visitados.append(mejor_nodo)

    return mas_cerca + costo_mst

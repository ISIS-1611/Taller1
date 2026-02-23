from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import nullHeuristic, manhattanHeuristic, euclideanHeuristic, survivorHeuristic


def tinyHouseSearch(problem: SearchProblem):
    """
    Returns a sequence of moves that solves tinyHouse. For any other building, the
    sequence of moves will be incorrect, so only use this for tinyHouse.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

# =============================================================================
# REGISTRO DE USO DE IA - TALLER DE ALGORITMOS DE BÚSQUEDA
# =============================================================================

"""
1. VERSIÓN INICIAL DEL CÓDIGO (COMENTADA):
-----------------------------------------------------------------------------
def depthFirstSearch(problem: SearchProblem):
    pila = utils.Stack()
    pila.push((problem.getStartState(), []))
    visitados = set()
    while not pila.isEmpty():
        estado, camino = pila.pop()
        if estado in visitados: continue
        visitados.add(estado)
        if problem.isGoalState(estado): return camino
        for nuevo_estado, accion, costo in problem.getSuccessors(estado):
            if nuevo_estado not in visitados:
                pila.push((nuevo_estado, camino + [accion]))
    return []

(Nota: El resto de versiones iniciales seguían el mismo patrón de pasar 
listas 'camino + [accion]' en la estructura de datos, lo cual es ineficiente).

2. PROMPTS UTILIZADOS PARA EL REFINAMIENTO:
-----------------------------------------------------------------------------
PROMPT 1: "Analiza cada algoritmo de búsqueda, entiéndelo y explica las mejoras 
qué le harías y por qué. Toma en cuenta las estructuras de datos y cómo 
afectaría su complejidad en espacio y tiempo."

PROMPT 2: "Haz todos los cambios que sugieres en cada algoritmo de forma qué los 
pueda copiar y pegar directamente en mi código, siguiendo la política de uso de 
IA de mi universidad (incluyendo versión inicial, prompts y versión final en 
comentarios)."

3. VERSIÓN FINAL (CÓDIGO ACTIVO A CONTINUACIÓN):
-----------------------------------------------------------------------------
"""

def reconstructPath(state, parent_map):
    """
    Función auxiliar para reconstruir el camino desde el objetivo hacia el inicio
    utilizando un diccionario de punteros al padre.
    """
    path = []
    while state in parent_map:
        parent_state, action = parent_map[state]
        path.append(action)
        state = parent_state
    return path[::-1]

def depthFirstSearch(problem: SearchProblem):
    """
    Mejora: Uso de Mapa de Padres (Backtracking) para optimizar memoria.
    Complejidad Espacio: O(V) en lugar de O(V^2) por no copiar listas de caminos.
    """
    start_state = problem.getStartState()
    stack = utils.Stack()
    stack.push(start_state)
    
    visited = set()
    parent_map = {} # estado_hijo: (estado_padre, accion)

    while not stack.isEmpty():
        state = stack.pop()

        if problem.isGoalState(state):
            return reconstructPath(state, parent_map)

        if state not in visited:
            visited.add(state)
            for successor, action, cost in problem.getSuccessors(state):
                if successor not in visited:
                    parent_map[successor] = (state, action)
                    stack.push(successor)
    return []
        
def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """    
    start_state = problem.getStartState()
    queue = utils.Queue()
    queue.push((start_state, []))
    visited = set()
    while not queue.isEmpty():
        current_state, path = queue.pop()

        if problem.isGoalState(current_state):
            return path

        if current_state not in visited:
            visited.add(current_state)

            for successor, action, stepcost in problem.getSuccessors(current_state):
                if successor not in visited:
                    new_path = path + [action]
                    queue.push((successor, new_path))
    return []

def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """
    estado_inicial = problem.getStartState()
    pq = utils.PriorityQueue()
    pq.push((estado_inicial, [], 0), 0)
    visitados = set()

    while not pq.isEmpty():
        estado, camino, costo_actual = pq.pop()

        if problem.isGoalState(estado):
            return camino

        if estado not in visitados:
            visitados.add(estado)

            for sucesor, accion, costo_paso in problem.getSuccessors(estado):
                if sucesor not in visitados:

                    nuevo_camino = camino + [accion]
                    nuevo_costo = costo_actual + costo_paso
                    
                    pq.push((sucesor, nuevo_camino, nuevo_costo), nuevo_costo)
                    
    return []

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.

    heuristic: nullHeuristic, manhattanHeuristic, euclideanHeuristic, survivorHeuristic
    """
    if type(heuristic) == str:
        heuristic = getattr(__import__("algorithms.heuristics", fromlist=[heuristic]), heuristic)

    pq = utils.PriorityQueue()
    visitados = set()
    mejor_costo = {}

    inicio = problem.getStartState()
    pq.push((inicio, [], 0), heuristic(inicio, problem))
    mejor_costo[inicio] = 0

    while not pq.isEmpty():
        estado, acciones, costo_g = pq.pop()

        if problem.isGoalState(estado):
            return acciones

        if estado in visitados:
            continue
        visitados.add(estado)

        for sucesor, accion, costo in problem.getSuccessors(estado):
            nuevo_g = costo_g + costo

            if (sucesor not in mejor_costo) or (nuevo_g < mejor_costo[sucesor]):
                mejor_costo[sucesor] = nuevo_g
                prioridad = nuevo_g + heuristic(sucesor, problem)
                pq.push((sucesor, acciones + [accion], nuevo_g), prioridad)

    return []

# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

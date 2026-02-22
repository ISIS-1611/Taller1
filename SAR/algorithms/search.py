from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import manhattanHeuristic, euclideanHeuristic


def tinyHouseSearch(problem: SearchProblem):
    """
    Returns a sequence of moves that solves tinyHouse. For any other building, the
    sequence of moves will be incorrect, so only use this for tinyHouse.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    estado_inicial = problem.getStartState()
    
    if problem.isGoalState(estado_inicial):
        return []
    
    pila = utils.Stack()
    pila.push((problem.getStartState(), []))
    
    visitados = set()

    while not pila.isEmpty():
        estado, camino = pila.pop()
        
        if estado in visitados:
            continue
        
        visitados.add(estado)
        
        if problem.isGoalState(estado):
            return camino
        # DFS no se preocupa por los costos porque siempre va a profundidad
        for nuevo_estado, accion in problem.getSuccessors(estado):
            if nuevo_estado not in visitados:
                nuevo_camino = camino + [accion]
                pila.push((nuevo_estado, nuevo_camino))
                
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

def aStarSearch(problem: SearchProblem, heuristic=manhattanHeuristic, tipo="manhattan"):
    """
    Search the node that has the lowest combined cost and heuristic first.

    tipo: "manhattan" o "euclidean"
    """
    if tipo == "euclidean":
        heuristica = euclideanHeuristic
    elif tipo == "manhattan":
        heuristica = manhattanHeuristic
    else:
        heuristica = heuristic

    pq = utils.PriorityQueue()
    visitados = set()
    mejor_costo = {}

    inicio = problem.getStartState()
    costo_g = 0
    costo_f = costo_g + heuristica(inicio, problem)

    pq.push((inicio, [], costo_g), costo_f)
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
                nuevo_f = nuevo_g + heuristica(sucesor, problem)
                pq.push((sucesor, acciones + [accion], nuevo_g), nuevo_f)

    return []

# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

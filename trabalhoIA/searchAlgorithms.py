from collections import defaultdict, deque, namedtuple
from queue import Queue, PriorityQueue
import math
import random
import string
import timeit
from graph import Graph
import utils

def irrevocable(graph, start_id, end_id):

    start_node = [node for node in list(graph.graph.keys()) if node.vertex_id == start_id][0]

    # Inicializando flag de sucesso e fracasso
    success = False
    fail = False
    solution = [start_node]
    visited = [start_node]

    while not success or not fail:
        ok = False
        current_node = solution[-1]
        edges = list(graph[current_node].keys())

        while len(edges) > 0:

            # Nesta implementacao a escolha da regra/edge é por ordem alfabética ou crescente (se forem numeros)
            edges.sort()
            chosen_node = edges[0]

            if chosen_node not in visited:
                visited.append(chosen_node)
                if chosen_node not in solution:
                    ok = True
                    break
            else:
                del edges[0]

        if not ok:
            fail = True
            break

        solution.append(chosen_node)
        if chosen_node.vertex_id == end_id:
            success = True
            break

    return [node.vertex_id for node in solution], "SUCCESS" if success else "FAILURE"

def backTracking(graph, start_id, end_id):

    start_node = [node for node in list(graph.graph.keys()) if node.vertex_id == start_id][0]

    # Inicializando flag de sucesso e fracasso
    success = False
    fail = False
    # A solucao sera descoberta manipulando uma "pilha"
    solution = [start_node]
    visited = [start_node]

    while not success or not fail:
        # Verificamos se e possivel aplicar regras no ultimo no na pilha
        current_node = solution[-1]
        edges = list(G[current_node].keys())

        # Se ainda existe pelo menos uma aresta que ainda não foi visitada entramos no if
        if not all(node in visited for node in edges):

            # Nesta implementacao a escolha da regra/edge é por ordem alfabética ou crescente (se forem numeros)
            edges.sort()
            chosen_node = edges[0]
            while chosen_node in visited:
                chosen_node = edges[edges.index(chosen_node) + 1]

            if chosen_node not in visited:
                visited.append(chosen_node)

            if chosen_node not in solution:
                solution.append(chosen_node)
                # Se o proximo no for o no terminal, ativamos a flag de sucesso e terminamos o loop
                if chosen_node.vertex_id == end_id:
                    success = True
                    break
        else:
            # Se voltarmos para o no inicial, significa que nao ha mais nos para serem explorados
            if current_node.vertex_id == start_id:
                fail = True
                break
            else:
                # Senao, voltamos na "arvore" de busca
                solution.pop()

    return [node.vertex_id for node in solution], "SUCCESS" if success else "FAILURE"

def breadth_first_search(graph, start_id, end_id):

    start_node = [node for node in list(graph.graph.keys()) if node.vertex_id == start_id][0]
    end_node = [node for node in list(graph.graph.keys()) if node.vertex_id == end_id][0]

    parentMap = {}
    visited = []
    solution = []
    current = start_node
    queue = deque()
    queue.append(current)
    visited.append(current)
    success = False

    while queue and not success:
        current = queue.popleft()
        if current == end_node:
            success = True
            break
        else:
            for child in graph[current]:
                if child not in visited:
                    queue.append(child)
                    visited.append(child)
                    parentMap[child.vertex_id] = current.vertex_id

    curr_id = current.vertex_id
    if success:
        while curr_id != start_node.vertex_id:
            solution.append(curr_id)
            curr_id = parentMap[curr_id]
        solution.append(curr_id)
        solution.reverse()
        return solution, "success"
    else:
        return solution, "failure"

def depth_first_search(graph, start_id, end_id):

    start_node = [node for node in list(graph.graph.keys()) if node.vertex_id == start_id][0]
    end_node = [node for node in list(graph.graph.keys()) if node.vertex_id == end_id][0]

    parentMap = {}
    visited = []
    stack = []
    solution = []
    current = start_node
    stack.append(current)
    success = False

    while stack:
        current = stack[-1]
        stack.pop()

        if current not in visited:
            visited.append(current)

        if current == end_node:
            success = True
            break

        for child in graph[current]:
            if child not in visited:
                stack.append(child)
                parentMap[child.vertex_id] = current.vertex_id

    curr_id = current.vertex_id
    if success:
        while curr_id != start_node.vertex_id:
            solution.append(curr_id)
            curr_id = parentMap[curr_id]
        solution.append(curr_id)
        solution.reverse()
        return solution, "success"
    else:
        return solution, "failure"

def uniform_cost_search(graph, start_id, end_id):

    start_node = [node for node in list(graph.graph.keys()) if node.vertex_id == start_id][0]
    end_node = [node for node in list(graph.graph.keys()) if node.vertex_id == end_id][0]

    success = False
    fail = False

    solution = []
    visited = []

    prority_queue = PriorityQueue()
    path_to_goal = []
    prority_queue.put((0, start_node, path_to_goal))

    cost = 0

    while not prority_queue.empty():
        top_q = prority_queue.get()
        current_node = top_q[1]
        current_path = top_q[2]

        if current_node.vertex_id == end_id:
            success = True
            solution = current_path
        else:
            if not current_node in visited:
                edges = list(graph[current_node].keys())
                edges.sort(
                    key=lambda edge: cost + graph[current_node][edge].weight
                )
                cost += graph[current_node][edges[0]].weight

                while len(edges) > 0:
                    edge = edges.pop()
                    prority_queue.put(
                        (cost + graph[current_node][edge].weight, edge, current_path + [current_node]))

                visited.append(current_node)

    return [node.vertex_id for node in solution + [end_node]], "SUCCESS" if success else "FAILURE"

def greedy(graph, start_id, end_id):

    start_node = [node for node in list(graph.graph.keys()) if node.vertex_id == start_id][0]
    end_node = [node for node in list(graph.graph.keys()) if node.vertex_id == end_id][0]

    solution = []
    solution.append(start_node.vertex_id)
    current = start_node

    success = False
    fail = False

    while not success:
        children = {}
        for child in graph[current]:
            if child.vertex_id not in solution:
                children[child] = utils.heuristic(child, end_node)

        if children:
            current = utils.find_smaller(children, 'greedy')
            solution.append(current.vertex_id)
            if current == end_node:
                success = True
                return solution, 'success'
        else:
            fail = True
            return solution, 'failure'

def a_star(graph, start_id, end_id):

    start_node = [node for node in list(graph.graph.keys()) if node.vertex_id == start_id][0]
    end_node = [node for node in list(graph.graph.keys()) if node.vertex_id == end_id][0]

    openList = {}
    closedList = {}

    # A lista contém respectivamente: g(custo acumulado), funcao h da heuristica e funcao f(g + h)
    openList[start_node] = [0, utils.heuristic(
        start_node, end_node), 0 + utils.heuristic(start_node, end_node)]

    success = False
    solution = []
    parentMap = {}

    while openList:
        current = utils.find_smaller(openList, 'a_star')
        closedList[current] = openList[current]
        del openList[current]
        if current == end_node:
            success = True
            break
        for child in graph[current]:
            if child in closedList:
                continue
            if child in openList:
                new_g = closedList[current][0] + graph[current][child].weight
                if openList[child][0] > new_g:
                    openList[child][0] = new_g
                    openList[child][2] = new_g + openList[child][1]
                    parentMap[child.vertex_id] = current.vertex_id
            else:
                child_g = closedList[current][0] + graph[current][child].weight
                child_h = utils.heuristic(child, end_node)
                openList[child] = [child_g, child_h, child_g + child_h]
                parentMap[child.vertex_id] = current.vertex_id

    curr_id = current.vertex_id
    if success:
        while curr_id != start_node.vertex_id:
            solution.append(curr_id)
            curr_id = parentMap[curr_id]
        solution.append(curr_id)
        solution.reverse()
        return solution, "success"
    else:
        return solution, "failure"

if __name__ == "__main__":

    G = Graph()

    nodes_list = list(string.ascii_uppercase)
    test_map = utils.map_generator(nodes_list, 0.1)

    vertex = namedtuple("Vertex", ["vertex_id", "vertex_x", "vertex_y"])
    for connection in test_map:
        node1 = vertex(vertex_id=connection[0][0], vertex_x=connection[0][1][0], vertex_y=connection[0][1][1])
        node2 = vertex(vertex_id=connection[1][0], vertex_x=connection[1][1][0], vertex_y=connection[1][1][1])
        weight = connection[2]
        G.add_edge(node1, node2, weight)

    # print(G)

    print(f"Irrevocable: {irrevocable(G, 'B', 'Z')}")
    print(f"Backtracking: {backTracking(G, 'B', 'Z')}")
    print(f"Breadth first search: {breadth_first_search(G, 'B', 'Z')}")
    print(f"Depth first search: {depth_first_search(G, 'B', 'Z')}")
    print(f"Uniform cost search: {irrevocable(G, 'B', 'Z')}")
    print(f"A star: {a_star(G, 'B', 'Z')}")
    print(f"Greedy: {greedy(G, 'B', 'Z')}")


    # Testando o a * em um exercicio executado em aula pelo professor
    # g = Graph()

    # vertex = namedtuple("Vertex", ["vertex_id", "vertex_x", "vertex_y"])
    # a = vertex(vertex_id='A', vertex_x=4, vertex_y=0)
    # b = vertex(vertex_id='B', vertex_x=11, vertex_y=0)
    # c = vertex(vertex_id='C', vertex_x=6, vertex_y=0)
    # d = vertex(vertex_id='D', vertex_x=8, vertex_y=0)
    # e = vertex(vertex_id='E', vertex_x=7, vertex_y=0)

    # g.add_edge(a, b, 4)
    # g.add_edge(a, c, 2)
    # g.add_edge(b, c, 1)
    # g.add_edge(b, d, 3)
    # g.add_edge(c, d, 5)
    # g.add_edge(c, e, 2)
    # g.add_edge(d, e, 1)
    # print(G.graph)
    # print(a_star(g, 'A', 'D'))

"""
Graph_coloring
"""
import sys
import random
import matplotlib.pyplot as plt
import networkx as nx

def read_file(filepath: str) -> list[tuple[list[int], int]]:
    """_summary_

    Args:
        filepath (str): path to file

    Returns:
        list[tuple[list[int], int]]: list with vertex and colors
    >>> read_file(123)
    False
    """ 
    if not isinstance(filepath, str):
        return False
    final = []
    output = []
    with open(filepath, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        f = lines[1]
        for i in f:
            i = i.strip()
            if i.isdigit():
                final.append([[], int(i)])
        for line in lines[2:]:
            number, nimber = map(int, line.strip().split(','))
            final[number - 1][0].append(nimber - 1)
            final[nimber - 1][0].append(number - 1)
        for lst in final:
            output.append((lst[0], lst[1]))
    return output

def create_cnf(
        graph: list[tuple[list[int], int]]) -> list[tuple[int, int]]:
    '''
    Converts a graph to his cnf form

    >>> create_cnf([([1,2],1),([0,3],0),([0,3],2),([1,2],0)])
    [(0, 2), (4, 5), (6, 7), (10, 11), \
(12, 14), (16, 17), (18, 19), (22, 23), \
(13, 13), (15, 15), (20, 20), (21, 21), \
(14, 17), (12, 18), (16, 22), (17, 23), \
(19, 22)]
    '''
    cnf = []
    colors = range(0, 3)

    # Блок Є
    for node, info_node in enumerate(graph):
        pos_colors_for_node = [col for col in colors if col != info_node[1]]
        cnf.append((node * 3 + pos_colors_for_node[0], node * 3 + pos_colors_for_node[1]))

    # Блок НЕ
    for node, info_node in enumerate(graph):
        pos_colors_for_node = [col for col in colors if col != info_node[1]]
        cnf.append((node * 3 + pos_colors_for_node[0] + len(graph) * 3,
                    node * 3 + pos_colors_for_node[1] + len(graph) * 3))

    # Блок заперечення попереднього кольору
    for node, info_node in enumerate(graph):
        pos_colors_for_node = [col for col in colors if col != info_node[1]]
        cnf.append((node * 3 + info_node[1] + len(graph) * 3,
                    node * 3 + info_node[1] + len(graph) * 3))

    # Блок Об'єднання
    for node_ind, node in enumerate(graph):
        for neighbor_ind in node[0]:
            if neighbor_ind <= node_ind:
                continue

            neighbor = graph[neighbor_ind]

            for color in colors:
                if color != node[1] and color != neighbor[1]:
                    cnf.append((
                        node_ind * 3 + color + len(graph) * 3,
                        neighbor_ind * 3 + color + len(graph) * 3
                    ))

    return cnf

def create_implication_graph(cnf: list[tuple[int, int]], vertexes_count: int) -> list[list[int]]:
    """
    This function takes cnf and returns implication graph

    Args:
        cnf (list[tuple[int, int]]): cnf
        vertexes_count (int): number of tuples in cnf

    Returns:
        list[list[int]]: implication graph
        
    >>> create_implication_graph([(1, 2), (2, 3), (3, 1)], 18)
    [[], [], [], [], [], [], [], [], [], [], [2, 3], [1, 3], [2, 1], [], [], [], [], []]
    >>> create_implication_graph([(0, 1), (1, 2), (2, 0), (9, 4)], 12)
    [[], [], [], [4], [], [], [1, 2], [0, 2], [1, 0], [], [9], []]
    """
    lst = []
    for _ in range(vertexes_count):
        lst.append([])

    for tpl in cnf:
        indx = (tpl[0] + (vertexes_count / 2)) % vertexes_count
        indx_2 = (tpl[1] + (vertexes_count / 2)) % vertexes_count
        lst[int(indx)].append(tpl[1])
        lst[int(indx_2)].append(tpl[0])

    return lst

def find_solution(implication_graph: list[list[int]]) -> list[bool] | None:
    '''
    Returns solution for the 2-SAT problem, which is represented in implication graph form
    If there are no such solution, returns None

    Args:
        implication_graph (list[list[int]]): corresponding implication graph to solve problem for

    Returns:
        (list[bool] | None): list of booleans, where each element
        representing value of corresponding vertex in implication graph
        or None if such coloring is impossible

    Examples:
        >>> find_solution([[5], [2], [3], [1], [0], [4]])
        [True, False, False, False, True, True]
        >>> find_solution([[1], [0]]) is None
        True
        >>> find_solution([[], []])
        [True, False]
    '''

    n = len(implication_graph)

    vertexes_counter = 0
    scc_counter = 0
    disc = [-1] * n
    low = [-1] * n
    vertices_stack = []
    in_stack = [False] * n
    scc_result = [-1] * n

    def tarjan_scc(vertex: int):
        nonlocal vertexes_counter
        nonlocal scc_counter

        disc[vertex] = vertexes_counter
        low[vertex] = vertexes_counter
        vertices_stack.append(vertex)
        in_stack[vertex] = True
        vertexes_counter += 1

        for next_vertex in implication_graph[vertex]:
            if disc[next_vertex] == -1:
                tarjan_scc(next_vertex)
                low[vertex] = min(low[vertex], low[next_vertex])
            elif in_stack[next_vertex]:
                low[vertex] = min(low[vertex], disc[next_vertex])

        if low[vertex] == disc[vertex]:
            while vertices_stack:
                elem = vertices_stack[-1]

                scc_result[elem] = scc_counter
                in_stack[elem] = False
                vertices_stack.pop()

                if disc[elem] == disc[vertex]:
                    break

            scc_counter += 1

    for i in range(n):
        if disc[i] == -1:
            tarjan_scc(i)

    result = [None] * n

    for i in range(int(n / 2)):
        if scc_result[i] == scc_result[int(n / 2) + i]:
            return None

        result[i] = scc_result[i] < scc_result[int(n / 2) + i]
        result[int(n / 2) + i] = not result[i]

    return result

def color_graph(cnf_solution: list[bool] | None) -> list[int] | None:
    '''
    Returns graph colors as a list of numbers, one number per vertex,
    each number is from 0 to 2 inclusively.
    If such coloring is impossible, returns None

    Args:
        cnf_solution (list[int] | None): corresponding CNF solution,
        which has 6*N vertexes and counts all necessary conditions for coloring
        or None if solution does not exist

    Returns:
        (list[int] | None): list of graph vertexes colors, each number is from 0 to 2 inclusively
        or None if such coloring is impossible

    Examples:
    >>> color_graph([True, False, False, False, True, True])
    [0]
    >>> color_graph([\
        False, False, True, False, True, False,\
        True, True, False, True, False, True\
    ])
    [2, 1]
    '''

    if cnf_solution is None:
        return None

    coloring = []
    for i in range(0, int(len(cnf_solution) / 2), 3):
        for j in range(0, 3):
            if cnf_solution[i + j]:
                coloring.append(j)
                break

    return coloring

def write_file(graph: list[tuple[list[int], int]],
               colored_graph: list[int], output_file: None|str) -> None:
    '''
    Writes a graph structure with color information to a text file.

    Args:
        graph (list[tuple[list[int], int]]): A list of tuples, each containing 
                                        a list of integers (nodes) and a single integer (color).
        colored_graph (list[int]): A list of integers representing the colors of the graph nodes.
        output_file (str): The path to the output text file where the graph will be written.

    Returns:
        None
    
    '''
    colors = ["red", "green", "blue"]
    colored_graph = [color if isinstance(color, int) else colors.index(color) \
                     for color in colored_graph]

    edges = []
    for index, node in enumerate(graph):
        for edge in node[0]:
            if index > edge:
                edges.append(f"{index},{edge}")

    graph_txt = f"{len(graph)},{len(edges)}\n"
    graph_txt += ",".join(map(str, colored_graph)) + "\n"
    graph_txt += "\n".join(edges)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(graph_txt.strip())
            return False
    else:
        return graph_txt.strip()

def display_graph(graph: list[tuple[list[int], int]],
                  colored_graph: list[int]) -> None:
    '''
    Visualizes a graph where each node has a specific color, with all possible edges between nodes.

    Args:
        graph (list[tuple[list[int], int]]): A list of tuples, 
                            each containing a list of integers (nodes) and a color (integer).
        colored_graph (list[int]): A list of integers representing the colors for each node.

    Returns:
        None: The function does not return any value
    '''
    colors = ["red", "green", "blue"]
    g = nx.Graph()
    oldcolors_labels = {index:colors[node[1]][0] for index, node in enumerate(graph)}

    colored_graph = list(map(lambda c: colors[c], colored_graph))
    g.add_nodes_from([(node, {"color":colored_graph[node]}) \
                     for node in range(len(graph))])

    for index, node in enumerate(graph):
        for edge in node[0]:
            g.add_edge(index, edge)

    pos = nx.spring_layout(g)

    plt.figure(figsize=(8, 6))
    nx.draw(g, pos, with_labels=True, node_color=colored_graph,\
         labels = oldcolors_labels,
         node_size=500, font_size=12, font_weight="bold")
    plt.title("Візуалізація графа з кольоровими вузлами")
    plt.show()

def generate_graph(num_nodes: int, density: int) -> list[tuple[list[int], int]]:
    '''
    Generates a large graph with `num_nodes` nodes, 
                where each node is connected to every other node.

    Args:
        num_nodes (int): The number of nodes in the graph.

    Returns:
        list[tuple[list[int], int]]: 
            A list of tuples, each containing a list of integers (nodes) and a color (integer).
    '''

    graph = [([], random.randint(0, 2)) for _ in range(0, num_nodes)]

    for i in range(0, num_nodes - 1):
        for _ in range(0, density):
            rand_connect = i
            while rand_connect == i or rand_connect in graph[i]:
                rand_connect = random.randint(0, num_nodes - 1)

            graph[i][0].append(rand_connect)
            graph[rand_connect][0].append(i)

    return graph

def create_colored_graph(graph: list[tuple[list[int], int]]):
    '''
    Func to process graph into colored graph
    '''

    sys.setrecursionlimit(max(sys.getrecursionlimit(), len(graph) * 2))

    cnf = create_cnf(graph)

    implication_graph = create_implication_graph(cnf, len(graph) * 6)
    cnf_solution = find_solution(implication_graph)

    colored_graph = color_graph(cnf_solution)

    if colored_graph is None:
        return False, "Solution for this input data - doesn't exists."
    return True, colored_graph

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    graph_ = generate_graph(10, 2)
    # graph_ = read_file("testfile.csv")

    sys.setrecursionlimit(max(sys.getrecursionlimit(), len(graph_) * 2))

    cnf_ = create_cnf(graph_)

    implication_graph_ = create_implication_graph(cnf_, len(graph_) * 6)
    cnf_solution_ = find_solution(implication_graph_)

    colored_graph_ = color_graph(cnf_solution_)

    write_file(graph_, colored_graph_, "output_file.csv")

    if colored_graph_ is None:
        print("Solution doesn't exist")
    else:
        display_graph(graph_, colored_graph_)

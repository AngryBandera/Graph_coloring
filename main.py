"""
Graph_coloring
"""
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


def create_knf(
        graph: list[tuple[list[int], int]]) -> list[tuple[int, int]]:
    '''
    Converts a graph to his knf form

    >>> create_knf([([1,2],1),([0,3],0),([0,3],2),([1,2],0)])
    [(0, 2), (4, 5), (6, 7), (10, 11),\
 (12, 14), (16, 17), (18, 19), (22, 23),\
 (12, 15), (13, 16), (14, 17),\
 (12, 18), (13, 19), (14, 20),\
 (15, 21), (16, 22), (17, 23),\
 (18, 21), (19, 22), (20, 23),\
 (13, 13), (15, 15), (20, 20), (21, 21)]
    '''
    knf = []
    kolors = [0,1,2]
    # Блок Є#
    for node,info_node in enumerate(graph):
        pos_kolors_for_node = [kol for kol in kolors if kol != info_node[1]]
        knf.append((node*3+pos_kolors_for_node[0], node*3+pos_kolors_for_node[1]))
    #Блок НЕ#
    for node,info_node in enumerate(graph):
        pos_kolors_for_node = [kol for kol in kolors if kol != info_node[1]]
        knf.append((node*3+pos_kolors_for_node[0]+len(graph)*3,\
                    node*3+pos_kolors_for_node[1]+len(graph)*3))
    #Блок Об'єднання#
    connection_between_nodes = []
    for node,info_node in enumerate(graph):
        if tuple(sorted([node, info_node[0][0]])) not in connection_between_nodes \
            and tuple(sorted([node, info_node[0][1]])):
            connection_between_nodes+=[tuple(sorted([node,con_node])) for con_node in info_node[0]]
    for connection in connection_between_nodes:
        for kol in kolors:
            knf.append((connection[0]*3+kol+len(graph)*3,(connection[1]*3+kol+len(graph)*3)))
    #Умова змінності кольорів#
    for node,info_node in enumerate(graph):
        knf.append((node*3+info_node[1]+len(graph)*3, node*3+info_node[1]+len(graph)*3))
    return knf


def create_implication_graph(knf: list[tuple[int, int]], vertexes_count: int) -> list[list[int]]:
    """
    This function takes KNF and returns implication graph

    Args:
        knf (list[tuple[int, int]]): knf
        vertexes_count (int): number of tuples in knf

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

    for tpl in knf:
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

                if low[elem] != disc[vertex]:
                    break

                scc_result[elem] = scc_counter
                in_stack[elem] = False
                vertices_stack.pop()

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
        False, False, True, True, True, False,\
        False, True, False, True, False, True\
    ])
    [2, 1]
    '''

    if cnf_solution is None:
        return None

    coloring = []
    for i in range(0, len(cnf_solution), 6):
        for j in range(0, 3):
            if cnf_solution[i + j]:
                coloring.append(j)
                break

    return coloring


def write_file(graph: list[tuple[list[int], int]],
               colored_graph: list[int], output_file: str) -> None:
    '''
    Writes a graph structure with color information to a text file.

    Args:
        graph (list[tuple[list[int], int]]): A list of tuples, each containing 
                                        a list of integers (nodes) and a single integer (color).
        colored_graph (list[int]): A list of integers representing the colors of the graph nodes.
        output_file (str): The path to the output text file where the graph will be written.

    Returns:
        None

    Examples:
    >>> import tempfile
    >>> graph = [([1, 2], 3), ([4, 5], 6)]
    >>> colored_graph = [7, 8]
    >>> with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
    ...     write_file(graph, colored_graph, tmpfile.name)
    ...     with open(tmpfile.name, "r", encoding="utf-8") as f:
    ...         print(f.read())
    1 2 7
    4 5 8
    '''
    nodes = [node[0] for node in graph]
    graph_txt = ""
    for node in zip(nodes, colored_graph):
        x, y, c = *node[0], node[1]
        graph_txt += f"{x} {y} {c}\n"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(graph_txt.strip())


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

    graph = [node[0] for node in graph]
    import_graph = []

    colored_graph = list(map(lambda c: colors[c], colored_graph))
    for (nodes, color) in zip(graph, colored_graph):
        import_graph.append((tuple(nodes), {"color":color}))
    g.add_nodes_from(import_graph)

    for node, _ in import_graph:
        for node_, _ in import_graph:
            if node != node_:
                g.add_edge(node, node_)

    pos = nx.spring_layout(g)
    node_colors = [g.nodes[node]['color'] for node in g.nodes]
    plt.figure(figsize=(8, 6))
    nx.draw(g, pos, with_labels=True, node_color=node_colors,\
         node_size=500, font_size=12, font_weight="bold")
    plt.title("Візуалізація графа з кольоровими вузлами")
    plt.show()

def generate_graph(num_nodes: int) -> list[tuple[list[int], int]]:
    '''
    Generates a large graph with `num_nodes` nodes, 
                where each node is connected to every other node.

    Args:
        num_nodes (int): The number of nodes in the graph.

    Returns:
        list[tuple[list[int], int]]: 
            A list of tuples, each containing a list of integers (nodes) and a color (integer).
    '''
    import random
    graph = []
    colored_graph = []

    for i in range(1, num_nodes + 1):
        nodes = [i, (i + 1) % num_nodes]
        color = random.randint(0, 2)
        graph.append((nodes, color))
        colored_graph.append(color)

    return graph, colored_graph

def main():
    '''
    Main function
    '''
    graph = read_file("testfile.csv")

    cnf = create_cnf(graph)

    implication_graph = create_implication_graph(cnf, len(graph) * 6)

    cnf_solution = find_solution(implication_graph)

    colored_graph = color_graph(cnf_solution)

    graph, colored_graph = generate_graph(20)

    write_file(graph, colored_graph, "output_file.csv")

    display_graph(graph, colored_graph)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()

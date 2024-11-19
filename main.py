"""
Graph_coloring
"""

def read_file(filepath: str) -> list[tuple[list[int], int]]:
    '''
    ...
    '''

    return []


def create_cnf(
        graph: list[tuple[list[int], int]]) -> list[tuple[int], int]:
    '''
    ...
    '''

    return []


def create_implication_graph(cnf: list[tuple[int, int]], vertexes_count: int) -> list[list[int]]:
    '''
    ...
    '''

    return []

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
    '''

    def tarjan_scc(vertex: int):
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
                vertices_stack.pop()

            scc_counter += 1

    n = len(implication_graph)

    vertexes_counter = 0
    scc_counter = 0
    disc = [-1] * n
    low = [-1] * n
    vertices_stack = []
    in_stack = [False] * n
    scc_result = [-1] * n

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
    each number is from 1 to 3 inclusively.
    If such coloring is impossible, returns None

    Args:
        cnf_solution (list[int] | None): corresponding CNF solution,
        which has 6*N vertexes and counts all necessary conditions for coloring
        or None if solution does not exist

    Returns:
        (list[int] | None): list of graph vertexes colors, each number is from 1 to 3 inclusively
        or None if such coloring is impossible

    Examples:
    >>> color_graph([True, False, False, False, True, True])
    [1]
    >>> color_graph([\
        False, False, True, True, True, False,\
        False, True, False, True, False, True\
    ])
    [3, 2]
    '''

    if cnf_solution is None:
        return None

    coloring = []
    for i in range(0, len(cnf_solution), 6):
        for j in range(0, 3):
            if cnf_solution[i + j]:
                coloring.append(j + 1)
                break

    return coloring


def write_file(colored_graph: list[int]) -> None:
    '''
    ...
    '''

    return None


def display_graph(colored_graph: list[int]):
    '''
    ...
    '''

    return None


def main():
    '''
    ...
    '''

    graph = read_file("testfile.csv")

    cnf = create_cnf(graph)

    implication_graph = create_implication_graph(cnf, len(graph) * 6)

    cnf_solution = find_solution(implication_graph)

    colored_graph = color_graph(cnf_solution)

    write_file(colored_graph)

    display_graph(colored_graph)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    main()

"""
Graph_coloring
"""

def read_file(filepath: str) -> list[tuple[list[int], int]]:
    '''
    ...
    '''

    return []


def create_knf(
        graph: list[tuple[list[int], int]]) -> list[tuple[int], int]:
    '''
    ...
    '''

    return []


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


def color_graph(implication_graph: list[list[int]]) -> list[int]:
    '''
    ...
    '''

    return []


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

    knf = create_knf(graph)

    implication_graph = create_implication_graph(knf, len(graph) * 6)

    colored_graph = color_graph(implication_graph)

    write_file(colored_graph)

    display_graph(colored_graph)

if __name__ == "__main__":
    main()

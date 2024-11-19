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
    '''
    ...
    '''

    return []


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

"""
Graph_coloring
"""
import matplotlib.pyplot as plt
import networkx as nx

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

    knf = create_knf(graph)

    implication_graph = create_implication_graph(knf, len(graph) * 6)

    colored_graph = color_graph(implication_graph)

    graph, colored_graph = generate_graph(20)

    write_file(graph, colored_graph, "output_file.csv")

    display_graph(graph, colored_graph)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()

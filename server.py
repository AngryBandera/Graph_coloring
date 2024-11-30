'Server to run website to display graph'

import re
from io import BytesIO
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from graph_handler import create_colored_graph, write_file, generate_graph

def validate_graph_file(lines) -> tuple[True, str]:
    """
    Validate the graph file format using regex.
    
    Args:
        content (str): The content of the graph file as a string.
        
    Returns:
        tuple: (bool, str) where the first element indicates if the file is valid,
               and the second element provides a message about the validation.

    Examples:
        >>> validate_graph_file("5,4\\n0,1,2,0,1\\n1,2\\n2,3\\n3,4\\n4,5")
        (True, 'Valid file.')
        
        >>> validate_graph_file("5,\\n0,1,2,0,1\\n1,2")
        (False, "First line must be 'nodes_num,edges_num' where both are integers.")
    """
    lines = lines.split("\n")
    if len(lines) < 2:
        return False, "File must have at least two lines: nodes/edges and node colors."

    # Validate the first line: nodes_num,edges_num
    if not re.match(r"\d+,\d+", lines[0].strip()):
        return False, "First line must be 'nodes_num,edges_num' where both are integers."

    if len(lines) < 50:
        # Validate the second line: colors
        if not re.match(r"([0-2],)*[0-2]", lines[1].strip()):
            return False, "Second line must be a comma-separated list of integers (0, 1, 2)."

        # Validate remaining lines: edges
        edge_pattern = re.compile(r"\d+,\d+")
        for line in lines[2:]:
            if line == '':
                continue
            if not edge_pattern.match(line.strip()):
                return False,f"Invalid edge format: '{line}'. Must be 'u,v' where u and v are integers."

    return True, "Valid file."

def graph_from_data(nodes_num: int, edges: list[list[int]],\
                    oldcolors: list[int]):
    '''Transforms ,,data,, to ,,factorset,, which is out graph storage method'''

    result = [[] for _ in range(nodes_num)]
    for edge in edges:
        result[edge[0]].append(edge[1])
        result[edge[1]].append(edge[0])
    return [(neighbors, oldcolors[i]) for i, neighbors in enumerate(result)]

def draw_graph(nodes_num: int, edges: list[list[int]],\
               oldcolors: list[int]) -> bool:
    """
    Draw the graph with nodes colored based on their color codes.
    """
    # transforming edges to 'factorset'
    graph = graph_from_data(nodes_num, edges, oldcolors)

    # using main algorithm to get colors of nodes
    is_valid, colored_graph = create_colored_graph(graph)
    if not is_valid:
        st.error("Solution for you graph does not exist")
        return False, False, False

    g = nx.Graph()

    colors = ["red", "green", "blue"]
    colored_graph = list(map(lambda c: colors[c], colored_graph))
    g.add_nodes_from([(node, {"color":colored_graph[node]}) \
                     for node in range(len(graph))])

    for index, node in enumerate(graph):
        for edge in node[0]:
            g.add_edge(index, edge)

    # Draw the graph
    if nodes_num > 1000:
        return True, "File is to big to draw", write_file(graph, colored_graph, None)

    plt.figure(figsize=(8, 6))
    nx.draw(
        g,
        with_labels=True,
        labels={index:str(colors[c][0]) for index, c in enumerate(oldcolors)},
        node_color=colored_graph,
        node_size=max(500-(nodes_num/50) * 100, 50),
        font_size=10,
        font_color="white",
    )
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return True, buf, write_file(graph, colored_graph, None)

def parse_graph(file_content) -> tuple[int, list, list]:
    """
    Parse the graph from the file content.
    """
    lines = file_content.splitlines()

    # Read number of nodes and edges
    nodes_num, _ = map(int, lines[0].split(","))

    # Read node colors
    colors = list(map(int, lines[1].split(",")))

    # Read edges
    edges = []
    for line in lines[2:]:
        u, v = map(int, line.split(","))
        edges.append((u, v))

    return nodes_num, edges, colors

def main() -> None:
    '''Main func'''
    # Streamlit UI
    st.title("Graph Visualization with Node Colors")

    # initialize var for image
    if "graph_img" not in st.session_state:
        st.session_state.graph_img = None
    if "graph_content" not in st.session_state:
        st.session_state.graph_content = None
    if "selected_method" not in st.session_state:
        st.session_state.selected_method = None

    input_method = st.radio("How would you like to input the graph?", \
                                ("Upload File", "Manual", "Random"))
    content = ""
    # handling user's method
    if input_method == "Manual":
        st.subheader("Input Graph Data")

        # Input size
        nodes_num = st.number_input("Number of nodes", min_value=1, step=1)
        edges_num = st.number_input("Number of edges", min_value=0, step=1)

        # Input colors
        st.text("Enter colors for each node as integers \
                (0 = red, 1 = green, 2 = blue), separated by commas:")
        colors_input = st.text_input("Node Colors")
        try:
            colors = [int(color.strip()) for color in colors_input.split(",")] \
                        if colors_input else []
        except ValueError:
            st.error("Ivalid colors format")\

        # Input edges
        st.text("Enter edges, one per line, in the format u,v (e.g., 1,2):")
        edges_input = st.text_area("Edges")
        edges = []
        if edges_input:
            for line in edges_input.splitlines():
                try:
                    u, v = map(int, line.split(","))
                    edges.append((u, v))
                except ValueError:
                    st.error(f"Invalid edge format: {line}")

        # Draw the graph if valid
        if st.button("Draw Graph"):
            if len(colors) == nodes_num and len(edges) <= edges_num:
                success, graph_image, content = draw_graph(nodes_num, edges, colors)
                if not success:
                    st.error("An error accured during drawing graph")
                else:
                    st.session_state.graph_content = content
                    st.session_state.graph_img = graph_image
                    if isinstance(graph_image, str):
                        st.error(graph_image)
                        st.session_state.graph_img = -1
            else:
                st.error("Please ensure the number of colors \
                        matches the number of nodes and the number of edges is valid.")

    elif input_method == "Upload File":
        st.subheader("Upload Graph File")
        uploaded_file = st.file_uploader("Choose a file", type=["csv"])

        if uploaded_file:
            file_content = uploaded_file.read().decode("utf-8")
            is_valid, msg = validate_graph_file(file_content)
            if is_valid:
                nodes_num, edges, colors = parse_graph(file_content)
                st.write("Graph loaded successfully!")
                st.write(f"Nodes: {nodes_num}, Edges: {len(edges)}")
                if st.button("Draw Graph"):
                    success, graph_image, content = draw_graph(nodes_num, edges, colors)
                    if not success:
                        st.error("An error accured during drawing graph")
                    else:
                        st.session_state.graph_content = content
                        st.session_state.graph_img = graph_image
                        if isinstance(graph_image, str):
                            st.error(graph_image)
                            st.session_state.graph_img = -1
            else:
                st.error(msg)

    elif input_method == "Random":
        nodes_num = st.number_input("Number of nodes", min_value=1, step=1)
        density = st.number_input("Density", min_value=0.0, max_value=1.0, step=0.1)

        if st.button("Draw Graph"):
            graph = generate_graph(nodes_num, density)
            edges = []
            for ind, node in enumerate(graph):
                for edge in node[0]:
                    if ind < edge:
                        edges.append([ind, edge])

            colors = list(map(lambda x: x[1], graph))

            success, graph_image, content = draw_graph(nodes_num, edges, colors)
            if not success:
                st.error("An error accured during drawing graph")
            else:
                st.session_state.graph_content = content
                st.session_state.graph_img = graph_image
                if isinstance(graph_image, str):
                    st.error(graph_image)
                    st.session_state.graph_img = -1

    if input_method != st.session_state.selected_method:
        st.session_state.graph_img = None
        st.session_state.selected_method = input_method

    if st.session_state.graph_img:
        if st.session_state.graph_img != -1:
            st.image(st.session_state.graph_img, caption="Graph Visualization")

        st.download_button(
            label="Download colored graph",
            data=st.session_state.graph_content,
            file_name="output.csv",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()

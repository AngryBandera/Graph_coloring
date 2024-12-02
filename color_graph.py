"""
Module to call functions from the command line interface
"""

import argparse
from streamlit.web import cli
import graph_handler

def main():
    """
    Main interaction function
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--visualizator", dest="visualizator", action='store_true')
    parser.add_argument("-i", dest="input_file")
    parser.add_argument("-o", dest="output_file")

    args = parser.parse_args()
    if args.visualizator:
        cli.main_run(["server.py"])
        return

    if args.input_file is None:
        args.input_file = "input.csv"
    if args.output_file is None:
        args.output_file = "output.csv"

    try:
        graph = graph_handler.read_file(args.input_file)
    except FileNotFoundError:
        print(f"File \"{args.input_file}\" is not found.")
        return

    result = graph_handler.create_colored_graph(graph)
    if not result[0]:
        print(f"Solution for the graph in file \"{args.input_file}\" does not exist.")
        return

    graph_handler.write_file(graph, result[1], args.output_file)

    print(f"Result was written to the \"{args.output_file}\".")

if __name__ == "__main__":
    main()

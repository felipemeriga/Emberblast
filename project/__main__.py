import sys

import matplotlib
from colorama import Fore
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from project.game import GameFactory
from project.map import MapFactory
from project.utils import print_greetings, generate_random_adjacent_matrix


def run_project(args):
    print_greetings()
    game_factory = GameFactory()
    game_orchestrator = game_factory.new_game()
    game_orchestrator.init_game()

# This function is an example of how to use Networkx
# def draw_graph(graph, labels=None, graph_layout='shell',
#                node_size=1600, node_color='blue', node_alpha=0.3,
#                node_text_size=12,
#                edge_color='blue', edge_alpha=0.3, edge_tickness=1,
#                edge_text_pos=0.3,
#                text_font='sans-serif'):
#     # create networkx graph
#     G = nx.Graph()
#
#     # add edges
#     for edge in graph:
#         G.add_edge(edge[0], edge[1])
#
#     # these are different layouts for the network you may try
#     # shell seems to work best
#     if graph_layout == 'spring':
#         graph_pos = nx.spring_layout(G)
#     elif graph_layout == 'spectral':
#         graph_pos = nx.spectral_layout(G)
#     elif graph_layout == 'random':
#         graph_pos = nx.random_layout(G)
#     else:
#         graph_pos = nx.shell_layout(G)
#
#     # draw graph
#     nx.draw_networkx_nodes(G, graph_pos, node_size=node_size,
#                            alpha=node_alpha, node_color=node_color)
#     nx.draw_networkx_edges(G, graph_pos, width=edge_tickness,
#                            alpha=edge_alpha, edge_color=edge_color)
#     nx.draw_networkx_labels(G, graph_pos, font_size=node_text_size,
#                             font_family=text_font)
#
#     if labels is None:
#         labels = range(len(graph))
#
#     edge_labels = dict(zip(graph, labels))
#     nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels,
#                                  label_pos=edge_text_pos)
#     plt.rcParams["figure.figsize"] = (100, 3)
#     plt.box(False)
#     # show graph
#     plt.show()


if __name__ == '__main__':
    try:
        run_project(sys.argv)

    except Exception as err:
        print(Fore.RED + "System shutdown with unexpected error")
        exit()

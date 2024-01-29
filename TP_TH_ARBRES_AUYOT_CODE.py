import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Chemin du fichier Excel contenant les données de liaisons routières
new_file_path = "ADRESSE DU FICHIER EXCEL SOURCE" #nom du fichier à modifier 

# Fonction pour créer le graphe à partir du fichier Excel
def create_graph(file_path):
    excel_data = pd.read_excel(file_path)
    G = nx.DiGraph()
    for _, row in excel_data.iterrows():
        G.add_edge(row['Noeud de Départ'], row['Nœud d\'Arrivée'], weight=row['Distance (km)'])
        G.add_edge(row['Nœud d\'Arrivée'], row['Noeud de Départ'], weight=row['Distance (km)'])
    return G

# Fonction pour sélectionner le sommet de départ
def select_starting_node(G):
    start_node = input("Entrez le nom du sommet de départ: ")
    while start_node not in G.nodes:
        print("Le sommet n'existe pas. Veuillez réessayer.")
        start_node = input("Entrez le nom du sommet de départ: ")
    return start_node

# Fonction pour sélectionner les sommets de passage
def select_passage_nodes(G, max_nodes=6):
    num_nodes = int(input(f"Entrez le nombre de sommets de passage (max {max_nodes}): "))
    num_nodes = min(num_nodes, max_nodes)  # Limiter à max_nodes
    nodes = []
    for i in range(num_nodes):
        node = input(f"Entrez le nom du sommet de passage {i+1}: ")
        while node not in G.nodes:
            print("Le sommet n'existe pas. Veuillez réessayer.")
            node = input(f"Entrez le nom du sommet de passage {i+1}: ")
        nodes.append(node)
    return nodes

# Fonction pour calculer et afficher le chemin optimal
def calculate_and_display_optimal_path(G, start_node, passage_nodes):
    # Calcul du chemin optimal en utilisant l'algorithme de Dijkstra
    optimal_path = [start_node]  # Le chemin commence par le sommet de départ
    total_distance = 0

    # Parcours des sommets de passage pour calculer le chemin optimal
    for i in range(len(passage_nodes)):
        shortest_path = nx.shortest_path(G, source=start_node, target=passage_nodes[i], weight='weight')
        optimal_path += shortest_path[1:]  # Ajout du chemin du sommet de départ au sommet de passage
        total_distance += nx.shortest_path_length(G, source=start_node, target=passage_nodes[i], weight='weight')
        start_node = passage_nodes[i]  # Mettre à jour le sommet de départ pour le prochain passage

    # Calcul du chemin le plus court pour revenir au point de départ
    shortest_return_path = nx.shortest_path(G, source=start_node, target=optimal_path[0], weight='weight')
    optimal_path += shortest_return_path[1:]  # Ajout du chemin de retour au point de départ
    total_distance += nx.shortest_path_length(G, source=start_node, target=optimal_path[0], weight='weight')

    # Affichage du chemin optimal
    print("Chemin optimal de livraison:")
    print(optimal_path)
    print("Distance totale parcourue:", round(total_distance, 2), "km")

    # Affichage du graphe avec le chemin optimal surligné en rouge
    pos = nx.spring_layout(G, k=2)  # Disposition des nœuds
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    for edge, label in edge_labels.items():
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', label_pos=0.5)
    for i in range(len(optimal_path) - 1):
        nx.draw_networkx_edges(G, pos, edgelist=[(optimal_path[i], optimal_path[i+1])], edge_color='red', width=2)
        plt.text((pos[optimal_path[i]][0] + pos[optimal_path[i+1]][0]) / 2,
                 (pos[optimal_path[i]][1] + pos[optimal_path[i+1]][1]) / 2,
                 str(round(G[optimal_path[i]][optimal_path[i+1]]['weight'], 2)) + 'km',
                 fontsize=8, color='black')
    plt.title("Graphe des Communes de la Guadeloupe")
    plt.show()

# Main - Intégration des étapes
if __name__ == "__main__":
    G_bidirectional = create_graph(new_file_path)
    start_node = select_starting_node(G_bidirectional)
    passage_nodes = select_passage_nodes(G_bidirectional)
    calculate_and_display_optimal_path(G_bidirectional, start_node, passage_nodes)


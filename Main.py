import heapq
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

# Grafo com as distâncias 
grafo = {
    'Guarita': {'Estacionamento': 500, 'Administrativo': 2000, 'Ginásio e academia': 8500},
    'Estacionamento': {'Guarita': 500, 'Subestação': 200, 'Administrativo': 1000},
    'Subestação': {'Estacionamento': 200, 'Garagem coberta': 200},
    'Garagem coberta': {'Subestação': 200},
    'Administrativo': {'Estacionamento': 1000, 'Salas de aula': 1610, 'Cantina': 3600, 'Guarita': 2000},
    'Salas de aula': {'Administrativo': 1610, 'Laboratorio': 904, 'Galpão de maquinas': 3986, 'Biblioteca e Pedagogico': 1160},
    'Laboratorio': {'Salas de aula': 904, 'Auditório': 1172},
    'Galpão de maquinas': {'Salas de aula': 3986},
    'Biblioteca e Pedagogico': {'Salas de aula': 1160, 'Auditório': 1082, 'Cantina': 2196},
    'Auditório': {'Biblioteca e Pedagogico': 1082, 'Laboratorio': 1172, 'Salas de aula': 1160},
    'Cantina': {'Biblioteca e Pedagogico': 2196, 'Administrativo': 3600, 'Ginásio e academia': 5000, 'Refeitório': 8176, 'Poço artesiano': 5449},
    'Ginásio e academia': {'Cantina': 5000, 'Guarita': 8500, 'Refeitório': 4130},
    'Refeitório': {'Cantina': 8176, 'Ginásio e academia': 4130},
    'Poço artesiano': {'Cantina': 5449},  
}

# Coordenadas personalizadas ajustadas para representar corretamente o mapa
pos_custom = {
    'Guarita': (10, -10),
    'Estacionamento': (8, -10),
    'Subestação': (6, -10),
    'Garagem coberta': (4, -10),
    'Administrativo': (8, -8),
    'Salas de aula': (6, -8),
    'Laboratorio': (4, -8),
    'Galpão de maquinas': (2, -8),
    'Biblioteca e Pedagogico': (6, -6),
    'Auditório': (4, -6),
    'Cantina': (8, -6),
    'Ginásio e academia': (10, -6),
    'Refeitório': (12, -6),
    'Poço artesiano': (8, -4)
}


def calcular_distancia(grafo, caminho):
    distancia_total = 0
    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i + 1]
        distancia_total += grafo[origem][destino]
    return distancia_total


def gerar_grafo_visual(grafo, caminho_bfs, caminho_dfs, caminho_dijkstra, dist_bfs, dist_dfs, dist_dijkstra, inicio, objetivo, pos_custom):
    G = nx.Graph()

    
    for local, vizinhos in grafo.items():
        for vizinho, distancia in vizinhos.items():
            G.add_edge(local, vizinho, weight=distancia)

    
    plt.figure(figsize=(12, 10))


    nx.draw_networkx(G, pos_custom, with_labels=True, node_size=3000, node_color="lightblue", font_size=10)

  
    path_edges = list(zip(caminho_dijkstra, caminho_dijkstra[1:]))
    nx.draw_networkx_edges(G, pos_custom, edgelist=path_edges, edge_color='r', width=2.5)

    # Resultados dos algoritmos BFS, DFS e Dijkstra 
    resultado_texto = (
        f"BFS: {' -> '.join(caminho_bfs)} (Distância: {dist_bfs} metros)\n"
        f"DFS: {' -> '.join(caminho_dfs)} (Distância: {dist_dfs} metros)\n"
        f"Dijkstra: {' -> '.join(caminho_dijkstra)} (Distância: {dist_dijkstra} metros)"
    )
    plt.figtext(0.1, 0.01, resultado_texto, wrap=True, horizontalalignment='left', fontsize=12)

    plt.title(f'Caminho mais rápido de {inicio} até {objetivo}')
    plt.show()


def buscar(grafo, inicio, objetivo):
    print(f"Buscando de {inicio} até {objetivo}...")
    
    caminho_bfs = bfs(grafo, inicio, objetivo)
    caminho_dfs = dfs(grafo, inicio, objetivo)
    caminho_dijkstra, dist_dijkstra = dijkstra(grafo, inicio, objetivo)

    if caminho_bfs and caminho_dfs and caminho_dijkstra:
        dist_bfs = calcular_distancia(grafo, caminho_bfs)
        dist_dfs = calcular_distancia(grafo, caminho_dfs)
        
       
        gerar_grafo_visual(grafo, caminho_bfs, caminho_dfs, caminho_dijkstra, dist_bfs, dist_dfs, dist_dijkstra, inicio, objetivo, pos_custom)

# Função BFS (Busca em Largura)
def bfs(grafo, inicio, objetivo):
    fila = deque([inicio])
    visitados = {inicio}
    caminho = {inicio: None}

    while fila:
        atual = fila.popleft()
        if atual == objetivo:
            return reconstruir_caminho(caminho, inicio, objetivo)
        
        for vizinho in grafo[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)
                caminho[vizinho] = atual

    return None

# Função DFS (Busca em Profundidade)
def dfs(grafo, inicio, objetivo):
    pilha = [inicio]
    visitados = {inicio}
    caminho = {inicio: None}

    while pilha:
        atual = pilha.pop()
        if atual == objetivo:
            return reconstruir_caminho(caminho, inicio, objetivo)
        
        for vizinho in grafo[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                pilha.append(vizinho)
                caminho[vizinho] = atual

    return None

# Função Dijkstra (Caminho mais curto com base em distâncias)
def dijkstra(grafo, inicio, objetivo):
    fila_prioridade = [(0, inicio)]
    distancias = {inicio: 0}
    caminho = {inicio: None}

    while fila_prioridade:
        dist_atual, atual = heapq.heappop(fila_prioridade)

        if atual == objetivo:
            return reconstruir_caminho(caminho, inicio, objetivo), dist_atual
        
        for vizinho, peso in grafo[atual].items():
            nova_dist = dist_atual + peso
            if vizinho not in distancias or nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                heapq.heappush(fila_prioridade, (nova_dist, vizinho))
                caminho[vizinho] = atual

    return None, float('inf')


def reconstruir_caminho(caminho, inicio, objetivo):
    caminho_final = []
    atual = objetivo
    while atual:
        caminho_final.append(atual)
        atual = caminho[atual]
    return caminho_final[::-1]


print("Locais disponíveis:")
for local in grafo:
    print(local)


inicio = input("\nDigite o ponto de partida: ")
objetivo = input("Digite o ponto de destino: ")

if inicio in grafo and objetivo in grafo:
    buscar(grafo, inicio, objetivo)
else:
    print("Ponto de partida ou destino inválido!")

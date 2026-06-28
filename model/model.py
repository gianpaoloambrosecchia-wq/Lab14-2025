import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}
        self._bestPath = []
        self._bestScore = 0


    def getPath(self, source):
        self._bestPath = []
        self._bestScore = 0
        parziale = [source]
        self._ricorsione(parziale, float("inf"))
        return self._bestPath, self._bestScore


    def _ricorsione(self, parziale, peso_prec):
        score = self._calcolaScore(parziale)
        if score > self._bestScore:
            self._bestScore = score
            self._bestPath = copy.deepcopy(parziale)

        for n in self._graph.successors(parziale[-1]):
            peso_corr = self._graph[parziale[-1]][n]["weight"]
            if peso_corr < peso_prec and n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, peso_corr)
                parziale.pop()


    def _calcolaScore(self, parziale):
        score = 0
        for i in range(len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return score


    def buildGraph(self, store, k):
        self._graph.clear()
        self._idMap = {}
        nodes = DAO.getAllNodes(store)
        self._graph.add_nodes_from(nodes)
        for node in nodes:
            self._idMap[node.order_id] = node
        edges = DAO.getAllEdges(store, k, self._idMap)
        for e in edges:
            self._graph.add_edge(e[0], e[1], weight = e[2])


    def getLongestPath(self, nodoSource):

        # METODO PIU SEMPLICE
        # Crea l'albero BFS a partire dal nodo sorgente
        albero_dfs = nx.dfs_tree(self._graph, nodoSource)

        # Restituisce i nodi dell'albero convertiti in lista (nodoSource incluso)
        return list(albero_dfs.nodes)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getAllStores(self):
        return DAO.getAllStores()


    def getNodes(self):
        return self._graph.nodes
import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._mappaA = {}

    def getRatings(self):
        return DAO.getRatings()

    def buildGraph(self, r1, r2):
        self._grafo.clear()
        self._nodiA = DAO.getNodiA(r1, r2)
        for n in self._nodiA:
            self._mappaA[n.id] = n
        self._grafo.add_nodes_from(self._nodiA)
        self._aggiungiArchi(r1, r2)

    def _aggiungiArchi(self, r1, r2):
        tupleArchi = DAO.getArchi(r1, r2, self._mappaA)
        for a1, a2, income in tupleArchi:
            if a1 in self._grafo.nodes and a2 in self._grafo.nodes:
                if self._grafo.has_edge(a1, a2):
                    self._grafo[a1][a2]["weight"] += int(income[1:])
                else:
                    self._grafo.add_edge(a1, a2, weight=int(income[1:]))

    def getConnessaInfo(self):
        components = list(nx.connected_components(self._grafo))
        largest = max(components, key=len)

        return len(components), largest

    def getArchiBest(self):
        archi = list(self._grafo.edges(data=True))
        archi.sort(key= lambda x: x[2]["weight"], reverse=True)
        return archi[:5]

    def getBestPath(self):
        self._bestPath = []
        parziale = []

        for n in self._grafo.nodes:
            parziale.append(n)
            self.ricorsione(parziale)
            parziale.pop()
        return self._bestPath

    def ricorsione(self, parziale):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        for n in self._grafo.neighbors(parziale[-1]):
            etaP = parziale[-1].date_of_birth
            etaS = n.date_of_birth
            if etaP > etaS:
                parziale.append(n)
                self.ricorsione(parziale)
                parziale.pop()


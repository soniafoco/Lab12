import copy
from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapRetailers = {}
        self._solBest = []
        self._bestObjVal = 0

    def getCountries(self):
        return DAO.getCountries()

    def buildGraph(self, year, country):
        self._retailers = DAO.getRetailersInCountry(country)
        for r in self._retailers:
            self._idMapRetailers[r.Retailer_code] = r

        self._grafo.clear()
        self._grafo.add_nodes_from(self._retailers)
        self._grafo.clear_edges()

        edges = DAO.getEdges(year, country)
        for edge in edges:
            r1 = self._idMapRetailers[edge[0]]
            r2 = self._idMapRetailers[edge[1]]
            if (not self._grafo.has_edge(r1, r2)) and (not self._grafo.has_edge(r2, r1)):
                self._grafo.add_edge(r1, r2, weight=edge[2])

        print(self._grafo)

    def getDettagliGraph(self):
        return len(self._grafo.nodes), len(self._grafo.edges)


    def getVolumi(self):
        retailersVolume = []
        for nodo in self._grafo.nodes:
            volume = 0
            vicini = self._grafo.neighbors(nodo)
            for v in vicini:
                volume += self._grafo[nodo][v]['weight']
            retailersVolume.append( (nodo, volume) )
        retailersVolume.sort(key=lambda x:x[1], reverse=True)
        return retailersVolume

    def getPath(self, lenght):
        paths = nx.simple_cycles(self._grafo, length_bound=lenght)
        validPaths = [p for p in paths if len(p)==lenght]
        self._solBest = []
        self._bestObjVal = 0
        for path in validPaths:
            path.append(path[0])
            objVal = self.getObjVal(path)
            if objVal > self._bestObjVal:
                self._bestObjVal = objVal
                self._bestPath = path

        return self._bestPath, self._bestObjVal


    def getPathRicorsione(self, lenght):
        self._solBest = []
        self._bestObjVal = 0

        parziale = []
        for v in self._grafo.nodes:
            parziale.append(v)
            self.ricorsione(parziale, lenght)
            parziale.pop()

        return self._solBest, self._bestObjVal


    def ricorsione(self, parziale, lenght):
        #Verifico se la lunghezza corrisponde a lenght
        if len(parziale)-1 == lenght and len(parziale)>1:
            print([x.Retailer_name for x in parziale])
            #Verifico se la soluzione è un ciclo ed è migliore della corrente
            if parziale[0]==parziale[-1]:
                objVal = self.getObjVal(parziale)
                if objVal>self._bestObjVal:
                    self._solBest = copy.deepcopy(parziale)
                    self._bestObjVal = objVal
            return

        #Aggiungo un nodo
        for v in self._grafo.neighbors(parziale[-1]):
            if len(parziale)-2!=lenght:
                if v not in parziale:
                    parziale.append(v)
                    self.ricorsione(parziale, lenght)
                    parziale.pop()
            else:
                parziale.append(v)
                self.ricorsione(parziale, lenght)
                parziale.pop()


    def getObjVal(self, list):
        objVal = 0
        for i in range(len(list)-1):
            objVal += self._grafo[list[i]][list[i+1]]["weight"]
        return objVal




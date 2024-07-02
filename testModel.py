import networkx as nx

from model.model import Model

myModel = Model()
myModel.buildGraph(2016, "Germany")

sol = myModel.getPath(5)

print("peso", sol[1])
for i in range(len(sol[0])-1):
    print(f"{sol[0][i].Retailer_name} --> {sol[0][i+1].Retailer_name}, {myModel._grafo[sol[0][i]][sol[0][i+1]]["weight"]}")

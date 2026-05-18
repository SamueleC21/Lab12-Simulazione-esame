from model.model import Model

model=Model()

model.buildGraph('8.8', '9.0')

print(model.getNumNodi())
print(model.getNumEdges())

from model.model import Model

model = Model() # creare il modello mi chiama il costruttore => il grafo esisterà ma sarà vuoto!
# costruisco il grafico
model.buildGraph()
# stampo il numero di nodi e di archi del grafo
print(f"Num nodi: {model.getNumNodi()}")
print(f"Num archi: {model.getNumArchi()}")


archiMaggiori = model.getEdgesPesati("12")
for a in archiMaggiori:
    print(a)
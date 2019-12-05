import rdflib

graph = rdflib.Graph()
graph.load('http://dbpedia.org/resource/Mathematics')

for object, predicate, subject in graph:
    print(object)
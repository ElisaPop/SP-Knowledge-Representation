#############################  DBPEDIA  ###############################
# from rdflib.plugins.sparql import prepareQuery
# from rdflib.graph import Graph
# #initNs={"dbpedia":'http://live.dbpedia.org/onthology/'}
# query = prepareQuery('''SELECT ?object WHERE {?subject dbpedia:language ?object.}''',
#                      initNs={"dbpedia": 'http://dbpedia.org/ontology/'})
#
# graph = Graph()
#
# graph.parse("http://dbpedia.org/resource/Romania.ntriples",format="n3")
#
# for dil in graph.query(query):
#     print(dil)
#########################  DBPEDIA   ####################################
# from SPARQLWrapper import SPARQLWrapper, JSON
#
# sparql = SPARQLWrapper("http://dbpedia.org/sparql")
# sparql.setQuery("""
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT ?label
#     WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
# """)
# sparql.setReturnFormat(JSON)
# results = sparql.query().convert()
#
# for result in results["results"]["bindings"]:
#     print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))
#####################################################################################
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
entropy_dictionary = dict()

stringPart1 = """SELECT DISTINCT ?org WHERE {
    ?org rdfs:subClassOf yago:Plant100017222 .
"""
stringPart2 = """FILTER (
            !EXISTS {
                ?tag rdf:type yago:
        """
stringPart3 = "}}"

def nrResults(subClass):
    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT (count(distinct ?tag)) as ?org WHERE { 
        ?tag rdf:type """ + "yago:" + subClass + """ .
        }
    """)
    sparql.setReturnFormat(JSON)
    results1 = sparql.query().convert()
    resultsString = str(results1)
    #print (resultsString)
    # return resultsString
    return resultsString[resultsString.find("'value': '") + 10: resultsString.find("'}}]") ]

def nrNonResults(subClass):
    return 0

def getAllPlants():
    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT (count(distinct ?tag)) as ?org WHERE { 
        ?tag rdf:type yago:Plant100017222 .
        }
    """)
    sparql.setReturnFormat(JSON)
    results1 = sparql.query().convert()
    resultsString = str(results1)
    return resultsString[resultsString.find("'value': '") + 10 : resultsString.find("'}}]}}")]

def printEntropy(subClass):
    nrRes = int(nrResults(subClass))
    nrNonRes = int(nrNonResults(subClass))
    if nrRes != 0:

        import re
        newString = re.sub(r"(\w)([A-Z])", r"\1 \2", subClass)
        newString1 = re.sub(r'[0-9]+', '', newString)
        newString1 = newString1.replace('Wikicat ','')
        newString1 = newString1.replace('Plants', 'Plant')
        entropy_dictionary[newString1] = nrRes


print(nrResults("PoisonousPlant113100156"))
print(getAllPlants())

sparql.setQuery("""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?org WHERE {
    ?org rdfs:subClassOf yago:Plant100017222 .
    }
 """)
sparql.setReturnFormat(JSON)
results = sparql.query()
#results.print_results()

for result in results:
    resultString = str(result)
    startPosition = resultString.find("yago/")
    endPosition = resultString.find("\" }")
    if  startPosition != -1 and resultString.find("DescribedIn") is -1 and resultString.find('&') is -1 and resultString[startPosition+5 : endPosition].find('\\') is -1:
        #print(resultString[startPosition+5:endPosition-1])
        printEntropy(resultString[startPosition+5 : endPosition])

import operator
sortedEntropy = sorted(entropy_dictionary.items(), key=operator.itemgetter(1))

for key,value in dict(sortedEntropy).items() :
    print(key,value)
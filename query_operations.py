import collections
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

string_part_1 = """SELECT DISTINCT ?org WHERE { ?org rdfs:subClassOf yago:Plant100017222 . """
string_part_2 = """FILTER ( !EXISTS { ?org rdfs:subClassOf yago:Performer110415638 . """
string_part_3 = "})}"

entropyDictionary = dict()

def append_exists(subClass):
    string_part_1.append("?org rdf:type: yago:" + subClass + " . ")

def append_not_exists(subClass):
    string_part_2.append("?org rdf:type yago:" + subClass + " . ")

def run_query():
    sparql.setQuery(string_part_1 + string_part_2 + string_part_3)
    sparql.setReturnFormat(JSON)
    results = sparql.query()

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

def get_entropy(sub_class):
    nrRes = int(nrResults(sub_class))
    if nrRes != 0:
        import re
        newString = re.sub(r"(\w)([A-Z])", r"\1 \2", sub_class)
        newString1 = re.sub(r'[0-9]+', '', newString)
        newString1 = newString1.replace('Wikicat ', '')
        newString1 = newString1.replace('Plants', 'Plant')
        entropyDictionary[(newString1,sub_class)] = nrRes

def print_entropies():
    sparql.setQuery(string_part_1 + string_part_2 + string_part_3)
    sparql.setReturnFormat(JSON)
    results = sparql.query()
    for result in results:
        resultString = str(result)
        startPosition = resultString.find("yago/")
        endPosition = resultString.find("\" }")
        if startPosition != -1 and resultString.find("DescribedIn") is -1 and resultString.find(
                '&') is -1 and resultString[startPosition + 5: endPosition].find('\\') is -1:
            # print(resultString[startPosition+5:endPosition-1])
            get_entropy(resultString[startPosition + 5: endPosition])

    import operator
    sortedEntropy = sorted(entropyDictionary.items(), key=operator.itemgetter(1))

    for key, value in dict(sortedEntropy).items():
        print(key, value)

def get_entropies():
    sparql.setQuery(string_part_1 + string_part_2 + string_part_3)
    sparql.setReturnFormat(JSON)
    results = sparql.query()
    for result in results:
        resultString = str(result)
        startPosition = resultString.find("yago/")
        endPosition = resultString.find("\" }")
        if startPosition != -1 and resultString.find("DescribedIn") is -1 and resultString.find(
                '&') is -1 and resultString[startPosition + 5: endPosition].find('\\') is -1:
            # print(resultString[startPosition+5:endPosition-1])
            get_entropy(resultString[startPosition + 5: endPosition])

    import operator
    sortedEntropy = sorted(entropyDictionary.items(), key=operator.itemgetter(1))

    return collections.OrderedDict(sortedEntropy)

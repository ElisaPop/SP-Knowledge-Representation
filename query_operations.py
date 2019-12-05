import collections
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

string_subclass_part_1 = """SELECT DISTINCT ?org WHERE { ?org rdfs:subClassOf yago:Plant100017222 . """
string_subclass_part_2 = """FILTER ( !EXISTS { ?org rdfs:subClassOf yago:Performer110415638 . """
string_subclass_part_3 = "})}"

string_type_part_1 = """ WHERE { ?tag rdf:type yago:Plant100017222"""
string_type_part_2 = """ . MINUS { SELECT DISTINCT ?tag WHERE {{?tag rdf:type: yago:WikicatAmericanFilms"""
string_type_part_3 = ". }}}}"

entropy_dictionary = dict()

def append_exists(subClass):
    string_subclass_part_1.append("?org rdfs:subClassOf yago:" + subClass + " . ")
    string_type_part_1.append("""; rdf:type yago:""" + subClass)

def append_not_exists(subClass):
    string_subclass_part_2.append("?org rdfs:subClassOf yago:" + subClass + " . ")
    string_type_part_2.append("""}UNION {?tag rdf:type yago:""" + subClass)

def run_query():
    sparql.setQuery(string_subclass_part_1 + string_subclass_part_2 + string_subclass_part_3)
    sparql.setReturnFormat(JSON)
    results = sparql.query()

def nr_results(subClass):
    sparql.setQuery("""SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + """; rdf:type yago:""" + subClass  + string_type_part_2 + string_type_part_3)
    sparql.setReturnFormat(JSON)
    results1 = sparql.query().convert()
    results_string = str(results1)
    #print("""SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + """ rdf:type yago:""" + subClass  + string_type_part_2 + string_type_part_3)
    return results_string[results_string.find("'value': '") + 10: results_string.find("'}}]") ]

def nr_non_results(subClass):
    sparql.setQuery("""SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + string_type_part_2 + """}UNION {?tag rdf:type yago:""" + subClass  + string_type_part_3)
    sparql.setReturnFormat(JSON)
    results1 = sparql.query().convert()
    results_string = str(results1)
    #print("""SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + string_type_part_2 + """}UNION {?tag rdf:type yago:""" + subClass  + string_type_part_3)
    return results_string[results_string.find("'value': '") + 10: results_string.find("'}}]")]

def get_entropy(sub_class):
    nrRes = int(nr_results(sub_class))
    if nrRes != 0:
        import re
        newString = re.sub(r"(\w)([A-Z])", r"\1 \2", sub_class)
        newString1 = re.sub(r'[0-9]+', '', newString)
        newString1 = newString1.replace('Wikicat ', '')
        newString1 = newString1.replace('Plants', 'Plant')
        entropy_dictionary[(newString1, sub_class)] = nrRes

def print_entropies():
    sparql.setQuery(string_subclass_part_1 + string_subclass_part_2 + string_subclass_part_3)
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
    sortedEntropy = sorted(entropy_dictionary.items(), key=operator.itemgetter(1))

    for key, value in dict(sortedEntropy).items():
        print(key, value)

def get_entropies():
    sparql.setQuery(string_subclass_part_1 + string_subclass_part_2 + string_subclass_part_3)
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
    sortedEntropy = sorted(entropy_dictionary.items(), key=operator.itemgetter(1))

    return collections.OrderedDict(sortedEntropy)

if __name__ == "__main__" :
    print(nr_non_results("PoisonousPlant113100156"))
    print(nr_results("PoisonousPlant113100156"))
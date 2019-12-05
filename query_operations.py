import collections
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict
from operator import getitem

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# #def global_paths():
# global string_subclass_part_1
# global string_subclass_part_2
# global string_subclass_part_3

string_subclass_part_1 = """SELECT DISTINCT ?org WHERE { ?org rdfs:subClassOf yago:Plant100017222 """
string_subclass_part_2 = """ . MINUS { SELECT DISTINCT ?org WHERE {{?org rdfs:subClassOf yago:Performer110415638"""
string_subclass_part_3 = ". }}}}"
#
# global string_type_part_1
# global string_type_part_2
# global string_type_part_3

string_type_part_1 = """ WHERE { ?tag rdf:type yago:Plant100017222"""
string_type_part_2 = """ . MINUS { SELECT DISTINCT ?tag WHERE {{?tag rdf:type: yago:WikicatAmericanFilms"""
string_type_part_3 = ". }}}}"

entropy_dictionary = dict()


def concat_string_types():
    return string_type_part_1 + string_type_part_2 + string_type_part_3


def concat_string_subclass():
    return string_subclass_part_1 + string_subclass_part_2 + string_subclass_part_3


def append_exists(subClass):
    global string_type_part_1
    global string_subclass_part_1

    string_subclass_part_1 += "; rdfs:subClassOf yago:" + subClass
    string_type_part_1 += """; rdf:type yago:""" + subClass

    #print(concat_string_subclass())
    #print(concat_string_types())


def append_not_exists(subClass):
    global string_type_part_2
    global string_subclass_part_2

    string_subclass_part_2 += "; rdfs:subClassOf yago:" + subClass
    string_type_part_2 += """}UNION {?tag rdf:type yago:""" + subClass

    #print(concat_string_subclass())
    #print(concat_string_types())


def run_query():
    sparql.setQuery(string_subclass_part_1 + string_subclass_part_2 + string_subclass_part_3)
    sparql.setReturnFormat(JSON)
    results = sparql.query()


###WORKING ###TESTED
def nr_results(sub_class):
    sparql.setQuery(
        """SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + """; rdf:type yago:""" + sub_class + string_type_part_2 + string_type_part_3)
    sparql.setReturnFormat(JSON)
    results1 = sparql.query().convert()
    results_string = str(results1)
    # print("""SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + """ rdf:type yago:""" + subClass  + string_type_part_2 + string_type_part_3)
    return results_string[results_string.find("'value': '") + 10: results_string.find("'}}]")]


###WORKING ###TESTED
def nr_non_results(subClass):
    sparql.setQuery(
        """SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + string_type_part_2 + """}UNION {?tag rdf:type yago:""" + subClass + string_type_part_3)
    sparql.setReturnFormat(JSON)
    results1 = sparql.query().convert()
    results_string = str(results1)
    # print("""SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + string_type_part_2 + """}UNION {?tag rdf:type yago:""" + subClass  + string_type_part_3)
    return results_string[results_string.find("'value': '") + 10: results_string.find("'}}]")]


def weird_division(n, d):
    return n / d if d else 0


def get_entropy(sub_class):
    nr_res = int(nr_results(sub_class))
    nr_non_res = int(nr_non_results(sub_class))
    if nr_res != 0 or nr_non_res != 0:
        import re
        new_string = re.sub(r"(\w)([A-Z])", r"\1 \2", sub_class)
        new_string = re.sub(r'[0-9]+', '', new_string)
        new_string = new_string.replace('Wikicat ', '')
        new_string = new_string.replace('Plants', 'Plant')
        entropy_dictionary[sub_class] = {'name': new_string, 'number': nr_res,
                                         'entropy': weird_division(nr_res, nr_non_res)}


def set_entropies():
    sparql.setQuery(concat_string_subclass())
    print(concat_string_subclass())
    sparql.setReturnFormat(JSON)
    results = sparql.query()
    for result in results:
        resultString = str(result)
        startPosition = resultString.find("yago/")
        endPosition = resultString.find("\" }")
        if startPosition != -1 and resultString.find("DescribedIn") is -1 and resultString.find(
                '&') is -1 and resultString[startPosition + 5: endPosition].find('\\') is -1:
            get_entropy(resultString[startPosition + 5: endPosition])


def print_entropies():
    set_entropies()
    res = OrderedDict(sorted(entropy_dictionary.items(),
                             key=lambda x: (getitem(x[1], 'entropy'), getitem(x[1], 'number'))))
    for sub in res:
        print(" " + res[sub]['name'] + ": " + str(res[sub]['entropy']))


def get_entropies():
    set_entropies()
    return OrderedDict(sorted(entropy_dictionary.items(),
                              key=lambda x: (getitem(x[1], 'entropy'), getitem(x[1], 'number'))))

if __name__ == "__main__":
    print(nr_non_results("PoisonousPlant113100156"))
    print(nr_results("PoisonousPlant113100156"))

    print_entropies()

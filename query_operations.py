import collections
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict
from operator import getitem

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# #def global_paths():
# global string_subclass_part_1
# global string_subclass_part_2
# global string_subclass_part_3

string_subclass_part_1 = """SELECT DISTINCT ?org WHERE { ?org rdfs:subClassOf yago:"""
string_subclass_part_2 = """Plant100017222"""
string_subclass_part_3 = " . }"

#
# global string_type_part_1
# global string_type_part_2
# global string_type_part_3

string_type_part_1 = """ WHERE { ?tag rdf:type yago:Plant100017222"""
string_type_part_2 = """ . MINUS { SELECT DISTINCT ?tag WHERE {{?tag rdf:type: yago:WikicatAmericanFilms"""
string_type_part_3 = " . }}}}"

current_label = "Plant"
max_results = 27983

entropy_dictionary = dict()
results_dictionary = dict()
sub_class_list = list
not_sub_class_list = list


def concat_string_types():
    return string_type_part_1 + string_type_part_2 + string_type_part_3


def concat_string_subclass():
    return string_subclass_part_1 + string_subclass_part_2 + string_subclass_part_3


def append_exists(sub_class):
    global string_type_part_1
    global string_subclass_part_2
    global current_label

    current_label = ''.join(i for i in sub_class if not i.isdigit())

    string_subclass_part_2 = sub_class
    string_type_part_1 += """; rdf:type yago:""" + sub_class


def append_not_exists(sub_class):
    global string_type_part_2
    string_type_part_2 += """}UNION {?tag rdf:type yago:""" + sub_class


def run_query():
    sparql.setQuery(concat_string_subclass())
    sparql.setReturnFormat(JSON)
    results = sparql.query()


def nr_results(sub_class):
    sparql.setQuery(
        """SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + """; rdf:type yago:""" + sub_class
        + string_type_part_2 + string_type_part_3)
    sparql.setReturnFormat(JSON)
    results1 = sparql.query().convert()
    results_string = str(results1)
    # print("""SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + """; rdf:type yago:""" + sub_class
    #     + string_type_part_2 + string_type_part_3)
    # print(results_string[results_string.find("'value': '") + 10: results_string.find("'}}]")])
    return results_string[results_string.find("'value': '") + 10: results_string.find("'}}]")]


def nr_non_results(sub_class):
    sparql.setQuery(
        """SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + string_type_part_2 +
        """}UNION {?tag rdf:type yago:""" + sub_class + string_type_part_3)
    sparql.setReturnFormat(JSON)
    results1 = sparql.query().convert()
    results_string = str(results1)
    # print("""SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + string_type_part_2 +
    #          """}UNION {?tag rdf:type yago:""" + sub_class + string_type_part_3)
    # print(results_string[results_string.find("'value': '") + 10: results_string.find("'}}]")])
    return results_string[results_string.find("'value': '") + 10: results_string.find("'}}]")]


def get_initial_max():
    global max_results
    sparql.setQuery("""SELECT (count(distinct ?tag)) as ?org""" + concat_string_types())
    sparql.setReturnFormat(JSON)
    results1 = sparql.query().convert()
    results_string = str(results1)
    max_results = int(results_string[results_string.find("'value': '") + 10: results_string.find("'}}]")])
    print(max_results)


def weird_division(n, d):
    if n + d > max_results: return 0
    return n / d if d else 0


def get_entropy(sub_class):
    nr_res = int(nr_results(sub_class))
    nr_non_res = int(nr_non_results(sub_class))
    div = weird_division(nr_res, nr_non_res)
    if div != 0:
        import re
        new_string = re.sub(r"(\w)([A-Z])", r"\1 \2", sub_class)
        new_string = re.sub(r'[0-9]+', '', new_string)
        new_string = new_string.replace('Wikicat ', '')
        new_string = new_string.replace('Plants', 'Plant')
        new_string = new_string.replace('Trees', 'Tree')
        entropy_dictionary[sub_class] = {'name': new_string, 'number': nr_res,
                                         'entropy': div}


def set_entropies():
    sparql.setQuery(concat_string_subclass())
    print(concat_string_subclass())
    sparql.setReturnFormat(JSON)
    results = sparql.query()
    for result in results:
        result_string = str(result)
        start_position = result_string.find("yago/")
        end_position = result_string.find("\" }")
        if start_position != -1 and result_string.find("DescribedIn") is -1 and result_string.find(
                '&') is -1 and result_string[start_position + 5: end_position].find('\\') is -1 \
                and result_string[start_position + 5: end_position].find('Of') is -1 \
                and result_string[start_position + 5: end_position].find('As') is -1 \
                and result_string[start_position + 5: end_position].find('Plant By') is -1 \
                and result_string[start_position + 5: end_position].find('Plant In') is -1 \
                and result_string[start_position + 5: end_position].find('.') is -1 \
                and result_string[start_position + 5: end_position].find('(.)') is -1:
            get_entropy(result_string[start_position + 5: end_position])


def set_results():
    sparql.setQuery("""SELECT DISTINCT ?tag""" + concat_string_types())
    print("""SELECT DISTINCT ?tag""" + concat_string_types())
    sparql.setReturnFormat(JSON)
    results = sparql.query()
    for result in results:
        result_string = str(result)
        print(result_string)
        start_position = result_string.find("resource/")
        end_position = result_string.find("\" }")
        if start_position != -1 and result_string.find("DescribedIn") is -1 and result_string.find(
                '&') is -1 and result_string[start_position + 9: end_position].find('\\') is -1 \
                and result_string[start_position + 9: end_position].find('Of') is -1 \
                and result_string[start_position + 9: end_position].find('As') is -1 \
                and result_string[start_position + 9: end_position].find('.') is -1 \
                and result_string[start_position + 9: end_position].find('(.)') is -1:
            results_dictionary[result_string[start_position + 9: end_position]] = {
                'name': result_string[start_position + 9: end_position]}


def print_entropies():
    entropy_dictionary.clear()
    set_entropies()
    res = OrderedDict(sorted(entropy_dictionary.items(),
                             key=lambda x: (getitem(x[1], 'entropy'), getitem(x[1], 'number'))))
    for sub in res:
        print(" " + res[sub]['name'] + ": " + str(res[sub]['entropy']))


def get_entropies():
    entropy_dictionary.clear()
    set_entropies()
    return OrderedDict(sorted(entropy_dictionary.items(),
                              key=lambda x: (getitem(x[1], 'entropy'), getitem(x[1], 'number'))))


def get_results():
    results_dictionary.clear()
    set_results()
    return OrderedDict(sorted(results_dictionary.items(),
                              key=lambda x: (getitem(x[1], 'name'))))


if __name__ == "__main__":
    # print(nr_non_results("PoinsonousPlants"))
    # print(nr_results("PoinsonousPlants"))
    # get_initial_max()
    print_entropies()
    append_exists("Tree113104059")
    print_entropies()

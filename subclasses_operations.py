from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict
from operator import getitem

import game
import subject_operations as po
from Subclass import Subclass

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

string_subclass_part_1 = """SELECT DISTINCT ?org WHERE { ?org rdfs:subClassOf yago:"""
string_subclass_part_2 = """Plant100017222"""
string_subclass_part_3 = " . }"

string_type_part_1 = """ WHERE { ?tag rdf:type yago:Plant100017222 ; rdf:type yago:VascularPlant113083586"""
string_type_part_2 = """ . MINUS { SELECT DISTINCT ?tag WHERE {{?tag rdf:type: yago:WikicatAmericanFilms"""
string_type_part_3 = " . }}}}"

entropy_list = []
entropy_zero = []
subclass_list = []
current_label = ""


def concat_string_types():
    return string_type_part_1 + string_type_part_2 + string_type_part_3


def concat_string_subclass():
    return string_subclass_part_1 + string_subclass_part_2 + string_subclass_part_3


def weird_division(n, d):
    # if n + d > max_results: return 0
    return n / d if d else 0


# Initializes the base subclasses we're going to get other subclasses from
def initialize():
    global string_subclass_part_2
    update_subclass("Plant100017222")
    subclass_list.append(Subclass(string_subclass_part_2, 0))
    update_subclass("VascularPlant113083586")
    subclass_list.append(Subclass(string_subclass_part_2, 0))


# Updates the current subclass whose subclasses we're adding to the entropy list
def update_subclass(subclass):
    global string_subclass_part_2
    global current_label
    string_subclass_part_2 = subclass


# Returns the number of Plants the given Subclass has to offer
def get_entropy(sub_class):
    sparql.setQuery(
        """SELECT (count(distinct ?tag)) as ?org""" + string_type_part_1 + """; rdf:type yago:""" + sub_class
        + string_type_part_2 + string_type_part_3)
    sparql.setReturnFormat(JSON)
    results1 = sparql.query().convert()
    results_string = str(results1)
    return results_string[results_string.find("'value': '") + 10: results_string.find("'}}]")]


def add_subclass(sub_class):
    entropy_list.append(Subclass(sub_class, get_entropy(sub_class)))


def create_entropy_list():
    global entropy_list
    global subclass_list
    entropy_list.clear()
    for subclass in subclass_list:
        update_subclass(subclass.label)
        set_entropies()

    # filters
    copy_entropy = entropy_list.copy()
    for sc in subclass_list:
        for ent in copy_entropy:
            if sc.name == ent.name or ent.entropy == 0:
                if ent in entropy_list:
                    entropy_list.remove(ent)


def set_entropies():
    sparql.setQuery(concat_string_subclass())
    # print(concat_string_subclass())
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
                and result_string[start_position + 5: end_position].find('(') is -1:
            sub_class = result_string[start_position + 5: end_position]
            if sub_class not in entropy_zero:
                ent = get_entropy(sub_class)
                if int(ent) > 0:
                    entropy_list.append(Subclass(sub_class, get_entropy(sub_class)))
                else:
                    entropy_zero.append(sub_class)


# In case the answer to one of the questions was "Y", append to subclass_list
# and add it to the entropy query
def append_exists(sub_class, b = 0):
    global subclass_list
    global string_type_part_1
    global string_subclass_part_2
    subclass_list.append(sub_class)
    string_type_part_1 += """; rdf:type yago:""" + sub_class.label
    if b == 1:
        string_subclass_part_2 = sub_class.label


# In case the answer to one of the questions was "N", add it to the entropy query
def append_not_exists(sub_class):
    global string_type_part_2
    string_type_part_2 += """}UNION {?tag rdf:type yago:""" + sub_class.label

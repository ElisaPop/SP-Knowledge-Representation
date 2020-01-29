from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict
from operator import getitem
import subclasses_operations as so
import game as game
from Plant import Plant
from Subject import Subject

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

string_plant_1 = "SELECT DISTINCT ?r WHERE{ dbr:"
string_plant_2 = "Caragana_arborescens"
string_plant_3 = " dct:subject ?r }"

plant_list = []
subject_list = []


def concat_string_plant():
    return string_plant_1 + string_plant_2 + string_plant_3


def append_subject(subject):
    so.string_type_part_1 += """; dct:subject dbc:""" + subject.label


def append_not_exist_subject(subject):
    so.string_type_part_2 += """}UNION {?tag dct:subject dbr:""" + subject.label


def set_plants():
    sparql.setQuery("""SELECT DISTINCT ?tag""" + so.concat_string_types())
    sparql.setReturnFormat(JSON)
    results = sparql.query()
    for result in results:
        result_string = str(result)
        start_position = result_string.find("resource/")
        end_position = result_string.find("\" }")
        if start_position != -1 and result_string.find("escribed") is -1 and result_string.find(
                '&') is -1 and result_string[start_position + 9: end_position].find('\\') is -1 \
                and result_string[start_position + 9: end_position].find('Of') is -1 \
                and result_string[start_position + 9: end_position].find(',') is -1 \
                and result_string[start_position + 9: end_position].find('As') is -1 \
                and result_string[start_position + 9: end_position].find('Wikicat') is -1 \
                and result_string[start_position + 9: end_position].find('.') is -1 \
                and result_string[start_position + 9: end_position].find('(') is -1:
            result = result_string[start_position + 9: end_position]
            plant_list.append(Plant(result))


def set_subjects(list_ap):
    sparql.setQuery(concat_string_plant())
    sparql.setReturnFormat(JSON)
    results = sparql.query()
    for result in results:
        result_string = str(result)
        start_position = result_string.find("Category:")
        end_position = result_string.find("\" }")
        if start_position != -1 and result_string.find("escribed") is -1 and result_string.find(
                '&') is -1 and result_string[start_position + 9: end_position].find('\\') is -1 \
                and result_string[start_position + 9: end_position].find('.') is -1 \
                and result_string[start_position + 9: end_position].find(',') is -1 \
                and result_string[start_position + 9: end_position].find('of') is -1 \
                and result_string[start_position + 9: end_position].find('(') is -1:
                list_ap.append(Subject(result_string[start_position + 9: end_position]))
    return list_ap


# and result_string[start_position + 9: end_position].find('plant') > 0 \

def create_plant_list():
    global plant_list

    plant_list.clear()
    set_plants()


def create_subject_list():
    global string_plant_2
    new_list = []
    for plt in plant_list:
        string_plant_2 = plt.label
        new_list = set_subjects(new_list)
        copy_list = new_list.copy()
        if subject_list.__len__() < 1:
            subject_list.extend(new_list)
            for s1 in subject_list:
                s1.add_plant(plt)

        for s1 in copy_list:
            for s2 in subject_list:
                if s2.label == s1.label:
                    if s2 in new_list:
                        new_list.remove(s2)
                    if s2 in subject_list:
                        s2.add_plant(plt)

        for s2 in new_list:
            s2.add_plant(plt)

        subject_list.extend(new_list)


def remove_plants_with_subject(subject):
    global plant_list
    copy_plant = plant_list.copy()
    for plt1 in copy_plant:
        for plt2 in subject.plant_list:
            if plt1.name == plt2.name:
                if plt1 in plant_list:
                    plant_list.remove(plt1)

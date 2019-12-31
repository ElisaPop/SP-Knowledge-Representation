import query_operations as qo

item = ()
seek = 0
results = 0

hasFlower = 0
hasFruit = 0

def ask_question():
    global item

    if results == 0:
        for sub in ordered_dictionary:
            print(" " + ordered_dictionary[sub]['name'] + ": " + str(ordered_dictionary[sub]['entropy']))
    else:
        for sub in ordered_dictionary:
            print(" " + ordered_dictionary[sub]['name'])

    item = ordered_dictionary.popitem(True)
    if item[1]['name'] == qo.current_label:
        item = ordered_dictionary.popitem(True)

    print("Is the plant a " + item[1]['name'] + "?")
    # print(type(item))


if __name__ == "__main__":

    print("Is the plant a Flower?")
    answer = str(input())
    if answer == 'Y':
        hasFlower = 1
    elif answer == 'N':
        hasFlower = 0

    qo.get_initial_max()



    while True:
        if seek == 0 and results == 0:
            ordered_dictionary = qo.get_entropies()
            if not bool(ordered_dictionary):
                results = 1

        if seek == 0 and results == 1:
            ordered_dictionary = qo.get_results()

        if not ordered_dictionary.keys():
            break
        else:
            ask_question()
            answer = str(input())
            if answer == 'Y':
                seek = 0
                qo.append_exists(item[0])
                ordered_dictionary.clear()
            elif answer == 'N':
                seek = 0
                qo.append_not_exists(item[0])
            else:
                seek = 1

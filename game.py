import query_operations as qo


def askQuestion():
    ordered_dictionary = qo.get_entropies()
    item = next(reversed(ordered_dictionary))

    print(ordered_dictionary.items())

    print("Is the plant a " + ordered_dictionary.get(item).get('name') + "?")
    answer = str(input())
    if (answer == 'Y'):
        qo.append_exists(item)
    else:
        qo.append_not_exists(item)


if __name__ == "__main__":
    while True:
        askQuestion()

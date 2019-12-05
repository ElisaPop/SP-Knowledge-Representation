import query_operations as qo

entropy_dictionary = qo.get_entropies()

def askQuestion():


    #second_word = (k[0][1] for k, v  in entropy_dictionary if word == k[0][0])


    print("Is the plant a " + list(entropy_dictionary.keys())[-1] + "?")
    answer = str(input())
    # if(answer == 'Y'):
    #     qo.append_exists()
    # else:
    #     qo.append_not_exists()



if __name__ == "__main__" :
    askQuestion()
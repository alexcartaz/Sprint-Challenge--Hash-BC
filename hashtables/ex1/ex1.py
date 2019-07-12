#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    print('weights: ' + str(weights) + ', length: ' + str(length) + ', limit: ' + str(limit))
    #if fewer than 2 weights    
    if length < 2:
        return None
    
    #initialize hash table
    ht = HashTable(limit)

    for index in range(0,length):
        hash_table_insert(ht, weights[index], index)

    #if 2+ weights and no exact weight
    index1 = 0
    index2 = 0
    for larger_weight in range(limit,0,-1):
        if larger_weight < limit/2:
            return None
        returned = hash_table_retrieve(ht, larger_weight)
        if returned != None:
            index1 = returned[0]
            smaller_weight = limit-larger_weight
            returned = hash_table_retrieve(ht, smaller_weight)
            if returned != None:
                index2 = returned[0]
                if index2 == index1:
                    index2 = returned[1]
                if index1 > index2:
                    return(index1, index2)
                else:
                    return(index2, index1)

    return None


def print_answer(answer):
    if answer is None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")

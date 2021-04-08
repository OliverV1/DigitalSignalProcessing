#!/usr/bin/python3
# -*- coding: utf-8 -*-

import timeit
import numpy as np

def looped_sum(R, V):
    summa = 0
    for i in range(1,R+1):
        for j in range(1,V+1):
            summa += 2*i*j
    return summa

def vectorized_sum(R, V):
    return (np.fromfunction(lambda i, j: (2*(i+1)*(j+1)), (R, V), dtype=int))

def fun_with_masks():
    listikene = np.random.randint(100, size=(4, 10))
    keskmine = np.mean(listikene)
    veergude_keskmine = np.mean(listikene,axis=0)
    mask = veergude_keskmine > keskmine
    return (listikene[:,mask])
    
   # print(veergude_keskmine)


    #for i in listikene:
        #mask = i > keskmine
        #print(i[mask])




def main():
    # t = timeit.Timer("vectorized_sum(1, 2)", "from yl2 import vectorized_sum")
    # print("Small vectorized", t.timeit(1000))
    # t = timeit.Timer("vectorized_sum(10, 10)", "from yl2 import vectorized_sum")
    # print("Small vectorized", t.timeit(1000))
    # t = timeit.Timer("vectorized_sum(100, 50)", "from yl2 import vectorized_sum")
    # print("Small vectorized", t.timeit(1000))
    # t = timeit.Timer("vectorized_sum(1000, 150)", "from yl2 import vectorized_sum")
    # print("Small vectorized", t.timeit(1000))
    # t = timeit.Timer("vectorized_sum(1000, 2000)", "from yl2 import vectorized_sum")
    # print("Small vectorized", t.timeit(1000))
    #
    # t = timeit.Timer("looped_sum(1, 2)", "from yl2 import looped_sum")
    # print("Small loops", t.timeit(1000))
    # t = timeit.Timer("looped_sum(10, 10)", "from yl2 import looped_sum")
    # print("Small loops", t.timeit(1000))
    # t = timeit.Timer("looped_sum(100, 50)", "from yl2 import looped_sum")
    # print("Small loops", t.timeit(1000))
    # t = timeit.Timer("looped_sum(1000, 150)", "from yl2 import looped_sum")
    # print("Small loops", t.timeit(1000))
    # t = timeit.Timer("looped_sum(1000, 2000)", "from yl2 import looped_sum")
    # print("Small loops", t.timeit(1000))
    print(vectorized_sum(10, 10))
    #print(looped_sum(10, 5))

    fun_with_masks()


    #np.fromfunction(lambda i, j: i + j, (3, 3), dtype=int)
    #https://numpy.org/doc/stable/reference/generated/numpy.fromfunction.html
    #Näide koodis toodud

if __name__ == "__main__":
    main()

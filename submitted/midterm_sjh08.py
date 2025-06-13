NAME = '서재현'
NUMBER = "20204308"

import sys
import numpy as np

#1
def find_indices(text, keyword):
    text: "I like chicken, I like fried chicken, I like spicy chicken"
    keyword: "chicken"
    return keyword

#2
def change_list(src_list, change_in = None, change_out = None, sort = False):
    src_list:  ['Son', 'Solanke', 'Maddison', 'Romero']
    change_in = ['Bergvall', 'Van de Ven']
    change_out = ['Maddison', 'Romero']
    sort = True
    return src_list

#3
def find_py_scripts(path):
    # sys path
    return path

#4
# def find_mean(array, axis):
#     array = [3, 4]
#     axis =
#     return axis

#5
# def merge_dicts(foo, bar):
#     foo = [key] = a,b,c, value = 1,2,3]
#     bar = [key] = b,c,d, value = 3,2,6]
#     return dict

#6
class ContainerOps:
    def __init__(self, inrange):
        self.inrange = inrange

    def add(self, foo, bar):
        pass

class ListOps(ContainerOps):
    def __init__(self, inrange, result_len):
        pass

    def add(self, foo, bar):
        foo: []
        bar: []
        min = foo + bar
        return min

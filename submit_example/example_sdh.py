import numpy as np
# MINUS: line space


def count_words(text):
    a = []
    b = []
    cnt = 0
    for i in text:
        a.append(i)
        if i == " ":
            b.append(a)
    return b


def average_list(data):
    result = sum(data)/len(data)
    return result


def get_key_with_max_value(data):
    a = []
    cnt = 0
    for i in data.values():
        a.append(i)
    max_val = max(a)
    idx = a.index(max_val)
    for i in data.keys():
        if cnt == idx:
            result = i
        cnt += 1
    return result


def merge_dicts(foo, bar):
    foo_key = list(foo.keys())
    bar_key = list(bar.keys())
    new_dic = {}
    return new_dic


def divide_and_sum(data, direction):
    result = 0
    arr1 = [[]]
    arr2 = [[]]
    a = 0
    r, c = np.shape(data)
    if direction == 'row':
        a = r//2
        for i in range(r-1):
            for j in range(c-1):
                if j > a:
                    arr2.append(data[i][j])
                else:
                    arr1.append(data[i][j])
    v1, v2 = 0, 0
    idx = np.shape(arr1)
    for i, j in range(idx):
        v1 += arr1[i][j]
        v2 += arr2[i][j]
    return v1, v2


def conditional_average(data, threshold):
    r, c = np.shape(data)
    lst = []
    for i in range(r):
        for j in range(c):
            if data[i][j] > threshold:
                lst.append(data[i][j])
    return sum(lst) / len(lst)


def mean_arrays(foo, bar):
    r, c = np.shape(foo)
    result = [0 for i in range(c)] * r
    for i in range(r-1):
        for j in range(c-1):
            result[i][j] = foo[i][j]
    return result

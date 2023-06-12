# 20174303 김용호
import numpy as np


def count_words(text):
    result = {}
    text = text.split()
    for i in text:
        if i in result.keys():
            result[i] += 1
        else:
            result[i] = 1
    return result


def average_list(data):
    data = np.array(data)
    result = data.sum() / len(data)
    return result


def get_key_with_max_value(data):
    result = "init"
    for i in data.keys():
        if result == "init":
            result = data[i]
        if data[i] > result:
            result = data[i]
    return result


def merge_dicts(foo, bar):
    result = {}
    for i in foo.keys():
        result[i] = foo[i]
    for i in bar.keys():
        if i in result.keys():
            result[i] += bar[i]
        else:
            result[i] = bar[i]
    return result


def divide_and_sum(data, direction):
    if direction not in ["row", "column"]:
        raise ValueError("Wrong direction value")
    if direction == "column":
        data = data.T
    row, col = data.shape
    result1, result2 = 0, 0
    for i in range(len(data)):
        if i + 1 <= row / 2:
            result1 += data[i].sum()
        else:
            result2 += data[i].sum()
    return result1, result2


def conditional_average(data, threshold):
    cnt, result = 0, 0
    for i in data:
        for j in i:
            if j > threshold:
                result += j
                cnt += 1
    if cnt == 0:
        return 0
    return result / cnt


def mean_arrays(foo, bar):
    if foo.shape != bar.shape:
        raise ValueError("different shapes")
    result = foo + bar
    result = result / 2
    return result

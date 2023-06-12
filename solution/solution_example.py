def count_words(text):
    words = text.split()
    words.sort()
    counts = {}
    for word in words:
        counts[word] = text.count(word)
    return counts


def average_list(data):
    return sum(data) / len(data)


def get_key_with_max_value(dct):
    if not dct:
        return None
    max_key = max(dct, key=dct.get)
    return max_key


def merge_dicts(d1, d2):
    result = dict(d1)
    for key, value in d2.items():
        if key in result:
            result[key] += value
        else:
            result[key] = value
    return result


import numpy as np


def divide_and_sum(data, direction):
    if direction == 'row':
        n = data.shape[0] // 2
        foo, bar = data[:n], data[n:]
    elif direction == 'column':
        n = data.shape[1] // 2
        foo, bar = data[:, :n], data[:, n:]
    else:
        raise ValueError('Wrong direction value')
    return np.sum(foo), np.sum(bar)


def conditional_average(data, threshold):
    target = data[data > threshold]
    if target.size == 0:
        return 0
    else:
        return np.mean(data[data > threshold])


def mean_arrays(foo, bar):
    if foo.shape != bar.shape:
        raise ValueError('different shapes')
    data = np.stack([foo, bar], axis=0)
    return np.mean(data, axis=0)

import os
import glob
import numpy as np


def find_indices(text, keyword):
    """
    :param text: 입력 문자열
    :param keyword: 검색어
    :return: text에 들어있는 모든 keyword를 검색하여 인덱스의 리스트 출력
    """
    result = []
    index = text.find(keyword)
    while index > 0:
        result.append(index)
        index = text.find(keyword, index+1)
    return result


def change_list(src_list, change_in=None, change_out=None, sort=False):
    """
    :param src_list: 원본 리스트
    :param change_in: src_list에 추가할 원소들을 리스트로 받음, 기본값 None이면 아무것도 하지 않음
    :param change_out: src_list에서 제거할 원소들을 리스트로 받음, 기본값 None이면 아무것도 하지 않음
    :param sort: True면 알파벳 순서로 정렬, False이면 아무것도 하지 않음
    :return: src_list에서 입력인자를 반영한 결과를 리턴
    """
    if change_in is not None:
        src_list.extend(change_in)
    if change_out is not None:
        for player in change_out:
            src_list.remove(player)
    if sort:
        src_list.sort()
    return src_list


def find_py_scripts(path):
    """
    path로 주어진 경로에서 .py 확장자를 가진 파일을 찾아 문자열 리스트로 반환한다.
    디렉토리가 아닌 파일만 찾아야 하며 파일이 위치한 경로가 포함되지 않도록 한다.
    path: 경로를 나타내는 문자열 e.g. "C:/mywork/project"
    return: list of file names e.g. ["apple.py", "banana.py", ...]
    """
    pattern = os.path.join(path, '*.py')
    files = glob.glob(pattern)
    files = [os.path.basename(file) for file in files]
    return files


def find_mean(array, axis):
    """
    array에서 axis에 대한 평균을 계산
    array: 2차원 배열 (N, M)
    axis: 평균을 구할 차원
    return: array를 axis에 대해 평균을 낸 결과
    """
    if axis == 0:
        mean = np.zeros((array.shape[1],))
        for i in range(array.shape[0]):
            mean += array[i]
        mean /= array.shape[0]
    else:
        mean = np.zeros((array.shape[0],))
        for i in range(array.shape[1]):
            mean += array[:, i]
        mean /= array.shape[1]
    return mean


def merge_dicts(foo, bar):
    """
    두 개의 dict 객체를 병합한 dict 객체를 만들어 반환한다.
    key가 겹칠 경우 두 값을 더하여 반영한다.
    :param foo: key는 문자열, value는 숫자인 dict 객체
    :param bar: key는 문자열, value는 숫자인 dict 객체
    :return: foo와 bar를 합친 dict 객체
    """
    result = {k: v for k, v in foo.items()}
    for k, v in bar.items():
        if k in result:
            result[k] += v
        else:
            result[k] = v
    return result


class ContainerOps:
    def __init__(self, inrange):
        """
        :param inrange: Tuple(int, int) 형태로 두 개의 값으로 입력된 값의 범위를 제한
            예를 들어, inrange=(5, 10)이면 1->5, 15->10으로 값을 바꿔서 계산해야 함
        """
        self.inrange = inrange

    def add(self, foo, bar):
        pass


class ListOps(ContainerOps):
    def __init__(self, inrange, result_len):
        """
        :param inrange: ContainerOps와 동일
        :param result_len: 연산 시 result_len 만큼만 구현
            예를 들어, result_len=5이면 앞의 5개 원소만 계산하고 반환
        """
        super().__init__(inrange)
        self.result_len = result_len

    def add(self, foo, bar):
        """
        foo와 bar의 값을 더한 새로운 리스트 반환, 두 리스트 중 짧은 쪽에 맞춰서 계산
        연산과정에서 inrange와 result_len 반영해야 함
        :param foo: 정수 데이터 리스트 (N)
        :param bar: 정수 데이터 리스트 (M)
        :return: foo와 bar의 값들을 더한 결과 (K=min(N,M))
        """
        # foo의 값들이 inrange[0] ~ inrange[1] 범위 안에 들어가도록 처리
        foo = [min(max(v, self.inrange[0]), self.inrange[1]) for v in foo]
        # bar의 값들이 inrange[0] ~ inrange[1] 범위 안에 들어가도록 처리
        bar = [min(max(v, self.inrange[0]), self.inrange[1]) for v in bar]
        # foo와 bar를 더하기
        result = [f+v for f, v in zip(foo, bar)][:self.result_len]
        return result





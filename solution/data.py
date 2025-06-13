import numpy as np

# 테스트 케이스를 명확하게 정의하기 위한 헬퍼 클래스
class FunctionInput:
    """함수 입력을 위한 클래스. 위치 인자와 키워드 인자를 모두 지원합니다."""
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class ClassInput:
    """클래스 테스트를 위한 클래스. 클래스 생성자와 메서드 호출을 구분합니다."""
    def __init__(self, init_args, method_args):
        self.init_args = init_args  # 클래스 생성자(__init__)에 전달될 인자 (튜플)
        self.method_args = method_args # 메서드에 전달될 인자 (FunctionInput 객체)


# 문제별 테스트 데이터 정의
TEST_CASES = {
    "find_indices": {
        "type": "function",
        "inputs": [
            FunctionInput("for the people by the people of the people", keyword="people"),
            FunctionInput("abracadabra", keyword="abra"),
            FunctionInput("aaaaa", keyword="aa"),
        ]
    },
    "change_list": {
        "type": "function",
        "inputs": [
            FunctionInput(['Son', 'Solanke', 'Maddison', 'Romero'], change_in=['Bergvall', 'Van de Ven'], change_out=['Maddison', 'Romero']),
            FunctionInput(['Son', 'Solanke', 'Bergvall', 'Van de Ven'], change_in=['Vicario'], sort=True),
            FunctionInput(['apple', 'banana', 'cherry'], sort=True),
        ]
    },
    "find_py_scripts": {
        "type": "function",
        # 입력은 run_test.py에서 동적으로 생성된 임시 디렉터리 경로가 됩니다.
        "inputs": [
            FunctionInput("dummy_path_1"),
            FunctionInput("dummy_path_2"),
            FunctionInput("dummy_path_3"),
        ]
    },
    "find_mean": {
        "type": "function",
        "inputs": [
            FunctionInput(np.arange(12).reshape(3, 4), axis=0),
            FunctionInput(np.arange(12).reshape(3, 4), axis=1),
            FunctionInput(np.array([[10, 20], [30, 40], [50, 60]]), axis=0),
        ]
    },
    "merge_dicts": {
        "type": "function",
        "inputs": [
            FunctionInput({'a': 1, 'b': 2, 'c': 3}, {'b': 3, 'c': 2, 'd': 6}),
            FunctionInput({'x': 10}, {'y': 20, 'z': 30}),
            FunctionInput({'a': 5}, {'a': 10, 'b': 15}),
        ]
    },
    "ListOps": {
        "type": "class",
        "class_name": "ListOps",
        "method_name": "add",
        "inputs": [
            ClassInput(init_args=((0, 5), 6), method_args=FunctionInput(list(range(0, 20, 2)), list(range(5, -5, -1)))),
            ClassInput(init_args=((-10, 10), 3), method_args=FunctionInput([15, -15, 5, 10], [-5, 12, -12, 8])),
            ClassInput(init_args=((0, 100), 10), method_args=FunctionInput([1, 2, 3], [101, -5, 200])),
        ]
    }
}

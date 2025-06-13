import importlib
import os
import shutil
import pandas as pd
import numpy as np
from glob import glob
import traceback

import config as cfg
from solution.data import TEST_CASES, FunctionInput, ClassInput

"""
채점 방법
- 문제에 대한 solution을 작성하여 solution.py로 저장한다.
- submitted_src 에 학생들이 제출한 파일을 넣는다.
- rename_files를 실행하여 이름을 수정한다.
- AI에게 solution.py를 넣어주고 적절한 예시 데이터를 만들어 data.py를 만든다.
- run_test.py를 돌려서 grade_result.csv 를 확인한다.
"""


class Grader:
    """학생들의 과제를 채점하고 결과를 집계하는 클래스"""

    def __init__(self, solution_mod_name, submit_pack_name, test_cases):
        self.solution_mod = self._safe_import(solution_mod_name)
        self.submit_pack = submit_pack_name
        self.test_cases = test_cases
        self.results = []

    def run(self):
        """제출된 모든 학생의 코드를 채점합니다."""
        if not self.solution_mod:
            print(f"Error: 정답 모듈 '{cfg.SOLUTION_MOD}'을 불러올 수 없습니다. 채점을 중단합니다.")
            return

        submitted_files = glob(os.path.join(self.submit_pack, '*.py'))
        print(f"총 {len(submitted_files)}개의 제출 파일을 찾았습니다.")

        for file_path in submitted_files:
            module_name = f"{self.submit_pack}.{os.path.basename(file_path)[:-3]}"
            print(f"\n--- 채점 시작: {module_name} ---")
            student_mod = self._safe_import(module_name)
            student_info = self._get_student_info(student_mod, module_name)

            # 학생 정보 변수가 없는 경우, 해당 파일 채점을 건너뜁니다.
            if student_info['name'] == 'Unknown' or student_info['number'] == 'Unknown':
                # Import 자체를 실패한 경우는 _get_student_info에서 'Import_Failed'를 반환하므로 여기 걸리지 않음
                if student_info['name'] != 'Import_Failed':
                    print(f"  [Error] {os.path.basename(file_path)} 파일에 NAME 또는 NUMBER 변수가 정의되지 않았습니다. 채점을 건너뜁니다.")
                    exit(1)

            scores = {'name': student_info['name'], 'number': student_info['number']}
            for problem_name, case_data in self.test_cases.items():
                if student_mod:  # 모듈 임포트 성공 시에만 채점
                    score = self._grade_one_problem(problem_name, case_data, student_mod)
                else:  # 임포트 실패 시 0점 처리
                    score = 0
                scores[problem_name] = score
                print(f"  - 문제 '{problem_name}': {score} / {len(case_data['inputs'])} 점")
            self.results.append(scores)
        self._save_results()

    def _grade_one_problem(self, problem_name, case_data, student_mod):
        """한 학생의 한 문제에 대해 채점을 진행합니다."""
        correct_count = 0

        # 'find_py_scripts'를 위한 동적 테스트 환경 생성
        temp_dirs = []
        if problem_name == 'find_py_scripts':
            # 테스트 케이스별로 임시 디렉터리 생성
            temp_dir_base = 'temp_test_dir'
            if os.path.exists(temp_dir_base):  # 혹시 이전에 비정상 종료로 남아있을 경우 삭제
                shutil.rmtree(temp_dir_base)
            os.makedirs(temp_dir_base)

            for i in range(len(case_data['inputs'])):
                temp_sub_dir = os.path.join(temp_dir_base, f'case_{i}')
                self._setup_find_py_scripts_env(temp_sub_dir)  # 여기서는 하위 디렉토리를 생성
                temp_dirs.append(temp_sub_dir)  # 실제 테스트에 사용될 경로

                # 중요: 실제 함수에 넘겨줄 인자는 base 디렉토리여야 함
                # setup_find_py_scripts_env가 temp_sub_dir 내부에 파일을 생성하므로
                # find_py_scripts 함수는 temp_sub_dir를 검색해야 합니다.
                case_data['inputs'][i] = FunctionInput(temp_sub_dir)

        for i, one_input in enumerate(case_data['inputs']):
            try:
                solution_target = self._get_target(self.solution_mod, problem_name, case_data)
                student_target = self._get_target(student_mod, problem_name, case_data)

                if student_target is None:  # 학생이 함수/클래스를 구현하지 않음
                    continue

                solution_result = self._execute(solution_target, one_input, case_data['type'])
                student_result = self._execute(student_target, one_input, case_data['type'])

                # find_py_scripts 결과는 순서가 다를 수 있으므로 정렬 후 비교
                if problem_name == 'find_py_scripts':
                    if self._compare_results(sorted(solution_result), sorted(student_result)):
                        correct_count += 1
                else:
                    if self._compare_results(solution_result, student_result):
                        correct_count += 1
            except Exception:
                # 학생 코드 실행 중 어떤 에러가 발생해도 0점 처리하고 계속 진행
                print(f"     [Error] 테스트 케이스 {i + 1} 실행 중 예외 발생:")
                # print(traceback.format_exc(limit=1)) # 자세한 에러 로그가 필요할 경우 주석 해제
                continue

        # 테스트 환경 정리 (수정된 부분)
        if temp_dirs:  # temp_dirs 리스트가 채워져 있는 경우 (find_py_scripts 문제)
            shutil.rmtree('temp_test_dir')  # 생성했던 부모 디렉터리만 한 번 삭제

        return correct_count

    def _execute(self, target, single_input, problem_type):
        """함수 또는 클래스 메서드를 실행하고 결과를 반환합니다."""
        if problem_type == 'function':
            return target(*single_input.args, **single_input.kwargs)
        elif problem_type == 'class':
            # 클래스 인스턴스화 -> 메서드 호출
            instance = target(*single_input.init_args)
            method = getattr(instance, single_input.method_args.kwargs.pop('method_name',
                                                                           TEST_CASES[target.__name__]['method_name']))
            return method(*single_input.method_args.args, **single_input.method_args.kwargs)

    def _get_target(self, module, problem_name, case_data):
        """모듈에서 채점 대상(함수 또는 클래스)을 안전하게 가져옵니다."""
        target_name = case_data.get('class_name', problem_name)
        return getattr(module, target_name, None)

    def _safe_import(self, module_name):
        """모듈을 안전하게 임포트하고, 실패 시 None을 반환합니다."""
        try:
            return importlib.import_module(module_name)
        except Exception as e:
            print(f"  [Import Error] 모듈 '{module_name}' 로딩 실패: {e}")
            return None

    def _get_student_info(self, module, module_name):
        """학생 정보(이름, 학번)를 모듈에서 가져옵니다."""
        if not module:
            return {'name': 'Import_Failed', 'number': module_name}
        return {
            'name': getattr(module, 'NAME', 'Unknown'),
            'number': getattr(module, 'NUMBER', 'Unknown')
        }

    def _setup_find_py_scripts_env(self, path):
        """find_py_scripts 테스트를 위한 임시 디렉터리 및 파일을 생성합니다."""
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(os.path.join(path, "subdir"))
        with open(os.path.join(path, "script1.py"), "w") as f: f.write("")
        with open(os.path.join(path, "script2.py"), "w") as f: f.write("")
        with open(os.path.join(path, "data.txt"), "w") as f: f.write("")
        with open(os.path.join(path, "subdir", "sub_script.py"), "w") as f: f.write("")

    def _compare_results(self, res1, res2):
        """두 결과가 같은지 비교합니다. Numpy 배열을 지원합니다."""
        if isinstance(res1, np.ndarray) or isinstance(res2, np.ndarray):
            return np.allclose(np.array(res1), np.array(res2))
        return res1 == res2

    def _save_results(self):
        """채점 결과를 CSV 파일로 저장합니다."""
        if not self.results:
            print("채점 결과가 없어 파일을 저장하지 않습니다.")
            return
        df = pd.DataFrame(self.results)
        cols = ['name', 'number'] + list(self.test_cases.keys())
        df = df[cols]
        df.sort_values(by='name', inplace=True, ignore_index=True)
        output_filename = 'grading_result.csv'
        df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        print(f"\n✅ 채점 완료! 결과가 '{output_filename}' 파일에 저장되었습니다.")


if __name__ == '__main__':
    grader = Grader(
        solution_mod_name=cfg.SOLUTION_MOD,
        submit_pack_name=cfg.SUBMIT_PACK,
        test_cases=TEST_CASES
    )
    grader.run()


import importlib
from glob import glob

import numpy as np
import pandas as pd


SOLUTION_MOD = 'solution.solution_example'
DATA_MOD = 'solution.data_example'


def run_test():
    solution_mod = importlib.import_module(SOLUTION_MOD)
    test_data = importlib.import_module(DATA_MOD).TEST_DATA
    module_files = glob('submitted/*.py')
    module_list = [mod.strip('./').strip('.py').replace('\\', '.') for mod in module_files]
    print('## submitted module list:', module_list)
    # module_list = module_list[:2]

    results = []
    for submitted_mod, mod_file in zip(module_list, module_files):
        # NOTE: when import error occurs, you should fix the error and mark 'MINUS' on the script
        submitted_mod = importlib.import_module(submitted_mod)
        result = evaluate_module(solution_mod, submitted_mod, test_data, mod_file)
        print('result', result)
        results += result

    df = pd.DataFrame(results)
    df.to_csv('eval_raw.csv', index=False, encoding='cp949')
    df = reform_table(df)
    df.to_csv('eval_mid.csv', index=False, encoding='cp949')


def evaluate_module(solution_mod, submitted_mod, test_data, mod_file):
    results = []
    user_name = submitted_mod.__name__.split('.')[1][:3]
    print(f'== evaluate user: {user_name}')
    for test_id, test_case in enumerate(test_data):
        print(f'-- evaluate test: {test_case.name}')
        result = eval_one_problem(solution_mod, submitted_mod, test_case, user_name, test_id)
        results.append(result)

    result = read_minus(mod_file, user_name)
    results.append(result)
    return results


def eval_one_problem(solution_mod, submitted_mod, test_case, user_name, test_id):
    result = {'user': user_name, 'test': f'{test_id+1}' + test_case.name, 'pass': 0, 'correct': 0}
    corr_func = eval('solution_mod.' + test_case.name)
    try:
        subm_func = eval('submitted_mod.' + test_case.name)
    except AttributeError as ae:
        print('[AttributeError]', ae)
        return result

    for one_input in test_case.inputs:
        exceptional_input = False
        try:
            corr_rslt = executer(corr_func, one_input)
        except ValueError as ve:
            print(f'Solution raised value error:', ve)
            exceptional_input = True

        try:
            subm_rslt = executer(subm_func, one_input)
        except ValueError as ve:
            if exceptional_input:
                result['pass'] += 1
                result['correct'] += 1
            continue
        except Exception as e:
            print(f'[Exception] failed to run {submitted_mod.__name__}.{subm_func.__name__}:', e)
            continue

        result['pass'] += 1
        if compare_results(corr_rslt, subm_rslt):
            result['correct'] += 1
    return result


def executer(function, input_val):
    if isinstance(input_val, tuple):
        out = function(*input_val)
    else:
        out = function(input_val)
    return out


def compare_results(corr_rslt, subm_rslt):
    try:
        if isinstance(corr_rslt, np.ndarray) and isinstance(subm_rslt, np.ndarray):
            if np.allclose(corr_rslt, subm_rslt):
                return True
        elif corr_rslt == subm_rslt:
            return True
        else:
            return False
    except ValueError as ve:
        print('[CompareError]', ve)
        return False


def read_minus(mod_file, user_name):
    result = {'user': user_name, 'test': 'minus', 'pass': 0, 'correct': 0}
    with open(mod_file, 'r', encoding='utf-8') as fr:
        scripts = fr.read()
    index = -1
    while 1:
        index = scripts.find('MINUS', index+1)
        if index < 0:
            break
        else:
            result['correct'] -= 1

    return result


def reform_table(df):
    df_pass = pivot_table(df, 'pass')
    df_corr = pivot_table(df, 'correct')
    print(df_corr)
    df_merg = df_pass.merge(df_corr, on='user')
    print(df_merg)
    return df_merg
    

def pivot_table(df, column):
    columns = list(set(df['test'].to_list()))
    column_mapper = {col: col[:10] + '_' + column[:4] for col in columns}
    df_pivot = df[['user', 'test', column]]
    df_pivot = df_pivot.pivot_table(column, ['user'], 'test')
    df_pivot = df_pivot.reset_index()
    df_pivot = df_pivot.rename(columns=column_mapper)
    return df_pivot


if __name__ == '__main__':
    run_test()

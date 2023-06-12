from dataclasses import dataclass
import numpy as np


@dataclass
class Function:
    name: str = ''
    inputs: list = None


TEST_DATA = [
    Function('count_words',
             ['for the people by the people of the people',
              'Success is walking from failure to failure with no loss of enthusiasm',
              'The ones who are crazy enough to think they can change the world, are the ones that do'
              ],
             ),
    Function('average_list',
             [[1, 2, 3, 4, 5],
              np.random.randint(0, 100, 10).tolist(),
              np.random.randint(0, 100, 50).tolist(),
              ],
             ),
    Function('get_key_with_max_value',
             [{'foo': 4, 'bar': 7, 'qux': 3},
              {'tot': 3, 'mct': 10, 'mnu': 8, 'liv': 5},
              {'son': 23, 'kane': 30, 'hol': 38, 'deb': 10},
              ],
             ),
    Function('merge_dicts',
             [({'kim': 2, 'lee': 5, 'park': 4}, {'lee': 3, 'john': 7, 'tom': 6}),
              ({'son': 25, 'kane': 12, 'hol': 54}, {'son': 8, 'hol': 3, 'deb': 9}),
              ]
             ),
    Function('divide_and_sum',
             [(np.random.randint(0, 10, (4, 5)), 'row'),
              (np.random.randint(0, 10, (7, 4)), 'row'),
              (np.random.randint(0, 10, (3, 5)), 'col'),
              (np.random.randint(0, 10, (3, 5)), 'mat'),
              ],
             ),
    Function('conditional_average',
             [(np.random.randint(0, 10, (2, 3)), 5),
              (np.random.randint(0, 30, (5, 3)), 10),
              (np.random.randint(0, 5, (4, 5)), 3),
              ],
             ),
    Function('mean_arrays',
             [(np.random.randint(0, 10, (2, 3)), np.random.randint(0, 10, (2, 3))),
              (np.random.randint(0, 30, (5, 4)), np.random.randint(0, 30, (5, 4))),
              (np.random.randint(0, 5, (4, 5)), np.random.randint(0, 5, (3, 5))),
              ],
             ),
]


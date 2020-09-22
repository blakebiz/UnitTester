import inspect
import timeit
import pprint
import test1, test2, test3
from copy import deepcopy
from typing import List, Dict, Callable, Union

def answer(x, *, y):
    return x+y


def log_time(name, solution, args, kwargs):
    if kwargs is None:
        cases = args
    else:
        cases = zip(args, kwargs)
    passed = total = 0
    for case in cases:
        if kwargs is None:
            arg1 = deepcopy(case)
            arg2 = deepcopy(case)
            s, a = solution(*arg1), answer(*arg2)
        else:
            arg, kwarg = case
            arg1, kwarg1 = deepcopy(arg), deepcopy(kwarg)
            arg2, kwarg2 = deepcopy(arg), deepcopy(kwarg)
            s, a = solution(*arg1, **kwarg1), answer(*arg2, **kwarg2)
        if s != a:
            Storage.results[name]['passed'] = False
            Storage.results[name]['failed'] = {'user': s, 'answer': a, 'cases passed': passed}
        else:
            passed += 1
        total += 1
    Storage.results[name]['total cases'] = total


class Storage:
    results: dict = {}
    @staticmethod
    def clear():
        Storage.results = {}


def test(solutions: Dict[str, Callable], args: List[tuple], kwargs: List[Dict[str, object]] = None,
         amount: int = 1) -> Dict[str, Dict[str, Union[bool, int, float, dict]]]:
    '''
    :param solutions: a Dictionary of {username (or ID) : user solution (must be callable like a function)}
    :param args: a List of test cases to pass to the function (each in tuples) or an empty list if None
    :param kwargs: a List of Dicts to pass to the function as kwargs (must be same length as args list)
    :param amount: amount of times each test case will be ran
    :return: a dictionary of {username: {'passed': bool, 'length': int, 'efficiency': float}}
    if the user fails then dictionary['failed'] will be equal to the test case that caused them to fail
    '''
    Storage.clear()
    for name, solution in solutions.items():
        Storage.results[name] = {'passed': True, 'length': len(inspect.getsource(solution).strip())}
        Storage.results[name]['efficiency'] = timeit.timeit(lambda: log_time(name, solution, args, kwargs), number=amount)
    return Storage.results


def main():
    solutions = {'test1': test1.solution, 'test2': test2.solution, 'test3': test3.solution}
    args = [(1,), (2,), (7,), (4,)]
    kwargs = [{'y': 5}, {'y': 3}, {'y': 8}, {'y': 3}]
    pprint.pprint(test(solutions, args, kwargs=kwargs))


if __name__ == '__main__':
    main()

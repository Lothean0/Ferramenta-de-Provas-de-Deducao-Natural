from typing import Optional

from servidor.utils.my_utils import split_expression

from config import n_hypothesis, knowledge_base, problems

def apply_implication_introduction(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:

    local_n_hypothesis = n_hypothesis
    local_knowledge_base = knowledge_base
    local_problems = problems

    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '->':
        raise ValueError('Implication introduction requires 3 arguments or symbol not ->')

    antecedent, consequent = arguments[1], arguments[2]
    # print(f'{antecedent} -> {consequent}')

    tmp = f'X{local_n_hypothesis}'
    knowledge_base[tmp] = antecedent
    local_n_hypothesis += 1

    available_hypothesis_new = available_hypothesis.copy()
    available_hypothesis_new.add(tmp)

    local_problems.pop(problem, None)

    local_problems[problem + '1'] = (consequent, available_hypothesis_new)

    result = [
        {
            "name": "(p0->p1)->p1",
            "parentId": "",
            "child": [],
            "hypothesis": [],
        },
        {
            "name": "p0->p1",
            "parentId": "",
            "child": [],
            "hypothesis": [],
        }
    ]

    return result
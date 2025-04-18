from typing import Any

from servidor.utils.my_utils import split_expression

from servidor.config import n_hypothesis, knowledge_base, problems

def apply_implication_introduction(
        logical_expr: str, # (p0 ->p1)
        available_hypothesis: set[str], # []
        problem: str #1
) -> list[dict[str, str | list[Any] | Any]]:

    local_n_hypothesis = n_hypothesis
    local_knowledge_base = knowledge_base
    local_problems = problems

    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '->':
        raise ValueError('Implication introduction requires 3 arguments or symbol not ->')

    antecedent, consequent = arguments[1], arguments[2]
    # print(f'{antecedent} -> {consequent}')

    tmp = f'X{local_n_hypothesis}'
    local_knowledge_base[tmp] = antecedent
    local_n_hypothesis += 1

    available_hypothesis_new = available_hypothesis.copy()
    available_hypothesis_new.add(tmp)

    print(f"Before remove{local_problems}")
    local_problems.pop(problem, None)
    print(f"After remove{local_problems}")

    print("Here 1")
    print(consequent)
    print(available_hypothesis_new)

    local_key = str(problem) + '1'

    local_problems[local_key] = (consequent, available_hypothesis_new)
    print("Here 2")

    result = [
        {
            "name": consequent,
            "parentId": "",
            "child": [],
            "knowledge_base": local_knowledge_base,
        },
    ]

    return result
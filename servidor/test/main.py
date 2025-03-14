from numpy.f2py.rules import aux_rules

from data_class import *
from utils import *
from grammar import myparser

import json

n_hypothesis = 0


# --- AXIOM ------------------------------------------------------------------------------------------------------------

def apply_axiom_rule(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    scanner = input('Select hypothesis: ')
    res = myparser.parse(scanner)
    for kb_key, kb_value in knowledge_base.items():
        if kb_value == res:
            if kb_key in available_hypothesis:
                problems.remove((logical_expr,available_hypothesis))
                return 'boo'
    return 'foo'


# --- IMPLICATION ------------------------------------------------------------------------------------------------------

def apply_implication_introduction(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '->':
        raise ValueError('Implication introduction requires 3 arguments or symbol not ->')

    antecedent, consequent = arguments[1], arguments[2]

    print(C_YELLOW + f'[DEBUG] ' + C_END + f'Arguments = {arguments}')
    print(C_YELLOW + f'[DEBUG] ' + C_END + f'Antecedent = {antecedent}')
    print(C_YELLOW + f'[DEBUG] ' + C_END + f'Consequent = {consequent}\n')

    global n_hypothesis
    tmp = next((kb_key for kb_key, kb_value in knowledge_base.items() if value == antecedent), None)

    if tmp is None:
        tmp = f'X{n_hypothesis}'
        knowledge_base[tmp] = antecedent
        n_hypothesis += 1

    if tmp not in available_hypothesis:
        available_hypothesis.append(tmp)

    if (logical_expr, available_hypothesis) in problems:
        problems.remove((logical_expr, available_hypothesis))

    problems.append((consequent, available_hypothesis))

    return consequent



"""
Modus Ponens (MP):
Also know as: Implication Elimination, Affirming the Antecedent

Modus Ponens is a valid rule of inference that states if you have a 
conditional statement (p->q) and the antecedent (p) is true, then you 
can infer that the consequent (q) is also true
"""

"""
Verificar esta regra!! temos de aplicar para qualquer hipotese. por exemplo (p1->p0)->p0 = II p0 = EI(p1->p0) (p1-p0)->p0, p0
"""
def apply_implication_elimination(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
        print(knowledge_base)
        res = input('Aux Formula (from kb or enter new expression): ')
        if res in knowledge_base:
            aux_formula = knowledge_base.get(res)
            problems.append((aux_formula, available_hypothesis))
            problems.append((f"EBinOp(->, {aux_formula}, {logical_expr})", available_hypothesis))
            return 'foo'
        else:
            aux_formula = myparser.parse(res)
            problems.append((aux_formula, available_hypothesis))
            problems.append((f"EBinOp(->, {aux_formula}, {logical_expr})", available_hypothesis))
            return 'boo'


# --- CONJUNCTION ------------------------------------------------------------------------------------------------------

def apply_conjunction_introduction(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '∧':
        raise ValueError('Conjunction introduction requires 3 arguments or symbol not ->')

    antecedent, consequent = arguments[1], arguments[2]

    problems.append((antecedent, available_hypothesis))
    problems.append((consequent, available_hypothesis))
    return 'boo'


def apply_conjunction_elimination_1(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    print(knowledge_base)
    res = input('Aux Formula (from kb or enter new expression): ')
    if res in knowledge_base:
        aux_formula = knowledge_base.get(res)
        problems.append((f"EBinOp(∧, {logical_expr}, {aux_formula})", available_hypothesis))
        return 'foo'
    else:
        aux_formula = myparser.parse(res)
        problems.append((f"EBinOp(∧, {logical_expr}, {aux_formula})", available_hypothesis))
        return 'boo'


def apply_conjunction_elimination_2(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    print(knowledge_base)
    res = input('Aux Formula (from kb or enter new expression): ')
    if res in knowledge_base:
        aux_formula = knowledge_base.get(res)
        problems.append((f"EBinOp(∧, {aux_formula}, {logical_expr})", available_hypothesis))
        return 'foo'
    else:
        aux_formula = myparser.parse(res)
        problems.append((f"EBinOp(∧, {aux_formula}, {logical_expr})", available_hypothesis))
        return 'boo'


# --- DISJUNCTION ------------------------------------------------------------------------------------------------------

def apply_disjunction_introduction_1(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '∨':
        raise ValueError('Disjunction introduction requires 3 arguments or symbol not ->')

    antecedent = arguments[1]

    problems.append((antecedent, available_hypothesis))
    return antecedent


def apply_disjunction_introduction_2(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '∨':
        raise ValueError('Disjunction introduction requires 3 arguments or symbol not ->')

    consequent = arguments[2]

    problems.append((consequent, available_hypothesis))
    return consequent


# ESTA ESTA MAL
def apply_disjunction_elimination(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    print(knowledge_base)
    res = input('Aux Formula (from kb or enter new expression): ')

    if res in knowledge_base:
        aux_formula = knowledge_base.get(res)
        problems.append((f"EBinOp(∧, {aux_formula}, {logical_expr})", available_hypothesis))
        return 'foo'
    else:
        aux_formula = myparser.parse(res)
        arguments = split_expression(aux_formula)
        if len(arguments) != 3 or arguments[0] != '∨':
            raise ValueError('Disjunction introduction requires 3 arguments or symbol not ->')
        problems.append((f"EBinOp(∧, {aux_formula}, {logical_expr})", available_hypothesis))
        return 'boo'



    knowledge_base.append('VARIAVEL 1')
    knowledge_base.append('VARIAVEL 2')
    problems.append(f"EBinOp(AND, EVar(VARIAVEL 1), EVar(VARIAVEL 2))")
    problems.extend([logical_expr] * 2)
    return 'boo'


# --- NEGATION ---------------------------------------------------------------------------------------------------------

def apply_negation_introduction(
        logical_expr: str,
        knowledge_base: Dict[str, str],
        available_hypothesis: List[str],
) -> Optional[str]:
    # logical_expr: EUnOp(~, EVar(p0))
    # content = expr.split("~,")[1].strip() or
    content = None
    match = re.search(r"EUnOp\(~, (.+)\)", logical_expr)

    if match:
        content = match.group(1)


    problems.append('ABSOLUTO')

    if content:
        knowledge_base.append(content)

    return 'boo'


# --- OTHERS -----------------------------------------------------------------------------------------------------------

def apply_rule(
        logical_expr: str,
        rule_name: str,
        available_hypothesis: List[str],
) -> Optional[Tuple[Optional[str], str]]:
    rule = rule_registry.get_rule(rule_name)
    if rule:
        return rule.apply(logical_expr, available_hypothesis), 'Ok'
    print(C_RED + f'[ERROR] ' + C_END + f'Rule not found')
    return None, 'Err'

def get_function_map() -> Dict[str, Callable[[str, List[str]], Optional[str]]]:
    return  {
        "apply_Implication_Introduction": apply_implication_introduction,
        "apply_Implication_Elimination": apply_implication_elimination,
        "apply_axiom_rule": apply_axiom_rule,
        "apply_Conjunction_Introduction": apply_conjunction_introduction,
        "apply_Conjunction_Elimination_1": apply_conjunction_elimination_1,
        "apply_Conjunction_Elimination_2": apply_conjunction_elimination_2,
        "apply_Disjunction_Introduction_1": apply_disjunction_introduction_1,
        "apply_Disjunction_Introduction_2": apply_disjunction_introduction_2,
        "apply_Disjunction_Elimination": apply_disjunction_elimination,
        "apply_Negation_Introduction": apply_negation_introduction
    }

def load_rules_from_file(file_path: str, rr: RuleRegistry) -> None:
    function_map = get_function_map()
    with open(file_path, 'r') as f:
        rules_data = json.load(f)

        for rule_data in rules_data:
            function_name = rule_data['apply']

            if function_name not in function_map:
                raise ValueError(f"Unknown function name in JSON: {function_name}")

            new_rule = Rule(
                name=rule_data['name'],
                other_names=rule_data.get('other_names', []),
                apply=function_map[function_name]
            )
            rr.register_rule(new_rule)


if __name__ == '__main__':

    rule_registry = RuleRegistry()

    load_rules_from_file('rules.json', rule_registry)

    knowledge_base = {}
    while True:
        res = input(C_BLUE + f'[ADD] ' + C_END + f'Add Hypothesis? (Yes/No) ').strip()
        print()
        if res.__eq__('Yes'):
            hypothesis = input(C_BLUE + f'[Hypt] (EVar() or EBinOp()) ' + C_END).strip()
            if hypothesis not in knowledge_base.values():
                knowledge_base[f'X{n_hypothesis}'] = hypothesis
                n_hypothesis += 1
        elif res.__eq__('No'):
            break
        else:
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Incorrect input')

    problems = []
    parsed_expression = myparser.parse(user_input := input('Enter logical expression: '))

    if parsed_expression:
        print(f'Parsed Expression: {parsed_expression}\n')
        problems.append((parsed_expression, [x for x in knowledge_base.keys() if x is not None]))

    else:
        print('Error parsing expression')

    while problems:
        print(C_GREEN + f'[INFO] ' + C_END + f'Problems List: {problems}')

        rule = input('Rule: ')
        print()

        print(C_GREEN + f'[INFO] ' + C_END + f'knowledge Base Before Applying Rule')
        if not knowledge_base:
            print(C_YELLOW + f'Empty knowledge base' + C_END)
        else:
            for key, value in knowledge_base.items():
                print(C_YELLOW + f'{key}: ' + C_END + f'{myparser.parse(value)}')
        result, status = apply_rule(problems[0][0], rule_name=rule,available_hypothesis=problems[0][1])

        if status == 'Ok':
            print(result)
            if result != 'boo' and result != 'foo':
                print(result)
                result = remove_outer_parentheses(myparser.parse(result))

        print(C_GREEN + f'[INFO] ' + C_END + f'knowledge Base After Applying Rule')
        if not knowledge_base:
            print(C_YELLOW + f'Empty knowledge base' + C_END)
        else:
            for key, value in knowledge_base.items():
                print(C_YELLOW + f'{key}: ' + C_END + f'{myparser.parse(value)}')

        print(C_GREEN + f'[INFO] ' + C_END + f'Result: {result}')

from matplotlib.style.core import available

from data_class import *
from myutils import *
from grammar import myparser
import os
import json

n_hypothesis = 0


# --- AXIOM ------------------------------------------------------------------------------------------------------------

def apply_axiom_rule(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:
    scanner = input('Select hypothesis: ')
    res = myparser.parse(scanner)
    for kb_key, kb_value in knowledge_base.items():
        if kb_value == res:
            if kb_key in available_hypothesis and logical_expr == kb_value:
                del problems[problem]
                return 'boo'
    return 'foo'


# --- IMPLICATION ------------------------------------------------------------------------------------------------------

def apply_implication_introduction(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '->':
        raise ValueError('Implication introduction requires 3 arguments or symbol not ->')

    antecedent, consequent = arguments[1], arguments[2]

    """print(C_YELLOW + f'[DEBUG] ' + C_END + f'Arguments = {arguments}')
    print(C_YELLOW + f'[DEBUG] ' + C_END + f'Antecedent = {antecedent}')
    print(C_YELLOW + f'[DEBUG] ' + C_END + f'Consequent = {consequent}\n')"""

    global n_hypothesis
    tmp = next((kb_key for kb_key, kb_value in knowledge_base.items() if kb_value == antecedent), None)
    print(tmp)

    if tmp is None:
        tmp = f'X{n_hypothesis}'
        knowledge_base[tmp] = antecedent
        n_hypothesis += 1

    available_hypothesis_new = available_hypothesis.copy()
    available_hypothesis_new.add(tmp)

    del problems[problem]

    problems[problem+'1'] = (consequent, available_hypothesis_new)

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
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:
        print(knowledge_base)
        res = input('Enter an Auxiliar Formula: ')
        if res in knowledge_base:
            aux_formula = knowledge_base.get(res)
            del problems[problem]
            problems[problem+'1']=(aux_formula, available_hypothesis)
            problems[problem+'2']=(f"EBinOp(->, {aux_formula}, {logical_expr})", available_hypothesis)
            return 'foo'
        else:
            aux_formula = myparser.parse(res)
            del problems[problem]
            problems[problem+'1']=(aux_formula, available_hypothesis)
            problems[problem+'2']=(f"EBinOp(->, {aux_formula}, {logical_expr})", available_hypothesis)
            return 'boo'


# --- CONJUNCTION ------------------------------------------------------------------------------------------------------

def apply_conjunction_introduction(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '∧':
        raise ValueError('Conjunction introduction requires 3 arguments or symbol not ->')

    antecedent, consequent = arguments[1], arguments[2]
    del problems[problem]
    problems[problem+'1']=(antecedent, available_hypothesis)
    problems[problem+'2']=(consequent, available_hypothesis)
    return 'boo'


def apply_conjunction_elimination_1(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:
    print(knowledge_base)
    res = input('Aux Formula (from kb or enter new expression): ')
    if res in knowledge_base:
        aux_formula = knowledge_base.get(res)
        del problems[problem]
        problems[problem+'1']=(f"EBinOp(∧, {logical_expr}, {aux_formula})", available_hypothesis)
        return 'foo'
    else:
        aux_formula = myparser.parse(res)
        del problems[problem]
        problems[problem+'1']=(f"EBinOp(∧, {logical_expr}, {aux_formula})", available_hypothesis)
        return 'boo'


def apply_conjunction_elimination_2(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:
    print(knowledge_base)
    res = input('Aux Formula (from kb or enter new expression): ')
    if res in knowledge_base:
        aux_formula = knowledge_base.get(res)
        del problems[problem]
        problems[problem+'1']=(f"EBinOp(∧, {aux_formula}, {logical_expr})", available_hypothesis)
        return 'foo'
    else:
        aux_formula = myparser.parse(res)
        del problems[problem]
        problems[problem+'1']=(f"EBinOp(∧, {aux_formula}, {logical_expr})", available_hypothesis)
        return 'boo'


# --- DISJUNCTION ------------------------------------------------------------------------------------------------------

def apply_disjunction_introduction_1(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '∨':
        raise ValueError('Disjunction introduction requires 3 arguments or symbol not ->')

    antecedent = arguments[1]

    del problems[problem]
    problems[problem+'1']=(antecedent, available_hypothesis)
    return antecedent


def apply_disjunction_introduction_2(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '∨':
        raise ValueError('Disjunction introduction requires 3 arguments or symbol not ->')

    consequent = arguments[2]

    del problems[problem]
    problems[problem+'1']=(consequent, available_hypothesis)
    return consequent


# --- DISJUNCTION ELIMINATION ------------------------------------------------------------------------------------------

def apply_disjunction_elimination(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:

    print(knowledge_base)
    res = input('Main Disjunction (from kb or enter new expression): ')
    res = myparser.parse(res)
    expr=split_expression(res)

    global n_hypothesis
    if len(expr) != 3 or expr[0] != '∨':
        raise ValueError('Disjunction elimination requires 3 arguments or symbol ∨')

    available_hypothesis_new1, available_hypothesis_new2 = available_hypothesis.copy(), available_hypothesis.copy()
    antecedent, consequent = expr[1], expr[2]


    for kb_key, kb_value in knowledge_base.items():
        if kb_value == antecedent:
            available_hypothesis_new1.add(kb_key)
        if kb_value == consequent:
            available_hypothesis_new2.add(kb_key)
            
    if expr[1] not in knowledge_base.values():
        knowledge_base[f'X{n_hypothesis}'] = antecedent
        n_hypothesis += 1
        available_hypothesis_new1.add(f'X{n_hypothesis-1}')

    if expr[2] not in knowledge_base.values():
        knowledge_base[f'X{n_hypothesis}'] = consequent
        n_hypothesis += 1
        available_hypothesis_new2.add(f'X{n_hypothesis-1}')

    del problems[problem]
    problems[problem+'1']=(f"EBinOp(∨, {antecedent}, {consequent})", available_hypothesis)
    problems[problem+'2']=(f"{logical_expr}", available_hypothesis_new1)
    problems[problem+'3']=(f"{logical_expr}", available_hypothesis_new2)
    return 'foo'

# --- NEGATION ---------------------------------------------------------------------------------------------------------

def apply_negation_introduction(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:
    # logical_expr: EUnOp(~, EVar(p0))
    # content = expr.split("~,")[1].strip() or
    content = None
    match = re.search(r"EUnOp\(~, (.+)\)", logical_expr)

    if match:
        content = match.group(1)

    del problems[problem]
    problems[problem+'1']=('ABSOLUTO', available_hypothesis)
    global n_hypothesis
    if content:
        if content not in knowledge_base.values():
            knowledge_base[f'X{n_hypothesis}'] = content
            n_hypothesis += 1
    return 'boo'

# --- IF AND ONLY IF ---------------------------------------------------------------------------------------------------


def apply_ifandonlyif_introduction(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:

    arguments = split_expression(logical_expr)

    if len(arguments) != 3 or arguments[0] != '⟺':
        raise ValueError('if and only if introduction requires 3 arguments or symbol ⟺')

    available_hypothesis_new1, available_hypothesis_new2 = available_hypothesis.copy(), available_hypothesis.copy()
    antecedent, consequent = arguments[1], arguments[2]

    # | ------------------ FALTA FAZER ISTO -------------------- |
    # | for kb_key, kb_value in knowledge_base.items():          |
    # |     if kb_value == antecedent:                           |
    # |         available_hypothesis_new1.add(kb_key)            |
    # |     if kb_value == consequent:                           |
    # |         available_hypothesis_new2.add(kb_key)            |
    # |                                                          |
    # | if arguments[1] not in knowledge_base.values():          |
    # |     knowledge_base[f'X{n_hypothesis}'] = antecedent      |
    # |     n_hypothesis += 1                                    |
    # |     available_hypothesis_new1.add(f'X{n_hypothesis - 1}')|
    # |                                                          |
    # | if arguments[2] not in knowledge_base.values():          |
    # |     knowledge_base[f'X{n_hypothesis}'] = consequent      |
    # |     n_hypothesis += 1                                    |
    # |     available_hypothesis_new2.add(f'X{n_hypothesis - 1}')|
    # | -------------------------------------------------------- |

    del problems[problem]
    problems[problem + '1'] = (antecedent, available_hypothesis_new1)  # available_hypothesis.add(antecedent)
    problems[problem + '2'] = (consequent, available_hypothesis_new2)
    return 'boo'


def apply_ifandonlyif_elimination_1(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:

    print(knowledge_base)
    res = input('Aux Formula (from kb or enter new expression): ')
    if res in knowledge_base:
        aux_formula = knowledge_base.get(res)
        del problems[problem]
        problems[problem + '1'] = (aux_formula, available_hypothesis)
        problems[problem + '2'] = (f"EBinOp(⟺, {aux_formula}, {logical_expr})", available_hypothesis)
        return 'foo'
    else:
        aux_formula = myparser.parse(res)
        del problems[problem]
        problems[problem + '1'] = (aux_formula, available_hypothesis)
        problems[problem + '2'] = (f"EBinOp(⟺, {aux_formula}, {logical_expr})", available_hypothesis)
        return 'boo'


def apply_ifandonlyif_elimination_2(
        logical_expr: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[str]:
    print(knowledge_base)
    res = input('Aux Formula (from kb or enter new expression): ')
    if res in knowledge_base:
        aux_formula = knowledge_base.get(res)
        del problems[problem]
        problems[problem + '1'] = (aux_formula, available_hypothesis)
        problems[problem + '2'] = (f"EBinOp(⟺, {logical_expr}, {aux_formula})", available_hypothesis)
        return 'foo'
    else:
        aux_formula = myparser.parse(res)
        del problems[problem]
        problems[problem + '1'] = (aux_formula, available_hypothesis)
        problems[problem + '2'] = (f"EBinOp(⟺, {logical_expr}, {aux_formula})", available_hypothesis)
        return 'boo'


# --- OTHERS -----------------------------------------------------------------------------------------------------------

def apply_rule(
        logical_expr: str,
        rule_name: str,
        available_hypothesis: set[str],
        problem: str
) -> Optional[Tuple[Optional[str], str]]:
    rule = rule_registry.get_rule(rule_name)
    if rule:
        return rule.apply(logical_expr, available_hypothesis, problem), 'Ok'
    print(C_RED + f'[ERROR] ' + C_END + f'Rule not found')
    return None, 'Err'

def get_function_map() -> Dict[str, Callable[[str, set[str], str], Optional[str]]]:
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
        "apply_Negation_Introduction": apply_negation_introduction,
        #"apply_IfAndOnlyIf_Introduction": apply_ifandonlyif_introduction,
        "apply_IfAndOnlyIf_Elimination_1": apply_ifandonlyif_elimination_1,
        "apply_IfAndOnlyIf_Elimination_2": apply_ifandonlyif_elimination_2
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


"""def print_tree(node: TreeNode, level: int = 0):
    indent = "    " * level
    print(f"{indent}- [{node.status}] Problem: {node.problem}")

    for child in node.children:
        print_tree(child, level + 1)"""


if __name__ == '__main__':

    rule_registry = RuleRegistry()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    load_rules_from_file(f'{dir_path}/rules.json', rule_registry)

    knowledge_base = {}
    while True:
        res = input(C_BLUE + f'[ADD] ' + C_END + f'Add Hypothesis? (Yes/No) ').strip()
        print()
        if res.__eq__('Yes'):
            hypothesis = myparser.parse(input(C_BLUE + f'Hypothesis: ' + C_END).strip())
            if hypothesis not in knowledge_base.values():
                knowledge_base[f'X{n_hypothesis}'] = hypothesis
                n_hypothesis += 1
        elif res.__eq__('No'):
            break
        else:
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Incorrect input')

    problems = {}
    parsed_expression = myparser.parse(user_input := input('Enter logical expression: '))

    if parsed_expression:
        print(f'Parsed Expression: {parsed_expression}\n')
        problems['P1'] = (parsed_expression, set([x for x in knowledge_base.keys() if x is not None]))
        """root_node = TreeNode(
            status="NotProve",
            problem={'Xi': parsed_expression},
            knowledge_base=knowledge_base.copy()
        )

        current_node = root_node"""

    else:
        print('Error parsing expression')

    while problems:
        #parsing needed
        print(C_GREEN + f'[INFO] ' + C_END + f'Problems List: {problems}')

        print()

        print(C_GREEN + f'[INFO] ' + C_END + f'knowledge Base Before Applying Rule')
        if not knowledge_base:
            print(C_YELLOW + f'Empty knowledge base' + C_END)
        else:
            print(C_YELLOW + f'{"Hypotesis"}: ' + C_END)
            for key, value in knowledge_base.items():
                print(C_YELLOW + f'{key}: ' + C_END + f'{myparser.parse(value)}')
        if len(problems) == 1:
            idx = list(problems.keys())[0]
        else:
            idx = input('Enter Problem index: ')
        if idx in problems.keys():
            rule = input('Rule: ')
            apply_rule(problems[idx][0], rule_name=rule, available_hypothesis=problems[idx][1], problem=idx)
        else:
            print(C_RED + '[ERROR] ' + C_END + 'Index out of range')
            continue

        """new_node = TreeNode(
            status='NotProve',
            problem={f'X_ii': result},
            knowledge_base=knowledge_base.copy(),
            parent=current_node
        )

        current_node.add_child(new_node)
        current_node = new_node"""

        print(C_GREEN + f'[INFO] ' + C_END + f'knowledge Base After Applying Rule')
        if not knowledge_base:
            print(C_YELLOW + f'Empty knowledge base' + C_END)
        else:
            print(C_YELLOW + f'{"Hypotesis"}: ' + C_END)
            for key, value in knowledge_base.items():
                print(C_YELLOW + f'{key}: ' + C_END + f'{myparser.parse(value)}')

        if not problems:
            print(C_GREEN + f'[INFO] ' + C_END + f'All problems solved')
            break
        else:
            print(C_YELLOW + f'{"Problems"}: ' + C_END)
            for key, value in problems.items():
                print(C_YELLOW + f'{key}: ' + C_END + f'{remove_outer_parentheses(myparser.parse(value[0]))}')

        # print_tree(root_node)

from data_class import *
import re
from grammar import myparser


n_hypothesis = 0


def removeOuterParentheses(s: str) -> str:
    result = ''

    if s[0] != '(':
        return s

    stack = []
    for i in s:
        stack.append(i)
        if stack and stack.count('(') == stack.count(')'):
            part = ''.join(stack)
            result += part[1:-1]
            stack = []

    return result

"""
This function checks if the antecedent or the negation of the consequent
is present in the knowledge base or wheter any of them can be deduced by
the current contents of the knowledge base.
"""
def split_expression(
        logical_expr: str,
) -> List[str]:
    pattern = r'([A-Za-z]+)\((.*)\)'
    match = re.match(pattern, logical_expr)
    if not match:
        raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Invalid expression')

    # match.group(1) = EbinOp
    content = match.group(2) # = [ -> , EVar(p0), EBinOp(->, EBinOp(->, EVar(p0), EVar(p1)), EVar(p1)) ]"
    balance, args, current_arg = 0, [], []

    for char in content:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1

        if char == ',' and balance == 0:
            args.append(''.join(current_arg).strip())
            current_arg = []
        else:
            current_arg.append(char)

    if current_arg:
        args.append(''.join(current_arg).strip())

    return args


def apply_axiom_rule(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    res = input('Select hypothesis: ')
    res=myparser.parse(res)
    for key, value in knowledge_base.items():
        if value == res:
            if key in available_hypothesis:
                problems.remove((logical_expr,available_hypothesis))
                return 'foo'
    return 'boo'

def apply_Implication_Introduction(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) < 3:
        return 'erro'
    # ERRO
    antecedent, consequent = arguments[1], arguments[2]

    print(C_YELLOW + f'[DEBUG] ' + C_END + f'Arguments = {arguments}')
    print(C_YELLOW + f'[DEBUG] ' + C_END + f'Antecedent = {antecedent}')
    print(C_YELLOW + f'[DEBUG] ' + C_END + f'Consequent = {consequent}\n')

    temp=''
    global n_hypothesis
    for key, value in knowledge_base.items():
        if value == antecedent:
            temp=key

    if temp == '':
        temp = f'X{n_hypothesis}'
        knowledge_base[temp] = antecedent
        n_hypothesis += 1

    available_hypothesis.append(temp)
    problems.remove((logical_expr,available_hypothesis))
    problems.append((consequent,available_hypothesis))

    return consequent


"""
Modus Ponens (MP):
Also know as: Implication Elimination, Affirming the Antecedent

Modus Ponens is a valid rule of inference that states if you have a 
conditional statement (p->q) and the antecedent (p) is true, then you 
can infer that the consequent (q) is also true
"""
def apply_Implication_Elimination(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
        print(knowledge_base)
        res = input('Select Hypothesis: ')
        if res in knowledge_base:
            problems.append(res)
            problems.append(f"EBinOp(->, {res}, {logical_expr})")
            return 'foo'
        return 'boo'


def apply_Conjunction_Introduction(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) < 3:
        return None

    antecedent, consequent = arguments[1], arguments[2]

    problems.append(antecedent)
    problems.append(consequent)
    return 'boo'


def apply_Conjunction_Elimination_1(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    print(knowledge_base)
    res = input('Select Hypothesis: ')
    if res in knowledge_base:
        problems.append(f"EBinOp(AND, {logical_expr}, {res})")
        return 'foo'
    return 'boo'


def apply_Conjunction_Elimination_2(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    print(knowledge_base)
    res = input('Select Hypothesis: ')
    if res in knowledge_base:
        problems.append(f"EBinOp(AND, {res}, {logical_expr})")
        return 'foo'
    return 'boo'


def apply_Disjunction_Introduction_1(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) < 3:
        return None

    antecedent, consequent = arguments[1], arguments[2]

    problems.append(antecedent)
    return antecedent


def apply_Disjunction_Introduction_2(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    if len(arguments) < 3:
        return None

    antecedent, consequent = arguments[1], arguments[2]

    problems.append(antecedent)
    return consequent


# ESTA ESTA MAL
def apply_Disjunction_Elimination(
        logical_expr: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    knowledge_base.append('VARIAVEL 1')
    knowledge_base.append('VARIAVEL 2')
    problems.append(f"EBinOp(AND, EVar(VARIAVEL 1), EVar(VARIAVEL 2))")
    problems.extend([logical_expr] * 2)
    return 'boo'


def apply_Negation_Introduction(
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


def apply_rule(
        logical_expr: str,
        rule_name: str,
        available_hypothesis: List[str],
) -> Optional[str]:
    rule = rule_registry.get_rule(rule_name)
    if rule:
        return rule.apply(logical_expr, available_hypothesis)
    print(C_RED + f'[ERROR] ' + C_END + f'Rule not found')
    return None


if __name__ == '__main__':

    rule_registry = RuleRegistry()

    rule_registry.register_rule(Rule(
        name='II',
        other_names=['Introduction: Implication'],
        apply=apply_Implication_Introduction,
    ))


    rule_registry.register_rule(Rule(
        name="EI",
        other_names=['Elimination: Implication'],
        apply=apply_Implication_Elimination
    ))

    rule_registry.register_rule(Rule(
        name="A",
        other_names=['Axiom'],
        apply=apply_axiom_rule
    ))

    rule_registry.register_rule(Rule(
        name="IC",
        other_names=['Introduction: Conjunction'],
        apply=apply_Conjunction_Introduction
    ))

    rule_registry.register_rule(Rule(
        name="EC_1",
        other_names=['Elimination: Conjunction_1'],
        apply=apply_Conjunction_Elimination_1
    ))

    rule_registry.register_rule(Rule(
        name="EC_2",
        other_names=['Elimination: Conjunction_2'],
        apply=apply_Conjunction_Elimination_2
    ))

    rule_registry.register_rule(Rule(
        name="ID_1",
        other_names=['Introduction: Disjunction_1'],
        apply=apply_Disjunction_Introduction_1
    ))

    rule_registry.register_rule(Rule(
        name="ID_2",
        other_names=['Introduction: Disjunction_2'],
        apply=apply_Disjunction_Introduction_2
    ))

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
        print(f'Parsed Expression: {parsed_expression}')
    else:
        print('Error parsing expression')

    expression_1 = parsed_expression
    problems.append((expression_1, [x for x in knowledge_base.keys() if x is not None]))

    while problems:
        print(C_GREEN + f'[INFO] ' + C_END + f'Problems List: {problems}')
        print(C_GREEN + f'[INFO] ' + C_END + f'knowledge Base_1: {knowledge_base}\n')

        rule = input('Rule: ')
        print()
        temp2 = []

        for temp in problems[0][1]:
            if temp in knowledge_base.keys():
                temp2.append(knowledge_base[temp])

        print(C_GREEN + f'[INFO] ' + C_END + f'Knowledge Base_2: {temp2}')

        result = apply_rule(problems[0][0], rule_name=rule,available_hypothesis=problems[0][1])
        if result != 'boo' and result != 'foo':
            print(result)
            result = removeOuterParentheses(myparser.parse(result))

        print(C_GREEN + f'[INFO] ' + C_END + f'Result: {result}')

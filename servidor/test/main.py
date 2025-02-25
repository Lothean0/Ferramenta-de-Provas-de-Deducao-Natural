import re
from data_class import *

"""
Rn if it doesnt find a suitable rule it stops
"""

def check_knowledge_base(
        premise_expr: str,
        knowledge_base: List[DeductionStep]
) -> bool:
    return any(premise_expr in step.obtained for step in knowledge_base)

def split_expression(
        logical_expr: str,
):
    pattern = r'([A-Za-z]+)\((.*)\)'

    match = re.match(pattern, logical_expr)
    if not match:
        raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Invalid expression')

    # match.group(1) = EbinOp
    content = match.group(2) # = [ -> , EVar(p0), EBinOp(->, EBinOp(->, EVar(p0), EVar(p1)), EVar(p1)) ]"

    args = []
    balance = 0
    current_arg = []

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


def apply_implication_rule(
        logical_expr: str,
        knowledge_base: List[DeductionStep]
) -> Optional[str]:
    arguments = split_expression(logical_expr)
    print(C_YELLOW + f'[DEBUG] ' + C_END + f'Arguments = {arguments}')
    if arguments:
        print(C_YELLOW + f'[DEBUG] ' + C_END + f'Antecedent = {arguments[1]}')
        print(C_YELLOW + f'[DEBUG] ' + C_END + f'Consequent = {arguments[2]}\n')

    if not check_knowledge_base(arguments[1], knowledge_base):
        knowledge_base.append(DeductionStep(obtained=[arguments[2]], rule="impl", from_=arguments[1]))
        return arguments[2]
    return None


def apply_negation_rule(
        logical_expr: str,
        knowledge_base: List[DeductionStep]
) -> Optional[str]:
    return None

def suggest_rule(
        logical_expr: str,
) -> Optional[str]:
    try:
        arguments = split_expression(logical_expr)
        operator = arguments[0]

        if operator == '->':
            return "impl"
        elif operator == '~':
            return "neg"
    except Exception as e:
        print(C_RED + f'[ERROR] ' + C_END + f'Invalid expression')
    return None

def apply_rule(
        logical_expr: str,
        rule_name: str,
        knowledge_base: List[DeductionStep]
) -> Optional[str]:
    if not rule_name:
        rule_name = suggest_rule(logical_expr)
        if rule_name:
            print(C_BLUE + f'[SUGGESTION] ' + C_END + f'Suggested Rule: {rule_name}')
            user_input = input(f'Apply this rule (Yes/No): ').strip().lower()
            print()
            if user_input == 'no':
                rule_name = input('Enter the rule you want to apply: ').strip()
                print(C_YELLOW + f'[DEBUG] ' + C_END + f'Applied Rule: {rule_name}')
            elif user_input != 'yes':
                print(C_RED + '[ERROR] ' + C_END + 'Invalid input')
                return None
        else:
            print(C_RED + f'[ERROR]' + C_END + f'No suitable rule found')
            print()
            return None
    rule = rule_registry.get_rule(rule_name)
    if rule:
        return rule.apply(logical_expr, knowledge_base)
    else:
        print(C_RED + f'[ERROR] ' + C_END + f'Rule not found')
        print()
        return None

if __name__ == '__main__':

    rule_registry = RuleRegistry()

    rule_registry.register_rule(Rule(
        name='impl',
        other_names=['Introduction: Implication'],
        description='If A -> B and A is known, then infer B.',
        apply=apply_implication_rule
    ))

    rule_registry.register_rule(Rule(
        name='neg',
        other_names=['Introduction: Negation'],
        description='',
        apply=apply_negation_rule
    ))

    knowledge_base = []
    expression = "EBinOp(->, EVar(p0), EBinOp(->, EBinOp(->, EVar(p0), EVar(p1)), EVar(p1)))"

    i = 0
    while expression:
        print(C_GREEN + f'[INFO] ' + C_END + f'Expression_{i}::{type(expression).__name__} = {expression}\n')
        result = apply_rule(expression, None, knowledge_base)
        print(C_GREEN + f'[INFO] ' + C_END + f'Result::{type(result).__name__} = {result}')
        print(C_GREEN + f'[INFO] ' + C_END + f'Knowledge Base::{type(knowledge_base).__name__} = {knowledge_base}\n')

        expression = result
        i = i+1



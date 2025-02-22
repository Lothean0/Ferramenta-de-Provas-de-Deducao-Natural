import re
from data_class import *

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
        raise ValueError(C_RED + f'[ERROR]' + C_END + f'Invalid expression')

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
    print(C_YELLOW + f'[DEBUG]' + C_END + f'Arguments = {arguments}')
    if arguments:
        print(C_YELLOW + f'[DEBUG]' + C_END + f'Antecedent = {arguments[1]}')
        print(C_YELLOW + f'[DEBUG]' + C_END + f'Consequent = {arguments[2]}\n')

        if not check_knowledge_base(arguments[1], knowledge_base):
            knowledge_base.append(DeductionStep(obtained=[arguments[2]], rule="impl", from_=arguments[1]))
            return arguments[2]
    return None

def apply_negation_rule(
        logical_expr: str,
        knowledge_base: List[DeductionStep]
) -> Optional[str]:
    return None

def apply_rule(
        logical_expr: str,
        rule_name: str,
        knowledge_base: List[DeductionStep]
) -> Optional[str]:
    rule = rule_registry.get_rule(rule_name)
    if rule:
        return rule.apply(logical_expr, knowledge_base)
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

    print(C_GREEN + f'[INFO]' + C_END + f'Initial expression::{type(expression).__name__} = {expression}\n')
    result = apply_rule(expression, "impl", knowledge_base)

    print(C_GREEN + f'[INFO]' + C_END + f'First Result::{type(result).__name__} = {result}')
    print(C_GREEN + f'[INFO]' + C_END + f'Knowledge Base::{type(knowledge_base).__name__} = {knowledge_base}\n')

    print(C_GREEN + f'[INFO]' + C_END + f'Second expression::{type(result).__name__} = {result}\n')
    result2 = apply_rule(result, "impl", knowledge_base)

    print(C_GREEN + f'[INFO]' + C_END + f'Second Result::{type(result2).__name__} = {result2}')
    print(C_GREEN + f'[INFO]' + C_END + f'Second Knowledge Base::{type(knowledge_base).__name__} = {knowledge_base}')
from data_class import *
import re

"""
This function checks if the antecedent or the negation of the consequent
is present in the knowledge base or wheter any of them can be deduced by
the current contents of the knowledge base.
"""

def check_knowledge_base(
        premise_expr: str,
        knowledge_base: List[str]
) -> bool:
    return premise_expr in knowledge_base


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


def apply_axiom_rule(
        logical_expr: str,
        knowledge_base: List[str],
) -> Optional[str]:
    res = input('Seleciona Axioma: ')
    return 'foo' if res in knowledge_base and res == logical_expr else 'boo'

def apply_Implication_Introduction(
        logical_expr: str,
        knowledge_base: List[str]
) -> Optional[str]:
    arguments = split_expression(logical_expr)

    print(C_YELLOW + f'[DEBUG] ' + C_END + f'Arguments = {arguments}')
    if arguments:
        print(C_YELLOW + f'[DEBUG] ' + C_END + f'Antecedent = {arguments[1]}')
        print(C_YELLOW + f'[DEBUG] ' + C_END + f'Consequent = {arguments[2]}\n')

    if not check_knowledge_base(arguments[1], knowledge_base):
        knowledge_base.append(
            arguments[1]
        )
    lista_branca.append(arguments[2])
    return arguments[2]

"""
Modus Ponens (MP):
Also know as: Implication Elimination, Affirming the Antecedent

Modus Ponens is a valid rule of inference that states if you have a 
conditional statement (p->q) and the antecedent (p) is true, then you 
can infer that the consequent (q) is also true
"""
def apply_Implication_Elimination(
        logical_expr: str,
        knowledge_base: List[str]
) -> Optional[str]:
        print(knowledge_base)
        res = input('Seliona hipotese')
        if res in knowledge_base:
            lista_branca.append(res)
            lista_branca.append(f"EBinOp(->, {res}, {logical_expr})")
            return 'foo2'
        return ''

def apply_rule(
        logical_expr: str,
        rule_name: str,
        knowledge_base: List[str]
) -> Optional[str]:
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
        name='II',
        other_names=['Introduction: Implication'],
        description='I dont know',
        apply=apply_Implication_Introduction,
    ))


    rule_registry.register_rule(Rule(
        name="EI",
        other_names=['Elimination: Implication'],
        description='If A -> B and A is known, then infer B.',
        apply=apply_Implication_Elimination
    ))

    rule_registry.register_rule(Rule(
        name="A",
        other_names=['Axiom: Implication'],
        description='I dont know',
        apply=apply_axiom_rule
    ))


    knowledge_base = []
    while True:
        res = input(C_BLUE + f'[ADD] ' + C_END + f'Add Hypt? (Yes/No) ').strip()
        if res.__eq__('Yes'):
            hypt = input(C_BLUE + f'[Hypt] (EVar() or EBinOp()) ' + C_END).strip()
            knowledge_base.append(hypt
            )
        elif res.__eq__('No'):
            break

    print(C_YELLOW + f'[INFO] ' + C_END + f'knowledge_Base_: {knowledge_base}\n')

    lista_branca = []
    expression_1 = "EBinOp(->, EVar(p0), EBinOp(->, EBinOp(->, EVar(p0), EVar(p1)), EVar(p1)))"
    lista_branca.append(expression_1)


    while lista_branca:
        print(C_YELLOW + f'[INFO] ' + C_END + f'Lista_: {lista_branca}\n')
        print(C_YELLOW + f'[INFO] ' + C_END + f'knowledge_Base_: {knowledge_base}\n')

        rule = input('Regra?')
        result = apply_rule(lista_branca[0], rule_name=rule, knowledge_base=knowledge_base)
        print(C_YELLOW + f'[INFO] ' + C_END + f'Result: {result}')
        if result != '':
            lista_branca.remove(lista_branca[0])
        print(C_YELLOW + f'[INFO] ' + C_END + f'knowledge_Base_: {knowledge_base}\n')

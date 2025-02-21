from data_class import *

def remove_outer_brackets(
        expression: str
) -> str:
    while expression.startswith("(") and expression.endswith(")"):
        inner_expr = expression[1:-1].strip()
        if is_balanced(inner_expr):
            expression = inner_expr
        else:
            break
    return expression


def is_balanced(
        expression: str
) -> bool:
    stack = 0
    for char in expression:
        if char == "(":
            stack += 1
        elif char == ")":
            stack -= 1
        if stack < 0:
            return False
    return stack == 0


def split_implication(
        expression: str
) -> Optional[List[str]]:
    expression = expression.strip()
    stack = 0
    for i in range(len(expression)):
        if expression[i] == "(":
            stack += 1
        elif expression[i] == ")":
            stack -= 1
        elif expression[i:i+2] == "->" and stack == 0:
            return [expression[:i].strip(), expression[i+2:].strip()]
    return None


def check_knowledge_base(
        premise: str,
        knowledge_base: List[DeductionStep]
) -> bool:
    return any(premise in step.obtained for step in knowledge_base)


def apply_implication_rule(
        expr: str,
        knowledge_base: List[DeductionStep]
) -> Optional[str]:
    split_expr = split_implication(expr)
    print(f'Expression after split: {split_expr}')
    if split_expr:
        before_imp, after_imp = map(remove_outer_brackets, split_expr)
        print(f'Before implication: {before_imp}')
        print(f'After implication: {after_imp}')
        if check_knowledge_base(before_imp, knowledge_base) or not knowledge_base:
            knowledge_base.append(DeductionStep(obtained=[after_imp], rule="impl", from_=before_imp))
            return after_imp
    return None


rule_registry = RuleRegistry()

rule_registry.register_rule(Rule(
    name="impl",
    other_names=["Introduction: Implication"],
    description="If 'A -> B' and A is known, then infer B.",
    apply=apply_implication_rule
))


def apply_rule(
        expr: str,
        rule_name: str,
        knowledge_base: List[DeductionStep]
) -> Optional[str]:
    rule = rule_registry.get_rule(rule_name)
    if rule:
        return rule.apply(expr, knowledge_base)
    return None


base = []
expression = "(p0 -> p1) -> p1"

result = apply_rule(expression, "impl", base)
print(result)
print(base)



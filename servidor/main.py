import re
from typing import List, Optional, Dict

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")


class Rule:
    def __init__(self, name: str, other_names: List[str], description: str, apply):
        self.name = name
        self.other_names = other_names
        self.description = description
        self.apply = apply


class RuleRegistry:
    def __init__(self):
        self.rules: Dict[str, Rule] = {}

    def register_rule(self, rule: Rule) -> None:
        self.rules[rule.name] = rule

    def get_rule(self, rule_name: str) -> Optional[Rule]:
        return self.rules.get(rule_name)


knowledge_base: List[str] = []
problems: List[str] = []
rule_registry = RuleRegistry()


def check_knowledge_base(premise_expr: str, knowledge_base: List[str]) -> bool:
    return premise_expr in knowledge_base


def split_expression(logical_expr: str) -> List[str]:
    pattern = r"([A-Za-z]+)\((.*)\)"
    match = re.match(pattern, logical_expr)
    if not match:
        raise ValueError(f"Invalid expression: {logical_expr}")

    content = match.group(2)
    balance = 0
    args: List[str] = []
    current_arg: List[str] = []

    for char in content:
        if char == "(":
            balance += 1
        elif char == ")":
            balance -= 1
        if char == "," and balance == 0:
            args.append("".join(current_arg).strip())
            current_arg = []
        else:
            current_arg.append(char)

    if current_arg:
        args.append("".join(current_arg).strip())

    return args


def apply_axiom_rule(logical_expr: str, knowledge_base: List[str]) -> Optional[str]:
    return "foo" if logical_expr in knowledge_base else "boo"


def apply_Implication_Introduction(
    logical_expr: str, knowledge_base: List[str]
) -> Optional[str]:
    arguments = split_expression(logical_expr)
    if len(arguments) < 3:
        return None

    antecedent, consequent = arguments[1], arguments[2]
    if not check_knowledge_base(antecedent, knowledge_base):
        knowledge_base.append(antecedent)

    problems.append(consequent)
    return consequent


def apply_Implication_Elimination(
    logical_expr: str, knowledge_base: List[str]
) -> Optional[str]:
    if logical_expr in knowledge_base:
        problems.append(logical_expr)
        return logical_expr
    return None


def apply_rule(
    logical_expr: str, rule_name: str, knowledge_base: List[str]
) -> Optional[str]:
    rule = rule_registry.get_rule(rule_name)
    if rule:
        return rule.apply(logical_expr, knowledge_base)
    return None


@app.route("/api/checkExpression", methods=["POST"])
def check_expression():
    data = request.get_json()
    expression = data.get("expression", "")
    rule = data.get("rule", "")

    if not expression or not rule:
        return jsonify({"error": "Missing expression or rule"}), 400

    problems.append(expression)  # Append expression to problems list
    result = apply_rule(expression, rule, knowledge_base)

    return jsonify(
        {"EXPRESSION": expression, "status": "Rule applied", "result": result}
    )


@app.route("/api/users", methods=["GET"])
def users():
    return jsonify({"users": ["daniel", "pedro", "simao"]})


rule_registry.register_rule(
    Rule(
        name="II",
        other_names=["Introduction: Implication"],
        description="Introduction of implication",
        apply=apply_Implication_Introduction,
    )
)
rule_registry.register_rule(
    Rule(
        name="EI",
        other_names=["Elimination: Implication"],
        description="If A -> B and A is known, then infer B.",
        apply=apply_Implication_Elimination,
    )
)
rule_registry.register_rule(
    Rule(
        name="A",
        other_names=["Axiom: Implication"],
        description="Axiom application rule",
        apply=apply_axiom_rule,
    )
)


if __name__ == "__main__":
    app.run(debug=True, port=3000)

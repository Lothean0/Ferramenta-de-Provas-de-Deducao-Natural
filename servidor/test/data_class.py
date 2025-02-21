from attr import dataclass
from typing import List, Optional, Dict, Callable


@dataclass
class DeductionStep:
    obtained: List[str]
    rule: str
    from_: Optional[str]


@dataclass
class Rule:
    name: str
    other_names: Optional[List[str]]
    description: Optional[str]
    apply: Callable[[str, List[DeductionStep]], Optional[str]]


class RuleRegistry:
    def __init__(self):
        self.rules: Dict[str, Rule] = {}

    def register_rule(self, rule: Rule):
        self.rules[rule.name] = rule
        if rule.other_names:
            for alias in rule.other_names:
                self.rules[alias] = rule

    def get_rule(self, name: str) -> Optional[Rule]:
        return self.rules.get(name)

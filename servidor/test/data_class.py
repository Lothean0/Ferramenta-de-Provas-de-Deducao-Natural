from attr import dataclass
from typing import List, Optional, Dict, Callable

C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE = '\033[94m'
C_END = '\033[0m'

@dataclass
class DeductionStep:
    obtained: List[str]
    rule: str
    from_: Optional[str]

    def __post_init__(self):
        if not self.obtained:
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'DeductionStep must have at least one obtained.')
        if not isinstance(self.rule, str) or not self.rule:
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'DeductionStep must have rule as string.')


@dataclass
class Rule:
    name: str
    other_names: Optional[List[str]]
    description: Optional[str]
    apply: Callable[[str, List[DeductionStep]], Optional[str]]

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Rule must have name as string.')
        if not callable(self.apply):
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Rule must have apply as callable.')



class RuleRegistry:
    def __init__(self):
        self.rules: Dict[str, Rule] = {}

    def register_rule(self, rule: Rule):
        if rule.name in self.rules:
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Rule already registered.')
        self.rules[rule.name] = rule
        if rule.other_names:
            for alias in rule.other_names:
                if alias in self.rules:
                    raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Rule already registered.')
                self.rules[alias] = rule

    def get_rule(self, name: str) -> Optional[Rule]:
        if not isinstance(name, str):
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Rule name must be string.')
        return self.rules.get(name)

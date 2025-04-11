from dataclasses import dataclass, field
from typing import Tuple, List, Optional, Dict, Callable

C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE = '\033[94m'
C_END = '\033[0m'


@dataclass(frozen=True, order=True)
class Rule:
    name: str
    other_names: Optional[List[str]] = field(default_factory=list)  # creates an empty list
    apply: Callable[[str, set[str], str], Optional[str]] = field(default=lambda x, y: None)

    def __post_init__(self) -> None:

        if not isinstance(self.name, str) or not self.name:
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Rule must have name as string.')

        if not isinstance(self.other_names, list) or not self.other_names:
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Rule must have other_names as tuple.')

        object.__setattr__(self, "other_names", tuple(self.other_names))

        if not callable(self.apply):
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Rule must have apply as callable.')


@dataclass(frozen=True, order=True)
class RuleRegistry:
    rules: Dict[str, Rule] = field(default_factory=dict)  # creates a empty dict

    def register_rule(self, rule: Rule) -> None:
        if rule.name in self.rules:
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Rule already registered.')

        self.rules[rule.name] = rule

        for alias in rule.other_names:
            if alias in self.rules:
                raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Rule already registered.')
            self.rules[alias] = rule

    def get_rule(self, name: str) -> Optional[Rule]:
        if not isinstance(name, str):
            raise ValueError(C_RED + f'[ERROR] ' + C_END + f'Rule name must be string.')
        return self.rules.get(name)

    def __str__(self) -> str:
        output = [C_BLUE + 'Registered rules:' + C_END + f'\n']
        printed = set()

        for rule in self.rules.values():
            if rule.name not in printed:
                aliases = ', '.join(rule.other_names) if rule.other_names else 'None'
                output.append(C_GREEN + f'    - {rule.name}' + C_END + f': {aliases}\n')
                printed.add(rule.name)

        return ''.join(output)
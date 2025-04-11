import re
from typing import Optional, Any, List
from servidor.coq.coq_ast.ast_nodes import (
    ProgramDeclaration,
    LemmaDeclaration,
    ProofDeclaration,
    ApplyRuleDeclaration,
    QuitDeclaration,
    EVarDeclaration,
    EUnOpDeclaration,
    BodyDeclaration,
    BinOpDeclaration
)

C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE = '\033[94m'
C_END = '\033[0m'


class CodeGenerator:

    def __init__(self):
        self.xml = []
        self.problem = {}
        self.knowledge_base = {}


    def visit(self, node: Any) -> Optional[str]:

        if node is None:
            return None

        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):
        raise Exception(f'No visit method for node type: {type(node).__name__}')


    def emit(self, instruction, comment=None):
        if comment:
            self.xml.append(f"\t{instruction}  //{comment}")
        else:
            self.xml.append(f"\t{instruction}")


    def generate_code(self, ast) -> str:
        self.visit(ast)
        return "\n".join(self.xml)


    def visit_ProgramDeclaration(self, node: ProgramDeclaration):

        self.emit(f'[ProgramDeclaration]', f'Starting point')
        for decl in node.declarations:
            self.visit(decl)


    def visit_ProofDeclaration(self, node: ProofDeclaration) -> Any:
        self.emit(f'\t[Visiting] ProofDeclaration')


    def visit_QuitDeclaration(self, node: QuitDeclaration) -> Any:
        self.emit('[QuitDeclaration]', f'Ending point\n')


    def visit_LemmaDeclaration(self, node: LemmaDeclaration) -> Any:
        self.emit(f'\t[Visiting] LemmaDeclaration')

        logical_expression = formula_to_string(node.body)
        logical_expression_2 = 'EBinOp(→, EVar(p1), EVar(p2))'
        self.problem['P1'] = (logical_expression, set([x for x in self.knowledge_base.keys() if x is not None]))
        self.problem['P2'] = (logical_expression_2, set([x for x in self.knowledge_base.keys() if x is not None]))
        #print(f'Self problems = {self.problem}')

        self.visit(node.body)


    def visit_BodyDeclaration(self, node: BodyDeclaration) -> Any:
        self.emit(f'\t[Visiting] BodyDeclaration')

        self.visit(node.body)


    def visit_BinOpDeclaration(self, node: BinOpDeclaration) -> Any:
        self.emit(f'\t[Visiting] BinOpDeclaration')
        self.visit(node.left)
        self.visit(node.right)


    def visit_EVarDeclaration(self, node: EVarDeclaration) -> Any:
        self.emit(f'\t[Visiting] EVarDeclaration')


    def visit_EUnOpDeclaration(self, node: EUnOpDeclaration) -> Any:
        self.emit(f'\t[Visiting] EUnOpDeclaration')
        if node.body is not None:
            self.visit(node.body)


    def visit_ApplyRuleDeclaration(self, node: ApplyRuleDeclaration):

        self.emit(f'\t[Visiting] ApplyRuleDeclaration')
        rule_name = node.name
        params = node.params

        # print(f'Function name = {rule_name}')
        # print(f'Params = {params}')

        # print(f'{self.problem}')
        if params not in self.problem.keys():
            raise ValueError(C_RED + f'No problem "{params}"' + C_END)

        self.apply_Implication_Introduction(self.problem[params][0], params)


    def apply_Implication_Introduction(
            self,
            logical_expr: str,
            problem_key: str):
        arguments = split_expression(logical_expr)

        if len(arguments) != 3 or arguments[0] != '→':
            raise ValueError('Implication introduction requires 3 arguments or symbol not →')

        antecedent, consequent = arguments[1], arguments[2]

        self.emit(f'\t\tApplying Implication Introduction on {logical_expr}')
        self.emit(f'\t\tAntecedent: {antecedent}', 'Hypothesis assumption')
        self.emit(f'\t\tConsequent: {consequent}', 'Derived conclusion')

        tmp = next((key for key, value in self.knowledge_base.items() if value == antecedent), None)

        if tmp is None:
            tmp = f'X{len(self.knowledge_base) + 1}'  # Generate new hypothesis
            self.knowledge_base[tmp] = antecedent  # Add to knowledge base

        available_hypothesis_new = self.problem[problem_key][1].copy()
        available_hypothesis_new.add(tmp)

        del self.problem[problem_key]
        new_problem_key = problem_key + '1'
        self.problem[new_problem_key] = (consequent, available_hypothesis_new)

        return consequent


# ------------------
# ------------------
# ------------------

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



def formula_to_string(node) -> str:
    if isinstance(node, EVarDeclaration):
        return f'EVar({node.name})'
    elif isinstance(node, BinOpDeclaration):
        left_str = formula_to_string(node.left)
        right_str = formula_to_string(node.right)
        return f'EBinOp({node.operation}, {left_str}, {right_str})'
    elif isinstance(node, BodyDeclaration):
        return formula_to_string(node.body)
    return ''


if __name__ == '__main__':
    appy_node_1 = ProgramDeclaration(
        declarations=[
            LemmaDeclaration(
                name='lm1',
                params=[{'var_name': 'p1'}, {'var_name': 'p2'}, {'var_name': 'p3'}],
                body=
                    BodyDeclaration(
                        body=
                            BinOpDeclaration(
                                operation='→',
                                left=
                                    BodyDeclaration(
                                        body=
                                            BinOpDeclaration(
                                                operation='→',
                                                left=
                                                    EVarDeclaration(
                                                        name='p1',
                                                        lineno=1),
                                                right=
                                                    EVarDeclaration(
                                                        name='p2',
                                                        lineno=1),
                                                lineno=0),
                                        lineno=1),
                                right=
                                    EVarDeclaration(
                                        name='p3',
                                        lineno=1),
                                lineno=0),
                        lineno=1),
                lineno=1),
            ProofDeclaration(lineno=2),
            ApplyRuleDeclaration(
                name='II',
                params='P1',
                lineno=3),
            ApplyRuleDeclaration(
                name='EI',
                params='P2',
                lineno=4),
            QuitDeclaration(
                lineno=5)],
        lineno=0)


    codegen = CodeGenerator()
    generated_code = codegen.generate_code(appy_node_1)

    print(generated_code)
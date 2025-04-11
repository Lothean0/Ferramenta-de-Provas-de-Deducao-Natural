__version__ = "2025.04.11"
__author__ = "Daniel Andrade (a100057@alunos.uminho.pt)"

C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE = '\033[94m'
C_END = '\033[0m'

try:
    from .codegen import CodeGenerator
    print(f"{__package__} package " + C_YELLOW + f"(version {__version__}) " + C_END + f"by " + C_BLUE + f"{__author__} " + C_END + f"is working.")
except ImportError as e:
    print(C_RED + f"Error importing coq_codegen package: {e}" + C_END)

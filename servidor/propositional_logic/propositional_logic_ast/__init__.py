__version__ = "2025.04.11"
__author__ = "Daniel Andrade (a100057@alunos.uminho.pt)"

from servidor.config import C_RED, C_GREEN, C_YELLOW, C_BLUE, C_END

try:
    from .ast_nodes import *
    print(f"\n{__package__} package " + C_YELLOW + f"(version {__version__}) " + C_END + f"is working.")
except ImportError as e:
    print(C_RED + f"Error importing coq_codegen package: {e}" + C_END)

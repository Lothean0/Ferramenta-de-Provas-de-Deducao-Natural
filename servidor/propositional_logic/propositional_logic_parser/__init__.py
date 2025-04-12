__version__ = "2025.04.11"
__author__ = "Daniel Andrade (a100057@alunos.uminho.pt)"

from config import C_RED, C_GREEN, C_YELLOW, C_BLUE, C_END

try:
    from .lexer import Lexer, tokens
    from .parser import Parser
    print(f"{__package__} package " + C_YELLOW + f"(version {__version__}) " + C_END + f"is working.")
except ImportError as e:
    print(f"Error importing coq_codegen package: {e}")

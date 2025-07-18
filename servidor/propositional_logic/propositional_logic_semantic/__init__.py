__version__ = "2025.04.11"

from servidor.config import C_YELLOW, C_END

try:
    from .semantic_analyzer import SemanticError, SemanticAnalyzer
    from .symbol_table import SymbolTable
    print(f"{__package__} package " + C_YELLOW + f"(version {__version__}) " + C_END + f"is working.")
except ImportError as e:
    print(f"Error importing coq_codegen package: {e}")

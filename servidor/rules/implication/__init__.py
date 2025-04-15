__version__ = "2025.04.12"

from servidor.config import knowledge_base, problems, n_hypothesis, C_RED, C_GREEN, C_YELLOW, C_BLUE, C_END

try:
    from .introduction import apply_implication_introduction, n_hypothesis, knowledge_base
    print(f"\n{__package__} package " + C_YELLOW + f"(version {__version__}) " + C_END + f"is working.")
except ImportError as e:
    print(C_RED + f"Error importing coq_codegen package: {e}" + C_END)

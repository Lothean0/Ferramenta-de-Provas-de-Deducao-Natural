__version__ = "2025.04.25"

from servidor.config import C_RED, C_YELLOW, C_END

try:
    from .introduction import apply_disjunction_introduction_1, apply_disjunction_introduction_2
    from .elimination import apply_disjunction_elimination
    print(f"\n{__package__} package " + C_YELLOW + f"(version {__version__}) " + C_END + f"is working.")
except ImportError as e:
    print(C_RED + f"Error importing coq_codegen package: {e}" + C_END)

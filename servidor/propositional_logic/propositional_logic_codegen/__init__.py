__version__ = "2025.04.11"

from servidor.config import C_RED, C_YELLOW, C_END

try:
    from .codegen import CodeGenerator
    print(f"{__package__} package " + C_YELLOW + f"(version {__version__}) " + C_END + f"is working.")
except ImportError as e:
    print(C_RED + f"Error importing coq_codegen package: {e}" + C_END)

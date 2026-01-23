"""Formula validation for Obsidian Bases."""

from typing import Any, List
from config import ValidationConfig


class FormulaValidator:
    """Validates formula sections in base files."""
    
    def __init__(self, config: ValidationConfig):
        self.config = config
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self, formulas: Any) -> None:
        """Validate formulas section."""
        if formulas is None:
            return
        
        if not isinstance(formulas, dict):
            self.errors.append(
                f"Formulas must be an object (dictionary). Current type: {type(formulas).__name__}. "
                f"Example:\n  formulas:\n    my_formula: 'if(property, \"Yes\", \"No\")'"
            )
            return
        
        for name, formula in formulas.items():
            self._validate_formula(name, formula)
    
    def _validate_formula(self, name: str, formula: Any) -> None:
        """Validate a single formula."""
        if not isinstance(name, str):
            self.errors.append(
                f"Formula name must be a string. Found: {name} ({type(name).__name__})"
            )
        
        if not isinstance(formula, str):
            self.errors.append(
                f"Formula '{name}' must be a string expression. "
                f"Current type: {type(formula).__name__}. "
                f"Example: '{name}': 'file.mtime.relative()'"
            )
        elif formula.strip() == '':
            self.warnings.append(
                f"Formula '{name}' is an empty string. "
                f"This formula will not compute any value."
            )

"""Filter validation for Obsidian Bases."""

from typing import Any, List
from config import ValidationConfig


class FilterValidator:
    """Validates filter sections in base files."""
    
    def __init__(self, config: ValidationConfig):
        self.config = config
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self, filters: Any) -> None:
        """Validate filters section."""
        if filters is None:
            return
        
        if isinstance(filters, str):
            self._validate_filter_string(filters)
        elif isinstance(filters, dict):
            self._validate_filter_object(filters)
        else:
            self.errors.append(
                f"Filters must be a string or object. Current type: {type(filters).__name__}. "
                f"Valid formats:\n"
                f"  1. String: filters: 'property == \"value\"'\n"
                f"  2. Object: filters:\n    and:\n      - 'condition1'\n      - 'condition2'"
            )
    
    def _validate_filter_string(self, filter_str: str) -> None:
        """Validate single filter string."""
        if not filter_str.strip():
            self.warnings.append(
                "Empty filter string found. "
                "Consider removing or using a meaningful filter expression."
            )
    
    def _validate_filter_object(self, filters: dict) -> None:
        """Validate filter object with and/or/not."""
        valid_keys = {'and', 'or', 'not'}
        
        for key in filters:
            if key not in valid_keys:
                self.errors.append(
                    f"Invalid filter key: '{key}'. "
                    f"Valid keys are: {', '.join(sorted(valid_keys))}. "
                    f"Example: filters:\n  and:\n    - 'property == \"value\"'\n    - file.hasTag(\"tag\")"
                )
            
            if not isinstance(filters[key], list):
                self.errors.append(
                    f"Filter '{key}' must be a list of conditions. "
                    f"Current type: {type(filters[key]).__name__}. "
                    f"Example: {key}:\n  - 'status == \"active\"'\n  - 'priority > 2'"
                )
            elif len(filters[key]) == 0:
                self.warnings.append(
                    f"Filter '{key}' has empty list. "
                    f"This filter will have no effect."
                )

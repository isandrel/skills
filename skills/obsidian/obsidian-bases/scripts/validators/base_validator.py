"""Main base file validator orchestrating all specialized validators."""

import yaml
from pathlib import Path
from typing import Dict, List, Optional

from config import ValidationConfig
from .filter_validator import FilterValidator
from .formula_validator import FormulaValidator
from .property_validator import PropertyValidator
from .view_validator import ViewValidator


class BaseValidator:
    """Orchestrates validation of entire base files using specialized validators."""
    
    def __init__(self, file_path: str, config: ValidationConfig):
        self.file_path = Path(file_path)
        self.config = config
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self) -> bool:
        """
        Validate the base file.
        
        Returns:
            True if valid, False otherwise
        """
        if not self.file_path.exists():
            self.errors.append(f"File not found: {self.file_path}")
            return False
        
        try:
            content = self._read_file()
            data = self._parse_yaml(content)
            
            if data is None:
                return False
            
            if not isinstance(data, dict):
                self.errors.append("Base file must be a YAML object (dictionary)")
                return False
            
            # Use specialized validators
            self._validate_with_validators(data)
            
            return len(self.errors) == 0
            
        except Exception as e:
            self.errors.append(f"Unexpected error: {e}")
            return False
    
    def _read_file(self) -> str:
        """Read file contents."""
        with open(self.file_path, 'r') as f:
            return f.read()
    
    def _parse_yaml(self, content: str) -> Optional[Dict]:
        """Parse YAML content."""
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error: {e}")
            return None
    
    def _validate_with_validators(self, data: Dict) -> None:
        """Use specialized validators for each section."""
        # Validate filters
        filter_validator = FilterValidator(self.config)
        filter_validator.validate(data.get('filters'))
        self.errors.extend(filter_validator.errors)
        self.warnings.extend(filter_validator.warnings)
        
        # Validate formulas
        formula_validator = FormulaValidator(self.config)
        formula_validator.validate(data.get('formulas'))
        self.errors.extend(formula_validator.errors)
        self.warnings.extend(formula_validator.warnings)
        
        # Validate properties
        property_validator = PropertyValidator(self.config)
        property_validator.validate(data.get('properties'))
        self.errors.extend(property_validator.errors)
        self.warnings.extend(property_validator.warnings)
        
        # Validate summaries (simple validation)
        self._validate_summaries(data.get('summaries'))
        
        # Validate views
        view_validator = ViewValidator(self.config)
        view_validator.validate(data.get('views'))
        self.errors.extend(view_validator.errors)
        self.warnings.extend(view_validator.warnings)
    
    def _validate_summaries(self, summaries) -> None:
        """Validate summaries section (simple check)."""
        if summaries is None:
            return
        
        if not isinstance(summaries, dict):
            self.errors.append(
                f"Summaries must be an object (dictionary). Current type: {type(summaries).__name__}. "
                f"Example:\n  summaries:\n    avgValue: 'values.mean().round(2)'"
            )
    
    def print_results(self) -> None:
        """Print validation results with colored output."""
        if self.errors:
            print(f"\n❌ Validation FAILED for {self.file_path}")
            print(f"\nErrors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if not self.errors and not self.warnings:
            print(f"\n✅ Validation PASSED for {self.file_path}")

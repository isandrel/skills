"""View validation for Obsidian Bases."""

from typing import Any, List
from config import ValidationConfig


class ViewValidator:
    """Validates view sections in base files."""
    
    def __init__(self, config: ValidationConfig):
        self.config = config
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self, views: Any) -> None:
        """Validate views section."""
        if views is None:
            if self.config.require_views:
                self.errors.append("Base file must have at least one view")
            return
        
        if not isinstance(views, list):
            self.errors.append("Views must be a list")
            return
        
        if len(views) == 0 and self.config.require_views:
            self.errors.append("Base file must have at least one view")
        
        for i, view in enumerate(views):
            self._validate_view(view, i)
    
    def _validate_view(self, view: Any, index: int) -> None:
        """Validate a single view."""
        if not isinstance(view, dict):
            self.errors.append(f"View {index} must be an object")
            return
        
        # Check required fields
        if self.config.require_view_type and 'type' not in view:
            self.errors.append(f"View {index} missing required 'type' field")
        elif 'type' in view and view['type'] not in self.config.valid_view_types:
            self.errors.append(
                f"View {index} has invalid type '{view['type']}'. "
                f"Must be one of: {', '.join(self.config.valid_view_types)}"
            )
        
        if self.config.require_view_name and 'name' not in view:
            self.errors.append(f"View {index} missing required 'name' field")
        
        # Check for unknown fields
        if not self.config.allow_unknown_view_fields:
            unknown = set(view.keys()) - self.config.known_view_fields
            if unknown:
                self.warnings.append(
                    f"View {index} has unknown fields: {', '.join(unknown)}. "
                    f"Known fields: {', '.join(sorted(self.config.known_view_fields))}"
                )

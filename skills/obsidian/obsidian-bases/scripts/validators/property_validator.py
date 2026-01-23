"""Property validation for Obsidian Bases."""

from typing import Any, List
from config import ValidationConfig


class PropertyValidator:
    """Validates property sections in base files."""
    
    def __init__(self, config: ValidationConfig):
        self.config = config
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self, properties: Any) -> None:
        """Validate properties section."""
        if properties is None:
            return
        
        if not isinstance(properties, dict):
            self.errors.append(
                f"Properties must be an object (dictionary). Current type: {type(properties).__name__}. "
                f"Example:\n  properties:\n    property_name:\n      displayName: \"Display Name\""
            )
            return
        
        for prop_name, config in properties.items():
            self._validate_property(prop_name, config)
    
    def _validate_property(self, prop_name: str, config: Any) -> None:
        """Validate a single property configuration."""
        if not isinstance(config, dict):
            self.errors.append(
                f"Property '{prop_name}' config must be an object. "
                f"Current type: {type(config).__name__}. "
                f"Example: {prop_name}:\n  displayName: \"My Property\""
            )
            return
        
        if self.config.warn_missing_display_name and 'displayName' not in config:
            self.warnings.append(
                f"Property '{prop_name}' missing 'displayName'. "
                f"Add: displayName: \"Human Readable Name\""
            )
        
        # Check for unknown keys (if strict mode enabled)
        if not self.config.allow_unknown_property_fields:
            unknown = set(config.keys()) - self.config.known_property_fields
            if unknown:
                self.warnings.append(
                    f"Property '{prop_name}' has unknown keys: {', '.join(unknown)}. "
                    f"Known keys: {', '.join(self.config.known_property_fields)}"
                )

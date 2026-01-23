"""
Validate Obsidian Base (.base) files.

This is the main entry point for validation.
The validation logic is organized into specialized modules for maintainability.

Usage:
    python validate.py <file.base>
"""

import sys
from pathlib import Path

from config import ValidationConfig
from validators import BaseValidator


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  python {Path(__file__).name} <file.base>")
        print("\nValidates Obsidian Base (.base) files for:")
        print("  - YAML syntax")
        print("  - Required fields (views, type, name)")
        print("  - Valid view types (table, cards, list, map)")
        print("  - Filter structure and operators")
        print("  - Formula and property syntax")
        print("  - All Bases syntax from references/")
        print("\nCustomization:")
        print("  Edit validate.toml to customize validation rules")
        print("\nModular Structure:")
        print("  config.py - Configuration loading")
        print("  validators/ - Specialized validators")
        sys.exit(1)
    
    # Load config from TOML file
    config_path = Path(__file__).parent / "validate.toml"
    config = ValidationConfig.load_from_toml(config_path)
    
    # Create validator with loaded config
    validator = BaseValidator(sys.argv[1], config)
    is_valid = validator.validate()
    validator.print_results()
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()

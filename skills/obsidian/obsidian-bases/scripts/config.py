"""Configuration management for Obsidian Bases validation."""

import sys
from pathlib import Path
from typing import Set
from dataclasses import dataclass

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Fallback for Python < 3.11
    except ImportError:
        tomllib = None


@dataclass
class ValidationConfig:
    """Configuration for base file validation. All values loaded from TOML."""
    
    # Valid view types
    valid_view_types: Set[str]
    
    # Valid sort directions
    valid_directions: Set[str]
    
    # Valid built-in summary functions
    valid_summaries: Set[str]
    
    # Known property fields
    known_property_fields: Set[str]
    
    # Known view fields
    known_view_fields: Set[str]
    
    # Filter operators
    comparison_operators: Set[str]
    logical_operators: Set[str]
    
    # File functions
    valid_file_functions: Set[str]
    
    # Formula functions (from references/formulas.md)
    global_functions: Set[str]
    date_functions: Set[str]
    string_functions: Set[str]
    number_functions: Set[str]
    list_functions: Set[str]
    type_functions: Set[str]
    
    # File properties (from references/properties.md)
    file_properties: Set[str]
    
    # Validation strictness
    require_views: bool
    require_view_name: bool
    require_view_type: bool
    warn_missing_display_name: bool
    allow_unknown_view_fields: bool
    allow_unknown_property_fields: bool
    
    @classmethod
    def load_from_toml(cls, toml_path: Path) -> 'ValidationConfig':
        """
        Load configuration from TOML file.
        
        Args:
            toml_path: Path to TOML configuration file
            
        Returns:
            ValidationConfig instance
            
        Raises:
            SystemExit: If TOML file is missing or invalid
        """
        if not tomllib:
            print("Error: TOML support not available.")
            print("Install tomli: pip install tomli")
            sys.exit(1)
        
        if not toml_path.exists():
            print(f"Error: Configuration file not found: {toml_path}")
            print("The validate.toml file is required for validation.")
            sys.exit(1)
        
        try:
            with open(toml_path, 'rb') as f:
                config_data = tomllib.load(f)
            
            # Extract all configuration values (no defaults!)
            validation = config_data['validation']
            view_types_cfg = config_data['view_types']
            sort_cfg = config_data['sort']
            summaries_cfg = config_data['summaries']
            property_fields_cfg = config_data['property_fields']
            view_fields_cfg = config_data['view_fields']
            filter_ops_cfg = config_data['filter_operators']
            file_funcs_cfg = config_data['file_functions']
            formula_funcs_cfg = config_data['formula_functions']
            file_props_cfg = config_data['file_properties']
            
            return cls(
                # View configuration
                valid_view_types=set(view_types_cfg['valid']),
                valid_directions=set(sort_cfg['directions']),
                valid_summaries=set(summaries_cfg['built_in']),
                known_property_fields=set(property_fields_cfg['known']),
                known_view_fields=set(view_fields_cfg['known']),
                
                # Filter configuration
                comparison_operators=set(filter_ops_cfg['comparison']),
                logical_operators=set(filter_ops_cfg['logical']),
                valid_file_functions=set(file_funcs_cfg['valid']),
                
                # Formula configuration
                global_functions=set(formula_funcs_cfg['global']),
                date_functions=set(formula_funcs_cfg['date']),
                string_functions=set(formula_funcs_cfg['string']),
                number_functions=set(formula_funcs_cfg['number']),
                list_functions=set(formula_funcs_cfg['list']),
                type_functions=set(formula_funcs_cfg['type']),
                
                # Property configuration
                file_properties=set(file_props_cfg['basic'] + file_props_cfg['timestamps'] + 
                                  file_props_cfg['size'] + file_props_cfg['links']),
                
                # Validation strictness
                require_views=validation['require_views'],
                require_view_name=validation['require_view_name'],
                require_view_type=validation['require_view_type'],
                warn_missing_display_name=validation['warn_missing_display_name'],
                allow_unknown_view_fields=validation['allow_unknown_view_fields'],
                allow_unknown_property_fields=validation['allow_unknown_property_fields']
            )
        except KeyError as e:
            print(f"Error: Missing required key in {toml_path}: {e}")
            print("Check validate.toml for missing configuration values.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: Failed to load configuration from {toml_path}: {e}")
            sys.exit(1)

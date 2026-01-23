"""
Shared configuration models for skill-creator scripts

Uses Pydantic for type-safe configuration and validation.
"""

from typing import Set, Optional
from pathlib import Path
from pydantic import BaseModel, Field, field_validator


class AuthorConfig(BaseModel):
    """Author information configuration"""
    name: str = Field(default="isandrel", description="Default author name")
    email: str = Field(default="", description="Optional author email")


class DefaultsConfig(BaseModel):
    """Default values for new skills"""
    category: str = Field(default="development", description="Default skill category")
    version: str = Field(default="0.0.1", description="Default starting version")


class ValidationRules(BaseModel):
    """Validation rules for skill structure"""
    # Naming rules
    min_name_length: int = Field(default=1, ge=1)
    max_name_length: int = Field(default=64, le=256)
    allow_uppercase: bool = Field(default=False)
    allow_underscores: bool = Field(default=False)
    
    # Description rules
    require_description: bool = Field(default=True)
    min_description_length: int = Field(default=50, ge=0)
    max_description_length: int = Field(default=1024, le=10000)
    
    # Frontmatter rules
    allowed_properties: Set[str] = Field(
        default={"name", "description", "license", "allowed-tools", "metadata"}
    )


class PackagingConfig(BaseModel):
    """Packaging configuration"""
    output_dir: str = Field(default="dist", description="Output directory for .skill files")
    compression_level: int = Field(default=9, ge=0, le=9, description="ZIP compression level")
    include_dotfiles: bool = Field(default=False, description="Include hidden files")
    exclude_patterns: list[str] = Field(
        default_factory=lambda: [".DS_Store", "__pycache__", "*.pyc", ".git", ".venv"]
    )


class DirectoriesConfig(BaseModel):
    """Directory creation settings"""
    create_scripts: bool = Field(default=True, description="Create scripts/ directory")
    create_references: bool = Field(default=True, description="Create references/ directory")
    create_assets: bool = Field(default=True, description="Create assets/ directory")


class TemplatesConfig(BaseModel):
    """Template file paths"""
    skill_template: str = Field(
        default="templates/skill.template.md",
        description="Path to SKILL.md template"
    )
    readme_template: str = Field(
        default="templates/readme.template.md",
        description="Path to README.md template"
    )
    example_script_template: str = Field(
        default="templates/example_script.template.py",
        description="Path to example script template"
    )
    example_reference_template: str = Field(
        default="templates/example_reference.template.md",
        description="Path to example reference template"
    )
    example_asset_template: str = Field(
        default="templates/example_asset.template.txt",
        description="Path to example asset template"
    )


class SkillCreatorConfig(BaseModel):
    """Complete skill-creator configuration"""
    author: AuthorConfig = Field(default_factory=AuthorConfig)
    defaults: DefaultsConfig = Field(default_factory=DefaultsConfig)
    validation: ValidationRules = Field(default_factory=ValidationRules)
    packaging: PackagingConfig = Field(default_factory=PackagingConfig)
    directories: DirectoriesConfig = Field(default_factory=DirectoriesConfig)
    templates: TemplatesConfig = Field(default_factory=TemplatesConfig)
    
    @classmethod
    def from_toml(cls, config_path: Path) -> "SkillCreatorConfig":
        """Load configuration from TOML file"""
        try:
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib
            
            with open(config_path, 'rb') as f:
                toml_data = tomllib.load(f)
                return cls(**toml_data)
        except Exception as e:
            print(f"⚠️  Warning: Could not load config.toml: {e}")
            return cls()  # Return default config


class SkillMetadata(BaseModel):
    """Skill metadata from frontmatter"""
    name: str
    description: str
    license: Optional[str] = None
    metadata: Optional[dict] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate skill name format"""
        if not v:
            raise ValueError("Skill name cannot be empty")
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Validate description format"""
        if not v:
            raise ValueError("Description cannot be empty")
        return v.strip()

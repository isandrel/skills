"""
Skill Validation Tool

Validates skill structure, naming conventions, and content quality.
Uses Pydantic for type-safe configuration and Typer for modern CLI.
"""

import sys
from pathlib import Path
from typing import Tuple, Optional
import re

# ============================================================================
# PREREQUISITE CHECKS
# ============================================================================

def check_prerequisites() -> Tuple[bool, str]:
    """Check if all required dependencies are installed"""
    missing = []
    
    try:
        import yaml
    except ImportError:
        missing.append("pyyaml")
    
    try:
        from rich.console import Console
    except ImportError:
        missing.append("rich")
    
    try:
        from pydantic import BaseModel
    except ImportError:
        missing.append("pydantic")
    
    try:
        import typer
    except ImportError:
        missing.append("typer")
    
    if missing:
        deps = " ".join(missing)
        return False, f"Missing dependencies: {deps}\n💡 Install with: pip install {deps}"
    
    return True, "All dependencies available"


# Check prerequisites first
prereq_ok, prereq_msg = check_prerequisites()
if not prereq_ok:
    print(f"❌ {prereq_msg}")
    sys.exit(1)

# Now import the rest after prerequisite check
import yaml
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing_extensions import Annotated

# Import Pydantic models
try:
    from config_models import SkillCreatorConfig, SkillMetadata
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from config_models import SkillCreatorConfig, SkillMetadata

console = Console()
app = typer.Typer(help="🔍 Skill Validation Tool - Validates skill structure and content")

# ============================================================================
# CONFIGURATION
# ============================================================================

def load_config() -> SkillCreatorConfig:
    """Load configuration from config.toml using Pydantic"""
    script_dir = Path(__file__).parent
    config_path = script_dir.parent / "config.toml"
    
    if config_path.exists():
        return SkillCreatorConfig.from_toml(config_path)
    else:
        console.print("⚠️  [yellow]Warning:[/yellow] config.toml not found, using defaults")
        return SkillCreatorConfig()


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_skill_structure(skill_path: Path) -> Tuple[bool, str]:
    """Validate basic skill directory structure"""
    if not skill_path.exists():
        return False, f"Skill directory not found: {skill_path}"
    
    if not skill_path.is_dir():
        return False, f"Path is not a directory: {skill_path}"
    
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"
    
    return True, "Skill structure OK"


def validate_frontmatter(content: str, config: SkillCreatorConfig) -> Tuple[bool, str, Optional[dict]]:
    """Validate YAML frontmatter"""
    if not content.startswith("---"):
        return False, "No YAML frontmatter found", None
    
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format", None
    
    frontmatter_text = match.group(1)
    
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary", None
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}", None
    
    # Check for unexpected properties
    unexpected = set(frontmatter.keys()) - config.validation.allowed_properties
    if unexpected:
        return False, (
            f"Unexpected frontmatter keys: {', '.join(sorted(unexpected))}\n"
            f"   Allowed: {', '.join(sorted(config.validation.allowed_properties))}"
        ), None
    
    # Check required fields
    if "name" not in frontmatter:
        return False, "Missing 'name' field in frontmatter", None
    if config.validation.require_description and "description" not in frontmatter:
        return False, "Missing 'description' field in frontmatter", None
    
    return True, "Frontmatter structure OK", frontmatter


def validate_skill_name(name: str, config: SkillCreatorConfig) -> Tuple[bool, str]:
    """Validate skill name against rules"""
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    
    name = name.strip()
    rules = config.validation
    
    # Check length
    if len(name) < rules.min_name_length:
        return False, f"Name too short ({len(name)} chars, min: {rules.min_name_length})"
    if len(name) > rules.max_name_length:
        return False, f"Name too long ({len(name)} chars, max: {rules.max_name_length})"
    
    # Check naming convention
    pattern = r"^[a-z0-9-"
    if rules.allow_uppercase:
        pattern = r"^[a-zA-Z0-9-"
    if rules.allow_underscores:
        pattern += "_"
    pattern += "]+$"
    
    if not re.match(pattern, name):
        chars_allowed = "lowercase letters, digits, and hyphens"
        if rules.allow_uppercase:
            chars_allowed = "letters, digits, and hyphens"
        if rules.allow_underscores:
            chars_allowed += " and underscores"
        return False, f"Name '{name}' should use {chars_allowed} only"
    
    # Check for invalid hyphen patterns
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, f"Name '{name}' has invalid hyphen pattern"
    
    return True, f"Name '{name}' is valid"


def validate_description(description: str, config: SkillCreatorConfig) -> Tuple[bool, str]:
    """Validate skill description"""
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    
    description = description.strip()
    rules = config.validation
    
    # Check for angle brackets
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"
    
    # Check length
    if len(description) < rules.min_description_length:
        return False, (
            f"Description too short ({len(description)} chars)\n"
            f"   Minimum: {rules.min_description_length} chars"
        )
    if len(description) > rules.max_description_length:
        return False, (
            f"Description too long ({len(description)} chars)\n"
            f"   Maximum: {rules.max_description_length} chars"
        )
    
    return True, f"Description OK ({len(description)} chars)"


def validate_skill(skill_path: Path, config: Optional[SkillCreatorConfig] = None) -> Tuple[bool, str]:
    """
    Main validation function
    
    Args:
        skill_path: Path to the skill directory
        config: Optional configuration (loads from config.toml if None)
    
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if config is None:
        config = load_config()
    
    # Create results table
    table = Table(title="🔍 Skill Validation Results", show_header=True)
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details", style="dim")
    
    all_valid = True
    
    # 1. Validate structure
    valid, msg = validate_skill_structure(skill_path)
    status = "✅" if valid else "❌"
    table.add_row("Structure", status, msg)
    if not valid:
        console.print(table)
        return False, msg
    
    # Read SKILL.md
    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text()
    
    # 2. Validate frontmatter
    valid, msg, frontmatter = validate_frontmatter(content, config)
    status = "✅" if valid else "❌"
    table.add_row("Frontmatter", status, msg)
    if not valid:
        console.print(table)
        return False, msg
    
    # 3. Validate name
    name = frontmatter.get("name", "")
    valid, msg = validate_skill_name(name, config)
    status = "✅" if valid else "❌"
    table.add_row("Skill Name", status, msg)
    all_valid = all_valid and valid
    
    # 4. Validate description
    description = frontmatter.get("description", "")
    valid, msg = validate_description(description, config)
    status = "✅" if valid else "❌"
    table.add_row("Description", status, msg)
    all_valid = all_valid and valid
    
    # Print results
    console.print(table)
    
    if all_valid:
        console.print("\n🎉 [bold green]Skill is valid![/bold green]")
        return True, "Skill is valid!"
    else:
        console.print("\n❌ [bold red]Skill validation failed[/bold red]")
        return False, "Skill has validation errors"


# ============================================================================
# CLI INTERFACE
# ============================================================================

@app.command()
def main(
    skill_path: Annotated[Path, typer.Argument(help="Path to the skill directory to validate")],
):
    """
    Validate a skill's structure and content.
    
    Checks SKILL.md frontmatter, naming conventions, and content requirements.
    """
    console.print(f"\n🔍 [bold]Validating skill:[/bold] {skill_path}\n")
    
    valid, message = validate_skill(skill_path)
    
    if valid:
        raise typer.Exit(0)
    else:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

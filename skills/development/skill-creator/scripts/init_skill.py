"""
Skill Initializer - Creates a new skill from template

Generates a skill directory with SKILL.md and example resource files.
Loads configuration from config.toml for customization.

Uses Pydantic for type-safe configuration and Typer for modern CLI.
"""

import sys
from pathlib import Path
from typing import Optional, Tuple

# ============================================================================
# PREREQUISITE CHECKS
# ============================================================================

def check_prerequisites() -> Tuple[bool, str]:
    """Check if all required dependencies are installed"""
    missing = []
    
    try:
        from pydantic import BaseModel
    except ImportError:
        missing.append("pydantic")
    
    try:
        import typer
    except ImportError:
        missing.append("typer")
    
    try:
        from rich.console import Console
    except ImportError:
        missing.append("rich")
    
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
try:
    from config_models import SkillCreatorConfig
    import typer
    from rich.console import Console
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from config_models import SkillCreatorConfig
    import typer
    from rich.console import Console

from typing_extensions import Annotated

console = Console()
app = typer.Typer(help="🚀 Skill Initializer - Creates new skills from templates")


def load_config() -> SkillCreatorConfig:
    """Load configuration from config.toml using Pydantic"""
    script_dir = Path(__file__).parent
    config_path = script_dir.parent / "config.toml"
    
    if config_path.exists():
        return SkillCreatorConfig.from_toml(config_path)
    else:
        console.print("⚠️  [yellow]Warning:[/yellow] config.toml not found, using defaults")
        return SkillCreatorConfig()


def load_template(template_path: str) -> str:
    """Load a template file from disk"""
    try:
        script_dir = Path(__file__).parent
        skill_creator_root = script_dir.parent
        full_path = skill_creator_root / template_path
        
        if full_path.exists():
            return full_path.read_text()
        else:
            console.print(f"⚠️  [yellow]Warning:[/yellow] Template not found: {full_path}")
            return ""
    except Exception as e:
        console.print(f"⚠️  [yellow]Warning:[/yellow] Could not load template {template_path}: {e}")
        return ""


def title_case_skill_name(skill_name: str) -> str:
    """Convert hyphenated skill name to Title Case for display"""
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def init_skill(
    skill_name: str,
    path: Path,
    category: Optional[str] = None,
    author: Optional[str] = None,
    config: Optional[SkillCreatorConfig] = None
) -> Optional[Path]:
    """
    Initialize a new skill directory with template files

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created
        category: Optional category (overrides config default)
        author: Optional author name (overrides config default)
        config: Optional configuration (loads from config.toml if None)

    Returns:
        Path to created skill directory, or None if error
    """
    if config is None:
        config = load_config()
    
    # Use provided values or fall back to config defaults
    if category is None:
        category = config.defaults.category
    if author is None:
        author = config.author.name
    
    # Determine skill directory path
    skill_dir = path.resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        console.print(f"❌ [bold red]Error:[/bold red] Skill directory already exists: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        console.print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        console.print(f"❌ [bold red]Error creating directory:[/bold red] {e}")
        return None

    # Load and create SKILL.md from template
    skill_title = title_case_skill_name(skill_name)
    skill_template_content = load_template(config.templates.skill_template)
    
    if not skill_template_content:
        console.print("❌ [bold red]Error:[/bold red] Could not load SKILL.md template")
        return None
    
    skill_content = skill_template_content.format(
        skill_name=skill_name,
        skill_title=skill_title,
        category=category,
        author=author,
        version=config.defaults.version
    )

    skill_md_path = skill_dir / "SKILL.md"
    try:
        skill_md_path.write_text(skill_content)
        console.print("✅ Created SKILL.md")
    except Exception as e:
        console.print(f"❌ [bold red]Error creating SKILL.md:[/bold red] {e}")
        return None

    # Load and create README.md from template
    readme_template_content = load_template(config.templates.readme_template)
    
    if not readme_template_content:
        console.print("❌ [bold red]Error:[/bold red] Could not load README.md template")
        return None
    
    readme_content = readme_template_content.format(skill_title=skill_title, skill_name=skill_name)
    readme_path = skill_dir / "README.md"
    try:
        readme_path.write_text(readme_content)
        console.print("✅ Created README.md")
    except Exception as e:
        console.print(f"❌ [bold red]Error creating README.md:[/bold red] {e}")
        return None

    # Create resource directories based on config
    try:
        if config.directories.create_scripts:
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir(exist_ok=True)
            
            # Load and create example script
            script_template = load_template(config.templates.example_script_template)
            if script_template:
                example_script = scripts_dir / "example.py"
                example_script.write_text(script_template.format(skill_name=skill_name))
                example_script.chmod(0o755)
                console.print("✅ Created scripts/example.py")

        if config.directories.create_references:
            references_dir = skill_dir / "references"
            references_dir.mkdir(exist_ok=True)
            
            # Load and create example reference
            reference_template = load_template(config.templates.example_reference_template)
            if reference_template:
                example_reference = references_dir / "api_reference.md"
                example_reference.write_text(reference_template.format(skill_title=skill_title))
                console.print("✅ Created references/api_reference.md")

        if config.directories.create_assets:
            assets_dir = skill_dir / "assets"
            assets_dir.mkdir(exist_ok=True)
            
            # Load and create example asset
            asset_template = load_template(config.templates.example_asset_template)
            if asset_template:
                example_asset = assets_dir / "example_asset.txt"
                example_asset.write_text(asset_template)
                console.print("✅ Created assets/example_asset.txt")
                
    except Exception as e:
        console.print(f"❌ [bold red]Error creating resource directories:[/bold red] {e}")
        return None

    # Print next steps
    console.print(f"\n✅ [bold green]Skill '{skill_name}' initialized successfully[/bold green] at {skill_dir}")
    console.print("\n📝 [bold]Generated files:[/bold]")
    console.print("   • SKILL.md - Skill definition for AI agents")
    console.print("   • README.md - Documentation for humans")
    if config.directories.create_scripts:
        console.print("   • scripts/ - Example executable scripts")
    if config.directories.create_references:
        console.print("   • references/ - Example reference documentation")
    if config.directories.create_assets:
        console.print("   • assets/ - Example asset files")
    console.print("\n[bold]Next steps:[/bold]")
    console.print("1. Edit SKILL.md and README.md to complete the TODO items")
    console.print("2. Customize or delete the example files in resource directories")
    console.print("3. Run validate.py when ready to check the skill structure")

    return skill_dir


@app.command()
def main(
    skill_name: Annotated[str, typer.Argument(help="Name of the skill (hyphen-case, e.g., 'my-skill')")],
    path: Annotated[Path, typer.Option("--path", "-p", help="Directory where skill should be created")] = Path("."),
    category: Annotated[Optional[str], typer.Option("--category", "-c", help="Skill category")] = None,
    author: Annotated[Optional[str], typer.Option("--author", "-a", help="Author name")] = None,
):
    """
    Initialize a new skill with template files.
    
    Creates a skill directory with SKILL.md, README.md, and example resource files.
    Configuration loaded from config.toml (or defaults if not found).
    
    Skill name requirements:
     • Hyphen-case identifier (e.g., 'data-analyzer')
     • Lowercase letters, digits, and hyphens only
     • Max 64 characters
    """
    console.print(f"\n🚀 [bold cyan]Initializing skill:[/bold cyan] {skill_name}")
    console.print(f"   Location: {path}")
    if category:
        console.print(f"   Category: {category}")
    if author:
        console.print(f"   Author: {author}")
    console.print()

    result = init_skill(skill_name, path, category, author)

    if result:
        console.print()
        raise typer.Exit(0)
    else:
        console.print()
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

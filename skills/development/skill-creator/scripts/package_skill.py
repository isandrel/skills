"""
Skill Packager - Creates distributable .skill files

Validates skill structure and packages into a ZIP archive for distribution.
Uses Pydantic for type-safe configuration and Typer for modern CLI.
"""

import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from typing import List, Optional, Tuple
import fnmatch

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

# Import validate module
try:
    from validate import validate_skill
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from validate import validate_skill

from typing_extensions import Annotated

console = Console()
app = typer.Typer(help="📦 Skill Packager - Creates distributable .skill files")


def load_config() -> SkillCreatorConfig:
    """Load configuration from config.toml using Pydantic"""
    script_dir = Path(__file__).parent
    config_path = script_dir.parent / "config.toml"
    
    if config_path.exists():
        return SkillCreatorConfig.from_toml(config_path)
    else:
        console.print("⚠️  [yellow]Warning:[/yellow] config.toml not found, using defaults")
        return SkillCreatorConfig()


def should_exclude(file_path: Path, base_path: Path, patterns: List[str], include_dotfiles: bool = False) -> bool:
    """Check if file should be excluded from packaging"""
    relative_path = file_path.relative_to(base_path)
    
    # Exclude dotfiles unless explicitly included
    if not include_dotfiles:
        for part in relative_path.parts:
            if part.startswith('.'):
                return True
    
    # Check against exclusion patterns
    path_str = str(relative_path)
    for pattern in patterns:
        if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(file_path.name, pattern):
            return True
    
    return False


def package_skill(
    skill_path: Path,
    output_dir: Optional[Path] = None,
    config: Optional[SkillCreatorConfig] = None,
    skip_validation: bool = False
) -> Optional[Path]:
    """
    Package a skill into a .skill file (ZIP archive)
    
    Args:
        skill_path: Path to the skill directory
        output_dir: Optional output directory (uses config default if None)
        config: Optional configuration (loads from config.toml if None)
        skip_validation: Skip validation step
    
    Returns:
        Path to created .skill file, or None if error
    """
    if config is None:
        config = load_config()
    
    skill_path = skill_path.resolve()
    
    # Validate first (unless skipped)
    if not skip_validation:
        console.print("🔍 [bold]Step 1:[/bold] Validating skill...\n")
        valid, msg = validate_skill(skill_path, config)
        if not valid:
            console.print(f"\n❌ [bold red]Validation failed:[/bold red] {msg}")
            console.print("💡 Fix validation errors before packaging")
            return None
        console.print()
    
    # Determine output directory
    if output_dir is None:
        output_dir = skill_path.parent / config.packaging.output_dir
    
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create .skill filename
    skill_name = skill_path.name
    skill_file = output_dir / f"{skill_name}.skill"
    
    console.print(f"📦 [bold]Step 2:[/bold] Packaging skill '{skill_name}'...")
    
    # Count files to package
    files_to_package = []
    for file_path in skill_path.rglob("*"):
        if file_path.is_file():
            if not should_exclude(
                file_path, 
                skill_path, 
                config.packaging.exclude_patterns,
                config.packaging.include_dotfiles
            ):
                files_to_package.append(file_path)
    
    if not files_to_package:
        console.print("❌ [bold red]Error:[/bold red] No files to package")
        return None
    
    console.print(f"   📄 Found {len(files_to_package)} files to package")
    
    # Create ZIP archive
    try:
        with ZipFile(skill_file, 'w', ZIP_DEFLATED, compresslevel=config.packaging.compression_level) as zipf:
            for file_path in files_to_package:
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)
        
        file_size = skill_file.stat().st_size
        size_kb = file_size / 1024
        
        console.print(f"\n✅ [bold green]Success![/bold green]")
        console.print(f"   📦 Created: {skill_file}")
        console.print(f"   📊 Size: {size_kb:.1f} KB")
        console.print(f"   🗜️  Compression: Level {config.packaging.compression_level}")
        
        return skill_file
        
    except Exception as e:
        console.print(f"\n❌ [bold red]Error creating package:[/bold red] {e}")
        return None


@app.command()
def main(
    skill_path: Annotated[Path, typer.Argument(help="Path to the skill directory to package")],
    output_dir: Annotated[Optional[Path], typer.Option("--output", "-o", help="Output directory for .skill file")] = None,
    skip_validation: Annotated[bool, typer.Option("--skip-validation", help="Skip validation step")] = False,
):
    """
    Package a skill into a distributable .skill file.
    
    Validates the skill structure and creates a ZIP archive with proper exclusions.
    """
    console.print("\n📦 [bold cyan]Skill Packager[/bold cyan]\n")
    
    result = package_skill(skill_path, output_dir, skip_validation=skip_validation)
    
    if result:
        console.print()
        raise typer.Exit(0)
    else:
        console.print()
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

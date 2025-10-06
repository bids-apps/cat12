"""Module responsible for generating method section."""

from pathlib import Path

from cat12._version import __version__
from jinja2 import Environment, FileSystemLoader, select_autoescape

from cat12.defaults import CAT_VERSION, MCR_VERSION


def generate_method_section(
    output_dir: Path,
    version: str = __version__,
    cat_version: str = CAT_VERSION,
    mcr_version: str = MCR_VERSION,
    batch: str | None = None,
) -> None:
    """Add a method section to the output dataset."""
    env = Environment(
        loader=FileSystemLoader(Path(__file__).parent),
        autoescape=select_autoescape(),
        lstrip_blocks=True,
        trim_blocks=True,
    )

    template = env.get_template("data/methods/template.jinja")

    output_file = output_dir / "logs" / "CITATION.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "version": version,
        "cat_version": cat_version,
        "mcr_version": mcr_version,
        "batch": batch,
    }

    with Path.open(output_file, "w") as f:
        print(template.render(data=data), file=f)

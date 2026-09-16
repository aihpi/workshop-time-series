from pathlib import Path
from IPython.display import Markdown, display


def display_datasets_info(section: str) -> None:
    """Render one section of `data/datasets.md` inside a notebook.

    That file is the single description of every dataset, and it is marked up
    with ``<!-- start:name -->`` and ``<!-- end:name -->`` comments so that a
    notebook can show just the part relevant to it. Keeping one copy is the
    point: a dataset's provenance is described once and read in several places.

    Args:
        section: the name between the start and end markers.
    """
    file_path = Path("../data/datasets.md")
    start_marker = f"<!-- start:{section} -->"
    end_marker = f"<!-- end:{section} -->"

    # Read the whole file as a string and split into lines
    lines = file_path.read_text(encoding="utf-8").splitlines()

    inside = False
    selected_lines = []
    for line in lines:
        if start_marker in line:
            inside = True
            continue
        if end_marker in line:
            inside = False
            break
        if inside:
            selected_lines.append(line)

    # Display as Markdown
    display(Markdown("\n".join(selected_lines)))

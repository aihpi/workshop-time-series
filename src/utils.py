from pathlib import Path
from IPython.display import Markdown, display


# Function to parse and display specific sections from datasets.md
def display_datasets_info(section: str) -> None:
    file_path = Path("../data/datasets.md")  # Path object
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

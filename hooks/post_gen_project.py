import json
import shutil
import subprocess
import tempfile
from pathlib import Path

MANUSCRIPT_FILENAME = "manuscript.tex"


def copy_journal_template_files(journal_template, project_dir):
    """
    Copies files from a package's resource directory to a target directory.

    Parameters:
    ===========
    journal_template : str
      The name of the journal latex template to use. It must be
      one of the available templates.
    project_dir : Path
      The path to the location of the output project where the files
      will be copied to.
    """
    context_file = project_dir / "cookiecutter.json"
    if context_file.exists():
        with context_file.open("r", encoding="utf-8") as f:
            context = json.load(f)
        cookiecutter_path = Path(context.get("_repo_dir", "unknown")).resolve()
    else:
        print("cookiecutter.json not found in output directory.")

    # Get the directory of resources
    template_dir = cookiecutter_path / "templates" / journal_template
    if not template_dir.exists():
        raise NotADirectoryError(f"Cannot find the provided journal_tamplate: "
                                 f"{journal_template}. Please contact the "
                                 f"software developers")
    for item in template_dir.iterdir():
        dest = project_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)
    return project_dir


def get_user_headers(repo_url):
    """
    Clone a Git repository containing LaTeX header files into a string.
    """
    headers = ""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        subprocess.run(["git", "clone", repo_url, str(tmp_path)], check=True)
        for item in tmp_path.glob('**/*'):
            if item.is_file() and str(item).endswith(".tex"):
                headers += item.read_text()+'\n'
    return headers


def extract_manuscript_packages(manuscript_path):
    contents = manuscript_path.read_text(encoding="utf-8")
    packages, the_rest = split_usepackage_lines(contents)
    Path(manuscript_path).write_text(the_rest, encoding="utf-8")
    return packages


def split_usepackage_lines(headers):
    usepackage_lines = []
    other_lines = []
    for line in headers.splitlines():
        if line.lstrip().startswith(r"\usepackage"):
            usepackage_lines.append(line)
        else:
            other_lines.append(line)
    return "\n".join(usepackage_lines), "\n".join(other_lines)


def insert_below_documentclass(manuscript_text, insert_text):
    lines = manuscript_text.splitlines()
    result_lines = []
    inserted = False
    for line in lines:
        result_lines.append(line)
        if not inserted and r"\documentclass" in line:
            result_lines.append(insert_text)
            inserted = True
    return "\n".join(result_lines)


def recompose_manuscript(manuscript_path, user_packages, user_commands):
    new_header = "\n".join([user_packages, user_commands])
    manuscript_contents = manuscript_path.read_text(encoding="utf-8")
    manuscript_contents_with_header = insert_below_documentclass(
        manuscript_contents, new_header
    )
    manuscript_path.write_text(
        manuscript_contents_with_header, encoding="utf-8"
    )


def main():
    project_dir = Path().cwd()
    manuscript_path = project_dir / MANUSCRIPT_FILENAME
    copy_journal_template_files(
        "{{ cookiecutter.journal_template }}", project_dir
    )
    user_headers = get_user_headers(
        "{{ cookiecutter.latex_headers_repo }}"
    )
    manuscript_packages = extract_manuscript_packages(manuscript_path)
    user_packages, the_rest = split_usepackage_lines(user_headers)
    all_packages = "/n".join([manuscript_packages, user_packages])
    recompose_manuscript(manuscript_path, all_packages, the_rest)


if __name__ == "__main__":
    main()

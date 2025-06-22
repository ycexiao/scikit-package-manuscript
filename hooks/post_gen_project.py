import shutil
from pathlib import Path
from typing import Literal

MANUSCRIPT_FILENAME = "manuscript.tex"


def get_scikit_manuscript_dir():
    """Return the full path to the local scikit-package-manuscript
    dir."""
    cookiecutter_dir = Path.home() / ".cookiecutters"
    candidates = []
    for candidate in cookiecutter_dir.iterdir():
        candidates.append(candidate)
        if (
            candidate.is_dir()
            and "scikit-package-manuscript" in candidate.name
        ):
            return candidate.resolve()
    return Path(
        f"couldn't find scikit-package-manuscript, but did "
        f"find {*candidates, }"
    )  # noqa E231


def copy_journal_template_files(journal_template_name, project_dir):
    """Copies files from a package's resource directory to a target
    directory.

    Parameters:
    ===========
    journal_template : str
      The name of the journal latex template to use, e.g. 'article'.
      It must be one of the available templates.
    project_dir : Path
      The path to the location of the output project where the files
      will be copied to.
    """
    cookiecutter_path = get_scikit_manuscript_dir()
    template_dir = cookiecutter_path / "templates" / journal_template_name
    if not template_dir.exists():
        raise FileNotFoundError(
            f"Cannot find the provided journal_template: "
            f"{journal_template_name}. Please contact the "
            f"software developers."
        )

    if not any(template_dir.iterdir()):
        raise FileNotFoundError(
            f"Template {journal_template_name} found but "
            f"it contains no files. Please contact the "
            f"software developers."
        )
    for item in template_dir.iterdir():
        dest = project_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)
    return


def get_input_type(input: str) -> Literal["url", "local", "None"]:
    input_type = "None"
    return input_type


def copy_files_from_url(repo_url: str, project_dir: Path) -> list[Path]:
    # side effect: files are copied into project_dir
    files = None
    print(f"{len(files)} found in {repo_url}.")
    return files


def copy_files_from_local(local_path: str, project_dir: Path) -> list[Path]:
    # side effect: files are copied into project_dir
    files = None
    print(f"{len(files)} found in {local_path}.")
    return files


def extract_lines(content: str, keyword: str) -> tuple[str, str]:
    lines = None
    return lines, content


def insert_lines(
    content: str,
    insert_text: str,
    location_keyword: str,
    method: Literal["below", "above"],
) -> str:
    update_contnet = None
    return update_contnet


def get_file_type(a_file: Path) -> Literal["header", "bib", "other"]:
    file_type = "other"
    return file_type


def add_headers_to_manuscript(header_files: list[Path], manuscript_path: Path):
    # side effect: 1. headers are inserted in to manuscript.
    #   2. header files are deleted.
    headers_content = "\n".join([file.read_text() for file in header_files])
    package_lines, cmd_lines = extract_lines(headers_content, r"\usepackage")
    manuscript_content = manuscript_path.read_text()
    manuscript_package_lines, other_content = extract_lines(
        manuscript_content, r"\usepacakge"
    )
    headers_content = "\n".join(
        [package_lines, manuscript_package_lines, cmd_lines]
    )
    manuscript_with_headers = insert_lines(
        other_content, headers_content, r"\begin{document}", "below"
    )
    manuscript_path.write_text(manuscript_with_headers)
    for file in header_files:
        file.unlink()


def add_bibliography_to_manuscript(
    bib_files: list[Path], manuscript_path: Path
):
    # side effect: 1. bib files name are added
    bib = ",".join([file.stem for file in bib_files])
    bib = r"\bibliography{" + bib + r"}"
    manuscript_content = manuscript_path.read_text()
    manuscript_bib, other_content = extract_lines(
        manuscript_content, r"\bibliography"
    )
    bib_content = "\n".join([bib, manuscript_bib])
    manuscript_with_bib = insert_lines(
        other_content, bib_content, r"\end{document}", "above"
    )
    manuscript_path.write_text(manuscript_with_bib)


def main():
    project_dir = Path().cwd()
    manuscript_path = project_dir / MANUSCRIPT_FILENAME
    copy_journal_template_files(
        "{{ cookiecutter.journal_template }}", project_dir
    )

    external_latex_files_path = "{{ cookiecutter.external_latex_files_path }}"
    input_type = get_input_type(external_latex_files_path)
    if input_type == "url":
        files = copy_files_from_url(external_latex_files_path)
    elif input_type == "local":
        files = copy_files_from_local(external_latex_files_path)
    else:
        return

    header_files = [f for f in files if get_file_type(f) == "header"]
    bib_files = [f for f in files if get_file_type(f) == "bib"]
    add_headers_to_manuscript(header_files, manuscript_path)
    print(f"{len(header_files)} header files Found.")
    add_bibliography_to_manuscript(bib_files, manuscript_path)
    print(f"{len(bib_files)} bib files Found.")


if __name__ == "__main__":
    main()

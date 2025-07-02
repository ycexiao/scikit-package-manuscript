import shutil
import subprocess
import tempfile
from pathlib import Path

MANUSCRIPT_FILENAME = "manuscript.tex"


def get_scikit_manuscript_dir():
    """Return the full path to the local scikit-package-manuscript
    dir."""
    cookiecutter_dir = Path.home() / ".cookiecutters"
    candidates = []
    for candidate in cookiecutter_dir.iterdir():
        candidates.append(candidate)
        if (candidate.is_dir() and
                "scikit-package-manuscript" == candidate.name):
            return candidate.resolve()
    return Path("Unable to find scikit-package-manuscript, but did "
                f"find {*candidates,}")  # noqa E231


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
        raise FileNotFoundError("Unable to find the provided journal_template: "
                                f"{journal_template_name}. Please leave an issue "
                                "on GitHub.")

    if not any(template_dir.iterdir()):
        raise FileNotFoundError(f"Template {journal_template_name} found but "
                                "it contains no files. Please leave an issue "
                                "on GitHub.")
    for item in template_dir.iterdir():
        dest = project_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)
    return


def get_user_headers(repo_url):
    """Clone a Git repository containing LaTeX header files into a
    string."""
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

def copy_all_files(source_dir, target_dir):
    """Copies files from a package's resource directory to a target
    directory.

    Parameters:
    ===========
    source_dir : Path
      The source dir from which all the files will be copied, recursively
    project_dir : Path
      The path to the location of the output project where the files
      will be copied to.
    """
    if not source_dir.exists():
        raise FileNotFoundError(
            "Unable to find the source directory: "
            f"{str(source_dir)}. Please leave an issue "
            "on GitHub."
        )

    if not any(source_dir.iterdir()):
        raise FileNotFoundError(
            f"Source directory {str(source_dir)} found "
            "but it contains no files. Please leave an issue "
            "on GitHub."
        )

    for item in source_dir.iterdir():
        dest = target_dir / item.name
        if dest.exists():
            raise FileExistsError(
                f"{dest.name} already exists in {str(target_dir)}. "
                "Please either remove this from the user-defined GitHub repo, "
                "or leave an issue on GitHub if you think the problem is with "
                "scikit-package."
            )

    for item in source_dir.iterdir():
        dest = target_dir / item.name
        if item.is_file():
            shutil.copy(item, dest)
        else:
            shutil.copytree(item, dest)
    return


def clone_gh_repo(url):
    """Clone the repo to a temporary location.

    Parameters
    ----------
    url : a url

    Returns
    -------
    The path to the contents of the repo on the local files-system
    """
    pass


def load_headers(headers_path, manuscript_path):
    """Loads usepackages.txt and newcommands.txt into manuscript.tex
    header.

    Updates manuscript.tex headers in place with the contents of the user-files.


    Parameters
    ----------
    headers_path : Path
      The path to the location of the usepackages.txt file
    manuscript_path : Path
      The path to the manuscript.tex file

    Returns
    -------
    None
    """
    pass

def load_bib_info(project_path, manuscript_file_name="manuscript.tex"):
    """Loads all bib files into manuscript.tex.

    Finds all bib files and manuscript.tex in project-dir, and loads the
    bib names into the bibliography field in manuscript.tex.

    Parameters
    ----------
    project_path : Path
      The path to the location of the project directory.

    Returns
    -------
    None
    """
    manuscript_path = project_path / manuscript_file_name
    if not manuscript_path.exists():
        raise FileNotFoundError(
            f"Unable to find {manuscript_file_name} in "
            f"{str(project_path)}. Please leave an issue on GitHub."
        )
    bibliography = []
    bib_stems = []
    for item in project_path.iterdir():
        if item.is_file() and item.name.endswith(".bib"):
            bib_stems.append(item.stem)
    if len(bib_stems) != 0:
        bibliography.append(r"\bibliography{" + ", ".join(sorted(bib_stems)) + "}")
    manuscript_content = manuscript_path.read_text()
    bib_in_manuscript, manuscript_without_bib = _split_lines_with_keyword(manuscript_content, r"\bibliography")
    bibstyle_in_manuscript = []
    for line in bib_in_manuscript.splitlines():
        if line.lstrip().startswith(r"\bibliography{"):
            continue
        else:
            bibstyle_in_manuscript.append(line)
    bibliography.extend(bibstyle_in_manuscript)
    bib_text = '\n'.join(bibliography)
    manuscript_with_bib = _insert_to_manuscript(manuscript_without_bib, bib_text, r"\end{document}", "above")
    manuscript_path.write_text(manuscript_with_bib)



def remove_temporary_files(tmpdir_path):
    pass


def main():
    project_dir = Path().cwd()
    manuscript_path = project_dir / MANUSCRIPT_FILENAME
    if ("{{ cookiecutter.latex_headers_repo_url }}" ==
            "use-scikit-package-default"):
        user_headers_repo_url = \
            "https://github.com/scikit-package/default-latex-headers.git"
    else:
        user_headers_repo_url = "{{ cookiecutter.latex_headers_repo_url }}"
    copy_journal_template_files(
        "{{ cookiecutter.journal_template }}", project_dir
    )
    user_headers = get_user_headers(user_headers_repo_url)
    manuscript_packages = extract_manuscript_packages(manuscript_path)
    user_packages, the_rest = split_usepackage_lines(user_headers)
    all_packages = "\n".join([manuscript_packages, user_packages])
    recompose_manuscript(manuscript_path, all_packages, the_rest)


if __name__ == "__main__":
    main()

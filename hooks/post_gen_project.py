import shutil
import subprocess
import tempfile
import requests
from pathlib import Path

MANUSCRIPT_FILENAME = "manuscript.tex"


def get_scikit_manuscript_dir():
    """return the full path to the local scikit-package-manuscript dir"""
    cookiecutter_dir = Path.home() / ".cookiecutters"
    candidates = []
    for candidate in cookiecutter_dir.iterdir():
        candidates.append(candidate)
        if (candidate.is_dir() and
                "scikit-package-manuscript" in candidate.name):
            return candidate.resolve()
    return Path(f"couldn't find scikit-package-manuscript, but did "
                f"find {*candidates,}")  # noqa E231


def copy_journal_template_files(journal_template_name, project_dir):
    """
    Copies files from a package's resource directory to a target directory.

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
        raise FileNotFoundError(f"Cannot find the provided journal_template: "
                                f"{journal_template_name}. Please contact the "
                                f"software developers.")

    if not any(template_dir.iterdir()):
        raise FileNotFoundError(f"Template {journal_template_name} found but "
                                f"it contains no files. Please contact the "
                                f"software developers.")
    for item in template_dir.iterdir():
        dest = project_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)
    return


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


def extract_manuscript_keyword_lines(manuscript_path, keyword=r'\usepackage'):
    contents = manuscript_path.read_text(encoding="utf-8")
    packages, the_rest = split_keyword_lines(contents, keyword=keyword)
    Path(manuscript_path).write_text(the_rest, encoding="utf-8")
    return packages


def split_keyword_lines(content, keyword=r'\usepackage'):
    """Split the lines containing keyword from the content."""
    keyword_lines = []
    other_lines = []
    for line in content.splitlines():
        if line.lstrip().startswith(keyword):
            keyword_lines.append(line)
        else:
            other_lines.append(line)
    return "\n".join(keyword_lines), "\n".join(other_lines)


def insert_keyword_lines(content, insert_text, location_keyword=r'\documentclass', method='below'):
    """Inser the lines below or above a certain location in the content."""
    lines = content.splitlines()
    result_lines = []
    inserted = False
    if method == 'below':
        for line in lines:
            result_lines.append(line)
            if not inserted and location_keyword in line:
                result_lines.append(insert_text)
                inserted = True
    elif method == 'above':
        for line in lines:
            if not inserted and location_keyword in line:
                result_lines.append(insert_text)
                inserted = True
            result_lines.append(line)
    return "\n".join(result_lines)


def recompose_manuscript(manuscript_path, user_packages, user_commands):
    new_header = "\n".join([user_packages, user_commands])
    manuscript_contents = manuscript_path.read_text(encoding="utf-8")
    manuscript_contents_with_header = insert_keyword_lines(
        manuscript_contents, new_header
    )
    manuscript_path.write_text(
        manuscript_contents_with_header, encoding="utf-8"
    )


def get_bib_path_type(bib_path):
    if bib_path == "None":
        return 'none'
    elif "github.com" in bib_path:
        response = requests.get(bib_path)
        if response.status_code != 200:
            raise FileNotFoundError(f"Cannot find Github repo {str(bib_path)}."
                                    f" Please make sure the URL is correct.")
        return "url"
    else:
        bib_path = Path(bib_path).expanduser()
        if not bib_path.exists():
            raise FileNotFoundError(f"Cannot find {str(bib_path)}. "
                                     "Please try again after running "
                                    f"'touch {str(bib_path)}'.")
        return "local"


def copy_bib_from_url(bib_path, project_dir):
    bib_names = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        subprocess.run(["git", "clone", bib_path, str(tmp_path)], check=True)
        for item in tmp_path.glob('**/*'):
            if item.is_file() and str(item).endswith(".bib"):
                bib_names.append(item.name)
                dest = project_dir / item.name
                shutil.copy2(item, dest)
    if len(bib_names) == 0:
        raise FileNotFoundError(f"Cannot find bib files in "
                                f"{str(bib_path)}. Please contact "
                                "the software developers")
    return bib_names


def copy_bib_from_local(bib_path, project_dir):
    bib_names = []
    bib_path = Path(bib_path).expanduser()
    if bib_path.is_dir():
        for item in bib_path.glob('**/*'):
            if item.is_file() and str(item).endswith(".bib"):
                bib_names.append(item.name)
                dest = project_dir / item.name
                shutil.copy2(item, dest)
    else:
        if bib_path.name.endswith(".bib"):
            bib_names.append(bib_path.name)
            dest = project_dir / bib_path.name
            shutil.copy2(bib_path, dest)
    if len(bib_names) == 0:
        raise FileNotFoundError(f"Cannot find bib files in "
                                f"{str(bib_path)}. Please create "
                                f"bib files in {str(bib_path)}")
    return bib_names


def insert_headers_from_repo(project_dir, manuscript_path, headers_repo_url):
    if ( headers_repo_url ==
            "use-scikit-package-default"):
        user_headers_repo_url = \
            "https://github.com/scikit-package/default-latex-headers.git"
    else:
        user_headers_repo_url = "{{ cookiecutter.latex_headers_repo_url }}"
    user_headers = get_user_headers(user_headers_repo_url)
    manuscript_packages = extract_manuscript_keyword_lines(manuscript_path)
    user_packages, the_rest = split_keyword_lines(user_headers)
    all_packages = "\n".join([manuscript_packages, user_packages])
    recompose_manuscript(manuscript_path, all_packages, the_rest)

    
def insert_bibliography_from_path(project_dir, manuscript_path, bib_path):
    bib_path_type = get_bib_path_type(bib_path)
    if bib_path_type == 'url':
        bib_names = copy_bib_from_url(bib_path, project_dir)
    elif bib_path_type == 'local':
        bib_names = copy_bib_from_local(bib_path, project_dir)
    else:
        return
    insert_bibliography = r'\bibliography{' + ", ".join(bib_names) + r'}'
    manuscript_bibliography = extract_manuscript_keyword_lines(manuscript_path, keyword=r"\bibliography")
    all_bibliography = '\n'.join([insert_bibliography, manuscript_bibliography])
    manuscript_contents = manuscript_path.read_text(encoding="utf-8")
    manuscript_content_with_bibliography = insert_keyword_lines(manuscript_contents, all_bibliography, location_keyword=r'\end{document}', method='above')
    manuscript_path.write_text(
        manuscript_content_with_bibliography, encoding="utf-8"
    )


def main():
    project_dir = Path().cwd()
    manuscript_path = project_dir / MANUSCRIPT_FILENAME
    copy_journal_template_files(
        "{{ cookiecutter.journal_template }}", project_dir
    )
    headers_repo_url = "{{ cookiecutter.latex_headers_repo_url }}" 
    insert_headers_from_repo(project_dir, manuscript_path, headers_repo_url)
    bib_path = "{{ cookiecutter.latex_bibliography_path }}"
    insert_bibliography_from_path(project_dir, manuscript_path, bib_path)


if __name__ == "__main__":
    main()

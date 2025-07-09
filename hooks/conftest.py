import shutil
from pathlib import Path
from unittest import mock

import pytest


@pytest.fixture(scope="session")
def template_files():
    spm_template_files = {
        "article-cls-in-spm.cls": r"Contents of article-cls-in-spm.cls",
        "manuscript-in-spm.tex": r"""
\documentclass{article}
\usepackage{package-in-manuscript}
\newcommand{\command_in_manuscript}[1]{\mathbf{#1}}
\begin{document}
Contents of manuscript
\bibliography{bib-in-manuscript}
\bibliographystyle{chicago}
\end{document}
""",
        "bib-in-project.bib": r"""Contents of bib-in-project.bib""",
    }
    yield spm_template_files


@pytest.fixture(scope="session")
def user_repo_files_and_contents():
    user_repo_files_and_contents = {
        "usepackages.txt": r"\usepackage{package-from-user-usepackage}",
        "newcommands.txt": (
            r"\newcommand{\command_from_user_newcommands}[1]{\mathrm{#1}}"
        ),
        "user-bib-file-1.bib": "Contents of user-bib-file-1.bib",
        "user-bib-file-2.bib": "Contents of user-bib-file-2.bib",
        "user-supplied-non-bib-file.tex": (
            "Contents of user-supplied-non-bib-file.tex"
        ),
    }
    yield user_repo_files_and_contents


@pytest.fixture
def mock_home(tmp_path):
    with mock.patch.object(Path, "home", return_value=tmp_path):
        yield tmp_path


@pytest.fixture
def user_filesystem(
    tmp_path,
    template_files,
    user_repo_files_and_contents,
):
    # create a filesystem with spm in a .cookiecutters directory and
    # template directories called article, other, and another
    # the article template contains a set of files defined in TEMPLATE_FILES
    #
    # directory structure:
    # ├── .cookiecutters
    # │   └── scikit-package-manuscript
    # │       └── templates
    # │           ├── another
    # │           ├── other
    # │           └── article
    # │               ├── article-cls-in-spm.cls
    # │               ├── bib-in-project.bib
    # │               └── manuscript-in-spm.tex
    # ├── empty-user-repo-dir
    # ├── user-repo-dir
    # │   ├── newcommands.txt
    # │   ├── usepackages.txt
    # │   ├── user-bib-file-1.bib
    # │   ├── user-bib-file-2.bib
    # │   └── user-supplied-non-bib-file.tex
    # └── project-dir
    spm_path = Path(tmp_path / ".cookiecutters" / "scikit-package-manuscript")
    spm_path.mkdir(parents=True, exist_ok=True)
    template_names = ["other", "another"]
    for template_name in template_names:
        template_path = spm_path / "templates" / template_name
        template_path.mkdir(parents=True, exist_ok=True)
    article_path = Path(spm_path / "templates" / "article")
    article_path.mkdir(parents=True, exist_ok=True)
    for key, value in template_files.items():
        template_file_path = article_path / key
        template_file_path.write_text(value)
    manuscript_path = article_path / "manuscript-in-spm.tex"

    user_repo_dir = tmp_path / "user-repo-dir"
    user_repo_dir.mkdir()
    project_dir = tmp_path / "project-dir"
    project_dir.mkdir()
    for key, value in user_repo_files_and_contents.items():
        file_path = user_repo_dir / key
        file_path.write_text(value)
    empty_dir = tmp_path / "empty-user-repo-dir"
    empty_dir.mkdir()

    important_paths = {
        "home-dir": tmp_path,
        "user-repo-dir": user_repo_dir,
        "project-dir": project_dir,
        "manuscript-path": manuscript_path,
    }
    yield important_paths


@pytest.fixture
def mock_clone(user_filesystem):
    user_repo_dir = user_filesystem["user-repo-dir"]
    with mock.patch("subprocess.check_output") as mock_check_output:
        mock_check_output.return_value = True

        def side_effect(cmd, cwd, stderr):
            shutil.copytree(user_repo_dir, cwd, dirs_exist_ok=True)

        mock_check_output.side_effect = side_effect
        yield mock_check_output

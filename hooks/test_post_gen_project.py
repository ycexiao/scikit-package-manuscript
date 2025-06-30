import shutil
from pathlib import Path

import pytest

from hooks.post_gen_project import copy_journal_template_files, load_bib_info


def _file_not_found_error_message(file_path):
    message = (
        "Unable to find the path: "
        f"{str(file_path)}. Please leave an issue "
        "on GitHub."
    )
    return message


# C1: multiple files in the template, expect all files will be copied
#   to project_path
def test_copy_journal_template_files(home_path, template_files, mock_home):
    project_dir = Path(home_path / "project-dir")
    copy_journal_template_files("article", project_dir)
    for key, value in template_files.items():
        assert Path(project_dir / key).exists()
        assert Path(project_dir / key).read_text() == value


@pytest.mark.parametrize(
    "input,errormessage",
    [
        # C1: template exists no files in the template. Expect
        # FileNotFoundError
        (
            "other",
            "Template other found but it contains no "
            "files. Please leave an issue on GitHub.",
        ),
        # C2: desired template does not exist. Expect FileNotFoundError
        (
            "yet-another",
            "Unable to find the provided journal_template: "
            "yet-another. Please leave an issue on GitHub.",
        ),
    ],
)
def test_copy_journal_template_files_bad(
    home_path, mock_home, input, errormessage
):
    project_dir = Path(home_path / "project-dir")

    with pytest.raises(
        FileNotFoundError,
        match=errormessage,
    ):
        copy_journal_template_files(input, project_dir)


@pytest.mark.parametrize(
    "exists_bib, expected_manuscript_content",
    [
        # C1: manuscript.tex and bib files exist in the directory.
        #   Expect bib names are inserted into the manuscript's bibliography.
        (
            True,
            r"""
\documentclass{article}
\usepackage{package-in-manuscript}
\newcommand{\command_in_manuscript}[1]{\mathbf{#1}}
\begin{document}
Contents of manuscript
\bibliography{bib-in-project, user-bib-file-1, user-bib-file-2}
\bibliographystyle{chicago}
\end{document}
""",
        ),
        # C2: manuscript.tex exists in the directory, but bib files don't.
        #   Expect the manuscript.tex content doesn't change.
        (
            False,
            r""""
\documentclass{article}
\usepackage{package-in-manuscript}
\newcommand{\command_in_manuscript}[1]{\mathbf{#1}}
\begin{document}
Contents of manuscript
\bibliographystyle{chicago}
\end{document}
""",
        ),
    ],
)
def test_load_bib_info(
    user_filesystem, exists_bib, expected_manuscript_content
):
    home_path, paths_in_filesystem = user_filesystem
    manuscript_path = paths_in_filesystem["manuscript.tex"]

    # a non-existing dir
    project_dir_with_bib = home_path / "project-dir-with-bib"
    manuscript_in_project = project_dir_with_bib / "manuscript.tex"
    shutil.copy(manuscript_path, manuscript_in_project)
    if exists_bib:
        Path(project_dir_with_bib / "bib-in-project.bib").touch()
        Path(project_dir_with_bib / "user-bib-file-1.bib").touch()
        Path(project_dir_with_bib / "user-bib-file-2.bib").touch()

    load_bib_info(project_dir_with_bib)
    actual_manuscript_content = manuscript_in_project.read_text()
    assert expected_manuscript_content == actual_manuscript_content


# C1: manuscript.tex doesn't exist in the project directory.
#   Expect FileNotFoundError.
def test_load_bib_info_bad(user_filesystem):
    home_path, _ = user_filesystem
    project_dir_without_manuscript = (
        home_path / "project-dir-without-manuscript"
    )
    project_dir_without_manuscript.mkdir()
    with pytest.raises(
        FileNotFoundError,
        match=(
            "Unable to find manuscript.tex in "
            f"{str(str(project_dir_without_manuscript))} "
            "Please leave an issue on GitHub."
        ),
    ):
        load_bib_info(project_dir_without_manuscript)

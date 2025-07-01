import shutil
from pathlib import Path

import pytest

from hooks.post_gen_project import (
    copy_all_files,
    copy_journal_template_files,
    load_headers,
)


# C1: multiple files in the template, expect all files will be copied
#   to project_path
def test_copy_journal_template_files(
    user_filesystem, template_files, mock_home
):
    project_dir = Path(user_filesystem / "project-dir")
    project_dir.mkdir(parents=True, exist_ok=True)
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
    user_filesystem, mock_home, input, errormessage
):
    project_dir = Path(user_filesystem / "project-dir")
    project_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(
        FileNotFoundError,
        match=errormessage,
    ):
        copy_journal_template_files(input, project_dir)


# C1: Existing source dir and target dir.
#  Expect all files in source dir are copied to target dir.
def test_copy_all_files(user_filesystem, user_repo_files_and_contents):
    source_dir = user_filesystem / "user-repo-dir"
    target_dir = user_filesystem / "target-dir"
    copy_all_files(source_dir, target_dir)
    for key, value in user_repo_files_and_contents.items():
        file_path = target_dir / key
        assert file_path.exists()
        assert file_path.read_text() == value


# C1: An non-existing source dir and an existing target dir.
#  Expect FileNotFoundError.
# C2: An empty source dir and an existing target dir.
#  Expect FlileNotFoundError.
# C3: Existing source dir and target dir, but there is a file with the same
#  name found in both dirs. Expect FileExistsError.
def test_copy_all_files_bad(user_filesystem):
    # non-existing source directory
    non_existing_source_dir = user_filesystem / "other-dir"
    assert not non_existing_source_dir.exists()
    target_dir = user_filesystem / "target-dir"
    with pytest.raises(
        FileNotFoundError,
        match=(
            "Unable to find the source directory: "
            f"{str(non_existing_source_dir)}. Please leave an issue "
            "on GitHub."
        ),
    ):
        copy_all_files(non_existing_source_dir, target_dir)

    # empty source directory
    empty_source_dir = user_filesystem / "empty-user-repo-dir"
    assert empty_source_dir.exists() and (not any(empty_source_dir.iterdir()))
    with pytest.raises(
        FileNotFoundError,
        match=(
            f"Source directory {str(empty_source_dir)} found "
            "but it contains no files. Please leave an issue "
            "on GitHub."
        ),
    ):
        copy_all_files(empty_source_dir, target_dir)

    # a file with the same name found in both dirs.
    source_dir = user_filesystem / "user-repo-dir"
    target_dir = user_filesystem / "duplicated-dir"
    target_dir.mkdir()
    duplicate_file = target_dir / "usepackages.txt"
    duplicate_file.touch()
    assert duplicate_file.exists()
    with pytest.raises(
        FileExistsError,
        match=(
            f"{duplicate_file.name} already exists in "
            f"{str(target_dir)}. Please either remove "
            "this from the user-defined GitHub repo, "
            "or leave an issue on GitHub if you think the problem is with "
            "scikit-package."
        ),
    ):
        copy_all_files(source_dir, target_dir)


@pytest.mark.parametrize(
    "existing_files, expected_manuscript_content",
    [
        # C1: `usepackages.txt` and `newcommands.txt` exist in the
        #   headers_path and there are several usepackages lines in the
        #   manuscript.
        #   Expect packages and commands are inserted into the manuscript in
        #   a order that packages come before commands.
        (
            ["usepackages.txt", "newcommands.txt"],
            r"""
\documentclass{article}
\usepackage{package-from-user-usepackage}
\usepackage{package-in-manuscript}
\newcommand{\command_from_user_newcommands}[1]{\mathrm{#1}}
\newcommand{\command_in_manuscript}[1]{\mathbf{#1}}
\begin{document}
Contents of manuscript
\bibliography{bib-in-manuscript}
\bibliographystyle{chicago}
\end{document}
""",
        ),
        # C2: Only usepackages.txt exists. Expect user's usepackages are
        #   inserted before manuscript's usepackages abd after
        #   \begin{documentclass}
        (
            ["usepackages.txt"],
            r"""
\documentclass{article}
\usepackage{package-from-user-usepackage}
\usepackage{package-in-manuscript}
\newcommand{\command_in_manuscript}[1]{\mathbf{#1}}
\begin{document}
Contents of manuscript
\bibliography{bib-in-manuscript}
\bibliographystyle{chicago}
\end{document}
""",
        ),
        # C3: Only newcommands.txt exists. Expect user's newcommands are
        #   inserted before manuscript's newcommands and after manuscrip'ts
        #   usepackages.
        (
            ["newcommands.txt"],
            r"""
\documentclass{article}
\usepackage{package-in-manuscript}
\newcommand{\command_from_user_newcommands}[1]{\mathrm{#1}}
\newcommand{\command_in_manuscript}[1]{\mathbf{#1}}
\begin{document}
Contents of manuscript
\bibliography{bib-in-manuscript}
\bibliographystyle{chicago}
\end{document}
""",
        ),
    ],
)
def test_load_headers(
    user_filesystem,
    existing_files,
    expected_manuscript_content,
):
    # a non-existing dir
    project_dir_with_header = user_filesystem / "project-dir-with-header"
    project_dir_with_header.mkdir()
    manuscript_path = (
        user_filesystem
        / ".cookiecutters"
        / "scikit-package-manuscript"
        / "templates"
        / "article"
        / "manuscript-in-spm.tex"
    )
    manuscript_in_project = project_dir_with_header / "manuscript.tex"
    shutil.copy(manuscript_path, manuscript_in_project)
    source_dir = user_filesystem / "user-repo-dir"
    for file_name in existing_files:
        source = source_dir / file_name
        dest = project_dir_with_header / file_name
        shutil.copy(source, dest)

    load_headers(project_dir_with_header)
    actual_manuscript_content = manuscript_in_project.read_text()
    assert expected_manuscript_content == actual_manuscript_content

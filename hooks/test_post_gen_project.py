import shutil
from pathlib import Path

import pytest

from hooks.post_gen_project import (
    copy_all_files,
    copy_journal_template_files,
    initialize_project,
    load_bib_info,
    load_headers,
)


# C1: multiple files in the template, expect all files will be copied
#   to project_path
def test_copy_journal_template_files(
    user_filesystem, template_files, mock_home
):
    project_dir = user_filesystem["project-dir"]
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
    project_dir = user_filesystem["project-dir"]
    with pytest.raises(
        FileNotFoundError,
        match=errormessage,
    ):
        copy_journal_template_files(input, project_dir)


# C1: Existing source dir and target dir.
#  Expect all files in source dir are copied to target dir.
def test_copy_all_files(user_filesystem, user_repo_files_and_contents):
    source_dir = user_filesystem["user-repo-dir"]
    project_dir = user_filesystem["project-dir"]
    copy_all_files(source_dir, project_dir)
    for key, value in user_repo_files_and_contents.items():
        file_path = project_dir / key
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
    home_dir = user_filesystem["home-dir"]
    non_existing_source_dir = home_dir / "other-dir"
    assert not non_existing_source_dir.exists()
    project_dir = user_filesystem["project-dir"]
    with pytest.raises(
        FileNotFoundError,
        match=(
            "Unable to find the source directory: "
            f"{str(non_existing_source_dir)}. Please leave an issue "
            "on GitHub."
        ),
    ):
        copy_all_files(non_existing_source_dir, project_dir)

    # empty source directory
    empty_source_dir = home_dir / "empty-user-repo-dir"
    assert empty_source_dir.exists() and (not any(empty_source_dir.iterdir()))
    with pytest.raises(
        FileNotFoundError,
        match=(
            f"Source directory {str(empty_source_dir)} found "
            "but it contains no files. Please leave an issue "
            "on GitHub."
        ),
    ):
        copy_all_files(empty_source_dir, project_dir)

    # a file with the same name found in both dirs.
    source_dir = user_filesystem["user-repo-dir"]
    dir_already_containing_duplicate_file = home_dir / "duplicated-dir"
    dir_already_containing_duplicate_file.mkdir()
    duplicate_file = dir_already_containing_duplicate_file / "usepackages.txt"
    duplicate_file.touch()
    assert duplicate_file.exists()
    with pytest.raises(
        FileExistsError,
        match=(
            f"{duplicate_file.name} already exists in "
            f"{str(dir_already_containing_duplicate_file)}. Please either "
            "remove this from the user-defined GitHub repo, "
            "or leave an issue on GitHub if you think the problem is with "
            "scikit-package."
        ),
    ):
        copy_all_files(source_dir, dir_already_containing_duplicate_file)


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
    home_dir = user_filesystem["home-dir"]
    # a non-existing dir
    project_dir_with_header = home_dir / "project-dir-with-header"
    project_dir_with_header.mkdir()
    manuscript_path = user_filesystem["manuscript-path"]
    manuscript_in_project = project_dir_with_header / "manuscript.tex"
    shutil.copy(manuscript_path, manuscript_in_project)
    source_dir = user_filesystem["user-repo-dir"]
    for file_name in existing_files:
        source = source_dir / file_name
        dest = project_dir_with_header / file_name
        shutil.copy(source, dest)
    load_headers(project_dir_with_header)
    actual_manuscript_content = manuscript_in_project.read_text()
    assert expected_manuscript_content == actual_manuscript_content


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
            r"""
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
    home_dir = user_filesystem["home-dir"]
    manuscript_path = user_filesystem["manuscript-path"]
    # a non-existing dir
    project_dir_with_bib = home_dir / "project-dir-with-bib"
    project_dir_with_bib.mkdir()
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
    home_dir = user_filesystem["home-dir"]
    project_dir_without_manuscript = (
        home_dir / "project-dir-without-manuscript"
    )
    project_dir_without_manuscript.mkdir()
    with pytest.raises(
        FileNotFoundError,
        match=(
            "Unable to find manuscript.tex in "
            f"{str(project_dir_without_manuscript)}. "
            "Please leave an issue on GitHub."
        ),
    ):
        load_bib_info(project_dir_without_manuscript)


# C1: use a template with manuscrip.tex and a GitHub repo with usepackages.txt,
#   newcommands.txt and bib files. Expect usepackages, commands and bib info
#   are inserted into the manuscrip.tex
def test_initialize_project():
    assert False

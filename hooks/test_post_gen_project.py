from pathlib import Path

import pytest

from hooks.post_gen_project import copy_journal_template_files, load_headers


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
            "files. Please contact the software "
            "developers.",
        ),
        # C2: desired template does not exist. Expect FileNotFoundError
        (
            "yet-another",
            "Cannot find the provided journal_template: "
            "yet-another. Please contact the "
            "software developers.",
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


@pytest.mark.parametrize(
    "missing_files, expected_manuscript_content",
    [
        # C1: `usepackages.txt` and `newcommands.txt` exist in the
        #   headers_path and there are several usepackages lines in the
        #   manuscript.
        #   Expect packages and commands are inserted into the manuscript in
        #   a order that packages come before commands.
        (
            [],
            r"""
    \documentclass{article}
    \usepackage{package-from-user-usepackage}
    \usepackage{package-in-manuscript}
    \newcommand{\command_in_manuscript}
    \newcommand{\command_from_user_newcommands}{}
    \begin{document}
    Contents of manuscript
    \bibliography{bib-in-manuscript}
    \bibliographystyle{chicago}
    \end{document}
""",
        ),
        # C2: Only `usepackages.txt`is missing. Expect commands are inserted
        #   after manuscript's usepackages and keeping the original packages
        #   and commands in the manuscript.
        (
            ["usepackages.txt"],
            r"""
    \documentclass{article}
    \usepackage{package-in-manuscript}
    \newcommand{\command_in_manuscript}
    \newcommand{\command_from_user_newcommands}{}
    \begin{document}
    Contents of manuscript
    \bibliography{bib-in-manuscript}
    \bibliographystyle{chicago}
    \end{document}
""",
        ),
        # C3: Only `newcommands.txt`is missing. Expect packages are inserted
        #   before manuscript's usepackages and keeping the original packages
        #   and commands in the manuscript.
        (
            ["newcommands.txt"],
            r"""
    \documentclass{article}
    \usepackage{package-from-user-usepackage}
    \usepackage{package-in-manuscript}
    \newcommand{\command_in_manuscript}
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
    missing_files,
    expected_manuscript_content,
    user_repo_files_and_contents,
):
    source_dir = user_filesystem / "source-dir"
    manuscript_path = (
        user_filesystem
        / ".cookiecutters"
        / "scikit-package-manuscript"
        / "templates"
        / "article"
        / "manuscript_with_headers_and_bib.tex"
    )
    for file in missing_files:
        Path(source_dir / file).unlink()

    for key in user_repo_files_and_contents:
        if key not in missing_files:
            assert Path(source_dir / key).exists()
        else:
            assert not Path(source_dir / key).exists()

    load_headers(source_dir, manuscript_path)
    actual_manuscript_content = manuscript_path.read_text()

    assert expected_manuscript_content == actual_manuscript_content

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
    "missed_file_names, expect_headers",
    [
        # C1: `usepackage.txt` and `newcommands.txt` exist in the headers_path,
        #   and there are several usepackage lines in the manuscript.
        #   Expect packages and commands are inserted into the manuscript in
        #   a order that packages come before commands.
        (
            [],
            r"""
    \usepackage{graphicx}
    \usepackage{amsmath}
    \renewcommand{\vec}[1]{\mathbf{#1}}
""",
        ),
        # C2: Only `usepackage.txt`is missed. Expect commands are inserted
        #   after manuscript's usepackages.
        (
            ["usepackage.txt"],
            r"""
    \usepackage{amsmath}
    \renewcommand{\vec}[1]{\mathbf{#1}}
""",
        ),
        # C3: Only `newcommands.txt`is missed. Expect packages are inserted
        #   before manuscript's usepackages.
        (
            ["newcommands.txt"],
            r"""
    \usepackage{graphicx}
    \usepackage{amsmath}
""",
        ),
    ],
)
def test_load_headers(user_filesystem, missed_file_names, expect_headers):
    source_dir = user_filesystem / "source-dir"
    manuscript_path = (
        user_filesystem
        / ".cookiecutters"
        / "scikit-package-manuscript"
        / "templates"
        / "article"
        / "manuscript.tex"
    )
    for file in missed_file_names:
        Path(source_dir / file).unlink()
    load_headers(source_dir, manuscript_path)
    manuscript_lines = manuscript_path.read_text().splitlines()
    actual_headers = ""
    for line in manuscript_lines[1:]:
        if line.startswith(r"\begin{document}"):
            break
        else:
            actual_headers += line
    assert expect_headers == actual_headers

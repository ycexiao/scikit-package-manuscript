from pathlib import Path

import pytest

from hooks.post_gen_project import copy_journal_template_files


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


# C1: `usepackage.txt` and `newcommands.txt` exist in the headers_path,
#   several usepackage lines in the manuscript.
#   Expect packages and commands are inserted into the manuscript in
#   a order that packages come before commands.
# C2: empty `usepackage.txt` and `newcommands.txt` exist in the headers_path,
#   several usepackage lines in the manuscript.
#   Expect the content of manuscript doesn't change.
def test_load_headers():
    pass


# C1: `usepackage.txt` doesn't exist. Expect FileNotFoundError.
# C2: `newcommands.txt` doesn't exist. Expect FileNotFoundError.
# C3: manuscript path doesn't exist. Expect FileNotFoundError.
def test_load_headers_bad():
    pass

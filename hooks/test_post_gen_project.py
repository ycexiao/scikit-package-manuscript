from pathlib import Path

import pytest
from post_gen_project import (
    copy_bib_from_local,
    copy_journal_template_files,
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


# C1: file containing bib files and non bib files.
#   Expect all files copied to project-dir
#   but only bib files have their names returned.
def test_copy_bib_from_local(user_filesystem, bib_files, mock_home):

    # directory
    mix_bib_dir_path = user_filesystem / "mix-bib-dir"
    project_dir = user_filesystem / "project-dir"
    actual_bib_names = copy_bib_from_local(mix_bib_dir_path, project_dir)
    for item in mix_bib_dir_path.glob("**/*"):
        copied_path = project_dir / item.name
        assert copied_path.exists()

    expected_bib_names = bib_files.keys()
    assert set(expected_bib_names) == set(actual_bib_names)


# C1: a not existed path. Expect FileNotFoundError
def test_copy_bib_from_local_bad(user_filesystem, mock_home):
    project_dir = user_filesystem / "project-dir"

    # directory
    other_bib_path = user_filesystem / "other-bib-dir"
    with pytest.raises(
        FileNotFoundError,
        match= 
        f"Cannot find {str(other_bib_path)}. "
         "Please try again after running " 
        f"'touch {str(other_bib_path)}'."
    ):
        copy_bib_from_local(str(other_bib_path), project_dir)
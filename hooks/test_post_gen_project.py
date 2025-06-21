from pathlib import Path

import pytest
from post_gen_project import (
    copy_bib_from_local,
    copy_journal_template_files,
    get_bib_path_type,
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


def test_get_bib_path_type(user_filesystem, bib_files, mock_repo_exists):
    # C1, github repo url, expect return "url"
    bib_path = "https://github.com/some/repo"
    expected_type = "url"
    actual_type = get_bib_path_type(bib_path)
    assert expected_type == actual_type

    # C2, a existed dir path, expect return "local"
    bib_dir_path = user_filesystem / "bib-dir"
    expected_type = "local"
    actual_type = get_bib_path_type(str(bib_dir_path))
    assert expected_type == actual_type

    # C3, a existed file path
    a_bib_file = list(bib_files.keys())[0]
    a_bib_path = bib_dir_path / a_bib_file
    expected_type = "local"
    actual_type = get_bib_path_type(str(a_bib_path))
    assert expected_type == actual_type


@pytest.mark.parametrize(
    "bib_path, errormessage",
    [
        # C1, a not existing github repo. Expected FileNotFoundError
        (
            "https://github.com/some/repo",
            "Cannot find Github repo https://github.com/some/repo. "
            "Please make sure the URL is correct.",
        ),
        # C2, a not existing dir path. Expect FileNotFoundError
        (
            "another-bib-dir",
            "Cannot find another-bib-dir. "
            "Please try again after running "
            "'touch another-bib-dir'.",
        ),
        # C3, a not existing file path. Expect FileNotFoundError
        (
            "another-bib.bib",
            "Cannot find another-bib.bib. "
            "Please try again after running "
            "'touch another-bib.bib'.",
        ),
    ],
)
def test_get_bib_path_type_bad(bib_path, errormessage, mock_repo_not_exists):
    with pytest.raises(FileNotFoundError, match=errormessage):
        get_bib_path_type(bib_path)


# C1: one bib dir, expect all bib files will be copied to project_path,
#   and all bib names will be returned
# C2: one bib file, expect the bib file will be copied and the bib name will be
#   returned
def test_copy_bib_from_local(user_filesystem, bib_files, mock_home):

    # directory
    bib_dir_path = user_filesystem / "bib-dir"
    project_dir = user_filesystem / "project-dir"
    project_dir.mkdir(parents=True, exist_ok=True)
    actual_bib_names = copy_bib_from_local(bib_dir_path, project_dir)
    for key, value in bib_files.items():
        assert Path(project_dir / key).exists()
        assert Path(project_dir / key).read_text() == value
    expected_bib_names = bib_files.keys()
    assert set(expected_bib_names) == set(actual_bib_names)

    # file
    key = list(bib_files.keys())[0]
    a_bib_path = bib_dir_path / key
    project_dir = user_filesystem / "other-project-dir"
    project_dir.mkdir(parents=True, exist_ok=True)
    expected_bib_name = a_bib_path.name
    actual_bib_name = copy_bib_from_local(a_bib_path, project_dir)[0]
    assert Path(project_dir / actual_bib_name).exists()
    assert Path(project_dir / actual_bib_name).read_text() == bib_files[key]
    assert expected_bib_name == actual_bib_name


# C1: dir without bib files. Expect FileNotFoundError
# C2: file that is not bib file. Expect FileNotFoundError
def test_copy_bib_from_local_bad(user_filesystem, mock_home):
    project_dir = user_filesystem / "project-dir"
    project_dir.mkdir(parents=True, exist_ok=True)

    # directory
    empty_bib_dir_path = user_filesystem / "empty-bib-dir"
    empty_bib_dir_path.mkdir(parents=True, exist_ok=True)
    files = ["README.md", "example.tex"]
    for file in files:
        file_path = empty_bib_dir_path / file
        file_path.touch()
    with pytest.raises(
        FileNotFoundError,
        match=f"Cannot find bib files in "
        f"{str(empty_bib_dir_path)}. Please create "
        f"bib files in {str(empty_bib_dir_path)}",
    ):
        copy_bib_from_local(str(empty_bib_dir_path), project_dir)

    # file
    not_bib_file = user_filesystem / "README.md"
    with pytest.raises(
        FileNotFoundError,
        match=f"Cannot find bib files in "
        f"{str(not_bib_file)}. Please create "
        f"bib files in {str(not_bib_file)}",
    ):
        copy_bib_from_local(str(not_bib_file), project_dir)

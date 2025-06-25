from pathlib import Path

import pytest

from hooks.post_gen_project import copy_all_files, copy_journal_template_files


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


# C1: existing source dir and target dir.
#  Expect all files in source dir are copied to target dir.
def test_copy_all_files(user_filesystem, user_repo_files_and_contents):
    source_dir = user_filesystem / "source-dir"
    target_dir = user_filesystem / "target-dir"
    copy_all_files(source_dir, target_dir)
    for key, value in user_repo_files_and_contents.items():
        file_path = target_dir / key
        assert file_path.exists()
        assert file_path.read_text() == value


# C1: an not existing source dir and an existing target dir.
#  Expect FileNotFoundError.
# C2: an empty source dir and an existing target dir.
#  Expect FlileNotFoundError.
# C3: existing source dir and target dir, but a file name exists in both dir.
#  Expect NameError.
def test_copy_all_files_bad(user_filesystem):
    source_dir = user_filesystem / "other-dir"
    assert not source_dir.exists()
    target_dir = user_filesystem / "target-dir"
    with pytest.raises(
        FileNotFoundError,
        match=f"Cannot find the source directory: "
        f"{str(source_dir)}. Please contact the "
        f"software developers.",
    ):
        copy_all_files(source_dir, target_dir)

    empty_dir = user_filesystem / "empty-dir"
    with pytest.raises(
        FileNotFoundError,
        match=f"Source directory {str(empty_dir)} found "
        f"but it contains no files. Please contact the "
        f"software developers.",
    ):
        copy_all_files(empty_dir, target_dir)

    source_dir = user_filesystem / "source-dir"
    dir_with_duplicated_file = user_filesystem / "duplicated-dir"
    dest = dir_with_duplicated_file / "usepackage.txt"
    with pytest.raises(
        NameError,
        match=f"{dest.name} already exists in "
        f"{str(dir_with_duplicated_file)}. Please either remove "
        f"this from the user-defined GitHub repo, "
        f"or contact the developers if you think the issue is with "
        " scikit-package",
    ):
        copy_all_files(source_dir, dir_with_duplicated_file)

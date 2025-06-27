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
    source_dir = user_filesystem / "source-dir"
    target_dir = user_filesystem / "target-dir"
    copy_all_files(source_dir, target_dir)
    for key, value in user_repo_files_and_contents.items():
        file_path = target_dir / key
        assert file_path.exists()
        assert file_path.read_text() == value


# C1: An nonexistent source dir and an existing target dir.
#  Expect FileNotFoundError.
# C2: An empty source dir and an existing target dir.
#  Expect FlileNotFoundError.
# C3: Existing source dir and target dir, but a file exists in both dir.
#  Expect FileExistsError.
def test_copy_all_files_bad(user_filesystem):
    # nonexistent source directory
    source_dir = user_filesystem / "other-dir"
    assert not source_dir.exists()
    target_dir = user_filesystem / "target-dir"
    with pytest.raises(
        FileNotFoundError,
        match="Unable to find the source directory: "
        f"{str(source_dir)}. Please leave an issue "
        "on GitHub.",
    ):
        copy_all_files(source_dir, target_dir)

    # empty source directory
    source_dir = user_filesystem / "empty-dir"
    assert source_dir.exists() and (not any(source_dir.iterdir()))
    with pytest.raises(
        FileNotFoundError,
        match=f"Source directory {str(source_dir)} found "
        "but it contains no files. Please leave an issue "
        "on GitHub.",
    ):
        copy_all_files(source_dir, target_dir)

    # target directory with duplicated file
    source_dir = user_filesystem / "source-dir"
    dir_with_duplicated_file = user_filesystem / "duplicated-dir"
    source_file = source_dir / "usepackage.txt"
    dest_file = dir_with_duplicated_file / "usepackage.txt"
    assert (
        source_dir.exists()
        and dir_with_duplicated_file.exists()
        and source_file.exists()
        and dest_file.exists()
    )
    with pytest.raises(
        FileExistsError,
        match=f"{dest_file.name} already exists in "
        f"{str(dir_with_duplicated_file)}. Please either remove "
        "this from the user-defined GitHub repo, "
        "or leave an issue on GitHub if you think the problem is with "
        "scikit-package.",
    ):
        copy_all_files(source_dir, dir_with_duplicated_file)

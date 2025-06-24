import pytest
from post_gen_project import copy_all_files


# C1: two valid directory path.
#  Expect all files in the source dir are copied to the target dir.
def test_copy_all_files(user_filesystem, repo_files):
    soruce_dir = user_filesystem / "cloned-dir"
    target_dir = user_filesystem / "project-dir"
    copy_all_files(soruce_dir, target_dir)
    for key, value in repo_files.items():
        copied_path = target_dir / key
        assert copied_path.exists()
        assert copied_path.read_text() == value


# C1: source_dir is invalid.
#  Expect FileNotFoundError.
def test_copy_all_file_bad(user_filesystem):
    source_dir = user_filesystem / "other-dir"
    assert not source_dir.exists()
    target_dir = user_filesystem / "project-dir"
    with pytest.raises(
        FileNotFoundError,
        match=f"Cannot find the source directory: "
        f"{str(source_dir)}. Please contact the "
        f"software developers.",
    ):
        copy_all_files(source_dir, target_dir)

from pathlib import Path

import pytest
from post_gen_project import copy_journal_template_files


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


# C1: template exists no files in the template. Expect FileNotFoundError
# C2: desired template does not exist. Expect FileNotFoundError
def test_copy_journal_template_files_bad(user_filesystem, mock_home):
    project_dir = Path(user_filesystem / "project-dir")
    project_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(
        FileNotFoundError,
        match="Template other found but it contains no "
        "files. Please contact the software "
        "developers.",
    ):
        # "other" exists but is empty
        copy_journal_template_files("other", project_dir)
    with pytest.raises(
        FileNotFoundError,
        match="Cannot find the provided journal_template: "
        "yet-another. Please contact the "
        "software developers.",
    ):
        # template "yet-another" doesn't exist and doesn't have a directory
        copy_journal_template_files("yet-another", project_dir)

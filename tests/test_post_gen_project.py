import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
from hooks.post_gen_project import (  # noqa: E402
    copy_journal_template_files,
    get_repo_dir,
)


def test_get_repo_dir(monkeypatch, user_filesystem):
    home_dir = user_filesystem[0]
    monkeypatch.setenv("HOME", str(home_dir))
    repo_path = home_dir / ".cookiecutters" / "scikit-package-manuscript"

    assert repo_path == get_repo_dir()


def test_without_repo_get_repo_dir(monkeypatch, user_filesystem_without_repo):
    home_dir = user_filesystem_without_repo[0]
    monkeypatch.setenv("HOME", str(home_dir))
    with pytest.raises(FileNotFoundError) as exc_info:
        get_repo_dir()
    assert "Couldn't find scikit-package-manuscript," in str(exc_info.value)


def test_copy_journal_template_files(monkeypatch, user_filesystem):
    home_dir = user_filesystem[0]
    monkeypatch.setenv("HOME", str(home_dir))
    journal_template = "article"
    project_dir = user_filesystem[1]
    project_dir = copy_journal_template_files(journal_template, project_dir)
    manuscript_file = project_dir / "manuscript.tex"
    assert manuscript_file.exists()


def test_without_template_copy_journal_template_files(
    monkeypatch, user_filesystem_without_template
):
    home_dir = user_filesystem_without_template[0]
    monkeypatch.setenv("HOME", str(home_dir))
    journal_template = "article"
    project_dir = user_filesystem_without_template[1]
    with pytest.raises(NotADirectoryError) as exc_info:
        project_dir = copy_journal_template_files(journal_template, project_dir)
    assert "Cannot find the provided journal_tamplate: " in str(exc_info.value)

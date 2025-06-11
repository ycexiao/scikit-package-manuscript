import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
from hooks.post_gen_project import get_repo_dir


def test_with_repo_get_repo_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    ck_path = tmp_path / ".cookiecutters"
    ck_path.mkdir()
    repo_path = ck_path / "scikit-package-manuscript"
    repo_path.mkdir()

    assert get_repo_dir() == repo_path


def test_without_repo_get_repo_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    ck_path = tmp_path / ".cookiecutters"
    ck_path.mkdir()
    repo_path = ck_path / "foo"
    repo_path.mkdir()
    repo_path = ck_path / "bar"
    repo_path.mkdir()

    with pytest.raises(FileNotFoundError) as exc_info:
        get_repo_dir()
        print(str(exc_info))
        assert (
            str(exc_info) == f"couldn't find scikit-package-manuscript, but did "
            f"find foo, bar"
        )

import pytest


@pytest.fixture
def user_filesystem(tmp_path):
    # create a filesystem with an empty ".cookiecutters" directory.
    cwd_dir = tmp_path / "cwd_dir"
    cwd_dir.mkdir()
    ck_path = tmp_path / ".cookiecutters"
    ck_path.mkdir()

    yield tmp_path, ck_path, cwd_dir


@pytest.fixture
def user_filesystem_with_repo(tmp_path):
    # create a filesystem with an empty ".cookiecutters" directory.
    cwd_dir = tmp_path / "cwd_dir"
    cwd_dir.mkdir()
    ck_path = tmp_path / ".cookiecutters"
    ck_path.mkdir()
    skm_path = ck_path / "scikit-package-manuscript"
    skm_path.mkdir()

    yield tmp_path, skm_path, cwd_dir
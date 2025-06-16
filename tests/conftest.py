import pytest


@pytest.fixture
def user_filesystem(tmp_path):
    # create a filesystem with all expected files.
    ck_path = tmp_path / ".cookiecutters"
    ck_path.mkdir()
    repo_path = ck_path / "scikit-package-manuscript"
    repo_path.mkdir()
    cwd_dir = tmp_path / "cwd_dir"
    cwd_dir.mkdir()

    manuscript_path = repo_path / "templates" / "article" / "manuscript.tex"
    manuscript_path.parent.mkdir(parents=True, exist_ok=True)
    manuscript_path.touch()

    yield tmp_path, cwd_dir


@pytest.fixture
def user_filesystem_without_repo(tmp_path):
    # Create a filesystem without the "scikit-package-manuscript" repo cloned.
    ck_path = tmp_path / ".cookiecutters"
    ck_path.mkdir()
    repo_path = ck_path / "foo"
    repo_path.mkdir()
    cwd_dir = tmp_path / "cwd_dir"
    cwd_dir.mkdir()
    yield tmp_path, cwd_dir


@pytest.fixture
def user_filesystem_without_template(tmp_path):
    # Create a filesystem without the "article" template in the "scikit-package-manuscript" repo.
    ck_path = tmp_path / ".cookiecutters"
    ck_path.mkdir()
    repo_path = ck_path / "scikit-package-manuscript"
    repo_path.mkdir()
    cwd_dir = tmp_path / "cwd_dir"
    cwd_dir.mkdir()

    manuscript_path = repo_path / "templates" / "foo" / "manuscript.tex"
    manuscript_path.parent.mkdir(parents=True, exist_ok=True)
    manuscript_path.touch()

    yield tmp_path, cwd_dir

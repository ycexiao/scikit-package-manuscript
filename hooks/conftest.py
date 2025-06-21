from pathlib import Path
from unittest import mock

import pytest

TEMPLATE_FILES = {
    "manuscript.tex": "Contents of manuscript.tex",
    "article.cls": "Contents of article.cls",
    "my-bib.bib": "Contents of my-bib.bib",
}

BIB_FILES = {
    "group.bib": "Contents of group.bib",
    "project.bib": "Contents of project.bib",
}


@pytest.fixture(scope="session")
def template_files():
    yield TEMPLATE_FILES


@pytest.fixture(scope="session")
def bib_files():
    yield BIB_FILES


@pytest.fixture
def mock_home(tmp_path):
    with mock.patch.object(Path, "home", return_value=tmp_path):
        yield tmp_path


@pytest.fixture
def mock_repo_exists():
    with mock.patch("post_gen_project.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        yield mock_get


@pytest.fixture
def mock_repo_not_exists():
    with mock.patch("post_gen_project.requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        yield mock_get


@pytest.fixture
def user_filesystem(tmp_path):
    # create a filesystem with spm in a .cookiecutters directory and
    # template directories called article, other, and another
    # the article template contains a set of files defined in TEMPLATE_FILES
    spm_path = Path(tmp_path / ".cookiecutters" / "scikit-package-manuscript")
    spm_path.mkdir(parents=True, exist_ok=True)

    template_names = ["other", "another"]
    for template_name in template_names:
        template_path = spm_path / "templates" / template_name
        template_path.mkdir(parents=True, exist_ok=True)

    article_path = Path(spm_path / "templates" / "article")
    article_path.mkdir(parents=True, exist_ok=True)
    for key, value in TEMPLATE_FILES.items():
        manuscript_path = article_path / key
        manuscript_path.write_text(value)

    bib_dir_path = tmp_path / "bib-dir"
    bib_dir_path.mkdir(parents=True, exist_ok=True)
    Path(tmp_path / "other-bib-dir-path").mkdir(parents=True, exist_ok=True)
    bib_files = []
    for filename, content in BIB_FILES.items():
        bib_file = bib_dir_path / filename
        bib_file.write_text(content)
        bib_files.append(bib_file)

    a_bib_file = tmp_path / "a-bib-file.bib"

    yield tmp_path

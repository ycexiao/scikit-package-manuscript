from pathlib import Path
from unittest import mock

import pytest

TEMPLATE_FILES = {
    "manuscript.tex": "Contents of manuscript.tex",
    "article.cls": "Contents of article.cls",
}

REPO_FILES = {
    "usepackage.txt": r"\usepackage{graphicx}",
    "newcommands.txt": r"\renewcommand{\vec}[1]{\mathbf{#1}}",
    "group-bib.bib": "Contents of group-bib.bib",
    "other.tex": "Contents of other.tex",
}


@pytest.fixture(scope="session")
def template_files():
    yield TEMPLATE_FILES


@pytest.fixture(scope="session")
def repo_files():
    yield REPO_FILES


@pytest.fixture
def mock_home(tmp_path):
    with mock.patch.object(Path, "home", return_value=tmp_path):
        yield tmp_path


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

    source_dir = tmp_path / "source-dir"
    source_dir.mkdir()
    target_dir = tmp_path / "target-dir"
    target_dir.mkdir()
    for key, value in REPO_FILES.items():
        file_path = source_dir / key
        file_path.write_text(value)

    empty_dir = tmp_path / "empty-dir"
    empty_dir.mkdir()

    dir_with_duplicated_file = tmp_path / "duplicated-dir"
    dir_with_duplicated_file.mkdir()
    key = "usepackage.txt"
    Path(dir_with_duplicated_file / key).touch()

    yield tmp_path

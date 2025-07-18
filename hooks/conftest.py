from pathlib import Path
from unittest import mock

import pytest

TEMPLATE_FILES = {
    "manuscript.tex": "Contents of manuscript.tex",
    "article.cls": "Contents of article.cls",
    "my-bib.bib": "Contents of my-bib.bib",
}


@pytest.fixture(scope="session")
def template_files():
    yield TEMPLATE_FILES


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
    yield tmp_path

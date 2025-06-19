import os
import pytest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
HOME = os.environ["HOME"]


@pytest.fixture
def user_filesystem(tmp_path):
    def add_dir(parent_dir, dirs):
        paths = []
        for tmp_dir in dirs:
            path = parent_dir / tmp_dir
            path.mkdir(parents=True, exist_ok=True)
            paths.append(path)
        return paths

    def add_files(parent_dir, files):
        paths = []
        for file in files:
            path = parent_dir / file
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
            paths.append(path)
        return paths

    def create_filesystem(cookiecutters, files):
        home_path = tmp_path
        os.environ["HOME"] = str(home_path)
        cookiecutters_path = home_path / ".cookiecutters"
        cookiecutters_path.mkdir()
        cwd_dir = home_path / "cwd_dir"
        cwd_dir.mkdir()

        cookiecutter_paths = add_dir(cookiecutters_path, cookiecutters)
        template_path = cookiecutters_path / "scikit-package-manuscript" / "templates" / "article"
        file_paths = add_files(template_path, files)

        return home_path, cookiecutter_paths

    yield create_filesystem
    os.environ["HOME"] = HOME


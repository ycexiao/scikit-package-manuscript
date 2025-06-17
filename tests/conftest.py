import pytest
import os 

HOME=os.environ["HOME"]

@pytest.fixture
def user_filesystem(tmp_path):
    # create a filesystem with an empty ".cookiecutters" directory.
    home_path = tmp_path
    os.environ['HOME'] = str(home_path)
    ck_path = home_path / ".cookiecutters"
    ck_path.mkdir()
    cwd_dir = home_path / "cwd_dir"
    cwd_dir.mkdir()
    yield home_path
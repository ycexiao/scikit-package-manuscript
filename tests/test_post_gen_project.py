import pytest
from hooks.post_gen_project import get_cookiecutter_dir, copy_journal_template_files



@pytest.mark.parametrize(
    # test the template are copied from cookiecutters. 
    #   Expect path can be found, and all files are copied.
    "cookiecutters", [
        # C1: with skm template and other templates, expect skm path will be returned.
        (["scikit-package-manuscript", "foo", "bar"]),
    ]
)
def test_get_cookiecutter_dir(user_filesystem, cookiecutters):
    home_path, cookiecutter_paths = user_filesystem(cookiecutters, [])
    expected_skm_path = home_path / ".cookiecutters" / "scikit-package-manuscript"
    actual_skm_path = get_cookiecutter_dir("scikit-package-manuscript")
    assert expected_skm_path == actual_skm_path


@pytest.mark.parametrize(
    # test the template are copied from cookiecutters. 
    #   Expect path can be found, and all files are copied.
    "cookiecutters, files", [
        # C1: with skm and a template file, expect skm will be found and all files will be copied.
        (["scikit-package-manuscript"], ["manuscript.tex"]),
        # C2: with skm and a template directory, expect skm will be found and all files will be copied.
        (["scikit-package-manuscirpt"], ["manuscript.tex", "style/article.cls", "style/article.bst"])
    ]
)
def test_copy_journal_template_files(user_filesystem, cookiecutters, files):
    home_path, expect_cookiecutter_paths = user_filesystem(cookiecutters, files)

    project_dir = home_path / "project_dir"
    project_dir.mkdir(parents=True, exist_ok=True)
    expceted_file_paths = [project_dir / file for file in files]
    copy_journal_template_files("article", project_dir)
    all_file_exists = []
    for file_path in expceted_file_paths:
        all_file_exists.append(file_path.exists())
    assert all(all_file_exists)
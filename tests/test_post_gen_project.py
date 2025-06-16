import os
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
from hooks.post_gen_project import (  # noqa: E402
    copy_journal_template_files,
    get_repo_dir,
)

@pytest.mark.parametrize("repos",[
    # test get_repo_dir when "scikit-package-manuscript" repo exists.
    # C1: with only "scikit-package-manuscript" repo
    ("scikit-package-manuscript",),
    # C2: with "scikit-package-manuscript" and other repos
    ("scikit-package-manuscript", "foo", "bar"),
]
)
def test_get_repo_dir(user_filesystem, repos):
    home_path, ck_path, cwd_path = user_filesystem
    skm_repo_path = home_path / ".cookiecutters" / "scikit-package-manuscript"
    os.environ["HOME"] = str(home_path)
    for repo in repos:
        repo_path = ck_path / repo
        repo_path.mkdir()
    actual = get_repo_dir()
    expected = skm_repo_path
    assert expected == actual


@pytest.mark.parametrize("repos",[
    # test get_repo_dir when "scikit-package-manuscript" repo does not exist.
    # C1: empty ".cookiecutters"
    (),
    # C2: without "scikit-package-manuscript"
    ("foo", "bar"),
]
)
def test_get_repo_dir_bad(user_filesystem, repos):
    home_path, ck_path, cwd_path = user_filesystem
    os.environ["HOME"] = str(home_path)
    for repo in repos:
        repo_path = ck_path / repo
        repo_path.mkdir()
    with pytest.raises(FileNotFoundError, match=r"Couldn't find scikit-package-manuscript,") as exc_info:
        get_repo_dir()

@pytest.mark.parametrize("existing_templates, template",[
    # test if copy_journal_template_files can find the expected template.
    # C1: with only one template
    (["article"], "article"),
    # C2: with multiple templates
    (["article", "foo", "bar"], "article")
]
)
def test_copy_journal_template_files_find_template(user_filesystem_with_repo, existing_templates, template):
    home_path, skm_repo_path, cwd_path = user_filesystem_with_repo
    os.environ["HOME"] = str(home_path)
    for existing_template in existing_templates:
        existing_template_path = skm_repo_path / "templates" / existing_template
        existing_template_path.mkdir(parents=True, exist_ok=True)
    
    cwd_path = copy_journal_template_files(template, cwd_path)


@pytest.mark.parametrize("existing_templates, template",[
    # test copy_journal_template_files when template is not existed.
    # C1: empty templates.
    ([], "article"),
    # C2: template does not exist.
    (["foo", "bar"], "article")
]
)
def test_copy_journal_template_files_find_template_bad(user_filesystem_with_repo, existing_templates, template):
    home_path, skm_repo_path, cwd_path = user_filesystem_with_repo
    os.environ["HOME"] = str(home_path)
    for existing_template in existing_templates:
        existing_template_path = skm_repo_path / "templates" / existing_template
        existing_template_path.mkdir(parents=True, exist_ok=True)

    with pytest.raises(NotADirectoryError, match=r"Cannot find the provided journal_tamplate: ") as exc_info:
        cwd_path = copy_journal_template_files(template, cwd_path)


@pytest.mark.parametrize("template_files",[
    # test copy_journal_template_files with different directory structure.
    # C1: empty template
    (),
    # C2: only one file in the template
    ("manuscript.tex"),
    # C3: multiple files in the template
    ("manuscript.tex","texstyle.cls","bibstyle.bst"),
    # C4: subdirectory in the template
    ("manuscript.tex", "style/texstyle.cls", "style/bibstyle.bst")
])
def test_copy_journal_template_files_copy_files(user_filesystem_with_repo, template_files):
    home_path, skm_repo_path, cwd_path = user_filesystem_with_repo
    os.environ["HOME"] = str(home_path)
    template_path = skm_repo_path/ "templates" / "article"
    template_path.mkdir(parents=True, exist_ok=True)
    for file in template_files:
        file_path = template_path / file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()

    project_path = cwd_path
    project_path = copy_journal_template_files(template_path, project_path)

    for file in template_files:
        file_path = project_path / file
        assert file_path.exists()


import os
import shutil
import subprocess
import pytest
from conftest import HOME
from hooks.post_gen_project import (  # noqa: E402
    copy_journal_template_files,
    get_cookiecutter_dir,
)


@pytest.mark.parametrize(
    "cookiecutters",
    [
        # test get_cookiecutter_dir when "scikit-package-manuscript"
        #   cookiecutter exists.
        # C1: with "scikit-package-manuscript" and other cookiecutters,
        #   expect return the path to "scikit-package-manuscript"
        ("scikit-package-manuscript", "foo", "bar"),
    ],
)
def test_get_cookiecutter_dir(user_filesystem, cookiecutters):
    home_path = user_filesystem
    for cookiecutter in cookiecutters:
        cookiecutter_path = home_path / ".cookiecutters" / cookiecutter
        cookiecutter_path.mkdir()
    actual = get_cookiecutter_dir()
    expected = home_path / ".cookiecutters" / "scikit-package-manuscript"
    assert expected == actual


@pytest.mark.parametrize(
    "cookiecutters",
    [
        # test get_cookiecutter_dir when "scikit-package-manuscript"
        #   cookiecutter does not exist.
        # C1: empty ".cookiecutters", expect FileNotFoundError.
        (),
        # C2: without "scikit-package-manuscript", expect FileNotFoundError.
        ("foo", "bar"),
    ],
)
def test_get_cookiecutter_dir_bad(user_filesystem, cookiecutters):
    home_path = user_filesystem
    ck_path = home_path / ".cookiecutters"
    for cookiecutter in cookiecutters:
        cookiecutter_path = ck_path / cookiecutter
        cookiecutter_path.mkdir()
    with pytest.raises(
        FileNotFoundError, match=r"Couldn't find scikit-package-manuscript,"
    ):
        get_cookiecutter_dir(cookiecutter_name="scikit-package-manuscript")


@pytest.mark.parametrize(
    "templates, expected_template",
    [
        # test if copy_journal_template_files can find the expected template.
        # C1: with multiple templates, expect no NotADiectoryError.
        (["article", "foo", "bar"], "article")
    ],
)
def test_copy_journal_template_files_find_template(
    user_filesystem, templates, expected_template
):
    home_path = user_filesystem
    skm_path = home_path / ".cookiecutters" / "scikit-package-manuscript"
    cwd_path = home_path / "cwd_dir"
    for template in templates:
        template_path = skm_path / "templates" / template
        template_path.mkdir(parents=True, exist_ok=True)
    copy_journal_template_files(expected_template, cwd_path)


@pytest.mark.parametrize(
    "templates, expected_template",
    [
        # test copy_journal_template_files when template is not existed.
        # C1: empty templates, expect NotADirectoryError.
        ([], "article"),
        # C2: template does not exist, expect NotADirectoryError.
        (["foo", "bar"], "article"),
    ],
)
def test_copy_journal_template_files_find_template_bad(
    user_filesystem, templates, expected_template
):
    home_path = user_filesystem
    skm_path = home_path / ".cookiecutters" / "scikit-package-manuscript"
    skm_path.mkdir(parents=True, exist_ok=True)
    cwd_path = home_path / "cwd_dir"
    for template in templates:
        template_path = skm_path / "templates" / template
        template_path.mkdir(parents=True, exist_ok=True)

    with pytest.raises(
        NotADirectoryError,
        match=r"Cannot find the provided journal_tamplate: ",
    ):
        cwd_path = copy_journal_template_files(expected_template, cwd_path)


@pytest.mark.parametrize(
    "template_files",
    [
        # test copy_journal_template_files with different journal
        #   template structure.
        # C1: empty template, expect nothing happens.
        (),
        # C2: multiple files in the template, expect all files will be copied
        #   to project_path
        ("manuscript.tex", "texstyle.cls", "bibstyle.bst"),
        # C3: subdirectory in the template, expect all files and folder will
        #   be copied into project_dir
        ("manuscript.tex", "style/texstyle.cls", "style/bibstyle.bst"),
    ],
)
def test_copy_journal_template_files_copy_files(
    user_filesystem, template_files
):
    home_path = user_filesystem
    template_path = (
        home_path
        / ".cookiecutters"
        / "scikit-package-manuscript"
        / "templates"
        / "article"
    )
    template_path.mkdir(parents=True, exist_ok=True)
    for file in template_files:
        file_path = template_path / file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()

    project_path = home_path / "cwd_dir"
    project_path = copy_journal_template_files("article", project_path)

    for file in template_files:
        file_path = project_path / file
        assert file_path.exists()


@pytest.mark.parametrize(
    "template",
    [
        # test the generated template, expect manuscript.pdf is successfully
        #   built in project_dir
        # C1: article template
        "article",
    ],
)
def test_build_manuscript(template, tmp_path, capsys):
    os.environ["HOME"] = HOME
    if shutil.which("latex") is not None:
        project_dir = tmp_path / "cwd_dir"
        project_dir.mkdir(parents=True, exist_ok=True)
        auxiliary_output = project_dir / "output_dir"
        auxiliary_output.mkdir()
        project_dir = copy_journal_template_files(template, project_dir)
        manuscript_file = project_dir / "manuscript.tex"
        result = subprocess.run(
            [
                "latex",
                f"-output-directory={str(auxiliary_output)}",
                str(manuscript_file),
            ]
        )
        if result.returncode != 0:
            with capsys.disabled():
                print(result.stdout)
                print(result.stderr)
            raise SyntaxError("Failed to build pdf from the templates: ",
                              f"{template}. Please contact the software ",
                              "developer"
                              )
    else:
        with capsys.disabled():
            print("Not found latex. Skip test for building pdf from ",
                  f"{template}.")

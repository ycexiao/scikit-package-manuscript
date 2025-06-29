from pathlib import Path

import pytest

from hooks.post_gen_project import copy_journal_template_files, load_bib_info


def _file_not_found_error_message(file_path):
    message = (
        "Unable to find the path: "
        f"{str(file_path)}. Please leave an issue "
        "on GitHub."
    )
    return message


# C1: multiple files in the template, expect all files will be copied
#   to project_path
def test_copy_journal_template_files(
    user_filesystem, template_files, mock_home
):
    project_dir = Path(user_filesystem / "project-dir")
    project_dir.mkdir(parents=True, exist_ok=True)
    copy_journal_template_files("article", project_dir)
    for key, value in template_files.items():
        assert Path(project_dir / key).exists()
        assert Path(project_dir / key).read_text() == value


@pytest.mark.parametrize(
    "input,errormessage",
    [
        # C1: template exists no files in the template. Expect
        # FileNotFoundError
        (
            "other",
            "Template other found but it contains no "
            "files. Please leave an issue on GitHub.",
        ),
        # C2: desired template does not exist. Expect FileNotFoundError
        (
            "yet-another",
            "Unable to find the provided journal_template: "
            "yet-another. Please leave an issue on GitHub.",
        ),
    ],
)
def test_copy_journal_template_files_bad(
    user_filesystem, mock_home, input, errormessage
):
    project_dir = Path(user_filesystem / "project-dir")
    project_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(
        FileNotFoundError,
        match=errormessage,
    ):
        copy_journal_template_files(input, project_dir)


# C1: There are bib files in the cloned directory.
#   Expect all bib name are inserted into manuscript,
#   and bib files are copied into manuscript's parent dir
#   exists.
# C2: There are no bib files in the cloned directory.
#   Expect manuscript bib entries will not be modified,
#   and no files are copied.
def test_load_bib_info(user_filesystem, template_files):
    source_dir = user_filesystem / "user-repo-dir"
    manuscript_path = (
        user_filesystem
        / ".cookiecutters"
        / "scikit-package-manuscript"
        / "templates"
        / "article"
        / "manuscript-in-spm.tex"
    )
    load_bib_info(source_dir, manuscript_path)
    actual_manuscript_content = manuscript_path.read_text()
    expected_manuscript_content = r"""
\documentclass{article}
\usepackage{package-in-manuscript}
\newcommand{\command_in_manuscript}[1]{\mathbf{#1}}
\begin{document}
Contents of manuscript
\bibliography{user-bib-file-1, user-bib-file-2}
\bibliography{bib-in-manuscript}
\bibliographystyle{chicago}
\end{document}
    """
    assert expected_manuscript_content == actual_manuscript_content
    manuscript_path.write_text(template_files["manuscript-in-spm.tex"])

    Path(source_dir / "user-bib-file-1.bib").unlink()
    Path(source_dir / "user-bib-file-2.bib").unlink()
    load_bib_info(source_dir, manuscript_path)
    actual_manuscript_content = manuscript_path.read_text()
    expected_manuscript_content = template_files["manuscript-in-spm.tex"]
    assert expected_manuscript_content == actual_manuscript_content
    manuscript_path.write_text(template_files["manuscript-in-spm.tex"])


# C1: The manuscript path doesn't exist. Expect file not found error.
def test_load_bib_info_bad(user_filesystem):
    source_dir = user_filesystem / "user-repo-dir"
    manuscript_path = user_filesystem / "not-existing-file"
    assert not manuscript_path.exists()

    with pytest.raises(
        FileNotFoundError, match=_file_not_found_error_message(manuscript_path)
    ):
        load_bib_info(source_dir, manuscript_path)

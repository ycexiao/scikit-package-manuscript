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
@pytest.mark.parametrize(
    "missing_files, error_message",
    [
        (
            [],
            r"""
\documentclass{article}
\usepackage{package-in-manuscript}
\newcommand{\command_in_manuscript}[1]{\mathbf{#1}}
\begin{document}
Contents of manuscript
\bibliography{bib-in-manuscript, user-bib-file-1, user-bib-file-2}
\bibliographystyle{chicago}
\end{document}
""",
        ),
        (
            ["user-bib-file-1.bib, user-bib-file-2.bib"],
            r""""
\documentclass{article}
\usepackage{package-in-manuscript}
\newcommand{\command_in_manuscript}[1]{\mathbf{#1}}
\begin{document}
Contents of manuscript
\bibliography{bib-in-manuscript, user-bib-file-1, user-bib-file-2}
\bibliographystyle{chicago}
\end{document}
""",
        ),
    ],
)
def test_load_bib_info(
    user_filesystem, template_files, missing_files, expected_manuscript_content
):
    source_dir = user_filesystem / "user-repo-dir"
    manuscript_path = (
        user_filesystem
        / ".cookiecutters"
        / "scikit-package-manuscript"
        / "templates"
        / "article"
        / "manuscript-in-spm.tex"
    )
    for file in missing_files:
        Path(source_dir / file).unlink()

    for file in source_dir.iterdir():
        if file.name in missing_files:
            assert not file.exists()
        else:
            assert file.exists()

    load_bib_info(source_dir, manuscript_path)
    actual_manuscript_content = manuscript_path.read_text()
    assert expected_manuscript_content == actual_manuscript_content
    manuscript_path.write_text(template_files["manuscript-in-spm.tex"])

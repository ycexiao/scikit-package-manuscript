from pathlib import Path
import shutil
import subprocess
import tempfile
from importlib.resources import as_file, files
import sys


from importlib.resources import files, as_file
from pathlib import Path
import shutil

def copy_package_files(resource_dir: str, target_dir: Path):
    """
    Copies all files from a package's internal resource directory to a target directory.

    Args:
        resource_dir (str): Subdirectory inside the package (relative to package root).
        target_dir (Path): Filesystem path to copy files to.
    """
    repo = "https://github.com/scikit-package/scikit-package-manuscript.git"
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Get the directory of resources
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        subprocess.run(["git", "clone", repo, str(tmp)], check=True)
        resource_dir = tmp_path / "templates" /resource_dir

        # Use as_file to ensure we get a real path (even if inside a zip)
        with as_file(resource_dir) as root_path:
            if not root_path.is_dir():
                raise NotADirectoryError(f"{resource_root} is not a directory")

            for item in root_path.iterdir():
                if item.is_file():
                    shutil.copy(item, target_dir / item.name)


def clone_headers(target_dir):
    repo = "https://github.com/Billingegroup/latex-headers"
    headers = ["packages.tex", "cmds-general.tex", "cmds-programs.tex"]
    target_path = Path(target_dir)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        subprocess.run(["git", "clone", repo, str(tmp_path)], check=True)
        src_dir = tmp_path / "latex_headers"
        for filename in headers:
            src = src_dir / filename
            dst = target_path / filename
            if not src.is_file():
                raise FileNotFoundError(f"Missing file: {src}")
            shutil.copy(src, dst)

def load_template(source_dir, target_dir):
    source_path = Path(source_dir)
    target_path = Path(target_dir)

    if not source_path.is_dir():
        raise NotADirectoryError(f"Source is not a directory: {source_path}")
    target_path.mkdir(parents=True, exist_ok=True)

    for item in source_path.iterdir():
        dest = target_path / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)


def main():
    sys.path.append(str(Path().cwd().parent))
    target_directory = Path().cwd()
    copy_package_files("{{ cookiecutter.journal_template }}", target_directory)
    clone_headers(target_directory)
    # template_directory = Path().cwd() / cookiecutter.template
    # load_template(template_directory, target_directory)


if __name__ == "__main__":
    main()

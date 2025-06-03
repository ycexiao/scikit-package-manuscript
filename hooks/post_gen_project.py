from pathlib import Path
import shutil
import subprocess
import tempfile
from importlib.resources import as_file, files
import sys
import re


from importlib.resources import files, as_file
from pathlib import Path
import shutil

def copy_package_files(package: str, resource_dir: str, target_dir: Path):
    """
    Copies all files from a package's internal resource directory to a target directory.

    Args:
        package (str): Dotted path to the package (e.g., "mypackage.resources").
        resource_dir (str): Subdirectory inside the package (relative to package root).
        target_dir (Path): Filesystem path to copy files to.
    """
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Get the directory of resources
    resource_root = files(package) / resource_dir

    # Use as_file to ensure we get a real path (even if inside a zip)
    with as_file(resource_root) as root_path:
        if not root_path.is_dir():
            raise NotADirectoryError(f"{resource_root} is not a directory")

        for item in root_path.iterdir():
            if item.is_file():
                shutil.copy(item, target_dir / item.name)


def clone_headers(target_dir, repo_url):
    target_path = Path(target_dir)
    package_names = []
    command_names = []    
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        subprocess.run(["git", "clone", repo_url, str(tmp_path)], check=True)
        src_dir = tmp_path
        for item in src_dir.glob('**/*'):
            if item.is_file() and str(item).endswith(".tex"):
                item_name = str(item).split('/')[-1]
                if item_name.startswith('package'):
                    package_names.append(item_name)
                elif item_name.startswith('cmd'):
                    command_names.append(item_name)
                else:
                    package_names.append(item_name)
                shutil.copy(item, target_dir / item_name)

    return package_names, command_names

def sort_cmd_headers(command_names):
    order = []
    with_order_index = []
    without_order_index = []
    for i,name in enumerate(command_names):
        item_order = re.findall(r'\d+', name)
        if len(item_order)==0:
            without_order_index.append(i)
        else:
            order.append(int(item_order[0]))
            with_order_index.append(i)

    order_index = sorted(range(len(order)), key = lambda i: order[i])
    with_order_index = [with_order_index[i] for i in order_index]
    sorted_index = [*with_order_index, *without_order_index]
    command_names = [command_names[i] for i in sorted_index]
    return command_names

def create_input_files(target_dir, package_names, command_names):
    target_path = Path(target_dir)
    package_path = target_path / 'auto-fetch-packages.tex'
    command_path = target_path / 'auto-fetch-commands.tex'

    with open(package_path, 'w') as f:
        for name in package_names:
            f.write(r"\input{" + str(name) + '}')
            f.write('\n')

    with open(command_path, 'w') as f:
        for name in command_names:
            f.write(r"\input{" + str(name) + '}')
            f.write('\n')



def main():
    sys.path.append(str(Path().cwd().parent))
    target_directory = Path().cwd()

    copy_package_files("scikit-package-manuscript.templates", "{{ cookiecutter.journal_template }}", target_directory)
    package_names, command_names = clone_headers(target_directory, "{{ cookiecutter.latex_headers_repo }}")
    command_names = sort_cmd_headers(command_names)

    create_input_files(target_directory, package_names, command_names)


if __name__ == "__main__":
    main()

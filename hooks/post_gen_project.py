from pathlib import Path
import shutil
import subprocess
import tempfile
from importlib.resources import as_file, files
import sys
import re



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


def clone_headers(repo_url):
    """
    Clone a Git repository containing LaTeX header files into a string.
    """
    headers = ""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        subprocess.run(["git", "clone", repo_url, str(tmp_path)], check=True)

        for item in tmp_path.glob('**/*'):
            if item.is_file() and str(item).endswith(".tex"):
                headers += item.read_text()+'\n'

    return headers

def extract_blocks(header_str):
    """
    Extracts blocks from a LaTeX header string.
    """
    lines = header_str.splitlines()
    keyword_pattern = re.compile(r'^\\([a-zA-Z]+)(?=\{|\[)')
    name_pattern = re.compile(r'(?<=\{)(.*?)(?=\})')
    blocks = []

    open_braces = 0
    next_line_same_block = False

    for i, line in enumerate(lines):
        if line.strip().startswith('%') or not line.strip():
            continue

        else:
            if next_line_same_block:
                blocks[-1]['content'] += line.rstrip() + '\n'
                open_braces += line.count('{') - line.count('}')
                if open_braces == 0:
                    next_line_same_block=False
                continue

            else:
                keywoard_match = keyword_pattern.findall(line)
                name_match = name_pattern.findall(line)
                if not keywoard_match or not name_match:
                    print(keywoard_match, name_match)
                    raise ValueError(f"Invalid block header: {line}")
                
                block = {}
                block['content'] = line.strip() + '\n'
                block['keyword'] = keywoard_match[0].strip()
                block['name'] = name_match[0].strip()
                blocks.append(block)

                open_braces += line.count('{') - line.count('}')
                if open_braces != 0:
                    next_line_same_block = True
    return blocks

def sort_blocsks(blocks):
    """
    Classify extracted blocks into package and command blocks and sort each type of the blocks alpha-numerically by their names.
    """
    package_keyword = ['usepackage', 'documentclass']
    command_keyword = ['newcommand', 'renewcommand', 'providecommand']

    package_blocks = []
    command_blocks = []

    for i in range(len(blocks)):
        if blocks[i]['keyword'] in package_keyword:
            package_blocks.append(blocks[i])
        elif blocks[i]['keyword'] in command_keyword:
            command_blocks.append(blocks[i])
        else:
            command_blocks.append(blocks[i])  # treat as command if not recognized

    get_alphanum_key = lambda s:  [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]
    package_blocks = sorted(package_blocks, key=lambda x: get_alphanum_key(x['name']))
    command_blocks = sorted(command_blocks, key=lambda x: get_alphanum_key(x['name']))
    return package_blocks, command_blocks
    
    
def insert_blocks(target_dir, package_blocks, command_blocks):
    """
    Inserts LaTeX header blocks into the manuscript.tex file in the target directory after the \documentclass line.
    """
    target_path = Path(target_dir) / "manuscript.tex"
    before_insert_region = ""
    after_insert_region = ""
    before_insert = True
    insert_start = "\\documentclass"
    with open(target_path, 'r') as f:
        for line in f:
            if before_insert:
                before_insert_region += line
            else:
                after_insert_region += line

            if len(line)>= len(insert_start) and line[:len(insert_start)] == insert_start:
                before_insert = False
                before_insert_region += "\n% Start of inserted headers\n"
                after_insert_region += "% End of inserted headers\n" 
    
    headers_content = ""
    for block in package_blocks:    
        headers_content += block['content'] 
    for block in command_blocks:
        headers_content += block['content']
    
    new_content = before_insert_region + headers_content + after_insert_region

    with open(target_path, 'w') as f:
        f.write(new_content)

    print(f"Headers written to {target_path}")



def main():
    sys.path.append(str(Path().cwd().parent))
    target_directory = Path().cwd()
    copy_package_files("scikit-package-manuscript.templates", "{{ cookiecutter.journal_template }}", target_directory)
    headers = clone_headers("{{ cookiecutter.latex_headers_repo }}")
    header_blocks = extract_blocks(headers)
    package_blocks, command_blocks = sort_blocsks(header_blocks)

    insert_blocks(target_directory , package_blocks, command_blocks)


if __name__ == "__main__":
    main()

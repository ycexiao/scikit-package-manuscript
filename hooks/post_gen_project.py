import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

MANUSCRIPT_FILENAME = "manuscript.tex"


def copy_journal_template_files(journal_template, project_dir):
    """
    Copies files from a package's resource directory to a target directory.

    Parameters:
    ===========
    journal_template : str
      The name of the journal latex template to use. It must be
      one of the available templates.
    project_dir : Path
      The path to the location of the output project where the files
      will be copied to.
    """
    context_file = project_dir / "cookiecutter.json"
    if context_file.exists():
        with context_file.open("r", encoding="utf-8") as f:
            context = json.load(f)
        cookiecutter_path = Path(context.get("_repo_dir", "unknown")).resolve()
    else:
        print("cookiecutter.json not found in output directory.")

    # Get the directory of resources
    template_dir = cookiecutter_path / "templates" / journal_template
    if not template_dir.exists():
        raise NotADirectoryError(f"Cannot find the provided journal_tamplate: "
                                 f"{journal_template}. Please contact the "
                                 f"software developers")
    for item in template_dir.iterdir():
        dest = project_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)
    return project_dir


def get_user_headers(repo_url):
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


def extract_manuscript_packages(manuscript_path):
    contents = manuscript_path.read_text(encoding="utf-8")
    packages, the_rest = split_usepackage_lines(contents)
    Path(manuscript_path).write_text(the_rest, encoding="utf-8")
    return packages


def split_usepackage_lines(headers):
    usepackage_lines = []
    other_lines = []
    for line in headers.splitlines():
        if line.lstrip().startswith(r"\usepackage"):
            usepackage_lines.append(line)
        else:
            other_lines.append(line)
    return "\n".join(usepackage_lines), "\n".join(other_lines)


def insert_below_documentclass(manuscript_text, insert_text):
    lines = manuscript_text.splitlines()
    result_lines = []
    inserted = False
    for line in lines:
        result_lines.append(line)
        if not inserted and r"\documentclass" in line:
            result_lines.append(insert_text)
            inserted = True
    return "\n".join(result_lines)


def recompose_manuscript(manuscript_path, user_packages, user_commands):
    new_header = "\n".join([user_packages, user_commands])
    manuscript_contents = manuscript_path.read_text(encoding="utf-8")
    manuscript_contents_with_header = insert_below_documentclass(
        manuscript_contents, new_header
    )
    manuscript_path.write_text(
        manuscript_contents_with_header, encoding="utf-8"
    )


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
            else:
                keywoard_match = keyword_pattern.findall(line)
                name_match = name_pattern.findall(line)
                if not keywoard_match or not name_match:
                    raise ValueError(f"Invalid block header: {line}")
                block = {}
                block['content'] = line.strip() + '\n'
                block['keyword'] = keywoard_match[0].strip()
                block['name'] = name_match[0].strip()
                blocks.append(block)
                open_braces += line.count('{') - line.count('}')
            if open_braces != 0:
                next_line_same_block = True
            else:
                next_line_same_block = False
    return blocks


def sort_blocks(blocks):
    """
    Classify extracted blocks into package and command blocks

    Sort each type of the blocks alpha-numerically by their names.
    """
    package_keyword = ['usepackage']
    command_keyword = ['newcommand', 'renewcommand', 'providecommand']
    package_blocks = []
    command_blocks = []

    for i in range(len(blocks)):
        if blocks[i]['keyword'] in package_keyword:
            package_blocks.append(blocks[i])
        elif blocks[i]['keyword'] in command_keyword:
            command_blocks.append(blocks[i])
        else:
            command_blocks.append(blocks[i])

    package_blocks = sorted(package_blocks,
                            key=lambda x: get_alphanum_key(x['name']))
    command_blocks = sorted(command_blocks,
                            key=lambda x: get_alphanum_key(x['name']))
    return package_blocks, command_blocks


def get_alphanum_key(name):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', name)]


def insert_blocks(manuscript_file, package_blocks, command_blocks):
    """
    Inserts LaTeX header blocks into the manuscript.tex file

    Blocks are inserted after the \\documentclass line.
    """
    before_insert_region = ""
    after_insert_region = ""
    before_insert = True
    insert_start = "\\documentclass"
    with open(manuscript_file, 'r') as f:
        for line in f:
            if before_insert:
                before_insert_region += line
            else:
                after_insert_region += line
            if len(line) >= len(insert_start) \
                    and line[:len(insert_start)] == insert_start:
                before_insert = False
                before_insert_region += "\n% Start of inserted headers\n"
                after_insert_region += "% End of inserted headers\n"

    headers_content = ""
    for block in package_blocks:
        headers_content += block['content']
    for block in command_blocks:
        headers_content += block['content']
    new_content = before_insert_region + headers_content + after_insert_region

    with open(manuscript_file, 'w') as f:
        f.write(new_content)

    print(f"Headers written to {manuscript_file}")


def main():
    project_dir = Path().cwd()
    manuscript_path = project_dir / MANUSCRIPT_FILENAME
    copy_journal_template_files(
        "{{ cookiecutter.journal_template }}", project_dir
    )
    user_headers = get_user_headers(
        "{{ cookiecutter.latex_headers_repo }}"
    )
    manuscript_packages = extract_manuscript_packages(manuscript_path)
    user_packages, the_rest = split_usepackage_lines(user_headers)
    all_packages = "/n".join([manuscript_packages, user_packages])
    recompose_manuscript(manuscript_path, all_packages, the_rest)


if __name__ == "__main__":
    main()

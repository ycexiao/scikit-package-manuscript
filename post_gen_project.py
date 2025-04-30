import json
import os
import shutil


def main():
    template_dir = os.path.dirname(os.path.abspath(__file__))
    cookiecutter_json_path = os.path.join(template_dir, "cookiecutter.json")
    if not os.path.exists(cookiecutter_json_path):
        print("cookiecutter.json not found.")
        return

    with open(cookiecutter_json_path, "r") as f:
        cookiecutter_config = json.load(f)

    repo_name = cookiecutter_config.get("repo_name", "default_project")
    target_dir = os.path.join(os.getcwd(), repo_name)

    files_to_copy = [
        "bg-pdf-standards.bib",
        "billinge-group-bib.bib",
        "cmds_general.tex",
        "cmds_programs.tex",
        "iucr.bst",
        "iucrit.bst",
        "iucrjournals.cls",
        "packages.tex"
    ]

    for file_name in files_to_copy:
        source_file = os.path.join(template_dir, file_name)
        target_file = os.path.join(target_dir, file_name)
        if os.path.exists(source_file):
            shutil.copy(source_file, target_file)
            print(f"Copied {file_name} to the generated project.")
        else:
            print(f"Warning: {file_name} not found in the template directory.")


if __name__ == "__main__":
    main()

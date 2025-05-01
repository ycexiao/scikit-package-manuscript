import os
import shutil
import subprocess
import tempfile


def clone_headers(target_dir):
    repo = "https://github.com/Billingegroup/latex-headers"
    headers = ["packages.tex", "cmds_general.tex", "cmds_programs.tex"]

    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "clone", repo, tmp], check=True)
        src_dir = os.path.join(tmp, "latex_headers")
        for f in headers:
            src = os.path.join(src_dir, f)
            dst = os.path.join(target_dir, f)
            if not os.path.isfile(src):
                raise FileNotFoundError(f"Missing file: {src}")
            shutil.copy(src, dst)


def main():
    clone_headers(os.getcwd())


if __name__ == "__main__":
    main()

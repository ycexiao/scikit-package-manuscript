This is a Cookiecutter template for creating Overleaf LaTex paper repositories using Billinge group standards.

# Features:
- Auto-generates the repository name, paper title, and one author name.
- Uses the IUCR LaTeX template (`iucr.bst`, `iucrit.bst`, `iucrjournals.cls`, `fig1.png`).
- Includes dynamically generated files `cmds-general.tex`, `cmds-programs.tex`, and `packages.tex` from https://github.com/Billingegroup/latex-headers.
- Includes empty .bib files: `bg-pdf-standards.bib`, `billinge-group-bib.bib`, ``hand-coded.bib``, and ``repo_name.bib``.

# HOW TO USE

1. cd to the directory that contains this folder.
   Install Cookiecutter, run the template, and follow the prompts:

   ```bash
   cookiecutter cookiecutter-overleaf
   ```

2. Push to GitHub:
   ```bash
   git remote add origin git@github.com:yourusername/repo_name.git
   git push -u origin main
   ```

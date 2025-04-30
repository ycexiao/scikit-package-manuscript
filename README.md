Here's the cookiecutter for creating an Overleaf GitHub repository.

Currently, it generates the repo name, paper title, and one author name based on the input provided.

The template uses source files from IUCr LaTeX macro package (`iucr.bst`, `iucrit.bst`, `iucrjournals.cls`).

Please refer to https://github.com/Billingegroup/latex-headers for updates for
`cmds_general.tex`, `cmds_programs.tex`, and `packages.tex`.

Please check zotero for the most up-to-date bibliographies:`bg-pdf-standards.bib` and `billinge-group-bib.bib`.

# HOW TO USE

1. cd to the directory that contains this folder.
   Install Cookiecutter, run the template, and follow the prompts:

   ```bash
   cookiecutter cookiecutter-overleaf # assumes the template is in your current directory
   python cookiecutter-overleaf/post_gen_project.py # copies the required .bib and .tex files
   ```

2. Push to GitHub if desired:
   ```bash
   git remote add origin git@github.com:yourusername/my_paper.git
   git push -u origin main
   ```

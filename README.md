This is a Cookiecutter template used in `scikit-package` project to create a configured manuscript folder. Please visit the latest developments and the official documentation [here](https://scikit-package.github.io/scikit-package/).

# Features:

- Auto-generates the repository name, paper title, and one author name.
- Provides the IUCR LaTeX template (`iucr.bst`, `iucrit.bst`, `iucrjournals.cls`, `fig1.png`).
- Includes a [default LaTeX repository](https://github.com/Billingegroup/latex-headers) with dynamically generated files: `cmds-general.tex`, `cmds-programs.tex`, and `packages.tex`.

# HOW TO USE

Install `scikit-pacakge` in the environment and follow the prompts:

```bash
conda create -n skpkg-env scikit-package
conda install skpkg-env
package create manuscript
```

For a full tutorial, please see [official documentation](https://scikit-package.github.io/scikit-package/).

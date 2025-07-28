This is a Cookiecutter template used in `scikit-package` project to create a configured manuscript folder. Please visit the latest developments and the official documentation [here](https://scikit-package.github.io/scikit-package/).

# Features:

- Auto-generates the repository name, paper title, and one author name.
- Provides the an empty `article` template by default.
- Includes a [default LaTeX repository](https://github.com/Billingegroup/latex-headers) with dynamically generated files: `cmds-general.tex`, `cmds-programs.tex`, and `packages.tex`.

Additional templates are available, for example, the IUCR LaTeX template (`iucr.bst`, `iucrit.bst`, `iucrjournals.cls`, `fig1.png`). If there is an additional template that you would like to add, please make a PR with this addition to this repository. If you are not familiar with GitHub workflows, please reach out to us with the files and we can do that for you.

# HOW TO USE

Install `scikit-pacakge` in the environment and follow the prompts:

```bash
conda create -n skpkg-env scikit-package
conda install skpkg-env
package create manuscript
```

For a full tutorial, please see [official documentation](https://scikit-package.github.io/scikit-package/).

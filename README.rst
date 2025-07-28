This is a ``cookiecutter`` template used in ``scikit-package`` to initialize a latex manuscript project. The use of the template is described in the main ``scikit-package`` documentation. Please visit the latest developments and the official documentation `here <https://scikit-package.github.io/scikit-package/>`_.

This template can be applied by running the command ``package create manuscript``. After running the command, a user-configurable set of latex files will be created on the filesystem. These files can include user-defined and maintained commands and bibliographies that may be converted into a git repository for archiving on ``GitHub`` or ``GitLab`` and uploaded to ``Overleaf``.

Features
========

- Auto-generates the project name, paper title, and one author name.
- Provides the an ``article`` template by default.
- Includes a `default LaTeX project <https://github.com/Billingegroup/latex-headers>`_ with dynamically generated files: ``usepackages.txt`` and ``newcommands.txt``.

Additional templates are available, for example, the IUCr LaTeX template (``iucr.bst``, ``iucrit.bst``, ``iucrjournals.cls``, ``fig1.png``). If there is an additional template that you would like to add, please make a PR with this addition to this repository. If you are not familiar with ``GitHub workflows``, please reach out to us with the files and we can do that for you.

HOW TO USE
==========

Install ``scikit-pacakge`` in the environment, run  ``package create manuscript`` command, and follow the prompts.

.. code:: bash

    conda create -n skpkg scikit-package
    conda activate skpkg
    package create manuscript
    # follow the prompts

For a full tutorial, please see `official documentation <https://scikit-package.github.io/scikit-package/>`_.

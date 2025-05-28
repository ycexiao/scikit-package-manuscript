;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "manuscript"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("iucrjournals" "")))
   (TeX-run-style-hooks
    "latex2e"
    "packages"
    "cmds_general"
    "cmds_programs"
    "iucrjournals"
    "iucrjournals10")
   (LaTeX-add-labels
    "fig:figure1")
   (LaTeX-add-bibliographies
    "bg-pdf-standards"
    " billinge-group-bib"
    " {{ cookiecutter.project_slug }}"))
 :latex)


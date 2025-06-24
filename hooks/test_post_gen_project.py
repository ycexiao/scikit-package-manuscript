# C1: a repo url. Expect return "url"
# C2: a local path. Expect return "local".
# C3: None. Expect return "None".
def test_get_input_type():
    pass


# C1: a repo url.
#   Expect all files are copied and all copied files name are returned.
def test_copy_files_from_url():
    pass


# C1: an not existing url. Expect FileNotFoundError.
def test_copy_files_from_url_bad():
    pass


# C1: a directory path.
#   Expect all files are copied and all copied files name are returned.
def test_copy_files_from_local():
    pass


# C1: a not existing directory path. Expect return FileNotFoundError.
def test_copy_files_from_local_bad():
    pass


# C1: a header file. Expect return "header"
# C2: a bib file. Expect return "bib"
# C3: another file. Expect return "other"
def test_get_file_type():
    pass


# C1: a keyword like "usepackage" and the content.
#   Expect all lines containing the keyword and other content are returned.
def test_extract_lines():
    pass


# C1: lines to be inserted, content,
#   location keyword like "begin{document}" and method "below" or "above".
#   Expect lines are inserted into the content "below" or "above"
#   the first line containing the keyword.
def test_insert_lines():
    pass


# C1: a existing template name.
#   Expect all files in the template are copied to the project_dir
def test_copy_journal_template():
    pass


# C1: a non existing template name. Expect FileNotFoundError.
def test_copy_journal_template_bad():
    pass

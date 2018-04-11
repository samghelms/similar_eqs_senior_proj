import re

def replace(se):
    clean = se.str.replace(r'\\\\begin{equation}', "")\
        .str.replace(r'\\\\end{equation}', "")
    # clean = clean.str.replace('[]\\n', "").str.replace('\\t', "")
    newline_pat = r"(?<!\\)\\n"
    tab_pat = r"(?<!\\)\\t"
    clean = clean.str.replace(newline_pat, '').str.replace(tab_pat, '')
    # clean = clean.str.replace(r"\\\\", r"\\")
    clean = clean.str.replace(r"{align[A-Za-z]{1,}}", r"{aligned}")
    return clean

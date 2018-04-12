import re


def replace(str, newline_pat = r"(?<!\\)\\n", tab_pat = r"(?<!\\)\\t"):
    clean = str.replace(r'\\\\begin{equation}', "")
    clean = clean.replace(r'\\\\end{equation}', "")
    # clean = clean.str.replace('[]\\n', "").str.replace('\\t', "")
    clean = clean.replace(newline_pat, '')
    clean = clean.replace(tab_pat, '')
    # clean = clean.str.replace(r"\\\\", r"\\")
    clean = clean.replace(r"{align[A-Za-z]{1,}}", r"{aligned}")
    return clean

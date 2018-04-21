import re


def replace(str, newline_pat = r"(?<!\\)\\n", tab_pat = r"(?<!\\)\\t"):
    clean = str.replace(r'\\begin{equation}', "")
    clean = clean.replace(r'\\end{equation}', "")
    # clean = clean.str.replace('[]\\n', "").str.replace('\\t', "")
    clean = re.sub(newline_pat, '', clean)
    clean = re.sub(tab_pat, '', clean)
    # clean = clean.str.replace(r"\\\\", r"\\")
    clean = re.sub(r"{align[A-Za-z]{1,}}", r"{aligned}", clean)
    return clean

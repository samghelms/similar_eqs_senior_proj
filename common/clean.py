import re


def replace(str, newline_pat = r"(?<!\\)\n", tab_pat = r"(?<!\\)\t"):
	# not all begin and end tags are bad: consider \\begin{pmatrix}
    clean = str.replace('\\begin{equation}', "")
    clean = clean.replace('\\end{equation}', "")
    # clean = clean.str.replace('[]\\n', "").str.replace('\\t', "")
    # clean = re.sub(newline_pat, '', clean)
    # clean = re.sub(tab_pat, '', clean)
    # clean = clean.str.replace(r"\\\\", r"\\")
    # clean = clean.replace('\\\\', '\\')
    clean = re.sub(r"{align[A-Za-z]{1,}}", r"{aligned}", clean)
    return clean

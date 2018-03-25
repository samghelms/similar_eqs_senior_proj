

def replace(se):
    clean = se.str.replace(r'\\\\begin{equation}', "")\
        .str.replace(r'\\\\end{equation}', "")
    # clean = clean.str.replace(r'\\n', "").str.replace(r'\\t', "")
    clean = clean.str.replace(r"\\\\", r"\\")
    clean = clean.str.replace(r"{align[A-Za-z]{1,}}", r"{aligned}")
    return clean

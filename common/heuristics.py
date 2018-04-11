import re


def split_high_level_eqs(s, split_chars=r'='):
    """@params: s: tuple of strings
        @returns tuple of strings split on equals"""
    dep_depth = 0
    prev_idx = 0
    ret = []
    i = 0
    l_dep_chars = r"{[(<"
    r_dep_chars = r"})]>"
    for c in s:
        if c in l_dep_chars:
            dep_depth += 1
        elif c in r_dep_chars:
            dep_depth -= 1
        elif c in split_chars:
            if dep_depth == 0:
                ret.append(s[prev_idx:i])
                prev_idx = i + 1
        i += 1
    if (prev_idx < i):
        ret.append(s[prev_idx:])
    if(dep_depth != 0):
        return None

    return ret


def high_level_eq_test(s):
    v = split_high_level_eqs(s)
    if v is None:
        return False
    if len(split_high_level_eqs(s)) > 1:
        return True
    return False


def has_op(s):
    """ @param li: list of strings
        @returns list of booleans that encodes whether a string in the list contains a
                 operator (+-*,/, etc.) at a high level (not within {})"""
    # others = [r'\dots', 'matrix', 'pmatrix', 'array']
    if s is None or len(s.strip()) == 0:
        return False
    ops = [r"\+", r'-', r"\\pmod", r"\\bmod", r"\\frac", r"\\tfrac",
               r"\\dfrac", r"\\times", r"\\sqrt", r'\\int', r'\\land',
               r'\\lor', r'\\in', r'\\subset', r'\\iiint', r'\\bigcup',
              r'\\bigsqcup', r'\\bigoplus', r'\\prod', r'\\bigotimes',
              r'\\bigcap', r'\\bigvee', r'\\oint', r'\\coprod', r'\\iint'
              r'\\idotsint', r'\\bigwedge', r'\\cfrac']

    regexp = lambda x: re.compile(x + r"(?![A-Za-z])")
    test_inner = lambda c, x: bool(re.search(regexp(c), x))
    test = lambda x: any([test_inner(c, x) for c in ops if x is not None])
    # get rid of leading negatives
    if s.strip()[0] == '-':
        return test(s.strip()[1:])
    return test(s)

def high_level_only(s):
    """@ params s: str
       @ returns sring with only high level chars left (not
       within {})"""
    dep_depth = 0
    prev_idx = 0
    curr = ""
    prev_c = "x"
    supsub = "^_"
    for c in s:
        if c in r"{[(<":
            dep_depth += 1
        elif c in r"})]>":
            dep_depth -= 1
        else:
            if dep_depth == 0 and prev_c not in supsub\
                              and c not in supsub:
                curr += c
        prev_c = c
    if(dep_depth != 0):
        return None

    return curr


def test_for_suitable(li):
    if li == None:
        return None
    ret = ([x for x in li if has_op(high_level_only(x))])
    if len(ret) < 2:
        return None
    return ret

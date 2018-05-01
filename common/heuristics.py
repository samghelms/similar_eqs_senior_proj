import re

l_dep_chars = ['{', '[', '(', '<', '\\langle', 
               '\\{', '\\lfloor', '\\lceil']
r_dep_chars = ['}', ')', ']', '>', '\\rangle'
               '\\}', '\\rfloor', '\\rceil']


def apply_split(token, all_tokens, index, prev_index):
    new_prev_idx = index
    new_prev_idx += 1
    if token == '\\':
        if index < len(all_tokens) - 1 and all_tokens[index + 1] == '\\':
            new_prev_idx += 1
    ret = all_tokens[prev_index:index]
    return new_prev_idx, ret

        # if all_tokens[index-1] == '\\':
def split_check(token, all_tokens, index):
    if token == '\\':
        if index < len(all_tokens) - 1:
            if all_tokens[index + 1] == '\\':
                return True
    elif token == ',':
        return True
    elif token == ';':
        return True
    return False

def split_exprs(tokens):
    """@params: tokens: a list of tokens
        @returns a list of lists of tokens from seperate subexpressions.
        Deals with, for example, aligned equations where the first line is
        something like f = x + y and the second line is g = 6 + i, which should
        not be considered aligned.

        Notes: (1) You need to treat newline like a macro because of the way
                   tokenize parses. This means encoding it as '\\n'"""
    dep_depth = 0
    prev_idx = 0
    ret = []
    i = 0
    for t in tokens:
        if t in l_dep_chars:
            dep_depth += 1
        elif t in r_dep_chars:
            dep_depth -= 1
        elif split_check(t, tokens, i):
            if dep_depth == 0:
                prev_idx, app = apply_split(t, tokens, i, prev_idx)
                ret.append(app)
        i += 1
    if (prev_idx < i):
        app = tokens[prev_idx:]
        ret.append(app)
    if(dep_depth != 0):
        return None

    return ret

def split_high_level_eqs(tokens, split_chars=['=', ',', ';', '\\equiv']):
    """@params: tokens: list of strings
        @returns list of lists of strings split on equals"""
    dep_depth = 0
    prev_idx = 0
    ret = []
    i = 0
    for t in tokens:
        if t in l_dep_chars:
            dep_depth += 1
        elif t in r_dep_chars:
            dep_depth -= 1
        elif t in split_chars:
            if dep_depth == 0:
                ret.append(tokens[prev_idx:i])
                prev_idx = i + 1
        i += 1
    if (prev_idx < i):
        ret.append(tokens[prev_idx:])
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
        if c in l_dep_chars:
            dep_depth += 1
        elif c in r_dep_chars:
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


def filter_tokens(tokens, 
                  tokens_to_filter=['\\begin', '\\end', '\\mbox',
                                    '\\text', '\\textrm',
                                    '\\textstyle', '\\hbox'],
                  prefixes_to_filter=['\\text', '\\math', '\\box']):
    in_subexpr = False
    filtered = []
    for i, t in enumerate(tokens):
        if in_subexpr is True:
            if t == '}':
                in_subexpr = False
        elif t in tokens_to_filter or any([pref in t
                                           for pref in prefixes_to_filter]):
            if i < len(tokens):
                if tokens[i+1] == '{':
                    in_subexpr = True
        else:
            filtered.append(t)
    return filtered

import re
import json
# operators listed below taken from wikipedia articles about math in latex
default_ops = [r"\+", r'-', r"\\pmod", r"\\bmod", r"\\frac", r"\\tfrac",
               r"\\dfrac", r"\\times", r"\\sqrt", r'\\int', r'\\land',
               r'\\lor', r'\\in', r'\\subset', r'\\iiint', r'\\bigcup',
              r'\\bigsqcup', r'\\bigoplus', r'\\prod', r'\\bigotimes',
              r'\\bigcap', r'\\bigvee', r'\\oint', r'\\coprod', r'\\iint'
              r'\\idotsint', r'\\bigwedge', r'\\cfrac'] + json.load(open('data/operator_list.json'))

def count_ops(tokens, 
           ops=default_ops,
           l_dep_tokens=json.load(open('data/open_list.json')) + ['{'], 
           r_dep_tokens=json.load(open('data/close_list.json')) + ['}'],):
    """ @param tokens: A list of tokens
        @param ops: list of operators. Default from KaTeX and my research online.
        @returns list of booleans that encodes whether a string in the list contains a
                 operator (+-*,/, etc.) at a high level (not within {})"""
    depth = 0
    ops_ct = 0
    # we don't care about ops at either end
    for t in tokens[1:len(tokens) - 1]:
        if t in l_dep_tokens:
            depth +=1
        elif t in r_dep_tokens:
            depth -= 1
        elif depth == 0:
            if t in ops:
                ops_ct += 1
    return ops_ct

def isnumber(token):
    periods = 0
    for t in token:
        if not t.isnumeric() and t != '.':
            return False
        if t == '.':
            periods += 1
            if periods > 1:
                return False

    return True


def count_vars(tokens,
           variables=json.load(open('data/vars_list.json'))+json.load(open('data/symbols.json')),
           l_dep_tokens=json.load(open('data/open_list.json')) + ['{'], 
           r_dep_tokens=json.load(open('data/close_list.json')) + ['}'],):
    """ @param tokens: A list of tokens
        @param ops: list of operators. Default from KaTeX and my research online.
        @returns list of booleans that encodes whether a string in the list contains a
                 operator (+-*,/, etc.) at a high level (not within {})"""
    depth = 0
    vars_ct = 0
    for i, t in enumerate(tokens):
        if t in l_dep_tokens:
            depth +=1
        elif t in r_dep_tokens:
            depth -= 1
        elif depth == 0:
            if i > 0 and tokens[i-1] in '^_':
                continue
            if t in variables:
                vars_ct += 1
            elif isnumber(t):
                vars_ct += 1
            elif t.isalpha():
                vars_ct += 1
    return vars_ct

def suitable(tokens):
    """Tests if a list of tokens is a suitable equation (more than one operator and variable)"""
    ops_ct = count_ops(tokens)
    vars_ct = count_vars(tokens)

    return ops_ct >= 1 and vars_ct >= 2

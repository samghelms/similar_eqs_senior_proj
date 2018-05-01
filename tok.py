"""Functions to tokenize equations.
Main interfaces are `tokenize` and `fix macros`. Combined into `tokenize_and_fix_macros`.
"""
import json
import re

def _break_rule(c, state):
    if state == 'macro': return 'append'
    elif state == 'new_macro': return 'new'
    elif state == 'new_num': return 'new'
    elif state == 'num': return 'append'
    elif state == 'var_or_op': return 'new'
    elif state == 'spacing': return 'append'
    elif state == 'newline': return 'append'
    elif state == 'num': return 'append'
    elif state == 'num_w_decimal': return 'append'
    return 'none'


def _update_state(c, state, spacing_chars=',;'):
    if c == '\\' and state not in ['macro', 'new_macro']: return 'new_macro'
    if state in ['macro', 'new_macro']:
        if c.isalpha():
            return 'macro'
        elif c == '\\' and state == 'new_macro':
            return 'newline'
        elif c == '\\' and state == 'macro':
            return 'new_macro'
        elif c in spacing_chars and state == 'new_macro':
            return 'spacing'
    if re.match(r'\s', c): return 'space'
    if c == '.':
        if state in ['num', 'new_num']: 
            return 'num_w_decimal'
        # deal with decimals like .05 (no leading num)
        else:
            return 'new_num'
    if c.isdigit():
        if state == 'num_w_decimal':
            return 'num_w_decimal'
        if state in ['num', 'new_num']:
            return 'num'
        else:
            return 'new_num'

    return 'var_or_op'

def tokenize(s, stop_words=['\n', '\t', 'START']):
    """Tokenizer using a finite state machine.
    @ param s: input string of math to tokenize
    @ param stop_words: list of tokens to drop when tokenizing 
      (note, this can be done later as well)
    @ returns a list of tokens
    Notes:
    (1) treats instances of '\\' (the latex line break in math)
    as macros. Ignore newlines, since latex will also ignore the character.
    (2) The weird notation for newlines in stopwords comes from having to
        parse latex macros like '\nabla' """
    cur = 'START'
    ret = []
    state = 'start'
    for c in s:
        # print(c)
        state = _update_state(c, state)
        # print(state)
        decision = _break_rule(c, state)
        # print(decision)
        if decision == 'new':
            if cur not in stop_words:
                ret.append(cur)
            cur = c
        elif decision == 'append':
            cur += c
    if cur != '' and cur not in stop_words:
        ret.append(cur)
    return ret

class CouldNotFindError(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

def _find_macro(macro_text, macro_dict):
    if macro_text not in macro_dict:
        found = False
        end = len(macro_text) - 1
        while end > 1:
            longest_subseq = macro_text[0:end]
            if longest_subseq in macro_dict:
                found = True
                return [longest_subseq, macro_text[end:]]
            end -= 1
        if not found:
            raise CouldNotFindError(('could not find a macro matching ', macro_text))
    return [macro_text]

def load_macros():
    macro_sources = ['data/all_symbols.json', 'data/inside_set_indicators.json',
                     'data/operator_list.json',
                     'data/punctuation_list.json', 'data/close_list.json',
                     'data/open_list.json', 'data/spacing_list.json',
                     'data/relations_list.json', 'data/functions.json', 
                     'data/macros.json', 'data/symbols.json']
    all_macros = {}
    for s in macro_sources:
        f = open(s)
        symbls = json.load(f)
        for s in symbls:
            all_macros[s.strip()] = 1
    return all_macros

def fix_macros(tokens, macro_dict=load_macros(), debug=False):
    """Runs through a list of tokens and picks out
    and splits accidental merges like \gammadx
    @ param tokens: list of tokens in need of correction
    @ param macro_dict: a dictionary of macros to check against
      (note, this can be done later as well). Default macros from around the web and katex.
    @ returns a list of corrected tokens
    Notes: raises a CouldNotFindError if it cannot find one of the tokens in the macro_dict
    """
    return_toks = []
    in_macro = False
    last_macro_idx = 0
    for i, tok in enumerate(tokens):
        # filter to get macro tokens
        if tok[0] == '\\':
            if debug is True:
                print("finding: " + tok)
            tok = _find_macro(tok, macro_dict)
            if debug is True:
                print("found: ")
                print(tok)
        else: tok = [tok]
        return_toks += tok
    return return_toks

def tokenize_and_fix_macros(s):
    """Interface combining the two functions above.
    Tokenizes an input string and then fixes macros.
    @ param s: input string
    @ returns a list of tokens with fixed macros
    """
    tokens = tokenize(s)
    return fix_macros(tokens)

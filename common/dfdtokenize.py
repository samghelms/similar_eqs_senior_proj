import re

def break_rule(c, state):
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


def update_state(c, state, spacing_chars=',;'):
    if c == '\\' and state not in 'macro': return 'new_macro'
    if state in ['macro', 'new_macro']:
        if re.match('[A-Za-z]', c):
            return 'macro'
        elif c == '\\' and state == 'new_macro':
            return 'newline'
        elif c == '\\' and state == 'macro':
            return 'new_macro'
        elif c in spacing_chars and state == 'new_macro':
            return 'spacing'
    if re.match('\s', c): return 'space'
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

class CouldNotFindError(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

def find_macro(macro_text, macro_trie):
    if macro_text not in macro_trie:
        found = False
        end = len(macro_text) - 1
        while end > 1:
            longest_subseq = macro_text[0:end]
            if longest_subseq in macro_trie:
                found = True
                return longest_subseq+" "+macro_text[end:]
            end -= 1
        if not found:
            raise CouldNotFindError(('could not find a macro matching ', macro_text))
    return macro_text

def fix_macros(string, macro_trie, debug=False):
    """Runs through a list of tokens and picks out
    and splits accidental merges like \gammadx"""
    return_string = []
    in_macro = False
    macro_text = '\\'
    last_macro_idx = 0
    for i, c in enumerate(string):
        # filter to get macro tokens
        if c == '\\' and not in_macro:
            in_macro = True
            return_string.append(string[last_macro_idx:i])
        elif in_macro:
            if c.isalpha():
                macro_text += c
            else:
                # check for escapes
                if len(macro_text) > 1:
                    if debug is True:
                        print("finding: " + macro_text)
                    macro = find_macro(macro_text, macro_trie)
                    if debug is True:
                        print("found: "+macro)
                    return_string.append(macro)
                    last_macro_idx = i
                in_macro = True if c == '\\' else False
                macro_text = '\\'
            if len(string) - 1 == i and in_macro == True:
                if len(macro_text) > 1:
                    if debug is True:
                        print("finding (final): " + macro_text)
                    macro = find_macro(macro_text, macro_trie)
                    return_string.append(macro)
                    last_macro_idx = i + 1

    if last_macro_idx < len(string):
        # space it in case you are adding to a macro
        return_string.append(" "+string[last_macro_idx:])
    return "".join(return_string)


def tokenize(s, stop_words=['\n', '\t', 'START']):
    """Tokenizer using a finite state machine.
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
        state = update_state(c, state)
        # print(state)
        decision = break_rule(c, state)
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
